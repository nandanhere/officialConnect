import 'package:official_connect/Screens/unified_screen.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:official_connect/Providers/themes.dart';

class Events extends StatelessWidget {
  const Events({Key? key}) : super(key: key);

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
    List<Element> tiles = [
      //Element(icon: Icons.person, onPressed: () {}, text: "Student Details"),
      //TODO add links for fee payment and wifi complaint
      Element(
          img: "https://www.easytourz.com/uploads/Businesslogo/1576651414.png",
          onPressed: () {},
          text: "Club1"),
      Element(
          img: "https://www.easytourz.com/uploads/Businesslogo/1576651414.png",
          onPressed: () {},
          text: "Club2"),
      Element(
          img: "https://www.easytourz.com/uploads/Businesslogo/1576651414.png",
          onPressed: () {},
          text: "Club3"),
      Element(
          img: "https://www.easytourz.com/uploads/Businesslogo/1576651414.png",
          onPressed: () {},
          text: "Club4"),
    ];

    return Container(
      decoration: BoxDecoration(gradient: linearGradientBG),
      child: SingleChildScrollView(
        physics: BouncingScrollPhysics(),
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
                    "Activites",
                    textAlign: TextAlign.left,
                    style: title,
                  ),
                ),
              ),
              // TODO : what is going on here? it is too convoluted.
              ...tiles.map((e) => Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: NeumorphicButton(
                      style: neumorphicStyle,
                      onPressed: () {},
                      child: ListTile(
                        leading: Image.network(e.img),
                        trailing: Text(
                          e.text,
                          style: buttonTitle,
                        ),
                      ),
                    ),
                  )),
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
