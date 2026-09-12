import 'package:flutter/material.dart';
import 'package:official_connect/Screens/login_screen/student_home/results_screen/cie_sub_screen/cie_screen.dart';
import 'package:official_connect/Screens/login_screen/student_home/results_screen/see_sub_screen/see_screen.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:flutter_neumorphic_plus/flutter_neumorphic.dart';
import 'package:official_connect/Providers/themes.dart';
import 'package:official_connect/Screens/login_screen/portal_refresh.dart';

class ResultsScreen extends StatelessWidget {
  final ValueNotifier<bool> seeOpt;
  const ResultsScreen(this.seeOpt, {Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    final mediaQuery = MediaQuery.of(context);
    final size = mediaQuery.size;
    final width = size.width;
    final height = size.height;
    final sisData = Provider.of<SisData>(context);
    final buttonTitle = CustomTheme.buttonTitle(context);
    final buttonTrailing = CustomTheme.buttonTrailing(context);
    final titleStyle = CustomTheme.titleStyle(context);
    final neumorphicStyle = CustomTheme.neumorphicStyle(context);
    final linearGradient = CustomTheme.linearGradient(context);
    final linearGradientBG = CustomTheme.linearGradientBG(context);
    // Results is information-dense. Keep Android accessibility scaling, while
    // preventing extreme display/font settings from turning it into a tablet
    // layout with clipped controls and disproportionately tall cards.
    final resultsTextScale = mediaQuery.textScaler.scale(1).clamp(0.8, 1.3);
    return MediaQuery(
      data: mediaQuery.copyWith(
        textScaler: TextScaler.linear(resultsTextScale),
      ),
      child: Container(
        decoration: BoxDecoration(gradient: linearGradientBG),
        child: RefreshIndicator(
          displacement: height * 0.1,
          backgroundColor: sisData.darkMode
              ? const Color(0xff101114)
              : Colors.white,
          color: sisData.darkMode
              ? const Color(0xffba3237)
              : const Color(0xffba3227),
          onRefresh: () async {
            await openPortalRefresh(context);
          },
          child: SafeArea(
            bottom: false,
            child: SingleChildScrollView(
              physics: const AlwaysScrollableScrollPhysics(
                parent: BouncingScrollPhysics(),
              ),
              child: ValueListenableBuilder<bool>(
                valueListenable: seeOpt,
                builder: (context, isSEE, child) => Container(
                  decoration: BoxDecoration(
                    gradient: isSEE ? linearGradientBG : linearGradient,
                  ),
                  padding: EdgeInsets.only(
                    left: width * 0.05,
                    right: width * 0.05,
                    top: 18,
                  ),
                  child: isSEE
                      ? SEEScreen(
                          height: height,
                          titleStyle: titleStyle,
                          buttonTitle: buttonTitle,
                          isSEE: isSEE,
                          width: width,
                          seeOpt: seeOpt,
                          neumorphicStyle: neumorphicStyle,
                          sisData: sisData,
                          buttonTrailing: buttonTrailing,
                        )
                      : CIEScreen(
                          height: height,
                          titleStyle: titleStyle,
                          buttonTitle: buttonTitle,
                          isSEE: isSEE,
                          width: width,
                          seeOpt: seeOpt,
                          neumorphicStyle: neumorphicStyle,
                          sisData: sisData,
                          buttonTrailing: buttonTrailing,
                        ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
