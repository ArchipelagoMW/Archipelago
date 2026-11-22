# DOTA 2 - Setup Guide

Follow these steps to play Deadlock with Archipelago

---

## Required Stoftware 
 - Most Recent version of Dota 2 on steam
 - this APWorld

---

## Important

 - For this APWorld to work properly you must 
    1. Set your Steam Profile to public
        Steam -> View my Profile -> Edit Profile -> Privacy Settings -> "My Profile" set to public.
    2. Expose Public Match Data on Dota 2
        in the Dota settings -> Social -> Expose Public Match Data
    3. Find your SteamId and convert it to its SteamId32 form. This is needed to fetch match data from the custom client
 
---

## Setup

 - 1. Install the **DOTA2.apworld** file through the Launcher or place the .apworld into the `worlds/` directory. **DOTA2 Client** should appear in the launcher and DOTA2 should appear in the options creator

 - 2. Create Options: Set your goal by selecting number of total wins, unique hero wins, and collectables needed to complete your goal

 - 3. Generate A multiworld with your options

 - 4. Open the **DOTA2 Client** from the launcher and connect with server, slot name, and password(if applicable)

 - 5. Set your SteamId32 using the custom method `/set_player_id 123456789`

 - 6. Play Dota 2 matches. After every match, even if youy lose, submit the match for checks by typing `/parse_recent_match` into the Dota 2 client

---

## Neccessary Client Commands to Know

`/set_player_id` - Saves the SteamId locally to submit matches.

`/parse_recent_match` - Tries to parse your most recent match data and get stats for checks. **May take a minute after the game for data to be available and may take several minutes for the api to parse all the game stats once method is called**.

`/goal` - See your goal and progress towards completing the goal.

`/heroes` - See which heroes are unlocked and which progressive unlock pool they belong to.

`/game_complete` - extra method to check if game is completed in case of no release. nothing will happen if goal is not complete.

`/hero_wins` - tells you number of unique hero wins and which heroes you have won with.

`/minigame` - sending in minigame score checks. command should be typed like /minigame {first world of minigame} {score}. Example /minigame Nest 100000 or /minigame gone 5000 
    minigame keywords are as follows [gone, bat, oasis, sand, sleet, dragon, zaug's, spoon, spleen, nest].

---

## Help

Ask on the [DOTA 2 Archipelago Discord](https://discord.gg/Xzrx7DcDvm) if something doesn't work.
