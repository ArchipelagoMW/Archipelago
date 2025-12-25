import functools
import math
from typing import Iterable

from .base_logic import BaseLogicMixin, BaseLogic
from ..data.game_item import Requirement, ItemTag
from ..data.requirement import ToolRequirement, BookRequirement, SkillRequirement, SeasonRequirement, YearRequirement, \
    CombatRequirement, QuestRequirement, \
    SpecificFriendRequirement, FishingRequirement, WalnutRequirement, RegionRequirement, TotalEarningsRequirement, \
    GrangeDisplayRequirement, \
    ForgeInfinityWeaponRequirement, EggHuntRequirement, CaughtFishRequirement, MuseumCompletionRequirement, \
    BuildingRequirement, FullShipmentRequirement, NumberOfFriendsRequirement, FishingCompetitionRequirement, \
    LuauDelightRequirementRequirement, MovieRequirement, CookedRecipesRequirement, CraftedItemsRequirement, \
    HelpWantedRequirement, ShipOneCropRequirement, ReceivedRaccoonsRequirement, PrizeMachineRequirement, \
    AllAchievementsRequirement, PerfectionPercentRequirement, ReadAllBooksRequirement, MinesRequirement, \
    DangerousMinesRequirement, HasItemRequirement, MeetRequirement, MonsterKillRequirement, CatalogueRequirement
from ..options import IncludeEndgameLocations
from ..strings.ap_names.community_upgrade_names import CommunityUpgrade
from ..strings.region_names import Region, LogicRegion


class RequirementLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requirement = RequirementLogic(*args, **kwargs)


class RequirementLogic(BaseLogic):

    def meet_all_requirements(self, requirements: Iterable[Requirement]):
        if not requirements:
            return self.logic.true_
        return self.logic.and_(*(self.logic.requirement.meet_requirement(requirement) for requirement in requirements))

    @functools.singledispatchmethod
    def meet_requirement(self, requirement: Requirement):
        raise ValueError(f"Requirements of type{type(requirement)} have no rule registered.")

    @meet_requirement.register
    def _(self, requirement: HasItemRequirement):
        return self.logic.has(requirement.item)

    @meet_requirement.register
    def _(self, requirement: ToolRequirement):
        return self.logic.tool.has_tool_generic(requirement.tool, requirement.tier)

    @meet_requirement.register
    def _(self, requirement: SkillRequirement):
        return self.logic.skill.has_level(requirement.skill, requirement.level)

    @meet_requirement.register
    def _(self, requirement: RegionRequirement):
        return self.logic.region.can_reach(requirement.region)

    @meet_requirement.register
    def _(self, requirement: BookRequirement):
        return self.logic.book.has_book_power(requirement.book)

    @meet_requirement.register
    def _(self, requirement: SeasonRequirement):
        return self.logic.season.has(requirement.season)

    @meet_requirement.register
    def _(self, requirement: YearRequirement):
        return self.logic.time.has_year(requirement.year)

    @meet_requirement.register
    def _(self, requirement: WalnutRequirement):
        return self.logic.walnut.has_walnut(requirement.amount)

    @meet_requirement.register
    def _(self, requirement: CombatRequirement):
        return self.logic.combat.can_fight_at_level(requirement.level)

    @meet_requirement.register
    def _(self, requirement: QuestRequirement):
        return self.logic.quest.can_complete_quest(requirement.quest)

    @meet_requirement.register
    def _(self, requirement: MeetRequirement):
        return self.logic.relationship.can_meet(requirement.npc)

    @meet_requirement.register
    def _(self, requirement: SpecificFriendRequirement):
        return self.logic.relationship.has_hearts(requirement.npc, requirement.hearts)

    @meet_requirement.register
    def _(self, requirement: NumberOfFriendsRequirement):
        return self.logic.relationship.has_hearts_with_n(requirement.friends, requirement.hearts)

    @meet_requirement.register
    def _(self, requirement: FishingRequirement):
        return self.logic.fishing.can_fish_at(requirement.region)

    @meet_requirement.register
    def _(self, requirement: TotalEarningsRequirement):
        return self.logic.money.can_have_earned_total(requirement.amount)

    @meet_requirement.register
    def _(self, requirement: GrangeDisplayRequirement):
        return self.logic.region.can_reach(LogicRegion.fair) & self.logic.festival.can_get_grange_display_max_score()

    @meet_requirement.register
    def _(self, requirement: EggHuntRequirement):
        return self.logic.region.can_reach(LogicRegion.egg_festival) & self.logic.festival.can_win_egg_hunt()

    @meet_requirement.register
    def _(self, requirement: FishingCompetitionRequirement):
        return self.logic.region.can_reach(LogicRegion.festival_of_ice) & self.logic.festival.can_win_fishing_competition()

    @meet_requirement.register
    def _(self, requirement: LuauDelightRequirementRequirement):
        return self.logic.region.can_reach(LogicRegion.luau) & self.logic.festival.can_get_luau_soup_delight()

    @meet_requirement.register
    def _(self, requirement: ForgeInfinityWeaponRequirement):
        return self.logic.combat.has_galaxy_weapon & self.logic.region.can_reach(Region.volcano_floor_10) & self.logic.has("Galaxy Soul")

    @meet_requirement.register
    def _(self, requirement: CaughtFishRequirement):
        if requirement.unique:
            return self.logic.fishing.can_catch_many_fish(requirement.number_fish)
        return self.logic.fishing.can_catch_many_fish(math.ceil(requirement.number_fish / 10)) & self.logic.time.has_lived_months(requirement.number_fish // 20)

    @meet_requirement.register
    def _(self, requirement: MuseumCompletionRequirement):
        return self.logic.museum.can_donate_museum_items(requirement.number_donated)

    @meet_requirement.register
    def _(self, requirement: FullShipmentRequirement):
        return self.logic.shipping.can_ship_everything()

    @meet_requirement.register
    def _(self, requirement: BuildingRequirement):
        return self.logic.building.has_building(requirement.building)

    @meet_requirement.register
    def _(self, requirement: MovieRequirement):
        return self.logic.region.can_reach(Region.movie_theater)

    @meet_requirement.register
    def _(self, requirement: CookedRecipesRequirement):
        return self.logic.cooking.can_have_cooked_recipes(requirement.number_of_recipes)

    @meet_requirement.register
    def _(self, requirement: CraftedItemsRequirement):
        return self.logic.crafting.can_have_crafted_recipes(requirement.number_of_recipes)

    @meet_requirement.register
    def _(self, requirement: HelpWantedRequirement):
        return self.logic.quest.can_complete_help_wanteds(requirement.number_of_quests)

    @meet_requirement.register
    def _(self, requirement: ShipOneCropRequirement):
        crops = self.content.find_tagged_items(ItemTag.CROPSANITY)
        crop_rules = [self.logic.shipping.can_ship(crop.name) for crop in crops]
        return self.logic.and_(*crop_rules)

    @meet_requirement.register
    def _(self, requirement: ReceivedRaccoonsRequirement):
        amount = min(requirement.number_of_raccoons, 8, 8 + self.options.bundle_per_room)
        if self.options.quest_locations.has_story_quests():
            amount += 1
        return self.logic.received(CommunityUpgrade.raccoon, amount)

    @meet_requirement.register
    def _(self, requirement: PrizeMachineRequirement):
        return self.logic.grind.can_grind_prize_tickets(requirement.number_of_tickets)

    @meet_requirement.register
    def _(self, requirement: AllAchievementsRequirement):
        return self.logic.goal.can_complete_perfection() & self.logic.has_progress_percent(100)

    @meet_requirement.register
    def _(self, requirement: PerfectionPercentRequirement):
        return self.logic.goal.can_complete_perfection()

    @meet_requirement.register
    def _(self, requirement: ReadAllBooksRequirement):
        books = self.content.find_tagged_items(ItemTag.BOOK_POWER)
        book_rules = [self.logic.book.has_book_power(book.name) for book in books]
        return self.logic.and_(*book_rules)

    @meet_requirement.register
    def _(self, requirement: MinesRequirement):
        return self.logic.mine.can_progress_in_the_mines_from_floor(requirement.floor)

    @meet_requirement.register
    def _(self, requirement: DangerousMinesRequirement):
        return self.logic.region.can_reach(Region.dangerous_mines_100) & self.logic.mine.has_mine_elevator_to_floor(requirement.floor)

    @meet_requirement.register
    def _(self, requirement: MonsterKillRequirement):
        return self.logic.monster.can_kill_any(requirement.monsters, math.log10(requirement.amount) // 1)

    @meet_requirement.register
    def _(self, requirement: CatalogueRequirement):
        if self.options.include_endgame_locations == IncludeEndgameLocations.option_true:
            return self.logic.received(requirement.catalogue)
        return self.logic.true_
