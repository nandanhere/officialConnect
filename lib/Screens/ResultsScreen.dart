import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:official_connect/Screens/CieScreen.dart';
import 'package:official_connect/Screens/SEEScreen.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Providers/Themes.dart';

class ResultsScreen extends StatelessWidget {
  ResultsScreen({Key? key}) : super(key: key);
  @override
  ValueNotifier<bool> seeOpt = ValueNotifier(false);
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
    return Container(
      decoration: BoxDecoration(gradient: linearGradient),
      padding: EdgeInsets.only(
          left: width * 0.05,
          right: width * 0.05,
          top: height * 0.06,
          bottom: height * 0.095),
      child: SingleChildScrollView(
        physics: const BouncingScrollPhysics(),
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
    );
  }
}
