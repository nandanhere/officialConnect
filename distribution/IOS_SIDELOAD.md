# Install OfficialConnect on an iPhone

## What you send

- `OfficialConnect-unsigned.ipa` (in this folder / the project `outputs/`)
- A link to this guide

The distributed `OfficialConnect-unsigned.ipa` contains the app but no shared
signing identity. Each user signs it locally with their own Apple account.
OfficialConnect itself never receives those Apple credentials; the selected
installer and Apple handle signing.

> Why unsigned? A free Apple account can only sign apps for devices registered
> to that account, so a build signed by the developer would refuse to install
> on anyone else's iPhone. Self-signing with AltStore is the zero-cost route;
> a paid Apple Developer Program account enables pre-signed ad-hoc builds and
> TestFlight instead.

## Windows (recommended route)

1. Install AltServer for Windows from <https://altstore.io/>.
2. Follow AltStore's Windows setup guide. It currently requires Apple's iTunes
   and iCloud installers **from apple.com (not the Microsoft Store)** and a
   USB connection for the initial setup.
3. Install AltStore on the iPhone: click the AltServer icon in the Windows
   system tray → **Install AltStore** → pick the iPhone, and sign in with your
   Apple ID when asked.
4. On the iPhone, enable **Settings → Privacy & Security → Developer Mode**
   (restart when iOS asks), then under
   **Settings → General → VPN & Device Management** trust your Apple ID's
   developer profile.
5. Save `OfficialConnect-unsigned.ipa` to the PC, then copy it to the iPhone
   (iTunes File Sharing into AltStore, iCloud Drive, or email it to yourself).
6. In AltStore on the iPhone, open **My Apps**, tap **+**, and select the IPA
   from Files. AltStore signs it with your Apple ID and installs it.

Free Apple accounts issue seven-day development provisioning. AltStore
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

The same AltStore flow works on macOS. A developer can also install directly:

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
