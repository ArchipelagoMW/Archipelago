# VVVVVV MultiWorld Setup Guide

## Required Software

- VVVVVV (Bought from the [Steam Store](https://store.steampowered.com/app/70300/VVVVVV/) or [GOG Store](https://www.gog.com/game/vvvvvv) Page, NOT Make and Play Edition!)
- [V6AP](https://github.com/N00byKing/VVVVVV/releases)

## Installation and Game Start Procedures

1. Install VVVVVV through either Steam or GOG
2. Go to the page linked for V6AP, and download the latest release
3. Unpack the zip file where you have VVVVVV installed.

# Joining a MultiWorld Game

To join, set the following launch options: `-v6ap_name YourName -v6ap_ip ServerIP:Port`. Launch options on steam can be found be right clicking VVVVVV and clicking properties 
Optionally, add `-v6ap_passwd "YourPassword"` if the room you are using requires a password. All parameters without quotation marks.
The Name in this case is the one specified in your generated .yaml file.
In case you are using the Archipelago Website, the IP should be `archipelago.gg`.

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
