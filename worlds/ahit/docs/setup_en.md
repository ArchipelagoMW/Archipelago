# Setup Guide for A Hat in Time in Archipelago

## Required Software
- [Steam release of A Hat in Time](https://store.steampowered.com/app/253230/A_Hat_in_Time/)

- [Archipelago Workshop Mod for A Hat in Time](https://steamcommunity.com/sharedfiles/filedetails/?id=3026842601)


## Optional Software
- [A Hat in Time Archipelago Map Tracker](https://github.com/Mysteryem/ahit-poptracker/releases), for use with [PopTracker](https://github.com/black-sliver/PopTracker/releases)


## Instructions

1. Have Steam running. Open the Steam console with this link: [steam://open/console](steam://open/console)   
This may not work for some browsers. If that's the case, and you're on Windows, open the Run dialog using Win+R,
paste the link into the box, and hit Enter.


2. In the Steam console, enter the following command: 
`download_depot 253230 253232 7770543545116491859`. ***Wait for the console to say the download is finished!***
This can take a while to finish (30+ minutes) depending on your connection speed, so please be patient. Additionally,
**try to prevent your connection from being interrupted or slowed while Steam is downloading the depot,**
or else the download may potentially become corrupted (see first FAQ issue below).


3. Once the download finishes, go to `steamapps/content/app_253230` in Steam's program folder.


4. There should be a folder named `depot_253232`. Rename it to HatinTime_AP and move it to your `steamapps/common` folder.


5. In the HatinTime_AP folder, navigate to `Binaries/Win64` and create a new file: `steam_appid.txt`. 
In this new text file, input the number **253230** on the first line.


6. Create a shortcut of `HatinTimeGame.exe` from that folder and move it to wherever you'd like. 
You will use this shortcut to open the Archipelago-compatible version of A Hat in Time.


7. Start up the game using your new shortcut. To confirm if you are on the correct version, 
go to Settings -> Game Settings. If you don't see an option labelled ***Live Game Events*** you should be running 
the correct version of the game. In Game Settings, make sure ***Enable Developer Console*** is checked.


## Connecting to the Archipelago server

To connect to the multiworld server, simply run the **ArchipelagoAHITClient** 
(or run it from the Launcher if you have the apworld installed) and connect it to the Archipelago server. 
The game will connect to the client automatically when you create a new save file.


## Console Commands

Commands will not work on the title screen, you must be in-game to use them. To use console commands, 
make sure ***Enable Developer Console*** is checked in Game Settings and press the tilde key or TAB while in-game.

`ap_say <message>` - Send a chat message to the server. Supports commands, such as `!hint` or `!release`.

`ap_deathlink` - Toggle Death Link.


## FAQ/Common Issues
### I followed the setup, but I receive an odd error message upon starting the game or creating a save file!
If you receive an error message such as 
**"Failed to find default engine .ini to retrieve My Documents subdirectory to use. Force quitting."** or
**"Failed to load map "hub_spaceship"** after booting up the game or creating a save file respectively, then the depot
download was likely corrupted. The only way to fix this is to start the entire download all over again.
Unfortunately, this appears to be an underlying issue with Steam's depot downloader. The only way to really prevent this
from happening is to ensure that your connection is not interrupted or slowed while downloading.

### The game keeps crashing on startup after the splash screen!
This issue is unfortunately very hard to fix, and the underlying cause is not known. If it does happen however,
try the following:

- Close Steam **entirely**.
- Open the downpatched version of the game (with Steam closed) and allow it to load to the titlescreen.
- Close the game, and then open Steam again. 
- After launching the game, the issue should hopefully disappear. If not, repeat the above steps until it does.

### I followed the setup, but "Live Game Events" still shows up in the options menu!
The most common cause of this is the `steam_appid.txt` file. If you're on Windows 10, file extensions are hidden by 
default (thanks Microsoft). You likely made the mistake of still naming the file `steam_appid.txt`, which, since file 
extensions are hidden, would result in the file being named `steam_appid.txt.txt`, which is incorrect. 
To show file extensions in Windows 10, open any folder, click the View tab at the top, and check
"File name extensions". Then you can correct the name of the file. If the name of the file is correct, 
and you're still running into the issue, re-read the setup guide again in case you missed a step. 
If you still can't get it to work, ask for help in the Discord thread.

### The game is running on the older version, but it's not connecting when starting a new save!
For unknown reasons, the mod will randomly disable itself in the mod menu. To fix this, go to the Mods menu 
(rocket icon) in-game, and re-enable the mod.

### Why do relics disappear from the stands in the Spaceship after they're completed?
This is intentional behaviour. Because of how randomizer logic works, there is no way to predict the order that 
a player will place their relics. Since there are a limited amount of relic stands in the Spaceship, relics are removed 
after being completed to allow for the placement of more relics without being potentially locked out. 
The level that the relic set unlocked will stay unlocked.

### When I start a new save file, the intro cinematic doesn't get skipped, Hat Kid's body is missing and the mod doesn't work!
There is a bug on older versions of A Hat in Time that causes save file creation to fail to work properly 
if you have too many save files. Delete them and it should fix the problem.