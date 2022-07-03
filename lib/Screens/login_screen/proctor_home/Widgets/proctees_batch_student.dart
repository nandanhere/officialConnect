import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Providers/Themes.dart';
import 'package:official_connect/Providers/proctor_data.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/login_screen/proctor_home/Widgets/proctees_card.dart';
import 'package:provider/provider.dart';

class ProcteesBatchStudent extends StatelessWidget {
  final batch;
  const ProcteesBatchStudent({required this.batch, Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final textStyle =
        CustomTheme.textStyle(context).copyWith(fontSize: width * 0.045);
    final proctorData = Provider.of<ProctorData>(context);
    final buttonTitle = CustomTheme.buttonTitle(context);
    final buttonTrailing = CustomTheme.buttonTrailing(context);
    final titleStyle = CustomTheme.titleStyle(context);
    final neumorphicStyle = CustomTheme.neumorphicStyle(context);
    final linearGradient = CustomTheme.linearGradient(context);
    final sisData = Provider.of<SisData>(context);
    return Scaffold(
        backgroundColor:
            (sisData.darkMode) ? Colors.black : NeumorphicColors.background,
        body: SingleChildScrollView(
          child: Container(
            // decoration: BoxDecoration(gradient: linearGradient),
            margin: const EdgeInsets.all(8),
            child: Padding(
              padding: EdgeInsets.only(
                left: width * 0.05,
                right: width * 0.05,
                top: height * 0.06,
              ),
              child: Column(children: [
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
                      SizedBox(
                        width: width * 0.03,
                      ),
                      Expanded(
                          child: AutoSizeText(
                        '$batch',
                        style: textStyle.copyWith(
                          fontWeight: FontWeight.bold,
                          fontSize: MediaQuery.of(context).size.width * 0.088,
                        ),
                      ))
                    ],
                  ),
                ),
                SizedBox(height: height * 0.02),
                // Neumorphic(
                //   style: neumorphicStyle.copyWith(
                //     color: sisData.darkMode
                //         // ? const Color.fromARGB(1, 77, 74, 74)
                //         ? Colors.black.withOpacity(0.4)
                //         : NeumorphicColors.background.withAlpha(150),
                //   ),
                   
                  
                // )

               ...proctorData.enrolled.where((element) => element['batch'] == batch).map((e) {
                                return ProcteesCard(
                                  name: e['name'],
                                  usn: e['usn'],
                                  height: height,
                                  width: width,
                                  title: CustomTheme.buttonTitle(context),
                                  subtitle: CustomTheme.buttonSubtitle(context),
                                  neumorphicStyle: neumorphicStyle,
                                  buttonTrailing: buttonTrailing,
                                  isDark: sisData.darkMode,
                                );
                              }).toList()
              ]),
            ),
          ),
        ));
  }
}
