# VVVVVV MultiWorld Setup Guide

## Required Software

- VVVVVV
  - [Steam Store Page](https://store.steampowered.com/app/70300/VVVVVV/)
  - [GOG Store Page](https://www.gog.com/game/vvvvvv)
- [V6AP](https://github.com/N00byKing/VVVVVV/releases)

## Installation and Game Start Procedures

1. Install VVVVVV through either Steam or GOG.
2. Go to the page linked for V6AP, and download the latest release.
3. Unpack the zip file where you have VVVVVV installed.

# Joining a MultiWorld Game

To join an Archipelago MultiWorld game, you must set the game's launch options. The two mandatory launch options are:  
  `-v6ap_name slotName`  
  `-v6ap_ip server:port`

If the game you are joining requires a password, you should also add the following to your launch options:  
`-v6ap_passwd secretPassword`

If the game is to be played offline in single-player mode, you should include this launch option:  
`-v6ap_file filePath`

Launch options may be found by right-clicking on the game in Steam and clicking "Properties" in the context menu. From there, open the "General" tab. There is a "Launch Options" setting near the bottom wherein you should enter the above options. Note that all launch options are separated by a space, and if there are spaces in your slot name or password, it should be surrounded with quotes.
If everything worked out, you will see a textbox informing you the connection has been established after the story intro.

# Playing offline

To play offline, first generate a seed on the game's options page.
Create a room and download the `.apv6` file, include the offline single-player launch option described above.

## Installation Troubleshooting

Start the game from the command line to view helpful messages regarding V6AP. These will look something like `V6AP: Message`.

### Game no longer starts after copying the .exe

The most likely cause of a startup failure is invalid launch options. Ensure the launch options are set properly as described above in
**Joining a MultiWorld Game**.

## Game Troubleshooting

### What happens if I lose connection?

If a disconnection occurs, wait a moment to see if the game automatically reconnects itself. If the problem presists, save and restart the game.
