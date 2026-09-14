import 'package:firebase_analytics/firebase_analytics.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';
import 'package:official_connect/Services/app_distribution.dart';
import 'package:official_connect/Services/sync_diagnostics.dart';
import 'package:official_connect/firebase_options.dart';

class FirebaseSyncDiagnostics {
  static Future<void> initialize({required bool enabled}) async {
    if (kIsWeb) return;
    try {
      if (Firebase.apps.isEmpty) {
        await Firebase.initializeApp(
          options: DefaultFirebaseOptions.currentPlatform,
        );
      }
      final analytics = FirebaseAnalytics.instance;
      if (enabled) {
        await analytics.setUserProperty(
          name: 'distribution_channel',
          value: AppDistribution.channel,
        );
      }
      await analytics.setAnalyticsCollectionEnabled(enabled);
      if (!enabled) {
        // Disable and discard startup events before attaching the Firebase
        // sink. Otherwise configure() would flush events queued while the app
        // was starting, contaminating production data from a local build.
        await SyncDiagnostics.setEnabled(false);
      }
      SyncDiagnostics.configure(
        (name, parameters) =>
            analytics.logEvent(name: name, parameters: parameters),
        collectionToggle: analytics.setAnalyticsCollectionEnabled,
      );
      if (enabled) {
        await SyncDiagnostics.setEnabled(true);
      }
    } catch (_) {
      // Local builds remain usable before Firebase platform files are linked.
      debugPrint('Update diagnostics are unavailable in this build.');
    }
  }

  static Future<void> setEnabled(bool enabled) =>
      SyncDiagnostics.setEnabled(enabled);
}
