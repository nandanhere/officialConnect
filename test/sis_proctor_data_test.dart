import 'package:flutter_test/flutter_test.dart';
import 'package:official_connect/Classes/sis_proctor_data.dart';

void main() {
  test('proctorData tolerates legacy list caches without throwing', () {
    // Past error/disabled syncs persisted proctorship as []; opening the
    // proctor screen from such a cache must not crash setVariables.
    final dynamic legacyCache = <dynamic>[];
    final data = SisProctorData.proctorData(legacyCache);
    expect(data.messages, isEmpty);
    expect(data.name, 'Not given');
    expect(data.phone, 'Not given');
  });

  test('proctorData tolerates maps with missing keys', () {
    final data = SisProctorData.proctorData(<String, dynamic>{});
    expect(data.messages, isEmpty);
    expect(data.name, 'Not given');
  });
}
