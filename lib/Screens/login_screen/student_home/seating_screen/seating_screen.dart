import 'dart:async';

import 'package:flutter_neumorphic_plus/flutter_neumorphic.dart';
import 'package:official_connect/Classes/seating_arrangement.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Providers/themes.dart';
import 'package:official_connect/Services/sync_diagnostics.dart';
import 'package:provider/provider.dart';

class SeatingScreen extends StatefulWidget {
  const SeatingScreen({super.key});

  @override
  State<SeatingScreen> createState() => _SeatingScreenState();
}

class _SeatingScreenState extends State<SeatingScreen> {
  String? _reportedState;

  void _recordState(String state) {
    if (_reportedState == state) return;
    _reportedState = state;
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (mounted) {
        unawaited(SyncDiagnostics.recordFeatureState('exam_seating', state));
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final sisData = context.watch<SisData>();
    final syncStatus = sisData.syncStatusFor('seating');
    final featureState = sisData.seating.isNotEmpty
        ? 'loaded'
        : syncStatus == 'error'
        ? 'error'
        : syncStatus == 'empty'
        ? 'empty'
        : syncStatus == 'disabled'
        ? 'disabled'
        : 'legacy_cache';
    _recordState(featureState);
    final now = DateTime.now();
    final today = DateTime(now.year, now.month, now.day);
    final upcoming = sisData.seating
        .where((item) => item.parsedDate?.isBefore(today) == false)
        .toList();
    final past = sisData.seating
        .where((item) => !upcoming.contains(item))
        .toList();
    return DefaultTabController(
      length: 2,
      child: Scaffold(
        backgroundColor: sisData.darkMode
            ? const Color(0xff101114)
            : Colors.white,
        appBar: AppBar(
          title: const Text('Exam seating'),
          backgroundColor: Colors.transparent,
          foregroundColor: sisData.darkMode ? Colors.white : Colors.black,
          elevation: 0,
          bottom: TabBar(
            indicatorColor: CustomTheme.accent,
            labelColor: CustomTheme.accent,
            unselectedLabelColor: sisData.darkMode
                ? Colors.white54
                : Colors.black54,
            tabs: const [
              Tab(text: 'Upcoming'),
              Tab(text: 'Past'),
            ],
          ),
        ),
        body: Container(
          decoration: BoxDecoration(
            gradient: CustomTheme.linearGradientBG(context),
          ),
          child: TabBarView(
            children: [
              _SeatingList(items: upcoming, upcoming: true),
              _SeatingList(items: past, upcoming: false),
            ],
          ),
        ),
      ),
    );
  }
}

class _SeatingList extends StatelessWidget {
  const _SeatingList({required this.items, required this.upcoming});
  final List<SeatingArrangement> items;
  final bool upcoming;

  @override
  Widget build(BuildContext context) {
    if (items.isEmpty) {
      return Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              Icons.event_seat_outlined,
              size: 48,
              color: CustomTheme.accent.withValues(alpha: 0.75),
            ),
            const SizedBox(height: 14),
            Text(
              upcoming ? 'No upcoming seating yet' : 'No past arrangements',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
                color: context.watch<SisData>().darkMode
                    ? Colors.white
                    : const Color(0xff1d1f24),
              ),
            ),
          ],
        ),
      );
    }
    return ListView.separated(
      padding: const EdgeInsets.fromLTRB(20, 22, 20, 36),
      itemCount: items.length,
      separatorBuilder: (_, __) => const SizedBox(height: 16),
      itemBuilder: (context, index) => _SeatingCard(item: items[index]),
    );
  }
}

class _SeatingCard extends StatelessWidget {
  const _SeatingCard({required this.item});
  final SeatingArrangement item;

  @override
  Widget build(BuildContext context) {
    final date = item.parsedDate;
    final primary = context.watch<SisData>().darkMode
        ? Colors.white
        : const Color(0xff1d1f24);
    return Neumorphic(
      style: CustomTheme.neumorphicStyle(context),
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: 54,
                  padding: const EdgeInsets.symmetric(vertical: 9),
                  decoration: BoxDecoration(
                    color: CustomTheme.accent.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: Column(
                    children: [
                      Text(
                        date == null ? 'DATE' : _month(date.month),
                        style: const TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.w700,
                          color: CustomTheme.accent,
                        ),
                      ),
                      Text(
                        date?.day.toString() ?? '—',
                        style: const TextStyle(
                          fontSize: 21,
                          fontWeight: FontWeight.w800,
                          color: CustomTheme.accent,
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        item.courseName,
                        style: TextStyle(
                          fontSize: 17,
                          height: 1.25,
                          fontWeight: FontWeight.w700,
                          color: primary,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        item.courseCode,
                        style: const TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.w600,
                          color: CustomTheme.accent,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 18),
            _InfoRow(
              icon: Icons.schedule_outlined,
              text: [
                item.timing,
                item.session,
              ].where((value) => value.isNotEmpty).join(' · '),
            ),
            const SizedBox(height: 10),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                if (item.block.isNotEmpty)
                  _PlaceChip(icon: Icons.apartment_outlined, text: item.block),
                if (item.room.isNotEmpty)
                  _PlaceChip(
                    icon: Icons.meeting_room_outlined,
                    text: 'Room ${item.room}',
                  ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _InfoRow extends StatelessWidget {
  const _InfoRow({required this.icon, required this.text});
  final IconData icon;
  final String text;

  @override
  Widget build(BuildContext context) => Row(
    children: [
      Icon(icon, size: 19, color: CustomTheme.accent),
      const SizedBox(width: 9),
      Expanded(
        child: Text(
          text,
          style: TextStyle(
            fontSize: 14,
            height: 1.3,
            color: context.watch<SisData>().darkMode
                ? Colors.white
                : const Color(0xff1d1f24),
          ),
        ),
      ),
    ],
  );
}

class _PlaceChip extends StatelessWidget {
  const _PlaceChip({required this.icon, required this.text});
  final IconData icon;
  final String text;

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 8),
    decoration: BoxDecoration(
      color: CustomTheme.accent.withValues(alpha: 0.08),
      borderRadius: BorderRadius.circular(12),
    ),
    child: Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(icon, size: 17, color: CustomTheme.accent),
        const SizedBox(width: 6),
        Text(
          text,
          style: TextStyle(
            fontSize: 13,
            fontWeight: FontWeight.w600,
            color: context.watch<SisData>().darkMode
                ? Colors.white
                : const Color(0xff1d1f24),
          ),
        ),
      ],
    ),
  );
}

String _month(int month) => const [
  'JAN',
  'FEB',
  'MAR',
  'APR',
  'MAY',
  'JUN',
  'JUL',
  'AUG',
  'SEP',
  'OCT',
  'NOV',
  'DEC',
][month - 1];
