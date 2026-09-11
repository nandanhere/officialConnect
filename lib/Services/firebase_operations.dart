import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';
import 'package:official_connect/Services/firebase_crash_reporting.dart';
import 'package:official_connect/Services/firebase_feature_flags.dart';
import 'package:official_connect/Services/firebase_sync_diagnostics.dart';
import 'package:official_connect/firebase_options.dart';

class FirebaseOperations {
  static Future<void> initialize({required bool enabled}) async {
    if (kIsWeb) return;
    try {
      if (Firebase.apps.isEmpty) {
        await Firebase.initializeApp(
          options: DefaultFirebaseOptions.currentPlatform,
        );
      }
      await Future.wait([
        FirebaseSyncDiagnostics.initialize(enabled: enabled),
        FirebaseFeatureFlags.initialize(),
        FirebaseCrashReporting.initialize(enabled: enabled),
      ]);
    } catch (_) {
      debugPrint('App health services are unavailable in this build.');
    }
  }

  static Future<void> setDiagnosticsEnabled(bool enabled) async {
    await Future.wait([
      FirebaseSyncDiagnostics.setEnabled(enabled),
      FirebaseCrashReporting.setEnabled(enabled),
    ]);
  }
}
