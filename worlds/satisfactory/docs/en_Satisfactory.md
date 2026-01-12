# Satisfactory

<!-- Spellchecker config - cspell:ignore FICSIT Nobelisk Zoop -->

## Where is the settings page?

The [player settings page for this game](../player-options)
contains all the options you need to configure and export a config file.

## What does randomization do to this game?

In Satisfactory, the HUB Milestones and MAM Research Nodes are shuffled,
causing technologies to be obtained in a non-standard order.
Hard Drive scanning results also contain Archipelago items,
meaning alternate recipes could now become part of your required progression path.
There are also a few new purchases in the AWESOME Shop.
The materials required for constructing Assemblers and Foundries is altered to increase early game recipe variety.

## What is the goal of Satisfactory?

The player can choose from a number of goals using their YAML settings:

- Complete the selected number of **[Space Elevator](https://satisfactory.wiki.gg/wiki/Space_Elevator) Phases**.
  - The goal completes upon submitting your selected Space Elevator Phase. Any other progression you may have access to (HUB, MAM, AWESOME Shop) is not required for goal completion.
  - Selecting Phase 5 is equivalent to beating the vanilla game by launching Project Assembly.
  - Expect Phase 1 to take ~3 hours to finish, Phase 2 to take ~8 hours, Phase 3 to take ~2 days, Phase 4 to take ~1 week, and Phase 5 to take ~1.5 weeks on default settings.
- Supply items to the [AWESOME Sink](https://satisfactory.wiki.gg/wiki/AWESOME_Sink) **totalling a configurable amount of points** to finish.
  - The goal is tracked in the background and completes once the points total is reached.
  - Your selected point total can be reviewed in the AWESOME Sink graph.
  - Time to finish this goal varies significantly depending on your goal level and Free Sample settings, and can technically be reached by AFKing at any point after you unlock the Sink.
- Supply items to the [AWESOME Sink](https://satisfactory.wiki.gg/wiki/AWESOME_Sink) **maintaining a configurable level of points per minute** to finish.
  - The goal is tracked in the background and completes once you have maintained the selected sink points rate for 10 minutes.
  - This goal requires establishing a more robust factory since it can't be AFKed like the points total or elevator goals.
  - Your selected points rate can be reviewed in the AWESOME Sink graph.
  - Time to finish this goal varies significantly depending on your Space Elevator packages in logic and the resource sink point improvement ratios of the recipes you have access to.
- **Explore the world to gather exotic items** and submit them in the HUB.
  - The goal completes upon submitting the HUB milestone.
  - There is no partial progress system for this goal - combining it with another goal is recommended.
  - Time to finish this goal varies significantly depending on your map knowledge, equipment, and movement skills.

You can also configure whether completing your slot requires *any one* goal or *all* goals to be met.

## What Satisfactory items can appear in other players' worlds?

Satisfactory's technologies are removed from the HUB, MAM, and Hard Drives and placed into other players' worlds.
When those technologies are found, they are sent back to Satisfactory
along with, optionally, free samples of those technologies.

Other players' worlds may have Resource Bundles of building materials, equipment, ammunition, or FICSIT Coupons.
They may also contain Traps.

## What is a Free Sample?

A free sample is a package of items in Satisfactory granted in addition to a technology received from another world.
For equipment and component crafting recipes, this is the output product.
For buildings, this is the ingredients for the building.
For example, receiving the [Nobelisk Detonator MAM Node](https://satisfactory.wiki.gg/wiki/Nobelisk_Detonator#Unlocking)
would give you one Nobelisk Detonator and 50 Nobelisk,
receiving the [Jump Pads Milestone](https://satisfactory.wiki.gg/wiki/Milestones#Tier_2)
would give you the ingredients to construct 5 Jump Pads and 5 U-Jelly Landing Pads, etc.
In Satisfactory multiplayer, each Satisfactory player gets a copy of the sample.
Certain recipes and items, like Somersloops, are always excluded from samples.

You can separately configure how many samples to receive for buildings, equipment, and crafting components
in your player settings.

## What is a Resource Bundle?

A Resource Bundle is a package of items received as a check from another world.
All resource bundle type items are named either `Single: <item name>` or `Bundle: <item name>` to distinguish them from component recipes.
They must be collected by constructing an Archipelago Portal.
For example, `Single: Jetpack` would contain a single jetpack, and `Bundle: Biomass` would contain one stack of biomass.

Any Resource Bundle type items added to your starting inventory will be delivered to your player inventory when you initally spawn,
unless they can't fit, in which case they can be collected by building an Archipelago Portal.

## What is a Trap?

Traps are items intended to disrupt the player that replace non-progression filler items.
Satisfactory's traps currently include spawning disruptive creatures or sending inconvenient items to your Archipelago Portal.
The player settings page gives full control over which traps are enabled,
how many traps replace filler items,
as well as some pre-selected groups of themed traps.

A complete list of traps and their effects is intentionally omitted to keep some surprise and mystery.
In the current implementation, the most severe traps could temporarily lock you out of a small area until you have gas/radiation protection.

## What does another world's item look like in Satisfactory?

In Satisfactory, items which need to be sent to other worlds appear in the HUB and MAM as info cards
in a similar manner to the base game's building and recipe unlocks.
Info cards have the Archipelago icon
and are color coded to indicate what Archipelago progression type they are.

Hover over them to read a description, since many Satisfactory UIs (such as the MAM) cut this information off.

![screenshot of HUB with some remote and some local items](https://raw.githubusercontent.com/Jarno458/SatisfactoryArchipelagoMod/main/Docs/localAndRemoteItems.JPG)

Upon successful unlock of the technology, the item will be sent to its home world.

## When the pioneer receives an item, what happens?

When the player receives a technology, it is instantly unlocked and able to be crafted or constructed.
A message will appear in the chat to notify the player,
and if free samples are enabled the player may also receive some items delivered directly to their inventory.
Bundles will instantly be added to the Archipelago Portal network and can be collected at any Archipelago Portal.

## What is EnergyLink?

EnergyLink is an energy storage supported by certain games that is shared across all worlds in a multiworld.
In Satisfactory, if enabled in the player settings, all base-game Power Storage buildings will act as Energy Link interfaces.
They will deposit surplus produced energy and draw energy from the shared storage when needed.

Just like the base game, there is no limit to the discharge/draw rate of one building,
and each Power Storage provides 100 MW of charging throughput.
The shared storage has unlimited capacity, and only a small amount of energy is lost during depositing.
The amount of energy currently in the shared storage is displayed in the Archipelago client
and appears in the Power Storage building UI.

You can find a list of Energy Link compatible games on the
[Archipelago Discord](https://discord.com/channels/731205301247803413/1010929117748809758/1174728119568048130).

## What is the Archipelago Portal?

The Archipelago Portal is a building that serves multiple purposes:

- Collecting received "Resource Bundle"-type items.
- Transfering items within your Satisfactory world to other Portals
- Transfering items between multiple Satisfactory worlds
- Gifting items to other games that support the **Archipelago Gifting** system.

The building requires power to operate.
You can build multiple portals or use faster belts to increase their bandwith.
However, they currently have no filtering capabilities,
so you must deal with this problem when handling their output items.

You can find a list of Gifting compatible games on the
[Archipelago Discord](https://discord.com/channels/731205301247803413/1134306496042258482/1247617772993908891).

## How do Hard Drives work?

All base game Hard Drive contents (alternate recipes) have been moved into the normal Archipelago pool.
Instead, Hard Drives can contain Archipelago items from a dedicated "Hard Drive" pool.
Scanning a drive presents a choice between 2 items from the pool,
and the scan time has been reduced from 10 minutes to 3 seconds.

Unlike the base game, Archipelago hard drive results have no hard progression requirements,
other than access to the MAM itself.
The random contents selection system prefers to pick items earlier in progression,
but keeping unselected Hard Drives in the Hard Drive Library will force later progression items to be presented.

The "Hard Drive Progression Items" option controls how many Hard Drives contain progression items,
the rest are filler or useful.

## Where do I run Archipelago commands?

You can use the game's built-in chat menu.
Check the game's keybinding options to see how to open it.
Run the `/help` command to list all available commands.
Note that Archipelago commands are *not* prefixed with `!` inside of Satisfactory.

Note that multiple base-game bugs affect the chat menu's functionality
and Archipelago can put a lot of info into the chat.
You may wish to launch the Archipelago Text Client and use it to run commands instead of the game's chat.

### Hints

Archipelago's hint system is available within Satisfactory via the `/hint` command.
Most multiworld item names have a prefix to distinguish recipes from bundles.
For example, to hint for the Assembler, run `/hint Building: Assembler`.

Satisfactory's hint system has special behavior for Satisfactory crafting items.
If you hint the unprefixed name of an item with multiple recipes, the system will hint the recipe you are expected to find first in randomizer logic.
For example, hinting `Smart Plating` will return the logically first Smart Plating recipe,
but hinting `Recipe: Smart Plating` or `Recipe: Plastic Smart Plating` will hint that specific recipe for Smart Plating,
which may or may not be in logic.

Exact Archipelago Item names (for hints/starting inventory/etc.) can be found
[on the mod's GitHub](https://github.com/Jarno458/Archipelago/blob/Satisfactory/worlds/satisfactory/Items.py).

## Multiplayer and Dedicated Servers

It is possible to host a Satisfactory Archipelago Slot using the game's built in multiplayer,
allowing other Satisfactory players to join in constructing your factory.
This experience is wonderful - but there are few things not yet properly working for multiplayer:

- Death-links do not kill clients
- Starting inventory for clients is missing

Remember that client players must have the same mods installed as the host player to join,
however, they do not need to configure Archipelago connection settings.

Dedicated server support is only working for Windows at the moment.

## Additional Mods

It is possible to use other Satisfactory mods in tandem with the Archipelago Satisfactory mod.
However, no guarantee is made that they will work correctly,
especially if they affect game progression, recipes, or add unlocks to base-game technologies.

Content added by unaffiliated mods may end up inaccessible based on your chosen slot settings,
for example, its milestones could be in a tier that is after your goal.
You may be able to write patches using [ContentLib](https://ficsit.app/mod/ContentLib)
to adjust other mods to work with your slot settings,
but doing so is out of the scope of this guide.

[The Satisfactory Archipelago mod GitHub](https://github.com/Jarno458/SatisfactoryArchipelagoMod/blob/main/Docs/AdditionalMods.md)
maintains a list of additional mods that have been tested with Archipelago to some extent.
