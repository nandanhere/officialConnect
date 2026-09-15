import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

typedef ExternalLinkLauncher = Future<bool> Function(Uri uri);

Future<bool> openExternalLink(
  BuildContext context,
  Uri uri, {
  ExternalLinkLauncher? launcher,
}) async {
  var opened = false;
  try {
    opened = await (launcher?.call(uri) ?? launchUrl(uri));
  } catch (_) {
    opened = false;
  }
  if (!opened && context.mounted) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Could not open that link. Try again.')),
    );
  }
  return opened;
}
