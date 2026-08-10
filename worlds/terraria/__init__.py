# Look at `Rules.dsv` first to get an idea for how this works
import dataclasses
import logging
from typing import Union, Tuple, List, Dict, Set, override

from Options import NumericOption
from rule_builder.cached_world import CachedRuleBuilderWorld
from rule_builder.field_resolvers import FromWorldAttr
from worlds.AutoWorld import WebWorld, World
from BaseClasses import Region, ItemClassification, Tutorial, CollectionState
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAny, HasAll, True_, False_, And, Or, Rule, TWorld, HasFromList, Filtered
from .Checks import (
    TerrariaItem,
    TerrariaLocation,
    Condition,
    goals,
    rules,
    rule_indices,
    labels,
    rewards,
    item_name_to_id,
    location_name_to_id,
    loc_to_item,
    COND_ITEM,
    COND_LOC,
    COND_FN,
    COND_GROUP,
    npcs,
    pickaxes,
    hammers,
    mech_bosses,
    armor_minions,
    accessory_minions,
    health_upgrades,
    quarter_fruits,
)
from .Options import TerrariaOptions, Goal, ter_option_groups, RandomizeNPCs, Calamity, RareAchievements, \
    TimeAchievements, HealthLogic, Getfixedboi, ShimmerSkips


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
    option_groups = ter_option_groups


class TerrariaWorld(CachedRuleBuilderWorld):
    """
    Terraria is a 2D multiplayer sandbox game featuring mining, building, exploration, and combat.
    Features 18 bosses and 4 classes.
    """
    game = "Terraria Beta"
    web = TerrariaWeb()
    options_dataclass = TerrariaOptions
    options: TerrariaOptions

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    calamity = False
    getfixedboi = False

    progression = set()
    npcs_to_randomize = set()

    ter_items: List[str]
    ter_locations: List[str]

    ter_goals: Dict[str, str]
    goal_items: Set[str]
    goal_locations: Set[str]

    required_client_version = (0, 6, 100)

    def generate_early(self) -> None:
        goal, goal_locations = goals[self.options.goal.value]
        slot_name = self.multiworld.player_name[self.player]
        match self.options.shuffle_to.value:
            case 0:
                pass
            case -1:
                goal = 0
            case _:
                if self.options.shuffle_to.value < self.options.goal.value:
                    logging.warning(f"SLOT {slot_name}: \"Shuffle To\" value ({Goal.name_lookup[self.options.shuffle_to.value]}) was set earlier than the goal ({Goal.name_lookup[self.options.goal.value]}); ignoring")
                else:
                    goal, _ = goals[self.options.shuffle_to.value]
        ter_goals = {}
        goal_items = set()

        if self.options.getfixedboi and self.options.randomize_npcs:
            logging.warning(f"SLOT {slot_name}: getfixedboi mode was selected with NPC rando enabled; disabling NPC rando")
            self.options.randomize_npcs.value = 0

        for location in goal_locations:
            if location == "Wall of Flesh" and not self.options.randomize_npcs.value:
                logging.warning(
                    f"SLOT {slot_name}: goal 'Wall of Flesh' was enabled was selected with NPC Randomization disabled. The resulting game will be goalable from Sphere 1."
                )
            flags = rules[rule_indices[location]].flags
            if not self.options.calamity.value and "Calamity" in flags:
                logging.warning(
                    f"SLOT {slot_name}: goal `{Goal.name_lookup[self.options.goal.value]}`, which requires Calamity, was selected with Calamity disabled; enabling Calamity"
                )
                self.options.calamity.value = 1

            if "Npc" in flags:
                event = location
            else:
                event = flags.get("Item") or f"Post-{location}"
            ter_goals[event] = location
            goal_items.add(event)

        location_count = 0
        locations = []
        item_count = 0
        items = []

        events = []

        def mark_progression(conditions):
            for condition in conditions:
                if condition.type == COND_ITEM:
                    prog = condition.condition in self.progression
                    self.progression.add(loc_to_item[condition.condition])
                    rule = rules[rule_indices[condition.condition]]
                    if (
                            not prog
                            and "Achievement" not in rule.flags
                            and "Location" not in rule.flags
                            and "Npc" not in rule.flags
                            and "Item" not in rule.flags
                    ):
                        mark_progression(rule.conditions)
                elif condition.type == COND_LOC:
                    mark_progression(rules[rule_indices[condition.condition]].conditions)
                elif condition.type == COND_GROUP:
                    _, conditions = condition.condition
                    mark_progression(conditions)
        valid_rules = rules[:goal] if goal != 0 else rules
        for rule in valid_rules:
            early = "Early" in rule.flags
            rare = "Rare" in rule.flags
            time = "Time" in rule.flags
            crafting = "Crafting" in rule.flags
            grindy = "Grindy" in rule.flags
            fishing = "Fishing" in rule.flags

            if (
                    (not self.options.getfixedboi.value and "Getfixedboi" in rule.flags)
                    or (self.options.getfixedboi.value and "Not Getfixedboi" in rule.flags)
                    or (not self.options.calamity.value and "Calamity" in rule.flags)
                    or (self.options.calamity.value and "Not Calamity" in rule.flags)
                    or (
                            self.options.getfixedboi.value
                            and self.options.calamity.value
                            and "Not Calamity Getfixedboi" in rule.flags
                    )
                    or (not self.options.shimmer_skips.value and "Shimmer" in rule.flags)
                    or (not self.options.early_achievements.value and early)
                    or (
                            not self.options.normal_achievements.value
                            and "Achievement" in rule.flags
                    )
                    or (not self.options.rare_achievements.value and rare)
                    or (not self.options.time_achievements.value and time)
                    or (not self.options.crafting_achievements.value and crafting)
                    or (not self.options.grindy_achievements.value and grindy)
                    or (not self.options.fishing_achievements.value and fishing)
            ) and rule.name not in goal_locations:
                continue

            # Special events
            if (
                    "Npc" in rule.flags
                    or "Pet" in rule.flags
                    or "Pickaxe" in rule.flags
                    or "Hammer" in rule.flags
                    or "Mech Boss" in rule.flags
                    or "Minions" in rule.flags
                    or "Armor Minions" in rule.flags
                    or "Health" in rule.flags
                    or "Quarter Fruit" in rule.flags
                    or rule.name in goal_locations
            ):
                self.progression.add(loc_to_item[rule.name])
                mark_progression(rule.conditions)

            if "Location" in rule.flags or "Achievement" in rule.flags or (
                    "Npc" in rule.flags and self.options.randomize_npcs.value):
                # Location
                location_count += 1
                locations.append(rule.name)
                if "Npc" in rule.flags:
                    self.npcs_to_randomize.add(rule.name)
                mark_progression(rule.conditions)
            elif (
                    "Achievement" not in rule.flags
                    and "Location" not in rule.flags
                    and "Item" not in rule.flags
                    and not ("Npc" in rule.flags and self.options.randomize_npcs.value)
            ):
                # Event
                locations.append(rule.name)
                events.append(rule.name)

            if ("Item" in rule.flags
                or ("Npc" in rule.flags and self.options.randomize_npcs.value)
            ) and not (
                    "Achievement" in rule.flags and rule.name not in goal_locations
            ):
                # Item
                item_count += 1
                if rule.name not in goal_locations:
                    items.append(rule.name)
            elif (
                    "Achievement" not in rule.flags
                    and "Location" not in rule.flags
                    and "Item" not in rule.flags
                    and not ("Npc" in rule.flags and self.options.randomize_npcs.value)
            ):
                # Event
                items.append(rule.name)

        pointless_events = [event for event in events if loc_to_item[event] not in self.progression]
        for event in pointless_events:
            locations.remove(event)
            items.remove(loc_to_item[event])
            location_count -= 1
            item_count -= 1

        ordered_rewards = [
            reward
            for reward in labels["ordered"]
            if self.options.calamity.value or "Calamity" not in rewards[reward]
        ]
        while (
                self.options.fill_extra_checks_with.value == 1
                and item_count < location_count
                and ordered_rewards
        ):
            items.append(ordered_rewards.pop(0))
            item_count += 1

        random_rewards = [
            reward
            for reward in labels["random"]
            if self.options.calamity.value or "Calamity" not in rewards[reward]
        ]
        self.multiworld.random.shuffle(random_rewards)
        while (
                self.options.fill_extra_checks_with.value == 1
                and item_count < location_count
                and random_rewards
        ):
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
            rule = rules[rule_indices[location]]
            if "Npc" in rule.flags and not self.options.randomize_npcs.value:
                location_id = None
            else:
                location_id = location_name_to_id.get(location)

            menu.locations.append(
                TerrariaLocation(
                    self.player, location, location_id, menu
                )
            )

        self.multiworld.regions.append(menu)

    def create_item(self, item: str) -> TerrariaItem:
        if item in self.progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        return TerrariaItem(item, classification, item_name_to_id[item], self.player)

    def create_items(self) -> None:
        for item in self.ter_items:
            if (rule_index := rule_indices.get(item)) is not None:
                rule = rules[rule_index]
                if "Item" in rule.flags:
                    name = rule.flags.get("Item") or f"Post-{item}"
                elif "Npc" in rule.flags and self.options.randomize_npcs.value == 1:
                    name = item
                else:
                    continue
            else:
                name = item

            self.multiworld.itempool.append(self.create_item(name))

        locked_items = {}

        for location in self.ter_locations:
            rule = rules[rule_indices[location]]
            if "Location" not in rule.flags and "Achievement" not in rule.flags \
                    and not ("Npc" in rule.flags and self.options.randomize_npcs.value):
                if location in self.progression:
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

    def create_rule_ini(
            self,
            operator: Union[bool, None],
            conditions: List[
                Tuple[
                    bool,
                    int,
                    Union[str, Tuple[Union[bool, None], list]],
                    Union[str, int, None],
                ]
            ]
    ) -> Rule:
        if operator is None:
            if len(conditions) == 0:
                return True_()
            if len(conditions) > 1:
                raise Exception("Found multiple conditions without an operator")
            cond = self.create_rule(conditions[0])
            return cond if isinstance(cond, Rule) else (True_() & cond)
        sub_rules = [self.create_rule(condition) for condition in conditions]
        return Or(*sub_rules) if operator else And(*sub_rules)

    def create_rule(self, condition: Condition) -> Rule:
        if condition.type == COND_ITEM:
            rule = rules[rule_indices[condition.condition]]
            if "Item" in rule.flags:
                name = rule.flags.get("Item") or f"Post-{condition.condition}"
            else:
                name = condition.condition

            assert(isinstance(name, str))
            return Has(name)
        elif condition.type == COND_LOC:
            rule = rules[rule_indices[condition.condition]]
            return self.create_rule_ini(rule.operator, rule.conditions)
        elif condition.type == COND_FN:
            if condition.condition == "npc":
                assert(isinstance(condition.argument, int))
                return HasFromList(*npcs, count=condition.argument)
            elif condition.condition == "npc_rando":
                return True_(options=[OptionFilter(RandomizeNPCs, condition.sign)])
            elif condition.condition == "calamity":
                return True_(options=[OptionFilter(Calamity, condition.sign)])
            elif condition.condition == "rare":
                return True_(options=[OptionFilter(RareAchievements, condition.sign)])
            elif condition.condition == "time":
                return True_(options=[OptionFilter(TimeAchievements, condition.sign)])
            elif condition.condition == "pickaxe":
                if type(condition.argument) is not int:
                    raise Exception("@pickaxe requires an integer argument")

                eligible_items = []
                for pickaxe, power in pickaxes.items():
                    if power >= condition.argument:
                        eligible_items.append(pickaxe)

                return HasAny(*eligible_items)
            elif condition.condition == "hammer":
                if type(condition.argument) is not int:
                    raise Exception("@hammer requires an integer argument")

                eligible_items = []
                for hammer, power in hammers.items():
                    if power >= condition.argument:
                        eligible_items.append(hammer)

                return HasAny(*eligible_items)
            elif condition.condition == "mech_boss":
                assert(isinstance(condition.argument, int))
                return HasFromList(*mech_bosses, count=condition.argument)
            elif condition.condition == "minions":
                assert (isinstance(condition.argument, int))
                return HasMinion(condition.argument)
            elif condition.condition == "health":
                if type(condition.argument) is not int:
                    raise Exception("@health requires an integer argument")

                health_option = OptionFilter(HealthLogic, 1)
                health_required = max(condition.argument + self.options.health_logic_handicap.value, 1)

                if health_required == 1:
                    return Has(health_upgrades[0], options=[health_option], filtered_resolution=True)
                elif health_required == 2:
                    return HasAll(*health_upgrades[:2], options=[health_option], filtered_resolution=True)

                highest_base = HasAll(*health_upgrades[:2])
                quarter_fruits_required = health_required - 2
                quarter_fruits_rule = HasFromList(
                    *quarter_fruits,
                    count=quarter_fruits_required,
                    options=[OptionFilter(Calamity, Calamity.option_true)],
                    filtered_resolution=True
                )
                return Filtered((highest_base & quarter_fruits_rule), options=[health_option], filtered_resolution=True)
            elif condition.condition == "getfixedboi":
                return True_(options=[OptionFilter(Getfixedboi, condition.sign)])
            elif condition.condition == "shimmer_skips":
                return True_(options=[OptionFilter(ShimmerSkips, condition.sign)])
            else:
                raise Exception(f"Unknown function {condition.condition}")
        elif condition.type == COND_GROUP:
            operator, conditions = condition.condition

            return self.create_rule_ini(operator, conditions)

    def set_rules(self) -> None:
        for location_name in self.ter_locations:
            if location_name == "Cryonic Ore":
                pass
            location = self.multiworld.get_location(location_name, self.player)
            rule = rules[rule_indices[location_name]]
            created_rule = self.create_rule_ini(rule.operator, rule.conditions)
            self.set_rule(location, created_rule)

        self.set_completion_rule(HasAll(*self.goal_items))

    def fill_slot_data(self) -> Dict[str, object]:
        return {
            "goal": list(self.goal_locations),
            "deathlink": bool(self.options.death_link),
            "version": list(self.required_client_version),
            # The rest of these are included for trackers
            "calamity": self.options.calamity.value,
            "getfixedboi": self.options.getfixedboi.value,
            "early_achievements": self.options.early_achievements.value,
            "normal_achievements": self.options.normal_achievements.value,
            "grindy_achievements": self.options.grindy_achievements.value,
            "fishing_achievements": self.options.fishing_achievements.value,
            "npc_rando": self.options.randomize_npcs.value,
            "randomize_npcs": list(self.npcs_to_randomize),
        }

@dataclasses.dataclass()
class HasMinion(Rule["TerrariaWorld"], game=TerrariaWorld.game):

    target: int

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        return self.Resolved(self.target, player=world.player, caching_enabled=True)

    class Resolved(Rule.Resolved):
        target: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            count = 1
            for armor, minion in armor_minions:
                if state.has(armor, self.player):
                    count += minion
                    break
            if count >= self.target:
                return True
            for accessory, minion in accessory_minions:
                if state.has(accessory, self.player):
                    count += minion
                    if count >= self.target:
                        return True
            return False

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            item_dict = {}
            for item in armor_minions + accessory_minions:
                item_dict[item[0]] = {id(self)}
            return item_dict
