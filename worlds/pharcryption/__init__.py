from dataclasses import dataclass
from typing import ClassVar, Dict, List, Any

from BaseClasses import Item, Location, ItemClassification, MultiWorld, Region, CollectionState
from worlds.AutoWorld import World
from .Options import PharcryptionOptions

ID_OFFSET = 400_400_000


class PharcryptionItem(Item):
    game = "Pharcryption"


class PharcryptionLocation(Location):
    game = "Pharcryption"


@dataclass
class PharcryptionItemData:
    block: int
    cost: int

    def increase_cost(self):
        self.cost += 1


class PharcryptionWorld(World):
    """
    A cooperative meta-game for Archipelago where players must work together to mine Pharcoins to decrypt their items
    from a malevolent ransomware program.
    """
    game: ClassVar[str] = "Pharcryption"
    data_version: ClassVar[int] = 0
    option_definitions = PharcryptionOptions
    item_name_to_id: ClassVar[Dict[str, int]] = {
        "1 Pharcoin":     ID_OFFSET + 0,
        "2 Pharcoins":    ID_OFFSET + 1,
        "3 Pharcoins":    ID_OFFSET + 2,
        "4 Pharcoins":    ID_OFFSET + 3,
        "5 Pharcoins":    ID_OFFSET + 4,
        "Decryption Key": ID_OFFSET + 5,
        "Nothing":        ID_OFFSET + 6,
    }
    location_name_to_id: ClassVar[Dict[str, int]] = {
        f"Encrypted Item {item_i + 1} in Block {block_i + 1}": ID_OFFSET + (100 * block_i) + item_i
        for item_i in range(100)
        for block_i in range(25)
    }

    # Pharcryption specific instance values.
    players: ClassVar[int]
    item_costs: Dict[int, List[PharcryptionItemData]]
    total_item_cost: int

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        # Only allow one Pharcryption world.
        if sum(game == "Pharcryption" for game in multiworld.game.values()) > 1:
            raise RuntimeError("Only one Pharcryption world is supported at this time.")

        # Ensure there is at least one other world (except for Archipelago) in addition to Pharcryption.
        cls.players = sum(game not in ["Pharcryption", "Archipelago"] for game in multiworld.game.values())
        if cls.players < 1:
            raise RuntimeError("There must be at least one additional non-Pharcryption or non-Archipelago world.")

    def create_item(self, name: str) -> PharcryptionItem:
        return PharcryptionItem(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def generate_early(self) -> None:
        # Make all locations "priority".
        for location in self.location_name_to_id.keys():
            self.multiworld.priority_locations[self.player].value.add(location)

        # Make all items non-local.
        for item in self.item_name_to_id.keys():
            self.multiworld.non_local_items[self.player].value.add(item)

        # THIS CODE IS TERRIBLE, BUT IT DOES THE JOB
        number_of_blocks = getattr(self.multiworld, "number_of_item_blocks")[self.player].value
        items_per_block = getattr(self.multiworld, "number_of_items_per_block")[self.player].value
        maximum_item_cost = getattr(self.multiworld, "maximum_pharcoin_cost")[self.player].value
        self.total_item_cost = self.random.randint(
            items_per_block * number_of_blocks * (maximum_item_cost - 3),  # Min
            items_per_block * number_of_blocks * (maximum_item_cost - 2)   # Max
        )

        item_cost_threshold = number_of_blocks * items_per_block
        max_item_costs: List[PharcryptionItemData] = []
        cur_item_costs: List[PharcryptionItemData] = [
            PharcryptionItemData(block, 1) for block in range(number_of_blocks) for _ in range(items_per_block)
        ]
        while item_cost_threshold < self.total_item_cost:
            random_data_index = self.random.randint(0, len(cur_item_costs) - 1)
            data = cur_item_costs[random_data_index]

            data.increase_cost()
            item_cost_threshold += 1
            if data.cost >= maximum_item_cost:
                max_item_costs.append(data)
                cur_item_costs.pop(random_data_index)

        self.item_costs = {}
        for data in [*max_item_costs, *cur_item_costs]:
            self.item_costs.setdefault(data.block, []).append(data)

    def create_items(self) -> None:
        number_of_blocks = getattr(self.multiworld, "number_of_item_blocks")[self.player].value
        number_of_items = getattr(self.multiworld, "number_of_items_per_block")[self.player].value * number_of_blocks
        maximum_item_cost = getattr(self.multiworld, "maximum_pharcoin_cost")[self.player].value
        extra_pharcoins = getattr(self.multiworld, "extra_pharcoins_per_player")[self.player].value * self.players
        final_total_cost = self.total_item_cost + extra_pharcoins

        item_pool: List[PharcryptionItem] = [self.create_item("1 Pharcoin") for _ in range(number_of_items)]
        max_cost_item_pool: List[PharcryptionItem] = []
        current_point_threshold = number_of_items
        while current_point_threshold < final_total_cost:
            random_item_index = self.random.randint(0, len(item_pool) - 1)
            item = item_pool[random_item_index]

            # Increase item size.
            item.code += 1
            if item.name == "1 Pharcoin":
                item.name = "2 Pharcoins"
            elif item.name == "2 Pharcoins":
                item.name = "3 Pharcoins"
            elif item.name == "3 Pharcoins":
                item.name = "4 Pharcoins"
            elif item.name == "4 Pharcoins":
                item.name = "5 Pharcoins"

            # Remove this item from our "increment" pool when an item reaches the maximum value.
            if item.name == "5 Pharcoins":
                max_cost_item_pool.append(item)
                item_pool.pop(random_item_index)

            # Increment Point Threshold
            current_point_threshold += 1

        # Add to item pool.
        self.multiworld.itempool += max_cost_item_pool
        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        number_of_blocks = getattr(self.multiworld, "number_of_item_blocks")[self.player].value
        number_of_items_per_block = getattr(self.multiworld, "number_of_items_per_block")[self.player].value

        menu_region = Region("Menu", self.player, self.multiworld)
        previous_region = menu_region

        self.multiworld.regions.append(menu_region)
        for block in range(number_of_blocks):
            block_region = Region(f"Block {block + 1}", self.player, self.multiworld)
            previous_region.connect(
                block_region,
                None,
                lambda state, b=block:
                    self._get_pharcoin_count(state, self.player) >= sum(d.cost for d in self.item_costs.get(b - 1, []))
            )

            locations = {}
            for item in range(number_of_items_per_block):
                location_name = f"Encrypted Item {item + 1} in Block {block + 1}"
                locations[location_name] = self.location_name_to_id[location_name]

            previous_region = block_region
            block_region.add_locations(locations)
            self.multiworld.regions.append(block_region)

    def set_rules(self) -> None:
        final_block = getattr(self.multiworld, "number_of_item_blocks")[self.player].value - 1
        self.multiworld.completion_condition[self.player] = lambda state: (
            self._get_pharcoin_count(state, self.player) >= sum(data.cost for data in self.item_costs[final_block])
        )

    def fill_slot_data(self) -> Dict[str, Any]:
        use_time_limit = bool(getattr(self.multiworld, "enable_time_limit")[self.player])
        slot_data = {
            "percentage": getattr(self.multiworld, "required_percentage_of_items_decrypted_for_block_unlock")[self.player].value,
            "password": getattr(self.multiworld, "starting_password")[self.player].value,
            "timelimit": getattr(self.multiworld, "time_limit_in_minutes")[self.player].value if use_time_limit else 0,
            "item_costs": {}
        }

        for block, _list in self.item_costs.items():
            slot_data["item_costs"][block] = {}
            for index, data in enumerate(_list, 0):
                location_id = ID_OFFSET + (block * 100) + index
                item = self.multiworld.get_location(self.location_id_to_name[location_id], self.player).item
                slot_data["item_costs"][block][location_id] = {
                    "id": item.code,
                    "player": item.player,
                    "cost": data.cost,
                }

        return slot_data

    @staticmethod
    def _get_pharcoin_count(state: CollectionState, player: int) -> int:
        return state.count("1 Pharcoin", player) + \
               state.count("2 Pharcoins", player) * 2 + \
               state.count("3 Pharcoins", player) * 3 + \
               state.count("4 Pharcoins", player) * 4 + \
               state.count("5 Pharcoins", player) * 5
