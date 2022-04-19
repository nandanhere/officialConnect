import 'package:flutter/material.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:provider/provider.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

late TooltipBehavior _tooltipBehavior;

class AttendanceInfo extends StatefulWidget {
  const AttendanceInfo({Key? key}) : super(key: key);

  @override
  State<AttendanceInfo> createState() => _AttendanceInfoState();
}

class _AttendanceInfoState extends State<AttendanceInfo> {
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
    final height = size.height;
    final sisData = Provider.of<SisData>(context);

    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(width * 0.08),
        color: NeumorphicColors.background,
      ),
      padding: EdgeInsets.only(
          left: width * 0.05,
          right: width * 0.05,
          top: height * 0.06,
          bottom: height * 0.13),
      child: Center(
        child: SingleChildScrollView(
          child: Column(
            children: [
              SizedBox(
                height: height * 0.5,
                child: SfCircularChart(
                  onTooltipRender: (TooltipArgs args) {
                    if (args.pointIndex != null)
                      args.header = sisData
                          .attendances[args.pointIndex!.toInt()].subjectName;
                  },
                  tooltipBehavior: _tooltipBehavior,
                  series: <CircularSeries>[
                    RadialBarSeries(
                      maximumValue: 100,
                      dataSource: sisData.attendances.map(
                        (e) {
                          return [
                            int.parse(e.percentage.replaceFirst("%", "")),
                            e.code
                          ];
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
              ),
              ...sisData.attendances
                  .map((e) => Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: NeumorphicButton(
                          padding: EdgeInsets.only(
                              top: height * 0.015,
                              bottom: height * 0.015,
                              left: width * 0.025,
                              right: width * 0.01),
                          onPressed: () => print("attendance details"),
                          style: NeumorphicStyle(
                              depth: 3,
                              boxShape: NeumorphicBoxShape.roundRect(
                                  BorderRadius.circular(20))),
                          child: ListTile(
                            title: Text(
                              e.subjectName,
                              style: const TextStyle(
                                  color: Colors.black,
                                  fontSize: 16,
                                  fontFamily: 'Comfortaa'),
                            ),
                            trailing: Text(
                              e.percentage,
                              style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: Colors.black,
                                  fontSize: 20,
                                  fontFamily: 'Comfortaa'),
                              textAlign: TextAlign.end,
                            ),
                          ),
                        ),
                      ))
                  .toList()
            ],
          ),
        ),
      ),
    );
  }
}
