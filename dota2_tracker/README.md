# Dota 2 Archipelago tracker

A web page that tracks a Dota 2 slot in an Archipelago multiworld, with nothing to install. It is a single static file, `index.html`, that runs in the browser.

## What it shows

- Goal progress: unique heroes won, wins and Primordial Fragments.
- Heroes: playable heroes with their group, attribute, attack type, legs and role, with filters and the heroes already won.
- Checks: wins by group, match objectives and item purchases. Purchases you can make, with all their components unlocked, are highlighted.
- Components unlocked, and the items received, with who sent them.
- Matches since the seed start, from OpenDota. For each match, the page deduces whether `/parse_recent_match` read it, from the checks done on the server.

## How it works

- Archipelago server: the page connects as a read-only tracker (`Tracker` tag), so it never sends checks. A sleeping archipelago.gg room is woken up, and its new port is found with the `room_status` API.
- Game data: heroes and shop items come from this repository's `worlds/dota_2/data` files, so the page follows the apworld's updates.
- Matches and stats: OpenDota's public API. Parsed match details are cached in the browser.
- Progress: estimated from OpenDota by default. Loading the client save (`Archipelago/saves/dota2/DOTA2__<seed>__<slot>.json`) gives the exact wins and heroes won.

Settings (room, slot, Steam account ID, seed start date) stay in the browser and are also put in the page address, so the tracker can be bookmarked or shared. The room password is only kept in the browser, never in the address.

## Hosting

Any static host works, for example GitHub Pages. To try it locally, serve the folder over HTTP:

```
python -m http.server 8000 --directory dota2_tracker
```

then open http://localhost:8000.
