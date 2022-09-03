import 'package:flutter/material.dart';
import 'package:official_connect/Classes/previous_result.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:provider/provider.dart';

class MarksCard extends StatelessWidget {
  final bool isBackLog;
  final List<Subject> subjects;
  const MarksCard({Key? key, required this.subjects, required this.isBackLog})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final heads = isBackLog
        ? ["Subject", "Credits", "Attempts"]
        : ["Subject", "Earned", "GPA"];
    const TextStyle headingStyle = TextStyle(
      fontWeight: FontWeight.bold,
      fontFamily: 'Comfortaa',
    );
    const TextStyle bodyStyle = TextStyle(
      fontWeight: FontWeight.w400,
      fontFamily: 'Comfortaa',
    );
    return Theme(
      data: sisData.darkMode ? ThemeData.dark() : ThemeData.light(),
      child: FittedBox(
        fit: BoxFit.fitWidth,
        child: SingleChildScrollView(
          child: DataTable(
            // horizontalMargin: width*0.05,
            dataRowHeight: height * 0.37, //100
            columnSpacing: width * 0.37, //20
            columns: [
              ...heads.map((element) {
                return DataColumn(
                    label: Text(
                  element,
                  style: headingStyle.copyWith(fontSize: 40),
                ));
              }).toList()
            ],
            rows: [
              ...subjects.map((e) {
                return DataRow(cells: [
                  DataCell(
                    Text(
                      "${e.subjectName} (${e.courseCode})",
                      style: bodyStyle.copyWith(fontSize: 40),
                    ),
                  ),
                  DataCell(
                    Text(
                      isBackLog
                          ? e.creditsRegistered
                          : "${e.creditsEarned} / ${e.creditsRegistered}",
                      style: bodyStyle.copyWith(fontSize: 40),
                    ),
                  ),
                  DataCell(
                    Text(
                      isBackLog ? e.gpa : "${e.gpa} (${e.grade})",
                      style: bodyStyle.copyWith(fontSize: 40),
                    ),
                  ),
                ]);
              }).toList(),
            ],
          ),
        ),
      ),
    );
  }
}
