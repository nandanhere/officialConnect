import 'package:auto_size_text/auto_size_text.dart';
import 'package:official_connect/Providers/dummy_data.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/branch_syllabus.dart';
import 'package:provider/provider.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:string_similarity/string_similarity.dart';
import 'package:official_connect/Providers/themes.dart';

class SyllabusScreen extends StatelessWidget {
  const SyllabusScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final sisData = Provider.of<SisData>(context);
    final buttonTitle = CustomTheme.buttonTitle(context);
    final titleStyle = CustomTheme.titleStyle(context);
    final neumorphicStyle = CustomTheme.neumorphicStyle(context);
    final linearGradient = CustomTheme.linearGradient(context);
    final linearGradientBG = CustomTheme.linearGradientBG(context);
    //var fullCourseName = sisData.courseFullName.split("-")[1];
    // we show on top the closest matches to user's branch. so they can see other syllabi aswell if they wish
    final List<String> sorted = DummyData.syllabusLinks.keys.toList();
    sorted.sort((a, b) =>
        StringSimilarity.compareTwoStrings(a, sisData.courseFullName) >
                StringSimilarity.compareTwoStrings(b, sisData.courseFullName)
            ? -1
            : 1);
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: linearGradientBG,
        ),
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
                  "Syllabi",
                  maxFontSize: 45,
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
                // ...DummyData.syllabusLinks.keys
                //     .map((name) => ((RegExp(r"[\w\s]*" + fullCourseName + r"$")
                //             .hasMatch(name))
                //         ? Padding(
                //             //map
                //             padding: const EdgeInsets.all(8.0),
                //             child: NeumorphicButton(
                //               padding: EdgeInsets.only(
                //                   top: height * 0.015,
                //                   bottom: height * 0.015,
                //                   left: width * 0.025,
                //                   right: width * 0.01),
                //               onPressed: () {
                //                 Navigator.of(context).push(MaterialPageRoute(
                //                     builder: (ctx) => BranchSyllabus(
                //                           name: name,
                //                         )));
                //               },
                //               style: neumorphicStyle,
                //               child: ListTile(
                //                 title: Text(name, style: buttonTitle),
                //               ),
                //             ),
                //           )
                //         : Container())),
                ...sorted
                    .map((name) => Padding(
                          //map
                          padding: const EdgeInsets.all(8.0),
                          child: NeumorphicButton(
                            padding: EdgeInsets.only(
                                top: height * 0.015,
                                bottom: height * 0.015,
                                left: width * 0.025,
                                right: width * 0.01),
                            onPressed: () {
                              Navigator.of(context).push(
                                MaterialPageRoute(
                                  builder: (ctx) => BranchSyllabus(
                                    name: name,
                                  ),
                                ),
                              );
                            },
                            style: neumorphicStyle,
                            child: ListTile(
                              title: Text(name, style: buttonTitle),
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
