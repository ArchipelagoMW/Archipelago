### How To Play

BEFORE MODDING, PLEASE INSTALL AND RUN KHDDD AT LEAST ONCE.

1. Install OpenKH and Lua Backend
- Download the latest release of OpenKH here: https://github.com/OpenKH/OpenKh/releases/tag/latest
- Extract the files to a directory of your choosing.
- Open OpenKh.Tools.ModsManager.exe and run first time set up.
- When prompted for game edition, choose PC, choose which platform you are playing on (**Only Steam is supported right now**), navigate to your KH 2.8 installation folder in the path box, then click "Next".
- When prompted, install Panacea. Make sure you have the Kingdom Hearts 2.8 collection selected, then click "Next".
- When prompted, check KH3D and click "Install and Configure Lua Backend" then click "Next".
- Extracting game data for KHDDD is unnecessary.
- Click "Finish".

2. Open "OpenKH.Tools.ModsManager.exe
3. Click the drop down menu at the top-right and choose "Dream Drop Distance"
4. Click Mods>Install a New Mod
5. In "Add a new mod from GitHub", paste "LuxMake/KHDDD-AP"
6. Click Install
7. Navigate to Mod Loader and click "Build Only"
8. Double-click the "khddd.apworld" file to install it to your custom_worlds folder
9. Run ArchipelagoLauncher.exe
10. Click "Generate Template Options". This will open the file explorer
11. Find "Kingdom Hearts Dream Drop Distance.yaml" and copy it to /Players/
12. Open the YAML file and change the line that says "name: Player{number}" to your desired player name
13. Adjust the settings in the YAML to your liking
14. Run ArchipelagoGenerate.exe or click "Open" under the Generate option in the Archipelago Launcher
15. Take the newly created AP_XXX.zip file in /output/ in upload it here: https://archipelago.gg/uploads
16. Open ArchipelagoLauncher.exe
17. Click "KHDDD Client". Once the client launches, you will see a message in the console stating "Searching for KHDDD Client...Please load your save file before connecting."
18. In OpenKH, click "Mod Loader", then "Build and Run"
19. Once the game launches, start a New Game (or load a save file if applicable)
20. After starting the game, a new message will appear in the Archipelago client stating "KHDDD Game Client Found". Once this message appears, you can connect to the server hosted on archipelago.gg
21. Play

### Additional Notes
- The save file in-game should be loaded before attempting to connect to the server in the AP client. Otherwise, you will get an error message when pressing "Connect".
- Conversely, the game will stutter trying to find the AP client if the save file is loaded before the AP client is launched. So the ideal setup is to: Launch AP client -> Load save file -> Connect to AP server. Future updates will aim to streamline this process.
- If either the game or the AP client have to be closed for any reason, it is recommended to completely close out of both clients to ensure stability.
