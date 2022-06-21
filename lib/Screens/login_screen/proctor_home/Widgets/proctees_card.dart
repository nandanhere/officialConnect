// ignore_for_file: prefer_typing_uninitialized_variables

import 'package:flutter_neumorphic/flutter_neumorphic.dart';

class ProcteesCard extends StatelessWidget {
  final height, width, neumorphicStyle, buttonTrailing, subtitle, title, isDark;
  final String name;
  final String usn;
  const ProcteesCard(
      {Key? key,
      this.height,
      this.width,
      this.neumorphicStyle,
      this.buttonTrailing,
      this.subtitle,
      this.title,
      this.isDark,
      required this.name,
      required this.usn})
      : super(key: key);

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
        onPressed: () {}, //TODO receipt download maybe?
        style: neumorphicStyle,
        child: Theme(
          data: Theme.of(context).copyWith(
            dividerColor: Colors.transparent,
          ),
          child: ExpansionTile(
            iconColor: const Color(0xffba3237),
            collapsedIconColor: isDark ? Colors.white : Colors.black,
            title: Text(
              name,
              style: buttonTrailing.copyWith(fontSize: width * 0.06),
            ),
            subtitle: Padding(
              padding: EdgeInsets.symmetric(
                  horizontal: width * 0.02, vertical: height * 0.01),
              child: Text(
                "Usn : " + usn.toUpperCase(),
                style: subtitle,
              ),
            ),
            children: [
              IconButton(
                onPressed: () {},
                icon: Icon(Icons.send),
              )
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
