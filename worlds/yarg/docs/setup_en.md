# YARG Randomizer Setup Guide

This is an Archipelago implementation for the open source, plastic band rhythm game, YARG!

# Setup
1. Download the YARC Launcher from https://yarg.in/
2. Inside the YARC Launcher download "YARG Nightly" and the "YARG Official Setlist"
3. Download the YARGAPClient from https://github.com/energymaster22/YARGAPClient/releases/latest
4. Download Archipelago from https://github.com/ArchipelagoMW/Archipelago/releases/latest
5. Set up Archipelago
6. Download the YARG.apworld from https://github.com/energymaster22/YARGArchipelago/releases/latest
7. Double click yarg.apworld to install it into Archipelago
8. Select "Generate Template Options" from within Archipelago to get a default YAML
9. Edit YARG.yaml to your liking and put it in your "Players" folder (should be one folder up from the "Templates" folder the previous step opened)
10. Select "Generate" from within Archipelago
11. Host your outputed multiworld either on https://archipelago.gg/ or locally
12. Launch the YARGAPClient
13. Click "Archipelago" on the main menu to open the login screen
14. Input the host address, port and slot name and press connect! (Game ID should be left blank if not playing on a fork) (Leave blank if unsure)

# Gameplay
1. Your goal in YARG AP is to find and complete your goal song!
2. The goal song may or may not be known depending on yaml settings.
3. Go into "Quickplay"
4. All of your collected songs will appear at the top in an "AP Songs" catagory
5. Play the songs that appear there to get checks for your multiworld!
6. When you get your goal song it will appear in an "AP Goal Song" catagory along with details on what you still need.
7. Collect the rest of the YARG Gems in the multiworld to fully unlock the goal song.
7. Play that song to finish the seed!

# Current Notes
"Star Power Bonus" items grant 25% Star Power upon collection\
\
If a song does not support your current instrument, or you otherwise cannot complete the song, you can use a bot player to clear it

# Common Problems
## My songs are not loading!

+ This can be caused by a few things. First make sure that you have downloaded the setlists from the YARC launcher.

+ Sometimes YARG needs to rescan of your library, to do so, go to Settings> Songs and click "Scan songs" up at the top

+ Other times YARG forks do not find the YARC setlists automatically. This is a slightly more involved fix:

1. Open the YARC Launcher
2. Scroll all the way down the left panel
3. Click the Settings button on the bottom left
4. Note the directory under "File Management"
5. In the YARGAPClient go to Settings> Songs
6. Click "Add New Folder"
7. Click "Browse" on the new entry
8. Navigate to the folder you saw in the YARC Launcher settings
9. Within the YARC install folder selct the "Setlists" folder
10. Click "Scan Songs"
