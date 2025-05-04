import 'package:flutter_neumorphic_plus/flutter_neumorphic.dart';


class NewProctorMessagesCard extends StatelessWidget {
  final height,
      width,
      neumorphicStyle,
      buttonTrailing,
      body,
      title,
      subtitle,
      isDark;
  final Map messageData;
  const NewProctorMessagesCard({
    Key? key,
    this.height,
    this.width,
    this.neumorphicStyle,
    this.buttonTrailing,
    this.body,
    this.title,
    this.subtitle,
    this.isDark,
    required this.messageData,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: NeumorphicButton(
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
              iconColor: const Color(0xffba3237),
              collapsedIconColor: isDark ? Colors.white : Colors.black,
              title: Text(
                messageData['message_title'],
                style: buttonTrailing.copyWith(fontSize: width * 0.06),
              ),
              subtitle: Text(
                DateTime.fromMillisecondsSinceEpoch(
                        (messageData['time'] as double).toInt() * 1000)
                    .toString(),
                style: subtitle,
              ),
              children: [
                Padding(
                  padding: EdgeInsets.symmetric(
                      horizontal: width * 0.04, vertical: height * 0.02),
                  child: Text(
                    messageData['message_body'],
                    style: subtitle,
                  ),
                )
              ],
            )),
      ),
    );
  }
}
