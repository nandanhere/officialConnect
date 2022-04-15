import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:provider/provider.dart';

class Settings extends StatelessWidget {
  static const String id = "settings";
  Settings({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider<ValueNotifier<int>>(
      create: (_) => ValueNotifier<int>(0),
      child: Scaffold(
        backgroundColor: Color(0xFF852528),
        body: Stack(
          children: [
            Container(),
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
                          elevation: 10,
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
                                label: "Settings"),
                          ],
                          currentIndex: value.value,
                          onTap: (index) {
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
