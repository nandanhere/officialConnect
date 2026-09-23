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
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
      stops: const [0.0, 0.55, 1.0],
      colors: (sisData.darkMode)
          ? const [Color(0xff171a20), Color(0xff12151a), _darkBase]
          : [
              const Color(0xfff7f9fa),
              const Color(0xfff1f5f6),
              const Color(0xffe9eff1),
            ],
    );
  }

  static LinearGradient linearGradient2(context) {
    final sisData = Provider.of<SisData>(context);
    return LinearGradient(
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
      stops: const [0.0, 1.0],
      colors: (sisData.darkMode)
          ? const [Color(0xff171a20), _darkBase]
          : [const Color(0xfff7f9fa), const Color(0xffe9eff1)],
    );
  }

  static LinearGradient linearGradientBG(context) {
    final sisData = Provider.of<SisData>(context);
    return LinearGradient(
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
      stops: const [0.0, 0.58, 1.0],
      colors: (sisData.darkMode)
          ? const [Color(0xff171a20), Color(0xff12151a), _darkBase]
          : [
              const Color(0xfff7f9fa),
              const Color(0xfff1f5f6),
              const Color(0xffe9eff1),
            ],
    );
  }
}
