# Meritous Randomizer Setup Guide

## Required Software

Download the game from the [Meritous Gaiden GitHub releases page](https://github.com/FelicitusNeko/meritous-ap/releases)

## Installation Procedures

Simply download the latest version of Meritous Gaiden from the link above, and extract it wherever you like.

- ⚠️ Do not extract Meritous Gaiden to Program Files, as this will cause file access issues.

## Joining a Multiworld Game

1. Modify the `meritous-ap.json` file with your server details, as outlined in the next section.
2. Run `meritous.exe`. If the AP settings file is detected, you will see "AP Enabled" show up in the bottom left of the menu screen.
3. Start a new game. If it is able to successfully connect to the AP server, "Connected" will show up in the bottom left of the game screen for a few seconds.

## AP Settings File

The format of `meritous-ap.json` should be as follows:

```json
{
    "ap-enable": true,
    "server": "archipelago.gg",
    "port": 38281,
    "password": null,
    "slotname": "YourName"
}
```

- `ap-enable`: Enables the game to connect to the Archipelago server. If this is `false` or missing, it will generate a local item randomizer.
- `server`: The server to which to connect. This can be a domain name (such as archipelago.gg) or an IP address (such as 127.0.0.1). If this is missing, the game will assume archipelago.gg.
- `port`: The port number to which to connect. By default, Archipelago will use port 38281 to host, unless the game is hosted on the Archipelago webhost. If this is missing, the game will assume 38281.
- `password`: The password to use for this game, if any. This can be omitted or set to `null` if there is no password.
- `slotname`: The slot name to use for this game. This is required, and must match the name provided on your YAML file.

Eventually, this process will be moved to in-game menus for better ease of use.

## Finishing the Game

Your initial goal is to find all three PSI Keys. Depending on your YAML options, these may be located on pedestals in special rooms in the Atlas Dome, or they may be scattered across other players' worlds. These PSI Keys are then brought to their respective locations in the Dome, where you will be subjected to a boss battle. Once all three bosses are defeated, this unlocks the Cursed Seal, hidden in the farthest-away location from the Entrance. The Compass tiles can help you find your way to these locations.

At minimum, every seed will require you to find the Cursed Seal and bring it back to the Entrance. The goal can then vary based on your `goal` YAML option:

- `return_the_cursed_seal`: You will fight the final boss, but win or lose, a victory will be posted.
- `any_ending`: You must defeat the final boss.
- `true_ending`: You must first explore all 3000 rooms of the Atlas Dome and find the Agate Knife, then fight the final boss' true form.

Once the goal has been completed, you may press F to send a release, sending out all of your world's remaining items to their respective players, and C to send a collect, which gathers up all of your world's items from their shuffled locations in other player's worlds. You may also press S to view your statistics, if you're a fan of numbers.

More in-depth information about the game can be found in the game's help file, accessed by pressing H while playing.

## Commands
While playing the multiworld you can interact with the server using various commands listed in the 
[commands guide](/tutorial/Archipelago/commands/en). As this game does not have an in-game text client at the moment,
You can optionally connect to the multiworld using the text client, which can be found in the 
[main Archipelago installation](https://github.com/ArchipelagoMW/Archipelago/releases) as Archipelago Text Client to
enter these commands.

## Game Troubleshooting

### An error message shows up at the bottom-left

- `Disconnected`: If the game does not reconnect automatically, you may need to save, quit, and reload the game to reconnect. Keep in mind that the game does not auto-save, and it is only possible to save the game at Save Tiles.
- `InvalidSlot`, `InvalidGame`: Make sure the `slotname` in `meritous-ap.json` matches the name provided in your Meritous YAML file.
- `IncompatibleVersion`: Make sure Meritous Gaiden has been updated to the latest version.
- `InvalidPassword`: Make sure the `password` in `meritous-ap.json` matches the password for your game. If there is no password, either set this to `null` (no quotes) or omit/remove it completely.
- `InvalidItemsHandling`: This is a bug and shouldn't happen if you downloaded a precompiled copy of the game. If you downloaded a precompiled copy, please let KewlioMZX know over GitHub or the AP Discord.
