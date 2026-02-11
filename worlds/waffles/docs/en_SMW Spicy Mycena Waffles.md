# Spicy Mycena Waffles


## Features

Spicy Mycena Waffles offers a wide variety of options to make your Super Mario World session very enjoyable, aside from brand new features compared to the original implementation, it also revamps some of the original's features in order to offer a different experience. All of the features (old and new) are the following:

* Level shuffle
* Random starting world
* Enemy shuffle
* Boss shuffle
* Map Transition shuffle
* Pipes and Star Road Warp shuffle
* Level exit destination shuffle
* Ability & item shuffle
* Random level effects
* A bunch of added locations
* Stat tracking
* Universal Tracker support
* ROM-less generation

There are several quality of life changes as well traps to keep you engaged, those are further disclosed on their respective sections.

## Quality of Life

The game features a lot of quality of life settings which aims to make the experience a lot smoother for not seasoned players, it also includes some other options to make the sessions less obnoxious.
### Difficulty accesibility

There are various ways where the implementation allows you to have an overall easier time playing the game.

* Level Logic: Levels are categorized into different difficulty levels (normal, hard, very hard). Each logic level changes the logical entry requirements for them but you can still complete them even if you don't meet them, that will simply be "out of logic".
* Extra Hit: If players have found a heart and picked it up, it'll follow them anywhere and will take a hit for them. It won't protect from falling into lava or pits.
* Infinite lives: Lives no longer exist in the game, they're replaced with hearts for the Extra Hit feature mentioned above.
* Extra Defense: A new item in the item pool allows players to not go back to Small Mario when taking a hit while being Cape Mario or Fire Mario, instead they will go back to Big Mario which results into an extra hit being granted.
* Better Timer: There are a few timer upgrades that will make the HUD timer tick much slower which acts as a counter to Timer Traps or as a help for people who love to play slowly.
* Hidden 1-Ups out of order: In vanilla, players are supposed to collect Hidden 1-Ups in a specific order for them to trigger the location, now that requirement is nullified and players can now collect them in any order they desire.

### Map gameplay enhancements

The map gameplay portion of the game has received some tweaks to allow smoother experiences

* Item tracker at the top of the border, you can see which items you've gotten so far.
* Location tracker at the top right corner of the border, it'll tell you which locations have been found so far in that particular level.
* Inventory system that's accessed via SELECT. More info in Inventory system.
* Fast travel to the starting location via L+R.
* Level tiles are changed to match which levels had their tiles swapped around. This also "caused" every level tile to match which kind of level is inside; if it's a ghost house or a regular level.

* Levels with big red dots or are gray houses had their exits swapped.

### Powerup and item enhancements

There have been some adjusments for the powerups and items to enhance their abilities to be slightly more useful.

* Fireballs can be thrown in an upwards arc when pressing UP while shooting them.
* Yoshi's Tongue is tied to a second Yoshi upgrade instead of being coupled with the regular Carry item.
* A second Swim upgrade was added which enhances the player's horizontal speed to match the one when Mario is holding an item.
* Mario is able to perform a wall run anywhere as long a second Run item is obtained and has full P-Speed.
* Mario walks faster on the map, even faster if Run is obtained.
* Super Stars now lasts more time the more Progressive Star items you obtain.

### Inventory system

A inventory system similar to NSMBWii has been added which allows you to enter levels with specific powerups or items. You can summon the inventory system via SELECT during the map gameplay portion.

There are ways to obtain inventory items in the game and use them any time.

* Goal Tape: By hitting the goal at a certain height, players can get a random inventory item (or coins). The higher the goal is hit, the better the reward is.
* Combos: Any kind of combo will grant a random inventory item, this includes: jumping in enemies, defeating them with a star, collecting silver coins or combo-ing them with a kicked shell. Every time a reward is granted all combo counters will be reset.
* EnergyLink: When the inventory is shown and your selected item count is 0 an additional counter will appear at the top suggesting that you can spend EnergyLink coins to obtain one of the currently selected item.
* Fishing Lakitu: By grabbing the hooked item players will receive a random inventory item.

## Locations

This randomizer allows you to select additional Locations other than the Level Exits which will increase the Location count.

As a bonus, most locations have a way to tell which kind of item is tied to them, allowing you to scout locations ahead of time... though it's mostly irrelevant for 80% of the game's locations. It does look cool though.

* Dragon Coins
* Midway Points
* 3-Up Moons
* Prizes from Star Blocks
* Hidden 1-Ups
* Most blocks with items or coins in the game

Note to players: The Hidden 1-Ups option enables some obscure checks, enable it at your own risk. The same applies to Yellow Switch Palace blocks when enabled as items as part of the Block Checks option.

### Golden Yoshi Eggs in level exits

The fork allows you to add extra locations in level exits that will have a Golden Yoshi Egg item which will be granted alongisde the Level Exit location. This creates a big opportunity for players to simulate a 96-exit session or a landmark one which includes:

* Castles
* Ghost Houses
* Switch Palaces
* Special World Levels

Even though the Boss Tokens aren't present anymore, players can still play an "All Bosses" seed if eggs are forcefully placed in Castles.

## Goals

This fork has the same goals as the original implementation, except this time the goals depend on the same McMuffin item; Golden Yoshi Eggs.

Like the original implementation, visiting Yoshi's House also allows you to know how many eggs are required to unlock the goal condition.

### Bowser

Collect Golden Yoshi Eggs scattered across the multiworld and then defeat Bowser.

While it's not based on Tokens, you can still recreate the "All Bosses" setting with some options. Read Golden Yoshi Eggs in level for more info.

### Yoshi House

Collect Golden Yoshi Eggs scattered across the multiworld and then visit Yoshi's House to beat the game.

## Traps

SMW offers players a wide variety of traps to play around with. They range from being a fun thing to being extremely annoying (depends on who you ask). Most of them are gone after getting a single hit or going back to the map, so they're not entirely annoying to deal with.

### Ice Trap

Makes the floor slippery. May be annoying on hard levels.

### Stun Trap

Freezes the player in place for a few seconds. May be deadly if combo'd with another trap.

### Literature Trap

Generates text on screen across multiple text boxes.

### Timer Trap

Brings the timer down to 100 seconds.

### Reverse Trap

Reverses the player's inputs, including the ABXY buttons.

### Thwimp Trap

Spawns a Thwimp above the player from outside the screen. May be deadly if the player is climbing or on high ground.

### Fishin' Boo Trap

Spawns a Fishin' Boo from the sides of the screen which will haunt the player until it hurts them.

### Screen Flip Trap

Flips the screen vertically. May disorient, even worse if paired with a reverse trap.

### Sticky Hands Trap

Players are unable to drop items.

### Sticky Floor Trap

Players are unable to walk. They're forced to jump and will get rid of the effect after jumping for a bit.

### Pixelate Trap

Pixelates the screen. May disorient a ton. Fun.

### Spotlight Trap

Limits the player vision to a small circle on screen.

### Bullet Time Trap

Makes the game run to 15fps. Lasts for THREE slowed down real world seconds.

### Invisibility Trap

Mario becomes invisible. Doesn't affect Yoshi, Star sparkles or hearts.

### Empty Item Box Trap

Removes your current held item. Does nothing if the box isn't unlocked.

## Linked features

Waffles aims to support most of the protocols available to interact with outside slots. More to come later.

### EnergyLink

Whenever players with EnergyLink active collect a coin, they will deposit a fraction of it in a shared Coin bank which gets converted to EnergyLink Coins. SMW players with EnergyLink active can spend EnergyLink Coins to purchase inventory items during the map gameplay segment if they don't have any of the currently selected inventory item. More info in the Inventory system section.

### TrapLink

Shared traps across slots! TrapLink players will send their traps once activated and will receive equivalent ones as well from other slots. Can be highly chaotic in big sessions!

### RingLink

CURRENTLY DISABLED. NEEDS A MORE INVOLVED SYSTEM BECAUSE LIVES NO LONGER EXISTS.

Every time a player with RingLink collects a coin, everyone else with RingLink will receive a coin (or whatever is equivalent to a coin).

### DeathLink

**CURRENTLY DISABLED. I BROKE IT WHEN SA-1 GOT ADDED.**

Any time a player dies, everyone dies! Can be highly chaotic.

## Graphics Packs

Sadly, I don't have the skills to explain how Graphics for SMW works, but MM102 made an excellent videos that covers part of it, though it fully requires you to understand how to hack Super Mario World.

* SMW Character Creation Tutorial (Video URL)
* SMW character creation Aseprite script (Video URL)
* SNES GFX Tools for aseprite (Video URL)

The Adjuster will allow you create Graphics Packs with ease and supports the output from MM102's Aseprite script.

Any futher assistance will be pointed towards SMW Central, as they will provide better assistance than me.

Hosting an index for Graphics Packs similar to LTTP's is unlikely to happen as it may be super annoying to maintain.

## Setup

Waffles require a similar setup found in other SNES games in Archipelago, you can follow one of those guides or keep reading this one.
Required Software

 * Archipelago 0.6.5 or newer
 * Software or hardware capable of loading and playing SNES ROM files:
 * * snes9x-nwa (Recommended!)
 * * snes9x-rr
 * * BSNES-plus (Do not reset within the emulator, it'll lead to RAM corruption)
 * * FxPak

    Any emulator or method not listed here is NOT endorsed by the developer, you may have varied results in those.
 * Your Super Mario World (US) ROM file from the original cartridge. Archipelago or I can't provide these.
        MD5: cdd3c8c37322978ca8669b34bc89c804

## Optional Software

* Universal Tracker

## How to play

* Place the .apworld in your Archipelago/custom_worlds folder, or double-click the .apworld to do so automatically.
* Use ArchipelagoLauncher.exe to open the Launcher, and click on Generate Template Options to create template yamls for your custom .apworlds.
* Place the desired player yamls in the Players folder, and customize them as you see fit.
* Use ArchipelagoGenerate.exe to generate the game.
* Upload the generated game (in the output folder) on the website at https://archipelago.gg/uploads and create a new room.

## Final Notes

* snes9x-nwa will require enabling Enable Emu Network Control under the Netplay menu in the emulator.
* snes9x will not run the randomized ROM if the overclock hacks within the emulator are enabled. Please disable those.
* FxPak will take a good amount of time to process bought items in the inventory menu with EnergyLink (around 20-30 seconds) as fetching SRAM changes is a slow procedure.

