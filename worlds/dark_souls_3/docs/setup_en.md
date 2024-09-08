# Dark Souls III Randomizer Setup Guide

## Required Software

- [Dark Souls III](https://store.steampowered.com/app/374320/DARK_SOULS_III/)
- [Dark Souls III AP Client](https://github.com/Marechal-L/Dark-Souls-III-Archipelago-client/releases)

## Optional Software

- Map tracker not yet updated for 3.0.0

## Setting Up

First, download the client from the link above. It doesn't need to go into any particular directory;
it'll automatically locate _Dark Souls III_ in your Steam installation folder.

Version 3.0.0 of the randomizer _only_ supports the latest version of _Dark Souls III_, 1.15.2. This
is the latest version, so you don't need to do any downpatching! However, if you've already
downpatched your game to use an older version of the randomizer, you'll need to reinstall the latest
version before using this version.

### One-Time Setup

Before you first connect to a multiworld, you need to generate the local data files for your world's
randomized item and (optionally) enemy locations. You only need to do this once per multiworld.

1. Before you first connect to a multiworld, run `randomizer\DS3Randomizer.exe`.

2. Put in your Archipelago room address (usually something like `archipelago.gg:12345`), your player
   name (also known as your "slot name"), and your password if you have one.

3. Click "Load" and wait a minute or two.

### Running and Connecting the Game

To run _Dark Souls III_ in Archipelago mode:

1. Start Steam. **Do not run in offline mode.** The mod will make sure you don't connect to the
   DS3 servers, and running Steam in offline mode will make certain scripted invaders fail to spawn.

2. Run `launchmod_darksouls3.bat`. This will start _Dark Souls III_ as well as a command prompt that
   you can use to interact with the Archipelago server.

3. Type `/connect {SERVER_IP}:{SERVER_PORT} {SLOT_NAME}` into the command prompt, with the
   appropriate values filled in. For example: `/connect archipelago.gg:24242 PlayerName`.

4. Start playing as normal. An "Archipelago connected" message will appear onscreen once you have
   control of your character and the connection is established.

## Frequently Asked Questions

### Where do I get a config file?

The [Player Options](/games/Dark%20Souls%20III/player-options) page on the website allows you to
configure your personal options and export them into a config file.
