import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:official_connect/Services/portal_scraper.dart';
import 'package:official_connect/Services/portal_session.dart';
import 'package:official_connect/Services/firebase_feature_flags.dart';

class _FixturePages {
  _FixturePages(this.responses, {this.throwingIds = const {}});

  final Map<String, String> responses;
  final Set<String> throwingIds;

  Future<String> navigateAndRead(Uri uri) async {
    final id = uri.queryParameters['id'];
    if (id != null && throwingIds.contains(id)) {
      throw StateError('simulated section failure');
    }
    if (uri == PortalSession.dashboardUri) return responses['dashboard']!;
    if (uri.toString().contains('attendencelist')) {
      return responses['attendance:$id']!;
    }
    if (uri.toString().contains('ciedetails')) return responses['marks:$id']!;
    if (uri.queryParameters['option'] == 'com_fee') return responses['fees']!;
    if (uri.queryParameters['task'] == 'observation') {
      return responses['proctor']!;
    }
    if (uri.queryParameters['option'] == 'com_history') {
      return responses['results']!;
    }
    throw StateError('No fixture for $uri');
  }
}

String _fixture(String name) => File('test/fixtures/$name').readAsStringSync();

void main() {
  tearDown(() => FirebaseFeatureFlags.setValuesForTesting(const {}));

  Map<String, String> fixtures() => {
    'dashboard': _fixture('dashboard_variant.html'),
    'attendance:good': _fixture('attendance_variant.html'),
    'attendance:bad': _fixture('malformed_section.html'),
    'marks:good': _fixture('marks_variant.html'),
    'marks:bad': _fixture('malformed_section.html'),
    'fees': _fixture('fees_variant.html'),
    'proctor': _fixture('proctor_variant.html'),
    'results': _fixture('results_variant.html'),
  };

  test('parses anonymized alternate portal layouts', () async {
    final pages = _FixturePages(fixtures());
    final result = await PortalScraper.forTesting(
      navigateAndRead: pages.navigateAndRead,
    ).scrapeAll();

    expect(result['name'], 'Test Student');
    expect(result['courseSmall'], 'B.E. ISE');
    expect((result['attendance'] as List), hasLength(1));
    expect(result['attendance'][0]['code'], 'IS701');
    expect(result['attendance'][0]['percentage'], '90%');
    expect((result['marks'] as List), hasLength(1));
    expect(result['marks'][0]['final cie'], '91');
    expect((result['fees'] as List), hasLength(1));
    expect((result['prevResults'] as List), hasLength(1));
    expect(result['prevResults'][0]['results'][0]['Grade'], 'A');
  });

  test('one malformed section cannot blank successful sections', () async {
    final pages = _FixturePages(fixtures(), throwingIds: const {'bad'});
    final result = await PortalScraper.forTesting(
      navigateAndRead: pages.navigateAndRead,
    ).scrapeAll();

    expect(result['name'], 'Test Student');
    expect((result['attendance'] as List), hasLength(1));
    expect((result['marks'] as List), hasLength(1));
    expect((result['fees'] as List), hasLength(1));
    expect((result['prevResults'] as List), hasLength(1));
    expect(result['_sync']['outcome'], 'partial');
    expect(result['_sync']['sections']['attendance']['status'], 'partial');
    expect(result['_sync']['sections']['marks']['status'], 'partial');
  });

  test('disabled sections are skipped without blocking enabled data', () async {
    FirebaseFeatureFlags.setValuesForTesting(const {
      'scraper_attendance_enabled': false,
      'scraper_marks_enabled': false,
    });
    final pages = _FixturePages(fixtures());
    final result = await PortalScraper.forTesting(
      navigateAndRead: pages.navigateAndRead,
    ).scrapeAll();

    expect(result['attendance'], isEmpty);
    expect(result['marks'], isEmpty);
    expect(result['_sync']['sections']['attendance']['status'], 'disabled');
    expect(result['_sync']['sections']['marks']['status'], 'disabled');
    expect((result['fees'] as List), hasLength(1));
    expect((result['prevResults'] as List), hasLength(1));
  });

  test(
    'missing course links are structural failures, not empty data',
    () async {
      final values = fixtures();
      values['dashboard'] = values['dashboard']!
          .replaceAll(RegExp(r'<a href="\?task=attendencelist[^<]+</a>'), '')
          .replaceAll(RegExp(r'<a href="\?task=ciedetails[^<]+</a>'), '');
      final pages = _FixturePages(values);

      final result = await PortalScraper.forTesting(
        navigateAndRead: pages.navigateAndRead,
      ).scrapeAll();

      expect(result['_sync']['sections']['attendance']['status'], 'error');
      expect(result['_sync']['sections']['marks']['status'], 'error');
      expect(result['_sync']['outcome'], 'partial');
    },
  );
}
