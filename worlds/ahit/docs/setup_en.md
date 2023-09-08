# Setup Guide for A Hat in Time in Archipelago

## Required Software
- [Steam release of A Hat in Time](https://store.steampowered.com/app/253230/A_Hat_in_Time/)

- [Archipelago Workshop Mod for A Hat in Time](https://steamcommunity.com/sharedfiles/filedetails/?id=3026842601)


## Instructions

1. Have Steam running. Open the Steam console with [this link.](steam://open/console)

2. In the Steam console, enter the following command: 
`download_depot 253230 253232 7770543545116491859`. Wait for the console to say the download is finished.

3. Once the download finishes, go to `steamapps/content/app_253230` in Steam's program folder.

4. There should be a folder named `depot_253232`. Rename it to HatinTime_AP and move it to your `steamapps/common` folder.

5. In the HatinTime_AP folder, navigate to `Binaries/Win64` and create a new file: `steam_appid.txt`. In this new text file, input the number **253230** on the first line.

6. Create a shortcut of `HatinTimeGame.exe` from that folder and move it to wherever you'd like. You will use this shortcut to open the Archipelago-compatible version of A Hat in Time.

7. Start up the game using your new shortcut. To confirm if you are on the correct version, go to Settings -> Game Settings. If you don't see an option labelled ***Live Game Events*** you should be running the correct version of the game. In Game Settings, make sure ***Enable Developer Console*** is checked.



## Connecting to the Archipelago server

When you create a new save file, you should be prompted to enter your slot name, password, and Archipelago server address:port after loading into the Spaceship. Once that's done, the game will automatically connect to the multiserver using the info you entered whenever that save file is loaded. If you must change the IP or port for the save file, use the `ap_set_connection_info` console command.


## Console Commands

Commands will not work on the title screen, you must be in-game to use them. To use console commands, make sure ***Enable Developer Console*** is checked in Game Settings and press the tilde key or TAB while in-game.

`ap_say <message>` - Send a chat message to the server. Supports commands, such as !hint or !release.

`ap_deathlink` - Toggle Death Link.

`ap_set_connection_info <ip> <port>` - Set the connection info for the save file. The IP address MUST BE IN QUOTES!

`ap_show_connection_info` - Show the connection info for the save file.