# The Messenger

## Quick Links
- [Setup](../../../../tutorial/The%20Messenger/setup/en)
- [Settings Page](../../../../games/The%20Messenger/player-settings)
- [Courier Github](https://github.com/Brokemia/Courier)
- [The Messenger Randomizer Github](https://github.com/minous27/TheMessengerRandomizerMod)
- [The Messenger Randomizer AP Github](https://github.com/alwaysintreble/TheMessengerRandomizerModAP)
- [Jacksonbird8237's Item Tracker](https://github.com/Jacksonbird8237/TheMessengerItemTracker)
- [PopTracker Pack](https://github.com/alwaysintreble/TheMessengerTrackPack)

## What does randomization do in this game?

All items and upgrades that can be picked up by the player in the game are randomized. The player starts in the Tower of
Time HQ with the past section finished, all area portals open, and with the cloud step, and climbing claws already
obtained. You'll be forced to do sections of the game in different ways with your current abilities.

## What items can appear in other players' worlds?

* The player's movement items
* Quest and pedestal items
* Music Box notes
* The Phobekins
* Time shards
* Shop Upgrades
* Power Seals

## Where can I find items?

You can find items wherever items can be picked up in the original game. This includes:
* Shopkeeper dialog where the player originally gains movement items
* Quest Item pickups
* Music Box notes
* Phobekins
* Bosses
* Shop Upgrades, Money Wrench, and Figurine Purchases
* Power seals
* Mega Time Shards

## What are the item name groups?

When you attempt to hint for items in Archipelago you can use either the name for the specific item, or the name of a
group of items. Hinting for a group will choose a random item from the group that you do not currently have and hint
for it. The groups you can use for The Messenger are:
* Notes - This covers the music notes
* Keys - An alternative name for the music notes
* Crest - The Sun and Moon Crests
* Phobekin - Any of the Phobekins
* Phobe - An alternative name for the Phobekins

## Other changes

* The player can return to the Tower of Time HQ at any point by selecting the button from the options menu
  * This can cause issues if used at specific times. Current known:
    * During Boss fights
    * After Courage Note collection (Corrupted Future chase)
      * This is currently an expected action in logic. If you do need to teleport during this chase sequence, it
        is recommended to quit to title and reload the save
* After reaching ninja village a teleport option is added to the menu to reach it quickly
* Toggle Windmill Shuriken button is added to option menu once the item is received
* The mod option menu will also have a hint item button, as well as a release and collect button that are all placed when
  the player fulfills the necessary conditions.
* After running the game with the mod, a config file (APConfig.toml) will be generated in your game folder that can be
  used to modify certain settings such as text size and color. This can also be used to specify a player name that can't
  be entered in game.

## Known issues
* Ruxxtin Coffin cutscene will sometimes not play correctly, but will still reward the item
* If you receive the Magic Firefly while in Quillshroom Marsh, The De-curse Queen cutscene will not play. You can exit
  to Searing Crags and re-enter to get it to play correctly.
* Sometimes upon teleporting back to HQ, Ninja will run left and enter a different portal than the one entered by the
  player. This may also cause a softlock.
* Text entry menus don't accept controller input
* Opening the shop chest in power seal hunt mode from the tower of time HQ will softlock the game.
* If you are unable to reset file slots, load into a save slot, let the game save, and close it.

## What do I do if I have a problem?

If you believe something happened that isn't intended, please get the `log.txt` from the folder of your game installation
and send a bug report either on GitHub or the [Archipelago Discord Server](http://archipelago.gg/discord)
