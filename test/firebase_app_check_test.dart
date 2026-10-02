import 'package:firebase_app_check/firebase_app_check.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:official_connect/Services/firebase_app_check.dart';

void main() {
  test('debug builds use the debug providers', () {
    expect(
      FirebaseAppCheckSetup.androidProvider(debug: true),
      isA<AndroidDebugProvider>(),
    );
    expect(
      FirebaseAppCheckSetup.appleProvider(debug: true),
      isA<AppleDebugProvider>(),
    );
  });

  test('release builds use Play Integrity and App Attest', () {
    expect(
      FirebaseAppCheckSetup.androidProvider(debug: false),
      isA<AndroidPlayIntegrityProvider>(),
    );
    expect(
      FirebaseAppCheckSetup.appleProvider(debug: false),
      isA<AppleAppAttestProvider>(),
    );
  });
}
