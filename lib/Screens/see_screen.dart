// ignore_for_file: prefer_typing_uninitialized_variables

import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Screens/see_details.dart';

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
                            inactiveTrackColor: NeumorphicColors.accent,
                            activeTrackColor: NeumorphicColors.disabled,
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
