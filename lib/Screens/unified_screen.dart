import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/events_screen.dart';
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
  Unified({Key? key}) : super(key: key);
  static ValueNotifier<int> screenNumber = ValueNotifier(2);
  final ValueNotifier<bool> seeOpt = ValueNotifier(false);

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);

    if ((sisData.usn == "" && !sisData.hasData) || !sisData.isValidData) {
      return const LoginScreen();
    } else {
      if (sisData.data.isEmpty) return const LoadingScreen();
      PageController _myCont = PageController(initialPage: 2);

      return Scaffold(
        backgroundColor: NeumorphicColors.background,
        body: Stack(
          children: [
            Positioned(
                child: ValueListenableBuilder(
                    valueListenable: screenNumber,
                    builder: (context, int listeningScreenValue, child) =>
                        PageView(
                          physics: const BouncingScrollPhysics(),
                          controller: _myCont,
                          children: [
                            const EventsScreen(),
                            const AttendanceInfo(),
                            const HomeScreen(),
                            ResultsScreen(seeOpt),
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
              child: ClipRRect(
                borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(
                        MediaQuery.of(context).size.width * 0.05),
                    topRight: Radius.circular(
                        MediaQuery.of(context).size.width * 0.05)),
                child: ValueListenableBuilder(
                  valueListenable: screenNumber,
                  builder: (context, int listeningValue, child) =>
                      BottomNavigationBar(
                    enableFeedback: true,
                    elevation: 0,
                    selectedLabelStyle:
                        const TextStyle(fontFamily: 'Comfortaa'),
                    unselectedLabelStyle:
                        const TextStyle(fontFamily: 'Comfortaa'),
                    selectedItemColor: const Color(0xffba3237),
                    unselectedItemColor: Colors.grey,
                    items: [
                      BottomNavigationBarItem(
                        icon: const FaIcon(Icons.list_alt_rounded),
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
                        icon: const FaIcon(FontAwesomeIcons.house),
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
            ),
          ],
        ),
      );
    }
  }
}
