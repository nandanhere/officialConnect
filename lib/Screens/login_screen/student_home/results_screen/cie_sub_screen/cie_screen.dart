// ignore_for_file: prefer_typing_uninitialized_variables

import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:official_connect/Providers/themes.dart';
import 'package:official_connect/Screens/login_screen/student_home/results_screen/cie_sub_screen/cie_details/cie_details.dart';
import 'package:official_connect/Screens/login_screen/student_home/results_screen/syllabus_sub_screen/syllabus_screen.dart';
import 'package:official_connect/Screens/login_screen/student_home/results_screen/cie_sub_screen/widgets/cie_graph.dart';
import 'package:url_launcher/url_launcher.dart';

class CIEScreen extends StatelessWidget {
  final height,
      titleStyle,
      buttonTitle,
      isSEE,
      width,
      seeOpt,
      neumorphicStyle,
      sisData,
      buttonTrailing;
  const CIEScreen(
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
  void _launchURL(BuildContext context, String url) async {
    if (!await launch(url)) throw 'Could not launch $url';
    // Navigator.of(context).push(
    //   MaterialPageRoute(
    //     builder: (ctx) => PDF().fromUrl(url),
    //   ),
    // );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Padding(
          padding: EdgeInsets.only(bottom: height * 0.04),
          child: Align(
            alignment: Alignment.topLeft,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text("Results", textAlign: TextAlign.left, style: titleStyle),
                const SizedBox(width: 40),
                NeumorphicButton(
                  child: Icon(
                    FontAwesomeIcons.bookAtlas,
                    color: sisData.darkMode ? Colors.white : Colors.black,
                    size: width * 0.05,
                  ),
                  style: neumorphicStyle,
                  onPressed: () {
                    _launchURL(context,
                        "https://drive.google.com/drive/folders/1xPhB1sYr3TdHmgURiogcqBfJpj7YKyEc?usp=sharing");
                  },
                ),
                NeumorphicButton(
                  child: Icon(
                    FontAwesomeIcons.book,
                    color: sisData.darkMode ? Colors.white : Colors.black,
                    size: width * 0.05,
                  ),
                  style: neumorphicStyle,
                  onPressed: () {
                    Navigator.of(context).push(MaterialPageRoute(
                        builder: (ctx) => const SyllabusScreen()));

                    // DummyData.syllabusLinks.keys.forEach((element) {
                    //   if (RegExp(r"[\w\s]*" + fullCourseName + r"$")
                    //       .hasMatch(element)) {
                    //     Navigator.of(context).push(MaterialPageRoute(
                    //         builder: (ctx) => BranchSyllabus(name: element)));
                    //   }
                    // });
                  },
                ),
              ],
            ),
          ),
        ),
        Padding(
          padding: EdgeInsets.symmetric(
            vertical: height * 0.02,
            horizontal: width * 0.1,
          ),
          child: SizedBox(
            height: height * 0.1,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: InkWell(
                    onTap: () {
                      seeOpt.value = false;
                    },
                    child: Text(
                      "CIE",
                      textAlign: TextAlign.left,
                      style: CustomTheme.titleStyle(context).copyWith(
                          color: Colors.lightBlue,
                          fontSize: width * (seeOpt.value ? 0.06 : 0.1),
                          fontWeight: (seeOpt.value
                              ? FontWeight.normal
                              : FontWeight.bold)),
                    ),
                  ),
                ),
                Container(
                  padding: EdgeInsets.symmetric(vertical: height * 0.02),
                  child: VerticalDivider(
                    color: sisData.darkMode ? Colors.white38 : Colors.black26,
                    thickness: 1.6,
                    width: 10,
                  ),
                ),
                Expanded(
                  child: InkWell(
                    onTap: () {
                      seeOpt.value = true;
                    },
                    child: Text("SEE",
                        textAlign: TextAlign.right,
                        style: CustomTheme.titleStyle(context).copyWith(
                          color: Colors.grey,
                          fontSize: width * (!seeOpt.value ? 0.06 : 0.1),
                          fontWeight: (!seeOpt.value
                              ? FontWeight.normal
                              : FontWeight.bold),
                        )),
                  ),
                ),
              ],
            ),
          ),
        ),
        sisData.attendances.isEmpty
            ? Center(
                child: Text(
                  "Data Not Uploaded",
                  style: titleStyle.copyWith(fontSize: width * 0.08),
                ),
              )
            : CieGraph(marks: sisData.marks),
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
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (ctx) => CIEDetails(subjectDetails: e),
                        ),
                      );
                    },
                    style: neumorphicStyle,
                    child: ListTile(
                      title: Text(
                        e.subjectName,
                        style: buttonTitle,
                      ),
                      trailing: Text(
                        e.finalCie.contains('%')
                            ? "-"
                            : ((e.t1 == '-') ? e.t1 : e.finalCie),
                        style: buttonTrailing,
                      ),
                    ),
                  ),
                ))
            .toList(),
        SizedBox(
          height: height * 0.095,
        )
      ],
    );
  }
}
