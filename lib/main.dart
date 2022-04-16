import 'package:flutter/material.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/AttendanceScreen.dart';
import 'package:official_connect/Screens/LoginScreen.dart';
import 'package:official_connect/Screens/Settings.dart';
import 'package:official_connect/Screens/cieScreen.dart';
import 'package:official_connect/Screens/home.dart';
import 'package:provider/provider.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (ctx) => SisData(),
      child: MaterialApp(
        title: 'Flutter Demo',
        theme: ThemeData(
          primarySwatch: Colors.blue,
        ),
        home: const Home(),
        routes: {
          LoginScreen.id: (context) => LoginScreen(),
          Home.id: (context) => const Home(),
          Settings.id: (context) => Settings(),
          AttendanceScreen.id: (context) => const AttendanceScreen(),
          //CieScreen.id: (context) => const CieScreen(),
        },
      ),
    );
  }
}
