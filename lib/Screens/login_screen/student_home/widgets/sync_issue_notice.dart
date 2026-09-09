import 'package:flutter/material.dart';
import 'package:official_connect/Providers/sisdata.dart';

class SyncIssueNotice extends StatelessWidget {
  const SyncIssueNotice({
    super.key,
    required this.sisData,
    this.section,
    this.hasVisibleData = false,
  });

  final SisData sisData;
  final String? section;
  final bool hasVisibleData;

  @override
  Widget build(BuildContext context) {
    final status = section == null
        ? (sisData.hasSyncIssues ? 'partial' : 'ok')
        : sisData.syncStatusFor(section!);
    if (status != 'partial' && status != 'error') {
      return const SizedBox.shrink();
    }

    final label = section == null
        ? 'Some information is temporarily unavailable. We’ll keep showing everything we could retrieve.'
        : hasVisibleData
            ? 'This section could not be fully refreshed. Showing the latest available information.'
            : 'This section is temporarily unavailable. We’re getting it checked.';

    return Container(
      margin: const EdgeInsets.only(top: 16, bottom: 8),
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
      decoration: BoxDecoration(
        color: const Color(0xfffff3dc),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: const Color(0xffe8c77d)),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(Icons.info_outline, color: Color(0xff8b641c), size: 21),
          const SizedBox(width: 10),
          Expanded(
            child: Text(
              label,
              style: const TextStyle(
                fontFamily: 'Comfortaa',
                fontSize: 13,
                height: 1.4,
                color: Color(0xff64470f),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
