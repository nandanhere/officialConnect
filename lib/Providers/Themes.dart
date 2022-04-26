import 'package:flutter/material.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';

class CustomTheme {
  static TextStyle textStyle(context) {
    final sisData = Provider.of<SisData>(context);
    return TextStyle(
        color: sisData.darkMode ? Colors.white : Colors.black,
        fontSize: MediaQuery.of(context).size.width * 0.04,
        fontFamily: 'Comfortaa');
  }

  static TextStyle titleStyle(context) {
    final sisData = Provider.of<SisData>(context);
    return TextStyle(
        color: sisData.darkMode ? Colors.white : Colors.black,
        fontSize: MediaQuery.of(context).size.width * 0.115,
        fontFamily: 'Comfortaa');
  }

  static TextStyle buttonSubtitle(context) {
    final sisData = Provider.of<SisData>(context);
    return TextStyle(
        color: sisData.darkMode ? Colors.white54 : Colors.black54,
        fontSize: MediaQuery.of(context).size.width * 0.04,
        fontFamily: 'Comfortaa');
  }

  static TextStyle buttonTitle(context) {
    final sisData = Provider.of<SisData>(context);
    return TextStyle(
        color: sisData.darkMode ? Colors.white : Colors.black,
        fontSize: MediaQuery.of(context).size.width * 0.045,
        fontFamily: 'Comfortaa');
  }

  static TextStyle buttonTrailing(context) {
    final sisData = Provider.of<SisData>(context);
    return TextStyle(
        color: sisData.darkMode ? Colors.white : Colors.black,
        fontSize: MediaQuery.of(context).size.width * 0.055,
        fontWeight: FontWeight.bold,
        fontFamily: 'Comfortaa');
  }

  static NeumorphicStyle neumorphicStyle(context) {
    final sisData = Provider.of<SisData>(context);
    return NeumorphicStyle(
        shadowLightColor: sisData.darkMode ? Colors.white : null,
        shadowDarkColor: sisData.darkMode ? NeumorphicColors.background : null,
        color: sisData.darkMode
            ? const Color.fromARGB(1, 77, 74, 74)
            : NeumorphicColors.background,
        depth: 3,
        boxShape: NeumorphicBoxShape.roundRect(BorderRadius.circular(20)));
  }

  static LinearGradient linearGradient(context) {
    final sisData = Provider.of<SisData>(context);
    return LinearGradient(
        begin: Alignment.bottomRight,
        end: Alignment.topLeft,
        colors: (sisData.darkMode)
            ? [Colors.black, Colors.black, Colors.blueGrey]
            : [
                NeumorphicColors.background,
                NeumorphicColors.background,
                Colors.white,
                Colors.white
              ]);
  }

  static LinearGradient linearGradient2(context) {
    final sisData = Provider.of<SisData>(context);
    return LinearGradient(
        begin: Alignment.bottomRight,
        end: Alignment.topLeft,
        colors: (sisData.darkMode)
            ? [
                Colors.black,
                Colors.black,
                Colors.black87
              ] // Equal people seem to like both.. idk what to do about it
            : [
                NeumorphicColors.background,
                NeumorphicColors.background,
                Colors.white,
                Colors.white
              ]);
  }
}
