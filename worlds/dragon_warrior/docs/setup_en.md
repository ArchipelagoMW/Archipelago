# Dragon Warrior Setup Guide 

## How do I generate a multiworld with Dragon Warrior?

You can install the dragon_warrior.apworld file in the Releases tab to your AP Launcher to generate a YAML, as well as a multiworld. When hosted on the AP website, the DW player should be able to simply hit the `Download Patch File...` button to receive their `.apdw` file.

## How do I join a multiworld with Dragon Warrior?

When hosted on the AP website, you can hit the `Download Patch File...` button to get your `.apdw` file, otherwise your host should send it to you. Ensure you have the Archipelago Launcher and Bizhawk installed, and double-click the `.apdw` patch file. This will open up the client and emulator with the patched ROM file.

## What does randomization do to this game?

By default, chests and their contents are randomized into the multiworld. There are also two checks associated with rescuing and returning Princess Gwaelin. Additional -sanity options exist to randomize search spots, level-ups,equipment shops, and monsters. Magic Key Vendors no longer sell them, instead, a single unbreakable Magic Key is shuffled into the multiworld as a progression item.

## What is the goal of Dragon Warrior when randomized?

In order to beat the game, you must collect the Staff of Rain, Stones of Sunlight, and Erdrick's Token in order to receive the Rainbow Drop and reach Charlock Castle. The completion condition is to defeat the Dragonlord. Erdrick's Token is in it's vanilla spot if `Searchsanity` is disabled.

## What items and locations get shuffled?

Quest items including the Magic Key get shuffled, as well as many filler items like herbs and gold. If `Shopsanity` is enabled, Progressive Equipment Items are also added to the progression item pool.

## Which items can be in another player's world?

Any shuffled item can be in other players' worlds.

## What does another world's item look like in Dragon Warrior?

All items appear in chests and search spots as "APItem". Levelups, Purchases, and Monster Kills do not have an explicit appearence and simply send a check out when achieved.

## When the player receives an item, what happens?

Currently, items are silently added to the player's inventory. If the player's inventory is full, a quest item will drop a filler item (Similar to the logic for Gwaelin's Love).
