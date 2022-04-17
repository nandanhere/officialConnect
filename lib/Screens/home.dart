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
                          depth: 2,
                          intensity: 1),
                      child: CircleAvatar(
                        backgroundImage: NetworkImage(
                          sisData.studentImage.toString(),
                        ),
                        backgroundColor: Colors.grey,
                        radius: width * 0.1,
                      ),
                    ),
                  ],
                ),
                Container(
                  padding: EdgeInsets.only(
                      left: width * 0.1,
                      right: width * 0.1,
                      top: height * 0.03,
                      bottom: height * 0.015),
                  child: Divider(
                    thickness: 1.6,
                  ),
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Neumorphic(
                      padding: EdgeInsets.only(left: width * 0.03),
                      style: NeumorphicStyle(
                          depth: 3,
                          boxShape: NeumorphicBoxShape.roundRect(
                              BorderRadius.circular(width))),
                      child: Row(
                        children: [
                          Text(
                            "Class ",
                            style: TextStyle(
                                color: Colors.black,
                                fontSize: width * 0.05,
                                fontFamily: 'Comfortaa'),
                          ),
                          Container(
                            padding: EdgeInsets.symmetric(
                                vertical: height * 0.01,
                                horizontal: width * 0.02),
                            child: Text(
                              "${sisData.semester}-${sisData.section[4]}",
                              style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: Colors.black,
                                  fontSize: width * 0.04,
                                  fontFamily: 'Comfortaa'),
                            ),
                            decoration: BoxDecoration(
                                border: Border.all(width: 1.3),
                                borderRadius: BorderRadius.circular(width)),
                          ),
                        ],
                      ),
                    ),
                    Neumorphic(
                      padding: EdgeInsets.only(left: width * 0.03),
                      style: NeumorphicStyle(
                          depth: 3,
                          boxShape: NeumorphicBoxShape.roundRect(
                              BorderRadius.circular(width))),
                      child: Row(
                        children: [
                          Text(
                            "Course ",
                            style: TextStyle(
                                color: Colors.black,
                                fontSize: width * 0.05,
                                fontFamily: 'Comfortaa'),
                          ),
                          Container(
                            padding: EdgeInsets.symmetric(
                                vertical: height * 0.01,
                                horizontal: width * 0.02),
                            child: Text(
                              "${sisData.course}adf",
                              style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: Colors.black,
                                  fontSize: width * 0.04,
                                  fontFamily: 'Comfortaa'),
                            ),
                            decoration: BoxDecoration(
                                border: Border.all(width: 1.3),
                                borderRadius: BorderRadius.circular(width)),
                          ),
                        ],
                      ),
                    )
                  ],
                ),
                //             ...sisData.fees.map((e) => Padding(
                //     padding: const EdgeInsets.all(8.0),
                //   child: NeumorphicButton(
                //     padding: EdgeInsets.only(
                //         top: height * 0.015,
                //         bottom: height * 0.015,
                //         left: width * 0.025,
                //         right: width * 0.01),
                //     onPressed: () {},//TODO receipt download maybe?
                //     style: NeumorphicStyle(
                //         depth: 3,
                //         boxShape: NeumorphicBoxShape.roundRect(
                //             BorderRadius.circular(20))),
                //     child: ListTile(
                //       title: Text(
                //         e.subjectName,
                //         style: const TextStyle(
                //             color: Colors.black,
                //             fontSize: 16,
                //             fontFamily: 'Comfortaa'),
                //       ),
                //       trailing: Text(
                //         e.percentage,
                //         style: const TextStyle(
                //             fontWeight: FontWeight.bold,
                //             color: Colors.black,
                //             fontSize: 20,
                //             fontFamily: 'Comfortaa'),
                //         textAlign: TextAlign.end,
                //       ),
                //     ),
                //   ),
                // ))
              ],
            ),
          ),
        ));
  }
}
