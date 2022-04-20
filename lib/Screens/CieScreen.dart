import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:syncfusion_flutter_charts/charts.dart';
import 'package:official_connect/Screens/CieDetails.dart';
import 'package:official_connect/Classes/Marks.dart';

class CieInfo extends StatefulWidget {
  const CieInfo({Key? key}) : super(key: key);

  @override
  State<CieInfo> createState() => _CieInfoState();
}

class _CieInfoState extends State<CieInfo> {
  late TooltipBehavior _tooltipBehavior;

  @override
  void initState() {
    // documentation at https://help.syncfusion.com/flutter/cartesian-charts/tooltip for customisation.
    _tooltipBehavior = TooltipBehavior(
        enable: true,
        header: "Subject Code",
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
              SfCartesianChart(
                onTooltipRender: (TooltipArgs args) {
                  if (args.pointIndex != null) {
                    args.header =
                        sisData.marks[args.pointIndex!.toInt()].subjectName;
                    args.text =
                        sisData.marks[args.pointIndex!.toInt()].finalCie;
                  }
                },
                tooltipBehavior: _tooltipBehavior,
                primaryXAxis: CategoryAxis(),
                isTransposed: true,
                primaryYAxis: NumericAxis(minimum: 0, maximum: 50),
                series: <ChartSeries<Marks, String>>[
                  BarSeries<Marks, String>(
                    gradient: const LinearGradient(
                      begin: Alignment.topRight,
                      end: Alignment.bottomLeft,
                      colors: [
                        Colors.blue,
                        Colors.red,
                      ],
                    ),
                    // Bind data source
                    dataSource: sisData.marks,
                    xValueMapper: (Marks a, _) =>
                        RegExp(r'\((.*)\)').firstMatch(a.subjectName)!.group(1),
                    yValueMapper: (Marks b, _) =>
                        // int.parse(b.finalCie.split('/').first))
                        double.parse((b.finalCie.contains('%'))
                                ? b.finalCie.replaceAll('%', "")
                                : b.finalCie.split('/').first)
                            .round(),
                    enableTooltip: true,
                  )
                ],
              ),
              ...sisData.marks
                  .map((e) => Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: NeumorphicButton(
                          padding: EdgeInsets.only(
                              top: height * 0.015,
                              bottom: height * 0.015,
                              left: width * 0.025,
                              right: width * 0.01),
                          onPressed: () {
                            Navigator.of(context).push(MaterialPageRoute(
                                builder: (ctx) =>
                                    CieDetails(subjectDetails: e)));
                          },
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
                              e.finalCie,
                              style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: Colors.black,
                                  fontSize: 20,
                                  fontFamily: 'Comfortaa'),
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
