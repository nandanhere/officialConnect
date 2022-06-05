import 'package:auto_size_text/auto_size_text.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/login_screen/student_home/attendance_screen/widgets/attendance_graph.dart';
import 'package:provider/provider.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'attendance_details/attendance_details.dart';
import 'package:official_connect/Providers/themes.dart';
import 'package:fluttertoast/fluttertoast.dart';

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
    final linearGradientBG = CustomTheme.linearGradientBG(context);

    return Container(
      decoration: BoxDecoration(gradient: linearGradientBG),
      child: RefreshIndicator(
        displacement: height * 0.1,
        backgroundColor: sisData.darkMode ? Colors.black : Colors.white,
        color: sisData.darkMode
            ? const Color(0xffba3237)
            : const Color(0xffba3227),
        onRefresh: () async {
          Fluttertoast.showToast(
              msg: "Updating data ",
              toastLength: Toast.LENGTH_LONG,
              gravity: ToastGravity.BOTTOM,
              timeInSecForIosWeb: 1,
              backgroundColor: const Color(0xffba3237),
              textColor: Colors.white,
              fontSize: 16.0);
          await sisData.getData("", "", true);
          Fluttertoast.showToast(
              msg: "Updated data 🎉 ",
              toastLength: Toast.LENGTH_LONG,
              gravity: ToastGravity.BOTTOM,
              timeInSecForIosWeb: 1,
              backgroundColor: const Color(0xffba3237),
              textColor: Colors.white,
              fontSize: 16.0);
        },
        child: SingleChildScrollView(
          physics: const BouncingScrollPhysics(),
          child: Container(
            decoration: BoxDecoration(
              gradient: linearGradient,
            ),
            padding: EdgeInsets.only(
              left: width * 0.05,
              right: width * 0.05,
              top: height * 0.06,
            ),
            child: Column(
              children: [
                AutoSizeText(
                  "Attendance Info",
                  maxFontSize: 45,
                  style: titleStyle,
                ),
                sisData.attendances.isEmpty
                    ? Center(
                        child: Text(
                          "Data Not Uploaded",
                          style: titleStyle.copyWith(fontSize: width * 0.08),
                        ),
                      )
                    : AttendanceGraph(
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
                    .toList(),
                SizedBox(
                  height: height * 0.13,
                )
              ],
            ),
          ),
        ),
      ),
    );
  }
}
