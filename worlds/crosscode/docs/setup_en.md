# CrossCode Setup Guide

This guide has been updated 08 November 2024 and is accurate as of version 0.6.1.

CrossCode is an "unsupported" Archipelago game, meaning it is not distributed with the main Archipelago installation. Fortunately, it is easy to run unsupported games even with stock Archipelago.
# Important: Complete CrossCode first

I (CodeTriangle) would strongly encourage you to complete the game at least once before running the game randomized. With many other games, including some that are quite similar to CrossCode, you may be able to get by in a randomized context with basic game knowledge. With some others, you may be able to have a good experience going in blind and randomized.

CrossCode is not one of those games. As a story-driven RPG, CrossCode relies heavily on its narrative to guide the player through the setpieces of the game. You will run into snags as you attempt to find many checks and even the final boss without full knowledge of the story.

Furthermore, because CrossCode is exceedingly linear, it requires an "open-world" mod, which allows the player to sequence-break the game and reach certain areas long before they would typically be unlocked. This will lead to further confusion as we have had to disable some of the methods that the CrossCode developers have implemented to remind players of their story progress and next objective. Many areas and gameplay features will become available without warning or fanfare where they would be helpfully telegraphed in a non-randomized playthrough.

It is also my (CodeTriangle's) opinion that CrossCode is one of the finest video game stories ever crafted. To play this game randomized without having beaten it vanilla is to deprive yourself of the ability to experience the story the way it was meant to be experienced.

You may choose for yourself whether you want to continue. If you do, know that support for issues stemming from this choice will be limited.

# How to generate your own multiworld with CrossCode seeds

First, you need a local installation of Archipelago itself. It should be as simple as downloading a release from [this page](https://github.com/ArchipelagoMW/Archipelago/releases/latest) and either unzipping it or running the installer, depending on your operating system.

Next, download the APWorld file and the template YAML from the [releases page of the CrossCode Archipelago project](https://github.com/CodeTriangle/CCMultiworldRandomizer/releases/latest) and put it into custom_worlds in your Archipelago installation folder (if you have installed an old version previously in lib/worlds, delete it before attempting to generate).

Make sure to customize the template YAML following the guides that Archipelago provides. The options should be self-explanatory, but if they are not, feel free to ask.

Then put your yamls in the Players directory (once again, in the root of your installation) and run the ArchipelagoGenerate program. If you need a yaml to build off of, we have some in the discord. The result should be in the output directory. The terminal window should tell you the filename.

This file can then be either self-hosted with the ArchipelagoServer program or cloud-hosted on https://archipelago.gg (or any of the third-party Archipelago host sites) so long as the server's Archipelago version is sufficiently up-to-date to support CrossCode.

# How to join a multiworld with CrossCode seeds

Install [CCLoader2](https://wiki.c2dl.info/CCLoader). CCLoader comes with a custom and versatile mod manager which can be used to install CCMultiworldRandomizer and its dependencies.

Open CrossCode and do the following:

* Enter the Options menu.
* Press the "mods" hotkey (listed in the top bar of the menu).
* Search or scroll through the mod list until you find the mod labeled Multiworld randomizer by CodeTriangle with the Archipelago logo as its icon.
* Select the mod and install it using the button listed at the bottom of the screen.
* You will be prompted to restart the game. Do that.

Now, assuming you don't get any errors in the top-right corner, you can start a new save file.

* Use the Game Start option. This should bring you to the Archipelago console screen.
* On the right of this menu, select the topmost button to set your connection details. Follow the tooltips if the terminology confuses you.
* After connecting, return to the Archipelago console and enter the New Game+ menu. Select your perks.
* Exit the menu to start playing.

You will know if the mod is working when you get to space for the first time and you don't recieve the Disc of Insight and Green Leaf Shade as expected. Instead, you should see a prompt in the top-right notifying you of what was actually found.

Alternatively, manual installation is supported, but not recommended. At this point, if you want to do a manual setup, skip the first bulleted list of this section guide and use [this page](https://github.com/CodeTriangle/CCMultiworldRandomizer/wiki/Dependencies#manual-installation) instead.
What New Game+ perks should I use?

When you arrive at the New Game+ perk selection screen, you may notice that the Randomizer Start option is automatically selected and cannot be deselected. This is a feature of the randomizer, an enhanced version of the Skip Beginning perk which starts Lea in Rookie Harbor after the tedious Rhombus Dungeon sequence).

All of the multipliers are very useful to decrease the grind. I don't recommend you carry anything over as that will probably ruin the purpose of the randomization. You may consider using Get on My Level so that you'll have the ability to fight back against enemies in areas the game does not expect you to be in, although this does increase the difficulty by quite a bit in areas that are meant to be easier.

Other modifiers are up to personal preference. Most of the rest of them increase the difficulty, which may or may not be something that interests you.

If you are looking for some more quirky options, you can install the New Game++ mod from CCModManager as well, which provides [these features](https://github.com/CCDirectLink/CCNewGamePP/blob/master/readme.md#features), though I do not guarantee compatibility or fun.

If you do find yourself regretting your NG+ perk choices, you can also install New game+ Cheats from CCModManager, which will allow you to switch out perks on the fly.

# Poptracker Pack

Courtesy of Lurch9229, you can have a fancier interface for tracking your progress. This is optional but extremely helpful, especially if you don't have a solid mental model of the world. [See here for information](https://github.com/lurch9229/CrossCode-Poptracker-AP).

Other tracking solutions are available, but the poptracker pack is developed by a trusted member and moderator of the community, and is therefore more likely to give accurate results.

# How to get support

First off, thank you for beta testing! I truly appreciate it.

Second off, please make sure you are using the most recent version of both the mod and the APWorld. I will provide only limited support for outdated versions of either.

With that out of the way, you have several options:

## Ask on the CrossCode Beta Testing server

* Join our [testing discord server](https://discord.gg/ZSWfgQdfGr).
* Make sure you can see the #bug-report forum.
* Create a new thread in that forum, following all the rules for posting. These include but are not limited to:
* * Software versions of all software involved.
* * What you did leading up to the issue.
* * The expected behavior.
* * The actual behavior (in enough detail that I could feasibly reproduce it).

I'm pretty active on Discord, so I should see your message within a few hours. For bugs that have a quick fix, I have generally been able to address them within a week. For more sophisticated bugs or for bugs that I suspect are hidden in code that will be rewritten later, I'll modify this page to include a workaround until such time as I can actually fix it.

## Ask on the Archipelago server

The Archipelago discord server (which you can join [here](https://discord.gg/8Z65BR2)) is also actively monitored. Once you are in the server, navigate to our thread in the #future-game-design forum (you can go directly there by clicking [here](https://discord.com/channels/731205301247803413/1128180904926396437)). Please still post the information outlined in the bulleted list above.

The beta testing server is the preferred option as we have more curated space for different activities. The ticketing system, where different bug reports can have their own separate threads is one major benefit. However, if you are already on the Archipelago server, this works perfectly well.

## Open a GitHub issue

If you have a GitHub account and you know how to do so, you can also open an issue on the [project's GitHub page](https://github.com/CodeTriangle/CCMultiworldRandomizer/issues). I get emails for GitHub issues here, so you can be sure I'll see it.

# A note on versions

As of 0.5, different versions of CCMultiworldRandomizer are intended to be fully compatibile with games generated and played on previous versions of the mod and APWorld. The mod failing after an update should be reported as a bug.

The only catch is that upgrading multiple versions at a time may not be as well-tested. You should still try report these issues as bugs.
