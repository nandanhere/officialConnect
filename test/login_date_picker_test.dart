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
}
