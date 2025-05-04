import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter_neumorphic_plus/flutter_neumorphic.dart';
import 'package:official_connect/Classes/previous_result.dart';
import 'package:official_connect/Providers/Themes.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/login_screen/student_home/results_screen/widgets/marks_card.dart';
import 'package:provider/provider.dart';
import 'package:http/http.dart' as http;
import 'dart:convert' as convert;
import 'package:flutter_spinkit/flutter_spinkit.dart';

class LatestResultsDetails extends StatelessWidget {
  const LatestResultsDetails(
      {Key? key, required this.even, required this.suppli})
      : super(key: key);
  final bool even;
  final bool suppli;
  Future<PreviousResult> loadResult(String usn) async {
    // in case you want to test out the api
    // var url = Uri.parse("http://192.168.43.212:5000/" + usn);

    var url = Uri.parse(
        "https://fg9jyaht14.execute-api.us-east-1.amazonaws.com/result" "?usn=${usn.trim()}&suppli=${suppli ? 'yes' : 'no'}&even=${even ? 'yes' : 'no'}");
    http.Response resp = await http.get(url);
    if (resp.statusCode == 200) {
      final Map<String, dynamic> temp = await convert.jsonDecode(resp.body);
      List<Map<String, dynamic>> results = [];
      if (temp['error']) {
        return PreviousResult(
            cgpa: null,
            creditsEarned: null,
            creditsRegistered: null,
            sgpa: null,
            results: [],
            term: null,
            semesterNumber: null);
      }
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
      return s;
    }
    if (resp.statusCode >= 500) {
      print("error1");
      return Future.error("server_error");
    }
    print("error2");
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
                      if (previousResult.term != null)
                        Text(
                          previousResult.term,
                          style:
                              buttonTrailing.copyWith(fontSize: width * 0.06),
                        ),
                      Text(
                          "Latest ${(even & !suppli) ? "Even" : (!even & !suppli) ? "Odd" : "Supplimentary"} Semester",
                          style:
                              buttonTrailing.copyWith(fontSize: width * 0.06)),
                      if (previousResult.cgpa == null)
                        Text(
                          "No results as of yet",
                          style: CustomTheme.titleStyle(context)
                              .copyWith(fontSize: width * 0.08),
                        ),
                      if (previousResult.cgpa != null) ...[
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
                        MarksCard(
                          subjects: previousResult.results,
                          isBackLog: false,
                        )
                      ]
                    ],
                  ),
                ),
              ),
            ),
          );
        } else if (snapshot.hasError) {
          String error = "";
          if (snapshot.error == "server_error") {
            error =
                "We encountered a server error. this could mean a server overload.Please try later";
          } else {
            error = "Unable to fetch results as of now";
          }
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
                      Text("Latest Semester",
                          style:
                              buttonTrailing.copyWith(fontSize: width * 0.06)),
                      Text(error)
                    ],
                  ),
                ),
              ),
            ),
          );
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
