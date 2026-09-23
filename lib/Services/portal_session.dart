import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';
import 'package:http/http.dart' as http;

String portalFailureReason(Object error) {
  if (error is PortalSessionExpiredException) return 'session_expired';
  if (error is PortalContentNotReadyException) return 'content_not_ready';
  if (error is FormatException) return 'parse_error';
  if (error is PortalRequestException) {
    final reason = error.reason.toLowerCase();
    if (reason.contains('timed out')) return 'timeout';
    if (reason.contains('not ready')) return 'browser_not_ready';
    if (reason.contains('empty')) return 'empty_response';
    return 'request_error';
  }
  return 'unknown';
}

@visibleForTesting
String? portalExpectedContentSelector(Uri target) {
  final task = target.queryParameters['task'];
  return switch (task) {
    'timetable' => 'table.cn-time-table, table.cn-time_table',
    'attendencelist' =>
      '.cn-legend, table.cn-attend-list1, table.cn-attend-list2',
    'ciedetails' => 'tr.odd, .cn-cie-stat, th[colspan="9"]',
    'observation' => 'table.cn-res-table, .md-card-head-text',
    'getResult' => 'table.res-table',
    'studFee' => 'table.cn-pay-table',
    'dashboard' => '.cn-stu-data, .cn-student-header, .cn-basic-details',
    _ => switch (target.queryParameters['option']) {
      'com_history' => 'table.res-table',
      'com_fee' => 'table.cn-pay-table',
      _ => null,
    },
  };
}

/// Owns the portal browser session used by the on-device scraper.
///
/// The portal login, parent verification and any challenge remain inside the
/// browser. Native requests reuse the resulting cookies only for direct reads
/// from the official portal; credentials are never sent to an app backend.
class PortalSession {
  PortalSession({CookieManager? cookieManager})
    : _cookieManager = cookieManager ?? CookieManager.instance();

  static final Uri loginUri = Uri.parse(
    'https://parents.msrit.edu/newparents/index.php',
  );
  static final Uri dashboardUri = Uri.parse(
    'https://parents.msrit.edu/newparents/index.php?option=com_studentdashboard&controller=studentdashboard&task=dashboard',
  );
  final CookieManager _cookieManager;

  InAppWebViewController? _controller;
  Uri? _authenticatedEntryUri;

  void attachController(InAppWebViewController controller) {
    _controller = controller;
  }

  void rememberPage(Uri? uri) {
    if (uri != null && uri.queryParameters.containsKey('ksign')) {
      _authenticatedEntryUri = uri;
    }
  }

  Uri _withSession(Uri uri) {
    final signed = _authenticatedEntryUri?.queryParameters['ksign'];
    if (signed == null || uri.queryParameters.containsKey('ksign')) return uri;
    return uri.replace(
      queryParameters: {...uri.queryParameters, 'ksign': signed},
    );
  }

  Future<void> clear() async {
    await _cookieManager.deleteAllCookies();
    await InAppWebViewController.clearAllCache();
  }

  Future<String> _cookieHeader() async {
    final cookies = await _cookieManager.getCookies(
      url: WebUri(loginUri.toString()),
    );
    return cookies
        .where((cookie) => cookie.value != null)
        .map((cookie) => '${cookie.name}=${cookie.value}')
        .join('; ');
  }

  Future<http.Response> fetch(Uri uri) async {
    uri = _withSession(uri);
    final cookieHeader = await _cookieHeader();
    final response = await http
        .get(
          uri,
          headers: {
            if (cookieHeader.isNotEmpty) 'Cookie': cookieHeader,
            'User-Agent': 'OfficialConnect/1.0',
          },
        )
        .timeout(
          const Duration(seconds: 15),
          onTimeout: () {
            throw PortalRequestException(uri, 'request timed out');
          },
        );

    final body = response.body.toLowerCase();
    if (response.statusCode >= 300 ||
        body.contains('id="login-form"') ||
        body.contains('name="username"')) {
      throw const PortalSessionExpiredException();
    }
    return response;
  }

  /// Fetches through the WebView itself, preserving every browser-only session
  /// primitive (cookies, redirects and portal JavaScript state).
  Future<String> currentHtml() async {
    final controller = _controller;
    if (controller == null) {
      throw PortalRequestException(loginUri, 'browser is not ready');
    }
    final html = await controller.evaluateJavascript(
      source: 'document.documentElement.outerHTML',
    );
    if (html is! String || html.isEmpty) {
      throw PortalRequestException(loginUri, 'current page is empty');
    }
    return html;
  }

  /// Reads a portal page through a real WebView navigation. The current portal
  /// rejects cookie-authenticated replay and same-page fetch requests, but
  /// accepts its own signed links when followed as browser navigations.
  Future<String> navigateAndRead(Uri uri) async {
    final controller = _controller;
    if (controller == null) {
      throw PortalRequestException(uri, 'browser is not ready');
    }
    // Keep the portal's own authenticated href exactly as emitted. Appending
    // ksign to these in-page links causes the portal to return the dashboard.
    final target = uri;
    final marker = DateTime.now().microsecondsSinceEpoch.toString();
    await controller.evaluateJavascript(
      source: "window.__officialConnectNavigationMarker = '$marker'",
    );
    await controller.evaluateJavascript(
      source:
          '''
        (function() {
          const target = new URL(${jsonEncode(target.toString())}, location.href);
          const routeKeys = ['option', 'controller', 'task'];
          const link = Array.from(document.querySelectorAll('a[href]')).find(function(anchor) {
            const candidate = new URL(anchor.href, location.href);
            return routeKeys.every(function(key) {
              return !target.searchParams.has(key) ||
                candidate.searchParams.get(key) === target.searchParams.get(key);
            });
          });
          if (link) link.click();
          else location.assign(target.href);
        })();
      ''',
    );
    for (var attempt = 0; attempt < 60; attempt++) {
      await Future.delayed(const Duration(milliseconds: 250));
      final currentMarker = await controller.evaluateJavascript(
        source: 'window.__officialConnectNavigationMarker',
      );
      final ready = await controller.evaluateJavascript(
        source: 'document.readyState',
      );
      // Android WebView serializes JavaScript strings with quotes. Without
      // normalizing the marker, the old dashboard can look like a newly loaded
      // document and be returned before location.assign has even started.
      final markerValue = currentMarker?.toString().replaceAll('"', '');
      final readyState = ready?.toString().replaceAll('"', '');
      if (markerValue != marker && readyState == 'complete') {
        // Wait for page-specific content rather than using a fixed delay. Most
        // pages are ready in well under a second; result history is allowed a
        // little longer because the portal initializes it asynchronously.
        final expectedSelector = portalExpectedContentSelector(target);
        if (expectedSelector != null) {
          final maxContentAttempts =
              target.queryParameters['option'] == 'com_history' ? 48 : 24;
          var contentFound = false;
          for (
            var contentAttempt = 0;
            contentAttempt < maxContentAttempts;
            contentAttempt++
          ) {
            final found = await controller.evaluateJavascript(
              source:
                  '!!document.querySelector(${jsonEncode(expectedSelector)})',
            );
            if (found == true || found?.toString() == 'true') {
              contentFound = true;
              break;
            }
            await Future.delayed(const Duration(milliseconds: 250));
          }
          if (!contentFound) {
            throw PortalContentNotReadyException(target);
          }
        } else {
          await Future.delayed(const Duration(milliseconds: 300));
        }
        final html = await currentHtml();
        final loadedUrl = await controller.getUrl();
        assert(() {
          final safeTarget = target.replace(
            queryParameters: Map<String, String>.from(target.queryParameters)
              ..remove('ksign'),
          );
          final parsedLoaded = Uri.tryParse(loadedUrl?.toString() ?? '');
          final safeLoaded = parsedLoaded?.replace(
            queryParameters: Map<String, String>.from(
              parsedLoaded.queryParameters,
            )..remove('ksign'),
          );
          // Only route information is logged; no HTML or session values.
          // ignore: avoid_print
          print(
            'Portal navigation completed: target=$safeTarget, '
            'loaded=$safeLoaded',
          );
          return true;
        }());
        return html;
      }
    }
    throw PortalRequestException(target, 'browser navigation timed out');
  }

  Future<String> fetchHtml(Uri uri) async {
    final controller = _controller;
    if (controller == null) {
      throw PortalRequestException(uri, 'browser is not ready');
    }
    final target = _withSession(uri);
    final result = await controller
        .callAsyncJavaScript(
          functionBody: '''
        const response = await fetch(url, {
          method: 'GET',
          credentials: 'include',
          redirect: 'follow',
          cache: 'no-store'
        });
        const body = await response.text();
        return {status: response.status, url: response.url, body: body};
      ''',
          arguments: {'url': target.toString()},
        )
        .timeout(
          const Duration(seconds: 20),
          onTimeout: () {
            throw PortalRequestException(target, 'browser request timed out');
          },
        );
    if (result == null || result.error != null || result.value is! Map) {
      throw PortalRequestException(
        target,
        result?.error?.toString() ?? 'empty browser response',
      );
    }
    final value = Map<String, dynamic>.from(result.value as Map);
    final status = value['status'] as int? ?? 0;
    final body = value['body']?.toString() ?? '';
    final lower = body.toLowerCase();
    if (status < 200 || status >= 300 || lower.contains('name="username"')) {
      throw const PortalSessionExpiredException();
    }
    return body;
  }

  /// Fetches a binary resource through the WebView itself (session cookies
  /// included) and returns it as a data URI. Used for the student photo,
  /// which the portal only serves to its authenticated browser session.
  Future<String?> fetchDataUri(Uri uri) async {
    final controller = _controller;
    if (controller == null) return null;
    try {
      final result = await controller
          .callAsyncJavaScript(
            functionBody: '''
          const response = await fetch(url, {
            method: 'GET',
            credentials: 'include',
            cache: 'no-store'
          });
          if (!response.ok) return {status: response.status};
          const buffer = await response.arrayBuffer();
          const bytes = new Uint8Array(buffer);
          let binary = '';
          const chunk = 0x8000;
          for (let i = 0; i < bytes.length; i += chunk) {
            binary += String.fromCharCode.apply(
              null, bytes.subarray(i, i + chunk));
          }
          return {
            status: response.status,
            mime: response.headers.get('content-type') || 'image/jpeg',
            base64: btoa(binary)
          };
        ''',
            arguments: {'url': uri.toString()},
          )
          .timeout(const Duration(seconds: 20));
      if (result == null || result.error != null || result.value is! Map) {
        return null;
      }
      final value = Map<String, dynamic>.from(result.value as Map);
      final base64 = value['base64']?.toString();
      if ((value['status'] as int? ?? 0) != 200 ||
          base64 == null ||
          base64.isEmpty) {
        return null;
      }
      return 'data:${value['mime']};base64,$base64';
    } catch (_) {
      return null;
    }
  }

  Future<bool> isAuthenticated() async {
    final controller = _controller;
    if (controller != null) {
      try {
        final currentPage = await controller.evaluateJavascript(
          source: '''
          (function() {
            const hasLogin = !!document.querySelector('input[name="username"], #username');
            const hasDashboard = !!document.querySelector(
              '.cn-stu-data, .cn-student-header, .cn-basic-details'
            );
            return !hasLogin && hasDashboard;
          })();
        ''',
        );
        if (currentPage == true || currentPage?.toString() == 'true') {
          final currentUrl = await controller.getUrl();
          if (currentUrl != null) {
            _authenticatedEntryUri = Uri.tryParse(currentUrl.toString());
          }
          return true;
        }
      } catch (_) {
        // Fall through to an authenticated dashboard request.
      }
    }
    try {
      await fetchHtml(dashboardUri);
      return true;
    } on PortalSessionExpiredException {
      return false;
    } catch (_) {
      return false;
    }
  }
}

class PortalSessionExpiredException implements Exception {
  const PortalSessionExpiredException();

  @override
  String toString() => 'The portal session has expired.';
}

class PortalContentNotReadyException implements Exception {
  const PortalContentNotReadyException(this.uri);
  final Uri uri;

  @override
  String toString() => 'Portal content was not ready.';
}

class PortalRequestException implements Exception {
  const PortalRequestException(this.uri, this.reason);
  final Uri uri;
  final String reason;

  @override
  String toString() => 'Portal request failed ($reason).';
}
