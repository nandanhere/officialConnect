# Analytics Access Runbook (GA4 + Firebase)

Goal: anyone's analytics access never depends on one person. Two co-admins
can grant read access to new contributors; leavers get removed the same way.

## Role design

| Role | Who | Can do |
|---|---|---|
| Administrator (GA4 property) | You + 2 trusted students | Grant/revoke any role, manage data settings |
| Viewer (GA4 property) | Every other contributor | Read all reports and explorations |
| Analyst (GA4 property) | Contributors on the analytics track | Viewer + create/share explorations |
| Firebase Viewer (GCP IAM) | Contributors needing Crashlytics | Read crashes and performance data |

Nobody outside co-admins gets Editor/Marketer. The service-account key
(`ga4-key.json`) stays with automation only — humans use their own Google
accounts, never the key.

## Granting read access (any co-admin can do this)

GA4 reporting access:
1. GA4 → Admin → **Property access management** (unofficialconnect property).
2. **Add users** → contributor's Google email → role **Viewer** (or
   **Analyst** for analytics-track contributors) → Add.

Crashlytics/Performance access:
1. Google Cloud Console → IAM & Admin → **IAM** (project behind the app).
2. **Grant access** → contributor's email → role **Firebase Viewer** → Save.

Tell the contributor both grants exist; most only need the GA4 one.

## Promoting a co-admin

Only an existing Administrator does this, and only after the contributor has
merged analytics work for ~2 months:
1. Same Property access management screen → new co-admin → **Administrator**.
2. Record the change (date + who approved) in the team notes.

Never have fewer than 2 or more than 3 Administrators.

## Offboarding (graduation / stepping away)

1. GA4 Property access management → remove the person.
2. GCP IAM → remove the person.
3. If they ever held the service-account key (they shouldn't), rotate it:
   Cloud Console → Service Accounts → create new key, update automation,
   delete the old key.

Do this the week they leave, not "later".

## Quarterly access review (15 minutes, any co-admin)

1. Export the member lists from both screens above.
2. Remove anyone who hasn't contributed in 6 months.
3. Confirm the Administrator count is 2–3.

## Future automation (not yet built)

- `daily-health` already runs the numbers; a weekly rollup mode plus a cron
  job can email/notify a digest (adoption, error rate, slowest sections,
  top crashes) so humans only open consoles on WARN/FAIL weeks.
- The digest must use the service account, never a human's login.
