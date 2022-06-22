import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:official_connect/Providers/proctor_data.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/login_screen/login_screen.dart';
import 'package:official_connect/Screens/login_screen/student_home/unified_screen.dart';
import 'package:official_connect/Utils/authentication.dart';
import 'package:provider/provider.dart';
import 'Screens/loading_screen.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/services.dart';

// to build web app
// flutter build web --web-renderer canvaskit --no-sound-null-safety --release

// to build flutter apk:
// flutter build apk --split-per-abi
// 1ms21scn05-t 1996-07-14
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  if (!kIsWeb) {
    await Firebase.initializeApp();
  }
  SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp])
      .then((_) {
    runApp(new MyApp());
  });
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (ctx) => SisData()),
        ChangeNotifierProvider(create: (ctx) => ProctorData())
      ],
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
