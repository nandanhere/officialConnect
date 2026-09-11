# Release hardening plan

This document is the acceptance checklist for the first release after the
portal-login migration. It deliberately separates app availability from
individual data sources: a broken portal section must not blank unrelated
cached information or require an emergency app-store release.

## Runtime controls

- Automatic refresh, portal sync, each portal section, regular results, and
  supplementary results can be disabled independently through Firebase Remote
  Config.
- Defaults are safe when Firebase is unreachable; a remotely disabled feature
  leaves cached information visible and explains that the source is
  temporarily unavailable.
- Remote values are operational switches only. They must never contain student
  identifiers, credentials, cookies, or scraped content.

## Observability

- Crashlytics records uncaught Flutter and native crashes by app version.
- Analytics records bounded outcomes for login, sync, parser sections, cached
  fallback, and result retrieval.
- Event parameters are allow-listed. Do not send USN, DOB, verification digits,
  names, contact details, cookies, URLs containing session tokens, or HTML.
- Rollout review uses outcome rates and durations, not raw student data.

## Data resilience

- Every scraper section is parsed independently.
- A section failure preserves the last successful cached version while other
  successful sections update normally.
- Anonymized HTML fixtures cover current, partial, empty, and structurally
  changed portal responses.

## User experience

- Refresh keeps cached screens, navigation, and gestures interactive.
- A compact global status communicates updating, success, partial success, or
  failure without a modal loading page.
- Light/dark themes, large text, long names/codes, small screens, empty data,
  and partial data have automated widget coverage.

## Android release checks

- Target and compile SDK meet the current Play requirement.
- Android 15+ edge-to-edge insets are handled.
- Native libraries are checked for 16 KB page alignment.
- A signed release bundle is built and validated before upload.
- The previous production source remains reproducibly buildable as an
  emergency higher-version recovery release.

## Staged rollout gates

1. Upload to internal testing and verify fresh login, cached upgrade, refresh,
   partial portal failure, regular results, and supplementary results.
2. Start production at 25% only when the upload key is active and the internal
   build passes.
3. Hold for at least 24 hours and inspect login/sync outcomes, Crashlytics,
   Android vitals, and support feedback.
4. Halt on a material regression. Use Remote Config first when the defect is
   isolated to a remotely controlled source.
5. Advance to 50%, then 100%, only after another healthy observation window at
   each stage.

## Rollback readiness

- During staged rollout, halt the release to stop additional users receiving
  it. Users already updated remain on that version.
- For a client-side defect, build the known production baseline with a version
  code higher than the failed candidate and publish it as the recovery release.
- For a portal/source defect, disable only the affected capability and keep
  showing cached or partial data while a parser fix is prepared.
