import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/LoadingScreen.dart';
import 'package:official_connect/Screens/home.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Screens/AttendanceInfo.dart';
import 'package:official_connect/Screens/CieScreen.dart';
import 'package:official_connect/Screens/SettingsScreen.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'LoginScreen.dart';

ValueNotifier<int> screenNumber = ValueNotifier(0);

class Unified extends StatelessWidget {
  static const String id = "unified";
  Unified({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    final size = MediaQuery.of(context).size;

    if (sisData.usn == "" && sisData.data.isEmpty) {
      return LoginScreen();
    } else {
      if (sisData.data.isEmpty) return const LoadingScreen();

      return Scaffold(
        backgroundColor: NeumorphicColors.background,
        body: Stack(
          children: [
            Positioned(
                child: ValueListenableBuilder(
                    valueListenable: screenNumber,
                    builder: (context, int listeningScreenValue, child) =>
                        screenWidget(page: listeningScreenValue))),
            Positioned(
              left: 0,
              right: 0,
              bottom: 0,
              child: SizedBox(
                  height: MediaQuery.of(context).size.height * 0.12,
                  child: ClipRRect(
                      child: ValueListenableBuilder(
                    valueListenable: screenNumber,
                    builder: (context, int listeningValue, child) =>
                        BottomNavigationBar(
                      selectedItemColor: const Color(0xFF852528),
                      unselectedItemColor: Colors.grey,
                      items: [
                        BottomNavigationBarItem(
                          icon: const FaIcon(FontAwesomeIcons.house),
                          label: "Home",
                          backgroundColor: sisData.darkMode
                              ? Colors.black54
                              : NeumorphicColors.background,
                        ),
                        BottomNavigationBarItem(
                          icon: const FaIcon(FontAwesomeIcons.calendarDay),
                          label: "Attendance",
                          backgroundColor: sisData.darkMode
                              ? Colors.black54
                              : NeumorphicColors.background,
                        ),
                        BottomNavigationBarItem(
                          icon: const FaIcon(FontAwesomeIcons.graduationCap),
                          label: "Results",
                          backgroundColor: sisData.darkMode
                              ? Colors.black54
                              : NeumorphicColors.background,
                        ),
                        BottomNavigationBarItem(
                          icon: const FaIcon(FontAwesomeIcons.gear),
                          label: "Settings",
                          backgroundColor: sisData.darkMode
                              ? Colors.black54
                              : NeumorphicColors.background,
                        ),
                      ],
                      currentIndex: listeningValue,
                      onTap: (index) {
                        screenNumber.value = index;
                      },
                    ),
                  ))),
            ),
          ],
        ),
      );
    }
  }
}

class screenWidget extends StatelessWidget {
  int page = 0;
  screenWidget({required this.page});
  @override
  Widget build(BuildContext context) {
    if (page == 3) {
      return GestureDetector(
          child: SettingsInfo(),
          onHorizontalDragUpdate: (val) {
            if (val.delta.dx > 10) {
              screenNumber.value = 2;
            } else if (val.delta.dx < -10) {
              screenNumber.value = 3;
            }
          });
    } else if (page == 2) {
      return GestureDetector(
        child: const CieInfo(),
        onHorizontalDragUpdate: (val) {
          if (val.delta.dx > 10) {
            screenNumber.value = 1;
          } else if (val.delta.dx < -10) {
            screenNumber.value = 3;
          }
        },
      );
    } else if (page == 1) {
      return GestureDetector(
        child: const AttendanceInfo(),
        onPanUpdate: (val) {
          if (val.delta.dx > 10) {
            screenNumber.value = 0;
          } else if (val.delta.dx < -10) {
            screenNumber.value = 2;
          }
        },
      );
    } else {
      return GestureDetector(
        child: const Home(),
        onHorizontalDragUpdate: (val) {
          if (val.delta.dx > 10) {
            screenNumber.value = 0;
          } else if (val.delta.dx < -10) {
            screenNumber.value = 1;
          }
        },
      );
    }
  }
}
