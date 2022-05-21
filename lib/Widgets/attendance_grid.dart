import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:intl/intl.dart';
import 'package:official_connect/Classes/attendance.dart';
import 'package:provider/provider.dart';

import '../Providers/sisdata.dart';

class AttendanceGrid extends StatelessWidget {
  final Attendance attendance;
  const AttendanceGrid({Key? key, required this.attendance}) : super(key: key);

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
    final size = MediaQuery.of(context).size;
    final width = size.width;
    final height = size.height;
    List<List> allDateList = [];
    var minAbsentDate = (attendance.absentDates.isNotEmpty)
        ? calcMinDate(attendance.absentDates)
        : DateTime.now();
    var maxAbsentDate = (attendance.absentDates.isNotEmpty)
        ? calcMaxDate(attendance.absentDates)
        : DateTime(2000);
    var minPresentDate = (attendance.presentDates.isNotEmpty)
        ? calcMinDate(attendance.presentDates)
        : DateTime.now(); //max and min date variables
    var maxPresentDate = (attendance.presentDates.isNotEmpty)
        ? calcMaxDate(attendance.presentDates)
        : DateTime(2000);

    var fromDate = calcFromDate(minPresentDate, minAbsentDate);
    var toDate = calcToDate(maxPresentDate, maxAbsentDate);
    // ignore: avoid_print
    var dateDiff = toDate.difference(fromDate).inDays;
    var startDay = DateFormat('EEEE').format(fromDate);
    //DateTime.now()
    int k = 0;
    switch (startDay.toString()) {
      case 'Monday':
        break;
      case 'Tuesday':
        k = 1;

        break;
      case 'Wednesday':
        k = 2;

        break;
      case 'Thursday':
        k = 3;

        break;
      case 'Friday':
        k = 4;

        break;
      case 'Saturday':
        k = 5;

        break;
      case 'Sunday':
        k = 6;
    }
    for (int i = 0; i < k; i++) {
      allDateList.add([-1]);
    }
    for (int i = 0; i < dateDiff.toInt(); i++) {
      //adding colors to the allDateList
      if (isPresntInDates(attendance.presentDates, fromDate)) {
        allDateList.add([
          1,
          fromDate,
          attendance.presentDates
              .where((element) => element.date == fromDate)
              .first
              .time
        ]);
      } else if (isPresntInDates(attendance.absentDates, fromDate)) {
        allDateList.add([
          0,
          fromDate,
          attendance.absentDates
              .where((element) => element.date == fromDate)
              .first
              .time
        ]);
      } else {
        allDateList.add([-1]);
      }
      fromDate = fromDate.add(const Duration(days: 1));
    }

    // DateTime i = fromDate;
    // for (; i != toDate; i.add(Duration(days: 1))) {
    //   // ignore: iterable_contains_unrelated_type
    //   if (isPresntInDates(attendance.absentDates, i)) {
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

    String toolTipMessage(List<dynamic> day) {
      var value = day[0];
      if (value == -1) {
        return "No class";
      } else {
        var formatter = DateFormat('dd-MM-yyyy');
        var date = formatter.format(day[1]);
        var time = day[2];
        if (value == 1) {
          return "$date, $time";
        } else if (value == 0) {
          return "$date, $time";
        } else {
          return "Not available";
        }
      }
    }

    Widget buildNumber(List day) => Tooltip(
          message: toolTipMessage(day),
          triggerMode: TooltipTriggerMode.tap,
          child: Neumorphic(
            // day is a list in which each element is [colornumber, date, time]
            style: NeumorphicStyle(
              color: getColor(day[0]),
              disableDepth: true,
            ),
            child: const Center(
                child: SizedBox(
              width: 50,
              height: 50,
            )),
          ),
        );

    Widget buildGridView() => GridView.builder(
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            childAspectRatio: 2.5,
            crossAxisCount: 7,
            mainAxisSpacing: 22.5,
            crossAxisSpacing: 17,
            // mainAxisExtent: 12,
          ),
          itemCount: allDateList.length,
          physics: const ScrollPhysics(),
          itemBuilder: (context, index) {
            final item = allDateList[index];
            return buildNumber(item);
          },
        );
    // ignore: todo
    final sisData = Provider.of<SisData>(context);

    return SizedBox(
      width: width,
      height: height,
      child: Padding(
        padding: EdgeInsets.symmetric(
          vertical: MediaQuery.of(context).size.height * 0.04,
          horizontal: MediaQuery.of(context).size.width * 0.04,
        ),
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    "Mon",
                    style: TextStyle(
                      color: sisData.darkMode ? Colors.white : Colors.black,
                      fontWeight: FontWeight.bold,
                    ),
                    textAlign: TextAlign.left,
                  ),
                  Text(
                    "Tue",
                    style: TextStyle(
                      color: sisData.darkMode ? Colors.white : Colors.black,
                      fontWeight: FontWeight.bold,
                    ),
                    textAlign: TextAlign.left,
                  ),
                  Text(
                    "Wed",
                    style: TextStyle(
                      color: sisData.darkMode ? Colors.white : Colors.black,
                      fontWeight: FontWeight.bold,
                    ),
                    textAlign: TextAlign.left,
                  ),
                  Text(
                    "Thur",
                    style: TextStyle(
                      color: sisData.darkMode ? Colors.white : Colors.black,
                      fontWeight: FontWeight.bold,
                    ),
                    textAlign: TextAlign.left,
                  ),
                  Text(
                    "Fri",
                    style: TextStyle(
                      color: sisData.darkMode ? Colors.white : Colors.black,
                      fontWeight: FontWeight.bold,
                    ),
                    textAlign: TextAlign.left,
                  ),
                  Text(
                    "Sat",
                    style: TextStyle(
                      color: sisData.darkMode ? Colors.white : Colors.black,
                      fontWeight: FontWeight.bold,
                    ),
                    textAlign: TextAlign.left,
                  ),
                  Text(
                    "Sun",
                    style: TextStyle(
                      color: sisData.darkMode ? Colors.white : Colors.black,
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
    );
  }
}
