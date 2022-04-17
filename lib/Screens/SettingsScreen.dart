import 'package:flutter/material.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';

class SettingsInfo extends StatelessWidget {
  const SettingsInfo({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
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
        child: ListOfSettings());
  }
}

class ListOfSettings extends StatelessWidget {
  List<Widget> tiles = [
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
    return ListView.builder(
      itemBuilder: (context, index) {
        return tiles[index];
      },
      itemCount: tiles.length,
    );
  }
}

class Element extends StatelessWidget {
  final Function() onPressed;
  final String text;
  bool toggle;
  final IconData icon;
  Element(
      {required this.onPressed,
      required this.text,
      this.toggle = false,
      required this.icon});

  ValueNotifier<bool> darkMode = ValueNotifier(false);
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: NeumorphicButton(
        onPressed: toggle
            ? () {
                darkMode.value = !darkMode.value;
              }
            : onPressed,
        style: NeumorphicStyle(
            depth: 3,
            boxShape: NeumorphicBoxShape.roundRect(BorderRadius.circular(20))),
        child: ListTile(
          leading: Icon(
            icon,
            color: Colors.red,
            size: 30,
          ),
          title: Text(
            text,
            style: TextStyle(
                color: Colors.black, fontSize: 15, fontFamily: 'Comfortaa'),
          ),
          trailing: toggle
              ? ValueListenableBuilder(
                  valueListenable: darkMode,
                  builder: (context, bool dark, child) => NeumorphicSwitch(
                    style: NeumorphicSwitchStyle(trackDepth: 10, thumbDepth: 2),
                    height: 20,
                    value: dark,
                    onChanged: (value) {
                      darkMode.value = value;
                    },
                  ),
                )
              : null,
        ),
      ),
    );
  }
}
