import 'package:flutter/material.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/LoginScreen.dart';
import 'package:official_connect/Screens/home.dart';
import 'package:provider/provider.dart';

class AttendanceScreen extends StatefulWidget {
  const AttendanceScreen({Key? key}) : super(key: key);

  @override
  State<AttendanceScreen> createState() => _AttendanceScreenState();
}

class _AttendanceScreenState extends State<AttendanceScreen> {
  Future goToHomeScreen() {
    return Navigator.push(
        context, MaterialPageRoute(builder: (context) => const Home()));
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(
          title: Text('Attendance Screen'),
          centerTitle: true,
        ),
        body: Center(
            child: IconButton(
          icon: Icon(Icons.home),
          onPressed: goToHomeScreen,
        )),
      );
}
