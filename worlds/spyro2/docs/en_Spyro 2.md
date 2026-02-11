# Spyro 2: Ripto's Rage

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## Which version of the game is supported?

This is an Archipelago implementation of the PlayStation 1 version of Spyro 2: Ripto's Rage (1999), **not**
the Reignited Trilogy version (2018).  This randomizer requires use of the 
NTSC-U (North America, as opposed to the PAL/European or NTSC-J/Japanese) version, due to differences in the internal workings of the game.

## What does randomization do to this game?

When the player completes a task (such as collecting a talisman or orb), an item is sent.
Collecting one of these may not increment the player's orb counter or count as a received talisman,
while a check received from another game may do so.

This does not randomize the location of orbs, talismans, or gems, shuffle entrances, or make large-scale cosmetic changes to the game.

Unlocking doors requires collecting the corresponding items through Archipelago.  Unlike the vanilla game, you may not need to complete
the talisman check for every level to advance.  The HUD's orb count
shows how many orb items you have received, while the in game Guidebook shows which checks you have completed.

## What items and locations get shuffled?
Talismans and orbs are always shuffled.  Based on the player's options, skill points and milestones for reaching certain numbers of gems
per level or overall may also release checks.

The item pool will always contain 6 Summer Forest talismans, 8 Autumn Plains talismans, and 64 orbs.
Depending on the player's options, Moneybags unlocks may
be shuffled into the pool, rather than having the player pay Moneybags.  Leftover items will be "filler", based on the player's
options.  Examples include giving extra lives, temporary invisibility, changing Spyro's color, or making the player Sparxless.

## Which items can be in another player's world?

Any of the items which can be shuffled may also be placed into another player's world.

## What does another world's item look like in Spyro 2?

The visuals of the game are unchanged by the Archipelago randomization.  The Spyro 2 Archipelago Client
will display the obtained item and to whom it belongs.

## When the player receives an item, what happens?

The player's game and HUD will update accordingly, provided that they are in their save file.  Some effects,
such as healing Sparx, may operate with a delay to avoid unintended interactions in game.

Talisman count is not displayed in game.  The `showTalismanCount` command can be entered into the client to see the current counts.

Receiving a Moneybags unlock will complete the unlock automatically.

If for any reason the player is not in their save file when items come in, there may be a temporary desync.
Talisman and orb count will update the next time the player completes a check or receives an item.  Missed Moneybags
unlocks require the `clearSpyroGameState` command to be entered into the client.

## Unique Local Commands

The following command (without a slash or exclamation point) is available when using the S2AP client to play with Archipelago.

- `clearSpyroGameState` Resync your save file's received items with the server.  This may result in duplicate filler items.
If playing on a new save file, you will still need to get to the end of each level and defeat the bosses to progress in the game.
- `showTalismanCount` Prints how many Summer Forest Talisman items and how many Autumn Plains Talisman items the player has received.
- `useQuietHints` Suppresses hints for found locations to make the client easier to read. On by default.
- `useVerboseHints` Include found locations in hint lists. Due to Archipelago Server limitations, only applies to hints requested after this change.
- `showUnlockedLevels` Show which levels the player has unlocked in open world mode.
- `showGoal` Show what your completion goal is.
