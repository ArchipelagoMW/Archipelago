# Final Fantasy Tactics Advance Setup Guide

1. Relevant files can be found here (or check the pins): https://github.com/spicynun/Archipelago/releases (expand the "assets" section for the latest version)
2. Put ffta.apworld in lib/worlds folder
3. Download your .apffta file from the rooms page for the current seed
4. In the Archipelago Launcher, click on Open Patch and select that .apffta file from the previous step
4. Doing this should create a AP_<...>.gba file next to the .apffta file, open up the Archipelago BizHawk Client, and load the rom in BizHawk for you (if you set gba files to open in BizHawk). If not, open the GBA file in BizHawk.
5. If BizHawk was opened automatically for you, you should see a Lua Console with "connector_bizhawk_generic" loaded. If not, open the Lua Console in BizHawk (Config->Lua Console), click on the folder icon, and load connector_bizhawk_generic.lua (probably located at C:\ProgramData\Archipelago\data\lua\connector_bizhawk_generic.lua). DO NOT LOAD BY GOING TO FILE->OPEN SESSION, that does not do the same thing!
6. The lua console should eventually say "Client connected", and the Archipelago BizHawk Client should say "Connected to BizHawk" and "Running handler for Final Fantasy Tactics Advance".
7. Connect to your Archipelago server and port in the Archipelago BizHawk Client.
8. When you stop playing and want to continue, the .apffta should now be openable by double clicking on it which should open everything for you again. If not, choose to "always open" with ArchipelagoLauncher.exe and it should stick