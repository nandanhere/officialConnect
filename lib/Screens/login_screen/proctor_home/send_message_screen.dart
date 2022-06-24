import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Providers/Themes.dart';
import 'package:official_connect/Providers/proctor_data.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:provider/provider.dart';

class SendMessageScreen extends StatefulWidget {
  final List<String> usns;
  const SendMessageScreen({Key? key, required this.usns}) : super(key: key);

  @override
  State<SendMessageScreen> createState() => _SendMessageScreenState();
}

class _SendMessageScreenState extends State<SendMessageScreen> {
  final _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    final proctorData = Provider.of<ProctorData>(context);

    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;

    final neumorphicStyle = CustomTheme.neumorphicStyle(context);
    final linearGradient = CustomTheme.linearGradient(context);
    final sisData = Provider.of<SisData>(context);
    TextEditingController messageController = TextEditingController();
    TextEditingController titleController = TextEditingController();

    TextFormField titleForm = TextFormField(
      style: CustomTheme.textStyle(context).copyWith(fontSize: width * 0.05),
      key: const ValueKey('title'),
      controller: titleController,
      minLines: 5,
      maxLines: 10,
      decoration: InputDecoration(
        labelText: "Enter title",
        labelStyle: CustomTheme.textStyle(context).copyWith(),
      ),
      validator: (value) {
        if (value!.isEmpty) {
          return "title cannot be empty";
        }
        return null;
      },
    );
    TextFormField messageForm = TextFormField(
      style: CustomTheme.textStyle(context).copyWith(fontSize: width * 0.05),
      key: const ValueKey('message'),
      controller: messageController,
      minLines: 5,
      maxLines: 10,
      decoration: InputDecoration(
        labelText: "Enter message",
        labelStyle: CustomTheme.textStyle(context).copyWith(),
      ),
      validator: (value) {
        if (value!.isEmpty) {
          return "Message cannot be empty";
        }
        return null;
      },
    );
    return Scaffold(
      floatingActionButton: NeumorphicFloatingActionButton(
        child: Icon(Icons.send),
        onPressed: () {
          if (_formKey.currentState!.validate()) {
            proctorData.sendMessage(widget.usns, messageController.text,
                titleController.text, context);
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
                      color: sisData.darkMode ? Colors.white : Colors.black,
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
                      "Sending to:",
                      maxLines: 1,
                      style: CustomTheme.textStyle(context),
                    ),
                    ...(widget.usns)
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
