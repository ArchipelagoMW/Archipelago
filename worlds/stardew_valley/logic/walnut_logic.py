from functools import cached_property

from .base_logic import BaseLogic, BaseLogicMixin
from ..content.vanilla.ginger_island import ginger_island_content_pack
from ..options import Walnutsanity
from ..stardew_rule import StardewRule
from ..strings.ap_names.ap_option_names import WalnutsanityOptionName
from ..strings.ap_names.event_names import Event
from ..strings.craftable_names import Furniture
from ..strings.crop_names import Fruit
from ..strings.metal_names import Fossil
from ..strings.region_names import Region
from ..strings.seed_names import Seed


class WalnutLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.walnut = WalnutLogic(*args, **kwargs)


class WalnutLogic(BaseLogic):

    def has_walnut(self, number: int) -> StardewRule:
        if not self.content.is_enabled(ginger_island_content_pack):
            return self.logic.false_
        if number <= 0:
            return self.logic.true_

        if self.options.walnutsanity == Walnutsanity.preset_none:
            return self.can_get_walnuts(number)
        if self.options.walnutsanity == Walnutsanity.preset_all:
            return self.has_received_walnuts(number)
        puzzle_walnuts = 61
        bush_walnuts = 25
        dig_walnuts = 18
        repeatable_walnuts = 33
        total_walnuts = puzzle_walnuts + bush_walnuts + dig_walnuts + repeatable_walnuts
        walnuts_to_receive = 0
        walnuts_to_collect = number
        if WalnutsanityOptionName.puzzles in self.options.walnutsanity:
            puzzle_walnut_rate = puzzle_walnuts / total_walnuts
            puzzle_walnuts_required = round(puzzle_walnut_rate * number)
            walnuts_to_receive += puzzle_walnuts_required
            walnuts_to_collect -= puzzle_walnuts_required
        if WalnutsanityOptionName.bushes in self.options.walnutsanity:
            bush_walnuts_rate = bush_walnuts / total_walnuts
            bush_walnuts_required = round(bush_walnuts_rate * number)
            walnuts_to_receive += bush_walnuts_required
            walnuts_to_collect -= bush_walnuts_required
        if WalnutsanityOptionName.dig_spots in self.options.walnutsanity:
            dig_walnuts_rate = dig_walnuts / total_walnuts
            dig_walnuts_required = round(dig_walnuts_rate * number)
            walnuts_to_receive += dig_walnuts_required
            walnuts_to_collect -= dig_walnuts_required
        if WalnutsanityOptionName.repeatables in self.options.walnutsanity:
            repeatable_walnuts_rate = repeatable_walnuts / total_walnuts
            repeatable_walnuts_required = round(repeatable_walnuts_rate * number)
            walnuts_to_receive += repeatable_walnuts_required
            walnuts_to_collect -= repeatable_walnuts_required
        return self.has_received_walnuts(walnuts_to_receive) & self.can_get_walnuts(walnuts_to_collect)

    def has_received_walnuts(self, number: int) -> StardewRule:
        return self.logic.received(Event.received_walnuts, number)

    def can_get_walnuts(self, number: int) -> StardewRule:
        # https://stardewcommunitywiki.com/Golden_Walnut#Walnut_Locations
        reach_south = self.logic.region.can_reach(Region.island_south)
        reach_north = self.logic.region.can_reach(Region.island_north)
        reach_west = self.logic.region.can_reach(Region.island_west)
        reach_hut = self.logic.region.can_reach(Region.leo_hut)
        reach_southeast = self.logic.region.can_reach(Region.island_south_east)
        reach_field_office = self.logic.region.can_reach(Region.field_office)
        reach_pirate_cove = self.logic.region.can_reach(Region.pirate_cove)
        reach_outside_areas = self.logic.and_(reach_south, reach_north, reach_west, reach_hut)
        reach_volcano_regions = [self.logic.region.can_reach(Region.volcano),
                                 self.logic.region.can_reach(Region.volcano_secret_beach),
                                 self.logic.region.can_reach(Region.volcano_floor_5),
                                 self.logic.region.can_reach(Region.volcano_floor_10)]
        reach_volcano = self.logic.or_(*reach_volcano_regions)
        reach_all_volcano = self.logic.and_(*reach_volcano_regions)
        reach_walnut_regions = [reach_south, reach_north, reach_west, reach_volcano, reach_field_office]
        reach_caves = self.logic.and_(self.logic.region.can_reach(Region.qi_walnut_room), self.logic.region.can_reach(Region.dig_site),
                                      self.logic.region.can_reach(Region.gourmand_frog_cave),
                                      self.logic.region.can_reach(Region.colored_crystals_cave),
                                      self.logic.region.can_reach(Region.shipwreck), self.logic.combat.has_slingshot)
        reach_entire_island = self.logic.and_(reach_outside_areas, reach_all_volcano,
                                              reach_caves, reach_southeast, reach_field_office, reach_pirate_cove)
        if number <= 5:
            return self.logic.or_(reach_south, reach_north, reach_west, reach_volcano)
        if number <= 10:
            return self.logic.count(2, *reach_walnut_regions)
        if number <= 15:
            return self.logic.count(3, *reach_walnut_regions)
        if number <= 20:
            return self.logic.and_(*reach_walnut_regions)
        if number <= 50:
            return reach_entire_island

        return reach_entire_island & self.logic.has(Fruit.banana) & self.logic.museum.has_all_gems() & \
            self.logic.ability.can_mine_perfectly() & self.logic.ability.can_fish_perfectly() & \
            self.logic.has(Furniture.flute_block) & self.logic.has(Seed.melon) & self.logic.has(Seed.wheat) & \
            self.logic.has(Seed.garlic) & self.can_complete_field_office()

    @cached_property
    def can_start_field_office(self) -> StardewRule:
        field_office = self.logic.region.can_reach(Region.field_office)
        professor_snail = self.logic.received("Open Professor Snail Cave")
        return field_office & professor_snail

    def can_complete_large_animal_collection(self) -> StardewRule:
        fossils = self.logic.has_all(Fossil.fossilized_leg, Fossil.fossilized_ribs, Fossil.fossilized_skull, Fossil.fossilized_spine, Fossil.fossilized_tail)
        return self.can_start_field_office & fossils

    def can_complete_snake_collection(self) -> StardewRule:
        fossils = self.logic.has_all(Fossil.snake_skull, Fossil.snake_vertebrae)
        return self.can_start_field_office & fossils

    def can_complete_frog_collection(self) -> StardewRule:
        fossils = self.logic.has_all(Fossil.mummified_frog)
        return self.can_start_field_office & fossils

    def can_complete_bat_collection(self) -> StardewRule:
        fossils = self.logic.has_all(Fossil.mummified_bat)
        return self.can_start_field_office & fossils

    def can_complete_field_office(self) -> StardewRule:
        return self.can_complete_large_animal_collection() & self.can_complete_snake_collection() & \
            self.can_complete_frog_collection() & self.can_complete_bat_collection()
