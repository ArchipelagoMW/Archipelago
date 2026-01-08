# Final Fantasy Tactics Advance

## Setup:
Generate on source https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/running%20from%20source.md
Open patch file (apffta) with the launcher. US Rom is required. 
Bizhawk client should launch then you connect to the server. 

## Things to know:
Currently judges and laws are disabled until I can figure out how to stop them from preventing item rewards which are the main checks.
You can discard mission items right now, please do not do that. There should be enough space for all of them. 
This is still early in development, be careful when throwing it in some long async with 31 mission gates. Although it should be fully beatable.
All blue mages have learn no matter the settings. 

## What is randomized?:
Starting unit job, race, amount of mastered abilities, enemies, mission order. 
From other players you can receive weapons, equipment, and mission items all depending on settings. 

## What are the locations?
Currently, it is just encounter mission rewards. Two rewards for every mission. There can be up to 28 mission gates which is 124 missions. 

## What is the goal?
There are mission gates with four missions each. One of the missions requires a mission item which will
be the one that unlocks the next mission gate. The goal is to unlock the final mission which is Royal Valley or
Decision Time based on settings. This mission is unlocked after clearing every mission gate.
There is also a setting to have a gauntlet of the totema missions which is added
alongside the mission gates and clearing the gauntlet will instead unlock the final mission. 

## Basepatch changes:
Max level raised to 99
Various cutscenes skipped
Mission item rewards hidden with ? bags
Tutorial and beginning sequence skipped
All missions cost 0 and reward the same amount of gil and AP 
All map tokens are unlocked by default

## Known issues:
Pausing in a battle on a Jagd area causes the game to freeze. Same with certain missions like Decision Time.
Receiving an item will currently always look like two items even if it is just one. The second will be blank though. Should still receive
the item though.

## Credits:
Leonarth - Made the engine hacks (no judges, quick start, animation hacks) and a lot of documentation on FFTA hacking. https://github.com/LeonarthCG/FFTA_Engine_Hacks Used with permission.
Darthatron - Made various FFTA tools and documentation. Used their tools a lot when debugging. 
FGKeiji and TojiKitten - Made the FFTA randomizer I referenced quite a bit. https://github.com/TojiKitten/FFTA-randomizer Used with permission. 
Rurusachi - Assistance with apworld and Rom programming
Zunawe - Made the bizhawk client and I used a lot of Emerald code as a reference for the apworld. 
Pilicious - Helped with ideas for the randomizer. 
Silvris - Created the patch process that fixed FFTA's patching issues. 
