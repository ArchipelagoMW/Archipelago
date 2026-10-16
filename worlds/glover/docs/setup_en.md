
# SETUP GUIDE FOR GLOVER ARCHIPELAGO

## Important

As we are using BizHawk, this guide is only applicable to Windows and Linux systems.
Our implementation also supports the Everdrive 3.0 and X7. (USB Support)

## Required Software and Hardware

-   PC Emulation:
    -   BizHawk:  [BizHawk Releases from TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
        -   Version <b>2.10</b> and later are supported.
        -   Detailed installation instructions for BizHawk can be found at the above link.
        -   Windows users must run the prereq installer first, which can also be found at the above link.
-   A Glover ROM (USA ONLY).

## Playing on BizHawk
### Configuring BizHawk

Once BizHawk has been installed, open EmuHawk and change the following settings:

-   Under Config > Customize, check the "Run in background" and "Accept background input" boxes. This will allow you to continue playing in the background, even if another window is selected.
-   Under Config > Hotkeys, many hotkeys are listed, with many bound to common keys on the keyboard. You will likely want to disable most of these, which you can do quickly using  `Esc`.
-   Under N64 enable "Use Expansion Slot". (The N64 menu only appears after loading a ROM.)
-   Under Config -> Speed/Skip, click "Audio Throttle" as this will fix the off pitch sounds while playing

It is strongly recommended to associate N64 rom extensions (*.n64, *.z64) to the EmuHawk we've just installed. To do so, we simply have to search any N64 rom we happened to own, right click and select "Open with…", unfold the list that appears and select the bottom option "Look for another application", then browse to the BizHawk folder and select EmuHawk.exe.

If you are experiencing performance issues with Glover, you can try the following:
- Under N64 -> Plugins, Set Active Video Plugin to Rice.
This will create some visual artifacts however, it should not affect gameplay.

### Setup - BizHawk
- Run Launcher.exe and select Glover Client
- If this is your first time running this version, it will prompt for your Glover (US) ROM
- The patched rom is located in your Archipelago root folder by default
    - The exact path is also printed on the Glover Client
    - You can also click "Browse Files" in the Launcher which will take you to this folder
- <b>one time only</b> run <b>/autostart</b> in the Glover Client and select Emuhawk.exe. This will automatically open Bizhawk, the patched Glover ROM and the required Lua script to connect.
- Connect the Archipelago Client with the server.
    - To connect the client to the multiserver simply put  `<address>:<port>`  on the textfield on top and press `connect` (if the server uses password, then it will prompt after connection).
- If you rather not use <b>/autostart</b>:
    - Open Bizhawk and open your patched Glover (US) game
    - Once you are in the game title menu or game select screen, drag and drop the connector_glover_bizhawk.lua script (which can be found in the data/lua folder of Archipelago) onto the Lua console window.