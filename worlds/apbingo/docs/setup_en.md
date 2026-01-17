# APBingo! Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases).

- Ap World from [Bingo](https://github.com/Cynichill/APBingo/releases).
    
## Installation Procedures

### Windows Setup

1. Requires other games to generate, cannot generate a solo bingo game. 
2. Generates 25 items, one for each square and sends them out to the multiworld.
3. Each bingo sends out 2 location checks (and an extra single location for getting ALL bingos) (25 total)
4. APworld has a client that opens up the board (seen in screenshot above) that autotracks which squares have been found, client also sends out checks if a bingo has been achieved.

5. Goal is to get X amount of bingos (set in the YAML)

## Create a Config (.yaml) File

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a config file?

The Player Settings page on the website allows you to configure your personal settings and export a config file from
them. Player settings page: [Final Fantasy V Career Day Player Settings Page](/games/Final%20Fantasy%20V%20Career%20Day/player-settings)

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the YAML Validator page. YAML
validator page: [YAML Validation page](/check)

## Generating a Single-Player Game

1. Requires other games to generate, cannot generate a solo bingo game. 

## Joining a MultiWorld Game

### Obtain your patch file and create your ROM

When you join a multiworld game, you will be asked to provide your config file to whoever is hosting. Once that is done,
the host will provide you with either a link.

### Connect to the Archipelago Server

Open the Archipelago Launcher. Find the bingo client in the list and click to launch. This should launch the client as well as the bingo board to play.

### Play the game

?

## Hosting a MultiWorld game

The recommended way to host a game is to use our hosting service. The process is relatively simple:

1. Collect config files from your players.
2. Create a zip file containing your players' config files.
3. Upload that zip file to the Generate page above.
    - Generate page: [WebHost Seed Generation Page](/generate)
4. Wait a moment while the seed is generated.
5. When the seed is generated, you will be redirected to a "Seed Info" page.
6. Click "Create New Room". This will take you to the server page. Provide the link to this page to your players, so
   they may download their patch files from there.
7. Note that a link to a MultiWorld Tracker is at the top of the room page. The tracker shows the progress of all
   players in the game. Any observers may also be given the link to this page.
8. Once all players have joined, you may begin playing.
