from typing import Dict, TYPE_CHECKING, Set

from BaseClasses import CollectionState, Item
from worlds.generic.Rules import add_item_rule, add_rule, CollectionRule
from .Items import BRAIN_JARS, LOCAL_SET
from .Locations import DEEP_ARROWHEAD_LOCATIONS, MENTAL_COBWEB_LOCATIONS
from .Names import LocationName, ItemName, RegionName
from .Options import Goal

if TYPE_CHECKING:
    from . import PSYWorld


class PsyRules:
    player: int
    world: "PSYWorld"

    region_rules: Dict[str, CollectionRule]

    def __init__(self, world: "PSYWorld") -> None:
        self.player = world.player
        self.world = world
        self.multiworld = world.multiworld

        self.region_rules = {
            RegionName.CAGP: self.has_button,

            # The true logic for ranks would be exceedingly complicated if not impossible due to the many different ways
            # to gain Ranks:
            # 1) +1 for purchasing a PSI Challenge Core from the Main Lodge Store with Arrowheads (farmable)
            # 2) +1 for collecting a PSI Challenge Marker
            # 3) +1 for combining 9 PSI Cards into a PSI Challenge Marker at Ford's Sanctuary
            # 4) +1 for reuniting Emotional Baggage with its Tag
            # 5) +5 for each half of the Scavenger Hunt Completed
            # 6) +1 for every 100 Figment Points collected
            # 7) +? for each Memory Vault collected (the rewards from Memory Vaults are typically randomized)
            # Technically, all that is required to reach Rank 101 is Sasha's Button because Arrowheads can be farmed and
            # then Ranks can be purchased at the Main Lodge Store. However, this would be incredibly slow in practice.

            # Meeting four of these conditions adds ranks 5-20 to logic
            RegionName.RANK5to20: lambda state: sum([
                self.has_button(state),
                self.has_coach_mind(state),
                self.has_most_sasha_mind_access(state),
                self.has_most_milla_mind_access(state),
                self.has_linda_mind(state),
                self.has_most_boyd_mind_access(state),
                self.has_half_gloria_mind_access(state),
                self.has_fred_mind(state),
                self.has_edgar_mind(state),
            ]) >= 4,

            # Meeting five of these conditions adds ranks 25-40 to logic
            RegionName.RANK25to40: lambda state: sum([
                self.has_button(state) and (
                            self.has_oarsmans_badge(state)
                            or self.has_squirrel_dinner(state)
                            or self.has_lili_bracelet(state)),
                self.has_coach_mind(state),
                self.has_most_sasha_mind_access(state),
                self.has_most_milla_mind_access(state),
                self.has_most_linda_mind_access(state),
                self.has_most_boyd_mind_access(state),
                self.has_half_gloria_mind_access(state),
                self.has_most_fred_mind_access(state),
                self.has_edgar_mind(state),
                self.has_half_oly_mind_access(state),
            ]) >= 5,

            # Having Sasha's Button AND Meeting six of these conditions adds ranks 45-60 to logic
            RegionName.RANK45to60: lambda state: self.has_button(state) and sum([
                self.has_all_extra_campground_access(state),
                self.has_coach_mind(state),
                self.has_most_sasha_mind_access(state),
                self.has_most_milla_mind_access(state),
                self.has_most_linda_mind_access(state),
                self.has_most_boyd_mind_access(state),
                self.has_most_gloria_mind_access(state),
                self.has_most_fred_mind_access(state),
                self.has_edgar_mind(state),
                self.has_most_asylum_access(state),
                self.has_most_oly_mind_access(state),

            ]) >= 6,

            # Rank Regions form a dependent sequence, so ranks 45 and higher all require Sasha's Button.
            # Meeting seven of these conditions adds ranks 65-80 to logic
            RegionName.RANK65to80: lambda state: sum([
                self.has_all_extra_campground_access(state),
                self.has_coach_mind(state),
                self.has_most_sasha_mind_access(state),
                self.has_most_milla_mind_access(state),
                self.has_most_linda_mind_access(state),
                self.has_most_boyd_mind_access(state),
                self.has_most_gloria_mind_access(state),
                self.has_most_fred_mind_access(state),
                self.has_most_edgar_mind_access(state),
                self.has_most_asylum_access(state),
                self.has_most_oly_mind_access(state),
            ]) >= 7,

            # Meeting eight of these conditions adds ranks 85-101 to logic
            RegionName.RANK85to101: lambda state: sum([
                self.has_all_extra_campground_access(state),
                self.has_coach_mind(state),
                self.has_most_sasha_mind_access(state),
                self.has_most_milla_mind_access(state),
                self.has_most_linda_mind_access(state),
                self.has_most_boyd_mind_access(state),
                self.has_most_gloria_mind_access(state),
                self.has_most_fred_mind_access(state),
                self.has_most_edgar_mind_access(state),
                self.has_most_asylum_access(state),
                self.has_most_oly_mind_access(state),
            ]) >= 8,

            RegionName.CAGPSquirrel: self.has_invisibility,

            RegionName.CAGPGeyser: self.has_shield,

            RegionName.CAMALev: self.has_levitation,

            RegionName.CAKC: self.has_lili_bracelet,

            RegionName.CAKCLev: self.has_levitation,

            RegionName.CAKCPyro: self.has_pyrokinesis,

            RegionName.CARE: self.has_squirrel_dinner,

            RegionName.CARELev: self.has_levitation,

            RegionName.CAREMark: self.has_marksmanship,

            RegionName.CABH: self.has_oarsmans_badge,

            RegionName.CABHLev: self.has_levitation,

            RegionName.ASGR: self.has_lungfish_call,

            RegionName.ASGRLev: self.has_levitation,

            RegionName.ASCOLev: self.has_levitation,

            RegionName.ASCOInvis: self.has_invisibility,

            RegionName.ASUP: lambda state: self.has_upper_asylum_access(state),

            RegionName.ASUPLev: self.has_levitation,

            RegionName.ASUPTele: self.has_telekinesis,

            RegionName.BBA1: self.has_coach_mind,

            RegionName.BBA2Duster: self.has_cobweb_duster,

            RegionName.SACU: lambda state: self.has_marksmanship(state) and self.has_sasha_mind(state),

            RegionName.SACULev: self.has_levitation,

            RegionName.MIFL: lambda state: self.has_levitation(state) and self.has_milla_mind(state),

            RegionName.NIMPMark: self.has_marksmanship,

            RegionName.NIBA: self.has_levitation,

            RegionName.LOMA: self.has_linda_mind,

            RegionName.LOMAShield: self.has_shield,

            RegionName.MMI1Fridge: self.has_boyd_mind,

            RegionName.MMI1BeforeSign: self.has_clairvoyance,

            RegionName.MMI1AfterSign: self.has_stop_sign,

            RegionName.MMI1Hedgetrimmers: self.has_hedge_trimmers,

            RegionName.MMI1RollingPin: self.has_rolling_pin,

            RegionName.MMI1Duster: self.has_cobweb_duster,

            RegionName.MMI2: lambda state: (self.has_flowers(state)
                                            and self.has_plunger(state)
                                            and self.has_pyrokinesis(state)
                                            and self.has_shield(state)),

            RegionName.MMI1Powerlines: self.has_cobweb_duster,

            RegionName.MMDM: lambda state: self.has_invisibility(state) and self.has_telekinesis(state),

            RegionName.THMS: self.has_gloria_mind,

            RegionName.THMSLev: self.has_levitation,

            RegionName.THMSDuster: self.has_cobweb_duster,

            RegionName.THMSStorage: self.has_invisibility,

            RegionName.THCW: lambda state: (self.has_pyrokinesis(state)
                                            and self.has_candle(state)
                                            and self.has_levitation(state)
                                            and self.has_megaphone(state)),

            RegionName.THFB: lambda state: self.has_both_candles(state),

            RegionName.WWMA: self.has_fred_mind,

            RegionName.WWMALev: self.has_levitation,

            RegionName.WWMACarpRoof: lambda state: self.has_levitation(state) and self.has_invisibility(state),

            RegionName.WWMADuster: self.has_cobweb_duster,

            RegionName.WWMADusterLev: self.has_levitation,

            RegionName.WWMADusterLevPyro: self.has_pyrokinesis,

            RegionName.WWMAV1: self.has_freds_letter,

            RegionName.WWMAKnight: self.has_telekinesis,

            RegionName.WWMAV2: lambda state: self.has_priceless_coin(state) and self.has_telekinesis(state),

            RegionName.WWMAV3: self.has_musket,

            RegionName.WWMADone: self.has_levitation,

            RegionName.BVRB: self.has_edgar_mind,

            RegionName.BVRBLev: self.has_levitation,

            RegionName.BVRBTele: self.has_telekinesis,

            RegionName.BVRBDuster: self.has_cobweb_duster,

            RegionName.BVRBLogs: self.has_pyrokinesis,

            RegionName.BVESLev: self.has_levitation,

            RegionName.BVESCobra: self.has_confusion,

            RegionName.BVESBoss: self.has_telekinesis,

            RegionName.MCTC: lambda state: self.has_cobweb_duster(state) and self.has_oly_mind(state),

            RegionName.MCTCLev: self.has_levitation,

            RegionName.MCTCEscort: self.has_telekinesis,

        }

    def has_button(self, state: CollectionState) -> bool:
        return state.has(ItemName.SashaButton, self.player)

    def has_lili_bracelet(self, state: CollectionState) -> bool:
        return state.has(ItemName.LilisBracelet, self.player)

    def has_squirrel_dinner(self, state: CollectionState) -> bool:
        return state.has(ItemName.SquirrelDinner, self.player)

    def has_oarsmans_badge(self, state: CollectionState) -> bool:
        return state.has(ItemName.OarsmansBadge, self.player)

    def has_lungfish_call(self, state: CollectionState) -> bool:
        return state.has(ItemName.LungfishCall, self.player)

    def has_cake(self, state: CollectionState) -> bool:
        return state.has(ItemName.Cake, self.player)

    def has_coach_mind(self, state: CollectionState) -> bool:
        return state.has(ItemName.CoachMind, self.player)

    def has_sasha_mind(self, state: CollectionState) -> bool:
        return state.has(ItemName.SashaMind, self.player)

    def has_milla_mind(self, state: CollectionState) -> bool:
        return state.has(ItemName.MillaMind, self.player)

    def has_linda_mind(self, state: CollectionState) -> bool:
        return state.has(ItemName.LindaMind, self.player)

    def has_boyd_mind(self, state: CollectionState) -> bool:
        return state.has(ItemName.BoydMind, self.player)

    def has_gloria_mind(self, state: CollectionState) -> bool:
        return state.has(ItemName.GloriaMind, self.player)

    def has_fred_mind(self, state: CollectionState) -> bool:
        return state.has(ItemName.FredMind, self.player)

    def has_edgar_mind(self, state: CollectionState) -> bool:
        return state.has(ItemName.EdgarMind, self.player)

    def has_oly_mind(self, state: CollectionState) -> bool:
        return state.has(ItemName.OlyMind, self.player)

    def has_most_sasha_mind_access(self, state: CollectionState) -> bool:
        return state.has_all([ItemName.SashaMind, ItemName.Marksmanship], self.player)

    def has_most_milla_mind_access(self, state: CollectionState) -> bool:
        return state.has_all([ItemName.MillaMind, ItemName.Levitation], self.player)

    def has_most_linda_mind_access(self, state: CollectionState) -> bool:
        return state.has_all([ItemName.LindaMind, ItemName.Shield], self.player)

    def has_most_boyd_mind_access(self, state: CollectionState) -> bool:
        return state.has_all([ItemName.BoydMind, ItemName.Clairvoyance, ItemName.StopSign], self.player)

    def has_half_gloria_mind_access(self, state: CollectionState) -> bool:
        return state.has_all([ItemName.CobwebDuster, ItemName.GloriaMind, ItemName.Invisibility], self.player)

    def has_most_gloria_mind_access(self, state: CollectionState) -> bool:
        items = [
            ItemName.CobwebDuster,
            ItemName.GloriaMind,
            ItemName.Candle,
            ItemName.Pyrokinesis,
            ItemName.Levitation,
            ItemName.Invisibility,
            ItemName.Megaphone
        ]
        return state.has_all(items, self.player)

    def has_most_fred_mind_access(self, state: CollectionState) -> bool:
        return state.has_all([ItemName.CobwebDuster, ItemName.FredMind], self.player)

    def has_most_edgar_mind_access(self, state: CollectionState) -> bool:
        return state.has_all([ItemName.EdgarMind, ItemName.CobwebDuster], self.player)

    def has_half_oly_mind_access(self, state: CollectionState) -> bool:
        return state.has_all([ItemName.OlyMind, ItemName.CobwebDuster], self.player)

    def has_most_oly_mind_access(self, state: CollectionState) -> bool:
        items = [ItemName.OlyMind, ItemName.CobwebDuster, ItemName.Levitation, ItemName.Telekinesis]
        return state.has_all(items, self.player)

    def has_all_extra_campground_access(self, state: CollectionState) -> bool:
        return state.has_all([ItemName.OarsmansBadge, ItemName.SquirrelDinner, ItemName.LilisBracelet], self.player)

    def has_most_asylum_access(self, state: CollectionState) -> bool:
        items = [ItemName.Telekinesis, ItemName.Levitation, ItemName.OarsmansBadge, ItemName.LungfishCall]
        return state.has_all(items, self.player) and self.has_upper_asylum_access(state)

    def has_stop_sign(self, state: CollectionState) -> bool:
        return state.has(ItemName.StopSign, self.player)

    def has_flowers(self, state: CollectionState) -> bool:
        return state.has(ItemName.Flowers, self.player)

    def has_plunger(self, state: CollectionState) -> bool:
        return state.has(ItemName.Plunger, self.player)

    def has_hedge_trimmers(self, state: CollectionState) -> bool:
        return state.has(ItemName.HedgeTrimmers, self.player)

    def has_rolling_pin(self, state: CollectionState) -> bool:
        return state.has(ItemName.RollingPin, self.player)

    def has_candle(self, state: CollectionState) -> bool:
        return state.has(ItemName.Candle, self.player)

    def has_both_candles(self, state: CollectionState) -> bool:
        return state.has(ItemName.Candle, self.player, 2)

    def has_megaphone(self, state: CollectionState) -> bool:
        return state.has(ItemName.Megaphone, self.player)

    def has_freds_letter(self, state: CollectionState) -> bool:
        return state.has(ItemName.FredsLetter, self.player)

    def has_priceless_coin(self, state: CollectionState) -> bool:
        return state.has(ItemName.PricelessCoin, self.player)

    def has_musket(self, state: CollectionState) -> bool:
        return state.has(ItemName.Musket, self.player)

    def has_cobweb_duster(self, state: CollectionState) -> bool:
        return state.has(ItemName.CobwebDuster, self.player)

    def has_levitation(self, state: CollectionState) -> bool:
        if self.world.options.StartingLevitation:
            return True
        else:
            return state.has(ItemName.Levitation, self.player)

    def has_telekinesis(self, state: CollectionState) -> bool:
        return state.has(ItemName.Telekinesis, self.player)

    def has_pyrokinesis(self, state: CollectionState) -> bool:
        return state.has(ItemName.Pyrokinesis, self.player)

    def has_clairvoyance(self, state: CollectionState) -> bool:
        return state.has(ItemName.Clairvoyance, self.player)

    def has_marksmanship(self, state: CollectionState) -> bool:
        return state.has(ItemName.Marksmanship, self.player)

    def has_invisibility(self, state: CollectionState) -> bool:
        return state.has(ItemName.Invisibility, self.player)

    def has_shield(self, state: CollectionState) -> bool:
        return state.has(ItemName.Shield, self.player)

    def has_confusion(self, state: CollectionState) -> bool:
        return state.has(ItemName.Confusion, self.player)

    def has_upper_asylum_access(self, state: CollectionState) -> bool:
        return state.has_all([ItemName.LobotoPainting, ItemName.GloriasTrophy, ItemName.StraightJacket], self.player)

    def has_oleander_boss_access(self, state: CollectionState) -> bool:
        return state.has_all([ItemName.Cake, ItemName.Telekinesis, ItemName.Pyrokinesis], self.player)

    def redeemed_brain_goal(self, state: CollectionState, amount) -> bool:
        return amount <= sum([state.has(item_name, self.player) for item_name in BRAIN_JARS])

    def set_psy_rules(self) -> None:
        multiworld = self.world.multiworld
        player = self.player

        for region in multiworld.get_regions(player):
            if region.name in self.region_rules:
                for entrance in region.entrances:
                    entrance.access_rule = self.region_rules[region.name]

        self.set_psy_goal()

        # Locations which are not included in PsychoSeed generation do not place items into the Psychonauts game world,
        # instead relying on the Archipelago client to tell Psychonauts to spawn in the item as if it were receiving a
        # non-local item, so these locations cannot contain Psychonauts items that can only be placed locally.
        local_only_forbidden: Set[str] = set()

        if self.world.options.DeepArrowheadShuffle:
            # Deep Arrowhead Shuffle locations do not place items into the world.
            local_only_forbidden.update(DEEP_ARROWHEAD_LOCATIONS.keys())

            def has_dowsing_rod(state: CollectionState):
                return state.has(ItemName.DowsingRod, player)

            for deep_ah_location_name in DEEP_ARROWHEAD_LOCATIONS:
                location = multiworld.get_location(deep_ah_location_name, player)
                add_rule(location, has_dowsing_rod)

        if self.world.options.MentalCobwebShuffle:
            local_only_forbidden.update(MENTAL_COBWEB_LOCATIONS.keys())

            for mental_cobweb_location_name in MENTAL_COBWEB_LOCATIONS:
                location = multiworld.get_location(mental_cobweb_location_name, player)
                # For simplicity, the rule is currently added to all mental cobweb locations, but it might be worth
                # considering skipping adding the rule if the location's region already requires the Cobweb Duster to
                # access.
                add_rule(location, self.has_cobweb_duster)

            # Extra per-cobweb rules that are not covered by the Region the cobweb is in:
            # BB Grindrail Wall requires Levitation because the ground around the cobweb is sloped and Raz bounces off
            # it when falling onto it too fast, so Levitation is needed to float down slowly.
            add_rule(multiworld.get_location(LocationName.CobwebGrindrailWall, player), self.has_levitation)

        if local_only_forbidden:
            def forbid_local_only(item: Item):
                return item.player != player or item.name not in LOCAL_SET

            for location_name in local_only_forbidden:
                location = multiworld.get_location(location_name, player)
                add_item_rule(location, forbid_local_only)

    def set_psy_goal(self):
        goal_option = self.world.options.Goal

        # Goals are always logically completed in sequence:
        # 1) Brain Hunt
        # 2) Brain Tank
        # 3) Meat Circus
        # Victory is achieved upon completing the last goal in the sequence that is enabled.

        # Either the Brain Hunt goal or the Brain Tank goal will always be enabled.

        # Brain Hunt goal
        if goal_option == Goal.option_brain_hunt or goal_option == Goal.option_asylum_brain_tank_and_brain_hunt:
            redeemed_required_brains = self.multiworld.get_location(LocationName.RedeemedBrainsEvent, self.player)
            brains_required = self.world.options.BrainsRequired.value
            redeemed_required_brains.access_rule = lambda state: self.redeemed_brain_goal(state, brains_required)
        else:
            redeemed_required_brains = None

        # Brain Tank goal
        if goal_option == Goal.option_asylum_brain_tank or goal_option == Goal.option_asylum_brain_tank_and_brain_hunt:
            oleander_boss_location = self.multiworld.get_location(LocationName.OleanderBrainTankBossEvent, self.player)
            oleander_boss_location.access_rule = self.has_oleander_boss_access
            # With Brain Hunt also enabled, accessing the Brain Tank is set to logically require completing the Brain
            # Hunt first, though this is not currently enforced by Psychonauts.
            if redeemed_required_brains:
                add_rule(oleander_boss_location, redeemed_required_brains.can_reach)
        else:
            oleander_boss_location = None

        # Meat Circus Final Boss goal
        if self.world.options.RequireMeatCircus:
            # The Meat Circus Final Boss can only be accessed after completing the previous enabled goal(s). This is
            # enforced by Psychonauts.
            final_boss_location = self.multiworld.get_location(LocationName.MeatCircusFinalBossEvent, self.player)
            # If enabled, the Brain Tank will be the previous goal, otherwise it will be the Brain Hunt.
            previous_goal_location = oleander_boss_location or redeemed_required_brains
            final_boss_location.access_rule = previous_goal_location.can_reach

        self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Victory, self.player)
