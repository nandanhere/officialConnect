class SeatingArrangement {
  const SeatingArrangement({
    required this.date,
    required this.courseCode,
    required this.courseName,
    required this.timing,
    required this.session,
    required this.block,
    required this.room,
  });

  final String date;
  final String courseCode;
  final String courseName;
  final String timing;
  final String session;
  final String block;
  final String room;

  factory SeatingArrangement.fromMap(Map<dynamic, dynamic> value) =>
      SeatingArrangement(
        date: value['date']?.toString() ?? '',
        courseCode: value['course_code']?.toString() ?? '',
        courseName: value['course_name']?.toString() ?? '',
        timing: value['timing']?.toString() ?? '',
        session: value['session']?.toString() ?? '',
        block: value['block']?.toString() ?? '',
        room: _cleanRoom(value['room']?.toString() ?? ''),
      );

  static List<SeatingArrangement> getList(Object? values) => values is List
      ? values
            .whereType<Map>()
            .map(SeatingArrangement.fromMap)
            .where((entry) => entry.courseName.isNotEmpty)
            .toList()
      : const [];

  DateTime? get parsedDate => DateTime.tryParse(date);
}

String _cleanRoom(String value) => value
    .replaceFirst(
      RegExp(
        r'\s+(?:Contineo|Terms of Service|Privacy Policy)\b.*$',
        caseSensitive: false,
      ),
      '',
    )
    .replaceFirst(RegExp(r'\s+Copyright.*$', caseSensitive: false), '')
    .trim();
