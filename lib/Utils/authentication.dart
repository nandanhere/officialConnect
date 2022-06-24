import 'dart:convert';

import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:http/http.dart' as http;

final FirebaseAuth _auth = FirebaseAuth.instance;

String? uid;
String? userEmail;
Future<User?> registerWithEmailPassword(
    String email, String password, String name) async {
  // Initialize Firebase
  await Firebase.initializeApp();
  User? user;

  try {
    UserCredential userCredential = await _auth.createUserWithEmailAndPassword(
      email: email.toLowerCase().trim(),
      password: password,
    );

    user = userCredential.user;

    if (user != null) {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setBool('auth', true);
      print("set the vals");
      uid = user.uid;
      String userEmail = user.email!;
      print('updating user info');
      await user.updateDisplayName(name);
      final bod = {
        "proctor_email": userEmail.trim(),
        "proctor_name": name.trim()
      };
      final headers = {'Content-Type': 'application/json'};
      final encoding = Encoding.getByName("utf-8");

      final resp = await http.post(
        Uri.parse(
            "https://msrit-student-proctor-api.herokuapp.com/add_proctor"),
        headers: headers,
        encoding: encoding,
        body: jsonEncode(bod),
      );
      if (jsonDecode(resp.body)['message'] != "SUCCESS") {
        throw Exception("Error in proctor api");
      }
    }
  } catch (e) {
    print(e);
  }

  return user;
}

Future<User?> signInWithEmailPassword(String email, String password) async {
  await Firebase.initializeApp();
  User? user;

  try {
    UserCredential userCredential = await _auth.signInWithEmailAndPassword(
      email: email,
      password: password,
    );
    user = userCredential.user;

    if (user != null) {
      uid = user.uid;
      userEmail = user.email;

      SharedPreferences prefs = await SharedPreferences.getInstance();
      await prefs.setBool('auth', true);
    }
  } on FirebaseAuthException catch (e) {
    if (e.code == 'user-not-found') {
      SisData.showToast('No user found for that email.');
    } else if (e.code == 'wrong-password') {
      SisData.showToast('Wrong password provided.');
    }
  }

  return user;
}

Future<String> signOut() async {
  await _auth.signOut();

  SharedPreferences prefs = await SharedPreferences.getInstance();
  prefs.setBool('auth', false);

  uid = null;
  userEmail = null;

  return 'User signed out';
}

final GoogleSignIn googleSignIn = GoogleSignIn();

String? name;
String? imageUrl;
Future<String> signInWithGoogle() async {
  // Initialize Firebase
  await Firebase.initializeApp();
  User? user;

  // The `GoogleAuthProvider` can only be used while running on the web
  GoogleAuthProvider authProvider = GoogleAuthProvider();

  try {
    final UserCredential userCredential =
        await _auth.signInWithPopup(authProvider);

    user = userCredential.user;
  } catch (e) {
    debugPrint(e.toString());
  }

  if (user != null) {
    uid = user.uid;
    name = user.displayName;
    userEmail = user.email;
    imageUrl = user.photoURL;

    SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setBool('auth', true);
  }

  return user!.uid;
}

void signOutGoogle() async {
  await googleSignIn.signOut();
  await _auth.signOut();

  SharedPreferences prefs = await SharedPreferences.getInstance();
  prefs.setBool('auth', false);

  uid = null;
  name = null;
  userEmail = null;
  imageUrl = null;

  print("User signed out of Google account");
}
