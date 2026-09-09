# Install OfficialConnect on an iPhone

The distributed `OfficialConnect-unsigned.ipa` contains the app but no shared
signing identity. Each user signs it locally with their own Apple account.
OfficialConnect itself never receives those Apple credentials; the selected
installer and Apple handle signing.

## Windows (recommended route)

1. Install AltServer for Windows from <https://altstore.io/>.
2. Follow AltStore's Windows setup guide. It currently requires Apple's iTunes
   and iCloud installers and a USB connection for the initial setup.
3. Install AltStore on the iPhone and enable Developer Mode when iOS asks.
4. Save `OfficialConnect-unsigned.ipa` to the PC.
5. In AltStore on the iPhone, open **My Apps**, tap **+**, and select the IPA
   from Files. Keep AltServer available on the same network for refreshes.

Free Apple accounts issue seven-day development provisioning. AltStore can
refresh the app before it expires when the phone can reach AltServer. This is
an Apple platform limitation, not an OfficialConnect login requirement.

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
