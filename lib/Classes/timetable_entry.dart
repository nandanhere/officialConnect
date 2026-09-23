class TimetableEntry {
  const TimetableEntry({
    required this.date,
    required this.day,
    required this.time,
    required this.code,
    required this.name,
    required this.faculty,
    required this.room,
    required this.batch,
  });

  final String date;
  final String day;
  final String time;
  final String code;
  final String name;
  final String faculty;
  final String room;
  final String batch;

  factory TimetableEntry.fromMap(Map<dynamic, dynamic> value) => TimetableEntry(
    date: value['date']?.toString() ?? '',
    day: value['day']?.toString() ?? '',
    time: value['time']?.toString() ?? '',
    code: value['code']?.toString() ?? '',
    name: value['name']?.toString() ?? '',
    faculty: value['faculty']?.toString() ?? '',
    room: value['room']?.toString() ?? '',
    batch: value['batch']?.toString() ?? '',
  );

  static List<TimetableEntry> getList(Object? values) => values is List
      ? values
            .whereType<Map>()
            .map(TimetableEntry.fromMap)
            .where((entry) => entry.time.isNotEmpty && entry.name.isNotEmpty)
            .toList()
      : const [];
}
