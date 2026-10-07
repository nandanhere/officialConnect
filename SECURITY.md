# Security Policy

## Supported versions

Only the latest Play release (and `main`) receives fixes. Older versions
are unsupported — please update before reporting.

## Reporting a vulnerability

Do NOT open a public issue for security bugs. Instead, email the
maintainer (see the GitHub profile) with:

- What is affected (app version, screen/flow, or file).
- Steps to reproduce, with test credentials/data only — never real
  student credentials, portal sessions, or personal data.
- The impact you see.

You will get an acknowledgement within a few days. Please give the fix a
reasonable window to ship before disclosing publicly.

## Scope notes

- This app scrapes the MSRIT parent portal on-device with the user's own
  session. Reports about the portal's own security belong to MSRIT, not
  this repo — but tell us if the app mishandles portal data.
- Never submit real credentials, session tokens, or personal data in any
  report, issue, or PR. Redact first.
