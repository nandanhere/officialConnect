import 'package:official_connect/Providers/dummy_data.dart';
import 'package:official_connect/Screens/login_screen/student_home/events_screen/widgets/about_club_dialog.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:official_connect/Providers/themes.dart';
import 'package:fluttertoast/fluttertoast.dart';

class EventsScreen extends StatelessWidget {
  const EventsScreen({Key? key}) : super(key: key);

  void _launchURL(String url) async {
    if (!await launchUrl(Uri.dataFromString(url))) {
      throw 'Could not launch $url';
    }
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final sisData = Provider.of<SisData>(context);
    final buttonTitle = CustomTheme.buttonTitle(context);
    final title = CustomTheme.titleStyle(context);
    final neumorphicStyle = CustomTheme.neumorphicStyle(context);
    final linearGradientBG = CustomTheme.linearGradientBG(context);

    return Container(
      decoration: BoxDecoration(gradient: linearGradientBG),
      child: RefreshIndicator(
        displacement: height * 0.1,
        backgroundColor: sisData.darkMode ? Colors.black : Colors.white,
        color: sisData.darkMode
            ? const Color(0xffba3237)
            : const Color(0xffba3227),
        onRefresh: () async {
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
                      "Clubs",
                      textAlign: TextAlign.left,
                      style: title,
                    ),
                  ),
                ),
                ...DummyData.clubs.map(
                  (e) => Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: NeumorphicButton(
                      style: neumorphicStyle,
                      onPressed: () => showDialog(
                        builder: (context) => AboutClubDialog(
                          e: e,
                          sisData: sisData,
                          width: width,
                          title: title,
                          height: height,
                        ),
                        context: context,
                      ),
                      child: ListTile(
                        leading: Image.asset(
                          'images/club_images/' +
                              (sisData.darkMode ? "dark_" : "light_") +
                              e['image']!,
                        ),
                        trailing: Text(
                          e['name']!,
                          style: buttonTitle,
                        ),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class Element {
  final Function() onPressed;
  final String text;
  final String img;
  Element({required this.onPressed, required this.text, required this.img});
}
