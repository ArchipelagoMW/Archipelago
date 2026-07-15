# Json World Specification

## Loading

todo

## Formats

The Json World specification is made up of modules of data with varying formats allowed.
Format overrides are formated as
```json
{
  "formats": {
    "item_name_to_id": "explicit"
  }
}
```

### Item Datapackage

Item Datapackage uses the format key `item_name_to_id` with the default value of `explicit`

#### Item Datapackage - explicit

The key `item_name_to_id` is expected to have the full dict[str, int] mapping.

### Location Datapackage

Location Datapackage uses the format key `location_name_to_id` with the default value of `explicit`

#### Location Datapackage - explicit

The key `location_name_to_id` is expected to have the full dict[str, int] mapping.

### Item Groups

Item Group definitions use the format key `item_name_groups` with the default value of `explicit`

#### Item Groups - explicit

The key `item_name_groups` is expected to have the full dict[str, list[str]] mapping.

### Location Groups

Location Group definitions use the format key `location_name_groups` with the default value of `explicit`

#### Location Groups - explicit

The key `location_name_groups` is expected to have the full dict[str, list[str]] mapping.
Alternatively 

### Region List

TODO: is there a reason to not always calculate this from region_map?
Region List uses the format key `region_list` with the default value of `explicit`

#### Region List - explicit

The key `region_list` is expected to have the full list[str] object.

#### Region List - region_map

The key `region_map` is expected to have a dict[str, dict[str, Rule]] mapping of region connections,
and the region list is calculated by the join of inner and outer dict keys.

### Rules

Rule definitions use the format key `rule` with the default value of `dnf_items`.
`null` is the json format is always a valid Rule regardless of format to represent rules that are
itemless (the default access rule).


Rules are handled differently than other data, there is no common place for Rules in the full json,
but instead are parsed out inside of other data structures.

#### Rules - dnf_items

Rules are expected in the format list[list[str]] where all items of any one inner list is logical access.
For example, the following would be true with either a sword and a shield or with a sword and a health up item.
```json
{
  "completion_rule": [["sword", "shield"], ["sword", "health up"]]
}
```

### Region Map

Region Map uses the format key `region_map` with the default value of `explicit`

#### Region Map - explicit

The key `region_map` is expected to have the full dict[str, dict[str, Rule]]
for mapping Source Region to Target Region to Access Rule

### Location Map

Location Map uses the format key `location_map` with the default value of `explicit`

#### Location Map - explicit

The key `location_map` is expected to have the full dict[str, dict[str, Rule]]
for mapping Parent Region to Location to Access Rule

### Event Map

Event Map uses the format key `event_map` with the default value of `explicit`

#### Event Map - explicit

The key `event_map` is expected to have the full ???

### Item List

Item List uses the format key `item_list` with the default value of `explicit`

#### Item List - explicit

The key `item_list` is expected to have the full list[str] object of item names

#### Item List - counter

The key `item_count` is expected to have a dict[str, int] mapping of item to item count

### Completion Rule

Completion Rule does not have a format key, and instead always uses the `completion_rule` key
with any non-null Rule

### Classification Lookup

Classification Lookup uses the format key `classification_lookup` with the default value of `explicit`

#### Classification Lookup - explicit

The key `classification_lookup` is expected to have a dict[str, str] mapping
for mapping item name to classification name (i.e. `progression`)

#### Classification Lookup - reverse_lookup

The key `classification_lookup` is expected to have a dict[str, str] mapping
for mapping classification name (i.e. `progression`) to item name

### Filler Weights

Filler Weights uses the format key `filler_weights` with the default value `explicit`
Note: filler item names do not have to be items with filler classification.

#### Filler Weights - explicit

The key `filler_weights` is expected to have a dict[str, int] mapping
for mapping filler item names to random weights.

#### Filler Weights - single

The key `filler_item` is expected to have a single str item name to be used for all itempool filling.
