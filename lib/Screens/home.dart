import 'dart:ffi';

import 'package:cached_network_image/cached_network_image.dart';
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
      .join('\n');
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
    print(sisData.studentImage);
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
                  Padding(
                    padding: EdgeInsets.symmetric(
                        horizontal: width * 0.02, vertical: height * 0.02),
                    child: Neumorphic(
                      style: NeumorphicStyle(
                          depth: 3,
                          intensity: 1,
                          boxShape: NeumorphicBoxShape.roundRect(
                              BorderRadius.circular(20))),
                      child: Padding(
                        padding: EdgeInsets.symmetric(
                            horizontal: width * 0.05, vertical: height * 0.025),
                        child: Column(
                          children: [
                            Padding(
                              padding: EdgeInsets.only(bottom: height * 0.02),
                              child: Row(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
                                mainAxisSize: MainAxisSize.max,
                                children: [
                                  Expanded(
                                    child: Text(
                                      "Hi, ${sisData.studentName.toTitleCase()} ",
                                      style: const TextStyle(
                                        color: Colors.black,
                                        fontSize: 30,
                                        fontFamily: 'Comfortaa',
                                      ),
                                    ),
                                  ),
                                  Neumorphic(
                                    style: const NeumorphicStyle(
                                        boxShape: NeumorphicBoxShape.circle(),
                                        depth: 2,
                                        intensity: 1),
                                    child: CircleAvatar(
                                      backgroundImage:
                                          CachedNetworkImageProvider(
                                              sisData.studentImage),
                                      backgroundColor: Colors.grey,
                                      radius: width * 0.1,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
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
                                        color: Colors.black54,
                                        fontSize: width * 0.04,
                                        fontFamily: 'Comfortaa'),
                                  ),
                                  // decoration: BoxDecoration(
                                  // border: Border.all(width: 1.3),
                                  // borderRadius: BorderRadius.circular(width)),
                                ),
                              ],
                            ),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
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
                                    sisData.course,
                                    style: TextStyle(
                                        fontWeight: FontWeight.bold,
                                        color: Colors.black54,
                                        fontSize: width * 0.04,
                                        fontFamily: 'Comfortaa'),
                                  ),
                                  // decoration: BoxDecoration(
                                  // border: Border.all(width: 1.3),
                                  // borderRadius: BorderRadius.circular(width)),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                  Container(
                    padding: EdgeInsets.only(
                        left: width * 0.1,
                        right: width * 0.1,
                        top: height * 0.03,
                        bottom: height * 0.015),
                    child: const Divider(
                      thickness: 1.6,
                    ),
                  ),
                  Column(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Padding(
                        padding: EdgeInsets.symmetric(
                            horizontal: width * 0.2, vertical: height * 0.02),
                        child: const Text(
                          "Your Fees Paid",
                          style: TextStyle(
                              color: Colors.black,
                              fontSize: 16,
                              fontFamily: 'Comfortaa',
                              fontWeight: FontWeight.bold),
                        ),
                      ),
                      ...sisData.fees.map((e) => Padding(
                            padding: const EdgeInsets.all(8.0),
                            child: NeumorphicButton(
                              padding: EdgeInsets.only(
                                  top: height * 0.015,
                                  bottom: height * 0.015,
                                  left: width * 0.025,
                                  right: width * 0.01),
                              onPressed: () {}, //TODO receipt download maybe?
                              style: NeumorphicStyle(
                                  depth: 2,
                                  boxShape: NeumorphicBoxShape.roundRect(
                                      BorderRadius.circular(20))),
                              child: ExpansionTile(
                                title: Text(
                                  e.amountPaid,
                                  style: TextStyle(
                                      fontWeight: FontWeight.bold,
                                      color: Colors.black,
                                      fontSize: width * 0.06,
                                      fontFamily: 'Comfortaa'),
                                ),
                                subtitle: Padding(
                                  padding: EdgeInsets.symmetric(
                                      horizontal: width * 0.02,
                                      vertical: height * 0.01),
                                  child: Text(
                                    "For Year ${e.yearNumber} on ${e.date}",
                                    style: TextStyle(
                                        color: Colors.black54,
                                        fontSize: width * 0.04,
                                        fontFamily: 'Comfortaa'),
                                  ),
                                ),
                                children: [
                                  Padding(
                                    padding: EdgeInsets.symmetric(
                                        horizontal: width * 0.04,
                                        vertical: height * 0.02),
                                    child: Row(
                                      mainAxisAlignment:
                                          MainAxisAlignment.spaceBetween,
                                      children: [
                                        Text(
                                          "Challan No:",
                                          style: TextStyle(
                                              color: Colors.black,
                                              fontSize: width * 0.04,
                                              fontFamily: 'Comfortaa'),
                                        ),
                                        Text(
                                          e.challanNumber,
                                          style: TextStyle(
                                              color: Colors.black54,
                                              fontSize: width * 0.04,
                                              fontFamily: 'Comfortaa'),
                                          textAlign: TextAlign.end,
                                        ),
                                      ],
                                    ), //ChallanNo
                                  ),
                                  (e.mode != "CASH")
                                      ? Padding(
                                          padding: EdgeInsets.symmetric(
                                              horizontal: width * 0.04,
                                              vertical: height * 0.02),
                                          child: Row(
                                            mainAxisAlignment:
                                                MainAxisAlignment.spaceBetween,
                                            crossAxisAlignment:
                                                CrossAxisAlignment.start,
                                            children: [
                                              Text(
                                                "Cheque No:",
                                                style: TextStyle(
                                                    color: Colors.black,
                                                    fontSize: width * 0.04,
                                                    fontFamily: 'Comfortaa'),
                                              ),
                                              Expanded(
                                                child: Text(
                                                  e.chequeNumber,
                                                  style: TextStyle(
                                                      color: Colors.black54,
                                                      fontSize: width * 0.04,
                                                      fontFamily: 'Comfortaa'),
                                                  textAlign: TextAlign.end,
                                                ),
                                              ),
                                            ],
                                          ),
                                        )
                                      : Container(),
                                ],
                              ),
                            ),
                          ))
                    ],
                  )
                ]),
          ),
        ));
  }
}
