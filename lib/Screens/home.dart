import 'dart:ffi';

import 'package:flutter/material.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';

extension StringCasingExtension on String {
  String toCapitalized() =>
      length > 0 ? '${this[0].toUpperCase()}${substring(1).toLowerCase()}' : '';
  String toTitleCase() => replaceAll(RegExp(' +'), ' ')
      .split(' ')
      .map((str) => str.toCapitalized())
      .join(' ');
}

extension WordSelection on String {
  String firstFew(int n) =>
      this.toTitleCase().split(" ").sublist(0, n).join(" ");
}

class Home extends StatelessWidget {
  const Home({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final sisData = Provider.of<SisData>(context);
    return Container(
        height: height,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(width * 0.08),
          color: NeumorphicColors.background,
        ),
        padding: EdgeInsets.only(
            left: width * 0.08,
            right: width * 0.08,
            top: height * 0.06,
            bottom: height * 0.13),
        child: SingleChildScrollView(
          child: Center(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  mainAxisSize: MainAxisSize.max,
                  children: [
                    Text(
                      "Hi, ${sisData.studentName.firstFew(2).split(" ")[0]} \n"
                      " ${sisData.studentName.firstFew(2).split(" ")[1]} ",
                      style: const TextStyle(
                        color: Colors.black,
                        fontSize: 30,
                        fontFamily: 'Comfortaa',
                      ),
                    ),
                    Neumorphic(
                      style: const NeumorphicStyle(
                          boxShape: NeumorphicBoxShape.circle(),
                          depth: 5,
                          intensity: 1),
                      child: CircleAvatar(
                        backgroundColor: Colors.grey,
                        radius: width * 0.1,
                      ),
                    ),
                  ],
                ),
                Row()
              ],
            ),
          ),
        ));
  }
}
