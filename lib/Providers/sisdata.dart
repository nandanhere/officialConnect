// ignore_for_file: dead_code

import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:http/http.dart' as http;
import 'package:official_connect/Classes/attendance.dart';
import 'package:official_connect/Classes/fees_data.dart';
import 'package:official_connect/Classes/marks.dart';
import 'package:official_connect/Classes/previous_result.dart';
import 'package:official_connect/Classes/sis_proctor_data.dart';
import 'package:official_connect/Providers/dummy_data.dart';
import 'dart:convert' as convert;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:official_connect/Services/firebase_operations.dart';

class SisData with ChangeNotifier {
  Map<String, dynamic> _data = {};
  List<Attendance> _attendances = [];
  List<FeesData> _fees = [];
  List<Marks> _marks = [];
  List<PreviousResult> _previousResults = [];
  final List<dynamic> _proctorMessages = [];
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
  String _themeMode = 'system';
  bool _darkMode = false;
  bool _diagnosticsEnabled = true;
  double _ver = 0.0;
  String _proctorEmail = "";
  String _downloadLink = "";
  SisProctorData _proctorData = SisProctorData([], "", "", "", "");
  SisData() {
    // Re-evaluate the effective theme when the OS theme changes while the
    // preference is set to "system".
    ui.PlatformDispatcher.instance.onPlatformBrightnessChanged = () {
      if (_themeMode == 'system') notifyListeners();
    };
    // cleanData();
    setup();
  }

  Future<bool> isConnected() async {
    try {
      final result = await InternetAddress.lookup('google.com');
      if (result.isNotEmpty && result[0].rawAddress.isNotEmpty) {
        return true;
      }
    } on SocketException catch (_) {
      return false;
    }
    return false;
  }

  static void showToast(String message) {
    Fluttertoast.showToast(
      msg: message,
      toastLength: Toast.LENGTH_LONG,
      gravity: ToastGravity.BOTTOM,
      timeInSecForIosWeb: 1,
      backgroundColor: const Color(0xffba3237),
      textColor: Colors.white,
      fontSize: 16.0,
    );
  }

  void setup() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    // if we already have data, check if the data is
    if (prefs.containsKey('hasData') && prefs.getBool('hasData') == true) {
      _hasData = true;
      var time = prefs.getInt('timeStamp') ?? 0;
      _usn = prefs.getString('usn') ?? "";
      _dob = prefs.getString('dob') ?? "";
      _proctorEmail = prefs.getString('proctorEmail') ?? "";
      _darkMode = prefs.getBool('darkMode') ?? false;
      // Migrate the old boolean preference: an explicit dark/light choice is
      // kept, otherwise the theme follows the OS setting.
      _themeMode =
          prefs.getString('themeMode') ??
          (prefs.containsKey('darkMode')
              ? (_darkMode ? 'dark' : 'light')
              : 'system');
      _diagnosticsEnabled = prefs.getBool('diagnosticsEnabled') ?? true;
      await FirebaseOperations.setDiagnosticsEnabled(_diagnosticsEnabled);
      debugPrint(
        "data was there before. checking if it is older than 12 hours",
      );
      needToUpdate =
          DateTime.fromMillisecondsSinceEpoch(
            time,
          ).difference(DateTime.now()).inMilliseconds.abs() >
          const Duration(hours: 12).inMilliseconds;
      notifyListeners();

      // A missing or corrupted cache payload must never leave the app stuck
      // on the loading spinner: mark it as logged out instead.
      final raw = prefs.getString('data');
      if (raw == null || raw.isEmpty) {
        debugPrint('cache flagged as present but payload missing; resetting');
        await prefs.setBool('hasData', false);
        _hasData = false;
        notifyListeners();
        return;
      }
      try {
        _data = Map<String, dynamic>.from(await convert.jsonDecode(raw) as Map);
      } catch (e) {
        debugPrint('cached payload unreadable ($e); resetting');
        await prefs.setBool('hasData', false);
        _hasData = false;
        _data = {};
        notifyListeners();
        return;
      }
      // Keep showing cached data immediately. Refresh now requires the
      // authenticated portal WebView session; the legacy Lambda path cannot
      // satisfy the portal's current verification flow.
      await setVariables();
      // if (iscon) {
      //   await getProctorMessages();
      // }
      needToUpdate = false;

      notifyListeners();
    }
  }

  // This runs if the data stored is old/older than 12 hours
  void update() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();

    debugPrint("updating");
    showToast("Updating Data");

    await prefs.setBool('hasData', false);
    await getData("", "", true);
    await setVariables();
    notifyListeners();
    showToast("Updated data 🎉 ");
  }

  // This calls the scraper and gets the data for a user
  Future<void> getData(String usn, String dob, bool update) async {
    const debug = false;
    usn = usn.toUpperCase();
    _hasData = false;
    notifyListeners();
    // usn == "" means we are updating the values.
    debugPrint("getting data");
    if (usn != "DUMMY") {
      var url = Uri.parse(
        // in case you want to test out the api
        // "http://192.168.43.212:5000/getsisdata/${update ? _usn : usn}/${update ? _dob : dob}",
        "https://exv9mhwed2.execute-api.ap-south-1.amazonaws.com/default/sis?usn=${update ? _usn.trim() : usn.trim()}&dob=${update ? _dob : dob}",
      );
      // debugPrint(url.toString());
      http.Response resp = await http.get(url);
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
              // await getProctorMessages();
            }
          }
        }
      } else if (resp.statusCode == 428) {
        try {
          final validation = convert.jsonDecode(resp.body);
          _errorMessage =
              validation['message'] ??
              "The portal requires an additional validation step.";
        } catch (_) {
          _errorMessage = "The portal requires an additional validation step.";
        }
        isValidData = false;
      } else if (resp.statusCode >= 500) {
        isValidData = false;
        _errorMessage =
            "We encountered a Server error. Sorry for the inconvinience";
      }
    } else {
      debugPrint("getting dummy data");
      _data = await convert.jsonDecode(DummyData.data);
    }
    if (_data.isEmpty) {
      isValidData = false;
      _errorMessage =
          _errorMessage ==
              "We encountered a Server error. Sorry for the inconvinience"
          ? "We encountered a Server error. Sorry for the inconvinience"
          : "Error! please check the entered details";
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

  /// Applies data scraped inside the authenticated portal WebView and writes
  /// it to the same cache used by the existing native screens.
  Future<void> applyPortalData(
    Map<String, dynamic> data,
    String usn,
    String dob,
  ) async {
    final previous = Map<String, dynamic>.from(_data);
    final merged = Map<String, dynamic>.from(data);
    final sections = ((data['_sync'] as Map?)?['sections'] as Map?) ?? {};
    const sectionKeys = {
      'attendance': ['attendance'],
      'marks': ['marks'],
      'results': ['prevResults'],
      'fees': ['fees', 'refunds'],
      'proctor': ['proctorship'],
    };
    for (final entry in sectionKeys.entries) {
      final status = (sections[entry.key] as Map?)?['status'];
      if (status == 'error' || status == 'disabled') {
        for (final key in entry.value) {
          if (previous.containsKey(key)) merged[key] = previous[key];
        }
      } else if (status == 'partial' &&
          (entry.key == 'attendance' || entry.key == 'marks')) {
        final key = entry.value.single;
        merged[key] = _mergePartialCourseData(
          previous[key],
          merged[key],
          section: entry.key,
        );
      }
    }
    // A partial profile update should not blank fields already shown by the
    // app. Successful empty data sections are still allowed to replace cache.
    for (final entry in previous.entries) {
      if (!merged.containsKey(entry.key) && entry.key != '_sync') {
        merged[entry.key] = entry.value;
      }
    }
    merged['usn'] = usn.toUpperCase();
    _data = merged;
    _usn = usn.toUpperCase();
    _dob = dob;
    _hasData = true;
    isValidData = true;
    needToUpdate = false;
    await setVariables();
    if (!isValidData || _data.isEmpty) {
      throw const FormatException('Portal data is incompatible with the app');
    }
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('data', convert.jsonEncode(merged));
    await prefs.setString('usn', _usn);
    await prefs.setString('dob', _dob);
    await prefs.setBool('hasData', true);
    await prefs.setInt('timeStamp', DateTime.now().millisecondsSinceEpoch);
    notifyListeners();
  }

  List<dynamic> _mergePartialCourseData(
    Object? cached,
    Object? refreshed, {
    required String section,
  }) {
    final mergedByIdentity = <String, dynamic>{};
    final unidentified = <dynamic>[];

    void addItems(Object? source) {
      if (source is! List) return;
      for (final item in source) {
        if (item is! Map) continue;
        final identity = _courseIdentity(item, section: section);
        if (identity.isEmpty) {
          unidentified.add(item);
        } else {
          // Cached values are inserted first; refreshed values with the same
          // stable identity replace them when this helper is called second.
          mergedByIdentity[identity] = item;
        }
      }
    }

    addItems(cached);
    addItems(refreshed);
    return [...mergedByIdentity.values, ...unidentified];
  }

  String _courseIdentity(Map item, {required String section}) {
    String normalize(Object? value) =>
        value.toString().toLowerCase().replaceAll(RegExp(r'[^a-z0-9]'), '');

    if (section == 'attendance') {
      final code = normalize(item['code']);
      if (code.isNotEmpty) return 'code:$code';
    }

    final name = item['name']?.toString() ?? '';
    final codeInName = RegExp(
      r'\(([a-z0-9]+)\)',
      caseSensitive: false,
    ).firstMatch(name)?.group(1);
    if (codeInName != null && codeInName.isNotEmpty) {
      return 'code:${normalize(codeInName)}';
    }
    final normalizedName = normalize(name);
    return normalizedName.isEmpty ? '' : 'name:$normalizedName';
  }

  // after getting any sort of data, the data has to be read from. this does that
  Future<void> setVariables() async {
    debugPrint("setting variables");

    if (_data.isEmpty && _usn != "") getData("", "", true);

    try {
      const debug = true;

      _usn = _data['usn'] ?? '';
      _proctorData = SisProctorData.proctorData(_data['proctorship'] ?? []);
      if (debug) debugPrint("Proctor data");

      _previousResults = PreviousResult.getList(_data['prevResults'] ?? []);
      if (debug) debugPrint("Previous Results");

      _attendances = Attendance.getList(_data['attendance'] ?? []);
      if (debug) debugPrint("Attendances");

      _fees = FeesData.getList(_data['fees'] ?? []);
      if (debug) debugPrint("Fees");

      _marks = Marks.getList(_data['marks'] ?? []);
      if (debug) debugPrint("Marks");

      _creditsEarned = int.tryParse(_data['earned'] ?? '0') ?? 0;
      if (debug) debugPrint("Earned");

      _toEarn = int.tryParse(_data['to_earn'] ?? '0') ?? 0;
      if (debug) debugPrint("To earn");

      _name = _data['name'] ?? 'Unknown';
      if (debug) debugPrint("name");

      _section = _data["sec"] ?? 'Unknown';
      if (debug) debugPrint("sec");

      _course = _data["courseSmall"] ?? 'Unknown';
      if (debug) debugPrint("courseSmall");

      _semester = _data["sem"] ?? 'Unknown';
      if (debug) debugPrint("sem");

      _batch = _data["BATCH:"] ?? 'Unknown';
      if (debug) debugPrint("batch");

      _categoryAlloted = _data["Category Alloted:"] ?? 'Unknown';
      if (debug) debugPrint("category alotted");

      _categoryClaimed = _data["Category Claimed:"] ?? 'Unknown';
      if (debug) debugPrint("category claimed ");

      _courseFullName = _data["Course:"] ?? 'Unknown';
      if (debug) debugPrint("Course");

      _email = _data["Email Id:"] ?? 'Unknown';
      if (debug) debugPrint("Email Id");

      _phone = _data["MOBILE:"] ?? 'Unknown';
      if (debug) debugPrint("Mobile");

      _studentImage = _data["studentImage"] ?? '';
      if (debug) debugPrint("Student Image");

      _ver = double.tryParse(_data["ver"] ?? '1.0') ?? 1.0;
      if (debug) debugPrint("version");

      _downloadLink = _data["downloadLink"] ?? '';
      if (debug) debugPrint("downloadLink");
    } catch (e) {
      debugPrint(e.toString());
      _hasData = true;
      isValidData = false;

      _errorMessage =
          "Error in processing data! Contact Your IT department to resolve this issue";
      _data = {};
      notifyListeners();
    }
  }

  void cleanData() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    // Keep portal_* autofill suggestions across sign-out. A user can erase the
    // whole saved login set by clearing the USN on the native login screen.
    for (final key in const [
      'hasData',
      'timeStamp',
      'usn',
      'dob',
      'proctorEmail',
      'darkMode',
      'data',
      'auth',
    ]) {
      await prefs.remove(key);
    }
    _usn = "";
    _data = {};
    isValidData = true;
    _hasData = false;
    _usn = "";
    _darkMode = false;
    _dob = "";
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

  void proctorAuth(bool val) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setBool('auth', val);
  }

  set darkMode(bool val) {
    _darkMode = val;
    themeMode = val ? 'dark' : 'light';
  }

  /// 'system' (default), 'light' or 'dark'.
  String get themeMode => _themeMode;

  set themeMode(String val) {
    _themeMode = val;
    _darkMode = val == 'dark';
    SharedPreferences.getInstance().then((prefs) {
      prefs.setString('themeMode', val);
    });
    notifyListeners();
  }

  bool get darkMode {
    if (_themeMode == 'dark') return true;
    if (_themeMode == 'light') return false;
    return ui.PlatformDispatcher.instance.platformBrightness ==
        ui.Brightness.dark;
  }

  bool get diagnosticsEnabled => _diagnosticsEnabled;

  set diagnosticsEnabled(bool value) {
    _diagnosticsEnabled = value;
    SharedPreferences.getInstance().then((prefs) {
      prefs.setBool('diagnosticsEnabled', value);
    });
    FirebaseOperations.setDiagnosticsEnabled(value);
    notifyListeners();
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

  SisProctorData get proctordata {
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

  String get proctorEmail {
    return _proctorEmail;
  }

  List<dynamic> get proctorMessages {
    return _proctorMessages;
  }

  Map<String, dynamic> get syncMetadata =>
      Map<String, dynamic>.from((_data['_sync'] as Map?) ?? const {});

  String syncStatusFor(String section) {
    final sections = syncMetadata['sections'] as Map?;
    return (sections?[section] as Map?)?['status']?.toString() ?? 'unknown';
  }

  bool get hasSyncIssues {
    final sections = syncMetadata['sections'] as Map?;
    if (sections == null) return false;
    return sections.values.whereType<Map>().any((section) {
      final status = section['status'];
      return status == 'partial' || status == 'error';
    });
  }
}
