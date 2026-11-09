# Paquerette Down The Bunburrows

## Quick Links

- [Game Page]()
- [Setup Guide](../../../tutorial/Paquerette%20Down%20The%20Bunburrows/setup_en)
- [Options Page](../player-options)
- [APWorld Repository](https://github.com/SergeAzel/Archipelago_PDTB/releases)
- [Client Mod - Thunderstore](https://thunderstore.io/c/paquerette-down-the-bunburrows/p/BNYSmod/Bunject_Archipelago/)
- [Client Repository](https://github.com/SergeAzel/Bunject/releases/)
- [AI Usage Disclosure](https://github.com/SergeAzel/Archipelago_PDTB/blob/main/worlds/paquerette_down_the_bunburrows/ai.md)


## Compatibility

This version of the APWorld targets **Paquerette Down The Bunburrows v1.1.4** and the
**Bunject Archipelago client mod v1.3.0**. See the [Setup Guide](../../../tutorial/Paquerette%20Down%20The%20Bunburrows/setup_en) for details.


## What kind of game is this?

Paquerette Down The Bunburrows is a sokoban-inspired top down puzzle game, about collecting bunnies.
A *sokobun* if you will.

The player, as Paquerette, will chase bunnies.  The bunnies will try to flee.

The game will teach you some of the basics starting out, but players will be expected to pay attention
and learn various bunny behaviors.


## Where do I get the Archipelago Client for this game?

See the [Setup Guide](../../../tutorial/Paquerette%20Down%20The%20Bunburrows/setup_en)!



## What should I expect from playing it for Archipelago?

**WARNING: Playing this game for Archipelago makes things even more difficult**  
This game is considered a challenging puzzle experience as is.

This Archipelago World is best suited for players with experience in the game already.

New players are recommended to become familiar with the base game first.
Determined new players are **strongly advised** to use the following options:

- Victory Condition: Credits
- Home Captures Only: False
- Expert Routing: False
- Unlock Computer: True
- Unlock Map: True


## I'm still in, what should I know about the client?

See the Setup guide for more details on installation and logging in.

Paquerette Down The Bunburrows generally gives players all the tools they need to solve any particular room, 
and players may progress as they see fit with few restrictions.

The Archipelago implementation steals Paquerette's tools.  Each toolset within a room is an Archipelago item to be unlocked.
Each bunny to capture, conversely, is an Archipelago location to check.

Unlocked rooms behave as normal in the 

Playing alone, capturing bunnies grants you various rooms tools.

While the base game generally allows you to skip puzzles freely, playing in Archipelago will very likely gatekeep your progress 
behind very specific puzzles, or there many be only one bunny you can capture at a time.

Last to note, there is a **new Computer Tab** in the in-game computer for tracking Archipelago unlocks.
This can show what tools you have unlocked so far.


## Archipelago Items and Locations

### Basics

1. Bunnies are locations.  Capturing bunnies qualifies as checking the location.
These locations are named after the Bunny's "Identity.
A bunny's identity tells you what room they are in, and which bunny they are:

Bunny identity **W-6-2** would be the **2nd** bunny in room **W-6**

2. Tools for various rooms are item.  These items are named after the rooms they unlock the tools for.
Unlocking **N-4** means you now have tools available in room **N-6**


### Fluff

**Fluff** is the go-to junk item for this game.  If you capture a bunny and find Fluff, then congratulations you get nothing!

**Golden Fluff** is specifically used for the **Golden Fluff** victory condition,
where some amount of **Golden Fluff** is distributed through your world to be located.

These will only distribute within Paquerette Down The Bunburrows, so someone else cannot win your game for you.



### Traps

There are two forms of traps avaiable:

- **Surface Teleport Trap**:  Returns the player to the surface, as if they used their own *bunny superpower* to do so.  
Mildly inconvenient at times.

- **Elevator Trap**: Sends the player into an unskippable Elevator scene, where they are eventually forced back into the shop.
The depth of the Elevator is configurable - and for the daring, there are options to increase the Elevator length every trip.


## How does Death Link work?

There is no dying in Paquerette Down The Bunburrows, so this client never sends deaths.
Instead, when someone else dies, Paquerette will act as if it recieved one of the traps:
- Sent to the surface, or
- Sent to an Elevator

This is configurable in the options.


## Options


### Home Captures Only:
**Considerd an Experts Only option**
Enable this to ensure that only Home Captures count as true location checks.


### Victory Condition:
Determines when you are considered successful in the game.

Four options available, in order of length / difficulty:

- Credits:  Reach the credits to win.  **This is the only beginner-friendly option**
- Golden Bunny:  Reach the **Golden Bunny** to win.
- Golden Fluff:  Collect all **Golden Fluff** to win.
- Full Clear:  Collect all 134 bunnies to win.


### Golden Fluff:
Determines how much Golden Fluff to generate for Golden Fluff runs.
Does not affect games with other victory conditions.


### Expert Routing:
**Considered an Experts Only option**
When randomizing, Expert Routing may result in games that require complicated, challenging, or unintuitive routes or captures.
For example, **N-4** can be home-captured without **N-4** tools, but the method involved is complicated.


### Unlock Computer:
Determines whether the player's (portable) computer will be unlocked at the start of the game.
Typically this unlock is only given through game progression, but it can be useful for tracking captures.
The Computer can be accessed on the pause menu.


### Unlock Map:
Detrmines whether the player's map will be unlocked at the start of the game.
Typically this unlock is only given through game progression, but it can be useful for tracking captures.
The map can be found within the Computer.


### Elevator Trap Odds:
The odds of a junk item being rolled as an Elevator Trap.


### Surface Trap Odds
The odds of a junk item being rolled as a Surface Teleport Trap.


### Elevator Trap Depth:
Determines how long of an Elevator ride is given from Elevator traps.


### Elevator Trap Increment:
If set above zero, will increase the length of the Elevator trap each time it is encountered.


### Death Link:
Enables Death Link for the client


### Death Link Behavior:
Determines what trap behavior a Death will result in:
- Surface Teleport Trap
- Elevator Trap


## Known Issues:

- Exiting the game after connecting to Archipelago may result in the window freezing for 5 to 7 seconds.
    If the window does not close after this, please close it manually with Task Manager as needed.

- Exiting to the main menu, and reconnecting to Archipelago, will result in duplicate log entries, and potentially odd behavior.
    Please close the game entirely and restart to reconnect.
