Berserker's Multiworld Utilities for Bonta's Multiworld
=======================================================

This is a complete fork of Bonta's Multiworld V31, which assumes you already know how to setup and use that project. Instructions here are only for the additions.
This is a drop-in replacement with everything from Bonta's Multiworld included.
You can find a guide here: https://docs.google.com/document/d/1r7qs1-MK7YbFf2d-mEUeTy2wHykIf1ALG9pLtVvUbSw/edit#

Additions/Changes
-----------------

Project
 * Compatible with Python 3.7 and 3.8. Potentially future versions as well.
 * Update modules if they are too old, preventing a crash when trying to connect among potential other issues
 * Autoinstall missing modules
 * Allow newer versions of modules than specified, as they will *usually* not break compatibility
 * Support for V31 extendedmsu
 
MultiMystery.py
 * Allows you to generate a Multiworld with individual player mystery weights. Since weights can also be set to 100%, this also allows for individual settings for each player in a regular multiworld.
Basis is a .yaml file that sets these weights. You can find an easy.yaml in this project folder to get started.
 * Additional instructions and settings are at the start of the file. Open with a text editor.
 
 MultiServer.py
  * Added a try/except to prevent malformed console commands from crashing the entire server
  * /forfeitplayer Playername now works when the player is not currently connected
  * Added /hint command on the server (use just /hint for help on command)  
can be used as /hint Playername Itemname  
All Itemnames can be found in Items.py starting at line 25  
example:  
/hint Berserker Progressive Sword  
Notice (Team #1): [Hint]: Berserker's Progressive Sword can be found in Hype Cave - Top in ahhdurr's World  
Notice (Team #1): [Hint]: Berserker's Progressive Sword can be found in Blind's Hideout - Far Right in Schulzer's World  
Notice (Team #1): [Hint]: Berserker's Progressive Sword can be found in Palace of Darkness - Map Chest in Thorus's World  
Notice (Team #1): [Hint]: Berserker's Progressive Sword can be found in Ganons Tower - Map Chest in Will's World  

Mystery.py
 * Defaults to generating a non-race ROM (Bonta's only makes race ROMs at this time)
If a race ROM is desired, pass --create-race as argument to it
 * When an error is generated due to a broken .yaml file, it now mentions in the error trace which file, line and character is the culprit
 * Option for progressive items, allowing you to turn them off (see easy.yaml for more info)
 * Rom-Option for extendedmsu (see easy.yaml for more info)

 
