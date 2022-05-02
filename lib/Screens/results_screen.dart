import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:official_connect/Screens/cie_screen.dart';
import 'package:official_connect/Screens/see_screen.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Providers/themes.dart';

class ResultsScreen extends StatelessWidget {
  final seeOpt;
  ResultsScreen(this.seeOpt);
  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final sisData = Provider.of<SisData>(context);
    final buttonTitle = CustomTheme.buttonTitle(context);
    final buttonTrailing = CustomTheme.buttonTrailing(context);
    final titleStyle = CustomTheme.titleStyle(context);
    final neumorphicStyle = CustomTheme.neumorphicStyle(context);
    final linearGradient = CustomTheme.linearGradient(context);
    final linearGradientBG = CustomTheme.linearGradientBG(context);

    return Container(
      decoration: BoxDecoration(gradient: linearGradientBG),
      child: SingleChildScrollView(
        physics: const BouncingScrollPhysics(),
        child: ValueListenableBuilder(
          valueListenable: seeOpt,
          builder: (context, isSEE, child) => Container(
            decoration: BoxDecoration(
                gradient: seeOpt.value ? linearGradientBG : linearGradient),
            padding: EdgeInsets.only(
              left: width * 0.05,
              right: width * 0.05,
              top: height * 0.06,
            ),
            child: ValueListenableBuilder(
                valueListenable: seeOpt,
                builder: (context, bool isSEE, child) => isSEE
                    ? SEEScreen(
                        height: height,
                        titleStyle: titleStyle,
                        buttonTitle: buttonTitle,
                        isSEE: isSEE,
                        width: width,
                        seeOpt: seeOpt,
                        neumorphicStyle: neumorphicStyle,
                        sisData: sisData,
                        buttonTrailing: buttonTrailing)
                    : CIEScreen(
                        height: height,
                        titleStyle: titleStyle,
                        buttonTitle: buttonTitle,
                        isSEE: isSEE,
                        width: width,
                        seeOpt: seeOpt,
                        neumorphicStyle: neumorphicStyle,
                        sisData: sisData,
                        buttonTrailing: buttonTrailing)),
          ),
        ),
      ),
    );
  }
}
