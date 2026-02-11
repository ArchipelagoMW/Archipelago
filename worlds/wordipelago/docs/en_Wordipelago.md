
# Wordipelago
## Overview
**Wordipelago** is a unique twist on the classic word-guessing game created by Josh Wardle and purchased by the New York Times. **Wordipelago** is a strategic reimagining of this word guessing game format, designed to work with the **Archipelago** multi-game system, it introduces restrictive starts, progressive mechanics, and configurable difficulty.

Players start with a limited set of letters, fewer guesses, and no visual aids like yellow letter indicators or greyed-out incorrect letters. To accommodate this, the default setting allows players to guess non-dictionary 'words'. However, this is configurable and players can enable an option at any time to require that all guesses be valid dictionary words.

If all guesses are used without identifying the correct word, a cooldown period is enforced before a new round starts and play continues against a new word.

## Objective
#### Goals
Wordipelago supports two main goal types:
- Correctly guess a specific number of words
- Achieve a streak of consecutive correct guesses

Players can choose either objective or combine both for a further challenge. These goals are fully configurable to match your preferred difficulty or game length.
#### Difficulty Options
The game features two options that directly adjust difficulty:
- logic_difficulty: This adjusts how restrictive progression is, reducing the number of letters and guesses that are expected to be needed to reach later gameplay.
- word_weighting: Adjusts how likely your next word is to align well with your current letter pool. Higher weighting gives more "guessable" words based on what you’ve unlocked.

Other options such as reducing starting guesses, letters or cooldown time will also impact difficulty in some way or another.

## Unlocks and Items
As players progress, they can unlock new gameplay mechanics and helpful tools using progression or earned points. Points are awarded primarily through discovering green letters and achieving unlock milestones.

#### Progression Items
Key items that are required for progression:
- Access to additional letters in the alphabet
- Visibility of misplaced letters (yellow indicators)
- Increased number of guesses per word
#### Supportive Items
Helpful utilities to help you progress faster:
- Automatic greying out of incorrect letters
- Reduced cooldown time between words
- Shop point bundles
- Suggestions
(Provides a possible word that may or may not be related to the current word)
#### Traps
Negative effects to keep you on your toes:
- Increased Cooldown (1 round only)
- Random Guesses: a selection of your unlocked letters
- Bad Guesses: I don't even think those are letters

## Progression and Locations
Players unlock progression and rewards by completing specific in-game achievements, such as:

- Successfully guessing each letter in any word
- Identifying 1, 2, 3, 4, or 5 correctly position letters in a single word
- Identifying each combination of green letters
- Identifying each combination of yellow letters
(Note: combinations track green or yellow letters separately; mixed colors are not used)
- Successfully guessing words toward your configured goal
- Reaching new word streak highs
- Purchasing Items from the point shop

## Technical Details
**Wordipelago** is implemented in JavaScript and works in all modern HTML5-capable browsers. The game state is automatically saved and synchronized across devices, allowing you to switch machines or play with multiple clients without issues or losing progress.

## Configuration
The  [Player Options Page](../player-options) provides a full suite of configuration settings and lets you export a setup tailored to your desired gameplay experience.