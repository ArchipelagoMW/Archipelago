# MMRecompRando

This is an Archipelago randomizer mod for Majora's Mask: Recompiled with both Singleplayer and Multiworld support.

## Disclaimer

This randomizer is still under development in the beta phase but is considered stable for playing. You may encounter features that are not finished yet or errors. Be sure to check the Issues page and report anything you encounter there.

## Setup

> [!IMPORTANT]
> To install mods (including MMRecompRando), drag and drop the downloaded mod zip onto the Zelda64Recomp window before you press "Start Game" and the game will handle extracting and installing the mods for you.

### Mod Installation
1. Download the latest [Visual Studio C++ Redist](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170#latest-microsoft-visual-c-redistributable-version).
2. Download [Zelda64Recomp](https://github.com/Zelda64Recomp/Zelda64Recomp/releases/latest).
3. Download [MMRecompRando.zip](https://github.com/RecompRando/MMRecompRando/releases/latest).
4. Optionally download any additional mods or texture packs you'd like from [Thunderstore](https://thunderstore.io/c/zelda-64-recompiled/).
    - You only need to drag and drop mod zips from GitHub or Thunderstore onto the game window to install them.
5. You can also download [poptracker](https://github.com/black-sliver/PopTracker/releases/latest) along with [G4M3RL1F3's fork of Seto's pack](https://github.com/G4M3RL1F3/Majoras-Mask-AP-PopTracker-Pack/releases/latest)
6. Open `Zelda64Recompiled`.
    1. Select your ROM file.
    2. Install MMRecompRando and any additional mods.
    3. Select Start Game.
7. Go nuts.

### Solo Setup
1. Launch the game with the randomizer mod enabled.
2. Select `Solo` in the randomizer menu.
3. Create a new session and choose which settings you'd like.
    - Details about these settings are currently not available through the mod only, you will have to look at the [multiworld's example YAML](https://github.com/RecompRando/MMRecompRando/releases/download/v0.9.5/EXAMPLE_YAML.yaml) for more information on what each setting does.
4. Hit `Generate` and select your seed.

### Multiworld Setup
1. Launch the game with the randomizer mod enabled.
2. Select `Multiworld` in the randomizer menu.
3. Input your Server Address, Player/Slot Name, and optionally a Password.
4. Hit `Connect`.
5. Profit.

### Multiworld Archipelago Setup
1. Know [Archipelago](https://archipelago.gg/tutorial/Archipelago/setup/en).
2. Download the [apworld](https://github.com/RecompRando/MMRecompRando/releases/latest).
3. **MAKE SURE** to clear out _any_ apworlds named `mm-recomp.apworld` or `mm_recomp.apworld` from your `Archipelago/lib/worlds` folder and your `Archipelago/custom_worlds` folder.
4. Place the apworld into `Archipelago/custom_worlds/`.
5. Generate a multiworld, and host the game either locally or on the website.

## FAQ

### I launched this mod and my save is gone? Did rando delete my save?

Don't worry, your vanilla saves are intact. When playing this mod, a per-session savefile will be created. Your normal save file will not be touched.

### I got Letter to Kafei and now I can't use the Pendant of Memories! Is it just gone?

Try moving your cursor to the Letter to Kafei and pressing the N64's L or A button. That should cycle through all quest items in that slot. That's true for the Moon's Tear item slot and the Room Key item slot as well.

### I opened a chest/got a check and it always shows a grey Archipelago item, what's wrong with you?

The phantom AP item means either something went wrong with your connection or the check is not yet implemented. Please use a text client or Seto's/G4M3RL1F3's amazing poptracker pack from step 5 to see checks that you can definitely get (though some implemented checks may be missing until the tracker is updated).

If you picked up a phantom on a check that should be implemented, you can open an issue on this repo letting us know!

## Known Issues

- Kotake sometimes does not show the price of her shopsanity item in the second dialogue.
- When using mod version 0.9.5, the game will crash when connecting to a seed generated on version 0.9.4 or below. Until this is properly addressed, a temporary solution is to downgrade the mod to [0.9.4](https://github.com/RecompRando/MMRecompRando/releases/tag/v0.9.4).

## Credit for additional mods included

Thank you to the original authors of some of the other recomp mods used!

- ThatHypedPerson (Color Mods)
- danielryb (Better SoDT, Z-Target Fix, Song Utils)

## Writing mods
See [this document](https://hackmd.io/fMDiGEJ9TBSjomuZZOgzNg) for an explanation of the modding framework, including how to write function patches and perform interop between different mods.

## Tools
You'll need to install `clang` and `make` to build rando.
* On Windows, using [chocolatey](https://chocolatey.org/) to install both is recommended. The packages are `llvm` and `make` respectively.
* On MacOS, these can both be installed using Homebrew, as well as `zip`. Apple clang won't work, as you need a mips target for building the mod code.
* On Linux, install the above packages, and some additional ones: `clang`, `make`, `llvm`, `lld`, `zip`, using your distro's package manager.

You'll also need to build [N64Recomp](https://github.com/N64Recomp/N64Recomp) for the `RecompModTool` utility, and copy it into your clone of rando (or put it on your PATH).

## Building
* First, make sure you've cloned the repo recursively `git clone https://github.com/RecompRando/MMRecompRando --recurse-submodules` or you can update the submodules afterwards `git submodule update --init --recursive`.
* Then, run `make` (with an optional job count) to build the mod code itself.
