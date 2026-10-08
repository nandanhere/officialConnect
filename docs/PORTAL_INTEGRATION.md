# Portal integration notes

How OfficialConnect talks to MSRIT sites. Contributor reference — users
don't need this page.

OfficialConnect is an unofficial, on-device viewer. It is not affiliated
with or endorsed by MSRIT. Portal credentials never leave the device;
only parsed app JSON is kept in the local cache (see `docs/PRIVACY.md`).

## Parent-portal login

The portal login form uses `username` plus three date selectors. Format
examples (placeholders, not real data): `dd` values carry a trailing
space, `mm` is two digits, `yyyy` is the four-digit year. Changing
`yyyy` invokes the portal's `putdate()` function, which generates the
hidden password value.

The app-side WebView fills these controls and continues through the
portal's ordinary login and verification buttons. It must not fabricate
or bypass any server-side CAPTCHA/token validation.

Login details are cached locally to suggest them on the next launch.
Clearing the USN clears the saved login set. Future dates are rejected
as stale cache values. The date picker must preserve the user's selected
date; opening it must not overwrite it with today's date.

## On-device scraper

The app establishes the authenticated portal session in a WebView. On
the ordinary successful path the WebView stays mounted behind a native
progress screen, so users see app-owned status instead of portal UI. If
the portal ever needs an interactive step, the error state offers an
explicit **Open portal** fallback instead of failing silently.

Scraping runs inside that authenticated WebView, preserving the portal's
browser and network context. The scraper visits prerequisite
authenticated pages first and waits for page-specific content rather
than fixed delays. The retired AWS Lambda scraper and proctor service
are not part of the application architecture.

Diagnostic timing (API 35 emulator, 2026-09-08; varies with portal and
network latency): the optimized flow took ~14s for a repeat sync and
~11s for a cleared-cookie autofilled login, with ~3-4s in scraping.

## Examination results source

The **latest result** shortcuts are separate from the parent portal.
They use the MSRIT examination results site (`exam.msrit.edu`) and must
not be populated from cached parent-portal history.

The old server-side contract is invalid: the legacy route returns 404,
the root page now represents the currently published regular cycle, and
both the current regular page and the legacy supplementary page require
a session-bound image security code. The app keeps a hidden WebView for
the examination-site session, fills the cached USN, shows only the
site's security image in native UI, submits the user-entered code in
that same session, parses the returned table, and renders native result
cards. A successful parsed result is cached by USN and source for
instant reopening; refresh deliberately requests a new live result.

Do not attempt to solve or bypass the security code. If upstream
changes again, update the URLs, selectors, and HTML parser in
`lib/Services/exam_result_scraper.dart` and keep the WebView/session
boundary intact.
