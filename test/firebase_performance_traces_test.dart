import 'package:flutter_test/flutter_test.dart';
import 'package:official_connect/Services/firebase_performance_traces.dart';

void main() {
  test('performance traces stay silent without native Firebase', () async {
    // No Firebase app is configured in unit tests: initialize must degrade
    // to disabled instead of throwing, and every later call stays a no-op.
    await FirebasePerformanceTraces.initialize(enabled: true);

    await FirebasePerformanceTraces.startPortalSync();
    await FirebasePerformanceTraces.startSection('attendance');
    await FirebasePerformanceTraces.stopSection(
      'attendance',
      status: 'ok',
      count: 3,
    );
    await FirebasePerformanceTraces.stopPortalSync(status: 'complete');

    // Unknown, unstopped, and double-stopped sections are ignored.
    await FirebasePerformanceTraces.stopSection('never-started',
        status: 'ok');
    await FirebasePerformanceTraces.stopSection('attendance',
        status: 'ok');
    await FirebasePerformanceTraces.stopPortalSync(status: 'complete');
  });

  test('disabling performance traces clears pending state', () async {
    await FirebasePerformanceTraces.initialize(enabled: false);

    await FirebasePerformanceTraces.startPortalSync();
    await FirebasePerformanceTraces.startSection('marks');
    await FirebasePerformanceTraces.setEnabled(false);

    await FirebasePerformanceTraces.stopSection('marks', status: 'ok');
    await FirebasePerformanceTraces.stopPortalSync(status: 'ok');
    await FirebasePerformanceTraces.setEnabled(true);
    await FirebasePerformanceTraces.setEnabled(false);
  });
}
