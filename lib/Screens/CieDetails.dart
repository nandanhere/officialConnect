import 'package:flutter/material.dart';
import 'package:official_connect/Classes/Marks.dart';
import 'package:official_connect/Widgets/CieDetailsGraph.dart';
import 'package:official_connect/Widgets/CieTable.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';

class CieDetails extends StatelessWidget {
  final Marks subjectDetails;
  const CieDetails({Key? key, required this.subjectDetails}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    return Scaffold(
      backgroundColor:
          (sisData.darkMode) ? Colors.black : NeumorphicColors.background,
      // appBar: AppBar(
      //   centerTitle: true,
      //   foregroundColor: const Color(0xFF852528),
      //   backgroundColor: Colors.transparent,
      //   elevation: 0,
      //   title: Text(
      //     "CIE details",
      //     style: TextStyle(
      //         color: const Color(0xFF852528),
      //         fontSize: MediaQuery.of(context).size.width * 0.06,
      //         fontFamily: 'Comfortaa'),
      //   ),
      // ),
      body: SingleChildScrollView(
        child: Container(
          decoration: BoxDecoration(
              gradient: LinearGradient(
                  begin: Alignment.bottomRight,
                  end: Alignment.topLeft,
                  colors: (sisData.darkMode)
                      ? [Colors.black, Colors.black, Colors.blueGrey]
                      : [
                          NeumorphicColors.background,
                          NeumorphicColors.background,
                          Colors.white,
                          Colors.white
                        ])),
          padding: EdgeInsets.only(
              left: width * 0.05,
              right: width * 0.05,
              top: height * 0.06,
              bottom: height * 0.25),
          child: Column(
            children: [
              Padding(
                padding: EdgeInsets.only(bottom: height * 0.04),
                child: Align(
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
                      Text(
                        "CIE Details",
                        textAlign: TextAlign.left,
                        style: TextStyle(
                            color:
                                sisData.darkMode ? Colors.white : Colors.black,
                            fontSize: 40,
                            fontFamily: 'Comfortaa'),
                      ),
                    ],
                  ),
                ),
              ),
              Text(
                subjectDetails.subjectName,
                style: TextStyle(
                    color: sisData.darkMode ? Colors.white : Colors.black,
                    fontSize: MediaQuery.of(context).size.width * 0.05,
                    fontFamily: 'Comfortaa'),
              ),
              Padding(
                padding: EdgeInsets.symmetric(
                  vertical: MediaQuery.of(context).size.height * 0.04,
                  horizontal: MediaQuery.of(context).size.width * 0.04,
                ),
                child: CieDetailsGraph(subjectDetails: subjectDetails),
              ),
              CieTable(
                marks: subjectDetails,
              )
            ],
          ),
        ),
      ),
    );
  }
}
