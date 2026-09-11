import 'package:flutter_neumorphic_plus/flutter_neumorphic.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';

/// Central palette and shared styles. Dark mode uses a soft slate scale
/// instead of pure black; light mode keeps the neumorphic base with a
/// slightly warmer finish. All screens pick these up through the helpers
/// below.
class CustomTheme {
  /// Brand accent used across the app.
  static const Color accent = Color(0xffba3237);
  static const Color accentBright = Color(0xffd93b3f);

  // Dark palette
  static const Color _darkBase = Color(0xff101114);
  static const Color _darkRaised = Color(0xff1b1d22);
  static const Color _darkEdge = Color(0xff26292f);

  // Light palette
  static const Color _lightText = Color(0xff1d1f24);

  static TextStyle textStyle(context) {
    final sisData = Provider.of<SisData>(context);
    return TextStyle(
      color: sisData.darkMode ? Colors.white : _lightText,
      fontSize: (MediaQuery.sizeOf(context).width * 0.04).clamp(14.0, 17.0),
      fontFamily: 'Comfortaa',
    );
  }

  static TextStyle titleStyle(context) {
    final sisData = Provider.of<SisData>(context);
    return TextStyle(
      color: sisData.darkMode ? Colors.white : _lightText,
      fontSize: (MediaQuery.of(context).size.width * 0.09).clamp(28.0, 36.0),
      fontWeight: FontWeight.w600,
      fontFamily: 'Comfortaa',
    );
  }

  static TextStyle buttonSubtitle(context) {
    final sisData = Provider.of<SisData>(context);
    return TextStyle(
      color: sisData.darkMode ? Colors.white54 : Colors.black54,
      fontSize: (MediaQuery.sizeOf(context).width * 0.04).clamp(13.0, 16.0),
      fontFamily: 'Comfortaa',
    );
  }

  static TextStyle buttonTitle(context) {
    final sisData = Provider.of<SisData>(context);
    return TextStyle(
      color: sisData.darkMode ? Colors.white : _lightText,
      fontSize: (MediaQuery.sizeOf(context).width * 0.045).clamp(15.0, 19.0),
      fontFamily: 'Comfortaa',
    );
  }

  static TextStyle buttonTrailing(context) {
    final sisData = Provider.of<SisData>(context);
    return TextStyle(
      color: sisData.darkMode ? Colors.white : _lightText,
      fontSize: (MediaQuery.sizeOf(context).width * 0.055).clamp(17.0, 23.0),
      fontWeight: FontWeight.bold,
      fontFamily: 'Comfortaa',
    );
  }

  static NeumorphicStyle neumorphicStyle(context) {
    final sisData = Provider.of<SisData>(context);
    return NeumorphicStyle(
      shadowLightColor: sisData.darkMode
          ? Colors.white.withValues(alpha: 0.04)
          : null,
      shadowDarkColor: sisData.darkMode
          ? Colors.black.withValues(alpha: 0.7)
          : null,
      border: sisData.darkMode
          ? const NeumorphicBorder(width: 0.6, color: _darkEdge)
          : const NeumorphicBorder(width: 0),
      color: sisData.darkMode ? _darkRaised : NeumorphicColors.background,
      depth: 2,
      boxShape: NeumorphicBoxShape.roundRect(BorderRadius.circular(16)),
    );
  }

  static LinearGradient linearGradient(context) {
    final sisData = Provider.of<SisData>(context);
    return LinearGradient(
      begin: Alignment.bottomRight,
      end: Alignment.topLeft,
      colors: (sisData.darkMode)
          ? const [_darkBase, _darkBase, Color(0xff17181d), Color(0xff1d2026)]
          : [
              NeumorphicColors.background,
              NeumorphicColors.background,
              Colors.white,
            ],
    );
  }

  static LinearGradient linearGradient2(context) {
    final sisData = Provider.of<SisData>(context);
    return LinearGradient(
      begin: Alignment.bottomRight,
      end: Alignment.topLeft,
      colors: (sisData.darkMode)
          ? const [_darkBase, Color(0xff17181d)]
          : [
              NeumorphicColors.background,
              NeumorphicColors.background,
              Colors.white,
              Colors.white,
            ],
    );
  }

  static LinearGradient linearGradientBG(context) {
    final sisData = Provider.of<SisData>(context);
    return LinearGradient(
      begin: Alignment.bottomRight,
      end: Alignment.topCenter,
      colors: (sisData.darkMode)
          ? const [_darkBase, _darkBase, Color(0xff1d2026)]
          : [
              NeumorphicColors.background,
              NeumorphicColors.background,
              Colors.white,
            ],
    );
  }
}
