# Kingdom Hearts 2 Archipelago Setup Guide
<h2 style="text-transform:none";>Quick Links</h2>

- [Main Page](../../../../games/Kingdom%20Hearts%202/info/en)
- [Settings Page](../../../../games/Kingdom%20Hearts%202/player-settings)

<h2 style="text-transform:none";>Setting up the Mod Manager</h2>

Follow this Guide [KH2Rando.com](https://tommadness.github.io/KH2Randomizer/setup/Panacea-ModLoader/)

<h3 style="text-transform:none";>Loading A Seed</h3>

When you generate a game you will see a download link for a KH2 .zip seed on the room page. Download the seed then open OpenKH Mod Manager and click the green plus and `Select and install Mod Archive`. Make sure the seed is on the top of the list (Highest Priority)

<h3 style="text-transform:none";>Archipelago Compainion Mod and recommended mods</h3>

Load this mod just like the GoA ROM you did during the KH2 Rando setup. `JaredWeakStrike/APCompanion` Have this mod second highest priority below the .zip seed
Load this mod just like the GoA ROM you did during the KH2 Rando setup. `KH2FM-Mods-equations19/auto-save` Location doesn't matter, recommended in case of crashes.
Load this mod just like the GoA ROM you did during the KH2 Rando setup. `KH2FM-Mods-equations19/soft-reset` Location doesn't matter, recommneded in case of soft locks.

<h2 style="text-transform:none";>Using the KH2 Client</h2>

Once you have started the game through OpenKH Mod Manager and are on the title screen run the ArchipelagoKH2Client.exe. When you successfully connect to the server the client will automatically hook into the game to send/receive checks. If the client ever loses connection to the game, it will also disconnect from the server and you will need to reconnect. Make sure the game is open whenever you try to connect the client to the server otherwise it will immediately disconnect you. Most checks will be sent to you anywhere outside of a load or cutscene but if you obtain magic, you will need to pause your game to have it show up in your inventory, then enter a new room for it to become properly usable.

<h2 style="text-transform:none";>Generating a game</h2>

<h3 style="text-transform:none";>What is a YAML?</h3>

YAML is the file format which Archipelago uses in order to configure a player's world. It allows you to dictate which
game you will be playing as well as the settings you would like for that game.

YAML is a format very similar to JSON however it is made to be more human-readable. If you are ever unsure of the
validity of your YAML file you may check the file by uploading it to the check page on the Archipelago website. Check
page: [YAML Validation Page](/mysterycheck)

<h3 style="text-transform:none";>Creating a YAML</h3>

YAML files may be generated on the Archipelago website by visiting the games page and clicking the "Settings Page" link
under any game. Clicking "Export Settings" in a game's settings page will download the YAML to your system. Games
page: [Archipelago Games List](/games)

In a multiworld there must be one YAML per world. Any number of players can play on each world using either the game's
native coop system or using Archipelago's coop support. Each world will hold one slot in the multiworld and will have a
slot name and, if the relevant game requires it, files to associate it with that multiworld.

If multiple people plan to play in one world cooperatively then they will only need one YAML for their coop world. If
each player is planning on playing their own game then they will each need a YAML.

