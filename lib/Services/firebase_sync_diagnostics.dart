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
      SyncDiagnostics.configure(
        (name, parameters) =>
            analytics.logEvent(name: name, parameters: parameters),
        collectionToggle: analytics.setAnalyticsCollectionEnabled,
      );
      await SyncDiagnostics.setEnabled(enabled);
    } catch (_) {
      // Local builds remain usable before Firebase platform files are linked.
      debugPrint('Update diagnostics are unavailable in this build.');
    }
  }

  static Future<void> setEnabled(bool enabled) =>
      SyncDiagnostics.setEnabled(enabled);
}
