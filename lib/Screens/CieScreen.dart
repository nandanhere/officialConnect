import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:official_connect/Classes/Marks.dart';
import 'package:official_connect/Screens/ResultsDetails.dart';
import 'package:official_connect/Widgets/CieGraph.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';

import 'package:official_connect/Screens/CieDetails.dart';
import 'package:official_connect/Providers/Themes.dart';

class CieInfo extends StatelessWidget {
  CieInfo({Key? key}) : super(key: key);
  @override
  ValueNotifier<bool> seeOpt = ValueNotifier(false);
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
    return Container(
      decoration: BoxDecoration(gradient: linearGradient),
      padding: EdgeInsets.only(
          left: width * 0.05,
          right: width * 0.05,
          top: height * 0.06,
          bottom: height * 0.095),
      child: SingleChildScrollView(
        physics: const BouncingScrollPhysics(),
        child: ValueListenableBuilder(
          valueListenable: seeOpt,
          builder: (context, bool isSEE, child) => isSEE
              ? Column(
                  children: [
                    Padding(
                      padding: EdgeInsets.only(bottom: height * 0.04),
                      child: Align(
                        alignment: Alignment.topLeft,
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text("Results",
                                textAlign: TextAlign.left, style: titleStyle),
                            Padding(
                              padding:
                                  EdgeInsets.symmetric(vertical: height * 0.02),
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Text(
                                    "CIE",
                                    textAlign: TextAlign.left,
                                    style: buttonTitle,
                                  ),
                                  NeumorphicSwitch(
                                    style: const NeumorphicSwitchStyle(
                                        activeTrackColor:
                                            NeumorphicColors.accent,
                                        inactiveTrackColor:
                                            NeumorphicColors.accent,
                                        trackDepth: 10,
                                        thumbDepth: 2),
                                    height: width * 0.055,
                                    value: isSEE,
                                    onChanged: (value) {
                                      seeOpt.value = value;
                                    },
                                  ),
                                  Text(
                                    "SEE",
                                    textAlign: TextAlign.left,
                                    style: buttonTitle,
                                  ),
                                ],
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
                        color:
                            sisData.darkMode ? Colors.white38 : Colors.black26,
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
                        .toList()
                  ],
                )
              : Column(
                  children: [
                    Padding(
                      padding: EdgeInsets.only(bottom: height * 0.04),
                      child: Align(
                        alignment: Alignment.topLeft,
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              "Results",
                              textAlign: TextAlign.left,
                              style: titleStyle,
                            ),
                            Padding(
                              padding:
                                  EdgeInsets.symmetric(vertical: height * 0.02),
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Text(
                                    "CIE",
                                    textAlign: TextAlign.left,
                                    style: buttonTitle,
                                  ),
                                  NeumorphicSwitch(
                                    style: const NeumorphicSwitchStyle(
                                        activeTrackColor:
                                            NeumorphicColors.disabled,
                                        inactiveTrackColor:
                                            NeumorphicColors.accent,
                                        trackDepth: 10,
                                        thumbDepth: 2),
                                    height: width * 0.055,
                                    value: isSEE,
                                    onChanged: (value) {
                                      seeOpt.value = value;
                                    },
                                  ),
                                  Text(
                                    "SEE",
                                    textAlign: TextAlign.left,
                                    style: buttonTitle,
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                    CieGraph(marks: sisData.marks),
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
                                      builder: (ctx) =>
                                          CieDetails(subjectDetails: e),
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
                                    e.finalCie,
                                    style: buttonTrailing,
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
