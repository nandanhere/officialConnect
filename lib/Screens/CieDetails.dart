import 'package:flutter/material.dart';
import 'package:official_connect/Classes/Marks.dart';
import 'package:official_connect/Widgets/CieDetailsGraph.dart';

class CieDetails extends StatelessWidget {
  final Marks subjectDetails;
  const CieDetails({Key? key, required this.subjectDetails}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final averages = subjectDetails.averages;
    return Scaffold(
      appBar: AppBar(
        foregroundColor: const Color(0xFF852528),
        backgroundColor: Colors.white,
        title: Text(
          "Cie details",
          style: TextStyle(
              color: const Color(0xFF852528),
              fontSize: MediaQuery.of(context).size.width * 0.06,
              fontFamily: 'Comfortaa'),
        ),
      ),
      body: Center(
        child: SingleChildScrollView(
          child: Column(
            children: [
              Text(
                subjectDetails.subjectName,
                style: TextStyle(
                    color: Colors.black,
                    fontSize: MediaQuery.of(context).size.width * 0.05,
                    fontFamily: 'Comfortaa'),
              ),
              CieDetailsGraph(subjectDetails: subjectDetails),
              Text("average score of class in :"),
              for (String k in averages.keys)
                Text(k + ":" + averages[k].toString()),
            ],
          ),
        ),
      ),
    );
  }
}
