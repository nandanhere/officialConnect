import 'package:flutter/material.dart';
import 'package:official_connect/Classes/proctor_data.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/login_screen/login_screen.dart';
import 'package:official_connect/Screens/login_screen/proctor_home/proctor_home.dart';
import 'package:official_connect/Screens/login_screen/student_home/unified_screen.dart';
import 'package:provider/provider.dart';
import 'Screens/loading_screen.dart';

// to build web app
// flutter build web --web-renderer canvaskit --no-sound-null-safety --release

// to build flutter apk:
// flutter build apk --split-per-abi
// 1ms21scn05-t 1996-07-14
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
        title: 'Connect',
        theme: ThemeData(
          primarySwatch: Colors.blue,
        ),
        // home: Unified(),
        home: const LoadingScreen(),
        routes: {
          LoginScreen.id: (context) => const LoginScreen(),
          Unified.id: (context) => Unified(),
        },
      ),
    );
  }
}
