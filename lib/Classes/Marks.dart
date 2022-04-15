class Marks {
  final String a1, a2, finalCie, t1, t2, subjectName;

  Marks(
      {required this.subjectName,
      required this.a1,
      required this.a2,
      required this.finalCie,
      required this.t1,
      required this.t2});
  static List<Marks> getList(List<dynamic> data) {
    return data
        .map((e) => Marks(
            subjectName: e['name'],
            a1: e['a1'],
            a2: e['a2'],
            finalCie: e['final cie'],
            t1: e['t1'],
            t2: e['t2']))
        .toList();
  }
}
