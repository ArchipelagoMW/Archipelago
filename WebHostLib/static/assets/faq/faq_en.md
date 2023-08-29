# Frequently Asked Questions

## What is Archipelago?

Archipelago is a multi-game, multi-world randomizer for a variety of supported games. But what does that mean? 
Let's break down all the parts that make up Archipelago.

### What is a randomizer?

A randomizer is a modification of a video game which reorganizes the items required to progress through the game. A
typical play-through of a game might consist of using item A to unlock item B, which then allows you to collect item C, 
and so forth. In a randomized game, you instead might find item C, then A, then B.

This transforms games from a linear experience into a puzzle, presenting players with a new challenge each time they
play a randomized game. Putting items in non-standard locations can require the player to think about the game world and
the items they encounter in new and interesting ways.

### What is a multi-world?

While a randomizer shuffles a game, a multi-world randomizer shuffles that game for multiple players. For example, in a
two player multi-world, players A and B each get their own randomized version of a game, called a world. In each player's
game, they may find items which belong to the other player. If player A finds an item which belongs to player B, the
item will be sent to player B's world over the internet.

### What does multi-game mean?

While a multi-world game traditionally requires all players to be playing the same game, a multi-game multi-world allows
players to randomize any of a number of supported games, and send items between them. This allows players of different
games to interact with one another in a single multiplayer environment.

This creates a cooperative experience during multi-world games, requiring players to rely upon each other to complete
their game.

### Archipelago as a whole
In short, Archipelago is cross-game randomizer that allows multiple people playing different games to experience a
unified multiplayer randomizer experience. This means that you and your friends can play the games you love the most,
helping each other piece together the randomizer puzzle. Archipelago is more powerful than most randomizer environments
by allowing any combination of different games with different settings to seamlessly interact with each other.


## Can I generate a single-player game with Archipelago?

Yes! All our supported games can be generated as single-player experiences. You can either generate them online through
our website, or if you download the Archipelago software, generate and play your single-player game without the need of 
an internet connection.

## How do I get started?

If you are ready to start randomizing games, or want to start playing your favorite randomizer with others, please join
our discord server at the [Archipelago Discord](https://discord.gg/8Z65BR2). There are always people ready to answer
any questions you might have.

If you feel confident in your ability to set up software and read through guides, you can also look at the 
[list of supported games](/games) to determine which game you might want to randomize and determine how to modify your
specific game for Archipelago randomization.

*Note: Most games require an Archipelago client in order to connect to servers. To learn more about setting up the 
client, follow the guides for [Windows](/tutorial/Archipelago/setup/en) and [Mac](/tutorial/Archipelago/mac/en) 
installation.*

## What happens if an item is placed somewhere it is impossible to get?

The randomizer has many strict sets of rules it must follow when generating a game. One of the functions of these rules
is to ensure items necessary to complete the game will be accessible to the player. Many games also have a subset of
rules allowing certain items to be placed in normally unreachable locations, provided the player has indicated they are
comfortable exploiting certain glitches in the game. Therefore, the game will always be able to be completed under the
player's rules determined at generation.

## What happens if a person has to leave early?

The answer to this question depends on the style of game that you are playing. Games can largely be split up into
**Synchronous** and **Asynchronous** games. Synchronous games involved all players simultaneously playing their games,
with the intent of completing them in one sitting. Asynchronous games, on the other hand, do not require players to be
online at the same time, and can be completed over the course of multiple days.

### Asynchronous
If you are playing an Asynchronous game, then a player can safely disconnect without losing any progress any of the 
games. All items sent out through the multi-world persist independently of a player being connected to the 
Archipelago servers.

### Synchronous
When playing a Synchronous game, if a player must leave early, they can use Archipelago's release system. When a player 
releases their game, all the items their game are sent out automatically, so other players can continue to play without
worrying about if their items are in the absent player's games.

## What are some common terms I should know?

Since randomizers and multi-world randomizers have been around for a while, there are quite a few common terms
that are used by the communities surrounding them. For terms that are relevant to Archipelago and its specific systems,
please see the [Glossary](/glossary/en).

## I want to add a game to the Archipelago randomizer. How do I do that?

The best way to get started is to take a look at our code on GitHub
at [Archipelago GitHub Page](https://github.com/ArchipelagoMW/Archipelago).

There you will find examples of games in the worlds folder
at [/worlds Folder in Archipelago Code](https://github.com/ArchipelagoMW/Archipelago/tree/main/worlds).

You may also find developer documentation in the docs folder
at [/docs Folder in Archipelago Code](https://github.com/ArchipelagoMW/Archipelago/tree/main/docs).

If you have more questions, feel free to ask in the **#archipelago-dev** channel on our Discord.
