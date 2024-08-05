# Psychonauts Archipelago Setup Guide

<h2 style="text-transform:none";>Quick Links</h2>

- [Game Info Page](../../../../games/Psychonauts/info/en)
- [Player Options Page](../../../../games/Psychonauts/player-options)
- [PsychoRando Setup Guide](https://docs.google.com/document/d/1b7QOnOLmTSvdC7A1YK3bsSmhtSOsAMs0XF5j-tyE6Zw/edit?usp=sharing)
- [PopTracker Pack](https://github.com/Mysteryem/Psychonauts_AP_PopTracker/releases)

<h2 style="text-transform:none";>Required Software:</h2> <br>

`Psychonauts` for PC

- [Steam](https://store.steampowered.com/app/3830/Psychonauts/)
- [Xbox](https://www.xbox.com/en-US/games/store/Psychonauts/C5HHPG1TXDNG)

[Astralathe Mod Loader](https://gitlab.com/scrunguscrungus/astralathe/-/releases) <br>
[PsychoRando Mod, AP Branch](https://github.com/Akashortstack/PsychoRando/releases) <br>

The [PsychoRando Setup Guide](https://docs.google.com/document/d/1b7QOnOLmTSvdC7A1YK3bsSmhtSOsAMs0XF5j-tyE6Zw/edit?usp=sharing)
provides detailed steps for installing both Astralathe and the PsychoRando Mod.

<h3 style="text-transform:none";>Updating Your Host.yaml</h3>

Find the folder that contains your Psychonauts and Astralathe installation. With the folder open, right-click on the
file path and copy address as text. This will copy the address of your Psychonauts game directory used in host.yaml.
Run ArchipelagoLauncher.exe and open host.yaml from the Archipelago Launcher, find the psychonauts_options and paste
your Psychonauts game directory into the root_directory setting between the quotes. If the pasted root directory
contains single slashes between lines, change all of these to double
slashes. `If you don't, the client may fail to open.`

<h3 style="text-transform:none";>Installing A Seed</h3>

When generating from the website, your player slot will have a Psychonauts.zip seed on the room page. Download the seed,
then extract it to access the RandoSeed.lua file inside. If the game is generated locally, extract the Archipelago
Seed.zip in the output folder (or have the person who generated the seed do this and send you the Psychonauts.zip), then
extract your Psychonauts.zip. Copy RandoSeed.lua, then find your Psychonauts directory where Astralathe and the
PsychoRando mod are installed. Inside ModResource, open the PsychoRando mod folder, find the Scripts folder and paste
RandoSeed.lua inside. Make sure to overwrite the old file.

<h2 style="text-transform:none";>Using the Psychonauts Client</h2>

Once you have launched the game using AstralatheLauncher.exe and are on the title screen, run the
ArchipelagoPsychonautsClient.exe. <br>
When you successfully connect to the server the client will automatically hook into the game to send/receive
checks. <br>
Enter the Yellow Door and choose a bunk to start a new game. Raz will wake up in the Collective Unconscious, and you can
start playing! <br>
Most checks will be sent to you anywhere outside a load or cutscene. Checks are sent one item at a time. <br>
To swap between seeds, just change your RandoSeed.lua in the Scripts folder. The Client uses the seed name from
RandoSeed.lua to keep information between seeds seperated. <br>

