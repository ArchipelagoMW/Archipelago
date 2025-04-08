## Soulslike Archipelago Location Naming Guide

This is a style guide for creating location names for "soulslike" games to hook up to Archipelago, based on the conventions arrived at for naming locations in _Dark Souls 3_, the first such game to be added to Archipelago. The names of all the DS3 locations can be found [on the locations page](https://archipelago.gg/tutorial/Dark%20Souls%20III/locations/en#detailed-location-descriptions), as can the [guide for understanding them](https://archipelago.gg/tutorial/Dark%20Souls%20III/locations/en#understanding-location-names).

### Structure of a Name

In general, location names should have three parts:

1. The region, an acronym of four or fewer letters indicating the general area the item is found. Since these games generally give explicit names to regions, it should follow those naming conventions. One example in DS3 is "HWL", for "High Wall of Lothric". Generally, each region should only have one acronym even if it changes over time or multiple parts open up over time. The region code in a location name *does not need to match* the region it's in according to Archipelago's logic, and in fact sometimes it shouldn't. (For example, `FS: Black Iron Helm - shop after killing Tsorig` is logically in Smoldering Lake because it can't be accessed until the player kills Tsorig, but because the item is actually retrieved in Firelink Shrine it still starts with `FS:`.)

2. The name of the item that was originally in this location. This is useful for two reasons. First, some locations have multiple items, such as drops that contain the entire outfit for a given armor set, and the Archipelago infrastructure need a way to distinguish between each location. Second, players familiar with the vanilla game will often remember where items are found (especially but not exclusively for unique items like weapons and spells), so this can be helpful information in finding the location.

3. A brief description of where in the region the item is located. This shouldn't be longer than a few words. To help keep it terse, it should freely use made-up names of sub-regions which are defined in detail in the game's location description page. This may be omitted only when the original item name clearly indicates its location, such as `HWL: Soul of the Dancer`.

These are combined in the form `<region>: <original item> - <description>`—for example, `HWL: Astora Straight Sword - fort walkway, drop down`.

### What makes a good description?

A good description should be:

* Terse. Five words on average, almost never longer than eight.
* All lower case except when referencing in-game proper nouns like NPC names or locations that are named in game.
* Not enemy-specific. Since enemies will likely be randomized as well, say "boss" or "miniboss" rather than listing specific boss names. If there are multiple bosses/minibosses in the region, disambiguate based on location (as in `LC: Irithyll Rapier - basement, miniboss drop`).
* Written with the assumption that the player knows the game in vanilla. It's not worth spending extra space explaining where an NPC is if they only show up in one place in a region.

#### Describing a region

It's rarely the case that the game itself names every feature in a region with enough detail to unambiguously represent every location. This means it's up to the Archipelago author to describe it themselves and give various parts names. Don't get too fancy with it—choose simple, descriptive, and where possible one-word names like "bridge", "basement", and "streets". It's fine to use multiple words when referring to a smaller part of a larger area or disambiguating two areas, like "settlement roofs" or "left island".

For games that have built-in compasses, use cardinal directions when referring to relative locations ("bridge north" or "south of island"). For games that don't, consider using the location documentation to define specific sides as "left", "right", "front", and "back" so you can refer to those instead.

Write up the location documentation as you define new terms—_don't_ wait until you're done writing all the location names, or you'll end up forgetting important details.

#### Common location patterns

* If an item is a reward for beating a boss, miniboss, or enemy, write "<enemy location> drop". For example, `IBV: Divine Blessing - great hall, mob drop` or `CC: Soul of a Demon - tomb, miniboss drop`.
* If a location is sold or given away by an NPC, just write that NPC's name (and location if they show up multiple places in the region).
* If an NPC only makes a location available after they receive a different item (such as a spellbook making new spells available), write `<NPC name> for <unlock item>`. For example, `FS: Chaos Storm - Cornyx for Izalith Tome`.
* If an NPC only makes a location available after a certain event, write `<NPC name> after <brief description of event>`. For example, `FS: Dancer's Armor - shop after killing LC entry boss`.
* For the specific case of boss soul items (or your game's equivalent), write `<NPC> for <short boss name>`. For example, `FS: Ludleth for Dancer`.
* Any time you need to refer to another region, use its acronym.