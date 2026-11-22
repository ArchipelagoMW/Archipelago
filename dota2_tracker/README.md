# Dota 2 Archipelago tracker

Two web pages for Dota 2 in Archipelago, which run in your browser:

- `index.html`, the tracker: follows a Dota 2 slot in a multiworld.
- `options.html`, the YAML page: builds a player YAML, with the number of checks and items the seed will have.

## Running it

### Run it on your computer

If someone already hosts the tracker online, just open their link: there is nothing to install. Otherwise, the tracker runs on your computer in a few steps. You only do steps 1 and 2 once.

**1. Install Python** (a free program the tracker uses to show its pages in your browser)

- **Windows**: download the installer from https://www.python.org/downloads/ (the big yellow "Download Python" button) and open it. On its first screen, tick **"Add python.exe to PATH"**, then click **Install Now**.
- **Mac**: download the installer from https://www.python.org/downloads/ and open it, then follow its steps.
- **Linux**: Python is usually already there. If not, install the `python3` package from your distribution's software center.

**2. Download the tracker**

On this repository's GitHub page, click the green **Code** button, then **Download ZIP**. Unzip the file (right-click → Extract All on Windows, double-click on Mac). The tracker is in its `dota2_tracker` folder.

**3. Start it**

Open a terminal in the `dota2_tracker` folder:

- **Windows**: open the folder in the File Explorer, click the address bar at the top, type `cmd` and press Enter.
- **Mac**: open the **Terminal** app (search "Terminal" with Spotlight, ⌘ Space), type `cd ` with a space after it, drag the `dota2_tracker` folder onto the Terminal window, and press Enter.
- **Linux**: right-click inside the folder and choose **Open in Terminal**.

Then type this command and press Enter:

- **Windows**: `py -m http.server 8000`
- **Mac and Linux**: `python3 -m http.server 8000`

**4. Open it in your browser**

Go to http://localhost:8000 for the tracker, or http://localhost:8000/options.html for the YAML page.

Keep the terminal window open while you use the tracker; close it (or press Ctrl+C in it) to stop. Next time, only steps 3 and 4 are needed.

Opening `index.html` directly with a double-click may not work: the page is meant to be served like this to load the game data and your matches.

### Host your own copy (for developers)

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

## Help

Questions and bug reports: the [DOTA 2 Archipelago Discord](https://discord.gg/Xzrx7DcDvm).
