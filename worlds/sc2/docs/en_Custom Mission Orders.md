# Custom Mission Orders for Starcraft 2

## What is this?

This is usage documentation for the `custom_mission_order` YAML option for Starcraft 2. In the future, you might enable this by setting `mission_order: custom` in your YAML, but currently all the options normally affecting mission orders do nothing. As examples, this includes campaign switches, maximum size, disabling Very Hard missions, and excluded missions.

You will need to know how to write a YAML before engaging with this feature, and should read the [Archipelago YAML documentation](https://archipelago.gg/tutorial/Archipelago/advanced_settings/en) before continuing here.

Every example in this document should be valid to generate.

## Basic structure

Custom Mission Orders consist of three kinds of structures:
- The mission order itself contains campaigns (like Wings of Liberty)
- Campaigns contain layouts (like Mar Sara)
- Layouts contain mission slots (like Liberation Day)

To illustrate, the following is what the default custom mission order currently looks like. If you're not sure what some options mean, they will be explained in more depth later.
```yaml
  custom_mission_order:
    # This is a campaign, defined by its name
    Default Campaign:
      # This defines where the campaign shows up
      order: 0
      # How many previous campaigns must be beaten
      # before this one can be accessed
      unlock_count: -1
      # Which specific parts of the mission order must be beaten
      # before this one can be accessed
      unlock_specific: []
      # Whether beating this campaign is part of the world's goal
      required: true
      # The lowest difficulty of missions in this campaign
      min_difficulty: relative
      # The highest difficulty of missions in this campaign
      max_difficulty: relative
      # This is a special layout that defines defaults
      # for other layouts in the campaign
      global:
        # This defines where in the campaign the layout shows up
        order: 0
        # See Default Layout
        limit: 0
        # Whether this layout must be beaten to beat the campaign
        required: false
        # How many previous layouts must be beaten
        # before this one can be accessed
        unlock_count: -1
        # Which specific parts of the mission order must be beaten
        # before this one can be accessed
        unlock_specific: []
        # Which missions are allowed to appear in this layout
        mission_pool:
          - all missions
        # The lowest difficulty of missions in this layout
        min_difficulty: relative
        # The highest difficulty of missions in this layout
        max_difficulty: relative
      # This is a regular layout, defined by its name
      Default Layout:
        # This defines how missions in the layout are organized,
        # as well as how they connect to one another
        type: grid
        # How many total missions should appear in this layout
        size: 9
        # Optional secondary size value that is subject to
        # interpretation by the layout type
        # In the case of grid this sets the grid's width
        limit: 3
```
This default option also defines default values (though you won't get the Default Campaign and Default Layout), so you can omit the options you don't want to change in your own YAML.

Notably however, layouts are required to have both a `type` and a `size`, but neither have defaults. You must define both of them for every layout, either through your own `global` layout, or in the options of every individual layout.

If you want multiple campaigns or layouts, it would look like this:
```yaml
  custom_mission_order:
    My first campaign!:
        # Campaign options here
        global: # Can be omitted if the above defaults work for you
          # Makes all the other layouts only have Terran missions
          mission_pool:
            - terran missions
          # Other layout options here
        My first layout:
          # Defining at least type and size of a layout is mandatory
          type: column
          size: 3
          # Other layout options here
        my second layout:
          type: grid
          size: 4
        layout number 3:
          type: column
          size: 3
        # etc.
    Second campaign:
      the other first layout:
        type: grid
        size: 10
    # etc.
```
It is also possible to access mission slots by their index, which is defined by the type of the layout they are in. The below shows an example of how to access a mission slot, as well as the defaults for their options.

However, keep in mind that layout types will set their own options for specific slots. As before, the options are explained in more depth later.
```yaml
  custom_mission_order:
    My Campaign:
      My Layout:
        type: column
        size: 5
        # 0 is often the layout's starting mission
        # Any index between 0 and (size - 1) is accessible
        0:
          # Which specific mission should go in this slot
          # Defaults to none, picking randomly from the mission pool
          mission: ""
          # Whether this mission is required to beat the campaign
          required: false
          # Whether this mission is accessible as soon as the
          # layout is accessible
          entrance: false
          # Whether this mission is required to beat the layout
          exit: false
          # Whether this slot contains a mission at all
          empty: false
          # Which missions in the layout are unlocked by this mission
          # This is normally set by the layout's type
          next: []
          # How many missions in the campaign must be beaten
          # to access this mission
          unlock_count: 0
          # Which specific parts of the mission order must be beaten
          # before this one can be accessed
          unlock_specific: []
          # Which missions are allowed to appear in this slot
          # If not defined, the slot inherits the layout's pool
          mission_pool:
            - all missions
          # Which specific difficulty this mission should have
          difficulty: relative
```
## Access Rules

If you've read the short option descriptions, you will have seen the word "access" a lot. Normally when you play a Starcraft 2 world, you have a table of missions in the Archipelago SC2 Client, and hovering over a mission tells you what missions are required to access it.

This is still true for custom mission orders, but they also allow defining access rules for campaigns and layouts, which then apply to their entrance missions, and show up on those in the client. Entrance missions of layouts are those that either the layout type or your YAML mark with `entrance: true`. Entrance missions of campaigns are the entrance missions of layouts that have no access rules.

Similarly, a mission in a custom mission order may require a campaign or layout to be beaten, which means beating all of their exit missions. Exit missions of layouts are those that either the layout type or your YAML mark with `exit: true`. Exit missions of campaigns are the exit missions of layouts that are marked as `required: true` and the missions your YAML marks with `required: true`. If you do not mark any required layouts or missions, all layouts of the highest order in the campaign will be required by default.

There are four different ways to restrict access to a mission:
- A layout's type will define the natural flow of missions, eg. to access a mission in a column layout you must beat the mission above it. Specific layout types are covered at the end of this document. You can override this flow using the `next` option on missions.
- `order` and `unlock_count` allow defining a similar flow for layouts and campaigns. This process is explained below.
- For missions, `unlock_count` defines how many other missions in the same campaign must be beaten before the mission can be accessed.
- `unlock_specific` allows picking specific campaigns, layouts, or missions to turn into a requirement. This process is also explained below.

## Shared options

All the options below are listed with their defaults.

---
```yaml
# For campaigns
required: true
# For layouts and missions
required: false
```
For campaigns, this determines whether the campaign is required to beat the world. If you turn this off for every campaign, the campaigns with the highest order are automatically marked as required.

For layouts and missions, this determines whether the layout or mission is required to beat the campaign they are in. If no missions or layouts are marked as required, the layouts of the highest order are automatically marked as required.

---
```yaml
order: 0
```
Applies to campaigns and layouts. Can be any integer value.

The order determines where the campaign or layout is placed relative to other campaigns or layouts. Lower orders appear earlier and ties are considered to be parallel. For layouts, the order is only relative to other layouts within the same campaign.

The order also determines where the campaign or layout is placed in the client. Lower-order campaigns are higher up, and lower-order layouts are further left. Ties are broken randomly.

---

```yaml
unlock_count: -1 
```
Applies to campaigns and layouts. Must be bigger than or equal to -1.

Missions also have a `unlock_count` option, but it works differently for them, and is covered later.

This determines how many campaigns or layouts of the next-lowest order need to be beaten to access this campaign or layout. Negative values, including the default, mean that every previous-order campaign or layout is required.

Next-lowest and previous order here only count orders that are defined in the YAML. If you want a campaign or layout to have a specific order but not use this access rule, set `unlock_count: 0` on it.

The following is an example of these two options:
```yaml
  custom_mission_order:
    Campaign A:
      order: 0 # This is the default and could be omitted
      global:
        type: column
        size: 3
      Layout A-1:
        order: -5 # Negative orders are allowed
      Layout A-2:
        order: 1
      Layout A-3:
        order: 1
      Layout A-4:
        order: 2
        unlock_count: 1
    Campaign B:
      order: 1
      Layout B-1:
        order: -3
        type: column
        size: 3
```
This would result in the following visual layout in the client:
```
                           Campaign A
  Layout A-1   |  Layout A-2   |  Layout A-3   |  Layout A-4
---------------------------------------------------------------
 Mission A-1-0 | Mission A-2-0 | Mission A-3-0 | Mission A-4-0
 Mission A-1-1 | Mission A-2-1 | Mission A-3-1 | Mission A-4-1
 Mission A-1-2 | Mission A-2-2 | Mission A-3-2 | Mission A-4-2

  Campaign B
  Layout B-1
---------------
 Mission B-1-0
 Mission B-1-1
 Mission B-1-2
```
It is possible for `Layout A-2` and `Layout A-3` to randomly swap places here, because they are in the same campaign and their orders are equal.

The following rules apply here:
- `Layout A-1` is immediately accessible, because it is the lowest-order layout of the lowest-order campaign and has no further access rules.
- `Layout A-2` and `Layout A-3` both require `Layout A-1` to be beaten, because it has the biggest order lower than their own (-5 < 1).
  - `Layout B-1`'s order (-3) is technically closer to 1 than -5, however, it is not part of the same campaign, so `Campaign A`'s layouts ignore it.
- `Layout A-4` would by default require both `Layout A-2` and `Layout A-3` to be beaten (because 1 is the biggest order lower than its 2), but because of its `unlock_count: 1` option, it only requires either one of the two to be beaten.
- `Campaign B` requires `Campaign A` to be beaten because of their relative orders, by the same concept as the layout orders explained above.
  - Because no layout in `Campaign A` is marked with `required: true`, it defaults to setting its highest-order layouts (only `Layout A-4` in this case) as required, so unlocking `Campaign B` really requires beating `Layout A-4`.
- Because no campaign is marked with `required: false`, all of them are required to beat this world.

As a reminder, a column's default entrance is its top-most mission and its default exit is its bottom-most mission, so by default, to beat a column-type layout you must beat every mission in it.

Together, this forms the following playthrough:
- The first available mission is `A-1-0`.
- Beat `Layout A-1` by beating `A-1-1`, then `A-1-2`.
- Beat either one out of `Layout A-2` and `Layout A-3` by beating all their respective missions.
- Beat `Layout A-4` by beating all its missions. This also beats `Campaign A`.
- Beat `Layout B-1` by beating all its missions. This also beats `Campaign B`, which beats the world.

---

```yaml
# These two apply to campaigns and layouts
min_difficulty: relative
max_difficulty: relative
# This one applies to missions
difficulty: relative
```
Valid values are:
- Relative
- Starter
- Easy
- Medium
- Hard
- Very Hard

These determine the difficulty of missions within campaigns, layouts, or specific mission slots.

On `relative`, the difficulty of mission slots is dynamically scaled based on earliest possible access to that mission. By default, this scales the entire mission order to go from Starter missions at the start to Very Hard missions at the end.

Campaigns can override these limits, layouts can likewise override the limits set by their campaigns, and missions can simply define their desired difficulty.

In every case, if a mission's mission pool does not contain missions of an appropriate difficulty, it will attempt to find a mission of a nearby difficulty, preferring lower ones.

```yaml
  custom_mission_order:
    Campaign:
      min_difficulty: easy
      max_difficulty: medium
      Layout 1:
        max_difficulty: hard
        type: column
        size: 3
      Layout 2:
        type: column
        size: 3
        0:
          difficulty: starter
```
In this example, `Campaign` is restricted to missions between Easy and Medium. `Layout 1` overrides Medium to be Hard instead, so its 3 missions will go from Easy to Hard. `Layout 2` keeps the campaign's limits, but its first mission is set to Starter. In this case, the first mission will be a Starter mission, but the other two missions will scale towards Medium as if the first had been an Easy one.

---

```yaml
unlock_specific: []
```
Applies to campaigns, layouts, and missions.

This is a list of addresses to other parts of the mission order. The campaign, layout, or mission that defines this list will require all of the defined parts to be beaten.

The basic structure of an address is `<Campaign>/<Layout>/<Mission Index>`, where `<Campaign>` and `<Layout>` are the names of a campaign and a layout within that campaign, and `<Mission Index>` is the index of a mission slot in that layout. As explained earlier, the indices of mission slots are determined by the layout's type.

It is possible to omit the later parts, so `<Campaign>` and `<Campaign>/<Layout>` are valid addresses, and will require beating the entire specified campaign or layout.

In layouts and missions it is also allowed to omit the earlier parts, so a layout can use `<Layout>/<Mission>`, and a mission can additionally use `<Mission>` as addresses. In these cases the omitted parts are assumed to be the containing campaign and layout. In combination with the above, layouts and missions can also use `<Layout>` to require beating a certain layout from the same campaign.

```yaml
  custom_mission_order:
    Campaign A:
      Layout A-1:
        type: column
        size: 3
      Layout A-2:
        type: column
        size: 3
        unlock_specific:
          - Layout A-1
        1:
          unlock_specific:
            - Layout A-1/1
            - 0
    Campaign B:
      unlock_specific:
        - Campaign A
        - Campaign A/Layout A-2
        - Campaign A/Layout A-2/2
      Layout B-1:
        type: column
        size: 3
```
The following rules apply in this example:
- Every campaign and layout uses the default order, so none of them have restricted access via the order mechanism.
- `Layout A-2` requires `Layout A-1`, so this would be the same as setting `Layout A-1` to a lower order than `Layout A-2`.
- The second mission of `Layout A-2` requires the second mission of `Layout A-1`, and the first mission of its containing layout (`Layout A-2`). The second rule here is superfluous, because in a column the second mission already requires the first, but this illustrates how to refer to a mission in the same layout.
- `Campaign B` requires `Campaign A`, `Layout A-2` from `Campaign A`, and the third mission of `Campaign A`'s `Layout A-2`. Because of how `Campaign A` and `Layout A-2` are structured, all three of these are equivalent.
- Because no campaign is marked `required: false`, this world is beaten by beating every campaign. However, the access rules turn this setup into a linear mission order, so `Campaign B` will be the last campaign to be beaten.

---

```yaml
mission_pool:
  - all missions
```
Applies to layouts and missions.

Valid values are names of specific missions and names of mission groups. Group names can be looked up here: [APSC2 Mission Groups](https://matthewmarinets.github.io/ap_sc2_icons/missiongroups)

If a mission defines this, it ignores the pool of its containing layout. To define a pool for a full campaign, define it in the `global` layout.

This is a list of instructions for constructing a mission pool, executed from top to bottom, so the order of values is important.

There are three available instructions:
- Addition: `<Group Name>`, `+<Group Name>` or `+ <Group Name>`
  - This adds the missions of the specified group into the pool
- Subtraction: `~<Group Name>` or `~ <Group Name>`
  - This removes the missions of the specified group from the pool
  - Note that the operator is `~` and not `-`, because the latter is a reserved symbol in YAML.
- Intersection: `and <Group Name>`
  - This removes all the missions from the pool that are not in the specified group.

As a reminder, `<Group Name>` can also be the name of a specific mission.

The first instruction in a pool must always be an addition.

```yaml
  custom_mission_order:
    Campaign:
      global:
        type: column
        size: 3
        mission_pool:
          - terran missions
          - ~ no-build missions
      Layout A-1:
        mission_pool:
          - zerg missions
          - and kerrigan missions
          - + Lab Rat
      Layout A-2:
        0:
          mission_pool:
            - For Aiur!
            - Liberation Day
```
The following pools are constructed in this example:
- `Campaign` defines a pool that contains Terran missions, and then removes all No-Build missions from it.
- `Layout A-1` overrides this pool with Zerg missions, then keeps only the ones with Kerrigan in them, and then adds Lab Rat back to it.
  - Lab Rat does not contain Kerrigan, but because the instruction to add it is placed after the instruction to remove non-Kerrigan missions, it is added regardless.
- The pool for the first mission of `Layout A-2` is contains For Aiur! and Liberation Day. The remaining missions of `Layout A-2` use the Terran pool set by the `global` layout.

## Campaign Options

Campaigns have no further options at this time.

## Layout Options

```yaml
type: # There is no default
```
Determines how missions are placed relative to one another within a layout, as well as how they connect to each other.

Valid values are:
- Column
- Grid

Details about specific layout types are covered at the end of this document.

---

```yaml
size: # There is no default
```
Determines how many missions a layout contains. Valid values are positive numbers.

---

```yaml
limit: 0
```
This is interpreted by each layout type as a secondary parameter for determining the placement of missions. Valid values are non-negative numbers. See each layout type for details on how this value is used.

## Mission Slot Options

For all options in mission slots, the type of their containing layout choses the defaults, and any values you define override the type's defaults.

---

```yaml
mission: ""
```
Valid values are names of specific missions. If this is set, the mission slot will be set to the chosen mission, ignoring any restrictions by the slot's mission pool or difficulty.

---

```yaml
unlock_count: 0
```
Valid values are non-negative numbers.

Unlike with campaigns and layouts, this is a requirement on the number of missions beaten across the whole campaign that this mission is in.

---

```yaml
entrance: false
```
Determines whether this mission is an entrance for its containing layout. An entrance mission becomes available when the access requirements for its layout become fulfilled, but may further be restricted by its own access requirements.

If for any reason a layout has missions which cannot be unlocked by beating other missions, for example if you set the first mission of a column to not be an entrance, then those missions will be automatically marked as entrances. However, this cannot detect circular dependencies, for example if you cut off a section of a grid, so make sure to manually set entrances as appropriate in those cases.

---

```yaml
exit: false
```
Determines whether this mission is an exit for its containing layout. A layout is considered beaten when all its exit missions are beaten.

Layout types will always have at least one default exit, but you can manually turn them off to make a layout without exits. In this case, make sure that beating the layout is not required to access any missions, or generation will fail.

---

```yaml
empty: false
```
Determines whether this mission slot contains a mission at all. If enabled, the slot is empty and will show up as a blank space in the client.

Layout types may have empty slots depending on other settings, and it is up to the layout type whether their empty slots are accessible by index.

---

```yaml
next: []
```
Valid values are indices of other missions within the same layout. Note that unlike `unlock_specific`, this does not accept addresses.

This is the mechanism layout types use to establish mission flow. Overriding this will break the intended order of missions within a type. If you wish to add on to the type's flow rather than replace it, you must manually include the type's intended indices.

Mechanically, a mission is unlocked when any other mission that contains the former in its `next` list is beaten. If a mission is not present in any other mission's `next` list, it is automatically marked as an entrance.
```yaml
  custom_mission_order:
    Wings of Liberty:
      Char:
        type: column
        size: 4
        0:
          next:
            - 1
            - 2
        1:
          next:
            - 3
```
This example creates the branching path within `Char` in the Vanilla mission order.


## Layout Types

### Column (`column`)

This is a linear order going from top to bottom.

`limit` is ignored for this type.

A `size: 5` column has the following indices:
```yaml
0 # This is the default entrance
1
2
3
4 # This is the default exit (size - 1)
```

---

### Grid (`grid`)

This is a rectangular order. Beating a mission unlocks adjacent missions in cardinal directions.

`limit` sets the width of the grid, and height is determined via `size` and `limit`. If `limit` is set to 0, the width and height are determined automatically.

If `size` is too small for the determined width and height, then slots in the bottom left and top right corners will be removed to fit the given `size`. These empty slots are still accessible by index.

A `size: 25`, `limit: 5` grid has the following indices:
```yaml
 0  1  2  3  4
 5  6  7  8  9
10 11 12 13 14
15 16 17 18 19
20 21 22 23 24
```
The top left corner (index `0`) is the default entrance. The bottom right corner (index `size - 1`) is the default exit.