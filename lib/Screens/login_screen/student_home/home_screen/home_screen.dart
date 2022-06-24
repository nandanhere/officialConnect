import 'package:auto_size_text/auto_size_text.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Providers/dummy_data.dart';
import 'package:official_connect/Screens/login_screen/student_home/home_screen/widgets/Proctor_messages_card.dart';
import 'package:official_connect/Screens/login_screen/student_home/home_screen/widgets/fees_card.dart';
import 'package:official_connect/Screens/login_screen/student_home/home_screen/widgets/new_proctor_messages_card%20copy.dart';
import 'package:official_connect/Screens/login_screen/student_home/home_screen/widgets/request_proctor_dialog.dart';
import 'package:provider/provider.dart';
import 'package:official_connect/Providers/sisdata.dart';
import "dart:math";
import 'package:official_connect/Providers/themes.dart';
import 'package:flutter/foundation.dart';
import 'package:fluttertoast/fluttertoast.dart';

extension StringCasingExtension on String {
  String toCapitalized() =>
      length > 0 ? '${this[0].toUpperCase()}${substring(1).toLowerCase()}' : '';
  String toTitleCase() => replaceAll(RegExp(' +'), ' ')
      .split(' ')
      .map((str) => str.toCapitalized())
      .join('\n');
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  bool isLoadingMessages = false;
  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final buttonTitle = CustomTheme.buttonTitle(context);
    final buttonTrailing = CustomTheme.buttonTrailing(context);
    final title = CustomTheme.textStyle(context);
    final neumorphicStyle = CustomTheme.neumorphicStyle(context);
    final linearGradient = CustomTheme.linearGradient(context);
    final linearGradientBG = CustomTheme.linearGradientBG(context);
    final subtitle = CustomTheme.buttonSubtitle(context);
    final emoji = DummyData.emojis[Random().nextInt(DummyData.emojis.length)];
    final sisData = Provider.of<SisData>(context);
    return Container(
      decoration: BoxDecoration(gradient: linearGradientBG),
      child: RefreshIndicator(
        displacement: height * 0.1,
        backgroundColor: sisData.darkMode ? Colors.black : Colors.white,
        color: sisData.darkMode
            ? const Color(0xffba3237)
            : const Color(0xffba3227),
        onRefresh: () async {
          SisData.showToast("Updating data ");
          await sisData.getData("", "", true);
          SisData.showToast("Updated data 🎉 ");
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
                                        "Hi, ${sisData.studentName.toTitleCase()} $emoji",
                                        style: buttonTrailing.copyWith(
                                            // fontFamily: "Lobster",
                                            fontSize: width * 0.08,
                                            fontWeight: FontWeight.normal),
                                      ),
                                    ),
                                    Neumorphic(
                                      style: neumorphicStyle.copyWith(
                                          boxShape: const NeumorphicBoxShape
                                              .circle()),
                                      // TODO : show circular progress indicator while loading image
                                      child: CircleAvatar(
                                        child: (sisData.studentImage ==
                                                "http://parents.msrit.edu/images/defaultimages.png")
                                            ? const Icon(Icons.person)
                                            : null,
                                        backgroundImage: (sisData
                                                    .studentImage !=
                                                "http://parents.msrit.edu/images/defaultimages.png")
                                            ? CachedNetworkImageProvider(
                                                kIsWeb
                                                    ? "https://sis-scraper-rit.herokuapp.com/getimage/" +
                                                        sisData.studentImage
                                                            .split('/')
                                                            .last
                                                            .split('.')
                                                            .first
                                                    : sisData.studentImage,
                                                headers: {
                                                    "Origin":
                                                        "http://localhost:8080",
                                                  })
                                            : null,
                                        backgroundColor: Colors.grey,
                                        radius: width * 0.1,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                              Row(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
                                children: [
                                  Text(
                                    "Class ",
                                    style: buttonTitle.copyWith(
                                        fontSize: width * 0.045),
                                  ),
                                  Container(
                                    padding: EdgeInsets.symmetric(
                                        vertical: height * 0.01,
                                        horizontal: width * 0.02),
                                    child: Text(
                                      "${sisData.semester}-${sisData.section[4]}",
                                      style: subtitle,
                                    ),
                                    // decoration: BoxDecoration(
                                    // border: Border.all(width: 1.3),
                                    // borderRadius: BorderRadius.circular(width)),
                                  ),
                                ],
                              ),
                              Row(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
                                children: [
                                  Text(
                                    "Course ",
                                    style: buttonTitle.copyWith(
                                        fontSize: width * 0.045),
                                  ),
                                  Container(
                                    padding: EdgeInsets.symmetric(
                                        vertical: height * 0.01,
                                        horizontal: width * 0.02),
                                    child:
                                        Text(sisData.course, style: subtitle),
                                    // decoration: BoxDecoration(
                                    // border: Border.all(width: 1.3),
                                    // borderRadius: BorderRadius.circular(width)),
                                  ),
                                ],
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                    Container(
                      //line between student card and fees card
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
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Padding(
                            padding:
                                EdgeInsets.symmetric(vertical: height * 0.02),
                            child: Center(
                              child: ListTile(
                                trailing: isLoadingMessages
                                    ? const CircularProgressIndicator()
                                    : IconButton(
                                        icon: Icon(sisData.proctorEmail == ""
                                            ? Icons.app_registration
                                            : Icons.refresh),
                                        onPressed: () async {
                                          if (sisData.proctorEmail == "") {
                                            showDialog(
                                                context: context,
                                                builder: (ctx) {
                                                  return RequestProctorDialog(
                                                    height: height,
                                                    width: width,
                                                  );
                                                });
                                          } else {
                                            setState(() {
                                              isLoadingMessages = true;
                                            });
                                            await sisData.getProctorMessages();
                                            setState(() {
                                              isLoadingMessages = false;
                                            });
                                            SisData.showToast(
                                                "Proctor messages recieved!");
                                          }
                                        },
                                      ),
                                title: AutoSizeText(
                                  "Proctor Announcements",
                                  maxLines: 1,
                                  style: buttonTrailing,
                                ),
                              ),
                            ),
                          ),
                          if (sisData.proctorEmail != "")
                            ...sisData.proctorMessages
                                .map((e) => NewProctorMessagesCard(
                                      height: height,
                                      width: width,
                                      title: title,
                                      subtitle: subtitle,
                                      neumorphicStyle: neumorphicStyle,
                                      buttonTrailing: buttonTrailing,
                                      isDark: sisData.darkMode,
                                      messageData: e,
                                    )),
                          ...sisData.proctordata.messages
                              .map(
                                (e) => ProctorMessagesCard(
                                  height: height,
                                  width: width,
                                  title: title,
                                  subtitle: subtitle,
                                  neumorphicStyle: neumorphicStyle,
                                  buttonTrailing: buttonTrailing,
                                  isDark: sisData.darkMode,
                                  messageData: e,
                                ),
                              )
                              .toList()
                              .reversed,
                          sisData.proctordata.messages.isEmpty
                              ? Text(
                                  "No messages from proctor",
                                  style:
                                      subtitle.copyWith(fontSize: width * 0.04),
                                )
                              : Container()
                        ]),
                    Container(
                      //line between ProctorMessages card and fees card
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
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Padding(
                          padding: EdgeInsets.symmetric(
                              horizontal: width * 0.2, vertical: height * 0.02),
                          child: Text(
                            "Your Fees Paid",
                            style: buttonTrailing,
                          ),
                        ),
                        ...sisData.fees.map((e) => FeesCard(
                              height: height,
                              width: width,
                              neumorphicStyle: neumorphicStyle,
                              feeData: e,
                              buttonTrailing: buttonTrailing,
                              subtitle: subtitle,
                              title: title,
                              isDark: sisData.darkMode,
                            ))
                      ],
                    ),
                    SizedBox(
                      height: height * 0.13,
                    )
                  ]),
            ),
          ),
        ),
      ),
    );
  }
}
