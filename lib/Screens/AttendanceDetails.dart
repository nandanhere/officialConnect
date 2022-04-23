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
        body: Container(
            alignment: Alignment.center,
            color: Colors.grey,
            child:
                // Column(
                //   children: [
                Column(
              children: [
                Expanded(
                  child: GridView.count(
                    mainAxisSpacing: 20.0,
                    crossAxisCount: 7,
                    children: [
                      Text("Mon"),
                      Text("Tue"),
                      Text("Wed"),
                      Text("Thur"),
                      Text("Fri"),
                      Text("Sat"),
                      Text("Sun"),
                    ],
                  ),
                ),
                Expanded(
                    child: GridView.count(
                  crossAxisCount: 7,
                  mainAxisSpacing: 20.0,
                  children: [],
                ))
              ],
            )
            //   ],
            // ),
            )
        // Center(
        //   child: Text(attendanceDetails.subjectName),
        // ),
        );
  }
}
