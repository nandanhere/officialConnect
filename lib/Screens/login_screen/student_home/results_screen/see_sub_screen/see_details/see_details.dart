import 'package:flutter_neumorphic_plus/flutter_neumorphic.dart';
import 'package:official_connect/Classes/previous_result.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Providers/themes.dart';
import 'package:official_connect/Screens/login_screen/student_home/results_screen/widgets/marks_card.dart';
import 'package:provider/provider.dart';

class ResultsDetails extends StatelessWidget {
  const ResultsDetails({
    super.key,
    required this.previousResult,
    this.contextLabel,
    this.onRefresh,
  });

  final PreviousResult previousResult;
  final String? contextLabel;
  final VoidCallback? onRefresh;

  String _cleanMetric(Object? value, String label) {
    final cleaned = value
        .toString()
        .replaceFirst(RegExp('^$label\\s*:\\s*', caseSensitive: false), '')
        .trim();
    return cleaned.isEmpty || cleaned.toLowerCase() == 'null' ? '–' : cleaned;
  }

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    final dark = sisData.darkMode;
    final term = previousResult.term.toString().trim();
    final termLower = term.toLowerCase();
    final isBackLog = termLower.contains('back');
    final isSupplementary = termLower.contains('supplementary');
    final semester = previousResult.semesterNumber.toString().trim();
    final heading = contextLabel ??
        (isBackLog
            ? 'Backlog result'
            : isSupplementary
                ? 'Supplementary result'
                : semester.isNotEmpty
                    ? 'Semester $semester'
                    : 'Semester result');
    final sgpa = _cleanMetric(previousResult.sgpa, 'SGPA');
    final rawCgpa = _cleanMetric(previousResult.cgpa, 'CGPA');
    final cgpa = rawCgpa == '–' ? sgpa : rawCgpa;
    final foreground = dark ? Colors.white : const Color(0xff1e2629);
    final secondary = dark ? Colors.white60 : Colors.black54;

    return Scaffold(
      backgroundColor: dark ? Colors.black : NeumorphicColors.background,
      body: SafeArea(
        child: SingleChildScrollView(
          physics: const BouncingScrollPhysics(),
          padding: const EdgeInsets.fromLTRB(14, 6, 14, 24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Row(
                children: [
                  IconButton(
                    tooltip: 'Back',
                    onPressed: () => Navigator.of(context).pop(),
                    icon: Icon(Icons.arrow_back_ios_new_rounded,
                        size: 18, color: foreground),
                  ),
                  Expanded(
                    child: Column(
                      children: [
                        Text(
                          heading,
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          textAlign: TextAlign.center,
                          style: CustomTheme.buttonTrailing(context).copyWith(
                            color: foreground,
                            fontSize: 21,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                        if (term.isNotEmpty && term != heading)
                          Padding(
                            padding: const EdgeInsets.only(top: 2),
                            child: Text(
                              term,
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              textAlign: TextAlign.center,
                              style: CustomTheme.textStyle(context).copyWith(
                                color: secondary,
                                fontSize: 12,
                              ),
                            ),
                          ),
                      ],
                    ),
                  ),
                  SizedBox(
                    width: 48,
                    child: onRefresh == null
                        ? null
                        : IconButton(
                            tooltip: 'Check for a newer result',
                            onPressed: onRefresh,
                            icon: const Icon(
                              Icons.refresh_rounded,
                              color: Color(0xffba3237),
                            ),
                          ),
                  ),
                ],
              ),
              const SizedBox(height: 14),
              if (!isBackLog)
                Container(
                  decoration: BoxDecoration(
                    color: dark
                        ? const Color(0xff222526)
                        : const Color(0xffdfe8ea),
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(
                      color: dark ? Colors.white10 : const Color(0x14243238),
                    ),
                  ),
                  padding: const EdgeInsets.symmetric(vertical: 13),
                  child: Row(
                    children: [
                      _SummaryMetric(label: 'SGPA', value: sgpa),
                      _SummaryMetric(label: 'CGPA', value: cgpa),
                      _SummaryMetric(
                        label: 'REGISTERED',
                        value: _cleanMetric(
                          previousResult.creditsRegistered,
                          'Credits Registered',
                        ),
                      ),
                      _SummaryMetric(
                        label: 'EARNED',
                        value: _cleanMetric(
                          previousResult.creditsEarned,
                          'Credits Earned',
                        ),
                        last: true,
                      ),
                    ],
                  ),
                ),
              MarksCard(
                subjects: previousResult.results,
                isBackLog: isBackLog,
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _SummaryMetric extends StatelessWidget {
  const _SummaryMetric({
    required this.label,
    required this.value,
    this.last = false,
  });

  final String label;
  final String value;
  final bool last;

  @override
  Widget build(BuildContext context) {
    final dark = Provider.of<SisData>(context, listen: false).darkMode;
    final foreground = dark ? Colors.white : const Color(0xff1e2629);
    return Expanded(
      child: Container(
        decoration: BoxDecoration(
          border: last
              ? null
              : Border(
                  right: BorderSide(
                    color: dark ? Colors.white12 : Colors.black12,
                  ),
                ),
        ),
        child: Column(
          children: [
            Text(
              label,
              maxLines: 1,
              style: CustomTheme.textStyle(context).copyWith(
                color: foreground.withValues(alpha: 0.55),
                fontSize: 8.5,
                fontWeight: FontWeight.w700,
                letterSpacing: 0.25,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              value,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: CustomTheme.buttonTitle(context).copyWith(
                color: foreground,
                fontSize: 15,
                fontWeight: FontWeight.w700,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
