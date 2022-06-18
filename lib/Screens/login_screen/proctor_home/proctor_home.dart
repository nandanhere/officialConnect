import 'dart:convert';

import 'package:auto_size_text/auto_size_text.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Providers/Themes.dart';
import 'package:official_connect/Providers/dummy_data.dart';
import 'package:official_connect/Utils/authentication.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import "dart:math";
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

extension StringCasingExtension on String {
  String toCapitalized() =>
      length > 0 ? '${this[0].toUpperCase()}${substring(1).toLowerCase()}' : '';
  String toTitleCase() => replaceAll(RegExp(' +'), ' ')
      .split(' ')
      .map((str) => str.toCapitalized())
      .join('\n');
}

class ProctorHome extends StatelessWidget {
  const ProctorHome({Key? key}) : super(key: key);
  Future<Map<String, dynamic>> getData(String userEmail) async {
    final url = Uri.parse(
        "https://msrit-student-proctor-api.herokuapp.com/get_proctor_details");
    final bod = {"proctor_email": userEmail};
    final headers = {'Content-Type': 'application/json'};
    final encoding = Encoding.getByName("utf-8");
    http.Response resp = await http.post(
      url,
      headers: headers,
      encoding: encoding,
      body: jsonEncode(bod),
    );
    print(resp.body);
    if (resp.body.isNotEmpty) {
      return jsonDecode(resp.body);
    }
    return Future.error('error');
  }

  @override
  Widget build(BuildContext context) {
    final auth = FirebaseAuth.instance;
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final buttonTrailing = CustomTheme.buttonTrailing(context);
    final neumorphicStyle = CustomTheme.neumorphicStyle(context);
    final linearGradient = CustomTheme.linearGradient(context);
    final linearGradientBG = CustomTheme.linearGradientBG(context);
    final sisData = Provider.of<SisData>(context);

    return FutureBuilder(
        future: getData(auth.currentUser!.email ?? ""),
        builder: (context, snapshot) {
          if (!snapshot.hasData) {
            return const Padding(
              padding: EdgeInsets.all(8.0),
              child: Center(child: CircularProgressIndicator()),
            );
          }
          if (snapshot.hasData) print((snapshot.data! as Map)['_id']);
          return Container(
            decoration: BoxDecoration(gradient: linearGradientBG),
            child: SingleChildScrollView(
              physics: const BouncingScrollPhysics(),
              child: Container(
                decoration: BoxDecoration(gradient: linearGradient),
                padding: EdgeInsets.only(
                  left: width * 0.08,
                  right: width * 0.08,
                  top: height * 0.06,
                ),
                child: Center(
                  child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Image.asset(
                          'images/logo.png',
                          color: sisData.darkMode ? (Colors.white) : null,
                        ),
                        Padding(
                          padding: EdgeInsets.symmetric(
                              horizontal: width * 0.02,
                              vertical: height * 0.02),
                          child: Neumorphic(
                            style: neumorphicStyle,
                            child: Padding(
                              padding: EdgeInsets.symmetric(
                                  horizontal: width * 0.05,
                                  vertical: height * 0.025),
                              child: Column(
                                children: [
                                  Padding(
                                    padding:
                                        EdgeInsets.only(bottom: height * 0.02),
                                    child: Row(
                                      mainAxisAlignment:
                                          MainAxisAlignment.spaceBetween,
                                      mainAxisSize: MainAxisSize.max,
                                      children: [
                                        Expanded(
                                          child: AutoSizeText(
                                            "Hi, " +
                                                (auth.currentUser!
                                                        .displayName ??
                                                    "") +
                                                " " +
                                                (auth.currentUser!.email ?? ""),
                                            style: buttonTrailing.copyWith(
                                                // fontFamily: "Lobster",
                                                fontSize: width * 0.08,
                                                fontWeight: FontWeight.normal),
                                          ),
                                        ),
                                        Neumorphic(
                                          style: neumorphicStyle.copyWith(
                                              boxShape: const NeumorphicBoxShape
                                                  .circle()),
                                          // TODO : show teacher's photo here
                                          child: CircleAvatar(),
                                        ),
                                      ],
                                    ),
                                  ),
                                  Padding(
                                    padding:
                                        EdgeInsets.only(bottom: height * 0.02),
                                    child: Row(
                                      children: [
                                        AutoSizeText("Messages sent",
                                            style:
                                                CustomTheme.textStyle(context)),
                                      ],
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        ),
                        Container(
                          padding: EdgeInsets.only(
                              left: width * 0.1,
                              right: width * 0.1,
                              top: height * 0.03,
                              bottom: height * 0.015),
                          child: Divider(
                            color: sisData.darkMode
                                ? Colors.white38
                                : Colors.black26,
                            thickness: 1.6,
                          ),
                        ),
                        SizedBox(
                          height: height * 0.095,
                        ),
                        Column(
                          children: [
                            NeumorphicButton(
                              style: NeumorphicStyle(
                                  intensity: 0.5,
                                  color: const Color(0x00c00000),
                                  boxShape: NeumorphicBoxShape.roundRect(
                                      BorderRadius.circular(30))),
                              child: const Text(
                                "Sign Out",
                                textAlign: TextAlign.center,
                                style: TextStyle(
                                    fontWeight: FontWeight.bold,
                                    color: Colors.black,
                                    fontSize: 20,
                                    fontFamily: 'Comfortaa'),
                              ),
                              onPressed: () {
                                signOut();
                                sisData.cleanData();
                                Navigator.pop(context);
                              },
                            ),
                          ],
                        ),
                      ]),
                ),
              ),
            ),
          );
        });
  }
}
