import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Classes/Attendance.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Widgets/attendanceGrid.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';

class AttendanceDetails extends StatelessWidget {
  final Attendance attendanceDetails;

  const AttendanceDetails({Key? key, required this.attendanceDetails})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;

    return Scaffold(
      backgroundColor: NeumorphicColors.background,
      body: SingleChildScrollView(
        child: Container(
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
          margin: const EdgeInsets.all(8),
          // alignment: Alignment.center,
          // color: Colors.grey,
          child: Padding(
            padding: EdgeInsets.only(
              left: width * 0.05,
              right: width * 0.05,
              top: height * 0.06,
            ),
            child: Column(
              children: [
                Align(
                  alignment: Alignment.topLeft,
                  child: Row(
                    children: [
                      IconButton(
                          onPressed: () {
                            Navigator.of(context).pop();
                          },
                          icon: Icon(Icons.chevron_left)),
                    ],
                  ),
                ),
                Text(
                  "${attendanceDetails.subjectName} (${attendanceDetails.code})",
                  style: TextStyle(
                      color: sisData.darkMode ? Colors.white : Colors.black,
                      fontSize: MediaQuery.of(context).size.width * 0.05,
                      fontFamily: 'Comfortaa'),
                ),
                AttendanceGrid(attendance: attendanceDetails)
              ],
            ),
          ),
        ),
      ),
    );
  }
}
