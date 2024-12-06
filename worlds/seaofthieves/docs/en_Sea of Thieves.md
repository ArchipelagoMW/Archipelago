# Sea of Thieves

## Introduction

This is not a mod/hack and you will not be at risk of being banned while running for hacking.
This application works by logging into the Sea of Thieves account on www.seaofthieves.com and viewing your accounts
progression data.

## Modes of Play

Typically randomizers have a "world" that a single player plays when finding locations. This randomizer has two modes
you can play using

- Crew Mode: Your "ship and its crew" are the player. Anything done by your "ship and its crew" is treated as one world.
- Pirate Mode: Your "pirate" is the player. Anyting done by your "pirate" is treated as one world.

Using the modes above, here are some examples of ways to play:

- Possible: My friend and I want to play a coop multiworld of SOT. We will generate 1 world and run it in ship mode
  while both on the same ship with 1 client running.
- Possible: My friend and I want to play a 2 player multiworld of SOT but we want to be on the same ship. We will
  generate 2 worlds and run them in pirate mode with 2 clients running.
- Possible: My friend and I want to play a 2 player multiworld of SOT but we each want to be on our own ship. We will
  generate 2 worlds and run them in pirate mode with 2 clients running.
- Not Possible: My squad of 4 wants to play a 2 player multiworld each of us on a team of two but on the same galleon.

## What does randomization do to this game?

Most things that are trackable through your capainancy page on www.seaofthieves.com are locations containing randomized
items.
When completing a location, you are only rewarded the item at the location if you have the required items to visit the
location.
The following items are randomized:

Sails
- Sail - Unlocks the ability to check locations away from the starting island
- Ashen Sail - Unlocks the ability to check locations in the Devil's Roar

Voyage Bundles
- Voyages of Sea Forts - Allows location rewards related to Fortresses
- Voyages of Gold Hoarders - Allows location rewards for completing Voyages
- Voyages of Merchants - Allows location rewards for completing voyages
- Voyages of Souls - Allows location rewards for completing voyages
- Voyages of Athena - Allows location rewards for completing voyages
- Voyages of Reaper - Allows location rewards for selling any Reaper chest
- Voyages of Tall Tales - Allows location rewards for completeing Tall Tales
- Voyages of Destiny - Allows access to the Skull of Destiny (required for Fort of the Damned Entry)

Emissary Flags
- Emissary of Gold Hoarders - Allows location rewards for emmissary actions
- Emissary of Merchants - Allows location rewards for emmissary actions
- Emissary of Souls - Allows location rewards for emmissary actions
- Emissary of Athena - Allows location rewards for emmissary actions
- Emissary of Reaper - Allows location rewards for emmissary actions

Shop Catelogs
- Catalog of Ancient Spire - Allows access to the shop
- Catalog of Dagger Tooth - Allows access to the shop
- Catalog of Galleon's Grave - Allows access to the shop
- Catalog of Morrow's Peak - Allows access to the shop
- Catalog of Plunder - Allows access to the shop
- Catalog of Sanctuary - Allows access to the shop

Barrels
- Food Barrel - Allows access to locations that expect you to have food (note read Stove)
- Cannon Barrel - Allows access to locations that expect you to have cannonballs (note read Ship Weapons)
- Wood Barrel - Allows access to locations that would expect you to repair the ship

Misc. Items
- Personal Weapons - Allows access to pirate combat related loctions (ex: Kill Skeleton quest)
- Ship Weapons - Allows access to ship combat related locations (ex: Ghost Ship voyage)
- Fishing Rod - Allows location rewards for fishing
- Shovel - Allows location rewards for digging related locations
- Stove - Allows access to EAT, COOK, BURN checks that would usually require cooking
- Progressive Wallet (amount = 2) - Increases your fund limit for the client shop

Victory Condition
- Pirate Legend - Once achieved, you win. This items is awarded on FOTD completion 

The following items are filler:
- Gold Coins
- Ancient Coins
- Dabloons

The following items are traps:

- Kraken - Makes you lose your client money sent to your session

## What can you do with Gold, Dabloon, and Ancient Coin?

The game client tracks how much money you make in game. It also tracks how much money other players give you.
You can spend this money on the `/shop` of the client

## What is the goal of this game when randomized?

The goal is to defeat The Ghost of Graymarrow at the Fort of the Damned.
However you cannot simply sail to his island, you must first:

* Aquire Emissary Seals by completing a single voyage for specific trading companies
* Aquire the Voyages of Destiny so that you can initiate the Fort of the Damned

The amount of seals required is configurable (0-5).

## Which of my items can be in another player's world?

Your world will always contain:

- All 5 faction Seals
- The Sail
- Pirate Legend on Fort of the Damned Completion

All other items are shuffled.

## How does the game know I complete a check?

The SOT client periodically scans the stats of a ship from SOT's website.
In general, when a stat related to a location in game changes, the locations reward is sent to the correct player.
The location reward will never trigger unless you have all the required items to logically complete the check.
You can check what locations are in logic by typing `/locs` in the client

WARNING: Make sure you only do checks that the client says are possible!!! Even if you know an item exists on a specific
location that lets you do another nearby, you must wait till the client awards you the item first even if you know it is
comming.

## How does the shop work?

This randomizer allows for a client shop. While playing the game, whenever you sell anything in game or if you recieve a
gold, dabloon, or ancient coin item, your personal money in the tracking client will increase. This fake money can be
exchanged for items in the `/shop` with the `/buy` command.
Your personal fake money wallet has a limit though, to increase its size you will need to find the Wallet item.

## Unique Local Commands

The following commands are only available when using the Sea of Thieves Client to play with Archipelago. You can list
them any time in the client with `/help`.

* `/hints` Shows hints you have purchased with `/buy` in the `/shop`
* `/tracker` Shows the status of the autotracker
* `/forceunlock` Removes all logic requirements for every location. Only use if the game logic is buggy and preventing you from accessing a location
* `/shop` Opens the shop
* `/buy #` Buys an item from the shop
* `/locs` Shows all possible locations with your current items that were not excluded by game settings.
* `/locs -f` Shows all possible locations with your current items
* `/complete <locID>` Force completes a location. You can use any variation of `/locs` to see the location ids
* `/complete -all` Force completes all locations currently shown by `/locs`
* `/complete -allf` Force completes all locations currently shown by `/locs -f`
* `/connect <ip:port>` Connects to host
* `/mrkrabs` Gives you a large amount of money
* `/setmode <id>`, Sets the mode of the game. Use and id of "NA" for pirate mode. Use an id of a numeric value to set
  your corresponding ship to be tracked
* `/setcookie`, Sets your authentication cookie for the auto-tracker
