import 'dart:math';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:official_connect/Classes/Marks.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:provider/provider.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

class CieDetails extends StatelessWidget {
  final Marks subjectDetails;
  const CieDetails({Key? key, required this.subjectDetails}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final data = [
      [subjectDetails.t1, "t1"],
      [subjectDetails.t2, "t2"],
      [subjectDetails.a1, "a1"],
      [subjectDetails.a2, "a2"]
    ];
    print(data);
    print(subjectDetails.subjectName);
    return Scaffold(
      appBar: AppBar(
        title: const Text("Cie details"),
      ),
      body: Center(
        child: SingleChildScrollView(
          child: Column(
            children: [
              Text(subjectDetails.subjectName),
              SfCartesianChart(
                primaryXAxis: CategoryAxis(),
                isTransposed: true,
                primaryYAxis: NumericAxis(
                    minimum: 0,
                    maximum: data
                        .map((e) => double.tryParse(e[0].split('/').first) ?? 0)
                        .toList()
                        .reduce(max)),
                series: <ChartSeries<List<String>, String>>[
                  BarSeries<List<String>, String>(
                    gradient: const LinearGradient(
                      begin: Alignment.topRight,
                      end: Alignment.bottomLeft,
                      colors: [
                        Colors.blue,
                        Colors.red,
                      ],
                    ),
                    // Bind data source
                    dataSource: data,
                    xValueMapper: (e, _) => e[1],
                    yValueMapper: (e, _) =>
                        int.tryParse(e[0].split("/").first) ?? 0,
                  )
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
