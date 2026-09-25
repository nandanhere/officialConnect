import 'package:firebase_analytics/firebase_analytics.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';
import 'package:official_connect/Services/app_distribution.dart';
import 'package:official_connect/Services/firebase_crash_reporting.dart';
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
        (name, parameters) async {
          await analytics.logEvent(name: name, parameters: parameters);
          // Leave a bounded trail so a crash during a long refresh shows
          // which section the sync reached. Never affects the event stream.
          final crumb = FirebaseCrashReporting.breadcrumbFor(
            name,
            parameters,
          );
          if (crumb != null) {
            await FirebaseCrashReporting.logBreadcrumb(crumb);
          }
        },
        collectionToggle: analytics.setAnalyticsCollectionEnabled,
      );
      // Use the bounded Flutter route as both name and class so the
      // default Screens report separates routes instead of collapsing
      // everything into one native host-activity row.
      SyncDiagnostics.configureScreenReporter(
        (screen) => analytics.logScreenView(
          screenName: screen,
          screenClass: screen,
        ),
      );
      if (enabled) {
        await SyncDiagnostics.setEnabled(true);
      }
    } catch (_) {
      // Local builds remain usable before Firebase platform files are linked.
      SyncDiagnostics.configureScreenReporter(null);
      debugPrint('Update diagnostics are unavailable in this build.');
    }
  }

  static Future<void> setEnabled(bool enabled) =>
      SyncDiagnostics.setEnabled(enabled);
}
