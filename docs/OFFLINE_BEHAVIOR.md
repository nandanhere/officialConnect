# Offline behavior

OfficialConnect is cache-first after a successful portal login. Network access
is required to sign in, refresh portal information, retrieve an uncached latest
result, open external links, and load images that were not previously cached.

## Expected behavior

- **First launch:** the login screen remains usable, but login cannot complete
  without access to the portal.
- **Returning user:** the last valid portal snapshot opens from local storage.
  Home, attendance, prior semester results, and settings remain navigable.
- **Stale data:** cached data is shown rather than blocked. A failed refresh must
  not remove that snapshot.
- **Latest regular/supplementary result:** a successfully retrieved result is
  saved per USN and source and can be reopened offline. A source that has never
  been retrieved requires connectivity and its security-code flow.
- **Settings:** theme and diagnostics preferences are local. External payment,
  helpdesk, and feedback links still require another reachable app or network.
- **Student image:** the academic snapshot remains available; an image may be
  absent when the image cache was not populated before going offline.
- **Sign out:** academic cache is removed. Saved portal form suggestions remain
  until the user clears the saved USN from the login form.

## Limitations

The app does not currently display a dedicated offline banner or an age label
for cached data. It cannot perform a first-time login or refresh without a
connection. SharedPreferences stores the academic snapshot for availability;
it is not an encrypted database.

Automated coverage in `test/offline_functionality_test.dart` checks a clean
first launch, restoration and navigation of cached sections, and rendering a
cached examination result without waiting for a network response.
