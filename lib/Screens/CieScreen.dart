import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:official_connect/Widgets/CieGraph.dart';
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
              CieGraph(marks: sisData.marks),
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
