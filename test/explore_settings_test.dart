import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/login_screen/student_home/events_screen/events_screen.dart';
import 'package:official_connect/Screens/login_screen/student_home/settings_screen/settings_screen.dart';
import 'package:official_connect/Services/safe_external_link.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

Widget _screen(
  Widget child,
  SisData sisData, {
  Size size = const Size(390, 844),
  double textScale = 1,
}) {
  return ChangeNotifierProvider<SisData>.value(
    value: sisData,
    child: MaterialApp(
      home: MediaQuery(
        data: MediaQueryData(
          size: size,
          textScaler: TextScaler.linear(textScale),
        ),
        child: Scaffold(body: child),
      ),
    ),
  );
}

Color? _renderedTextColor(WidgetTester tester, String text) {
  final paragraph = tester.renderObject<RenderParagraph>(find.text(text));
  return paragraph.text.style?.color;
}

void main() {
  setUp(() {
    SharedPreferences.setMockInitialValues(const {});
  });

  test('campus services use secure current destinations', () {
    expect(campusServiceLinks, hasLength(3));
    expect(
      campusServiceLinks.every((link) => link.url.startsWith('https://')),
      isTrue,
    );
    expect(
      campusServiceLinks.firstWhere((link) => link.key == 'fee-payment').url,
      'https://www.msrit.edu/',
    );
    expect(
      campusServiceLinks.firstWhere((link) => link.key == 'wifi-helpdesk').url,
      'https://rithelpdesk.msrit.edu/',
    );
  });

  testWidgets('Explore launches each campus service', (tester) async {
    final opened = <Uri>[];
    final sisData = SisData();
    addTearDown(sisData.dispose);
    await tester.pumpWidget(
      _screen(
        EventsScreen(
          linkLauncher: (uri) async {
            opened.add(uri);
            return true;
          },
        ),
        sisData,
      ),
    );

    for (final link in campusServiceLinks) {
      final target = find.byKey(ValueKey(link.key));
      await tester.ensureVisible(target);
      await tester.tap(target);
      await tester.pump(const Duration(milliseconds: 150));
    }

    expect(
      opened.map((uri) => uri.toString()),
      campusServiceLinks.map((link) => link.url),
    );
    expect(tester.takeException(), isNull);
  });

  testWidgets('external link failures are graceful and do not throw', (
    tester,
  ) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Builder(
          builder: (context) => Scaffold(
            body: TextButton(
              onPressed: () => openExternalLink(
                context,
                Uri.parse('https://example.invalid'),
                launcher: (_) async => throw StateError('unavailable'),
              ),
              child: const Text('Open'),
            ),
          ),
        ),
      ),
    );

    await tester.tap(find.text('Open'));
    await tester.pumpAndSettle();

    expect(find.text('Could not open that link. Try again.'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });

  testWidgets('appearance selector changes theme without hidden controls', (
    tester,
  ) async {
    final sisData = SisData();
    addTearDown(sisData.dispose);
    await tester.pumpWidget(
      _screen(
        const SettingsInfo(),
        sisData,
        size: const Size(320, 568),
        textScale: 1.15,
      ),
    );

    expect(find.byKey(const ValueKey('theme-selector')), findsOneWidget);
    expect(find.byType(DropdownButton<String>), findsNothing);
    await tester.tap(find.text('Dark'));
    await tester.pumpAndSettle();

    expect(sisData.themeMode, 'dark');
    expect(_renderedTextColor(tester, 'System'), Colors.white70);
    expect(_renderedTextColor(tester, 'Light'), Colors.white70);
    expect(_renderedTextColor(tester, 'Dark'), const Color(0xff4b4552));

    await tester.tap(find.text('Light'));
    await tester.pumpAndSettle();

    expect(sisData.themeMode, 'light');
    expect(_renderedTextColor(tester, 'System'), Colors.black87);
    expect(_renderedTextColor(tester, 'Light'), const Color(0xff4b4552));
    expect(_renderedTextColor(tester, 'Dark'), Colors.black87);
    expect(tester.takeException(), isNull);
  });

  testWidgets('appearance options remain readable in dark mode', (
    tester,
  ) async {
    final sisData = SisData()..themeMode = 'dark';
    addTearDown(sisData.dispose);
    await tester.pumpWidget(_screen(const SettingsInfo(), sisData));

    expect(_renderedTextColor(tester, 'System'), Colors.white70);
    expect(_renderedTextColor(tester, 'Light'), Colors.white70);
    expect(_renderedTextColor(tester, 'Dark'), const Color(0xff4b4552));
    expect(tester.takeException(), isNull);
  });

  testWidgets('appearance options retain contrast in light mode', (
    tester,
  ) async {
    final sisData = SisData()..themeMode = 'light';
    addTearDown(sisData.dispose);
    await tester.pumpWidget(_screen(const SettingsInfo(), sisData));

    expect(_renderedTextColor(tester, 'System'), Colors.black87);
    expect(_renderedTextColor(tester, 'Dark'), Colors.black87);
    expect(_renderedTextColor(tester, 'Light'), const Color(0xff4b4552));
    expect(tester.takeException(), isNull);
  });
}
