import 'package:auto_size_text/auto_size_text.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import "dart:math";
import 'package:official_connect/Providers/Themes.dart';

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
    final buttonTitle = CustomTheme.buttonTitle(context);
    final buttonTrailing = CustomTheme.buttonTrailing(context);
    final title = CustomTheme.textStyle(context);
    final neumorphicStyle = CustomTheme.neumorphicStyle(context);
    final linearGradient = CustomTheme.linearGradient2(context);
    final subtitle = CustomTheme.buttonSubtitle(context);
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
      decoration: BoxDecoration(gradient: linearGradient),
      padding: EdgeInsets.only(
          left: width * 0.08,
          right: width * 0.08,
          top: height * 0.06,
          bottom: height * 0.095),
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
                style: neumorphicStyle,
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
                                style: buttonTrailing.copyWith(
                                    fontSize: width * 0.06),
                              ),
                            ),
                            Neumorphic(
                              style: neumorphicStyle.copyWith(
                                  boxShape: NeumorphicBoxShape.circle()),
                              // TODO : show circular progress indicator while loading image
                              child: CircleAvatar(
                                child: (sisData.studentImage ==
                                        "http://parents.msrit.edu/images/defaultimages.png")
                                    ? Icon(Icons.person)
                                    : null,
                                backgroundImage: (sisData.studentImage !=
                                        "http://parents.msrit.edu/images/defaultimages.png")
                                    ? CachedNetworkImageProvider(
                                        sisData.studentImage,
                                      )
                                    : null,
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
                            style:
                                buttonTitle.copyWith(fontSize: width * 0.045),
                          ),
                          Container(
                            padding: EdgeInsets.symmetric(
                                vertical: height * 0.01,
                                horizontal: width * 0.02),
                            child: Text(
                              "${sisData.semester}-${sisData.section[4]}",
                              style: subtitle,
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
                            style:
                                buttonTitle.copyWith(fontSize: width * 0.045),
                          ),
                          Container(
                            padding: EdgeInsets.symmetric(
                                vertical: height * 0.01,
                                horizontal: width * 0.02),
                            child: Text(sisData.course, style: subtitle),
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
              child: Divider(
                color: sisData.darkMode ? Colors.white38 : Colors.black26,
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
                    style: buttonTrailing,
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
                        style: neumorphicStyle,
                        child: Theme(
                          data: Theme.of(context)
                              .copyWith(dividerColor: Colors.transparent),
                          child: ExpansionTile(
                            title: Text(
                              e.amountPaid,
                              style: buttonTrailing.copyWith(
                                  fontSize: width * 0.06),
                            ),
                            subtitle: Padding(
                              padding: EdgeInsets.symmetric(
                                  horizontal: width * 0.02,
                                  vertical: height * 0.01),
                              child: Text(
                                "For Year ${e.yearNumber} on ${e.date}",
                                style: subtitle,
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
                                      style: title,
                                    ),
                                    Text(
                                      e.challanNumber,
                                      style: subtitle,
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
                                            style: title,
                                          ),
                                          Expanded(
                                            child: Text(
                                              e.chequeNumber,
                                              style: subtitle,
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
