import 'package:flutter_neumorphic_plus/flutter_neumorphic.dart';

class NewProctorMessagesCard extends StatelessWidget {
  final double height;
  final double width;
  final NeumorphicStyle neumorphicStyle;
  final TextStyle buttonTrailing;
  final Object? body;
  final Object? title;
  final TextStyle subtitle;
  final bool isDark;
  final Map messageData;
  const NewProctorMessagesCard({
    Key? key,
    required this.height,
    required this.width,
    required this.neumorphicStyle,
    required this.buttonTrailing,
    this.body,
    this.title,
    required this.subtitle,
    required this.isDark,
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
          right: width * 0.01,
        ),
        style: neumorphicStyle,
        child: Theme(
          data: Theme.of(context).copyWith(dividerColor: Colors.transparent),
          child: ExpansionTile(
            iconColor: const Color(0xffba3237),
            collapsedIconColor: isDark ? Colors.white : Colors.black,
            title: Text(
              messageData['message_title'],
              style: buttonTrailing.copyWith(fontSize: width * 0.06),
            ),
            subtitle: Text(
              DateTime.fromMillisecondsSinceEpoch(
                (messageData['time'] as double).toInt() * 1000,
              ).toString(),
              style: subtitle,
            ),
            children: [
              Padding(
                padding: EdgeInsets.symmetric(
                  horizontal: width * 0.04,
                  vertical: height * 0.02,
                ),
                child: Text(messageData['message_body'], style: subtitle),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
