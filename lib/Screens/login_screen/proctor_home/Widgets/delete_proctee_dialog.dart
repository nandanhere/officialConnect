// ignore_for_file: prefer_typing_uninitialized_variables

import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Providers/Themes.dart';
import 'package:official_connect/Providers/proctor_data.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:provider/provider.dart';

import 'package:url_launcher/url_launcher.dart';

class DeleteProcteeDialog extends StatefulWidget {
  final height, width, studDetails;
  const DeleteProcteeDialog({
    Key? key,
    this.height,
    this.width,
    this.studDetails,
  }) : super(key: key);

  @override
  State<DeleteProcteeDialog> createState() => _DeleteProcteeDialogState();
}

class _DeleteProcteeDialogState extends State<DeleteProcteeDialog> {
  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);

    return AlertDialog(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
      ),
      backgroundColor:
          sisData.darkMode ? Colors.black : NeumorphicColors.background,
      title: Text(
        'Are you sure you want to delete this proctee?',
        style: CustomTheme.buttonTrailing(context),
      ),
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
          onPressed: () async {
            Provider.of<ProctorData>(context, listen: false)
                .removeProctee({"usn": widget.studDetails});
            Navigator.of(context).pop(false);
          },
          child: Text(
            'Confirm deletion',
            style: CustomTheme.buttonTitle(context),
          ),
        ),
      ],
    );
  }
}
