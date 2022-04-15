import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert' as convert;

class SisData with ChangeNotifier {
  Map<String, dynamic> _data = {};
  bool _hasData = false;
  bool isValidData = true;

  void getData(String usn, String dob) async {
    var url = Uri.parse(
        "https://sis-scraper-rit.herokuapp.com/getsisdata/${usn}/${dob}");
    http.Response resp = await http.get(url);
    if (resp.statusCode == 200) {
      _data = convert.jsonDecode(resp.body);
      // print(_data['fees']);
      if (_data.isEmpty) isValidData = false;
      _hasData = true;
      notifyListeners();
    }
  }

  Map<String, dynamic> get data {
    return _data;
  }

  bool get hasData {
    return _hasData;
  }
}
