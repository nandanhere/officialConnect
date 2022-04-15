import 'package:flutter/material.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/AttendanceScreen.dart';
import 'package:official_connect/Screens/LoginScreen.dart';
import 'package:provider/provider.dart';

class Home extends StatelessWidget {
  const Home({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    if (sisData.usn == "")
      return LoginScreen();
    else {
      return Scaffold(
        appBar: AppBar(actions: [
          IconButton(
            icon: Icon(Icons.logout),
            onPressed: () => sisData.cleanData(),
          )
        ]),
        body: Column(
          children: [
            Center(
              child: (sisData.updating)
                  ?const  CircularProgressIndicator()
                  : Column(
                      children: sisData.previousResults.map((e) {
                      return Text(e.term + " " + e.cgpa + " " + e.sgpa);
                    }).toList()),
            ),
            IconButton(
              icon: const Icon(Icons.bar_chart),
              onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const AttendanceScreen())),
            )
          ],
        ),
      );
    }
  }
}
