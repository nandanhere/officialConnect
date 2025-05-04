import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter_neumorphic_plus/flutter_neumorphic.dart';
import 'package:official_connect/Classes/attendance.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/login_screen/student_home/attendance_screen/attendance_details/widgets/attendance_details_calender_version.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/themes.dart';
import 'package:animated_text_kit/animated_text_kit.dart';

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
    final neumorphicStyle = CustomTheme.neumorphicStyle(context);
    final textStyle =
        CustomTheme.textStyle(context).copyWith(fontSize: width * 0.045);
    final linearGradient = CustomTheme.linearGradient2(context);
    var totalClasses = attendanceDetails.present +
        attendanceDetails.absent +
        attendanceDetails.remaining;
    var alreadyMissed = attendanceDetails.absent;
    // String howManyYouCanMiss(int per) {
    //   double p85 = (totalClasses * 0.85);
    //   double p75 = (totalClasses * 0.75);
    //   if (per == 85) {
    //     return "${p85.toInt()}";
    //   } else if (per == 75) {
    //     return "${p75.toInt()}";
    //   } else {
    //     return "N/A";
    //   }
    // }
    String howManyYouCanMiss(int per) {
      double p85 = (totalClasses * 0.85);
      double p75 = (totalClasses * 0.75);
      double calc85 = totalClasses - p85 - alreadyMissed;
      double calc75 = totalClasses - p75 - alreadyMissed;

      if (per == 85 && calc85 >= 0) {
        return "${calc85.toInt()}";
      } else if (per == 75 && calc75 >= 0) {
        return "${calc75.toInt()}";
      } else {
        return "0";
      }
    }

    ValueNotifier<bool> show = ValueNotifier(false);
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
                      SizedBox(
                        width: width * 0.03,
                      ),
                      Expanded(
                        child: GestureDetector(
                          onLongPress: () {
                            show.value = true;
                            Future.delayed(const Duration(seconds: 7), () {
                              show.value = false;
                            });
                          },
                          child: Text(
                              "${attendanceDetails.subjectName} (${attendanceDetails.code})",
                              style: textStyle.copyWith(
                                fontWeight: FontWeight.bold,
                                fontSize:
                                    MediaQuery.of(context).size.width * 0.055,
                              )),
                        ),
                      )
                    ],
                  ),
                ),
                SizedBox(height: height * 0.02),
                //column start here
                // Card(
                //   color: (sisData.darkMode)
                //       ? NeumorphicColors.darkBackground
                //       : NeumorphicColors.background,
                //   elevation: 0.5,
                //   shape: const RoundedRectangleBorder(
                //       borderRadius: BorderRadius.all(Radius.circular(10))),
                //   child: Column(
                //     children: [
                //       Align(
                //         alignment: Alignment.center,
                //         child: Row(
                //           mainAxisSize: MainAxisSize.min,
                //           children: [
                //             AutoSizeText(
                //                 "Attended : ${attendanceDetails.present}",
                //                 style: textStyle),
                //             SizedBox(
                //               width: width * 0.03,
                //             ),
                //             AutoSizeText("Missed : ${attendanceDetails.absent}",
                //                 style: textStyle)
                //           ],
                //         ),
                //       ),
                //       Align(
                //         alignment: Alignment.center,
                //         child: Row(
                //           mainAxisSize: MainAxisSize.min,
                //           children: [
                //             AutoSizeText(
                //                 "Remaining: ${attendanceDetails.remaining}",
                //                 style: textStyle),
                //             SizedBox(
                //               width: width * 0.03,
                //             ),
                //             AutoSizeText(
                //                 "Percentage : ${attendanceDetails.percentage}",
                //                 style: textStyle)
                //           ],
                //         ),
                //       ),
                //       Align(
                //         alignment: Alignment.center,
                //         child: AutoSizeText(
                //           "Total : $totalClasses ",
                //           style: textStyle,
                //           textAlign: TextAlign.left,
                //         ),
                //       ),
                //     ],
                //   ),
                // ),
                Neumorphic(
                  style: neumorphicStyle.copyWith(
                    color: sisData.darkMode
                        // ? const Color.fromARGB(1, 77, 74, 74)
                        ? Colors.black.withOpacity(0.4)
                        : NeumorphicColors.background.withAlpha(150),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Column(
                      children: [
                        Align(
                          alignment: Alignment.center,
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              AutoSizeText(
                                  "Attended : ${attendanceDetails.present}",
                                  style: textStyle),
                              SizedBox(
                                width: width * 0.03,
                              ),
                              AutoSizeText(
                                  "Missed : ${attendanceDetails.absent}",
                                  style: textStyle)
                            ],
                          ),
                        ),
                        Align(
                          alignment: Alignment.center,
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              AutoSizeText(
                                  "Remaining: ${attendanceDetails.remaining}",
                                  style: textStyle),
                              SizedBox(
                                width: width * 0.03,
                              ),
                              AutoSizeText(
                                  "Percentage : ${attendanceDetails.percentage}",
                                  style: textStyle)
                            ],
                          ),
                        ),
                        Align(
                          alignment: Alignment.center,
                          child: AutoSizeText(
                            "Total : $totalClasses ",
                            style: textStyle,
                            textAlign: TextAlign.left,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                //column end here
                SizedBox(height: height * 0.004),
                ValueListenableBuilder(
                    valueListenable: show,
                    builder: (context, bool listening, child) => (listening)
                        ? Align(
                            alignment: Alignment.center,
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                AnimatedTextKit(
                                    totalRepeatCount: 1,
                                    animatedTexts: [
                                      TypewriterAnimatedText(
                                          //"For 85% : ${howManyYouCanMiss(85)}/$totalClasses",
                                          "You can miss ${howManyYouCanMiss(85)} classes for 85%",
                                          textStyle: textStyle,
                                          speed:
                                              const Duration(milliseconds: 60)),
                                      TypewriterAnimatedText(
                                          "You can miss ${howManyYouCanMiss(75)} classes for 75%",
                                          textStyle: textStyle,
                                          speed:
                                              const Duration(milliseconds: 60))
                                    ])
                              ],
                            ),
                          )
                        : Container()),
                AttendanceCalenderVersion(attendance: attendanceDetails)
              ],
            ),
          ),
        ),
      ),
    );
  }
}
