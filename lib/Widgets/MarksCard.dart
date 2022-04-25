import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:official_connect/Classes/Marks.dart';
import 'package:official_connect/Classes/PreviousResult.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/ResultsDetails.dart';
import 'package:provider/provider.dart';

class MarksCard extends StatelessWidget {
  final List<Subject> subjects;
  const MarksCard({Key? key, required this.subjects}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);

    final heads = ["Subject", "Earned", "GPA"];
    const TextStyle headingStyle = const TextStyle(
      fontWeight: FontWeight.bold,
      fontFamily: 'Comfortaa',
    );
    const TextStyle bodyStyle = const TextStyle(
      fontWeight: FontWeight.w400,
      fontFamily: 'Comfortaa',
    );
    return Theme(
      data: sisData.darkMode ? ThemeData.dark() : ThemeData.light(),
      child: DataTable(
        dataRowHeight: 100,
        columnSpacing: 20,
        columns: [
          ...heads.map((element) {
            return DataColumn(
                label: Text(
              element,
              style: headingStyle,
            ));
          }).toList()
        ],
        rows: [
          ...subjects.map((e) {
            return DataRow(cells: [
              DataCell(
                Text(
                  "${e.subjectName} (${e.courseCode})",
                  style: bodyStyle,
                ),
              ),
              DataCell(
                Text("${e.creditsEarned} / ${e.creditsRegistered}",
                    style: bodyStyle),
              ),
              DataCell(
                Text("${e.gpa} (${e.grade})", style: bodyStyle),
              ),
            ]);
          }).toList(),
        ],
      ),
    );
  }
}
