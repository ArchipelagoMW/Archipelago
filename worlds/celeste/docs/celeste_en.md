# Celeste Randomizer Setup Guide

## Required Software

- [Everest mod loader](https://everestapi.github.io) installed on your copy of Celeste.
- CelesteArchipelago Everest mod from the [GitHub releases page](https://github.com/doshyw/CelesteArchipelago/releases).
- Celeste APWorld from the [GitHub releases page](https://github.com/doshyw/CelesteArchipelago/releases).
- Archipelago from the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases).

## Configuring your YAML file

### Generating a Celeste game (online)

1. Follow the instructions in the [Archipelago Setup Guide](tutorial/Archipelago/setup/en#on-the-website) to generate a
`.yaml` file using the [Celeste Player Settings Page](/games/celeste/player-settings).
1. If playing multiplayer, follow the instructions in the [Archipelago Setup Guide](tutorial/Archipelago/setup/en#generating-a-multiplayer-game) to complete the generation and hosting steps.

### Generating a Celeste game (offline)

1. Download and install [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases).
1. Open your Archipelago installation in a file explorer (defaults to `C:\ProgramData\Archipelago` on Windows).
1. Download `celeste.apworld` from the [GitHub releases page](https://github.com/doshyw/CelesteArchipelago/releases)
and add it to the `lib\worlds` folder under your Archipelago installation.
1. Follow the instructions in the [Archipelago Setup Guide](tutorial/Archipelago/setup/en#on-your-local-installation) to
generate and host your game.


## Setting up your Celeste client

### Installation

1. Follow the steps in the [Installing Everest guide](https://everestapi.github.io/#installing-everest) to download 
Olympus and use it to install the Everest mod loader for your Celeste client.
1. Download the `CelesteArchipelago.zip` Everest mod from the 
[GitHub releases page](https://github.com/doshyw/CelesteArchipelago/releases) and place it into the `Mods` directory 
under your Celeste installation.
1. Launch Olympus, click "Manage Installed Mods", and ensure that `CelesteArchipelago` is the only mod enabled.


### Connect to the MultiServer

1. Launch Celeste (either by normal means or by clicking "Everest" on the Olympus main menu).
1. Press the "Archipelago" button on the main menu.
1. Enter in your connection details
    - Name: enter your slot name (e.g., `Madeline`).
    - Server: enter the IP/HTTP address (e.g., `archipelago.gg`).
    - Port: enter the port you wish to connect on (e.g., `38281`).
    - Password: enter the password set for the room (leave this blank if no password has been set).
1. Press "Connect to Session" to connect to the MultiServer! Happy playing!


### Using Archipelago console commands

At this stage, the Everest mod does not support sending commands to the Archipelago server. If you wish to do so, you 
will need to open `ArchipelagoTextClient.exe` under your local 
[Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) installation and separately connect to the 
MultiServer to execute commands.
