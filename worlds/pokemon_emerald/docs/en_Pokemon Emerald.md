# Pokémon Emerald

## Where is the options page?

You can read through all the options and generate a YAML [here](../player-options).

## What does randomization do to this game?

This randomizer handles both item randomization and pokémon randomization. Badges, HMs, gifts from NPCs, and items on
the ground can all be randomized. There are also many options for randomizing wild pokémon, starters, opponent pokémon,
abilities, types, etc… You can even change a percentage of single battles into double battles. Check the
[options page](../player-options) for a more comprehensive list of what can be changed.

## What items and locations get randomized?

The most interesting items that can be added to the item pool are badges and HMs, which most affect what locations you
can access. Key items like the Devon Scope or Mach Bike can also be randomized, as well as the many Potions, Revives,
TMs, and other items that you can find on the ground or receive as gifts.

## What other changes are made to the game?

There are many quality of life improvements meant to speed up the game a little and improve the experience of playing a
randomizer. Here are some of the more important ones:

- Shoal Cave switches between high tide and low tide every time you re-enter
- Bag space is greatly expanded (you're all but guaranteed to never need to store items in the PC)
- Trade evolutions have been changed to level or item evolutions
- You can have both bikes simultaneously
- You can run or bike (almost) anywhere
- The Wally catching tutorial is skipped
- All text is instant and, with an option, can be automatically progressed by holding A
- When a Repel runs out, you will be prompted to use another
- [Many more minor improvements…](/tutorial/Pokemon%20Emerald/rom_changes/en)

## Where is my starting inventory?

Except for badges, your starting inventory will be in the PC.

## What does another world's item look like in Pokémon Emerald?

When you find an item that is not your own, you will see the item's name and its owner while the item received jingle
plays.

## When the player receives an item, what happens?

You will only receive items while in the overworld and not during battles. Depending on your `Receive Item Messages`
option, the received item will either be silently added to your bag or you will be shown a text box with the item's
name and the item will be added to your bag while a fanfare plays.

## Can I play offline?

Yes, the client and connector are only necessary for sending and receiving items. If you're playing a solo game, you
don't need to play online unless you want the rest of Archipelago's functionality (like hints and auto-tracking). If
you're playing a multiworld game, the client will sync your game with the server the next time you connect.

## Will battle mechanics be updated?

Unfortunately, no. We don't want to force new mechanics on players who would prefer to play with the classic mechanics,
but updating would require such drastic changes to the underlying code that it would be unreasonable to toggle between
them.

## Is this randomizer compatible with other mods?

No, other mods cannot be applied. It would be impossible to generalize this implementation's changes in a way that is
compatible with any other mod or romhack. Romhacks could be added as their own games, but they would have to be
implemented separately. Check out [Archipelago's Discord server](https://discord.gg/8Z65BR2) if you want to make a
suggestion or contribute.

## Can I use tools like the Universal Pokémon Randomizer?

No, tools like UPR expect data to be in certain locations and in a certain format, but this randomizer has to shift it
around. Using tools to try to modify the game would only corrupt the ROM.

We realize this means breaking from established habits when it comes to randomizing Pokémon games, but this randomizer
would be many times more complex to develop if it were constrained by something like UPR.

### There are two possible exceptions

#### PKHex

You may be able to extract pokémon from your save using PKHeX, but this isn't a guarantee, and we make no effort to keep
our saves compatible with PKHeX. Box and party pokémon are the only aspects of your save file likely to work.

#### PokéFinder/RNG Reporter

In the spirit of randomization, Emerald's broken RNG is fixed in Archipelago. More specifically, it's reverted to work
as it did in Ruby/Sapphire. So while you can't make the assumption that the RNG is seeded at 0, you can set the battery
to dry, which will seed it in the same way that Ruby/Sapphire are seeded when the battery is dry.
