import 'package:flutter/material.dart';
import 'package:official_connect/Classes/Marks.dart';
import 'package:syncfusion_flutter_charts/charts.dart';
import 'dart:math';

class CieDetailsGraph extends StatefulWidget {
  const CieDetailsGraph({Key? key, required this.subjectDetails})
      : super(key: key);
  final Marks subjectDetails;
  @override
  State<CieDetailsGraph> createState() => _CieDetailsGraphState();
}

class _CieDetailsGraphState extends State<CieDetailsGraph> {
  late TooltipBehavior _tooltipBehavior;

  @override
  void initState() {
    // documentation at https://help.syncfusion.com/flutter/cartesian-charts/tooltip for customisation.
    _tooltipBehavior = TooltipBehavior(
        enable: true,
        header: "Test/Quiz",
        tooltipPosition: TooltipPosition.pointer);
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    final data = [
      [widget.subjectDetails.t1, "t1"],
      [widget.subjectDetails.t2, "t2"],
      [widget.subjectDetails.a1, "a1"],
      [widget.subjectDetails.a2, "a2"]
    ];
    return SfCartesianChart(
      tooltipBehavior: _tooltipBehavior,
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
          yValueMapper: (e, _) => int.tryParse(e[0].split("/").first) ?? 0,
        )
      ],
    );
  }
}
