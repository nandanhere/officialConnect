import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:official_connect/Classes/Marks.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/CieDetails.dart';
import 'package:provider/provider.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

class CieScreen extends StatelessWidget {
  static const String id = "cie";
  const CieScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final sisData = Provider.of<SisData>(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text("Cie details"),
      ),
      body: Center(
        child: SingleChildScrollView(
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
                  .map((e) => SizedBox(
                        width: size.width * .95,
                        height: size.height * .2,
                        child: Card(
                          child: ListTile(
                            onTap: () {
                              Navigator.of(context).push(MaterialPageRoute(
                                  builder: (ctx) =>
                                      CieDetails(subjectDetails: e)));
                            },
                            title: Text(e.subjectName),
                            subtitle: Text(
                              e.finalCie,
                              style: const TextStyle(fontSize: 20),
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
