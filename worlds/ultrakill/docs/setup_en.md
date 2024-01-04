# ULTRAKILL Multiworld Setup Guide

1. Download and install the Archipelago mod with r2modman, or manually by extracting the contents of the zip file into the `UMM Mods` folder. If you decide to install manually, you will also need to install [PluginConfigurator](https://thunderstore.io/c/ultrakill/p/EternalsTeam/PluginConfigurator/).

*Note that only one player in the multiworld will need to complete steps 2-5.*

2. Download and install [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases). Then, download `ultrakill.apworld` from the mod's [releases page](https://github.com/TRPG0/ArchipelagoULTRAKILL/releases) and add it to your `worlds` folder. (Default path: `C:\ProgramData\Archipelago\lib\worlds`)

3. Set up all `.yaml` files for each player in the multiworld, then add them to the `Players` folder. A template can be downloaded for ULTRAKILL from the mod's [releases page.](https://github.com/TRPG0/ArchipelagoULTRAKILL/releases)

4. Run `ArchipelagoGenerate.exe` to generate a game, which will appear in the `output` folder.

5. Host a game, either manually, or by [uploading](https://archipelago.gg/uploads) it to the Archipelago website.

6. Enable Archipelago in game, then restart ULTRAKILL.

7. To connect to the server, first select a new save file. Then open the options menu, click the PLUGIN CONFIG button, click Configure next to Archipelago, and open the PLAYER SETTINGS menu. Enter your name, the server's address in the form of `address:port`, and a password if necessary, then click the Connect button.

There are some additional commands that can be used by pressing `F8` to open the console:

- `connect [address:port] [player] [password]` - Connect to an Archipelago server.
- `disconnect`: Disconnect from an Archipelago server.
- `say [message]`: Send messages or commands to the server.