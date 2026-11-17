# DOTA 2

A **Meta-progression randomizer** for DOTA 2. You play regular online matches and the Archipelago client parses your match results and sends location checks (hero wins, stats, shop purchases)

## How it works

- **Heroes** - You are given a random pool of 30 heroes to start and can unlock more by finding "Progressive Group Unlock" items. Wins with a hero from each group is a check. 

- **Stats and Attributes** - Checks such as "Win with a Melee Hero", "Win with a Support Hero", "Have X kills", "Have X Dewards" are examples of some checks in the game

- **Shop Items** - While you can buy any item in a Dota 2 match, the checks for buying those items will be **locked** for the Archipelago until the right unlock items are found. All Consumable Items will start unlocked: Tangos, Salves, Wards etc. For an Item to be available **all Basic Components** of that item must be unlocked (Recipes not included). Example: the `"Unlock Ring of Protection"` item unlocks both the `"Ring of Protection"` check and the `"Buckler"` check (ring + recipe), however the `"Soul Ring"` check would require the `"Unlock Gauntlets of Strength"` item as well (ring + gauntlets + recipe). 

- **Global Challenges** - Checks any hero can do, read from the parsed match: get first blood, kill a courier, pick up each type of rune, use a buyback, pick up the Aegis, win as each position (1 to 5), win a short match (no leaver or bot in the match), win a long match, and win a match where your team took Roshan.

- **Quests** - Checks that add up over the whole seed: stack camps, place wards (observers and sentries) and damage buildings. Each match counts once, even if parsed again. Type `/quests` in the client to see your progress.

- **Customizing checks** - All global challenges and quests are in the seed by default. In your YAML, `disabled_checks` removes families or single checks, and `check_values` changes their values (for example the short match length or the number of wards). Only list what you want to change:

```yaml
DOTA 2:
  disabled_checks: ["Runes", "Kill a Courier"]
  check_values:
    Short Win Minutes: 25
    Wards Placed: 20
```

- **Collectables** - A certain number of **Primordial Fragments** set by the options are required to complete the goal. This is needed so the archipelago has something it can actually track and generate the logic around

- **Goal** - Have the number of Unique Hero Wins, Total Wins, and Primordial Fragments set by the YAML

see the **Setup Guide** in setup_en.md for setup and custome client instructions