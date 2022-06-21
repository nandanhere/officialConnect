import 'package:flutter/material.dart';
import 'package:official_connect/Providers/proctor_data.dart';
import 'package:official_connect/Screens/login_screen/proctor_home/proctor_home.dart';
import 'package:provider/provider.dart';

class ProctorUnified extends StatelessWidget {
  const ProctorUnified({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
        create: (ctx) => ProctorData(), child: const ProctorHome());
  }
}
