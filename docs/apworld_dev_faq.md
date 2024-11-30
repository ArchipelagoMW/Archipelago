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

The world API document mentions registering indirect conditions using multiworld.register_indirect_condition() and **when** you should use them, but not *how* they work and *why* they are necessary. This is because the explanation is quite complicated.

Region sweep (the algorithm that determines which regions are reachable) is a Breadth-First Search of the region graph from the origin region, checking entrances one by one and adding newly reached nodes (regions) and their entrances to the queue until there is nothing more to check.

For performance reasons, AP only checks every entrance once. However, if any entrance's access_rule depends on region access, then it is possible for this to happen:
1. An entrance that depends on a region is checked and determined to be nontraversable because the region hasn't been reached yet during the graph search.
2. After that, the region is reached by the graph search.

The entrance *would* now be determined to be traversable if it were rechecked, but it is not.
To account for this case, AP would have to recheck all entrances every time a new region is reached until no new regions are reached.

However, there is a way to **manually** define that a *specific* entrance needs to be rechecked during region sweep if a *specific* region is reached during it. This is what an indirect condition is.
This keeps almost all of the performance upsides. Even a game making heavy use of indirect conditions (See: The Witness) is still significantly faster than if it just blanket "rechecked all entrances until nothing new is found".
The reason entrance access rules using `location.can_reach` and `entrance.can_reach` are also affected is simple: They call `region.can_reach` on their respective parent/source region.

We recognize it can feel like a trap since it will not alert you when you are missing an indirect condition, and that some games have very complex access rules.
As of [PR #3682 (Core: Region handling customization)](https://github.com/ArchipelagoMW/Archipelago/pull/3682) being merged, it is also possible for a world to opt out of indirect conditions entirely, although it does come at a flat performance cost.
It should only be used by games that *really* need it. For most games, it should be reasonable to know all entrance &rarr; region dependencies, and in this case, indirect conditions are still preferred because they are faster.
