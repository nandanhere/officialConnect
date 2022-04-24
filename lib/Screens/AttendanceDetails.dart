import 'package:flutter/material.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:official_connect/Classes/Attendance.dart';

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

    for (int i = 0; i < dateDiff.toInt(); i++) {
      if (isPresntInDates(attendanceDetails.presentDates, fromDate)) {
        allDateList.add(1);
      } else if (isPresntInDates(attendanceDetails.absentDates, fromDate)) {
        allDateList.add(0);
      } else {
        allDateList.add(-1);
      }
      fromDate = fromDate.add(const Duration(days: 1));
    }

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
          child: Center(
            child: Container()
          ),
        );

    // ignore: dead_code
    Widget buildGridView() => GridView.builder(
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 7,
              mainAxisSpacing: 20,
              crossAxisSpacing: 15,
              mainAxisExtent: 12),
          itemCount: allDateList.length,
          itemBuilder: (context, index) {
            final item = allDateList[index];
            return buildNumber(item);
          },
        );
    return Scaffold(
      appBar: AppBar(title: const Text("Attendance details")),
      backgroundColor: NeumorphicColors.background,
      body: Container(
        margin: EdgeInsets.all(8),
        alignment: Alignment.center,
        // color: Colors.grey,
        child:
            // Column(
            //   children: [

            Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
          children: [
              Row(
                
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: const [
                  Text("Mon" , style: TextStyle(fontWeight: FontWeight.bold ,), textAlign: TextAlign.left,),
                  Text("Tue" , style: TextStyle(fontWeight: FontWeight.bold ,), textAlign: TextAlign.left,),
                  Text("Wed",style: TextStyle(fontWeight: FontWeight.bold ,), textAlign: TextAlign.left,),
                  Text("Thur",style: TextStyle(fontWeight: FontWeight.bold ,), textAlign: TextAlign.left,),
                  Text("Fri",style: TextStyle(fontWeight: FontWeight.bold ,), textAlign: TextAlign.left,),
                  Text("Sat",style: TextStyle(fontWeight: FontWeight.bold ,), textAlign: TextAlign.left,),
                  Text("Sun",style: TextStyle(fontWeight: FontWeight.bold ,), textAlign: TextAlign.left,),
                ],
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
