import 'package:flutter_neumorphic_plus/flutter_neumorphic.dart';
import 'package:official_connect/Providers/themes.dart';
import 'package:intl/intl.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:provider/provider.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'package:date_picker_plus/date_picker_plus.dart';
import 'package:official_connect/Screens/login_screen/portal_login_screen.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LoginScreen extends StatefulWidget {
  static const String id = "login";

  const LoginScreen({Key? key, this.closeAfterSync = false}) : super(key: key);

  final bool closeAfterSync;

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
  TextEditingController verificationValueController = TextEditingController();
  String verificationType = "Father's mobile number";
  FocusNode passwordFocus = FocusNode();
  DateFormat formatter = DateFormat('yyyy-MM-dd');
  var selectedDate = DateTime.now();
  bool _loadedSavedLogin = false;
  bool _autoSyncStarted = false;

  @override
  void initState() {
    super.initState();
    usnController.addListener(_handleUsnChanged);
    _loadSavedLogin();
  }

  Future<void> _loadSavedLogin() async {
    final prefs = await SharedPreferences.getInstance();
    final usn = prefs.getString('portal_usn') ?? '';
    if (!mounted) return;
    usnController.text = usn;
    final savedDob = prefs.getString('portal_dob') ?? '';
    final parsedDob = DateTime.tryParse(savedDob);
    // Never reuse an impossible future DOB from stale local cache.
    dobController.text =
        parsedDob != null && !parsedDob.isAfter(DateTime.now()) ? savedDob : '';
    verificationType =
        prefs.getString('portal_verification_type') ?? verificationType;
    verificationValueController.text =
        prefs.getString('portal_verification_value') ?? '';
    setState(() {
      _loadedSavedLogin = true;
      if (widget.closeAfterSync) fillForm = true;
    });
    if (widget.closeAfterSync &&
        !_autoSyncStarted &&
        usnController.text.trim().isNotEmpty &&
        dobController.text.trim().isNotEmpty &&
        verificationValueController.text.trim().isNotEmpty) {
      _autoSyncStarted = true;
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted) _openPortalLogin();
      });
    }
  }

  void _handleUsnChanged() {
    if (_loadedSavedLogin && usnController.text.trim().isEmpty) {
      _clearSavedLogin();
    }
  }

  Future<void> _saveLogin() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(
        'portal_usn', usnController.text.trim().toUpperCase());
    await prefs.setString('portal_dob', dobController.text.trim());
    await prefs.setString('portal_verification_type', verificationType);
    await prefs.setString(
        'portal_verification_value', verificationValueController.text.trim());
  }

  Future<void> _clearSavedLogin() async {
    final prefs = await SharedPreferences.getInstance();
    await Future.wait([
      prefs.remove('portal_usn'),
      prefs.remove('portal_dob'),
      prefs.remove('portal_verification_type'),
      prefs.remove('portal_verification_value'),
    ]);
    if (!mounted) return;
    dobController.clear();
    verificationValueController.clear();
    setState(() => verificationType = "Father's mobile number");
  }

  Widget getDateRangePicker() {
    return Center(
      // child: SfDateRangePicker(
      //   view: DateRangePickerView.decade,
      //   selectionMode: DateRangePickerSelectionMode.single,
      //   // minDate: DateTime(1990, 01, 01),
      //   // maxDate: DateTime(2009, 01, 01),

      //   navigationDirection: DateRangePickerNavigationDirection.vertical,
      //   onSelectionChanged: (DateRangePickerSelectionChangedArgs args) {
      //     selectedDate = args.value;
      //     setState(() {
      //       dobController.text = formatter.format(selectedDate);
      //     });
      //   },
      child: DatePicker(
        initialPickerType: PickerType.years,
        minDate: DateTime(DateTime.now().year - 32, 01, 01),
        maxDate: DateTime(DateTime.now().year - 15, 01, 01),
        onDateSelected: (value) {
          setState(() {
            dobController.text = formatter.format(value);
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
          return AlertDialog(
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(20),
              ),
              title: const Text('Pick a date'),
              content: SizedBox(
                height: size.height * 0.5,
                width: size.width * 0.8,
                child: Column(
                  children: <Widget>[
                    Center(
                      child: getDateRangePicker(),
                    ),
                    MaterialButton(
                      child: const Text("OK"),
                      onPressed: () {
                        Navigator.pop(context);
                      },
                    )
                  ],
                ),
              ));
        });
  }

  Future<void> _openPortalLogin() async {
    final sisData = Provider.of<SisData>(context, listen: false);
    final isDummy = usnController.text.trim().toUpperCase() == 'DUMMY';
    if (!isDummy && !(_formKey.currentState?.validate() ?? false)) return;
    if (isDummy) {
      await sisData.getData('DUMMY', '', false);
      if (mounted && widget.closeAfterSync) Navigator.of(context).pop();
      return;
    }
    await _saveLogin();
    final synced = await Navigator.of(context).push<bool>(MaterialPageRoute(
      builder: (_) => PortalLoginScreen(
        initialUsn: usnController.text.toUpperCase(),
        initialDob: dobController.text,
        initialVerificationType: verificationType,
        initialVerificationValue: verificationValueController.text.trim(),
        reuseSession: sisData.hasData &&
            sisData.usn.trim().toUpperCase() ==
                usnController.text.trim().toUpperCase(),
      ),
    ));
    if (synced == true &&
        mounted &&
        (widget.closeAfterSync || Navigator.of(context).canPop())) {
      Navigator.of(context).pop();
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
  void dispose() {
    usnController.removeListener(_handleUsnChanged);
    usnController.dispose();
    dobController.dispose();
    verificationValueController.dispose();
    passwordFocus.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    final textStyle = CustomTheme.textStyle(context);
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    TextFormField usnForm = TextFormField(
      style: textStyle.copyWith(fontSize: width * 0.05),
      cursorHeight: 30, // autofocus: true,
      controller: usnController,
      key: const ValueKey('usn'),
      onFieldSubmitted: _submitUSN,
      decoration: InputDecoration(labelText: "USN", labelStyle: textStyle),
      validator: (value) {
        if (!RegExp(r"1MS\d\d[A-Z]+\d+").hasMatch(value!.toUpperCase()) &&
            value != "dummy") {
          setState(() {
            isPressed = false;
          });
          return "Please enter a valid USN, such as 1ms22is001";
        }
        return null;
      },
    );
    TextFormField dobForm = TextFormField(
      onTap: () {
        _selectDate(context);
      },
      style: textStyle.copyWith(fontSize: width * 0.05),
      readOnly: true,
      key: const ValueKey('dob'),
      controller: dobController,
      focusNode: passwordFocus,
      decoration: InputDecoration(
          labelText: "Date of Birth",
          labelStyle: textStyle,
          suffix: GestureDetector(
            child: const Icon(Icons.calendar_view_month),
            onTap: () {
              _selectDate(context);
            },
          )),
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
              child: Stack(
                children: [
                  if (fillForm && !isPressed)
                    Positioned(
                      top: height * 0.07,
                      left: width * 0.04,
                      child: NeumorphicButton(
                        padding: EdgeInsets.all(width * 0.03),
                        style: NeumorphicStyle(
                            intensity: 0.5,
                            color: const Color(0x00c00000),
                            boxShape: NeumorphicBoxShape.roundRect(
                                BorderRadius.circular(30))),
                        child: const Icon(Icons.chevron_left),
                        onPressed: () {
                          setState(() {
                            fillForm = false;
                            dobController.clear();
                            _formKey.currentState!.reset();
                            sisData.isValidData = true;
                          });
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
                              if (!fillForm)
                                const Text(
                                  "By students of",
                                  style: TextStyle(
                                      color: Colors.black,
                                      fontSize: 20,
                                      fontFamily: 'Comfortaa'),
                                ),
                              SizedBox(
                                height: (!fillForm) ? 50 : 10,
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
                                        padding: const EdgeInsets.only(
                                            left: 50.0, right: 50.0),
                                        child: usnForm,
                                      ),
                                      Padding(
                                        padding: const EdgeInsets.only(
                                            left: 50.0, right: 50.0),
                                        child: dobForm,
                                      ),
                                      Padding(
                                        padding: const EdgeInsets.symmetric(
                                            horizontal: 50.0),
                                        child: DropdownButtonFormField<String>(
                                          initialValue: verificationType,
                                          decoration: InputDecoration(
                                              labelText: 'Verification type',
                                              labelStyle: textStyle),
                                          items: const [
                                            DropdownMenuItem(
                                                value: "Father's mobile number",
                                                child: Text(
                                                    "Father's mobile number")),
                                            DropdownMenuItem(
                                                value: "Mother's mobile number",
                                                child: Text(
                                                    "Mother's mobile number")),
                                            DropdownMenuItem(
                                                value: 'ID card number',
                                                child: Text('ID card number')),
                                          ],
                                          onChanged: (value) => setState(
                                              () => verificationType = value!),
                                        ),
                                      ),
                                      Padding(
                                        padding: const EdgeInsets.symmetric(
                                            horizontal: 50.0),
                                        child: TextFormField(
                                          controller:
                                              verificationValueController,
                                          keyboardType: TextInputType.number,
                                          maxLength: 4,
                                          decoration: InputDecoration(
                                              labelText: verificationType ==
                                                      'ID card number'
                                                  ? 'ID card number'
                                                  : 'Last four digits',
                                              labelStyle: textStyle),
                                          validator: (value) => value == null ||
                                                  value.trim().length < 4
                                              ? 'Enter the required verification value'
                                              : null,
                                        ),
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
                                  : NeumorphicButton(
                                      style: NeumorphicStyle(
                                          intensity: 0.5,
                                          color: const Color(0x00c00000),
                                          boxShape:
                                              NeumorphicBoxShape.roundRect(
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
                                          : const Text(
                                              "Student Login",
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
                                          setState(() => isPressed = false);
                                          await _openPortalLogin();
                                        }
                                      },
                                    ),
                              const SizedBox(
                                height: 20,
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
                ],
              ),
            ),
          );
  }
}
