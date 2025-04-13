# Helpful Commands

Commands are split into two types: client commands and server commands. Client commands are commands which are executed
by the client and do not affect the Archipelago remote session. Server commands are commands which are executed by the
Archipelago server and affect the Archipelago session or otherwise provide feedback from the server.

In clients which have their own commands the commands are typically prepended by a forward slash: `/`. 

Server commands are always submitted to the server prepended with an exclamation point: `!`. <br/>

# Server Commands

Server commands may be executed by any client which allows for sending text chat to the Archipelago server. If your
client does not allow for sending chat then you may connect to your game slot with the TextClient which comes with the
Archipelago installation. In order to execute the command you need to merely send a text message with the command,
including the exclamation point.

### General
- `!help` Returns a listing of available commands.
- `!license` Returns the software licensing information.
- `!options` Returns the current server options, including password in plaintext.
- `!players` Returns info about the currently connected and non-connected players.
- `!status` Returns information about the connection status and check completion numbers for all players in the current room. <br /> (Optionally mention a Tag name and get information on who has that Tag. For example: !status DeathLink)


### Utilities
- `!countdown <number of seconds>` Starts a countdown using the given seconds value. Useful for synchronizing starts.
  Defaults to 10 seconds if no argument is provided.
- `!alias <alias>` Sets your alias, which allows you to use commands with the alias rather than your provided name.
  `!alias` on its own will reset the alias to the player's original name.
- `!admin <command>` Executes a command as if you typed it into the server console. Remote administration must be
  enabled.

### Information
- `!remaining` Lists the items remaining in your game, but not where they are or who they go to.
- `!missing` Lists the location checks you are missing from the server's perspective.
- `!checked` Lists all the location checks you've done from the server's perspective.

### Hints
- `!hint` Lists all hints relevant to your world, the number of points you have for hints, and how much a hint costs.
- `!hint <item name>` Tells you the game world and location your item is in, uses points earned from completing locations.
- `!hint_location <location>` Tells you what item is in a specific location, uses points earned from completing locations.

### Collect/Release
- `!collect` Grants you all the remaining items for your world by collecting them from all games. Typically used after 
  goal completion.
- `!release` Releases all items contained in your world to other worlds. Typically, done automatically by the server,
  but can be configured to allow/require manual usage of this command.

### Cheats
- `!getitem <item>` Cheats an item to the currently connected slot, if it is enabled in the server.


## Host only (on Archipelago.gg or in your server console)

### General
- `/help` Returns a list of commands available in the console.
- `/license` Returns the software licensing information.
- `/options` Lists the server's current options, including password in plaintext.
- `/players` List currently connected players.
- `/save` Saves the state of the current multiworld. Note that the server auto-saves on a minute basis.
- `/exit` Shutdown the server

### Utilities
- `/countdown <number of seconds>` Starts a countdown sent to all players via text chat. Defaults to 10 seconds if no
  argument is provided.
- `/option <option name> <option value>` Set a server option. For a list of options, use the `/options` command.
- `/alias <player name> <alias name>` Assign a player an alias, allowing you to reference the player by the alias in commands.
  `!alias <player name>` on its own will reset the alias to the player's original name.


### Collect/Release
- `/collect <player name>` Send out any items remaining in the multiworld belonging to the given player.
- `/release <player name>` Sends out all remaining items in this world regardless of settings and game completion status.
- `/allow_release <player name>` Allows the given player to use the `!release` command.
- `/forbid_release <player name>` Prevents the given player from using the `!release` command.

### Cheats
- `/send <player name> <item name>` Grants the given player the specified item.
- `/send_multiple <amount> <player name> <item name>` Grants the given player the stated amount of the specified item.
- `/send_location <player name> <location name>` Send out the given location for the specified player as if the player checked it
- `/hint <player name> <item or location name>` Send out a hint for the given item or location for the specified player.

<br/> <br/>

# Local Commands

This a list of client commands which may be available to you through your Archipelago client. You can
execute these commands in your client window.

The following commands are available in the clients that use the CommonClient, for example: TextClient, SNIClient, etc.

- `/connect <address:port>` Connect to the multiworld server at the given address.
- `/disconnect` Disconnects you from your current session.
- `/help` Returns a list of available commands.
- `/license` Returns the software licensing information.
- `/received` Displays all the items you have received from all players, including yourself.
- `/missing` Displays all the locations along with their current status (checked/missing).
- `/items` Lists all the item names for the current game.
- `/item_groups` Lists all the item group names for the current game.
- `/locations` Lists all the location names for the current game.
- `/location_groups` Lists all the location group names for the current game.
- `/ready` Sends ready status to the server.
- Typing anything that doesn't start with `/` will broadcast a message to all players.

## SNIClient Only

The following command is only available when using the SNIClient for SNES based games.

- `/snes` Attempts to connect to your SNES device via SNI.
- `/snes_close` Closes the current SNES connection.
- `/slow_mode` Toggles on or off slow mode, which limits the rate in which you receive items.
