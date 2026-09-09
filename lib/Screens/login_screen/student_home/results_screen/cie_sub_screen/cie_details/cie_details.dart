import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:official_connect/Classes/marks.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:provider/provider.dart';

/// Redesigned CIE details: a headline score summary plus per-component
/// progress bars with the class average shown alongside each score.
class CIEDetails extends StatelessWidget {
  final Marks subjectDetails;
  const CIEDetails({Key? key, required this.subjectDetails}) : super(key: key);

  static const _accent = Color(0xffba3237);

  /// Parses "26/30", "78%", "-" into (score, max). Null when not numeric.
  static (double, double)? _scoreMax(String raw) {
    final s = raw.trim();
    if (s.isEmpty || s == '-') return null;
    if (s.contains('%')) {
      final v = double.tryParse(s.replaceAll('%', '').trim());
      return v == null ? null : (v, 100);
    }
    final parts = s.split('/');
    final score = double.tryParse(parts.first.trim());
    if (score == null) return null;
    final max = parts.length > 1 ? double.tryParse(parts[1].trim()) : null;
    return (score, max ?? 50);
  }

  static String _fmt(double v) =>
      v == v.roundToDouble() ? v.toInt().toString() : v.toStringAsFixed(1);

  @override
  Widget build(BuildContext context) {
    final sisData = Provider.of<SisData>(context);
    final dark = sisData.darkMode;
    final size = MediaQuery.of(context).size;
    final width = size.width;

    final bg = dark ? const Color(0xff101114) : const Color(0xfff4f5f7);
    final card = dark ? const Color(0xff1b1d22) : Colors.white;
    final textMain = dark ? Colors.white : const Color(0xff1d1f24);
    final textSub = dark ? Colors.white54 : Colors.black54;

    final name = subjectDetails.subjectName;
    final code =
        RegExp(r'\(([^)]*)\)').firstMatch(name)?.group(1) ?? '';
    final title =
        code.isEmpty ? name : name.replaceAll(RegExp(r'\s*\([^)]*\)'), '').trim();

    final finalParsed = _scoreMax(subjectDetails.finalCie);
    final components = <_Component>[
      _Component('CIE 1', subjectDetails.t1, subjectDetails.avgt1),
      _Component('CIE 2', subjectDetails.t2, subjectDetails.avgt2),
      _Component('Assignment 1', subjectDetails.a1, subjectDetails.avga1),
      _Component('Assignment 2', subjectDetails.a2, subjectDetails.avga2),
    ];

    return Scaffold(
      backgroundColor: bg,
      body: SafeArea(
        child: SingleChildScrollView(
          physics: const BouncingScrollPhysics(),
          padding: EdgeInsets.symmetric(horizontal: width * 0.055),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Row(
                children: [
                  IconButton(
                    onPressed: () => Navigator.of(context).pop(),
                    icon: Icon(Icons.chevron_left, color: textMain, size: 30),
                  ),
                  Text(
                    'CIE Breakdown',
                    style: TextStyle(
                      fontFamily: 'Comfortaa',
                      fontWeight: FontWeight.w700,
                      fontSize: width * 0.055,
                      color: textMain,
                    ),
                  ),
                ],
              ),
              SizedBox(height: size.height * 0.015),

              // Subject header
              Text(
                title,
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontFamily: 'Comfortaa',
                  fontWeight: FontWeight.w600,
                  fontSize: width * 0.05,
                  color: textMain,
                  height: 1.3,
                ),
              ),
              if (code.isNotEmpty) ...[
                const SizedBox(height: 8),
                Center(
                  child: Container(
                    padding: const EdgeInsets.symmetric(
                        horizontal: 12, vertical: 4),
                    decoration: BoxDecoration(
                      color: _accent.withValues(alpha: dark ? 0.25 : 0.1),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Text(
                      code,
                      style: const TextStyle(
                        fontFamily: 'Comfortaa',
                        fontSize: 12.5,
                        fontWeight: FontWeight.w600,
                        color: _accent,
                        letterSpacing: 1.1,
                      ),
                    ),
                  ),
                ),
              ],
              SizedBox(height: size.height * 0.03),

              // Final score card
              Container(
                padding: const EdgeInsets.all(22),
                decoration: BoxDecoration(
                  color: card,
                  borderRadius: BorderRadius.circular(24),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withValues(alpha: dark ? 0.35 : 0.06),
                      blurRadius: 18,
                      offset: const Offset(0, 8),
                    ),
                  ],
                ),
                child: Row(
                  children: [
                    SizedBox(
                      width: 108,
                      height: 108,
                      child: CustomPaint(
                        painter: _ScoreRingPainter(
                          fraction: finalParsed == null
                              ? 0
                              : (finalParsed.$1 /
                                      (finalParsed.$2 == 0
                                          ? 1
                                          : finalParsed.$2))
                                  .clamp(0, 1),
                          color: _accent,
                          trackColor:
                              dark ? Colors.white12 : const Color(0xfff0e2e3),
                        ),
                        child: Center(
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Text(
                                finalParsed == null
                                    ? '-'
                                    : _fmt(finalParsed.$1),
                                style: TextStyle(
                                  fontFamily: 'Comfortaa',
                                  fontSize: 26,
                                  fontWeight: FontWeight.w700,
                                  color: textMain,
                                ),
                              ),
                              Text(
                                finalParsed == null
                                    ? 'no score'
                                    : 'of ${_fmt(finalParsed.$2)}',
                                style: TextStyle(
                                  fontFamily: 'Comfortaa',
                                  fontSize: 11.5,
                                  color: textSub,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 20),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Final CIE',
                            style: TextStyle(
                              fontFamily: 'Comfortaa',
                              fontSize: 15,
                              fontWeight: FontWeight.w700,
                              color: textMain,
                            ),
                          ),
                          const SizedBox(height: 6),
                          Text(
                            finalParsed == null
                                ? 'Marks are not published for this subject yet.'
                                : '${_fmt(finalParsed.$1 / (finalParsed.$2 == 0 ? 1 : finalParsed.$2) * 100)}% of the total internal marks.',
                            style: TextStyle(
                              fontFamily: 'Comfortaa',
                              fontSize: 12.5,
                              height: 1.45,
                              color: textSub,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              SizedBox(height: size.height * 0.025),

              // Component breakdown
              ...components.map(
                (c) => _ComponentCard(
                  component: c,
                  dark: dark,
                  card: card,
                  textMain: textMain,
                  textSub: textSub,
                  accent: _accent,
                ),
              ),
              SizedBox(height: size.height * 0.04),
            ],
          ),
        ),
      ),
    );
  }
}

class _Component {
  final String label;
  final String score;
  final String average;
  const _Component(this.label, this.score, this.average);
}

class _ComponentCard extends StatelessWidget {
  final _Component component;
  final bool dark;
  final Color card, textMain, textSub, accent;
  const _ComponentCard({
    required this.component,
    required this.dark,
    required this.card,
    required this.textMain,
    required this.textSub,
    required this.accent,
  });

  @override
  Widget build(BuildContext context) {
    final parsed = CIEDetails._scoreMax(component.score);
    final avgScore = double.tryParse(component.average.trim());
    final fraction = parsed == null
        ? 0.0
        : (parsed.$1 / (parsed.$2 == 0 ? 1 : parsed.$2)).clamp(0.0, 1.0);
    final avgFraction = (parsed != null && avgScore != null && parsed.$2 > 0)
        ? (avgScore / parsed.$2).clamp(0.0, 1.0)
        : null;
    final aboveAvg = avgFraction != null && fraction >= avgFraction;

    return Container(
      margin: const EdgeInsets.only(bottom: 14),
      padding: const EdgeInsets.fromLTRB(18, 16, 18, 18),
      decoration: BoxDecoration(
        color: card,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: dark ? 0.3 : 0.05),
            blurRadius: 14,
            offset: const Offset(0, 6),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                component.label,
                style: TextStyle(
                  fontFamily: 'Comfortaa',
                  fontWeight: FontWeight.w700,
                  fontSize: 14.5,
                  color: textMain,
                ),
              ),
              Text(
                parsed == null
                    ? component.score.trim().isEmpty ||
                            component.score.trim() == '-'
                        ? '—'
                        : component.score
                    : '${CIEDetails._fmt(parsed.$1)} / ${CIEDetails._fmt(parsed.$2)}',
                style: TextStyle(
                  fontFamily: 'Comfortaa',
                  fontWeight: FontWeight.w700,
                  fontSize: 14.5,
                  color: parsed == null ? textSub : accent,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          LayoutBuilder(
            builder: (context, constraints) {
              return Stack(
                children: [
                  Container(
                    height: 8,
                    decoration: BoxDecoration(
                      color: dark ? Colors.white12 : const Color(0xffeceff1),
                      borderRadius: BorderRadius.circular(6),
                    ),
                  ),
                  FractionallySizedBox(
                    widthFactor: fraction,
                    child: Container(
                      height: 8,
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          colors: [
                            accent,
                            accent.withValues(alpha: 0.65),
                          ],
                        ),
                        borderRadius: BorderRadius.circular(6),
                      ),
                    ),
                  ),
                  if (avgFraction != null)
                    Positioned(
                      left: math.max(
                          0.0,
                          constraints.maxWidth * avgFraction - 1.5),
                      top: -3,
                      child: Container(
                        width: 3,
                        height: 14,
                        decoration: BoxDecoration(
                          color: dark ? Colors.white70 : Colors.black45,
                          borderRadius: BorderRadius.circular(2),
                        ),
                      ),
                    ),
                ],
              );
            },
          ),
          const SizedBox(height: 10),
          Row(
            children: [
              Icon(
                aboveAvg ? Icons.trending_up : Icons.trending_flat,
                size: 16,
                color: aboveAvg
                    ? const Color(0xff2e9e5b)
                    : textSub,
              ),
              const SizedBox(width: 6),
              Text(
                avgScore == null
                    ? 'Class average not available'
                    : 'Class average ${CIEDetails._fmt(avgScore)}'
                        '${aboveAvg ? ' · above average' : ''}',
                style: TextStyle(
                  fontFamily: 'Comfortaa',
                  fontSize: 12,
                  color: aboveAvg ? const Color(0xff2e9e5b) : textSub,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _ScoreRingPainter extends CustomPainter {
  final double fraction;
  final Color color;
  final Color trackColor;
  const _ScoreRingPainter({
    required this.fraction,
    required this.color,
    required this.trackColor,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = size.center(Offset.zero);
    final radius = size.shortestSide / 2 - 6;
    final track = Paint()
      ..color = trackColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = 9
      ..strokeCap = StrokeCap.round;
    final progress = Paint()
      ..color = color
      ..style = PaintingStyle.stroke
      ..strokeWidth = 9
      ..strokeCap = StrokeCap.round;
    canvas.drawCircle(center, radius, track);
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      -math.pi / 2,
      2 * math.pi * fraction,
      false,
      progress,
    );
  }

  @override
  bool shouldRepaint(_ScoreRingPainter oldDelegate) =>
      oldDelegate.fraction != fraction ||
      oldDelegate.color != color ||
      oldDelegate.trackColor != trackColor;
}
