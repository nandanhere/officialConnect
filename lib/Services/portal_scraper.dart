import 'dart:async';
import 'package:html/parser.dart' as parser;
import 'package:html/dom.dart';
import 'package:official_connect/Services/portal_session.dart';

/// Parses the portal's authenticated HTML into the JSON shape used by the
/// existing Flutter models. Requests are made with the WebView session cookie.
class PortalScraper {
  PortalScraper(this.session, {this.onProgress});

  final PortalSession session;
  final void Function(String stage)? onProgress;

  Future<Map<String, dynamic>> scrapeAll() async {
    final syncWatch = Stopwatch()..start();
    final sections = <String, dynamic>{};
    void recordSection(
      String name,
      String status, {
      int count = 0,
      int attempted = 0,
      int failed = 0,
      int durationMs = 0,
    }) {
      sections[name] = {
        'status': status,
        'count': count,
        'attempted': attempted,
        'failed': failed,
        'duration_ms': durationMs,
      };
    }

    onProgress?.call('Reading your profile');
    // A previous sync normally leaves the browser on result history. Always
    // return to the signed dashboard so refreshes rediscover every current
    // attendance, CIE, fee and history link before scraping.
    final dashboard = await session.navigateAndRead(PortalSession.dashboardUri);
    final document = parser.parse(dashboard);
    final result = <String, dynamic>{};
    _parseStudentSummary(document, result);
    _parseFees(document, result);
    final profileValues = [
      result['name'],
      result['courseSmall'],
      result['sem'],
    ];
    final profileCount = profileValues
        .where((value) => value?.toString().trim().isNotEmpty == true)
        .length;
    recordSection(
      'profile',
      profileCount == profileValues.length
          ? 'ok'
          : profileCount == 0
          ? 'error'
          : 'partial',
      count: profileCount,
      attempted: profileValues.length,
      failed: profileValues.length - profileCount,
    );

    final links = document
        .querySelectorAll('a[href]')
        .map((e) => e.attributes['href'] ?? '')
        .where((href) => href.isNotEmpty)
        .map((href) => PortalSession.loginUri.resolve(href))
        .toSet();
    final attendanceLinks = links
        .where((u) => u.toString().contains('attendencelist'))
        .toList();
    final marksLinks = links
        .where((u) => u.toString().contains('ciedetails'))
        .toList();

    final attendance = <Map<String, dynamic>>[];
    var attendanceFailures = 0;
    var invalidAttendancePages = 0;
    final attendanceWatch = Stopwatch()..start();
    if (attendanceLinks.isNotEmpty) {
      onProgress?.call('Syncing attendance');
    }
    for (final uri in attendanceLinks) {
      try {
        final attendanceDocument = parser.parse(
          await session.navigateAndRead(uri),
        );
        final item = _parseAttendance(attendanceDocument);
        if (_hasCourseIdentity('${item['code']} ${item['name']}') &&
            _hasAttendanceStructure(attendanceDocument)) {
          attendance.add(item);
        } else {
          invalidAttendancePages++;
        }
      } catch (_) {
        attendanceFailures++;
      }
    }
    attendanceWatch.stop();
    // The current portal appends one intentionally blank link. Ignore that
    // shell when valid courses exist, but flag empty/extra invalid pages.
    attendanceFailures += attendance.isEmpty
        ? invalidAttendancePages
        : (invalidAttendancePages - 1).clamp(0, invalidAttendancePages);
    result['attendance'] = attendance;
    recordSection(
      'attendance',
      _sectionStatus(
        attendanceLinks.length,
        attendance.length,
        attendanceFailures,
      ),
      count: attendance.length,
      attempted: attendanceLinks.length,
      failed: attendanceFailures,
      durationMs: attendanceWatch.elapsedMilliseconds,
    );

    final marks = <Map<String, dynamic>>[];
    var marksFailures = 0;
    var invalidMarksPages = 0;
    final marksWatch = Stopwatch()..start();
    if (marksLinks.isNotEmpty) onProgress?.call('Syncing internal marks');
    for (final uri in marksLinks) {
      try {
        final marksDocument = parser.parse(await session.navigateAndRead(uri));
        final item = _parseMarks(marksDocument);
        if (_hasCourseIdentity(item['name'].toString()) &&
            marksDocument.querySelectorAll('tr.odd td').isNotEmpty) {
          marks.add(item);
        } else {
          invalidMarksPages++;
        }
      } catch (_) {
        marksFailures++;
      }
    }
    marksWatch.stop();
    marksFailures += marks.isEmpty
        ? invalidMarksPages
        : (invalidMarksPages - 1).clamp(0, invalidMarksPages);
    // The dashboard can include a trailing empty attendance/CIE link. It
    // resolves to a valid page shell, but has no course identity and must not
    // become a blank subject card in the native UI.
    result['marks'] = marks;
    recordSection(
      'marks',
      _sectionStatus(marksLinks.length, marks.length, marksFailures),
      count: marks.length,
      attempted: marksLinks.length,
      failed: marksFailures,
      durationMs: marksWatch.elapsedMilliseconds,
    );

    Uri matchingLink(String fragment, Uri fallback) => links.firstWhere(
      (uri) => uri.toString().contains(fragment),
      orElse: () => fallback,
    );
    final resultLink = matchingLink(
      'com_history',
      Uri.parse(
        'https://parents.msrit.edu/newparents/index.php?option=com_history&task=getResult',
      ),
    );
    // The portal's result endpoint is not ready immediately after login. Visit
    // the lighter authenticated pages first so result history can initialize
    // in the background instead of waiting through a guaranteed empty shell.
    onProgress?.call('Syncing proctor updates');
    final proctorWatch = Stopwatch()..start();
    Document? proctorDocument;
    try {
      proctorDocument = parser.parse(
        await session.navigateAndRead(
          matchingLink(
            'task=observation',
            Uri.parse(
              'https://parents.msrit.edu/newparents/index.php?option=com_studentdashboard&controller=studentdashboard&task=observation',
            ),
          ),
        ),
      );
      result['proctorship'] = _parseProctor(proctorDocument);
      recordSection(
        'proctor',
        'ok',
        count: 1,
        attempted: 1,
        durationMs: proctorWatch.elapsedMilliseconds,
      );
    } catch (_) {
      result['proctorship'] = <dynamic>[];
      recordSection(
        'proctor',
        'error',
        attempted: 1,
        failed: 1,
        durationMs: proctorWatch.elapsedMilliseconds,
      );
    }

    final feeLink = links.where(
      (uri) => uri.queryParameters['option'] == 'com_fee',
    );
    if (feeLink.isNotEmpty) {
      onProgress?.call('Syncing fee history');
      final feeWatch = Stopwatch()..start();
      try {
        final feeDocument = parser.parse(
          await session.navigateAndRead(feeLink.first),
        );
        _parseFees(feeDocument, result);
        final feeCount = (result['fees'] as List?)?.length ?? 0;
        recordSection(
          'fees',
          feeCount == 0 ? 'empty' : 'ok',
          count: feeCount,
          attempted: 1,
          durationMs: feeWatch.elapsedMilliseconds,
        );
      } catch (_) {
        final dashboardFeeCount = (result['fees'] as List?)?.length ?? 0;
        recordSection(
          'fees',
          dashboardFeeCount > 0 ? 'partial' : 'error',
          count: dashboardFeeCount,
          attempted: 1,
          failed: 1,
          durationMs: feeWatch.elapsedMilliseconds,
        );
      }
    } else {
      recordSection(
        'fees',
        (result['fees'] as List?)?.isNotEmpty == true ? 'ok' : 'empty',
        count: (result['fees'] as List?)?.length ?? 0,
      );
    }

    onProgress?.call('Syncing semester results');
    final resultsWatch = Stopwatch()..start();
    Document? resultsDocument;
    var resultAttempts = 0;
    try {
      resultAttempts++;
      resultsDocument = parser.parse(await session.navigateAndRead(resultLink));
      result['prevResults'] = _parsePreviousResults(resultsDocument);
      // Keep one fast retry for unusually slow portal sessions.
      if ((result['prevResults'] as List).isEmpty) {
        await Future<void>.delayed(const Duration(milliseconds: 500));
        resultAttempts++;
        resultsDocument = parser.parse(
          await session.navigateAndRead(resultLink),
        );
        result['prevResults'] = _parsePreviousResults(resultsDocument);
      }
      final count = (result['prevResults'] as List).length;
      recordSection(
        'results',
        count == 0 ? 'empty' : 'ok',
        count: count,
        attempted: resultAttempts,
        durationMs: resultsWatch.elapsedMilliseconds,
      );
    } catch (_) {
      result['prevResults'] = <dynamic>[];
      recordSection(
        'results',
        'error',
        attempted: resultAttempts,
        failed: 1,
        durationMs: resultsWatch.elapsedMilliseconds,
      );
    }
    syncWatch.stop();
    final statuses = sections.values
        .whereType<Map>()
        .map((section) => section['status'])
        .toList();
    result['_sync'] = {
      'version': 1,
      'outcome':
          statuses.any((status) => status == 'error' || status == 'partial')
          ? 'partial'
          : 'complete',
      'duration_ms': syncWatch.elapsedMilliseconds,
      'sections': sections,
    };
    assert(() {
      // ignore: avoid_print
      print(
        'Portal detail pages: '
        'resultTables=${resultsDocument?.querySelectorAll('table.res-table').length ?? 0}, '
        'proctorRows=${proctorDocument?.querySelectorAll('table.cn-res-table tbody tr').length ?? 0}',
      );
      return true;
    }());
    return result;
  }

  String _sectionStatus(int attempted, int count, int failed) {
    if (failed > 0 && count > 0) return 'partial';
    if (failed > 0) return 'error';
    if (attempted == 0 || count == 0) return 'empty';
    return 'ok';
  }

  bool _hasCourseIdentity(String value) =>
      value.replaceAll(RegExp(r'[\s()\-]'), '').isNotEmpty;

  bool _hasAttendanceStructure(Document document) =>
      RegExp(
        r'\[[^\]]*\]',
      ).allMatches(document.querySelector('.cn-legend')?.text ?? '').length >=
      2;

  void _parseStudentSummary(Document doc, Map<String, dynamic> out) {
    final name = doc.querySelector('.cn-stu-data1 h3')?.text.trim();
    if (name != null && name.isNotEmpty) out['name'] = name;
    final summary =
        doc
            .querySelector('.cn-stu-data p')
            ?.text
            .split(',')
            .map((x) => x.trim())
            .toList() ??
        [];
    if (summary.length >= 3) {
      out['courseSmall'] = summary[0];
      out['sem'] = summary[1];
      out['sec'] = summary[2];
    }
    final legend = doc
        .querySelectorAll('.cn-legend span')
        .map((e) => e.text.trim())
        .toList();
    if (legend.length >= 2) {
      out['earned'] = legend[0].split(' ').first;
      out['to_earn'] = legend[1].split(' ').first;
    }
    final details = doc.querySelectorAll('.cn-basic-details table tr');
    for (final row in details) {
      final cells = row.querySelectorAll('td');
      if (cells.length >= 2) out[cells[0].text.trim()] = cells[1].text.trim();
    }
  }

  void _parseFees(Document doc, Map<String, dynamic> out) {
    final fees = <Map<String, String>>[];
    final refunds = <Map<String, String>>[];
    for (final table in doc.querySelectorAll('table.cn-pay-table')) {
      final headers = table
          .querySelectorAll('thead th, thead td')
          .map((e) => e.text.replaceAll(RegExp(r'\s+'), ' ').trim())
          .toList();
      final target =
          (table.querySelector('caption')?.text.trim() == 'Refund Details')
          ? refunds
          : fees;
      for (final row in table.querySelectorAll('tbody tr')) {
        final values = row
            .querySelectorAll('td')
            .map((e) => e.text.trim())
            .toList();
        final parsed = <String, String>{
          'Academic Year': '',
          'Amount Paid': '',
          'Challan No': '',
          'Cheque/DD No': '',
          'Date': '',
          'Mode': '',
          'Paid for Year': '',
          'Pay At': '',
          // The current portal no longer emits this legacy column, but the
          // existing native model still expects a non-null value.
          'Receipt': '',
          for (var i = 0; i < values.length && i < headers.length; i++)
            headers[i]: values[i],
        };
        target.add(parsed);
      }
    }
    out['fees'] = fees;
    out['refunds'] = refunds;
  }

  Map<String, dynamic> _parseAttendance(Document doc) {
    final details = doc
        .querySelectorAll('h3.md-card-head-text span')
        .map((e) => e.text.trim())
        .toList();
    final title = details.isNotEmpty
        ? details.first.split(RegExp(r'\s*-\s*'))
        : <String>[];
    final legend = doc.querySelector('.cn-legend')?.text ?? '';
    final nums = RegExp(r'\[([^\]]*)\]')
        .allMatches(legend)
        .map((m) => m.group(1)!.isEmpty ? '0' : m.group(1)!)
        .toList();
    final present = nums.isNotEmpty ? nums[0] : '0';
    final absent = nums.length > 1 ? nums[1] : '0';
    final remaining = nums.length > 2 ? nums[2] : '0';
    final total = (int.tryParse(present) ?? 0) + (int.tryParse(absent) ?? 0);
    return {
      'code': title.isNotEmpty ? title.first.trim() : '',
      'name': title.length > 1 ? title.sublist(1).join(' - ').trim() : '',
      'teacher':
          doc.querySelector('h3.md-card-head-text')?.nodes.first.text?.trim() ??
          '',
      'present': present,
      'absent': absent,
      'remaining': remaining,
      'percentage':
          '${total == 0 ? 0 : ((int.parse(present) / total) * 100).floor()}%',
      'present_dates': _parseClassDates(
        doc.querySelector('table.cn-attend-list1'),
      ),
      'absent_dates': _parseClassDates(
        doc.querySelector('table.cn-attend-list2'),
      ),
    };
  }

  List<Map<String, String>> _parseClassDates(Element? table) =>
      table?.querySelectorAll('tbody tr').map((row) {
        final cells = row
            .querySelectorAll('td')
            .map((e) => e.text.trim())
            .toList();
        return {
          'date': cells.length > 1 ? cells[1] : '',
          'time': cells.length > 2 ? cells[2].replaceAll('TO', '-').trim() : '',
          'index': '0',
          'status': 'None',
        };
      }).toList() ??
      [];

  Map<String, dynamic> _parseMarks(Document doc) {
    final values = doc
        .querySelectorAll('tr.odd td')
        .map((e) => e.text.trim().isEmpty ? '-' : e.text.trim())
        .toList();
    final name = doc.querySelector('th[colspan="9"]')?.text.trim() ?? '';
    final averageValues = RegExp(r'"col1"\s*:\s*(\d+)')
        .allMatches(doc.querySelector('.cn-cie-stat script')?.text ?? '')
        .map((m) => m.group(1)!)
        .toList();
    const averageKeys = ['t1', 't2', 't3', 't4', 'a1', 'a2', 'a3'];
    final averages = <String, String>{for (final key in averageKeys) key: '-'};
    for (var i = 0; i < averageValues.length && i < averageKeys.length; i++) {
      averages[averageKeys[i]] = averageValues[i];
    }
    String value(int i) => i < values.length ? values[i] : '-';
    return {
      'name': name,
      't1': value(0),
      't2': value(1),
      't3': value(2),
      't4': value(3),
      'a1': value(4),
      'a2': value(5),
      'a3': value(6),
      'final cie': value(7),
      'class_average': averages,
    };
  }

  List<Map<String, dynamic>> _parsePreviousResults(
    Document doc,
  ) => doc.querySelectorAll('table.res-table').map((table) {
    final result = <String, dynamic>{
      'term':
          table
              .querySelector('caption')
              ?.nodes
              .whereType<Text>()
              .map((n) => n.data.trim())
              .where((s) => s.isNotEmpty)
              .join(' ') ??
          '',
    };
    for (final span in table.querySelectorAll('caption span')) {
      final parts = span.text.split(':');
      if (parts.length >= 2) {
        result['${parts.first.trim()}${span.text.contains('Credits') ? ' ' : ''}'] =
            parts.sublist(1).join(':').trim();
      }
    }
    result['results'] = table.querySelectorAll('tbody tr').map((row) {
      final heads = table
          .querySelectorAll('thead th')
          .map((e) => e.text.replaceAll(RegExp(r'\s+'), ' ').trim())
          .toList();
      final vals = row
          .querySelectorAll('td')
          .map((e) => e.text.trim())
          .toList();
      return <String, String>{
        for (var i = 0; i < vals.length && i < heads.length; i++)
          heads[i]: vals[i],
      };
    }).toList();
    return result;
  }).toList();

  Map<String, dynamic> _parseProctor(Document doc) => {
    'proctor_name':
        doc.querySelector('h3.md-card-head-text')?.text.trim() ?? 'No data',
    'branch': 'No data',
    'email': 'No data',
    'phone': 'No data',
    'proctorial_notes': doc.querySelectorAll('table.cn-res-table tbody tr').map(
      (row) {
        final cells = row
            .querySelectorAll('td')
            .map((e) => e.text.trim())
            .toList();
        return {
          'date': cells.isNotEmpty ? cells[0] : '',
          'sender': cells.length > 1 ? cells[1] : '',
          'desc': cells.length > 2 ? cells[2] : '',
        };
      },
    ).toList(),
  };
}
