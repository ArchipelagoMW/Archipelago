# Super Mario 64 EX Advanced Setup Guide

## Required Software

- Super Mario 64 US Rom (Japanese will work also. Europe and Shindou not supported)
- Either of [sm64pclauncher](https://github.com/N00byKing/sm64pclauncher/releases) or
- Cloning and building [sm64ex](https://github.com/N00byKing/sm64ex) manually.

NOTE: The above linked sm64pclauncher is a special version designed to work with the Archipelago build of sm64ex.
You can use other sm64-port based builds with it, but you can't use a different launcher with the Archipelago build of sm64ex.

## Building with Textures, Models and Patch Files

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
8. Set the location for the Models Pack
9. Set the location for the Texture Pack
10. Point the Launcher to your Super Mario 64 US/JP Rom, and set the Region correspondingly
11. Copy the .patch file/s to the enachancements folder which is located in e.g. C:/sm64pclauncher/apmario/enhancements NOTE: outside patches may break the game. Only the ones supplied with the repo are tested
12. click on refresh patchlist click on the patchs you want
13. Set Build Options. Recommended: `-jn` where `n` is the Number of CPU Cores, to build faster and add EXTERNAL_DATA=1 to the build options
SM64EX will now be compiled. The Launcher will appear to have crashed, but this is not likely the case. Best wait a bit, but there may be a problem if it takes longer than 10 Minutes

After it's done, the Build list should have another entry titled with what you named the folder in step 7.

NOTE: For some reason first start of the game always crashes the launcher. Just restart it.
If it still crashes, recheck if you typed the launch options correctly (Described in "Joining a MultiWorld Game")

# Manual Compilation (Linux/Windows)

Dependencies for Linux: `sdl2 glew cmake python make`.
Dependencies for Windows: `mingw-w64-x86_64-gcc mingw-w64-x86_64-glew mingw-w64-x86_64-SDL2 git make python3 mingw-w64-x86_64-cmake`
SM64EX will link `jsoncpp` dynamic if installed. If not, it will compile and link statically.

1. Clone `https://github.com/N00byKing/sm64ex` recursively, `command: git clone -b archipelago --recursive https://github.com/N00byKing/sm64ex`
2. Enter `sm64ex` and copy your Rom to `baserom.REGION.z64` where `REGION` is either `us` or `jp` respectively.
3. Compile with `make`. For faster compilation set the parameter `-jn` where `n` is the Number of CPU Cores. plus EXTERNAL_DATA=1

The Compiled binary will be in `build/REGION_pc/`.

# Other Build Options
There are more build options it's recommended to use only what is required but if you want to use these options USE AT YOUR OWN RISK.
They are listed as Build Option, Default, Possible Values and Description sourced from here https://github.com/sm64pc/sm64ex/wiki/Build-options
1. BETTERCAMERA 0, (0,1) If 1, build with analog camera support (uses Puppycam).
2. NODRAWINGDISTANCE 0, (0,1) If 1, build with disabled draw distance (every object is active at all times). May affect gameplay.
3. TEXTURE_FIX	0, (0,1) If 1, enable various texture-related bugfixes (e.g. fixes the smoke texture).
4. EXTERNAL_DATA 0, (0,1) If 1, load textures and soundbanks from external files. Allows you to use texture packs. The default data is copied to a res folder next to the produced executable.
