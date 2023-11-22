# Super Mario 64 EX MultiWorld Setup Guide

## Required Software

- Super Mario 64 US or JP Rom (Europe and Shindou not supported)
- Either of
    - [SM64AP-Launcher](https://github.com/N00byKing/SM64AP-Launcher/releases) or
    - Cloning and building [sm64ex](https://github.com/N00byKing/sm64ex) manually
- Optional, for sending [commands](/tutorial/Archipelago/commands/en) like `!hint`: the TextClient from [the most recent Archipelago release](https://github.com/ArchipelagoMW/Archipelago/releases)

NOTE: The above linked launcher is a special version designed to work with the Archipelago build of sm64ex.
You can use other sm64-port based builds with it, but you can't use a different launcher with the Archipelago build of sm64ex.

## Installation and Game Start Procedures

### Installation via SM64AP-Launcher

*Windows Preparations*

First, install [MSYS](https://www.msys2.org/) as described on the page. DO NOT INSTALL INTO A FOLDER PATH WITH SPACES.
It is extremely encouraged to use the default install directory!
Then continue to `Using the Launcher`

*Linux Preparations*

You will need to install some dependencies before using the launcher.
The launcher itself needs `qt6`, `patch` and `git`, and building the game requires `sdl2 glew cmake python make` (If you install `jsoncpp` as well, it will be linked dynamically).
Then continue to `Using the Launcher`

*Using the Launcher*

1. Go to the page linked for SM64AP-Launcher, and press on the topmost entry
2. Scroll down, and download the zip file for your OS.
3. Unpack the zip file in an empty folder
4. Run the Launcher. On first start, press `Check Requirements`, which will guide you through the rest of the needed steps.
    - Windows: If you did not use the default install directory for MSYS, close this window, check `Show advanced options` and reopen using `Re-check Requirements`. You can then set the path manually.
5. When finished, use `Compile default SM64AP build` to continue
    - Advanced user can use `Show advanced options` to build with custom makeflags (`BETTERCAMERA`, `NODRAWINGDISTANCE`, ...), different repos and branches, and game patches such as 60FPS, Enhanced Moveset and others.
6. Press `Download Files` to prepare the build, afterwards `Create Build`.
7. SM64EX will now be compiled. This can take a while.

After it's done, the build list should have another entry with the name you gave it.

NOTE: If it does not start when pressing `Play selected build`, recheck if you typed the launch options correctly (Described in "Joining a MultiWorld Game")

### Manual Compilation (Linux/Windows)

*Windows Preparations*

First, install [MSYS](https://www.msys2.org/) as described on the page. DO NOT INSTALL INTO A FOLDER PATH WITH SPACES.

After launching msys2 using a MinGW x64 shell (there should be a start menu entry), update by entering `pacman -Syuu` in the command prompt. Next, install the relevant dependencies by entering `pacman -S unzip mingw-w64-x86_64-gcc mingw-w64-x86_64-glew mingw-w64-x86_64-SDL2 git make python3 mingw-w64-x86_64-cmake`.

Continue to `Compiling`.

*Linux Preparations*

Install the relevant dependencies `sdl2 glew cmake python make patch git`. SM64EX will link `jsoncpp` dynamic if installed. If not, it will compile and link statically.

Continue to `Compiling`.

*Compiling*

Obtain the code base by cloning the relevant repository via `git clone --recursive https://github.com/N00byKing/sm64ex`. Copy your legally dumped rom into your sm64ex folder (if you are not sure where your folder is located, do a quick Windows search for sm64ex). The name of the ROM needs to be `baserom.REGION.z64` where `REGION` is either `us` or `jp` respectively.

After all these preparatory steps have succeeded, type `cd sm64ex && make` in your command prompt and get ready to wait for a bit. If you want to speed up compilation, tell the compiler how many CPU cores to use by using `make -jn` instead, where n is the number of cores you want.

After the compliation was successful, there will be a binary in your `sm64ex/build/REGION_pc/` folder.

### Joining a MultiWorld Game

To join, set the following launch options: `--sm64ap_name YourName --sm64ap_ip ServerIP:Port`.
For example, if you are hosting a game using the website, `YourName` will be the name from the Settings Page, `ServerIP` is `archipelago.gg` and `Port` the port given on the Archipelago room page.
Optionally, add `--sm64ap_passwd "YourPassword"` if the room you are using requires a password.
Should your name or password have spaces, enclose it in quotes: `"YourPassword"` and `"YourName"`.

Should the connection fail (for example when using the wrong name or IP/Port combination) the game will inform you of that.
Additionally, any time the game is not connected (for example when the connection is unstable) it will attempt to reconnect and display a status text.

**Important:** You must start a new file for every new seed you play. Using `⭐x0` files is **not** sufficient.
Failing to use a new file may make some locations unavailable. However, this can be fixed without losing any progress by exiting and starting a new file.

### Playing offline

To play offline, first generate a seed on the game's settings page.
Create a room and download the `.apsm64ex` file, and start the game with the `--sm64ap_file "path/to/FileName"` launch argument.

### Optional: Using Batch Files to play offline and MultiWorld games

As an alternative to launching the game with SM64AP-Launcher, it is also possible to launch the completed build with the use of Windows batch files. This has the added benefit of streamlining the join process so that manual editing of connection info is not needed for each new game. However, you'll need to be somewhat comfortable with creating and using batch files.

IMPORTANT NOTE: The remainder of this section uses copy-and-paste code that assumes you're using the US version. If you instead use the Japanese version, you'll need to edit the EXE name accordingly by changing "sm64.us.f3dex2e.exe" to "sm64.jp.f3dex2e.exe".

### Making an offline.bat for launching offline patch files

Open Notepad. Paste in the following text: `start sm64.us.f3dex2e.exe --sm64ap_file %1`

Go to File > Save As...

Navigate to the folder you selected for your SM64 build when you followed the Build guide for SM64AP-Launcher earlier. Once there, navigate further into `build` and then `us_pc`. This folder should be the same folder that `sm64.us.f3dex2e.exe` resides in. 

Make the file name `"offline.bat"` . THE QUOTE MARKS ARE IMPORTANT! Otherwise, it will create a text file instead ("offline.bat.txt"), which won't work as a batch file.

Now you should have a file called `offline.bat` with a gear icon in the same folder as your "sm64.us.f3dex2e.exe". Right click `offline.bat` and choose `Send To > Desktop (Create Shortcut)`.
-  If the icon for this file is a notepad rather than a gear, you saved it as a .txt file on accident. To fix this, change the file extension to .bat.

From now on, whenever you start an offline, single-player game, just download the `.apsm64ex` patch file from the Generator, then drag-and-drop that onto `offline.bat` to open the game and start playing.

NOTE: When playing offline patch files, a `.save` file is created in the same directory as your patch file, which contains your save data for that seed. Don't delete it until you're done with that seed.

### Making an online.bat for launching online Multiworld games

These steps are very similar. You will be making a batch file in the same location as before. However, the text you put into this batch file is different, and you will not drag patch files onto it.

Use the same steps as before to open Notepad and paste in the following:

`set /p port="Enter port number of room - "`

`set /p slot="Enter slot name - "`

`start sm64.us.f3dex2e.exe --sm64ap_name "%slot%" --sm64ap_ip archipelago.gg:%port%`

Save this file as `"online.bat"`, then create a shortcut by following the same steps as before. 

To use this batch file,  double-click it. A window will open. Type the five-digit port number of the room you wish to join, then type your slot name.
- The port number is provided on the room page. The game host should share this page with all players.
- The slot name is whatever you typed in the "Name" field when creating a config file. All slot names are visible on the room page.

Once you provide those two bits of information, the game will open. 
- If the game only says `Connecting`, try again. Double-check the port number and slot name; even a single typo will cause your connection to fail.

### Addendum - Deleting old saves

Loading an old Mario save alongside a new seed is a bad idea, as it can cause locked doors and castle secret stars to already be unlocked / obtained. You should avoid opening a save that says "Stars x 0" as opposed to one that simply says "New".

You can manually delete these old saves in-game before starting a new game, but that can be tedious. With a small edit to the batch files, you can delete these old saves automatically. Just add the line `del %AppData%\sm64ex\*.bin` to the batch file, above the `start` command. For example, here is `offline.bat` with the additional line:

`del %AppData%\sm64ex\*.bin`

`start sm64.us.f3dex2e.exe --sm64ap_file %1`

This extra line deletes any previous save data before opening the game. Don't worry about lost stars or checks - the AP server (or in the case of offline, the `.save` file) keeps track of your star count, unlocked keys/caps/cannons, and which locations have already been checked, so you won't have to redo them. At worst you'll have to rewatch the door unlocking animations, and catch the rabbit Mips twice for his first star again if you haven't yet collected the second one.

## Installation Troubleshooting

Start the game from the command line to view helpful messages regarding SM64EX.

### Game doesn't start after compiling

Most likely you forgot to set the launch options. `--sm64ap_name YourName` and `--sm64ap_ip ServerIP:Port` are required for startup for Multiworlds, and
`--sm64ap_file FileName` is required for (offline) singleplayer.
If your Name or Password have spaces in them, surround them in quotes.

### Game crashes upon entering Peach's Castle

This happens when the game is missing the relevant randomizer data. If you are trying to connect to a server, verify the
information entered is correct, and for a local file ensure you are using the full file path to the file in conjunction
with its name.

## Game Troubleshooting

### Known Issues

When using a US Rom, the In-Game messages are missing some letters: `J Q V X Z` and `?`.
The Japanese Version should have no problem displaying these.

### Toad does not have an item for me.

This happens when you load an existing file that had already received an item from that toad.
To resolve this, exit and start from a `NEW` file. The server will automatically restore your progress.

### What happens if I lose connection?

SM64EX tries to reconnect a few times, so be patient.
Should the problem still be there after about a minute or two, just save and restart the game.

### How do I update the Game to a new Build?

When using the Launcher follow the normal build steps, but when choosing a folder name use the same as before. The launcher will recognize this, and offer to replace it.
When manually compiling just pull in changes and run `make` again. Sometimes it helps to run `make clean` before.
