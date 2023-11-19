# Zillion

Zillion is a metroidvania-style game released in 1987 for the 8-bit Sega Master System.

It's based on the anime Zillion (赤い光弾ジリオン, Akai Koudan Zillion).

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and export a config file.

## What changes are made to this game?

The way the original game lets the player choose who to level up has a few drawbacks in a multiworld randomizer:
 - Possible softlock from making bad choices (example: nobody has jump 3 when it's required)
 - In multiworld, you won't be able to choose because you won't know it's coming beforehand.

So this randomizer uses a new level-up system:
 - Everyone levels up together (even if they're not rescued yet).
 - You can choose how many opa-opas are required for a level up.
 - You can set a max level from 1 to 8.
 - The currently active character is still the only one that gets the health refill.

---

You can set these options to choose when characters will be able to attain certain jump levels:

```
jump levels

vanilla         balanced        low             restrictive

jj  ap  ch      jj  ap  ch      jj  ap  ch      jj  ap  ch
2   3   1       1   2   1       1   1   1       1   1   1
2   3   1       2   2   1       1   2   1       1   1   1
2   3   1       2   3   1       2   2   1       1   2   1
2   3   1       2   3   2       2   3   1       1   2   1
3   3   2       3   3   2       2   3   2       2   2   1
3   3   2       3   3   2       3   3   2       2   2   1
3   3   3       3   3   3       3   3   2       2   3   1
3   3   3       3   3   3       3   3   3       2   3   2
```

Note that in "restrictive" mode, Apple is the only one that can get jump level 3.

---

You can set these options to choose when characters will be able to attain certain Zillion power (gun) levels:

```
zillion power

vanilla         balanced        low             restrictive

jj  ap  ch      jj  ap  ch      jj  ap  ch      jj  ap  ch
1   1   3       1   1   2       1   1   1       1   1   1
2   2   3       2   1   2       1   1   2       1   1   2
3   3   3       2   2   3       2   1   2       2   1   2
                3   2   3       2   1   3       2   1   3
                3   3   3       2   2   3       2   2   3
                                3   2   3
                                3   3   3
```

Note that in "restrictive" mode, Champ is the only one that can get Zillion power level 3.

## What does another world's item look like in Zillion?

Canisters retain their original appearance, so you won't know if an item belongs to another player until you collect it.

When you collect an item, you see the name of the player it goes to. You can see in the client log what item was
collected.

## When the player receives an item, what happens?

The item collect sound is played. You can see in the client log what item was received.

## Unique Local Commands

The following commands are only available when using the ZillionClient to play with Archipelago.

- `/sms` Tell the client that Zillion is running in RetroArch.
- `/map` Toggle view of the map tracker.
