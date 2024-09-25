# Setup Guide for Adventure: Archipelago

## Important

As we are using BizHawk, this guide is only applicable to Windows and Linux systems.

## Required Software

- BizHawk: [BizHawk Releases from TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
  - Version 2.3.1 and later are supported. Version 2.7 is recommended for stability.
  - Detailed installation instructions for BizHawk can be found at the above link.
  - Windows users must run the prereq installer first, which can also be found at the above link.
- The built-in Archipelago client, which can be installed [here](https://github.com/ArchipelagoMW/Archipelago/releases).
- An Adventure NTSC ROM file. The Archipelago community cannot provide these.

## Configuring BizHawk

Once BizHawk has been installed, open EmuHawk and change the following settings:

- (≤ 2.8) Go to Config > Customize. Switch to the Advanced tab, then switch the Lua Core from "NLua+KopiLua" to
  "Lua+LuaInterface". Then restart EmuHawk. This is required for the Lua script to function correctly.
  **NOTE: Even if "Lua+LuaInterface" is already selected, toggle between the two options and reselect it. Fresh installs** 
  **of newer versions of EmuHawk have a tendency to show "Lua+LuaInterface" as the default selected option but still load** 
  **"NLua+KopiLua" until this step is done.**
- Under Config > Customize, check the "Run in background" box. This will prevent disconnecting from the client while
EmuHawk is running in the background.

- It is recommended that you provide a path to EmuHawk in your host.yaml for Adventure so the client can start it automatically
- At the same time, you can set an option to automatically load the connector_adventure.lua script when launching EmuHawk
from AdventureClient.
Default Windows install example:
```rom_args: "--lua=C:/ProgramData/Archipelago/data/lua/connector_adventure.lua"```

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

You can generate a yaml or download a template by visiting the [Adventure Options Page](/games/Adventure/player-options)

### What are recommended options to tweak for beginners to the rando?
Setting difficulty_switch_a and lowering the dragons' speeds makes the dragons easier to avoid.  Adding Chalice to 
local_items guarantees you'll visit at least one of the interesting castles, as it can only be placed in a castle or
the credits room.

## Joining a MultiWorld Game

### Obtain your Adventure patch file

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your data file, or with a zip file containing everyone's data
files. Your data file should have a `.apadvn` extension.

Drag your patch file to the AdventureClient.exe to start your client and start the ROM patch process. Once the process 
is finished (this can take a while), the client and the emulator will be started automatically (if you set the emulator 
path as recommended).

### Connect to the Multiserver

Once both the client and the emulator are started, you must connect them, assuming you didn't set it up to be automatic.
Navigate to your Archipelago install folder, then to `data/lua`, and drag+drop the `connector_adventure.lua` script onto
the main EmuHawk window. (You could instead open the Lua Console manually, click `Script` 〉 `Open Script`, and navigate
to `connector_adventure.lua` with the file picker.)

To connect the client to the multiserver simply put `<address>:<port>` on the textfield on top and press enter (if the
server uses password, type in the bottom textfield `/connect <address>:<port> [password]`)

Press Reset and begin playing
