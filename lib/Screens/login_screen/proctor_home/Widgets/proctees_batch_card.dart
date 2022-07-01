import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Screens/login_screen/proctor_home/send_message_screen.dart';
class ProcteesBatchCard extends StatelessWidget {
    final height, width, neumorphicStyle, buttonTrailing, subtitle, title, isDark;
  final String batch;
  
  const ProcteesBatchCard({Key? key,
  this.height,
      this.width,
      this.neumorphicStyle,
      this.buttonTrailing,
      this.subtitle,
      this.title,
      this.isDark,
      required this.batch,
      
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
        onPressed: () {}, //TODO receipt download maybe?
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
              batch,
              style: buttonTrailing.copyWith(fontSize: width * 0.06),
            ),
            
            children: [
              Padding(
                padding:
                    EdgeInsets.only(left: width * 0.05, right: width * 0.05),
                child: TextButton(
                  onPressed: () {
                    // Navigator.of(context).push(MaterialPageRoute(
                    //     builder: (ctx) => SendMessageScreen(usns: [usn])));
                  },
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        "Send Message",
                        style: subtitle,
                      ),
                      Icon(
                        Icons.send,
                        color: isDark ? Colors.grey : Colors.black54,
                      ),
                    ],
                  ),
                ),
              )
            ],
          ),
        ),
      ),
    );
  }
}