# Sonic Adventure 2: Battle Randomizer Setup Guide

## Required Software

- Sonic Adventure 2: Battle from: [Sonic Adventure 2: Battle Steam Store Page](https://store.steampowered.com/app/213610/Sonic_Adventure_2/)
	- The Battle DLC is required if you choose to add Chao Karate locations to the randomizer
- SA Mod Manager from: [SA Mod Manager GitHub Releases Page](https://github.com/X-Hax/SA-Mod-Manager/releases)
- .NET Desktop Runtime 7.0 from: [.NET Desktop Runtime 7.0 Download Page](https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/runtime-desktop-7.0.9-windows-x64-installer)
- Archipelago Mod for Sonic Adventure 2: Battle
  from: [Sonic Adventure 2: Battle Archipelago Randomizer Mod Releases Page](https://github.com/PoryGone/SA2B_Archipelago/releases/)

## Optional Software
- Sonic Adventure 2 Tracker
	- PopTracker from: [PopTracker Releases Page](https://github.com/black-sliver/PopTracker/releases/)
	- Sonic Adventure 2: Battle Archipelago PopTracker pack from: [SA2B AP Tracker Releases Page](https://github.com/PoryGone/SA2B_AP_Tracker/releases/)
- Quality of life mods
	- SA2 Volume Controls from: [SA2 Volume Controls Release Page] (https://gamebanana.com/mods/381193)
- Sonic Adventure DX from: [Sonic Adventure DX Steam Store Page](https://store.steampowered.com/app/71250/Sonic_Adventure_DX/)
	- For setting up the `SADX Music` option (See Additional Options for instructions).

## Installation Procedures (Windows)

1. Install Sonic Adventure 2: Battle from Steam.

2. Launch the game at least once without mods.

3. Install SA Mod Manager as per [its instructions](https://github.com/X-Hax/SA-Mod-Manager/tree/master?tab=readme-ov-file).

4. Unpack the Archipelago Mod into the `/mods` directory in the folder into which you installed Sonic Adventure 2: Battle, so that `/mods/SA2B_Archipelago` is a valid path.

5. In the SA2B_Archipelago folder, run the `CopyAPCppDLL.bat` script (a window will very quickly pop up and go away).

6. Launch the `SAModManager.exe` and make sure the SA2B_Archipelago mod is listed and enabled.

## Installation Procedures (Linux and Steam Deck)

1. Install Sonic Adventure 2: Battle from Steam.

2. In the properties for Sonic Adventure 2 on Steam, force the use of Proton Experimental as the compatibility tool.

3. Launch the game at least once without mods.

4. Create both a `/mods` directory and a `/SAManager` directory in the folder into which you installed Sonic Adventure 2: Battle.

5. Install SA Mod Manager as per [its instructions](https://github.com/X-Hax/SA-Mod-Manager/tree/master?tab=readme-ov-file). Specifically, extract SAModManager.exe file to the folder that Sonic Adventure 2: Battle is installed to. To launch it, add ``SAModManager.exe`` as a non-Steam game. In the properties on Steam for SA Mod Manager, set it to use Proton as the compatibility tool.

6. Run SAModManager.exe from Steam once. It should produce an error popup for a missing dependency, close the error.

7. Install protontricks, on the Steam Deck this can be done via the Discover store, on other distros instructions vary, [see its github page](https://github.com/Matoking/protontricks).

8. Download the [.NET 7 Desktop Runtime for x64 Windows](https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/runtime-desktop-7.0.17-windows-x64-installer). If this link does not work, the download can be found on [this page](https://dotnet.microsoft.com/en-us/download/dotnet/7.0).

9. Right click the .NET 7 Desktop Runtime exe, and assuming protontricks was installed correctly, the option to "Open with Protontricks Launcher" should be available. Click that, and in the popup window that opens, select SAModManager.exe. Follow the prompts after this to install the .NET 7 Desktop Runtime for SAModManager. Once it is done, you should be able to successfully launch SAModManager to steam.

6. Unpack the Archipelago Mod into this folder, so that `/mods/SA2B_Archipelago` is a valid path.

7. In the SA2B_Archipelago folder, copy the `APCpp.dll` file and paste it in the Sonic Adventure 2 install folder (where `sonic2app.exe` is).

8. Launch `SAModManager.exe` from Steam and make sure the SA2B_Archipelago mod is listed and enabled.

Note: Ensure that you launch Sonic Adventure 2 from Steam directly on Linux, rather than launching using the `Save & Play` button in SA Mod Manager.

## Joining a MultiWorld Game

1. Before launching the game, run the `SAModManager.exe`, select the SA2B_Archipelago mod, and hit the `Configure Mod` button.

2. For the `Server IP` field under `AP Settings`, enter the address of the server, such as archipelago.gg:38281, your server host should be able to tell you this.

3. For the `PlayerName` field under `AP Settings`, enter your "name" field from the yaml, or website config.

4. For the `Password` field under `AP Settings`, enter the server password if one exists, otherwise leave blank.

5. Click The `Save` button then hit `Save & Play` to launch the game. On Linux, launch Sonic Adventure 2 from Steam directly rather than using `Save & Play`.

6. Create a new save to connect to the MultiWorld game. A "Connected to Archipelago" message will appear if you sucessfully connect. If you close the game during play, you can reconnect to the MultiWorld game by selecting the same save file slot.

## Additional Options

Some additional settings related to the Archipelago messages in game can be adjusted in the SAModManager if you select `Configure Mod` on the SA2B_Archipelago mod. This settings will be under a `General Settings` tab.
	
- Message Display Count: This is the maximum number of Archipelago messages that can be displayed on screen at any given time.
- Message Display Duration: This dictates how long Archipelago messages are displayed on screen (in seconds).
- Message Font Size: The is the size of the font used to display the messages from Archipelago.

If you wish to use the `SADX Music` option of the Randomizer, you must own a copy of `Sonic Adventure DX` on Steam, and follow these steps:

1. Find the folder on your PC where `Sonic Adventure DX` is installed.

2. Enter the `SoundData` folder in the `Sonic Adventure DX` installation folder, and copy the `bgm` folder.

3. Paste the `bgm` folder into the `ADX` folder which exists within the `gd_PC` folder in your `SA2B_Archipelago` mod folder.

## Troubleshooting

- "The following mods didn't load correctly: SA2B_Archipelago: DLL error - The specified module could not be found."
	- Make sure the `APCpp.dll` is in the same folder as the `sonic2app.exe`. (See Installation Procedures step 6)
	
- "sonic2app.exe - Entry Point Not Found"
	- Make sure the `APCpp.dll` is up to date. Follow Installation Procedures step 6 to update the dll.

- Game is running too fast (Like Sonic).
	- Limit framerate using the mod manager:
		1. Launch `SAModManager.exe`.
		2. Select the `Game Config` tab, then select the `Patches` subtab.
		3. Check the `Lock framerate` box under the Patches section.
		4. Press the `Save` button.
	- If using an NVidia graphics card:
		1. Open the NVIDIA Control Panel.
		2. Select `Manage 3D Settings` under `3D settings` on the left.
		3. Select the `Program Settings` tab in the main window.
		4. Click the `Add` button and select `sonic2app.exe` (or browse to the exe location), then click `Add Selected Program`.
		5. Under `Specify the settings for this program:`, find the `Max Frame Rate` feature and click the Setting column for that feature.
		6. Choose the `On` radial option and in the input box next to the slide enter a value of 60 (or 59 if 60 causes the game to crash).

- Controller input is not working.
	1. Run the Launcher.exe which should be in the same folder as the your Sonic Adventure 2: Battle install.
	2. Select the `Player` tab and reselect the controller for the player 1 input method.
	3. Click the `Save settings and launch SONIC ADVENTURE 2` button. (Any mod manager settings will apply even if the game is launched this way rather than through the mod manager)
	
- Game crashes after display logos.
	- This may be caused by a high monitor refresh rate.
		- Change the monitor refresh rate to 60 Hz [Change display refresh rate on Windows] (https://support.microsoft.com/en-us/windows/change-your-display-refresh-rate-in-windows-c8ea729e-0678-015c-c415-f806f04aae5a)
	- This may also be fixed by setting Windows 7 compatibility mode on the sonic app:
		1. Right click on the sonic2app.exe and select `Properties`.
		2. Select the `Compatibility` tab.
		3. Check the `Run this program in compatility mode for:` box and select Windows 7 in the drop down.
		4. Click the `Apply` button.
		
- No resolution options in the Launcher.exe.
	- In the `Graphics device` dropdown, select the device and display you plan to run the game on. The `Resolution` dropdown should populate once a graphics device is selected.
	
- No music is playing in the game.
	- If you enabled an `SADX Music` option, then most likely the music data was not copied properly into the mod folder (See Additional Options for instructions).
	
- Mission 1 is missing a texture in the stage select UI.
	- Most likely another mod is conflicting and overwriting the texture pack. It is recommeded to have the SA2B Archipelago mod load last in the mod manager.

## Save File Safeguard (Advanced Option)

The mod contains a save file safeguard which associates a savefile to a specific Archipelago seed. By default, save files can only connect to Archipelago servers that match their seed. The safeguard can be disabled in the mod config.ini by setting `IgnoreFileSafety` to true. This is NOT recommended for the standard user as it will allow any save file to connect and send items to the Archipelago server.
