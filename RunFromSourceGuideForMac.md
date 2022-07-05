# Prerequisite Software
Here is a list of software to install and source code to download.
1. [Python](https://www.python.org/downloads/macos/), 3.8 or newer is necessary.
2. [Xcode](https://apps.apple.com/us/app/xcode/id497799835)
3. [Archipelago Source](https://github.com/ArchipelagoMW/Archipelago/archive/refs/heads/main.zip), this will download the source code in a zipped format.
4. [SNI](https://github.com/alttpo/sni/releases), be sure to select the asset with 'darwin' in the name. This one is only necessary for SNES games (A Link to the Past, Super Metroid, and SMZ3 at time of writing).
5. An Emulator of your choosing for games that need an emulator. For SNES games, I recommend [RetroArch](https://www.retroarch.com/?page=platforms), entirely because it was the easiest for me to setup on Mac.
# Steps to Run the Clients
1. Click on the Archipelago source code zip file to extract the files to an Archipelago directory.
2. Move this Archipelago directory out of your downloads directory.
3. Open terminal and navigate to your archipelago directory.
5. If your game doesn't have a patch file, run the command `python3 'client of choice'.py`.
6. If your game does have a patch file, move the base rom to the Archipelago directory and run the command `python3 'client of choice'.py 'path to patch file'` with the filename extension for the patch file (apsm, aplttp, apsmz3) included.
7. Your client should now be running and rom created (where applicable).
## Additional Steps for SNES games
1. Follow the instructions to set up your emulator [here](https://archipelago.gg/tutorial/A%20Link%20to%20the%20Past/multiworld/en)
2. Click on the SNI tar.gz download to extract the files to an SNI directory and move the SNI directory out of the downloads directory.
3. Open up the SNI directory and run the SNI executable file. 
4. Now that SNI, the client, and the emulator are all running, you should be good to go.
