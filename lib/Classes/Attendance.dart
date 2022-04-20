import 'package:intl/intl.dart';

class ClassDay {
  // index is so that the dates come in "latest first" order
  final int index;
  final DateTime date;
  final String time;
  final String status;

  ClassDay(
      {required this.index,
      required this.date,
      required this.time,
      required this.status});
  static List<ClassDay> getList(List<dynamic> data) {
    return data
        .map((e) => ClassDay(
            index: int.parse(e['index']),
            date: DateFormat('dd-MM-yyyy').parse(e['date']),
            time: e['time'],
            status: e['status']))
        .toList();
  }
}

class Attendance {
  final int absent;
  final List<ClassDay> absentDates;
  final String code;
  final String subjectName;
  final String percentage;
  final int present;
  final List<ClassDay> presentDates;
  final int remaining;
  final String teacher;

  Attendance(
      {required this.absent,
      required this.code,
      required this.subjectName,
      required this.percentage,
      required this.present,
      required this.remaining,
      required this.teacher,
      required this.absentDates,
      required this.presentDates});
  static List<Attendance> getList(List<dynamic> data) {
    final list = data.map((e) {
      List<ClassDay> presentDates = ClassDay.getList(e['present_dates']);
      List<ClassDay> absentDates = ClassDay.getList(e['absent_dates']);
      return Attendance(
          absent: int.parse(e['absent']),
          code: e['code'],
          subjectName: e['name'],
          percentage: e['percentage'],
          present: int.parse(e['present']),
          remaining: int.parse(e['remaining']),
          teacher: e['teacher'],
          absentDates: absentDates,
          presentDates: presentDates);
    }).toList();

    list.sort((a, b) => a.code.compareTo(b.code));
    return list;
  }

  int howManyCanIMiss(int forPercent) {
    if (forPercent == 75) {}
    if (forPercent == 80) {}
    return 0;
  }
}
