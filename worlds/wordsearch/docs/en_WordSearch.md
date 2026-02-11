# Word Search

## What is this game?

Everyone knows the word guessing game that was bought by the NY Times.
This is a Wordle randomiser built from the ground up to work with Archipelago.

You start with a limited number of letters (just a single letter by default), a reduced number of guesses, missing features such as show misplaced letters as yellow, and greying out wrong letters.
This means that guesses have to be possible with just a single letter, and so the normal limitation of guesses having to be a real word has been removed.
If you use all your guesses without getting the word, you have to wait for a cooldown before you can get a new word to guess.

The goal is to guess a certain number of words with options for even more of a challenge.

Items to unlock in the game are:
- The ability to use the rest of the letters
- showing of yellow letters
- Greying out of wrong letters
- More guesses
- Reduced cooldown time

Locations to find checks are:
- Successfully finding each letter in any word
- The first time you find 1, 2, 3, 4, and 5 letters correct in a word
- Guessing each word up to your goal

It's all build in JavaScript so it can run in most modern HTML5-capable browsers.
It's resumable from anywhere, so you can very easily switch machines you're playing on, everything catches up as soon as you connect.

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure
and export a config file.
