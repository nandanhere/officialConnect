import 'package:flutter/widgets.dart';
import 'package:flutter/material.dart';
import 'package:official_connect/Classes/attendance.dart';
import 'package:syncfusion_flutter_charts/charts.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';

class AttendanceGraph extends StatefulWidget {
  const AttendanceGraph(
      {Key? key,
      required this.height,
      required this.width,
      required this.attendances})
      : super(key: key);
  final double height, width;
  final List<Attendance> attendances;

  @override
  State<AttendanceGraph> createState() => _AttendanceGraphState();
}

class _AttendanceGraphState extends State<AttendanceGraph> {
  late TooltipBehavior _tooltipBehavior;

  @override
  void initState() {
    // documentation at https://help.syncfusion.com/flutter/circular-charts/tooltip for more customisation
    _tooltipBehavior = TooltipBehavior(
        enable: true,
        format: "point.x : point.y%",
        tooltipPosition: TooltipPosition.pointer);
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final sisData = Provider.of<SisData>(context);
    return SizedBox(
      height: widget.height * 0.5,
      child: SfCircularChart(
        legend: Legend(
            isVisible: true,
            toggleSeriesVisibility: true,
            textStyle: TextStyle(
                color: sisData.darkMode ? Colors.white : Colors.black,
                fontSize: width * 0.04,
                fontFamily: 'Comfortaa'),
            position: LegendPosition.bottom,
            overflowMode: LegendItemOverflowMode.wrap),
        onTooltipRender: (TooltipArgs args) {
          if (args.pointIndex != null) {
            args.header =
                widget.attendances[args.pointIndex!.toInt()].subjectName;
          }
        },
        tooltipBehavior: _tooltipBehavior,
        series: <CircularSeries>[
          RadialBarSeries(
            maximumValue: 100,
            dataSource: widget.attendances.map(
              (e) {
                return [int.parse(e.percentage.replaceFirst("%", "")), e.code];
              },
            ).toList(),
            pointRadiusMapper: (data, _) => data[1],
            xValueMapper: (a, b) => a[1],
            yValueMapper: (a, b) => a[0],
            cornerStyle: CornerStyle.bothCurve,
            enableTooltip: true,
          )
        ],
      ),
    );
  }
}
