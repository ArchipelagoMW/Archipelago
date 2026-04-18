# Ducks Can Drive — Archipelago Setup Guide

*Ducks Can Drive* is a small free driving game by Joseph Cook. This guide
walks you through installing the client mod, configuring your connection,
and joining an Archipelago multiworld.

## Required software

- **Ducks Can Drive** — free on [Steam](https://store.steampowered.com/app/2472840/Ducks_Can_Drive/).
- **MelonLoader 0.7.x** — mod loader for Unity Mono games. Download from [MelonLoader on GitHub](https://github.com/LavaGang/MelonLoader/releases) (pick the latest `MelonLoader.x64.zip`).
- **DucksAP mod** — the client. Get the latest `DucksAP.dll` from the [DucksAP releases page](https://github.com/sebdevar/ducks-archipelago/releases) (or build it yourself — see the project README).

## Install MelonLoader into the game

1. Find the game's install folder. Default on Windows: `C:\Program Files (x86)\Steam\steamapps\common\Ducks Can Drive\`. You can also right-click the game in Steam → *Manage* → *Browse local files*.
2. Extract the contents of `MelonLoader.x64.zip` directly into that folder so that a `MelonLoader\` directory sits next to `Ducks Can Drive.exe`.
3. Launch the game once. MelonLoader bootstraps itself and creates `Mods\`, `Plugins\`, and `UserData\` subfolders. Close the game.

## Install DucksAP

1. Drop `DucksAP.dll` into the game's `Mods\` folder (created in the previous step).
2. Launch the game once more so MelonLoader generates `UserData\DucksAP.cfg` with default values. Close the game.

## Configure the connection

Open `UserData\DucksAP.cfg` in a text editor. It looks like this:

```toml
[DucksAP]
# Archipelago server URL, e.g. ws://localhost:38281
server = ""
# Slot name configured in the multiworld yaml
slot = ""
# Optional server password
password = ""
```

Fill in the three fields to match the multiworld you're joining, then save.
- For a hosted game, `server` typically looks like `ws://archipelago.gg:38281` (replace the port with the one your tracker shows).
- For a local test, use `ws://localhost:<port>` where `<port>` is whatever `MultiServer.py` is running on.
- `slot` must match the `name:` field in your player YAML.
- Leave `password` empty if the server isn't password-protected.

## Per-slot options

Options you can set in your player YAML (see `StartingMoney` in `options.py`):

- **`starting_money`** — lifetime money budget the mod grants across all city entries for this seed. Default `12500` covers every tier in one sitting; lower values (e.g. `3000`) force you to budget across sessions. Once spent, the pool is empty — you can still earn money from in-session deliveries but it won't carry over.
- **`include_banana`** — off by default. When on, adds the secret Banana Offline track to the seed as a location (and its unlock to the item pool). Banana has no Track Select menu button — the only way into it is to let a time-trial's timer run past 10 minutes without finishing. Leave off unless you specifically want a scavenger-hunt objective in your seed.
- **`include_par_times`** — on by default. The six par-time locations (Duck Circuit under 35s, Lake Loop under 40s, etc.) reward skillful driving. Turn off if you'd rather a gentler seed that only rewards finishing the tracks, not speedrunning them; Rubber Duck filler count scales down automatically to keep the pool balanced.

## Joining a multiworld

1. Launch Ducks Can Drive. The MelonLoader console window pops up alongside the game.
2. Watch the console (or the on-screen message overlay in the top-left) for `Connected to Archipelago`. If connection fails, see **Troubleshooting** below.
3. Play the game normally — see **How the AP integration works** below.

## How the AP integration works

Ducks Can Drive has three in-game systems, all of which feed into Archipelago:

### Upgrades (25 locations)

The garage in the city lets you buy five upgrade tiers for five stats (Speed, Acceleration, Offroad, Boost, Handling). Each tier is one AP location. You'll see the upgrade ladder gated on receiving `Progressive <Stat>` items:

- Having N `Progressive <Stat>` items permits you to buy exactly N tiers of that stat.
- The UI squares for already-earned tiers are painted green on city entry.
- Buying a tier sends the corresponding `Upgrade <Stat> Tier N` check.

Money is a lifetime pool sized by `starting_money`. The mod overwrites the stock game's per-entry $500 with your remaining budget on every city entry.

### Books (8 locations)

The 8 collectible duckbooks (`Book1`..`Book8`) scattered in the city are free-pickup AP locations. No gating — drive into the trigger, get the check.

### Time trials (13 locations)

Each of the 7 offline time-trial tracks has a "Finish `<track>`" AP location, and 6 of them have an additional "Beat par on `<track>`" location (Banana has no par). Tracks are locked until Archipelago delivers the matching `<Track> Unlock` item — locked buttons are greyed out in the Track Select menu.

### Goal

Collecting all 25 `Progressive <Stat>` items is the goal. The mod sends a `CLIENT_GOAL` status update to the server automatically when your inventory fills up.

## On-screen overlay

The top-left of the screen shows recent Archipelago events — connects, item receives, and goal — for about 8 seconds each. It's the quickest way to tell if a check or item went through without alt-tabbing to the MelonLoader console.

## Troubleshooting

- **`[ap] no server URL configured; skipping connect.`** — You haven't edited `UserData\DucksAP.cfg`, or the `server` line is still empty quotes. Add a URL, save, and relaunch.
- **`[ap] <- ConnectionRefused`** — Slot name mismatch, wrong password, or your APWorld version doesn't match what the server expects. Check the tracker page for the correct slot name; re-generate the multiworld if you've bumped the APWorld version.
- **Money feels stuck at \$0 despite unspent deliveries.** — The AP money pool is separate from in-session delivery earnings, and in-session earnings don't persist across city entries. If `starting_money` is spent, further city entries start you at $0 from the AP side; you have to grind deliveries each session.
- **Buttons in the Track Select menu are greyed out.** — That's intended — you haven't received the matching `<Track> Unlock` item yet. Keep playing; checks in the city will eventually deliver them.
- **Garage tier squares don't turn green until I buy.** — Leaving and re-entering the city should re-paint them from your AP inventory. If it still doesn't, the squares will at least fill in as you buy each tier.

## Reporting issues

Please include your `MelonLoader\Latest.log` (or the most recent log under `MelonLoader\Logs\`) when filing an issue, plus the contents of `UserData\DucksAP.cfg`. Don't share server passwords.
