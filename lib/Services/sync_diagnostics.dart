import 'package:flutter/foundation.dart';

typedef DiagnosticsEventSink =
    Future<void> Function(String name, Map<String, Object> parameters);
typedef DiagnosticsCollectionToggle = Future<void> Function(bool enabled);

/// Emits only bounded, allowlisted operational health signals.
class SyncDiagnostics {
  static const _sections = {
    'profile',
    'attendance',
    'marks',
    'proctor',
    'fees',
    'results',
  };
  static const _outcomes = {
    'started',
    'success',
    'complete',
    'partial',
    'empty',
    'ok',
    'error',
    'disabled',
    'cancelled',
    'session_expired',
    'network_error',
    'portal_attention',
    'parse_error',
  };
  static const _resultSources = {'regular', 'supplementary'};

  static DiagnosticsEventSink? _sink;
  static DiagnosticsCollectionToggle? _collectionToggle;
  static bool _enabled = true;

  static void configure(
    DiagnosticsEventSink? sink, {
    DiagnosticsCollectionToggle? collectionToggle,
  }) {
    _sink = sink;
    _collectionToggle = collectionToggle;
  }

  static Future<void> setEnabled(bool enabled) async {
    _enabled = enabled;
    try {
      await _collectionToggle?.call(enabled);
    } catch (error) {
      debugPrint('Diagnostics collection preference could not be applied.');
    }
  }

  static Future<void> recordSummary(
    Map<String, dynamic> sync, {
    required bool refresh,
  }) async {
    final sections = sync['sections'] as Map? ?? const {};
    for (final entry in sections.entries) {
      final value = entry.value as Map? ?? const {};
      await _emit('sync_section', {
        'section': _safeSection(entry.key),
        'outcome': _safeOutcome(value['status']),
        'item_count': _safeCount(value['count']),
        'attempted_count': _safeCount(value['attempted']),
        'failed_count': _safeCount(value['failed']),
        'duration_ms': _safeDuration(value['duration_ms']),
        'sync_mode': refresh ? 'refresh' : 'first_login',
        'parser_version': _safeCount(sync['version']),
      });
    }
    await _emit('sync_finished', {
      'outcome': _safeOutcome(sync['outcome']),
      'section_count': sections.length.clamp(0, _sections.length),
      'duration_ms': _safeDuration(sync['duration_ms']),
      'sync_mode': refresh ? 'refresh' : 'first_login',
      'parser_version': _safeCount(sync['version']),
    });
  }

  static Future<void> recordFailure({required bool refresh}) => _emit(
    'sync_finished',
    {'outcome': 'error', 'sync_mode': refresh ? 'refresh' : 'first_login'},
  );

  static Future<void> recordLoginStarted({required bool refresh}) => _emit(
    'login_flow_started',
    {'sync_mode': refresh ? 'refresh' : 'first_login'},
  );

  static Future<void> recordLoginFinished({
    required String outcome,
    required bool refresh,
    int? durationMs,
  }) => _emit('login_flow_finished', {
    'outcome': _safeOutcome(outcome),
    'sync_mode': refresh ? 'refresh' : 'first_login',
    if (durationMs != null) 'duration_ms': _safeDuration(durationMs),
  });

  static Future<void> recordResult({
    required String source,
    required String outcome,
    int? durationMs,
  }) => _emit('result_fetch_finished', {
    'result_source': _resultSources.contains(source) ? source : 'unknown',
    'outcome': _safeOutcome(outcome),
    if (durationMs != null) 'duration_ms': _safeDuration(durationMs),
  });

  static Future<void> _emit(String name, Map<String, Object> parameters) async {
    if (!_enabled) return;
    assert(() {
      debugPrint('Diagnostics: $name $parameters');
      return true;
    }());
    try {
      await _sink?.call(name, parameters);
    } catch (error) {
      // Operational diagnostics must never affect login, sync, or navigation.
      debugPrint('Diagnostics event could not be recorded.');
    }
  }

  static String _safeToken(Object? value) {
    final token = value?.toString().toLowerCase() ?? 'unknown';
    return RegExp(r'^[a-z0-9_]{1,32}$').hasMatch(token) ? token : 'unknown';
  }

  static String _safeSection(Object? value) {
    final token = _safeToken(value);
    return _sections.contains(token) ? token : 'unknown';
  }

  static String _safeOutcome(Object? value) {
    final token = _safeToken(value);
    return _outcomes.contains(token) ? token : 'unknown';
  }

  static int _safeCount(Object? value) {
    final count = int.tryParse(value?.toString() ?? '') ?? 0;
    return count.clamp(0, 1000);
  }

  static int _safeDuration(Object? value) {
    final duration = int.tryParse(value?.toString() ?? '') ?? 0;
    return duration.clamp(0, 600000);
  }
}
