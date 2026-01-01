# Old School Runescape

## What is the Goal of this Randomizer?
The goal is to complete the quest "Dragon Slayer I" with limited access to gear and map chunks while following normal
Ironman/Group Ironman restrictions on a fresh free-to-play account.

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file. OSRS contains many options for a highly customizable experience. The options available to you are:

* **Starting Area** - The starting region of your run. This is the first region you will have available, and you can always
freely return to it (see the section below for when it is allowed to cross locked regions to access it)
  * You may select a starting city from the list of Lumbridge, Al Kharid, Varrock (East or West), Edgeville, Falador,
Draynor Village, or The Wilderness (Ferox Enclave)
  * The option "Any Bank" will choose one of the above regions at random
  * The option "Chunksanity" can start you in _any_ chunk, regardless of whether it has access to a bank.
* **Brutal Grinds** - If enabled, the logic will assume you are willing to go to great lengths to train skills.
  * As an example, when enabled, it might be in logic to obtain tin and copper from mob drops and smelt bronze bars to
reach Smithing Level 40 to smelt gold for a task.
  * If left disabled, the logic will always ensure you have a reasonable method for training a skill to reach a specific
task, such as having access to intermediate-level training options
* **Progressive Tasks** - If enabled, tasks for a skill are generated in order from earliest to latest.
  * For example, your first Smithing task would always be "Smelt an Iron Bar", then "Smelt a Silver Bar", and so on.
You would never have the task "Smelt a Gold Bar" without having every previous Smithing task as well. 
This can lead to a more consistent length of run, and is generally shorter than disabling it, but with less variety.
* **Skill Category Weighting Options**
  * These are available in each task category (all trainable skills plus "Combat" and "General")
  * **Max [Category] Level** - The highest level you intend to have to reach in order to complete all tasks for this
category. For the Combat category, this is the max level of monster you are willing to fight.
General tasks do not have a level and thus do not have this option.
  * **Max [Category] Tasks** - The highest number of tasks in this category you are willing to be assigned.
Note that you can end up with _less_ than this amount, but never more. The "General" category is used to fill remaining
spots so a maximum is not specified, instead it has a _minimum_ count.
  * **[Category] Task Weighting** - The relative weighting of this category to all of the others. Increase this to make 
tasks in this category more likely.

## What does randomization do to this game?
The OSRS Archipelago Randomizer takes the form of a "Chunkman" account, a form of challenge account
where you are limited to specific regions of the map (known as "chunks") until you complete tasks to unlock
more. The plugin will interface with the [Region Locker Plugin](https://github.com/slaytostay/region-locker) to
visually display these chunk borders and highlight them as locked or unlocked. The optional included GPU plugin for the
Region Locker can tint the locked areas gray, but is incompatible with other GPU plugins such as 117's HD OSRS.
If you choose not to include it, the world map will show locked and unlocked regions instead.

In order to access a region, you will need to access it entirely through unlocked regions. At no point are you
ever allowed to cross through locked regions, with the following exceptions:
* If your starting region is not Lumbridge, when you complete Tutorial Island, you will need to traverse locked regions
to reach your intended starting location.
* If your starting region is not Lumbridge, you are allowed to "Home Teleport" to your starting region by using the
Lumbridge Home Teleport Spell and then walking to your start location. This is to prevent you from getting "stuck" after
using one-way transportation such as the Port Sarim Jail Teleport from Shantay Pass and being locked out of progression.
* All of your starting Tutorial Island items are assumed to be available at all times. If you have lost an important
item such as a Tinderbox, and cannot re-obtain it in your unlocked region, you are allowed to enter locked regions to
replace it in the least obtrusive way possible.
* If you need to adjust Group Ironman settings, such as adding or removing a member, you may freely access The Node
to do so.

When passing through locked regions for such exceptions, do not interact with any NPCs, items, or enemies and attempt
to spend as little time in them as possible.

The plugin will prevent equipping items that you have not unlocked the ability to wield. For example, attempting
to equip an Iron Platebody before the first Progressive Armor unlock will display a chat message and will not
equip the item.

The plugin will show a list of your current tasks in the sidebar. The plugin will be able to detect the completion
of most tasks, but in the case that a task cannot be detected (for example, killing an enemy with no
drop table such as Deadly Red Spiders), the task can be marked as complete manually by clicking
on the button. This button can also be used to mark completed tasks you have done while playing OSRS mobile or
on a different client without having the plugin available. Simply click the button the next time you are logged in to
Runelite and connected to send the check.

Due to the nature of randomizing a live MMO with no ability to freely edit the character or adjust game logic or
balancing, this randomizer relies heavily on **the honor system**. The plugin cannot prevent you from walking through
locked regions or equipping locked items with the plugin disabled before connecting. It is important
to acknowledge before starting that the entire purpose of the randomizer is a self-imposed challenge, and there
is little point in cheating by circumventing the plugin's restrictions or marking a task complete without actually
completing it. If you wish to play OSRS with no restrictions, that is always available without the plugin.

In order to access the AP Text Client commands (such as `!hint` or to chat with other players in the seed), enter your
command in chat prefaced by the string `!ap`. Example commands:

`!ap buying gf 100k` -> Sends the message "buying gf 100k" to the server  
`!ap !hint Area: Lumbridge` -> Attempts to hint for the "Area: Lumbridge" item. Results will appear in your chat box.

Other server messages, such as chat, will appear in your chat box, prefaced by the Archipelago icon.

## What items and locations get shuffled?
Items:
- Every map region (at least one chunk but sometimes more)
- Weapon tiers from iron to Rune (bronze is available from the start)
- Armor tiers from iron to Rune (bronze is available from the start)
- Two Spell Tiers (bolt and blast spells)
- Three tiers of Ranged Armor (leather, studded leather + vambraces, green dragonhide)
- Three tiers of Ranged Weapons (oak, willow, maple bows and their respective highest tier of arrows)

Locations:
* Every Quest is a location that will always be included in every seed
* A random assortment of tasks, separated into categories based on the skill required.
These task categories can have different weights, minimums, and maximums based on your options.
  * For a full list of Locations, items, and regions, see the 
[Logic Document](https://docs.google.com/spreadsheets/d/1R8Cm8L6YkRWeiN7uYrdru8Vc1DlJ0aFAinH_fwhV8aU/edit?usp=sharing)

## Which items can be in another player's world?
Any item or region unlock can be found in any player's world.

## What does another world's item look like in Old School Runescape?
Upon completing a task, the item and recipient will be listed in the player's chatbox.

## When the player receives an item, what happens?
In addition to the message appearing in the chatbox, a UI window will appear listing the item and who sent it.
These boxes also appear when connecting to a seed already in progress to list the items you have acquired while offline.
The sidebar will list all received items below the task list, starting with regions, then showing the highest tier of
equipment in each category.