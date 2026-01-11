# Shadow The Hedgehog

## Where is the options page?

You can read through all the options and generate a YAML [here](../player-options).

## What does randomization do to this game?

Randomisation in this game affects the memory of the game to unlock various events and behaviours. Level access is determined based on settings, either unlocking them individually through Select mode, playing through story mode, or a combination of both.
Once you have the goal met, The Last Way will open and be available from the Story menu. If you play story mode, then the game recommends playing through story mode, and new missions will became available from clearing stages. If you play story/shuffle/last way shuffle, The Last Way will *not* open up, and must be found through story mode, same with Devil Doom.

## What items and locations get randomized?

Every level completion is a check in the game, so this includes Hero missions, Neutral missions and Dark mission.
Future versions will include further level completions as checks for The Last Way and boss fights.

Items are used to unlock stages via the Select menu, which should happen automatically upon receiving the item from the multiworld.

Shadow The Hedgehog has mission objectives which require obtaining a number of things.
Each step of progress on these checks is a multiworld item.
Likewise, all of these mission objectives are items that can be received, requiring you to meet the total to finish
the several Dark and Hero missions of the game.

The game includes further enemysanity and configuration around the percent of these checks to include.
Checkpoint sanity allows each numbered checkpoint to be an individual check.

Enemysanity logic requires the entire stage to be accessible for any of the checks to be in logic.

Keysanity is an additional, this keeps track of each individual key rather the counter. This tracks individual keys and will describe the index of the key in the stage when picking up.

Weaponsanity is an option which prevents you from holding weapons until they are unlocked, which has an affect on logic. There is an option to add checks for holding each weapon, and this can be configured to be only when unlocked as well.

Veichle sanity has been implemented, allowing for vehicles to despawn until you have the correct multiworld item.

Object unlocks are also included, similar to vehicles, which despawns objects in the stages needed to progress. All of these are seperately configurable and include Pulleys, Ziplines, Light Dash Trails, Warp Holes and Rockets.

Other checks include checking shadow boxes, gold beetles, energy cores and keydoors.

There are some junk items and special weapon unlocks are also available, regardless of weaponsanity.

It is possible to tweak the settings to remove some of the specific checks and alter total to the players choice.
Likewise, it is possible to exclude stages.

Bosses are now available checks. Bosses are required to navigate through story mode and are only available through this mode.

Future checks and items are expected to be added in the future.



## What other changes are made to the game?

The current changes to the game are all in-memory so the game has not been modified in any major way.
However, in order for the randomisation to work the way that level accessibility behaves is changed.

When entering a level with an objective (excluding all Neutral missions and missions with only 1 objective)
the total amount required for each check per level will be increased by 2. This number and range may change with future versions.

This is to prevent levels and checks becoming unreachable once you have all the required items as you would unable to play some levels as the level would auto-complete.

Once you make progress on an objective, the number will increase in game, but will be reset when handled by the client.

The client will keep the current amount set to the amount you have received from the Multiworld. Objective-less sanity does not behaviour like this. In any objective sanity mode, this is required to lower the max, which defaults to +100 to the maximum available value in the world.

Ensure you have the mission character selected and pause the game, hold the Z button, and the total value will visibly change. Enemy-based levels will autoclear at this point, otherwise you must clear 1 more in the objective. As such, ensure to do this BEFORE activating the last available in the stage.

Other objective sanity modes will reset to different numbers and not sent to finish, but will still change the max value once the level is reasonably completable.

Levels which require you to defeat a number of enemies of a particular type will clear as soon as you close the pause menu.
Other missions require you to achieve 1 more step in the objective.

Character interactions in levels have been made to not happen, but will happen the first time when charactersanity is enabled.
This is done by setting the flags to true when the player enters a level, but for those which have been seen.

Some levels with particular interactions will automatically clear after clearing other missions and the goal being met. This does not clear the mission on the save file but does handle them in the archipelago.  These include: 
- Cosmic Wall Hero auto clears Cosmic Wall Dark
- Digital Circuit Dark auto clears Digital Circuit Hero
- Space Gadget Hero auto clears Space Gadget Dark 
Mission Tokens, when enabled will be given to the player for completing missions when possible. This requires at least one of the levels missions to be cleared.

There are options to shuffle the story mode and handle goals based exclusively on story progression. Shuffling in The Last Way and Devil Doom will require the player to also find Devil Doom within the story web as part of the goal. Note that finding the stage early will reduce the player's rings to 0, forcing Super Shadow to fall, in a loop, so return to Devil Doom once you have met the other goal conditions.

## How do I use the additional commands?

The Shadow Archipelago Client has additional commands to help make life easier.

/weapons
Lists the weapons you have available.

If you provide no arguments, you will be shown the weapons in your current stage.

If you provide /s you can define which stage, either by in-game code or name.

If you provide /a, you can show all the weapons you have regardless of stage.

If you provide /h, you can see status of whether you have held the weapon for those types of checks.


/sanity (/dark, /hero, /gun, /egg, /alien /darkclear /heroclear)
Lists the sanity percentages required for beating the stage requirements, allowing to work out the percentages for you. 

If you don't provide either of these, it will show all sanities for the stage. This will show the current progress, total required and total available, as well as the frequency value.

/story /s{stage}
e.g. /story /sPrison Island
Sets the current story path to the given level. Only allows setting levels currently available to the player. This makes story mode more convinent, allowing the player to not have to play through early stages to return to levels. This cannot be used for technical reasons for mid-story bosses but can be used for final bosses.

 Not providing an argument will list all the stages available to the player in story mode.
 
/token
Shows the progress and total requirements for token counts for unlocking the end game.

/boss /s{boss name}
To compensate for the technical issues with bosses not being able to be set in story mode, this shows you which stage points to a boss. Will show all found options.

## How does Story Shuffle work?

If you enable story shuffle, the story path will be randomised to make it more interesting.
The first step is ensuring that all stages can be accessed. Once all base stages have been ensured reachable, stages will lead to provided final bosses, then bosses, and then fill in the rest of the details.

After that, the story progression field will determine a likely path, reducing the amount of completion requirements in order to complete the earlier missions and potentially increase for the later missions, making the player less likely to be BK'd for as long.

Higher story progression values will be more likely to choose paths which unlock more stages accessible without objectivesanity requirements. 
The changed requirements will affect the % of items required to finish objective sanity mission objectives to progress.
The larger the groups available the higher the requirement percentage will be, so higher values will be less gradual but more unlocked when unleashed.
The amount of passes for this functionality is defined by story_progression_balancing_passes.


## What does the game look like?

Currently this project has no feedback on what the item you have found is, and requires the use of the Text Client.

## When the player receives an item, what happens?

When you receive an item, the Text Client will update to inform you. 

## Can I play offline?

This game requires to be connected to the server at all times as it is if you wish to connect to a multiworld. Features such as level restriction and object progression will not work if you are offline. This is due to the in-memory handling, and nothing is stored currently in the save file for completed data.

However, you can play a solo world offline if you so wish to do so, just generate your solo world seed, open the Archipelago Launcher and select Host. Then open your generated seed and open the Shadow the Hedgehog Client to start playing.


## How do I finish an objective?
Meet the alignment character in the stage, select that mission, pause the game, press Z and the requirement count
will return to normal. This will auto clear for enemy-based missions, but other missions require you to add to the objective count.
If Z does not change your view, you do not have the required archipelago items to finish the stage.

For further details, fully read other sections.

## How do I finish?

You select your goal type when setting up in the yaml file. Once you reach these conditions you have set,
based on percentage and enabling, Last Story will unlock in the Story menu. Walk through this and defeat the final boss to finish.
Each goal has a seperate token or required it based on the flags set.
If you are playing Story Mode with story shuffle and last way shuffle enabled, you must find Devil Doom in the story shuffle. If you get to this stage earlier, the game will set your rings to 0, causing you to be unable to finish the super-form boss.

## Known Issues
- Some stages do not currently implement per-sanity, currently
- Easy logic has not been idealised yet, please report issues that may affect easy logic. (Easy logic is deemed anything that a new player might expect to be required as it is there in vanilla, even when there is an method, such as the Gun Jumper in Sky Troops)
