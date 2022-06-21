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
  static SisProctorData proctorData(Map<String, dynamic> data) {
    return SisProctorData(
        ProctorMessage.getMessageList(data['proctorial_notes']),
        data['proctor_name'],
        data['phone'],
        data['email'],
        data['branch']);
  }
}
