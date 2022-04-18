import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';

class SettingsInfo extends StatelessWidget {
  List<Element> tiles = [
    Element(icon: Icons.person, onPressed: () {}, text: "Student Details"),
    Element(icon: Icons.lock, onPressed: () {}, text: "Change Password"),
    Element(icon: Icons.doorbell, onPressed: () {}, text: "Notification"),
    Element(
      icon: Icons.settings,
      onPressed: () {},
      text: "Dark Mode",
      toggle: true,
    ),
  ];
  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final sisData = Provider.of<SisData>(context);
    return Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(width * 0.08),
          color: sisData.darkMode ? Colors.black : NeumorphicColors.background,
        ),
        padding: EdgeInsets.only(
            left: width * 0.05,
            right: width * 0.05,
            top: height * 0.06,
            bottom: height * 0.13),
        child: ListView(
          children: [
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
                        color: Colors.red,
                        size: 30,
                      ),
                      title: Text(
                        e.text,
                        style: TextStyle(
                            color:
                                sisData.darkMode ? Colors.white : Colors.black,
                            fontSize: 15,
                            fontFamily: 'Comfortaa'),
                      ),
                      trailing: e.toggle
                          ? NeumorphicSwitch(
                              style: const NeumorphicSwitchStyle(
                                  trackDepth: 10, thumbDepth: 2),
                              height: 20,
                              value: sisData.darkMode,
                              onChanged: (value) {
                                sisData.darkMode = value;
                              },
                            )
                          : null,
                    ),
                  ),
                ))
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
