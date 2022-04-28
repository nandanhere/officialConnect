import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/loading_screen.dart';
import 'package:official_connect/Screens/home_screen.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Screens/attendance_info.dart';
import 'package:official_connect/Screens/results_screen.dart';
import 'package:official_connect/Screens/settings_screen.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'login_screen.dart';

// ignore: must_be_immutable
class Unified extends StatelessWidget {
  static const String id = "unified";
  const Unified({Key? key}) : super(key: key);
  static ValueNotifier<int> screenNumber = ValueNotifier(0);

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);

    if ((sisData.usn == "" && !sisData.hasData) || !sisData.isValidData) {
      return const LoginScreen();
    } else {
      if (sisData.data.isEmpty) return const LoadingScreen();
      PageController _myCont = PageController(initialPage: 0);

      return Scaffold(
        backgroundColor: NeumorphicColors.background,
        body: Stack(
          children: [
            Positioned(
                child: ValueListenableBuilder(
                    valueListenable: screenNumber,
                    builder: (context, int listeningScreenValue, child) =>
                        PageView(
                          controller: _myCont,
                          children: [
                            const HomeScreen(),
                            const AttendanceInfo(),
                            ResultsScreen(),
                            const SettingsInfo()
                          ],
                          onPageChanged: (page) {
                            screenNumber.value = page;
                          },
                        ))),
            Positioned(
              left: 0,
              right: 0,
              bottom: 0,
              child: ValueListenableBuilder(
                valueListenable: screenNumber,
                builder: (context, int listeningValue, child) =>
                    BottomNavigationBar(
                  elevation: 0,
                  selectedLabelStyle: const TextStyle(fontFamily: 'Comfortaa'),
                  unselectedLabelStyle:
                      const TextStyle(fontFamily: 'Comfortaa'),
                  selectedItemColor: const Color(0xffba3237),
                  unselectedItemColor: Colors.grey,
                  items: [
                    BottomNavigationBarItem(
                      icon: const FaIcon(FontAwesomeIcons.house),
                      label: "",
                      backgroundColor: sisData.darkMode
                          ? Colors.black
                          : NeumorphicColors.background,
                    ),
                    BottomNavigationBarItem(
                      icon: const FaIcon(FontAwesomeIcons.calendarDay),
                      label: "",
                      backgroundColor: sisData.darkMode
                          ? Colors.black
                          : NeumorphicColors.background,
                    ),
                    BottomNavigationBarItem(
                      icon: const FaIcon(FontAwesomeIcons.graduationCap),
                      label: "",
                      backgroundColor: sisData.darkMode
                          ? Colors.black
                          : NeumorphicColors.background,
                    ),
                    BottomNavigationBarItem(
                      icon: const FaIcon(FontAwesomeIcons.gear),
                      label: "",
                      backgroundColor: sisData.darkMode
                          ? Colors.black
                          : NeumorphicColors.background,
                    ),
                  ],
                  currentIndex: listeningValue,
                  onTap: (index) {
                    _myCont.animateToPage(index,
                        curve: Curves.easeIn,
                        duration: const Duration(milliseconds: 250));
                  },
                ),
              ),
            ),
          ],
        ),
      );
    }
  }
}
