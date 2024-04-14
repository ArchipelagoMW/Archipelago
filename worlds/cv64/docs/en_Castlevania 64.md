# Castlevania 64

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

All items that you would normally pick up throughout the game, be it from candles, breakables, or sitting out, have been
moved around. This includes the key items that the player would normally need to find to progress in some stages, which can
now be found outside their own stages, so returning to previously-visited stages will very likely be necessary (see: [How do
I jump to a different stage?](#how-do-i-jump-to-a-different-stage?)). The positions of the stages can optionally be randomized
too, so you may start out in Duel Tower and get Forest of Silence as your penultimate stage before Castle Keep, amongst
many other possibilities.

## How do I jump to a different stage?

Instant travel to an earlier or later stage is made possible through the Warp Menu, a major addition to the game that can
be pulled up while not in a boss fight by pressing START while holding Z and R. By finding Special1 jewels (the item that
unlocks Hard Mode in vanilla Castlevania 64), more destinations become available to be selected on this menu. The destinations
on the list are randomized per seed and the first one, which requires no Special1s to select, will always be your starting 
area.

NOTE: Regardless of which option on the menu you are currently highlighting, you can hold Z or R while making your selection
to return to Villa's crypt or Castle Center's top elevator room respectively, provided you've already been to that place at
least once. This can make checking out both character stages at the start of a route divergence far less of a hassle.

## Can I do everything as one character?

Yes! The Villa end-of-level coffin has had its behavior modified so that which character stage slot it sends you to
depends on the time of day, and likewise both bridges at the top of Castle Center's elevator are intact so both exits are
reachable regardless of who you are. With these changes in game behavior, every stage can be accessed by any character
in a singular run.

NOTE: By holding L while loading into a map (this can even be done while cancelling out of the Warp Menu), you can swap to
the other character you are not playing as, and/or hold C-Up to swap to and from the characters' alternate costumes. Unless
you have Carrie Logic enabled, and you are not playing as her, switching should never be necessary.

## What is the goal of Castlevania 64 when randomized?

Make it to Castle Keep, enter Dracula's chamber, and defeat him to trigger an ending and complete your goal. Whether you
get your character's good or bad ending does **not** matter; the goal will send regardless. Options exist to force a specific
ending for those who prefer a specific one.

Dracula's chamber's entrance door is initially locked until whichever of the following objectives that was specified on your
YAML under `draculas_condition` is completed:
- `crystal`: Activate the big crystal in the basement of Castle Center. Doing this entails finding two Magical Nitros and 
two Mandragoras to blow up both cracked walls (see: [How does the Nitro transport work in this?](#how-does-the-nitro-transport-work-in-this?)).
Behemoth and Rosa/Camilla do **NOT** have to be defeated.
- `bosses`: Kill bosses with visible health meters to earn Trophies. The number of Trophies required can be specified under
`bosses_required`.
- `special2s`: Find enough Special2 jewels (the item that normally unlocks alternate costumes) that are shuffled in the
regular item pool. The total amount and percent needed can be specified under `total_special2s` and `percent_special2s_required` respectively.

If `none` was specified, then there is no objective. Dracula's chamber door is unlocked from the start, and you merely have to reach it.

## What items and locations get shuffled?

Inventory items, jewels, moneybags, and PowerUps are all placed in the item pool by default. Randomizing Sub-weapons is optional,
and they can be shuffled in their own separate pool or in the main item pool. An optional hack can be enabled to make your
old sub-weapon drop behind you when you receive a different one, so you can pick it up again if you still want it. Location
checks by default include freestanding items, items from one-hit breakables, and the very few items given through NPC text. Additional
locations that can be toggled are:
- Objects that break in three hits.
- Sub-weapon locations if they have been shuffled anywhere.
- Seven items sold by the shopkeeper Renon.
- The two items beyond the crawlspace in Waterway that normally require Carrie, if Carrie Logic is on.
- The six items inside the Lizard-man generators in Castle Center that open randomly to spawn Lizard-men. These are particularly annoying!

## How does the Nitro transport work in this?

Two Magical Nitros and two Mandragoras are placed into the item pool for blowing up the cracked walls in Castle Center
and two randomized items are placed on both of their shelves. The randomized Magical Nitro will **NOT** kill you upon landing
or taking damage, so don't panic when you receive one! Hazardous Waste Dispoal bins are disabled and the basement crack with
a seal will not let you set anything at it until said seal is removed so none of the limited ingredients can be wasted.

In short, Nitro is still in, explode-y business is not! Unless you turn on explosive DeathLink, that is...

## Which items can be in another player's world?

Any of the items which can be shuffled may also be placed into another player's world. The exception is if sub-weapons
are shuffled in their own pool, in which case they will only appear in your world in sub-weapon spots.

## What does another world's item look like in Castlevania 64?

An item belonging to another world will show up as that item if it's from another Castlevania 64 world, or one of two
Archipelago logo icons if it's from a different game entirely. If the icon is big and has an orange arrow in the top-right
corner, it is a progression item for that world; definitely get these! Otherwise, if it's small and with no arrow, it is
either filler, useful, or a trap.

When you pick up someone else's item, you will not receive anything and the item textbox will show up to announce what you
found and who it was for. The color of the text will tell you its classification:
- <font color="moccasin">Light brown-ish</font>: Filler
- <font color="white">White</font>/<font color="yellow">Yellow</font>: Useful
- <font color="yellow">Yellow</font>/<font color="lime">Green</font>: Progression
- <font color="yellow">Yellow</font>/<font color="red">Red</font>: Trap

## When the player receives an item, what happens?

A textbox containing the name of the item and the player who sent it will appear, and they will get it.
Just like the textbox that appears when sending an item, the color of the text will tell you its classification.

NOTE: You can press B to close the item textbox instantly and get through your item queue quicker.

## What tricks and glitches should I know for Hard Logic?

The following tricks always have a chance to be required:
- Left Tower Skip in Castle Wall
- Copper Door Skip in Villa (both characters have their own methods for this)
- Waterfall Skip if you travel backwards into Underground Waterway
- Slope Jump to Room of Clocks from Castle Keep
- Jump to the gated ledge from the level above in Tower of Execution

Enabling Carrie Logic will also expect the following:

- Orb-sniping dogs through the front gates in Villa

Library Skip is **NOT** logically expected by any options. The basement arena crack will always logically expect two Nitros
and two Mandragoras even with Hard Logic on due to the possibility of wasting a pair on the upper wall, after managing
to skip past it. And plus, the RNG manip may not even be possible after picking up all the items in the Nitro room.

## What are the item name groups?
The groups you can use for Castlevania 64 are `bomb` and `ingredient`, both of which will hint randomly for either a
Magical Nitro or Mandragora.

## What are the location name groups?
In Castlevania 64, every location that is specific to a stage is part of a location group under that stage's name.
So if you want to exclude all of, say, Duel Tower, you can do so by just excluding "Duel Tower" as a whole.

## I'm stuck and/or I can't find this hinted location...is there a map tracker?
At the moment, no map tracker exists. [Here](https://github.com/ArchipelagoMW/Archipelago/tree/main/worlds/cv64/docs/obscure_checks.md)
is a list of many checks that someone could very likely miss, with instructions on how to find them. See if the check you
are missing is on there and if it isn't, or you still can't find it, reach out in the [Archipelago Discord server](https://discord.gg/archipelago)
to inquire about having the list updated if you think it should be.

If you are new to this randomizer, it is strongly recommended to play with the Countdown option enabled to at least give you a general
idea of where you should be looking if you get completely stuck. It can track the total number of unchecked locations in the
area you are currently in, or the total remaining majors.

## Why does the game stop working when I sit on the title screen for too long?
This is an issue that existed with Castlevania 64 on mupen64plus way back in 2017, and BizHawk never updated their
mupen64plus core since it was fixed way back then. This is a Castlevania 64 in general problem that happens even with the
vanilla ROM, so there's not much that can done about it besides opening an issue to them (which [has been done](https://github.com/TASEmulators/BizHawk/issues/3670))
and hoping they update their mupen64plus core one day...

## How the f*** do I set Nitro/Mandragora?
<font color="yellow">(>)</font>
