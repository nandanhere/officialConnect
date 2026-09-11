import 'dart:async';

import 'package:flutter/material.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/login_screen/login_screen.dart';
import 'package:official_connect/Screens/login_screen/portal_login_screen.dart';
import 'package:official_connect/Services/firebase_feature_flags.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

bool _portalRefreshInFlight = false;

enum BackgroundSyncState { idle, updating, success, partial, error }

/// Lightweight app-wide state for the status chip shown above navigation.
/// It deliberately lives with the refresh coordinator so screens do not need
/// to maintain separate loading flags or block their own content.
final ValueNotifier<BackgroundSyncState> backgroundSyncState = ValueNotifier(
  BackgroundSyncState.idle,
);

Timer? _statusTimer;

void setBackgroundSyncState(
  BackgroundSyncState state, {
  Duration visibleFor = const Duration(seconds: 3),
}) {
  _statusTimer?.cancel();
  backgroundSyncState.value = state;
  if (state != BackgroundSyncState.idle &&
      state != BackgroundSyncState.updating) {
    _statusTimer = Timer(visibleFor, () {
      backgroundSyncState.value = BackgroundSyncState.idle;
    });
  }
}

/// Refreshes portal data in place: the authenticated portal flow runs
/// off-screen and a small notification reports the outcome. Falls back to
/// the full sync page when no saved login exists or the background sync
/// needs user attention.
Future<void> openPortalRefresh(
  BuildContext context, {
  bool allowInteractiveFallback = true,
}) async {
  if (_portalRefreshInFlight) return;
  _portalRefreshInFlight = true;
  try {
    final messenger = ScaffoldMessenger.of(context);
    if (!FirebaseFeatureFlags.portalSyncEnabled) {
      if (allowInteractiveFallback) {
        messenger.showSnackBar(
          const SnackBar(
            behavior: SnackBarBehavior.floating,
            content: Text(
              'Updates are temporarily unavailable. Your saved information is still here.',
            ),
          ),
        );
      }
      return;
    }
    final sisData = Provider.of<SisData>(context, listen: false);
    final prefs = await SharedPreferences.getInstance();
    final usn = prefs.getString('portal_usn') ?? '';
    final dob = prefs.getString('portal_dob') ?? '';
    final verificationType =
        prefs.getString('portal_verification_type') ?? "Father's mobile number";
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
      if (allowInteractiveFallback) await openFullSyncPage();
      return;
    }
    setBackgroundSyncState(BackgroundSyncState.updating);
    if (usn.trim().toUpperCase() == 'DUMMY') {
      await sisData.loadDummyData();
      setBackgroundSyncState(BackgroundSyncState.success);
      return;
    }

    // A transparent Navigator route still installs a modal barrier and blocks
    // the page underneath. Mount the hidden WebView in an IgnorePointer
    // overlay instead, so cached data and bottom navigation remain usable.
    final completion = Completer<bool>();
    late final OverlayEntry entry;
    entry = OverlayEntry(
      builder: (_) => IgnorePointer(
        child: PortalLoginScreen(
          silent: true,
          initialUsn: usn.trim().toUpperCase(),
          initialDob: dob,
          initialVerificationType: verificationType,
          initialVerificationValue: verificationValue,
          reuseSession:
              sisData.hasData &&
              sisData.usn.trim().toUpperCase() == usn.trim().toUpperCase(),
          onFinished: (result) {
            entry.remove();
            if (!completion.isCompleted) completion.complete(result);
          },
        ),
      ),
    );
    Overlay.of(context, rootOverlay: true).insert(entry);
    final synced = await completion.future;
    if (!context.mounted) return;

    if (synced == true) {
      setBackgroundSyncState(
        sisData.hasSyncIssues
            ? BackgroundSyncState.partial
            : BackgroundSyncState.success,
      );
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
      setBackgroundSyncState(BackgroundSyncState.error);
      if (!allowInteractiveFallback) return;
      messenger
        ..hideCurrentSnackBar()
        ..showSnackBar(
          SnackBar(
            behavior: SnackBarBehavior.floating,
            duration: const Duration(seconds: 5),
            content: const Text('Could not refresh in the background.'),
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
    if (backgroundSyncState.value == BackgroundSyncState.updating) {
      setBackgroundSyncState(BackgroundSyncState.error);
    }
  }
}
