import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:provider/provider.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';

class Settings extends StatelessWidget {
  static const String id = "settings";
  Settings({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider<ValueNotifier<int>>(
      create: (_) => ValueNotifier<int>(3),
      child: Scaffold(
        appBar: AppBar(
          backgroundColor: Colors.transparent,
          elevation: 0,
        ),
        backgroundColor: Color(0xFF852528),
        body: Stack(
          children: [
            Positioned(
                child: Consumer<ValueNotifier<int>>(
                    builder: (context, value, child) =>
                        screenWidget(page: value.value))),
            Positioned(
              left: 0,
              right: 0,
              bottom: 0,
              child: SizedBox(
                  height: MediaQuery.of(context).size.height * 0.12,
                  child: ClipRRect(
                      borderRadius: const BorderRadius.only(
                          topRight: Radius.circular(20),
                          topLeft: Radius.circular(20)),
                      child: Consumer<ValueNotifier<int>>(
                        builder: (context, value, child) => BottomNavigationBar(
                          selectedItemColor: Color(0xFF852528),
                          unselectedItemColor: Colors.grey,
                          items: const [
                            BottomNavigationBarItem(
                                icon: FaIcon(FontAwesomeIcons.house),
                                label: "Home"),
                            BottomNavigationBarItem(
                                icon: FaIcon(FontAwesomeIcons.calendarDay),
                                label: "Attendance"),
                            BottomNavigationBarItem(
                                icon: FaIcon(FontAwesomeIcons.graduationCap),
                                label: "Results"),
                            BottomNavigationBarItem(
                                icon: FaIcon(FontAwesomeIcons.gear),
                                label: "Settings",
                                backgroundColor: NeumorphicColors.background),
                          ],
                          currentIndex: value.value,
                          onTap: (index) {
                            if (index == 0) Navigator.pop(context);
                            value.value = index;
                          },
                        ),
                      ))),
            ),
          ],
        ),
      ),
    );
  }
}

class screenWidget extends StatelessWidget {
  int page = 0;
  screenWidget({required this.page});
  @override
  Widget build(BuildContext context) {
    if (page == 3) {
      return Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(30),
            color: NeumorphicColors.background,
          ),
          padding: EdgeInsets.symmetric(horizontal: 20, vertical: 20),
          child: ListOfElements());
    } else
      return Container();
  }
}

class ListOfElements extends StatelessWidget {
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
        return Padding(
          padding: const EdgeInsets.all(8.0),
          child: tiles[index],
        );
      },
      itemCount: tiles.length,
    );
  }
}

class Element extends StatefulWidget {
  final Function() onPressed;
  final String text;
  bool toggle;
  final IconData icon;
  Element(
      {required this.onPressed,
      required this.text,
      this.toggle = false,
      required this.icon});

  @override
  State<Element> createState() => _ElementState();
}

class _ElementState extends State<Element> {
  @override
  bool darkMode = false;
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(5.0),
      child: NeumorphicButton(
        padding: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
        onPressed: widget.onPressed,
        style: NeumorphicStyle(
            depth: 8,
            boxShape: NeumorphicBoxShape.roundRect(BorderRadius.circular(20))),
        child: ListTile(
          leading: Icon(
            widget.icon,
            color: Colors.red,
            size: 30,
          ),
          title: Text(
            widget.text,
            style: TextStyle(
                color: Colors.black, fontSize: 15, fontFamily: 'Comfortaa'),
          ),
          trailing: widget.toggle
              ? NeumorphicSwitch(
                  style: NeumorphicSwitchStyle(trackDepth: 10, thumbDepth: 2),
                  height: 20,
                  value: darkMode,
                  onChanged: (value) {
                    setState(() {
                      darkMode = value;
                    });
                  },
                )
              : null,
        ),
      ),
    );
  }
}
