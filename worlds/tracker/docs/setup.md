# Tracker Prerequisites

1) Have Archipelago installed with the generator enabled
2) Have the relevant player .yaml files in the Players folder in the AP install directory

# Install

1) Download the most recent version of the tracker to lib/worlds in your AP install directory  
     This can be gotten from https://github.com/FarisTheAncient/Archipelago/releases

# Running the tracker

This part depends on if you have a game with tracker integration (like [Minit](https://github.com/qwint/APMinit/releases) or [AP Manual](https://github.com/ManualForArchipelago/Manual/releases))

if you do, you can just launch that game's client and if you have the tracker installed it will just work™

if you don't, you can launch the ArchipelagoLauncher and click the "Universal Tracker" button,  
Then connect like you would with a text client and from there you can use the tracker as both a tracker AND as a normal text client

# Known "Gaps" in UT

* Currently the Universal Tracker determines what's in logic or not by creating an internal multiworld, and syncing it up with the "real" one on the server, however this has a single gap that is difficult to resolve without help from the indiviual world's devolopers  
* If you have any form of "randomness" in logic (e.g. random starting location, random goals, random weights, entrance randomizer etc.) then the internal multiworld will be desynced from the "real" one, and won't give you correct logic  
* Randomness in the YAML can be resolved by using the `player_files_path` option in the host.yaml file to set an alternate path to a players folder, where you modify the yamls to have the options that got rolled by the original generation  

# Errors

if you get "Generation Failure" it means that something broke when the tracker setup the internal World, and usually points to the yamls not being correct  
if you don't, but there's nothing in the Tracker tab, or worse it's not making sense what it thinks is in logic (saying you can get to places that you *for sure* don't have access to) then it points to a game with non-deterministic logic, and might not be a supported game

in either case, if you ping Faris with the yaml in the Universal Tracker channel in the AP discord (and a link to the apworld if it's not in core) and i'll take a look at exactly what's going wrong

# Host.yaml options

* `player_files_path` : Sets a different location for the players folder, this is useful as fewer yamls that UT tries to generate means faster launch times, and can also allow for un-randomized yamls without editing the original file
* `include_region_name` : Chooses if the tracker output will include the region name, for some games this can be useful, but for others it just adds duplicate information or worse *missleading* information to the user
* `include_location_name` : Chooses if the tracker output will include the location name... this is likely less useful for users, but can be useful for devs trying to debug logic issues, and it will display the regions you can access regardless of location logic
* `hide_excluded_locations` : Chooses if the tracker output will include excluded locations, usually not an issue but for some games/yaml settings the number of excluded locations can be considerable so this reduces visual clutter
