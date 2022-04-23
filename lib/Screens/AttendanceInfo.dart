import 'package:flutter/material.dart';
import 'package:official_connect/Classes/Attendance.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Widgets/AttendanceGraph.dart';
import 'package:provider/provider.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import './AttendanceDetails.dart';

class AttendanceInfo extends StatelessWidget {
  const AttendanceInfo({Key? key}) : super(key: key);

  DateTime calcMinDate(List<ClassDay> dates) {
    //Calculates min date
    DateTime minDate = dates[0].date;
    for (int i = 0; i < dates.length; i++) {
      if (dates[i].date.isBefore(minDate)) {
        minDate = dates[i].date;
      }
    }
    return minDate;
  }

  DateTime calcMaxDate(List<ClassDay> dates) {
    //Calculates max date
    DateTime maxDate = dates[0].date;
    for (int i = 0; i < dates.length; i++) {
      if (dates[i].date.isAfter(maxDate)) {
        maxDate = dates[i].date;
      }
    }
    return maxDate;
  }

  DateTime calcFromDate(DateTime pDate, DateTime aDate) {
    //calculates from date
    if (pDate.isBefore(aDate)) {
      return pDate;
    } else if (pDate.isAfter(aDate)) {
      return aDate;
    } else {
      return pDate;
    }
  }

  DateTime calcToDate(DateTime pDate, DateTime aDate) {
    //calculates to date
    if (pDate.isBefore(aDate)) {
      return aDate;
    } else if (pDate.isAfter(aDate)) {
      return pDate;
    } else {
      return pDate;
    }
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    final sisData = Provider.of<SisData>(context);

    return Container(
      decoration: BoxDecoration(
          gradient: LinearGradient(
              begin: Alignment.bottomRight,
              end: Alignment.topLeft,
              colors: (sisData.darkMode)
                  ? [Colors.black, Colors.black, Colors.blueGrey]
                  : [
                      NeumorphicColors.background,
                      NeumorphicColors.background,
                      Colors.white,
                      Colors.white
                    ])),
      padding: EdgeInsets.only(
          left: width * 0.05,
          right: width * 0.05,
          top: height * 0.06,
          bottom: height * 0.13),
      child: Center(
        child: SingleChildScrollView(
          physics: const BouncingScrollPhysics(),
          child: Column(
            children: [
              Text(
                "Attendance Info",
                style: TextStyle(
                    color: sisData.darkMode ? Colors.white : Colors.black,
                    fontSize: 40,
                    fontFamily: 'Comfortaa'),
              ),
              AttendanceGraph(
                  height: height,
                  width: width,
                  attendances: sisData.attendances),
              ...sisData.attendances
                  .map((e) => Padding(
                        //map
                        padding: const EdgeInsets.all(8.0),
                        child: NeumorphicButton(
                          padding: EdgeInsets.only(
                              top: height * 0.015,
                              bottom: height * 0.015,
                              left: width * 0.025,
                              right: width * 0.01),
                          onPressed: () {
                            List allDateList = [];
                            var minAbsentDate = calcMinDate(e.absentDates);
                            var maxAbsentDate = calcMaxDate(e.absentDates);
                            var minPresentDate = calcMinDate(
                                e.presentDates); //max and min date variables
                            var maxPresentDate = calcMaxDate(e.presentDates);
                            var fromDate =
                                calcFromDate(minPresentDate, minAbsentDate);
                            var toDate =
                                calcToDate(maxPresentDate, maxAbsentDate);

                            Navigator.of(context).push(MaterialPageRoute(
                                builder: (ctx) =>
                                    AttendanceDetails(attendanceDetails: e)));
                          },
                          style: NeumorphicStyle(
                              shadowLightColor:
                                  sisData.darkMode ? Colors.white : null,
                              shadowDarkColor: sisData.darkMode
                                  ? NeumorphicColors.background
                                  : null,
                              color: sisData.darkMode
                                  ? Color.fromARGB(1, 77, 74, 74)
                                  : NeumorphicColors.background,
                              depth: 3,
                              boxShape: NeumorphicBoxShape.roundRect(
                                  BorderRadius.circular(20))),
                          child: ListTile(
                            title: Text(
                              e.subjectName,
                              style: TextStyle(
                                  color: sisData.darkMode
                                      ? Colors.white
                                      : Colors.black,
                                  fontSize: width * 0.045,
                                  fontFamily: 'Comfortaa'),
                            ),
                            subtitle: Text(
                              "(${e.code})",
                              style: TextStyle(
                                  color: sisData.darkMode
                                      ? Colors.white
                                      : Colors.black,
                                  fontSize: width * 0.045,
                                  fontFamily: 'Comfortaa'),
                            ),
                            trailing: Text(
                              e.percentage,
                              style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: sisData.darkMode
                                      ? Colors.white
                                      : Colors.black,
                                  fontSize: width * 0.055,
                                  fontFamily: 'Comfortaa'),
                              textAlign: TextAlign.end,
                            ),
                          ),
                        ),
                      ))
                  .toList()
            ],
          ),
        ),
      ),
    );
  }
}
