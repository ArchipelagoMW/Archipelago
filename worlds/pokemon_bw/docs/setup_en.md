# Setup Guide for Pokémon Black and White: Archipelago

## Important

As we are using BizHawk, this guide is only applicable to Windows and Linux systems. 
This APWorld is still in development, so expect bugs! 
If you find one, please report it to the #future-game-design thread for this game!

## Required Software

- BizHawk: [Bizhawk Releases from TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
  - Version 2.10 is recommended
  - **Important**: Upon opening the emulator for the first time, go to `Config > Customize... > Advanced` 
    and **disable** `AutoSaveRam`. Else, save data might not be properly saved.
  - Detailed installation instructions for BizHawk can be found at the above link.
  - Windows users must run the prerequisite installer first, which can also be found at the above link.
- The built-in BizHawk client within the Archipelago software, which can be found 
  [here](https://github.com/ArchipelagoMW/Archipelago/releases)
- A .nds file for the english version of Pokémon Black and White
  - The english versions for USA and Europe are the same

## Joining a MultiWorld Game

### Obtain your NDS patch file

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your data file, or with a zip file containing everyone's data
files. Your data file should have a `.apblack` or `.apwhite` extension. 

Double-click on your `.apblack` or `.apwhite` file to start your client and start the ROM patch process. 
Once the process is finished, the client and the emulator will be started automatically, 
if you associated the extension to the client as recommended.
If the extension isn't associated, select the Archipelago Launcher as the program to open the 
`.apblack` or `.apwhite` file with.

### Connect client to emulator

Once both the client and the emulator are started, you must connect them, if this is not done automatically. Within the 
emulator click on the "Tools" menu and select "Lua Console". Click the folder button or press Ctrl+O to open a Lua 
script.

Navigate to your Archipelago install folder and open `data/lua/connector_bizhawk_generic.lua`.

### Connect to the Multiserver

To connect the client to the multiserver simply put `<address>:<port>` on the textfield on top and 
press enter or `Connect`. 
An alternative way to connect is typing `/connect <address>:<port> [password]` into the bottom text field and then 
typing your slot name (if prompted).
