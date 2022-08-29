import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Providers/Themes.dart';
import 'package:official_connect/Providers/proctor_data.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:provider/provider.dart';

class ViewSentMessageScreen extends StatefulWidget {
  final Map messageData;
  const ViewSentMessageScreen({
    Key? key,
    required this.messageData,
  }) : super(key: key);

  @override
  State<ViewSentMessageScreen> createState() => _ViewSentMessageScreenState();
}

class _ViewSentMessageScreenState extends State<ViewSentMessageScreen> {
  @override
  Widget build(BuildContext context) {
    final _formKey = GlobalKey<FormState>();
    final proctorData = Provider.of<ProctorData>(context);

    final linearGradient = CustomTheme.linearGradient(context);
    final neumorphicStyle = CustomTheme.neumorphicStyle(context);
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;

    TextEditingController messageController = TextEditingController();
    TextEditingController titleController = TextEditingController();

    TextFormField titleForm = TextFormField(
      style: CustomTheme.textStyle(context).copyWith(fontSize: width * 0.05),
      key: const ValueKey('title'),
      controller: titleController,
      enabled: false,
      minLines: 5,
      maxLines: 10,
    );
    titleController.text = widget.messageData['message_title'];
    messageController.text = widget.messageData['message_body'];
    TextFormField messageForm = TextFormField(
      style: CustomTheme.textStyle(context).copyWith(fontSize: width * 0.05),
      key: const ValueKey('message'),
      controller: messageController,
      enabled: false,
      minLines: 5,
      maxLines: 10,
    );
    return Scaffold(
      floatingActionButton: NeumorphicFloatingActionButton(
        child: const Icon(Icons.delete_forever),
        onPressed: () {
          if (_formKey.currentState!.validate()) {
            proctorData.deleteMessage(widget.messageData, context);
            print("deleting");
          }
        },
      ),
      body: Container(
        decoration: BoxDecoration(gradient: linearGradient),
        padding: EdgeInsets.only(
          left: width * 0.08,
          right: width * 0.08,
          top: height * 0.06,
        ),
        child:
            Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  NeumorphicButton(
                    child: Icon(
                      Icons.navigate_before,
                      size: width * 0.05,
                    ),
                    style: neumorphicStyle,
                    onPressed: () {
                      Navigator.pop(context);
                    },
                  ),
                ],
              ),
              Padding(
                padding: EdgeInsets.symmetric(vertical: height * 0.02),
                child: Center(
                  child: AutoSizeText(
                    "Send Message",
                    maxLines: 1,
                    style: CustomTheme.titleStyle(context),
                  ),
                ),
              ),
              SizedBox(
                height: height * 0.08,
                child: ListView(
                  scrollDirection: Axis.horizontal,
                  children: [
                    AutoSizeText(
                      "Sent:",
                      maxLines: 1,
                      style: CustomTheme.textStyle(context),
                    ),
                    ...(widget.messageData['usn_list'])
                        .map((e) => Padding(
                              padding: const EdgeInsets.all(8.0),
                              child: Neumorphic(
                                child: Padding(
                                  padding: const EdgeInsets.all(8.0),
                                  child: Text(e),
                                ),
                              ),
                            ))
                        .toList(),
                  ],
                ),
              ),
              Form(
                  key: _formKey,
                  child: Column(
                    children: [titleForm, messageForm],
                  )),
            ],
          ),
        ]),
      ),
    );
  }
}
