class Marks {
  final String a1, a2, finalCie, t1, t2, subjectName;
  final Map<String, dynamic> averages;
  Marks({
    required this.subjectName,
    required this.a1,
    required this.a2,
    required this.finalCie,
    required this.t1,
    required this.t2,
    required this.averages,
  });
  static List<Marks> getList(List<dynamic> data) {
    final list = data
        .map((e) => Marks(
            averages: e['class_average'],
            subjectName: e['name'],
            a1: e['a1'],
            a2: e['a2'],
            finalCie: e['final cie'],
            t1: e['t1'],
            t2: e['t2']))
        .toList();
    print(list[0].averages);
    final reg = RegExp(r".*\((.*)\)");
    list.sort((a, b) {
      if (reg.hasMatch(a.subjectName) && reg.hasMatch(b.subjectName)) {
        return reg
            .firstMatch(a.subjectName)!
            .group(1)!
            .compareTo(reg.firstMatch(b.subjectName)!.group(1)!);
      }
      return 0;
    });
    return list;
  }
}
