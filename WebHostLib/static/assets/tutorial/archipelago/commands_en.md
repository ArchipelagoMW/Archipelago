### Helpful Commands
Commands are split into two types: client commands and server commands. Client commands are commands which are executed by the client and do not affect the Archipelago remote session. Server commands are commands which are executed by the Archipelago server and affect the Archipelago session or otherwise provide feedback from the server.

In clients which have their own commands the commands are typically prepended by a forward slash:`/`. Remote commands are always submitted to the server prepended with an exclamation point: `!`.

#### Local Commands
The following list is a list of client commands which may be available to you through your Archipelago client. You execute these commands in your client window.

- `/connect <address:port>` Connect to the multiworld server.
- `/disconnect` Disconnects you from your current session.
- `/nes` Shows the current status of the NES connection, when applicable.
- `/snes` Shows the current status of the SNES connection, when applicable.
- `/received` Displays all the items you have found or been sent.
- `/missing` Displays all the locations along with their current status (checked/missing).
- Just typing anything will broadcast a message to all players

#### Remote Commands
- `!hint <item name>` Tells you at which location in whose game your Item is. Note you need to have checked some locations
to earn a hint. You can check how many you have by just running `!hint`
- `!forfeit` If you didn't turn on auto-forfeit or you allowed forfeiting prior to goal completion. Remember that "forfeiting" actually means sending out your remaining items in your world.
- `!collect` Grants you all of the remaining checks in your world. Can only be used after your goal is complete or you have forfeited.

#### Host only (on Archipelago.gg or in your server console)
- `/forfeit <Player Name>` Forfeits someone regardless of settings and game completion status
