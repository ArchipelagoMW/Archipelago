# Welcome to Sonic 1, 1991, with bonus features.

## What you need to know about the Archipelago mode

- The location checks for this game are every monitor, all six bosses and all six special zones.
- Rings placed in the world are not checks, collect or ignore as you want.  All referenences to rings are talking about AP items.
- This world will add to the item pool 6 emeralds, some level keys, 2 buff items (more on those in a moment), rings, and filler.
- There are 6 keys for the normal zones, 1 for the Final Zone, and 6 for the special stages.  Special stages are **progressive** unlock, based on how many special stage keys you have.
- The player will start with one random normal zone key unlocked, the remaining keys are in the pool.
- Exact initial keys can be configured in YAML.
- The pool rings are split into the goal count number of Shiny Rings (progression) and the remaining pool are Gold Rings (useful).
- To complete the world you need to (by default) beat the 6 specials, 6 bosses, get 6 emeralds in the pool, and get some amount of the pool rings.
- The those goals can be changed via yaml options.
- The number of rings added to the pool is set by an option, the remaining item slots will contain junk items.
- You won't be able to enter any levels until the BizHawk client has connected to the AP server.  It needs to receive the room info.  You'll know because there will be no arrows lit up.

## Required Software

- This world uses the BizHawk client, thus the usual instructions apply.
- Archipelago launcher with this world, it can't track your game otherwise.
- A Sonic The Hedgehog 16 bit (1991) ROM file.  We can't help you acquire this, please don't ask. You need one of the following:
    - Sonic The Hedgehog Revision 0 - This is the original world wide release cart.
    - Sonic The Hedgehog Revision 1 - This is the updated cart released in Japan.
    - Sega Classics SONIC_w.68K - This is actually just the rev1 ROM with an odd name.
    - Sonic The Hedgehog GameCube Edition - This is almost the same as rev1 so it's close enough.

## Tracker support

- Universal Tracker is supported, just requires having both worlds on the same launcher.
- Pop Tracker is supported, you can load the tracker directory or download the packaged .poptracker.zip file.

Both have working auto tracking and map following, just connect to your AP game.

## World options

The generation options are suitably documented.  Some specific notes:
- If you want to generate a solo world be sure that "No local key placement" isn't enabled.
- Ring Goal specifies the number of ring items you need to collect from the item pool.
- Available Rings specifies how many rings items are added to the item pool.
- If Available is lower than the Goal, Ring Goal will be set to the value of Available Rings.
- The Ring Goal won't pose much of a challenge in a normal game, you can tweak these settings to make things much harder.
- The default difficulty is tuned to the assumption you will need to check most monitors in a reasonable amount of time.
- The Boring Filler option is there to disable the joke filler items.  All (non-functional) junk items have "(Junk)" in the name.
- The advanced option final_zone_last can delay access to FZ so that it is the last thing to do:
  - **Anytime:** You can do Final Zone as soon as you have the key.
  - **Last But Optional:** If your victory conditions can be achieved without beating Final Zone you skip it.
  - **Always Last:** Final Zone unlocks once you have every other victory condition, beat it to win.
- Note that this may change how certain mechanics behave:
  - "Always Last" essentially forces the boss goal to be at least 1, "Last But Optional" will not.
  - Both "Always Last" and "Last But Optional" will add the Final Zone key to your starting inventory.
  - "Always Last" and "Last But Optional" are identical with 6 bosses.
  - An example of less than 6: "Always Last" with 3 bosses will require any 2 of the Act 3 bosses then FZ, "Last But Optional" requires any 2 of the Act 3 bosses then either FZ or a third Act 3 boss.

Example YAML using default values:
```yaml
Sonic the Hedgehog 1:
  # Add extra keys by name, eg: 'Green Hill Key'
  starting_zone:
    ['Random']
  # Restrict local placement rules to force this world's keys to be placed in other worlds.
  no_local_keys: false
  # Enable the buff items
  allow_disable_goal: true
  allow_disable_r: true
  # Number of rings sent to the pool
  available_rings: 150
  # Number of rings you need from the pool for victory
  ring_goal: 100
  # Number of bosses you need to beat
  boss_goal: 6
  # Number of Specials you need to beat
  specials_goal: 6
  # Number of emeralds you need to receive
  emerald_goal: 6
  # Control when Final Zone can unlock, wait until all other victory conditions are met
  final_zone_last: anytime
  # When enabled, AP won't give you safety rings and you only drop 6 when hurt.
  hard_mode: false
  # Enable to remove the fun junk items
  boring_filler: false
  # How many of each powerup to put in pool, set to 0 to disable completely
  pow_invinc: 5
  pow_shield: 5
  pow_speeds: 5
  # When enabled the speed shoes are filled as a trap item instead of a useful item.
  pow_ss_trap_flag: true
  # Enable this to send deathlink packets when you die
  send_death: false
  # Enable this to die when deathlink packets are received
  recv_death: false
```

## What changes to Sonic 1 you need to know about

- Progression:
    - To make this sane to play you start in level select and get kicked back there after a level.
    - Monitor breaking is persistent and all of them are now ring boxes.  This will slightly increase difficulty.
    - Special stages will play in order, you won't move on to the next until you pass one.
    - You (by default) start with a random zone unlocked, further zone unlocks are via keys in other players' pools
- Rings and damge:
    - If you take damage and when you enter a level the mod will treat your AP received Ring count as your minimum instead of 0.
    - With the AP ring gift, you can survive any damage that would make you drop rings, like you immediately pick up rings.
    - The AP ring gift can be disabled during world gen.
    - To save rom space, Sonic hurt from an enemy will drop 6 rings and reset to the AP count as long as you have at least 1 ring.
    - You are not immune to instant deaths like squishing, time out and drowning.
    - Spikes floors are potentially more dangerous, they can lock you into a bounce loop instead of killing you.
    - You don't lose lives when dying, since it makes no sense in this context.
- Helping:
    - Pause a level and press C to exit back to level select.
    - A basic spin dash has been added to make life a little less miserable.
    - The 50 ring secret upper path on SBZ2 is disabled as there are no checks up there.
    - Special stage buffs:  The UP block is disabled, no speeding up.  Goal and R blocks can be disabled using buff items in the pool.
    - ReadySonic's "Roll into Catakiller" fix has been included, so you can kill them by rolling into them.
    - ReadySonic's "High speed camera fix" has also been included to hopefully make things a little safer.
- Rewards:
    - Repeating a boss doesn't give you extra rewards.
    - You don't gain extra lives for 100 rings, but you can't lose lives either.
    - Completing a stage with 50 rings won't spawn a giant ring due to progression gating.
    - Completing acts 2 or 3 of Scrap Brain won't advance you to the next zone.

## FAQ

- If the log says the seeds don't match, navigate down to Reset Save and choose it, that'll reset the SRAM for the client to redo setup.
- If the log isn't giving messages and you still don't have the starting keys, make sure you're connected to the server.
- Using the disconnect/connect button in the Bizhawk Client to reconnect without closing Bizhawk might help if the initial setup failed.
- If you're still having issues, please provide a screenshot of the log window to Discord.
- Yes, the monitor in credits is known and intentional... it's an easter egg.
