# Autopelago

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What is this game?

Autopelago is a game that plays itself, built specifically for Archipelago. It's meant to help practice playing the game
solo in a more realistic setting, with other players in the world that need items from the multiworld to achieve their
goal — and vice versa.

The "player" is represented by a rat that moves around the map from location to location, trying to complete the task at
that location. When it succeeds, it sends out the check and moves onto the next one.

Most locations are "fillers" to bulk out the map without any special rules by themselves, but then several locations are
"landmarks" that can only be completed if you've collected certain items.

## What do items do?

When you collect a progression item (other than a Pack Rat or the Rat Pack), then its icon in the panel on the left will
light up to show this. *Pack Rat and the Rat Pack will just increase your rat count by 1 or 5, respectively.*

When you collect an item with buffs / traps on it (as enabled / disabled in your options), then the corresponding meter
or indicator will light up accordingly — though a few have upper limits on how high they can go.

When you collect an item without any buffs / traps on it, then nothing happens.

## What can I do in the game?

The rat *primarily* runs around by itself, but there are some *limited* ways that you can influence what it does:

1. In the game's chat, **any player** can type `@RatName go LOCATION`, where `RatName` is the rat's slot name (or alias,
   if it's unique), and `LOCATION` is the name of a location on the map. *`@RatName stop LOCATION` will cancel such a
   request, in case you changed your mind for whatever reason*.
2. In the game window itself, you can click on a specific location, and the rat will "hyper-focus" that location,
   overriding everything else except the "Startled" debuff.
3. Also in the game window, you can click on an item in the left panel to request a hint, after a confirmation prompt.

You can also click the rat icon to toggle on / off a dashed line showing its exact intended path to its current target,
and you can hover over any location (or the rat) to see some basic information about it in a tooltip.

*For everything above that says "click", you can also tab over to it and press Enter to do the same, and their tooltips
also show up as you tab over to them.*

## How does the rat decide where to go?

It checks these rules in order and chooses the first one that applies:

1. If it's startled, then it will run towards the beginning.
2. If it has a "hyper-focus" location, then it will run towards that.
3. If it has everything that it needs to complete the goal, then it will run towards the end.
4. If a "Smart" or "Conspiratorial" item has given the rat its own idea, then it will run towards that.
5. If any players have told it to go somewhere that it can reach, then it will run towards the earliest requested one.
6. If it can reach any unchecked location, then it will run towards the nearest one.
7. Otherwise, it will stay where it is.
