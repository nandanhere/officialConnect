// ignore_for_file: prefer_typing_uninitialized_variables

import 'package:flutter/material.dart';
import 'package:official_connect/Providers/sisdata.dart';

class AboutClubDialog extends StatelessWidget {
  final Map<String, String> e;
  final height, width, sisData, title;
  const AboutClubDialog(
      {Key? key,
      this.sisData,
      required this.e,
      this.height,
      this.width,
      this.title})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
      ),
      backgroundColor: sisData.darkMode ? Colors.black87 : Colors.white,
      title: FittedBox(
        child: Image.asset(
          "images/club_images/" + e['image']!,
        ),
      ),
      content: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(e['name']!, style: title.copyWith(fontSize: width * 0.075)),
          SizedBox(
            height: height * 0.02,
          ),
          SizedBox(
            height: height * 0.04,
          ),
          Text(
            e['desc']!,
            style: (title as TextStyle).copyWith(fontSize: 15),
          )
        ],
      ),
      actions: <Widget>[
        TextButton(
          onPressed: () => Navigator.pop(context, 'Cancel'),
          child: const Text('Ok'),
        ),
      ],
    );
  }
}
