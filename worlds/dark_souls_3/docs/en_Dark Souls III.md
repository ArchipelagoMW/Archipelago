# Dark Souls III

Game Page | [Items] | [Locations]

[Items]: /tutorial/Dark%20Souls%20III/items/en
[Locations]: /tutorial/Dark%20Souls%20III/locations/en

## What do I need to do to randomize DS3?

See full instructions on [the setup page].

[the setup page]: /tutorial/Dark%20Souls%20III/setup/en

## Where is the options page?

The [player options page for this game][options] contains all the options you
need to configure and export a config file.

[options]: ../player-options

## What does randomization do to this game?

1. All item locations are randomized, including those in the overworld, in
   shops, and dropped by enemies. Most locations can contain games from other
   worlds, and any items from your world can appear in other players' worlds.

2. By default, all enemies and bosses are randomized. This can be disabled by
   setting "Randomize Enemies" to false.

3. By default, the starting equipment for each class is randomized. This can be
   disabled by setting "Randomize Starting Loadout" to false.

4. By setting the "Randomize Weapon Level" or "Randomize Infusion" options, you
   can randomize whether the weapons you find will be upgraded or infused.

There are also options that can make playing the game more convenient or
bring a new experience, like removing equip loads or auto-equipping weapons as
you pick them up. Check out [the options page][options] for more!

## What's the goal?

Your goal is to find the four "Cinders of a Lord" items randomized into the
multiworld and defeat the boss in the Kiln of the First Flame.

## Do I have to check every item in every area?

Dark Souls III has about 1500 item locations, which is a lot of checks for a
single run! But you don't necessarily need to check all of them. Locations that
you can potentially miss, such as rewards for failable quests or soul
transposition items, will _never_ have items required for any game to progress.
The following types of locations are also guaranteed not to contain progression
items by default:

* **Hidden:** Locations that are particularly difficult to find, such as behind
  illusory walls, down hidden drops, and so on. Does not include large locations
  like Untended Graves or Archdragon Peak.

* **Small Crystal Lizards:** Drops from small crystal lizards.

* **Upgrade:** Locations that contain upgrade items in vanilla, including
  titanite, gems, and Shriving Stones.

* **Small Souls:** Locations that contain soul items in vanilla, not including
  boss souls.

* **Miscellaneous:** Locations that contain generic stackable items in vanilla,
  such as arrows, firebombs, buffs, and so on.

You can customize which locations are guaranteed not to contain progression
items by setting the `exclude_locations` field in your YAML to the [location
groups] you want to omit. For example, this is the default setting but without
"Hidden" so that hidden locations can contain progression items:

[location groups]: /tutorial/Dark%20Souls%20III/locations/en#location-groups

```yaml
Dark Souls III:
  exclude_locations:
  - Small Crystal Lizards
  - Upgrade
  - Small Souls
  - Miscellaneous
```

This allows _all_ non-missable locations to have progression items, if you're in
for the long haul:

```yaml
Dark Souls III:
  exclude_locations: []
```

## What if I don't want to do the whole game?

If you want a shorter DS3 randomizer experience, you can exclude entire regions
from containing progression items. The items and enemies from those regions will
still be included in the randomization pool, but none of them will be mandatory.
For example, the following configuration just requires you to play the game
through Irithyll of the Boreal Valley:

```yaml
Dark Souls III:
  # Enable the DLC so it's included in the randomization pool
  enable_dlc: true

  exclude_locations:
    # Exclude late-game and DLC regions
    - Anor Londo
    - Lothric Castle
    - Consumed King's Garden
    - Untended Graves
    - Grand Archives
    - Archdragon Peak
    - Painted World of Ariandel
    - Dreg Heap
    - Ringed City

    # Default exclusions
    - Hidden
    - Small Crystal Lizards
    - Upgrade
    - Small Souls
    - Miscellaneous
```

## Where can I learn more about Dark Souls III locations?

Location names have to pack a lot of information into very little space. To
better understand them, check out the [location guide], which explains all the
names used in locations and provides more detailed descriptions for each
individual location.

[location guide]: /tutorial/Dark%20Souls%20III/locations/en

## Where can I learn more about Dark Souls III items?

Check out the [item guide], which explains the named groups available for items.

[item guide]: /tutorial/Dark%20Souls%20III/items/en

## What's new from 2.x.x?

Version 3.0.0 of the Dark Souls III Archipelago client has a number of
substantial differences with the older 2.x.x versions. Improvements include:

* Support for randomizing all item locations, not just unique items.

* Support for randomizing items in shops, starting loadouts, Path of the Dragon,
  and more.

* Built-in integration with the enemy randomizer, including consistent seeding
  for races.

* Support for the latest patch for Dark Souls III, 1.15.2. Older patches are
  *not* supported.

* Optional smooth distribution for upgrade items, upgraded weapons, and soul
  items so you're more likely to see weaker items earlier and more powerful
  items later.

* More detailed location names that indicate where a location is, not just what
  it replaces.

* Other players' item names are visible in DS3.

* If you pick up items while static, they'll still send once you reconnect.
 
However, 2.x.x YAMLs are not compatible with 3.0.0. You'll need to [generate a
new YAML configuration] for use with 3.x.x.

[generating a new YAML configuration]: /games/Dark%20Souls%20III/player-options

The following options have been removed:

* `enable_boss_locations` is now controlled by the `soul_locations` option.

* `enable_progressive_locations` was removed because all locations are now
  individually randomized rather than replaced with a progressive list.

* `pool_type` has been removed. Since there are no longer any non-randomized
  items in randomized categories, there's not a meaningful distinction between
  "shuffle" and "various" mode.

* `enable_*_locations` options have all been removed. Instead, you can now add
  [location group names] to the `exclude_locations` option to prevent them from
  containing important items.

  [location group names]: /tutorial/Dark%20Souls%20III/locations/en#location-groups

  By default, the Hidden, Small Crystal Lizards, Upgrade, Small Souls, and
  Miscellaneous groups are in `exclude_locations`. Once you've chosen your
  excluded locations, you can set `excluded_locations: unrandomized` to preserve
  the default vanilla item placements for all excluded locations.

* `guaranteed_items`: In almost all cases, all items from the base game are now
  included somewhere in the multiworld.

In addition, the following options have changed:

* The location names used in options like `exclude_locations` have changed. See
  the [location guide] for a full description.
