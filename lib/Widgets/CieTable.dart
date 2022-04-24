import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:official_connect/Classes/Marks.dart';

class CieTable extends StatelessWidget {
  final Marks marks;
  const CieTable({Key? key, required this.marks}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return DataTable(
      columns: [
        const DataColumn(
          label: Text("Test/Assignment"),
        ),
        const DataColumn(
          label: Text("Score"),
        )
      ],
      rows: [
        DataRow(cells: [
          const DataCell(Text('Cie 1')),
          DataCell(Text(marks.t1)),
        ]),
        DataRow(cells: [
          const DataCell(Text('Cie 2')),
          DataCell(Text(marks.t2)),
        ]),
        DataRow(cells: [
          const DataCell(const Text('Assignment 1')),
          DataCell(Text(marks.a1)),
        ]),
        DataRow(cells: [
          const DataCell(Text('Assignment 2')),
          DataCell(Text(marks.a2)),
        ]),
      ],
    );
  }
}
