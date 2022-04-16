import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Screens/AttendanceInfo.dart';
import 'package:official_connect/Screens/CieScreen.dart';
import 'package:official_connect/Screens/SettingsScreen.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';

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

class Unified extends StatelessWidget {
  static const String id = "unified";
  Unified({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    int args = ModalRoute.of(context)!.settings.arguments as int;
    ValueNotifier<int> value = ValueNotifier(args);
    return Scaffold(
      appBar: AppBar(
        title: Expanded(
          child: Text(
              "Hi, ${Provider.of<SisData>(context).studentName.firstFew(2)}",
              style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 20,
                  fontFamily: 'Comfortaa')),
        ),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      backgroundColor: const Color(0xFF852528),
      body: Stack(
        children: [
          Positioned(
              child: ValueListenableBuilder(
                  valueListenable: value,
                  builder: (context, int listeningValue, child) =>
                      screenWidget(page: listeningValue))),
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
                    child: ValueListenableBuilder(
                      valueListenable: value,
                      builder: (context, int listeningValue, child) =>
                          BottomNavigationBar(
                        selectedItemColor: const Color(0xFF852528),
                        unselectedItemColor: Colors.grey,
                        items: const [
                          BottomNavigationBarItem(
                              icon: FaIcon(FontAwesomeIcons.house),
                              label: "Home",
                              backgroundColor: NeumorphicColors.background),
                          BottomNavigationBarItem(
                              icon: FaIcon(FontAwesomeIcons.calendarDay),
                              label: "Attendance",
                              backgroundColor: NeumorphicColors.background),
                          BottomNavigationBarItem(
                              icon: FaIcon(FontAwesomeIcons.graduationCap),
                              label: "Results",
                              backgroundColor: NeumorphicColors.background),
                          BottomNavigationBarItem(
                              icon: FaIcon(FontAwesomeIcons.gear),
                              label: "Settings",
                              backgroundColor: NeumorphicColors.background),
                        ],
                        currentIndex: listeningValue,
                        onTap: (index) {
                          if (index == 0) Navigator.pop(context);
                          value.value = index;
                        },
                      ),
                    ))),
          ),
        ],
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
      return const SettingsInfo();
    } else if (page == 2) {
      return const CieInfo();
    } else if (page == 1) {
      return const AttendanceInfo();
    } else {
      return Container();
    }
  }
}
