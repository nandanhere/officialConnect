import 'package:flutter/material.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Screens/LoginScreen.dart';
import 'package:provider/provider.dart';

class Home extends StatelessWidget {
  const Home({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    print(sisData.data['attendance']);
    if (sisData.usn == "" || sisData.data.isEmpty)
      return LoginScreen();
    else {
      return Scaffold(
        body: Center(
          child: IconButton(
            icon: Icon(Icons.logout),
            onPressed: () => sisData.cleanData(),
          ),
        ),
      );
    }
  }
}
