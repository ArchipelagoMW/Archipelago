# Dark Souls III Enemy Randomization

[Game Page] | [Setup] | [Items] | [Locations] | Enemy Randomization

[Game Page]: /games/Dark%20Souls%20III/info/en
[Setup]: /tutorial/Dark%20Souls%20III/setup/en
[Items]: /tutorial/Dark%20Souls%20III/items/en
[Locations]: /tutorial/Dark%20Souls%20III/locations/en

If `randomize_enemies` in your Dark Souls 3 player config YAML is enabled, bosses, minibosses and basic enemies will
be shuffled with themselves respectively.

To further customize enemy randomization beyond that, there is a section called `random_enemy_preset`.

This tutorial will show all the ways how to configure that preset.

## Table of Contents
- [The Basics](#the-basics)
- [Individual Assignments](#individual-assignments)
- [Pools](#pools)
  * [Pool Groups](#pool-groups)
    + [RandomByType](#randombytype)
  * [Weights](#weights)
- [Settings](#settings)
  * [Boss](#boss)
  * [Miniboss](#miniboss)
  * [Basic](#basic)
    + [BuffBasicEnemiesAsBosses](#buffbasicenemiesasbosses)
  * [Enemies](#enemies)
  * [DontRandomize](#dontrandomize)
  * [RemoveSource](#removesource)
  * [OopsAll](#oopsall)
- [Enemy Categories](#enemy-categories)

## The Basics

There are two main ways to assign an enemy to be randomized: [individual enemy assignments](#individual-assignments)
to target a singular enemy placement and setting up [Pools](#pools) to target a category of enemies.

Custom pools are recommended unless you specifically want to single out one enemy placement.

All bosses also have their own category, so individual assignment is not necessary in those cases.

Be aware of correct indentation of your YAML file. Every example in this document will need to be nested under the
`random_enemy_preset:` section.

Disable the preset by leaving just empty brackets `{}`. Like usual with YAML, you can add comments by using `#`.

For further examples, check out the "presets" folder of the standalone randomizer.

## Individual Assignments

Individual enemy assignment allows you to target individual enemies, rather than a category as under pools.

This overrides pools and any other configuration, will usually ignore progression, and can possibly cause you to have to
fight Yhorm the Giant without Storm Ruler.

You use it in the [`Enemies`](#enemies) section by selecting a specific enemy using its unique
ID, or its specific name followed by its ID.

See the '/randomizer/preset/Template.txt' file of the static randomizer for all available IDs.

There are also some special target names available for individual assignments:

- `any`: This is the default and allows any enemy in the pool to appear there.

- `norandom`: Assigns an enemy to itself. This has the same effect as adding the enemy name to [`DontRandomize`](#dontrandomize).

## Pools

A pool is a collection of enemies. A pool can both be a randomization target and an eligible group of random enemies to
be drawn from for randomization. See [Enemy Categories](#enemy-categories) for all available pools.

Pool assignment generally respects progression, like requiring Storm Ruler to be accessible before Yhorm the Giant.

By default, using a boss as another boss, or a miniboss as another miniboss, takes the source enemy out of the default
pool for that category, so each enemy will still be used once if possible. However, the enemy can still appear more
than once if used in a custom pool.

### Pool Groups

Pools can be joined into a pool group by joining several names, separated by a semicolon.

```yaml
# All basic enemies are just different hollows now
Basic:
- Weight: 100
  Pool: Hollow Soldiers; Large Hollow Soldiers
```

#### RandomByType

By default, selection will be random across all eligible enemies. In our example above it would select from:

- Hollow Soldier
- Road of Sacrifices Hollow Soldier
- Cathedral Hollow Soldier
- Lothric Castle Hollow Soldier
- Grand Archives Hollow Soldier

and

- Large Hollow Soldier
- Cathedral Large Hollow Soldier
- Lothric Castle Large Hollow Soldier

However, this would make it more likely to select a regular soldier instead of a large one (5 out of 8), just because
there are fewer entries in the latter category.

You can specify `RandomByType: true` to select randomly from the list itself (Hollow Soldiers, Large Hollow Soldiers)
and make our previous example a true 50/50 split.

```yaml
# All basic enemies are just different hollows now
Basic:
- Weight: 100
  Pool: Hollow Soldiers; Large Hollow Soldiers
  RandomByType: true # To make it truly 50/50 between the categories
```

### Weights

Weights can be used to select multiple different outcomes within a pool, weighted to give different probabilities each.

Weights don't necessarily have to add up to 100, but doing it that way makes estimating probabilities very intuitive.

```yaml
Boss:
- Weight: 79 # 79% of bosses will still be bosses
  Pool: default
- Weight: 20 # Replace 20% of all bosses with minibosses
  Pool: Miniboss
- Weight: 1 # Replace 1% of all bosses with regular enemies. It's always funny
  Pool: Basic
```

Be aware that weights will not work in the [`Enemies`](#enemies) section.

## Settings

### Boss

This setting indicates which enemies can be used as replacements for bosses.
By default, this is the pool of all 29 bosses.

```yaml
Boss:
- Weight: 80
  Pool: default
- Weight: 20 # Replace 20% of all bosses with minibosses
  Pool: Miniboss
```

### Miniboss

This setting indicates which enemies can be used as replacements for minibosses.
By default, this is the pool of all 32 minibosses (including duplicates).

```yaml
Miniboss:
- Weight: 80
  Pool: default
- Weight: 20 # Replace 20% of all minibosses with bosses
  Pool: Boss
```

### Basic

This setting indicates which enemies can be used as replacements for all other enemies, so non-bosses and non-minibosses.
By default, this is the pool of all ~2000 basic enemies (including duplicates).

```yaml
Basic:
- Weight: 94
  Pool: default
- Weight: 5 # Replace 5% of all basic enemies with minibosses
  Pool: Miniboss
- Weight: 1 # Replace 1% of all basic enemies with bosses
  Pool: Boss
```

#### BuffBasicEnemiesAsBosses

If enabled, this causes basic enemies to become a lot stronger when randomized into the slot of a boss.

```yaml
Boss:
- Weight: 100 # All bosses are just basic enemies...
  Pool: Basic

BuffBasicEnemiesAsBosses: true # ...but they are strong
```

### Enemies

Under the `Enemies:` setting you can add more nuanced replacements of random enemies.
There are two ways you can adjust enemies:
- Assign to a group of enemies using their category pool (see [Enemy Categories](#enemy-categories))
- Assign to one specifc enemy by using its number (see [Individual Assignments](#individual-assignments))

```yaml
Enemies:
  # Replace only the very first Ravenous Crystal Lizard with the final boss
  Ravenous Crystal Lizard 4000380: Lords of Cinder
  
  # Replace all regular soldiers with skeletons or small crabs
  Hollow Soldiers: Skeletons; Lesser Crab
  
  # Knights remain knights, but variants (i.e. weapons) are still shuffled within the category
  High Wall Lothric Knight: High Wall Lothric Knight
```

### DontRandomize

A semicolon-separated list of enemies or enemy types to not randomize (assign to themselves).
It is taken out of its default pool and also custom pools in this case, but it can still be assigned to
[individual enemies](#individual-assignments).

```yaml
DontRandomize: Iudex Gundyr # Iudex Gundyr will be at his vanilla location

Boss:
- Weight: 100
  Pool: default # Boss slots other than Iudex Gundyr will never become him
```

### RemoveSource

A semicolon-separated list of enemies or enemy types to remove from all pools.
It can still be assigned to individual enemies.
This is overridden by [`DontRandomize`](#dontrandomize) directives.

```yaml
# Remove the most annoying enemies from all pools
RemoveSource: Bridge Darkeater Midir; Ancient Wyvern Mob; Curse-rotted Greatwood; High Lord Wolnir; Carthus Sandworm
```

### OopsAll

Assigning an enemy or a pool to `OopsAll` sets all pools to that specific enemy or category of enemy. This can still be
overridden using [individual enemy assginments](#individual-assignments), but otherwise every enemy is replaced by
this setting.

```yaml
# This run suddenly got very spooky
OopsAll: Skeletons
```

---

## Enemy Categories

The following enemy category pools are available:

- Any
- Bosses
- Minibosses
- Bosses and Minibosses
- Basic
- Abyss Watchers
- Aldrich, Devourer of Gods
- Ancient Wyvern
- Ancient Wyvern Mob
- Angel Pilgrim
- Basilisk
- Black Knight
- Blackflame Friede
- Boreal Outrider Knight
- Bridge Darkeater Midir
- Cage Spider
- Carthus Sandworm
- Cathedral Evangelist
- Cathedral Knight
- Cemetery Hollow
- Champion Gundyr
- Champion's Gravetender and Gravetender Greatwolf
- Consumed King Oceiros
- Corpse-grub
- Corvian
- Corvian Knight
- Corvian Settler
- Crabs
  - Lesser Crab
  - Greater Crab
  - Ariandel Greater Crab
- Crystal Lizard
- Crystal Sage
- Crystal Sage in Archives
- Curse-rotted Greatwood
- Dancer of the Boreal Valley
- Darkeater Midir
- Darkwraith
- Deacon
  - Cathedral Deacon
  - Wide Deacon
  - Irirthyll Deacon
  - Irirthyll Tall Deacon
- Deacons of the Deep
- Deep Accursed
- Demon
- Demon Cleric
- Demon Prince
- Demonic Statue
- Dragonslayer Armour
- Dreg Heap Thrall
- Elder Ghru
- Father Ariandel
- Farron Follower
- Fire Witch
- Gargoyles
  - Profaned Capital Gargoyle
  - Archives Gargoyle
- Ghru Grunt
- Giant Fly
- Giant Slave
- Grand Archives Scholar
- Grave Warden
- Halflight, Spear of the Church
- Harald Legion Knight
- High Lord Wolnir
- Hobbled Cleric
- Hollow Manservant
- Hollow Soldiers
  - Hollow Soldier
  - Road of Sacrifices Hollow Soldier
  - Cathedral Hollow Soldier
  - Lothric Castle Hollow Soldier
  - Grand Archives Hollow Soldier
- Hound Rat
- Infested Corpse
- Irirthyll Dungeon Peasant Hollow
- Irithyll Giant Slave
- Irithyll Starved Hound
- Irithyllian Slave
- Iudex Gundyr
- Jailer
- Judicator
- King of the Storm
- Large Hollow Soldiers
  - Large Hollow Soldier
  - Cathedral Large Hollow Soldier
  - Lothric Castle Large Hollow Soldier
- Large Hound Rat
- Large Serpent-Man
- Large Starved Hound
- Locust Preacher
- Lords of Cinder (actually called "Soul of Cinder" ingame)
- Lorian, Elder Prince
- Lothric Knights
  - High Wall Lothric Knight
  - Lothric Castle Lothric Knight
  - Dreg Heap Lothric Knight
  - Red-Eyed Lothric Knight
- Lothric Priest
- Lothric, Younger Prince
- Lycanthrope
- Lycanthrope Hunter
- Maggot Belly Starved Hound
- Millwood Knight
- Mimic Chest
- Monstrosity of Sin
- Murkman
- Murkman Summoner
- Nameless King
- Old Demon King
- Passive Locust Preacher
- Peasant Hollow
- Poisonhorn Bug
- Pontiff Knight
- Pontiff Sulyvahn
- Pus of Man
- Ravenous Crystal Lizard
- Reanimated Corpse
- Ringed City Cleric
- Ringed Knight
- Road of Sacrifices Sorcerer
- Rock Lizard
- Rotten Slug
- Serpent-Man
- Serpent-Man Summoner
- Sewer Centipede
- Silver Knight
- Sister Friede
- Skeletons
  - Skeleton
  - Bonewheel Skeleton
  - Carthus Curved Sword Skeleton
  - Carthus Shotel Skeleton
  - Ringed City Skeleton
- Slave Knight Gael
  - Slave Knight Gael 1
  - Slave Knight Gael 2
- Small Locust Preacher
- Smouldering Ghru Grunt
- Starved Hound
- Stray Demon
- Sulyvahn's Beast
- Thrall
- Tree Woman
- Vordt of the Boreal Valley
- Winged Knight
- Wolves
  - Smaller Wolf
  - Larger Wolf
  - Greatwolf
- Wretch
- Writhing Flesh
  - Catacombs Writhing Flesh
  - Smouldering Writhing Flesh
  - Anor Londo Writhing Flesh
- Yhorm the Giant
