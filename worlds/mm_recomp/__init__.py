from typing import List
from typing import Dict

from BaseClasses import Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import MMRItem, item_data_table, item_table, code_to_item_table
from .Locations import MMRLocation, location_data_table, location_table, code_to_location_table, locked_locations, prices_ints
from .Options import MMROptions
from .Regions import region_data_table, get_exit
from .Rules import *
from .NormalRules import *
from .Constants import default_shop_prices

class MMRWebWorld(WebWorld):
    # ~ theme = "partyTime"
    
    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Majora's Mask Recompiled in Archipelago.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["LittleCube"]
    )
    
    tutorials = [setup_en]


class MMRWorld(World):
    """A Zelda game we're not completely burnt out on."""

    game = "Majora's Mask Recompiled"
    data_version = 1
    web = MMRWebWorld()
    options_dataclass = MMROptions
    options = MMROptions
    location_name_to_id = location_table
    item_name_to_id = item_table
    prices = ""

    def generate_early(self):
        pass
    
    def create_item(self, name: str) -> MMRItem:
        return MMRItem(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def place(self, location, item):
        player = self.player
        mw = self.multiworld

        mw.get_location(location, player).place_locked_item(self.create_item(item))

    def create_items(self) -> None:
        mw = self.multiworld

        item_pool: List[MMRItem] = []
        item_pool_count: Dict[str, int] = {}
        for name, item in item_data_table.items():
            item_pool_count[name] = 0
            if item.code and item.can_create(self.options):
                while item_pool_count[name] < item.num_exist:
                    item_pool.append(self.create_item(name))
                    item_pool_count[name] += 1

        mw.itempool += item_pool

        mw.push_precollected(self.create_item("Ocarina of Time"))
        mw.push_precollected(self.create_item("Song of Time"))

        if self.options.swordless.value:
            mw.itempool.append(self.create_item("Progressive Sword"))

        if self.options.shieldless.value:
            mw.itempool.append(self.create_item("Progressive Shield"))
            
        if self.options.start_with_soaring.value:
            mw.push_precollected(self.create_item("Song of Soaring"))
            self.create_and_add_filler_items()
        
        if self.options.shuffle_spiderhouse_reward.value:
            mw.itempool.append(self.create_item("Progressive Wallet"))

        if self.options.shuffle_regional_maps.value == 1:
            mw.push_precollected(self.create_item("Clock Town Map"))
            mw.push_precollected(self.create_item("Woodfall Map"))
            mw.push_precollected(self.create_item("Snowhead Map"))
            mw.push_precollected(self.create_item("Romani Ranch Map"))
            mw.push_precollected(self.create_item("Great Bay Map"))
            mw.push_precollected(self.create_item("Stone Tower Map"))
            self.create_and_add_filler_items(6)
            
        if self.options.scrubsanity.value != 0:
            self.create_and_add_filler_items(4)
        
        if self.options.shopsanity.value != 0:
            self.create_and_add_filler_items(27)

        if self.options.shopsanity.value == 2:
            self.create_and_add_filler_items(15)
        
        if self.options.cowsanity.value != 0:
            self.create_and_add_filler_items(8)

        shp = self.options.starting_hearts.value
        if self.options.starting_hearts_are_containers_or_pieces.value == 0:
            for i in range(0, int((12 - shp)/4)):
                mw.itempool.append(self.create_item("Heart Container"))
            for i in range(0, (12 - shp) % 4):
                mw.itempool.append(self.create_item("Heart Piece"))
        else:
            for i in range(0, 12 - shp):
                mw.itempool.append(self.create_item("Heart Piece"))

    def create_regions(self) -> None:
        player = self.player
        mw = self.multiworld

        # Create shop prices.
        if self.options.shopsanity.value != 0:
            price_max = 0

            if self.options.shop_prices.value == 2:
                price_max = 99
            elif self.options.shop_prices.value == 3:
                price_max = 200
            elif self.options.shop_prices.value == 4:
                price_max = 500

            # There are 34 (+2 fake) shop locations that need prices
            for i in range(0, 36):
                if self.options.shop_prices.value == 0:
                    price = default_shop_prices[i]
                else:
                    price = self.random.randint(0, price_max)
                prices_ints.append(price)
                self.prices += str(price) + " "

            self.prices = self.prices[:-1]

        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, player, mw)
            mw.regions.append(region)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = mw.get_region(region_name, player)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in location_data_table.items()
                if location_data.region == region_name and location_data.can_create(self.options)
            }, MMRLocation)
            region.add_exits(region_data.connecting_regions)

        # Place locked locations.
        for location_name, location_data in locked_locations.items():
            # Ignore locations we never created.
            if not location_data.can_create(self.options):
                continue

            self.place(location_name, location_data_table[location_name].locked_item)

        if self.options.shuffle_regional_maps.value == 0:
            self.place("Tingle Clock Town Map Purchase", "Clock Town Map")
            self.place("Tingle Woodfall Map Purchase", "Woodfall Map")
            self.place("Tingle Snowhead Map Purchase", "Snowhead Map")
            self.place("Tingle Romani Ranch Map Purchase", "Romani Ranch Map")
            self.place("Tingle Great Bay Map Purchase", "Great Bay Map")
            self.place("Tingle Stone Tower Map Purchase", "Stone Tower Map")

        if self.options.shuffle_boss_remains.value == 0:
            self.place("Woodfall Temple Odolwa's Remains", "Odolwa's Remains")
            self.place("Snowhead Temple Goht's Remains", "Goht's Remains")
            self.place("Great Bay Temple Gyorg's Remains", "Gyorg's Remains")
            self.place("Stone Tower Temple Inverted Twinmold's Remains", "Twinmold's Remains")
        
        if self.options.shuffle_boss_remains.value == 2:
            remains_list = ["Odolwa's Remains", "Goht's Remains", "Gyorg's Remains", "Twinmold's Remains"]
            
            self.place("Woodfall Temple Odolwa's Remains", remains_list.pop(self.random.randint(0, 3)))
            self.place("Snowhead Temple Goht's Remains", remains_list.pop(self.random.randint(0, 2)))
            self.place("Great Bay Temple Gyorg's Remains", remains_list.pop(self.random.randint(0, 1)))
            self.place("Stone Tower Temple Inverted Twinmold's Remains", remains_list[0])

        if not self.options.shuffle_spiderhouse_reward.value:
            self.place("Swamp Spider House Reward", "Mask of Truth")
            self.place("Ocean Spider House Reward", "Progressive Wallet")

        if self.options.skullsanity.value == 0:
            for i in range(0, 31):
                if i != 3:
                    self.place(code_to_location_table[0x3469420062700 | i], "Swamp Skulltula Token")
                if i != 0:
                    self.place(code_to_location_table[0x3469420062800 | i], "Ocean Skulltula Token")
                

        if not self.options.shuffle_great_fairy_rewards.value:
            self.place("North Clock Town Great Fairy Reward", "Progressive Magic")
            self.place("North Clock Town Great Fairy Reward (Has Transformation Mask)", "Great Fairy Mask")
            self.place("Woodfall Great Fairy Reward", "Great Spin Attack")
            self.place("Snowhead Great Fairy Reward", "Progressive Magic")
            self.place("Great Bay Great Fairy Reward", "Double Defense")
            self.place("Stone Tower Great Fairy Reward", "Great Fairy Sword")

        if not self.options.keysanity.value:
            self.place("Woodfall Temple Moving Flower Platform Room Chest", "Small Key (Woodfall)")

            self.place("Snowhead Temple Orange Door Behind Block Chest", "Small Key (Snowhead)")
            self.place("Snowhead Temple Upstairs 2F Icicle Room Snowball Chest", "Small Key (Snowhead)")
            self.place("Snowhead Temple Initial Runway Ice Blowers Chest", "Small Key (Snowhead)")

            self.place("Great Bay Temple Froggy Entrance Room Underwater Chest", "Small Key (Great Bay)")

            self.place("Stone Tower Temple Armos Room Lava Chest", "Small Key (Stone Tower)")
            self.place("Stone Tower Temple Eyegore Room Dexi Hand Ledge Chest", "Small Key (Stone Tower)")
            self.place("Stone Tower Temple Inverted Eastern Air Gust Room Hall Floor Switch Chest", "Small Key (Stone Tower)")
            self.place("Stone Tower Temple Inverted Death Armos Maze Chest", "Small Key (Stone Tower)")

        if not self.options.fairysanity.value:
            self.place("Laundry Pool Stray Fairy (Clock Town)", "Stray Fairy (Clock Town)")

            self.place("Woodfall Temple Entrance Chest", "Stray Fairy (Woodfall)")
            self.place("Woodfall Temple Wooden Flower Switch Chest", "Stray Fairy (Woodfall)")
            self.place("Woodfall Temple Black Boe Room Chest", "Stray Fairy (Woodfall)")
            self.place("Woodfall Temple Entrance Freestanding SF", "Stray Fairy (Woodfall)")
            self.place("Woodfall Temple Wooden Flower Deku Baba SF", "Stray Fairy (Woodfall)")
            self.place("Woodfall Temple Wooden Flower Pot SF", "Stray Fairy (Woodfall)")
            self.place("Woodfall Temple Moving Flower Platform Room Beehive SF", "Stray Fairy (Woodfall)")
            self.place("Woodfall Temple Wooden Flower Bubble SF", "Stray Fairy (Woodfall)")
            self.place("Woodfall Temple Push Block Skulltula SF", "Stray Fairy (Woodfall)")
            self.place("Woodfall Temple Push Block Bubble SF", "Stray Fairy (Woodfall)")
            self.place("Woodfall Temple Push Block Beehive SF", "Stray Fairy (Woodfall)")
            self.place("Woodfall Temple Final Room Right Lower Platform SF", "Stray Fairy (Woodfall)")
            self.place("Woodfall Temple Final Room Right Upper Platform SF", "Stray Fairy (Woodfall)")
            self.place("Woodfall Temple Final Room Left Upper Platform SF", "Stray Fairy (Woodfall)")
            self.place("Woodfall Temple Final Room Bubble SF", "Stray Fairy (Woodfall)")
            
            self.place("Snowhead Temple Bottom Floor Switch Chest", "Stray Fairy (Snowhead)")
            self.place("Snowhead Temple Elevator Room Invisible Platform Chest", "Stray Fairy (Snowhead)")
            self.place("Snowhead Temple Orange Door Upper Chest", "Stray Fairy (Snowhead)")
            self.place("Snowhead Temple Green Door Ice Blowers Chest", "Stray Fairy (Snowhead)")
            self.place("Snowhead Temple Light Blue Door Upper Chest", "Stray Fairy (Snowhead)")
            self.place("Snowhead Temple Upstairs 2F Icicle Room Hidden Chest", "Stray Fairy (Snowhead)")
            self.place("Snowhead Temple Column Room 2F Hidden Chest", "Stray Fairy (Snowhead)")
            self.place("Snowhead Temple Initial Runway Tower Bubble SF", "Stray Fairy (Snowhead)")
            self.place("Snowhead Temple Initial Runway Under Platform Bubble SF", "Stray Fairy (Snowhead)")
            self.place("Snowhead Temple Elevator Freestanding SF", "Stray Fairy (Snowhead)")
            self.place("Snowhead Temple Grey Door Near Bombable Stairs Box SF", "Stray Fairy (Snowhead)")
            self.place("Snowhead Temple Timed Switch Room Bubble SF", "Stray Fairy (Snowhead)")
            self.place("Snowhead Temple Snowmen Bubble SF", "Stray Fairy (Snowhead)")
            self.place("Snowhead Temple Dinolfos Room First SF", "Stray Fairy (Snowhead)")
            self.place("Snowhead Temple Dinolfos Room Second SF", "Stray Fairy (Snowhead)")

            self.place("Great Bay Temple Four Torches Chest", "Stray Fairy (Great Bay)")
            self.place("Great Bay Temple Bio-Baba Hall Chest", "Stray Fairy (Great Bay)")
            self.place("Great Bay Temple Green Pipe Freezable Waterwheel Upper Chest", "Stray Fairy (Great Bay)")
            self.place("Great Bay Temple Green Pipe Freezable Waterwheel Lower Chest", "Stray Fairy (Great Bay)")
            self.place("Great Bay Temple Seesaw Room Chest", "Stray Fairy (Great Bay)")
            self.place("Great Bay Temple Room Behind Waterfall Ceiling Chest", "Stray Fairy (Great Bay)")
            self.place("Great Bay Temple Waterwheel Room Skulltula SF", "Stray Fairy (Great Bay)")
            self.place("Great Bay Temple Waterwheel Room Bubble Under Platform SF", "Stray Fairy (Great Bay)")
            self.place("Great Bay Temple Pot At Bottom Of Blender SF", "Stray Fairy (Great Bay)")
            self.place("Great Bay Temple Blender Room Barrel SF", "Stray Fairy (Great Bay)")
            self.place("Great Bay Temple Red-Green Pipe First Room Pot SF", "Stray Fairy (Great Bay)")
            self.place("Great Bay Temple Froggy Entrance Room Pot SF", "Stray Fairy (Great Bay)")
            self.place("Great Bay Temple Seesaw Room Underwater Barrel SF", "Stray Fairy (Great Bay)")
            self.place("Great Bay Temple Before Boss Room Underneath Platform Bubble SF", "Stray Fairy (Great Bay)")
            self.place("Great Bay Temple Before Boss Room Exit Tunnel Bubble SF", "Stray Fairy (Great Bay)")

            self.place("Stone Tower Temple Entrance Room Eye Switch Chest", "Stray Fairy (Stone Tower)")
            self.place("Stone Tower Temple Armos Room Upper Chest", "Stray Fairy (Stone Tower)")
            self.place("Stone Tower Temple Eyegore Room Switch Chest", "Stray Fairy (Stone Tower)")
            self.place("Stone Tower Temple Mirror Room Sun Face Chest", "Stray Fairy (Stone Tower)")
            self.place("Stone Tower Temple Mirror Room Sun Block Chest", "Stray Fairy (Stone Tower)")
            self.place("Stone Tower Temple Air Gust Room Side Chest", "Stray Fairy (Stone Tower)")
            self.place("Stone Tower Temple Air Gust Room Goron Switch Chest", "Stray Fairy (Stone Tower)")
            self.place("Stone Tower Temple Eyegore Chest", "Stray Fairy (Stone Tower)")
            self.place("Stone Tower Temple Eastern Water Room Underwater Chest", "Stray Fairy (Stone Tower)")
            self.place("Stone Tower Temple Inverted Entrance Room Sun Face Chest", "Stray Fairy (Stone Tower)")
            self.place("Stone Tower Temple Inverted Eastern Air Gust Room Ice Eye Switch Chest", "Stray Fairy (Stone Tower)")
            self.place("Stone Tower Temple Inverted Wizzrobe Chest", "Stray Fairy (Stone Tower)")
            self.place("Stone Tower Temple Inverted Eastern Air Gust Room Fire Chest", "Stray Fairy (Stone Tower)")
            self.place("Stone Tower Temple Entrance Room Lower Chest", "Stray Fairy (Stone Tower)")
            self.place("Stone Tower Temple After Garo Upside Down Chest", "Stray Fairy (Stone Tower)")

        sword_location = mw.get_location("Link's Inventory (Kokiri Sword)", player)
        if self.options.swordless.value:
            sword_location.item_rule = lambda item: item.name != "Progressive Sword"
        else:
            sword_location.place_locked_item(self.create_item("Progressive Sword"))

        shield_location = mw.get_location("Link's Inventory (Hero's Shield)", player)
        if self.options.shieldless.value:
            shield_location.item_rule = lambda item: item.name != "Progressive Shield"
        else:
            shield_location.place_locked_item(self.create_item("Progressive Shield"))

        shp = self.options.starting_hearts.value
        if self.options.starting_hearts_are_containers_or_pieces.value == 0:
            containers = int(shp/4) - 1
            for i in range(0, containers):
                self.place(code_to_location_table[0x34694200D0000 | i], "Heart Container")

            hearts_left = shp % 4
            for i in range(0, hearts_left):
                self.place(code_to_location_table[0x34694200D0000 | (containers + i)], "Heart Piece")

            if (shp % 4) != 0:
                for i in range(containers + hearts_left, containers + 4):
                    mw.get_location(code_to_location_table[0x34694200D0000 | i], player).item_rule = lambda item: item.name != "Heart Piece" and item.name != "Heart Container"
        else:
            for i in range(0, shp - 4):
                self.place(code_to_location_table[0x34694200D0000 | i], "Heart Piece")

            for i in range(shp - 4, 8):
                mw.get_location(code_to_location_table[0x34694200D0000 | i], player).item_rule = lambda item: item.name != "Heart Piece" and item.name != "Heart Container"

        # TODO: check options to see what player starts with
        # ~ mw.get_location("Top of Clock Tower (Ocarina of Time)", player).place_locked_item(self.create_item(self.get_filler_item_name()))
        # ~ mw.get_location("Top of Clock Tower (Song of Time)", player).place_locked_item(self.create_item(self.get_filler_item_name()))

    def create_and_add_filler_items(self, count: int = 1):
        for i in range(count):
            self.multiworld.itempool.append(self.create_item(self.get_filler_item_name()))

    def get_filler_item_name(self) -> str:
        filler_items = ["Blue Rupee", "Red Rupee", "Purple Rupee", "Silver Rupee", "Gold Rupee"]
        return self.random.choice(filler_items)
        # filler_weights = (50, 25, 10, 5, 1)
        # return self.random.choices(filler_items, weights=filler_weights)[0]

    def set_rules(self) -> None:
        player = self.player
        mw = self.multiworld
        options = self.options

        # Completion condition.
        mw.completion_condition[player] = lambda state: state.has("Victory", player)

        if (self.options.logic_difficulty.value == 4):
            return

        # ~ if (self.options.logic_difficulty.value == 0):
            # ~ region_rules = get_baby_region_rules(player, options)
            # ~ location_rules = get_baby_location_rules(player, options)
        if (self.options.logic_difficulty.value == 1):
            region_rules = get_region_rules(player, options)
            location_rules = get_location_rules(player, options)

        for entrance_name, rule in region_rules.items():
            entrance = mw.get_entrance(entrance_name, player)
            entrance.access_rule = rule

        for location in mw.get_locations(player):
            name = location.name
            if self.options.skullsanity.value == 2 and (name == "Swamp Spider House Reward" or name == "Ocean Spider House Reward"):
                continue
            if name in location_rules and location_data_table[name].can_create(self.options):
                location.access_rule = location_rules[name]

    def fill_slot_data(self):
        shp = self.options.starting_hearts.value
        starting_containers = int(shp/4) - 1
        starting_pieces = shp % 4
        shuffled_containers = int((12 - shp)/4)
        shuffled_pieces = (12 - shp) % 4
        return {
            "skullsanity": self.options.skullsanity.value,
            "fairysanity": self.options.fairysanity.value,
            "shopsanity": self.options.shopsanity.value,
            "scrubsanity": self.options.scrubsanity.value,
            "shop_prices": self.prices,
            "cowsanity": self.options.cowsanity.value,
            "damage_multiplier": self.options.damage_multiplier.value,
            "death_behavior": self.options.death_behavior.value,
            "death_link": self.options.death_link.value,
            "camc": self.options.camc.value,
            "starting_heart_locations": 8 if self.options.starting_hearts_are_containers_or_pieces.value == 1 else starting_containers + starting_pieces + shuffled_containers + shuffled_pieces,
            "majora_remains_required": self.options.majora_remains_required.value,
            "moon_remains_required": self.options.moon_remains_required.value,
            "start_with_consumables": self.options.start_with_consumables.value,
            "permanent_chateau_romani": self.options.permanent_chateau_romani.value,
            "start_with_inverted_time": self.options.start_with_inverted_time.value,
            "receive_filled_wallets": self.options.receive_filled_wallets.value,
            "remains_allow_boss_warps": self.options.remains_allow_boss_warps.value,
            "magic_is_a_trap": self.options.magic_is_a_trap.value,
            "shuffle_regional_maps": self.options.shuffle_regional_maps.value,
            "shuffle_spiderhouse_reward": self.options.shuffle_spiderhouse_reward.value,
            "shuffle_great_fairy_rewards": self.options.shuffle_great_fairy_rewards.value,
            "link_tunic_color": ((self.options.link_tunic_color.value[0] & 0xFF) << 16) | ((self.options.link_tunic_color.value[1] & 0xFF) << 8) | (self.options.link_tunic_color.value[2] & 0xFF),
            "logic_difficulty": self.options.logic_difficulty.value
        }
