import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Classes/attendance.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Widgets/attendance_grid.dart';
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
    final textStyle =
        CustomTheme.textStyle(context).copyWith(fontSize: width * 0.045);
    final linearGradient = CustomTheme.linearGradient2(context);
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
    // String howManyYouCanMiss(int per) {
    //   double p85 = (totalClasses * 0.85);
    //   double p75 = (totalClasses * 0.75);
    //   double calc85 = totalClasses-p85;
    //   double calc75 = totalClasses-p75;
    //   if (per == 85 && calc85>=0) {
    //     return "${calc85.toInt()}";
    //   } else if (per == 75 && calc75>=0) {
    //     return "${calc75.toInt()}";
    //   } else {
    //     return "N/A";
    //   }
    // }

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
                            Future.delayed(
                                Duration(seconds: 4, milliseconds: 200), () {
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
                SizedBox(height: height * 0.04),
                Align(
                  alignment: Alignment.center,
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      AutoSizeText("Attended : ${attendanceDetails.present}  ",
                          style: textStyle),
                      SizedBox(
                        width: width * 0.03,
                      ),
                      AutoSizeText("Missed : ${attendanceDetails.absent}  ",
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
                          "Remaining : ${attendanceDetails.remaining}  ",
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
                SizedBox(height: height * 0.02),
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
                                          "For 85% : ${howManyYouCanMiss(85)}/$totalClasses",
                                          textStyle: textStyle,
                                          speed: Duration(milliseconds: 50)),
                                      TypewriterAnimatedText(
                                          "For 75% : ${howManyYouCanMiss(75)}/$totalClasses",
                                          textStyle: textStyle,
                                          speed: Duration(milliseconds: 50))
                                    ])
                                // AutoSizeText(
                                //   "For 85% : ${howManyYouCanMiss(85)}/$totalClasses  ",
                                //   style: textStyle,
                                // ),
                                // SizedBox(
                                //   width: width * 0.04,
                                // ),
                                // AutoSizeText(
                                //   "For 75% : ${howManyYouCanMiss(75)}/$totalClasses",
                                //   style: textStyle,
                                // ),
                              ],
                            ),
                          )
                        : Container()),
                AttendanceGrid(attendance: attendanceDetails)
              ],
            ),
          ),
        ),
      ),
    );
  }
}
