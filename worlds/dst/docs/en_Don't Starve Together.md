# Don't Starve Together

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Instead of learning recipes from a prototyping station, your recipes are earned by doing tasks in Don't Starve Together,
or when another player in your multiworld finds one of your items.

The generator will ensure progression logic to be able to reach your goal, which you have 3 difficulties to choose from:
- Easy: Ensure items useful for your survival such as weapons, armor, lighting, seasonal gear, and base structures.
- Advanced: Expects you to know the game well and to survive seasons under-equipped.
- Expert: Expects you to be a pro and survive in riskier conditions, such as entering the ruins with nothing but a torch, etc.

## When the player receives an item, what happens?

New recipes will appear in your crafting menu, and will appear as prototypable if you have the materials, without the need
to be near a crafting station.

## Which items can be in another player's world?

Most recipes that would normally be learned at a Science Machine, Alchemy Engine, Prestithatitor, Shadow Manipulator, and
Think Tank, and rare blueprints have been shuffled into the item pool, along with various boss loot. Traps may be included
if you choose to enable them. Optionally, you can also shuffle your basic starting items or items normally only craftable
at the Ancient Pseudoscience Station or Celestial Altar.

However, not included in the item pool are:
- Character-specific recipes
- Cosmetic and decorative items
- Fishing lures learnable at the Tackle Receptacle. (The Tackle Receptacle itself is shuffled)
- Turfs learnable at the Terra Firma Tamper. (The Terra Firma Tamper itself is shuffled)
- Post-Ancient-Fuelweaver and post-Celestial-Champion content. These items will be included when the game's new content arcs are more developed.

Anything not shuffled will be craftable at their respective crafting station as in vanilla Don't Starve Together.

## What does another world's item look like in Don't Starve Together?

When near a crafting station, you will see "Interdimensional Research" items with the Archipelago icon, along with information
what the item is and its recipient. However 95% of the time a trap item will have a randomly generated name, so keep an eye
out for fakes!

Items can also appear as blueprint labelled with its containing item and recipient, which can then be activated to award your check.

In most other cases you won't see the physical item in-game but you will receive a chat notification when you find an item.

## What is the goal of Don't Starve Together?

The player is able to choose their victory condition in their config file:
- Survival: The player must live for a target number of days. This is based on the survivor's time alive and not the world age.
Being a ghost will not progress your timer.
- Bosses: The player can choose which bosses they need to defeat in order to meet their victory condition. You can choose
between defeating any one of a selection of bosses, or all of them. Boss and location checks that happen to be part of your progression
path will be prioritized for having progression items.

## What are location checks in Don't Starve Together?

Location checks in Don't Starve Together include:
- Creatures (Optional): Either killing or non-violently interacting with creatures (such as capturing or trading with).
- Bosses: Defeating a boss. You can choose whether or not harder bosses can have important progression items in your config.
- Crock Pot Dishes (Optional): Cooking a meal in the Crock Pot. You can customize whether or not Warly's exclusive dishes count,
or whether to only count meat or veggie meals.
- Farming Giant Crops (Optional): Growing and harvesting a giant farm plant.
- Crafting Stations: Crafting stations themselves are not shuffled, but have Archipelago items that you can craft.
- Crabby Hermit: Progressing through Crabby Hermit's quests unlocks Archipelago items you can exchange for empty bottles.
- Various Milestones: Such as finding Pig King, Chester, Hutch, or places you would find rare blueprints.

Additionally, you can control how much of the game is randomized, with the cave_regions and ocean_regions options in the yaml to toggle Caves and
Oceans respectively.

## What about grindy checks, like trying to spawn a Treeguard? Do I still have to go for those?

Some grindier checks have been set to not be allowed progression items.

## Can this work with a world without caves?

As of Version 1.2, worlds without caves are supported. Make sure in your yaml that cave_regions is set to none, and that your goal is not set to a cave boss.

## What happens if I choose Survival or Wilderness as my server playstyle or otherwise regenerate my world?

If the world regenerates, or starting on a new world, your checks and items will sync from the Archipelago server, giving back your AP
items when you first spawn in. Trap items will not be given again, except your last season trap received, if any. If you haven't connected
to Archipelago when restarting your world, progress since you've last connected will be lost.

Your day count will reset, setting back your progress if your completion goal is to survive a number of days. The same applies if
you reset your character through commands or dying in Wilderness mode, but not when switching your character using a Celestial Portal
and Moon Rock Idol.

## Is this compatible with other Don't Starve Together mods?

This should be compatible with most other Don't Starve Together mods. Modded items will not be shuffled and will be craftable as normal.

Known incompatibilities:
- [API] Gem Core: May cause some issues with the crafting menu
- Don't Starve Alone (Mod)

## Can this be played in multiplayer?

Yes, other players can join your world. Everyone will work together in the same Archipelago slot. Each player can get
location checks, and each player will receive Archipelago items. If you chose the survival goal type, only the longest-living
survivor will count for the victory condition.

## I am new to Don't Starve Together, or I find the game too hard!

Don't Starve Together is designed to be an unforgiving survival game, while also being scaled for multiplayer. Yet it is very learnable, and offers several
solutions for the challenges it presents to players, even if playing solo. Additionally, there are several ways to customize the game, which are just as
valid as playing the game on default settings.

If you want an easier experience:
- Do not enable caves or ocean regions in your YAML. Choose the survival goal, or choose Eye Of Terror as your goal boss.
- Set damage multipliers in the mod's configuration options.
- Use the free-build crafting mode.
- Set your server playstyle to Relaxed.
- Play with mods.
- Use the [Don't Starve Wiki](https://dontstarve.wiki.gg). Especially for Crock Pot recipes.
- Ask for advice.
