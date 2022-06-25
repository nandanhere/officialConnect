import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:official_connect/Providers/proctor_data.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/login_screen/proctor_home/proctor_home.dart';
import 'package:official_connect/Screens/login_screen/proctor_home/requests_screen.dart';
import 'package:official_connect/Screens/login_screen/proctor_home/sent_messages_screen.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/Themes.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Utils/authentication.dart';

class ProctorUnified extends StatelessWidget {
  static const String id = "unified";
  ProctorUnified({Key? key}) : super(key: key);
  static ValueNotifier<int> screenNumber = ValueNotifier(1);

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    final size = MediaQuery.of(context).size;
    final height = size.height;
    final width = size.width;
    final neumorphicStyle = CustomTheme.neumorphicStyle(context);
    final proctorData = Provider.of<ProctorData>(context);
    PageController _myCont = PageController(initialPage: 1);

    return Scaffold(
      backgroundColor: (sisData.darkMode) ? Colors.black : Colors.white,
      body: Stack(
        children: [
          Positioned(
              child: ValueListenableBuilder(
                  valueListenable: screenNumber,
                  builder: (context, int listeningScreenValue, child) =>
                      PageView(
                        physics: const BouncingScrollPhysics(),
                        controller: _myCont,
                        children: const [
                          RequestsScreen(),
                          ProctorHome(),
                          SentMessagesScreen()
                        ],
                        onPageChanged: (page) {
                          screenNumber.value = page;
                        },
                      ))),
          Positioned(
            left: 0,
            right: 0,
            bottom: -height * 0.013,
            child: ClipRRect(
              borderRadius: BorderRadius.only(
                  topLeft:
                      Radius.circular(MediaQuery.of(context).size.width * 0.05),
                  topRight: Radius.circular(
                      MediaQuery.of(context).size.width * 0.05)),
              child: ValueListenableBuilder(
                valueListenable: screenNumber,
                builder: (context, int listeningValue, child) =>
                    BottomNavigationBar(
                  type: BottomNavigationBarType.shifting,
                  enableFeedback: true,
                  elevation: 0,
                  selectedLabelStyle: const TextStyle(fontFamily: 'Comfortaa'),
                  unselectedLabelStyle:
                      const TextStyle(fontFamily: 'Comfortaa'),
                  selectedItemColor: const Color(0xffba3237),
                  unselectedItemColor: Colors.grey,
                  items: [
                    BottomNavigationBarItem(
                      icon: listeningValue == 0
                          ? const FaIcon(
                              Icons.person_add_alt_1,
                              size: 30,
                            )
                          : const FaIcon(
                              Icons.person_add_alt,
                              size: 30,
                            ),
                      label: "",
                      backgroundColor: sisData.darkMode
                          ? Colors.black
                          : NeumorphicColors.background,
                    ),
                    BottomNavigationBarItem(
                      icon: listeningValue == 1
                          ? const FaIcon(
                              Icons.home,
                              size: 35,
                            )
                          : const FaIcon(
                              Icons.home_outlined,
                              size: 35,
                            ),
                      label: "",
                      backgroundColor: sisData.darkMode
                          ? Colors.black
                          : NeumorphicColors.background,
                    ),
                    BottomNavigationBarItem(
                      icon: listeningValue == 2
                          ? const FaIcon(
                              Icons.message_rounded,
                              size: 30,
                            )
                          : const FaIcon(
                              Icons.message_outlined,
                              size: 30,
                            ),
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
