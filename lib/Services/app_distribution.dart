class AppDistribution {
  static const defineName = 'OFFICIAL_CONNECT_DISTRIBUTION';
  static const _configured = String.fromEnvironment(
    defineName,
    defaultValue: 'local',
  );

  static String get channel => normalize(_configured);

  /// Production telemetry is deliberately fail-closed. A developer build,
  /// including a release-mode build made without the Play release script,
  /// must not appear in the live app's Analytics or Crashlytics data.
  static bool get allowsProductionTelemetry => channel == 'production';

  static String normalize(String value) {
    final normalized = value.trim().toLowerCase();
    return normalized == 'production' ? normalized : 'local';
  }
}
