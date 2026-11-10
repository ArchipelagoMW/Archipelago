# Undertale Randomizer Setup Guide

### Required Software

- Undertale from the [Steam page](https://store.steampowered.com/app/391540)
- Archipelago from the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)

### PLEASE READ!

Please read the Game Info page in its entirety before asking questions! Most importantly, there is a list of 
gameplay differences you are likely to need to know.
[Undertale Game Info Page](/games/Undertale/info/en)

### First time setup

Start the Undertale client from your Archipelago folder and input `/auto_patch <Your Undertale Install Directory>` at the bottom. 

This directory is usually located at `C:\Program Files\Steam\steamapps\Undertale`, but it can be different depending on 
your installation. You can easily find the directory by opening the Undertale directory through Steam by right-clicking 
Undertale in your library and selecting `Manage -> Browse local files`. Then, on Windows you can see the directory that 
you need at the top of the window that opens.

After using the `/auto_patch` command, **Archipelago will make an Undertale folder within the Archipelago install location.** 
That folder contains the version of Undertale you will use for Archipelago. (If you update Archipelago, 
you will need to redo this set-up.)

**Linux Users**: The Linux installation is mostly similar, however, Undertale will be installed on Steam as the Linux 
variant. Since this randomizer only supports the Windows version, we must fix this, by right-click the game in Steam, 
going to `Properties -> Compatibility`, and checking `Force the use of a specific Steam Play compatibility tool`. This
downloads the Windows version of Undertale to use instead of the Linux version. If the play button is greyed out in 
Steam, be sure to go to `Settings -> Compatibility` and toggle `Enable Steam Play for all other titles`.

### Connect to the MultiServer

Make sure both Undertale **from the Archipelago folder** and its client are running. (Undertale will ask for a save slot
to play on. Archipelago Undertale does not overwrite vanilla saves, but you may want to back up your save as a precaution.)

In the top text box of the client, type the `IP Address` (or `Hostname`) and `Port` separated with a `:` symbol. 
(Ex. `archipelago.gg:38281`)

The client will then ask for the slot name, input your slot name chosen during YAML creation in the text box at the 
bottom of the client.

Windows users are now ready to play!

Linux users will need the additional section down below.

### Linux Users

When you start the client, it is likely that the save data path is incorrect, and how the game
is played depends on where the save data folder is located.

*Linux through Steam (via Proton)*: This assumes the game is in a Steam Library folder.  Right-click Undertale, go to `Manage -> 
Browse Local Files`. Go up the directories to the `steamapps` folder, open `compatdata/391540` (391540 is the "magic number" for
Undertale in Steam).  Save data from here is at `/pfx/drive_c/users/steamuser/AppData/Local/UNDERTALEAP`.

*Linux through WINE directly*: This depends on the prefix used.  If it is default, then the save data is located at
`/home/USERNAME/.wine/drive_c/users/USERNAME/AppData/Local/UNDERTALEAP`.

Once the save data folder is located, run the `/savepath` command to redirect the client to the correct save data folder
before connecting.

### Play the game

When the console tells you that you have joined the room, you're all set. Congratulations on successfully joining a
multi-world game!

### The game opens in widescreen and doesn't go past the title?

The vanilla installation of Undertale was modified before patching.
Steam allows you to "Verify integrity of game files" using a button in the game properties, 
which will fix all file issues.

### The "auto_patch" command fails with a "Permission Denied" error?

The vanilla installation of Undertale was modified before patching.
Steam will not be able to fix this one properly, but it is very simple to do so.
Make sure there are no folders within the Steam installation of Undertale, and if there are any, delete them.

### Where do I get a YAML file?

You can customize your options by visiting the [Undertale Player Options Page](/games/Undertale/player-options)
