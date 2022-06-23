import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Providers/Themes.dart';
import 'package:official_connect/Providers/proctor_data.dart';
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
    final sisData = Provider.of<SisData>(context);
    final proctorData = Provider.of<ProctorData>(context);

    if (!proctorData.dataPresent) {
      proctorData.getData();
      return const LoadingIndicator();
    }
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
                      mainAxisAlignment: MainAxisAlignment.end,
                      children: [
                        NeumorphicButton(
                          child: Icon(
                            Icons.logout,
                            color:
                                sisData.darkMode ? Colors.white : Colors.black,
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
                    Image.asset(
                      'images/logo.png',
                      color: sisData.darkMode ? (Colors.white) : null,
                    ),
                    Padding(
                      padding: EdgeInsets.symmetric(
                          horizontal: width * 0.02, vertical: height * 0.02),
                      child: Neumorphic(
                        style: neumorphicStyle,
                        child: Padding(
                          padding: EdgeInsets.symmetric(
                              horizontal: width * 0.05,
                              vertical: height * 0.025),
                          child: Column(
                            children: [
                              Padding(
                                padding: EdgeInsets.only(bottom: height * 0.02),
                                child: Row(
                                  mainAxisAlignment:
                                      MainAxisAlignment.spaceBetween,
                                  mainAxisSize: MainAxisSize.max,
                                  children: [
                                    Expanded(
                                      child: AutoSizeText(
                                        "Hi, " +
                                            (proctorData.name) +
                                            " " +
                                            (proctorData.email),
                                        style: buttonTrailing.copyWith(
                                            // fontFamily: "Lobster",
                                            fontSize: width * 0.08,
                                            fontWeight: FontWeight.normal),
                                      ),
                                    ),
                                    // Neumorphic(
                                    //   style: neumorphicStyle.copyWith(
                                    //       boxShape: const NeumorphicBoxShape
                                    //           .circle()),
                                    // TODO : show teacher's photo here
                                    //   child: CircleAvatar(),
                                    // ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                    if (proctorData.requests.isNotEmpty)
                      NeumorphicButton(
                        onPressed: () {
                          Navigator.of(context).push(
                            MaterialPageRoute(
                                builder: (BuildContext context) =>
                                    RequestsScreen()),
                          );
                          // Navigator.of(context).push(MaterialPageRoute(
                          //     builder: (context) => RequestsScreen()));
                        },
                        child: Text(
                          "Tap here to see requests",
                          style: CustomTheme.textStyle(context),
                        ),
                      ),
                    SizedBox(
                      height: 30,
                    ),
                    if (proctorData.messages.isNotEmpty)
                      NeumorphicButton(
                        onPressed: () {
                          Navigator.of(context).push(
                            MaterialPageRoute(
                                builder: (BuildContext context) =>
                                    SentMessagesScreen()),
                          );
                          // Navigator.of(context).push(MaterialPageRoute(
                          //     builder: (context) => RequestsScreen()));
                        },
                        child: Text(
                          "Tap here to see your sent messages",
                          style: CustomTheme.textStyle(context),
                        ),
                      ),
                    Container(
                      padding: EdgeInsets.only(
                        left: width * 0.1,
                        right: width * 0.1,
                        top: height * 0.03,
                        bottom: height * 0.015,
                      ),
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
                              "Your Proctees",
                              maxLines: 1,
                              style: buttonTrailing,
                            ),
                          ),
                        ),
                        ...proctorData.enrolled.map((e) {
                          return ProcteesCard(
                            name: e['name'],
                            usn: e['usn'],
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
