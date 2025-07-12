# Imports of base Archipelago modules must be absolute.
from collections.abc import Mapping
from typing import Any

from BaseClasses import CollectionState, Entrance, Item, ItemClassification, Location, Region

from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule, set_rule

# Imports of your world's files must be relative.
from .options import APQuestOptions, option_groups, option_presets


# It is common practice to override the base Location class to override the "game" field.
class APQuestLocation(Location):
    game = "APQuest"

# It is common practice to override the base Item class to override the "game" field.
class APQuestItem(Item):
    game = "APQuest"

class APQuestWebWorld(WebWorld):
    game = "APQuest"

    option_groups = option_groups
    options_presets = option_presets

# The world class is the heart and soul of an apworld implementation.
# It holds all the data and functions required to build the world and submit it to the multiworld generator.
class APQuestWorld(World):
    game = "APQuest"

    # This is how we associate the options defined in our options.py with our world.
    options: APQuestOptions
    options_dataclass = APQuestOptions

    # Every location must have a unique integer ID associated with it.
    # Even if a location doesn't exist on specific options, it must be present in location_name_to_id.
    location_name_to_id = {
        "Top Left Room Chest": 1,
        "Top Middle Chest": 2,
        "Bottom Left Chest": 3,
        "Bottom Right Room Left Chest": 4,
        "Bottom Right Room Right Chest": 5,
        "Right Room Enemy Drop": 10,  # Location IDs don't need to be sequential, as long as they're unique
    }

    # Every item must have a unique integer ID associated with it.
    # Even if an item doesn't exist on specific options, it must be present in item_name_to_id.
    item_name_to_id = {
        "Key": 1,
        "Sword": 2,
        "Shield": 3,
        "Health Upgrade": 4,
        "Confetti Cannon": 5,
    }

    # There is always one region that the generator starts from & assumes you can always go back to.
    # This defaults to "Menu", but you can change it by overriding origin_region_name.
    origin_region_name = "Overworld"

    def create_regions(self) -> None:
        ###########
        # REGIONS #
        ###########

        # Creating a region is as simple as calling its constructor.
        overworld = Region("Overworld", self.player, self.multiworld)
        top_left_room = Region("Top Left Room", self.player, self.multiworld)
        bottom_right_room = Region("Bottom Right Room", self.player, self.multiworld)
        right_room = Region("Right Room", self.player, self.multiworld)
        final_boss_room = Region("Top Right Room", self.player, self.multiworld)

        # We now need to add these regions to multiworld.regions so that AP knows about their existence.
        self.multiworld.regions += [overworld, top_left_room, bottom_right_room, right_room, final_boss_room]

        ######################
        # REGION CONNECTIONS #
        ######################

        # Next, we connect the regions to each other. For this, we need to create Entrances.
        # Entrances are inherently one-way, but crucially, AP assumes you can always return to the origin region.
        # One way to create an Entrance is by calling the Entrance constructor.
        overworld_to_bottom_right_room = Entrance(
            self.player, "Overworld to Bottom Right Room", parent=overworld
        )
        overworld.exits.append(overworld_to_bottom_right_room)

        # You can then connect the Entrance to the target region.
        overworld_to_bottom_right_room.connect(bottom_right_room)

        # An even easier way is to use the region.connect helper.
        overworld.connect(right_room, "Overworld to Right Room")
        right_room.connect(final_boss_room, "Right Room to Final Boss Room")

        # The region.connect helper even allows adding a rule immediately.
        # We'll talk more about rule creation in set_rules().
        overworld.connect(top_left_room, "Overworld to Top Left Room", lambda state: state.has("Key", self.player))

        #############
        # LOCATIONS #
        #############

        # Finally, we need to put the Locations ("checks") into their regions.
        # One way to create locations is by just creating them directly via their constructor.
        bottom_left_chest = APQuestLocation(
            self.player, "Bottom Left Chest", self.location_name_to_id["Bottom Left Chest"], overworld
        )
        top_middle_chest = APQuestLocation(
            self.player, "Top Middle Chest", self.location_name_to_id["Top Middle Chest"], overworld
        )

        # You can then add them to the region.
        overworld.locations += [bottom_left_chest, top_middle_chest]

        # A simpler way to do this is by using the region.add_locations helper.
        # For this, you need to have a dict of location names to their IDs (i.e. a subset of location_name_to_id)
        # You also need to pass your overridden Location class.
        bottom_right_room_locations = {
            "Bottom Right Room Left Chest": self.location_name_to_id["Bottom Right Room Left Chest"],
            "Bottom Right Room Right Chest": self.location_name_to_id["Bottom Right Room Right Chest"],
        }
        bottom_right_room.add_locations(bottom_right_room_locations, APQuestLocation)

        top_left_room_locations = {
            "Top Left Room Chest": self.location_name_to_id["Top Left Room Chest"],
        }
        top_left_room.add_locations(top_left_room_locations, APQuestLocation)

        right_room_locations = {
            "Right Room Enemy Drop": self.location_name_to_id["Right Room Enemy Drop"],
        }
        right_room.add_locations(right_room_locations, APQuestLocation)

        ##########
        # EVENTS #
        ##########

        # Sometimes, the player may perform in-game actions that allow them to progress which are not related to Items.
        # In our case, the player must press a button in the top left room to open the final boss door.
        # AP has something for this purpose: "Event locations" and "Event items".
        # An event location is no different than a regular location, except it has the address "None".
        # It is treated during generation like any other location, but then it is discarded.
        # This location cannot be "sent" and its item cannot be "received", but the item can be used in logic rules.
        # One way to create an event is simply to use one of the normal methods of creating a location.
        button_in_top_left_room = Location(self.player, "Top Left Room Button", None, top_left_room)
        top_left_room.locations += [button_in_top_left_room]

        # We then need to put an event item onto the location. Item creation is discussed more in create_items().
        button_item = APQuestItem("Top Left Room Button Pressed", ItemClassification.progression, None, self.player)
        button_in_top_left_room.place_locked_item(button_item)

        # A way simpler way to do this is by using the region.create_event helper.
        # Luckily, we have another event we want to create: The Victory event.
        # We will use this event to track whether the player can win the game.
        # The Victory event is a completely optional abstraction - This will be discussed more in set_rules().
        final_boss_room.add_event(
            "Final Boss Defeated", "Victory", location_type=APQuestLocation, item_type=APQuestItem
        )

        # If you create all your regions and locations line-by-line like this,
        # the length of your create_regions might get out of hand.
        # Many worlds use more data-driven approaches using dataclasses or NamedTuples.
        # However, it is worth understanding how the actual creation of regions and locations works,
        # That way, we're not just mindlessly copy-pasting! :)

    def set_rules(self) -> None:
        # In order for AP to be able to randomize into an item layout that is actually possible to complete,
        # We need to define rules for our Entrances and Locations.
        # Note: Regions do not have rules, the Entrances connecting them do!
        # First, we need to actually grab our locations and entrances. Luckily, there are helper methods for this.
        overworld_to_bottom_right_room = self.get_entrance("Overworld to Bottom Right Room")

        # One way to set rules is via the set_rule() function, which works on both Entrances and Locations.
        # A rule is a function. We can define this function like any other function.
        # However, the function needs to have the player number baked into it, so it must be locally defined.
        def can_destroy_bush(state: CollectionState) -> bool:
            return state.has("Sword", self.player)

        set_rule(overworld_to_bottom_right_room, can_destroy_bush)

        # Because the function has to be defined locally, most worlds prefer the lambda syntax.
        overworld_to_top_left_room = self.get_entrance("Overworld to Top Left Room")
        set_rule(overworld_to_top_left_room, lambda state: state.has("Key", self.player))

        # Conditions can depend on events.
        right_room_to_final_boss_room = self.get_entrance("Right Room to Final Boss Room")
        set_rule(right_room_to_final_boss_room, lambda state: state.has("Top Left Room Button Pressed", self.player))

        # Sometimes, you may want to have different rules depending on the player's chosen options.
        right_room_enemy = self.get_location("Right Room Enemy Drop")

        if self.options.hard_mode:
            # If you have multiple conditions, you can obviously chain them via "or" or "and".
            # However, there are also the nice helper functions "state.has_any" and "state.has_all".
            set_rule(right_room_enemy, lambda state: (
                 state.has("Sword", self.player) and state.has_any(("Shield", "Health Upgrade"), self.player)
            ))
        else:
            set_rule(right_room_enemy, lambda state: state.has("Sword", self.player))

        # Another way to chain multiple conditions is via the add_rule function.
        # This is generally somewhat slow though, so it should only be used if your structure justifies it.
        # In our case, it's pretty useful because hard mode and easy mode have different requirements.
        final_boss = self.get_location("Final Boss Defeated")
        add_rule(final_boss, lambda state: state.has("Sword", self.player))
        add_rule(final_boss, lambda state: state.has("Shield", self.player))

        if self.options.hard_mode:
            # You can check for multiple copies of an item by using the optional count parameter of state.has().
            add_rule(final_boss, lambda state: state.has("Health Upgrade", self.player, 2))

        # Finally, we need to set a victory condition.
        # You can just set a victory condition directly like any other condition, referencing items the player receives:
        self.multiworld.completion_condition[self.player] = (
            lambda state: state.has_all(("Sword", "Shield"), self.player)
        )

        # In our case, we went for the Victory event design pattern, so our victory condition will be:
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def create_items(self) -> None:
        # Creating items should generally be done via your create_item() function.

        self.multiworld.itempool += [
            self.create_item("Key"),
            self.create_item("Sword"),
            self.create_item("Shield"),
            self.create_item("Health Upgrade"),
            self.create_item("Health Upgrade"),
            self.create_item("Confetti Cannon"),
        ]

    # Items should have a defined default classification.
    # In our case, we will make a dictionary from item name to classification.
    ITEM_CLASSIFICATIONS = {
        "Key": ItemClassification.progression,
        "Sword": ItemClassification.progression | ItemClassification.useful,  # Items can have multiple classifications.
        "Shield": ItemClassification.progression,
        "Health Upgrade": ItemClassification.useful,
        "Confetti Cannon": ItemClassification.filler,  # Your game should have at least one repeatable filler item.
    }

    def create_item(self, name: str) -> APQuestItem:
        classification = self.ITEM_CLASSIFICATIONS[name]

        # It is perfectly normal and valid for an item's classification to differ based on the player's options.
        # In our case, Health Upgrades are only logically considered in hard mode.
        if name == "Health Upgrade" and self.options.hard_mode:
            classification = ItemClassification.progression

        return APQuestItem(name, classification, self.item_name_to_id[name], self.player)

    # For features such as item links and panic-method start inventory, AP may ask your world to create extra filler.
    # The way it does this is by calling get_filler_item_name.
    # You must override this function and have it return the name of an infinitely repeatable filler item.
    # If you have multiple repeatable filler items, you can randomly choose one using e.g. self.random.choice(...).
    def get_filler_item_name(self) -> str:
        return "Confetti Canon"

    # There may be data that the game client will need to modify the behavior of the game.
    # This is what slot_data exists for. Upon every client connection, the slot's slot_data is sent to the client.
    def fill_slot_data(self) -> Mapping[str, Any]:
        # If you need access to the chosen options on the client side, there is a helper for that.
        return self.options.as_dict("hard_mode", "confetti_explosiveness", "player_sprite")
