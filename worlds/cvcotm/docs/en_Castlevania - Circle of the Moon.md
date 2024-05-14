# Castlevania: Circle of the Moon

## Quick Links
- [Setup](../setup/en)
- [Options Page](../player-options)
- [PopTracker Pack](https://github.com/sassyvania/Circle-of-the-Moon-Rando-AP-Map-Tracker-/releases/latest)
- [Repo of the original non-Archipelago version of this randomizer](https://github.com/calm-palm/cotm-randomizer)
- [Web version of the above randomizer](https://rando.circleofthemoon.com/)

## What does randomization do to this game?

All items that you would normally find on pedestals throughout the game have had their locations changed. In addition to
magic items and stat max ups, the DSS Cards have been added to the item pool as well; you will now receive these as randomized
items rather than by farming them via enemy drops.

## What is the goal of Castlevania: Circle of the Moon when randomized?

Depending on what was chosen for the `completion_goal` option, your goal may be to defeat Dracula, complete the Battle Arena, or both.

- `dracula`: Make it to the Ceremonial Room and kill Dracula's first and second forms to view the credits. The door to the
Ceremonial Room can be set to require anywhere between 0-9 Last Keys to open it. If `require_all_bosses` is enabled, 8 keys
will be required, and they will be guaranteed to be placed behind all 8 bosses (that are not Dracula).
- `battle_arena`: Survive every room in the Battle Arena and pick up the Shinning Armor on the pedestal at the end. To make it
easier, the `disable_battle_arena_mp_drain` option can be enabled to make the Battle Arena not drain your MP to 0, allowing
DSS to be used. Reaching the Battle Arena in the first place requires finding the Heavy Ring and Roc Wing.
- `battle_arena_and_dracula`: Complete both of the above-mentioned objectives. The server will remember which ones (if any) were
already completed on previous sessions upon connecting.

## What items and locations get shuffled?

Stat max ups, magic items, and DSS Cards are all randomized into the item pool, and the check locations are the pedestals
that you would normally find the first two types of items on.

The sole exception is the pedestal at the end of the Battle Arena. This location will always have Shinning Armor regardless
of the chosen options.

## Which items can be in another player's world?

Stat max ups, magic items, and DSS Cards can all be placed into another player's world.

The Shinning Armor is not randomized; it will always be found at the end of the Battle Arena in your own world.
And depending on your goal, you may or may not be required to pick it up.

## What does another world's item look like in Castlevania: Circle of the Moon?

All items from other worlds will show up as the unused Map magic item. In-game, it does nothing when picked up besides setting
the flag for the location so that the client can detect and send the location check.

Upon sending an item, a textbox announcing the item being sent and the player who it's for will show up on-screen, accompanied
by a sound depending on whether the item is filler, progression/useful, or trap-classified.

## When the player receives an item, what happens?

A textbox announcing the item being received and the player who sent it will pop up on-screen, and it will be received.
Similar to the outgoing item textbox, it will be accompanied by a sound depending on the item received being filler or progression/useful.

## What are the item name groups?
When you attempt to hint for items in Archipelago you can use either the name for the specific item, or the name of a group
of items. Hinting for a group will choose a random item from the group that you do not currently have and hint for it. The
groups you can use for Castlevania: Circle of the Moon are as follows:

* `DSS` or `Card`: Any DSS Card of either type.
* `Action` or `Action Card`: Any Action Card.
* `Attribute` or `Attribute Card`: Any Attribute Card.
* `Freeze`: Any card that logically lets you freeze enemies to use as platforms.
* `Action Freeze`: Either Action Card that logically lets you freeze enemies.
* `Attribute Freeze`: Either Attribute Card that logically lets you freeze enemies.

## What are the location name groups?
In Castlevania: Circle of the Moon, every location is part of a location group under that location's area name.
So if you want to exclude all of, say, Underground Waterway, you can do so by just excluding "Underground Waterway" as a whole.

## Why do magic items sometimes look glitched?
This is to do with the fact that the magic item's graphics cannot be loaded at the same time as some special action objects
that might be in that same room, such as crumbling platforms and push/tackle blocks. It will still function as expected when
picked up, it just looks weird.

## Will the Castlevania Advance Collection and/or Wii U Virtual Console versions work?

The Castlevania Advance Collection ROM is tested and known to work. However, there are some major caveats when playing with the
Advance Collection ROM; most notably the fact that the audio does not function when played in an emulator outside the collection,
which is currently a requirement to connect to a multiworld. This happens because all audio code was stripped
from the ROM, and all sound is instead played externally through the collection itself.

For this reason, it is most recommended to acquire the ROM by dumping it from an original cartridge of the game that you legally own.
Though, the Advance Collection *can* still technically be an option if you cannot do that and don't mind the lack of sound.

The Wii U Virtual Console version is currently untested. If you happen to have purchased it before the Wii U eShop shut down, you can try
dumping and playing with it. However, at the moment, we cannot guarantee that it will work well due to it being untested.

Regardless of which released ROM you intend to try playing with, the US version of the game is required.
