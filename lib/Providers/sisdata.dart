import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert' as convert;

import 'package:shared_preferences/shared_preferences.dart';

class SisData with ChangeNotifier {
  Map<String, dynamic> _data = {};
  bool _hasData = false;
  bool isValidData = true;
  bool needToUpdate = true;
  String _usn = "";
  String _dob = "";
  SisData() {
    setup();
  }
  void setup() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    if (prefs.containsKey('hasData')) {
      _hasData = prefs.getBool('hasData')!;
      var time = prefs.getInt('timeStamp');
      _usn = prefs.getString('usn') ?? "";
      _dob = prefs.getString('dob') ?? "";
      print("data was there before");
      needToUpdate = DateTime.fromMillisecondsSinceEpoch(time!)
              .difference(DateTime.now())
              .inHours >
          24;
      if (needToUpdate) {
        prefs.setBool('hasData', false);
      } else {
        _data = convert.jsonDecode(prefs.getString('data') ?? "{}");
      }
      notifyListeners();
    }
  }

  void cleanData() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.clear();
    _usn = "";
    _data = {};
    notifyListeners();
  }

  void getData(String usn, String dob) async {
    var url = Uri.parse(
        "https://sis-scraper-rit.herokuapp.com/getsisdata/${(_usn == "") ? usn : _usn}/${(_dob == "") ? dob : _dob}");
    http.Response resp = await http.get(url);
    if (resp.statusCode == 200) {
      _data = convert.jsonDecode(resp.body);
      print(_data);
      try {
        SharedPreferences prefs = await SharedPreferences.getInstance();
        prefs.setBool('hasData', true);
        prefs.setInt('timeStamp', DateTime.now().millisecondsSinceEpoch);
        prefs.setString('data', resp.body);
        prefs.setString('dob', (_usn == "") ? usn : _usn);
        prefs.setString('usn', (_dob == "") ? dob : _dob);
      } finally {
        _usn = usn;
        _dob = dob;
      }

      // print("sis" + _data['fees']);
      if (_data.isEmpty) isValidData = false;
      _hasData = true;
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
}
