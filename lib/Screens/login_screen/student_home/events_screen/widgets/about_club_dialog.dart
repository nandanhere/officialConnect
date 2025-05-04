// ignore_for_file: prefer_typing_uninitialized_variables

import 'package:flutter_neumorphic_plus/flutter_neumorphic.dart';

import 'package:official_connect/Providers/themes.dart';
import 'package:url_launcher/url_launcher.dart';

class AboutClubDialog extends StatelessWidget {
  final Map<String, String> e;
  final height, width, sisData, title;
  const AboutClubDialog(
      {Key? key,
      this.sisData,
      required this.e,
      this.height,
      this.width,
      this.title})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
      ),
      backgroundColor: sisData.darkMode ? Colors.black87 : Colors.white,
      title: FittedBox(
        child: Image.asset(
          "images/club_images/" +
              (sisData.darkMode ? "dark_" : "light_") +
              e['image']!,
        ),
      ),
      content: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(e['name']!, style: title.copyWith(fontSize: width * 0.075)),
          SizedBox(
            height: height * 0.02,
          ),
          Text(
            e['desc']!,
            style: (title as TextStyle).copyWith(fontSize: 15),
          ),
          SizedBox(
            height: height * 0.04,
          ),
          NeumorphicButton(
            onPressed: () async {
              if (!await launch(e['linktree']!)) throw 'Could not launch  ';
            },
            style: CustomTheme.neumorphicStyle(context).copyWith(
              boxShape: const NeumorphicBoxShape.circle(),
            ),
            child: Image.asset('images/linktree.png', width: 40, height: 40),
          ),
        ],
      ),
      actions: <Widget>[
        NeumorphicButton(
          style: CustomTheme.neumorphicStyle(context),
          onPressed: () {
            Navigator.pop(context, "Cancel");
          },
          child: Text(
            'Ok',
            style: CustomTheme.buttonTitle(context),
          ),
        ),
      ],
    );
  }
}
