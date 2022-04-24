import 'package:flutter/material.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Classes/Attendance.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';

class AttendanceDetails extends StatelessWidget {
  final Attendance attendanceDetails;

  const AttendanceDetails({Key? key, required this.attendanceDetails})
      : super(key: key);

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

  bool isPresntInDates(List<ClassDay> dates, DateTime date) {
    for (int i = 0; i < dates.length; i++) {
      if (dates[i].date.isAtSameMomentAs(date)) {
        return true;
      }
    }
    return false;
  }

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    List<int> allDateList = [];
    var minAbsentDate = calcMinDate(attendanceDetails.absentDates);
    var maxAbsentDate = calcMaxDate(attendanceDetails.absentDates);
    var minPresentDate = calcMinDate(
        attendanceDetails.presentDates); //max and min date variables
    var maxPresentDate = calcMaxDate(attendanceDetails.presentDates);

    var fromDate = calcFromDate(minPresentDate, minAbsentDate);
    var toDate = calcToDate(maxPresentDate, maxAbsentDate);
    // ignore: avoid_print
    var dateDiff = toDate.difference(fromDate).inDays;
    var startDay = DateFormat('EEEE').format(fromDate);
    //DateTime.now()
    int k = 0;
    switch (startDay.toString()) {
      case 'Monday':
        print("mon it is");
        break;
      case 'Tuesday':
        k = 1;
        print("tue it is");
        break;
      case 'Wednesday':
        k = 2;
        print("wed it is");
        break;
      case 'Thursday':
        k = 3;
        print("thur it is");
        break;
      case 'Friday':
        k = 4;
        print("fri it is");
        break;
      case 'Saturday':
        k = 5;
        print("sat it is");
        break;
      case 'Sunday':
        k = 6;
        print('sun it is');
    }
    for (int i = 0; i < k; i++) {
      allDateList.add(-1);
    }
    for (int i = 0; i < dateDiff.toInt(); i++) {
      //adding colors to the allDateList
      if (isPresntInDates(attendanceDetails.presentDates, fromDate)) {
        allDateList.add(1);
      } else if (isPresntInDates(attendanceDetails.absentDates, fromDate)) {
        allDateList.add(0);
      } else {
        allDateList.add(-1);
      }
      fromDate = fromDate.add(const Duration(days: 1));
    }
    print(dateDiff);
    // DateTime i = fromDate;
    // for (; i != toDate; i.add(Duration(days: 1))) {
    //   // ignore: iterable_contains_unrelated_type
    //   if (isPresntInDates(attendanceDetails.absentDates, i)) {
    //     print("it works");
    //   }

    // }
    Color getColor(int number) {
      if (number == 1) {
        return Colors.lightGreen;
      }
      if (number == 0) {
        return Colors.red;
      }
      return Colors.grey;
    }

    Widget buildNumber(int number) => Neumorphic(
          style: NeumorphicStyle(color: getColor(number)),
          child: Center(child: Container()),
        );

    Widget buildGridView() => GridView.builder(
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 7,
            mainAxisSpacing: 20,
            crossAxisSpacing: 15,
            mainAxisExtent: 12,
          ),
          primary: true,
          shrinkWrap: true,
          itemCount: allDateList.length,
          itemBuilder: (context, index) {
            final item = allDateList[index];
            return buildNumber(item);
          },
        );
    return Scaffold(
      // appBar: AppBar(title: const Text("Attendance details")),
      backgroundColor: NeumorphicColors.background,
      body: Container(
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
        margin: const EdgeInsets.all(8),
        // alignment: Alignment.center,
        // color: Colors.grey,
        child: Padding(
          padding: EdgeInsets.only(
            left: width * 0.05,
            right: width * 0.05,
            top: height * 0.06,
          ),
          // padding: EdgeInsets.only(
          //     left: width * 0.05,
          //     right: width * 0.05,
          //     top: height * 0.06,
          //     bottom: height * 0.25),

          child: Column(
            children: [
              Padding(
                padding: EdgeInsets.only(bottom: height * 0.04),
                child: Align(
                  alignment: Alignment.topLeft,
                  child: Text(
                    "Attendance Details",
                    textAlign: TextAlign.left,
                    style: TextStyle(
                        color: sisData.darkMode ? Colors.white : Colors.black,
                        fontSize: 40,
                        fontFamily: 'Comfortaa'),
                  ),
                ),
              ),
              Text(
                "${attendanceDetails.subjectName} (${attendanceDetails.code})",
                style: TextStyle(
                    color: sisData.darkMode ? Colors.white : Colors.black,
                    fontSize: MediaQuery.of(context).size.width * 0.05,
                    fontFamily: 'Comfortaa'),
              ),
              Padding(
                padding: EdgeInsets.symmetric(
                  vertical: MediaQuery.of(context).size.height * 0.04,
                  horizontal: MediaQuery.of(context).size.width * 0.04,
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: const [
                    Text(
                      "Mon",
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                      ),
                      textAlign: TextAlign.left,
                    ),
                    Text(
                      "Tue",
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                      ),
                      textAlign: TextAlign.left,
                    ),
                    Text(
                      "Wed",
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                      ),
                      textAlign: TextAlign.left,
                    ),
                    Text(
                      "Thur",
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                      ),
                      textAlign: TextAlign.left,
                    ),
                    Text(
                      "Fri",
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                      ),
                      textAlign: TextAlign.left,
                    ),
                    Text(
                      "Sat",
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                      ),
                      textAlign: TextAlign.left,
                    ),
                    Text(
                      "Sun",
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                      ),
                      textAlign: TextAlign.left,
                    ),
                  ],
                ),
              ),
              Expanded(
                child: buildGridView(),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
