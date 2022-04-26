// ignore_for_file: prefer_typing_uninitialized_variables

import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Screens/cie_details.dart';
import 'package:official_connect/Widgets/cie_graph.dart';

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
                Text(
                  "Results",
                  textAlign: TextAlign.left,
                  style: titleStyle,
                ),
                Padding(
                  padding: EdgeInsets.symmetric(vertical: height * 0.02),
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
                            activeTrackColor: NeumorphicColors.disabled,
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
                        e.finalCie,
                        style: buttonTrailing,
                      ),
                    ),
                  ),
                ))
            .toList()
      ],
    );
  }
}
