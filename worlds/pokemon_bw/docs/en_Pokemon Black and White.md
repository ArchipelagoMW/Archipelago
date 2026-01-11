# Pokémon Black and White

## What is this game?

Pokémon Black and White are the introduction to the fifth generation of the Pokémon franchise. 
Travel through the Unova region, catch a variety of brand-new Pokémon you have never seen before, 
collect the eight gym badges, fight Team Plasma, who claim to be the saviors of all the Pokémon, 
and become the champion of the region.
These games present themselves in 2.5D graphics, 
while still using the well-known grid-based movement mechanics and battle UI. 

## FAQ (kinda)

- ***How do I set up this game?***
  <br>If you're new to setting up a custom apworld, type `&apworld` into the game's thread for more information.
  <br>Other than that, follow the [setup guide for this game.](setup_en.md)
- ***Where is the options page?***
  <br>As this game is not (yet) merged into main, type `&template` into the game's thread for more information.
- ***Is there a tracker?***
  <br>You can use the Universal Tracker, which is fully compatible and includes a map tracker. See the 
      `#universal-tracker` channel on the Discord server for more information.
- ***Can I use UPR to randomize other parts of the rom?***
  <br>No. It will mess up logic due to the randomizer not knowing in what way the rom was modified 
      and break the game before even getting to choose your starter.
- ***Can I use PKHex to edit my save file?***
  <br>Yes! No changes have been made to the save file structure that would break compatibility.
  <br>However, trying to edit items will result in automatically deleting key items that are not obtainable in vanilla. 
      You can prevent this by opening PKHeX in `PKHaX` mode (see [this article](
      https://projectpokemon.org/home/tutorials/save-editing/using-pkhex/how-to-use-pkhax-mode-with-pkhex-r78/)
      for more information).
- ***Help, I lost important items (due to PKHex, game crashes, ...)!***
  <br>Just open the game and connect to the server again. Important items such as key items, badges, etc. will get 
      automatically re-added if collected but missing in your save file.
- ***I want to contribute to development, how can I do that?***
  <br>First of all, propose your ideas/changes/... in the game's thread, so we can talk about things beforehand.
  <br>The fork of this implementation is found at https://github.com/SparkyDaDoggo/Archipelago/tree/main.
- ***This game info page looks quite different compared to those of other games...***
  <br>This game has not been merged into main yet, and people tend to get confused by "not working" option
      pages (which will only work once merged into main).
  <br>Once this game does get merged into main, this info page and the setup page will be changed 
      to the default structure.

## Other useful or interesting pages

- [Rom changes](rom%20changes.md)
- [Changelog](changelog.md)
- [Credits](credits.md)
- [Features roadmap](roadmap.md)
- [Encounter Plando guide](encounter%20plando.md)

## Known bugs (might be outdated)

- Using dig while having season control enabled crashes the game
