# Chrono Trigger: Jets of Time

## Where is the settings page?

Settings for Jets of Time are handled by a multiworld variant of the main Jet of Time web generator. 
Game modes and settings are documented in depth on the Jet of Time wiki.

The ROM and YAML generated from the multiworld site are a pair and must be used together.  Unlike most other
Archipelago games, a new YAML/ROM pair must be generated for each multiworld session.  If one of the files is 
accidentally lost or deleted, they can be re-downloaded from `https://multiworld.ctjot.com/share/share_id` 
where share_id is the fifteen character ID located in the filename.

Links: 
 - [CTJoT Multiworld Generator](https://multiworld.ctjot.com/)
 - [CTJoT Wiki: Main Page](https://wiki.ctjot.com/)
 - [CTJoT Wiki: Multiworld](https://wiki.ctjot.com/doku.php?id=multiworld)
 - [CTJoT Wiki: Settings](https://wiki.ctjot.com/doku.php?id=flags)

## What does randomization do to this game?

Jets of Time turns Chrono Trigger into a much more open world experience.  The player stars with two characters
and the winged Epoch and must hunt for additional characters and key items to open the way to Lavos.

The following elements are randomized based on chosen settings:
  - Key item locations
  - Character recruitments (including duplicate characters)
  - Boss locations
  - Treasure chests
  - Shop inventory and prices
  - Enemy drops/charms
  - Tech order
  - Tab stat growth
  - Gear and healing item stats

## What Chrono Trigger items can appear in other players' worlds?

Key items, gear, and consumables can be shuffled into other players' worlds.  Bucket fragments are also
shuffled into other players' worlds if that setting is chosen.  

## What does receiving an item from another world look like?
An in-game text box will display any items that are received by the player and the item will 
be added to the player's inventory.  Received items are also listed in the client console.

## What does another world's item look like in Jets of Time?

Completing checks or opening chests will award the player a new "APItem".  This will happen even if the
item is for the player's own world.  The actual item will then be displayed in the client console and
sent to the appropriate player.  

## Known Issues/Limitations

1. Items will not be delivered on the overworld.
2. Items can be delivered in many, but not all locations. If you see on the client that you received an item 
   but it isn't being delivered, it probably means the map you are on does not support item delivery. 
   Keep playing and you'll get it eventually.
3. If you receive an item while in the middle of a cutscene, do not move. Receiving an item can return control 
   to the player at unintended times, and moving where the game doesn't expect you to be can cause problems 
   with cutscenes.
4. When finding an APItem for yourself, sometimes the client can send the item before the treasure text shows 
   up from the chest. This will cause the treasure chest text to say that you received the item itself rather 
   than the APItem, followed by the client delivering the item. This looks a little funny, but the item is only 
   actually received once.
5. If you receive an item while standing on a save point, pressing A will open the save menu instead 
   of closing the text box, causing the player to get stuck on the save point. If this happens, hold a direction 
   away from the save point and tap A for one frame.



