# Castlevania 64

## Where is the settings page?

The player settings page for this game(../player-settings) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

All items that you would normally pick up throughout the game, be it from candles, breakables, or sitting out, have been
moved around. This includes the key items that the player would normally need to find to progress in some stages, which can
now be found outside their own stages, so returning to previously-visited stages may be necessary. The positions of the stages
can be optionally randomized too, so you can possibly start out in Duel Tower and get Forest of Silence as your penultimate
stage before Castle Keep, amongst other possibilities.

## How do I return to a previous stage?

Instant travel to an earlier or later stage is made possible through the Warp Menu, a major addition to the game that can
be pulled up while not in a boss fight by pressing START while holding Z and R. By finding Special1 jewels (the item that
unlocks Hard Mode in vanilla CV64), more destinations become available to be selected on this menu. The destinations on
the list are randomized per seed and the first one, which requires no Special1s to select, will always be the player's
starting location.

NOTE: Regardless of which option on the menu you are currently highlighting, you can hold Z or R while making your selection
to return to Villa's crypt or Castle Center's top elevator room respectively, provided you've already been in there at
least once. This can make checking out both character stages at the start of a route divergence far less of a hassle.

## Do I need to do separate playthroughs with each character to check everything?

Nope! The Villa end-of-level coffin has had its behavior modified so that which character stage slot it sends you to
depends on the time of day, and likewise both bridges at the top of Castle Center's elevator are intact so both exits are
reachable regardless of who you are. Because of these changes in game behavior, every stage can be accessed by any character
in a single playthrough.

NOTE: By holding L while loading into a map (this can even be done while cancelling out of the Warp Menu), you can swap to
the other character you are not playing as, and/or hold C-Up to swap to and from the characters' alternate costumes. Unless
you have Carrie Logic enabled, and you are playing as Reinhardt, switching should never be necessary.

## What is the goal of Castlevania 64 when randomized?

Make it to Castle Keep, enter Dracula's chamber, and defeat him to trigger an ending and complete your goal. Whether you
get your character's good or bad ending does **not** matter; the goal will send regardless. Options exist to force a specific
ending for those who prefer a specific one.

Dracula's chamber's entrance door is initially locked until whichever of the following objectives that was specified on the
player's YAML under `draculas_condition` is completed:
- `crystal`: Activate the big crystal in the basement of Castle Center. Doing this requires finding two Magical Nitros and two Mandragoras. Behemoth and Rosa/Camilla do **NOT** have to be defeated.
- `bosses`: Kill bosses with visible health meters to earn Trophies. The number of Trophies required can be specified under `bosses_required`.
- `special2s`: Find enough Special2 jewels (the item that normally unlocks alternate costumes) that are shuffled in the regular item pool. The total amount and percent needed can be specified under `total_special2s` and `percent_special2s_required` respectively.

If `none` was specified, then there is no objective. Dracula's chamber door is unlocked from the start, and you merely have to reach it.

## What items and locations get shuffled?

Inventory items, jewels, moneybags, and PowerUps are all placed in the item pool by default. Randomizing Sub-weapons is optional,
and they can be shuffled in their own separate pool or in the main item pool. An optional hack can be enabled to make your
old sub-weapon drop behind you when you receive a different one, so you can pick it up again if you still want it. Location
checks by default include freestanding items, items from one-hit breakables, and the few items given through NPC text. Additional
locations that can be toggled are:
- Objects that break in three hits.
- Sub-weapon locations if they have been shuffled anywhere.
- Seven items sold by the shopkeeper Renon.
- The two items beyond the crawlspace in Waterway that normally require Carrie, if Carrie Logic is on.
- The six items inside the Lizard-man generators in Castle Center that open randomly to spawn Lizard-men. These are particularly annoying!

## How does the infamous Nitro transport work in this?

Two Magical Nitros and two Mandragoras are placed into the item pool for blowing up the cracked walls in Castle Center
and two randomized items are placed on both of their shelves. The randomized Magical Nitro will **NOT** kill you upon landing
or taking damage, so don't panic when you receive one! Hazardous Waste Dispoal bins are disabled and the basement crack with
a seal will not let you set anything at it until said seal is removed so none of the limited ingredients can be wasted.

In short, Nitro is still in, explode-y business is not! Unless you turn on explosive DeathLink, that is...

## Which items can be in another player's world?

Any of the items which can be shuffled may also be placed into another player's world. The exception is if sub-weapons
are shuffled in their own pool, in which case they will only appear in your world.

## What does another world's item look like in Castlevania 64?

An item belonging to another world will show up as that item if it's from another Castlevania 64 world, or one of two
Archipelago logo icons if it's from a different game entirely. If the icon is big and has an orange arrow in the top-right
corner, it is a progression item for that world; definitely get these! Otherwise, if it's small and with no arrow, it is
either filler, useful, or a trap.

When you pick up someone else's item, you will not receive anything and the item textbox will show up to announce what you
found and who it was for. The color of the text will tell you its classification:
- Light brown: Common
- White/Yellow: Useful
- Yellow/Green: Progression
- Yellow/Red: Trap


## When the player receives an item, what happens?

When the player receives an item, a textbox containing the name of the item and the player who sent it will appear, and they
will get it. Just like the textbox that appears when sending an item, the color of the text will tell you its classification.

NOTE: You can press B to close the item textbox instantly and get through your item queue quicker.

## What tricks and glitches should I know for Hard Logic?

The following tricks always have a chance to be required:
- Left Tower Skip in Castle Wall
- Copper Door Skip in Villa (both characters have their own methods for this)
- Waterfall Skip if you travel backwards into Underground Waterway
- Slope Jump to Room of Clocks from Castle Keep
- Jump to the gated ledge in Tower of Execution (not everyone may think to do this)

Enabling Carrie Logic will also expect the following:

- Orb-sniping dogs through the front gates in Villa

Library Skip will **never** be logically expected. The downstairs hallway crack will always logically expect two Nitros
and two Mandragoras even with these settings on due to the possibility of wasting a pair on the upper wall, after managing
to skip past it. And plus, the RNG manip may not even be possible after picking up all the items in the Nitro room.

## What are the item name groups?
When you attempt to hint for items in Archipelago you can use either the name for the specific item, or the name of a group
of items. Hinting for a group will choose a random item from the group that you do not currently have and hint for it.
The groups you can use for Castlevania 64 are `bomb` and `ingredient`, both of which can be used to hint for a Magical Nitro
or Mandragora.

## What are the location name groups?
When you exclude locations in Archipelago, you can either exclude a specific location, or an entire group of locations that
all fall under a name. In Castlevania 64, every location within a stage is part of a location group under that stage's name.
So if you want to exclude all of, say, Duel Tower, you can do so by just excluding "Duel Tower" as a whole.

## How do I set Nitro/Mandragora?

C-right.
