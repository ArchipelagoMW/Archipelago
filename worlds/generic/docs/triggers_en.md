# Archipelago Triggers Guide

This guide details the use of the Archipelago YAML trigger system. This guide is intended for a more advanced user with
more in-depth knowledge of Archipelago YAML options as well as experience editing YAML files. This guide should take
about 5 minutes to read.

## What are triggers?

Triggers allow you to customize your game options by allowing you to define one or many options which only occur under
specific conditions. These are essentially "if, then" statements for options in your game. A good example of what you
can do with triggers is the [custom mercenary mode YAML
](https://github.com/alwaysintreble/Archipelago-yaml-dump/blob/main/Snippets/Mercenary%20Mode%20Snippet.yaml) that was
created using entirely triggers and plando.

For more information on plando, you can reference the [general plando guide](/tutorial/Archipelago/plando/en) or the
[A Link to the Past plando guide](/tutorial/A%20Link%20to%20the%20Past/plando/en).

## Trigger use

Triggers may be defined in either the root or in the relevant game sections. Generally, the best place to do this is the
bottom of the YAML for clear organization.

Each trigger consists of four parts:
- `option_category` specifies the section which the triggering option is defined in.
    - Example: `A Link to the Past`
    - This is the category the option is located in. If the option you're triggering off of is in root then you
      would use `null`, otherwise this is the game for which you want this option trigger to activate.
- `option_name` specifies the name of the triggering option.
    - Example: `shop_item_slots`
    - This can be any option from any category defined in the YAML file in either root or a game section.
- `option_result` specifies the value of the option that activates this trigger.
    - Example: `15`
    - Each trigger must be used for exactly one option result. If you would like the same thing to occur with multiple
      results, you would need multiple triggers for this.
- `options` is where you define what will happen when the trigger activates. This can be something as simple as ensuring
  another option also gets selected or placing an item in a certain location. It is possible to have multiple things
  happen in this section.
    - Example:
  ```yaml
  A Link to the Past:
    start_inventory: 
      Rupees (300): 2
  ```

The general format is:

  ```yaml
  category:
    option to change:
      desired result
  ```

### Examples

The above examples all together will end up looking like this:

  ```yaml
  triggers:
    - option_category: A Link to the Past
      option_name: shop_item_slots
      option_result: 15
      options:
        A Link to the Past:
          start_inventory:
            Rupees(300): 2
  ```

For this example, if the generator happens to roll 15 shuffled in shop item slots for your game, you'll be granted 600
rupees at the beginning. Triggers can also be used to change other options.

For example:

  ```yaml
  triggers:
    - option_category: Timespinner
      option_name: SpecificKeycards
      option_result: true
      options:
        Timespinner:
          Inverted: true
  ```

In this example, if your world happens to roll SpecificKeycards, then your game will also start in inverted.

It is also possible to use imaginary values in options to trigger specific settings. You can use these made-up values in
either your main options or to trigger from another trigger. Currently, this is the only way to trigger on "setting 1
AND setting 2".

For example:

  ```yaml
  triggers:
    - option_category: Secret of Evermore
      option_name: doggomizer
      option_result: pupdunk
      options:
        Secret of Evermore:
          difficulty:
            normal: 50
            pupdunk_hard: 25
            pupdunk_mystery: 25
          exp_modifier:
            150: 50
            200: 50
    - option_category: Secret of Evermore
      option_name: difficulty
      option_result: pupdunk_hard
      options:
        Secret of Evermore:
          fix_wings_glitch: false
          difficulty: hard
    - option_category: Secret of Evermore
      option_name: difficulty
      option_result: pupdunk_mystery
      options:
        Secret of Evermore:
          fix_wings_glitch: false
          difficulty: mystery
  ```

In this example (thanks to @Black-Sliver), if the `pupdunk` option is rolled, then the difficulty values will be rolled
again using the new options `normal`, `pupdunk_hard`, and `pupdunk_mystery`, and the exp modifier will be rerolled using
new weights for 150 and 200. This allows for two more triggers that will only be used for the new `pupdunk_hard`
and `pupdunk_mystery` options so that they will only be triggered on "pupdunk AND hard/mystery".

## Adding or Removing from a List, Set, or Dict Option

List, set, and dict options can additionally have values added to or removed from itself without overriding the existing
option value by prefixing the option name in the trigger block with `+` (add) or `-` (remove). The exact behavior for 
each will depend on the option type.

- For sets, `+` will add the value(s) to the set and `-` will remove the value(s) from the set. Sets do not allow 
  duplicates.
- For lists, `+` will add new values(s) to the list and `-` will remove the first matching values(s) it comes across. 
  Lists allow duplicate values.
- For dicts, `+` will add the value(s) to the given key(s) inside the dict if it exists, or add it otherwise. `-` is the
  inverse operation of addition (and negative values are allowed).

For example:

```yaml
Super Metroid:
  start_location: 
    landing_site: 50
    aqueduct: 50
  start_hints:
    - Morph Ball
  start_inventory:
    Power Bombs: 1
  triggers:
    - option_category: Super Metroid
      option_name: start_location
      option_result: aqueduct
      options:
        Super Metroid:
          +start_hints:
            - Gravity Suit
```

In this example, if the `start_location` option rolls `landing_site`, only a starting hint for Morph Ball will be 
created. If `aqueduct` is rolled, a starting hint for Gravity Suit will also be created alongside the hint for Morph 
Ball.
