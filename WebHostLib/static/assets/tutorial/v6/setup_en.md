# VVVVVV MultiWorld Setup Guide

## Required Software

- VVVVVV (Bought from the [Steam Store](https://store.steampowered.com/app/70300/VVVVVV/) or [GOG Store](https://www.gog.com/game/vvvvvv) Page, NOT Make and Play Edition!)
- [V6MW patched VVVVVV.exe](https://github.com/N00byKing/VVVVVV/actions/workflows/ci.yml?query=branch%3Aarchipelago)

## Installation and Game Start Procedures

1. Install VVVVVV through either Steam or GOG
2. Go to the page linked for V6MW, and press on the topmost entry
3. Scroll down, and download the zip file corresponding to your platform (NOTE: Linux currently does not build automatically. Linux users will have to compile manually for now)
4. Replace VVVVVV.exe of the original game with the one contained in the zip file. It might be worth it to copy it away instead of deleting to remove the Mod later.

# Joining a MultiWorld Game

To join, set the following launch options: `-v6mw_name "YourName" -v6mw_ip "ServerIP"`.
Optionally, add `-v6mw_passwd "YourPassword"` if the room you are using requires a password. All parameters without quotation marks.
The Name in this case is the one specified in your generated .yaml file.
In case you are using the Archipelago Website, the IP should be `archipelago.gg`.

If everything worked out, you will see a textbox informing you the connection has been established after the story intro.

## Installation Troubleshooting

Start the game from the command line to view helpful messages regarding V6MW. These will look something like "V6MW: Message"

### Game no longer starts after copying the .exe

Most likely you forgot to set the launch options. `-v6mw_name "YourName"` and `-v6mw_ip "ServerIP"` are required for startup.

## Game Troubleshooting

### What happens if I lose connection?

V6MW tries to reconnect a few times, so be patient.
Should the problem still be there after about a minute or two, just save and restart the game.
