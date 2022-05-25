import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:intl/intl.dart';
import 'package:official_connect/Providers/Themes.dart';
import 'package:syncfusion_flutter_calendar/calendar.dart';
import 'package:official_connect/Classes/attendance.dart';
import 'package:provider/provider.dart';
import '../Providers/Themes.dart';
import '../Providers/sisdata.dart';

extension DateOnlyCompare on DateTime {
  bool isSameDate(DateTime other) {
    return year == other.year && month == other.month && day == other.day;
  }
}

class AttendanceCalenderVersion extends StatelessWidget {
  final Attendance attendance;
  const AttendanceCalenderVersion({Key? key, required this.attendance})
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
    final size = MediaQuery.of(context).size;
    final height = size.height;
    final width = size.width;
    final sisData = Provider.of<SisData>(context);
    final textStyle = CustomTheme.textStyle(context);
    if (attendance.absentDates.isEmpty && attendance.presentDates.isEmpty) {
      return AutoSizeText(
        "No data has been uploaded as of now",
        style: CustomTheme.textStyle(context),
      );
    }
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
    var dateDiff = toDate.difference(fromDate).inDays;

    for (int i = 0; i < dateDiff.toInt(); i++) {
      //adding colors to the allDateList
      if (isPresntInDates(attendance.presentDates, fromDate)) {
        allDateList.add([
          1,
          DateTime(fromDate.year, fromDate.month, fromDate.day),
          fromDate.add(Duration(hours: 7)),
          attendance.presentDates
              .where((element) => element.date == fromDate)
              .first
              .time
        ]);
      } else if (isPresntInDates(attendance.absentDates, fromDate)) {
        allDateList.add([
          0,
          DateTime(fromDate.year, fromDate.month, fromDate.day),
          fromDate.add(Duration(hours: 7)),
          attendance.absentDates
              .where((element) => element.date == fromDate)
              .first
              .time
        ]);
      } else {
        allDateList
            .add([-1, DateTime(fromDate.year, fromDate.month, fromDate.day)]);
      }
      fromDate = fromDate.add(const Duration(days: 1));
    }

    Color getColor(int number) {
      if (number == 1) {
        return Colors.lightGreen;
      }
      if (number == 0) {
        return Colors.red;
      }
      return sisData.darkMode ? Colors.grey.shade800 : Colors.grey;
    }

    List<DataSource> _getSource() {
      List<DataSource> _dataSource = <DataSource>[];

      for (List data in allDateList) {
        if (data.length > 2) {
          DataSource newData =
              DataSource(data[3], data[1], data[2], getColor(data[0]), true);
          _dataSource.add(newData);
        } else {
          _dataSource
              .add(DataSource("No Class", data[1], data[1], Colors.grey, true));
        }
      }
      return _dataSource;
    }

    Color _getMonthCellBackgroundColor(DateTime date) {
      for (List givenDate in allDateList) {
        if (date.isAtSameMomentAs(givenDate[1])) {
          return getColor(givenDate[0]);
        }
      }
      if (date.isSameDate(DateTime.now())) return Colors.blue;
      return Colors.transparent;
    }

    return Container(
      height: height * 0.7,
      child: Padding(
        padding: EdgeInsets.symmetric(
          horizontal: MediaQuery.of(context).size.width * 0.04,
        ),
        child: SfCalendar(
          minDate: allDateList[0][1],
          maxDate: DateTime.now(),
          viewHeaderStyle: ViewHeaderStyle(
              dateTextStyle: textStyle, dayTextStyle: textStyle),
          headerStyle: CalendarHeaderStyle(textStyle: textStyle),
          cellBorderColor: sisData.darkMode ? Colors.white : Colors.black,
          view: CalendarView.month,
          dataSource: MeetingDataSource(_getSource()),
          monthViewSettings: MonthViewSettings(
              showTrailingAndLeadingDates: false,
              appointmentDisplayMode: MonthAppointmentDisplayMode.none,
              showAgenda: true,
              agendaItemHeight: height * 0.07),
          monthCellBuilder:
              (BuildContext buildContext, MonthCellDetails details) {
            final Color backgroundColor =
                _getMonthCellBackgroundColor(details.date);
            final Color defaultColor =
                Theme.of(context).brightness == Brightness.dark
                    ? Colors.black54
                    : Colors.white;
            return Container(
              decoration: BoxDecoration(
                  color: backgroundColor == Colors.blue
                      ? Colors.transparent
                      : backgroundColor,
                  border:
                      Border.all(color: defaultColor, width: 0.002 * width)),
              child: Center(
                child: Container(
                  padding: const EdgeInsets.all(4),
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: backgroundColor,
                  ),
                  child: Text(
                    details.date.day.toString(),
                    style: textStyle,
                  ),
                ),
              ),
            );
          },
          showNavigationArrow: true,
        ),
      ),
    );
  }
}

class MeetingDataSource extends CalendarDataSource {
  /// Creates a meeting data source, which used to set the appointment
  /// collection to the calendar
  MeetingDataSource(List<DataSource> source) {
    appointments = source;
  }

  @override
  DateTime getStartTime(int index) {
    return appointments![index].from;
  }

  @override
  DateTime getEndTime(int index) {
    return appointments![index].to;
  }

  @override
  String getSubject(int index) {
    return appointments![index].eventName;
  }

  @override
  Color getColor(int index) {
    return appointments![index].background;
  }

  @override
  bool isAllDay(int index) {
    return appointments![index].isAllDay;
  }
}

class DataSource {
  DataSource(
      this.eventName, this.from, this.to, this.background, this.isAllDay);
  String eventName;
  DateTime? from;
  DateTime? to;
  Color background;
  bool isAllDay;
  @override
  String toString() {
    // TODO: implement toString
    return "${this.eventName},${this.from},${this.to},${this.background},${this.isAllDay}";
  }
}
