# ChecksMate Chess Randomizer Setup Guide

![A chess piece with several blurry opposing pieces in the background](https://i.imgur.com/fqng206.png)

## Required Software

- Any ChecksMate client. Currently, a modified ChessV client is supported and can be accessed via
  its [GitHub releases page](https://github.com/chesslogic/chessv/releases/latest) (latest version)
- Archipelago from the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases/latest)

## Configuring your YAML file

### What is a YAML file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

Some releases of the ChecksMate client include an example YAML file demonstrating some supported options.

### Where do I get a YAML file?

You can customize your options by visiting the [ChecksMate Player Options Page](/games/ChecksMate/player-options)

Some examples of certain outcomes are available in [this valid players file](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/checksmate/docs/checksmate-example.yaml), which can be used
to generate a multiplayer multiworld (but should instead be used for your own inspiration).

#### Material

A normal (FIDE) army has 8 points of pawns plus 31 points of pieces (12 from 4 minor pieces, 10 from 2 rooks, and 9 from
1 queen). Material isn't everything: An army of 27 pawns plus 4 Knights is considered to be extremely powerful.
Conversely, having no pawns whatsoever opens your position dramatically, allowing your pieces to make very aggressive
moves and to maintain a very high tempo.

### Generating a ChecksMate game

**ChecksMate is a short game! You might restart many times, but you should expect no more than an hour of gameplay!**

You need to start a ChecksMate client yourself, which are available from the [releases page](https://github.com/chesslogic/chessv/releases/latest).
Generally, these need to be extracted to a folder before they are run, due to a dependency on asset files and dynamic libraries.

### Connect to the MultiServer

First start ChecksMate.

Once ChecksMate is started, in the client at the top type in the spot labeled `Server` type the `IP Address` and `Port`
separated with a `:` symbol. Then input your slot name in the next box. The third box can be used for any password,
and is often left empty.

These connection settings will be saved in a simple text file for the next time you start the client. (You may safely
delete this convenience file.)

### Play the game

When the console tells you that you have joined the room, you're all set. Congratulations on successfully joining a
multiworld game!
