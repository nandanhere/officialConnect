import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:http/retry.dart';
import 'package:official_connect/Classes/Attendance.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Widgets/attendanceGrid.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/Themes.dart';

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
    final textStyle = CustomTheme.textStyle(context);
    final linearGradient = CustomTheme.linearGradient(context);
    var totalClasses = attendanceDetails.present +
        attendanceDetails.absent +
        attendanceDetails.remaining;
    String howManyYouCanMiss(int per) {
      double p85 = (totalClasses * 0.85);
      double p75 = (totalClasses * 0.75);
      if (per == 85) {
        return "${p85.toInt()}";
      } else if (per == 75) {
        return "${p75.toInt()}";
      } else {
        return "N/A";
      }
    }

    return Scaffold(
      backgroundColor:
          (sisData.darkMode) ? Colors.black : NeumorphicColors.background,
      body: SingleChildScrollView(
        child: Container(
          decoration: BoxDecoration(gradient: linearGradient),
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
                          icon: Icon(
                            Icons.chevron_left,
                            color: (!sisData.darkMode)
                                ? Colors.black
                                : NeumorphicColors.background,
                          )),
                    ],
                  ),
                ),
                //  Text(
                //         "Attendance Details",
                //         textAlign: TextAlign.left,
                //         style: TextStyle(
                //             color:
                //                 sisData.darkMode ? Colors.white : Colors.black,
                //             fontSize: 40,
                //             fontFamily: 'Comfortaa'),
                //       ),
                Text(
                    "${attendanceDetails.subjectName} (${attendanceDetails.code})",
                    style: textStyle.copyWith(
                      fontSize: MediaQuery.of(context).size.width * 0.055,
                    )),
                SizedBox(height: 30),
                Center(
                  child: Row(
                    children: [
                      AutoSizeText("Attended : ${attendanceDetails.present}  ",
                          style: textStyle),
                      AutoSizeText("Missed : ${attendanceDetails.absent}  ",
                          style: textStyle)
                    ],
                  ),
                ),
                Center(
                  child: Row(
                    children: [
                      AutoSizeText(
                          "Remaining : ${attendanceDetails.remaining}  ",
                          style: textStyle),
                      AutoSizeText(
                          "Percentage : ${attendanceDetails.percentage}",
                          style: textStyle)
                    ],
                  ),
                ),
                Center(
                  child: Row(
                    children: [
                      AutoSizeText(
                        "For 85% : ${howManyYouCanMiss(85)}/$totalClasses  ",
                        style: textStyle,
                       
                      ),
                      AutoSizeText(
                        "For 75% : ${howManyYouCanMiss(75)}/$totalClasses",
                        style: textStyle,
                        
                      ),
                    ],
                  ),
                ),
                 Align(
                   alignment: Alignment.topLeft,
                   child: AutoSizeText(
                      "Total : $totalClasses ",
                      style: textStyle,
                      textAlign: TextAlign.left,
                    ),
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
