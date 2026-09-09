# official_connect

The Official Student information system app for MSRIT students
## Getting Started
#todo : we need to make a proper todo for documentation purpose.

This project is a starting point for a Flutter application.

A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://flutter.dev/docs/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://flutter.dev/docs/cookbook)

For help getting started with Flutter, view our
[online documentation](https://flutter.dev/docs), which offers tutorials,
samples, guidance on mobile development, and a full API reference.
# Official Connect

## Portal login integration notes

The official portal login form uses `username` plus three date selectors:

- `dd` uses values with a trailing space, such as `08 `.
- `mm` uses two-digit values, such as `12`.
- `yyyy` uses the four-digit year, such as `2000`.
- Changing `yyyy` invokes the portal `putdate()` JavaScript function, which generates the hidden password value.

The app-side WebView fills these controls and then continues through the portal's ordinary login and verification buttons. It must not fabricate or bypass any server-side CAPTCHA/token validation.

Login details are cached locally to suggest them on the next launch. Clearing the USN clears the saved login set. Future dates are rejected as stale/invalid cache values. The DOB picker must preserve the date selected by the user; opening the picker must not overwrite it with today's date.

### Scraper architecture and deployed Lambda

The app establishes the authenticated portal session in a WebView. During the ordinary successful path, the WebView stays mounted and active behind a native progress screen, so users see app-owned status messages rather than the portal UI. If the portal ever requires an interactive step, the error state offers an explicit **Open portal** fallback instead of silently failing.

The `/sis` Lambda accepts that short-lived session only for one invocation and never persists or logs cookies. Session errors return HTTP 401 with `validation: session_expired`, and responses use `Cache-Control: no-store`. The deployed function uses Python 3.14, 512 MB of memory, a 60-second timeout, and a self-contained package with `aiohttp` and `lxml`; the obsolete dependency layer has been removed.

The portal currently rejects its Android WebView session when replayed from AWS, even with the same cookie, signed context, and user agent. The Android app therefore skips that known-failing Lambda hop and scrapes directly inside the authenticated WebView. This preserves the portal's browser and network context, keeps credentials on the device, and stores only the parsed native-app JSON in the existing local cache. The scraper visits prerequisite authenticated pages before exam history and waits for page-specific content instead of fixed delays.

Measured on the API 35 Android emulator on 2026-09-08, the old flow took 50.1 seconds end-to-end. The optimized flow took 14.0 seconds for a repeat sync and 11.3 seconds with cookies cleared and the complete autofilled portal login. Internal instrumentation measured 2.5-3.9 seconds for scraping and 8.9-9.6 seconds from WebView creation through cache completion. These are diagnostic development measurements and will vary with portal and network latency.

The Lambda session endpoint remains useful as a future server-side hotfix path if the portal stops binding sessions to the original browser/network context. Production deployment should add endpoint abuse protection/rate limiting and keep request-body logging disabled because portal cookies are bearer credentials.

### Examination results source

The **latest result** shortcuts are separate from the parent portal. They use the MSRIT examination results site (`exam.msrit.edu`) and must not be populated from cached parent-portal history.

The old results Lambda scraped three routes without a browser. That contract is no longer valid: the former `/eresultseven/` route returns 404, the root page now represents the currently published regular cycle, and both the current regular page and the legacy supplementary page require a session-bound image security code. The app therefore keeps a hidden WebView for the examination-site session, fills the cached USN, displays only the site's security image in native UI, submits the user-entered code in that same session, parses the returned table, and renders native result cards. It caches a successful parsed result by USN and source; reopening is instant, while the refresh action deliberately requests a new live result.

Do not attempt to solve or bypass the examination site's security code. If upstream changes again, update the URLs, selectors, and HTML parser in `lib/Services/exam_result_scraper.dart` and keep the WebView/session boundary intact.
