# APWorld Dev FAQ

This document is meant as a reference tool to show the best known solutions to common problems when developing an apworld

---

### My game has a restrictive start that leads to fill errors

Hint to the Generator that an item needs to be in sphere one with local_early_items
```
early_item_name = "Sword"
self.multiworld.local_early_items[self.player][early_item_name] = 1
```

---

### I have multiple settings that change the item/location pool counts and need to balance them out

Create extra filler based on the difference between your unfilled locations and your itempool by comparing [get_unfilled_locations](/BaseClasses.py) to your list of items to submit
```
total_locations = len(self.multiworld.get_unfilled_locations(self.player))
item_pool = self.create_non_filler_items()

while len(item_pool) < total_locations:
    item_pool.append(self.create_filler())

self.multiworld.itempool += item_pool
```
