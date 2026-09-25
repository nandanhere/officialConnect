import 'package:firebase_performance/firebase_performance.dart';
import 'package:flutter/foundation.dart';

/// Firebase Performance Monitoring traces mirroring the portal sync.
///
/// Timing parity with the `sync_section` analytics events: one `portal_sync`
/// trace per [scrapeAll] run plus one `sync_section_<name>` trace per parsed
/// section. The analytics event stream is untouched — this sink only adds
/// duration distributions and status attributes in the Firebase console.
///
/// Every entry point is fail-closed: web, missing native plugin, revoked
/// consent, or any platform error silently disables tracing and never throws.
class FirebasePerformanceTraces {
  static const _portalTraceName = 'portal_sync';
  static const _sectionTracePrefix = 'sync_section_';

  static bool _collectionEnabled = false;
  static FirebasePerformance? _performance;
  static Trace? _portalTrace;
  static final Map<String, Trace> _openSections = {};

  static Future<void> initialize({required bool enabled}) async {
    if (kIsWeb) return;
    try {
      _performance = FirebasePerformance.instance;
      _collectionEnabled = enabled;
      await _performance!.setPerformanceCollectionEnabled(enabled);
    } catch (_) {
      _performance = null;
      _collectionEnabled = false;
      debugPrint('Performance traces are unavailable in this build.');
    }
  }

  static Future<void> setEnabled(bool enabled) async {
    _collectionEnabled = enabled;
    try {
      await _performance?.setPerformanceCollectionEnabled(enabled);
    } catch (_) {
      // A toggle must never break the settings flow.
    }
    if (!enabled) {
      _portalTrace = null;
      _openSections.clear();
    }
  }

  /// Starts the overall sync trace. Safe to call when disabled (no-op).
  static Future<void> startPortalSync() async {
    if (!_collectionEnabled) return;
    try {
      final trace = _performance!.newTrace(_portalTraceName);
      await trace.start();
      _portalTrace = trace;
    } catch (_) {
      _portalTrace = null;
    }
  }

  static Future<void> stopPortalSync({required String status}) async {
    final trace = _portalTrace;
    _portalTrace = null;
    if (trace == null) return;
    try {
      trace.putAttribute('status', _safeStatus(status));
      await trace.stop();
    } catch (_) {
      // A failed stop must never surface to the sync flow.
    }
  }

  /// Starts a per-section trace. Calls are ignored unless collection runs.
  static Future<void> startSection(String section) async {
    if (!_collectionEnabled) return;
    final name = _sectionTraceName(section);
    if (name == null) return;
    try {
      final trace = _performance!.newTrace(name);
      await trace.start();
      _openSections[name] = trace;
    } catch (_) {
      // Individual sections degrade to analytics-only timing.
    }
  }

  /// Stops the open trace for [section], attributing its reported outcome.
  /// Unknown or already-stopped sections are ignored.
  static Future<void> stopSection(
    String section, {
    required String status,
    int? count,
  }) async {
    final name = _sectionTraceName(section);
    final trace = name == null ? null : _openSections.remove(name);
    if (trace == null) return;
    try {
      trace.putAttribute('status', _safeStatus(status));
      if (count != null) trace.setMetric('item_count', count);
      await trace.stop();
    } catch (_) {
      // A failed stop must never surface to the sync flow.
    }
  }

  static String? _sectionTraceName(String section) {
    final token = section.trim().toLowerCase();
    if (token.isEmpty) return null;
    final sanitized = token.replaceAll(RegExp(r'[^a-z0-9]'), '_');
    final name = '$_sectionTracePrefix$sanitized';
    return name.length <= 100 ? name : null;
  }

  static String _safeStatus(String status) {
    final token = status.trim().toLowerCase();
    return RegExp(r'^[a-z0-9][a-z0-9_.-]*$').hasMatch(token) &&
            token.length <= 32
        ? token
        : 'unknown';
  }
}
