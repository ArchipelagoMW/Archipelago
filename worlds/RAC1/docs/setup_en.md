# Setup Guide for Ratchet & Clank Archipelago

This guide is meant to help you get up and running with Ratchet & Clank in your Archipelago run.

## Requirements

The following are required in order to play Ratchet & Clank in Archipelago

- Installed [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) v0.5.0 or higher.\
   **Make sure to install the Generator if you intend to generate multiworlds.**
- The latest version of the [Ratchet & Clank apworld](https://github.com/Panda291/Archipelago/releases).
- A device to play on:
  - [RPCS3 Emulator](https://rpcs3.net/download).
  - A Homebrew enabled PS3 (easiest is PS3 HEN).
- A Ratchet & Clank PAL ISO (`NPEA00385`)
- The latest version of the [Ratchet & Clank Multiplayer Client](https://github.com/bordplate/rac1-multiplayer/releases).
- (optional) The latest version of the [Ratchet & Clank Multiplayer Server](https://github.com/bordplate/Lawrence/releases).

## AP World Installation

1. Unzip the downloaded Ratchet & Clank apworld zip file
2. Double-click the `rac1.apworld` to install it to your local Archipelago instance

## RPCS3 Settings
- make sure you enable networking:
    - Configuration -> System -> Network (in the top bar) -> Network Status to 'Connected'

## Setting Up a YAML

All players playing Ratchet & Clank must provide the room host with a YAML file containing the settings for their world.
A sample YAML file for Ratchet & Clank is supplied in the Ratchet & Clank apworld download. Refer to the comments in that file for details about what each setting does.

Once complete, provide the room host with your YAML file.

## Generating a Multiworld

If you're generating a multiworld game that includes Ratchet & Clank, you'll need to run it locally since the online
generator does not yet support it. Follow these steps to generate a multiworld:

1. Gather all player's YAMLs. Place these YAMLs into the `Players` folder of your Archipelago installation. If the
   folder does not exist, then it must be created manually. The files here should not be compressed.

2. Modify any local host settings for generation, as desired.

3. Run `ArchipelagoGenerate.exe` (without `.exe` on Linux) or click `Generate` in the launcher. The generation output
   is placed in the `output` folder (usually named something like `AP_XXXXX.zip`). \* Please note that if any player in the game you want to generate plays a game that needs a ROM file to generate,
   you will need the corresponding ROM files.

## Hosting a Room

If you're generating the multiworld, follow the instructions in the previous section.
Once you have the zip file corresponding to your multiworld, follow [these steps](https://archipelago.gg/tutorial/Archipelago/setup/en#hosting-an-archipelago-server) to host a room.
Follow the instructions for hosting on the website from a locally generated game or on a local machine.

## Installing the Ratchet & Clank Multiplayer Mod
To install the Ratchet & Clank Multiplayer Mod, it would be best to follow its [installation guide](https://github.com/bordplate/rac1-multiplayer/blob/main/README.md).
A short TL;DR:
- Have NPEA00385 installed to either your emulator or PS3
- Get the latest release of the [mod](https://github.com/bordplate/rac1-multiplayer/releases)
- Install the mod to your emulator or PS3 (this requires a modded PS3, I will not be going into the details here. Look up PS3 HEN if you don't know where to start)

## Connecting to a Room

- If you host the multiworld on the website, you can use the public multiplayer server to join it.
  - Simply start the Ratchet & Clank Multiplayer Client and select the 'Randomizer' Server from the public servers.
  - Here you can either press Circle to create your own lobby, or join one made by another player who will be playing on the same multiworld slot
  - The host of the lobby must fill in the multiworld room details to connect

- If you host the multiworld on your own machine, you must also host a Ratchet & Clank Multiplayer Server in order to join it.
  - Hosting the server locally is as simple as running "Lawrence.exe" and selecting to host "rando" in the configurator.
  - The IP does not matter if you are not planning to port forward your server
  - Connecting to the local server can be done from the main menu of the Client by pressing Circle to 'Direct connect' to your machine, the IP for localhost is '127.0.0.1'
  - When you make a lobby, make sure to set the address to '127.0.0.1' or 'localhost' for your local multiworld room.

## Connection Troubleshooting

- Use the latest Ratchet & Clank Archipelago release

  - Ratchet & Clank Archipelago: [Releases](https://github.com/Panda291/Archipelago/releases)

- Use the latest RPCS3

  - [RPCS3 Emulator](https://rpcs3.net/download)

- Use the Correct Version of the Game

  - Ensure your ISO of Ratchet & Clank is the supported version:
    - Platform: `PlayStation 3`
    - Serial: `NPEA00385`


- Enable Networking in RPCS3
  - In RPCS3, Under Configuration -> System -> Network (in the top bar) -> Network Status to 'Connected'

- For any problems, do not hesitate to check out the [Official Ratchet & Clank Multiplayer website](Configuration -> System -> Network (in the top bar) -> Network Status to 'Connected').