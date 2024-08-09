# Civlization 6 Archipelago

## Setup Guide
For setup instructions go [here](./docs/setup_en.md).

## What does randomization do to this game?

In Civilization VI, the tech and civic trees are both shuffled. This presents some interesting ways to play the game in a non-standard way. If you are feeling adventurous, you can enable the `boostsanity` option in order to really change up the way you normally would play a Civ game. Details on the option can be found [here](./docs/boostsanity.md)

There are a few changes that the Archipelago mod introduces in order to make this playable/fun. These are detailed in the __FAQ__ section below.

## What is the goal of Civilization VI when randomized?
The goal of randomized Civlization VI remains the same. Pursue any victory type you have enabled in your game settings, the one you normally go for may or may not be feasible based on how things have been changed up!

## Which items can be in another player's world?
All technologies and civics can be found in another player's world.

## What does another world's item look like in Civilization VI?
Each item from another world is represented as a researchable tech/civic in your normal tech/civic trees.

## When the player receives an item, what happens?
A short period after receiving an item, you will get a notification indicating you have discovered the relevant tech/civic. You will also get the regular popup that details what the given item has unlocked for you.

## FAQs
- Do I need the DLC to play this?
  - Yes, you need both Rise & Fall and Gathering Storm. If there is enough interest then I can eventually add support for Archipellago runs that don't require both expansions.

- Does this work with Multiplayer?
  - It does not and, despite my best efforts, probably won't until there's a new way for external programs to be able to interact with the game.

- Does my mod that reskins Barbarians as various Pro Wrestlers work with this??
  - Only one way to find out! Any mods that modify techs/civics will most likely cause issues, though.

- "Help! I can't see any of the items that have been sent to me!"
  - Both trees by default will show you the researchable Archipelago locations. To view the normal tree, you can click "Toggle Archipelago Tree" on the top left corner of the tree view.

- "Oh no! I received the Machinery tech and now instead of getting an Archer next turn, I have to wait an additional 10 turns to get a Crossbowman!"
  - Vanilla prevents you from building units of the same class from an earlier tech level after you have researched a later variant. For example, this could be problematic if someone unlocks Crossbowmen for you right out the gate since you won't be able to make Archers (which have a much lower production cost).

  - Solution: You can now go in to the tech tree, click "Toggle Archipelago Tree" to view your unlocked techs, and then can click any tech you have unlocked to toggle whether it is currently active or not. __NOTE__: This is an experimental feature and may yield some unexpected behaviors. Please DM `@Hesto2` on Discord if you run into any issues.

- I enabled `progressive districts` but I have no idea techs/civics what items are locked behind progression now!
  - Any technology or civic that grants you a new building in a district (or grants you the district itself) is now locked behind a progressive item. For example, `PROGRESSIVE_CAMPUS` would give you these items in the following order:
  1. `TECH_WRITING`
  2. `TECH_EDUCATION`
  3. `TECH_CHEMISTRY`
  - If you want to see the details around each item, you can review [this file](./data/progressive_districts.json)

- "How does DeathLink work? Am I going to have to start a new game every time one of my friends dies??"
  - Heavens no, my fellow Archipelago appreciator. When configuring your Archipelago options for Civilization on the options page, there are several choices available for you to fine tune the way you'd like to be punished for the follies of your friends. These include: Having a random unit destroyed, losing a percentage of gold or faith, or even losing a point on your era score. If you can't make up your mind, you can elect to have any of them be selected every time a death link is sent your way.

  - In the event you lose one of your units in combat (this means captured units don't count), then you will send a death link event to the rest of your friends.

