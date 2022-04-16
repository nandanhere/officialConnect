import 'package:flutter/material.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/LoginScreen.dart';
import 'package:official_connect/Screens/home.dart';
import 'package:provider/provider.dart';

class AttendanceScreen extends StatelessWidget {
  static const String id = "attendance";

  const AttendanceScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final sisData = Provider.of<SisData>(context);

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.red,
        title: Text('Attendance Details'),
        // centerTitle: true,
      ),
      body: Center(
        child: SingleChildScrollView(
          child: Column(
            children: [
              ...sisData.attendances.map((e) => SizedBox(
                    width: size.width * .95,
                    height: size.height * .2,
                    child: Card(
                      child: ListTile(
                        onTap: () => print("attendance details"),
                        title: Text(e.subjectName),
                        subtitle: Text(
                          e.percentage,
                          style: const TextStyle(fontSize: 20),
                          textAlign: TextAlign.end,
                          ),
                      ),
                    ),
                  )).toList()
            ],
          ),
        ),
      ),
    );
  }
}
