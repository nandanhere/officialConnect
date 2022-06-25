// ignore_for_file: prefer_typing_uninitialized_variables

import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Screens/login_screen/proctor_home/view_message_screen.dart';

class MessageCard extends StatelessWidget {
  final height, width, neumorphicStyle, buttonTrailing, subtitle, title, isDark;
  final Map messageData;
  final BuildContext context;
  const MessageCard(
      {Key? key,
      this.height,
      this.width,
      this.neumorphicStyle,
      this.buttonTrailing,
      this.subtitle,
      this.title,
      this.isDark,
      required this.context,
      required this.messageData})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: Neumorphic(
        padding: EdgeInsets.only(
            top: height * 0.015,
            bottom: height * 0.015,
            left: width * 0.025,
            right: width * 0.01),
        style: neumorphicStyle,
        child: Theme(
          data: Theme.of(context).copyWith(
            dividerColor: Colors.transparent,
          ),
          child: ExpansionTile(
            initiallyExpanded: true,
            iconColor: const Color(0xffba3237),
            collapsedIconColor: isDark ? Colors.white : Colors.black,
            title: Text(
              messageData["message_title"],
              style: buttonTrailing.copyWith(fontSize: width * 0.06),
            ),
            subtitle: Text(
              DateTime.fromMillisecondsSinceEpoch(
                      (messageData['time'] as double).toInt() * 1000)
                  .toString(),
              style: subtitle,
            ),
            children: [
              Center(
                child: Padding(
                  padding: EdgeInsets.all(height * 0.03),
                  child: NeumorphicButton(
                    style: neumorphicStyle,
                    child: Text(
                      "View message details",
                      style: title,
                    ),
                    onPressed: () {
                      Navigator.of(context).push(
                        MaterialPageRoute(
                            builder: (BuildContext context) =>
                                ViewSentMessageScreen(
                                  messageData: messageData,
                                )),
                      );
                    },
                  ),
                ),
              ),

              // Padding(
              //   padding: EdgeInsets.symmetric(
              //       horizontal: width * 0.04, vertical: height * 0.02),
              //   child: Row(
              //     mainAxisAlignment: MainAxisAlignment.spaceBetween,
              //     children: [],
              //   ), //ChallanNo
              // ),
            ],
          ),
        ),
      ),
    );
  }
}
