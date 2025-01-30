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

This guide will walk you through installing the Satisfactory Archipelago mod via the Mod Manager
and entering Archipelago server connection details in the mod configuration options.
The server will send the required data to the game client and create the content required by the seed at runtime.

## Create a Config (.yaml) File

### What is a config file and why do I need one?

Your config file contains a set of configuration options
which provide the generator with information about how it should generate your game.
Each player of a multiworld will provide their own config file.
This setup allows each player to enjoy an experience customized for their taste,
and different players in the same multiworld can all have different options.

### Where do I get a config file?

The Player Settings page on the website
allows you to configure your personal settings and export a config file from them.
Satisfactory player settings page: [Satisfactory Settings Page](/games/Satisfactory/player-settings)

> ⚠ Pre-Release Note: The above link does not work because it would go to the live Archipelago site.
> Manually construct a yaml yourself from the one pinned in the Discord:
> <https://discord.com/channels/731205301247803413/1018853131859267656>

### Verifying Your Config File

If you would like to validate your config file to make sure it works,
you may do so on the YAML Validator page.
YAML Validator page: [Yaml Validation Page](/mysterycheck)

> ⚠ Pre-Release Note: The above link does not work because it would go to the live Archipelago site.
> Manually construct a yaml yourself from the one pinned in the Discord:
> <https://discord.com/channels/731205301247803413/1018853131859267656>

### Starting Inventory

The Player Settings page provides a few options for controlling what materials you start with
and when certain key technologies are unlocked.

Advanced users can use Plando, Weighted Options, and manual yaml editing to further configure the starting inventory.
If you don't wish to use these techniques, consider using a Satisfactory's Advanced Game Settings to spawn the items you desire.

### Advanced Configuration

Advanced users can utilize the
[Weighted Options Page](/weighted-options)
and [Plando](/tutorial/Archipelago/plando)
to futher customize their experience.

> ⚠ Pre-Release Note: The above links do not work because it would go to the live Archipelago site.
> See these links instead:
>
> - <https://archipelago.gg/tutorial/Archipelago/advanced_settings/en>
> - <https://archipelago.gg/tutorial/Archipelago/plando/en>

## Prepare to Host Your Own Satisfactory Game

### Defining Some Terms

In Archipelago, multiple Satisfactory worlds may be played simultaneously.
Each of these worlds must be hosted by a Satisfactory Server which is connected to the Archipelago Server via the Archipelago mod.

This guide uses the following terms to refer to the software:

- **Archipelago Server** - The central Archipelago server, which connects all games to each other.
- **Satisfactory Server** - The Satisfactory instance (game client or dedicated server) which will be used to host the game.
  It must be supplied with the Archipelago Server connection details.
  Any number of Satisfactory Clients may connect to this server.
- **Satisfactory Client** - The Satisfactory instance (game client) with which additional players can use to connect to the same Satisfactory world.
  They must also have the Archipelago mod installed, but require no configuration.

It is important to note that the Satisfactory Archipelago mod
is not yet compatible with Linux dedicated servers - only Windows dedicated servers are supported.

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

> ⚠ Pre-Release Note: The above link does not work because it would go to the live Archipelago site.
> Use this link instead:
> <https://github.com/Jarno458/Archipelago/blob/Satisfactory/worlds/satisfactory/docs/en_Satisfactory.md#additional-mods>

### Entering Connection Details

After you have installed the mods, launch the game via the Mod Manager or via your preferred method.
Once the game has launched, click on the 'Mods' button on the main menu and open the Archipelago entry.

Next, enter the connection details in the relevant fields.
You can hover over the fields in the menu for more information and example values.

- **URI**: Archipelago Server URI and port, for example, `archipelago.gg:49236`
- **Username**: The name you entered as your Player Name when you created your config file. It's also listed in the Name column of your room page.
- **Password**: The password for your slot, blank if you did not assign one.
- **Archipelago Enabled**: Make sure this is checked, otherwise no server connection will be attempted.
- **Debug Mode**: Don't enable it unless the developers ask you to when reporting problems.
- **Force override settings in save**: Leave false for now. It is useful when the server changed ports. Read its tooltip for more info.

Note that the Satisfactory Server/Client does _not_ need a copy of your Archipelago config file.
The mod communicates with the Archipelago Server, which already has your config file,
to generate the required content at runtime.

### Creating a New World

Once you have entered connection details, create a new world using the game's New Game menu.
Make sure to check 'Skip Intro' if you don't want to deal with the game's tutorial sequence.
Consider enabling Advanced Game Settings to allow dealing with bugs that may arise.
Within the Advanced Game Settings menus,
you may wish to switch the "Keep Inventory" setting to "Keep Everything" to avoid dropping items on death,
although this will never lock you out of progression.

### Verifying Connection Success

Once connected to the AP server,
you can issue the `/help` command in the game's chat to list available commands, such as `/hint`.
For more information about the commands you can use, see the [Commands Guide](/tutorial/Archipelago/commands/en).
Note that Archipelago commands are not prefixed with `!` inside of Satisfactory.
You may wish to use the Text Client to run commands since Satisfactory's in game chat is not very user friendly.

> ⚠ Pre-Release Note: The above link does not work because it would go to the live Archipelago site.
> Use this link instead:
> <https://archipelago.gg/tutorial/Archipelago/commands/en>

Check out the HUB to get started!

> ⚠ IMPORTANT: Check your HUB immediately upon joining to ensure your save file has been set up correctly!
> Make sure that you see multiple HUB milestones from Archipelago in Tier 1 and Tier 2.
> If you don't, create a new Satisfactory save file with the same connection settings and it should resolve itself.
> See more information about this bug on the [GitHub issue tracker](https://github.com/Jarno458/SatisfactoryArchipelagoMod/issues/120).

<!-- ## Other Settings

TODO implement filter_item_sends and bridge_chat_out mentioned in the Factorio guide? -->

## Troubleshooting

- If you are having trouble connecting to the Archipelago server,
  make sure you have entered the correct server address and port.
  The server port may have changed if the room went to sleep.
  If you need to enter a new port,
  use the "Force override settings in save" option on the mod options menu before loading into a save.
- If you are having trouble using the Satisfactory Mod Manager, join the [Satisfactory Modding Discord](https://discord.ficsit.app) for support.
- If you encounter a game crash, please report it to us via the [Satisfactory Modding Discord](https://discord.ficsit.app).
  Please include the following information:
  - What you were doing when the crash occurred.
  - If you were a Satisfactory multiplayer host or client, and if you were playing on a dedicated server.
  - Use the Mod Manager to generate a debug zip and attach that file.
   [Satisfactory Modding Documentation FAQ: Generating a debug zip](https://docs.ficsit.app/satisfactory-modding/latest/faq.html#_where_can_i_find_the_games_log_files)
  - Attach your Archipelago config file and spoiler to your report.

## Additional Resources

- Satisfactory Wiki: [Satisfactory Official Wiki](https://satisfactory.wiki.gg/wiki/)
- Satisfactory Modding FAQ page: [Satisfactory Modding Documentation FAQ](https://docs.ficsit.app/satisfactory-modding/latest/faq.html)
- Satisfactory Archipelago Item names (for hints/starting inventory/etc.) can be found [on the mod's github](https://github.com/Jarno458/Archipelago/blob/Satisfactory/worlds/satisfactory/Items.py)
