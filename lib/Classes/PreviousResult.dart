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
  static List<Subject> getList(List<dynamic> data) {
    return data
        .map((e) => Subject(
            courseCode: e['COURSE CODE'],
            creditsEarned: e['Credits Earned'],
            creditsRegistered: e['Credits Reg'],
            gpa: e['GPA'],
            grade: e['Grade'],
            subjectName: e['SUBJECT NAME']))
        .toList();
  }
  // TODO : add reference examples like below
  //  {COURSE CODE: CV14, Credits Earned: 3, Credits Reg.: 3, GPA: 7, Grade: C, SUBJECT NAME: BASICS OF CIVIL ENGINEERING AND MECHANICS}
}

class PreviousResult {
  final cgpa, creditsEarned, creditsRegistered, sgpa, results, term;

  PreviousResult(
      {required this.cgpa,
      required this.creditsEarned,
      required this.creditsRegistered,
      required this.sgpa,
      required this.results,
      required this.term});
  static List<PreviousResult> getList(List<dynamic> data) {
    List<Subject> results = [];
    return data
        .map((e) => PreviousResult(
            cgpa: e['CGPA'],
            creditsEarned: e["Credits Earned"],
            creditsRegistered: e['Credits Registered'],
            sgpa: e['SGPA'],
            results: results,
            term: e['term']))
        .toList();
  }
}
