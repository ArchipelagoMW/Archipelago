# APWorld Dev FAQ

This document is meant as a reference tool to show the best known solutions to common problems when developing an apworld

## My game has a restrictive start that leads to fill errors


Hint to the Generator that an item needs to be in sphere one with local_early_items
```
early_item_name = "Sword"
self.multiworld.local_early_items[self.player][early_item_name] = 1
```