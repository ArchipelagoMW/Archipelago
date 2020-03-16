Berserker's Multiworld Utilities for Bonta's Multiworld
=======================================================

This is a complete fork of Bonta's Multiworld V31, which assumes you already know how to setup and use that project. Instructions here are only for the additions.
This is a drop-in replacement with everything from Bonta's Multiworld included.
You can find a guide here: https://docs.google.com/document/d/1r7qs1-MK7YbFf2d-mEUeTy2wHykIf1ALG9pLtVvUbSw/edit#

Additions/Changes
-----------------

Project
 * Available in precompiled form for Windows 64Bit on [Releases](https://github.com/Berserker66/MultiWorld-Utilities/releases) page.
 * Compatible with Python 3.7 and 3.8. Potentially future versions as well.
 * Update modules if they are too old, preventing a crash when trying to connect among potential other issues
 * Autoinstall missing modules
 * Allow newer versions of modules than specified, as they will *usually* not break compatibility
 * Support for V31 extendedmsu
 * Has support for binary patching to allow legal distribution of multiworld rom files
 * Various performance improvements
 * Various crash fixes
 
MultiMystery.py
 * Allows you to generate a Multiworld with individual player mystery weights. Since weights can also be set to 100%, this also allows for individual settings for each player in a regular multiworld.
Basis is a .yaml file that sets these weights. You can find an [easy.yaml](https://github.com/Berserker66/MultiWorld-Utilities/blob/master/easy.yaml) in this project folder to get started.
 * Additional instructions are at the start of the file. Open with a text editor.
 * Configuration options in the host.yaml file.
 
 MultiServer.py
  * Added a try/except to prevent malformed console commands from crashing the entire server
  * Supports automatic port-forwarding, can be enabled in host.yaml
  * improved `!players` command, mentioning how many players are currently connected of how many expected and who's missing
  * /forfeitplayer Playername now works when the player is not currently connected
  * various commands, like /senditem and /hint use "fuzzy text matching", no longer requiring you to enter a location, player name or item name perfectly
  * Added /hint command on the server (use just /hint for help on command)  
can be used as /hint Playername Itemname  
All Itemnames can be found in Items.py starting at line 25  
example:  
/hint Berserker Progressive Sword  
Notice (Team #1): [Hint]: Berserker's Progressive Sword can be found in Hype Cave - Top in ahhdurr's World  
Notice (Team #1): [Hint]: Berserker's Progressive Sword can be found in Blind's Hideout - Far Right in Schulzer's World  
Notice (Team #1): [Hint]: Berserker's Progressive Sword can be found in Palace of Darkness - Map Chest in Thorus's World  
Notice (Team #1): [Hint]: Berserker's Progressive Sword can be found in Ganons Tower - Map Chest in Will's World  
 * A player-side hint command "!hint" also exists. It needs to be turned on in the host.yaml and is based on points.

Mystery.py
 * Defaults to generating a non-race ROM (Bonta's only makes race ROMs at this time)
If a race ROM is desired, pass --create-race as argument to it
 * When an error is generated due to a broken .yaml file, it now mentions in the error trace which file, line and character is the culprit
 * Option for progressive items, allowing you to turn them off (see easy.yaml for more info)
 * Rom-Option for extendedmsu (see easy.yaml for more info)
 * Option for "timer"
 * Supports new Meta-Mystery mode. Read [meta.yaml](https://github.com/Berserker66/MultiWorld-Utilities/blob/master/meta.yaml) for details.
 * Added `dungeonssimple` and `dungeonsfull` ER modes
 
MultiClient.py
 * Awaits a Qusb2snes connection when started, latching on when available
 * Terminal improvements
 * Running it with a patch file will patch out the multiworld rom and then automatically connect to the host that created the multiworld
 * Cheating is now controlled by the server and can be disabled through host.yaml
 
