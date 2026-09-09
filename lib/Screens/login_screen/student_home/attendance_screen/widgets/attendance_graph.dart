import 'package:flutter_neumorphic_plus/flutter_neumorphic.dart';
import 'package:official_connect/Classes/attendance.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Providers/themes.dart';
import 'package:provider/provider.dart';

class AttendanceGraph extends StatelessWidget {
  const AttendanceGraph({
    super.key,
    required this.height,
    required this.width,
    required this.attendances,
  });

  final double height, width;
  final List<Attendance> attendances;

  int _percentage(Attendance attendance) =>
      int.tryParse(attendance.percentage.replaceAll(RegExp(r'[^0-9]'), '')) ??
      0;

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    final values = attendances.map(_percentage).toList();
    final average = values.isEmpty
        ? 0
        : (values.reduce((first, second) => first + second) / values.length)
            .round();
    final belowTarget = values.where((value) => value < 75).length;
    final meetsTarget = average >= 75;
    final accent =
        meetsTarget ? const Color(0xff288b57) : const Color(0xffba3237);
    final statusAccent =
        belowTarget == 0 ? const Color(0xff288b57) : const Color(0xffba3237);

    return Padding(
      padding: const EdgeInsets.fromLTRB(4, 24, 4, 14),
      child: Neumorphic(
        style: CustomTheme.neumorphicStyle(context),
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text(
                  '$average%',
                  style: CustomTheme.titleStyle(context).copyWith(
                    color: accent,
                    fontSize: 34,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(width: 10),
                Padding(
                  padding: const EdgeInsets.only(bottom: 5),
                  child: Text(
                    'average attendance',
                    style: CustomTheme.textStyle(context),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            ClipRRect(
              borderRadius: BorderRadius.circular(12),
              child: LinearProgressIndicator(
                value: (average / 100).clamp(0, 1),
                minHeight: 10,
                color: accent,
                backgroundColor:
                    sisData.darkMode ? Colors.white12 : Colors.black12,
              ),
            ),
            const SizedBox(height: 14),
            Row(
              children: [
                Icon(
                  belowTarget == 0
                      ? Icons.check_circle_outline
                      : Icons.warning_amber,
                  size: 18,
                  color: statusAccent,
                ),
                const SizedBox(width: 7),
                Expanded(
                  child: Text(
                    belowTarget == 0
                        ? 'All ${attendances.length} subjects are at or above 75%.'
                        : '$belowTarget of ${attendances.length} subjects below 75%.',
                    style: CustomTheme.textStyle(context).copyWith(
                      color: sisData.darkMode ? Colors.white70 : Colors.black54,
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
