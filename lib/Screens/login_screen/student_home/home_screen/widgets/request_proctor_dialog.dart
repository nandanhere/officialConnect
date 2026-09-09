// ignore_for_file: prefer_typing_uninitialized_variables

import 'package:flutter_neumorphic_plus/flutter_neumorphic.dart';
import 'package:official_connect/Providers/themes.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:provider/provider.dart';


class RequestProctorDialog extends StatefulWidget {
  final height, width;
  const RequestProctorDialog({
    Key? key,
    this.height,
    this.width,
  }) : super(key: key);

  @override
  State<RequestProctorDialog> createState() => _RequestProctorDialogState();
}

class _RequestProctorDialogState extends State<RequestProctorDialog> {
  final _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);

    TextEditingController messageController = TextEditingController();
    TextFormField messageForm = TextFormField(
      style: CustomTheme.textStyle(context)
          .copyWith(fontSize: widget.width * 0.05),
      key: const ValueKey('message'),
      controller: messageController,
      maxLines: null,
      decoration: InputDecoration(
          contentPadding: EdgeInsets.symmetric(horizontal: widget.width * 0.06),
          filled: true,
          fillColor: Colors.white10,
          labelText: "Enter Email here ",
          labelStyle: CustomTheme.textStyle(context).copyWith(),
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(30))),
      validator: (value) {
        if (value!.isEmpty) {
          return "Email cannot be empty";
        }
        return null;
      },
    );
    return AlertDialog(
      shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
          side: BorderSide(color: Colors.grey.shade900)),
      backgroundColor:
          sisData.darkMode ? Colors.black : NeumorphicColors.background,
      title: Text(
        'Enter email Address of your Proctor',
        style: CustomTheme.buttonTrailing(context),
      ),
      content: Form(key: _formKey, child: messageForm),
      actions: <Widget>[
        NeumorphicButton(
          style: CustomTheme.neumorphicStyle(context),
          onPressed: () {
            Navigator.of(context).pop(false);
          },
          child: Text(
            'Cancel',
            style: CustomTheme.buttonTitle(context),
          ),
        ),
        NeumorphicButton(
          style: CustomTheme.neumorphicStyle(context),
          onPressed: () {
            if (_formKey.currentState!.validate()) {
              // sisData.requestProctor(messageController.text);
              Navigator.of(context).pop(false);
            }
          },
          child: Text(
            'Send Request',
            style: CustomTheme.buttonTitle(context),
          ),
        ),
      ],
    );
  }
}
