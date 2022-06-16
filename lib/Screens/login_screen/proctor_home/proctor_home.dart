import 'package:auto_size_text/auto_size_text.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Providers/dummy_data.dart';
import 'package:official_connect/Utils/authentication.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import "dart:math";
import 'package:official_connect/Providers/themes.dart';
import 'package:flutter/foundation.dart';

extension StringCasingExtension on String {
  String toCapitalized() =>
      length > 0 ? '${this[0].toUpperCase()}${substring(1).toLowerCase()}' : '';
  String toTitleCase() => replaceAll(RegExp(' +'), ' ')
      .split(' ')
      .map((str) => str.toCapitalized())
      .join('\n');
}

class ProctorHome extends StatelessWidget {
  const ProctorHome({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final auth = FirebaseAuth.instance;
    print(auth.currentUser);
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final buttonTitle = CustomTheme.buttonTitle(context);
    final buttonTrailing = CustomTheme.buttonTrailing(context);
    final title = CustomTheme.textStyle(context);
    final neumorphicStyle = CustomTheme.neumorphicStyle(context);
    final linearGradient = CustomTheme.linearGradient(context);
    final linearGradientBG = CustomTheme.linearGradientBG(context);
    final subtitle = CustomTheme.buttonSubtitle(context);
    final emoji = DummyData.emojis[Random().nextInt(DummyData.emojis.length)];
    final sisData = Provider.of<SisData>(context);

    return Container(
      decoration: BoxDecoration(gradient: linearGradientBG),
      child: SingleChildScrollView(
        physics: const BouncingScrollPhysics(),
        child: Container(
          decoration: BoxDecoration(gradient: linearGradient),
          padding: EdgeInsets.only(
            left: width * 0.08,
            right: width * 0.08,
            top: height * 0.06,
          ),
          child: Center(
            child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
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
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
                                mainAxisSize: MainAxisSize.max,
                                children: [
                                  Expanded(
                                    child: AutoSizeText(
                                      "Hi, " +
                                          (auth.currentUser!.displayName ?? ""),
                                      style: buttonTrailing.copyWith(
                                          // fontFamily: "Lobster",
                                          fontSize: width * 0.08,
                                          fontWeight: FontWeight.normal),
                                    ),
                                  ),
                                  Neumorphic(
                                    style: neumorphicStyle.copyWith(
                                        boxShape:
                                            const NeumorphicBoxShape.circle()),
                                    // TODO : show teacher's photo here
                                    child: CircleAvatar(),
                                  ),
                                ],
                              ),
                            ),
                            Padding(
                              padding: EdgeInsets.only(bottom: height * 0.02),
                              child: Row(
                                children: [],
                              ),
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
                  SizedBox(
                    height: height * 0.095,
                  ),
                  Column(
                    children: [
                      NeumorphicButton(
                        style: NeumorphicStyle(
                            intensity: 0.5,
                            color: const Color(0x00c00000),
                            boxShape: NeumorphicBoxShape.roundRect(
                                BorderRadius.circular(30))),
                        child: const Text(
                          "Sign Out",
                          textAlign: TextAlign.center,
                          style: TextStyle(
                              fontWeight: FontWeight.bold,
                              color: Colors.black,
                              fontSize: 20,
                              fontFamily: 'Comfortaa'),
                        ),
                        onPressed: () {
                          signOut();
                          sisData.cleanData();
                          Navigator.pop(context);
                        },
                      ),
                    ],
                  ),
                ]),
          ),
        ),
      ),
    );
  }
}
