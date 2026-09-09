// ignore_for_file: prefer_typing_uninitialized_variables

import 'package:flutter/material.dart';

class Subject {
  final courseCode, creditsEarned, creditsRegistered, gpa, grade, subjectName;

  Subject(
      {required this.courseCode,
      required this.creditsEarned,
      required this.creditsRegistered,
      required this.gpa,
      required this.grade,
      required this.subjectName});
  static List<Subject> getList(List<Map<String, dynamic>> data) {
    final list = data
        .where((element) => element['COURSE CODE'].toString().trim() != "")
        .map((e) {
      // print(e.keys);
      bool isBack = e.containsKey("COURSE NAME");
      return Subject(
        courseCode: e['COURSE CODE'],
        creditsEarned: e['Credits Earned'].toString(),
        creditsRegistered: isBack ? e['Credits'] : e['Credits Reg.'].toString(),
        gpa: isBack ? e["Attempts"] : e['GPA'].toString(),
        grade: e['Grade'].toString(),
        subjectName: isBack ? e['COURSE NAME'] : e['SUBJECT NAME'].toString(),
      );
    }).toList();
    list.sort((a, b) => a.courseCode.compareTo(b.courseCode));
    return list;
  }
  // example code:
  //  {COURSE CODE: CV14, Credits Earned: 3, Credits Reg.: 3, GPA: 7, Grade: C, SUBJECT NAME: BASICS OF CIVIL ENGINEERING AND MECHANICS}
}

class PreviousResult {
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
    var semstart = 0;
    var cgpa = "";
    try {
      return data.map((e) {
        String term = e['term'].toString().toLowerCase();
        cgpa = term.contains('back') ? cgpa : e['CGPA'];
        return PreviousResult(
            cgpa: cgpa,
            creditsEarned: e["Credits Earned "],
            creditsRegistered: e['Credits Registered '],
            sgpa: e['SGPA'],
            results:
                Subject.getList(List<Map<String, dynamic>>.from(e['results'])),
            term: e['term'],
            semesterNumber:
                (term.contains('supplementary') || term.contains('back'))
                    ? semstart
                    : ++semstart
            // semesterNumber: (data.indexOf(e) + 1).toString(),
            );
      }).toList();
    } catch (e) {
      debugPrint(e.toString());
    }
    return [];
  }
}
