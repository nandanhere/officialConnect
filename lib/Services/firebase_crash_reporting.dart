import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'package:flutter/foundation.dart';

class FirebaseCrashReporting {
  static FlutterExceptionHandler? _previousFlutterHandler;
  static bool Function(Object, StackTrace)? _previousPlatformHandler;
  static bool _handlersCaptured = false;

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
    try {
      final crashlytics = FirebaseCrashlytics.instance;
      await crashlytics.setCrashlyticsCollectionEnabled(enabled);
      if (!enabled) {
        FlutterError.onError = _previousFlutterHandler;
        PlatformDispatcher.instance.onError = _previousPlatformHandler;
        return;
      }

      FlutterError.onError = crashlytics.recordFlutterFatalError;
      PlatformDispatcher.instance.onError = (error, stack) {
        crashlytics.recordError(error, stack, fatal: true);
        return true;
      };
    } catch (_) {
      debugPrint('Crash reporting preference could not be applied.');
    }
  }
}
