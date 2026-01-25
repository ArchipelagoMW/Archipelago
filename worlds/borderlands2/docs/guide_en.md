# Borderlands 2 Setup Guide

## Setup for playing

### Requirements
1. You should have the latest [BL2 mod manager](https://github.com/bl-sdk/willow2-mod-manager) (3.7+) ([release page](https://github.com/bl-sdk/willow2-mod-manager/releases/tag/v3.7))

2. the latest version of [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) (0.6.4+) ([release page](https://github.com/ArchipelagoMW/Archipelago/releases/tag/0.6.4))

3. the sdk mod requires [coroutines](https://bl-sdk.github.io/willow2-mod-db/mods/coroutines/) (1.1+) ([direct download](https://github.com/juso40/bl2sdk-mods/raw/refs/heads/main/coroutines/coroutines.sdkmod))  
   place it into the sdk_mods folder. A browser window will open if you still need to install this.

For any GitHub Release Page, scroll to the bottom of the release notes to find the files you want (under "Assets"). Don't download the source code by accident.

### Installation
1. Download the borderlands2.apworld file and BouncyLootGod.sdkmod file from the [release page](https://github.com/EdricY/Bouncy-Loot-God/releases)
2. BouncyLootGod.sdkmod goes into `.../Steam/steamapps/common/Borderlands 2/sdk_mods/`
3. borderlands2.apworld goes into `.../Archipelago/custom_worlds/` OR use the `Install APWorld` tool from the Archipelago Launcher. Restart your Archipelago launcher after installing the apworld.

more information on [sdk mod setup](https://bl-sdk.github.io/willow2-mod-db/faq/)  
more information on [apworld](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/apworld%20specification.md)

### Options yaml
Pick and download a file from sample-yamls. Heavy editing to the sample is not encouraged unless you know what you're doing. More samples coming soon.

### Getting your multi world started
1. Place player yaml file(s): Archipelago Client > Browse Files > Players > insert yaml files here.
2. Generate world: Archipelago Client > Generate
3. The outputted .zip file is at Archipelago Client > Browse Files > output > `AP_<numbers>.zip`
4. Upload this .zip at https://archipelago.gg/uploads to create a room  
   OR host locally with Archipelago Client > Host (if you know what you're doing)

### Running the mod
Backup your BL2 characters before proceeding! They are located at Documents/my games/Borderlands 2/WillowGame/SaveData/...

With a multiworld running, Open "Borderlands 2 Client" from the Archipelago Launcher (restart the launcher if it's not there), connect to the multiworld. Then open Borderlands 2 and enable the mod.

Double check from the ingame mod menu that coroutines says version 1.1 and "Loaded".

If you open the game first, use the Mod Options menu to "Connect to Socket Server" once the Archipelago Client is open.

The mod is currently running the entire time it's enabled. Any character you "Continue" with will have their inventory checked.

If the game crashes when loading your character, please try disabling the mod, then loading your character, then enabling the mod from Esc > Mods > BouncyLootGod

**Before doing any non-archipelago play in Borderlands 2, Disable the mod and Restart your game!!!**

## FAQ
### I keep getting "client is not connected", what do I do?
Make sure you have followed the steps in [Requirements](#requirements) (check versions!). And make sure you open "Borderlands 2 Client" from the Archipelago launcher, not Text Client.  
Also try hitting the "Connect to Socket Server" button as well as disabling and re-enabling the mod.  
Another potential issue you can be running into is having multiple watcher loops running in game. The may happen if you quickly re-enabled the mod or connected the client after launching the game. To fix this, try disabling the mod, waiting 5 seconds, then re-enabling the mod.
### A browser window opens when I enable the mod, what do I do?
You need to install coroutines. see [step 3 in Requirements](#requirements)
### I can't deal damage and want to deal damage, what do I do?
You may add Melee to your beginning items. see [blsample.yaml](https://github.com/EdricY/Bouncy-Loot-God/blob/main/blsample.yaml)  
Include something like this in your yaml:
```
  start_inventory_from_pool:
    Melee: 1
```
### Why isn't x gun y rarity?
If you want specifics, currently "Unique" for guns specifically means Blue, Purple, or E-Tech with red text. "Unique" for other gear is checked against a specific list.  
Feel free to report these issues, but if it seems like a matter of opinion or you're just trying to flex your knowledge of Borderlands guns, you will be ignored. Ex. Gearbox white guns have been decided to be labeled White, not Unique. Blood of Terramorphous is considered Unique for now.

### The mission displays exp but I didn't get any?
When you receive a mission reward from the multiworld, it should give you no exp. If you don't open your menu within 5 seconds of receiving it in game, it may display the exp numbers without granting you that amount of experience.

### Can I use skill points before level 5?
You can but it's a little weird. It'll still have the greyed out look, but it works. Your skill trees will look normal again after level 5.

### I received a Travel item can I go there early?
No. You just won't be blocked when trying to travel there.

### Where do I report issues?
You can message in the Discord or create an issue on GitHub. Please try to check if you are reporting a known issue on either the [release page](https://github.com/EdricY/Bouncy-Loot-God/releases) or searching in Discord.

## Development stuff

For developing the sdkmod, this is probably useful. Development things here are specific to Windows 11.
I probably can't help with a non-Windows development environment.

.../Steam/steamapps/common/Borderlands 2/Binaries/Win32/Plugins/unrealsdk.user.toml
```
[pyunrealsdk]
debugpy = true
pyexec_root = "C:\\path\\to\\repo\\BouncyLootGod\\sdk_mods"

[mod_manager]
extra_folders = [
   "C:\\path\\to\\repo\\BouncyLootGod\\sdk_mods"
]

```
In the console, use `pyexec BouncyLootGod\__init__.py` to re-execute the mod code. (You may still need to disable/re-enable the mod.)

For developing the AP world, I don't have a good process haha... I just have the Archipelago project open in PyCharm and copy the files over to commit.  
You could probably create a symlink or something similar within Archipelago/custom_worlds to point to worlds/borderlands2 in this repo.

Alternatively, if you don't want to run the Archipelago codebase from source, generate the `.apworld` file and open it or add it to your installed version of the Archipelago Launcher. Now just test it like it's live.  
`python zip-it.py deployap` makes this even faster

Generation can be tested quickly with by running the exe from command line:
`C:\ProgramData\Archipelago\ArchipelagoGenerate.exe`  
or  
(cmd) `python zip-it.py deployap && timeout /t 5 && C:\ProgramData\Archipelago\ArchipelagoGenerate.exe`  
(bash) `python zip-it.py deployap && sleep 5 && /c/ProgramData/Archipelago/ArchipelagoGenerate.exe`

To test generation rules, one technique is to use plando. First, go to `C:\ProgramData\Archipelago\host.yaml` and set `plando_options` to `"items"` or `"bosses, items"`. Now add a testing placement to your player yaml such as...
```
  plando_items:
    - item: "Travel: Three Horns Divide"
      location: "Symbol SouthernShelfBay: Ice Flows Shipwreck"
      from_pool: true
      force: true
```
After generating, you can check the spoiler for if the rule was properly met.  
We might consider adding unit tests in the future.

To create files for release: `python zip-it.py`  
This puts borderlands2.apworld and BouncyLootGod.sdkmod into /dist, which are the files needed to play outside of development mode.


Trello Board:  
https://trello.com/b/y4WWZF3E/bl2-archipelago

