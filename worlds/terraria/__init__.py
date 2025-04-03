# Look at `Rules.dsv` first to get an idea for how this works

from typing import Union, Tuple, List, Dict, Set
from worlds.AutoWorld import WebWorld, World
from BaseClasses import Region, ItemClassification, Tutorial, CollectionState
from .Checks import (
    TerrariaItem,
    TerrariaLocation,
    goals,
    rules,
    rule_indices,
    labels,
    rewards,
    item_name_to_id,
    location_name_to_id,
    COND_ITEM,
    COND_LOC,
    COND_FN,
    COND_GROUP,
    npcs,
    pickaxes,
    hammers,
    mech_bosses,
    progression,
    armor_minions,
    accessory_minions,
)
from .Options import TerrariaOptions


class TerrariaWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Terraria randomizer connected to an Archipelago Multiworld.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Seldom"],
        )
    ]


class TerrariaWorld(World):
    """
    Terraria is a 2D multiplayer sandbox game featuring mining, building, exploration, and combat.
    Features 18 bosses and 4 classes.
    """

    game = "Terraria"
    web = TerrariaWeb()
    options_dataclass = TerrariaOptions
    options: TerrariaOptions

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    # Turn into an option when calamity is supported in the mod
    calamity = False

    ter_items: List[str]
    ter_locations: List[str]

    ter_goals: Dict[str, str]
    goal_items: Set[str]
    goal_locations: Set[str]

    def generate_early(self) -> None:
        goal, goal_locations = goals[self.options.goal.value]
        ter_goals = {}
        goal_items = set()
        for location in goal_locations:
            _, flags, _, _ = rules[rule_indices[location]]
            item = flags.get("Item") or f"Post-{location}"
            ter_goals[item] = location
            goal_items.add(item)

        achievements = self.options.achievements.value
        location_count = 0
        locations = []
        for rule, flags, _, _ in rules[:goal]:
            if (
                (not self.calamity and "Calamity" in flags)
                or (achievements < 1 and "Achievement" in flags)
                or (achievements < 2 and "Grindy" in flags)
                or (achievements < 3 and "Fishing" in flags)
                or (
                    rule == "Zenith" and self.options.goal.value != 11
                )  # Bad hardcoding
            ):
                continue
            if "Location" in flags or ("Achievement" in flags and achievements >= 1):
                # Location
                location_count += 1
                locations.append(rule)
            elif (
                "Achievement" not in flags
                and "Location" not in flags
                and "Item" not in flags
            ):
                # Event
                locations.append(rule)

        item_count = 0
        items = []
        for rule, flags, _, _ in rules[:goal]:
            if not self.calamity and "Calamity" in flags:
                continue
            if "Item" in flags:
                # Item
                item_count += 1
                if rule not in goal_locations:
                    items.append(rule)
            elif (
                "Achievement" not in flags
                and "Location" not in flags
                and "Item" not in flags
            ):
                # Event
                items.append(rule)

        extra_checks = self.options.fill_extra_checks_with.value
        ordered_rewards = [
            reward
            for reward in labels["ordered"]
            if self.calamity or "Calamity" not in rewards[reward]
        ]
        while extra_checks == 1 and item_count < location_count and ordered_rewards:
            items.append(ordered_rewards.pop(0))
            item_count += 1

        random_rewards = [
            reward
            for reward in labels["random"]
            if self.calamity or "Calamity" not in rewards[reward]
        ]
        self.multiworld.random.shuffle(random_rewards)
        while extra_checks == 1 and item_count < location_count and random_rewards:
            items.append(random_rewards.pop(0))
            item_count += 1

        while item_count < location_count:
            items.append("Reward: Coins")
            item_count += 1

        self.ter_items = items
        self.ter_locations = locations

        self.ter_goals = ter_goals
        self.goal_items = goal_items
        self.goal_locations = goal_locations

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)

        for location in self.ter_locations:
            menu.locations.append(
                TerrariaLocation(
                    self.player, location, location_name_to_id.get(location), menu
                )
            )

        self.multiworld.regions.append(menu)

    def create_item(self, item: str) -> TerrariaItem:
        if item in progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        return TerrariaItem(item, classification, item_name_to_id[item], self.player)

    def create_items(self) -> None:
        for item in self.ter_items:
            if (rule_index := rule_indices.get(item)) is not None:
                _, flags, _, _ = rules[rule_index]
                if "Item" in flags:
                    name = flags.get("Item") or f"Post-{item}"
                else:
                    continue
            else:
                name = item

            self.multiworld.itempool.append(self.create_item(name))

        locked_items = {}

        for location in self.ter_locations:
            _, flags, _, _ = rules[rule_indices[location]]
            if "Location" not in flags and "Achievement" not in flags:
                if location in progression:
                    classification = ItemClassification.progression
                else:
                    classification = ItemClassification.useful

                locked_items[location] = TerrariaItem(
                    location, classification, None, self.player
                )

        for item, location in self.ter_goals.items():
            locked_items[location] = self.create_item(item)
        for location, item in locked_items.items():
            self.multiworld.get_location(location, self.player).place_locked_item(item)

    def check_condition(
        self,
        state,
        sign: bool,
        ty: int,
        condition: Union[str, Tuple[Union[bool, None], list]],
        arg: Union[str, int, None],
    ) -> bool:
        if ty == COND_ITEM:
            _, flags, _, _ = rules[rule_indices[condition]]
            if "Item" in flags:
                name = flags.get("Item") or f"Post-{condition}"
            else:
                name = condition

            return sign == state.has(name, self.player)
        elif ty == COND_LOC:
            _, _, operator, conditions = rules[rule_indices[condition]]
            return sign == self.check_conditions(state, operator, conditions)
        elif ty == COND_FN:
            if condition == "npc":
                if type(arg) is not int:
                    raise Exception("@npc requires an integer argument")

                npc_count = 0
                for npc in npcs:
                    if state.has(npc, self.player):
                        npc_count += 1
                        if npc_count >= arg:
                            return sign

                return not sign
            elif condition == "calamity":
                return sign == self.calamity
            elif condition == "grindy":
                return sign == (self.options.achievements.value >= 2)
            elif condition == "pickaxe":
                if type(arg) is not int:
                    raise Exception("@pickaxe requires an integer argument")

                for pickaxe, power in pickaxes.items():
                    if power >= arg and state.has(pickaxe, self.player):
                        return sign

                return not sign
            elif condition == "hammer":
                if type(arg) is not int:
                    raise Exception("@hammer requires an integer argument")

                for hammer, power in hammers.items():
                    if power >= arg and state.has(hammer, self.player):
                        return sign

                return not sign
            elif condition == "mech_boss":
                if type(arg) is not int:
                    raise Exception("@mech_boss requires an integer argument")

                boss_count = 0
                for boss in mech_bosses:
                    if state.has(boss, self.player):
                        boss_count += 1
                        if boss_count >= arg:
                            return sign

                return not sign
            elif condition == "minions":
                if type(arg) is not int:
                    raise Exception("@minions requires an integer argument")

                minion_count = 1
                for armor, minions in armor_minions.items():
                    if state.has(armor, self.player) and minions + 1 > minion_count:
                        minion_count = minions + 1
                        if minion_count >= arg:
                            return sign

                for accessory, minions in accessory_minions.items():
                    if state.has(accessory, self.player):
                        minion_count += minions
                        if minion_count >= arg:
                            return sign

                return not sign
            else:
                raise Exception(f"Unknown function {condition}")
        elif ty == COND_GROUP:
            operator, conditions = condition
            return sign == self.check_conditions(state, operator, conditions)

    def check_conditions(
        self,
        state,
        operator: Union[bool, None],
        conditions: List[
            Tuple[
                bool,
                int,
                Union[str, Tuple[Union[bool, None], list]],
                Union[str, int, None],
            ]
        ],
    ) -> bool:
        if operator is None:
            if len(conditions) == 0:
                return True
            if len(conditions) > 1:
                raise Exception("Found multiple conditions without an operator")
            return self.check_condition(state, *conditions[0])
        elif operator:
            return any(
                self.check_condition(state, *condition) for condition in conditions
            )
        else:
            return all(
                self.check_condition(state, *condition) for condition in conditions
            )

    def set_rules(self) -> None:
        for location in self.ter_locations:

            def check(state: CollectionState, location=location):
                _, _, operator, conditions = rules[rule_indices[location]]
                return self.check_conditions(state, operator, conditions)

            self.multiworld.get_location(location, self.player).access_rule = check

        self.multiworld.completion_condition[self.player] = lambda state: state.has_all(
            self.goal_items, self.player
        )

    def fill_slot_data(self) -> Dict[str, object]:
        return {
            "goal": list(self.goal_locations),
            "achievements": self.options.achievements.value,
            "deathlink": bool(self.options.death_link),
        }
