import 'dart:ffi';

import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Classes/sis_proctor_data.dart';
import 'package:official_connect/Providers/Themes.dart';
import 'package:official_connect/Providers/proctor_data.dart';
import 'package:official_connect/Screens/login_screen/proctor_home/Widgets/proctees_batch_card.dart';
import 'package:official_connect/Screens/login_screen/proctor_home/Widgets/proctees_card.dart';
import 'package:official_connect/Screens/login_screen/proctor_home/requests_screen.dart';
import 'package:official_connect/Screens/login_screen/proctor_home/sent_messages_screen.dart';
import 'package:official_connect/Utils/authentication.dart';
import 'package:official_connect/Widgets/loading_indicator.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';

// To take care of :
// When you are already logged in , and log out , it should show login screen properly
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

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final buttonTrailing = CustomTheme.buttonTrailing(context);
    final neumorphicStyle = CustomTheme.neumorphicStyle(context);
    final linearGradient = CustomTheme.linearGradient(context);
    final linearGradientBG = CustomTheme.linearGradientBG(context);
    final buttonTitle = CustomTheme.buttonTitle(context);
    final sisData = Provider.of<SisData>(context);
    final proctorData = Provider.of<ProctorData>(context);
    var batchList = [];
    // Future<Void> refresh() async {

    //   setState(() {
    //     print("update dataaaaaaaa");
    //   });

    // }

    if (!proctorData.dataPresent) {
      proctorData.getData();
      return const LoadingIndicator();
    }
    void batchToList() {
      proctorData.enrolled.map((e) {
        batchList.add(e['batch']);
      }).toList();
      batchList = batchList.toSet().toList();
    }

    batchToList();
    void updateData() {
      print("Update Data");
    }

    return Container(
      height: height,
      decoration: BoxDecoration(gradient: linearGradientBG),
      child: RefreshIndicator(
        color: Colors.red,
        backgroundColor: sisData.darkMode ? Colors.black : Colors.white,
        onRefresh: () async {
          await Future.delayed(Duration(seconds: 2));
          updateData();
        },
        child: SingleChildScrollView(
          physics: const BouncingScrollPhysics(),
          child: Stack(
            children: [
              Positioned(
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
                                      padding: EdgeInsets.only(
                                          bottom: height * 0.02),
                                      child: Row(
                                        mainAxisAlignment:
                                            MainAxisAlignment.spaceBetween,
                                        mainAxisSize: MainAxisSize.max,
                                        children: [
                                          Expanded(
                                            child: AutoSizeText(
                                              "Hi, " + (proctorData.name),
                                              style: buttonTrailing.copyWith(
                                                  // fontFamily: "Lobster",
                                                  fontSize: width * 0.08,
                                                  fontWeight:
                                                      FontWeight.normal),
                                            ),
                                          ),
                                          // TODO : show teacher's photo here
                                          Neumorphic(
                                            style: neumorphicStyle.copyWith(
                                                boxShape:
                                                    const NeumorphicBoxShape
                                                        .circle()),
                                            child: CircleAvatar(
                                                backgroundColor: Colors.grey,
                                                radius: width * 0.1),
                                          ),
                                        ],
                                      ),
                                    ),
                                    Row(
                                      mainAxisAlignment:
                                          MainAxisAlignment.spaceBetween,
                                      children: [
                                        Text(
                                          "Email :",
                                          style: buttonTitle.copyWith(
                                              fontSize: width * 0.045),
                                        ),
                                        Text(
                                          proctorData.email,
                                          style: buttonTitle.copyWith(
                                              fontSize: width * 0.045),
                                        ),
                                      ],
                                    )
                                  ],
                                ),
                              ),
                            ),
                          ),
                          // if (proctorData.requests.isNotEmpty)
                          //   Padding(
                          //     padding: EdgeInsets.symmetric(
                          //         horizontal: width * 0.02, vertical: height * 0.02),
                          //     child: NeumorphicButton(
                          //       onPressed: () {
                          //         Navigator.of(context).push(
                          //           MaterialPageRoute(
                          //               builder: (BuildContext context) =>
                          //                   RequestsScreen()),
                          //         );
                          //         // Navigator.of(context).push(MaterialPageRoute(
                          //         //     builder: (context) => RequestsScreen()));
                          //       },
                          //       child: Text(
                          //         "Tap here to see requests",
                          //         style: CustomTheme.textStyle(context),
                          //       ),
                          //     ),
                          //   ),
                          // SizedBox(
                          //   height: 30,
                          // ),
                          // if (proctorData.messages.isNotEmpty)
                          //   Padding(
                          //     padding: EdgeInsets.symmetric(
                          //         horizontal: width * 0.02, vertical: height * 0.01),
                          //     child: NeumorphicButton(
                          //       onPressed: () {
                          //         Navigator.of(context).push(
                          //           MaterialPageRoute(
                          //               builder: (BuildContext context) =>
                          //                   SentMessagesScreen()),
                          //         );
                          //         // Navigator.of(context).push(MaterialPageRoute(
                          //         //     builder: (context) => RequestsScreen()));
                          //       },
                          //       child: Text(
                          //         "Tap here to see your sent messages",
                          //         style: CustomTheme.textStyle(context),
                          //       ),
                          //     ),
                          //   ),
                          Container(
                            padding: EdgeInsets.only(
                              left: width * 0.1,
                              right: width * 0.1,
                              top: height * 0.01,
                              bottom: height * 0.007,
                            ),
                            child: Divider(
                              color: sisData.darkMode
                                  ? Colors.white38
                                  : Colors.black26,
                              thickness: 1.6,
                            ),
                          ),
                          Column(
                            children: [
                              Padding(
                                padding: EdgeInsets.symmetric(
                                    vertical: height * 0.02),
                                child: Center(
                                  child: AutoSizeText(
                                    "Your Proctees",
                                    maxLines: 1,
                                    style: buttonTrailing,
                                  ),
                                ),
                              ),
                              // ...proctorData.enrolled.map((e) {
                              //   return ProcteesCard(
                              //     name: e['name'],
                              //     usn: e['usn'],
                              //     height: height,
                              //     width: width,
                              //     title: CustomTheme.buttonTitle(context),
                              //     subtitle: CustomTheme.buttonSubtitle(context),
                              //     neumorphicStyle: neumorphicStyle,
                              //     buttonTrailing: buttonTrailing,
                              //     isDark: sisData.darkMode,
                              //   );
                              // }).toList()
                              ...batchList
                                  .map((e) => ProcteesBatchCard(
                                        batch: e,
                                        height: height,
                                        width: width,
                                        title: CustomTheme.buttonTitle(context),
                                        subtitle:
                                            CustomTheme.buttonSubtitle(context),
                                        neumorphicStyle: neumorphicStyle,
                                        buttonTrailing: buttonTrailing,
                                        isDark: sisData.darkMode,
                                      ))
                                  .toList(),
                            ],
                          ),
                          SizedBox(
                            height: height * 0.13,
                          )
                        ]),
                  ),
                ),
              ),
              Positioned(
                left: 10,
                right: 10,
                top: height * 0.05,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    NeumorphicButton(
                      child: Icon(
                        sisData.darkMode ? Icons.light_mode : Icons.dark_mode,
                        color: sisData.darkMode ? Colors.white : Colors.black,
                        size: width * 0.05,
                      ),
                      style: neumorphicStyle,
                      onPressed: () {
                        sisData.darkMode = !sisData.darkMode;
                      },
                    ),
                    NeumorphicButton(
                      child: Icon(
                        Icons.logout,
                        color: sisData.darkMode ? Colors.white : Colors.black,
                        size: width * 0.05,
                      ),
                      style: neumorphicStyle,
                      onPressed: () async {
                        await signOut();
                        proctorData.toggleLogin();
                      },
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
