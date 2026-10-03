import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/login_screen/login_screen.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  testWidgets('date picker stays usable on a small phone screen', (
    WidgetTester tester,
  ) async {
    tester.view.physicalSize = const Size(320, 568);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    SharedPreferences.setMockInitialValues({});

    await tester.pumpWidget(
      MaterialApp(
        home: ChangeNotifierProvider(
          create: (_) => SisData(),
          child: const Scaffold(body: LoginScreen()),
        ),
      ),
    );
    await tester.pumpAndSettle();

    await tester.tap(find.text('Student Login'));
    await tester.pumpAndSettle();
    expect(tester.takeException(), isNull, reason: 'form render');

    await tester.tap(find.byKey(const ValueKey('dob')));
    await tester.pumpAndSettle();

    expect(find.text('Pick a date'), findsOneWidget);
    // A RenderFlex overflow inside the dialog is reported as a framework
    // error; none may occur on small screens.
    expect(tester.takeException(), isNull);

    // The year grid is taller than the dialog viewport on small screens;
    // dragging must scroll the content instead of overflowing.
    await tester.drag(find.text('Pick a date'), const Offset(0, -300));
    await tester.pumpAndSettle();
    await tester.tapAt(const Offset(10, 10));
    await tester.pumpAndSettle();

    expect(find.text('Pick a date'), findsNothing);
    expect(find.byKey(const ValueKey('dob')), findsOneWidget);
    expect(tester.takeException(), isNull);
  });

  for (final width in [320.0, 390.0, 800.0]) {
    testWidgets('every year cell fits the dialog at ${width.toInt()}px wide', (
      WidgetTester tester,
    ) async {
      tester.view.physicalSize = Size(width, 844);
      tester.view.devicePixelRatio = 1.0;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      SharedPreferences.setMockInitialValues({});

      await tester.pumpWidget(
        MaterialApp(
          home: ChangeNotifierProvider(
            create: (_) => SisData(),
            child: const Scaffold(body: LoginScreen()),
          ),
        ),
      );
      await tester.pumpAndSettle();

      await tester.tap(find.text('Student Login'));
      await tester.pumpAndSettle();
      await tester.tap(find.byKey(const ValueKey('dob')));
      await tester.pumpAndSettle();

      // The picker opens on the page containing maxDate (now - 15y) with
      // 12-year pages starting at minDate (now - 32y).
      final minYear = DateTime.now().year - 32;
      final maxYear = DateTime.now().year - 15;
      final page = ((maxYear - minYear + 1) / 12).ceil() - 1;
      final startYear = minYear + page * 12;

      // Every cell of the page must be on-screen (a clipped third column
      // lands outside the visible bounds and can never be tapped).
      for (var year = startYear; year < startYear + 12; year++) {
        final cell = find.text('$year');
        expect(cell, findsOneWidget, reason: 'year $year present');
        final center = tester.getCenter(cell);
        expect(
          center.dx,
          inInclusiveRange(0.0, width),
          reason: 'year $year on-screen horizontally',
        );
      }
      expect(tester.takeException(), isNull);
    });
  }
}
