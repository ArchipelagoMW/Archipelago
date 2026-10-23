# Taylor Swift Discography Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest)
- [Archipelago Music Client](https://github.com/benny-dreamly/archipelagomusicclient/releases/latest)
  - Requires **Java 25** or newer (bundled with the release download)
  - You need your music files **locally on your computer** (ripped from CD or purchased from iTunes or similar). Streaming services like Spotify and Apple Music will not work.

## Optional Software

- [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases?q=Tracker)
  - Tracks which locations are currently in logic

## Generating a Game

1. Open the Archipelago Launcher
2. Click **Generate Template Options** to create a template YAML for this game
3. Edit the YAML to your liking (or use the [player options page](/games/Taylor%20Swift%20Discography/player-options) on the website)
4. Generate the game

If you are hosting, click **Create Room** after generation to get a link you can share with other players.

## Connecting to a Game

### From a WebHost Room

If your room is hosted on [archipelago.gg](https://archipelago.gg), click your name in the player list. This opens the Archipelago Launcher and prompts you to choose a client. Select the Text Client and note the server address and slot name.

### Using the Music Client

Before starting with these steps, head over to the configuration section to find out where to put the configuration files you've downloaded along with this APWorld.

1. Open the Archipelago Music Client (standalone application)
2. Enter all the details into the client application's window, including the game name, which in this case is `Taylor Swift Discography`
3. Hit **Connect** and enjoy.

## Configuration

The Music Client uses configuration files stored in your operating system's application data directory. The correct configuration files for use with the client are included in the APWorld download, however the albumFolders.json is not populated with file paths as those tend to contain user directories in them. See the documentation on how to create that file. The configuration files are:

| File                               | Purpose                                                                  |
|------------------------------------|--------------------------------------------------------------------------|
| `albumFolders.json`                | Maps album names to folder paths where your local music files are stored |
| `albumOrder.json`                  | Controls the display order of albums in the music library                |
| `locations.json`                   | Defines all available songs and their relationships                      |
| `slot_data.json`                   | Describes what is unlocked or available in randomizer mode               |
| `album_metadata.json` *(optional)* | Provides metadata such as album type and year                            |

See the [Music Client documentation](https://github.com/benny-dreamly/archipelagomusicclient/tree/main/docs) for detailed configuration instructions and platform-specific file paths.

## Switching Rooms

The Music Client can switch rooms without restarting. Click **Disconnect**, then connect to a different slot or room.
