# Kingdom Hearts Birth by Sleep Setup Guide

### How to play:

BEFORE MODDING, PLEASE INSTALL AND RUN KHBBS AT LEAST ONCE.

    Install OpenKH and the Lua Backend.

1. Download the latest release of OpenKH here: https://github.com/OpenKH/OpenKh/releases/tag/latest
    Extract the files to a directory of your choosing.
    Open OpenKh.Tools.ModsManager.exe and run first time set up.
    When prompted for game edition, choose PC, choose which platform you are playing on (Steam or EGS), navigate to your KH I.5 + II.5 installation folder in the path box, then click "Next"
    When prompted, install Panacea, then click "Next"
    When prompted, check KHBBS plus any other AP game you play (KH2) and click "Install and configure Lua backend", then click "Next".
    Extracting game data for KHBBS is unnecessary, but you may want to extract data for KH2 if you plan on playing KH2 AP.
    Click "Finish"

2. Open "OpenKh.Tools.ModsManager.exe"
3. Click the drop down menu at the top-right and choose "Birth by Sleep"
4. Click Mods>Install a New Mod
5. In "Add a new mod from GitHub" paste "gaithern/KH-BBS-AP-LUA"
6. Click Install
7. Navigate to Mod Loader and click "Build Only"
8. Place your khbbs.apworld file in your worlds folder (usually /lib/worlds/)
9. Run ArchipelagoLauncher.exe
10. Click "Generate Template Settings". This will open file explorer
11. Find "Kingdom Hearts Birth by Sleep.yaml" and copy it to /Players/ (create this folder if it does not exist)
12. Open the YAML file and change the line that says "name: Player{number}" to your desired player name.
13. Adjust the settings in the YAML to your liking
14. Run ArchipelagoGenerate.exe
15. Take the newly created AP_XXX.zip file in /output/ in upload it here: https://archipelago.gg/uploads
16. Open ArchipelagoLauncher.exe
17. Click "KHBBS Client" and connect to your server hosted on archipelago.gg
18. From the zip file mentioned above, retrieve the seed zip file (example: AP-95162914732603780136-P1-Player1_0.5.0.zip)
19. In OpenKH, click the green plus to add a mod, then click "Select and install Mod Archive or Lua Script"
20. Navigate to and select your seed zip.
21. With both the companion and the seed checked, click "Mod Loader", then "Build and Run"
22. Play!


## Hosting a MultiWorld game

The recommended way to host a game is to use our hosting service. The process is relatively simple:

1. Collect config files from your players.
2. Create a zip file containing your players' config files.
3. Upload that zip file to the Generate page above.
    - Generate page: [WebHost Seed Generation Page](/generate)
4. Wait a moment while the seed is generated.
5. When the seed is generated, you will be redirected to a "Seed Info" page.
6. Click "Create New Room". This will take you to the server page. Provide the link to this page to your players, so
   they may download their patch files from there.
7. Note that a link to a MultiWorld Tracker is at the top of the room page. The tracker shows the progress of all
   players in the game. Any observers may also be given the link to this page.
8. Once all players have joined, you may begin playing.
