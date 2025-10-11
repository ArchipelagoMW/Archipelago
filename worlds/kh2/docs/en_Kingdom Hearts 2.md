# Kingdom Hearts 2

## Changes from the vanilla game

This randomizer creates a more dynamic play experience by randomizing the locations of most items in Kingdom Hearts 2. Currently all items within Chests, Popups, Get Bonuses, Form Levels, Summon Levels,and Sora's Levels are randomized. This allows abilities that Sora would normally have to be placed on Keyblades with random stats. Additionally, there are several options for ways to finish the game, allowing for different goals beyond beating the final boss.

## Where is the options page

The [player options page for this game](../player-options) contains all the options you need to configure and export a config file.


## What is randomized in this game?


- Chests
- Popups
- Get Bonuses
- Form Levels
- Summon Levels
- Sora's Levels
- Keyblade Stats
- Keyblade Abilities

## What Kingdom Hearts 2 items can appear in other players' worlds?


Every item in the game except for abilities on weapons.

## What is The Garden of Assemblage "GoA"?


The Garden of Assemblage Mod made by Sonicshadowsilver2 and Num turns the Garden of Assemblage into a “World Hub” where each portal takes you to one of the game worlds (as opposed to having a world map). This allows you to enter worlds at any time, and world progression is maintained for each world individually.

## What does another world's item look like in Kingdom Hearts 2?


In Kingdom Hearts 2, items which need to be sent to other worlds appear in any location that has a item in the vanilla game. They are represented by the Archipelago icon, and must be "picked up" as if it were a normal item. Upon obtaining the item, it will be sent to its home world.

## When the player receives an item, what happens?


It is added to your inventory.

## What Happens if I die before Room Saving?


When you die in vanilla Kingdom Hearts 2, you are reverted to the last non-boss room you entered and your status is reverted to what it was at that time. However, in archipelago, any item that you have sent/received will not be taken away from the player, any chest you have opened will remain open, and you will keep your level, but lose the experience.


For example, if you are fighting Roxas, receive Reflect Element, then die mid-fight, you will keep that Reflect Element. You will still need to pause your game to have it show up in your inventory, then enter a new room for it to become properly usable.

## Customization options:


- Choose a goal from the list below (with an additional option to Kill Final Xemnas alongside your goal).
    1. Obtain Three Proofs.
    2. Obtain a desired amount of Lucky Emblems.
    3. Obtain a desired amount of Bounties that are on late locations.
- Customize how many World-Locking Items you need to progress in that world.
- Customize the amount of World-Locking Items you start with.
- Customize how many of Sora's Levels are locations.
- Customize the EXP multiplier for Sora, his Drive Forms, and his Summons.
- Customize the available abilities on keyblades.
- Customize the amount and level of progressive movement (Growth Abilities) you start with.
- Customize start inventory, i.e., begin every run with certain items or spells of your choice.

## What are Lucky Emblems?
Lucky Emblems are items that are required to beat the game if your goal is "Lucky Emblem Hunt".<br>
You can think of these as requiring X number of Proofs of Nonexistence to open the final door.

## What is Hitlist/Bounties?
The Hitlist goal adds "bounty" items to select late-game fights and locations, and you need to collect X number of them to win.<br>
The list of possible locations that can contain a bounty:

- Each of the 13 Data Fights
- Max level (7) for each Drive Form
- Max level (7) of Summons
- Last song of Atlantica
- Sephiroth
- Lingering Will
- Starry Hill
- Transport to Remembrance
- Goddess of Fate cup and Hades Paradox cup

## Quality of life:


With the help of Shananas, Num, and ZakTheRobot we have many QoL features such are:


- Faster Wardrobe.
- Faster Water Jafar Chase.
- Faster Bulky Vendors
- Carpet Skip.
- Start with Lion Dash.
- Faster Urns.
- Removal of Absent Silhouette and go straight into the Data Fights.
- And much more can be found at [Kingdom Hearts 2 GoA Overview](https://tommadness.github.io/KH2Randomizer/overview/)

## What does each mod do?

1. Archipelago Companion:
- This mod under the hood is a collection of smaller mods that change things such as item icons and specific things in the GOA that make it work better for archipelago.
This mod needs to be above the GOA because it has to overwrite the GOA lua script with its own for things to work according to the client. Such as giving you consumable items
I.E potions, ethers, boosts etc.
- This mod also has some consistent mods that should always be on such as Port Royal Map Skip, Better STT and Allowing you to enter drive forms where you shouldnt normally be able to (Dive to the Heart before Data Fights, 100 Acre Woods) Credit to KSX on nexus mods for the basis of the script that does this that was changed for it to work in AP.
- Changes The Absent Silhouettes to be the data version instead of how it works traditionally where you would defeat the absent silhouette version to unlock the data fight using the same entry point.
- The biggest misconception is that the APCompanion is the client/connects to the server like other game's companions mod. This is not the case. The apcompanion is mainly a collection of static modifications that were taken out of the apworld to reduce seed size.
- There are many little things this mod does so if you have any questions feel free to ping me (@JaredWeakStrike) in the archipelago discord and I can hopefully answer your question.
2. TopazTK/ArchipelagoEnablers
- This is in sense another companion mod and is required for many things to work correctly.
- Notification System: Allows the client to flip a byte in game for it to trigger a puzzle piece popup/information popup/chest popup
- Deathlink: Allows the client to flip a byte to kill sora when the client sets sora's hp to 0 (normally it doesnt kill sora when his hp is set to 0)
- Instant Movement: No need to pause when you obtain movement for it to update.
- Instant Magic: No need to room transition to update magic
- Autosave: Creates a save file in slot 99 that is treated like a normal save file. It is made on room transition. Do note: it does overwrite any save in slot 99
- Soft Reset: All shoulder buttons+start. For ds4 its L1+l2+R1+R2+Options for example
3. TopazTK/ArchipelagoEnablersLITE
- Everything in Archipelago Enablers EXCEPT auto save and soft reset
- This mod is to be used with H2FM-Mods-equations19/auto-save or H2FM-Mods-equations19/soft-reset
- Both equations' mods require KH2FM-Mods-equations19/KH2-Lua-Library
- equations19/soft-reset: Use all shoulder buttons+start to reset 
- equations19/auto-save: To load an auto-save, hold down the Select or your equivalent on your preferred controller while choosing a NO PROGRESS save file i.e. A save file that is at the start of the game and has no progress made. Make sure to hold the button down the whole time.
