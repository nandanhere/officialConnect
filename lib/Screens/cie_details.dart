import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:official_connect/Classes/marks.dart';
import 'package:official_connect/Widgets/cie_details_graph.dart';
import 'package:official_connect/Widgets/cie_table.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Providers/themes.dart';

class CIEDetails extends StatelessWidget {
  final Marks subjectDetails;
  const CIEDetails({Key? key, required this.subjectDetails}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final buttonTitle = CustomTheme.buttonTitle(context);
    final titleStyle = CustomTheme.titleStyle(context);
    final linearGradient = CustomTheme.linearGradient2(context);

    return Scaffold(
      backgroundColor:
          (sisData.darkMode) ? Colors.black : NeumorphicColors.background,
      body: SingleChildScrollView(
        child: Container(
          decoration: BoxDecoration(gradient: linearGradient),
          padding: EdgeInsets.only(
              right: width * 0.05, top: height * 0.06, bottom: height * 0.25),
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
                      AutoSizeText("Details",
                          textAlign: TextAlign.left, style: titleStyle),
                    ],
                  ),
                ),
              ),
              Text(subjectDetails.subjectName, style: buttonTitle),
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
