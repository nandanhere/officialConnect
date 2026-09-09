import 'package:flutter/material.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/login_screen/login_screen.dart';
import 'package:official_connect/Screens/login_screen/portal_login_screen.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

bool _portalRefreshInFlight = false;

/// Refreshes portal data in place: the authenticated portal flow runs
/// off-screen and a small notification reports the outcome. Falls back to
/// the full sync page when no saved login exists or the background sync
/// needs user attention.
Future<void> openPortalRefresh(BuildContext context) async {
  if (_portalRefreshInFlight) return;
  _portalRefreshInFlight = true;
  try {
    final messenger = ScaffoldMessenger.of(context);
    final sisData = Provider.of<SisData>(context, listen: false);
    final prefs = await SharedPreferences.getInstance();
    final usn = prefs.getString('portal_usn') ?? '';
    final dob = prefs.getString('portal_dob') ?? '';
    final verificationType = prefs.getString('portal_verification_type') ??
        "Father's mobile number";
    final verificationValue =
        prefs.getString('portal_verification_value') ?? '';
    if (!context.mounted) return;

    Future<void> openFullSyncPage() => Navigator.of(context).push(
          MaterialPageRoute(
            builder: (_) => const LoginScreen(closeAfterSync: true),
          ),
        );

    // Without a complete saved login the user must review the form, so keep
    // the original full-page flow.
    if (usn.isEmpty || dob.isEmpty || verificationValue.isEmpty) {
      await openFullSyncPage();
      return;
    }
    if (usn.trim().toUpperCase() == 'DUMMY') {
      await sisData.getData('DUMMY', '', false);
      return;
    }

    final synced = await Navigator.of(context).push<bool>(
      PageRouteBuilder(
        opaque: false,
        transitionDuration: Duration.zero,
        reverseTransitionDuration: Duration.zero,
        pageBuilder: (_, __, ___) => PortalLoginScreen(
          silent: true,
          initialUsn: usn.trim().toUpperCase(),
          initialDob: dob,
          initialVerificationType: verificationType,
          initialVerificationValue: verificationValue,
          reuseSession: sisData.hasData &&
              sisData.usn.trim().toUpperCase() == usn.trim().toUpperCase(),
        ),
      ),
    );
    if (!context.mounted) return;

    if (synced == true) {
      messenger
        ..hideCurrentSnackBar()
        ..showSnackBar(
          const SnackBar(
            behavior: SnackBarBehavior.floating,
            duration: Duration(seconds: 2),
            content: Text('Your information is up to date.'),
          ),
        );
    } else {
      messenger
        ..hideCurrentSnackBar()
        ..showSnackBar(
          SnackBar(
            behavior: SnackBarBehavior.floating,
            duration: const Duration(seconds: 5),
            content: const Text(
              'Could not refresh in the background.',
            ),
            action: SnackBarAction(
              label: 'Open sync',
              onPressed: () {
                if (context.mounted) openFullSyncPage();
              },
            ),
          ),
        );
    }
  } finally {
    _portalRefreshInFlight = false;
  }
}
