import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Screens/login_screen/proctor_home/proctor_home.dart';
import 'package:official_connect/Providers/themes.dart';
import 'package:intl/intl.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:provider/provider.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class ProctorLogin extends StatefulWidget {
  static const String id = "login";

  const ProctorLogin({Key? key}) : super(key: key);

  @override
  State<ProctorLogin> createState() => _ProctorLoginState();
}

class _ProctorLoginState extends State<ProctorLogin> {
  final _formKey = GlobalKey<FormState>();
  double depthVal = 5;
  bool isPressed = false;
  bool fillForm = false;
  TextEditingController emailController = TextEditingController();
  TextEditingController pwdController = TextEditingController();
  FocusNode passwordFocus = FocusNode();
  DateFormat formatter = DateFormat('yyyy-MM-dd');
  var selectedDate = DateTime.now();

  void _submit() {}

  void _submitUSN(value) {
    emailController.text = value;
    passwordFocus.requestFocus();
    if (pwdController.text == "") {}
  }

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    final textStyle = CustomTheme.textStyle(context);
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;

    TextFormField emailForm = TextFormField(
      style: textStyle.copyWith(fontSize: width * 0.05),
      cursorHeight: 30, // autofocus: true,
      controller: emailController,
      key: const ValueKey('email'),
      onFieldSubmitted: _submitUSN,
      decoration: InputDecoration(labelText: "Email", labelStyle: textStyle),
      validator: (value) {
        if (!RegExp(r"[A-Z0-9_.]+[@](msrit.edu)")
                .hasMatch(value!.toUpperCase()) &&
            value != "dummy") {
          setState(() {
            isPressed = false;
          });
          return "Please Enter a valid Email like teacher@msrit.edu";
        }
        return null;
      },
    );
    TextFormField pwdForm = TextFormField(
      style: textStyle.copyWith(fontSize: width * 0.05),
      readOnly: true,
      key: const ValueKey('pwd'),
      controller: pwdController,
      focusNode: passwordFocus,
      decoration: InputDecoration(
        labelText: "Password",
        labelStyle: textStyle,
      ),
    );

    return sisData.updating
        ? Scaffold(
            backgroundColor: (sisData.darkMode) ? Colors.black : Colors.white,
            body: const Center(
              child: SpinKitSpinningLines(
                color: Colors.red,
                size: 100.0,
              ),
            ),
          )
        : Scaffold(
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
                          height: 20,
                        ),
                        const Text(
                          "CONNECT",
                          style: TextStyle(
                              color: Colors.black,
                              fontSize: 40,
                              fontFamily: 'Comfortaa'),
                        ),
                        Form(
                          key: _formKey,
                          child: Column(
                            children: [
                              Padding(
                                padding: const EdgeInsets.only(
                                    left: 50.0, right: 50.0),
                                child: emailForm,
                              ),
                              Padding(
                                padding: const EdgeInsets.only(
                                    left: 50.0, right: 50.0),
                                child: pwdForm,
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(
                          height: 10,
                        ),
                        // (isPressed &&
                        //         !sisData.hasData &&
                        //         _formKey.currentState!.validate())
                        //     ? const CircularProgressIndicator()
                        //     :
                        NeumorphicButton(
                          style: NeumorphicStyle(
                              depth: depthVal,
                              intensity: 0.5,
                              color: const Color(0x00c00000),
                              boxShape: NeumorphicBoxShape.roundRect(
                                  BorderRadius.circular(30))),
                          child: const Text(
                            "Proctor Login",
                            style: TextStyle(
                                fontWeight: FontWeight.bold,
                                color: Colors.black,
                                fontSize: 15,
                                fontFamily: 'Comfortaa'),
                          ),
                          onPressed: () {
                            if (!fillForm) {
                              setState(() {
                                fillForm = true;
                                depthVal = -1 * depthVal;
                              });
                            } else {
                              setState(() {
                                isPressed = true;
                              });
                              //_submit();
                            }
                            Navigator.push(
                                context,
                                MaterialPageRoute(
                                    builder: (context) => ProctorHome()));
                          },
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
