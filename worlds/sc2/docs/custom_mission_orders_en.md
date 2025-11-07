# Custom Mission Orders for Starcraft 2

<details>
    <summary>Table of Contents</summary>

- [Custom Mission Orders for Starcraft 2](#custom-mission-orders-for-starcraft-2)
  - [What is this?](#what-is-this)
  - [Basic structure](#basic-structure)
  - [Interactions with other YAML options](#interactions-with-other-yaml-options)
  - [Instructions for building a mission order](#instructions-for-building-a-mission-order)
  - [Shared options](#shared-options)
    - [Display Name](#display-name)
    - [Unique name](#unique-name)
    - [Goal](#goal)
    - [Exit](#exit)
    - [Entry rules](#entry-rules)
    - [Unique progression track](#unique-progression-track)
    - [Difficulty](#difficulty)
    - [Mission Pool](#mission-pool)
  - [Campaign Options](#campaign-options)
    - [Preset](#preset)
  - [Campaign Presets](#campaign-presets)
    - [Static Presets](#static-presets)
      - [Preset Options](#preset-options)
        - [Missions](#missions)
        - [Shuffle Raceswaps](#shuffle-raceswaps)
        - [Keys](#keys)
    - [Golden Path](#golden-path)
  - [Layout Options](#layout-options)
    - [Type](#type)
    - [Size](#size)
    - [Missions](#missions-1)
  - [Mission Slot Options](#mission-slot-options)
    - [Entrance](#entrance)
    - [Empty](#empty)
    - [Next](#next)
    - [Victory Cache](#victory-cache)
  - [Layout Types](#layout-types)
    - [Column](#column)
    - [Grid](#grid)
      - [Grid Index Functions](#grid-index-functions)
        - [point(x, y)](#pointx-y)
        - [rect(x, y, width, height)](#rectx-y-width-height)
    - [Canvas](#canvas)
      - [Canvas Index Functions](#canvas-index-functions)
        - [group(character)](#groupcharacter)
    - [Hopscotch](#hopscotch)
      - [Hopscotch Index Functions](#hopscotch-index-functions)
        - [top](#top)
        - [bottom](#bottom)
        - [middle](#middle)
        - [corner(index)](#cornerindex)
    - [Gauntlet](#gauntlet)
    - [Blitz](#blitz)
      - [Blitz Index Functions](#blitz-index-functions)
        - [row(height)](#rowheight)
</details>

## What is this?

This is usage documentation for the `custom_mission_order` YAML option for Starcraft 2. You can enable Custom Mission Orders by setting `mission_order: custom` in your YAML.

You will need to know how to write a YAML before engaging with this feature, and should read the [Archipelago YAML documentation](https://archipelago.gg/tutorial/Archipelago/advanced_settings/en) before continuing here.

Every example in this document should be valid to generate.

## Basic structure

Custom Mission Orders consist of three kinds of structures:
- The mission order itself contains campaigns (like Wings of Liberty)
- Campaigns contain layouts (like Mar Sara)
- Layouts contain mission slots (like Liberation Day)

As a note, layouts are also called questlines in the UI. Layouts and questlines refer to the same thing, though this document will only use layouts.

To illustrate, the following is what the default custom mission order currently looks like. If you're not sure what some options mean, they will be explained in more depth later.
```yaml
  custom_mission_order:
    # This is a campaign, defined by its name
    Default Campaign:
      # The campaign's name as displayed in the client
      display_name: "null"
      # Whether this campaign must have a unique name in the client
      unique_name: false
      # Conditions that must be fulfilled to access this campaign
      entry_rules: []
      # Whether beating this campaign is part of the world's goal
      goal: true
      # The lowest difficulty of missions in this campaign
      min_difficulty: relative
      # The highest difficulty of missions in this campaign
      max_difficulty: relative
      # This is a special layout that defines defaults
      # for other layouts in the campaign
      global:
        # The layout's name as displayed in the client
        display_name: "null"
        # Whether this layout must have a unique name in the client
        unique_name: false
        # Whether beating this layout is part of the world's goal
        goal: false
        # Whether this layout must be beaten to beat the campaign
        exit: false
        # Conditions that must be fulfilled to access this layout
        entry_rules: []
        # Which missions are allowed to appear in this layout
        mission_pool:
          - all missions
        # The lowest difficulty of missions in this layout
        min_difficulty: relative
        # The highest difficulty of missions in this layout
        max_difficulty: relative
        # Used for overwriting default options of mission slots,
        # which are set by the layout type (see Default Layout)
        missions: []
      # This is a regular layout, defined by its name
      Default Layout:
        # This defines how missions in the layout are organized,
        # as well as how they connect to one another
        type: grid
        # How many total missions should appear in this layout
        size: 9
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
If you don't want to have a campaign container for your layouts, you can also forego the campaign layer like this:
```yaml
  custom_mission_order:
    Example campaign-level layout:
      # Make sure to always declare these two, like with regular layouts
      type: column
      size: 3
    
    # Regular campaigns and campaign-less layouts
    # can be mixed however you want
    Some Campaign:
      Some Layout:
        type: column
        size: 3
```
It is also possible to access mission slots by their index, which is defined by the type of the layout they are in. The below shows an example of how to access a mission slot, as well as the defaults for their options.

However, keep in mind that layout types will set their own options for specific slots, overwriting the below defaults, and using this option in turn overwrites the values set by layout types. As before, the options are explained in more depth later.
```yaml
  custom_mission_order:
    My Campaign:
      My Layout:
        type: column
        size: 5
        missions:
          # 0 is often the layout's starting mission
          # Any index between 0 and (size - 1) is accessible
          - index: 0
            # Whether this mission is part of the world's goal
            goal: false
            # Whether this mission is accessible as soon as the
            # layout is accessible
            entrance: false
            # Whether this mission is required to beat the layout
            exit: false
            # Whether this slot contains a mission at all
            empty: false
            # Conditions that must be fulfilled to access this mission
            entry_rules: []
            # Which missions in the layout are unlocked by this mission
            # This is normally set by the layout's type
            next: []
            # Which missions are allowed to appear in this slot
            # If not defined, the slot inherits the layout's pool
            mission_pool:
              - all missions
            # Which specific difficulty this mission should have
            difficulty: relative
```
## Interactions with other YAML options

Custom Mission Orders respect all the options that change which missions can appear as if the options' relevant missions had been excluded. For example, `selected_races: protoss` is equivalent to excluding all Zerg and Terran missions, and `enabled_campaigns: ["Wings of Liberty"]` is equivalent to excluding all but WoL missions.

This means that if you want total control over available missions in your mission order via `mission_pool`s, you should enable all races and campaigns and leave your `excluded_missions` list empty, but you can also use these options to get rid of particular missions you never want and can then ignore those missions in your `mission_pool`s.

There are, however, several options that are ignored by Custom Mission Orders:
- `mission_order`, because it has to be `custom` for your Custom Mission Order to apply
- `maximum_campaign_size`, because you determine the size of the mission order via layout `size` attributes
- `two_start_positions`, which you can instead determine in individual layouts of the appropriate `type`s (see Grid and Hopscotch sections below)
- `key_mode`, which you can still specify for presets (see Campaign Presets section), and can otherwise manually set up using Item entry rules

## Instructions for building a mission order

Normally when you play a Starcraft 2 world, you have a table of missions in the Archipelago SC2 Client, and hovering over a mission tells you what missions are required to access it. This is still true for custom mission orders, but you now have control over the way missions are visually organized, as well as their access requirements.

This section is meant to offer some guidance when making your own mission order for the first time.

To begin making your own mission order, think about how you visually want your missions laid out. This should inform the layout `type`s you want to use, and give you some idea about the overall structure of your mission order.

For example, if you want to make a custom campaign like the vanilla ones, you will want a lot of layouts of [`type: column`](#column). If you want a Hopscotch layout with certain missions or races, a single layout with [`type: hopscotch`](#hopscotch) will suffice. If you want to play through a funny shape, you will want to draw with a [`type: canvas`](#canvas). If you just want to make a minor change to a vanilla campaign, you will want to start with a [`preset` campaign](#preset).

The natural flow of a mission order is defined by the types of its layouts. It makes sense for a mission to unlock its neighbors, it makes sense for a Hopscotch layout to wrap around the sides, and it makes sense for a Column's final mission to be at the bottom. Layout types create their flow by setting [`next`](#next), [`entrance`](#entrance), [`exit`](#exit), and [`entry_rules`](#entry-rules) on missions. More on these in a little bit.

Layout types dictate their own visual structure, and will only rarely make mission slots with `empty: true`. If you want a certain shape that's not exactly like an existing type, you can pick a type with more slots than you want and remove the extras by setting `empty: true` on them.

With the basic setup in place, you should decide on what the goal of your mission order is. By default every campaign has `goal: true`, meaning all campaigns must be beaten to complete the world. You can additionally set `goal: true` on layouts and mission slots to require them to be beaten as well. If you set `goal: false` on everything, the mission order will default to setting the last campaign (lowest in your YAML) as the goal.

After deciding on a goal, you can complicate your way towards it. At the start of a world, the only accessible missions in the mission order are all the missions marked `entrance: true`. When you beat one of these missions, it unlocks all the missions in the beaten mission's `next` list. This process repeats until all the missions are accessible.

If this behavior isn't enough for your planned mission order, you can interrupt the natural flow of layout types using `entry_rules` in combination with `exit`.

When this document refers to "beating" something, it means the following:
- A mission is beaten if it is accessible and its victory location is checked.
- Beating a layout means beating all the missions in the layout with `exit: true`
- Beating a campaign means beating all the layouts in the campaign with `exit: true`

Note victory checks may be claimed by someone else running `!collect` in a multiworld and receiving an item on a victory check. Collecting victory cache checks do not count, only victory checks.

Layouts will have their default exit missions set by the layout type. If you don't want to use this default, you will have to manually set `exit: false` on the default exits. Campaigns default to using the last layout in them (the lowest in your YAML) as their exit, but only if you don't manually set `exit: true` on a layout.

Using `entry_rules`, you can make a mission require beating things other than those missions whose `next` points to it, and you can make layouts and campaigns not available from the start.

Note that `entry_rules` are an addition to the `next` behavior. If you want a mission to completely ignore the natural flow and only use your `entry_rules`, simply set `entrance: true` on it.

Please see the [`entry_rules`](#entry-rules) section below for available rules and examples.

With your playthrough sufficiently complicated, it only remains to add flavor to your mission order by changing [`mission_pool`](#mission-pool) and [`difficulty`](#difficulty) options as you like them. These options are also explained below.

To summarize:
- Start by setting up campaigns and layouts with appropriate layout `type`s and `size`s
- Decide the mission order's `goal`s
- Customize access requirements as desired:
  - Use `entrance`, `next`, and `empty` on mission slots to change the unlocking order of missions within a layout
  - Use `entry_rules` in combination with `exit` to add additional restrictions to missions, layouts, and campaigns
- Use the `mission_pool` and `difficulty` options to add flavor
- Finally, generate and have fun!

## Shared options

These are the options that are shared between at least two of campaigns, layouts and missions. All the options below are listed with their defaults.

---
### Display Name
```yaml
# For campaigns and layouts
display_name: "null"
```
As shown in the examples, every campaign and layout is defined with a name in your YAML. This name is used to find campaigns and layouts within the mission order (see `entry_rules` section), and by default (meaning with `display_name: "null"`) it is also shown in the client.

This option changes the name shown in the client without affecting the definition name.

There are two special use cases for this option:
```yaml
# This means the campaign or layout
# will not have a title in the client
display_name: ""
```
```yaml
# This will randomly pick a name from the given list of options
display_name:
  - My First Choice
  - My Second Choice
  - My Third Choice
```

---
### Unique name
```yaml
# For campaigns and layouts
unique_name: false
```
This option prevents names from showing up multiple times in the client. It is recommended to be used in combination with lists of `display_name`s to prevent the generator from picking duplicate names.

---
### Goal
```yaml
# For campaigns
goal: true
```
```yaml
# For layouts and missions
goal: false
```
This determines whether the campaign, layout or mission is required to beat the world. If you turn this off for everything, the last defined campaign (meaning the lowest one in your YAML) is chosen by default.

---
### Exit
```yaml
# For layouts and missions
exit: false
```
This determines whether beating the mission is required to beat its parent layout, and whether beating the layout is required to beat its parent campaign.

---
### Entry rules
```yaml
# For campaigns, layouts, and missions
entry_rules: []
```
This defines access restrictions for parts of the mission order.

These are the available rules:
```yaml
entry_rules:
  # Beat these things ("Beat rule")
  - scope: []
  # Beat X amount of missions from these things ("Count rule")
  - scope: []
    amount: -1
  # Find these items ("Item rule")
  - items: {}
  # Fulfill X amount of other conditions ("Subrule rule")
  - rules: []
    amount: -1
```
Note that Item rules take both a name and amount for each item (see the example below). In general this rule treats items like the `locked_items` option, including that it will override `excluded_items`, but as a notable difference all items required for Item rules are marked as progression. If multiple Item rules require the same item, the largest required amount will be locked, **not** the sum of all amounts.

Additionally, Item rules accept a special item:
```yaml
entry_rules:
  - items:
      Key: 1
```
This is a generic item that is converted to a key item for the specific scope it is under. Missions get Mission Keys, layouts get Questline Keys, and campaigns get Campaign Keys. If you want to know which specific key is created (for example to tie multiple unlocks to the same key), you can generate a test game and check in the client.

You can also use one of the following key items for this purpose:
<details>
  <summary>Custom keys</summary>

  - `Terran Key`
  - `Zerg Key`
  - `Protoss Key`
  - `Raynor Key`
  - `Tychus Key`
  - `Swann Key`
  - `Stetmann Key`
  - `Hanson Key`
  - `Nova Key`
  - `Tosh Key`
  - `Valerian Key`
  - `Warfield Key`
  - `Mengsk Key`
  - `Han Key`
  - `Horner Key`
  - `Kerrigan Key`
  - `Zagara Key`
  - `Abathur Key`
  - `Yagdra Key`
  - `Kraith Key`
  - `Slivan Key`
  - `Zurvan Key`
  - `Brakk Key`
  - `Stukov Key`
  - `Dehaka Key`
  - `Niadra Key`
  - `Izsha Key`
  - `Artanis Key`
  - `Zeratul Key`
  - `Tassadar Key`
  - `Karax Key`
  - `Vorazun Key`
  - `Alarak Key`
  - `Fenix Key`
  - `Urun Key`
  - `Mohandar Key`
  - `Selendis Key`
  - `Rohana Key`
  - `Reigel Key`
  - `Davis Key`
  - `Ji'nara Key`

</details>

These keys will never be used by the generator unless you specify them yourself.

There is also a special type of key:
```yaml
entry_rules:
  - items:
      # These two forms are equivalent
      Progressive Key: 5
      Progressive Key 5: 1
```
Progressive keys come in two forms: `Progressive Key: <track>` and `Progressive Key <track>: 1`. In the latter form the item amount is ignored. Their track is used to group them, so all progressive keys with track 1 belong together, as do all with track 2, and so on. Item rules using progressive keys are sorted by how far into the mission order they appear and have their required amounts set automatically so that deeper rules require more keys, with each track of progressive keys performing its own sorting.

Note that if any Item rule within a track belongs to a mission, the generator will accept ties, in which case the affected rules will require the same number of progressive keys. If a track only contains Item rules belonging to layouts and campaigns, the track will be sorted in definition order (top to bottom in your YAML), so there will be no ties.

If you prefer not to manually specify the track, use the [`unique_progression_track`](#unique-progression-track) option.

The Beat and Count rules both require a list of scopes. This list accepts addresses towards other parts of the mission order.

The basic form of an address is `<Campaign>/<Layout>/<Mission>`, where `<Campaign>` and `<Layout>` are the definition names (not `display_names`!) of a campaign and a layout within that campaign, and `<Mission>` is the index of a mission slot in that layout or an index function for the layout's type. See the section on your layout's type to find valid indices and functions.

If you don't want to point all the way down to a mission slot, you can omit the later parts. `<Campaign>` and `<Campaign>/<Layout>` are valid addresses, and will point to the entire specified campaign or layout.

Futhermore, you can generically refer to the parent of an object using `..`, so if you are creating entry rules for a given layout and want to point at a different `<Layout>` in the same `<Campaign>`, the following are identical:
- `../<Layout>`
- `<Campaign>/<Layout>`

You can also chain these, so for a given mission `../..` will point to its parent campaign.

Lastly, you can point to the whole mission order via `<Campaign>/..` (or the equivalent number of `..`s from a given layer), but this is only supported for Count rules and not Beat rules.

Note that if you have a campaign-less layout, you will not require a `<Campaign>` part to find it, and `..` will skip the campaign layer.

Below are examples of the available entry rules:
```yaml
  custom_mission_order:
    Some Missions:
      type: grid
      size: 9
      entry_rules:
        # Item rule:
        # To access the Some Missions layout,
        # you have to find or receive your Marine
        - items:
            Marine: 1
    
    Wings of Liberty:
      Mar Sara:
        type: column
        size: 3
      Artifact:
        type: column
        size: 3
        entry_rules:
          # Beat rule:
          # To access the Artifact layout,
          # you have to first beat Mar Sara
          - scope: ../Mar Sara
      Prophecy:
        type: column
        size: 3
        entry_rules:
          # Beat rule:
          # Beat the mission at index 1 in the Artifact layout
          - scope: ../Artifact/1
          # This is identical to the above
          # because this layout is already in Wings of Liberty
          - scope: Wings of Liberty/Artifact/1
      Covert:
        type: column
        size: 3
        entry_rules:
          # Count rule:
          # Beat any 7 missions from Wings of Liberty
          - scope: Wings of Liberty
            amount: 7
    
    Complicated Access:
      type: column
      size: 3
      entry_rules:
        # Subrule rule:
        # To access this layout,
        # fulfill any 1 of the nested rules
        # (See amount value at the bottom)
        - rules:
            # Nested Subrule rule:
            # Fulfill all of the nested rules
            # Amount can be at the top if you prefer
            - amount: -1 # -1 means "all of them"
              rules:
              # Count rule:
              # Beat any 5 missions from Wings of Liberty
              - scope: Wings of Liberty
                amount: 5
              # Count rule:
              # Beat any 5 missions from Some Missions
              - scope: Some Missions
                amount: 5
            # Count rule:
            # Beat any 10 combined missions from
            # Wings of Liberty or Some Missions
            - scope:
                - Wings of Liberty
                - Some Missions
              amount: 10
          amount: 1
```
As this last example shows, the Subrule rule is a powerful tool for making arbitrarily complex requirements. Put plainly, the example accomplishes the following: To unlock the `Complicated Access` layout, either beat 5 missions in both the `Wings of Liberty` campaign and the `Some Missions` layout, or beat 10 missions across both of them.

---
### Unique progression track
```yaml
# For campaigns and layouts
unique_progression_track: 0
```
This option specifically affects Item entry rules using progressive keys. Progressive keys used by children of this campaign/layout that are on the given track will automatically be put on a track that is unique to the container instead.
```yaml
  custom_mission_order:
    First Column:
      type: column
      size: 3
      unique_progression_track: 0 # Default
      missions:
        - index: [1, 2]
          entry_rules:
          - items:
              Progressive Key: 0
    Second Column:
      type: column
      size: 3
      unique_progression_track: 0 # Default
      missions:
        - index: [1, 2]
          entry_rules:
          - items:
              Progressive Key: 0
```
In this example the two columns will use separate progressive keys for their missions.

In the case that a mission slot uses a progressive key whose track matches the `unique_progression_track` of both its containing layout and campaign, the key will use the layout's unique track and not the campaign's. To avoid this behavior simply use different `unique_progression_track` values for the layout and campaign.

---
### Difficulty
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
        missions:
          - index: 0
            difficulty: starter
```
In this example, `Campaign` is restricted to missions between Easy and Medium. `Layout 1` overrides Medium to be Hard instead, so its 3 missions will go from Easy to Hard. `Layout 2` keeps the campaign's limits, but its first mission is set to Starter. In this case, the first mission will be a Starter mission, but the other two missions will scale towards Medium as if the first had been an Easy one.

---
### Mission Pool
```yaml
# For layouts and missions
mission_pool:
  - all missions
```
Valid values are names of specific missions and names of mission groups. Group names can be looked up here: [APSC2 Mission Groups](https://matthewmarinets.github.io/ap_sc2_icons/missiongroups)

If a mission defines this, it ignores the pool of its containing layout. To define a pool for a full campaign, define it in the `global` layout.

This is a list of instructions for constructing a mission pool, executed from top to bottom, so the order of values is important.

There are three available instructions:
- Addition: `<Group Name>`, `+<Group Name>` or `+ <Group Name>`
  - This adds the missions of the specified group into the pool
- Subtraction: `~<Group Name>` or `~ <Group Name>`
  - This removes the missions of the specified group from the pool
  - Note that the operator is `~` and not `-`, because the latter is a reserved symbol in YAML.
- Intersection: `^<Group Name>` or `^ <Group Name>`
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
          - ^ kerrigan missions
          - + Lab Rat
      Layout A-2:
        missions:
          - index: 0
            mission_pool:
              - For Aiur!
              - Liberation Day
```
The following pools are constructed in this example:
- `Campaign` defines a pool that contains Terran missions, and then removes all No-Build missions from it.
- `Layout A-1` overrides this pool with Zerg missions, then keeps only the ones with Kerrigan in them, and then adds Lab Rat back to it.
  - Lab Rat does not contain Kerrigan, but because the instruction to add it is placed after the instruction to remove non-Kerrigan missions, it is added regardless.
- The pool for the first mission of `Layout A-2` contains For Aiur! and Liberation Day. The remaining missions of `Layout A-2` use the Terran pool set by the `global` layout.

## Campaign Options

These options can only be used in campaigns.

---
### Preset
```yaml
preset: none
```
This option loads a pre-built campaign into your mission order. Presets may accept additional options in addition to regular campaign options.

With all presets, you can override their layout options by defining the layouts like normal in your YAML.
```yaml
  custom_mission_order:
    My Campaign:
      preset: wol + prophecy
      missions: random # Optional
      shuffle_raceswaps: false # Optional
      keys: none # Optional
      Prophecy:
        mission_pool:
          - zerg missions
```
This example loads the Wol + Prophecy preset and then changes Prophecy's missions to be Zerg instead of Protoss.

See the following section for available presets.

## Campaign Presets

There are two kinds of presets: Static presets that are based on vanilla campaigns, and scripted presets that dynamically create a complex campaign based on extra required options.

---
### Static Presets
Available static presets are the following:
- `WoL + Prophecy`
- `WoL`
- `Prophecy`
- `HotS`
- `Prologue`, `LotV Prologue`
- `LotV`
- `Epilogue`, `LotV Epilogue`
- `NCO`
- `Mini WoL + Prophecy`
- `Mini WoL`
- `Mini Prophecy`
- `Mini HotS`
- `Mini Prologue`, `Mini LotV Prologue`
- `Mini LotV`
- `Mini Epilogue`, `Mini LotV Epilogue`
- `Mini NCO`

For these presets, the layout names used to override settings match the names shown in the client, with some exceptions:
- Prophecy, Prologue and Epilogue contain a single Gauntlet each, which are named `Prophecy`, `Prologue` and `Epilogue` respectively.
- The Gauntlets in the Mini variants of the above are also named `Prophecy`, `Prologue` and `Epilogue`.
- NCO and Mini NCO contain three columns each, named `Mission Pack 1`, `Mission Pack 2` and `Mission Pack 3`.

#### Preset Options
All static presets accept these options, as shown in the example above:

##### Missions
The `missions` option accepts these possible values:
- `random` (default), which removes pre-defined `mission_pool` options from layouts and missions, meaning all missions will follow the pool defined in your campaign's `global` layout. This is the default if you don't define the `missions` option.
- `vanilla_shuffled`, which will leave `mission_pool`s on layouts to shuffle vanilla missions within their respective campaigns.
- `vanilla`, which will leave all missions as they are in the vanilla campaigns.

##### Shuffle Raceswaps
The `shuffle_raceswaps` option accepts `true` and `false` (default). If enabled, the missions pools in the preset will contain raceswapped missions. This means `missions: vanilla_shuffled` will shuffle raceswaps alongside their regular variants, and `missions: vanilla` will allow a random variant of the mission in each slot. This option does nothing if `missions` is set to `random`.

##### Keys
The `keys` option accepts these possible values:
- `none` (default), which does not add any Key Item rules to the preset.
- `layouts`, which adds Key Item rules to layouts besides the preset's left-most layout, in addition to their regular entry rules.
- `missions`, which adds Key Item rules to missions besides the preset's starter mission, in addition to their regular entry rules.
- `progressive_layouts`, which adds Progressive Key Item rules to layouts besides the preset's left-most layout, in addition to their regular entry rules. These progressive keys use track 0, with presets using the default `unique_progression_track: 0`.
- `progressive_missions`, which adds Progressive Key Item rules to missions besides the preset's starter mission, in addition to their regular entry rules. These progressive keys use track 1 and do not make use of `unique_progression_track`.
- `progressive_per_layout`, which adds Progressive Key Item rules to all missions within each layout besides the preset's left-most one. These progressive keys use track 0, with presets and their layouts using the default `unique_progression_track: 0`.

---
### Golden Path
```yaml
preset: golden path
size: # Required, no default, accepts positive numbers
two_start_positions: false
keys: none # Optional
```
Golden Path aims to create a dynamically-sized campaign with branching paths to create a similar experience to the Wings of Liberty campaign. It accomplishes this by having a main column that requires an increasing number of missions to be beaten to advance, and a number of side columns that require progressing the main column to advance. The exit of a Golden Path campaign is the last mission of the main column.

The `size` option defines the number of missions in the campaign.

If `two_start_positions`, the first mission will be skipped, and the first two branches will be available from the start instead.

The columns in a Golden Path get random names from a `display_name` list and have `unique_name: true` set on them. Their definition names for overriding options are `"0"`, `"1"`, `"2"`, etc., with `"0"` always being the main column, `"1"` being the left-most side column, and so on.

Since the number of side columns depends on the number of missions, it is best to generate a test game for a given size to see how many columns are generated.

Golden Path also accepts a `keys` option, which works like the same option for static presets, and accepts the following values:
- `none` (default), which does not add any Key Item rules to the preset.
- `layouts`, which adds Key Item rules to all side columns, in addition to their regular entry rules.
- `missions`, which adds Key Item rules to missions besides the preset's starter mission, in addition to their regular entry rules.
- `progressive_layouts`, which adds Progressive Key Item rules to all side columns, in addition to their regular entry rules. These progressive keys use track 0, with this preset using the default `unique_progression_track: 0`.
- `progressive_missions`, which adds Progressive Key Item rules to missions besides the preset's starter mission, in addition to their regular entry rules. These progressive keys use track 1 and do not make use of `unique_progression_track`.
- `progressive_per_layout`, which adds Progressive Key Item rules to all missions within each side column. These progressive keys use track 0, with this preset and its layouts using the default `unique_progression_track: 0`.

## Layout Options

Layouts may have special options depending on their `type`. These are covered in the section on Layout Types.
Below are the options that apply to every layout.

---
### Type
```yaml
type: # There is no default
```
Determines how missions are placed relative to one another within a layout, as well as how they connect to each other.

Currently, valid values are:
- Column
- Grid
- Hopscotch
- Gauntlet
- Blitz

Details about specific layout types are covered at the end of this document.

---
### Size
```yaml
size: # There is no default
```
Determines how many missions a layout contains. Valid values are positive numbers.

### Missions
```yaml
missions: []
```
This is used to access mission slots and overwrite the options that the layout type set for them. Valid options for mission slots are covered below, but the `index` option used to find mission slots is explained here.

Note that this list is evaluated from top to bottom, meaning if you perform conflicting changes on the same mission slot, the last defined operation (lowest in your YAML) will be the one that takes effect.

The following example shows ways to access and modify missions:
```yaml
  custom_mission_order:
    My Example:
      type: grid
      size: 4
      missions:
        # Indices can be a numerical value
        # This sets the mission at index 1 to be an exit
        - index: 1
          exit: true
        # Indices can be special index functions
        # Valid functions are 'exits', 'entrances', and 'all'
        # These are available for all types of layouts
        # This takes all exits, including the one set above,
        # and turns them into non-exits
        - index: exits
          exit: false
        # Indices can be index functions
        # Available functions depend on the layout's type
        # In this case the function will return the indices 1 and 3
        # and then mark those two slots as empty
        - index: rect(1, 0, 1, 2)
          empty: true
        # Indices can be a list of valid values
        # This takes all entrances as well as the mission at index 2
        # and marks all of them as both entrances and exits
        - index:
            - entrances
            - 2
          entrance: true
          exit: true
```
The result of this example will be a grid where the two missions on the right are empty, and the two missions on the left are both entrances and exits.

## Mission Slot Options

For all options in mission slots, the layout type containing the mission slot choses the defaults, and any values you define override the type's defaults.

---
### Entrance
```yaml
entrance: false
```
Determines whether this mission is an entrance for its containing layout. An entrance mission becomes available its parent layout's and campaign's `entry_rules` are fulfilled, but may further be restricted by its own `entry_rules`.

If for any reason a mission cannot be unlocked by beating other missions, meaning that there is no mission whose `next` points at this mission, then this missions will be automatically marked as entrances. However, this cannot detect circular dependencies, for example if you cut off a section of a grid, so make sure to manually set entrances as appropriate in those cases.

---
### Empty
```yaml
empty: false
```
Determines whether this mission slot contains a mission at all. If set to `true`, the slot is empty and will show up as a blank space in the client.

Layout types have their own means of creating blank spaces in the client, and so rarely use this option. If you want complete control over a layout's slots, use a layout of `type: grid`.

---
### Next
```yaml
next: []
```
Valid values are indices of other missions within the same layout and index functions for the layout's type. Note that this does not accept addresses.

This is the mechanism layout types use to establish mission flow. Overriding this will break the intended order of missions within a type. If you wish to add on to the type's flow rather than replace it, you must manually include the indices intended by the type.

Mechanically, a mission is unlocked when any other mission that contains the former in its `next` list is beaten. If a mission is not present in any other mission's `next` list, it is automatically marked as an entrance.
```yaml
  custom_mission_order:
    Wings of Liberty:
      Char:
        type: column
        size: 4
        missions:
          - index: 0
            next:
              - 1
              - 2
          - index: 1
            next:
              - 3
          # The below two are default for a column
          # and could be removed from this list
          - index: 2
            next:
              - 3
          - index: 3
            next: []

```
This example creates the branching path within `Char` in the Vanilla mission order.

---
### Victory Cache
```yaml
victory_cache: 0
```
Valid values are integers in the range 0 to 10. Sets the number of extra locations given for victory on a mission.

By default, when this value is not set, the option is set to 0 for goal missions and to the global `victory_cache` option for all other missions.

## Layout Types

The below types are listed with their custom options and their defaults.

---
### Column
```yaml
type: column
```

This is a linear order going from top to bottom.

A `size: 5` column has the following indices:
```yaml
0 # This is the default entrance
1
2
3
4 # This is the default exit (size - 1)
```

---
### Grid
```yaml
type: grid
width: 0 # Accepts positive numbers
two_start_positions: false # Accepts true/false
```
This is a rectangular order. Beating a mission unlocks adjacent missions in cardinal directions.

`width` sets the width of the grid, and height is determined via `size` and `width`. If `width` is set to 0, the width and height are determined automatically.

If `two_start_positions`, the top left corner will be set to `empty: true`, and its two neighbors will be entrances instead.

If `size` is too small for the determined width and height, then slots in the bottom left and top right corners will be removed to fit the given `size`. These empty slots are still accessible by index.

A `size: 25`, `width: 5` grid has the following indices:
```yaml
 0  1  2  3  4
 5  6  7  8  9
10 11 12 13 14
15 16 17 18 19
20 21 22 23 24
```
The top left corner (index `0`) is the default entrance. The bottom right corner (index `size - 1`) is the default exit.

#### Grid Index Functions
Grid supports the following index functions:

##### point(x, y)
`point(x, y)` returns the index at the given zero-based X and Y coordinates. In the above example, `point(2, 4)` is index `22`.

##### rect(x, y, width, height)
`rect(x, y, width, height)` returns the indices within the rectangle defined by the starting point at the X and Y coordinates and the width and height arguments. In the above example, `rect(1, 2, 3, 2)` returns the indices `11, 12, 13, 16, 17, 18`.

---
### Canvas
```yaml
type: canvas
canvas: # No default
jump_distance_orthogonal: 1 # Accepts numbers >= 1
jump_distance_diagonal: 1 # Accepts numbers >= 0
```

This is a special type of grid that is created from a drawn canvas. For this type of layout `canvas` is required and `size` is ignored if specified.

`canvas` is a list of strings that form a rectangular grid, from which the layout's `size` is determined automatically. Every space in the canvas creates an empty slot, while every character that is not a space creates a filled mission slot. The resulting grid determines its indices like [Grid](#Grid).

```yaml
type: canvas
canvas:
- '     ggg     ' # 0
- '    ggggg    ' # 1
- '    ggggg    ' # 2
- ' bbb ggg rrr ' # 3
- 'bbbbb g rrrrr' # 4
- 'bbbbb   rrrrr' # 5
- ' ggg     bbb ' # 6
- 'ggggg   bbbbb' # 7
- 'gggg     bbbb' # 8
- 'ggg  rrr  bbb' # 9
- ' gg rrrrr bb ' # 10
- '    rrrrr    ' # 11
- '    rrrrr    ' # 12
- '     rrr     ' # 13
jump_distance_orthogonal: 2
jump_distance_diagonal: 1
missions:
- index: group(g)
  mission_pool: Terran Missions
- index: group(b)
  mission_pool: Protoss Missions
- index: group(r)
  mission_pool: Zerg Missions
```
This example draws the Archipelago logo using missions of different races as its colors. Note that while this example fits into 13 lines, there is no set limit for how many lines you may use, and likewise lines may be as long as you need them to be. Short lines are padded with spaces to match the longest line in the canvas, so lines are left-aligned in this case.

You may have noticed that the above example has gaps between missions. Canvas layouts support jumping over gaps via `jump_distance_orthogonal` and `jump_distance_diagonal`, which determine the maximum distance over which two missions may be connected, in orthogonal and diagonal directions respectively. Missions at higher distances will only connect if there is no other mission in front of them.

```yaml
type: canvas
canvas:
- 'A  A'
- 'B XB'
jump_distance_orthogonal: 3
jump_distance_diagonal: 0
```
In this example the two `A`s will connect because they are less than 3 missions apart, but the two `B`s will not connect because `X` is between them, and both `B`s will connect to `X` instead. Both sets of `AB`s will also connect because they are neighbors.

Diagonal jumps function identically, with one exception:
```yaml
type: canvas
canvas:
- 'A  '
- ' B '
- ' XC'
jump_distance_orthogonal: 1
jump_distance_diagonal: 1
```
Missions that are diagonal neighbors only connect if they do not already share an orthogonal neighbor. In this example `A` and `B` connect, but `B` and `C` don't because `X` already connects them. No such restriction exists for higher-distance diagonal jumps, so it is recommended to keep `jump_distance_diagonal` low.

Finally, the default entrance and exit on a canvas are dynamically set to be the non-empty slots that are closest to the top left and bottom right corner respectively, but only if you don't set any entrances or exits yourself. It is highly recommended to set your own entrance and exit.

#### Canvas Index Functions
Canvas supports all of [Grid's index functions](#grid-index-functions), as well as the following:

##### group(character)
`group(character)` returns the indices which match the given character on the canvas. In the Archipelago logo example, `group(g)` gives the indices of all the `g`s on the canvas. Note that there is no group for spaces, so `group(" ")` does not work.

---
### Hopscotch
```yaml
type: hopscotch
width: 7 # Accepts numbers >= 4
spacer: 2 # Accepts numbers >= 1
two_start_positions: false # Accepts true/false
```

This order alternates between one and two missions becoming available at a time.

`width` determines how many mini columns are allowed to be next to one another before they wrap around the sides. `spacer` determines the amount of empty slots between diagonals in the client.

If `two_start_positions`, the top left corner will be set to `empty: true`, and its two neighbors will be entrances instead.

A `size: 23`, `width: 4`, `spacer: 1` Hopscotch layout has the following indices:
```yaml
 0  2
 1  3  5
    4  6  8
11     7  9
12 14    10
13 15 17
   16 18 20
      19 21
         22
```
The top left corner (index `0`) is the default entrance. The bottom-most mission of the lowest column (index `size - 1`) is the default exit.

#### Hopscotch Index Functions
Hopscotch supports the following index functions:

##### top
`top()` (or `top`) returns the indices of all the top-right corners. In the above example, it returns the indices `2, 5, 8, 11, 14, 17, 20`.

##### bottom
`bottom()` (or `bottom`) returns the indices of all the bottom-left corners. In the above example, it returns the indices `1, 4, 7, 10, 13, 16, 19, 22`.

##### middle
`middle()` (or `middle`) returns the indices of all the middle slots. In the above example, it returns the indices `0, 3, 6, 9, 12, 15, 18, 21`.

##### corner(index)
`corner(index)` returns the indices within the given corner. A corner is a slot in the middle and the slots to the bottom and right of it. `corner(0)` would return `0, 1, 2`, `corner(1)` would return `3, 4, 5`, and so on. In the above example, `corner(7)` will only return `21, 22` because it does not have a right mission.

---
### Gauntlet
```yaml
type: gauntlet
width: 7 # Accepts positive numbers
```
This type works the same way as column, but it goes horizontally instead of vertically.

`width` is the maximum allowed missions on a row before it wraps around into a new row.

A `size: 21`, `width: 7` gauntlet has the following indices:
```yaml
 0  1  2  3  4  5  6

 7  8  9 10 11 12 13

14 15 16 17 18 19 20
```
The left-most mission on the top row (index `0`) is the default entrance. The right-most mission on the bottom row (index `size - 1`) is the default exit.

---
### Blitz
```yaml
type: blitz
width: 0 # Accepts positive numbers
```
This type features rows of missions, where beating a mission in a row unlocks the entire next row.

`width` determines how many missions there are in a row. If set to 0, the width is determined automatically based on the total number of missions (the layout's `size`), but limited to be between 2 and 5.

A `size: 20`, `width: 5` Blitz layout has the following indices:
```yaml
 0  1  2  3  4
 5  6  7  8  9
10 11 12 13 14
15 16 17 18 19
```
The top left corner (index `0`) is the default entrance. The right-most mission on the bottom row (index `size - 1`) is the default exit.

#### Blitz Index Functions
Blitz supports the following index function:

##### row(height)
`row(height)` returns the indices of the row at the given zero-based height. In the above example, `row(1)` would return `5, 6, 7, 8, 9`.
