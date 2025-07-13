# Civilization 6 Archipelago

## What does randomization do to this game?

In Civilization VI, the tech and civic trees are both shuffled. This presents some interesting ways to play the game in a non-standard way. If you are feeling adventurous, you can enable the "boostsanity" option in order to really change up the way you normally would play a Civ game. Details on the option can be found in the [Boostsanity](#boostsanity) section below.

There are a few changes that the Archipelago mod introduces in order to make this playable/fun. These are detailed in the [__FAQ__](#faqs) section below.

## What is the goal of Civilization VI when randomized?
The goal of randomized Civilization VI remains the same. Pursue any victory type you have enabled in your game settings, the one you normally go for may or may not be feasible based on how things have been changed up!

## Which items can be in another player's world?
All technologies and civics can be found in another player's world.

## What does another world's item look like in Civilization VI?
Each item from another world is represented as a researchable tech/civic in your normal tech/civic trees.

## When the player receives an item, what happens?
A short period after receiving an item, you will get a notification indicating you have discovered the relevant tech/civic. You will also get the regular popup that details what the given item has unlocked for you.

## FAQs
- Do I need the DLC to play this?
    - You need both expansions, Rise & Fall and Gathering Storm. You do not need the other DLCs but they fully work with this.
- Does this work with Multiplayer?
    - It does not and, despite my best efforts, probably won't until there's a new way for external programs to be able to interact with the game.
- Does this work with other mods?
    - A lot of mods seem to work without issues combined with this, but you should avoid any mods that change things in the tech or civic tree, as even if they would work it could cause issues with the logic.
- "Help! I can't see any of the items that have been sent to me!"
    - Both trees by default will show you the researchable Archipelago locations. To view the normal tree, you can click "Toggle Archipelago Tree" in the top-left corner of the tree view.
- "Oh no! I received the Machinery tech and now instead of getting an Archer next turn, I have to wait an additional 10 turns to get a Crossbowman!"
    - Vanilla prevents you from building units of the same class from an earlier tech level after you have researched a later variant. For example, this could be problematic if someone unlocks Crossbowmen for you right out the gate since you won't be able to make Archers (which have a much lower production cost).
    - Solution: You can now go in to the tech tree, click "Toggle Archipelago Tree" to view your unlocked techs, and then can click any tech you have unlocked to toggle whether it is currently active or not.
	- If you think you should be able to make Field Cannons but seemingly can't try disabling `Telecommunications`
- "How does DeathLink work? Am I going to have to start a new game every time one of my friends dies?"
    - Heavens no, my fellow Archipelago appreciator. When configuring your Archipelago options for Civilization on the options page, there are several choices available for you to fine tune the way you'd like to be punished for the follies of your friends. These include: Having a random unit destroyed, losing a percentage of gold or faith, or even losing a point on your era score. If you can't make up your mind, you can elect to have any of them be selected every time a death link is sent your way.
    In the event you lose one of your units in combat (this means captured units don't count), then you will send a death link event to the rest of your friends.

- I enabled `progressive districts` but I have no idea what tech or civic a progressive district unlocks for me!
    - Any technology or civic that grants you a new building in a district (or grants you the district itself) is now locked behind a progressive item. For example, `PROGRESSIVE_CAMPUS` would give you these items in the following order:
          1. `TECH_WRITING`
          2. `TECH_EDUCATION`
          3. `TECH_CHEMISTRY`
	- An important thing to note is that the seaport is part of progressive industrial zones, due to electricity having both an industrial zone building and the seaport.
    - If you want to see the details around each item, you can review [this file](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/civ_6/data/progressive_districts.py).

## Boostsanity
Boostsanity takes all of the Eureka & Inspiration events and makes them location checks. This feature is the one to change up the way Civilization is played in an AP multiworld/randomizer. What normally are mundane tasks that are passively collected now become a novel and interesting bucket list that you need to pay attention to  in order to unlock items for yourself and others!
Boosts have logic associated with them in order to verify you can always reach the ones you need to, when you need to. One side effect of this is that when boostsanity is enabled, some previously "Useful" items are now flagged as "Progression" (Urbanization, Pottery, The Wheel, to name a few).

### Boostsanity FAQs
- Someone sent me a tech/civic, and I'm worried I won't be able to boost it anymore!
    - Fear not! Through a lot of wizardry 🧙‍♂️ you can boost civics/techs that have already been received. Additionally, the UI has been updated to show you whether they have been boosted or not after receiving them.
- I need to kill a unit with a slinger/archer/musketman or some other obsolete unit I can't build anymore, how can I do this?
    - Don't forget you can go into the Tech Tree and click on a Vanilla tech you've received in order to toggle it on/off. This is necessary in order to pursue some of the boosts if you receive techs in certain orders.
- Something happened, and I'm not able to unlock the boost due to game rules!
    - A few scenarios you may worry about: "Found a religion", "Make an alliance with another player", "Develop an alliance to level 2", "Build a wonder from X Era", to name a few. Any boost that is "miss-able" has been flagged as an "Excluded" location and will not ever receive a progression item. For a list of how each boost is flagged, take a look [here](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/civ_6/data/boosts.py).
- I'm worried that my `PROGRESSIVE_ERA` item is going to be stuck in a boost I won't have time to complete before my maximum unlocked era ends!
    - The unpredictable timing of boosts and unlocking them can occasionally lead to scenarios where you'll have to first encounter a locked era defeat and then load a previous save. To help reduce the frequency of this, local `PROGRESSIVE_ERA` items will never be located at a boost check.
- There's too many boosts, how will I know which one's I should focus on?!
    - In order to give a little more focus to all the boosts rather than just arbitrarily picking them at random, items in both of the vanilla trees will now have an advisor icon on them if its associated boost contains a progression item.
