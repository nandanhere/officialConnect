import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Classes/previous_result.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/login_screen/student_home/results_screen/widgets/marks_card.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/themes.dart';

class ResultsDetails extends StatelessWidget {
  final PreviousResult previousResult;
  const ResultsDetails({Key? key, required this.previousResult})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final buttonTrailing = CustomTheme.buttonTrailing(context);
    final title = CustomTheme.textStyle(context);
    final bool isBackLog =
        previousResult.term.toString().toLowerCase().contains('back');
    return Scaffold(
      backgroundColor:
          (sisData.darkMode) ? Colors.black : NeumorphicColors.background,
      body: SingleChildScrollView(
        child: Container(
          margin: const EdgeInsets.all(8),
          // alignment: Alignment.center,
          // color: Colors.grey,
          child: Padding(
            padding: EdgeInsets.only(
              right: width * 0.05,
              top: height * 0.06,
            ),
            child: Column(
              children: [
                Align(
                  alignment: Alignment.topLeft,
                  child: Row(
                    children: [
                      IconButton(
                          onPressed: () {
                            Navigator.of(context).pop();
                          },
                          icon: Icon(
                            Icons.chevron_left,
                            color: (!sisData.darkMode)
                                ? Colors.black
                                : NeumorphicColors.background,
                          )),
                    ],
                  ),
                ),
                Center(
                  child: AutoSizeText(
                    previousResult.term,
                    maxLines: 1,
                    style: buttonTrailing.copyWith(fontSize: width * 0.08),
                  ),
                ),
                if (!isBackLog) ...[
                  if (previousResult.term.toString().contains('supplementary'))
                    Text("Semester ${previousResult.semesterNumber}",
                        style: buttonTrailing.copyWith(fontSize: width * 0.06)),
                  Card(
                    color:  (sisData.darkMode)
                     ? NeumorphicColors.decorationMaxDarkColor
                      : NeumorphicColors.darkDefaultBorder,
                    elevation: 0.5,
                    shape: const RoundedRectangleBorder(
                        borderRadius: BorderRadius.all(Radius.circular(10))),
                    child: Column(
                      children: [
                        Padding(
                          padding: EdgeInsets.all(height * 0.01),
                          child: Center(
                            child: Padding(
                              padding: EdgeInsets.only(left: width * 0.1),
                              child: Row(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
                                children: [
                                  AutoSizeText(
                                    "SGPA : ${previousResult.sgpa}  ",
                                    style: title,
                                  ),
                                  AutoSizeText(
                                      "CGPA : ${previousResult.cgpa == "" ? previousResult.sgpa : previousResult.cgpa}  ",
                                      style: title)
                                ],
                              ),
                            ),
                          ),
                        ),
                        Padding(
                          padding: EdgeInsets.all(height * 0.01),
                          child: Center(
                            child: Padding(
                              padding: EdgeInsets.only(left: width * 0.1),
                              child: Row(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
                                children: [
                                  AutoSizeText(
                                    "Registered : ${previousResult.creditsRegistered.toString().trim()}  ",
                                    style: title,
                                  ),
                                  AutoSizeText(
                                    "Earned : ${previousResult.creditsEarned.toString().trim()}  ",
                                    style: title,
                                  )
                                ],
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
                SizedBox(height: height * 0.004),
                MarksCard(
                  subjects: previousResult.results,
                  isBackLog: isBackLog,
                )
              ],
            ),
          ),
        ),
      ),
    );
  }
}
