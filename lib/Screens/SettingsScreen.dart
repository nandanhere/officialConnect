import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';

class SettingsInfo extends StatelessWidget {
  void _logOut(BuildContext context) {}

  List<Element> tiles = [
    Element(icon: Icons.person, onPressed: () {}, text: "Student Details"),
    Element(icon: Icons.lock, onPressed: () {}, text: "Change Password"),
    Element(icon: Icons.doorbell, onPressed: () {}, text: "Log Out"),
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
          color: NeumorphicColors.background,
        ),
        padding: EdgeInsets.only(
            left: width * 0.05,
            right: width * 0.05,
            top: height * 0.06,
            bottom: height * 0.13),
        child: ListView(
          children: [
            // TODO : what is going on here? it is too convoluted.
            ...tiles.map((e) => Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: NeumorphicButton(
                    onPressed: e.toggle
                        ? () {
                            e.darkMode.value = !e.darkMode.value;
                          }
                        : e.onPressed,
                    style: NeumorphicStyle(
                        depth: 3,
                        boxShape: NeumorphicBoxShape.roundRect(
                            BorderRadius.circular(20))),
                    child: ListTile(
                      leading: Icon(
                        e.icon,
                        color: Color(0xFF852528),
                        size: 30,
                      ),
                      title: Text(
                        e.text,
                        style: const TextStyle(
                            color: Colors.black,
                            fontSize: 15,
                            fontFamily: 'Comfortaa'),
                      ),
                      trailing: e.toggle
                          ? ValueListenableBuilder(
                              valueListenable: e.darkMode,
                              builder: (context, bool dark, child) =>
                                  NeumorphicSwitch(
                                style: const NeumorphicSwitchStyle(
                                    trackDepth: 10, thumbDepth: 2),
                                height: 20,
                                value: dark,
                                onChanged: (value) {
                                  e.darkMode.value = value;
                                },
                              ),
                            )
                          : null,
                    ),
                  ),
                )),
            const SizedBox(
              height: 100,
            ),
            Center(
              child: NeumorphicButton(
                onPressed: () {
                  showDialog(
                      context: context,
                      builder: (ctx) {
                        return AlertDialog(
                          backgroundColor: NeumorphicColors.background,
                          title: const Text(
                            'Do you want to Log out?',
                            style: TextStyle(
                                color: Colors.black, fontFamily: 'Comfortaa'),
                          ),
                          content: const Text(
                            'All stored data will be wiped out',
                            style: TextStyle(
                                color: Colors.black, fontFamily: 'Comfortaa'),
                          ),
                          actions: <Widget>[
                            NeumorphicButton(
                              onPressed: () {
                                Navigator.of(context).pop(false);
                              },
                              child: const Text('No'),
                            ),
                            NeumorphicButton(
                              onPressed: () {
                                Navigator.of(context).pop(false);
                                sisData.cleanData();
                              },
                              child: const Text('Yes'),
                            ),
                          ],
                        );
                      });
                },
                style: NeumorphicStyle(
                  depth: 3,
                  boxShape: NeumorphicBoxShape.roundRect(
                    BorderRadius.circular(20),
                  ),
                ),
                child: const Text(
                  "Sign out",
                  style: TextStyle(
                      color: Colors.black,
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
  Element({
    required this.onPressed,
    required this.text,
    this.toggle = false,
    required this.icon,
  });
  ValueNotifier<bool> darkMode = ValueNotifier(false);
}
