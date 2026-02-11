# Welcome to Sonic 1, 1991, with bonus features.

## What you need to know about the Archipelago mode

- The location checks for this game are every monitor, all six bosses and all six special zones.
- This world will add to the item pool 6 emeralds, 14 keys, 2 buff items (more on those in a moment), rings, and filler.
- There are 6 keys for the normal zones, 1 for the Final Zone, 1 for Specials access, and 6 for the special stages themselves.
- The player will start with the Specials access key and one random normal zone key unlocked, the remaining 12 are in the pool.
- The 195 possible rings are split into 10 classed as Useful and 185 classed as Filler, the hope is that this will balance the distribution.
- To complete the world you need to complete the 6 specials, 6 bosses, get the 6 emeralds in the pool, and some amount of the pool rings.
- The number of rings added to the pool is set by an option, the remaining item slots will contain junk items.

## What changes to Sonic 1 you need to know about

- To make this sane to play you start in level select and get kicked back there after a level.
- Monitor breaking is persistent and all of them are now ring boxes.  This will slightly increase difficulty.
- Special stages will play in order, you won't move on to the next until you pass one.
- If you take damage and when you enter a level the mod will treat your AP received Ring count as your minimum instead of 0.
- With the AP ring gift, you can survive any damage that would make you drop rings, like you immediately pick up additional rings.
- To save rom space, Sonic hurt from an enemy will drop 6 rings and reset to the AP count as long as you have at least 1 ring.
- You are not immune to instant deaths like squishing, time out and drowning.
- Spikes floors are potentially more dangerous, they can lock you into a bounce loop instead of killing you.
- Pause a level and press C to exit back to level select.
- A basic spin dash has been added to make life a little less miserable.
- You don't lose lives when dying, since it makes no sense in this context.
- Repeating a boss doesn't give you extra rewards.
- You don't gain extra lives for 100 rings, but you can't lose lives either.
- Completing a stage with 50 rings won't spawn a giant ring due to progression gating.
- Completing acts 2 or 3 of Scrap Brain won't advance you to the next zone.
- You start with a random zone unlocked, further zone unlocks are via keys in other players' pools
- The 50 ring secret upper path on SBZ2 is disabled as there are no checks up there.
- Special stage buffs:  The UP block is disabled, no speeding up.  Goal and R blocks can be disabled using the two buff items in the pool.
- ReadySonic's "Roll into Catakiller" fix has been included, so you can kill them by rolling into them.
- ReadySonic's "High speed camera fix" has also been included to hopefully make things a little safer.

## Setup

- The supplied patch is applied against the Sonic 1 world REV0 release (`Sonic The Hedgehog (W) (REV00)`)
- Downgrade patches are also supplied, if you need to turn REV1 into REV0.
- The game state is tracked via SRAM, this includes the game seed to keep stale saves from messing up new runs.
- It is recommended, if you have save data from a previous attempt, to use the `RESET SAVE` level select option before connecting to the server.
- Resetting mid run will result in the client writing the progress that has been received from the AP server.
- The level select will currently only rerender the progress indicators when you press an input button, just press up or down after reset.
- The server reapplying saved progress (after a save reset) while in a level may result in problems, it's strongly advised to avoid doing so.
- The most likely bug I've missed from patching is some oddity in how rings are reset after taking damage.  Let me know if you can get silly numbers consistently.

## TODO/Missing features

- The code will probably need a little cleanup.
- Worth adding item received messages via BizHawk Client's message feature?  Feedback welcome on that