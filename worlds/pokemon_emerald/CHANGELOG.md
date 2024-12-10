# 2.3.0

### Features

- Added a Swedish translation of the setup guide.
- The client communicates map transitions to any trackers connected to the slot.
- Added the player's Normalize Encounter Rates option to slot data for trackers.

### Fixes

- Fixed a rare issue where receiving a wonder trade could partially corrupt the save data, preventing the player from
receiving new items.
- Fixed the client spamming the "goal complete" status update to the server instead of sending it once.
- Fixed the `trainer_party_blacklist` option checking for the existence of the "_Legendaries" shortcut in the
`starter_blacklist` option instead of itself.
- Fixed a logic issue where the "Mauville City - Coin Case from Lady in House" location only required a Harbor Mail if
the player randomized NPC gifts.
- The Dig tutor has its compatibility percentage raised to 50% if the player's TM/tutor compatibility is set lower.
- A Team Magma Grunt in the Space Center which could become unreachable while trainersanity is active by overlapping
with another NPC was moved to an unoccupied space.
- Fixed a problem where the client would crash on certain operating systems while using certain python versions if the
player tried to wonder trade.
- Prevent the poke flute sound from replacing the evolution fanfare, which would cause the game to wait in silence for
a long time during the evolution scene.

# 2.2.0

### Features

- When you blacklist species from wild encounters and turn on dexsanity, blacklisted species are not added as locations
and won't show up in the wild. Previously they would be forced to show up exactly once.
- Added support for some new autotracking events.
- Updated option descriptions.
- Added `full` alias for `100` on TM and HM compatibility options.

### Fixes

- The Lilycove Wailmer now logically block you from the east. Actual game behavior is still unchanged for now.
- Water encounters in Slateport now correctly require Surf.
- Mirage Tower can no longer be your only logical access to a species in the wild, since it can permanently disappear.
- Updated the tracker link in the setup guide.

# 2.1.1

### Features

- You no longer need a copy of Pokemon Emerald to generate a game, patch files generate much faster.

# 2.1.0

_Separately released, branching from 2.0.0. Included procedure patch migration, but none of the 2.0.1 fixes._

# 2.0.1

### Fixes

- Changed "Ho-oh" to "Ho-Oh" in options.
- Temporary fix to alleviate problems with sometimes not receiving certain items just after connecting if `remote_items`
is `true`.
- Temporarily disable a possible location for Marine Cave to spawn, as it causes an overflow.
- Water encounters in Dewford now correctly require Surf.

# 2.0.0

### Features
- Picking up items for other players will display the actual item name and receiving player in-game instead of
"ARCHIPELAGO ITEM". (This does have a limit, but you're unlikely to reach it in all but the largest multiworlds.)
- New goal `legendary_hunt`. Your goal is to catch/defeat some number of legendary encounters. That is, the static
encounters themselves, whatever species they may be. Legendary species found in the wild don't count.
    - You can force the goal to require captures with `legendary_hunt_catch`. If you accidentally faint a legendary, you
    can respawn it by beating the champion.
    - The number of legendaries needed is controlled by the `legendary_hunt_count` option.
    - The caves containing Kyogre and Groudon are fixed to one location per seed. You need to go to the weather
    institute to trigger a permanent weather event at the corresponding locations. Only one weather event can be active
    at a time.
    - The move tutor for the move Sleep Talk has been changed to Dig and is unlimited use (for Sealed Chamber).
    - Relicanth and Wailord are guaranteed to be reachable in the wild (for Sealed Chamber). Interacting with the Sealed
    Chamber wall will give you dex info for Wailord and Relicanth.
    - Event legendaries are included for this goal (see below for new ferry behavior and event tickets).
    - The roamer is included in this count. It will _always_ be Latios no matter what your options are. Otherwise you
    might not have any way of knowing which species is roaming to be able to track it. In legendary hunt, Latios will
    never appear as a wild pokemon to make tracking it easier. The television broadcast that creates the roamer will
    give you dex info for Latios.
    - You can set which encounters are considered for this goal with the `allowed_legendary_hunt_encounters` option.
- New option `dexsanity`. Adds pokedex entries as locations.
    - Added locations contribute either a Poke Ball, Great Ball, or Ultra Ball to the item pool, based on the evolution
    stage.
    - Logic uses only wild encounters for now.
    - Defeating a gym leader awards "seen" info on 1/8th of the pokedex.
- New option `trainersanity`. Defeating a trainer awards a random item.
    - Trainers no longer award money upon defeat. Instead they add a sellable item to the item pool.
    - Missable trainers are prevented from disappearing when this is enabled.
    - Gym trainers remain active after their leader is defeated.
    - Does not include trainers in the Trick House.
- New option `berry_trees`. Adds berry trees as locations.
    - All soil patches start with a fully grown berry tree that gives one item.
    - There are 88 berry trees.
    - Berries cannot be planted in soil with this option enabled.
    - Soil that doesn't start with a tree on a fresh save contributes a Sitrus Berry to the item pool.
- New option `death_link`. Forgive me, Figment.
- Added Artisan Cave locations
    - Requires Wailmer Pail and the ability to Surf to access.
- Added Trick House locations. The Trick Master is finally here!
    - He will make new layouts only if you have the corresponding badge (or beat the game) and have completed the
    previous layout (all vanilla behavior).
    - If you neglect to pick up an item in a puzzle before completing it, the Trick Master will give the item to you
    alongside the prize.
    - Locations are enabled or disabled with their broader categories (npc gifts, overworld items, etc...)
- Added daily berry gift locations. There are a half dozen or so NPCs that give you one or two berries per day.
    - All these locations are considered NPC gifts.
    - The NPCs have been reworked to give this gift once permanently so they can be added as locations.
- New option `remote_items`. All randomized items are sent from the server instead of being patched into your game
(except for start inventory, which remains in the PC)
    - As a side effect, when you pick up your own item, there will be a gap between the item disappearing from the
    overworld and your game actually receiving it. It also causes gifts from NPCs which contain your own items to not
    show up until after their text box closes. It can feel odd, but there should be no danger to it.
    - If the seed is in race mode, this is forcibly enabled.
    - Benefits include:
        - Two players can play the same slot and both receive items that slot picks up for itself (as long as it was
        randomized)
        - You receive items you picked up for yourself if you lose progress on your save
        - Competitive integrity; the patch file no longer has any knowledge of item placement
- New option `match_trainer_levels`. This is a sort of pseudo level cap for a randomizer context.
    - When you start a trainer fight, all your pokemon have their levels temporarily set to the highest level in the
    opponent's party.
    - During the battle, all earned exp is set to 0 (EVs are still gained during battle as normal). When the outcome of
    the battle is decided, your pokemon have their levels reset to what they were before the fight and exp is awarded as
    it would have been without this option. Think of it as holding earned exp in reserve and awarding it at the end
    instead, even giving it to fainted pokemon if they earned any before fainting.
    - Exp gain is based on _your_ party's average level to moderate exp over the course of a seed. Wild battles are
    entirely unchanged by this option.
- New option `match_trainer_levels_bonus`. A flat bonus to apply to your party's levels when using
`match_trainer_levels`. In case you want to give yourself a nerf or buff while still approximately matching your
opponent.
- New option `force_fully_evolved`. Define a level at which trainers will stop using pokemon that have further evolution
stages.
- New option `move_blacklist`. Define a list of moves that should not be given randomly to learnsets or TMs. Move names
are accurate to Gen 3 except for capitalization.
- New option `extra_bumpy_slope`. Adds a "bumpy slope" to Route 115 that lets you hop up the ledge with the Acro Bike.
- New option `modify_118`. Changes Route 118 so that it must be crossed with the Acro Bike, and cannot be crossed by
surfing.
- Changed `require_flash` option to a choice between none, only granite cave, only victory road, or both caves.
- Removed `static_encounters` option.
- New option `legendary_encounters`. Replaces `static_encounters`, but only concerns legendaries.
- New option `misc_pokemon`. Replaces `static_encounters`, but only concerns non-legendaries.
- Removed `fly_without_badge` option. (Don't worry)
- New option `hm_requirements`. Will eventually be able to give you more control over the badge requirements for all
HMs. For now, only includes the presets `vanilla` and `fly_without_badge`.
- Removed `allow_wild_legendaries`, `allow_starter_legendaries`, and `allow_trainer_legendaries` options.
- New options `wild_encounter_blacklist`, `starter_blacklist`, and `trainer_party_blacklist`.
    - These take lists of species and prevent them from randomizing into the corresponding categories
    - If adhering to your blacklist would make it impossible to choose a random species, your blacklist is ignored in
    that case
    - All three include a shorthand for excluding legendaries
- Removed `enable_ferry` option.
    - The ferry is now always present.
    - The S.S. Ticket item/location is now part of `key_items`.
- Added event tickets and islands.
    - All event tickets are given to the player by Norman after defeating the Champion alongside the S.S. Ticket.
    - As in vanilla, these tickets are only usable from Lilycove. Not Slateport or the Battle Frontier.
- New option `event_tickets`. Randomizes the above-mentioned tickets into the item pool.
- New option `enable_wonder_trading`. You can participate in Wonder Trading by interacting with the center receptionist
on the second floor of Pokemon Centers.
    - Why is this an option instead of just being enabled? You might want to disable wonder trading in a meta yaml to
    make sure certain rules can't be broken. Or you may want to turn it off for yourself to definitively prevent being
    asked for help if you prefer to keep certain walls up between your game and others. Trades _do_ include items and
    known moves, which means there is potential for an extra level of cooperation and even ways to go out of logic. But
    that's not a boundary everyone wants broken down all the time. Please be respectful of someone's choice to not
    participate if that's their preference.
    - A lot of time was spent trying to make this all work without having to touch your client. Hopefully it goes
    smoothly, but there's room for jank. Anything you decide to give to her you should consider gone forever, whether
    because it was traded away or because something "went wrong in transit" and the pokemon's data got lost after being
    removed from the server.
    - Wonder Trading is _not_ resistant to save scumming in either direction. You _could_ abuse it to dupe pokemon,
    because there's not realistically a way for me to prevent it, but I'd urge you to stick to the spirit of the design
    unless everyone involved doesn't mind.
    - The wonder trades you receive are stored in your save data even before you pick them up, so if you save after the
    client tells you that you received a wonder trade, it's safe. You don't need to retrieve it from a poke center for
    it to persist. However, if you reset your game to a point in time before your client popped the "Wonder trade
    received" message, that pokemon is lost forever.
- New `easter_egg` passphrase system.
    - All valid easter egg passphrases will be a phrase that it's possible to submit as a trendy phrase in Dewford Town.
    Changing the trendy phrase does ***not*** trigger easter eggs. Only the phrase you put in your YAML can trigger an
    easter egg.
    - There may be other ways to learn more information.
    - Phrases are case insensitive. Here are a couple examples of possible phrases: `"GET FOE"`,
    `"HERE GOES GRANDMOTHER"`, `"late eh?"` (None of those do anything, but I'd love to hear what you think they would.)  
- Added three new easter egg effects.
- Changed the original easter egg phrase to use the new system.
- Renamed `tm_moves` to `tm_tutor_moves`. Move tutors are also affected by this option (except the new Dig tutor).
- Renamed `tm_compatibility` to `tm_tutor_compatibility`. Move tutors are also affected by this option.
- Changed `tm_tutor_compatibility` to be a percent chance instead of a choice. Use `-1` for vanilla.
- Changed `hm_compatibility` to be a percent chance instead of a choice. Use `-1` for vanilla.
- New option `music`. Shuffles all looping music. Includes FRLG tracks and possibly some unused stuff.
- New option `fanfares`. Shuffles all fanfares. Includes FRLG tracks. When this is enabled, pressing B will interrupt
most fanfares.
- New option `purge_spinners`. Trainers that change which direction they face will do so predictably, and will no longer
turn to face you when you run.
- New option `normalize_encounter_rates`. Sets every encounter slot to (almost) equal probability. Does NOT make every
species equally likely to appear, but makes rare encounters less rare.
- Added `Trick House` location group.
- Removed `Postgame Locations` location group.
- Added a Spanish translation of the setup guide.

### QoL

- Can teach moves over HM moves.
- Fishing is much less random; pokemon will always bite if there's an encounter there.
- Mirage Island is now always present.
- Waking Rayquaza is no longer required. After releasing Kyogre, going to Sootopolis will immediately trigger the
Rayquaza cutscene.
- Renamed some locations to be more accurate.
- Most trainers will no longer ask to be registered in your Pokegear after battle. Also removed most step-based match
calls.
- Removed a ledge on Route 123. With careful routing, it's now possible to check every location without having to save
scum or go back around.
- Added "GO HOME" button on the start menu where "EXIT" used to be. Will teleport you to Littleroot.
- Some locations which are directly blocked by completing your goal are automatically excluded.
    - For example, the S.S. Ticket and a Champion goal, or the Sludge Bomb TM and the Norman goal.
    - Your particular options might still result in locations that can't be reached until after your goal. For example,
    setting a Norman goal and setting your E4 requirement to 8 gyms means that post-Champion locations will not be
    reachable before defeating Norman, but they are NOT excluded by this modification. That's one of the simpler
    examples. It is extremely tedious to try to detect these sorts of situations, so I'll instead leave it to you to be
    aware of your own options.
- Species in the pokedex are searchable by type even if you haven't caught that species yet

### Fixes

- Mt. Pyre summit state no longer changes when you finish the Sootopolis events, which would lock you out of one or two
locations.
- Whiting out under certain conditions no longer softlocks you by moving Mr. Briney to an inaccessible area.
- It's no longer possible to join a room using the wrong patch file, even if the slot names match.
- NPCs now stop moving while you're receiving an item.
- Creating a secret base no longer triggers sending the Secret Power TM location.
- Hopefully fix bug where receiving an item while walking over a trigger can skip that trigger (the Moving
Truck/Petalburg wrong warp)

## Easter Eggs

There are plenty among you who are capable of ~~cheating~~ finding information about the easter egg phrases by reading
source code, writing brute force scripts, and inspecting memory for clues and answers. By all means, go ahead, that can
be your version of this puzzle and I don't intend to stand in your way. **However**, I would ask that any information
you come up with by doing this, you keep entirely to yourself until the community as a whole has figured out what you
know. There was not previously a way to reasonably learn about or make guesses at the easter egg, but that has changed.
There are mechanisms by which solutions can be found or guessed over the course of multiple games by multiple people,
and I'd rather the fun not get spoiled immediately.

Once a solution has been found I'd _still_ prefer discussion about hints and effects remain behind spoiler tags just in
case there are people who want to do the hunt on their own. Thank you all, and good luck.
