import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/unified_screen.dart';
import 'package:provider/provider.dart';

class LoadingScreen extends StatefulWidget {
  const LoadingScreen({Key? key}) : super(key: key);

  @override
  State<LoadingScreen> createState() => _LoadingScreenState();
}

class _LoadingScreenState extends State<LoadingScreen> {
  @override
  void initState() {
    super.initState();
    _navigateToUnifiedScreen();
  }

  _navigateToUnifiedScreen() async {
    await Future.delayed(const Duration(milliseconds: 1500), () {
      Navigator.pushReplacement(
          context, MaterialPageRoute(builder: (context) => Unified()));
    });
  }

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    return Scaffold(
      backgroundColor: (sisData.darkMode) ? Colors.black : Colors.white,
      body: const Center(
        child: SpinKitSpinningLines(
          itemCount: 4,
          color: Colors.red,
          size: 100.0,
        ),
      ),
    );
  }
}
