// ignore_for_file: prefer_typing_uninitialized_variables

import 'package:flutter/material.dart';

class AboutConnectDialog extends StatelessWidget {
  final sisData, title, height, width;
  const AboutConnectDialog(
      {Key? key, this.sisData, this.title, this.height, this.width})
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
          "images/logo.png",
        ),
      ),
      content: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Text("RIT Connect", style: title.copyWith(fontSize: width * 0.075)),
          SizedBox(
            height: height * 0.02,
          ),
          Text(
            "by",
            style: title.copyWith(fontSize: width * 0.055),
          ),
          SizedBox(
            height: height * 0.04,
          ),
          Padding(
            padding: EdgeInsets.symmetric(horizontal: width * 0.22),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Row(
                  //mainAxisAlignment: MainAxisAlignment.center,
                  textBaseline: TextBaseline.alphabetic,
                  children: [
                    Text(
                      "N",
                      style: title.copyWith(
                        fontSize: width * 0.075,
                      ),
                    ),
                    Text(
                      "andan",
                      style: title.copyWith(fontSize: width * 0.035),
                    )
                  ],
                ),
                Row(
                  //mainAxisAlignment: MainAxisAlignment.center,
                  textBaseline: TextBaseline.alphabetic,
                  children: [
                    Text(
                      "A",
                      style: title.copyWith(
                        fontSize: width * 0.075,
                      ),
                    ),
                    Text(
                      "rnav",
                      style: title.copyWith(fontSize: width * 0.035),
                    )
                  ],
                ),
                Row(
                  //mainAxisAlignment: MainAxisAlignment.center,
                  textBaseline: TextBaseline.alphabetic,
                  children: [
                    Text(
                      "P",
                      style: title.copyWith(
                        fontSize: width * 0.075,
                      ),
                    ),
                    Text(
                      "rateek ",
                      style: title.copyWith(fontSize: width * 0.035),
                    )
                  ],
                ),
                Text(
                  "😴",
                  style: title.copyWith(fontSize: width * 0.055),
                )
              ],
            ),
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
