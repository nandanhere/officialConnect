import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';
import 'package:official_connect/Services/app_distribution.dart';
import 'package:official_connect/Services/firebase_crash_reporting.dart';
import 'package:official_connect/Services/firebase_feature_flags.dart';
import 'package:official_connect/Services/firebase_sync_diagnostics.dart';
import 'package:official_connect/Services/sync_diagnostics.dart';
import 'package:official_connect/firebase_options.dart';

class FirebaseOperations {
  static bool _desiredDiagnosticsEnabled = true;

  static Future<void> initialize({required bool enabled}) async {
    _desiredDiagnosticsEnabled = enabled;
    if (kIsWeb) return;
    try {
      if (Firebase.apps.isEmpty) {
        await Firebase.initializeApp(
          options: DefaultFirebaseOptions.currentPlatform,
        );
      }
      final collectionEnabled =
          enabled && AppDistribution.allowsProductionTelemetry;
      await Future.wait([
        FirebaseSyncDiagnostics.initialize(enabled: collectionEnabled),
        FirebaseFeatureFlags.initialize(),
        FirebaseCrashReporting.initialize(enabled: collectionEnabled),
      ]);
      SyncDiagnostics.configureCrashContext(FirebaseCrashReporting.setContext);
      // A user can change this preference while Firebase is starting. Apply
      // the latest choice once initialization finishes instead of restoring
      // the value captured at launch.
      await setDiagnosticsEnabled(_desiredDiagnosticsEnabled);
    } catch (_) {
      debugPrint('App health services are unavailable in this build.');
    }
  }

  static Future<void> setDiagnosticsEnabled(bool enabled) async {
    _desiredDiagnosticsEnabled = enabled;
    final collectionEnabled =
        enabled && AppDistribution.allowsProductionTelemetry;
    await Future.wait([
      FirebaseSyncDiagnostics.setEnabled(collectionEnabled),
      FirebaseCrashReporting.setEnabled(collectionEnabled),
    ]);
    if (!collectionEnabled) {
      SyncDiagnostics.configureCrashContext(null);
    } else {
      SyncDiagnostics.configureCrashContext(FirebaseCrashReporting.setContext);
    }
  }
}
