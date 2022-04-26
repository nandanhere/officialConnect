import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Widgets/AttendanceGraph.dart';
import 'package:provider/provider.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import './AttendanceDetails.dart';
import 'package:official_connect/Providers/Themes.dart';

class AttendanceInfo extends StatelessWidget {
  const AttendanceInfo({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final sisData = Provider.of<SisData>(context);
    final buttonTitle = CustomTheme.buttonTitle(context);
    final buttonTrailing = CustomTheme.buttonTrailing(context);
    final titleStyle = CustomTheme.titleStyle(context);
    final neumorphicStyle = CustomTheme.neumorphicStyle(context);
    final linearGradient = CustomTheme.linearGradient(context);

    return Container(
      decoration: BoxDecoration(
        gradient: linearGradient,
      ),
      padding: EdgeInsets.only(
          left: width * 0.05,
          right: width * 0.05,
          top: height * 0.06,
          bottom: height * 0.13),
      child: Center(
        child: SingleChildScrollView(
          physics: const BouncingScrollPhysics(),
          child: Column(
            children: [
              AutoSizeText(
                "Attendance Info",
                style: titleStyle,
              ),
              AttendanceGraph(
                  height: height,
                  width: width,
                  attendances: sisData.attendances),
              ...sisData.attendances
                  .map((e) => Padding(
                        //map
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
                                    AttendanceDetails(attendanceDetails: e)));
                          },
                          style: neumorphicStyle,
                          child: ListTile(
                            title: Text(e.subjectName, style: buttonTitle),
                            subtitle: Text("(${e.code})", style: buttonTitle),
                            trailing: Text(
                              e.percentage,
                              style: buttonTrailing,
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
