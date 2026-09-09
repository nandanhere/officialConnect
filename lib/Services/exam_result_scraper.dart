import 'package:html/dom.dart';
import 'package:html/parser.dart' as html_parser;
import 'package:official_connect/Classes/previous_result.dart';

enum ExamResultSource { regular, supplementary }

extension ExamResultSourceDetails on ExamResultSource {
  String get label => this == ExamResultSource.regular
      ? 'Latest regular result'
      : 'Latest supplementary result';

  String get pageUrl => this == ExamResultSource.regular
      ? 'https://exam.msrit.edu/'
      : 'https://exam.msrit.edu/eresultssupply/';

  String get captchaSelector =>
      this == ExamResultSource.regular ? '#captcha' : '#captchaCode0';

  String get captchaInputSelector =>
      this == ExamResultSource.regular ? '#securityCode' : '#osolCatchaTxt0';
}

class ExamResultParseException implements Exception {
  const ExamResultParseException(this.message);

  final String message;

  @override
  String toString() => message;
}

/// Converts the examination site's result page into the model used by the
/// app's native result cards. Parsing by headings first keeps this compatible
/// with both the current UIkit page and the older supplementary template.
class ExamResultScraper {
  static PreviousResult parse(String html, ExamResultSource source) {
    final document = html_parser.parse(html);
    final table = document.querySelector('table.res-table') ??
        document.querySelector('table.uk-table') ??
        _findResultTable(document);
    if (table == null) {
      throw const ExamResultParseException(
        'The examination site did not return a result table.',
      );
    }

    final rows = table.querySelectorAll('tr');
    if (rows.length < 2) {
      throw const ExamResultParseException('The returned result is empty.');
    }

    final headers = rows.first
        .querySelectorAll('th, td')
        .map((cell) => _normalise(cell.text))
        .toList();
    final subjects = <Subject>[];
    for (final row in rows.skip(1)) {
      final cells = row.querySelectorAll('td');
      if (cells.length < 2) continue;
      String cell(List<String> names, int fallback) {
        final index = headers.indexWhere(
          (header) => names.any((name) => header.contains(name)),
        );
        final resolved = index >= 0 ? index : fallback;
        return resolved >= 0 && resolved < cells.length
            ? _clean(cells[resolved].text)
            : '';
      }

      final code = cell(const ['course code', 'subject code'], 0);
      final name = cell(const ['subject name', 'course name'], 1);
      if (code.isEmpty && name.isEmpty) continue;
      subjects.add(
        Subject(
          courseCode: code,
          subjectName: name,
          creditsEarned: cell(const ['credits earned', 'credit earned'], 2),
          creditsRegistered:
              cell(const ['credits reg', 'credits registered', 'credits'], 3),
          gpa: cell(const ['gpa', 'grade point'], -1),
          grade: cell(const ['grade'], cells.length - 1),
        ),
      );
    }
    if (subjects.isEmpty) {
      throw const ExamResultParseException(
        'No subjects were present in the returned result.',
      );
    }

    final term = _metric(document, const [
          '.stu-data.stu-data2',
          '.stu-data2',
          '.headingdate',
        ]) ??
        source.label;
    final semesterMatch = RegExp(
      r'sem(?:ester)?\s*[-:]?\s*(\d+)',
      caseSensitive: false,
    ).firstMatch(term);

    return PreviousResult(
      cgpa: _metric(document, const ['.credits-sec4'], label: 'CGPA') ?? '',
      creditsEarned:
          _metric(document, const ['.credits-sec2'], label: 'Credits Earned') ??
              '',
      creditsRegistered: _metric(
            document,
            const ['.credits-sec1'],
            label: 'Credits Registered',
          ) ??
          '',
      sgpa: _metric(document, const ['.credits-sec3'], label: 'SGPA') ?? '',
      results: subjects,
      term: term,
      semesterNumber: semesterMatch?.group(1) ?? '',
    );
  }

  static Element? _findResultTable(Document document) {
    for (final table in document.querySelectorAll('table')) {
      final text = _normalise(table.text);
      if (text.contains('course code') &&
          (text.contains('grade') || text.contains('subject name'))) {
        return table;
      }
    }
    return null;
  }

  static String? _metric(
    Document document,
    List<String> selectors, {
    String? label,
  }) {
    for (final selector in selectors) {
      final element = document.querySelector(selector);
      if (element == null) continue;
      var value = _clean(element.querySelector('p')?.text ?? element.text);
      if (label != null) {
        value = value.replaceFirst(
          RegExp('^${RegExp.escape(label)}\\s*:?\\s*', caseSensitive: false),
          '',
        );
      }
      if (value.isNotEmpty) return value;
    }
    return null;
  }

  static String _normalise(String value) =>
      _clean(value).toLowerCase().replaceAll(RegExp(r'[^a-z0-9]+'), ' ');

  static String _clean(String value) =>
      value.replaceAll(RegExp(r'\s+'), ' ').trim();
}
