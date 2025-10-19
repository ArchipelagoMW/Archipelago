# PokéPark Wii: Pikachu's Adventure

## What does randomization do to this game?

Pokémon friendship and unlocking Pokémon in the overworld are randomized. Befriending Pokémon, completing
events, quests and playing minigames are treated as locations.

The story has been removed, and some changes were made to the game’s logic to support randomization.

## Other Pages

- [Setup](https://github.com/Mekurushi/Archipelago_Pokepark/blob/main/worlds/pokepark/docs/setup_en.md)

## Rom Changes

### Treehouse

| Location / Entrance | Condition                             |
|---------------------|---------------------------------------|
| Meadow Zone Gate    | None                                  |
| Beach Zone Gate     | Venusaur Prisma                       |
| Cavern Zone Gate    | Empoleon Prisma                       |
| Haunted Zone Gate   | Blaziken Prisma                       |
| Granite Zone Gate   | Rotom Prisma                          |
| Skygarden Piplup    | Prisma count (depends on used option) |
| Bibarel Instructor  | Venusaur Prisma                       |
| Ponyta Instructor   | Pelipper Prisma                       |
| Primeape Instructor | Empoleon Prisma                       |

### Meadow Zone

| Location / Entrance | Condition         |
|---------------------|-------------------|
| Venusaur Gate       | Bulbasaur Prisma  |
| Big Berry Crate     | Bulbasaur Prisma  |
| Bidoof Quest        | Mankey Friendship |

### Beach Zone

| Location / Entrance          | Condition                 |
|------------------------------|---------------------------|
| Ice Zone Boulder             | Gyarados Prisma           |
| Bridges                      | Beach Zone Bridge Unlocks |
| Pelipper Attraction Entrance | None                      |
| Gyarados Attraction Entrance | None                      |      

### Ice Zone

| Location / Entrance          | Condition            |
|------------------------------|----------------------|
| Lift                         | Ice Zone Lift Unlock |
| Prinplup                     | None                 |
| Lake                         | Ice Zone Lake Unlock |
| Empoleon Gate                | Gyarados Prisma      |  
| Empoleon Attraction Entrance | None                 |

### Cavern Zone

| Location / Entrance | Condition        |
|---------------------|------------------|
| Magma Zone Gate     | Bastiodon Prisma |
| Diglett             | Bastiodon Prisma |
| Dugtrio             | Bastiodon Prisma |

### Magma Zone

| Location / Entrance           | Condition                   |
|-------------------------------|-----------------------------|
| Blaziken Gate                 | Rhyperior Prisma            |
| Fire Wall                     | Magma Zone Fire Wall Unlock |
| Rhyperior Attraction Entrance | None                        |

### Haunted Zone

| Location / Entrance    | Condition                         |
|------------------------|-----------------------------------|
| Mansion Entrance       | Tangrowth Prisma                  |
| Mansion Doors          | Haunted Zone Mansion Doors Unlock |
| Rotom Hidden Bookshelf | Dusknoir Prisma                   |
| Mismagius              | None                              |
| Spinarak               | Rotom Prisma                      |

### Granite Zone

| Location / Entrance | Condition    |
|---------------------|--------------|
| Flygon Door         | Absol Prisma |

### Misc

- Postgame Pokemon unlocked in Attractions
- Drifblim always spawns
- Removed Intro and Ending files

## Feature Roadmap

- In-game client messages
- In-game hints
- Entrance randomizer
- Model randomizer
- Locations of missing Pokemon

## Credits

### Core Development / APWorld Integration

- Joe Mama (Mekurushi)
- Seph — Reverse Engineering & Tools Support

### Testing & Feedback

- River — Testing, Q&A, and Feedback
- Various users in the #future-game-design thread

### Resources & References

- Various other APWorlds as references