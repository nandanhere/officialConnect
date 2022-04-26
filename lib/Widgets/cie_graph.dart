import 'package:flutter/material.dart';
import 'package:official_connect/Classes/marks.dart';
import 'package:syncfusion_flutter_charts/charts.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';

class CieGraph extends StatefulWidget {
  const CieGraph({Key? key, required this.marks}) : super(key: key);
  final List<Marks> marks;

  @override
  State<CieGraph> createState() => _CieGraphState();
}

class _CieGraphState extends State<CieGraph> {
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
    final sisData = Provider.of<SisData>(context);

    return SfCartesianChart(
      onTooltipRender: (TooltipArgs args) {
        if (args.pointIndex != null) {
          args.header = widget.marks[args.pointIndex!.toInt()].subjectName;
          args.text = widget.marks[args.pointIndex!.toInt()].finalCie;
        }
      },
      tooltipBehavior: _tooltipBehavior,
      primaryXAxis: CategoryAxis(
          labelStyle: TextStyle(
              color: sisData.darkMode ? Colors.white54 : Colors.black54,
              fontSize: MediaQuery.of(context).size.width * 0.025,
              fontFamily: 'Comfortaa')),
      isTransposed: true,
      primaryYAxis: NumericAxis(minimum: 0, maximum: 50),
      series: <ChartSeries<Marks, String>>[
        BarSeries<Marks, String>(
          borderRadius: BorderRadius.only(
              topLeft: Radius.circular(7), topRight: Radius.circular(7)),
          gradient: const LinearGradient(
            begin: Alignment.topRight,
            end: Alignment.bottomLeft,
            colors: [
              Colors.blue,
              Colors.red,
            ],
          ),
          // Bind data source
          dataSource: widget.marks,
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
    );
  }
}
