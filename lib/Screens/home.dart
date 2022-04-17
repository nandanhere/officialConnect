import 'package:flutter/material.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/LoginScreen.dart';
import 'package:provider/provider.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

extension StringCasingExtension on String {
  String toCapitalized() =>
      length > 0 ? '${this[0].toUpperCase()}${substring(1).toLowerCase()}' : '';
  String toTitleCase() => replaceAll(RegExp(' +'), ' ')
      .split(' ')
      .map((str) => str.toCapitalized())
      .join(' ');
}

extension WordSelection on String {
  String firstFew(int n) =>
      this.toTitleCase().split(" ").sublist(0, n).join(" ");
}

class Home extends StatelessWidget {
  static const String id = "home";
  const Home({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    if (sisData.usn == "" && sisData.data.isEmpty)
      return LoginScreen();
    else {
      if (sisData.data.isEmpty) return CircularProgressIndicator();
      print(sisData.studentImage);
      return Scaffold(
        backgroundColor: Color(0xFF852528),
        appBar: AppBar(
          title: FittedBox(
            child: Text(
                "Hi, ${Provider.of<SisData>(context).studentName.firstFew(2)}",
                style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 20,
                    fontFamily: 'Comfortaa')),
          ),
          elevation: 0,
          backgroundColor: Colors.transparent,
          leading: IconButton(
            color: Colors.white,
            icon: Icon(Icons.logout),
            onPressed: () => sisData.cleanData(),
          ),
        ),
        body: Center(
          child: Neumorphic(
            style: NeumorphicStyle(
                shadowLightColor: Color(0xFFcf5f63),
                shadowDarkColor: Color(0xFF450c0d),
                intensity: 0.9,
                surfaceIntensity: 0.5,
                depth: 10,
                boxShape:
                    NeumorphicBoxShape.roundRect(BorderRadius.circular(20))),
            child: Container(
              padding: EdgeInsets.symmetric(horizontal: 20, vertical: 50),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Button(
                        icon: FontAwesomeIcons.house,
                        selected: true,
                        screen_number: 0,
                      ),
                      Button(
                        icon: FontAwesomeIcons.calendarDay,
                        selected: false,
                        screen_number: 1,
                      )
                    ],
                  ),
                  Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Button(
                        icon: FontAwesomeIcons.graduationCap,
                        selected: false,
                        screen_number: 2,
                      ),
                      Button(
                        icon: FontAwesomeIcons.gear,
                        selected: false,
                        screen_number: 3,
                      )
                    ],
                  ),
                ],
              ),
            ),
          ),
        ),
      );
    }
  }
}

class Button extends StatelessWidget {
  final IconData icon;
  final double size = 60;
  final bool selected;
  final int screen_number;
  Button(
      {required this.icon,
      required this.selected,
      required this.screen_number});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 20, vertical: 20),
      child: IconButton(
        onPressed: () {
          Navigator.pushNamed(context, screen_number == 0 ? "" : "unified",
              arguments: screen_number);
        },
        color: selected ? Color(0xFF852528) : Colors.black87,
        icon: FaIcon(icon),
        iconSize: 60,
      ),
    );
  }
}
