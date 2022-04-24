import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:official_connect/Screens/ResultsDetails.dart';
import 'package:official_connect/Widgets/CieGraph.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';

import 'package:official_connect/Screens/CieDetails.dart';

class CieInfo extends StatelessWidget {
  CieInfo({Key? key}) : super(key: key);
  @override
  ValueNotifier<bool> seeOpt = ValueNotifier(false);
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final sisData = Provider.of<SisData>(context);
    return Container(
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
      padding: EdgeInsets.only(
          left: width * 0.05,
          right: width * 0.05,
          top: height * 0.06,
          bottom: height * 0.13),
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
                        child: Text(
                          "Results",
                          textAlign: TextAlign.left,
                          style: TextStyle(
                              color: sisData.darkMode
                                  ? Colors.white
                                  : Colors.black,
                              fontSize: 40,
                              fontFamily: 'Comfortaa'),
                        ),
                      ),
                    ),
                    Padding(
                      padding: EdgeInsets.symmetric(vertical: height * 0.02),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            "CIE",
                            textAlign: TextAlign.left,
                            style: TextStyle(
                                color: sisData.darkMode
                                    ? Colors.white
                                    : Colors.black,
                                fontSize: width * 0.04,
                                fontFamily: 'Comfortaa'),
                          ),
                          NeumorphicSwitch(
                            style: const NeumorphicSwitchStyle(
                                inactiveTrackColor: NeumorphicColors.accent,
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
                            style: TextStyle(
                                color: sisData.darkMode
                                    ? Colors.white
                                    : Colors.black,
                                fontSize: width * 0.04,
                                fontFamily: 'Comfortaa'),
                          ),
                        ],
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
                                style: NeumorphicStyle(
                                    shadowLightColor:
                                        sisData.darkMode ? Colors.white : null,
                                    shadowDarkColor: sisData.darkMode
                                        ? NeumorphicColors.background
                                        : null,
                                    color: sisData.darkMode
                                        ? Color.fromARGB(1, 77, 74, 74)
                                        : NeumorphicColors.background,
                                    depth: 3,
                                    boxShape: NeumorphicBoxShape.roundRect(
                                        BorderRadius.circular(20))),
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
                                    e.term,
                                    style: TextStyle(
                                        color: sisData.darkMode
                                            ? Colors.white
                                            : Colors.black,
                                        fontSize: width * 0.045,
                                        fontFamily: 'Comfortaa'),
                                  ),
                                  trailing: Text(
                                    e.cgpa,
                                    style: TextStyle(
                                        fontWeight: FontWeight.bold,
                                        color: sisData.darkMode
                                            ? Colors.white
                                            : Colors.black,
                                        fontSize: width * 0.055,
                                        fontFamily: 'Comfortaa'),
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
                        child: Text(
                          "Results",
                          textAlign: TextAlign.left,
                          style: TextStyle(
                              color: sisData.darkMode
                                  ? Colors.white
                                  : Colors.black,
                              fontSize: 40,
                              fontFamily: 'Comfortaa'),
                        ),
                      ),
                    ),
                    Padding(
                      padding: EdgeInsets.symmetric(vertical: height * 0.02),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            "CIE",
                            textAlign: TextAlign.left,
                            style: TextStyle(
                                color: sisData.darkMode
                                    ? Colors.white
                                    : Colors.black,
                                fontSize: width * 0.04,
                                fontFamily: 'Comfortaa'),
                          ),
                          NeumorphicSwitch(
                            style: const NeumorphicSwitchStyle(
                                inactiveTrackColor: NeumorphicColors.accent,
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
                            style: TextStyle(
                                color: sisData.darkMode
                                    ? Colors.white
                                    : Colors.black,
                                fontSize: width * 0.04,
                                fontFamily: 'Comfortaa'),
                          ),
                        ],
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
                                style: NeumorphicStyle(
                                    shadowLightColor:
                                        sisData.darkMode ? Colors.white : null,
                                    shadowDarkColor: sisData.darkMode
                                        ? NeumorphicColors.background
                                        : null,
                                    color: sisData.darkMode
                                        ? Color.fromARGB(1, 77, 74, 74)
                                        : NeumorphicColors.background,
                                    depth: 3,
                                    boxShape: NeumorphicBoxShape.roundRect(
                                        BorderRadius.circular(20))),
                                child: ListTile(
                                  title: Text(
                                    e.subjectName,
                                    style: TextStyle(
                                        color: sisData.darkMode
                                            ? Colors.white
                                            : Colors.black,
                                        fontSize: width * 0.045,
                                        fontFamily: 'Comfortaa'),
                                  ),
                                  trailing: Text(
                                    e.finalCie,
                                    style: TextStyle(
                                        fontWeight: FontWeight.bold,
                                        color: sisData.darkMode
                                            ? Colors.white
                                            : Colors.black,
                                        fontSize: width * 0.055,
                                        fontFamily: 'Comfortaa'),
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

// Column(
// children: [
// Padding(
// padding: EdgeInsets.only(bottom: height * 0.04),
// child: Align(
// alignment: Alignment.topLeft,
// child: Text(
// "Results",
// textAlign: TextAlign.left,
// style: TextStyle(
// color: sisData.darkMode ? Colors.white : Colors.black,
// fontSize: 40,
// fontFamily: 'Comfortaa'),
// ),
// ),
// ),
// Row(
// mainAxisAlignment: MainAxisAlignment.center,
// children: [
// Text(
// "CIE",
// textAlign: TextAlign.left,
// style: TextStyle(
// color: sisData.darkMode ? Colors.white : Colors.black,
// fontSize: width * 0.04,
// fontFamily: 'Comfortaa'),
// ),
// NeumorphicSwitch(
// style: const NeumorphicSwitchStyle(
// inactiveTrackColor: NeumorphicColors.accent,
// trackDepth: 10,
// thumbDepth: 2),
// height: width * 0.055,
// value: seeOpt.value,
// onChanged: (value) {
// seeOpt.value = value;
// },
// ),
// Text(
// "SEE",
// textAlign: TextAlign.left,
// style: TextStyle(
// color: sisData.darkMode ? Colors.white : Colors.black,
// fontSize: width * 0.04,
// fontFamily: 'Comfortaa'),
// ),
// ],
// ),
// CieGraph(marks: sisData.marks),
// ...sisData.marks
//     .map((e) => Padding(
// padding: const EdgeInsets.all(8.0),
// child: NeumorphicButton(
// padding: EdgeInsets.only(
// top: height * 0.015,
// bottom: height * 0.015,
// left: width * 0.025,
// right: width * 0.01),
// onPressed: () {
// Navigator.of(context).push(MaterialPageRoute(
// builder: (ctx) => CieDetails(subjectDetails: e)));
// },
// style: NeumorphicStyle(
// shadowLightColor:
// sisData.darkMode ? Colors.white : null,
// shadowDarkColor: sisData.darkMode
// ? NeumorphicColors.background
//     : null,
// color: sisData.darkMode
// ? Color.fromARGB(1, 77, 74, 74)
// : NeumorphicColors.background,
// depth: 3,
// boxShape: NeumorphicBoxShape.roundRect(
// BorderRadius.circular(20))),
// child: ListTile(
// title: Text(
// e.subjectName,
// style: TextStyle(
// color: sisData.darkMode
// ? Colors.white
//     : Colors.black,
// fontSize: width * 0.045,
// fontFamily: 'Comfortaa'),
// ),
// trailing: Text(
// e.finalCie,
// style: TextStyle(
// fontWeight: FontWeight.bold,
// color: sisData.darkMode
// ? Colors.white
//     : Colors.black,
// fontSize: width * 0.055,
// fontFamily: 'Comfortaa'),
// ),
// ),
// ),
// ))
// .toList()
// ],
// )
