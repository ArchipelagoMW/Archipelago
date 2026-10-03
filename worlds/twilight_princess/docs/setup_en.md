# Twilight Princess Setup Guide

This guide explains how to play Twilight Princess with the Archipelago
Twilight Princess world.

Twilight Princess is included directly in Archipelago, so no separate APWorld
installation is required.

## Requirements

You will need:

- A current Archipelago installation.
- Dolphin Emulator.
- A legally obtained North American GameCube copy of The Legend of Zelda:
  Twilight Princess.
- The Twilight Princess files required by the randomizer/client.

For Linux, Dolphin can be installed through your distribution or from the
[Dolphin Emulator website](https://dolphin-emu.org/download/).

## Archipelago setup

Because Twilight Princess is included in Archipelago, the world is available
directly from the Archipelago Launcher and Generator.

You do not need to:

- install a separate `.apworld` file;
- download a separate Twilight Princess APWorld release.

## Twilight Princess files

The Twilight Princess client requires the game files used by the randomizer
and its loader.

The exact files and their installation procedure depend on the supported game
region and the current Twilight Princess randomizer implementation.

Do not use files from an unrelated or older standalone-randomizer
installation unless they are explicitly compatible with the current
Archipelago Twilight Princess implementation.

If a future official distribution provides these files, follow its included
README and use the files corresponding to your game region.

## Setting up a YAML

Each player using Twilight Princess needs a YAML configuration containing
their world options.

The Twilight Princess options are available through the normal Archipelago
player configuration workflow.

Once the YAML is configured, place it in the Archipelago `Players` directory
when generating locally.

## Generating a multiworld

To generate a multiworld locally:

1. Put the YAML files for all players in the `Players` directory.
2. Run the Archipelago Generator, either from the launcher or from the
   command line.
3. The generated multiworld will be written to the `output` directory.
4. Use the resulting archive to host the Archipelago room.

Twilight Princess does not require a ROM file merely to generate its
Archipelago world.

## Connecting Twilight Princess

1. Open Dolphin and launch Twilight Princess.
2. Start the Twilight Princess loader/randomizer environment required by the
   current Archipelago implementation.
3. Start a save file and wait until you have control of Link.
4. Launch the Twilight Princess client from the Archipelago Launcher.
5. The client will connect to Dolphin automatically when the required game
   state is available.
6. Connect the client to the Archipelago server using the room address and
   port.
7. If necessary, use the client's `/name` command to set Link's save-file name
   to the Archipelago slot name.

The client may refuse to connect while the game is still in menus or before
the randomizer has finished loading. This is expected.

## PopTracker

A community PopTracker pack is available from the
[TPRAP PopTracker project](https://github.com/Kizugaya/TPRAP_poptracker).

You will also need [PopTracker](https://github.com/black-sliver/PopTracker)
itself.

The PopTracker pack is a separate project from the Archipelago world.

## Troubleshooting

### The Twilight Princess client is not visible

Make sure you are running the same Archipelago installation in which the
Twilight Princess world is installed.

Because Twilight Princess is part of Archipelago, do not place an additional
Twilight Princess world included with Archipelago.

### The client cannot connect to Dolphin

Check that:

- Dolphin is running Twilight Princess.
- The required Twilight Princess loader/randomizer environment is active.
- You have reached an actual save file and have control of Link.
- Dolphin's emulated-memory-size override is disabled.
- No Dolphin cheats or codes are modifying the game memory.

### The client reports a seed/client version mismatch

The client and generated world should use compatible versions.

If the generated seed was created with a different Twilight Princess world
version, regenerate the seed with the same Archipelago source/version used by
the client.

### Dolphin reports memory-reading errors

This generally indicates that the Dolphin connection was lost or that the
game is not currently in a supported state.

Make sure the game is running and retry the connection.

### The game does not load the Twilight Princess randomizer environment

Check that the loader/randomizer files are installed in the correct Dolphin
save location and that they correspond to the game region being used.

Remove incompatible files from older standalone-randomizer installations if
they interfere with the current setup.

## Frequently Asked Questions

### Do I need to install the Twilight Princess APWorld?

No. Twilight Princess is included directly in Archipelago.


### Can I generate Twilight Princess together with other Archipelago worlds?

Yes. Twilight Princess is an Archipelago world and can participate in normal
multiworld generation.

### What does the client do?

The Twilight Princess client communicates between the Archipelago server and
the running game in Dolphin. It sends location checks and delivers received
items to the game.

### Why do received items appear as green rupees?

The current Twilight Princess game-side implementation uses the in-game
green-rupee representation for received Archipelago items.

### What happens if I receive several items?

Received items are queued by the client and delivered to the game as Link can
accept them.

### Do the in-game hints represent the actual Archipelago item?

No. The current game-side representation does not expose the Archipelago item
name through the normal in-game hint system.

### Why does the client wait before connecting?

The client needs the game to reach a state where it can safely identify the
active player/save and communicate with the randomizer.

## Reporting issues

When reporting a Twilight Princess issue, include:

- Archipelago version or source revision;
- game region;
- Dolphin version;
- whether the issue occurs before or after connecting to the server;
- the client log/error message;
- the steps required to reproduce the issue.

Avoid sharing copyrighted game files or save files containing them.
