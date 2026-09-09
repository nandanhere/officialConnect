import 'package:flutter/material.dart';
import 'package:official_connect/Screens/login_screen/login_screen.dart';

/// Opens the authenticated portal flow while leaving currently cached data
/// visible if the user cancels or the portal is temporarily unavailable.
Future<void> openPortalRefresh(BuildContext context) async {
  await Navigator.of(context).push(MaterialPageRoute(
    builder: (_) => const LoginScreen(closeAfterSync: true),
  ));
}
