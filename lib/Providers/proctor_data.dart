import 'dart:convert';

import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:fluttertoast/fluttertoast.dart';

class ProctorData with ChangeNotifier {
  bool _dataPresent = false;
  bool _isLoggedIn = true;
  bool _waitForLoginCheck = true;
  List _requests = [];
  List _messages = [];
  List _enrolled = [];
  String _name = "";
  String _email = "";

  ProctorData() {
    checkIfLogin();
  }
  void checkIfLogin() async {
    FirebaseAuth.instance.authStateChanges().listen((event) {
      final auth = FirebaseAuth.instance.currentUser;
      if (auth != null) {
        _email = auth.email!;
        _isLoggedIn = true;
      } else {
        _isLoggedIn = false;
      }
      _waitForLoginCheck = false;
      notifyListeners();
    });
  }

  void getData() async {
    if (_email == "") return;
    final url = Uri.parse(
        "https://msrit-student-proctor-api.herokuapp.com/get_proctor_details");
    final bod = {"proctor_email": _email};
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

  void showToast(String message) {
    Fluttertoast.showToast(
        msg: message,
        toastLength: Toast.LENGTH_LONG,
        gravity: ToastGravity.BOTTOM,
        timeInSecForIosWeb: 1,
        backgroundColor: const Color(0xffba3237),
        textColor: Colors.white,
        fontSize: 16.0);
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
        showToast("Proctee accepted!");
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

  void sendMessage(List<String> usns, String message, String title,
      BuildContext context) async {
    final url = Uri.parse(
        "https://msrit-student-proctor-api.herokuapp.com/send_message");
    final bod = {
      "proctor_email": _email,
      "message_title": title,
      "proctor_name": _name,
      "message_body": message,
      "usn_list": usns
    };
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
        getData();
        showToast("Message sent successfully!");
        Navigator.of(context).pop();
      }
      notifyListeners();
    } else {
      showToast("Error in sending message");
    }
  }

  void deleteMessage(Map messageDetails, BuildContext context) async {
    final url = Uri.parse(
        "https://msrit-student-proctor-api.herokuapp.com/delete_message");
    final bod = {
      "proctor_email": _email,
      "message_id": messageDetails['_id']["\$oid"]
    };
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
        _messages.removeAt(
            _messages.indexWhere((element) => element == messageDetails));
        showToast("Successfully deleted this message");
        Navigator.of(context).pop();
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

  bool get isLoggedIn {
    return _isLoggedIn;
  }

  bool get waitForLoggedIn {
    return _waitForLoginCheck;
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

  void toggleLogin() {
    final auth = FirebaseAuth.instance.currentUser;
    if (auth != null) {
      _isLoggedIn = true;
    } else {
      _isLoggedIn = false;
    }
    notifyListeners();
  }
}
