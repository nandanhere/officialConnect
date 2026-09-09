import 'package:flutter/foundation.dart';

typedef DiagnosticsEventSink =
    Future<void> Function(String name, Map<String, Object> parameters);
typedef DiagnosticsCollectionToggle = Future<void> Function(bool enabled);

/// Emits only aggregate synchronization health. The production analytics sink
/// is attached during app startup; debug builds remain useful without it.
class SyncDiagnostics {
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
    await _collectionToggle?.call(enabled);
  }

  static Future<void> recordSummary(
    Map<String, dynamic> sync, {
    required bool refresh,
  }) async {
    final sections = sync['sections'] as Map? ?? const {};
    for (final entry in sections.entries) {
      final value = entry.value as Map? ?? const {};
      await _emit('sync_section', {
        'section': _safeToken(entry.key),
        'outcome': _safeToken(value['status']),
        'item_count': _safeCount(value['count']),
        'attempted_count': _safeCount(value['attempted']),
        'failed_count': _safeCount(value['failed']),
        'duration_ms': _safeDuration(value['duration_ms']),
        'sync_mode': refresh ? 'refresh' : 'first_login',
        'parser_version': _safeCount(sync['version']),
      });
    }
    await _emit('sync_finished', {
      'outcome': _safeToken(sync['outcome']),
      'section_count': sections.length,
      'duration_ms': _safeDuration(sync['duration_ms']),
      'sync_mode': refresh ? 'refresh' : 'first_login',
      'parser_version': _safeCount(sync['version']),
    });
  }

  static Future<void> recordFailure({required bool refresh}) => _emit(
    'sync_finished',
    {'outcome': 'error', 'sync_mode': refresh ? 'refresh' : 'first_login'},
  );

  static Future<void> _emit(String name, Map<String, Object> parameters) async {
    if (!_enabled) return;
    assert(() {
      debugPrint('Diagnostics: $name $parameters');
      return true;
    }());
    await _sink?.call(name, parameters);
  }

  static String _safeToken(Object? value) {
    final token = value?.toString().toLowerCase() ?? 'unknown';
    return RegExp(r'^[a-z0-9_]{1,32}$').hasMatch(token) ? token : 'unknown';
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
