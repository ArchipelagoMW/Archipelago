# APWorld integration

This document describes the changes you need to make to fully integrate your APWorld with Universal Tracker (UT). It assumes you are already familiar with the basics of how UT works. If you haven't already, read through the [re-gen-passthrough](re-gen-passthrough.md) document.

The examples listed in this document are high-level. For reference implementations for these different features take a look at the [UT Integration Library](https://discord.com/channels/731205301247803413/1367996449270530080/1367997223991902219) thread in the AP discord.

## Providing information during generation

UT does not have access to the seed used during the original generation. This means that any randomization that is not a direct result of YAML options or AP items will not be the same when UT runs and must be provided in slot data. This can include entrance rando, level order, starting location, or similar options that don't use items directly.

Best practice is to pass these randomized results into `fill_slot_data`.

```python
    def fill_slot_data(self) -> dict[str, Any]:
        return {
            "starting_location": self.starting_location,
            "entrances": self.randomized_entrances, # eg the result of calling randomize_entrances(...).pairings
            # Add any as needed
        }
```

## Loading provided information

You can access the slot data from the original generation by defining an `interpret_slot_data` function in your world. UT will call this function once connected to the multiworld with the slot data it received from that slot. Using this data, you can adjust any world state that affects your rules, such as world instance attributes or entrance connections.

```python
    def interpret_slot_data(self, slot_data: dict[str, Any]) -> None:
        if "starting_location" in slot_data:
            self.origin_region_name = slot_data["starting_location"]

        if "entrances" in slot_data:
            # Update entrance connections for ER
            entrances = {
                entrance.name: entrance
                for region in self.get_regions()
                for entrance in region.entrances
            }
            for source_exit, target_entrance in slot_data["entrances"]:
                entrances[source_exit].connected_region = entrances[target_entrance].parent_region
```

You may also want to adjust your world's behaviour in other functions to reduce the amount of work you need to do in `interpret_slot_data`. To do so, you can check the `generation_is_fake` attribute on the `multiworld` object, which will be `True` if your world is generating inside UT. You can use this to skip doing things that will be handled by `interpret_slot_data` later, or to run code that would normally be skipped based on options. For example, you can create every possible location and let UT filter them out to just what exists from the server so you don't need to worry about creating them later.

```python
    def create_regions(self) -> None:
        is_ut = getattr(self.multiworld, "generation_is_fake", False)
        if self.randomly_rolled_property == 1 or is_ut:
            # This location will always be created by UT regardless of what UT happens to roll
            self.create_location(...)
```

## Generating without a YAML

You can also make it so a YAML is not required to generate for your world. To do so, you must first store all options that affect generation in your slot data. Take care not to include options that don't affect generation and aren't useful for the game client.

```python
    def fill_slot_data(self) -> dict[str, Any]:
        return {
            # Keep other randomized results as above
            "options": self.options.as_dict("randomize_things", "randomize_stuff", "logic_difficulty"),
        }
```

To make implementation simpler, instead of the large amount of adjustments you'd likely have to make in `interpret_slot_data`, you can instead turn it into a static method that simply returns the slot data. This will inform UT that instead of doing an initial generation when it opens, it will do a regeneration once connected to the multiworld.

```python
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        # Trigger a regen in UT
        return slot_data
```

During the regeneration, you can access the slot data via `re_gen_passthrough` on the multiworld object. Early in the generation you can inspect this object to set any instance attributes or options needed from the slot data so your later functions will behave as expected.

```python
    def generate_early(self) -> None:
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            # Get the passed through slot data from the real generation
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]

            slot_options: dict[str, Any] = slot_data.get("options", {})
            # Set all your options here instead of getting them from the yaml
            for key, value in slot_options.items():
                opt: Optional[Option] = getattr(self.options, key, None)
                if opt is not None:
                    # You can also set .value directly but that won't work if you have OptionSets
                    setattr(self.options, key, opt.from_any(value))
```

The last thing you can do is inform UT that your world can generate without a YAML. This is not necessary to do, but it may be convenient. It does mean that someone cannot edit their local YAML to see what would have been in logic had they chosen different options.

```python
class MyWorld(World):
    ut_can_gen_without_yaml = True
```
