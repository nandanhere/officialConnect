import 'dart:convert';

import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class ProctorData with ChangeNotifier {
  bool _dataPresent = false;
  List _requests = [];
  List _messages = [];
  List _enrolled = [];
  String _name = "";
  String _email = "";
  ProctorData() {
    getData();
  }
  void getData() async {
    final auth = FirebaseAuth.instance.currentUser;
    final url = Uri.parse(
        "https://msrit-student-proctor-api.herokuapp.com/get_proctor_details");
    final bod = {"proctor_email": auth!.email};
    final headers = {'Content-Type': 'application/json'};
    final encoding = Encoding.getByName("utf-8");
    http.Response resp = await http.post(
      url,
      headers: headers,
      encoding: encoding,
      body: jsonEncode(bod),
    );
    print(resp.body);
    if (resp.body.isNotEmpty) {
      _dataPresent = true;
      processData(jsonDecode(resp.body));
      notifyListeners();
    }
  }

  void processData(Map data) {
    _requests = data['requests'];
    _messages = data['messages'];
    _enrolled = data['enrolled'];
    _name = data['proctor_name'];
    _email = data['proctor_email'];
  }

  void acceptProctee(Map studDetails) async {
    final url = Uri.parse(
        "https://msrit-student-proctor-api.herokuapp.com/accept_proctee");
    final bod = {"proctor_email": _email, "usn": studDetails["usn"]};
    final headers = {'Content-Type': 'application/json'};
    final encoding = Encoding.getByName("utf-8");
    http.Response resp = await http.post(
      url,
      headers: headers,
      encoding: encoding,
      body: jsonEncode(bod),
    );
    if (resp.body.isNotEmpty) {
      if (jsonDecode(resp.body)['message'] == "SUCCESS") {
        _requests.removeAt(
          _requests.indexWhere(
            (element) => element['usn'] == studDetails['usn'],
          ),
        );
        _enrolled.add(studDetails);
      }
      notifyListeners();
    }
  }

  void rejectProctee(Map studDetails) async {
    final url = Uri.parse(
        "https://msrit-student-proctor-api.herokuapp.com/reject_proctee");
    final bod = {"proctor_email": _email, "usn": studDetails["usn"]};
    final headers = {'Content-Type': 'application/json'};
    final encoding = Encoding.getByName("utf-8");
    http.Response resp = await http.post(
      url,
      headers: headers,
      encoding: encoding,
      body: jsonEncode(bod),
    );
    if (resp.body.isNotEmpty) {
      if (jsonDecode(resp.body)['message'] == "SUCCESS") {
        _requests.removeAt(
          _requests.indexWhere(
            (element) => element['usn'] == studDetails['usn'],
          ),
        );
      }
      notifyListeners();
    }
  }

  String get name {
    return _name;
  }

  String get email {
    return _email;
  }

  bool get dataPresent {
    return _dataPresent;
  }

  List get messages {
    return _messages;
  }

  List get enrolled {
    return _enrolled;
  }

  List get requests {
    return _requests;
  }
}
