# Schedule 1 Archipelago Randomizer Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest)
- [The Schedule I apworld](https://github.com/NewSoupVi/Archipelago/releases),
- [Thunderstore Mod Manager](https://www.overwolf.com/app/thunderstore-thunderstore_mod_manager)
- [Narcopelago Mod](https://thunderstore.io/c/schedule-i/p/Narcopelago/Narcopelago/)

## How to play

First, you need a room to connect to. For this, you or someone you know has to generate a game.  
This will not be explained here,
but you can check the [Archipelago Setup Guide](/tutorial/Archipelago/setup_en#generating-a-game).

You also need to have [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest) installed
and the [The Schedule I apworld](https://github.com/MacH8s/Narcopelago/releases/latest) installed into Archipelago.

### Install Mod

Install Thunderstore Mod Manager and open it.
Choose Schedule I and make a profile for Archipelago, name it whatever you like.
Search for 'Narcopelago' in the mod search and install it.
From there you can launch the game as Modded on the top right and your install has been complete! You must launch the game this way every time you want to play Archipelago.

### Joining Game

Use In-Game UI to connect to server. Once connected, Create a new world and skip the prologue.
Make sure to save as often as you can, and you are able to rejoin. Restart your game if you need to rejoin the world!
If you want to play with friends (Untested): Invite them to your lobby. All of you connect as same archipelago Info, Load into world.

## Switching Rooms
Restart your game to switch rooms. There may be some issues if you don't do so even if it shows things are working.


# Schedule 1

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

 - Sends checks from all missions.
 - Sends and receives all customer checks and items.
 - Customers can be unlocked by receiving them through archipelago when randomize_customers is true in the YAML.
 - checks for samples will be sent no matter the settings and are functional.
 - Dealers will send checks when recruiting regardless of settings.
 - Dealer AP unlock will allow user to then recruit them in game. Check is still possible when having them as a possible contact.
 - Suppliers will not be unlockable if suppliers are randomized and only unlocked through ap items
 - Suppliers give checks for unlocking them when suppliers are not randomized
 - Every Action that would cause cartel influence in a region to drop is a check (x7 per region)
 - Unable to reduce cartel influence naturally and cartel influence items added to pool when randomize_cartel_influence is true
 - Level up rewards are suppressed when randomize_level_up_rewards is true
 - Level up rewards are added to the item pool when randomize_level_up_rewards is true
 - Whenever you'd nomrally get unlocks for leveling up, you get a check regardless of the option
 - Deathlink is sent when a player dies or when they arrested. Recieved deathlink causes player to get arrested
 - Property and busniesses give checks when purchased
 - Randomized properties or businesses will not be unlocked when purchased if randomization on, properties and/or businesses will be added to the item pool
 - Recipe checks are sent when recipes are learned
 - Cash for trash are sent every 10 trash burned
 - Filler items will be sent as deaddrop quests

## Once I'm inside Schedule1, how do I play Schedule1AP

Use In-Game UI to connect to server. Once connected, Create a new world and skip the prologue.
Make sure to save as often as you can, and you are able to rejoin. Restart your game if you need to rejoin the world!
If you want to play with friends (Untested): Invite them to your lobby. All of you connect as same archipelago Info, Load into world.

## A statement on the ownership over Schedule1AP

Schedule I apworld is MIT license. Created by MacH8s


# [Archipelago](https://archipelago.gg) ![Discord Shield](https://discordapp.com/api/guilds/731205301247803413/widget.png?style=shield) | [Install](https://github.com/ArchipelagoMW/Archipelago/releases)

Archipelago provides a generic framework for developing multiworld capability for game randomizers. In all cases,
presently, Archipelago is also the randomizer itself.

Currently, the following games are supported:

* The Legend of Zelda: A Link to the Past
* Factorio
* Subnautica
* Risk of Rain 2
* The Legend of Zelda: Ocarina of Time
* Timespinner
* Super Metroid
* Secret of Evermore
* Final Fantasy
* VVVVVV
* Raft
* Super Mario 64
* Meritous
* Super Metroid/Link to the Past combo randomizer (SMZ3)
* ChecksFinder
* Hollow Knight
* The Witness
* Sonic Adventure 2: Battle
* Starcraft 2
* Donkey Kong Country 3
* Dark Souls 3
* Super Mario World
* Pokémon Red and Blue
* Hylics 2
* Overcooked! 2
* Zillion
* Lufia II Ancient Cave
* Blasphemous
* Wargroove
* Stardew Valley
* The Legend of Zelda
* The Messenger
* Kingdom Hearts 2
* The Legend of Zelda: Link's Awakening DX
* Adventure
* DLC Quest
* Noita
* Undertale
* Bumper Stickers
* Mega Man Battle Network 3: Blue Version
* Muse Dash
* DOOM 1993
* Terraria
* Lingo
* Pokémon Emerald
* DOOM II
* Shivers
* Heretic
* Landstalker: The Treasures of King Nole
* Final Fantasy Mystic Quest
* TUNIC
* Kirby's Dream Land 3
* Celeste 64
* Castlevania 64
* A Short Hike
* Yoshi's Island
* Mario & Luigi: Superstar Saga
* Bomb Rush Cyberfunk
* Aquaria
* Yu-Gi-Oh! Ultimate Masters: World Championship Tournament 2006
* A Hat in Time
* Old School Runescape
* Kingdom Hearts 1
* Mega Man 2
* Yacht Dice
* Faxanadu
* Saving Princess
* Castlevania: Circle of the Moon
* Inscryption
* Civilization VI
* The Legend of Zelda: The Wind Waker
* Jak and Daxter: The Precursor Legacy
* Super Mario Land 2: 6 Golden Coins
* shapez
* Paint
* Celeste (Open World)
* Choo-Choo Charles
* APQuest
* Satisfactory
* EarthBound

For setup and instructions check out our [tutorials page](https://archipelago.gg/tutorial/).
Downloads can be found at [Releases](https://github.com/ArchipelagoMW/Archipelago/releases), including compiled
windows binaries.

## History

Archipelago is built upon a strong legacy of brilliant hobbyists. We want to honor that legacy by showing it here.
The repositories which Archipelago is built upon, inspired by, or otherwise owes its gratitude to are:

* [bonta0's MultiWorld](https://github.com/Bonta0/ALttPEntranceRandomizer/tree/multiworld_31)
* [AmazingAmpharos' Entrance Randomizer](https://github.com/AmazingAmpharos/ALttPEntranceRandomizer)
* [VT Web Randomizer](https://github.com/sporchia/alttp_vt_randomizer)
* [Dessyreqt's alttprandomizer](https://github.com/Dessyreqt/alttprandomizer)
* [Zarby89's](https://github.com/Ijwu/Enemizer/commits?author=Zarby89)
  and [sosuke3's](https://github.com/Ijwu/Enemizer/commits?author=sosuke3) contributions to Enemizer, which make up the
  vast majority of Enemizer contributions.

We recognize that there is a strong community of incredibly smart people that have come before us and helped pave the
path. Just because one person's name may be in a repository title does not mean that only one person made that project
happen. We can't hope to perfectly cover every single contribution that lead up to Archipelago, but we hope to honor
them fairly.

### Path to the Archipelago

Archipelago was directly forked from bonta0's `multiworld_31` branch of ALttPEntranceRandomizer (this project has a
long legacy of its own, please check it out linked above) on January 12, 2020. The repository was then named to
_MultiWorld-Utilities_ to better encompass its intended function. As Archipelago matured, then known as
"Berserker's MultiWorld" by some, we found it necessary to transform our repository into a root level repository
(as opposed to a 'forked repo') and change the name (which came later) to better reflect our project.

## Running Archipelago

For most people, all you need to do is head over to
the [releases page](https://github.com/ArchipelagoMW/Archipelago/releases), then download and run the appropriate
installer, or AppImage for Linux-based systems.

If you are a developer or are running on a platform with no compiled releases available, please see our doc on
[running Archipelago from source](docs/running%20from%20source.md).

## Related Repositories

This project makes use of multiple other projects. We wouldn't be here without these other repositories and the
contributions of their developers, past and present.

* [z3randomizer](https://github.com/ArchipelagoMW/z3randomizer)
* [Enemizer](https://github.com/Ijwu/Enemizer)
* [Ocarina of Time Randomizer](https://github.com/TestRunnerSRL/OoT-Randomizer)

## Contributing

To contribute to Archipelago, including the WebHost, core program, or by adding a new game, see our
[Contributing guidelines](/docs/contributing.md).

## FAQ

For Frequently asked questions, please see the website's [FAQ Page](https://archipelago.gg/faq/en/).

## Code of Conduct

Please refer to our [code of conduct](/docs/code_of_conduct.md).
