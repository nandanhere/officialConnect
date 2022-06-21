import 'package:flutter_neumorphic/flutter_neumorphic.dart';

import '../../../../../Classes/sis_proctor_data.dart';

class ProctorMessagesCard extends StatelessWidget {
  final height,
      width,
      neumorphicStyle,
      buttonTrailing,
      body,
      title,
      subtitle,
      isDark;
  final ProctorMessage messageData;
  const ProctorMessagesCard({
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
                messageData.from,
                style: buttonTrailing.copyWith(fontSize: width * 0.06),
              ),
              subtitle: Text(
                messageData.date,
                style: subtitle,
              ),
              children: [
                Padding(
                  padding: EdgeInsets.symmetric(
                      horizontal: width * 0.04, vertical: height * 0.02),
                  child: Text(
                    messageData.desc,
                    style: subtitle,
                  ),
                )
              ],
            )),
      ),
    );
  }
}
