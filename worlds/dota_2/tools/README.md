# Updating the DOTA 2 apworld after a game update

When Valve adds, removes or changes items or heroes:

1. From the repository root, run `python -m worlds.dota_2.tools.update_data`. It reads OpenDota's constants and:
   - adds new shop items, their components ("Unlock ..." items) and new heroes;
   - follows recipe changes;
   - refreshes ability damage types;
   - gives ids to the new names in `data/ids.json`.

   It never overwrites what was set by hand: hero roles, and `data/shopOverrides.json`.
2. Read the summary it prints:
   - **Items Valve removed**: OpenDota keeps them, so add them to `exclude` in `data/shopOverrides.json` and run it again.
   - **A new hero**: check its roles in `data/heroes.json` (Carry or Support decide the role wins).
   - **A recipe OpenDota gets wrong**: set its components in `requirements` of `data/shopOverrides.json`.
3. Raise `world_version` in `archipelago.json`.
4. Run the tests: `python -m pytest worlds/dota_2/test`.

## Seeds in progress

Ids never move (`data/ids.json`), so seeds made before the update keep working with the new client:

- checks of items the game no longer has are sent for the player on connection;
- a component unlock added since doesn't block a purchase;
- heroes added since aren't in the seed;
- the client says when the seed was made with another `world_version`.

With an older client, a check that can no longer be done can be sent by the room's host with
`/send_location <player> <location>`, or with `!release` once the goal allows it.
