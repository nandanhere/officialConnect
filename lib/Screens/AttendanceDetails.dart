import 'package:flutter/material.dart';
import 'package:official_connect/Classes/Attendance.dart';

class AttendanceDetails extends StatelessWidget {
  final Attendance attendanceDetails;
  const AttendanceDetails({Key? key, required this.attendanceDetails})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Attendance details")),
      body: Center(
        child: Text(attendanceDetails.subjectName),
      ),
    );
  }
}
