# Mega Man X5

## What does randomization do to this game?

Weapons, armor parts, tanks and Heart Tanks are shuffled into the multiworld
item pool. You start with nothing but your buster, and every Maverick weapon,
armor piece and tank arrives as a multiworld item — possibly from someone
else's game.

All eight Maverick stages are open from the start, exactly as in vanilla, so
routing is yours to decide. The collision countdown is frozen, so there is no
time pressure and you can revisit stages freely once you have the items to
reach what you missed.

## What is the goal?

Two options:

- **sigma** (default) — reach and defeat Sigma. Victory is detected from the
  ending itself, so the credits rolling completes your goal.
- **launch** — collect all 8 Enigma/Shuttle Parts and complete a successful
  launch. The launch only succeeds once every part is in hand; partial sets
  fail, vanilla-style.

## What items and locations get shuffled?

**Items (36):** the 8 special weapons, 8 Heart Tanks, 2 Sub-Tanks, the W-Tank,
the EX-Tank, all 8 armor parts (Falcon and Gaea sets), and 4 Enigma + 4 Shuttle
launcher parts.

**Locations (45):** the intro stage, plus per Maverick stage — the boss, its
Heart Tank, its armor capsule, its DNA reward and its DNA Part — plus the four
tank pickups.

Beating a Maverick checks **three** locations at once (boss, DNA reward, DNA
Part), because vanilla grants three rewards for a boss kill: the weapon, the
Life/Energy upgrade, and an equippable Part.

## What does another world's item look like in Mega Man X5?

There is no in-game item display. Checks are detected and items delivered by
the Archipelago client while the game runs in BizHawk. Received items are
written straight into your save data: weapons become usable immediately, Heart
Tanks raise max HP for both characters, tanks appear in the pause menu, and a
complete armor set unlocks at character select after the next results screen.

## Anything unusual I should know?

- **Armor capsules still play Light's dialogue but grant nothing.** That is
  correct — the capsule is the *check*; the armor part itself comes from the
  multiworld. You must walk fully into a capsule, not merely stand beside it,
  or the sequence will not start.
- **Boss difficulty is an option.** Boss Level in X5 scales with the time
  remaining on the countdown, and since that countdown is frozen, the
  `boss_difficulty` option decides what the fixed base is. Bosses still get
  stronger as you defeat more Mavericks and collect more weapons.
- **Checks appear a few seconds after a boss dies**, not instantly — the game
  commits the kill shortly after the results screen.
- **"Small Energy" filler items do nothing in-game** — they pad the item pool
  when there are more locations than real items.
