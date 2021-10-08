#Archipelago Triggers Usage Guide

##What are triggers?
Triggers allow you to customize your game settings by allowing you to define certain options or even a variety of settings to occur or "trigger" whenever a certain condition happens.<br>
A good example of what you can do with triggers is the custom [mercenary mode](https://github.com/alwaysintreble/Archipelago-yaml-dump/blob/main/Snippets/Mercenary%20Mode%20Snippet.yaml) that was created using entirely triggers and plando. For more information on plando you can reference [this guide](http://archipelago.gg:48484/tutorial/zelda3/plando/en).

##Trigger use
Triggers have to be defined in the root of the yaml file meaning it must be outside of a game section. The best place to do this is the bottom of the yaml.<br>
- Triggers comprise of the trigger section and then each trigger must have an `option_category`, `option_name`, and `option_result` from which it will react to and then an `options` section where the definition of what will happen.
- `option_category` is the defining section from which the option is defined in.
    - Example: `A Link to the Past`
    - This is the root category the option is located in. If the option you're triggering off of is in root then you would use `null`, otherwise this is the game for which you want this option trigger to activate.
- `option_name` is the option setting from which the triggered choice is going to react to.
    - Example: `shop_item_slots` 
    - This can be any option from any category defined in the yaml file in either root or a game section except for `game`.
- `option_result` is the result of this option setting from which you would like to react.
    - Example: `15`
    - Each trigger must be used for exactly one option result. If you would like the same thing to occur with multiple results you would need multiple triggers for this.
- `options` is where you define what will happen when this is detected. This can be something as simple as ensuring another option also gets selected or placing an item in a certain location. 
    - Example: 
```yaml
A Link to the Past:
  start_inventory: 
    Rupees (300): 2
```
    - This format must be:
```yaml
 root option:
  option to change:
    desired result
```

###Example
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

For this example if the generator happens to roll 15 shuffled in shop item slots for your game you'll be granted 600 rupees at the beginning.
These can also be used to change other options.<br> For example:
```yaml
triggers:
  - option_category: Timespinner
    option_name: SpecificKeycards
    option_result: true
    options:
      Timespinner:
        Inverted: true
```
In this example if your world happens to roll SpecificKeycards then your game will also start in inverted.