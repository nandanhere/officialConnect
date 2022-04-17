import 'dart:math';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:official_connect/Classes/Marks.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

class CieDetails extends StatelessWidget {
  final Marks subjectDetails;
  const CieDetails({Key? key, required this.subjectDetails}) : super(key: key);

  @override
  Widget build(BuildContext context) {
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
        foregroundColor: const Color(0xFF852528),
        backgroundColor: Colors.white,
        title: Text(
          "Cie details",
          style: TextStyle(
              color: const Color(0xFF852528),
              fontSize: MediaQuery.of(context).size.width * 0.06,
              fontFamily: 'Comfortaa'),
        ),
      ),
      body: Center(
        child: SingleChildScrollView(
          child: Column(
            children: [
              Text(subjectDetails.subjectName,
                  style: TextStyle(
                      color: Colors.black,
                      fontSize: MediaQuery.of(context).size.width * 0.05,
                      fontFamily: 'Comfortaa')),
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
