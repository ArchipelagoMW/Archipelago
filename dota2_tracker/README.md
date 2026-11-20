# Dota 2 Archipelago tracker

Two static web pages for Dota 2 in Archipelago, with nothing to install:

- `index.html`, the tracker: follows a Dota 2 slot in a multiworld.
- `options.html`, the YAML page: builds a player YAML, with the number of checks and items the seed will have.

## Running it

### Run it on your computer

You need Python 3. From the repository root:

```
python -m http.server 8000 --directory dota2_tracker
```

(`py` instead of `python` on Windows), then open http://localhost:8000 for the tracker, or http://localhost:8000/options.html for the YAML page. Stop the server with Ctrl+C.

Serve the folder over HTTP like this rather than opening the files directly: the pages load the game data and OpenDota with web requests.

### Host your own copy

Any static host works. GitHub Pages only serves a branch's root or its `docs` folder, so put `index.html` and `options.html` at the root of the branch Pages serves (with an empty `.nojekyll` file), then choose that branch in the repository's Settings > Pages.

## Using the tracker

1. Fill in the settings:
   - **Room link or server**: the room page link on archipelago.gg, or a server address like `host:port`.
   - **Slot name**: your player name in the multiworld.
   - **Room password**: only if the room has one.
   - **Steam account ID**: the number you gave the client with `/set_player_id` (the 64-bit SteamID works too). The page's help explains where to find it.
   - **Seed start date**: matches before it are not shown.
   - **Client save** (optional): `Archipelago/saves/dota2/DOTA2__<seed>__<slot>.json`, for your exact wins and heroes won instead of an estimate.
2. Click **Show my tracker**.
3. **Copy link** gives an address with your settings, to bookmark or open on another device. The password is never put in it.

## What it shows

- Goal progress: unique heroes won, wins and Primordial Fragments.
- Heroes: playable heroes with their group, attribute, attack type, legs and role, with filters and the heroes already won.
- Checks: wins by group, stats, match challenges, quests and item purchases. Purchases you can make, with all their components unlocked, are highlighted.
- Components unlocked, and the items received, with who sent them.
- Matches since the seed start, from OpenDota. For each match, the page deduces whether `/parse_recent_match` read it, from the checks done on the server.

## How it works

- Archipelago server: the page connects as a read-only tracker (`Tracker` tag), so it never sends checks. A sleeping archipelago.gg room is woken up, and its new port is found with the `room_status` API.
- Game data: heroes, shop items and damage types come from this repository's `worlds/dota_2/data` files, so the pages follow the apworld's updates.
- Matches and stats: OpenDota's public API. Parsed match details are cached in the browser.
- Progress: estimated from OpenDota by default, or exact from the client save.

Settings stay in the browser. The YAML page keeps your choices in the browser too.
