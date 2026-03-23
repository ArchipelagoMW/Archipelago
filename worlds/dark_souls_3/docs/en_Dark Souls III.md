# Dark Souls III

Game Page | [Setup] | [Items] | [Locations] | [Enemy Randomization]

[Setup]: /tutorial/Dark%20Souls%20III/setup/en
[Items]: /tutorial/Dark%20Souls%20III/items/en
[Locations]: /tutorial/Dark%20Souls%20III/locations/en
[Enemy Randomization]: /tutorial/Dark%20Souls%20III/enemy-randomization/en

## What do I need to do to randomize DS3?

See full instructions on [the setup page].

[the setup page]: /tutorial/Dark%20Souls%20III/setup/en

## How do I set options?

The DS3 client download includes an example YAML file which includes
documentation for every option Dark Souls III supports. Use this to customize
your experience.

**Note:** Some options in this YAML may not yet be available on the
archipelago.gg version of the Dark Souls III apworld, which is limited by the
Archipelago core code review/release cycle. For the absolute latest features,
use the `dark_souls_3.apworld` that's bundled with the client.

## What does randomization do to this game?

1. All item locations are randomized, including those in the overworld, in
   shops, and dropped by enemies. Most locations can contain games from other
   worlds, and any items from your world can appear in other players' worlds.

2. By default, all enemies and bosses are randomized. This can be disabled by
   setting `randomize_enemies: false` in your YAML.

3. By default, the starting equipment for each class is randomized. This can be
   disabled by setting `randomize_starting_loadout: false` in your YAML.

There are also options that can make playing the game more convenient or
bring a new experience. Check out the example YAML file for more information!

## What's the goal?

By default, your goal is to find the four "Cinders of a Lord" items randomized
into the multiworld and defeat the boss in the Kiln of the First Flame.

You can customize which bosses you fight by setting the `goal` option in your
YAML. For example, if you want to make both DLCs mandatory in addition to the
main game, you would use:

```yaml
Dark Souls III:
  goal:
  - Kiln of the First Flame Boss
  - Ringed City End Boss
  - Painted World of Ariandel End Boss
```

## Do I have to check every item in every area?

Dark Souls III has about 1500 item locations, which is a lot of checks for a
single run! But you don't necessarily need to check all of them. Locations that
you can miss permanently, such as rewards for failable quests or soul
transposition items, will _never_ have items required for any game to progress.
The following types of locations also won't contain progression items by
default:

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
still be included in the randomization pool, but none of the locations there
will be mandatory. For example, the following configuration just requires you to
play the game through Irithyll of the Boreal Valley:

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

## I'm sending too many items into the multiworld!

Because Dark Souls III has so many more checks than most Archipelago games, it
also sends many more items into the multiworld. If you're playing in a small
group, this may mean that most players' games are mostly full of items from DS3.
That's not ideal!

You can mitigate this by forcing certain item groups to be local, meaning that
those items will only ever be placed in your game and not anyone else's. For
example, the following configuration substantially limits how many items you'll
send out into the multiworld:

```yaml
Dark Souls III:
  local_items:
  - Armor
  - Miscellaneous
  - Small Souls
  - Upgrade
```

**Warning:** Because Archipelago places local items before placing progression
items, marking too many items as local can mean there's not enough room for all
the progression you need which can cause generation to fail. If you're getting a
lot of failures, try reducing the number of local items. Also consider adding
your 👍 to [this pull request] which would allow *locations* to be marked as
local instead of items!

[this pull request]: https://github.com/ArchipelagoMW/Archipelago/pull/3758

## Where can I learn more about Dark Souls III locations?

Location names have to pack a lot of information into very little space. To
better understand them, check out the [location guide], which explains all the
names used in locations and provides more detailed descriptions for each
individual location.

[location guide]: /tutorial/Dark%20Souls%20III/locations/en

## Where can I learn more about Dark Souls III items?

Check out the [item guide], which explains the named groups available for items.

[item guide]: /tutorial/Dark%20Souls%20III/items/en

## How can I change what enemies get randomized?

The [enemy randomization guide] explains how to further customize enemy randomization
for challenge runs or convenience. You can target specific enemies or entire
categories and even remove annoying enemy types outright.

[enemy randomization guide]: /tutorial/Dark%20Souls%20III/enemy-randomization/en

## What's new from 3.x.x?

Version 4.0.0 of the Dark Souls III Archipelago client has a number of
substantial differences with the older 3.x.x versions. Improvements include:

* It's built on Mod Engine 3, which is more reliable than Mod Engine 2 and
  is actively maintained.

* There's now a dedicated in-game Archipelago overlay which displays the
  Archipelago message log and allows the player to change their room URL
  settings in-game.

* There's better protection against issues like collecting items while
  disconnected from the server.

* Auto-equip is no longer supported.

In addition, 4.0.0 supports several new features. Some of these require using
the new `dark_souls_3.apworld` that's bundled with the 4.0.0 client in place of the
one that's included with Archipelago by default.

* The goal is now customizable. You can choose any boss or set of bosses to be
  required. The default is still just defeating Soul of Cinder.

* Death link is now more customizable. You can choose to only send death links
  when you die *without* picking up your souls. You can also enable "death link
  amnesty", which allows you to choose how many deaths you have to experience
  before sending a death link to your team.

* Visiting a shop will now send hints to the Archipelago server for all the
  items in that shop, so that your teammates can see which items you can buy for
  them.
 
In general, 3.x.x YAMLs and multiworlds that use the 3.x.x apworld *are*
compatible with 4.0.0. However, the `auto_equip` and `lock_equip` options have
been removed, and if they're set in your YAML they will no longer have any
effect.
