import 'package:auto_size_text/auto_size_text.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/login_screen/student_home/attendance_screen/widgets/attendance_graph.dart';
import 'package:provider/provider.dart';
import 'package:flutter_neumorphic_plus/flutter_neumorphic.dart';
import 'attendance_details/attendance_details.dart';
import 'package:official_connect/Providers/themes.dart';
import 'package:official_connect/Screens/login_screen/portal_refresh.dart';
import 'package:official_connect/Screens/login_screen/student_home/widgets/sync_issue_notice.dart';

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
        backgroundColor: sisData.darkMode ? const Color(0xff101114) : Colors.white,
        color: sisData.darkMode
            ? const Color(0xffba3237)
            : const Color(0xffba3227),
        onRefresh: () async {
          await openPortalRefresh(context);
        },
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(
            parent: BouncingScrollPhysics(),
          ),
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
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                AutoSizeText(
                  "Attendance",
                  maxFontSize: 36,
                  style: titleStyle,
                ),
                SyncIssueNotice(
                  sisData: sisData,
                  section: 'attendance',
                  hasVisibleData: sisData.attendances.isNotEmpty,
                ),
                sisData.attendances.isEmpty
                    ? Padding(
                        padding: EdgeInsets.only(top: height * 0.055),
                        child: Neumorphic(
                          style: neumorphicStyle,
                          padding: const EdgeInsets.symmetric(
                            horizontal: 24,
                            vertical: 30,
                          ),
                          child: Column(
                            children: [
                              const Icon(
                                Icons.event_busy_outlined,
                                color: Color(0xffba3237),
                                size: 48,
                              ),
                              const SizedBox(height: 16),
                              Text(
                                "No attendance data",
                                textAlign: TextAlign.center,
                                style: buttonTrailing,
                              ),
                              const SizedBox(height: 8),
                              Text(
                                "The portal has no current-semester attendance for this account.",
                                textAlign: TextAlign.center,
                                style: buttonTitle.copyWith(
                                  color: sisData.darkMode
                                      ? Colors.white60
                                      : Colors.black54,
                                  height: 1.45,
                                ),
                              ),
                              const SizedBox(height: 20),
                              TextButton.icon(
                                onPressed: () => openPortalRefresh(context),
                                icon: const Icon(Icons.refresh),
                                label: const Text('Refresh data'),
                                style: TextButton.styleFrom(
                                  foregroundColor: const Color(0xffba3237),
                                ),
                              ),
                            ],
                          ),
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
                const SizedBox(height: 32),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
