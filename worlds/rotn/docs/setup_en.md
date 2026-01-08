# Setup Guide
## Requirements
- [Rift of the Necrodancer](https://store.steampowered.com/app/2073250/Rift_of_the_NecroDancer/) from Steam
- [RiftArchipelago](https://github.com/studkid/RiftArchipelago/releases) mod from the github releases.

## Installation
1. Download and extract the RiftArchipelago.zip file into the Rift of the Necrodancer installation folder.  This folder can be found by right clicking on Rift of the Necrodancer on steam and navigating Manage -> Browse Local files.
2. **Linux Only**: Right click Rift of the Necrodancer on steam and open up properties.  In the Launch Options, add `WINEDLLOVERRIDES="winhttp.dll=n,b" %command%`.
3. On the title screen there should now be a connection window on the top corner to input your server info.

If for whatever reason the bundled version of BepInEx doesn't work you can try installing it manually from [BepInEx's releases page](https://github.com/BepInEx/BepInEx/releases/tag/v5.4.23.2).