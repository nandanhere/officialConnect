import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:official_connect/Classes/previous_result.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/login_screen/login_screen.dart';
import 'package:official_connect/Screens/login_screen/student_home/results_screen/results_screen.dart';
import 'package:official_connect/Screens/login_screen/student_home/results_screen/widgets/marks_card.dart';
import 'package:official_connect/Services/exam_result_scraper.dart';
import 'package:official_connect/Services/sync_diagnostics.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  test('examination result HTML is converted into native result data', () {
    const html = '''
      <div class="stu-data stu-data2"><p>Even May 2026 Semester 6</p></div>
      <div class="credits-sec1"><p>Credits Registered: 20</p></div>
      <div class="credits-sec2"><p>Credits Earned: 20</p></div>
      <div class="credits-sec3"><p>SGPA: 8.75</p></div>
      <div class="credits-sec4"><p>CGPA: 8.41</p></div>
      <table class="uk-table res-table">
        <tr><th>Course Code</th><th>Subject Name</th><th>Credits Earned</th><th>Credits Reg.</th><th>Grade</th></tr>
        <tr><td>IS601</td><td>Cloud Computing</td><td>4</td><td>4</td><td>A</td></tr>
      </table>
    ''';
    final result = ExamResultScraper.parse(html, ExamResultSource.regular);

    expect(result.semesterNumber, '6');
    expect(result.sgpa, '8.75');
    expect(result.cgpa, '8.41');
    expect(result.results.single.subjectName, 'Cloud Computing');
    expect(result.results.single.grade, 'A');
  });

  test('backlog tables do not consume a semester number', () {
    Map<String, dynamic> result(String term, {String cgpa = '9.0'}) => {
      'term': term,
      'CGPA': cgpa,
      'Credits Earned ': '20',
      'Credits Registered ': '20',
      'SGPA': '9.0',
      'results': <Map<String, dynamic>>[],
    };

    final results = PreviousResult.getList([
      result('Back-Log Courses'),
      result('Jan 2023'),
      result('May/June 2023'),
    ]);

    expect(results[0].semesterNumber, 0);
    expect(results[1].semesterNumber, 1);
    expect(results[2].semesterNumber, 2);
  });

  test('partial portal updates preserve failed sections', () async {
    SharedPreferences.setMockInitialValues({});
    final sisData = SisData();
    await sisData.getData('DUMMY', '', false);
    final previousAttendance = sisData.attendances.length;

    await sisData.applyPortalData(
      {
        'name': 'Updated Student',
        'marks': <dynamic>[],
        '_sync': {
          'version': 1,
          'outcome': 'partial',
          'sections': {
            'attendance': {'status': 'error'},
            'marks': {'status': 'empty'},
          },
        },
      },
      'TEST',
      '2000-01-01',
    );

    expect(sisData.attendances.length, previousAttendance);
    expect(sisData.marks, isEmpty);
    expect(sisData.hasSyncIssues, isTrue);
    expect(sisData.syncStatusFor('attendance'), 'error');
  });

  test('update diagnostics only emit bounded aggregate fields', () async {
    final events = <Map<String, Object>>[];
    SyncDiagnostics.configure((name, parameters) async {
      events.add({'name': name, ...parameters});
    });
    await SyncDiagnostics.setEnabled(true);

    await SyncDiagnostics.recordSummary({
      'version': 1,
      'outcome': 'partial',
      'duration_ms': 999999999,
      'usn': 'SHOULD_NOT_APPEAR',
      'sections': {
        'attendance': {
          'status': 'partial',
          'count': 5,
          'failed': 1,
          'student_name': 'SHOULD_NOT_APPEAR',
        },
        'student-secret': {'status': 'error'},
      },
    }, refresh: true);

    final encoded = events.toString();
    expect(encoded, isNot(contains('SHOULD_NOT_APPEAR')));
    expect(encoded, isNot(contains('student-secret')));
    expect(encoded, contains('section: unknown'));
    expect(encoded, contains('duration_ms: 600000'));
  });

  testWidgets('student login opens the native verification form', (
    WidgetTester tester,
  ) async {
    SharedPreferences.setMockInitialValues({});
    await tester.pumpWidget(
      ChangeNotifierProvider(
        create: (_) => SisData(),
        child: const MaterialApp(home: LoginScreen()),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('Student Login'), findsOneWidget);
    await tester.tap(find.text('Student Login'));
    await tester.pumpAndSettle();

    expect(find.byKey(const ValueKey('usn')), findsOneWidget);
    expect(find.byKey(const ValueKey('dob')), findsOneWidget);
    expect(find.text('Verification type'), findsOneWidget);
    expect(find.text('Login'), findsOneWidget);
  });

  testWidgets('dummy login loads populated offline data', (
    WidgetTester tester,
  ) async {
    SharedPreferences.setMockInitialValues({});
    final sisData = SisData();
    await tester.pumpWidget(
      ChangeNotifierProvider.value(
        value: sisData,
        child: const MaterialApp(home: LoginScreen()),
      ),
    );
    await tester.pumpAndSettle();

    await tester.tap(find.text('Student Login'));
    await tester.pumpAndSettle();
    await tester.enterText(find.byKey(const ValueKey('usn')), 'DUMMY');
    await tester.ensureVisible(find.text('Login'));
    await tester.tap(find.text('Login'));
    await tester.pumpAndSettle();

    expect(sisData.hasData, isTrue);
    expect(sisData.isValidData, isTrue);
    expect(sisData.studentName, isNotEmpty);
    expect(sisData.attendances, isNotEmpty);
    expect(sisData.marks, isNotEmpty);
    expect(sisData.previousResults, isNotEmpty);
  });

  testWidgets('SEE renders quick-result shortcuts without a runtime error', (
    WidgetTester tester,
  ) async {
    SharedPreferences.setMockInitialValues({});
    final sisData = SisData();
    await sisData.getData('DUMMY', '', false);
    final showSee = ValueNotifier(false);
    addTearDown(showSee.dispose);

    await tester.pumpWidget(
      ChangeNotifierProvider.value(
        value: sisData,
        child: MaterialApp(home: Scaffold(body: ResultsScreen(showSee))),
      ),
    );
    await tester.pumpAndSettle();
    await tester.tap(find.text('SEE'));
    await tester.pumpAndSettle();

    expect(tester.takeException(), isNull);
    expect(find.text('Quick results'), findsOneWidget);
    expect(find.text('Latest regular result'), findsOneWidget);
    expect(find.text('Supplementary results'), findsOneWidget);
  });

  testWidgets('result subjects render as a compact table', (
    WidgetTester tester,
  ) async {
    final sisData = SisData();
    final subjects = [
      Subject(
        courseCode: 'IS601',
        subjectName: 'Cloud Computing',
        creditsEarned: '4',
        creditsRegistered: '4',
        gpa: '9',
        grade: 'A',
      ),
    ];

    await tester.pumpWidget(
      ChangeNotifierProvider.value(
        value: sisData,
        child: MaterialApp(
          home: Scaffold(body: MarksCard(subjects: subjects, isBackLog: false)),
        ),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('Course'), findsOneWidget);
    expect(find.text('Credits\nE / R'), findsOneWidget);
    expect(find.text('Result'), findsOneWidget);
    expect(find.text('Cloud Computing'), findsOneWidget);
    expect(find.text('4 / 4'), findsOneWidget);
    expect(find.text('A'), findsOneWidget);
  });
}
