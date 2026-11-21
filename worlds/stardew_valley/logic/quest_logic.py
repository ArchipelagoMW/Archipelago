from typing import Dict

from .base_logic import BaseLogicMixin, BaseLogic
from ..stardew_rule import StardewRule, Has, True_
from ..strings.ap_names.ap_option_names import SecretsanityOptionName
from ..strings.ap_names.community_upgrade_names import CommunityUpgrade
from ..strings.artisan_good_names import ArtisanGood
from ..strings.building_names import Building
from ..strings.craftable_names import Craftable
from ..strings.crop_names import Fruit, Vegetable
from ..strings.fish_names import Fish
from ..strings.food_names import Meal
from ..strings.forageable_names import Forageable
from ..strings.machine_names import Machine
from ..strings.material_names import Material
from ..strings.metal_names import MetalBar, Ore, Mineral
from ..strings.monster_drop_names import Loot
from ..strings.quest_names import Quest
from ..strings.region_names import Region
from ..strings.season_names import Season
from ..strings.special_item_names import SpecialItem
from ..strings.tool_names import Tool, FishingRod
from ..strings.villager_names import NPC
from ..strings.wallet_item_names import Wallet


class QuestLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quest = QuestLogic(*args, **kwargs)


class QuestLogic(BaseLogic):

    def initialize_rules(self):
        self.update_rules({
            Quest.introductions: True_(),
            Quest.how_to_win_friends: self.logic.quest.can_complete_quest(Quest.introductions),
            Quest.getting_started: self.logic.has(Vegetable.parsnip),
            Quest.to_the_beach: self.logic.region.can_reach(Region.beach),
            Quest.raising_animals: self.logic.quest.can_complete_quest(Quest.getting_started) & self.logic.building.has_building(Building.coop),
            Quest.feeding_animals: self.logic.quest.can_complete_quest(Quest.getting_started) & self.logic.building.has_building(Building.silo),
            Quest.advancement: self.logic.quest.can_complete_quest(Quest.getting_started) & self.logic.has(Craftable.scarecrow),
            Quest.archaeology: self.logic.tool.has_tool(Tool.hoe) | self.logic.mine.can_mine_in_the_mines_floor_1_40() | self.logic.fishing.can_fish_chests,
            Quest.rat_problem: self.logic.region.can_reach_all(Region.town, Region.community_center),
            Quest.meet_the_wizard: self.logic.region.can_reach_all(Region.community_center, Region.wizard_tower) & self.logic.received("Wizard Invitation"),
            Quest.forging_ahead: self.logic.has(Ore.copper) & self.logic.has(Machine.furnace),
            Quest.smelting: self.logic.has(MetalBar.copper),
            Quest.initiation: self.logic.mine.can_mine_in_the_mines_floor_1_40(),
            Quest.robins_lost_axe: self.logic.season.has(Season.spring) & self.logic.relationship.can_meet(NPC.robin),
            Quest.jodis_request: self.logic.season.has(Season.spring) & self.logic.has(Vegetable.cauliflower) & self.logic.relationship.can_meet(NPC.jodi),
            Quest.mayors_shorts: self.logic.has(SpecialItem.lucky_purple_shorts) &
                                 self.logic.relationship.can_meet(NPC.lewis),
            Quest.blackberry_basket: self.logic.season.has(Season.fall) & self.logic.relationship.can_meet(NPC.linus) & self.logic.region.can_reach(
                Region.tunnel_entrance),
            Quest.marnies_request: self.logic.relationship.has_hearts(NPC.marnie, 3) & self.logic.has(Forageable.cave_carrot),
            Quest.pam_is_thirsty: self.logic.season.has(Season.summer) & self.logic.has(ArtisanGood.pale_ale) & self.logic.relationship.can_meet(NPC.pam),
            Quest.a_dark_reagent: self.logic.season.has(Season.winter) & self.logic.has(Loot.void_essence) & self.logic.relationship.can_meet(NPC.wizard),
            Quest.cows_delight: self.logic.season.has(Season.fall) & self.logic.has(Vegetable.amaranth) & self.logic.relationship.can_meet(NPC.marnie),
            Quest.the_skull_key: self.logic.received(Wallet.skull_key),
            Quest.crop_research: self.logic.season.has(Season.summer) & self.logic.has(Fruit.melon) & self.logic.relationship.can_meet(NPC.demetrius),
            Quest.knee_therapy: self.logic.season.has(Season.summer) & self.logic.has(Fruit.hot_pepper) & self.logic.relationship.can_meet(NPC.george),
            Quest.robins_request: self.logic.season.has(Season.winter) & self.logic.has(Material.hardwood) & self.logic.relationship.can_meet(NPC.robin),
            Quest.qis_challenge: True_(),  # The skull cavern floor 25 already has rules
            Quest.the_mysterious_qi: (self.logic.region.can_reach_all(Region.bus_tunnel, Region.railroad, Region.mayor_house) &
                                      self.logic.has_all(ArtisanGood.battery_pack, Forageable.rainbow_shell, Vegetable.beet, Loot.solar_essence)),
            Quest.carving_pumpkins: self.logic.season.has(Season.fall) & self.logic.has(Vegetable.pumpkin) & self.logic.relationship.can_meet(NPC.caroline),
            Quest.a_winter_mystery: self.logic.season.has(Season.winter),
            Quest.strange_note: self.logic.has(Forageable.secret_note) & self.logic.has(ArtisanGood.maple_syrup),
            Quest.cryptic_note: self.logic.has(Forageable.secret_note) & self.logic.region.can_reach(Region.skull_cavern_100),
            Quest.fresh_fruit: self.logic.season.has(Season.spring) & self.logic.has(Fruit.apricot) & self.logic.relationship.can_meet(NPC.emily),
            Quest.aquatic_research: self.logic.season.has(Season.summer) & self.logic.has(Fish.pufferfish) & self.logic.relationship.can_meet(NPC.demetrius),
            Quest.a_soldiers_star: (self.logic.season.has(Season.summer) & self.logic.time.has_year_two & self.logic.has(Fruit.starfruit) &
                                    self.logic.relationship.can_meet(NPC.kent)),
            Quest.mayors_need: self.logic.season.has(Season.summer) & self.logic.has(ArtisanGood.truffle_oil) & self.logic.relationship.can_meet(NPC.lewis),
            Quest.wanted_lobster: (self.logic.season.has(Season.fall) & self.logic.season.has(Season.fall) & self.logic.has(Fish.lobster) &
                                   self.logic.relationship.can_meet(NPC.gus)),
            Quest.pam_needs_juice: self.logic.season.has(Season.fall) & self.logic.has(ArtisanGood.battery_pack) & self.logic.relationship.can_meet(NPC.pam),
            Quest.fish_casserole: self.logic.relationship.has_hearts(NPC.jodi, 4) & self.logic.has(Fish.largemouth_bass),
            Quest.catch_a_squid: self.logic.season.has(Season.winter) & self.logic.has(Fish.squid) & self.logic.relationship.can_meet(NPC.willy),
            Quest.fish_stew: self.logic.season.has(Season.winter) & self.logic.has(Fish.albacore) & self.logic.relationship.can_meet(NPC.gus),
            Quest.pierres_notice: self.logic.season.has(Season.spring) & self.logic.has(Meal.sashimi) & self.logic.relationship.can_meet(NPC.pierre),
            Quest.clints_attempt: self.logic.season.has(Season.winter) & self.logic.has(Mineral.amethyst) & self.logic.relationship.can_meet(NPC.emily),
            Quest.a_favor_for_clint: self.logic.season.has(Season.winter) & self.logic.has(MetalBar.iron) & self.logic.relationship.can_meet(NPC.clint),
            Quest.staff_of_power: self.logic.season.has(Season.winter) & self.logic.has(MetalBar.iridium) & self.logic.relationship.can_meet(NPC.wizard),
            Quest.grannys_gift: self.logic.season.has(Season.spring) & self.logic.has(Forageable.leek) & self.logic.relationship.can_meet(NPC.evelyn),
            Quest.exotic_spirits: self.logic.season.has(Season.winter) & self.logic.has(Forageable.coconut) & self.logic.relationship.can_meet(NPC.gus),
            Quest.catch_a_lingcod: self.logic.season.has(Season.winter) & self.logic.has(Fish.lingcod) & self.logic.relationship.can_meet(NPC.willy),
            Quest.dark_talisman: self.logic.region.can_reach(Region.railroad) & self.logic.wallet.has_rusty_key() & self.logic.relationship.can_meet(
                NPC.krobus),
            Quest.goblin_problem: self.logic.region.can_reach(Region.witch_swamp)
                                  # Void mayo can be fished at 5% chance in the witch swamp while the quest is active. It drops a lot after the quest.
                                  & (self.logic.has(ArtisanGood.void_mayonnaise) | self.logic.fishing.can_fish()),
            Quest.magic_ink: self.logic.region.can_reach(Region.witch_hut) & self.logic.relationship.can_meet(NPC.wizard),
            Quest.the_pirates_wife: self.logic.relationship.can_meet(NPC.kent) & self.logic.relationship.can_meet(NPC.gus) &
                                    self.logic.relationship.can_meet(NPC.sandy) & self.logic.relationship.can_meet(NPC.george) &
                                    self.logic.relationship.can_meet(NPC.wizard) & self.logic.relationship.can_meet(NPC.willy),
            Quest.giant_stump: self.logic.received(CommunityUpgrade.raccoon) & self.logic.has(Material.hardwood)
        })

    def update_rules(self, new_rules: Dict[str, StardewRule]):
        self.registry.quest_rules.update(new_rules)

    def can_complete_quest(self, quest: str) -> StardewRule:
        return Has(quest, self.registry.quest_rules, "quest")

    def has_club_card(self) -> StardewRule:
        if self.options.quest_locations.has_story_quests() or SecretsanityOptionName.secret_notes in self.options.secretsanity:
            return self.logic.received(Wallet.club_card)
        return self.logic.quest.can_complete_quest(Quest.the_mysterious_qi)

    def has_magnifying_glass(self) -> StardewRule:
        if self.options.quest_locations.has_story_quests():
            return self.logic.received(Wallet.magnifying_glass)
        return self.logic.quest.can_complete_quest(Quest.a_winter_mystery)

    def has_dark_talisman(self) -> StardewRule:
        if self.options.quest_locations.has_story_quests():
            return self.logic.received(Wallet.dark_talisman)
        return self.logic.quest.can_complete_quest(Quest.dark_talisman)

    def has_magic_ink(self) -> StardewRule:
        if self.options.quest_locations.has_story_quests():
            return self.logic.received(Wallet.magic_ink)
        return self.logic.quest.can_complete_quest(Quest.magic_ink)

    def has_raccoon_shop(self, tier: int = 1) -> StardewRule:
        number_raccoons_required = 1 + tier  # 1 for Mr Raccoon, plus 1 for each shop tier at Mrs Raccoon
        if self.options.quest_locations.has_story_quests():
            # Add one for repairing the tree. This one is done manually if quests are turned off
            return self.logic.received(CommunityUpgrade.raccoon, 1 + number_raccoons_required)
        return self.logic.received(CommunityUpgrade.raccoon, number_raccoons_required) & self.logic.quest.can_complete_quest(Quest.giant_stump)

    def can_complete_help_wanteds(self, number: int) -> StardewRule:
        number_per_month = 7
        number_months = number // number_per_month
        if number <= 7:
            return self.logic.time.has_lived_months(number_months)
        return self.logic.time.has_lived_months(number_months) &\
               self.can_do_item_delivery_quest() & self.can_do_gathering_quest() &\
               self.can_do_fishing_quest() & self.can_do_slaying_quest()

    def can_do_item_delivery_quest(self) -> StardewRule:
        return self.logic.region.can_reach(Region.town)

    def can_do_gathering_quest(self) -> StardewRule:
        return self.logic.region.can_reach_all(*(Region.town, Region.forest)) & \
               self.logic.region.can_reach_any(*(Region.mines, Region.quarry, Region.skull_cavern_25)) & \
               self.logic.tool.has_tool(Tool.axe) & \
               self.logic.tool.has_tool(Tool.pickaxe)

    def can_do_fishing_quest(self) -> StardewRule:
        return self.logic.region.can_reach_all(*(Region.town, Region.beach)) & \
               self.logic.tool.has_fishing_rod(FishingRod.bamboo)

    def can_do_slaying_quest(self) -> StardewRule:
        return self.logic.region.can_reach_all(*(Region.town, Region.mines_floor_10))

    def can_drink_snake_milk(self) -> StardewRule:
        if self.options.quest_locations.has_story_quests() or SecretsanityOptionName.secret_notes in self.options.secretsanity:
            return self.logic.received(Wallet.iridium_snake_milk)
        return self.logic.quest.can_complete_quest(Quest.cryptic_note) & self.logic.region.can_reach(Region.skull_cavern_100)
