# Guide to change maximum locations in shapez

## Where do I find the settings to increase/decrease the amount of possible locations?

The maximum values of the `goal_amount` and `shapesanity_amount` are hardcoded settings that affect the datapackage. 
They are stored in a file called `options.json` inside the apworld. By changing them, you will create a custom apworld 
on your local machine.

## How to change datapackage options

This tutorial is for advanced users and can result in the software not working properly, if not read carefully. 
Proceed at your own risk.

1. Go to `<AP installation>/lib/worlds`.
2. Rename `shapez.apworld` to `shapez.zip`.
3. Open the zip file and go to `shapez/data/options.json`.
4. Edit the values in this file to your desire and save the file.
   - `max_shapesanity` cannot be lower than `4`, as this is the minimum amount to prevent FillErrors.
   - `max_shapesanity` also cannot be higher than `75800`, as this is the maximum amount of possible shapesanity names. 
     Else the multiworld generation might fail.
   - `max_levels_and_upgrades` cannot be lower than `27`, as this is the minimum amount for the `mam` goal to properly 
     work.
5. Close the zip and rename it back to `shapez.apworld`.

## Why do I have to do this manually?

For every game in Archipelago, there must be a list of all possible locations, **regardless of player options**. When 
generating a multiworld, a list of all locations of all included games will be saved in the multiworld data and sent to 
all clients. The higher the amount of possible locations, the bigger the datapackage. And having ~80000 possible 
locations at one point made the datapackage for shapez bigger than all other supported games combined. So to reduce the 
datapackage of shapez, the locations for shapesanity are named `Shapesanity 1`, `Shapesanity 2` etc. instead of their 
actual names. By creating a custom apworld, you can increase the amount of possible locations, but you will also 
increase the size of the datapackage at the same time.
