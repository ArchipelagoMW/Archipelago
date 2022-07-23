# Super Mario 64 EX MultiWorld Setup Guide

## Required Software

- Super Mario 64 US Rom (Japanese may work also. Europe and Shindou not supported)
- Either of [sm64pclauncher](https://github.com/N00byKing/sm64pclauncher/releases) or
- Cloning and building [sm64ex](https://github.com/N00byKing/sm64ex) manually.

NOTE: The above linked sm64pclauncher is a special version designed to work with the Archipelago build of sm64ex.
You can use other sm64-port based builds with it, but you can't use a different launcher with the Archipelago build of sm64ex.

## Installation and Game Start Procedures

# Installation via sm64pclauncher (For Windows)

First, install [MSYS](https://www.msys2.org/) as described on the page. DO NOT INSTALL INTO A FOLDER PATH WITH SPACES.
Do all steps up to including step 6.
Best use default install directory.
Then follow the steps below

1. Go to the page linked for sm64pclauncher, and press on the topmost entry
3. Scroll down, and download the zip file
4. Unpack the zip file in an empty folder
5. Run the Launcher and press build.
6. Set the location where you installed MSYS when prompted. Check the "Install Dependencies" Checkbox
7. Set the Repo link to `https://github.com/N00byKing/sm64ex` and the Branch to `archipelago` (Top two boxes). You can choose the folder (Secound Box) at will, as long as it does not exist yet
8. Point the Launcher to your Super Mario 64 US/JP Rom, and set the Region correspondingly
9. Set Build Options. Recommended: `-jn` where `n` is the Number of CPU Cores, to build faster.
10. SM64EX will now be compiled. The Launcher will appear to have crashed, but this is not likely the case. Best wait a bit, but there may be a problem if it takes longer than 10 Minutes

After it's done, the Build list should have another entry titled with what you named the folder in step 7.

NOTE: For some reason first start of the game always crashes the launcher. Just restart it.
If it still crashes, recheck if you typed the launch options correctly (Described in "Joining a MultiWorld Game")

# Manual Compilation (Linux/Windows)

Dependencies for Linux: `sdl2 glew cmake python make`.
Dependencies for Windows: `mingw-w64-x86_64-gcc mingw-w64-x86_64-glew mingw-w64-x86_64-SDL2 git make python3 mingw-w64-x86_64-cmake`
SM64EX will link `jsoncpp` dynamic if installed. If not, it will compile and link statically.

1. Clone `https://github.com/N00byKing/sm64ex` recursively
2. Enter `sm64ex` and copy your Rom to `baserom.REGION.z64` where `REGION` is either `us` or `jp` respectively.
3. Compile with `make`. For faster compilation set the parameter `-jn` where `n` is the Number of CPU Cores.

The Compiled binary will be in `build/REGION_pc/`.

# Joining a MultiWorld Game

To join, set the following launch options: `--sm64ap_name YourName --sm64ap_ip ServerIP:Port`.
Optionally, add `--sm64ap_passwd "YourPassword"` if the room you are using requires a password.
The Name in this case is the one specified in your generated .yaml file.
In case you are using the Archipelago Website, the IP should be `archipelago.gg`.

If everything worked out, you will see a textbox informing you the connection has been established after the story intro.

# Playing offline

To play offline, first generate a seed on the game's settings page.
Create a room and download the `.apsm64ex` file, and start the game with the `--sm64ap_file "path/to/FileName"` launch argument.

# Using Batch Files to play offline and MultiWorld games

As an alternative to launching the game with sm64pclauncher, it is also possible to launch the completed build with the use of Windows batch files. This has the added benefit of streamlining the join process so that manual editing of connection info is not needed for each new game. However, you'll need to be somewhat comfortable with creating and using batch files.

IMPORTANT NOTE: The remainder of this section uses copy-and-paste code that assumes you're using the US version. If you instead use the Japanese version, you'll need to edit the EXE name accordingly by changing "sm64.us.f3dex2e.exe" to "sm64.jn.f3dex2e.exe".

### Making an offline.bat for launching offline patch files

Open Notepad. Paste in the following text: `start sm64.us.f3dex2e.exe --sm64ap_file %1 --skip-intro`

Go to File > Save As...

Navigate to the folder you selected for your SM64 build when you followed the Build guide for SM64PCLauncher earlier. Once there, navigate further into `build` and then `us_pc`. This folder should be the same folder that `sm64.us.f3dex2e.exe` resides in. 

For "File name:" name it as: `"offline.bat"` . THE QUOTE MARKS ARE IMPORTANT! Otherwise it will create a text file instead ("offline.bat.txt") which won't work as a batch file until you alter the extension properly.

Now you should have a "offline.bat" file with a gear icon in the same folder as your "sm64.us.f3dex2e.exe". (If the icon is instead a notepad, you saved it as a TXT file instead and need to change the extension to BAT). Right click that offline.bat file and choose Send To > Desktop (Create Shortcut).

The batch file you just created and made a shortcut for is set up to accept patch files dragged into it. Start an offline singleplayer game if you haven't already, download the `.apsm64ex` patch file that was prepared by the seed generation, and drag-n-drop that onto the batch file to open the game and start playing.

NOTE: When playing offline patch files, a `.save` file is created in the same directory as your patch file, which contains your save data for that seed. Don't delete it until you're done with that seed.

### Making an online.bat for launching online Multiworld games

The steps here are very similar, as you will be making a batch file in the same location as the offline one. However, the text you put into the batch file is different, and you won't be dragging patch files onto it.

Use the same steps as before to open Notepad and paste in the following:

`set /p port="Enter port number of room - "`

`set /p slot="Enter slot name - "`

`start sm64.us.f3dex2e.exe --sm64ap_name "%slot%" --sm64ap_ip archipelago.gg:%port% --skip-intro`

Save and shortcut the same as before. Unlike the offline batch file, you'll open this one simply by double-clicking it. The window that opens will ask you for the port of the room you wish to join - this five-digit number will be provided by the seed page the game host will share with all players post-generation. Then it will ask you for your slot name - this name is set up in your YAML, and also will be shown on the same seed page previously mentioned, if you need to double-check it.

Once you provide those two bits of information, the game will open. If the info is correct, upon starting the game you should see "Connected to Archipelago" on the bottom of your screen, and be able to enter the castle. If you don't see this text and crash upon entering the castle, try again and ensure you're typing the port and slot name correctly - even a single typo will cause your connection to fail.

### Addendum - Deleting old saves

Loading an old Mario save alongside a new seed is a bad idea, as it can cause locked doors and castle secret stars to already be unlocked / obtained. You should avoid opening a save that says "Stars x 0" as opposed to one that simply says "New".

You can manually delete these old saves ingame before starting a new game, but this can become tedious to do every time. With a small edit to the previous batch files, you can have these old saves deleted automatically, by adding this line to the batch file before the start command. As an example, here it's added to the offline bat:

`del %AppData%\sm64ex\*.bin`

`start sm64.us.f3dex2e.exe --sm64ap_file %1 --skip-intro`

This extra line deletes any previous save data before opening the game. Don't worry about lost stars or checks - the AP server (or in the case of offline, the patch's `.save` file) keeps track of your star count, unlocked keys/caps/cannons, and which locations have already been checked, so you won't have to redo them. At worst you'll have to rewatch the door unlocking animations, and catch rabbit Mips twice for his first star again if you haven't yet collected the second one.

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

### What happens if I lose connection?

SM64EX tries to reconnect a few times, so be patient.
Should the problem still be there after about a minute or two, just save and restart the game.

### How do I update the Game to a new Build?

When manually compiling just pull in changes and run `make` again. Sometimes it helps to run `make clean` before.

When using the Launcher follow the normal build steps, but when choosing a folder name use the same as before. Then continue as normal.
