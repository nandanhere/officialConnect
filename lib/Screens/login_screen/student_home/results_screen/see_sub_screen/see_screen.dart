// ignore_for_file: prefer_typing_uninitialized_variables
import 'dart:async';

import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter_neumorphic_plus/flutter_neumorphic.dart';

import 'package:official_connect/Classes/previous_result.dart';
import 'package:official_connect/Providers/themes.dart';
import 'package:official_connect/Screens/login_screen/student_home/results_screen/see_sub_screen/latest_results.dart';
import 'package:official_connect/Screens/login_screen/student_home/results_screen/see_sub_screen/see_details/see_details.dart';
import 'package:official_connect/Services/exam_result_scraper.dart';
import 'package:official_connect/Screens/login_screen/student_home/widgets/sync_issue_notice.dart';
import 'package:official_connect/Services/sync_diagnostics.dart';

class SEEScreen extends StatelessWidget {
  final height,
      titleStyle,
      buttonTitle,
      isSEE,
      width,
      seeOpt,
      neumorphicStyle,
      sisData,
      buttonTrailing;

  const SEEScreen(
      {Key? key,
      this.height,
      this.titleStyle,
      this.buttonTitle,
      this.isSEE,
      this.width,
      this.seeOpt,
      this.neumorphicStyle,
      this.sisData,
      this.buttonTrailing})
      : super(key: key);
  @override
  Widget build(BuildContext context) {
    final rawCgpa = sisData.previousResults.isEmpty
        ? ''
        : sisData.previousResults.last.cgpa.toString();
    final cgpa = rawCgpa
        .replaceFirst(RegExp(r'^CGPA\s*:\s*', caseSensitive: false), '')
        .trim();
    Widget latestResultTile({
      required String title,
      required IconData icon,
      required ExamResultSource source,
    }) =>
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
          child: Neumorphic(
            style: neumorphicStyle,
            child: ListTile(
              contentPadding:
                  const EdgeInsets.symmetric(horizontal: 16, vertical: 5),
              leading: Icon(icon, color: const Color(0xffba3237)),
              title: Text(title, style: buttonTitle),
              subtitle: Text(
                source == ExamResultSource.regular
                    ? 'From the current MSRIT examination results page'
                    : 'From the MSRIT supplementary results page',
                style: CustomTheme.textStyle(context).copyWith(
                  color: sisData.darkMode ? Colors.white54 : Colors.black45,
                  fontSize: 11,
                ),
              ),
              trailing: const Icon(Icons.chevron_right, size: 20),
              onTap: () {
                unawaited(SyncDiagnostics.recordFeature(
                  source == ExamResultSource.regular
                      ? 'latest_regular_result'
                      : 'supplementary_results',
                ));
                Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (_) => LatestResultsDetails(source: source),
                  ),
                );
              },
            ),
          ),
        );
    return Column(
      children: [
        Padding(
          padding: EdgeInsets.only(bottom: height * 0.025),
          child: Align(
            alignment: Alignment.topLeft,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text("Results", textAlign: TextAlign.left, style: titleStyle),
                const SizedBox(width: 40),
                // NeumorphicButton(
                //   child: Icon(
                //     FontAwesomeIcons.bookAtlas,
                //     color: sisData.darkMode ? Colors.white : Colors.black,
                //     size: width * 0.05,
                //   ),
                //   style: neumorphicStyle,
                //   onPressed: () {
                //     _launchURL(context,
                //         "https://drive.google.com/drive/folders/1xPhB1sYr3TdHmgURiogcqBfJpj7YKyEc?usp=sharing");
                //   },
                // ),
                // NeumorphicButton(
                //   child: Icon(
                //     FontAwesomeIcons.book,
                //     color: sisData.darkMode ? Colors.white : Colors.black,
                //     size: width * 0.05,
                //   ),
                //   style: neumorphicStyle,
                //   onPressed: () {
                //     Navigator.of(context).push(MaterialPageRoute(
                //         builder: (ctx) => const SyllabusScreen()));
                //
                //     // DummyData.syllabusLinks.keys.forEach((element) {
                //     //   if (RegExp(r"[\w\s]*" + fullCourseName + r"$")
                //     //       .hasMatch(element)) {
                //     //     Navigator.of(context).push(MaterialPageRoute(
                //     //         builder: (ctx) => BranchSyllabus(name: element)));
                //     //   }
                //     // });
                //   },
                // ),
              ],
            ),
          ),
        ),
        Padding(
          padding: EdgeInsets.symmetric(
              vertical: height * 0.01, horizontal: width * 0.06),
          child: SizedBox(
            height: height * 0.065,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: InkWell(
                    onTap: () {
                      unawaited(SyncDiagnostics.recordFeature('cie_marks'));
                      seeOpt.value = false;
                    },
                    child: Text(
                      "CIE",
                      textAlign: TextAlign.left,
                      style: CustomTheme.titleStyle(context).copyWith(
                        fontSize: width * (seeOpt.value ? 0.05 : 0.065),
                        fontWeight: (seeOpt.value
                            ? FontWeight.normal
                            : FontWeight.bold),
                      ),
                    ),
                  ),
                ),
                Container(
                  padding: EdgeInsets.symmetric(vertical: height * 0.01),
                  child: VerticalDivider(
                    color: sisData.darkMode ? Colors.white38 : Colors.black26,
                    thickness: 1.6,
                    width: 10,
                  ),
                ),
                Expanded(
                  child: InkWell(
                    onTap: () {
                      unawaited(
                        SyncDiagnostics.recordFeature('semester_results'),
                      );
                      seeOpt.value = true;
                    },
                    child: Text(
                      "SEE",
                      textAlign: TextAlign.right,
                      style: CustomTheme.titleStyle(context).copyWith(
                        color: const Color(0xffba3237),
                        fontSize: width * (!seeOpt.value ? 0.05 : 0.065),
                        fontWeight: (!seeOpt.value
                            ? FontWeight.normal
                            : FontWeight.bold),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
        SyncIssueNotice(
          sisData: sisData,
          section: 'results',
          hasVisibleData: sisData.previousResults.isNotEmpty,
        ),
        if (sisData.previousResults.isNotEmpty) ...[
          SizedBox(
            height: height * 0.015,
          ),
          Text("CGPA $cgpa",
              textAlign: TextAlign.left,
              style: buttonTitle.copyWith(
                fontSize: width * 0.065,
                fontWeight: FontWeight.w600,
              )),
          Container(
            padding: EdgeInsets.only(
                left: width * 0.16,
                right: width * 0.16,
                top: height * 0.01,
                bottom: height * 0.015),
            child: Divider(
              color: sisData.darkMode ? Colors.white38 : Colors.black26,
              thickness: 1.6,
            ),
          ),
          ...sisData.previousResults
              .map((PreviousResult e) => Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Neumorphic(
                      padding: EdgeInsets.only(
                          top: height * 0.015,
                          bottom: height * 0.015,
                          left: width * 0.025,
                          right: width * 0.01),
                      style: neumorphicStyle,
                      child: ListTile(
                        onTap: () {
                          unawaited(
                            SyncDiagnostics.recordFeature('result_details'),
                          );
                          Navigator.of(context).push(
                            MaterialPageRoute(
                              builder: (ctx) => ResultsDetails(
                                previousResult: e,
                              ),
                            ),
                          );
                        },
                        title: AutoSizeText(
                          (e.term.toLowerCase().contains('supplementary') ||
                                  e.term.toLowerCase().contains("back"))
                              ? e.term
                              : "Sem - ${e.semesterNumber}",
                          // maxFontSize: ((width * 0.08) as double).round(),
                          maxLines: 2,
                          style: buttonTrailing,
                        ),
                        trailing: (e.term.toLowerCase().contains("back"))
                            ? null
                            : Text(
                                e.sgpa,
                                style: buttonTrailing,
                              ),
                      ),
                    ),
                  ))
              .toList(),
        ],
        if (sisData.previousResults.isNotEmpty) ...[
          const SizedBox(height: 18),
          Align(
            alignment: Alignment.centerLeft,
            child: Padding(
              padding: const EdgeInsets.fromLTRB(10, 0, 10, 7),
              child: Text(
                'Quick results',
                style: buttonTrailing.copyWith(fontSize: 20.0),
              ),
            ),
          ),
        ],
        latestResultTile(
          title: 'Latest regular result',
          icon: Icons.school_outlined,
          source: ExamResultSource.regular,
        ),
        latestResultTile(
          title: 'Supplementary results',
          icon: Icons.history_edu_outlined,
          source: ExamResultSource.supplementary,
        ),
        SizedBox(
          height: height * 0.095,
        ),
      ],
    );
  }
}
