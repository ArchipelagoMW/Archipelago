# Satisfactory Setup Guide

<!-- Spellchecker config - cspell:ignore FICSIT Randomizer Plando -->

## Required Software

- Satisfactory, either
  - Steam [Satisfactory (Steam)](https://store.steampowered.com/app/526870/Satisfactory/)
  - Epic [Satisfactory (Epic)](https://www.epicgames.com/store/en-US/product/satisfactory/home)
- Satisfactory Mod Manager, either
  - Automatically via [smm.ficsit.app](https://smm.ficsit.app/) or
  - Manually via [latest stable release on GitHub](https://github.com/satisfactorymodding/SatisfactoryModManager/releases/latest/)

## Overview

This guide walks you through installing the Satisfactory Archipelago mod via the Satisfactory Mod Manager,
configuring an Archipelago slot for Satisfactory,
and playing the game with a Satisfactory client.

### Defining Some Terms

In Archipelago, multiple Satisfactory worlds may be played simultaneously.
Each of these worlds must be hosted by a Satisfactory Host which is connected to the Archipelago Server via the Archipelago mod.

This guide uses the following terms to refer to the software:

- **Archipelago Server** - The central Archipelago server, which connects all games to each other.
- **Archipelago Client** - The desktop application used by many Archipelago games as middleware. Satisfactory does NOT require this software, unless you would like to generate a world locally.
- **Archipelago (Satisfactory) mod** - The Satisfactory mod which implements Archipelago in-game functionality and connectivity.
  All Satisfactory hosts and clients must have this mod installed.
- **Satisfactory Host** - The Satisfactory instance which will be used to host the game.
  This could be a Satisfactory Client using Singleplayer or host-and-play multiplayer, or it could be a Satisfactory dedicated server.
  It must be supplied with the Archipelago Server connection details.
  *Any number of Satisfactory Clients may connect to this server.*
- **Satisfactory Client** - The Satisfactory instance (game client) with which additional players can use to connect to the same Satisfactory world.

### What a Playable State Looks Like

- An Archipelago Server
- One running modded Satisfactory Host (game client or dedicated server) per Satisfactory world
- Optionally, additional modded Satisfactory Clients for additional players

### Additional Resources

- Satisfactory Wiki: [Satisfactory Official Wiki](https://satisfactory.wiki.gg/wiki/)
- Satisfactory Modding 'Frequently Asked Questions' page: [Satisfactory Modding Documentation FAQ](https://docs.ficsit.app/satisfactory-modding/latest/faq.html)
- Satisfactory Archipelago Item names (for hints/starting inventory/etc.) can be found [on the mod's github](https://github.com/Jarno458/Archipelago/blob/Satisfactory/worlds/satisfactory/Items.py)

## Preparing to Play Satisfactory Archipelago

### Installing Satisfactory

Purchase and install Satisfactory via one the sources linked [above](#required-software).
Launch the game at least once to ensure that the Mod Manager can detect the game's install location.

Make sure that you are running the correct branch of the game (Release or Experimental) that Archipelago supports.
Learn how to switch branches here:
[Satisfactory Modding Documentation FAQ: Switching Branches](https://docs.ficsit.app/satisfactory-modding/latest/faq.html#_how_do_i_get_the_experimental_or_early_access_branch_of_the_game)

### Installing Satisfactory Mod Manager

The Mod Manager is used to install and manage mods for Satisfactory.
It automatically detects your game install location and automatically handles mod dependencies for you.

Download the Mod Manager here:
[Satisfactory Mod Manager automatic download via ficsit.app](https://smm.ficsit.app/)

Directions for setting and using up the Mod Manager can be found here:
[Satisfactory Modding Documentation FAQ: Installing the Mod Manager](https://docs.ficsit.app/satisfactory-modding/latest/ForUsers/SatisfactoryModManager.html)

### Installing the Archipelago Mod

Once the Mod Manager is installed you can install mods directly in the manager or via the Satisfactory Mod Repository website.

Inside the Mod Manager, search for and install the "Archipelago Randomizer".
Alternatively, visit the mod page: [Archipelago Randomizer mod on ficsit.app](https://ficsit.app/mod/Archipelago).
Once on the mod page, click the "Install" link in the Latest Versions card.

The Mod Manager will install all required dependency mods for you with no additional action required.

As soon as you have the relevant mods installed,
you do not need to launch the game through the Mod Manager -
desktop shortcuts, Steam, Epic. etc. will all launch the game with mods still loaded.

### Installing Additional Mods

You may also wish to install some of the suggested mods mentioned on the
[Archipelago Info page for Satisfactory](/games/Satisfactory/info/en#additional-mods).
If you are playing multiplayer in the same Satisfactory world, all Satisfactory Clients should have the same mods installed.
The Mod Manager's profile import/export feature makes coordinating this easy.

## Connecting to Someone Else's Satisfactory Game

If you are joining someone else's existing Satisfactory game,
your setup process is almost complete.
If your host has sent you a Mod Manager profile containing additional mods,
be sure to install it.
See [Satisfactory Modding Documentation: Profiles](https://docs.ficsit.app/satisfactory-modding/latest/ForUsers/SatisfactoryModManager.html#_profiles) for more information.

To get started playing, connect to the Satisfactory Host using the connection details provided by your host.
([Satisfactory Wiki: Joining a Session](https://satisfactory.wiki.gg/wiki/Multiplayer#Joining_a_session))

See the [Troubleshooting section below](#troubleshooting) if you encounter any issues.

## Hosting Your Own Satisfactory Game

If you're hosting your own Satisfactory game,
you will need to configure an Archipelago world and set up the Satisfactory Host you will be playing on.

### Create a Config (.yaml) File

#### What is a config file and why do I need one?

Your config file contains a set of configuration options
which provide the generator with information about how it should generate your game.
Each player of a multiworld will provide their own config file.
This setup allows each player to enjoy an experience customized for their taste,
and different players in the same multiworld can all have different options.

#### Where do I get a config file?

The Player Settings page on the website
allows you to configure your personal settings and export a config file from them.
Satisfactory player settings page: [Satisfactory Settings Page](/games/Satisfactory/player-settings)

#### Verifying Your Config File

If you would like to validate your config file to make sure it works,
you may do so on the YAML Validator page.
YAML Validator page: [Yaml Validation Page](/mysterycheck)

#### Starting Inventory

The Player Settings page provides a few options for controlling what materials you start with
and when certain key technologies are unlocked.
Any Resource Bundle type items added to your starting inventory will be delivered to your player inventory when you initally spawn,
unless they can't fit, in which case they can be collected by building an Archipelago Portal.

Advanced users can use Plando, Weighted Options, and manual yaml editing to further configure the starting inventory.
If you don't wish to use these techniques, consider using Satisfactory's
[Advanced Game Settings (Satisfactory Wiki)](https://satisfactory.wiki.gg/wiki/Advanced_Game_Settings)
to spawn the items you desire.

#### Advanced Configuration

Advanced users can utilize the
[Weighted Options Page](/weighted-options)
and [Plando](/tutorial/Archipelago/plando)
to futher customize their experience.

### Generating and Hosting the Multiworld

Generating a game and hosting an Archipelago server is explained in the [Archipelago Setup Guide](/tutorial/Archipelago/setup/en).

### Creating the Satisfactory World

After you have installed the mods, launch the game via the Mod Manager or via your preferred method.
Once the game has launched, start creating a new game.

Select your starting location and Skip Intro if you wish to skip the tutorial sequence,
then click the "Mod Savegame Settings" button in the bottom right corner of the screen.
Next, enter the connection details in the relevant fields.

- **Server URI**: Archipelago Server URI and port, for example, `archipelago.gg:49236`
- **User Name**: The name you entered as your Player Name when you created your config file. It's also listed in the Name column of your room page.
- **Password**: The password for your Archipelago room, blank if you did not assign or receive one.

Note that the Satisfactory Host/Client does *not* need a copy of your Archipelago config file.
The mod communicates with the Archipelago Server, which already has your config file,
to generate the required content at runtime.

Consider setting the following options in the "Options" > "Gameplay" section, especially because they are per-user and persist across your game saves:

- **Creature Hostility**: `Default` (the game's default). Some of the mod's Traps involve creatures, and having them Passive or Retaliate cheapens the experience.
- **Keep Inventory**: `Keep Everything` or `Keep Equipment` (the game's default). Although dying and dropping items will never lock you out of progression, Free Samples and Bundles means you can easily gain items you can't easily replace.

### Verifying Connection Success

After you have created your new world,
you should see in-game chat messages confirming that you have connected to the Archipelago Server.

You can issue the `/help` command in the game's chat to list available commands, such as `/hint`.
For more information about the commands you can use, see the [Commands Guide](/tutorial/Archipelago/commands/en).
Note that Archipelago commands are not prefixed with `!` inside of Satisfactory.
You may wish to use the Text Client to run commands since Satisfactory's in game chat is not very user friendly.

Check out the HUB to get started!

See the [Troubleshooting section below](#troubleshooting) if you encounter any issues.

### Allowing Other People to Join Your Game

Additional players can join your game using the game's built-in multiplayer functionality.
For more information, see [Satisfactory Wiki: Multiplayer](https://satisfactory.wiki.gg/wiki/Multiplayer).

Have anyone you want to join follow the [Preparing to Play Satisfactory Archipelago](#preparing-to-play-satisfactory-archipelago) section above.
If you're using any additional mods, be sure to export a profile using the Mod Manager for players to import.
[Satisfactory Modding Documentation: Sharing Mod Manager Profiles](https://docs.ficsit.app/satisfactory-modding/latest/ForUsers/SatisfactoryModManager.html#_sharing_profiles)

As mentioned above, it is possible to use a Satisfactory dedicated Server as your Satisfactory Host.
The process for setting up and configuring a dedicated server is out of scope of this guide,
but you can find more information here: [Satisfactory Modding Documentation: Installing Mods on Dedicated Servers](https://docs.ficsit.app/satisfactory-modding/latest/ForUsers/DedicatedServerSetup.html).

It is important to note that the Satisfactory Archipelago mod
is not yet compatible with Linux dedicated servers - only Windows dedicated servers are supported.

### Port Changes

If you are using a public Archipelago Server to host your game,
rooms are automatically put to sleep after a period of inactivity.
The room can be awoken by visiting the room page on the Archipelago website.
This may cause the room's assigned port to change,
requiring you to update your "Mod Savegame Settings" with the new Server URI.
To do this, open your save, go to the pause menu's "Mod Savegame Settings" section,
enter the updated Server URI, then save and reload the game.

## Troubleshooting

- If you are having trouble connecting to the Archipelago Server,
  make sure you have entered the correct server address and port.
  The server port may have changed if the room went to sleep.
  See the [Port Changes section](#port-changes) above for more information.
- If you are having trouble using the Satisfactory Mod Manager, join the [Satisfactory Modding Discord](https://discord.ficsit.app) for support.
- If you encounter a game crash, please report it to us via the [Satisfactory Modding Discord](https://discord.ficsit.app).
  Please include the following information:
  - What you were doing when the crash occurred.
  - If you were a Satisfactory multiplayer host or client, and if you were playing on a dedicated server.
  - Use the Mod Manager to generate a debug zip and attach that file.
   [Satisfactory Modding Documentation FAQ: Generating a debug zip](https://docs.ficsit.app/satisfactory-modding/latest/faq.html#_where_can_i_find_the_games_log_files)
  - Attach your Archipelago config file and spoiler to your report.
