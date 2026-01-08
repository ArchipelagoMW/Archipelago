from BaseClasses import Location, MultiWorld
from .Options import RandomGunTierD, RandomGunTierC, RandomGunTierB, RandomGunTierA, RandomGunTierS, \
    RandomItemTierD, RandomItemTierC, RandomItemTierB, RandomItemTierA, RandomItemTierS, PickupAmount, TrapAmount

class GungeonLocation(Location):
    game: str = "Enter The Gungeon"

def get_total_locations() -> int:
    total_locations = RandomGunTierD.range_end
    total_locations += RandomGunTierC.range_end
    total_locations += RandomGunTierB.range_end
    total_locations += RandomGunTierA.range_end
    total_locations += RandomGunTierS.range_end
    total_locations += RandomItemTierD.range_end
    total_locations += RandomItemTierC.range_end
    total_locations += RandomItemTierB.range_end
    total_locations += RandomItemTierA.range_end
    total_locations += RandomItemTierS.range_end
    # Gnawed Key, Old Crest, Weird Egg
    total_locations += 3
    total_locations += PickupAmount.range_end
    total_locations += TrapAmount.range_end
    return total_locations

location_table = { }

# Fill location table with chests until we reach the maximum possible item amount
for i in range(0, get_total_locations()):
    location_table.update({f"Chest {i + 1} (Any Rarity)": 8755000 + i})

event_location_table = {
    "Blobulord": None,
    "The Old King": None,
    "The Resourceful Rat": None,
    "Agunim": None,
    "The Advanced Dragun": None,
    "The High Dragun": None,
    "The Lich": None
}

location_table.update(event_location_table)
