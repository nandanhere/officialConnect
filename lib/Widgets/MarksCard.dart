import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:official_connect/Classes/Marks.dart';
import 'package:official_connect/Classes/PreviousResult.dart';
import 'package:official_connect/Screens/ResultsDetails.dart';

class MarksCard extends StatelessWidget {
  final List<Subject> subjects;
  const MarksCard({Key? key, required this.subjects}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final heads = ["Subject", "earned", "GPA"];
    return DataTable(
      dataRowHeight: 100,
      columnSpacing: 30,
      columns: [
        ...heads.map((element) {
          return DataColumn(label: Text(element));
        }).toList()
      ],
      rows: [
        ...subjects.map((e) {
          return DataRow(cells: [
            DataCell(
              Text(
                "${e.subjectName} (${e.courseCode})",
              ),
            ),
            DataCell(
              Text("${e.creditsEarned} / ${e.creditsRegistered}"),
            ),
            DataCell(
              Text("${e.gpa} (${e.grade})"),
            ),
          ]);
        }).toList(),
      ],
    );
  }
}
