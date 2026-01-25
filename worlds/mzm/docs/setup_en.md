# Setup Guide for Metroid Zero Mission: Archipelago

# Download and installation
First, download and install the latest BizHawk emulator: https://tasvideos.org/Bizhawk/ReleaseHistory
(mGBA also works: https://discord.com/channels/731205301247803413/1192236871468711966/1193963132377374762)

Download the latest .apworld from:
https://github.com/lilDavid/Archipelago-Metroid-Zero-Mission/releases
Type `&apworld` anywhere in this server for instructions.
Open your .apmzm patch with the Archipelago launcher, which should start BizHawk with your patched rom and automatically open the BizHawk client and the Lua connector. Then just put in your server address in the BizHawk client and you should be good to go!

# Poptracker pack (by Ladybunne)
https://github.com/ladybunne/MetroidZeroMission_PopTrackerPack/releases

# Notes/Changes made for the randomizer
* You can warp back to the starting room from anywhere by pressing L while on the map screen. **Note that doing this resets your progress to your last save**. Logic accounts for this when taking potential one-way paths. If you do this during the ZSS segment, Mother Brain gets unkilled.
* Unknown Item blocks are activated by collecting the item on the appropriate Chozo statue nearby, **not** by finding the corresponding Unknown Item. I.E. collecting the item at Crateria Unknown Item Statue activates the Unknown Item blocks there, not having Plasma Beam.
* Beams and "Misc" upgrades can be toggled on or off in the equipment screen of the pause menu. This can be useful if you need to freeze an enemy but your beam does too much damage, or if Screw Attack is breaking blocks you want to land on.
* Some of the layout patches have logical implications. Notably, you can go "backwards" through Crateria if you have crateria_water_speedway enabled along with a way to fly up from the landing site. This patch is on by default, but taking this backwards path without the vanilla requirements is only logical on Normal level logic or higher.

## Next post has known issues.
