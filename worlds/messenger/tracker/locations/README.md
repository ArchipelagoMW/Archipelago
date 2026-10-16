# Messenger Tracker Locations JSON Structure

This folder contains one JSON file per region (for example `AutumnHills.json`, `BambooCreek.json`).

## Expected top-level shape

Each file must be a JSON array with this structure:

1. **Overworld node** for the region  
2. **Key locations group**  
3. **Power Seals group**  
4. **Mega Shards group**  
5. **Transitions group**

If a group has no entries for a region, skip that group entirely (do not include an object with an empty `children` array).

Example skeleton:

```json
[
  {
    "name": "<Region Name>",
    "sections": [ /* region sections for overworld display */ ],
    "map_locations": [
      {
        "map": "Overworld",
        "x": 0,
        "y": 0
      }
    ]
  },
  {
    "name": "<Region Name> - Key locations",
    "children": [ /* key location child entries */ ]
  },
  {
    "name": "<Region Name> - Power Seals",
    "children": [ /* power seal child entries */ ]
  },
  {
    "name": "<Region Name> - Mega Shards",
    "children": [ /* mega shard child entries */ ]
  },
  {
    "name": "<Region Name> - Transitions",
    "children": [ /* transition child entries */ ]
  }
]
```

## Important rule for transitions
- Do not add transition sections to the overworld node (`"<Region Name>"` first object).
- Transition sections must exist only under:
  - `"<Region Name> - Transitions"` → `children[*].sections`
  - with matching `children[*].map_locations` on the regional map.

## Child entry structure
Each child in grouped sections should follow this pattern:

```json
{
  "name": "<Display Name>",
  "sections": [
    { "name": "<Section Name>" }
  ],
  "map_locations": [
    {
      "map": "<Regional Map Name>",
      "x": "<Location X Position>",
      "y": "<Location Y Position>"
    }
  ]
}
```

## Naming conventions
- Group names:
  - `"<Region> - Key locations"`
  - `"<Region> - Power Seals"`
  - `"<Region> - Mega Shards"`
  - `"<Region> - Transitions"`
- Transition section names should match tracker event names exactly (for example `"... exit"` / `"... Portal"`).

## Exception: The Shop (`TheShop.json`)
`TheShop.json` does not follow the regional grouping model above.

Reason:
- The Shop is not a gameplay traversal region like Autumn Hills or Bamboo Creek.
- Shop checks are purchasable entries displayed directly on the Overworld.

Expected Shop structure:

- Top-level array of direct entries (no Key/Seals/Mega/Transitions grouped children required).
- Entries use `map_locations.map = "Overworld"`.
- Figurines are also tracked as overworld entries.
- No transition grouping is required for The Shop.
