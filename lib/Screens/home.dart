import 'package:auto_size_text/auto_size_text.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import "dart:math";

extension StringCasingExtension on String {
  String toCapitalized() =>
      length > 0 ? '${this[0].toUpperCase()}${substring(1).toLowerCase()}' : '';
  String toTitleCase() => replaceAll(RegExp(' +'), ' ')
      .split(' ')
      .map((str) => str.toCapitalized())
      .join('\n');
}

class Home extends StatelessWidget {
  const Home({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final emojis = [
      "😀",
      "😊",
      "🤠",
      "😸",
      "😋",
      "🎉",
      "👋",
      "😛",
      "😇",
      "🤗",
      "😎",
      "👽",
      "💩",
      "👻",
      "😺",
      "🤟"
    ];
    final emoji = emojis[Random().nextInt(emojis.length)];
    final sisData = Provider.of<SisData>(context);
    return Container(
      height: height,
      decoration: BoxDecoration(
          gradient: LinearGradient(
              begin: Alignment.bottomRight,
              end: Alignment.topLeft,
              colors: (sisData.darkMode)
                  ? [Colors.black, Colors.black, Colors.blueGrey]
                  // ? [Colors.black, Colors.black, Colors.black87] Equal people seem to like both.. idk what to do about it
                  : [
                      NeumorphicColors.background,
                      NeumorphicColors.background,
                      Colors.white
                    ])),
      padding: EdgeInsets.only(
          left: width * 0.08,
          right: width * 0.08,
          top: height * 0.06,
          bottom: height * 0.13),
      child: SingleChildScrollView(
        physics: const BouncingScrollPhysics(),
        child: Center(
          child:
              Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
            Image.asset(
              'images/logo.png',
              color: sisData.darkMode ? (Colors.white) : null,
            ),
            Padding(
              padding: EdgeInsets.symmetric(
                  horizontal: width * 0.02, vertical: height * 0.02),
              child: Neumorphic(
                style: NeumorphicStyle(
                    shadowLightColor: sisData.darkMode ? Colors.white : null,
                    shadowDarkColor:
                        sisData.darkMode ? NeumorphicColors.background : null,
                    color: sisData.darkMode
                        ? Color.fromARGB(1, 77, 74, 74)
                        : NeumorphicColors.background,
                    depth: 2,
                    intensity: 1,
                    boxShape: NeumorphicBoxShape.roundRect(
                        BorderRadius.circular(20))),
                child: Padding(
                  padding: EdgeInsets.symmetric(
                      horizontal: width * 0.05, vertical: height * 0.025),
                  child: Column(
                    children: [
                      Padding(
                        padding: EdgeInsets.only(bottom: height * 0.02),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          mainAxisSize: MainAxisSize.max,
                          children: [
                            Expanded(
                              child: AutoSizeText(
                                "Hi, ${sisData.studentName.toTitleCase()} ${emoji} ",
                                style: TextStyle(
                                  color: sisData.darkMode
                                      ? Colors.white
                                      : Colors.black,
                                  // fontSize: width * 0.09,
                                  fontWeight: FontWeight.bold,
                                  fontFamily: 'Comfortaa',
                                ),
                              ),
                            ),
                            Neumorphic(
                              style: NeumorphicStyle(
                                  shadowLightColor:
                                      sisData.darkMode ? Colors.white : null,
                                  shadowDarkColor: sisData.darkMode
                                      ? NeumorphicColors.background
                                      : null,
                                  color: sisData.darkMode
                                      ? Color.fromARGB(1, 77, 74, 74)
                                      : NeumorphicColors.background,
                                  boxShape: NeumorphicBoxShape.circle(),
                                  depth: 2,
                                  intensity: 1),
                              // TODO : show circular progress indicator while loading image
                              child: CircleAvatar(
                                backgroundImage: CachedNetworkImageProvider(
                                    sisData.studentImage),
                                backgroundColor: Colors.grey,
                                radius: width * 0.1,
                              ),
                            ),
                          ],
                        ),
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            "Class ",
                            style: TextStyle(
                                color: sisData.darkMode
                                    ? Colors.white
                                    : Colors.black,
                                fontSize: width * 0.05,
                                fontFamily: 'Comfortaa'),
                          ),
                          Container(
                            padding: EdgeInsets.symmetric(
                                vertical: height * 0.01,
                                horizontal: width * 0.02),
                            child: Text(
                              "${sisData.semester}-${sisData.section[4]}",
                              style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: sisData.darkMode
                                      ? Colors.white54
                                      : Colors.black54,
                                  fontSize: width * 0.04,
                                  fontFamily: 'Comfortaa'),
                            ),
                            // decoration: BoxDecoration(
                            // border: Border.all(width: 1.3),
                            // borderRadius: BorderRadius.circular(width)),
                          ),
                        ],
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            "Course ",
                            style: TextStyle(
                                color: sisData.darkMode
                                    ? Colors.white
                                    : Colors.black,
                                fontSize: width * 0.05,
                                fontFamily: 'Comfortaa'),
                          ),
                          Container(
                            padding: EdgeInsets.symmetric(
                                vertical: height * 0.01,
                                horizontal: width * 0.02),
                            child: Text(
                              sisData.course,
                              style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: sisData.darkMode
                                      ? Colors.white54
                                      : Colors.black54,
                                  fontSize: width * 0.04,
                                  fontFamily: 'Comfortaa'),
                            ),
                            // decoration: BoxDecoration(
                            // border: Border.all(width: 1.3),
                            // borderRadius: BorderRadius.circular(width)),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ),
            Container(
              padding: EdgeInsets.only(
                  left: width * 0.1,
                  right: width * 0.1,
                  top: height * 0.03,
                  bottom: height * 0.015),
              child: const Divider(
                thickness: 1.6,
              ),
            ),
            Column(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Padding(
                  padding: EdgeInsets.symmetric(
                      horizontal: width * 0.2, vertical: height * 0.02),
                  child: Text(
                    "Your Fees Paid",
                    style: TextStyle(
                        color: sisData.darkMode ? Colors.white : Colors.black,
                        fontSize: width * 0.05,
                        fontFamily: 'Comfortaa',
                        fontWeight: FontWeight.bold),
                  ),
                ),
                ...sisData.fees.map((e) => Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: NeumorphicButton(
                        padding: EdgeInsets.only(
                            top: height * 0.015,
                            bottom: height * 0.015,
                            left: width * 0.025,
                            right: width * 0.01),
                        onPressed: () {}, //TODO receipt download maybe?
                        style: NeumorphicStyle(
                            shadowLightColor:
                                sisData.darkMode ? Colors.white : null,
                            shadowDarkColor: sisData.darkMode
                                ? NeumorphicColors.background
                                : null,
                            color: sisData.darkMode
                                ? Color.fromARGB(1, 77, 74, 74)
                                : NeumorphicColors.background,
                            depth: 2,
                            boxShape: NeumorphicBoxShape.roundRect(
                                BorderRadius.circular(20))),
                        child: ExpansionTile(
                          title: Text(
                            e.amountPaid,
                            style: TextStyle(
                                fontWeight: FontWeight.bold,
                                color: sisData.darkMode
                                    ? Colors.white
                                    : Colors.black,
                                fontSize: width * 0.06,
                                fontFamily: 'Comfortaa'),
                          ),
                          subtitle: Padding(
                            padding: EdgeInsets.symmetric(
                                horizontal: width * 0.02,
                                vertical: height * 0.01),
                            child: Text(
                              "For Year ${e.yearNumber} on ${e.date}",
                              style: TextStyle(
                                  color: sisData.darkMode
                                      ? Colors.white54
                                      : Colors.black54,
                                  fontSize: width * 0.04,
                                  fontFamily: 'Comfortaa'),
                            ),
                          ),
                          children: [
                            Padding(
                              padding: EdgeInsets.symmetric(
                                  horizontal: width * 0.04,
                                  vertical: height * 0.02),
                              child: Row(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
                                children: [
                                  Text(
                                    "Challan No:",
                                    style: TextStyle(
                                        color: sisData.darkMode
                                            ? Colors.white
                                            : Colors.black,
                                        fontSize: width * 0.04,
                                        fontFamily: 'Comfortaa'),
                                  ),
                                  Text(
                                    e.challanNumber,
                                    style: TextStyle(
                                        color: sisData.darkMode
                                            ? Colors.white54
                                            : Colors.black54,
                                        fontSize: width * 0.04,
                                        fontFamily: 'Comfortaa'),
                                    textAlign: TextAlign.end,
                                  ),
                                ],
                              ), //ChallanNo
                            ),
                            (e.mode != "CASH")
                                ? Padding(
                                    padding: EdgeInsets.symmetric(
                                        horizontal: width * 0.04,
                                        vertical: height * 0.02),
                                    child: Row(
                                      mainAxisAlignment:
                                          MainAxisAlignment.spaceBetween,
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          "Cheque No:",
                                          style: TextStyle(
                                              color: sisData.darkMode
                                                  ? Colors.white
                                                  : Colors.black,
                                              fontSize: width * 0.04,
                                              fontFamily: 'Comfortaa'),
                                        ),
                                        Expanded(
                                          child: Text(
                                            e.chequeNumber,
                                            style: TextStyle(
                                                color: sisData.darkMode
                                                    ? Colors.white54
                                                    : Colors.black54,
                                                fontSize: width * 0.04,
                                                fontFamily: 'Comfortaa'),
                                            textAlign: TextAlign.end,
                                          ),
                                        ),
                                      ],
                                    ),
                                  )
                                : Container(),
                          ],
                        ),
                      ),
                    ))
              ],
            )
          ]),
        ),
      ),
    );
  }
}
