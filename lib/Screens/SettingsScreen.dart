import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:url_launcher/url_launcher.dart';

class SettingsInfo extends StatelessWidget {
  void _logOut(BuildContext context) {}
  void _launchURL(String url) async {
    if (!await launch(url)) throw 'Could not launch $url';
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final sisData = Provider.of<SisData>(context);

    List<Element> tiles = [
      Element(icon: Icons.person, onPressed: () {}, text: "Student Details"),
      Element(
          icon: Icons.lock,
          onPressed: () {
            _launchURL("https://google.com");
          },
          text: "Feedback"),
      Element(
          icon: Icons.info_outline_rounded,
          onPressed: () => showDialog(
                builder: (context) => AlertDialog(
                    backgroundColor:
                        sisData.darkMode ? Colors.black87 : Colors.white,
                    title: FittedBox(
                      child: Image.asset(
                        "images/logo.png",
                      ),
                    ),
                    content: Column(
                      children: [
                        Text(
                          "RIT Connect",
                          style: TextStyle(
                              color: sisData.darkMode
                                  ? Colors.white
                                  : Colors.black,
                              fontSize: width * 0.075,
                              fontFamily: 'Comfortaa'),
                        ),
                        SizedBox(
                          height: height * 0.02,
                        ),
                        Text(
                          "by",
                          style: TextStyle(
                              color: sisData.darkMode
                                  ? Colors.white
                                  : Colors.black,
                              fontSize: width * 0.055,
                              fontFamily: 'Comfortaa'),
                        ),
                      ],
                    ),
                    actions: <Widget>[
                      TextButton(
                        onPressed: () => Navigator.pop(context, 'Cancel'),
                        child: const Text('Ok'),
                      ),
                    ]),
                context: context,
              ),
          text: "About"),
      Element(
        icon: Icons.settings,
        onPressed: () {},
        text: "Dark Mode",
        toggle: true,
      ),
    ];

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
        child: ListView(
          physics: const BouncingScrollPhysics(),
          children: [
            // TODO : what is going on here? it is too convoluted.
            ...tiles.map((e) => Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: NeumorphicButton(
                    onPressed: e.toggle
                        ? () {
                            sisData.darkMode = !sisData.darkMode;
                          }
                        : e.onPressed,
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
                      leading: Icon(
                        e.icon,
                        color: Color(0xffd93b3f),
                        size: 30,
                      ),
                      title: Text(
                        e.text,
                        style: TextStyle(
                            color:
                                sisData.darkMode ? Colors.white : Colors.black,
                            fontSize: width * 0.045,
                            fontFamily: 'Comfortaa'),
                      ),
                      trailing: e.toggle
                          ? NeumorphicSwitch(
                              style: const NeumorphicSwitchStyle(
                                  trackDepth: 10, thumbDepth: 2),
                              height: width * 0.055,
                              value: sisData.darkMode,
                              onChanged: (value) {
                                sisData.darkMode = value;
                              },
                            )
                          : null,
                    ),
                  ),
                )),
            const SizedBox(
              height: 50,
            ),
            Center(
              child: NeumorphicButton(
                onPressed: () {
                  showDialog(
                      context: context,
                      builder: (ctx) {
                        return AlertDialog(
                          backgroundColor: sisData.darkMode
                              ? Colors.black
                              : NeumorphicColors.background,
                          title: Text(
                            'Do you want to Log out?',
                            style: TextStyle(
                                color: sisData.darkMode
                                    ? Colors.white
                                    : Colors.black,
                                fontFamily: 'Comfortaa'),
                          ),
                          content: Text(
                            'All stored data will be wiped out',
                            style: TextStyle(
                                color: sisData.darkMode
                                    ? Colors.white
                                    : Colors.black,
                                fontFamily: 'Comfortaa'),
                          ),
                          actions: <Widget>[
                            NeumorphicButton(
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
                                  BorderRadius.circular(20),
                                ),
                              ),
                              onPressed: () {
                                Navigator.of(context).pop(false);
                              },
                              child: Text(
                                'No',
                                style: TextStyle(
                                    color: sisData.darkMode
                                        ? Colors.white
                                        : Colors.black,
                                    fontFamily: 'Comfortaa'),
                              ),
                            ),
                            NeumorphicButton(
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
                                  BorderRadius.circular(20),
                                ),
                              ),
                              onPressed: () {
                                Navigator.of(context).pop(false);
                                sisData.cleanData();
                              },
                              child: Text(
                                'Yes',
                                style: TextStyle(
                                    color: sisData.darkMode
                                        ? Colors.white
                                        : Colors.black,
                                    fontFamily: 'Comfortaa'),
                              ),
                            ),
                          ],
                        );
                      });
                },
                style: NeumorphicStyle(
                  shadowLightColor: sisData.darkMode ? Colors.white : null,
                  shadowDarkColor:
                      sisData.darkMode ? NeumorphicColors.background : null,
                  color: sisData.darkMode
                      ? Color.fromARGB(1, 77, 74, 74)
                      : NeumorphicColors.background,
                  depth: 2,
                  boxShape: NeumorphicBoxShape.roundRect(
                    BorderRadius.circular(20),
                  ),
                ),
                child: Text(
                  "Sign out",
                  style: TextStyle(
                      color: sisData.darkMode ? Colors.white : Colors.black,
                      fontSize: 15,
                      fontFamily: 'Comfortaa'),
                ),
              ),
            ),
          ],
        ));
  }
}

class Element {
  final Function() onPressed;
  final String text;
  bool toggle;
  final IconData icon;
  Element(
      {required this.onPressed,
      required this.text,
      this.toggle = false,
      required this.icon});
}
