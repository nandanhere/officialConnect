import 'package:flutter/material.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:provider/provider.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';

class AttendanceInfo extends StatelessWidget {
  const AttendanceInfo({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final sisData = Provider.of<SisData>(context);

    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(30),
        color: NeumorphicColors.background,
      ),
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
      child: Center(
        child: SingleChildScrollView(
          padding: EdgeInsets.only(
              bottom: size.height * 0.1, top: size.height * 0.04),
          child: Column(
            children: [
              ...sisData.attendances
                  .map((e) => Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: NeumorphicButton(
                          padding: const EdgeInsets.only(
                              top: 10, bottom: 10, left: 10, right: 2),
                          onPressed: () => print("attendance details"),
                          style: NeumorphicStyle(
                              depth: 3,
                              boxShape: NeumorphicBoxShape.roundRect(
                                  BorderRadius.circular(20))),
                          child: ListTile(
                            title: Text(
                              e.subjectName,
                              style: const TextStyle(
                                  color: Colors.black,
                                  fontSize: 16,
                                  fontFamily: 'Comfortaa'),
                            ),
                            trailing: Text(
                              e.percentage,
                              style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: Colors.black,
                                  fontSize: 20,
                                  fontFamily: 'Comfortaa'),
                              textAlign: TextAlign.end,
                            ),
                          ),
                        ),
                      ))
                  .toList()
            ],
          ),
        ),
      ),
    );
  }
}
