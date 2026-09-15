// ignore_for_file: prefer_typing_uninitialized_variables

import 'package:flutter_neumorphic_plus/flutter_neumorphic.dart';

import 'package:official_connect/Services/safe_external_link.dart';

class AboutClubDialog extends StatelessWidget {
  final Map<String, String> e;
  final height, width, sisData, title;
  const AboutClubDialog({
    Key? key,
    this.sisData,
    required this.e,
    this.height,
    this.width,
    this.title,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      insetPadding: const EdgeInsets.symmetric(horizontal: 24, vertical: 28),
      contentPadding: const EdgeInsets.fromLTRB(22, 8, 22, 8),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
      backgroundColor: sisData.darkMode ? Colors.black87 : Colors.white,
      title: SizedBox(
        height: height * 0.24,
        child: Image.asset(
          "images/club_images/" +
              (sisData.darkMode ? "dark_" : "light_") +
              e['image']!,
          fit: BoxFit.contain,
        ),
      ),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(
            e['name']!,
            style: title.copyWith(
              fontSize: width * 0.065,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 12),
          Text(
            e['desc']!,
            style: (title as TextStyle).copyWith(fontSize: 13, height: 1.4),
          ),
          const SizedBox(height: 20),
          FilledButton.icon(
            onPressed: () async {
              await openExternalLink(context, Uri.parse(e['linktree']!));
            },
            style: FilledButton.styleFrom(
              backgroundColor: const Color(0xffba3237),
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(vertical: 12),
            ),
            icon: const Icon(Icons.open_in_new, size: 18),
            label: const Text('Open club links'),
          ),
        ],
      ),
      actions: <Widget>[
        TextButton(
          onPressed: () {
            Navigator.pop(context);
          },
          child: const Text('Close'),
        ),
      ],
    );
  }
}
