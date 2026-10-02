class ProctorMessage {
  final String date, from, desc;

  ProctorMessage(this.date, this.from, this.desc);
  static List<ProctorMessage> getMessageList(List<dynamic> data) {
    return data
        .map((e) => ProctorMessage(e['date']!, e['sender']!, e['desc']!))
        .toList();
  }
}

class SisProctorData {
  final List<ProctorMessage> messages;
  final String name, phone, email, branch;

  SisProctorData(this.messages, this.name, this.phone, this.email, this.branch);
  static SisProctorData proctorData(dynamic data) {
    // Past error/disabled syncs persisted proctorship as []; tolerate legacy
    // shapes so opening the proctor screen from an old cache cannot crash.
    final map = data is Map
        ? Map<String, dynamic>.from(data)
        : <String, dynamic>{};
    final notes = map['proctorial_notes'];
    return SisProctorData(
      ProctorMessage.getMessageList(notes is List ? notes : <dynamic>[]),
      map['proctor_name']?.toString() ?? 'Not given',
      map['phone']?.toString() ?? 'Not given',
      map['email']?.toString() ?? 'Not given',
      map['branch']?.toString() ?? 'Not given',
    );
  }
}
