import 'dart:async';

import 'package:flutter_neumorphic_plus/flutter_neumorphic.dart';
import 'package:official_connect/Classes/timetable_entry.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Providers/themes.dart';
import 'package:official_connect/Screens/login_screen/portal_refresh.dart';
import 'package:official_connect/Services/sync_diagnostics.dart';
import 'package:provider/provider.dart';

class TimetableScreen extends StatefulWidget {
  const TimetableScreen({super.key});

  @override
  State<TimetableScreen> createState() => _TimetableScreenState();
}

class _TimetableScreenState extends State<TimetableScreen> {
  String? _selectedDate;
  String? _reportedState;

  void _recordState(String state) {
    if (_reportedState == state) return;
    _reportedState = state;
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (mounted) {
        unawaited(SyncDiagnostics.recordFeatureState('timetable', state));
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final sisData = context.watch<SisData>();
    final grouped = <String, List<TimetableEntry>>{};
    for (final entry in sisData.timetable) {
      grouped.putIfAbsent(entry.date, () => []).add(entry);
    }
    final dates = grouped.keys.toList()..sort();
    final today = _isoDate(DateTime.now());
    final selected = grouped.containsKey(_selectedDate)
        ? _selectedDate!
        : grouped.containsKey(today)
        ? today
        : dates.isEmpty
        ? ''
        : dates.first;
    final entries = grouped[selected] ?? const <TimetableEntry>[];
    final completedToday = selected == today;
    final syncStatus = sisData.syncStatusFor('timetable');
    final featureState = dates.isNotEmpty
        ? 'loaded'
        : syncStatus == 'error'
        ? 'error'
        : syncStatus == 'empty'
        ? 'empty'
        : syncStatus == 'disabled'
        ? 'disabled'
        : 'legacy_cache';
    _recordState(featureState);

    return Scaffold(
      backgroundColor: sisData.darkMode
          ? const Color(0xff101114)
          : Colors.white,
      appBar: AppBar(
        title: const Text('Timetable'),
        backgroundColor: Colors.transparent,
        foregroundColor: sisData.darkMode ? Colors.white : Colors.black,
        elevation: 0,
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: CustomTheme.linearGradientBG(context),
        ),
        child: dates.isEmpty
            ? _EmptyTimetable(
                state: featureState,
                onRefresh: featureState == 'disabled'
                    ? null
                    : () {
                        unawaited(SyncDiagnostics.recordFeature('update_data'));
                        unawaited(openPortalRefresh(context));
                      },
              )
            : Column(
                children: [
                  SizedBox(
                    height: 82,
                    child: ListView.separated(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 20,
                        vertical: 10,
                      ),
                      scrollDirection: Axis.horizontal,
                      itemCount: dates.length,
                      separatorBuilder: (_, __) => const SizedBox(width: 10),
                      itemBuilder: (context, index) {
                        final date = dates[index];
                        final first = grouped[date]!.first;
                        final parsed = DateTime.tryParse(date);
                        return _DayChip(
                          weekday: _shortDay(first.day),
                          date: parsed?.day.toString() ?? date,
                          active: date == selected,
                          onTap: () => setState(() => _selectedDate = date),
                        );
                      },
                    ),
                  ),
                  Expanded(
                    child: ListView.separated(
                      padding: const EdgeInsets.fromLTRB(20, 12, 20, 36),
                      itemCount: entries.length,
                      separatorBuilder: (_, __) => const SizedBox(height: 12),
                      itemBuilder: (context, index) => _ScheduleRow(
                        entry: entries[index],
                        isLast: index == entries.length - 1,
                        isCompleted:
                            completedToday && _hasEnded(entries[index].time),
                      ),
                    ),
                  ),
                ],
              ),
      ),
    );
  }
}

class _DayChip extends StatelessWidget {
  const _DayChip({
    required this.weekday,
    required this.date,
    required this.active,
    required this.onTap,
  });
  final String weekday;
  final String date;
  final bool active;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) => InkWell(
    borderRadius: BorderRadius.circular(18),
    onTap: onTap,
    child: AnimatedContainer(
      duration: const Duration(milliseconds: 180),
      width: 58,
      padding: const EdgeInsets.symmetric(vertical: 7),
      decoration: BoxDecoration(
        color: active
            ? CustomTheme.accent
            : CustomTheme.accent.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(18),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(
            weekday,
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w600,
              color: active ? Colors.white70 : CustomTheme.accent,
            ),
          ),
          const SizedBox(height: 2),
          Text(
            date,
            style: TextStyle(
              fontSize: 19,
              fontWeight: FontWeight.w700,
              color: active ? Colors.white : CustomTheme.accent,
            ),
          ),
        ],
      ),
    ),
  );
}

class _ScheduleRow extends StatelessWidget {
  const _ScheduleRow({
    required this.entry,
    required this.isLast,
    required this.isCompleted,
  });
  final TimetableEntry entry;
  final bool isLast;
  final bool isCompleted;

  @override
  Widget build(BuildContext context) {
    final details = [
      entry.room,
      entry.batch,
    ].where((value) => value.isNotEmpty).join(' · ');
    final darkMode = context.watch<SisData>().darkMode;
    final primary = isCompleted
        ? (darkMode ? Colors.white54 : Colors.black45)
        : (darkMode ? Colors.white : const Color(0xff1d1f24));
    final muted = isCompleted
        ? (darkMode ? Colors.white38 : Colors.black38)
        : (darkMode ? Colors.white70 : Colors.black54);
    return IntrinsicHeight(
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          SizedBox(
            width: 74,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  _startTime(entry.time),
                  style: const TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w700,
                    color: CustomTheme.accent,
                  ),
                ),
                if (_endTime(entry.time).isNotEmpty)
                  Text(
                    _endTime(entry.time),
                    style: TextStyle(fontSize: 11, color: muted),
                  ),
              ],
            ),
          ),
          Container(
            width: 3,
            margin: const EdgeInsets.only(right: 14),
            decoration: BoxDecoration(
              color: isCompleted
                  ? (darkMode ? Colors.white24 : Colors.black26)
                  : isLast
                  ? CustomTheme.accent.withValues(alpha: 0.35)
                  : CustomTheme.accent,
              borderRadius: BorderRadius.circular(4),
            ),
          ),
          Expanded(
            child: Neumorphic(
              style: CustomTheme.neumorphicStyle(context),
              child: Padding(
                padding: const EdgeInsets.all(15),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      entry.name,
                      maxLines: 3,
                      overflow: TextOverflow.ellipsis,
                      style: TextStyle(
                        fontSize: 16,
                        height: 1.25,
                        fontWeight: FontWeight.w700,
                        color: primary,
                      ),
                    ),
                    const SizedBox(height: 7),
                    Text(
                      entry.code,
                      style: const TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                        color: CustomTheme.accent,
                      ),
                    ),
                    if (details.isNotEmpty) ...[
                      const SizedBox(height: 3),
                      Text(
                        details,
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                        style: TextStyle(fontSize: 13, color: muted),
                      ),
                    ],
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _EmptyTimetable extends StatelessWidget {
  const _EmptyTimetable({required this.state, required this.onRefresh});

  final String state;
  final VoidCallback? onRefresh;

  @override
  Widget build(BuildContext context) {
    final title = switch (state) {
      'legacy_cache' => 'Update to load your timetable',
      'error' => 'Timetable could not be updated',
      'disabled' => 'Timetable is temporarily unavailable',
      _ => 'No timetable published for this week',
    };
    final detail = switch (state) {
      'legacy_cache' => 'Your saved data is from an earlier app version.',
      'error' => 'Your other saved information is still available.',
      'disabled' => 'Your other saved information is still available.',
      _ => 'You can check again whenever the schedule is updated.',
    };
    final buttonLabel = state == 'legacy_cache' ? 'Update data' : 'Check again';
    final darkMode = context.watch<SisData>().darkMode;
    return Center(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(28),
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 360),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(
                Icons.calendar_today_outlined,
                size: 44,
                color: CustomTheme.accent,
              ),
              const SizedBox(height: 14),
              Text(
                title,
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w700,
                  color: darkMode ? Colors.white : const Color(0xff1d1f24),
                ),
              ),
              const SizedBox(height: 8),
              Text(
                detail,
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 14,
                  height: 1.35,
                  color: darkMode ? Colors.white70 : Colors.black54,
                ),
              ),
              if (onRefresh != null) ...[
                const SizedBox(height: 18),
                FilledButton.icon(
                  onPressed: onRefresh,
                  icon: const Icon(Icons.refresh_rounded),
                  label: Text(buttonLabel),
                  style: FilledButton.styleFrom(
                    backgroundColor: CustomTheme.accent,
                    foregroundColor: Colors.white,
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

String _isoDate(DateTime value) =>
    '${value.year}-${value.month.toString().padLeft(2, '0')}-${value.day.toString().padLeft(2, '0')}';
String _shortDay(String value) => value.length < 3
    ? value.toUpperCase()
    : value.substring(0, 3).toUpperCase();
String _startTime(String value) => value.split(RegExp(r'\s+-\s+')).first.trim();
String _endTime(String value) {
  final parts = value.split(RegExp(r'\s+-\s+'));
  return parts.length > 1 ? parts.last.trim() : '';
}

bool _hasEnded(String value) {
  final parts = RegExp(r'(\d{1,2}):(\d{2})').allMatches(value).toList();
  if (parts.length < 2) return false;
  final hour = int.tryParse(parts.last.group(1)!);
  final minute = int.tryParse(parts.last.group(2)!);
  if (hour == null || minute == null) return false;
  final now = DateTime.now();
  return hour * 60 + minute < now.hour * 60 + now.minute;
}
