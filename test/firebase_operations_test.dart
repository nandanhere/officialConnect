import 'package:flutter_test/flutter_test.dart';
import 'package:official_connect/Services/firebase_feature_flags.dart';
import 'package:official_connect/Services/sync_diagnostics.dart';

void main() {
  tearDown(() {
    FirebaseFeatureFlags.setValuesForTesting(const {});
    SyncDiagnostics.configure(null);
    FirebaseFeatureFlags.configureRefreshForTesting(null);
  });

  test('feature controls default to enabled and compose safely', () {
    FirebaseFeatureFlags.setValuesForTesting(const {});
    expect(FirebaseFeatureFlags.portalSyncEnabled, isTrue);
    expect(FirebaseFeatureFlags.automaticRefreshEnabled, isTrue);
    expect(FirebaseFeatureFlags.sectionEnabled('attendance'), isTrue);
    expect(FirebaseFeatureFlags.resultSourceEnabled('regular'), isTrue);
  });

  test('portal switch disables portal sections and automatic refresh', () {
    FirebaseFeatureFlags.setValuesForTesting(const {
      FirebaseFeatureFlags.portalSyncKey: false,
    });
    expect(FirebaseFeatureFlags.portalSyncEnabled, isFalse);
    expect(FirebaseFeatureFlags.automaticRefreshEnabled, isFalse);
    expect(FirebaseFeatureFlags.sectionEnabled('marks'), isFalse);
    expect(FirebaseFeatureFlags.resultSourceEnabled('regular'), isTrue);
  });

  test('individual sections and result sources can be disabled', () {
    FirebaseFeatureFlags.setValuesForTesting(const {
      'scraper_marks_enabled': false,
      FirebaseFeatureFlags.supplementaryResultsKey: false,
    });
    expect(FirebaseFeatureFlags.sectionEnabled('marks'), isFalse);
    expect(FirebaseFeatureFlags.sectionEnabled('attendance'), isTrue);
    expect(FirebaseFeatureFlags.resultSourceEnabled('supplementary'), isFalse);
    expect(FirebaseFeatureFlags.resultSourceEnabled('regular'), isTrue);
    expect(FirebaseFeatureFlags.resultSourceEnabled('invented'), isFalse);
  });

  test('telemetry emits only bounded allowlisted operational data', () async {
    final events = <Map<String, Object>>[];
    SyncDiagnostics.configure((name, parameters) async {
      events.add({'name': name, ...parameters});
    });
    await SyncDiagnostics.setEnabled(true);

    await SyncDiagnostics.recordLoginStarted(refresh: false);
    await SyncDiagnostics.recordLoginFinished(
      outcome: 'student_identifier_1MS22IS086',
      refresh: false,
      durationMs: 999999999,
    );
    await SyncDiagnostics.recordResult(
      source: '1MS22IS086',
      outcome: '<html>secret</html>',
      durationMs: -12,
    );
    await SyncDiagnostics.recordSummary({
      'outcome': 'complete',
      'sections': {
        '1ms22is086': {'status': 'ok'},
      },
    }, refresh: true);

    final encoded = events.toString();
    expect(encoded, isNot(contains('1MS22IS086')));
    expect(encoded, isNot(contains('1ms22is086')));
    expect(encoded, isNot(contains('<html>')));
    expect(encoded, contains('outcome: unknown'));
    expect(encoded, contains('duration_ms: 600000'));
    expect(encoded, contains('duration_ms: 0'));
    expect(encoded, contains('section: unknown'));
  });

  test('disabled collection suppresses all operational events', () async {
    final events = <Map<String, Object>>[];
    SyncDiagnostics.configure((name, parameters) async {
      events.add({'name': name, ...parameters});
    });
    await SyncDiagnostics.setEnabled(false);
    await SyncDiagnostics.recordLoginStarted(refresh: true);
    await SyncDiagnostics.recordResult(source: 'regular', outcome: 'success');
    expect(events, isEmpty);
  });

  test('feature analytics accepts only coarse allowlisted values', () async {
    final events = <Map<String, Object>>[];
    SyncDiagnostics.configure((name, parameters) async {
      events.add({'name': name, ...parameters});
    });
    await SyncDiagnostics.setEnabled(true);

    await SyncDiagnostics.recordScreen('results');
    await SyncDiagnostics.recordFeature('fee_payment');
    await SyncDiagnostics.recordPreference('theme', 'dark');
    await SyncDiagnostics.recordScreen('1MS22IS086');
    await SyncDiagnostics.recordFeature('marks_for_1MS22IS086');
    await SyncDiagnostics.recordPreference('theme', '24/02/2004');

    expect(
      events.any(
        (event) =>
            event['name'] == 'app_screen_view' && event['screen'] == 'results',
      ),
      isTrue,
    );
    expect(
      events.any(
        (event) =>
            event['name'] == 'feature_opened' &&
            event['feature'] == 'fee_payment',
      ),
      isTrue,
    );
    expect(
      events.any(
        (event) =>
            event['name'] == 'preference_changed' &&
            event['preference'] == 'theme' &&
            event['value'] == 'dark',
      ),
      isTrue,
    );
    final encoded = events.toString();
    expect(encoded, isNot(contains('1MS22IS086')));
    expect(encoded, isNot(contains('24/02/2004')));
    expect(encoded, contains('feature: unknown'));
    expect(encoded, contains('value: unknown'));
  });

  test('diagnostics sink failures never propagate', () async {
    SyncDiagnostics.configure((_, __) async => throw StateError('offline'));
    await SyncDiagnostics.setEnabled(true);

    await expectLater(
      SyncDiagnostics.recordLoginStarted(refresh: false),
      completes,
    );
    await expectLater(
      SyncDiagnostics.recordSummary({
        'outcome': 'partial',
        'sections': {
          'marks': {'status': 'error'},
        },
      }, refresh: true),
      completes,
    );
  });

  test('collection toggle failures never propagate', () async {
    SyncDiagnostics.configure(
      null,
      collectionToggle: (_) async => throw StateError('unavailable'),
    );
    await expectLater(SyncDiagnostics.setEnabled(false), completes);
  });

  test('feature refresh is fail-open and throttled while offline', () async {
    var attempts = 0;
    FirebaseFeatureFlags.configureRefreshForTesting(() async {
      attempts++;
      throw StateError('offline');
    });

    await FirebaseFeatureFlags.refresh();
    await FirebaseFeatureFlags.refresh();

    expect(attempts, 1);
    expect(FirebaseFeatureFlags.portalSyncEnabled, isTrue);
  });
}
