# world/age2DE/__init__.py

import sys

from . import ordered_set

sys.modules.setdefault("ordered_set", ordered_set)

import functools
import logging
from Options import OptionError
from rule_builder.cached_world import CachedRuleBuilderWorld
import settings
from typing import Any, ClassVar, Mapping
from BaseClasses import CollectionState, Entrance, Item, Location, MultiWorld, Region
from NetUtils import JSONMessagePart
from worlds.AutoWorld import World
from worlds.LauncherComponents import Component, Type, components, icon_paths, launch as launch_subprocess
from worlds.age2de.locations import Buildings
from worlds.age2de.locations.connections import LocationMapping
from worlds.age2de.locations.Buildings import Age2BuildingData
from worlds.age2de.locations.Scenarios import CAMPAIGN_TO_SCENARIOS
from .generation import Identity, LocalStart, SlotData, WorldVersion
from .generation.Age2Pool import Age2Pool
from .regions.UnitRegions import UnitRegions
from .Options import (
    Age2Options,
    Caveman,
    ExistingTechs,
    ScenarioBranching,
    ShuffleVillager,
    Techsanity,
    Unitsanity,
)
from .items import Items
from .locations import (
    Campaigns,
    Locations,
    Scenarios,
)
from .locations.Players import TRADE_BUILDINGS
from .locations.VillagerJobs import Age2VillagerJobData
from .locations.connections import (
    BuildingSeeds as BuildingSeeds,
    CivilizationBuildings as CivilizationBuildings,
    CivilizationTechs as CivilizationTechs,
    CivilizationUnits as CivilizationUnits,
    GameCosts as GameCosts,
    ScenarioCavemanExemptions as ScenarioCavemanExemptions,
    ScenarioExclusions as ScenarioExclusions,
    ScenarioPlayers as ScenarioPlayers,
    ScenarioResources as ScenarioResources,
    ScenarioStartupUnits as ScenarioStartupUnits,
    ScenarioTriggerUnits as ScenarioTriggerUnits,
    TechCounters as TechCounters,
    UnitBuildings as UnitBuildings,
    UnitCounters as UnitCounters,
    UnitLineUnits as UnitLineUnits,
    UnitRoles as UnitRoles,
    UnitTechs as UnitTechs,
    UnitUpgradeTokens as UnitUpgradeTokens,
    UnitVariants as UnitVariants,
    VillagerJobBuildings as VillagerJobBuildings,
)
from .explain import Explainer
from .rules.Rules import Rules

logger = logging.getLogger(__name__)

AGE2_DE = "Age Of Empires II: Definitive Edition"
class Age2Settings(settings.Group):
    class UserDirectory(settings.UserFolderPath):
        """The users local age2de user folder.
        Usually located at:
            "C:/Users/<USER>/Games/Age of Empires 2 DE/<STRING_OF_NUMBERS>/"
        Select the <STRING_OF_NUMBERS> folder as the user folder."""
        description = "Age of Empires II: Definitive Edition User Directory"
    
    user_folder: UserDirectory = UserDirectory(AGE2_DE)
        
UT_SEED = "ut_seed"
"""Slot data key: the world's own seed, for Universal Tracker to rebuild the same world."""


class Age2World(CachedRuleBuilderWorld):
    """
    Age of Empires II: Definitive Edition is a Real-Time Strategy game centered around the medieval
    ages and the various battles, conquests, and wars of history.
    """
    game = AGE2_DE  # name of the game/world
    settings: ClassVar[Age2Settings]
    options_dataclass = Age2Options  # options the player can set
    options: Age2Options  # typing hints for option results
    topology_present = True  # show path to required location checks in spoiler

    item_names = set(Items.item_name_to_id)
    location_names = set(LocationMapping.location_name_list)
    item_name_to_id = Items.item_name_to_id
    item_id_to_name = Items.item_id_to_name
    location_name_to_id = LocationMapping.location_name_to_id
    location_id_to_name = LocationMapping.location_id_to_name
    item_mapping = Items.item_mapping
    item_name_groups = {"Traps": set(Items.TRAP_NAMES)}
    
    pool: Age2Pool
    unit_regions: UnitRegions
    rules: Rules

    def __init__(self, multiworld: 'MultiWorld', player: int) -> None:
        super().__init__(multiworld, player)

    @classmethod
    def create_group(cls, multiworld: 'MultiWorld', new_player_id: int, players: set[int]) -> World:
        group = super().create_group(multiworld, new_player_id, players)
        group.pool = Age2Pool(group)
        return group

    def inspect_options(self, options: Age2Options, player_name: str) -> None:
        if not options.enabled_campaigns.value:
            raise OptionError(f"{player_name}: enabled_campaigns needs at least one campaign.")
        enabled = {campaign.campaign_name for campaign in Campaigns.Age2CampaignData
                   if campaign.campaign_name in options.enabled_campaigns}
        if not options.starting_campaigns.value:
            drawn = self.random.choice(sorted(enabled))
            options.starting_campaigns.value = {drawn}
            logger.info("%s left starting_campaigns blank; starting them in %s.",
                        player_name, drawn)
        elif not enabled & set(options.starting_campaigns.value):
            raise OptionError(f"{player_name}: starting_campaigns must include at least one "
                              f"enabled campaign. Enabled: {sorted(options.enabled_campaigns.value)}.")
        for campaign in Campaigns.Age2CampaignData:
            if campaign.campaign_name in enabled and not CAMPAIGN_TO_SCENARIOS[campaign]:
                raise OptionError(f"{player_name}: {campaign.campaign_name} has no scenarios.")
        techsanity = options.techsanity.value
        existing_techs = options.existing_techs
        if (
            techsanity == Techsanity.option_none
            and existing_techs.value != ExistingTechs.option_vanilla
        ):
            existing_techs.value = ExistingTechs.option_vanilla
            logger.warning(
                f"{player_name}'s Existing Techs needs Techsanity. With Techsanity off, "
                f"Existing Techs falls back to vanilla."
            )
        if (
            techsanity == Techsanity.option_generic
            and existing_techs.value == ExistingTechs.option_only_find_units
        ):
            existing_techs.value = ExistingTechs.option_vanilla
            logger.warning(
                f"{player_name}'s Existing Techs Only Find Units needs Techsanity units or all. "
                f"With Techsanity {options.techsanity.current_key}, no upgrade tech is a "
                f"location, so Existing Techs falls back to vanilla."
            )
        caveman = options.caveman
        if not caveman.value:
            return
        if options.unitsanity.value == Unitsanity.option_none:
            caveman.value = Caveman.option_false
            logger.warning(
                f"{player_name}'s Caveman needs Unitsanity. With Unitsanity off, "
                f"Caveman is turned off."
            )
        elif techsanity in (Techsanity.option_none, Techsanity.option_generic):
            caveman.value = Caveman.option_false
            logger.warning(
                f"{player_name}'s Caveman needs Techsanity units or all. With Techsanity "
                f"{options.techsanity.current_key}, Caveman is turned off."
            )

    def generate_early(self) -> None:
        self.seed_for_tracker()
        self.inspect_options(self.options, self.player_name)
        self.check_installable_name()
        self.pool = Age2Pool(self)

    def seed_for_tracker(self) -> None:
        regen = getattr(self.multiworld, "re_gen_passthrough", {}).get(self.game, {})
        self.ut_seed: int = regen.get(UT_SEED) if UT_SEED in regen else self.random.getrandbits(64)
        self.random.seed(self.ut_seed)

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        """Universal Tracker: rebuild with the server's slot data, so seed_for_tracker can match it."""
        return slot_data

    def check_installable_name(self) -> None:
        """/install names each campaign file after the slot, so the name has to survive a file
        name. Refuse a name that leaves nothing behind, and announce one that merely changes."""
        safe_name = Identity.sanitize_player(self.player_name)
        if not safe_name:
            raise OptionError(
                f"{self.player_name}: this name has no characters that can be used in a file name. "
                f"Age2 installs campaign files named after your slot, so pick a name that is not "
                r'made up entirely of <>:"/\|?* and dots.')
        if safe_name != self.player_name:
            logger.warning(
                "%s's name contains characters that cannot be used in a file name. Their campaigns "
                "will be installed as \"%s\".", self.player_name, safe_name)

    def create_regions(self) -> None:
        
        
        regions: list[Region] = [Region(self.origin_region_name, self.player, self.multiworld)]
        scenario_regions: dict[Scenarios.Age2ScenarioData, Region] = {}
        
        for campaign in self.pool.campaigns.enabled:
            scenarios = self.pool.scenarios.in_campaign(campaign)
            prev_region: Region = regions[0]
            for scenario in scenarios:
                region = self.add_scenario_region(scenario, prev_region)
                regions.append(region)
                scenario_regions[scenario] = region
                prev_region = region
                
        buildings = Region("Can Build", self.player, self.multiworld)
        source = regions[0]
        connection = Entrance(self.player, f"{buildings.name}", source)
        source.exits.append(connection)
        connection.connect(buildings)
        for building in self.pool.buildings.locations:
            buildings.locations.append(
                Location(self.player, building.location_name, building.id, buildings))
        for age in self.pool.ages.locations:
            buildings.locations.append(
                Location(self.player, age.location_name, age.id, buildings))
        regions.append(buildings)

        standing = Region("Starts With Building", self.player, self.multiworld)
        connection = Entrance(self.player, standing.name, source)
        source.exits.append(connection)
        connection.connect(standing)
        regions.append(standing)

        building_regions: dict[Buildings.Age2BuildingData, Region] = {}
        for building in Age2BuildingData:
            if not self.pool.buildings.hosts_locations(building):
                continue
            region = Region(building.item.item_name, self.player, self.multiworld)
            connection = Entrance(self.player, f"{region.name}", buildings)
            buildings.exits.append(connection)
            connection.connect(region)
            connection = Entrance(self.player, f"Standing {region.name}", standing)
            standing.exits.append(connection)
            connection.connect(region)
            regions.append(region)
            building_regions[building] = region
            linked_buildings: set[Region] = set()
            for tech in self.pool.techs.by_building(building):
                host = self.pool.techs.host_building(tech)
                if host is building:
                    region.locations.append(
                        Location(self.player, tech.location_name, tech.id, region))
                    continue

                # Its location is in the host's region already; reach it by a ruleless entrance.
                existing_building = building_regions[host]
                if existing_building in linked_buildings:
                    continue
                linked_buildings.add(existing_building)
                alternate = Entrance(
                    self.player,
                    f"{region.name} to {existing_building.name} Techs", region)
                region.exits.append(alternate)
                alternate.connect(existing_building)

        self.unit_regions = UnitRegions(self, building_regions, scenario_regions)
        regions += self.unit_regions.create()

        regions[0].add_event("Victory", Items.Age2ItemData.VICTORY.item_name)

        self.multiworld.regions += regions

    def add_scenario_region(self, scenario: Scenarios.Age2ScenarioData, source: Region) -> Region:
        new_region = Region(scenario.scenario_name, self.player, self.multiworld)
        connection = Entrance(self.player, f"{new_region.name}", source)
        source.exits.append(connection)
        connection.connect(new_region)
        for location in Locations.REGION_TO_LOCATIONS.get(scenario.scenario_name, ()):
            if not self.pool.scenarios.includes_location(location):
                continue
            new_location = Location(self.player, location.global_name(), location.id, new_region)
            new_region.locations.append(new_location)
        if scenario.scenario_name in Locations.VICTORY_SCENARIO_LOCATIONS:
            new_region.add_event("Complete " + scenario.scenario_name,
                                 scenario.scenario_name + ": Unlock Next Scenario",
                                 show_in_spoiler=False)
        for player in scenario.players:
            if self.options.partner_trade.needs_defeat_event(player):
                new_region.add_event(
                    player.defeat_event(scenario.scenario_name),
                    show_in_spoiler=False,
                )
            for building in TRADE_BUILDINGS:
                if self.options.partner_trade.needs_guard_event(player, building):
                    new_region.add_event(
                        player.guard_event(scenario.scenario_name, building),
                        show_in_spoiler=False,
                    )
        return new_region
        
    
    def create_items(self) -> None:
        items: list[Item] = []
        for item in Items.Age2ItemData:
            if isinstance(item.type, Items.Victory):
                continue
            elif isinstance(item.type, (Items.ScenarioItem, Items.Mercenary)):
                if item.type.vanilla_scenario in self.pool.scenarios.included:
                    items.append(self.create_item(item.item_name))
            elif isinstance(item.type, Items.Campaign):
                if item.type.vanilla_campaign in self.pool.campaigns.enabled:
                    ap_item = self.create_item(item.item_name)
                    if item.type.vanilla_campaign in self.pool.campaigns.starting:
                        self.multiworld.push_precollected(ap_item)
                    else:
                        items.append(ap_item)
            elif isinstance(item.type, Items.ProgressiveScenario):
                if item.type.vanilla_campaign in self.pool.campaigns.enabled:
                    for i in range(item.type.num_additional_scenarios):
                        items.append(self.create_item(item.item_name))
            elif isinstance(item.type, Items.Resources):
                continue
            elif isinstance(item.type, Items.StartingResources):
                continue
            elif isinstance(item.type, Items.SeedResources):
                if item in self.pool.resources.seeds:
                    items.append(self.create_item(item.item_name))
            elif isinstance(item.type, Items.Age2AgeData):
                age_item = self.create_item(item.item_name)
                if item.type in self.pool.ages.locations:
                    items.append(age_item)
                else:
                    self.multiworld.push_precollected(age_item)
            elif isinstance(item.type, Items.Building):
                continue
            elif isinstance(item.type, Items.Tech):
                continue
            elif isinstance(item.type, Items.UnitLine):
                continue
            elif isinstance(item.type, Items.UnitUpgrade):
                continue
            elif isinstance(item.type, Items.UnitBuilding):
                continue
            elif isinstance(item.type, Items.VillagerProfession):
                continue
            elif isinstance(item.type, Items.Trap):
                continue
            elif isinstance(item.type, Items.Skip):
                continue
            else:
                raise ValueError(f"Item {item} has unknown type {type(item.type)}")

        for building in Age2BuildingData:
            building_item: Item = self.create_item(building.item.item_name)
            if building in self.pool.buildings.locations:
                items.append(building_item)
            else:
                self.multiworld.push_precollected(building_item)

        if Age2BuildingData.HOUSE in self.pool.buildings.locations:
            # A civilisation that builds houses has no base without one, and no base means no easy
            # source of anything. A late House left Joan 3 starving for most of a seed.
            self.multiworld.early_items[self.player][Age2BuildingData.HOUSE.item.item_name] = 1

        builder = Age2VillagerJobData.BUILDER_MALE
        if (self.options.shuffle_villager == ShuffleVillager.option_include_professions
                and self.pool.units.job_possible(builder)):
            self.multiworld.early_items[self.player][builder.item.item_name] = 1

        for tech in self.pool.techs.shuffled:
            items.append(self.create_item(tech.item.item_name))

        for item in self.unit_regions.items():
            items.append(self.create_item(item.item_name))
                

        self.multiworld.itempool += items
        
        itempool = len(items)
        number_of_unfilled_locations = len(self.multiworld.get_unfilled_locations(self.player))
        
        needed_number_of_filler_items = number_of_unfilled_locations - itempool
        
        # Starting resources come first, up to half the open locations, and stop once every
        # target is met. Traps only roll over the locations left after that, so they never cost
        # the player economy.
        planned = self.pool.resources.plan(needed_number_of_filler_items)
        spare = needed_number_of_filler_items - len(planned)
        starting_items = [self.create_item(data.item_name) for data in planned]
        traps = [self.create_item(data.item_name) for data in self.pool.traps.roll(spare)]

        self.multiworld.itempool += starting_items
        self.multiworld.itempool += traps
        
        itempool = len(items + starting_items + traps)
        
        needed_number_of_filler_items = number_of_unfilled_locations - itempool
        
        self.multiworld.itempool += [self.create_filler() for _ in range(needed_number_of_filler_items)]

    def create_item(self, name: str) -> Item:
        item = Items.NAME_TO_ITEM[name]
        return Item(
            item.item_name,
            Items.classification_for(item),
            item.id,
            self.player
        )

    def get_filler_item_name(self) -> str:
        filler = []
        for item in Items.filler_items:
            filler.append(Items.item_id_to_name[item.id])
        filler_item_name = self.random.choice(filler)
        return filler_item_name
    
    def set_rules(self) -> None:
        self.rules = Rules(self)
        self.rules.set_rules()

    def pre_fill(self) -> None:
        LocalStart.apply(self)

    # -- Universal Tracker asks the world first, before its own /explain ---------------------

    def explain_rule(self, dest_name: str, state: CollectionState) -> list[JSONMessagePart] | None:
        return self.explainer.explain_rule(dest_name, state)

    def explain_more(self, argument: str, state: CollectionState) -> list[JSONMessagePart]:
        return self.explainer.explain_more(argument, state)

    @functools.cached_property
    def explainer(self) -> Explainer:
        return Explainer(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        mapping: Mapping[str, Any] = {
            WorldVersion.SLOT_DATA_KEY: self.world_version.as_simple_string(),
        }
        for campaign in self.pool.campaigns.enabled:
            mapping[campaign.campaign_name + "_unlocked"] = campaign in self.pool.campaigns.starting
        for option_name in SlotData.OPTIONS.values():
            mapping[option_name] = int(getattr(self.options, option_name).value)
        mapping[ScenarioBranching.internal_name] = int(self.options.scenario_branching.value)
        mapping[UT_SEED] = self.ut_seed
        return mapping


def run_client(*args: Any):
    print("Running Age of Empires II: Definitive Edition Client")
    from .client.ApClient import main  # lazy import

    launch_subprocess(main, name="Age2Client")

icon_paths["age2de_client"] = f"ap:{__name__}/icons/age2de_client.png"

components.append(
    Component(
        "Age of Empires II: DE Client",
        func=run_client,
        component_type=Type.CLIENT,
        icon="age2de_client",
    )
)