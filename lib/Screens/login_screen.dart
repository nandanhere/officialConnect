import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:syncfusion_flutter_core/theme.dart';

import 'package:intl/intl.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:provider/provider.dart';
import 'package:syncfusion_flutter_datepicker/datepicker.dart';

class LoginScreen extends StatefulWidget {
  static const String id = "login";

  const LoginScreen({Key? key}) : super(key: key);

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  double depthVal = 5;
  bool isPressed = false;
  bool fillForm = false;
  TextEditingController usnController = TextEditingController();
  TextEditingController dobController = TextEditingController();
  FocusNode passwordFocus = FocusNode();
  DateFormat formatter = DateFormat('yyyy-MM-dd');
  var selectedDate = DateTime.now();

  Widget getDateRangePicker() {
    return SfDateRangePickerTheme(
      data: SfDateRangePickerThemeData(
          // TODO : dark mode stuff
          // brightness: Brightness.dark,
          // backgroundColor: Colors.grey,

          ),
      child: SfDateRangePicker(
        view: DateRangePickerView.decade,
        selectionMode: DateRangePickerSelectionMode.single,
        minDate: DateTime(1990, 01, 01),
        maxDate: DateTime(2009, 01, 01),
        navigationDirection: DateRangePickerNavigationDirection.vertical,
        onSelectionChanged: (DateRangePickerSelectionChangedArgs args) {
          selectedDate = args.value;
          setState(() {
            dobController.text = formatter.format(selectedDate);
          });
        },
      ),
    );
  }

// TODO : Make this more organised.
  _selectDate(BuildContext context) async {
    showDialog(
        context: context,
        builder: (BuildContext context) {
          final size = MediaQuery.of(context).size;
          return Theme(
            data: ThemeData.dark(),
            child: AlertDialog(
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(20),
                ),
                title: const Text('Pick a date'),
                content: SizedBox(
                  height: size.height * 0.5,
                  width: size.width * 0.8,
                  child: Column(
                    children: <Widget>[
                      getDateRangePicker(),
                      MaterialButton(
                        child: const Text("OK"),
                        onPressed: () {
                          Navigator.pop(context);
                        },
                      )
                    ],
                  ),
                )),
          );
        });
  }

  void _submit() {
    final isValid = _formKey.currentState!.validate();
    if (isValid) {
      Provider.of<SisData>(context, listen: false)
          .getData(usnController.text, dobController.text, false);
      // print(usnController.text + " " + dobController.text);
    }
  }

  void _submitUSN(value) {
    usnController.text = value;
    passwordFocus.requestFocus();
    if (dobController.text == "") {
      _selectDate(context);
    }
  }

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    // some first year student's deets
    // usnController.text = "1MS21CS035-T";
    // dobController.text = "2003-06-11";
    // prateek
    // usnController.text = "1ms19cs030";
    // dobController.text = "2000-11-15";
    // nadnan
    // usnController.text = "1ms19is076";
    // dobController.text = "2000-12-08";

    // usnController.text = "dummy";
    TextFormField usnForm = TextFormField(
      // autofocus: true,
      controller: usnController,
      key: const ValueKey('usn'),
      onFieldSubmitted: _submitUSN,
      decoration: const InputDecoration(
        labelText: "USN",
      ),
      validator: (value) {
        if (!RegExp(r"1MS\d\d[A-Z]+\d+").hasMatch(value!.toUpperCase()) &&
            value != "dummy") {
          setState(() {
            isPressed = false;
          });
          return "Please Enter a valid USN like 1ms19is076";
        }
        return null;
      },
    );
    TextFormField dobForm = TextFormField(
      readOnly: true,
      key: const ValueKey('dob'),
      controller: dobController,
      focusNode: passwordFocus,
      decoration: InputDecoration(
          labelText: "Date of Birth",
          suffix: IconButton(
            icon: const Icon(Icons.calendar_month),
            onPressed: () {
              _selectDate(context);
              dobController.text = formatter.format(selectedDate);
            },
          )),
    );

    return Scaffold(
      backgroundColor: NeumorphicColors.background,
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.only(top: 60.0),
          child: SafeArea(
            child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 40.0),
                    child: Image.asset('images/logo.png'),
                  ),
                  const SizedBox(
                    height: 100,
                  ),
                  const Text(
                    "CONNECT",
                    style: TextStyle(
                        color: Colors.black,
                        fontSize: 40,
                        fontFamily: 'Comfortaa'),
                  ),
                  if (!fillForm)
                    const Text(
                      "By students of",
                      style: TextStyle(
                          color: Colors.black,
                          fontSize: 20,
                          fontFamily: 'Comfortaa'),
                    ),
                  const SizedBox(
                    height: 10,
                  ),
                  if (!fillForm)
                    const Text(
                      "MSRIT",
                      style: TextStyle(
                          color: Colors.red,
                          fontSize: 20,
                          fontFamily: 'Comfortaa'),
                    ),
                  if (fillForm)
                    Form(
                      key: _formKey,
                      child: Column(
                        children: [
                          Padding(
                            padding:
                                const EdgeInsets.only(left: 50.0, right: 50.0),
                            child: usnForm,
                          ),
                          Padding(
                            padding:
                                const EdgeInsets.only(left: 50.0, right: 50.0),
                            child: dobForm,
                          ),
                        ],
                      ),
                    ),
                  const SizedBox(
                    height: 10,
                  ),
                  (isPressed &&
                          !sisData.hasData &&
                          _formKey.currentState!.validate())
                      ? const CircularProgressIndicator()
                      : GestureDetector(
                          onTap: () {
                            if (!fillForm) {
                              setState(() {
                                fillForm = true;
                                depthVal = -1 * depthVal;
                              });
                            } else {
                              setState(() {
                                isPressed = true;
                              });
                              _submit();
                            }
                          },
                          child: Hero(
                            tag: "bar",
                            child: Neumorphic(
                                padding: const EdgeInsets.symmetric(
                                    horizontal: 15, vertical: 10),
                                style: NeumorphicStyle(
                                    depth: depthVal,
                                    intensity: 0.5,
                                    color: const Color(0x00c00000),
                                    boxShape: NeumorphicBoxShape.roundRect(
                                        BorderRadius.circular(30))),
                                child: fillForm
                                    ? const Text(
                                        "Login",
                                        style: TextStyle(
                                            fontWeight: FontWeight.bold,
                                            color: Colors.black,
                                            fontSize: 20,
                                            fontFamily: 'Comfortaa'),
                                      )
                                    : const Icon(Icons.chevron_right_rounded)),
                          ),
                        ),
                  if (!sisData.isValidData)
                    Text(
                      sisData.errorMessage,
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                          color: Colors.red,
                          fontSize: 10,
                          fontFamily: 'Comfortaa'),
                    )
                ]),
          ),
        ),
      ),
    );
  }
}
