import 'package:flutter/material.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';

class LoginScreen extends StatefulWidget {
  static const String id = "login";

  LoginScreen({Key? key}) : super(key: key);

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  @override
  double depthVal = 5;

  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const Text(
              "Connect",
              style: TextStyle(
                  color: Colors.black, fontSize: 40, fontFamily: 'Comfortaa'),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 40.0),
              child: Image.asset('images/logo.png'),
            ),
            const Text(
              "By students of",
              style: TextStyle(
                  color: Colors.black, fontSize: 20, fontFamily: 'Comfortaa'),
            ),
            SizedBox(
              height: 10,
            ),
            const Text(
              "MSRIT",
              style: TextStyle(
                  color: Colors.red, fontSize: 20, fontFamily: 'Comfortaa'),
            ),
            SizedBox(
              height: 10,
            ),
            GestureDetector(
              onTap: () {
                setState(() {
                  depthVal = -1 * depthVal;
                  //Navigator.pushNamed(context, )
                });
              },
              child: Neumorphic(
                padding: EdgeInsets.symmetric(horizontal: 15, vertical: 10),
                style: NeumorphicStyle(
                    depth: depthVal,
                    intensity: 0.7,
                    color: Colors.white,
                    boxShape: NeumorphicBoxShape.roundRect(
                        BorderRadius.circular(30))),
                child: const Text(
                  "Login",
                  style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: Colors.black,
                      fontSize: 20,
                      fontFamily: 'Comfortaa'),
                ),
              ),
            )
          ],
        ),
      ),
    );
  }
}
