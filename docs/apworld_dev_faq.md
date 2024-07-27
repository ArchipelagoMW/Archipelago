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
