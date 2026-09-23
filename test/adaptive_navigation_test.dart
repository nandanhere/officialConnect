import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/login_screen/student_home/unified_screen.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

const _labels = ['Explore', 'Results', 'Home', 'Attendance', 'Settings'];

Future<SisData> _readySisData() async {
  final sisData = SisData();
  await sisData.loadDummyData();
  return sisData;
}

Future<void> _pumpUnified(
  WidgetTester tester,
  SisData sisData, {
  Size size = const Size(390, 844),
  double textScale = 1,
}) async {
  tester.view.physicalSize = size;
  tester.view.devicePixelRatio = 1;
  await tester.pumpWidget(
    ChangeNotifierProvider<SisData>.value(
      value: sisData,
      child: MaterialApp(
        builder: (context, child) => MediaQuery(
          data: MediaQuery.of(context).copyWith(
            textScaler: TextScaler.linear(textScale),
          ),
          child: child!,
        ),
        home: const Unified(),
      ),
    ),
  );
  await tester.pumpAndSettle();
}

void main() {
  setUp(() {
    SharedPreferences.setMockInitialValues(const {});
    Unified.screenNumber.value = 2;
  });

  tearDown(() {
    Unified.screenNumber.value = 2;
  });

  testWidgets('phone keeps bottom navigation with five destinations', (
    tester,
  ) async {
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    final sisData = await _readySisData();
    addTearDown(sisData.dispose);

    await _pumpUnified(tester, sisData, size: const Size(390, 844));

    expect(find.byType(BottomNavigationBar), findsOneWidget);
    expect(find.byType(NavigationRail), findsNothing);
    for (final label in _labels) {
      expect(find.text(label), findsOneWidget);
    }
    expect(tester.takeException(), isNull);
  });

  testWidgets('phone selection follows bottom navigation taps', (tester) async {
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    final sisData = await _readySisData();
    addTearDown(sisData.dispose);

    await _pumpUnified(tester, sisData, size: const Size(360, 800));

    await tester.tap(find.text('Attendance'));
    await tester.pumpAndSettle();

    expect(Unified.screenNumber.value, 3);
    expect(
      tester.widget<BottomNavigationBar>(find.byType(BottomNavigationBar))
          .currentIndex,
      3,
    );
    expect(tester.takeException(), isNull);
  });

  testWidgets('tablet uses a persistent rail with constrained content', (
    tester,
  ) async {
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    final sisData = await _readySisData();
    addTearDown(sisData.dispose);

    await _pumpUnified(tester, sisData, size: const Size(800, 1280));

    expect(find.byType(NavigationRail), findsOneWidget);
    expect(find.byType(BottomNavigationBar), findsNothing);
    final rail = tester.widget<NavigationRail>(find.byType(NavigationRail));
    expect(rail.destinations, hasLength(5));
    for (final label in _labels) {
      expect(
        find.descendant(
          of: find.byType(NavigationRail),
          matching: find.text(label),
        ),
        findsOneWidget,
      );
    }
    final constrained = tester
        .widgetList<ConstrainedBox>(find.byType(ConstrainedBox))
        .where((box) => box.constraints.maxWidth == 900);
    expect(constrained, isNotEmpty);
    expect(tester.takeException(), isNull);
  });

  testWidgets('tablet rail selection updates the shared tab state', (
    tester,
  ) async {
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    final sisData = await _readySisData();
    addTearDown(sisData.dispose);

    await _pumpUnified(tester, sisData, size: const Size(1024, 768));

    await tester.tap(
      find.descendant(
        of: find.byType(NavigationRail),
        matching: find.text('Results'),
      ),
    );
    await tester.pumpAndSettle();

    expect(Unified.screenNumber.value, 1);
    expect(
      tester.widget<NavigationRail>(find.byType(NavigationRail))
          .selectedIndex,
      1,
    );
    expect(tester.takeException(), isNull);
  });

  testWidgets('phone navigation survives large text scaling', (tester) async {
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    final sisData = await _readySisData();
    addTearDown(sisData.dispose);

    await _pumpUnified(
      tester,
      sisData,
      size: const Size(360, 800),
      textScale: 2,
    );

    expect(find.byType(BottomNavigationBar), findsOneWidget);
    expect(tester.takeException(), isNull);
  });

  testWidgets('tablet rail survives large text scaling', (tester) async {
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    final sisData = await _readySisData();
    addTearDown(sisData.dispose);

    await _pumpUnified(
      tester,
      sisData,
      size: const Size(800, 1280),
      textScale: 2,
    );

    expect(find.byType(NavigationRail), findsOneWidget);
    expect(find.byType(BottomNavigationBar), findsNothing);
    expect(tester.takeException(), isNull);
  });
}
