import 'package:flutter/material.dart';
import 'package:official_connect/Classes/Attendance.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Widgets/AttendanceGraph.dart';
import 'package:provider/provider.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import './AttendanceDetails.dart';

class AttendanceInfo extends StatelessWidget {
  const AttendanceInfo({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final sisData = Provider.of<SisData>(context);

    return Container(
      decoration: BoxDecoration(
          gradient: LinearGradient(
              begin: Alignment.bottomRight,
              end: Alignment.topLeft,
              colors: (sisData.darkMode)
                  ? [Colors.black, Colors.black, Colors.blueGrey]
                  : [
                      NeumorphicColors.background,
                      NeumorphicColors.background,
                      Colors.white,
                      Colors.white
                    ])),
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
              Text(
                "Attendance Info",
                style: TextStyle(
                    color: sisData.darkMode ? Colors.white : Colors.black,
                    fontSize: 40,
                    fontFamily: 'Comfortaa'),
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
                          style: NeumorphicStyle(
                              shadowLightColor:
                                  sisData.darkMode ? Colors.white : null,
                              shadowDarkColor: sisData.darkMode
                                  ? NeumorphicColors.background
                                  : null,
                              color: sisData.darkMode
                                  ? Color.fromARGB(1, 77, 74, 74)
                                  : NeumorphicColors.background,
                              depth: 3,
                              boxShape: NeumorphicBoxShape.roundRect(
                                  BorderRadius.circular(20))),
                          child: ListTile(
                            title: Text(
                              e.subjectName,
                              style: TextStyle(
                                  color: sisData.darkMode
                                      ? Colors.white
                                      : Colors.black,
                                  fontSize: width * 0.045,
                                  fontFamily: 'Comfortaa'),
                            ),
                            subtitle: Text(
                              "(${e.code})",
                              style: TextStyle(
                                  color: sisData.darkMode
                                      ? Colors.white
                                      : Colors.black,
                                  fontSize: width * 0.045,
                                  fontFamily: 'Comfortaa'),
                            ),
                            trailing: Text(
                              e.percentage,
                              style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: sisData.darkMode
                                      ? Colors.white
                                      : Colors.black,
                                  fontSize: width * 0.055,
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
