# Zork Grand Inquisitor

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
configuration file.

## Is a tracker available for this game?

Yes! You can download the latest PopTracker pack for Zork Grand Inquisitor [here](https://github.com/SerpentAI/ZorkGrandInquisitorAPTracker/releases/latest).

## What does randomization do to this game?

A majority of inventory items you can normally pick up are completely removed from the game (e.g. the lantern won't be 
in the crate, the mead won't be at the fish market, etc.). Instead, these items will be distributed in the multiworld.
This means that you can expect to access areas and be in a position to solve certain puzzles in a completely different 
order than you normally would.

Subway, teleporter and totemizer destinations are initially locked and need to be unlocked by receiving the 
corresponding item in the multiworld. This alone enables creative routing in a game that would otherwise be rather 
linear. The Crossroads destination is always unlocked for both the subway and teleporter to prevent softlocks. Until you
receive your first totemizer destination, it will be locked to Newark, New Jersey. 

Important hotspots are also randomized. This means that you will be unable to interact with certain objects until you 
receive the corresponding item in the multiworld. This can be a bit confusing at first, but it adds depth to the
randomization and makes the game more interesting to play.

You can travel back to the surface without dying by looking inside the bucket. This will work as long as the rope is
still attached to the well.

Attempting to cast VOXAM will teleport you back to the Crossroads. Fast Travel!

## What item types are distributed in the multiworld?

- Inventory items
- Pouch of Zorkmids
- Spells
- Totems
- Subway destinations
- Teleporter destinations
- Totemizer destinations
- Hotspots (with option to start with the items enabling them instead if you prefer not playing with the randomization 
  of hotspots)

## When the player receives an item, what happens?

- **Inventory items**: Directly added to the player's inventory.
- **Pouch of Zorkmids**: Appears on the inventory screen. The player can then pick up Zorkmid coins from it.
- **Spells**: Learned and directly added to the spell book.
- **Totems**: Appears on the inventory screen.
- **Subway destinations**: The destination button on the subway map becomes functional.
- **Teleporter destinations**: The destination can show up on the teleporter screen.
- **Totemizer destinations**: The destination button on the panel becomes functional.
- **Hotspots**: The hotspot becomes interactable.

## What is considered a location check in Zork Grand Inquisitor?

- Solving puzzles
- Accessing certain areas for the first time
- Triggering certain interactions, even if they aren't puzzles per se
- Dying in unique ways (Optional; Deathsanity option)

## The location check names are fun but don't always convey well what's needed to unlock them. Is there a guide?

Yes! You can find a complete guide for the location checks [here](https://gist.github.com/nbrochu/f7bed7a1fef4e2beb67ad6ddbf18b970).

## What is the victory condition?

Victory is achieved when the 3 artifacts of magic are retrieved and placed inside the walking castle.

## Can I use the save system without a problem?

Absolutely! The save system is fully supported (and its use is in fact strongly encouraged!). You can save and load your 
game as you normally would and the client will automatically sync your items and hotspots with what you should have in 
that game state. 

Depending on how your game progresses, there's a chance that certain location checks might become missable. This 
presents an excellent opportunity to utilize the save system. Simply make it a habit to save before undertaking 
irreversible actions, ensuring you can revert to a previous state if necessary. If you prefer not to depend on the save 
system for accessing missable location checks, there's an option to automatically unlock them as they become 
unavailable.

## Unique Local Commands
The following commands are only available when using the Zork Grand Inquisitor Client to play the game with Archipelago.

- `/zork` Attempts to attach to a running instance of Zork Grand Inquisitor. If successful, the client will then be able 
   to read and control the state of the game.
- `/brog` Lists received items for Brog.
- `/griff` Lists received items for Griff.
- `/lucy` Lists received items for Lucy.
- `/hotspots` Lists received hotspots.

## Known issues

- You will get a second rope right after using GLORF (one in your inventory and one on your cursor). This is a harmless
  side effect that will go away after you store it in your inventory as duplicates are actively removed.
- After climbing up to the Monastery for the first time, a rope will forever remain in place in the vent. When you come
  back to the Monastery, you will be able to climb up without needing to combine the sword and rope again. However, when
  arriving at the top, you will receive a duplicate sword on a rope. This is a harmless side effect that will go away
  after you store it in your inventory as duplicates are actively removed.
- Since the client is reading and manipulating the game's memory, rare game crashes can happen. If you encounter one, 
  simply restart the game, load your latest save and use the `/zork` command again in the client. Nothing will be lost.
