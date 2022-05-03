import 'package:official_connect/Providers/dummy_data.dart';
import 'package:official_connect/Screens/unified_screen.dart';
import 'package:official_connect/Widgets/about_club_dialog.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:official_connect/Providers/themes.dart';

class EventsScreen extends StatelessWidget {
  const EventsScreen({Key? key}) : super(key: key);

  void _launchURL(String url) async {
    if (!await launchUrl(Uri.dataFromString(url)))
      throw 'Could not launch $url';
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
    final linearGradient = CustomTheme.linearGradient(context);
    final linearGradientBG = CustomTheme.linearGradientBG(context);
    var fullCourseName = sisData.courseFullName.split("-")[1];

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
                    "Clubs",
                    textAlign: TextAlign.left,
                    style: title,
                  ),
                ),
              ),
              // TODO : what is going on here? it is too convoluted.

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
    );
  }
}

class Element {
  final Function() onPressed;
  final String text;
  final String img;
  Element({required this.onPressed, required this.text, required this.img});
}
