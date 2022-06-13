import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Screens/login_screen/proctor_home/proctor_home.dart';
import 'package:official_connect/Providers/themes.dart';
import 'package:intl/intl.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Utils/authentication.dart';
import 'package:provider/provider.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'dart:math';

//e09zOTux2U@msrit.edu
//password123

//TODO add loading animation

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
  bool register = true;

  void _submit() {}

  void _submitEmail(value) {
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
      onFieldSubmitted: _submitEmail,
      decoration: InputDecoration(labelText: "Email", labelStyle: textStyle),
      validator: (value) {
        if (!RegExp(r"[a-zA-Z0-9]+@msrit\.edu").hasMatch(value!) &&
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
      key: const ValueKey('pwd'),
      controller: pwdController,
      focusNode: passwordFocus,
      obscureText: true,
      decoration: InputDecoration(
        labelText: "Password",
        labelStyle: textStyle,
      ),
      validator: (value) {
        if (value!.length < 8) {
          setState(() {
            isPressed = false;
          });
          return "Enter a password of length greater than 8";
        }
        return null;
      },
    );

    String generateRandomString(int len) {
      var r = Random();
      const _chars =
          'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890';
      return List.generate(len, (index) => _chars[r.nextInt(_chars.length)])
          .join();
    }

    //emailController.text = generateRandomString(10) + "@msrit.edu";
    pwdController.text = "password123";
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
              child: Stack(
                children: [
                  Positioned(
                    top: height * 0.07,
                    left: width * 0.04,
                    child: NeumorphicButton(
                      padding: EdgeInsets.all(width * 0.02),
                      style: NeumorphicStyle(
                          intensity: 0.5,
                          color: const Color(0x00c00000),
                          boxShape: NeumorphicBoxShape.roundRect(
                              BorderRadius.circular(30))),
                      child: const Icon(Icons.chevron_left),
                      onPressed: () {
                        if (!register) {
                          setState(() {
                            register = true;
                          });
                        } else {
                          Navigator.pop(context);
                        }
                      },
                    ),
                  ),
                  Positioned(
                    child: Padding(
                      padding: const EdgeInsets.only(top: 60.0),
                      child: SafeArea(
                        child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              Padding(
                                padding: const EdgeInsets.symmetric(
                                    horizontal: 40.0),
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
                              register
                                  ? Column(
                                      mainAxisAlignment:
                                          MainAxisAlignment.center,
                                      children: [
                                        NeumorphicButton(
                                          style: NeumorphicStyle(
                                              intensity: 0.5,
                                              color: const Color(0x00c00000),
                                              boxShape:
                                                  NeumorphicBoxShape.roundRect(
                                                      BorderRadius.circular(
                                                          30))),
                                          child: const Text(
                                            "Register",
                                            style: TextStyle(
                                                fontWeight: FontWeight.bold,
                                                color: Colors.black,
                                                fontSize: 15,
                                                fontFamily: 'Comfortaa'),
                                          ),
                                          onPressed: () async {
                                            setState(() {
                                              isPressed = true;
                                            });
                                            //_submit();
                                            if (_formKey.currentState!
                                                .validate()) {
                                              print(emailController.text +
                                                  " " +
                                                  pwdController.text);
                                              await registerWithEmailPassword(
                                                      emailController.text,
                                                      pwdController.text)
                                                  .then((result) {
                                                if (result != null) {
                                                  setState(() {
                                                    Navigator.push(
                                                      context,
                                                      MaterialPageRoute(
                                                        builder: (context) =>
                                                            ProctorHome(),
                                                      ),
                                                    );
                                                  });
                                                  print(result);
                                                }
                                              }).catchError((error) {
                                                print(
                                                    'Registration Error: $error');
                                                setState(() {
                                                  // loginStatus =
                                                  //     'Error occured while registering';
                                                  // loginStringColor = Colors.red;
                                                });
                                              });
                                            }

                                            // Navigator.push(
                                            //   context,
                                            //   MaterialPageRoute(
                                            //     builder: (context) => ProctorHome(),
                                            //   ),
                                            // );
                                          },
                                        ), //Register
                                        const SizedBox(
                                          height: 10,
                                        ),
                                        Text(
                                          "Already a user ?",
                                          style: textStyle,
                                        ),
                                        const SizedBox(
                                          height: 10,
                                        ),
                                        NeumorphicButton(
                                          style: NeumorphicStyle(
                                              // depth: depthVal,
                                              intensity: 0.5,
                                              color: const Color(0x00c00000),
                                              boxShape:
                                                  NeumorphicBoxShape.roundRect(
                                                      BorderRadius.circular(
                                                          30))),
                                          child: const Text(
                                            "Sign-in",
                                            style: TextStyle(
                                                fontWeight: FontWeight.bold,
                                                color: Colors.black,
                                                fontSize: 15,
                                                fontFamily: 'Comfortaa'),
                                          ),
                                          onPressed: () async {
                                            setState(() {
                                              register = false;
                                            });
                                          },
                                        ) // Login
                                      ],
                                    )
                                  : NeumorphicButton(
                                      style: NeumorphicStyle(
                                          intensity: 0.5,
                                          color: const Color(0x00c00000),
                                          boxShape:
                                              NeumorphicBoxShape.roundRect(
                                                  BorderRadius.circular(30))),
                                      child: const Text(
                                        "Login",
                                        style: TextStyle(
                                            fontWeight: FontWeight.bold,
                                            color: Colors.black,
                                            fontSize: 15,
                                            fontFamily: 'Comfortaa'),
                                      ),
                                      onPressed: () async {
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
                                        if (_formKey.currentState!.validate()) {
                                          print(emailController.text +
                                              " " +
                                              pwdController.text);
                                          await signInWithEmailPassword(
                                                  emailController.text,
                                                  pwdController.text)
                                              .then((result) {
                                            if (result != null) {
                                              Navigator.push(
                                                context,
                                                MaterialPageRoute(
                                                  builder: (context) =>
                                                      ProctorHome(),
                                                ),
                                              );
                                              print(result);
                                            }
                                          }).catchError((error) {
                                            print('Login Error: $error');
                                            setState(() {
                                              // loginStatus =
                                              //     'Error occured while registering';
                                              // loginStringColor = Colors.red;
                                            });
                                          });
                                        }
                                      },
                                    ),

                              // if (!sisData.isValidData)
                              //   Text(
                              //     sisData.errorMessage,
                              //     textAlign: TextAlign.center,
                              //     style: const TextStyle(
                              //         color: Colors.red,
                              //         fontSize: 10,
                              //         fontFamily: 'Comfortaa'),
                              //   )
                            ]),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          );
  }
}
