import 'package:flutter/material.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';
import 'package:official_connect/Services/portal_session.dart';
import 'package:official_connect/Services/portal_scraper.dart';
import 'package:official_connect/Providers/sisdata.dart';
import 'package:official_connect/Services/sync_diagnostics.dart';
import 'package:provider/provider.dart';

class PortalLoginScreen extends StatefulWidget {
  const PortalLoginScreen(
      {super.key,
      this.initialUsn,
      this.initialDob,
      this.initialVerificationType,
      this.initialVerificationValue,
      this.reuseSession = false,
      this.silent = false});

  final String? initialUsn;
  final String? initialDob;
  final String? initialVerificationType;
  final String? initialVerificationValue;
  final bool reuseSession;

  /// Runs the portal login and scrape off-screen (transparent route). The
  /// caller stays visible and shows its own completion notification.
  final bool silent;

  @override
  State<PortalLoginScreen> createState() => _PortalLoginScreenState();
}

class _PortalLoginScreenState extends State<PortalLoginScreen> {
  final PortalSession _session = PortalSession();
  bool _scrapeStarted = false;
  bool _finished = false;
  bool _showPortal = false;
  String _stage = 'Getting things ready';
  String _detail = 'This usually takes a few seconds.';
  String? _error;
  final Stopwatch _flowWatch = Stopwatch();

  void _updateStage(String stage, {String? detail}) {
    assert(() {
      debugPrint(
        'Portal timing: ${_flowWatch.elapsedMilliseconds}ms - $stage',
      );
      return true;
    }());
    if (!mounted || _finished) return;
    setState(() {
      _stage = stage;
      if (detail != null) _detail = detail;
    });
  }

  Future<void> _scrapeAndCache() async {
    if (_scrapeStarted) return;
    _scrapeStarted = true;
    final scrapeWatch = Stopwatch()..start();
    _updateStage(
      'Login complete',
      detail: 'Updating your information.',
    );
    try {
      // The portal currently rejects replay of its browser session from AWS.
      // Scraping directly in this authenticated WebView avoids that failed
      // network hop and keeps credentials on the device.
      final data = await PortalScraper(
        _session,
        onProgress: (stage) => _updateStage(stage),
      ).scrapeAll();
      assert(() {
        debugPrint('Portal scraper sections: '
            'attendance=${(data['attendance'] as List?)?.length ?? 0}, '
            'marks=${(data['marks'] as List?)?.length ?? 0}, '
            'results=${(data['prevResults'] as List?)?.length ?? 0}, '
            'fees=${(data['fees'] as List?)?.length ?? 0}');
        return true;
      }());
      final hasUsefulSections = data['courseSmall'] != null ||
          (data['attendance'] is List &&
              (data['attendance'] as List).isNotEmpty) ||
          (data['marks'] is List && (data['marks'] as List).isNotEmpty) ||
          (data['prevResults'] is List &&
              (data['prevResults'] as List).isNotEmpty) ||
          (data['fees'] is List && (data['fees'] as List).isNotEmpty);
      if (!hasUsefulSections) {
        throw PortalRequestException(
          PortalSession.dashboardUri,
          'scraper returned incomplete portal data',
        );
      }
      await Provider.of<SisData>(context, listen: false).applyPortalData(
        data,
        widget.initialUsn ?? '',
        widget.initialDob ?? '',
      );
      await SyncDiagnostics.recordSummary(
        Map<String, dynamic>.from((data['_sync'] as Map?) ?? const {}),
        refresh: widget.reuseSession,
      );
      scrapeWatch.stop();
      _updateStage('Finishing up');
      assert(() {
        debugPrint(
          'Portal scraper: cache updated successfully in '
          '${scrapeWatch.elapsedMilliseconds}ms; total '
          '${_flowWatch.elapsedMilliseconds}ms',
        );
        return true;
      }());
      if (mounted) {
        _finished = true;
        Navigator.of(context).pop(true);
      }
    } catch (error) {
      await SyncDiagnostics.recordFailure(refresh: widget.reuseSession);
      assert(() {
        final detail = error is PortalRequestException ? error.reason : '';
        debugPrint('Portal scraper failed: ${error.runtimeType} $detail');
        return true;
      }());
      if (mounted) {
        if (widget.silent) {
          // No UI is visible in silent mode; report failure to the caller
          // so it can notify and offer the full sync page instead.
          _finished = true;
          Navigator.of(context).pop(false);
          return;
        }
        setState(() {
          _error = 'Some information could not be updated. You can show the '
              'page if it needs your attention.';
          _stage = 'Update needs attention';
          _detail = 'Anything already available will remain visible.';
        });
      }
    }
  }

  Future<void> _checkSession() async {
    final authenticated = await _session.isAuthenticated();
    if (!mounted) return;
    if (authenticated) await _scrapeAndCache();
    if (!authenticated) {
      _updateStage(
        'Signing you in',
        detail: 'Finishing the sign-in steps.',
      );
    }
  }

  Future<void> _prefillPortalForm(InAppWebViewController controller) async {
    final usn = widget.initialUsn;
    final dob = widget.initialDob;
    if (usn == null || dob == null || dob.length != 10) return;
    final parts = dob.split('-');
    if (parts.length != 3) return;
    final verification =
        (widget.initialVerificationValue ?? '').replaceAll("'", "\\'");
    final verificationType = (widget.initialVerificationType ?? '')
        .toLowerCase()
        .replaceAll("'", "\\'");
    final script = """
      (function() {
        const username = document.getElementById('username');
        const isVerificationPage = document.body.innerText.toLowerCase()
          .includes('select verification type');
        if (!username && !isVerificationPage) return;
        const dd = document.getElementById('dd');
        const mm = document.getElementById('mm');
        const yyyy = document.getElementById('yyyy');
        if (username) username.value = '${usn.replaceAll("'", "\\'")}';
        // The portal's day option values contain a trailing space (for example, "08 ").
        if (dd) dd.value = '${parts[2]} ';
        if (mm) mm.value = '${parts[1]}';
        if (yyyy) yyyy.value = '${parts[0]}';
        if (typeof putdate === 'function') putdate();
        const value = '$verification';
        document.querySelectorAll('input, select').forEach(function(el) {
          const label = ((el.name || '') + ' ' + (el.id || '') + ' ' + (el.placeholder || '')).toLowerCase();
          if (label.includes('father') || label.includes('mother') || label.includes('parent') || label.includes('card') || label.includes('verification')) {
            el.value = value;
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
          }
        });
        // Verification page: select the matching parent/ID option and fill
        // the four separate last-four-digit boxes used by the portal.
        const wanted = '$verificationType';
        document.querySelectorAll('select').forEach(function(select) {
          const option = Array.from(select.options).find(function(o) {
            const text = (o.text || '').toLowerCase();
            return wanted.includes('father') && text.includes('father') ||
              wanted.includes('mother') && text.includes('mother') ||
              wanted.includes('id') && (text.includes('id') || text.includes('card'));
          });
          if (option) {
            select.value = option.value;
            select.dispatchEvent(new Event('change', {bubbles: true}));
          }
        });
        const digits = value.split('');
        const boxes = Array.from(document.querySelectorAll('input')).filter(function(el) {
          return el.offsetParent !== null && (el.type === 'text' || el.type === 'number');
        });
        if (boxes.length >= 4 && digits.length >= 4) {
          boxes.slice(-4).forEach(function(el, index) {
            el.value = digits[index];
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
          });
        }
        // Continue through ordinary portal buttons after the fields are ready.
        // The login page uses an invisible reCAPTCHA. Wait for the portal's
        // own callback to populate its hidden token before clicking Login.
        setTimeout(function() {
          const loginReady = !!(document.getElementById('username')?.value &&
            document.getElementById('dd')?.value &&
            document.getElementById('mm')?.value &&
            document.getElementById('yyyy')?.value);
          const verificationReady = boxes.length >= 4 &&
            boxes.slice(-4).every(function(el) { return el.value; });
          if (verificationReady) {
            const submit = document.querySelector('input[type="submit"], button[type="submit"]');
            if (submit) {
              submit.click();
              return;
            }
            const form = boxes[boxes.length - 1].form || document.querySelector('form');
            if (form) {
              if (typeof form.requestSubmit === 'function') form.requestSubmit();
              else form.submit();
              return;
            }
          }
          const buttons = Array.from(document.querySelectorAll('button, input[type="submit"], input[type="button"]'));
          const button = buttons.find(function(el) {
            const label = ((el.innerText || el.value || '') + '').trim().toLowerCase();
            return loginReady && label.includes('login');
          });
          const captcha = document.getElementById('captcha-response');
          if (button && !window.__officialConnectLoginScheduled) {
            window.__officialConnectLoginScheduled = true;
            let attempts = 0;
            const submitWhenReady = function() {
              attempts += 1;
              if (!captcha || captcha.value) {
                if (captcha && typeof window.check1 !== 'function') {
                  window.check1 = function() {
                    return !!captcha.value;
                  };
                }
                button.click();
                return;
              }
              if (attempts === 2 && window.grecaptcha &&
                  !window.__officialConnectRecaptchaRequested) {
                window.__officialConnectRecaptchaRequested = true;
                try {
                  window.grecaptcha.ready(function() {
                    const challenge = document.querySelector('.g-recaptcha');
                    if (!challenge) return;
                    let widgetId = 0;
                    try {
                      widgetId = window.grecaptcha.render(challenge, {
                        sitekey: challenge.dataset.sitekey,
                        size: 'invisible',
                        callback: function(token) {
                          captcha.value = token;
                          if (typeof window.onSubmit === 'function') {
                            window.onSubmit(token);
                          }
                        }
                      });
                    } catch (_) {
                      // The API may already have auto-rendered widget zero.
                    }
                    try { window.grecaptcha.execute(widgetId); } catch (_) {}
                  });
                } catch (_) {
                  window.__officialConnectRecaptchaRequested = false;
                }
              }
              if (attempts < 30) {
                setTimeout(submitWhenReady, 500);
              } else {
                window.__officialConnectLoginScheduled = false;
              }
            };
            submitWhenReady();
          }
        }, 800);
      })();
    """;
    // The portal may attach/replace its form after onLoadStop. Retry briefly
    // so autofill remains reliable on slower emulator/network runs.
    for (final delay in const [
      Duration.zero,
      Duration(milliseconds: 350),
      Duration(milliseconds: 900)
    ]) {
      if (delay != Duration.zero) await Future.delayed(delay);
      if (!mounted || _finished) return;
      try {
        await controller.evaluateJavascript(source: script);
      } catch (_) {
        // The route can close while a delayed autofill retry is pending.
        if (!mounted || _finished) return;
        rethrow;
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor:
          widget.silent ? Colors.transparent : const Color(0xfff2f7f8),
      body: Stack(
        children: [
          Positioned.fill(
            child: Opacity(
              opacity: widget.silent ? 0 : 1,
              child: IgnorePointer(
                ignoring: widget.silent,
                child: InAppWebView(
              initialUrlRequest: URLRequest(url: WebUri('about:blank')),
              initialSettings: InAppWebViewSettings(
                javaScriptEnabled: true,
                javaScriptCanOpenWindowsAutomatically: true,
                mediaPlaybackRequiresUserGesture: false,
                domStorageEnabled: true,
                databaseEnabled: true,
                thirdPartyCookiesEnabled: true,
              ),
              onWebViewCreated: (controller) async {
                _flowWatch.start();
                _session.attachController(controller);
                if (!widget.reuseSession) await _session.clear();
                await controller.loadUrl(
                  urlRequest: URLRequest(
                    url: WebUri(PortalSession.loginUri.toString()),
                  ),
                );
              },
              onUpdateVisitedHistory: (_, url, __) {
                _session.rememberPage(url);
              },
              onLoadStop: (controller, __) async {
                if (_finished) return;
                _session.rememberPage(await controller.getUrl());
                await _prefillPortalForm(controller);
                if (!_finished) await _checkSession();
              },
                ),
              ),
            ),
          ),
          if (!widget.silent && !_showPortal)
            Positioned.fill(
              child: ColoredBox(
                color: const Color(0xfff2f7f8),
                child: SafeArea(
                  child: Column(
                    children: [
                      Align(
                        alignment: Alignment.centerLeft,
                        child: IconButton(
                          tooltip: 'Cancel',
                          onPressed: () => Navigator.of(context).pop(false),
                          icon: const Icon(Icons.close),
                        ),
                      ),
                      Expanded(
                        child: Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 34),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Image.asset('images/logo.png', height: 82),
                              const SizedBox(height: 42),
                              if (_error == null)
                                const SizedBox(
                                  width: 34,
                                  height: 34,
                                  child: CircularProgressIndicator(
                                    strokeWidth: 3,
                                    color: Color(0xffba3237),
                                  ),
                                )
                              else
                                const Icon(
                                  Icons.sync_problem_outlined,
                                  size: 42,
                                  color: Color(0xffba3237),
                                ),
                              const SizedBox(height: 24),
                              Text(
                                _stage,
                                textAlign: TextAlign.center,
                                style: const TextStyle(
                                  fontFamily: 'Comfortaa',
                                  fontSize: 21,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                              const SizedBox(height: 10),
                              Text(
                                _detail,
                                textAlign: TextAlign.center,
                                style: const TextStyle(
                                  fontFamily: 'Comfortaa',
                                  color: Colors.black54,
                                  height: 1.4,
                                ),
                              ),
                              if (_error != null) ...[
                                const SizedBox(height: 28),
                                FilledButton.icon(
                                  onPressed: () =>
                                      setState(() => _showPortal = true),
                                  icon: const Icon(Icons.open_in_browser),
                                  label: const Text('Show page'),
                                  style: FilledButton.styleFrom(
                                    backgroundColor: const Color(0xffba3237),
                                  ),
                                ),
                              ],
                            ],
                          ),
                        ),
                      ),
                      const Padding(
                        padding: EdgeInsets.fromLTRB(28, 0, 28, 24),
                        child: Text(
                          'Keep the app open while your information is updated.',
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            fontFamily: 'Comfortaa',
                            fontSize: 12,
                            color: Colors.black45,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          if (_showPortal)
            Positioned(
              top: MediaQuery.paddingOf(context).top + 8,
              left: 8,
              child: Material(
                color: Colors.white,
                shape: const CircleBorder(),
                elevation: 3,
                child: IconButton(
                  tooltip: 'Close portal',
                  onPressed: () => setState(() => _showPortal = false),
                  icon: const Icon(Icons.close),
                ),
              ),
            ),
        ],
      ),
    );
  }
}
