
class ItemTier:
    def __init__(self):
        self.max_slot_bucket = None
        self.items = []

    def append(self, *items):
        self.items.extend(items)

    def extend(self, items):
        self.items.extend(items)

    def remove(self, item):
        self.items.remove(item)

    def __contains__(self, item):
        return item in self.items

    def set_max_slot_bucket(self, idx):
        self.max_slot_bucket = idx

class PriorityAssigner:
    def __init__(self):
        self._slot_tiers = []
        self._item_tiers = []

    def slot_tier(self, idx):
        while idx >= len(self._slot_tiers):
            self._slot_tiers.append([])
        return self._slot_tiers[idx]

    def item_tier(self, idx):
        while idx >= len(self._item_tiers):
            self._item_tiers.append(ItemTier())
        return self._item_tiers[idx]

    def assign(self, rnd):
        assignment = {}
        slot_tier_idx = 0
        slots = []
        items = []
        for item_tier in self._item_tiers:
            items.extend(item_tier.items)
            if item_tier.max_slot_bucket is None:
                max_slot_tier = len(self._slot_tiers) - 1
            else:
                max_slot_tier = item_tier.max_slot_bucket

            while slot_tier_idx <= max_slot_tier:
                if slot_tier_idx < len(self._slot_tiers):
                    slots.extend(self._slot_tiers[slot_tier_idx])
                slot_tier_idx += 1

            count = min(len(slots), len(items))
            rnd.shuffle(items)
            rnd.shuffle(slots)

            for i in range(count):
                assignment[slots[i]] = items[i]

            slots = slots[count:]
            items = items[count:]

        while slot_tier_idx < len(self._slot_tiers):
            if slot_tier_idx < len(self._slot_tiers):
                slots.extend(self._slot_tiers[slot_tier_idx])
            slot_tier_idx += 1

        return assignment, slots, items
