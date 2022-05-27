import 'package:fluttertoast/fluttertoast.dart';
import 'package:official_connect/Screens/login_screen/student_home/unified_screen.dart';
import 'package:official_connect/Screens/login_screen/student_home/settings_screen/widgets/about_dialog.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:official_connect/Providers/themes.dart';

const double version = 0.2;

class SettingsInfo extends StatelessWidget {
  const SettingsInfo({Key? key}) : super(key: key);

  void _launchURL(String url) async {
    if (!await launchUrl(Uri.parse(url))) throw 'Could not launch $url';
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
    final linearGradientBG = CustomTheme.linearGradientBG(context);
    // var fullCourseName = sisData.courseFullName.split("-")[1];
    List<Element> tiles = [
      //Element(icon: Icons.person, onPressed: () {}, text: "Student Details"),
      //TODO add links for fee payment and wifi complaint
      Element(
          icon: Icons.attach_money_outlined,
          onPressed: () {
            _launchURL("https://google.com");
          },
          text: "Fee Payment"),
      Element(
          icon: Icons.wifi_off_outlined,
          onPressed: () {
            _launchURL("http://ithelpdesk.msrit.edu/");
          },
          text: "Register WiFi complaint"),

      Element(
        icon: Icons.settings,
        onPressed: () {},
        text: "Dark Mode",
        toggle: true,
      ),
      Element(
          icon: Icons.lock,
          onPressed: () {
            _launchURL("https://forms.gle/FyF3PZxxonNf8kUz5");
          },
          text: "Feedback"),
      Element(
          icon: Icons.info_outline_rounded,
          onPressed: () => showDialog(
                builder: (context) => AboutConnectDialog(
                  sisData: sisData,
                  width: width,
                  title: title,
                  height: height,
                ),
                context: context,
              ),
          text: "About"),
      Element(
          icon: Icons.update,
          onPressed: () async {
            Fluttertoast.showToast(
                msg: "Updating data ",
                toastLength: Toast.LENGTH_LONG,
                gravity: ToastGravity.BOTTOM,
                timeInSecForIosWeb: 1,
                backgroundColor: const Color(0xffba3237),
                textColor: Colors.white,
                fontSize: 16.0);
            await sisData.getData("", "", true);
            Fluttertoast.showToast(
                msg: "Updated data 🎉 ",
                toastLength: Toast.LENGTH_LONG,
                gravity: ToastGravity.BOTTOM,
                timeInSecForIosWeb: 1,
                backgroundColor: const Color(0xffba3237),
                textColor: Colors.white,
                fontSize: 16.0);
          },
          text: "Update data"),
    ];

    return Container(
      decoration: BoxDecoration(gradient: linearGradientBG),
      child: SingleChildScrollView(
        physics: const BouncingScrollPhysics(),
        child: Container(
          decoration: BoxDecoration(gradient: linearGradientBG),
          padding: EdgeInsets.only(
            left: width * 0.05,
            right: width * 0.05,
            top: height * 0.06,
          ),
          child: Column(
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
              SizedBox(
                height: height * 0.06,
              ),
              Center(
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    NeumorphicButton(
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
                                      Unified.screenNumber.value = 2;
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
                    if (sisData.ver != version)
                      NeumorphicButton(
                        onPressed: () {
                          _launchURL(
                              "https://drive.google.com/drive/folders/16rRMfepxMabz7rNBMhybCLbizBtvdpAw?usp=sharing");
                        },
                        style: neumorphicStyle,
                        child: Text(
                          "Update",
                          style: buttonTitle,
                        ),
                      ),
                  ],
                ),
              ),
              SizedBox(
                height: height * 0.05,
              ),

              if (sisData.ver == version)
                Text(
                  "Currently using version " + version.toString(),
                ),
              if (sisData.ver != version) const Text("Using Outdated Verison")
            ],
          ),
        ),
      ),
    );
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
