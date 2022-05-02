import 'package:advance_pdf_viewer/advance_pdf_viewer.dart';
import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter_cached_pdfview/flutter_cached_pdfview.dart';
import 'package:official_connect/Providers/dummy_data.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Providers/themes.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';

class BranchSyllabus extends StatelessWidget {
  final name;
  const BranchSyllabus({Key? key, this.name}) : super(key: key);
  void _launchURL(BuildContext context, String url) async {
    if (!await launch(url)) throw 'Could not launch $url';
    // Navigator.of(context).push(
    //   MaterialPageRoute(
    //     builder: (ctx) => PDF().fromUrl(url),
    //   ),
    // );
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final buttonTitle = CustomTheme.buttonTitle(context);
    final titleStyle = CustomTheme.titleStyle(context);
    final neumorphicStyle = CustomTheme.neumorphicStyle(context);
    final linearGradient = CustomTheme.linearGradient(context);
    final linearGradientBG = CustomTheme.linearGradientBG(context);
    final sisData = Provider.of<SisData>(context);

    return Scaffold(
      body: Container(
        decoration: BoxDecoration(gradient: linearGradientBG),
        child: SingleChildScrollView(
          physics: const BouncingScrollPhysics(),
          child: Container(
            decoration: BoxDecoration(
              gradient: linearGradient,
            ),
            padding: EdgeInsets.only(
              left: width * 0.05,
              right: width * 0.05,
              top: height * 0.06,
            ),
            child: Column(
              children: [
                AutoSizeText(
                  name,
                  maxFontSize: 30,
                  style: titleStyle,
                ),
                Container(
                  padding: EdgeInsets.symmetric(
                      horizontal: width * 0.16, vertical: height * 0.02),
                  child: Divider(
                    color: sisData.darkMode ? Colors.white38 : Colors.black26,
                    thickness: 1.1,
                  ),
                ),
                ...DummyData.syllabusLinks[name]!
                    .map((l) => Padding(
                          //map
                          padding: const EdgeInsets.all(8.0),
                          child: NeumorphicButton(
                            padding: EdgeInsets.only(
                                top: height * 0.015,
                                bottom: height * 0.015,
                                left: width * 0.025,
                                right: width * 0.01),
                            onPressed: () async {
                              _launchURL(context, l[1]);
                            },
                            style: neumorphicStyle,
                            child: ListTile(
                              title: Text(l[0], style: buttonTitle),
                            ),
                          ),
                        ))
                    .toList(),
                SizedBox(
                  height: height * 0.095,
                )
              ],
            ),
          ),
        ),
      ),
    );
  }
}
