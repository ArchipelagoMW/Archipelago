# DOTA 2

A **Meta-progression randomizer** for DOTA 2. You play regular online matches and the Archipelago client parses your match results and sends location checks (hero wins, stats, shop purchases)

## How it works

- **Heroes** - You are given a random pool of heroes to start (30 by default, option `starting_heroes`) and can unlock more by finding "Progressive Group Unlock" items. The other heroes are split evenly into groups (7 by default, option `hero_groups`). Wins with a hero from each group is a check. 

- **Stats and Attributes** - Checks such as "Win as a Melee Hero", "Win as a Support Hero", and kills, assists, dewards, last hits and denies in a match: one check per stat by default ("Get 15 Kill(s)"), or one per threshold you list in the YAML. Thresholds go by steps (Last Hits by 25, damage by 2,500...), so that each one has its own check name.

- **Shop Items** - While you can buy any item in a Dota 2 match, the checks for buying those items will be **locked** for the Archipelago until the right unlock items are found. All Consumable Items will start unlocked: Tangos, Salves, Wards etc. For an Item to be available **all Basic Components** of that item must be unlocked (Recipes not included). Example: the `"Unlock Ring of Protection"` item unlocks both the `"Ring of Protection"` check and the `"Buckler"` check (ring + recipe), however the `"Soul Ring"` check would require the `"Unlock Gauntlets of Strength"` item as well (ring + gauntlets + recipe). 

- **Global Challenges** - Checks any hero can do, read from the parsed match: get first blood, kill a courier, pick up each type of rune, use a buyback, pick up the Aegis, win as each position (1 to 5), win a short match (no leaver or bot in the match), win a long match, and win a match where your team took Roshan.

- **Healing and damage** - In a match: healing done to heroes, physical and magical damage to heroes, one big physical or magical hit on a hero, and seconds of stun on enemy heroes. Damage types come from the abilities (auto-attacks are physical, pure damage counts as magical, items as neither).

- **Quests** - Checks that add up over the whole seed: stack camps, place wards (observers and sentries), damage buildings, heal heroes, deal physical or magical damage to heroes and stun enemies, each with a lower and a full target by default. Each match counts once, even if parsed again. Type `/quests` in the client to see your progress.

- **Customizing checks** - All checks are in the seed by default. In your YAML, `disabled_checks` removes families (such as Legs Wins, Purchases or Runes) or single checks, and `check_values` changes their values: stat thresholds, short and long match lengths, Roshan kills, quest targets. Only list what you want to change; the options page lists every family and value with its default:

```yaml
DOTA 2:
  starting_heroes: 30
  hero_groups: 7
  disabled_checks: ["Runes", "Legs Wins", "Divine Rapier"]
  check_values:
    Kills: 8
    Last Hits: [75, 150, 250]
    Short Win Minutes: 25
    Wards Placed: 20
```

  Wins with a hero group and the goal can't be removed. If too many checks are removed to place the seed's items, generation stops and says so.

- **Collectables** - A certain number of **Primordial Fragments** set by the options are required to complete the goal. This is needed so the archipelago has something it can actually track and generate the logic around

- **Goal** - Have the number of Unique Hero Wins, Total Wins, and Primordial Fragments set by the YAML

see the **Setup Guide** in setup_en.md for setup and custome client instructions