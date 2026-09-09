import 'package:flutter_neumorphic_plus/flutter_neumorphic.dart';
import 'package:official_connect/Classes/previous_result.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Providers/themes.dart';
import 'package:provider/provider.dart';

class MarksCard extends StatelessWidget {
  const MarksCard({
    super.key,
    required this.subjects,
    required this.isBackLog,
  });

  final bool isBackLog;
  final List<Subject> subjects;

  String _display(Object? value) {
    final text = value?.toString().trim() ?? '';
    return text.isEmpty || text.toLowerCase() == 'null' ? '–' : text;
  }

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    final dark = sisData.darkMode;
    final border = dark ? Colors.white12 : const Color(0x1f243238);
    final header = dark ? const Color(0xff24282a) : const Color(0xffdce5e7);
    final alternate = dark ? const Color(0xff151718) : const Color(0xfff4f7f8);
    final primary = dark ? Colors.white : const Color(0xff1e2629);
    final secondary = dark ? Colors.white60 : Colors.black54;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(4, 14, 4, 9),
          child: Text(
            '${subjects.length} subjects',
            style: CustomTheme.textStyle(context).copyWith(color: secondary),
          ),
        ),
        ClipRRect(
          borderRadius: BorderRadius.circular(12),
          child: DecoratedBox(
            decoration: BoxDecoration(
              border: Border.all(color: border),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Table(
              columnWidths: const {
                0: FlexColumnWidth(2.9),
                1: FlexColumnWidth(0.85),
                2: FlexColumnWidth(0.9),
              },
              border: TableBorder(
                horizontalInside: BorderSide(color: border),
                verticalInside: BorderSide(color: border),
              ),
              defaultVerticalAlignment: TableCellVerticalAlignment.middle,
              children: [
                TableRow(
                  decoration: BoxDecoration(color: header),
                  children: [
                    _HeaderCell(label: 'Course', color: primary),
                    _HeaderCell(
                      label: isBackLog ? 'Credits' : 'Credits\nE / R',
                      color: primary,
                      centered: true,
                    ),
                    _HeaderCell(
                        label: 'Result', color: primary, centered: true),
                  ],
                ),
                ...subjects.indexed.map((entry) {
                  final index = entry.$1;
                  final subject = entry.$2;
                  final grade = _display(subject.grade);
                  final gpa = _display(subject.gpa);
                  return TableRow(
                    decoration: BoxDecoration(
                      color: index.isOdd ? alternate : Colors.transparent,
                    ),
                    children: [
                      Padding(
                        padding: const EdgeInsets.fromLTRB(10, 10, 8, 10),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              _display(subject.courseCode),
                              style: CustomTheme.textStyle(context).copyWith(
                                color: const Color(0xffba3237),
                                fontSize: 11.5,
                                fontWeight: FontWeight.w700,
                              ),
                            ),
                            const SizedBox(height: 3),
                            Text(
                              _display(subject.subjectName),
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                              style: CustomTheme.buttonTitle(context).copyWith(
                                color: primary,
                                fontSize: 13,
                                fontWeight: FontWeight.w600,
                                height: 1.25,
                              ),
                            ),
                          ],
                        ),
                      ),
                      _BodyCell(
                        primary: isBackLog
                            ? _display(subject.creditsRegistered)
                            : '${_display(subject.creditsEarned)} / ${_display(subject.creditsRegistered)}',
                        color: primary,
                      ),
                      _BodyCell(
                        primary: grade,
                        secondary: isBackLog
                            ? 'Attempts $gpa'
                            : gpa == '–'
                                ? null
                                : 'GPA $gpa',
                        color: primary,
                      ),
                    ],
                  );
                }),
              ],
            ),
          ),
        ),
        const SizedBox(height: 28),
      ],
    );
  }
}

class _HeaderCell extends StatelessWidget {
  const _HeaderCell({
    required this.label,
    required this.color,
    this.centered = false,
  });

  final String label;
  final Color color;
  final bool centered;

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 9),
        child: Text(
          label,
          textAlign: centered ? TextAlign.center : TextAlign.left,
          style: CustomTheme.textStyle(context).copyWith(
            color: color,
            fontSize: 11.5,
            fontWeight: FontWeight.w700,
            height: 1.15,
          ),
        ),
      );
}

class _BodyCell extends StatelessWidget {
  const _BodyCell({
    required this.primary,
    required this.color,
    this.secondary,
  });

  final String primary;
  final String? secondary;
  final Color color;

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 10),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              primary,
              textAlign: TextAlign.center,
              style: CustomTheme.buttonTitle(context).copyWith(
                color: color,
                fontSize: 13,
                fontWeight: FontWeight.w700,
              ),
            ),
            if (secondary != null) ...[
              const SizedBox(height: 2),
              Text(
                secondary!,
                textAlign: TextAlign.center,
                style: CustomTheme.textStyle(context).copyWith(
                  color: color.withValues(alpha: 0.58),
                  fontSize: 9.5,
                ),
              ),
            ],
          ],
        ),
      );
}
