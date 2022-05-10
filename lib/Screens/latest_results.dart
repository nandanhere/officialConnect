import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Classes/previous_result.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Widgets/marks_card.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/themes.dart';
import 'package:http/http.dart' as http;
import 'dart:convert' as convert;
import 'package:flutter_spinkit/flutter_spinkit.dart';

class LatestResultsDetails extends StatelessWidget {
  const LatestResultsDetails({
    Key? key,
  }) : super(key: key);

  Future<PreviousResult> loadResult(String usn) async {
    var url = Uri.parse("https://results-scraper-rit.herokuapp.com/" + usn);
    http.Response resp = await http.get(url);
    if (resp.statusCode == 200) {
      final Map<String, dynamic> temp = await convert.jsonDecode(resp.body);
      List<Map<String, dynamic>> results = [];
      for (List<dynamic> l in temp['results']) {
        // ["MAOE04","APPLIED GRAPH THEORY","3.00","3.00","A"]
        Map<String, dynamic> m = {};
        m = {
          "COURSE CODE": l[0],
          "Credits Earned": l[2],
          "Credits Reg.": l[3],
          "GPA": "-",
          "Grade": l[4],
          "SUBJECT NAME": l[1]
        };
        results.add(m);
      }
      PreviousResult s = PreviousResult(
          cgpa: temp['cgpa'],
          creditsEarned: temp['credits_earned'],
          creditsRegistered: temp['credits_registered'],
          sgpa: temp['sgpa'],
          results: Subject.getList(results),
          term: "",
          semesterNumber: "");
      print("done");
      return s;
    }
    return Future.error('error');
  }

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final buttonTrailing = CustomTheme.buttonTrailing(context);
    final title = CustomTheme.textStyle(context);
    return FutureBuilder<PreviousResult>(
      future: loadResult(sisData.usn),
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          final PreviousResult previousResult = snapshot.data!;
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
                      Text(
                        previousResult.term,
                        style: buttonTrailing.copyWith(fontSize: width * 0.06),
                      ),
                      Text("Latest Semester",
                          style:
                              buttonTrailing.copyWith(fontSize: width * 0.06)),
                      Padding(
                        padding: EdgeInsets.all(height * 0.01),
                        child: Center(
                          child: Padding(
                            padding: EdgeInsets.only(left: width * 0.22),
                            child: Row(
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
                            padding: EdgeInsets.only(left: width * 0.16),
                            child: Row(
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
                      MarksCard(subjects: previousResult.results)
                    ],
                  ),
                ),
              ),
            ),
          );
        } else if (snapshot.hasError) {
          return Text("${snapshot.error}");
        }
        return Scaffold(
          backgroundColor: (sisData.darkMode) ? Colors.black : Colors.white,
          body: const Center(
            child: SpinKitSpinningLines(
              color: Colors.red,
              size: 100.0,
            ),
          ),
        );
      },
    );
  }
}
