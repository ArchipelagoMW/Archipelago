# MegaMan Battle Network 3

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and
export a config file.

## What does randomization do to this game?

Items which the player would normally acquire throughout the game have been moved around. Logic remains, so the game is
always able to be completed, but because of the item shuffle, the player may need to access certain areas before they
would in the vanilla game.

The game begins in "Open Mode", in a story state just before leaving for the WWW Base. All story progress leading up to
that point has been auto completed. You will be given a Style Change upon starting, but will
have default MegaMan equipped, you can switch to your new style if you want through the Navi menu.

Higsby's Chip Trader has been replaced with a shop interface where you can pay 500z to access the next item in the
trader sequence.
Dialog has been rewritten for both the Trader and the hat kid next to the trader to explain it.

The Nut-Wafer Chocolate Stand in the Yoka Metro has been replaced with a system for trading BugFrags for items.
Dialog has been rewritten to give it a story reason for accepting BugFrags.

The Secret Area is unlocked from the start, since the Library is filled automatically. Jacking Out has been enabled
in the Secret Area.

## What is the goal of MegaMan Battle Network 3 when randomized?

Defeat Alpha on the WWW Base. You will not be able to access the Island until you have acquired the item `GigFreez`,
which will be the eight item in the `progressive-undernet` item sequence. You will need to acquire Undernet Ranks
10, 9, 8, 7, 3, 2, and 1 before acquiring `GigFreez`
(Note: The skipping of 6-4 is intentional. They do not exist in the base game.)

## What items and locations get shuffled?

Locations in which items can be found:
- All Blue and Purple Mystery Data.
- The rewards from all available Jobs (Note: The four "Tora" jobs are story progress, and therefore have 
been already completed). 
- All overworld item pick ups, including Trades and Quizzes with NPCs
- 31 Items from the Numberman Lottery Trader (which have been changed to require Zenny instead of lotto numbers)
- 32 Items from the Nut-Wafer Chocolate stand in Yoka Metro Station (which have been changed to require BugFrags 
instead of Zenny)

Items that are shuffled:
- All of the original rewards from above (Note: Certain common chips and low amounts of Zenny have been classified
as "filler" and might be replaced with progression items)
- All four Cybermetro passes, normally obtained through story progression
- Eight Progressive Undernet Ranks, normally obtained through story progression
- Several chips required for specific Jobs or Trades that would normally be unobtainable without RNG
- The NaviCust "Press" program, normally obtained through story progression
- Two ExpMems and ModTools for the Navi Customizer, normally obtained through story progression
- Higsby's `OrderSys`, which will enable access to the Chip Order System

## What items are _not_ randomized?
Certain Key Items are kept in their original locations:
- All four of the ID Keys in the WWW-Comp machines on the WWW Base
- Items in Undernet 7 locked behind post-game progression gates, such as beating Serenade or gathering all chips

## Which items can be in another player's world?

Any shuffled item can be in other players' worlds.


## What does another world's item look like in Mega Man Battle Network 3?

Item pickups all retain their original appearance. Text Boxes for accessing an item or given in dialog will mention
what item and what player is receiving the item

## When the player receives an item, what happens?

Whenever you have an item pending, the next time you are not in a battle, menu, or dialog box, you will receive a
message on screen notifying you of the item and sender, and the item will be added directly to your inventory.

## Unique Local Commands

The following commands are only available when using the MMBN3Client to play with Archipelago.

- `/gba` Check GBA Connection State
- `/debug` Toggle the Debug Text overlay in ROM
