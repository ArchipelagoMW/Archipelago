# Zork Grand Inquisitor

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and export a
configuration file.

## What does randomization do to this game?

A majority of inventory items you can normally pick up are completely removed from the game (e.g. the lantern won't be 
in the crate, the mead won't be at the fish market, etc.). Instead, these items will be distributed in the multiworld.
This means that you can expect to access areas and be in a position to solve certain puzzles in a completely different 
order than you normally would.

Subway and teleporter destinations are initially locked and need to be unlocked by receiving the corresponding item in 
the multiworld. This alone enables creative routing in a game that would otherwise be rather linear. The Crossroads 
destination is always unlocked for both the subway and teleporter to prevent softlocks.

Inventory items necessary to complete time tunnels are revealed (and can be picked up) instead of directly inserted into
the player's inventory. This is to prevent issues because they are only meant to be held by totemized characters.

The blank spell scroll crate in the Spell Lab has been locked and requires an item to open it.

## What item types are distributed in the multiworld?

- Inventory items
- Pouch of Zorkmids
- Spells
- Totems
- Subway destinations
- Teleporter destinations
- Time tunnel item reveals (e.g. Playing cards in Past Port Foozle, Torches and Grue Eggs in White House, etc.)
- Spell Lab blank spell scroll crate unlock

## When the player receives an item, what happens?

- **Inventory items**: Directly added to the player's inventory.
- **Pouch of Zorkmids**: Appears on the inventory screen. The player can then pick up Zorkmid coins from it.
- **Spells**: Learned and directly added to the spell book.
- **Totems**: Appears on the inventory screen.
- **Subway destinations**: The destination button on the subway map becomes functional.
- **Teleporter destinations**: The destination can show up on the teleporter screen.
- **Time tunnel item reveals**: All items inside the time tunnel are revealed at once and can be picked up.
- **Spell Lab blank spell scroll crate unlock**: The crate is unlocked and blank scrolls can be picked up.

## What is considered a location check in Zork Grand Inquisitor?

- Solving puzzles
- Accessing certain areas for the first time
- Dying in unique ways (Optional; Deathsanity option)

## What is the victory condition?

Victory is achieved when the 3 artifacts of magic are retrieved and placed inside the walking castle.

## Can I use the save system without a problem?

Absolutely! The save system is fully supported (and its use is in fact strongly encouraged!). You can save and load your 
game as you normally would and the client will automatically sync your items with what you should have in that game 
state.

## Unique Local Commands
The following commands are only available when using the Zork Grand Inquisitor Client to play the game with Archipelago.

- `/zork` Attempts to attach to a running instance of Zork Grand Inquisitor. If successful, the client will then be able 
   to read and control the state of the game.

## Known issues

- Puzzles that yield an inventory item on the same screen when solved (fairly uncommon) will sometimes show that 
  inventory item even though it can't be picked up or interacted with. This is just a visual glitch. It happens because 
  even though the game state says the item isn't there, the screen isn't redrawn after the puzzle is solved.
- Time tunnel items will keep reappearing after you pick them up when the screen is redrawn. Mildly annoying, but 
  doesn't affect gameplay at all. Just don't pick them up again.
- Since the client is reading and manipulating the game's memory, rare game crashes can happen. If you encounter one, 
  simply restart the game, load your latest save and use the `/zork` command again in the client. Nothing will be lost.