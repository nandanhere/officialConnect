import 'dart:async';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:official_connect/Services/portal_scraper.dart';
import 'package:official_connect/Services/portal_session.dart';
import 'package:official_connect/Services/firebase_feature_flags.dart';

class _FixturePages {
  _FixturePages(this.responses, {this.throwingIds = const {}});

  final Map<String, String> responses;
  final Set<String> throwingIds;

  Future<String> navigateAndRead(Uri uri) async {
    final id = uri.queryParameters['id'];
    if (id != null && throwingIds.contains(id)) {
      throw StateError('simulated section failure');
    }
    if (uri == PortalSession.dashboardUri) return responses['dashboard']!;
    if (uri.toString().contains('attendencelist')) {
      return responses['attendance:$id']!;
    }
    if (uri.toString().contains('ciedetails')) return responses['marks:$id']!;
    if (uri.queryParameters['option'] == 'com_fee') return responses['fees']!;
    if (uri.queryParameters['task'] == 'observation') {
      return responses['proctor']!;
    }
    if (uri.queryParameters['task'] == 'timetable') {
      return responses['timetable']!;
    }
    if (uri.queryParameters['task'] == 'seating') {
      return responses['seating']!;
    }
    if (uri.queryParameters['option'] == 'com_history') {
      return responses['results']!;
    }
    throw StateError('No fixture for $uri');
  }
}

String _fixture(String name) => File('test/fixtures/$name').readAsStringSync();

void main() {
  tearDown(() => FirebaseFeatureFlags.setValuesForTesting(const {}));

  Map<String, String> fixtures() => {
    'dashboard': _fixture('dashboard_variant.html'),
    'attendance:good': _fixture('attendance_variant.html'),
    'attendance:bad': _fixture('malformed_section.html'),
    'marks:good': _fixture('marks_variant.html'),
    'marks:bad': _fixture('malformed_section.html'),
    'fees': _fixture('fees_variant.html'),
    'proctor': _fixture('proctor_variant.html'),
    'results': _fixture('results_variant.html'),
    'timetable': _fixture('timetable_variant.html'),
    'seating': _fixture('seating_variant.html'),
  };

  test('parses anonymized alternate portal layouts', () async {
    final pages = _FixturePages(fixtures());
    final result = await PortalScraper.forTesting(
      navigateAndRead: pages.navigateAndRead,
    ).scrapeAll();

    expect(result['name'], 'Test Student');
    expect(result['courseSmall'], 'B.E. ISE');
    expect((result['attendance'] as List), hasLength(1));
    expect(result['attendance'][0]['code'], 'IS701');
    expect(result['attendance'][0]['percentage'], '90%');
    expect((result['marks'] as List), hasLength(1));
    expect(result['marks'][0]['final cie'], '91');
    expect((result['fees'] as List), hasLength(1));
    expect((result['prevResults'] as List), hasLength(1));
    expect(result['prevResults'][0]['results'][0]['Grade'], 'A');
    expect((result['timetable'] as List), hasLength(2));
    expect(result['timetable'][0]['room'], 'LAB 5');
    expect((result['seating'] as List), hasLength(1));
    expect(result['seating'][0]['room'], 'AB504');
    expect(result['_sync']['sections']['timetable']['status'], 'ok');
    expect(result['_sync']['sections']['seating']['status'], 'ok');
  });

  test('one malformed section cannot blank successful sections', () async {
    final pages = _FixturePages(fixtures(), throwingIds: const {'bad'});
    final result = await PortalScraper.forTesting(
      navigateAndRead: pages.navigateAndRead,
    ).scrapeAll();

    expect(result['name'], 'Test Student');
    expect((result['attendance'] as List), hasLength(1));
    expect((result['marks'] as List), hasLength(1));
    expect((result['fees'] as List), hasLength(1));
    expect((result['prevResults'] as List), hasLength(1));
    expect(result['_sync']['outcome'], 'partial');
    expect(result['_sync']['sections']['attendance']['status'], 'partial');
    expect(result['_sync']['sections']['marks']['status'], 'partial');
    expect(
      result['_sync']['sections']['attendance']['failure_reason'],
      'unknown',
    );
  });

  test('disabled sections are skipped without blocking enabled data', () async {
    FirebaseFeatureFlags.setValuesForTesting(const {
      'scraper_attendance_enabled': false,
      'scraper_marks_enabled': false,
    });
    final pages = _FixturePages(fixtures());
    final result = await PortalScraper.forTesting(
      navigateAndRead: pages.navigateAndRead,
    ).scrapeAll();

    expect(result['attendance'], isEmpty);
    expect(result['marks'], isEmpty);
    expect(result['_sync']['sections']['attendance']['status'], 'disabled');
    expect(result['_sync']['sections']['marks']['status'], 'disabled');
    expect((result['fees'] as List), hasLength(1));
    expect((result['prevResults'] as List), hasLength(1));
  });

  test('monday timetable tables parse with their date', () async {
    final values = fixtures();
    values['timetable'] = _fixture('timetable_monday_variant.html');
    final pages = _FixturePages(values);
    final result = await PortalScraper.forTesting(
      navigateAndRead: pages.navigateAndRead,
    ).scrapeAll();

    final timetable = result['timetable'] as List;
    expect(timetable, hasLength(2));
    expect(timetable[0]['day'], 'MONDAY');
    expect(timetable[0]['date'], '2026-09-14');
    expect(result['_sync']['sections']['timetable']['status'], 'ok');
  });

  test('a hung page times out without stalling later sections', () async {
    final values = fixtures();
    final pages = _FixturePages(values);
    Future<String> hangingRead(Uri uri) {
      if (uri.queryParameters['task'] == 'timetable') {
        return Completer<String>().future;
      }
      return pages.navigateAndRead(uri);
    }

    final watch = Stopwatch()..start();
    final result = await PortalScraper.forTesting(
      navigateAndRead: hangingRead,
      pageReadTimeout: const Duration(milliseconds: 50),
    ).scrapeAll();
    watch.stop();

    expect(watch.elapsed, lessThan(const Duration(seconds: 30)));
    expect(result['_sync']['sections']['timetable']['status'], 'error');
    expect(
      result['_sync']['sections']['timetable']['failure_reason'],
      'timeout',
    );
    expect(result['_sync']['sections']['seating']['status'], 'ok');
    expect(result['_sync']['outcome'], 'partial');
  });

  test(
    'missing course links are structural failures, not empty data',
    () async {
      final values = fixtures();
      values['dashboard'] = values['dashboard']!
          .replaceAll(RegExp(r'<a href="\?task=attendencelist[^<]+</a>'), '')
          .replaceAll(RegExp(r'<a href="\?task=ciedetails[^<]+</a>'), '');
      final pages = _FixturePages(values);

      final result = await PortalScraper.forTesting(
        navigateAndRead: pages.navigateAndRead,
      ).scrapeAll();

      expect(result['_sync']['sections']['attendance']['status'], 'error');
      expect(result['_sync']['sections']['marks']['status'], 'error');
      expect(
        result['_sync']['sections']['attendance']['failure_reason'],
        'missing_links',
      );
      expect(
        result['_sync']['sections']['marks']['failure_reason'],
        'missing_links',
      );
      expect(result['_sync']['outcome'], 'partial');
    },
  );
}
