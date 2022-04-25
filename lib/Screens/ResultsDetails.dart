import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Classes/PreviousResult.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Widgets/MarksCard.dart';
import 'package:provider/provider.dart';

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
                          icon: const Icon(Icons.chevron_left)),
                    ],
                  ),
                ),
                Text(
                  previousResult.term,
                  style: TextStyle(
                    color: sisData.darkMode ? Colors.white : Colors.black,
                    fontSize: MediaQuery.of(context).size.width * 0.06,
                    fontFamily: 'Comfortaa',
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Text(
                  "Semester ${previousResult.semesterNumber}",
                  style: TextStyle(
                    color: sisData.darkMode ? Colors.white : Colors.black,
                    fontSize: MediaQuery.of(context).size.width * 0.06,
                    fontFamily: 'Comfortaa',
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Center(
                    child: Padding(
                      padding: const EdgeInsets.only(left: 30.0),
                      child: Row(
                        children: [
                          AutoSizeText(
                            "SGPA : ${previousResult.sgpa}  ",
                            style: TextStyle(
                              color: sisData.darkMode
                                  ? Colors.white
                                  : Colors.black,
                              fontSize:
                                  MediaQuery.of(context).size.width * 0.04,
                              fontFamily: 'Comfortaa',
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          AutoSizeText(
                            "CGPA : ${previousResult.cgpa == "" ? previousResult.sgpa : previousResult.cgpa}  ",
                            style: TextStyle(
                              color: sisData.darkMode
                                  ? Colors.white
                                  : Colors.black,
                              fontSize:
                                  MediaQuery.of(context).size.width * 0.04,
                              fontFamily: 'Comfortaa',
                              fontWeight: FontWeight.bold,
                            ),
                          )
                        ],
                      ),
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Center(
                    child: Padding(
                      padding: const EdgeInsets.only(left: 30.0),
                      child: Row(
                        children: [
                          AutoSizeText(
                            "Registered : ${previousResult.creditsRegistered.toString().trim()}  ",
                            style: TextStyle(
                              color: sisData.darkMode
                                  ? Colors.white
                                  : Colors.black,
                              fontSize:
                                  MediaQuery.of(context).size.width * 0.04,
                              fontFamily: 'Comfortaa',
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          AutoSizeText(
                            "Earned : ${previousResult.creditsEarned.toString().trim()}  ",
                            style: TextStyle(
                              color: sisData.darkMode
                                  ? Colors.white
                                  : Colors.black,
                              fontSize:
                                  MediaQuery.of(context).size.width * 0.04,
                              fontFamily: 'Comfortaa',
                              fontWeight: FontWeight.bold,
                            ),
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
  }
}
