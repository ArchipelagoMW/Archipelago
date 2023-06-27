### Helpful Commands

Commands are split into two types: client commands and server commands. Client commands are commands which are executed
by the client and do not affect the Archipelago remote session. Server commands are commands which are executed by the
Archipelago server and affect the Archipelago session or otherwise provide feedback from the server.

In clients which have their own commands the commands are typically prepended by a forward slash:`/`. Remote commands
are always submitted to the server prepended with an exclamation point: `!`.

#### Local Commands

The following list is a list of client commands which may be available to you through your Archipelago client. You
execute these commands in your client window.

The following commands are available in these clients: SNIClient, FactorioClient, FF1Client.

- `/connect <address:port>` Connect to the multiworld server.
- `/disconnect` Disconnects you from your current session.
- `/received` Displays all the items you have found or been sent.
- `/missing` Displays all the locations along with their current status (checked/missing).
- `/items` Lists all the item names for the current game.
- `/locations` Lists all the location names for the current game.
- `/ready` Sends ready status to the server.
- `/help` Returns a list of available commands.
- `/license` Returns the software licensing information.
- Just typing anything will broadcast a message to all players

##### FF1Client Only

The following command is only available when using the FF1Client for the Final Fantasy Randomizer.

- `/nes` Shows the current status of the NES connection.

##### SNIClient Only

The following command is only available when using the SNIClient for SNES based games.

- `/snes` Attempts to connect to your SNES device via SNI.
- `/snes_close` Closes the current SNES connection.
- `/slow_mode` Toggles on or off slow mode, which limits the rate in which you receive items.

##### FactorioClient Only

The following command is only available when using the FactorioClient to play Factorio with Archipelago.

- `/factorio <command text>` Sends the command argument to the Factorio server as a command.

#### Remote Commands

Remote commands may be executed by any client which allows for sending text chat to the Archipelago server. If your
client does not allow for sending chat then you may connect to your game slot with the TextClient which comes with the
Archipelago installation. In order to execute the command you need to merely send a text message with the command,
including the exclamation point.

- `!help` Returns a listing of available remote commands.
- `!license` Returns the software licensing information.
- `!countdown <countdown in seconds>` Starts a countdown using the given seconds value. Useful for synchronizing starts.
  Defaults to 10 seconds if no argument is provided.
- `!options` Returns the current server options, including password in plaintext.
- `!admin <command>` Executes a command as if you typed it into the server console. Remote administration must be
  enabled.
- `!players` Returns info about the currently connected and non-connected players.
- `!status` Returns information about your team. (Currently all players as teams are unimplemented.)
- `!remaining` Lists the items remaining in your game, but not where they are or who they go to.
- `!missing` Lists the location checks you are missing from the server's perspective.
- `!checked` Lists all the location checks you've done from the server's perspective.
- `!alias <alias>` Sets your alias.
- `!getitem <item>` Cheats an item, if it is enabled in the server.
- `!hint_location <location>` Hints for a location specifically. Useful in games where item names may match location
  names such as Factorio.
- `!hint <item name>` Tells you at which location in whose game your Item is. Note you need to have checked some
  locations to earn a hint. You can check how many you have by just running `!hint`
- `!release` If you didn't turn on auto-release or if you allowed releasing prior to goal completion. Remember that "
  releasing" actually means sending out your remaining items in your world.
- `!collect` Grants you all the remaining checks in your world. Typically used after goal completion.

#### Host only (on Archipelago.gg or in your server console)

- `/help` Returns a list of commands available in the console.
- `/license` Returns the software licensing information.
- `/countdown <seconds>` Starts a countdown which is sent to all players via text chat. Defaults to 10 seconds if no
  argument is provided.
- `/options` Lists the server's current options, including password in plaintext.
- `/save` Saves the state of the current multiworld. Note that the server autosaves on a minute basis.
- `/players` List currently connected players.
- `/exit` Shutdown the server
- `/alias <player name> <alias name>` Assign a player an alias.
- `/collect <player name>` Send out any items remaining in the multiworld belonging to the given player.
- `/release <player name>` Releases someone regardless of settings and game completion status
- `/allow_release <player name>` Allows the given player to use the `!release` command.
- `/forbid_release <player name>` Bars the given player from using the `!release` command.
- `/send <player name> <item name>` Grants the given player the specified item.
- `/send_multiple <amount> <player name> <item name>` Grants the given player the stated amount of the specified item.
- `/send_location <player name> <location name>` Send out the given location for the specified player as if the player checked it
- `/hint <player name> <item or location name>` Send out a hint for the given item or location for the specified player.
- `/option <option name> <option value>` Set a server option. For a list of options, use the `/options` command.
