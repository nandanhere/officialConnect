import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'package:flutter/foundation.dart';

class FirebaseCrashReporting {
  static FlutterExceptionHandler? _previousFlutterHandler;
  static bool Function(Object, StackTrace)? _previousPlatformHandler;
  static bool _handlersCaptured = false;
  static bool _enabled = false;

  static void _captureHandlers() {
    if (_handlersCaptured) return;
    _previousFlutterHandler = FlutterError.onError;
    _previousPlatformHandler = PlatformDispatcher.instance.onError;
    _handlersCaptured = true;
  }

  static Future<void> initialize({required bool enabled}) async {
    _captureHandlers();
    await setEnabled(enabled);
  }

  static Future<void> setEnabled(bool enabled) async {
    _captureHandlers();
    _enabled = enabled;
    try {
      final crashlytics = FirebaseCrashlytics.instance;
      await crashlytics.setCrashlyticsCollectionEnabled(enabled);
      if (!enabled) {
        FlutterError.onError = _previousFlutterHandler;
        PlatformDispatcher.instance.onError = _previousPlatformHandler;
        return;
      }

      FlutterError.onError = (details) {
        (_previousFlutterHandler ?? FlutterError.presentError)(details);
        // Framework errors can be recoverable (for example a failed widget
        // frame). Record them without claiming that Android terminated.
        crashlytics.recordFlutterError(details);
      };
      PlatformDispatcher.instance.onError = (error, stack) {
        // Returning true keeps the isolate alive, so this is non-fatal by
        // definition. Native process crashes are captured by the SDK itself.
        crashlytics.recordError(error, stack, fatal: false);
        return true;
      };
    } catch (_) {
      debugPrint('Crash reporting preference could not be applied.');
    }
  }

  static Future<void> setContext(Map<String, String> values) async {
    if (!_enabled) return;
    try {
      final crashlytics = FirebaseCrashlytics.instance;
      for (final entry in values.entries) {
        await crashlytics.setCustomKey(entry.key, entry.value);
      }
    } catch (_) {
      debugPrint('Crash context could not be updated.');
    }
  }
}
