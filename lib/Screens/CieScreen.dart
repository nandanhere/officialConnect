import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:syncfusion_flutter_charts/charts.dart';
import 'package:official_connect/Screens/CieDetails.dart';
import 'package:official_connect/Classes/Marks.dart';

class CieInfo extends StatelessWidget {
  const CieInfo({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final sisData = Provider.of<SisData>(context);
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(30),
        color: NeumorphicColors.background,
      ),
      padding: EdgeInsets.symmetric(horizontal: 20, vertical: 20),
      child: Center(
        child: SingleChildScrollView(
          padding: EdgeInsets.only(
              bottom: size.height * 0.1, top: size.height * 0.04),
          child: Column(
            children: [
              SfCartesianChart(
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
                      xValueMapper: (Marks a, _) => RegExp(r'\((.*)\)')
                          .firstMatch(a.subjectName)!
                          .group(1),
                      yValueMapper: (Marks b, _) =>
                          int.parse(b.finalCie.split('/').first))
                ],
              ),
              ...sisData.marks
                  .map((e) => Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: NeumorphicButton(
                          padding: EdgeInsets.only(
                              top: 10, bottom: 10, left: 10, right: 2),
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
