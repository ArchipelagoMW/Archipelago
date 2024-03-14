# Frequently Asked Questions

## What is a randomizer?

A randomizer is a modification of a game which reorganizes the items required to progress through that game. A
normal play-through might require you to use item A to unlock item B, then C, and so forth. In a randomized
game, you might first find item C, then A, then B.

This transforms the game from a linear experience into a puzzle, presenting players with a new challenge each time they
play. Putting items in non-standard locations can require the player to think about the game world and the items they
encounter in new and interesting ways.

## What is a multiworld?

While a randomizer shuffles a game, a multiworld randomizer shuffles that game for multiple players. For example, in a
two player multiworld, players A and B each get their own randomized version of a game, called a world. In each
player's game, they may find items which belong to the other player. If player A finds an item which belongs to
player B, the item will be sent to player B's world over the internet. This creates a cooperative experience, requiring
players to rely upon each other to complete their game.

## What does multi-game mean?

While a multiworld game traditionally requires all players to be playing the same game, a multi-game multiworld allows
players to randomize any of the supported games, and send items between them. This allows players of different
games to interact with one another in a single multiplayer environment.  Archipelago supports multi-game multiworld.
Here is a list of our [Supported Games](https://archipelago.gg/games).

## Can I generate a single-player game with Archipelago?

Yes. All of our supported games can be generated as single-player experiences both on the website and by installing 
the Archipelago generator software. The fastest way to do this is on the website. Find the Supported Game you wish to
play, open the Settings Page, pick your settings, and click Generate Game.

## How do I get started?

We have a [Getting Started](https://archipelago.gg/tutorial/Archipelago/setup/en) guide that will help you get the
software set up. You can use that guide to learn how to generate multiworlds. There are also basic instructions for
including multiple games, and hosting multiworlds on the website for ease and convenience.

If you are ready to start randomizing games, or want to start playing your favorite randomizer with others, please join
our discord server at the [Archipelago Discord](https://discord.gg/8Z65BR2). There are always people ready to answer
any questions you might have.

## What are some common terms I should know?

As randomizers and multiworld randomizers have been around for a while now, there are quite a few common terms used
by the communities surrounding them. A list of Archipelago jargon and terms commonly used by the community can be
found in the [Glossary](/glossary/en).

## Does everyone need to be connected at the same time?

There are two different play-styles that are common for Archipelago multiworld sessions. These sessions can either
be considered synchronous (or "sync"), where everyone connects and plays at the same time, or asynchronous (or "async"),
where players connect and play at their own pace. The setup for both is identical. The difference in play-style is how
you and your friends choose to organize and play your multiworld. Most groups decide on the format before creating
their multiworld.

If a player must leave early, they can use Archipelago's release system. When a player releases their game, all items
in that game belonging to other players are sent out automatically. This allows other players to continue to play
uninterrupted. Here is a list of all of our [Server Commands](https://archipelago.gg/tutorial/Archipelago/commands/en).

## What happens if an item is placed somewhere it is impossible to get?

The randomizer has many strict sets of rules it must follow when generating a game. One of the functions of these rules
is to ensure items necessary to complete the game will be accessible to the player. Many games also have a subset of
rules allowing certain items to be placed in normally unreachable locations, provided the player has indicated they are
comfortable exploiting certain glitches in the game.

## I want to add a game to the Archipelago randomizer. How do I do that?

The best way to get started is to take a look at our code on GitHub:  
[Archipelago GitHub Page](https://github.com/ArchipelagoMW/Archipelago).

There, you will find examples of games in the `worlds` folder:  
[/worlds Folder in Archipelago Code](https://github.com/ArchipelagoMW/Archipelago/tree/main/worlds).

You may also find developer documentation in the `docs` folder:  
[/docs Folder in Archipelago Code](https://github.com/ArchipelagoMW/Archipelago/tree/main/docs).

If you have more questions, feel free to ask in the **#archipelago-dev** channel on our Discord.
