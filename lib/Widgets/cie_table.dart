import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:official_connect/Classes/marks.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:provider/provider.dart';

class CieTable extends StatelessWidget {
  final Marks marks;
  const CieTable({Key? key, required this.marks}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
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
      child: DataTable(
        columns: [
          const DataColumn(
            label: Text(
              "Test/Assignment",
              style: headingStyle,
            ),
          ),
          const DataColumn(
            label: Text("Score", style: headingStyle),
          )
        ],
        rows: [
          DataRow(cells: [
            const DataCell(Text(
              'Cie 1',
              style: bodyStyle,
            )),
            DataCell(Text(
              marks.t1,
              style: bodyStyle,
            )),
          ]),
          DataRow(cells: [
            const DataCell(Text(
              'Cie 2',
              style: bodyStyle,
            )),
            DataCell(Text(
              marks.t2,
              style: bodyStyle,
            )),
          ]),
          DataRow(cells: [
            const DataCell(Text(
              'Assignment 1',
              style: bodyStyle,
            )),
            DataCell(Text(
              marks.a1,
              style: bodyStyle,
            )),
          ]),
          DataRow(cells: [
            const DataCell(Text(
              'Assignment 2',
              style: bodyStyle,
            )),
            DataCell(Text(
              marks.a2,
              style: bodyStyle,
            )),
          ]),
        ],
      ),
    );
  }
}
