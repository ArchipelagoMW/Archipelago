Berserker's Multiworld Utilities for Bonta's Multiworld
=======================================================

This is a complete fork of Bonta's Multiworld V31, which assumes you already know how to setup and use that project. Instructions here are only for the additions.
This is a drop-in replacement with everything from Bonta's Multiworld included.

Additions/Changes
-----------------

MultiMystery.py
 * Allows you to generate a Multiworld with individual player mystery weights. Since weights can also be set to 100%, this also allows for individual settings for each player in a regular multiworld.
 * Basis is a .yaml file that sets these weights. You can find an easy.yaml in this project folder to get started.
 * Additional instructions and settings are at the start of the file. Open with a text editor.
 
 MultiServer.py
  * Added a try/except to prevent malformed console commands from crashing the entire server
  * Added /hint command on the server (use just /hint for help on command)
  * can be used as /hint Playername Itemname
  * All Itemnames can be found in Items.py starting at line 25
  * example  
/hint Berserker Progressive Sword  
Notice (Team #1): [Hint]: Berserker's Progressive Sword can be found in Hype Cave - Top in ahhdurr's World  
Notice (Team #1): [Hint]: Berserker's Progressive Sword can be found in Blind's Hideout - Far Right in Schulzer's World  
Notice (Team #1): [Hint]: Berserker's Progressive Sword can be found in Palace of Darkness - Map Chest in Thorus's World  
Notice (Team #1): [Hint]: Berserker's Progressive Sword can be found in Ganons Tower - Map Chest in Will's World  

Mystery.py
 * Defaults to generating a non-race ROM (Bonta's only makes race ROMs at this time)
 * If a race ROM is desired, pass --create-race as argument to it
 * When an error is generated due to a broken .yaml file, it now mentions in the error trace which file it is