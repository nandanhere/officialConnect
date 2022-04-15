class FeesData {
  final String academicYear,
      amountPaid,
      challanNumber,
      chequeNumber,
      date,
      mode,
      yearNumber,
      paidAt,
      reciept;
  FeesData(
      {required this.academicYear,
      required this.amountPaid,
      required this.challanNumber,
      required this.chequeNumber,
      required this.date,
      required this.mode,
      required this.yearNumber,
      required this.paidAt,
      required this.reciept});
  static List<FeesData> getList(List<dynamic> data) {
    return data
        .map((e) => FeesData(
            academicYear: e['Academic Year'],
            amountPaid: e['Amount Paid'],
            challanNumber: e['Challan No'],
            chequeNumber: e['Cheque/DD No'],
            date: e['Date'],
            mode: e['Mode'],
            yearNumber: e['Paid for Year'],
            paidAt: e['Pay At'],
            reciept: e['Receipt']))
        .toList();
  }
}
