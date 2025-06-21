
# SETUP GUIDE FOR BANJO-TOOIE ARCHIPELAGO

## Important

As we are using BizHawk, this guide is only applicable to Windows and Linux systems.
Our implementation also supports the Everdrive 3.0 and X7. (USB Support)

## Required Software and Hardware

-   PC Emulation:
    -   BizHawk:  [BizHawk Releases from TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
        -   Version <b>2.9.1</b> will be dropping support soon.
        -   Version <b>2.10</b> and later are supported.
        -   Detailed installation instructions for BizHawk can be found at the above link.
        -   Windows users must run the prereq installer first, which can also be found at the above link.
-   Everdrive:
    - The USB driver on the PC that will be connecting to the everdrive
        - Windows: https://ftdichip.com/wp-content/uploads/2021/08/CDM212364_Setup.zip
        - Linux: https://ftdichip.com/wp-content/uploads/2022/07/libftd2xx-x86_64-1.4.27.tgz
    - For Everdrive 3.0, the OS version needs to be 3.06 to be compatible.
    - The Nintendo 64 Expansion Pak is required
    -   Grab the latest release of the Everdrive connector from https://github.com/jjjj12212/AP_Banjo-Tooie/releases
-   A Banjo-Tooie ROM (USA ONLY).

## Playing on BizHawk
### Configuring BizHawk

Once BizHawk has been installed, open EmuHawk and change the following settings:

-   Under Config > Customize, check the "Run in background" and "Accept background input" boxes. This will allow you to continue playing in the background, even if another window is selected.
-   Under Config > Hotkeys, many hotkeys are listed, with many bound to common keys on the keyboard. You will likely want to disable most of these, which you can do quickly using  `Esc`.
-   If playing with a controller, when you bind controls, disable "P1 A Up", "P1 A Down", "P1 A Left", and "P1 A Right" as these interfere with aiming if bound. Set directional input using the Analog tab instead.
-   Under N64 enable "Use Expansion Slot". (The N64 menu only appears after loading a ROM.)
-   Under Config -> Speed/Skip, click "Audio Throttle" as this will fix the off pitch sounds while playing

It is strongly recommended to associate N64 rom extensions (*.n64, *.z64) to the EmuHawk we've just installed. To do so, we simply have to search any N64 rom we happened to own, right click and select "Open with…", unfold the list that appears and select the bottom option "Look for another application", then browse to the BizHawk folder and select EmuHawk.exe.

If you are experiencing performance issues with Banjo-Tooie, you can try the following:
- Under N64 -> Plugins, Set Active Video Plugin to Rice.
This will create some visual artifacts however, it should not affect gameplay.

### Setup - BizHawk
- Run Launcher.exe and select Banjo-Tooie Client
- If this is your first time running this version, it will prompt for your Banjo-Tooie (US) ROM
- The patched rom is located in your Archipelago root folder
    - The exact path is also printed on the Banjo-Tooie Client
    - You can also click "Browse Files" in the Launcher which will take you to this folder
- Connect the Archipelago Client with the server.
    - To connect the client to the multiserver simply put  `<address>:<port>`  on the textfield on top and press `connect` (if the server uses password, then it will prompt after connection).
- Open Bizhawk (2.10+) and open your patched Banjo-Tooie (US) game
- Once you are in the game title menu or game select screen, drag and drop the banjo_tooie_connector lua script (which can be found in the data/lua folder of Archipelago) onto the Lua console window.

## Playing on Everdrive
- Run ArchipelagoLauncher.exe and select Banjo-Tooie Client
- If this is your first time running this version, it will prompt for your Banjo-Tooie (US) ROM
- The patched rom is located in your Archipelago root folder
    - The exact path is also printed on the Banjo-Tooie Client
    - You can also click "Browse Files" in the Launcher which will take you to this folder
- Load the patched version of the ROM on your everdrive sd card
- The Everdrive will need to have a USB connection to the PC that will be running the Banjo-Tooie Client.
- Open the banjo_tooie_everdrive_connector.exe (you have to do this before you connect the Banjo-Tooie Client with Archipelago)
    - If you are on Linux, run Banjo_Tooie_everdrive_connector_linux instead
- Run the patched Banjo-Tooie Rom on the everdrive
- Connect the Archipelago client with the server. (The banjo_tooie_connector window should say, "Connection Established")
- To connect the client to the multiserver, simply put  `<address>:<port>`  on the textfield on top and press `connect` (if the server uses password, then it will prompt after connection).
