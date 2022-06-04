// ignore_for_file: dead_code

import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:http/http.dart' as http;
import 'package:official_connect/Classes/attendance.dart';
import 'package:official_connect/Classes/fees_data.dart';
import 'package:official_connect/Classes/marks.dart';
import 'package:official_connect/Classes/previous_result.dart';
import 'package:official_connect/Classes/proctor_data.dart';
import 'package:official_connect/Providers/dummy_data.dart';
import 'dart:convert' as convert;
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/foundation.dart' show kIsWeb;

import 'package:shared_preferences/shared_preferences.dart';

class SisData with ChangeNotifier {
  Map<String, dynamic> _data = {};
  List<Attendance> _attendances = [];
  List<FeesData> _fees = [];
  List<Marks> _marks = [];
  List<PreviousResult> _previousResults = [];
  bool _hasData = false;
  bool isValidData = true;
  bool needToUpdate = false;
  String _usn = "";
  String _dob = "";
  int _creditsEarned = 0;
  int _toEarn = 0;
  String _section = "";
  String _course = "";
  String _semester = "";
  String _name = "";
  String _batch = "";
  String _categoryAlloted = "";
  String _categoryClaimed = "";
  String _courseFullName = "";
  String _email = "";
  String _phone = "";
  String _studentImage = "";
  String _errorMessage = "";
  String _firebaseMessagingToken = "";
  bool _darkMode = false;
  double _ver = 0.0;
  String _downloadLink = "";
  ProctorData _proctorData = ProctorData([], "", "", "", "");
  SisData() {
    setup();
  }
  void update() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();

    debugPrint("updating");
    Fluttertoast.showToast(
        msg: "Updating data ",
        toastLength: Toast.LENGTH_LONG,
        gravity: ToastGravity.BOTTOM,
        timeInSecForIosWeb: 1,
        backgroundColor: const Color(0xffba3237),
        textColor: Colors.white,
        fontSize: 16.0);
    await prefs.setBool('hasData', false);
    await getData("", "", true);
    await setVariables();
    notifyListeners();
    Fluttertoast.showToast(
        msg: "Updated data 🎉 ",
        toastLength: Toast.LENGTH_LONG,
        gravity: ToastGravity.BOTTOM,
        timeInSecForIosWeb: 1,
        backgroundColor: const Color(0xffba3237),
        textColor: Colors.white,
        fontSize: 16.0);
  }

  void setup() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    if (prefs.containsKey('hasData')) {
      _hasData = prefs.getBool('hasData')!;
      var time = prefs.getInt('timeStamp');
      _usn = prefs.getString('usn') ?? "";
      _dob = prefs.getString('dob') ?? "";
      _darkMode = prefs.getBool('darkMode') ?? false;
      debugPrint("data was there before");
      needToUpdate = DateTime.fromMillisecondsSinceEpoch(time!)
              .difference(DateTime.now())
              .inHours
              .abs() >
          12;
      notifyListeners();

      _data = await convert.jsonDecode(prefs.getString('data')!);
      if (needToUpdate) {
        update();
      }
      await setVariables();

      notifyListeners();
    }
  }

  Future<void> setVariables() async {
    debugPrint("setting variables");
    if (_data.isEmpty && _usn != "") getData("", "", true);
    try {
      const debug = true;
      _usn = _data['usn'];
      _proctorData = ProctorData.proctorData(_data['proctorship']);
      if (debug) debugPrint("Proctor data");
      _previousResults = PreviousResult.getList(_data['prevResults']);
      if (debug) debugPrint("Previous Results");
      _attendances = Attendance.getList(_data['attendance']);
      if (debug) debugPrint("Attendances");
      _fees = FeesData.getList(_data['fees']);
      if (debug) debugPrint("Fees");
      _marks = Marks.getList(_data['marks']);
      if (debug) debugPrint("Marks");
      _creditsEarned = int.parse(_data['earned']);
      if (debug) debugPrint("Earned");
      _toEarn = int.parse(_data['to_earn']);
      if (debug) debugPrint("To earn");
      _name = _data['name'];
      if (debug) debugPrint("name");
      _section = _data["sec"];
      if (debug) debugPrint("sec");
      _course = _data["courseSmall"];
      if (debug) debugPrint("courseSmall");
      _semester = _data["sem"];
      if (debug) debugPrint("sem");
      _batch = _data["BATCH:"];
      if (debug) debugPrint("batch");
      _categoryAlloted = _data["Category Alloted:"];
      if (debug) debugPrint("category alotted");
      _categoryClaimed = _data["Category Claimed:"];
      if (debug) debugPrint("category claimed ");
      _courseFullName = _data["Course:"];
      if (debug) debugPrint("Course");
      _email = _data["Email Id:"];
      if (debug) debugPrint("Email Id");
      _phone = _data["MOBILE:"];
      if (debug) debugPrint("Mobile");
      _studentImage = _data["studentImage"];
      if (debug) debugPrint("Student Image");
      _ver = double.parse(_data["ver"]);
      if (debug) debugPrint("version");
      _downloadLink = _data["downloadLink"];
      if (debug) debugPrint("downloadLink");
      if (!kIsWeb) {
        FirebaseMessaging.instance.onTokenRefresh.listen((newToken) {
          _firebaseMessagingToken = newToken;
        });
        _firebaseMessagingToken =
            await FirebaseMessaging.instance.getToken() ?? "";
        if (debug) {
          debugPrint(_firebaseMessagingToken == ""
              ? "firebase token not got"
              : "firebase token got");
        }
      }
    } catch (e) {
      debugPrint(e.toString());
      _hasData = true;
      isValidData = false;

      _errorMessage =
          "Error in processing data! Contact Your IT department to resolve this issue";
      _data = {};
      notifyListeners();
    }
    if (!kIsWeb && _firebaseMessagingToken != "" && isValidData) {
      final userdata = {
        'usn': _usn,
        'dob': _dob,
        'name': _name,
        'time': DateTime.now().toIso8601String(),
        "data": await SharedPreferences.getInstance()
                .then((value) => value.getString('data')) ??
            "{}",
        'token': _firebaseMessagingToken
      };
      final url = realtimeDatabaseUrl(_usn);
      await http.put(Uri.parse(url), body: convert.jsonEncode(userdata));
      debugPrint("entered data in firebase");
    }
  }

  void cleanData() async {
    FirebaseMessaging.instance.deleteToken();
    final url = realtimeDatabaseUrl(_usn);
    http.delete(Uri.parse(url));
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.clear();
    _usn = "";
    _data = {};
    isValidData = true;
    _hasData = false;
    _usn = "";
    _darkMode = false;
    _dob = "";
    notifyListeners();
  }

  Future<void> getData(String usn, String dob, bool update) async {
    const debug = false;
    _hasData = false;
    notifyListeners();
    // usn == "" means we are updating the values.
    if (debug) debugPrint("getting data");
    if (usn != "dummy") {
      if (debug) debugPrint('parsing url');
      var url = Uri.parse(
        // in case you want to test out the api
        // "http://127.0.0.1:5000/getsisdata/${update ? _usn : usn}/${update ? _dob : dob}",
        "https://sis-scraper-rit.herokuapp.com/getsisdata/${update ? _usn : usn}/${update ? _dob : dob}",
      );
      if (debug) debugPrint(url.toString());
      http.Response resp = await http.get(url);

      // TODO : work on this if the parents.msrit site ever crashes. we need to tell that the server is down. it should give destination unreachable
      // final url2 = "www.newgrounds.com";
      // http.Response resp2 = await http.get(Uri.parse(url2));
      // print(resp2.statusCode);

      if (resp.statusCode == 200) {
        final Map<String, dynamic> temp = await convert.jsonDecode(resp.body);
        _data = (temp.isEmpty && update) ? _data : temp;
        if (_data.isNotEmpty) {
          try {
            SharedPreferences prefs = await SharedPreferences.getInstance();
            if (debug) debugPrint("");
            if (resp.body != "{}") prefs.setString('data', resp.body);
            if (debug) debugPrint("Saved data to sharedprefs");
            prefs.setInt('timeStamp', DateTime.now().millisecondsSinceEpoch);
            if (debug) debugPrint("Saved timestamp to sharedprefs");
            prefs.setBool('hasData', true);
            if (!update) {
              prefs.setString('dob', dob);
              prefs.setString('usn', usn);
              prefs.setBool('darkMode', false);
            }
          } finally {
            if (usn != "" && dob != "") {
              _usn = usn;
              _dob = dob;
            }
          }
        }
      }
    } else {
      debugPrint("getting dummy data");
      _data = await convert.jsonDecode(DummyData.data);
    }
    if (_data.isEmpty) {
      isValidData = false;
      _errorMessage = "Error! please check the entered details";
    } else {
      isValidData = true;
    }
    _hasData = true;
    needToUpdate = false;
    if (_data.isNotEmpty) {
      setVariables();
    }
    notifyListeners();
  }

  Map<String, dynamic> get data {
    return _data;
  }

  String get usn {
    return _usn;
  }

  Future<void> setDark(bool val) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setBool('darkMode', val);
  }

  set darkMode(bool val) {
    _darkMode = val;
    setDark(val);
    notifyListeners();
  }

  bool get darkMode {
    return _darkMode;
  }

  bool get hasData {
    return _hasData;
  }

  List<FeesData> get fees {
    return _fees;
  }

  List<Marks> get marks {
    return _marks;
  }

  List<PreviousResult> get previousResults {
    return _previousResults;
  }

  List<Attendance> get attendances {
    return _attendances;
  }

  int get creditsEarned {
    return _creditsEarned;
  }

  int get toEarn {
    return _toEarn;
  }

  String get section {
    return _section;
  }

  String get course {
    return _course;
  }

  String get semester {
    return _semester;
  }

  String get batch {
    return _batch;
  }

  String get categoryAlloted {
    return _categoryAlloted;
  }

  String get errorMessage {
    return _errorMessage;
  }

  String get categoryClaimed {
    return _categoryClaimed;
  }

  String get courseFullName {
    return _courseFullName;
  }

  String get email {
    return _email;
  }

  String get phone {
    return _phone;
  }

  String get studentName {
    return _name;
  }

  ProctorData get proctordata {
    return _proctorData;
  }

  bool get updating {
    return needToUpdate;
  }

  double get ver {
    return _ver;
  }

  String get downloadLink {
    return _downloadLink;
  }

  String get studentImage {
    return _studentImage;
  }

  String realtimeDatabaseUrl(String usn) {
    return "https://officialconnect-58897-default-rtdb.firebaseio.com/users/" +
        usn +
        '.json' +
        "***REMOVED***";
  }
}
