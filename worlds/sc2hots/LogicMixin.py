from BaseClasses import MultiWorld
from worlds.AutoWorld import LogicMixin
from .Options import get_option_value
from .Items import get_basic_units, defense_ratings, zerg_defense_ratings

KERRIGAN_ACTIVES = [
    {'Kinetic Blast (Kerrigan Tier 1)', 'Leaping Strike (Kerrigan Tier 1)'},
    {'Crushing Grip (Kerrigan Tier 2)', 'Psionic Shift (Kerrigan Tier 2)'},
    set(),
    {'Wild Mutation (Kerrigan Tier 4)', 'Spawn Banelings (Kerrigan Tier 4)', 'Mend (Kerrigan Tier 4)'},
    set(),
    set(),
    {'Apocalypse (Kerrigan Tier 7)', 'Spawn Leviathan (Kerrigan Tier 7)', 'Drop-Pods (Kerrigan Tier 7)'},
]

KERRIGAN_PASSIVES = [
    {"Heroic Fortitude (Kerrigan Tier 1)"},
    {"Chain Reaction (Kerrigan Tier 2)"},
    {"Zergling Reconstitution (Kerrigan Tier 3)", "Improved Overlords (Kerrigan Tier 3)", "Automated Extractors (Kerrigan Tier 3)"},
    set(),
    {"Twin Drones (Kerrigan Tier 5)", "Malignant Creep (Kerrigan Tier 5)", "Vespene Efficiency (Kerrigan Tier 5)"},
    {"Infest Broodlings (Kerrigan Tier 6)", "Fury (Kerrigan Tier 6)", "Ability Efficiency (Kerrigan Tier 6)"},
    set(),
]
KERRIGAN_ONLY_PASSIVES = {
    "Heroic Fortitude (Kerrigan Tier 1)", "Chain Reaction (Kerrigan Tier 2)",
    "Infest Broodlings (Kerrigan Tier 6)", "Fury (Kerrigan Tier 6)", "Ability Efficiency (Kerrigan Tier 6)"
}

class SC2HotSLogic(LogicMixin):
    def _sc2hots_has_common_unit(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_any(get_basic_units(multiworld, player), player)

    def _sc2hots_has_good_antiair(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_any({'Hydralisk', 'Mutalisk'}, player) or \
            self.has_all({'Swarm Host', 'Pressurized Glands (Swarm Host)'}, player) or \
            (get_option_value(multiworld, player, 'required_tactics') > 0 and self.has('Infestor', player))

    def _sc2hots_has_minimal_antiair(self, multiworld: MultiWorld, player: int) -> bool:
        return self._sc2hots_has_good_antiair(multiworld, player) or get_option_value(multiworld, player, 'kerriganless') == 0 or \
            self.has('Swarm Queen', player) or (get_option_value(multiworld, player, 'required_tactics') > 0 and self.has('Spore Crawler', player))
    
    def _sc2hots_has_brood_lord(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_all({'Mutalisk', 'Brood Lord Strain (Mutalisk)'}, player)
    
    def _sc2hots_has_viper(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_all({'Mutalisk', 'Viper Strain (Mutalisk)'}, player)

    def _sc2hots_has_impaler_or_lurker(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has('Hydralisk', player) and self.has_any({'Impaler Strain (Hydralisk)', 'Lurker Strain (Hydralisk)'}, player)

    def _sc2hots_has_competent_comp(self, multiworld: MultiWorld, player: int) -> bool:
        advanced = get_option_value(multiworld, player, 'required_tactics') > 0
        core_unit = self.has_any({'Roach', 'Aberration', 'Zergling'}, player)
        support_unit = self.has_any({'Swarm Queen', 'Hydralisk'}, player) \
                       or self._sc2hots_has_brood_lord(multiworld, player) \
                       or advanced and (self.has('Infestor', player) or self._sc2hots_has_viper(multiworld, player))
        if core_unit and support_unit:
            return True
        vespene_unit = self.has_any({'Ultralisk', 'Aberration'}, player) \
                       or advanced and self._sc2hots_has_viper(multiworld, player)
        return vespene_unit and self.has_any({'Zergling', 'Swarm Queen'}, player)

    def _sc2hots_has_basic_comp(self, multiworld: MultiWorld, player: int) -> bool:
        if get_option_value(multiworld, player, 'game_difficulty') < 3 \
           or self._sc2hots_has_basic_kerrigan(multiworld, player) \
           or self._sc2hots_has_two_kerrigan_actives(multiworld, player):
            return self._sc2hots_has_common_unit(multiworld, player)
        else:
            return self._sc2hots_has_competent_comp(multiworld, player)

    def _sc2hots_can_spread_creep(self, multiworld: MultiWorld, player: int) -> bool:
        return get_option_value(multiworld, player, 'required_tactics') > 0 or self.has('Swarm Queen', player)
    
    def _sc2hots_has_competent_defense(self, multiworld: MultiWorld, player: int) -> bool:
        return self._sc2hots_has_common_unit(multiworld, player) and \
            ((self.has('Swarm Host', player) or self._sc2hots_has_brood_lord(multiworld, player) or self._sc2hots_has_impaler_or_lurker(multiworld, player)) or \
            (get_option_value(multiworld, player, 'required_tactics') > 0 and (self._sc2hots_has_viper(multiworld, player) or self.has('Spine Crawler', player))))

    def _sc2hots_has_basic_kerrigan(self, multiworld: MultiWorld, player: int) -> bool:
        # One active ability that can be used to defeat enemies directly on Standard
        if get_option_value(multiworld, player, "required_tactics") == 0 and \
            not self.has_any({"Kinetic Blast (Kerrigan Tier 1)", "Leaping Strike (Kerrigan Tier 1)",
                              "Crushing Grip (Kerrigan Tier 2)", "Psionic Shift (Kerrigan Tier 2)",
                              "Spawn Banelings (Kerrigan Tier 4)"}, player):
            return False
        # Two non-ultimate abilities
        count = 0
        for item in ("Kinetic Blast (Kerrigan Tier 1)", "Leaping Strike (Kerrigan Tier 1)", "Heroic Fortitude (Kerrigan Tier 1)",
                     "Chain Reaction (Kerrigan Tier 2)", "Crushing Grip (Kerrigan Tier 2)", "Psionic Shift (Kerrigan Tier 2)",
                     "Spawn Banelings (Kerrigan Tier 4)", "Infest Broodlings (Kerrigan Tier 6)", "Fury (Kerrigan Tier 6)"):
            if self.has(item, player):
                count += 1
            if count >= 2:
                return True
        return False

    def _sc2hots_has_two_kerrigan_actives(self, multiworld: MultiWorld, player: int) -> bool:
        count = 0
        for i in range(7):
            if self.has_any(KERRIGAN_ACTIVES[i], player):
                count += 1
        return count >= 2

    def _sc2hots_has_low_tech(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_any({'Zergling', 'Swarm Queen', 'Spine Crawler'}, player) \
               or self._sc2hots_has_common_unit(multiworld, player) and self._sc2hots_has_basic_kerrigan(multiworld, player)

    # def _sc2wol_has_air(self, multiworld: MultiWorld, player: int) -> bool:
    #     return self.has_any({'Viking', 'Wraith', 'Banshee'}, player) or get_option_value(multiworld, player, 'required_tactics') > 0 \
    #             and self.has_any({'Hercules', 'Medivac'}, player) and self._sc2wol_has_common_unit(multiworld, player)

    # def _sc2wol_has_air_anti_air(self, multiworld: MultiWorld, player: int) -> bool:
    #     return self.has('Viking', player) \
    #            or get_option_value(multiworld, player, 'required_tactics') > 0 and self.has('Wraith', player)

    # def _sc2wol_has_competent_anti_air(self, multiworld: MultiWorld, player: int) -> bool:
    #     return self.has('Goliath', player) \
    #             or self.has('Marine', player) and self.has_any({'Medic', 'Medivac'}, player) \
    #             or self._sc2wol_has_air_anti_air(multiworld, player)

    # def _sc2wol_has_anti_air(self, multiworld: MultiWorld, player: int) -> bool:
    #     return self.has_any({'Missile Turret', 'Thor', 'War Pigs', 'Spartan Company', "Hel's Angel", 'Battlecruiser', 'Marine', 'Wraith'}, player) \
    #             or self._sc2wol_has_competent_anti_air(multiworld, player) \
    #             or get_option_value(multiworld, player, 'required_tactics') > 0 and self.has_any({'Ghost', 'Spectre'}, player)

    # def _sc2wol_defense_rating(self, multiworld: MultiWorld, player: int, zerg_enemy: bool, air_enemy: bool = True) -> bool:
    #     defense_score = sum((defense_ratings[item] for item in defense_ratings if self.has(item, player)))
    #     if self.has_any({'Marine', 'Marauder'}, player) and self.has('Bunker', player):
    #         defense_score += 3
    #     if self.has_all({'Siege Tank', 'Maelstrom Rounds'}, player):
    #         defense_score += 2
    #     if zerg_enemy:
    #         defense_score += sum((zerg_defense_ratings[item] for item in zerg_defense_ratings if self.has(item, player)))
    #         if self.has('Firebat', player) and self.has('Bunker', player):
    #             defense_score += 2
    #     if not air_enemy and self.has('Missile Turret', player):
    #         defense_score -= defense_ratings['Missile Turret']
    #     # Advanced Tactics bumps defense rating requirements down by 2
    #     if get_option_value(multiworld, player, 'required_tactics') > 0:
    #         defense_score += 2
    #     return defense_score

    # def _sc2wol_has_competent_comp(self, multiworld: MultiWorld, player: int) -> bool:
    #     return (self.has('Marine', player) or self.has('Marauder', player) and
    #             self._sc2wol_has_competent_anti_air(multiworld, player)) and self.has_any({'Medivac', 'Medic'}, player) or \
    #            self.has('Thor', player) or self.has("Banshee", player) and self._sc2wol_has_competent_anti_air(multiworld, player) or \
    #            self.has('Battlecruiser', player) and self._sc2wol_has_common_unit(multiworld, player) or \
    #            self.has('Siege Tank', player) and self._sc2wol_has_competent_anti_air(multiworld, player)

    # def _sc2wol_has_train_killers(self, multiworld: MultiWorld, player: int) -> bool:
    #     return (self.has_any({'Siege Tank', 'Diamondback', 'Marauder'}, player) or get_option_value(multiworld, player, 'required_tactics') > 0
    #             and self.has_all({'Reaper', "G-4 Clusterbomb"}, player) or self.has_all({'Spectre', 'Psionic Lash'}, player))

    # def _sc2wol_able_to_rescue(self, multiworld: MultiWorld, player: int) -> bool:
    #     return self.has_any({'Medivac', 'Hercules', 'Raven', 'Viking'}, player) or get_option_value(multiworld, player, 'required_tactics') > 0

    # def _sc2wol_has_protoss_common_units(self, multiworld: MultiWorld, player: int) -> bool:
    #     return self.has_any({'Zealot', 'Immortal', 'Stalker', 'Dark Templar'}, player) \
    #             or get_option_value(multiworld, player, 'required_tactics') > 0 and self.has_any({'High Templar', 'Dark Templar'}, player)

    # def _sc2wol_has_protoss_medium_units(self, multiworld: MultiWorld, player: int) -> bool:
    #     return self._sc2wol_has_protoss_common_units(multiworld, player) and \
    #            self.has_any({'Stalker', 'Void Ray', 'Phoenix', 'Carrier'}, player) \
    #            or get_option_value(multiworld, player, 'required_tactics') > 0 and self.has_any({'High Templar', 'Dark Templar'}, player)

    # def _sc2wol_beats_protoss_deathball(self, multiworld: MultiWorld, player: int) -> bool:
    #     return self.has_any({'Banshee', 'Battlecruiser'}, player) and self._sc2wol_has_competent_anti_air(multiworld, player) or \
    #            self._sc2wol_has_competent_comp(multiworld, player) and self._sc2wol_has_air_anti_air(multiworld, player)

    # def _sc2wol_has_mm_upgrade(self, multiworld: MultiWorld, player: int) -> bool:
    #     return self.has_any({"Combat Shield (Marine)", "Stabilizer Medpacks (Medic)"}, player)

    # def _sc2wol_survives_rip_field(self, multiworld: MultiWorld, player: int) -> bool:
    #     return self.has("Battlecruiser", player) or \
    #        self._sc2wol_has_air(multiworld, player) and \
    #        self._sc2wol_has_competent_anti_air(multiworld, player) and \
    #        self.has("Science Vessel", player)

    # def _sc2wol_has_nukes(self, multiworld: MultiWorld, player: int) -> bool:
    #     return get_option_value(multiworld, player, 'required_tactics') > 0 and self.has_any({'Ghost', 'Spectre'}, player)

    # def _sc2wol_final_mission_requirements(self, multiworld: MultiWorld, player: int):
    #     beats_kerrigan = self.has_any({'Marine', 'Banshee', 'Ghost'}, player) or get_option_value(multiworld, player, 'required_tactics') > 0
    #     if get_option_value(multiworld, player, 'all_in_map') == 0:
    #         # Ground
    #         defense_rating = self._sc2wol_defense_rating(multiworld, player, True, False)
    #         if self.has_any({'Battlecruiser', 'Banshee'}, player):
    #             defense_rating += 3
    #         return defense_rating >= 12 and beats_kerrigan
    #     else:
    #         # Air
    #         defense_rating = self._sc2wol_defense_rating(multiworld, player, True, True)
    #         return defense_rating >= 8 and beats_kerrigan \
    #             and self.has_any({'Viking', 'Battlecruiser'}, player) \
    #             and self.has_any({'Hive Mind Emulator', 'Psi Disruptor', 'Missile Turret'}, player)

    def _sc2hots_cleared_missions(self, multiworld: MultiWorld, player: int, mission_count: int) -> bool:
        return self.has_group("Missions", player, mission_count)
