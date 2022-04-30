class Subject {
  final String courseCode,
      creditsEarned,
      creditsRegistered,
      gpa,
      grade,
      subjectName;

  Subject(
      {required this.courseCode,
      required this.creditsEarned,
      required this.creditsRegistered,
      required this.gpa,
      required this.grade,
      required this.subjectName});
  static List<Subject> getList(List<Map<String, dynamic>> data) {
    final list = data
        .map((e) => Subject(
            courseCode: e['COURSE CODE'],
            creditsEarned: e['Credits Earned'].toString(),
            creditsRegistered: e['Credits Reg.'].toString(),
            gpa: e['GPA'].toString(),
            grade: e['Grade'].toString(),
            subjectName: e['SUBJECT NAME'].toString()))
        .toList();
    list.sort((a, b) => a.courseCode.compareTo(b.courseCode));
    return list;
  }
  // example code:
  //  {COURSE CODE: CV14, Credits Earned: 3, Credits Reg.: 3, GPA: 7, Grade: C, SUBJECT NAME: BASICS OF CIVIL ENGINEERING AND MECHANICS}
}

class PreviousResult {
  // ignore: prefer_typing_uninitialized_variables
  final cgpa, creditsEarned, creditsRegistered, sgpa, term, semesterNumber;
  final List<Subject> results;

  PreviousResult(
      {required this.cgpa,
      required this.creditsEarned,
      required this.creditsRegistered,
      required this.sgpa,
      required this.results,
      required this.term,
      required this.semesterNumber});
  static List<PreviousResult> getList(List<dynamic> data) {
    return data
        .map(
          (e) => PreviousResult(
              cgpa: e['CGPA'],
              creditsEarned: e["Credits Earned "],
              creditsRegistered: e['Credits Registered '],
              sgpa: e['SGPA'],
              results: Subject.getList(
                  List<Map<String, dynamic>>.from(e['results'])),
              term: e['term'],
              semesterNumber: (data.indexOf(e) + 1).toString()),
        )
        .toList();
  }
}
