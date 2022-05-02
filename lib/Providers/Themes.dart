import 'package:flutter/cupertino.dart';
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
        shadowLightColor: sisData.darkMode ? Colors.blueGrey.shade600 : null,
        shadowDarkColor: sisData.darkMode ? Colors.grey.shade900 : null,
        border: sisData.darkMode
            ? NeumorphicBorder(width: 0.14, color: Colors.grey.shade900)
            : NeumorphicBorder(width: 0),
        color: sisData.darkMode
            // ? const Color.fromARGB(1, 77, 74, 74)
            ? Colors.black.withOpacity(0.4)
            : NeumorphicColors.background,
        depth: 3,
        //intensity: sisData.darkMode ? 0.7 : null,
        boxShape: NeumorphicBoxShape.roundRect(BorderRadius.circular(20)));
  }

  static LinearGradient linearGradient(context) {
    final sisData = Provider.of<SisData>(context);
    return LinearGradient(
        begin: Alignment.bottomRight,
        end: Alignment.topLeft,
        colors: (sisData.darkMode)
            ? [
                Colors.black,
                Colors.black,
                Colors.black,
                Colors.black,
                Colors.blueGrey.shade900
              ]
            : [
                NeumorphicColors.background,
                NeumorphicColors.background,
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

  static LinearGradient linearGradientBG(context) {
    final sisData = Provider.of<SisData>(context);
    return LinearGradient(
        begin: Alignment.bottomRight,
        end: Alignment.topCenter,
        colors: (sisData.darkMode)
            ? [Colors.black, Colors.black, Colors.blueGrey.shade900]
            : [
                NeumorphicColors.background,
                NeumorphicColors.background,
                Colors.white
              ]);
  }
}

// ThemeData t = ThemeData(textTheme: TextTheme(
//   bodyMedium: TextStyle(
//       color: sisData.darkMode ? Colors.white : Colors.black,
//       fontSize: MediaQuery.of(context).size.width * 0.055,
//       fontWeight: FontWeight.bold,
//       fontFamily: 'Comfortaa'),
//   bodyLarge: TextStyle(
//       color: sisData.darkMode ? Colors.white : Colors.black,
//       fontSize: MediaQuery.of(context).size.width * 0.045,
//       fontFamily: 'Comfortaa'),
//   subtitle1: TextStyle(
//       color: sisData.darkMode ? Colors.white54 : Colors.black54,
//       fontSize: MediaQuery.of(context).size.width * 0.04,
//       fontFamily: 'Comfortaa'),
//   titleLarge: TextStyle(
//       color: sisData.darkMode ? Colors.white : Colors.black,
//       fontSize: MediaQuery.of(context).size.width * 0.115,
//       fontFamily: 'Comfortaa'),
//
//   bodySmall: TextStyle(
//       color: sisData.darkMode ? Colors.white : Colors.black,
//       fontSize: MediaQuery.of(context).size.width * 0.04,
//       fontFamily: 'Comfortaa')
// ));
