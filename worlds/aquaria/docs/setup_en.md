# Aquaria Randomizer Setup Guide

## Required Software

- The original Aquaria Game (purchasable from most online game stores)
- The [Aquaria randomizer](https://github.com/tioui/Aquaria_Randomizer/releases/latest)

## Optional Software
 
- For sending [commands](/tutorial/Archipelago/commands/en) like `!hint`: the TextClient from [the most recent Archipelago release](https://github.com/ArchipelagoMW/Archipelago/releases/latest)
- [Aquaria AP Tracker](https://github.com/palex00/aquaria-ap-tracker/releases/latest), for use with
[PopTracker](https://github.com/black-sliver/PopTracker/releases/latest)

## Installation and execution Procedures

### Windows

First, you should copy the original Aquaria folder game. The randomizer will possibly modify the game so that
the original game will stop working. Copying the folder will guarantee that the original game keeps on working.
Also, in Windows, the save files are stored in the Aquaria folder. So copying the Aquaria folder for every Multiworld
game you play will make sure that every game has its own save game.

Unzip the Aquaria randomizer release and copy all unzipped files in the Aquaria game folder. The unzipped files are:
- aquaria_randomizer.exe
- OpenAL32.dll
- randomizer_files (directory)
- SDL2.dll
- usersettings.xml
- wrap_oal.dll
- cacert.pem

If there is a conflict between files in the original game folder and the unzipped files, you should overwrite
the original files with the ones from the unzipped randomizer.

There is multiple way to start the game. The easiest one is using the launcher. To do that, just run
the `aquaria_randomizer.exe` file.

You can also launch the randomizer using the command line interface (you can open the command line interface
by typing `cmd` in the address bar of the Windows File Explorer). Here is the command line used to start the
randomizer:

```bash
aquaria_randomizer.exe --name YourName --server theServer:thePort
```

or, if the room has a password:

```bash
aquaria_randomizer.exe  --name YourName --server theServer:thePort --password thePassword
```

### Linux when using the AppImage

If you use the AppImage, just copy it into the Aquaria game folder. You then have to make it executable. You
can do that from the command line by using:

```bash
chmod +x Aquaria_Randomizer-*.AppImage
```

or by using the Graphical file Explorer of your system (the permission can generally be set in the file properties).

To launch the randomizer using the integrated launcher, just execute the AppImage file.

You can also use command line arguments to set the server and slot of your game:

```bash
./Aquaria_Randomizer-*.AppImage --name YourName --server theServer:thePort
```

or, if the room has a password:

```bash
./Aquaria_Randomizer-*.AppImage --name YourName --server theServer:thePort --password thePassword
```

Note that you should not have multiple Aquaria_Randomizer AppImage file in the same folder. If this situation occurs,
the preceding commands will launch the game multiple times.

### Linux when using the tar file

First, you should copy the original Aquaria folder game. The randomizer will possibly modify the game so that
the original game will stop working. Copying the folder will guarantee that the original game keeps on working.

Untar the Aquaria randomizer release and copy all extracted files in the Aquaria game folder. The extracted files are:
- aquaria_randomizer
- randomizer_files (directory)
- usersettings.xml
- cacert.pem

If there is a conflict between files in the original game folder and the extracted files, you should overwrite
the original files with the ones from the extracted randomizer files.

Then, you should use your system package manager to install `liblua5`, `libogg`, `libvorbis`, `libopenal` and `libsdl2`.
On Debian base systems (like Ubuntu), you can use the following command:

```bash
sudo apt install liblua5.1-0-dev libogg-dev libvorbis-dev libopenal-dev libsdl2-dev
```

Also, if there are certain `.so` files in the original Aquaria game folder (`libgcc_s.so.1`, `libopenal.so.1`,
`libSDL-1.2.so.0` and `libstdc++.so.6`), you should remove them from the Aquaria Randomizer game folder. Those are
old libraries that will not work on the recent build of the randomizer.

To launch the randomizer using the integrated launcher, just execute the `aquaria_randomizer` file.

You can also use command line arguments to set the server and slot of your game:

```bash
./aquaria_randomizer --name YourName --server theServer:thePort
```

or, if the room has a password:

```bash
./aquaria_randomizer --name YourName --server theServer:thePort --password thePassword
```

Note: If you get a permission denied error when using the command line, you can use this command to be
sure that your executable has executable permission:

```bash
chmod +x aquaria_randomizer
```
### Steam deck

On the Steamdeck, go in desktop mode and follow the same procedure as the Linux Appimage.


### No sound on Linux/Steam deck

If your game play without problems, but with no sound, the game probably does not use the correct
driver for the sound system. To fix that, you can use `ALSOFT_DRIVERS=pulse` before your command
line to make it work. Something like this (depending on the way you launch the randomizer):

```bash
ALSOFT_DRIVERS=pulse ./Aquaria_Randomizer-*.AppImage --name YourName --server theServer:thePort
```

## Auto-Tracking

Aquaria has a fully functional map tracker that supports auto-tracking.

1. Download [Aquaria AP Tracker](https://github.com/palex00/aquaria-ap-tracker/releases/latest) and
[PopTracker](https://github.com/black-sliver/PopTracker/releases/latest).
2. Put the tracker pack into /packs/ in your PopTracker install.
3. Open PopTracker, and load the Aquaria pack.
4. For autotracking, click on the "AP" symbol at the top.
5. Enter the Archipelago server address (the one you connected your client to), slot name, and password.

This pack will automatically prompt you to update if one is available.
