# Castlevania: Circle of the Moon

## Quick Links
- [Setup](/tutorial/Castlevania%20-%20Circle%20of%20the%20Moon/setup/en)
- [Options Page](/games/Castlevania%20-%20Circle%20of%20the%20Moon/player-options)
- [PopTracker Pack](https://github.com/sassyvania/Circle-of-the-Moon-Rando-AP-Map-Tracker-/releases/latest)
- [Repo for the original, standalone CotMR](https://github.com/calm-palm/cotm-randomizer)
- [Web version of the above randomizer](https://rando.circleofthemoon.com/)
- [A more in-depth guide to CotMR's nuances](https://docs.google.com/document/d/1uot4BD9XW7A--A8ecgoY8mLK_vSoQRpY5XCkzgas87c/view?usp=sharing)

This Game Page is focused more specifically on the Archipelago functionality. If you have a more general Circle of the Moon-related
question that is not answered here, try the above guide.

## What does randomization do to this game?

Almost all items that you would normally find on pedestals throughout the game have had their locations changed. In addition to
Magic Items (barring the Dash Boots which you always start with) and stat max ups, the DSS Cards have been added to the
item pool as well; you will now find these as randomized items rather than by farming them via enemy drops.

## Can I use any of the alternate modes?

Yes. All alternate modes (Magician, Fighter, Shooter, and Thief Mode) are all unlocked and usable from the start by registering
the name password shown on the Data Select screen for the mode of your choice. 

If you intend to play Magician Mode, putting all of your cards in "Start Inventory from Pool" is recommended due to the fact
that it naturally starts with all cards. In Fighter Mode, unlike in the regular game, you will be able to receive and use
DSS Cards like in all other modes.

## What is the goal of Castlevania: Circle of the Moon when randomized?

Depending on what was chosen for the "Completion Goal" option, your goal may be to defeat Dracula, complete the Battle Arena, or both.

- "Dracula": Make it to the Ceremonial Room and kill Dracula's first and second forms to view the credits. The door to the
Ceremonial Room can be set to require anywhere between 0-9 Last Keys to open it.
- "Battle Arena": Survive every room in the Battle Arena and pick up the Shinning Armor <sup>sic</sup> on the pedestal at the end. To make it
easier, the "Disable Battle Arena Mp Drain" option can be enabled to make the Battle Arena not drain your MP to 0, allowing
DSS to be used. Reaching the Battle Arena in the first place requires finding the Heavy Ring and Roc Wing (as well as Double or Kick Boots
if "Nerf Roc Wing" is on).
- "Battle Arena And Dracula": Complete both of the above-mentioned objectives. The server will remember which ones (if any) were
already completed on previous sessions upon connecting.

NOTE: If "All Bosses" was chosen for the "Required Skirmishes" option, 8 Last Keys will be required, and they will be guaranteed
to be placed behind all 8 bosses (that are not Dracula). If "All Bosses And Arena" was chosen for the option, an additional
required 9th Last Key will be placed on the Shinning Armor <sup>sic</sup> pedestal at the end of the Battle Arena in addition to
the 8 that will be behind all the bosses.

If you aren't sure what goal you have, there are two in-game ways you can check:

- Pause the game, go to the Magic Item menu, and view the Dash Boots tutorial.
- Approach the door to the first Battle Arena combat room and the textbox that normally explains how the place works will tell you.

There are also two in-game ways to see how many Last Keys are in the item pool for the slot:

- Pause the game, go to the Magic Item menu, and view the Last Key tutorial.
- If you don't have any keys, touch the Ceremonial Room door before acquiring the necessary amount.


## What items and locations get shuffled?

Stat max ups, Magic Items, and DSS Cards are all randomized into the item pool, and the check locations are the pedestals
that you would normally find the first two types of items on.

The sole exception is the pedestal at the end of the Battle Arena. This location, most of the time, will always have 
Shinning Armor <sup>sic</sup> unless "Required Skirmishes" is set to "All Bosses And Arena", in which case it will have a Last Key instead.

## Which items can be in another player's world?

Stat max ups, Magic Items, and DSS Cards can all be placed into another player's world.

The Dash Boots and Shinning Armor <sup>sic</sup> are not randomized in the item pool; the former you will always start with and the
latter will always be found at the end of the Battle Arena in your own world. And depending on your goal, you may or may
not be required to pick it up.

## What does another world's item look like in Castlevania: Circle of the Moon?

Items for other Circle of the Moon players will show up in your game as that item, though you won't receive it yourself upon
picking it up. Items for non-Circle of the Moon players will show up as one of four Archipelago Items depending on how its 
classified:

* "Filler": Just the six spheres, nothing extra.
* "Useful": Blue plus sign in the top-right corner.
* "Progression": Orange up arrow in the top-right corner.
* "Progression" and "Useful": Orange up arrow in the top-right corner, blue plus sign in the bottom-right corner.
* "Trap": Reports from the local residents of the remote Austrian village of \[REDACTED], Styria claim that they disguise themselves
as Progression but with the important difference of \[DATA EXPUNGED]. Verification of these claims are currently pending...

Upon sending an item, a textbox announcing the item being sent and the player who it's for will show up on-screen, accompanied
by a sound depending on whether the item is filler-, progression-/useful-, or trap-classified.

## When the player receives an item, what happens?

A textbox announcing the item being received and the player who sent it will pop up on-screen, and it will be given.
Similar to the outgoing item textbox, it will be accompanied by a sound depending on the item received being filler or progression/useful.

## What are the item name groups?

When you attempt to hint for items in Archipelago you can use either the name for the specific item, or the name of a group
of items. Hinting for a group will choose a random item from the group that you do not currently have and hint for it. The
groups you can use for Castlevania: Circle of the Moon are as follows:

* "DSS" or "Card": Any DSS Card of either type.
* "Action" or "Action Card": Any Action Card.
* "Attribute" or "Attribute Card": Any Attribute Card.
* "Freeze": Any card that logically lets you freeze enemies to use as platforms.
* "Action Freeze": Either Action Card that logically lets you freeze enemies.
* "Attribute Freeze": Either Attribute Card that logically lets you freeze enemies.

## What are the location name groups?

In Castlevania: Circle of the Moon, every location is part of a location group under that location's area name.
So if you want to exclude all of, say, Underground Waterway from having progression, you can do so by just excluding
"Underground Waterway" as a whole.

In addition to the area location groups, the following groups also exist:

* "Breakable Secrets": All locations behind the secret breakable walls, floors, and ceilings.
* "Bosses": All the primary locations behind bosses that Last Keys normally get forced onto when bosses are required. If you want
to prioritize every boss to be guarding a progression item for someone, this is the group for you!

## How does the item drop randomization work?

There are three tiers of item drops: Low, Mid, and High. Each enemy has two item "slots" that can both drop its own item; a Common slot and a Rare one.

On Normal item randomization, "easy" enemies (below 61 HP) will only have Low-tier drops in both of their slots, bosses
and candle enemies will be guaranteed to have High drops in one or both of their slots respectively (bosses are made to
only drop one slot 100% of the time), and everything else can have a Low or Mid-tier item in its Common drop slot and a
Low, Mid, OR High-tier item in its Rare drop slot.

If Item Drop Randomization is set to Tiered, the HP threshold for enemies being considered "easy" will raise to below
144, enemies in the 144-369 HP range (inclusive) will have a Low-tier item in its Common slot and a Mid-tier item in
its rare slot, and enemies with more than 369 HP will have a Mid-tier in its Common slot and a High-tier in its Rare
slot, making them more worthwhile to go after. Candles and bosses still have Rares in all their slots, but now the guaranteed
drops that land on bosses will be exclusive to them; no other enemy in the game will have their item.

Note that the Shinning Armor <sup>sic</sup> can never be placed randomly onto a normal enemy; you can only receive it by completing the Battle Arena.
If "Required Skirmishes" is set to "All Bosses And Arena", which replaces the Shinning Armor <sup>sic</sup> on the pedestal at the end with
a Last Key, the Devil fought in the last room before the end pedestal will drop Shinning Armor <sup>sic</sup> 100% of the time upon defeat.

For more information and an exact breakdown of what items are considered which tier, see Malaert64's guide 
[here](https://docs.google.com/document/d/1uot4BD9XW7A--A8ecgoY8mLK_vSoQRpY5XCkzgas87c/view#heading=h.5iz6ytaji08m).

## Is it just me, or does the Countdown seem inaccurate to the number of checks in the area?
Some Countdown regions are funny because of how the developers of the game decided what rooms belong to which areas in spite of
what most players might think. For instance, the Skeleton Athlete room is actually part of the Chapel Tower area, not the Audience Room.
And the Outer Wall very notably has several rooms isolated from its "main" area, like the Were-Horse/Jaguar Armory.
See [this map](https://docs.google.com/document/d/1uot4BD9XW7A--A8ecgoY8mLK_vSoQRpY5XCkzgas87c/view#heading=h.scu4u49kvcd4) 
to know exactly which rooms make up which Countdown regions.

## Will the Castlevania Advance Collection and/or Wii U Virtual Console versions work?

The Castlevania Advance Collection ROM is tested and known to work. However, there are some major caveats when playing with the
Advance Collection ROM; most notably the fact that the audio does not function when played in an emulator outside the collection,
which is currently a requirement to connect to a multiworld. This happens because all audio code was stripped
from the ROM, and all sound is instead played by the collection through external means.

The Wii U Virtual Console version does not work due to changes in the code in that version.

Due to the reasons mentioned above, it is most recommended to obtain the ROM by dumping it from an original cartridge of the
game that you legally own. However, the Advance Collection *is* an option if you cannot do that and don't mind the lack of sound.

Regardless of which released ROM you intend to try playing with, the US version of the game is required.

## What are the odds of a pentabone?
The odds of skeleton Nathan throwing a big bone instead of a little one, verified by looking at the code itself, is <sup>1</sup>&frasl;<sub>8</sub>, or 12.5%.

Soooooooooo, to throw 5 big bones back-to-back...

(<sup>1</sup>&frasl;<sub>8</sub>)<sup>5</sup> = <sup>1</sup>&frasl;<sub>32768</sub>, or 0.0030517578125%. Good luck, you're gonna need it!
