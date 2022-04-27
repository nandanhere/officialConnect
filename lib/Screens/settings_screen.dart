import 'package:official_connect/Screens/unified_screen.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:official_connect/Providers/themes.dart';

class SettingsInfo extends StatelessWidget {
  const SettingsInfo({Key? key}) : super(key: key);

  void _launchURL(String url) async {
    if (!await launch(url)) throw 'Could not launch $url';
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final sisData = Provider.of<SisData>(context);
    final buttonTitle = CustomTheme.buttonTitle(context);
    final buttonTrailing = CustomTheme.buttonTrailing(context);
    final title = CustomTheme.titleStyle(context);
    final neumorphicStyle = CustomTheme.neumorphicStyle(context);
    final linearGradient = CustomTheme.linearGradient2(context);

    List<Element> tiles = [
      //Element(icon: Icons.person, onPressed: () {}, text: "Student Details"),
      Element(
          icon: Icons.lock,
          onPressed: () {
            _launchURL("https://forms.gle/FyF3PZxxonNf8kUz5");
          },
          text: "Feedback"),
      Element(
          icon: Icons.info_outline_rounded,
          onPressed: () => showDialog(
                builder: (context) => AlertDialog(
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(20),
                    ),
                    backgroundColor:
                        sisData.darkMode ? Colors.black87 : Colors.white,
                    title: FittedBox(
                      child: Image.asset(
                        "images/logo.png",
                      ),
                    ),
                    content: Column(
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        Text("RIT Connect",
                            style: title.copyWith(fontSize: width * 0.075)),
                        SizedBox(
                          height: height * 0.02,
                        ),
                        Text(
                          "by",
                          style: title.copyWith(fontSize: width * 0.055),
                        ),
                        SizedBox(
                          height: height * 0.04,
                        ),
                        Padding(
                          padding:
                              EdgeInsets.symmetric(horizontal: width * 0.22),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              Row(
                                //mainAxisAlignment: MainAxisAlignment.center,
                                textBaseline: TextBaseline.alphabetic,
                                children: [
                                  Text(
                                    "N",
                                    style: title.copyWith(
                                      fontSize: width * 0.075,
                                    ),
                                  ),
                                  Text(
                                    "andan",
                                    style:
                                        title.copyWith(fontSize: width * 0.035),
                                  )
                                ],
                              ),
                              Row(
                                //mainAxisAlignment: MainAxisAlignment.center,
                                textBaseline: TextBaseline.alphabetic,
                                children: [
                                  Text(
                                    "A",
                                    style: title.copyWith(
                                      fontSize: width * 0.075,
                                    ),
                                  ),
                                  Text(
                                    "rnav",
                                    style:
                                        title.copyWith(fontSize: width * 0.035),
                                  )
                                ],
                              ),
                              Row(
                                //mainAxisAlignment: MainAxisAlignment.center,
                                textBaseline: TextBaseline.alphabetic,
                                children: [
                                  Text(
                                    "P",
                                    style: title.copyWith(
                                      fontSize: width * 0.075,
                                    ),
                                  ),
                                  Text(
                                    "rateek ",
                                    style:
                                        title.copyWith(fontSize: width * 0.035),
                                  )
                                ],
                              ),
                              Text(
                                "😴",
                                style: title.copyWith(fontSize: width * 0.055),
                              )
                            ],
                          ),
                        )
                      ],
                    ),
                    actions: <Widget>[
                      TextButton(
                        onPressed: () => Navigator.pop(context, 'Cancel'),
                        child: const Text('Ok'),
                      ),
                    ]),
                context: context,
              ),
          text: "About"),
      Element(
        icon: Icons.settings,
        onPressed: () {},
        text: "Dark Mode",
        toggle: true,
      ),
    ];

    return Container(
        decoration: BoxDecoration(gradient: linearGradient),
        padding: EdgeInsets.only(
          left: width * 0.05,
          right: width * 0.05,
          top: height * 0.06,
        ),
        child: ListView(
          physics: const BouncingScrollPhysics(),
          children: [
            Padding(
              padding: EdgeInsets.only(bottom: height * 0.04),
              child: Align(
                alignment: Alignment.topLeft,
                child: Text(
                  "Settings",
                  textAlign: TextAlign.left,
                  style: title,
                ),
              ),
            ),
            // TODO : what is going on here? it is too convoluted.
            ...tiles.map((e) => Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: NeumorphicButton(
                    onPressed: e.toggle
                        ? () {
                            sisData.darkMode = !sisData.darkMode;
                          }
                        : e.onPressed,
                    style: neumorphicStyle,
                    child: ListTile(
                      leading: Icon(
                        e.icon,
                        color: const Color(0xffd93b3f),
                        size: 30,
                      ),
                      title: Text(
                        e.text,
                        style: buttonTitle,
                      ),
                      trailing: e.toggle
                          ? NeumorphicSwitch(
                              style: const NeumorphicSwitchStyle(
                                  trackDepth: 10, thumbDepth: 2),
                              height: width * 0.055,
                              value: sisData.darkMode,
                              onChanged: (value) {
                                sisData.darkMode = value;
                              },
                            )
                          : null,
                    ),
                  ),
                )),
            const SizedBox(
              height: 50,
            ),
            Center(
              child: NeumorphicButton(
                onPressed: () {
                  showDialog(
                      context: context,
                      builder: (ctx) {
                        return AlertDialog(
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(20),
                          ),
                          backgroundColor: sisData.darkMode
                              ? Colors.black
                              : NeumorphicColors.background,
                          title: Text(
                            'Do you want to Log out?',
                            style: buttonTrailing,
                          ),
                          content: Text(
                            'All stored data will be wiped out',
                            style: buttonTitle,
                          ),
                          actions: <Widget>[
                            NeumorphicButton(
                              style: neumorphicStyle,
                              onPressed: () {
                                Navigator.of(context).pop(false);
                              },
                              child: Text(
                                'No',
                                style: buttonTitle,
                              ),
                            ),
                            NeumorphicButton(
                              style: neumorphicStyle,
                              onPressed: () {
                                Unified.screenNumber.value = 0;
                                Navigator.of(context).pop(false);
                                sisData.cleanData();
                              },
                              child: Text(
                                'Yes',
                                style: buttonTitle,
                              ),
                            ),
                          ],
                        );
                      });
                },
                style: neumorphicStyle,
                child: Text(
                  "Sign out",
                  style: buttonTitle,
                ),
              ),
            ),
            SizedBox(
              height: height * 0.095,
            )
          ],
        ));
  }
}

class Element {
  final Function() onPressed;
  final String text;
  bool toggle;
  final IconData icon;
  Element(
      {required this.onPressed,
      required this.text,
      this.toggle = false,
      required this.icon});
}
