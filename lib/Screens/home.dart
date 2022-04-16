import 'package:flutter/material.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/LoginScreen.dart';
import 'package:provider/provider.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

class Home extends StatelessWidget {
  static const String id = "home";
  const Home({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    if (sisData.usn == "" || sisData.data.isEmpty)
      return LoginScreen();
    else {
      return Scaffold(
        backgroundColor: Color(0xFF852528),
        appBar: AppBar(
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
            child: Hero(
              tag: "bar",
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
                          route: "",
                          selected: true,
                        ),
                        Button(
                          icon: FontAwesomeIcons.calendarDay,
                          route: "attendance",
                          selected: false,
                        )
                      ],
                    ),
                    Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Button(
                          icon: FontAwesomeIcons.graduationCap,
                          route: "cie",
                          selected: false,
                        ),
                        Button(
                          icon: FontAwesomeIcons.gear,
                          route: "settings",
                          selected: false,
                        )
                      ],
                    ),
                  ],
                ),
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
  final String route;
  final bool selected;
  Button({required this.icon, required this.route, required this.selected});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 20, vertical: 20),
      child: IconButton(
        onPressed: () {
          Navigator.pushNamed(context, route);
        },
        color: selected ? Color(0xFF852528) : Colors.black87,
        icon: FaIcon(icon),
        iconSize: 60,
      ),
    );
  }
}
