# VVVVVV MultiWorld Setup Guide

## Required Software

- VVVVVV (Bought from the [Steam Store](https://store.steampowered.com/app/70300/VVVVVV/) or [GOG Store](https://www.gog.com/game/vvvvvv) Page, NOT Make and Play Edition!)
- [V6AP](https://github.com/N00byKing/VVVVVV/releases)

## Installation and Game Start Procedures

1. Install VVVVVV through either Steam or GOG
2. Go to the page linked for V6AP, and download the latest release
3. Unpack the zip file where you have VVVVVV installed.

# Joining a MultiWorld Game

To join an Archipelago MultiWorld game, you must set the game's launch options. The two mandatory launch options are:
`-v6ap_name slotName`
`-v6ap_ip server:port`

If the game you are joining requires a password, you should also add the following to your launch options:
`-v6ap_passwd secretPassword`

Launch options may be found by right-clicking on the game in Steam, and clicking "Properties" in the context menu. From there, open the "General" tab. There is a "Launch Options" setting near the bottom wherein you should enter the above options. Note that all launch options are seperated by a space, and if there are spaces in your password, it should be surrounded with quotes

If everything worked out, you will see a textbox informing you the connection has been established after the story intro.

# Playing offline

To play offline, first generate a seed on the game's settings page.
Create a room and download the `.apv6` file, and start the game with the `-v6ap_file FileName` launch argument.

## Installation Troubleshooting

Start the game from the command line to view helpful messages regarding V6AP. These will look something like "V6AP: Message"

### Game no longer starts after copying the .exe

Most likely you forgot to set the launch options. `-v6ap_name YourName` and `-v6ap_ip ServerIP:Port` are required for startup for Multiworlds, and
`-v6ap_file FileName` is required for (offline) singleplayer.
If your Name or Password have spaces in them, surround them in quotes.

## Game Troubleshooting

### What happens if I lose connection?

V6AP tries to reconnect a few times, so be patient.
Should the problem still be there after about a minute or two, just save and restart the game.
