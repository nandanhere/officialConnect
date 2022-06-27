import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Providers/Themes.dart';
import 'package:official_connect/Providers/proctor_data.dart';
import 'package:official_connect/Screens/login_screen/proctor_home/Widgets/message_card.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
// TODO
// To take care of :
// When you are already logged in , and log out , it should show login screen properly

class SentMessagesScreen extends StatelessWidget {
  const SentMessagesScreen({
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final buttonTitle = CustomTheme.buttonTitle(context);
    final titleStyle = CustomTheme.titleStyle(context);
    final neumorphicStyle = CustomTheme.neumorphicStyle(context);
    final linearGradient = CustomTheme.linearGradient(context);
    final linearGradientBG = CustomTheme.linearGradientBG(context);
    final sisData = Provider.of<SisData>(context);
    final proctorData = Provider.of<ProctorData>(context);
    void updateData() {
      print("Update Data");
    }
    return Container(
      height: height,
      decoration: BoxDecoration(gradient: linearGradient),
      child: RefreshIndicator(
        color: Colors.red,
        backgroundColor: sisData.darkMode ? Colors.black : Colors.white,
        onRefresh: () async {
          await Future.delayed(Duration(seconds: 2));
          updateData();
        },
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
                    // Row(
                    //   mainAxisAlignment: MainAxisAlignment.start,
                    //   children: [
                    //     NeumorphicButton(
                    //       child: Icon(
                    //         Icons.navigate_before,
                    //         color:
                    //             sisData.darkMode ? Colors.white : Colors.black,
                    //         size: width * 0.05,
                    //       ),
                    //       style: neumorphicStyle,
                    //       onPressed: () {
                    //         Navigator.pop(context);
                    //       },
                    //     ),
                    //   ],
                    // ),
                    // Container(
                    //   padding: EdgeInsets.only(
                    //       left: width * 0.1,
                    //       right: width * 0.1,
                    //       top: height * 0.03,
                    //       bottom: height * 0.015),
                    //   child: Divider(
                    //     color:
                    //         sisData.darkMode ? Colors.white38 : Colors.black26,
                    //     thickness: 1.6,
                    //   ),
                    // ),
                    Column(
                      children: [
                        Padding(
                          padding: EdgeInsets.symmetric(vertical: height * 0.02),
                          child: Center(
                              child: AutoSizeText(
                            "Sent Messages",
                            maxFontSize: 45,
                            style: titleStyle,
                          )),
                        ),
                        ...proctorData.messages.map((e) {
                          return MessageCard(
                            context: context,
                            messageData: e,
                            height: height,
                            width: width,
                            title: CustomTheme.textStyle(context),
                            subtitle: CustomTheme.buttonSubtitle(context),
                            neumorphicStyle: neumorphicStyle,
                            buttonTrailing: buttonTitle,
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
