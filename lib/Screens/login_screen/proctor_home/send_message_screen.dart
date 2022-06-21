import 'package:flutter/material.dart';

class SendMessageScreen extends StatefulWidget {
  final List<String> usns;
  const SendMessageScreen({Key? key, required this.usns}) : super(key: key);

  @override
  State<SendMessageScreen> createState() => _SendMessageScreenState();
}

class _SendMessageScreenState extends State<SendMessageScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("send message"),
      ),
      body: Center(
        child: Column(
          children: widget.usns.map((e) => Text(e)).toList(),
        ),
      ),
    );
  }
}
