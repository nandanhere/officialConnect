// ignore_for_file: prefer_typing_uninitialized_variables

import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:official_connect/Providers/themes.dart';
import 'package:official_connect/Screens/see_details.dart';
import 'package:official_connect/Screens/syllabus_screen.dart';

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
              vertical: height * 0.02, horizontal: width * 0.1),
          child: Container(
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
                        fontSize: width * (seeOpt.value ? 0.06 : 0.1),
                        fontWeight: (seeOpt.value
                            ? FontWeight.normal
                            : FontWeight.bold),
                      ),
                    ),
                  ),
                ),
                // NeumorphicSwitch(
                //   style: const NeumorphicSwitchStyle(
                //       activeTrackColor: NeumorphicColors.accent,
                //       inactiveTrackColor: NeumorphicColors.accent,
                //       trackDepth: 10,
                //       thumbDepth: 2),
                //   height: width * 0.055,
                //   value: isSEE,
                //   onChanged: (value) {
                //     seeOpt.value = value;
                //   },
                // ),
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
                    child: Text(
                      "SEE",
                      textAlign: TextAlign.right,
                      style: CustomTheme.titleStyle(context).copyWith(
                        fontSize: width * (!seeOpt.value ? 0.06 : 0.1),
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
        SizedBox(
          height: height * 0.015,
        ),
        Text("CGPA - ${sisData.previousResults.last.cgpa}",
            textAlign: TextAlign.left,
            style: buttonTitle.copyWith(fontSize: width * 0.08)),
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
            .map((e) => Padding(
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
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (ctx) => ResultsDetails(
                              previousResult: e,
                            ),
                          ),
                        );
                      },
                      title: Text(
                        "Sem - ${e.semesterNumber}",
                        style: buttonTrailing,
                      ),
                      trailing: Text(
                        e.sgpa,
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
