import 'package:firebase_remote_config/firebase_remote_config.dart';
import 'package:flutter/foundation.dart';

/// Operational switches that fail open if Remote Config is unavailable.
class FirebaseFeatureFlags {
  static const refreshThrottle = Duration(minutes: 15);
  static const portalSyncKey = 'portal_sync_enabled';
  static const automaticRefreshKey = 'automatic_refresh_enabled';
  static const regularResultsKey = 'results_regular_enabled';
  static const supplementaryResultsKey = 'results_supplementary_enabled';

  static const _sectionKeys = {
    'profile': 'scraper_profile_enabled',
    'attendance': 'scraper_attendance_enabled',
    'marks': 'scraper_marks_enabled',
    'proctor': 'scraper_proctor_enabled',
    'fees': 'scraper_fees_enabled',
    'results': 'scraper_results_enabled',
    'timetable': 'scraper_timetable_enabled',
    'seating': 'scraper_seating_enabled',
  };

  static final Map<String, bool> _values = {
    portalSyncKey: true,
    automaticRefreshKey: true,
    regularResultsKey: true,
    supplementaryResultsKey: true,
    for (final key in _sectionKeys.values) key: true,
  };
  static DateTime? _lastRefreshAttempt;
  static Future<bool> Function()? _fetchForTesting;

  static Future<void> initialize() async {
    final remoteConfig = FirebaseRemoteConfig.instance;
    await remoteConfig.setDefaults(_values);
    await remoteConfig.setConfigSettings(
      RemoteConfigSettings(
        fetchTimeout: const Duration(seconds: 10),
        minimumFetchInterval: kDebugMode
            ? Duration.zero
            : const Duration(hours: 1),
      ),
    );
    // Apply the last activated values immediately, including when offline.
    _readCurrentValues();
    await refresh(force: true);
  }

  /// Refreshes controls without making callers wait. Existing values remain
  /// active when offline or when Firebase is unavailable.
  static void refreshInBackground({bool force = false}) {
    refresh(force: force);
  }

  static Future<void> refresh({bool force = false}) async {
    final now = DateTime.now();
    if (!force &&
        _lastRefreshAttempt != null &&
        now.difference(_lastRefreshAttempt!) < refreshThrottle) {
      return;
    }
    _lastRefreshAttempt = now;
    try {
      if (_fetchForTesting != null) {
        await _fetchForTesting!.call();
      } else {
        await FirebaseRemoteConfig.instance.fetchAndActivate();
      }
      _readCurrentValues();
    } catch (_) {
      debugPrint(
        'Feature controls could not be refreshed; using saved values.',
      );
    }
  }

  static void _readCurrentValues() {
    final remoteConfig = FirebaseRemoteConfig.instance;
    for (final key in _values.keys) {
      _values[key] = remoteConfig.getBool(key);
    }
  }

  static bool get portalSyncEnabled {
    refreshInBackground();
    return _values[portalSyncKey] ?? true;
  }

  static bool get automaticRefreshEnabled =>
      portalSyncEnabled && (_values[automaticRefreshKey] ?? true);

  static bool sectionEnabled(String section) {
    final key = _sectionKeys[section];
    return portalSyncEnabled && (key == null || (_values[key] ?? true));
  }

  static bool resultSourceEnabled(String source) {
    final key = switch (source) {
      'regular' => regularResultsKey,
      'supplementary' => supplementaryResultsKey,
      _ => null,
    };
    return key != null && (_values[key] ?? true);
  }

  @visibleForTesting
  static void setValuesForTesting(Map<String, bool> values) {
    _values
      ..updateAll((_, _) => true)
      ..addAll(values);
  }

  @visibleForTesting
  static void configureRefreshForTesting(Future<bool> Function()? fetch) {
    _fetchForTesting = fetch;
    _lastRefreshAttempt = null;
  }
}
