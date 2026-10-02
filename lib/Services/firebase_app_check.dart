import 'package:firebase_app_check/firebase_app_check.dart' as app_check;
import 'package:flutter/foundation.dart';

// Client-side App Check enrolment. Enforcement stays OFF server-side until
// a later release, so activation only starts minting attestation tokens
// without changing any request behavior.
class FirebaseAppCheckSetup {
  static app_check.AndroidAppCheckProvider androidProvider({
    required bool debug,
  }) => debug
      ? const app_check.AndroidDebugProvider()
      : const app_check.AndroidPlayIntegrityProvider();

  static app_check.AppleAppCheckProvider appleProvider({required bool debug}) =>
      debug
          ? const app_check.AppleDebugProvider()
          : const app_check.AppleAppAttestProvider();

  static Future<void> initialize() async {
    if (kIsWeb) return;
    try {
      await app_check.FirebaseAppCheck.instance.activate(
        providerAndroid: androidProvider(debug: kDebugMode),
        providerApple: appleProvider(debug: kDebugMode),
      );
    } catch (_) {
      debugPrint('App Check is unavailable in this build.');
    }
  }
}
