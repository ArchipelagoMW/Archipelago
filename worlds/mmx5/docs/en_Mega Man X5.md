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

Three options:

- **all_mavericks** (default) — defeat all 8 Mavericks, then reach and defeat
  Sigma. Mega Man X5 does not normally require the full set: it opens the
  endgame as soon as the Eurasia colony situation resolves, which can happen
  well before the eighth Maverick. Under this goal the endgame stays shut
  until all eight are down and opens on the eighth kill. This is enforced by
  the client, so it needs no disc change.
- **sigma** — defeat Sigma, however you got there. Victory is detected from the
  ending itself, so the credits rolling completes your goal, whether or not you
  fought every Maverick.
- **launch** — collect all 8 Enigma/Shuttle Parts and complete a successful
  launch. By default the launch succeeds exactly when every part is in hand and
  partial sets always fail; see `launch_odds` if you would rather gamble.

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
- **Boss difficulty is an option.** X5 scales bosses with a "Boss Level" taken
  from the hours left on the colony countdown, and the randomizer freezes that
  countdown — so `boss_difficulty` picks what it freezes at. **relaxed** is 17
  hours (starting level 1), **standard** is 8 hours (level 9, the default), and
  **intense** is 1 hour (level 17). Fewer hours means a *higher* level, because
  the game ramps up as the crisis deepens. It scales boss HP rather than their
  attack patterns, and it decides which reward a boss gives in the original
  game — level 4+ offers the Life/Energy Up choice, level 8+ upgrades it and
  adds a Part. Bosses keep getting stronger either way as you collect Mavericks
  and weapons; this only sets the starting point, and no setting can make a
  seed unbeatable.
- **`launch_odds` decides whether a launch is a sure thing.** By default it
  succeeds exactly when you hold all 8 Enigma and Shuttle Parts and fails
  otherwise. Set it to **vanilla** and the original game's gamble comes back:
  the Enigma is 6.25% with no parts and 12.5% with any (extra Enigma parts do
  nothing in the original either), and the Shuttle is 12.5% / 37.5% / 75% for
  0, 1–2, and 3–4 parts.
  **Under the `launch` goal, vanilla odds can make a seed unwinnable** — that
  goal needs a successful launch, you get two attempts, and a full part set is
  still only 75%. Fail both and the colony falls with no third chance. The
  combination is allowed on purpose and warns at generation. Under
  `all_mavericks`, no launch can succeed before all 8 Mavericks are down
  whatever this is set to, or an early success would open the endgame ahead of
  the goal.
- **`text_skip` makes dialogue get out of the way.** X5 types text out one
  character every 5 frames and then waits for a button on every box — a single
  line can run past 200 characters, roughly 20 seconds before you can even
  press advance. With this on, boxes appear instantly and advance themselves,
  so cutscenes and Alia's in-stage calls play through without input.
  **Choices are not skipped**: Alia's Life Up / Energy Up prompt still stops
  and waits for you to pick, and the Enigma/Shuttle launch decision is a
  stage-select menu that this does not touch. Nothing that affects your run is
  answered for you. You will not be able to read the story at this speed, so
  leave it off for a first playthrough.
- **Checks appear a few seconds after a boss dies**, not instantly — the game
  commits the kill shortly after the results screen.
- **"Small Energy" filler items do nothing in-game** — they pad the item pool
  when there are more locations than real items.
- **The Enigma/Shuttle parts screen lies to you.** It shows parts the original
  game hands out for beating Mavericks, not the ones Archipelago sent you.
  Only the parts you actually received count toward the **launch** goal, and
  the client will tell you your real count in its log. Under the launch goal
  the story's own shuttle launch — which happens automatically once all eight
  Mavericks are down — does **not** finish your run; you still need all 8
  parts.
