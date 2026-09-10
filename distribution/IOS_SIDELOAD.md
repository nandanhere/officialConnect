# Install OfficialConnect on an iPhone

This package contains OfficialConnect **1.1.0 (build 7)** for iPhones running
**iOS 15 or later**. No jailbreak is required.

## What you send

- `OfficialConnect-unsigned.ipa`
- This guide
- `SHA256SUMS.txt`, which can be used to verify that the IPA was copied intact

The distributed `OfficialConnect-unsigned.ipa` contains the app but no shared
signing identity. Each user signs it locally with their own Apple account.
OfficialConnect itself never receives those Apple credentials; the selected
installer and Apple handle signing.

> Why unsigned? A free Apple account can only sign apps for devices registered
> to that account, so a build signed by the developer would refuse to install
> on anyone else's iPhone. Self-signing with AltStore is the zero-cost route;
> a paid Apple Developer Program account enables pre-signed ad-hoc builds and
> TestFlight instead.

## Windows quick start (recommended for most users)

1. Install AltServer for Windows from <https://altstore.io/> only.
2. Follow the official guide at
   <https://faq.altstore.io/altstore-classic/how-to-install-altstore-windows>.
   It currently requires Apple's iTunes
   and iCloud installers **from apple.com (not the Microsoft Store)** and a
   USB connection for the initial setup.
3. Install AltStore on the iPhone: click the AltServer icon in the Windows
   system tray → **Install AltStore** → pick the iPhone, and sign in with your
   Apple ID when asked.
4. On the iPhone, enable **Settings → Privacy & Security → Developer Mode**
   (restart when iOS asks), then under
   **Settings → General → VPN & Device Management** trust your Apple ID's
   developer profile.
5. Save `OfficialConnect-unsigned.ipa` to iCloud Drive or another location
   visible in the iPhone Files app.
6. In AltStore on the iPhone, open **My Apps**, tap **+**, and select the IPA
   from Files. AltStore signs it with your Apple ID and installs it.

Free Apple accounts issue seven-day development provisioning and ordinarily
allow three active sideloaded apps. AltStore
refreshes the app before it expires whenever the phone can reach AltServer
on the same network. This is an Apple platform limitation, not an
OfficialConnect login requirement.

### Troubleshooting

- **"Untrusted Developer" when opening the app** — step 4 (trust the profile)
  is incomplete; the phone must be online when you tap Trust.
- **AltServer can't see the iPhone** — use the Apple (non-Microsoft-Store)
  iTunes/iCloud installs, keep the phone unlocked, and accept the Trust
  prompt on the phone.
- **App stops opening after a week** — open AltStore on the same Wi-Fi as the
  PC running AltServer and tap Refresh, or just re-open AltStore and it
  refreshes in the background.

## macOS

The same AltStore flow works on macOS. Follow
<https://faq.altstore.io/altstore-classic/how-to-install-altstore-macos>, then
choose this IPA from AltStore's **My Apps** page. A developer can alternatively
install directly from source:

1. Connect the iPhone, trust the Mac, and enable Developer Mode.
2. Open `ios/Runner.xcworkspace` in Xcode.
3. Select a personal or paid Development Team under **Signing & Capabilities**.
4. Select the connected iPhone and press **Run**.

The first trust and pairing generally needs a cable. After Xcode has paired the
phone, enable **Connect via network** in Xcode's Devices and Simulators window
to run future development builds wirelessly while both devices are reachable.

For a paid Apple Developer Program account, an ad-hoc IPA can instead be built
for registered device IDs. Those users do not need to re-sign the IPA locally,
but every target iPhone must be included in the provisioning profile.

## Build the unsigned IPA

From the repository root on a Mac with Xcode installed:

```sh
./scripts/build_ios_sideload.sh
```

The package is written to the workspace `outputs` folder. Never include a
developer certificate, private key, provisioning profile, Apple password, or
student login details in the distribution ZIP.

## Safety and privacy

- Do not send your Apple ID password, verification code, student details, or
  portal cookies to the person who shared this ZIP.
- AltServer needs your Apple ID only to ask Apple to sign the app for your own
  device. OfficialConnect does not receive that Apple ID.
- The app stores its portal login details locally so it can refresh. Use the
  app's sign-out/clear-login controls before giving the phone to someone else.
- Verify the download if desired: on Windows run
  `certutil -hashfile OfficialConnect-unsigned.ipa SHA256`; on macOS run
  `shasum -a 256 OfficialConnect-unsigned.ipa`. The result should match
  `SHA256SUMS.txt`.
