# A Link to the Past Randomizer Multiworld Setup Guide

<div style="width:100%; text-align: center;">
    <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/mJKEHaiyR_Y" frameborder="0"
      allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
    </iframe>
</div>

## Required Software
- [Multiworld Utilities](https://github.com/Berserker66/MultiWorld-Utilities/releases)
- [QUsb2Snes](https://github.com/Skarsnik/QUsb2snes/releases) (Included in the above Utilities)
- Hardware or software capable of loading and playing SNES ROM files
    - An emulator capable of running Lua scripts
      ([snes9x Multitroid](https://drive.google.com/drive/folders/1_ej-pwWtCAHYXIrvs5Hro16A1s9Hi3Jz),
      [BizHawk](http://tasvideos.org/BizHawk.html))
    - An SD2SNES, [FXPak Pro](https://krikzz.com/store/home/54-fxpak-pro.html), or other compatible hardware
- Your Japanese v1.0 ROM file, probably named `Zelda no Densetsu - Kamigami no Triforce (Japan).sfc`

## Installation Procedures

### Windows Setup
1. Download and install the Multiworld Utilities from the link above, making sure to install the most recent version.
**The file is located in the assets section at the bottom of the version information**. If you intend to play normal
multiworld games, you want _Setup.BerserkerMultiWorld.exe_.
    - If you intend to play the doors variant of multiworld, you will want to download the alternate doors file.
    - During the installation process, you will be asked to browse for your Japanese 1.0 ROM file. If you have
      installed this software before and are simply upgrading now, you will not be prompted to locate your
      ROM file a second time.
    - You may also be prompted to install Microsoft Visual C++. If you already have this software on your computer
      (possibly because a Steam game installed it already), the installer will not prompt you to install it again.

2. If you are using an emulator, you should assign your Lua capable emulator as your default program
for launching ROM files.
    1. Extract your emulator's folder to your Desktop, or somewhere you will remember. 
    2. Right click on a ROM file and select **Open with...**
    3. Check the box next to **Always use this app to open .sfc files**
    4. Scroll to the bottom of the list and click the grey text **Look for another App on this PC**
    5. Browse for your emulator's `.exe` file and click **Open**. This file should be located inside
       the folder you extracted in step one.

### Macintosh Setup
- We need volunteers to help fill this section! Please contact **Farrak Kilhn** on Discord if you want to help.

### Linux Setup
- Coming Soon™

## Configuring your YAML file

### What is a YAML file and why do I need one?
Your YAML file contains a set of configuration options which provide the generator with information about how
it should generate your game. Each player of a multiworld will provide their own YAML file. This setup allows
each player to enjoy an experience customized for their taste, and different players in the same multiworld
can all have different options.

### Your YAML file is weighted
Throughout your YAML file, you will see many options which look similar to this:
```yaml
map_shuffle:
  on: 5
  off: 15
```
In the above example, imagine the generator creates a bucket labelled "map_shuffle", and places a folded
piece of paper into the bucket for each sub-option. Here, there are twenty pieces of paper in the bucket:
five for "on" and fifteen for "off". When the generator is deciding whether or not to turn on map shuffle
for your game, it reaches into this bucket and pulls out a piece of paper at random. In this example,
you are much more likely to have map shuffle turned off. If you never want an option to be chosen, simply
set its value to zero.

### ROM Options
At the bottom of your YAML file, you will find a set of ROM options. These control various aesthetic changes
which do not affect gameplay. These options are also weighted, in case you want to be surprised by the color
of your hearts or by the silliness of your overworld palette.

If you would like to add a sprite to the list, simply include its name and give it a weight like so:
```yaml
rom:
  sprite: # Enter the name of your preferred sprite and weight it appropriately
    random: 0
    randomonhit: 0
    link: 1
    vegeta: 3
    rottytops: 5
    rocko: 5
    luigi: 3
```

## Joining a Multiworld Game

### Obtain your patch file and create your ROM
When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that
is done, the host will provide you with either a link to download your patch file, or with a zip file containing
everyone's patch files. Your patch file should have a `.bmbp` extension. Put your patch file on your desktop or
somewhere convenient, and double click it. This should automatically launch the client, and will also create
your ROM file in the same place as your patch file.

### Connect to the client

#### With an emulator
When the client launched automatically, QUsb2Snes should have also automatically launched in the background.
If this is its first time launching, you may be prompted to allow it to communicate through the Windows
Firewall.

##### snes9x Multitroid
1. Load your ROM file if it hasn't already been loaded.
2. Click on the File menu and hover on **Lua Scripting**
3. Click on **New Lua Script Window...**
4. In the new window, click **Browse...**
5. Browse to the location you extracted snes9x Multitroid to, enter the `lua` folder, and choose `multibridge.lua`
6. Observe a name has been assigned to you, and that the client shows "SNES Device: Connected", with that same
   name in the upper left corner.

##### BizHawk
1. Load your ROM file if it hasn't already been loaded.
2. Click on the Tools menu and click on **Lua Console**
3. Click the button to open a new Lua script.
4. Browse to your Multiworld Utilities installation directory, and into the following folders:  
   `QUsb2Snes --> Qusb2Snes --> LuaBridge`
5. Select `luabridge.lua` and click Open.
6. Observe a name has been assigned to you, and that the client shows "SNES Device: Connected", with that same
   name in the upper left corner. 

#### With hardware
This guide assumes you have downloaded the correct firmware for your device. If you have not
done so already, please do this now. SD2SNES and FXPak Pro users may download the appropriate firmware
[here](https://github.com/RedGuyyyy/sd2snes/releases). Other hardware may find helpful information
[on this page](http://usb2snes.com/#supported-platforms).

**To connect with hardware you must use an old version of QUsb2Snes
([v0.7.16](https://github.com/Skarsnik/QUsb2snes/releases/tag/v0.7.16)).**  
Versions of QUsb2Snes later than this break compatibility with multiworld.

1. Close your emulator, which may have auto-launched.
2. Close QUsb2Snes, which launched automatically with the client.
3. Launch the appropriate version of QUsb2Snes (v0.7.16).
4. Power on your device and load the ROM.
5. Observe the client window now shows "SNES Device: Connected", and lists the name of your device.

### Connect to the MultiServer
The patch file which launched your client should have automatically connected you to the MultiServer.
However there are a few reasons this may not happen, including if the game is hosted on the website but
was generated elsewhere. If the client window shows "Server Status: Not Connected", simply ask the host
for the address of the server, and copy/paste it into the "Server" input field then press enter.
The client will attempt to reconnect to the new server address, and should momentarily show "Server
Status: Connected". If the client does not connect after a few moments, you may need to refresh the page.

### Play the game
When the client shows both SNES Device and Server as connected, you're ready to begin playing. Congratulations
on successfully joining a multiworld game!

## Hosting a game
The recommended way to host a game is to use the hosting service provided on
[the website](https://berserkermulti.world/generate). The process is relatively simple:
1. Collect YAML files from your players.
2. Create a zip file containing your players' YAML files.
3. Upload that zip file to the website linked above.
4. Wait a moment while the seed is generated.
5. Provide your players with a link to the "Seed Info" page so they may download their patch files.
6. Click "Create New Room". This will take you to the server page, where you may find the server address to
   send to your players if they do not connect automatically. It should look similar to: `45.83.104.96:50783`
7. Note that a link to a Multiworld Tracker is at the top of the room page. You should also provide this link
   to your players so they can watch the progress of the game.
8. Once all players have joined, you may begin playing.
