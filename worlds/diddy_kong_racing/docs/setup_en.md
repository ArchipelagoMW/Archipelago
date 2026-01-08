# Setup Guide For Diddy Kong Racing Archipelago

## Important

As we are using BizHawk, this guide is only applicable to Windows and Linux systems.

## Required Software/Files

- BizHawk:  [BizHawk Releases from TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
  - Only version 2.10 is supported.
  - Detailed installation instructions for BizHawk can be found at the above link.
  - Windows users must run the prereq installer first, which can also be found at the above link.
- Grab the latest release from https://github.com/zakwiz/DiddyKongRacingAP
- A Diddy Kong Racing v1.0 ROM (USA ONLY).

## Configuring BizHawk

Once BizHawk has been installed, open EmuHawk and change the following settings:

- Under Config > Customize, check the "Run in background" and "Accept background input" boxes. This will allow you to
  continue playing in the background, even if another window is selected.
- Under Config > Hotkeys, many hotkeys are listed, with many bound to common keys on the keyboard. You will likely want
  to disable most of these, which you can do quickly using  `Esc`.
- If playing with a controller, when you bind controls, disable "P1 A Up", "P1 A Down", "P1 A Left", and "P1 A Right" as
  these interfere with aiming if bound. Set directional input using the Analog tab instead.
- Under N64 enable "Use Expansion Slot". (The N64 menu only appears after loading a ROM.)

It is strongly recommended to associate N64 rom extensions (*.n64, *.z64) to the EmuHawk we've just installed. To do so,
we simply have to search any N64 rom we happened to own, right click and select "Open with…", unfold the list that
appears and select the bottom option "Look for another application", then browse to the BizHawk folder and select
EmuHawk.exe.

## How To Install - Server Side

Double-click `diddy_kong_racing.apworld` to install it into the `custom_worlds` folder of your Archipelago install.

## How To Install - Client Side

- Double-click `diddy_kong_racing.apworld` to install it into the `custom_worlds` folder of your Archipelago install.
- Move `connector_diddy_kong_racing.lua` into the `data/lua` folder of your Archipelago install.
- Run the Archipelago launcher and select Diddy Kong Racing Client.
- The client will prompt you to select your ROM so it can be patched.
- Once the patching is complete, connect the Diddy Kong Racing client to the server by clicking the Connect button.
- Open Bizhawk (version 2.10 required) and open your patched Diddy Kong Racing ROM (it should be in the top-level folder
  of your Archipelago install).
- Run the `connector_diddy_kong_racing.lua` script from the `data/lua` folder of your Archipelago install (drag and drop
  it into Bizhawk).

## Generating Your World

Familiarize yourself on how Archipelago works. Here is a guide to learn how to generate your
world: https://archipelago.gg/tutorial/Archipelago/setup/en#generating-a-game

## Connect To The Multiserver

To connect the client to the multiserver, simply put `<address>:<port>` in the textfield on top and press `connect` (if
the server uses password, then it will prompt after connection).
