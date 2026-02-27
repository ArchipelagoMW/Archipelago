# Void Sols Randomizer Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- Void Sols on Steam

## Installation Procedures

1. Download and install [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest).
2. Navigate to Void Sols in your Steam library.
3. Right click on Void Sols and select "Properties..."
4. Select "Game Versions & Betas."
5. Select the "archipelago-stable" branch and update the game.
6. Launch the game and verify you see the Archipelago marker on the title screen.

## Create a Config (.yaml) File

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a config file?

The Player Options page on the website allows you to configure your personal options and export a config file from
them. Player options page: [Void Sols Player Options Page](/games/Void%20Sols/player-options)

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the YAML Validator page. YAML
validator page: [YAML Validation page](/check)

## Joining a MultiWorld Game

1. Launch Void Sols and verify you see the Archipelago logo on the main menu.
2. For new games, press "Play" and then "New Game". Enter the server address, port, your slot name, and optional password. Fields are case-sensitive.
3. For returning games, simply click on your save file to connect and play with saved info. If any information changes, use the three vertical dots context menu on the save to edit the data.

## Hosting a MultiWorld game

The recommended way to host a game is to use our hosting service. The process is relatively simple:

1. Collect config files from your players.
2. Create a zip file containing your players' config files.
3. Upload that zip file to the Generate page.
    - Generate page: [WebHost Seed Generation Page](/generate)
4. Wait a moment while the seed is generated.
5. When the seed is generated, you will be redirected to a "Seed Info" page.
6. Click "Create New Room". This will take you to the server page. Provide the link to this page to your players, so
   they may download their patch files from there (if applicable) or get the connection details.
