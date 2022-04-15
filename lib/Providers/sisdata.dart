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

  SisData() {
    setup();
  }
  void setup() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    if (prefs.containsKey('hasData')) {
      _hasData = prefs.getBool('hasData')!;
      notifyListeners();
      var time = prefs.getInt('timeStamp');
      _usn = prefs.getString('usn') ?? "";
      _dob = prefs.getString('dob') ?? "";
      // print("data was there before");
      needToUpdate = DateTime.fromMillisecondsSinceEpoch(time!)
              .difference(DateTime.now())
              .inDays
              .abs() >
          1;
      _data = await convert.jsonDecode(prefs.getString('data')!);
      if (needToUpdate) {
        // print("updating");
        await prefs.setBool('hasData', false);
        await getData("", "");
        // print(_data['prevResults'][0]);
      }
      setVariables();

      notifyListeners();
    }
  }

  void setVariables() async {
    if (_data.isEmpty) getData("", "");
    _previousResults = PreviousResult.getList(_data['prevResults']);
    _attendances = Attendance.getList(_data['attendance']);
    _fees = FeesData.getList(_data['fees']);
    _marks = Marks.getList(_data['marks']);
    _creditsEarned = int.parse(_data['earned']);
    _toEarn = int.parse(_data['to_earn']);
    _section = _data['sec'];
    _course = _data['course'];
    _semester = _data['sem'];
    _name = _data['name'];
  }

  void cleanData() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.clear();
    _usn = "";
    _data = {};
    notifyListeners();
  }

  Future<void> getData(String usn, String dob) async {
    var url = Uri.parse(
        "https://sis-scraper-rit.herokuapp.com/getsisdata/${(_usn == "") ? usn : _usn}/${(_dob == "") ? dob : _dob}");
    http.Response resp = await http.get(url);
    if (resp.statusCode == 200) {
      final Map<String, dynamic> temp = await convert.jsonDecode(resp.body);
      _data = temp.isEmpty ? _data : temp;
      try {
        SharedPreferences prefs = await SharedPreferences.getInstance();
        prefs.setBool('hasData', true);
        prefs.setInt('timeStamp', DateTime.now().millisecondsSinceEpoch);
        prefs.setString('data', resp.body);
        prefs.setString('dob', (_usn == "") ? usn : _usn);
        prefs.setString('usn', (_dob == "") ? dob : _dob);
      } finally {
        if (usn != "" && dob != "") {
          _usn = usn;
          _dob = dob;
        }
      }

      if (_data.isEmpty) isValidData = false;
      _hasData = true;
      needToUpdate = false;
      setVariables();
      notifyListeners();
    }
  }

  Map<String, dynamic> get data {
    return _data;
  }

  String get usn {
    return _usn;
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

  String get studentName {
    return _name;
  }

  bool get updating {
    return needToUpdate;
  }
}
