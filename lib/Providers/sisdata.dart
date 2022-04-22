import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart';
import 'package:official_connect/Classes/Attendance.dart';
import 'package:official_connect/Classes/FeesData.dart';
import 'package:official_connect/Classes/Marks.dart';
import 'package:official_connect/Classes/PreviousResult.dart';
import 'dart:convert' as convert;

import 'package:shared_preferences/shared_preferences.dart';

class SisData with ChangeNotifier {
  Map<String, dynamic> _data = {};
  List<Attendance> _attendances = [];
  List<FeesData> _fees = [];
  List<Marks> _marks = [];
  List<PreviousResult> _previousResults = [];
  bool _hasData = false;
  bool isValidData = true;
  bool needToUpdate = true;
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
  bool _darkMode = false;

  SisData() {
    setup();
  }
  void setup() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    if (prefs.containsKey('hasData')) {
      _hasData = prefs.getBool('hasData')!;
      var time = prefs.getInt('timeStamp');

      _usn = prefs.getString('usn') ?? "";
      prefs.setString('usn', "");
      _dob = prefs.getString('dob') ?? "";
      _darkMode = prefs.getBool('darkMode') ?? false;
      notifyListeners();

      // debugPrint("data was there before");
      needToUpdate = DateTime.fromMillisecondsSinceEpoch(time!)
              .difference(DateTime.now())
              .inDays
              .abs() >
          1;
      _data = await convert.jsonDecode(prefs.getString('data')!);
      if (needToUpdate) {
        debugPrint("updating");
        await prefs.setBool('hasData', false);
        await getData("", "", true);
        // debugPrint(_data['prevResults'][0]);
      }
      await setVariables();

      notifyListeners();
    }
  }

  Future<void> setVariables() async {
    debugPrint("setting variables");
    if (_data.isEmpty && _usn != "") getData("", "", true);
    try {
      const debug = false;
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
    } catch (e) {
      debugPrint(e.toString());
      _hasData = false;
    }
  }

  void cleanData() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.clear();
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
    _hasData = false;
    notifyListeners();
    // usn == "" means we are updating the values.
    debugPrint("getting data");
    var url = Uri.parse(
        "https://sis-scraper-rit.herokuapp.com/getsisdata/${update ? _usn : usn}/${update ? _dob : dob}");
    http.Response resp = await http.get(url);
    if (resp.statusCode == 200) {
      final Map<String, dynamic> temp = await convert.jsonDecode(resp.body);
      _data = (temp.isEmpty && update) ? _data : temp;
      if (_data.isNotEmpty) {
        try {
          SharedPreferences prefs = await SharedPreferences.getInstance();
          prefs.setInt('timeStamp', DateTime.now().millisecondsSinceEpoch);
          if (resp.body != "{}") prefs.setString('data', resp.body);
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
      if (_data.isEmpty) {
        isValidData = false;
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

  String get categoryClaimed {
    return _categoryClaimed;
  }

  String get courseFullName {
    return _courseFullName;
  }

  String get email {
    return _email;
  }

  String get studentName {
    return _name;
  }

  bool get updating {
    return needToUpdate;
  }

  String get studentImage {
    return _studentImage;
  }
}
