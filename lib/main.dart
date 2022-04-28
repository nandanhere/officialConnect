import 'package:flutter/material.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/login_screen.dart';
import 'package:official_connect/Screens/unified_screen.dart';
import 'package:provider/provider.dart';
import 'Screens/loading_screen.dart';

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
