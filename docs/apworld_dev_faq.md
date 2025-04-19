# APWorld Dev FAQ

This document is meant as a reference tool to show solutions to common problems when developing an apworld.
It is not intended to answer every question about Archipelago and it assumes you have read the other docs, 
including [Contributing](contributing.md), [Adding Games](<adding games.md>), and [World API](<world api.md>).

---

### My game has a restrictive start that leads to fill errors

Hint to the Generator that an item needs to be in sphere one with local_early_items. Here, `1` represents the number of "Sword" items to attempt to place in sphere one.
```py
early_item_name = "Sword"
self.multiworld.local_early_items[self.player][early_item_name] = 1
```

Some alternative ways to try to fix this problem are:
* Add more locations to sphere one of your world, potentially only when there would be a restrictive start
* Pre-place items yourself, such as during `create_items`
* Put items into the player's starting inventory using `push_precollected`
* Raise an exception, such as an `OptionError` during `generate_early`, to disallow options that would lead to a restrictive start

---

### I have multiple settings that change the item/location pool counts and need to balance them out

In an ideal situation your system for producing locations and items wouldn't leave any opportunity for them to be unbalanced. But in real, complex situations, that might be unfeasible.

If that's the case, you can create extra filler based on the difference between your unfilled locations and your itempool by comparing [get_unfilled_locations](https://github.com/ArchipelagoMW/Archipelago/blob/main/BaseClasses.py#:~:text=get_unfilled_locations) to your list of items to submit

Note: to use self.create_filler(), self.get_filler_item_name() should be defined to only return valid filler item names
```py
total_locations = len(self.multiworld.get_unfilled_locations(self.player))
item_pool = self.create_non_filler_items()

for _ in range(total_locations - len(item_pool)):
    item_pool.append(self.create_filler())

self.multiworld.itempool += item_pool
```

A faster alternative to the `for` loop would be to use a [list comprehension](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions):
```py
item_pool += [self.create_filler() for _ in range(total_locations - len(item_pool))]
```

---

### I learned about indirect conditions in the world API document, but I want to know more. What are they and why are they necessary?

The world API document mentions how to use `multiworld.register_indirect_condition` to register indirect conditions and **when** you should use them, but not *how* they work and *why* they are necessary. This is because the explanation is quite complicated.

Region sweep (the algorithm that determines which regions are reachable) is a Breadth-First Search of the region graph. It starts from the origin region, checks entrances one by one, and adds newly reached regions and their entrances to the queue until there is nothing more to check.

For performance reasons, AP only checks every entrance once. However, if an entrance's access_rule depends on region access, then the following may happen:
1. The entrance is checked and determined to be nontraversable because the region in its access_rule hasn't been reached yet during the graph search.
2. Then, the region in its access_rule is determined to be reachable.

This entrance *would* be in logic if it were rechecked, but it won't be rechecked this cycle.
To account for this case, AP would have to recheck all entrances every time a new region is reached until no new regions are reached.

An indirect condition is how you can manually define that a specific entrance needs to be rechecked during region sweep if a specific region is reached during it.
This keeps most of the performance upsides. Even in a game making heavy use of indirect conditions (ex: The Witness), using them is significantly faster than just "rechecking each entrance until nothing new is found".
The reason entrance access rules using `location.can_reach` and `entrance.can_reach` are also affected is because they call `region.can_reach` on their respective parent/source region.

We recognize it can feel like a trap since it will not alert you when you are missing an indirect condition, and that some games have very complex access rules.
As of [PR #3682 (Core: Region handling customization)](https://github.com/ArchipelagoMW/Archipelago/pull/3682) being merged, it is possible for a world to opt out of indirect conditions entirely, instead using the system of checking each entrance whenever a region has been reached, although this does come with a performance cost.
Opting out of using indirect conditions should only be used by games that *really* need it. For most games, it should be reasonable to know all entrance &rarr; region dependencies, making indirect conditions preferred because they are much faster.

---

### I uploaded the generated output of my world to the webhost and webhost is erroring on corrupted multidata

The error `Could not load multidata. File may be corrupted or incompatible.` occurs when uploading a locally generated
file where there is an issue with the multidata contained within it. It may come with a description like
`(No module named 'worlds.myworld')` or `(global 'worlds.myworld.names.ItemNames' is forbidden)`

Pickling is a way to compress python objects such that they can be decompressed and be used to rebuild the
python objects. This means that if one of your custom class instances ends up in the multidata, the server would not
be able to load that custom class to decompress the data, which can fail either because the custom class is unknown
(because it cannot load your world module) or the class it's attempting to import to decompress is deemed unsafe.

Common situations where this can happen include:
* Using Option instances directly in slot_data. Ex: using `options.option_name` instead of `options.option_name.value`.
  Also, consider using the `options.as_dict("option_name", "option_two")` helper.
* Using enums as Location/Item names in the datapackage. When building out `location_name_to_id` and `item_name_to_id`,
  make sure that you are not using your enum class for either the names or ids in these mappings.
