# Risk of Rain 2

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Risk of Rain is already a random game, by virtue of being a roguelite. The Archipelago mod implements pure multiworld
functionality in which certain chests will send an item out to the
multiworld. The items that _would have been_ in those chests will be returned to the Risk of Rain player via grants by
other players in other worlds.

There are two modes in risk of rain. Classic Mode and Explore Mode

Classic Mode:

  - Certain chests (made clear via a location check progress bar) will send an item out to the
    multiworld. The location of these chests do not matter, since all environments share a unified location pool.

Explore Mode:

  - Chests will continue to work as they did in Classic Mode, the difference being that each environment
  will have a set amount of items that can be sent out. In addition, shrines, radio scanners, newt altars, 
  and scavenger bags will need to be checked, depending on your settings.
  This mode also makes each environment an item. In order to access a particular stage, you'll need it to be 
  sent in the multiworld.

## What is the goal of Risk of Rain 2 in Archipelago?

Just like in the original game, any way to "beat the game" counts as a win. This means beating one of the bosses 
on Commencement, The Planetarium, or A Moment, Whole. Alternatively, if you are new to the game and 
aren't very confident in being able to "beat the game", you can set **Final Stage Death is Win** to true
(You can turn this on in your player settings.) This will make it so dying on either Commencement or The Planetarium,
or **obliterating yourself in A Moment, Fractured** will count as your goal.
**You do not need to complete all the location checks** to win; any item you don't collect may be released if the 
server options allow.

If you die before you accomplish your goal, you can start a new run. You will start the run with any items that you
received from other players. However, these items will be randomized within their rarity at the start of each run. 
Any items that you picked up the "normal" way will be lost.

Note, you can play Simulacrum mode as part of an Archipelago, but you can't achieve any of the victory conditions in
Simulacrum. So you could, for example, collect most of your items through a Simulacrum run(only works in classic mode),
then finish a normal mode run while keeping the items you received via the multiworld.

## Can you play multiplayer?

Yes! You can have a single multiplayer instance as one world in the multiworld. All the players involved need to have
the Archipelago mod, but only the host needs to configure the Archipelago settings. When someone finds an item for your
world, all the connected players will receive a copy of the item, and the location check bar will increase whenever any
player finds an item in Risk of Rain.

You cannot have players with different player slots in the same co-op game instance. Only the host's Archipelago
settings apply, so each Risk of Rain 2 player slot in the multiworld needs to be a separate game instance. You could,
for example, have two players trade off hosting and making progress on each other's player slot, but a single co-op
instance can't make progress towards multiple player slots in the multiworld.

Explore mode is untested in multiplayer and will likely not work until a later release.

## What Risk of Rain items can appear in other players' worlds?

The Risk of Rain items are:

* `Common Item`    (White items)
* `Uncommon Item`  (Green items)
* `Boss Item`      (Yellow items)
* `Legendary Item` (Red items)
* `Lunar Item`     (Blue items)
* `Equipment`      (Orange items)
* `Dio's Best Friend` (Used if you set the YAML setting `total_revives_available` above `0`)
* `Void Item`      (Purple items) (needs dlc_sotv: enabled)

Each item grants you a random in-game item from the category it belongs to.

When an item is granted by another world to the Risk of Rain player then a random
in-game item of that tier will appear in the Risk of Rain player's inventory. If the item grant is an `Equipment` and
the player already has an equipment item equipped then the _item that was equipped_ will be dropped on the ground and 
_the new equipment_ will take it's place.

Explore Mode items are:

* `Titanic Plains (1)`, `Titanic Plains (2)`, `Distant Roost (1)`, `Distant Roost (2)`
* `Abandoned Aqueduct`, `Wetland Aspect`
* `Rallypoint Delta`, `Scorched Acres`
* `Abyssal Depths`, `Siren's Call`, `Sundered Grove`
* `Sky Meadow`
* `Commencement`
* `All the Hidden Realms`

Dlc_Sotv items
* `Siphoned Forest`
* `Aphelian Sanctuary`
* `Sulfur Pools`
* `Void Locus`

When an explore item is granted, it will unlock that environment and will now be accessible! The 
game will still pick randomly which environment is next, but it will first check to see if they are available. If you have
multiple of the next environments unlocked, it will weight the game to have a ***higher chance*** to go to one you 
have checks in versus one you have already completed. You will still be unable to go to a stage 3 environment from a stage 1 environment.



### How many items are there?

Since a Risk of Rain 2 run can go on indefinitely, you have to configure how many collectible items (also known as
"checks") the game has for purposes of Archipelago when you set up a multiworld. You can configure anywhere from **10
to 250** items. The number of items will be randomized between all players, so you may want to adjust the number and
item pickup step based on how many items the other players in the multiworld have. (Around 100 seems to be a good
ballpark if you want to have a similar number of items to most other games.)

In explore mode, the amount of checks are based on how many **chests, shrines, scavengers, radio scanners, and newt altars**
are in the pool. With just the base game, checks can range from **52 to 516**, with the DLC expanding it to **60 to 660**. 
Leaving everything on default, the total number of checks comes out to **216** locations.

After you have completed the specified number of checks, you won't send anything else to the multiworld. You can
receive up to the specified number of randomized items from the multiworld as the players find them. In either case,
you can continue to collect items as normal in Risk of Rain 2 if you've already found all your location checks.

## What does another world's item look like in Risk of Rain?

When the Risk of Rain player fills up their location check bar then the next spawned item will become an item grant for
another player's world (or possibly get sent back to yourself). The item in Risk of Rain will disappear in a poof of
smoke and the grant will automatically go out to the multiworld. Additionally, you will see a message in the chat saying
what item you sent out. If the message does not appear, this likely means that another game has collected their items from you.

## What is the item pickup step?

The item pickup step is a setting in the YAML which allows you to set how many items you need to spawn before the _next_ item
that is spawned disappears (in a poof of smoke) and goes out to the multiworld. For instance, an item step of **1** means that 
every other chest will send an item to the multiworld. An item step of **2** means that every third chest sends out an item 
just as an item step of **0** would send an item on **each chest.**

## Is Archipelago compatible with other Risk of Rain 2 mods?

Mostly, yes. Not every mod will work; in particular, anything that causes items to go directly into your inventory
rather than spawning onto the map will interfere with the way the Archipelago mod works. However, many common mods work
just fine with Archipelago.

For competitive play, of course, you should only use mods that are agreed-upon by the competitors so that you don't
have an unfair advantage.
