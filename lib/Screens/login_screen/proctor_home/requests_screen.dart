import 'package:auto_size_text/auto_size_text.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Providers/Themes.dart';
import 'package:official_connect/Providers/proctor_data.dart';
import 'package:official_connect/Screens/login_screen/proctor_home/Widgets/proctees_card.dart';
import 'package:official_connect/Screens/login_screen/proctor_home/Widgets/request_card.dart';
import 'package:official_connect/Utils/authentication.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
// TODO
// To take care of :
// When you are already logged in , and log out , it should show login screen properly

class RequestsScreen extends StatelessWidget {
  const RequestsScreen({
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final buttonTrailing = CustomTheme.buttonTrailing(context);
    final neumorphicStyle = CustomTheme.neumorphicStyle(context);
    final linearGradient = CustomTheme.linearGradient(context);
    final linearGradientBG = CustomTheme.linearGradientBG(context);
    final sisData = Provider.of<SisData>(context);
    final proctorData = Provider.of<ProctorData>(context);

    return Scaffold(
      body: Container(
        height: height,
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
                    Row(
                      mainAxisAlignment: MainAxisAlignment.start,
                      children: [
                        NeumorphicButton(
                          child: Icon(
                            Icons.navigate_before,
                            color:
                                sisData.darkMode ? Colors.white : Colors.black,
                            size: width * 0.05,
                          ),
                          style: neumorphicStyle,
                          onPressed: () {
                            Navigator.pop(context);
                          },
                        ),
                      ],
                    ),
                    Container(
                      padding: EdgeInsets.only(
                          left: width * 0.1,
                          right: width * 0.1,
                          top: height * 0.03,
                          bottom: height * 0.015),
                      child: Divider(
                        color:
                            sisData.darkMode ? Colors.white38 : Colors.black26,
                        thickness: 1.6,
                      ),
                    ),
                    Column(
                      children: [
                        Padding(
                          padding:
                              EdgeInsets.symmetric(vertical: height * 0.02),
                          child: Center(
                            child: AutoSizeText(
                              "Requested Students",
                              maxLines: 1,
                              style: buttonTrailing,
                            ),
                          ),
                        ),
                        ...proctorData.requests.map((e) {
                          return RequestCard(
                            context: context,
                            studDetails: e,
                            height: height,
                            width: width,
                            title: CustomTheme.textStyle(context),
                            subtitle: CustomTheme.buttonSubtitle(context),
                            neumorphicStyle: neumorphicStyle,
                            buttonTrailing: buttonTrailing,
                            isDark: sisData.darkMode,
                          );
                        }).toList()
                      ],
                    ),
                  ]),
            ),
          ),
        ),
      ),
    );
  }
}
