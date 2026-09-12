import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:official_connect/Screens/login_screen/portal_refresh.dart';
import 'package:official_connect/Screens/login_screen/portal_login_screen.dart';
import 'package:official_connect/Widgets/background_sync_status.dart';

Widget _testApp({
  required ValueNotifier<BackgroundSyncState> state,
  Size size = const Size(320, 568),
  double textScale = 1,
  Brightness brightness = Brightness.light,
}) {
  return MaterialApp(
    theme: ThemeData(brightness: brightness),
    home: MediaQuery(
      data: MediaQueryData(
        size: size,
        textScaler: TextScaler.linear(textScale),
      ),
      child: Scaffold(
        body: Stack(
          children: [
            PageView(
              children: const [
                Center(key: ValueKey('page-one'), child: Text('Page one')),
                Center(key: ValueKey('page-two'), child: Text('Page two')),
              ],
            ),
            Positioned(
              left: 8,
              right: 8,
              bottom: 8,
              child: Center(child: BackgroundSyncStatus(listenable: state)),
            ),
          ],
        ),
      ),
    ),
  );
}

void main() {
  testWidgets('hidden portal browser cannot cover the native login UI', (
    tester,
  ) async {
    tester.view.physicalSize = const Size(411, 914);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: Stack(
            children: [
              PortalBrowserViewport(
                hidden: true,
                child: ColoredBox(
                  key: ValueKey('portal-platform-view'),
                  color: Colors.red,
                ),
              ),
              Center(child: Text('Signing you in')),
            ],
          ),
        ),
      ),
    );

    final browser = find.byKey(const ValueKey('portal-platform-view'));
    expect(tester.getSize(browser), const Size(1, 1));
    expect(tester.getTopLeft(browser), const Offset(-2, -2));
    expect(find.text('Signing you in'), findsOneWidget);
    expect(tester.takeException(), isNull);

    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: Stack(
            children: [
              PortalBrowserViewport(
                hidden: false,
                child: ColoredBox(
                  key: ValueKey('portal-platform-view'),
                  color: Colors.red,
                ),
              ),
            ],
          ),
        ),
      ),
    );

    expect(tester.getSize(browser), const Size(411, 914));
    expect(tester.getTopLeft(browser), Offset.zero);
    expect(tester.takeException(), isNull);
  });

  testWidgets('background update status does not block page navigation', (
    tester,
  ) async {
    final state = ValueNotifier(BackgroundSyncState.updating);
    addTearDown(state.dispose);
    await tester.pumpWidget(_testApp(state: state));

    expect(find.text('Updating'), findsOneWidget);
    await tester.drag(find.byType(PageView), const Offset(-280, 0));
    await tester.pump(const Duration(milliseconds: 500));

    expect(find.byKey(const ValueKey('page-two')), findsOneWidget);
    expect(tester.takeException(), isNull);
  });

  testWidgets('all sync outcomes fit a small screen with large text', (
    tester,
  ) async {
    final state = ValueNotifier(BackgroundSyncState.success);
    addTearDown(state.dispose);
    await tester.pumpWidget(
      _testApp(state: state, size: const Size(280, 520), textScale: 2),
    );

    for (final value in [
      BackgroundSyncState.success,
      BackgroundSyncState.partial,
      BackgroundSyncState.error,
    ]) {
      state.value = value;
      await tester.pump(const Duration(milliseconds: 300));
      expect(tester.takeException(), isNull);
    }
    state.value = BackgroundSyncState.partial;
    await tester.pump(const Duration(milliseconds: 300));
    expect(find.text('Some information could not be updated'), findsOneWidget);
  });

  testWidgets('status remains readable in dark theme', (tester) async {
    final state = ValueNotifier(BackgroundSyncState.error);
    addTearDown(state.dispose);
    await tester.pumpWidget(
      _testApp(state: state, brightness: Brightness.dark),
    );

    final text = tester.widget<Text>(find.text('Update needs attention'));
    final background = tester.widget<Material>(
      find.byKey(const ValueKey('background-sync-status')),
    );
    expect(text.style?.color, isNot(background.color));
    expect(tester.takeException(), isNull);
  });
}
