import 'package:flutter_test/flutter_test.dart';
import 'package:official_connect/Classes/attendance.dart';
import 'package:official_connect/Screens/login_screen/student_home/attendance_screen/attendance_details/widgets/attendance_details_calender_version.dart';

ClassDay day({
  required int index,
  required DateTime date,
  required String time,
  required String status,
}) => ClassDay(index: index, date: date, time: time, status: status);

void main() {
  test('two slots on one day are both kept', () {
    final date = DateTime(2026, 9, 15);
    final grouped = groupDaySlots(
      presentDates: [
        day(index: 2, date: date, time: '09:00-10:50', status: 'Present'),
      ],
      absentDates: [
        day(index: 1, date: date, time: '11:05 - 12:00', status: 'Absent'),
      ],
    );

    final slots = grouped[DateTime(2026, 9, 15)]!;
    expect(slots.map((slot) => slot.time), [
      '09:00-10:50',
      '11:05 - 12:00',
    ]);
    expect(dayStatus(slots), 0);
  });

  test('all-attended day stays present, empty day has no status', () {
    final date = DateTime(2026, 9, 16);
    final grouped = groupDaySlots(
      presentDates: [
        day(index: 1, date: date, time: '09:00-10:50', status: 'Present'),
      ],
      absentDates: const [],
    );

    expect(dayStatus(grouped[DateTime(2026, 9, 16)]!), 1);
    expect(dayStatus(const []), -1);
  });

  test('slots group by calendar day regardless of timestamp', () {
    final grouped = groupDaySlots(
      presentDates: [
        day(
          index: 1,
          date: DateTime(2026, 9, 15, 14, 30),
          time: '09:00-10:50',
          status: 'Present',
        ),
      ],
      absentDates: [
        day(
          index: 2,
          date: DateTime(2026, 9, 15, 8, 5),
          time: '11:05 - 12:00',
          status: 'Absent',
        ),
      ],
    );

    expect(grouped.keys, [DateTime(2026, 9, 15)]);
    expect(grouped.values.single, hasLength(2));
  });
}
