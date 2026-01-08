from __future__ import annotations

from typing import List, Set

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class FinalFantasyXIVArchipelagoOptions:
    final_fantasy_xiv_content_types_allowed: FinalFantasyXIVContentTypesAllowed
    final_fantasy_xiv_expansions_accessible: FinalFantasyXIVExpansionsAccessible
    final_fantasy_xiv_playable_jobs: FinalFantasyXIVPlayableJobs


class FinalFantasyXIVGame(Game):
    # Initial implementation by @delcake on Discord

    name = "Final Fantasy XIV"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = FinalFantasyXIVArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete any instanced duty objectives without utilizing the Unrestricted Party option",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Travel without the use of Teleport, Return, or other item-based teleportation methods",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objective_list = list()
        
        # What percentage of the pool of possible objectives should each content type represent?
        battle_content_frequency = 0.35
        pvp_content_frequency = 0.2
        doh_dol_content_frequency = 0.25
        side_content_frequency = 0.2

        # What percentage of their parent content type should each objective type represent?
        # Each section should add up to 1.
        # Battle Content:
        fate_objective_frequency = 0.05
        guildhest_objective_frequency = 0.05
        treasure_hunt_objective_frequency = 0.05
        the_hunt_objective_frequency = 0.05
        dungeon_objective_Frequency = 0.15
        trial_objective_frequency = 0.15
        extreme_trial_objective_frequency = 0.03
        normal_raid_objective_frequency = 0.15
        savage_raid_objective_frequency = 0.03
        alliance_raid_objective_frequency = 0.05
        chaotic_alliance_raid_objective_frequency = 0.01
        deep_dungeon_objective_frequency = 0.04
        variant_dungeon_objective_frequency = 0.08
        adventuring_foray_objective_frequency = 0.05
        limited_job_objective_frequency = 0.06
        # PvP Content:
        crystalline_conflict_objective_frequency = 0.5
        frontline_objective_frequency = 0.4
        rival_wings_objective_frequency = 0.1
        # DoH/DoL Content:
        gathering_objective_frequency = 0.3
        fishing_objective_frequency = 0.2
        crafting_objective_frequency = 0.5
        # Side Content:
        jumping_puzzle_objective_frequency = 0.22
        gold_saucer_objective_frequency = 0.22
        triple_triad_objective_frequency = 0.55
        minigame_objective_frequency = 0.01

        # Objectives are determined entirely by what the player opts in to from their
        # configuration file. However, some types will be added as defaults if no valid
        # keys are provided to pick from.
        if "FATEs" in self.content_types_allowed or len(self.content_types_allowed) == 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete COUNT FATEs in ZONE with gold credit (Optional choice of jobs: JOBS)",
                    data={
                        "COUNT": (self.fate_range, 1),
                        "ZONE": (self.zones, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(battle_content_frequency, fate_objective_frequency, 0.6),
                ),
                GameObjectiveTemplate(
                    label="Complete one FATE with gold credit in each zone: ZONE (Optional choice of jobs: JOBS)",
                    data={
                        "ZONE": (self.zones, 3),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(battle_content_frequency, fate_objective_frequency, 0.35),
                ),
            ]

            if self.unreasonable_tasks_enabled:
                objective_list += [
                    GameObjectiveTemplate(
                        label="Complete World FATE 'NAME' with gold credit (Optional choice of jobs: JOBS)",
                        data={
                            "NAME": (self.world_fates, 1),
                            "JOBS": (self.combat_jobs, 2),
                        },
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=self.dynamic_weight(battle_content_frequency, fate_objective_frequency, 0.05),
                    ),
                ]

        if "Guildhests" in self.content_types_allowed or len(self.content_types_allowed) == 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete the Guildhest 'GUILDHEST' (Optional choice of jobs: JOBS)",
                    data={
                        "GUILDHEST": (self.guildhests, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(battle_content_frequency, guildhest_objective_frequency, 1),
                ),
            ]

        if "Jumping Puzzles" in self.content_types_allowed or len(self.content_types_allowed) == 0:
            if len(self.jumping_puzzles()) > 0:
                objective_list += [
                    GameObjectiveTemplate(
                        label="Scale the jumping puzzle located at LOC",
                        data={
                            "LOC": (self.jumping_puzzles, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=self.dynamic_weight(side_content_frequency, jumping_puzzle_objective_frequency, 0.9),
                    ),
                ]
            
            if "Gold Saucer" in self.content_types_allowed:
                objective_list += [
                    GameObjectiveTemplate(
                        label="Complete any 'Leap of Faith' GATE in the Gold Saucer",
                        data=dict(),
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=self.dynamic_weight(side_content_frequency, jumping_puzzle_objective_frequency, 0.1),
                    ),
                ]
        
        if "Treasure Hunt" in self.content_types_allowed:
            objective_list += [
                GameObjectiveTemplate(
                    label="Decipher a MAP and claim its treasure (Optional choice of jobs: JOBS)",
                    data={
                        "MAP": (self.treasure_hunt_maps, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(battle_content_frequency, treasure_hunt_objective_frequency, 0.7),
                ),
                GameObjectiveTemplate(
                    label="Enter the Treasure Dungeon 'DUNGEON' and clear at least one chamber for its reward (Optional choice of jobs: JOBS)",
                    data={
                        "DUNGEON": (self.treasure_hunt_dungeons, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(battle_content_frequency, treasure_hunt_objective_frequency, 0.25),
                ),
            ]

            if self.unreasonable_tasks_enabled:
                objective_list += [
                    GameObjectiveTemplate(
                        label="Enter the Treasure Dungeon 'DUNGEON' and successfully clear all chambers (Optional choice of jobs: JOBS)",
                        data={
                            "DUNGEON": (self.treasure_hunt_dungeons, 1),
                            "JOBS": (self.combat_jobs, 2),
                        },
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=self.dynamic_weight(battle_content_frequency, treasure_hunt_objective_frequency, 0.05),
                    ),
                ]

        if "The Hunt" in self.content_types_allowed or len(self.content_types_allowed) == 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="Locate and defeat B-rank Hunt mark MARK",
                    data={
                        "MARK": (self.hunt_b_ranks, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(battle_content_frequency, the_hunt_objective_frequency, 0.85),
                ),
            ]

            if self.unreasonable_tasks_enabled:
                objective_list += [
                    GameObjectiveTemplate(
                        label="Successfully spawn S-rank Hunt mark MARK",
                        data={
                            "MARK": (self.hunt_s_ranks, 1),
                        },
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=self.dynamic_weight(battle_content_frequency, the_hunt_objective_frequency, 0.15),
                    ),
                ]
        
        if "Dungeons" in self.content_types_allowed or len(self.content_types_allowed) == 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete the Dungeon 'DUTY' (Optional choice of jobs: JOBS)",
                    data={
                        "DUTY": (self.dungeons, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(battle_content_frequency, dungeon_objective_Frequency, 1),
                ),
            ]
        
        if "Trials" in self.content_types_allowed or len(self.content_types_allowed) == 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete the Trial 'DUTY' (Optional choice of jobs: JOBS)",
                    data={
                        "DUTY": (self.trials, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(battle_content_frequency, trial_objective_frequency, 1),
                ),
            ]

        if "Extreme Trials" in self.content_types_allowed:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete the Extreme Trial 'DUTY' (Optional choice of jobs: JOBS)",
                    data={
                        "DUTY": (self.extreme_trials, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=self.dynamic_weight(battle_content_frequency, extreme_trial_objective_frequency, 1),
                ),
            ]

        if "Normal Raids" in self.content_types_allowed:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete the Normal Raid 'DUTY' (Optional choice of jobs: JOBS)",
                    data={
                        "DUTY": (self.normal_raids, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(battle_content_frequency, normal_raid_objective_frequency, 1),
                ),
            ]

        if "Savage Raids" in self.content_types_allowed:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete the Savage Raid 'DUTY' (Optional choice of jobs: JOBS)",
                    data={
                        "DUTY": (self.savage_raids, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=self.dynamic_weight(battle_content_frequency, savage_raid_objective_frequency, 1),
                ),
            ]

        if "Alliance Raids" in self.content_types_allowed:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete the Alliance Raid 'DUTY' (Optional choice of jobs: JOBS)",
                    data={
                        "DUTY": (self.alliance_raids, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(battle_content_frequency, alliance_raid_objective_frequency, 1),
                ),
            ]

        if "Chaotic Alliance Raids" in self.content_types_allowed:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete the Chaotic Alliance Raid 'DUTY' (Optional choice of jobs: JOBS)",
                    data={
                        "DUTY": (self.chaotic_alliance_raids, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=self.dynamic_weight(battle_content_frequency, chaotic_alliance_raid_objective_frequency, 1),
                ),
            ]
        
        if "Deep Dungeons" in self.content_types_allowed:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete NUM unique sets of floors in DEEPDUNGEON (Prior saves allowed, optional choice of jobs: JOBS)",
                    data={
                        "NUM": (self.deep_dungeon_floor_range, 1),
                        "DEEPDUNGEON": (self.deep_dungeons, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=self.dynamic_weight(battle_content_frequency, deep_dungeon_objective_frequency, 0.3),
                ),
                GameObjectiveTemplate(
                    label="Obtain NUM Accursed Hoard from a single set of floors in DEEPDUNGEON (Prior saves allowed, optional choice of jobs: JOBS)",
                    data={
                        "NUM": (self.deep_dungeon_hoard_count, 1),
                        "DEEPDUNGEON": (self.deep_dungeons, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(battle_content_frequency, deep_dungeon_objective_frequency, 0.2),
                ),
                GameObjectiveTemplate(
                    label="Complete a single set of floors in DEEPDUNGEON without triggering any floor traps (Prior saves allowed, optional choice of jobs: JOBS)",
                    data={
                        "DEEPDUNGEON": (self.deep_dungeons, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(battle_content_frequency, deep_dungeon_objective_frequency, 0.2),
                ),
                GameObjectiveTemplate(
                    label="Defeat NUM enemies in DEEPDUNGEON (Prior saves allowed, optional choice of jobs: JOBS)",
                    data={
                        "NUM": (self.deep_dungeon_kill_count, 1),
                        "DEEPDUNGEON": (self.deep_dungeons, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(battle_content_frequency, deep_dungeon_objective_frequency, 0.2),
                ),
                GameObjectiveTemplate(
                    label="Complete a single set of floors in DEEPDUNGEON within 30 minutes (Prior saves allowed, optional choice of jobs: JOBS)",
                    data={
                        "DEEPDUNGEON": (self.deep_dungeons, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(battle_content_frequency, deep_dungeon_objective_frequency, 0.1),
                ),
            ]

        if "Variant Dungeons" in self.content_types_allowed and len(self.variant_dungeon_routes()) > 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="Complete the Variant Dungeon route which corresponds to the record entry 'ROUTE' (Optional choice of jobs: JOBS)",
                    data={
                        "ROUTE": (self.variant_dungeon_routes, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(battle_content_frequency, variant_dungeon_objective_frequency, 1),
                ),
            ]
        
        if "Adventuring Forays" in self.content_types_allowed:
            if self.has_stormblood:
                objective_list += [
                    GameObjectiveTemplate(
                        label="Defeat the Notorious Monster spawn at Eureka LOC (Optional choice of jobs: JOBS)",
                        data={
                            "LOC": (self.eureka_nm_fates, 1),
                            "JOBS": (self.combat_jobs, 2),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=self.dynamic_weight(battle_content_frequency, adventuring_foray_objective_frequency, 0.3),
                    ),
                    GameObjectiveTemplate(
                        label="Complete the Happy Bunny elemental conflict at Eureka FATE and uncover a QUALITY coffer (Optional choice of jobs: JOBS)",
                        data={
                            "FATE": (self.eureka_bunny_fates, 1),
                            "QUALITY": (self.eureka_bunny_coffers, 1),
                            "JOBS": (self.combat_jobs, 2),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=self.dynamic_weight(battle_content_frequency, adventuring_foray_objective_frequency, 0.15),
                    ),
                ]

                if self.unreasonable_tasks_enabled:
                    objective_list += [
                        GameObjectiveTemplate(
                            label="Spawn and defeat the Notorious Monster for Eureka LOC (Optional choice of jobs: JOBS)",
                            data={
                                "LOC": (self.eureka_nm_fates, 1),
                                "JOBS": (self.combat_jobs, 2),
                            },
                            is_time_consuming=True,
                            is_difficult=False,
                            weight=self.dynamic_weight(battle_content_frequency, adventuring_foray_objective_frequency, 0.05),
                        ),
                    ]

            if self.has_shadowbringers:
                objective_list += [
                    GameObjectiveTemplate(
                        label="Complete the Skirmish at LOC (Optional choice of jobs: JOBS)",
                        data={
                            "LOC": (self.bozja_fates, 1),
                            "JOBS": (self.combat_jobs, 2),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=self.dynamic_weight(battle_content_frequency, adventuring_foray_objective_frequency, 0.3),
                    ),
                    GameObjectiveTemplate(
                        label="Complete the Critical Engagement at LOC (Optional choice of jobs: JOBS)",
                        data={
                            "LOC": (self.bozja_ce_fates, 1),
                            "JOBS": (self.combat_jobs, 2),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=self.dynamic_weight(battle_content_frequency, adventuring_foray_objective_frequency, 0.15),
                    ),
                ]

                if self.unreasonable_tasks_enabled:
                    objective_list += [
                        GameObjectiveTemplate(
                            label="Win the Critical Engagement duel at LOC (Optional choice of jobs: JOBS)",
                            data={
                                "LOC": (self.bozja_duel_fates, 1),
                                "JOBS": (self.combat_jobs, 2),
                            },
                            is_time_consuming=True,
                            is_difficult=True,
                            weight=self.dynamic_weight(battle_content_frequency, adventuring_foray_objective_frequency, 0.05),
                        ),
                    ]

        if "Limited Jobs" in self.content_types_allowed:
            if "Blue Mage" in self.playable_jobs:
                objective_list += [
                    GameObjectiveTemplate(
                        label="In Masked Carnivale, complete the stage 'STAGE' within the TIME Completion Time",
                        data={
                            "STAGE": (self.masked_carnivale, 1),
                            "TIME": (self.masked_carnivale_completion_times, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=self.dynamic_weight(battle_content_frequency, limited_job_objective_frequency, 0.8),
                    ),
                    GameObjectiveTemplate(
                        label="In Masked Carnivale, complete the Weekly DIFF Target stage, satisfying all completion requirements within the TIME Completion Time",
                        data={
                            "DIFF": (self.masked_carnivale_weekly_targets, 1),
                            "TIME": (self.masked_carnivale_completion_times, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=self.dynamic_weight(battle_content_frequency, limited_job_objective_frequency, 0.2),
                    ),
                ]
        
        if "Gathering" in self.content_types_allowed and len(self.gathering_collectables()) > 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="Turn in COUNTx ITEM at the highest tier of collectability to a Collectable Appraiser",
                    data={
                        "COUNT": (self.gathering_collectables_count_range, 1),
                        "ITEM": (self.gathering_collectables, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(doh_dol_content_frequency, gathering_objective_frequency, 0.35),
                ),
                GameObjectiveTemplate(
                    label="Turn in at least one of each collectable at the highest tier of collectability to a Collectable Appraiser: ITEMS",
                    data={
                        "ITEMS": (self.gathering_collectables, 6),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(doh_dol_content_frequency, gathering_objective_frequency, 0.15),
                ),
                GameObjectiveTemplate(
                    label="Turn in COUNTx ITEM to the Firmament Resource Inspector",
                    data={
                        "COUNT": (self.firmament_gathering_collectables_count_range, 1),
                        "ITEM": (self.firmament_gathering_collectables, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(doh_dol_content_frequency, gathering_objective_frequency, 0.25),
                ),
                GameObjectiveTemplate(
                    label="Turn in COUNTx ITEM to the Firmament Resource Inspector",
                    data={
                        "COUNT": (self.firmament_gathering_collectables_count_range, 1),
                        "ITEM": (self.firmament_high_tier_gathering_collectables, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(doh_dol_content_frequency, gathering_objective_frequency, 0.2),
                ),
                GameObjectiveTemplate(
                    label="Defeat the following enemies with the Aetheromatic Auger in the Diadem: ENEMIES",
                    data={
                        "ENEMIES": (self.diadem_enemies, 3),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(doh_dol_content_frequency, gathering_objective_frequency, 0.05),
                ),
            ]

        if "Fishing" in self.content_types_allowed and len(self.fishing_collectables()) > 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="Turn in COUNTx ITEM at the highest tier of collectability to a Collectable Appraiser",
                    data={
                        "COUNT": (self.fishing_collectables_count_range, 1),
                        "ITEM": (self.fishing_collectables, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(doh_dol_content_frequency, fishing_objective_frequency, 0.3),
                ),
                GameObjectiveTemplate(
                    label="Turn in at least one of each collectable at the highest tier of collectability to a Collectable Appraiser: ITEMS",
                    data={
                        "ITEMS": (self.fishing_collectables, 6),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(doh_dol_content_frequency, fishing_objective_frequency, 0.15),
                ),
                GameObjectiveTemplate(
                    label="Turn in COUNTx ITEM to the Firmament Resource Inspector",
                    data={
                        "COUNT": (self.firmament_fishing_collectables_count_range, 1),
                        "ITEM": (self.firmament_fishing_collectables, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(doh_dol_content_frequency, fishing_objective_frequency, 0.3),
                ),
                GameObjectiveTemplate(
                    label="Turn in COUNTx ITEM to the Firmament Resource Inspector",
                    data={
                        "COUNT": (self.firmament_fishing_collectables_count_range, 1),
                        "ITEM": (self.firmament_high_tier_fishing_collectables, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(doh_dol_content_frequency, fishing_objective_frequency, 0.2),
                ),
            ]

            if self.unreasonable_tasks_enabled:
                objective_list += [
                    GameObjectiveTemplate(
                        label="Catch the Big Fish 'FISH'",
                        data={
                            "FISH": (self.big_fish, 1),
                        },
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=self.dynamic_weight(doh_dol_content_frequency, fishing_objective_frequency, 0.05),
                    ),
                ]

        if "Crafting" in self.content_types_allowed and len(self.crafting_collectables()) > 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="Turn in COUNTx ITEM at the highest tier of collectability to a Collectable Appraiser",
                    data={
                        "COUNT": (self.crafting_collectables_count_range, 1),
                        "ITEM": (self.crafting_collectables, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(doh_dol_content_frequency, crafting_objective_frequency, 0.35),
                ),
                GameObjectiveTemplate(
                    label="Turn in at least one of each collectable at the highest tier of collectability to a Collectable Appraiser: ITEMS",
                    data={
                        "ITEMS": (self.crafting_collectables, 4),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(doh_dol_content_frequency, crafting_objective_frequency, 0.15),
                ),
                GameObjectiveTemplate(
                    label="Turn in COUNTx ITEM at the highest tier of collectability to the Firmament Collectable Appraiser",
                    data={
                        "COUNT": (self.crafting_collectables_count_range, 1),
                        "ITEM": (self.firmament_crafting_collectables, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(doh_dol_content_frequency, crafting_objective_frequency, 0.3),
                ),
                GameObjectiveTemplate(
                    label="Turn in COUNTx ITEM at the highest tier of collectability to the Firmament Collectable Appraiser",
                    data={
                        "COUNT": (self.crafting_collectables_count_range, 1),
                        "ITEM": (self.firmament_high_tier_crafting_collectables, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(doh_dol_content_frequency, crafting_objective_frequency, 0.2),
                ),
            ]

        if "Crystalline Conflict" in self.content_types_allowed:
            objective_list += [
                GameObjectiveTemplate(
                    label="Participate in COUNT Crystalline Conflict matches (Optional choice of jobs: JOBS)",
                    data={
                        "COUNT": (self.crystalline_conflict_match_counts, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(pvp_content_frequency, crystalline_conflict_objective_frequency, 0.4),
                ),
                GameObjectiveTemplate(
                    label="Win COUNT Crystalline Conflict matches (Optional choice of jobs: JOBS)",
                    data={
                        "COUNT": (self.crystalline_conflict_match_counts, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=self.dynamic_weight(pvp_content_frequency, crystalline_conflict_objective_frequency, 0.1),
                ),
                GameObjectiveTemplate(
                    label="Score COUNT kills in a Crystalline Conflict match (Optional choice of jobs: JOBS)",
                    data={
                        "COUNT": (self.pvp_kill_counts, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=self.dynamic_weight(pvp_content_frequency, crystalline_conflict_objective_frequency, 0.15),
                ),
                GameObjectiveTemplate(
                    label="Score COUNT assists in a Crystalline Conflict match (Optional choice of jobs: JOBS)",
                    data={
                        "COUNT": (self.pvp_assist_counts, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(pvp_content_frequency, crystalline_conflict_objective_frequency, 0.35),
                ),
            ]

        if "Frontline" in self.content_types_allowed:
            objective_list += [
                GameObjectiveTemplate(
                    label="Participate in a Frontline match (Optional choice of jobs: JOBS)",
                    data={
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(pvp_content_frequency, frontline_objective_frequency, 0.4),
                ),
                GameObjectiveTemplate(
                    label="Win a Frontline match (Optional choice of jobs: JOBS)",
                    data={
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=self.dynamic_weight(pvp_content_frequency, frontline_objective_frequency, 0.1),
                ),
                GameObjectiveTemplate(
                    label="Score COUNT kills in a Frontline match (Optional choice of jobs: JOBS)",
                    data={
                        "COUNT": (self.pvp_kill_counts, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=self.dynamic_weight(pvp_content_frequency, frontline_objective_frequency, 0.15),
                ),
                GameObjectiveTemplate(
                    label="Score COUNT assists in a Frontline match (Optional choice of jobs: JOBS)",
                    data={
                        "COUNT": (self.pvp_assist_counts, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(pvp_content_frequency, frontline_objective_frequency, 0.35),
                ),
            ]

        if "Rival Wings" in self.content_types_allowed:
            objective_list += [
                GameObjectiveTemplate(
                    label="Participate in a Rival Wings match (Optional choice of jobs: JOBS)",
                    data={
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(pvp_content_frequency, rival_wings_objective_frequency, 0.4),
                ),
                GameObjectiveTemplate(
                    label="Win a Rival Wings match (Optional choice of jobs: JOBS)",
                    data={
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=self.dynamic_weight(pvp_content_frequency, rival_wings_objective_frequency, 0.1),
                ),
                GameObjectiveTemplate(
                    label="Score COUNT kills in a Rival Wings match (Optional choice of jobs: JOBS)",
                    data={
                        "COUNT": (self.pvp_kill_counts, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=self.dynamic_weight(pvp_content_frequency, rival_wings_objective_frequency, 0.15),
                ),
                GameObjectiveTemplate(
                    label="Score COUNT assists in a Rival Wings match (Optional choice of jobs: JOBS)",
                    data={
                        "COUNT": (self.pvp_assist_counts, 1),
                        "JOBS": (self.combat_jobs, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(pvp_content_frequency, rival_wings_objective_frequency, 0.35),
                ),
            ]

        if "Gold Saucer" in self.content_types_allowed or len(self.content_types_allowed) == 0:
            objective_list += [
                GameObjectiveTemplate(
                    label="TASK",
                    data={
                        "TASK": (self.gate_tasks, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(side_content_frequency, gold_saucer_objective_frequency, 0.15),
                ),
                GameObjectiveTemplate(
                    label="Successfully complete COUNT GATEs in the Gold Saucer",
                    data={
                        "COUNT": (self.gate_count, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=self.dynamic_weight(side_content_frequency, gold_saucer_objective_frequency, 0.2),
                ),
                GameObjectiveTemplate(
                    label="Claim a Small Item from The Moogle's Paw machine in the Gold Saucer",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(side_content_frequency, gold_saucer_objective_frequency, 0.1),
                ),
                GameObjectiveTemplate(
                    label="Earn a 'BRUTAL!!!' rating on the Cuff-a-Cur machine in the Gold Saucer",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(side_content_frequency, gold_saucer_objective_frequency, 0.1),
                ),
                GameObjectiveTemplate(
                    label="Earn a 'PULVERIZING!!!' rating on the Crystal Tower Striker machine in the Gold Saucer",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(side_content_frequency, gold_saucer_objective_frequency, 0.1),
                ),
                GameObjectiveTemplate(
                    label="Score 5+ points on the Monster Toss machine in the Gold Saucer",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(side_content_frequency, gold_saucer_objective_frequency, 0.05),
                ),
                GameObjectiveTemplate(
                    label="Participate in a Chocobo Race Duty Finder match",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(side_content_frequency, gold_saucer_objective_frequency, 0.2),
                ),
                GameObjectiveTemplate(
                    label="Place 1st in a Chocobo Race Duty Finder match",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=self.dynamic_weight(side_content_frequency, gold_saucer_objective_frequency, 0.1),
                ),
            ]

        if "Triple Triad" in self.content_types_allowed:
            objective_list += [
                GameObjectiveTemplate(
                    label="Defeat OPPONENT in a Triple Triad match",
                    data={
                        "OPPONENT": (self.triple_triad_opponents, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(side_content_frequency, triple_triad_objective_frequency, 0.2),
                ),
                GameObjectiveTemplate(
                    label="Defeat the following opponents in a Triple Triad match: OPPONENTS",
                    data={
                        "OPPONENTS": (self.triple_triad_opponents, 3),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(side_content_frequency, triple_triad_objective_frequency, 0.1),
                ),
                GameObjectiveTemplate(
                    label="Obtain the CARDFROMOPPONENT",
                    data={
                        "CARDFROMOPPONENT": (self.triple_triad_card_from_opponent_common, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=self.dynamic_weight(side_content_frequency, triple_triad_objective_frequency, 0.4),
                ),
                GameObjectiveTemplate(
                    label="Obtain the CARDFROMOPPONENT",
                    data={
                        "CARDFROMOPPONENT": (self.triple_triad_card_from_opponent_rare, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=self.dynamic_weight(side_content_frequency, triple_triad_objective_frequency, 0.3),
                ),
            ]

        if "Minigames" in self.content_types_allowed:
            if self.has_shadowbringers:
                objective_list += [
                    GameObjectiveTemplate(
                        label="Win COUNT consecutive matches of High or Low against Tista-Bie in Eulmore",
                        data={
                            "COUNT": (self.high_low_range, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=self.dynamic_weight(side_content_frequency, minigame_objective_frequency, 1),
                    ),
                ]
        
        return objective_list

    @property
    def expansions_accessible(self) -> Set[str]:
        return self.archipelago_options.final_fantasy_xiv_expansions_accessible.value

    def expansions(self) -> List[str]:
        return sorted(self.expansions_accessible)

    @property
    def has_heavensward(self) -> bool:
        return "Heavensward" in self.expansions_accessible

    @property
    def has_stormblood(self) -> bool:
        return "Stormblood" in self.expansions_accessible

    @property
    def has_shadowbringers(self) -> bool:
        return "Shadowbringers" in self.expansions_accessible

    @property
    def has_endwalker(self) -> bool:
        return "Endwalker" in self.expansions_accessible

    @property
    def has_dawntrail(self) -> bool:
        return "Dawntrail" in self.expansions_accessible

    @property
    def has_level_60_or_higher(self) -> bool:
        return (self.has_heavensward or self.has_level_70_or_higher)
    
    @property
    def has_level_70_or_higher(self) -> bool:
        return (self.has_stormblood or self.has_level_80_or_higher)
    
    @property
    def has_level_80_or_higher(self) -> bool:
        return (self.has_shadowbringers or self.has_level_90_or_higher)
    
    @property
    def has_level_90_or_higher(self) -> bool:
        return (self.has_endwalker or self.has_level_100_or_higher)
    
    @property
    def has_level_100_or_higher(self) -> bool:
        return (self.has_dawntrail)
    
    @property
    def content_types_allowed(self) -> Set[str]:
        return self.archipelago_options.final_fantasy_xiv_content_types_allowed.value

    @property
    def content_types_total(self) -> int:
        return len(self.archipelago_options.final_fantasy_xiv_content_types_allowed.valid_keys)

    @property
    def playable_jobs(self) -> Set[str]:
        return self.archipelago_options.final_fantasy_xiv_playable_jobs.value

    @property
    def unreasonable_tasks_enabled(self) -> bool:
        return "Unreasonable Tasks" in self.content_types_allowed

    @property
    def total_weight(self) -> int:
        return (len(self.content_types_allowed) * self.content_types_total * 2)

    def dynamic_weight(self, content_frequency, objective_type_frequency, objective_frequency) -> int:
        return int(self.total_weight * content_frequency * objective_type_frequency * objective_frequency)

    def combat_jobs(self) -> List[str]:
        combat_jobs = [
            "Paladin",
            "Warrior",
            "White Mage",
            "Scholar",
            "Monk",
            "Dragoon",
            "Ninja",
            "Bard",
            "Black Mage",
            "Summoner",
        ]

        heavensward_jobs = [
            "Dark Knight",
            "Astrologian",
            "Machinist",
        ]

        stormblood_jobs = [
            "Samurai",
            "Red Mage",
        ]

        shadowbringers_jobs = [
            "Gunbreaker",
            "Dancer",
        ]

        endwalker_jobs = [
            "Sage",
            "Reaper",
        ]

        dawntrail_jobs = [
            "Viper",
            "Pictomancer",
        ]

        if self.has_heavensward:
            combat_jobs.extend(heavensward_jobs)

        if self.has_stormblood:
            combat_jobs.extend(stormblood_jobs)

        if self.has_shadowbringers:
            combat_jobs.extend(shadowbringers_jobs)

        if self.has_endwalker:
            combat_jobs.extend(endwalker_jobs)

        if self.has_dawntrail:
            combat_jobs.extend(dawntrail_jobs)

        # Remove any jobs that the player has not enabled in their config.
        jobs = [job for job in combat_jobs if job in self.playable_jobs]

        if len(jobs) == 0:
            # The player didn't enable any jobs in their configuration, so
            # instead return all possible jobs.
            jobs = combat_jobs

        return sorted(jobs)

    def limited_jobs(self) -> List[str]:
        limited_jobs = [
            "Blue Mage",
            # "Beastmaster",
        ]

        # Remove any jobs that the player has not enabled in their config.
        jobs = [job for job in limited_jobs if job in self.playable_jobs]

        return sorted(jobs)

    @staticmethod
    def fate_range() -> range:
        return range(1, 6)

    def zones(self) -> List[str]:
        zones = [
            "Middle La Noscea",
            "Lower La Noscea",
            "Eastern La Noscea",
            "Western La Noscea",
            "Upper La Noscea",
            "Outer La Noscea",
            "Central Shroud",
            "East Shroud",
            "South Shroud",
            "North Shroud",
            "Western Thanalan",
            "Central Thanalan",
            "Eastern Thanalan",
            "Southern Thanalan",
            "Northern Thanalan",
            "Coerthas Central Highlands",
            "Mor Dhona",
        ]

        heavensward_zones = [
            "Coerthas Western highlands",
            "The Sea of Clouds",
            "Azys Lla",
            "The Dravanian Forelands",
            "The Dravanian Hinterlands",
            "The Churning Mists",
        ]

        stormblood_zones = [
            "The Fringes",
            "The Peaks",
            "The Lochs",
            "The Ruby Sea",
            "Yanxia",
            "The Azim Steppe",
        ]

        shadowbringers_zones = [
            "Lakeland",
            "Kholusia",
            "Amh Araeng",
            "Il Mheg",
            "The Rak'tika Greatwood",
            "The Tempest",
        ]

        endwalker_zones = [
            "Thavnair",
            "Garlemald",
            "Labyrinthos",
            "Mare Lamentorum",
            "Ultima Thule",
            "Elpis",
        ]

        dawntrail_zones = [
            "Urqopacha",
            "Kozama'uka",
            "Yak T'el",
            "Shaaloani",
            "Heritage Found",
            "Living Memory",
        ]

        if self.has_heavensward:
            zones.extend(heavensward_zones)

        if self.has_stormblood:
            zones.extend(stormblood_zones)

        if self.has_shadowbringers:
            zones.extend(shadowbringers_zones)

        if self.has_endwalker:
            zones.extend(endwalker_zones)

        if self.has_dawntrail:
            zones.extend(dawntrail_zones)

        return sorted(zones)

    def world_fates(self) -> List[str]:
        world_fates = [
            "He Taketh It with His Eyes",
            "Steel Reign",
        ]

        heavensward_world_fates = [
            "Coeurls Chase Boys Chase Coeurls",
            "Prey Online",
        ]

        stormblood_world_fates = [
            "A Horse Outside",
            "Foxy Lady",
        ]

        shadowbringers_world_fates = [
            "A Finale Most Formidable",
            "The Head, the Tail, the Whole Damned Thing",
        ]

        endwalker_world_fates = [
            "Devout Pilgrims vs. Daivadipa",
            "Omicron Recall: Killing Order",
        ]

        dawntrail_world_fates = [
            "The Serpentlord Seethes",
            "Mascot Murder",
        ]

        if self.has_heavensward:
            world_fates.extend(heavensward_world_fates)

        if self.has_stormblood:
            world_fates.extend(stormblood_world_fates)

        if self.has_shadowbringers:
            world_fates.extend(shadowbringers_world_fates)

        if self.has_endwalker:
            world_fates.extend(endwalker_world_fates)

        if self.has_dawntrail:
            world_fates.extend(dawntrail_world_fates)

        return sorted(world_fates)
    
    @staticmethod
    def guildhests() -> List[str]:
        guildests = [
            "Basic Training: Enemy Parties",
            "Under the Armor",
            "Basic Training: Enemy Strongholds",
            "Hero on the Half Shell",
            "Pulling Poison Posies",
            "Stinging Back",
            "All's Well that Ends in the Well",
            "Flicking Sticks and Taking Names",
            "More than a Feeler",
            "Annoy the Void",
            "Shadow and Claw",
            "Long Live the Queen",
            "Ward Up",
            "Solemn Trinity",
        ]

        return sorted(guildests)

    def treasure_hunt_maps(self) -> List[str]:
        maps = [
            "Timeworn Leather Map",
            "Timeworn Goatskin Map",
            "Timeworn Toadskin Map",
            "Timeworn Boarskin Map",
            "Timeworn Peisteskin Map",
            "Unhidden Leather Map",
        ]

        heavensward_maps = [
            "Timeworn Archaeoskin Map",
            "Timeworn Wyvernskin Map",
            "Timeworn Dragonskin Map",
        ]

        stormblood_maps = [
            "Timeworn Gaganaskin Map",
            "Timeworn Gazelleskin Map",
        ]

        shadowbringers_maps = [
            "Timeworn Gliderskin Map",
            "Timeworn Zonureskin Map",
        ]

        endwalker_maps = [
            "Timeworn Saigaskin Map",
            "Timeworn Kumbhiraskin Map",
            "Timeworn Ophiotauroskin Map",
        ]

        dawntrail_maps = [
            "Timeworn Loboskin Map",
            "Timeworn Br'aaxskin Map",
        ]

        if self.has_heavensward:
            maps.extend(heavensward_maps)

        if self.has_stormblood:
            maps.extend(stormblood_maps)

        if self.has_shadowbringers:
            maps.extend(shadowbringers_maps)

        if self.has_endwalker:
            maps.extend(endwalker_maps)

        if self.has_dawntrail:
            maps.extend(dawntrail_maps)

        return sorted(maps)
    
    def treasure_hunt_dungeons(self) -> List[str]:
        dungeons = list()

        heavensward_dungeons = [
            "The Aquapolis",
        ]

        stormblood_dungeons = [
            "The Lost Canals of Uznair",
            "The Shifting Altars of Uznair",
            "The Hidden Canals of Uznair",
        ]

        shadowbringers_dungeons = [
            "The Dungeons of Lyhe Ghiah",
            "The Shifting Oubliettes of Lyhe Ghiah",
        ]

        endwalker_dungeons = [
            "The Excitatron 6000",
            "The Shifting Gymnasion Agonon",
        ]

        dawntrail_dungeons = [
            "Cenote Ja Ja Gural",
        ]

        if self.has_heavensward:
            dungeons.extend(heavensward_dungeons)

        if self.has_stormblood:
            dungeons.extend(stormblood_dungeons)

        if self.has_shadowbringers:
            dungeons.extend(shadowbringers_dungeons)

        if self.has_endwalker:
            dungeons.extend(endwalker_dungeons)

        if self.has_dawntrail:
            dungeons.extend(dawntrail_dungeons)

        return sorted(dungeons)

    def hunt_b_ranks(self) -> List[str]:
        b_ranks = [
            "Skogs Fru",
            "Barbastelle",
            "Bloody Mary",
            "Dark Helmet",
            "Myradrosh",
            "Vuokho",
            "Sewer Syrup",
            "Ovjang",
            "Gatling",
            "Albin the Ashen",
            "Flame Sergeant Dalvag",
            "White Joker",
            "Stinging Sophie",
            "Monarch Ogrefly",
            "Phecda",
            "Naul",
            "Leech King",
        ]

        heavensward_b_ranks = [
            "Alteci",
            "Kreutzet",
            "Squonk",
            "Sanu Vali of Dancing Wings",
            "Gnath Cometdrone",
            "Thextera",
            "Scitalis",
            "The Scarecrow",
            "Pterygotus",
            "False Gigantopithecus",
            "Lycidas",
            "Omni",
        ]

        stormblood_b_ranks = [
            "Shadow-dweller Yamini",
            "Ouzelum",
            "Gwas-y-neidr",
            "Buccaboo",
            "Gauki Strongblade",
            "Guhuo Niao",
            "Deidar",
            "Gyorai Quickstrike",
            "Kurma",
            "Aswang",
            "Manes",
            "Kiwa",
        ]

        shadowbringers_b_ranks = [
            "La Velue",
            "Itzpapalotl",
            "Coquecigrue",
            "Indomitable",
            "Worm of the Well",
            "Juggler Hecatomb",
            "Domovoi",
            "Vulpangue",
            "Mindmaker",
            "Pachamama",
            "Gilshs Aath Swiftclaw",
            "Deacon",
        ]

        endwalker_b_ranks = [
            "Green Archon",
            "Ü-u-ü-u",
            "Vajrakumara",
            "Iravati",
            "Warmonger",
            "Emperor's Rose",
            "Daphnia Magna",
            "Genesis Rock",
            "Yumcax",
            "Shockmaw",
            "Level Cheater",
            "Oskh Rhei",
        ]

        dawntrail_b_ranks = [
            "Mad Maguey",
            "Chupacabra",
            "The Slammer",
            "Go'ozoabek'be",
            "Leafscourge Hadoll Ja",
            "Xty'iinbek",
            "Nopalitender Fabuloso",
            "Uktena",
            "Gallowsbeak",
            "Gargant",
            "Jewel Bearer",
            "13th Child",
        ]

        if self.has_heavensward:
            b_ranks.extend(heavensward_b_ranks)

        if self.has_stormblood:
            b_ranks.extend(stormblood_b_ranks)

        if self.has_shadowbringers:
            b_ranks.extend(shadowbringers_b_ranks)

        if self.has_endwalker:
            b_ranks.extend(endwalker_b_ranks)

        if self.has_dawntrail:
            b_ranks.extend(dawntrail_b_ranks)

        return sorted(b_ranks)
    
    def hunt_s_ranks(self) -> List[str]:
        s_ranks = [
            # Laideronnette excluded as it isn't spawned by players.
            # The Garlok excluded as it isn't spawned by players.
            "Nunyunuwi",
            "Agrippa the Mighty",
            "Mindflayer",
            "Bonnacon",
            "Safat",
            "Croakadile",
            "Croque-mitaine",
            "Wulgaru",
            "Lampalagua",
            "Brontes",
            "Thousand-cast Theda",
            "Zona Seeker",
            "Nandi",
            "Minhocao",
            "Chernobog",
        ]

        heavensward_s_ranks = [
            "The Pale Rider",
            "Gandarewa",
            "Leucrotta",
            "Senmurv",
            "Kaiser Behemoth",
            "Bird of Paradise",
        ]

        stormblood_s_ranks = [
            "Orghana",
            "Salt and Light",
            "Bone Crawler",
            "Okina",
            "Gamma",
            "Udumbara",
        ]

        shadowbringers_s_ranks = [
            "Aglaope",
            "Tarchia",
            "Tyger",
            "Ixtab",
            "Forgiven Pedantry",
            "Gunitt",
        ]

        endwalker_s_ranks = [
            "Sphatika",
            "Narrow-rift",
            "Ruminator",
            "Ophioneus",
            "Burfurlur the Canny",
            "Armstrong",
        ]

        dawntrail_s_ranks = [
            "Kirlirger the Abhorrent",
            "Neyoozoteel",
            "Inhuxokiy",
            "Atticus the Primogenitor",
            "The Forecaster",
            "Sansheya",
        ]

        if self.has_heavensward:
            s_ranks.extend(heavensward_s_ranks)

        if self.has_stormblood:
            s_ranks.extend(stormblood_s_ranks)

        if self.has_shadowbringers:
            s_ranks.extend(shadowbringers_s_ranks)

        if self.has_endwalker:
            s_ranks.extend(endwalker_s_ranks)

        if self.has_dawntrail:
            s_ranks.extend(dawntrail_s_ranks)

        return sorted(s_ranks)

    def jumping_puzzles(self) -> List[str]:
        jumping_puzzles = list()

        if self.has_heavensward:
            jumping_puzzles += ["The Firmament: Outer Towers"]

        if self.has_stormblood:
            jumping_puzzles += [
                "Kugane: Shiokaze Hostelry",
                "Kugane: Bokairo Inn",
                "Shirogane: Beach Lighthouse",
                "Rhalgr's Reach: Chakra Falls",
            ]
        
        if self.has_endwalker:
            jumping_puzzles += ["Radz-at-Han: Paksa's Path"]

        if self.has_dawntrail:
            jumping_puzzles += [
                "Tuliyollal: Pinion's Reach",
                "Tuliyollal: Hunu'iliy Tower",
            ]
        
        return sorted(jumping_puzzles)
    
    def dungeons(self) -> List[str]:
        dungeons = [
            "Sastasha",
            "The Tam-Tara Deepcroft",
            "Copperbell Mines",
            "Halatali",
            "The Thousand Maws of Toto-Rak",
            "Haukke Manor",
            "Brayflox's Longstop",
            "The Sunken Temple of Qarn",
            "Cutter's Cry",
            "The Stone Vigil",
            "Dzemael Darkhold",
            "The Aurum Vale",
            "The Wanderer's Palace",
            "Castrum Meridianum",
            "The Praetorium",
            "Amdapor Keep",
            "Pharos Sirius",
            "Copperbell Mines (Hard)",
            "Haukke Manor (Hard)",
            "The Lost City of Amdapor",
            "Halatali (Hard)",
            "Brayflox's Longstop (Hard)",
            "Hullbreaker Isle",
            "The Tam-Tara Deepcroft (Hard)",
            "The Stone Vigil (Hard)",
            "Snowcloak",
            "Sastasha (Hard)",
            "The Sunken Temple of Qarn (Hard)",
            "The Keeper of the Lake",
            "The Wanderer's Palace (Hard)",
            "Amdapor Keep (Hard)",
        ]

        heavensward_dungeons = [
            "The Dusk Vigil",
            "Sohm Al",
            "The Aery",
            "The Vault",
            "The Great Gubal Library",
            "The Aetherochemical Research Facility",
            "Neverreap",
            "The Fractal Continuum",
            "Saint Mocianne's Arboretum",
            "Pharos Sirius (Hard)",
            "The Antitower",
            "The Lost City of Amdapor (Hard)",
            "Sohr Khai",
            "Hullbreaker Isle (Hard)",
            "Xelphatol",
            "The Great Gubal Library (Hard)",
            "Baelsar's Wall",
            "Sohm Al (Hard)",
        ]

        stormblood_dungeons = [
            "The Sirensong Sea",
            "Shisui of the Violet Tides",
            "Bardam's Mettle",
            "Doma Castle",
            "Castrum Abania",
            "Ala Mhigo",
            "Kugane Castle",
            "The Temple of the Fist",
            "The Drowned City of Skalla",
            "Hells' Lid",
            "The Fractal Continuum (Hard)",
            "The Swallow's Compass",
            "The Burn",
            "Saint Mocianne's Arboretum (Hard)",
            "The Ghimlyt Dark",
        ]

        shadowbringers_dungeons = [
            "Holminster Switch",
            "Dohn Mheg",
            "The Qitana Ravel",
            "Malikah's Well",
            "Mt. Gulg",
            "Amaurot",
            "The Twinning",
            "Akadaemia Anyder",
            "The Grand Cosmos",
            "Anamnesis Anyder",
            "The Heroes' Gauntlet",
            "Matoya's Relict",
            "Paglth'an",
        ]

        endwalker_dungeons = [
            "The Tower of Zot",
            "The Tower of Babil",
            "Vanaspati",
            "Ktisis Hyperboreia",
            "The Aitiascope",
            "The Dead Ends",
            "Smileton",
            "The Stigma Dreamscape",
            "Alzadaal's Legacy",
            "The Fell Court of Troia",
            "Lapis Manalis",
            "The Aetherfont",
            "The Lunar Subterrane",
        ]

        dawntrail_dungeons = [
            "Ihuykatumu",
            "Worqor Zormor",
            "The Skydeep Cenote",
            "Vanguard",
            "Origenics",
            "Alexandria",
            "Tender Valley",
            "The Strayborough Deadwalk",
            "Yuweyawata Field Station",
        ]

        if self.has_heavensward:
            dungeons.extend(heavensward_dungeons)

        if self.has_stormblood:
            dungeons.extend(stormblood_dungeons)

        if self.has_shadowbringers:
            dungeons.extend(shadowbringers_dungeons)

        if self.has_endwalker:
            dungeons.extend(endwalker_dungeons)

        if self.has_dawntrail:
            dungeons.extend(dawntrail_dungeons)

        return sorted(dungeons)

    def trials(self) -> List[str]:
        trials = [
            "The Bowl of Embers",
            "The Navel",
            "The Howling Eye",
            "The Porta Decumana",
            "The Chrysalis",
            "A Relic Reborn: the Chimera",
            "A Relic Reborn: the Hydra",
            "Battle on the Big Bridge",
            "The Dragon's Neck",
            "Battle in the Big Keep",
            "The Bowl of Embers (Hard)",
            "The Howling Eye (Hard)",
            "The Navel (Hard)",
            "Thornmarch (Hard)",
            "The Whorleater (Hard)",
            "The Striking Tree (Hard)",
            "The Akh Afah Amphitheatre (Hard)",
            "Urth's Fount",
        ]

        heavensward_trials = [
            "Thok ast Thok (Hard)",
            "The Limitless Blue (Hard)",
            "The Singularity Reactor",
            "The Final Steps of Faith",
            "Containment Bay S1T7",
            "Containment Bay P1T6",
            "Containment Bay Z1T9",
        ]

        stormblood_trials = [
            "The Pool of Tribute",
            "Emanation",
            "The Royal Menagerie",
            "Castrum Fluminis",
            "Kugane Ohashi",
            "The Great Hunt",
            "The Jade Stoa",
            "Hells' Kier",
            "The Wreath of Snakes",
        ]

        shadowbringers_trials = [
            "The Dancing Plague",
            "The Crown of the Immaculate",
            "The Dying Gasp",
            "Cinder Drift",
            "The Seat of Sacrifice",
            "Castrum Marinum",
            "The Cloud Deck",
        ]

        endwalker_trials = [
            "The Dark Inside",
            "The Mothercrystal",
            "The Final Day",
            "Storm's Crown",
            "Mount Ordeals",
            "The Voidcast Dais",
            "The Abyssal Fracture",
            "The Gilded Araya",
        ]

        dawntrail_trials = [
            "Worqor Lar Dor",
            "Everkeep",
            "The Interphos",
        ]

        if self.has_heavensward:
            trials.extend(heavensward_trials)

        if self.has_stormblood:
            trials.extend(stormblood_trials)

        if self.has_shadowbringers:
            trials.extend(shadowbringers_trials)

        if self.has_endwalker:
            trials.extend(endwalker_trials)

        if self.has_dawntrail:
            trials.extend(dawntrail_trials)

        return sorted(trials)
    
    def extreme_trials(self) -> List[str]:
        extreme_trials = [
            "The Minstrel's Ballad: Ultima's Bane",
            "The Howling Eye (Extreme)",
            "The Navel (Extreme)",
            "The Bowl of Embers (Extreme)",
            "Thornmarch (Extreme)",
            "The Whorleater (Extreme)",
            "The Striking Tree (Extreme)",
            "The Akh Afah Amphitheatre (Extreme)",
        ]

        heavensward_extreme_trials = [
            "The Limitless Blue (Extreme)",
            "Thok ast Thok (Extreme)",
            "The Minstrel's Ballad: Thordan's Reign",
            "The Minstrel's Ballad: Nidhogg's Rage",
            "Containment Bay S1T7 (Extreme)",
            "Containment Bay P1T6 (Extreme)",
            "Containment Bay Z1T9 (Extreme)",
        ]

        stormblood_extreme_trials = [
            "The Pool of Tribute (Extreme)",
            "Emanation (Extreme)",
            "The Minstrel's Ballad: Shinryu's Domain",
            "The Minstrel's Ballad: Tsukuyomi's Pain",
            "The Great Hunt (Extreme)",
            "The Jade Stoa (Extreme)",
            "Hells' Kier (Extreme)",
            "The Wreath of Snakes (Extreme)",
        ]

        shadowbringers_extreme_trials = [
            "The Dancing Plague (Extreme)",
            "The Crown of the Immaculate (Extreme)",
            "The Minstrel's Ballad: Hades's Elegy",
            "Cinder Drift (Extreme)",
            "Memoria Misera (Extreme)",
            "The Seat of Sacrifice (Extreme)",
            "Castrum Marinum (Extreme)",
            "The Cloud Deck (Extreme)",
        ]

        endwalker_extreme_trials = [
            "The Minstrel's Ballad: Zodiark's Fall",
            "The Minstrel's Ballad: Hydaelyn's Call",
            "The Minstrel's Ballad: Endsinger's Aria",
            "Storm's Crown (Extreme)",
            "Mount Ordeals (Extreme)",
            "The Voidcast Dais (Extreme)",
            "The Abyssal Fracture (Extreme)",
        ]

        dawntrail_extreme_trials = [
            "Worqor Lar Dor (Extreme)",
            "Everkeep (Extreme)",
            "The Minstrel's Ballad: Sphene's Burden",
        ]

        if self.has_heavensward:
            extreme_trials.extend(heavensward_extreme_trials)

        if self.has_stormblood:
            extreme_trials.extend(stormblood_extreme_trials)

        if self.has_shadowbringers:
            extreme_trials.extend(shadowbringers_extreme_trials)

        if self.has_endwalker:
            extreme_trials.extend(endwalker_extreme_trials)

        if self.has_dawntrail:
            extreme_trials.extend(dawntrail_extreme_trials)

        return sorted(extreme_trials)

    def normal_raids(self) -> List[str]:
        normal_raids = [
            "The Binding Coil of Bahamut - Turn 1",
            "The Binding Coil of Bahamut - Turn 2",
            "The Binding Coil of Bahamut - Turn 3",
            "The Binding Coil of Bahamut - Turn 4",
            "The Binding Coil of Bahamut - Turn 5",
            "The Second Coil of Bahamut - Turn 1",
            "The Second Coil of Bahamut - Turn 2",
            "The Second Coil of Bahamut - Turn 3",
            "The Second Coil of Bahamut - Turn 4",
            "The Final Coil of Bahamut - Turn 1",
            "The Final Coil of Bahamut - Turn 2",
            "The Final Coil of Bahamut - Turn 3",
            "The Final Coil of Bahamut - Turn 4",
        ]

        heavensward_normal_raids = [
            "Alexander - The Fist of the Father",
            "Alexander - The Cuff of the Father",
            "Alexander - The Arm of the Father",
            "Alexander - The Burdern of the Father",
            "Alexander - The Fist of the Son",
            "Alexander - The Cuff of the Son",
            "Alexander - The Arm of the Son",
            "Alexander - The Burden of the Son",
            "Alexander - The Eyes of the Creator",
            "Alexander - The Breath of the Creator",
            "Alexander - The Heart of the Creator",
            "Alexander - The Soul of the Creator",
        ]

        stormblood_normal_raids = [
            "Deltascape V1.0",
            "Deltascape V2.0",
            "Deltascape V3.0",
            "Deltascape V4.0",
            "Sigmascape V1.0",
            "Sigmascape V2.0",
            "Sigmascape V3.0",
            "Sigmascape V4.0",
            "Alphascape V1.0",
            "Alphascape V2.0",
            "Alphascape V3.0",
            "Alphascape V4.0",
        ]

        shadowbringers_normal_raids = [
            "Eden's Gate: Resurrection",
            "Eden's Gate: Descent",
            "Eden's Gate: Inundation",
            "Eden's Gate: Sepulture",
            "Eden's Verse: Fulmination",
            "Eden's Verse: Furor",
            "Eden's Verse: Iconoclasm",
            "Eden's Verse: Refulgence",
            "Eden's Promise: Umbra",
            "Eden's Promise: Litany",
            "Eden's Promise: Anamorphosis",
            "Eden's Promise: Eternity",
        ]

        endwalker_normal_raids = [
            "Asphodelos: The First Circle",
            "Asphodelos: The Second Circle",
            "Asphodelos: The Third Circle",
            "Asphodelos: The Fourth Circle",
            "Abyssos: The Fifth Circle",
            "Abyssos: The Sixth Circle",
            "Abyssos: The Seventh Circle",
            "Abyssos: The Eighth Circle",
            "Anabaseios: The Ninth Circle",
            "Anabaseios: The Tenth Circle",
            "Anabaseios: The Eleventh Circle",
            "Anabaseios: The Twelfth Circle",
        ]

        dawntrail_normal_raids = [
            "AAC Light-heavyweight M1",
            "AAC Light-heavyweight M2",
            "AAC Light-heavyweight M3",
            "AAC Light-heavyweight M4",
        ]
        
        if self.has_heavensward:
            normal_raids.extend(heavensward_normal_raids)

        if self.has_stormblood:
            normal_raids.extend(stormblood_normal_raids)

        if self.has_shadowbringers:
            normal_raids.extend(shadowbringers_normal_raids)

        if self.has_endwalker:
            normal_raids.extend(endwalker_normal_raids)

        if self.has_dawntrail:
            normal_raids.extend(dawntrail_normal_raids)

        return sorted(normal_raids)
    
    def savage_raids(self) -> List[str]:
        savage_raids = [
            "The Second Coil of Bahamut (Savage) - Turn 1",
            "The Second Coil of Bahamut (Savage) - Turn 2",
            "The Second Coil of Bahamut (Savage) - Turn 3",
            "The Second Coil of Bahamut (Savage) - Turn 4",
        ]

        heavensward_savage_raids = [
            "Alexander - The Fist of the Father (Savage)",
            "Alexander - The Cuff of the Father (Savage)",
            "Alexander - The Arm of the Father (Savage)",
            "Alexander - The Burdern of the Father (Savage)",
            "Alexander - The Fist of the Son (Savage)",
            "Alexander - The Cuff of the Son (Savage)",
            "Alexander - The Arm of the Son (Savage)",
            "Alexander - The Burden of the Son (Savage)",
            "Alexander - The Eyes of the Creator (Savage)",
            "Alexander - The Breath of the Creator (Savage)",
            "Alexander - The Heart of the Creator (Savage)",
            "Alexander - The Soul of the Creator (Savage)",
        ]

        stormblood_savage_raids = [
            "Deltascape V1.0 (Savage)",
            "Deltascape V2.0 (Savage)",
            "Deltascape V3.0 (Savage)",
            "Deltascape V4.0 (Savage)",
            "Sigmascape V1.0 (Savage)",
            "Sigmascape V2.0 (Savage)",
            "Sigmascape V3.0 (Savage)",
            "Sigmascape V4.0 (Savage)",
            "Alphascape V1.0 (Savage)",
            "Alphascape V2.0 (Savage)",
            "Alphascape V3.0 (Savage)",
            "Alphascape V4.0 (Savage)",
        ]

        shadowbringers_savage_raids = [
            "Eden's Gate: Resurrection (Savage)",
            "Eden's Gate: Descent (Savage)",
            "Eden's Gate: Inundation (Savage)",
            "Eden's Gate: Sepulture (Savage)",
            "Eden's Verse: Fulmination (Savage)",
            "Eden's Verse: Furor (Savage)",
            "Eden's Verse: Iconoclasm (Savage)",
            "Eden's Verse: Refulgence (Savage)",
            "Eden's Promise: Umbra (Savage)",
            "Eden's Promise: Litany (Savage)",
            "Eden's Promise: Anamorphosis (Savage)",
            "Eden's Promise: Eternity (Savage)",
        ]

        endwalker_savage_raids = [
            "Asphodelos: The First Circle (Savage)",
            "Asphodelos: The Second Circle (Savage)",
            "Asphodelos: The Third Circle (Savage)",
            "Asphodelos: The Fourth Circle (Savage)",
            "Abyssos: The Fifth Circle (Savage)",
            "Abyssos: The Sixth Circle (Savage)",
            "Abyssos: The Seventh Circle (Savage)",
            "Abyssos: The Eighth Circle (Savage)",
            "Anabaseios: The Ninth Circle (Savage)",
            "Anabaseios: The Tenth Circle (Savage)",
            "Anabaseios: The Eleventh Circle (Savage)",
            "Anabaseios: The Twelfth Circle (Savage)",
        ]

        dawntrail_savage_raids = [
            "AAC Light-heavyweight M1 (Savage)",
            "AAC Light-heavyweight M2 (Savage)",
            "AAC Light-heavyweight M3 (Savage)",
            "AAC Light-heavyweight M4 (Savage)",
        ]
        
        if self.has_heavensward:
            savage_raids.extend(heavensward_savage_raids)

        if self.has_stormblood:
            savage_raids.extend(stormblood_savage_raids)

        if self.has_shadowbringers:
            savage_raids.extend(shadowbringers_savage_raids)

        if self.has_endwalker:
            savage_raids.extend(endwalker_savage_raids)

        if self.has_dawntrail:
            savage_raids.extend(dawntrail_savage_raids)

        return sorted(savage_raids)

    def alliance_raids(self) -> List[str]:
        alliance_raids = [
            "The Labyrinth of the Ancients",
            "Syrcus Tower",
            "The World of Darkness",
        ]

        heavensward_alliance_raids = [
            "The Void Ark",
            "The Weeping City of Mhach",
            "Dun Scaith",
        ]

        stormblood_alliance_raids = [
            "The Royal City of Rabanastre",
            "The Ridorana Lighthouse",
            "The Orbonne Monastery",
        ]

        shadowbringers_alliance_raids = [
            "The Copied Factory",
            "The Puppets' Bunker",
            "The Tower at Paradigm's Breach",
        ]

        endwalker_alliance_raids = [
            "Aglaia",
            "Euphrosyne",
            "Thaleia",
        ]

        dawntrail_alliance_raids = [
            "Jeuno: The First Walk",
        ]

        if self.has_heavensward:
            alliance_raids.extend(heavensward_alliance_raids)

        if self.has_stormblood:
            alliance_raids.extend(stormblood_alliance_raids)

        if self.has_shadowbringers:
            alliance_raids.extend(shadowbringers_alliance_raids)

        if self.has_endwalker:
            alliance_raids.extend(endwalker_alliance_raids)

        if self.has_dawntrail:
            alliance_raids.extend(dawntrail_alliance_raids)

        return sorted(alliance_raids)
    
    def chaotic_alliance_raids(self) -> List[str]:
        chaotic_alliance_raids = list()

        dawntrail_chaotic_alliance_raids = [
            "The Cloud of Darkness (Chaotic)",
        ]

        if self.has_dawntrail:
            chaotic_alliance_raids.extend(dawntrail_chaotic_alliance_raids)

        return sorted(chaotic_alliance_raids)

    @staticmethod
    def deep_dungeon_floor_range() -> range:
        return range(1,4)

    @staticmethod
    def deep_dungeon_hoard_count() -> range:
        return range(1,4)

    @staticmethod
    def deep_dungeon_kill_count() -> range:
        return range(35,61)

    def deep_dungeons(self) -> List[str]:
        deep_dungeons = ["Palace of the Dead"]

        if self.has_stormblood:
            deep_dungeons += ["Heaven-on-High"]

        if self.has_endwalker:
            deep_dungeons += ["Eureka Orthos"]

        return sorted(deep_dungeons)
    
    def variant_dungeon_routes(self) -> List[str]:
        routes = list()

        if self.has_endwalker:
            routes += [
                "Sil'dihn Subterrane: Whom the Silkie Serves",
                "Sil'dihn Subterrane: Pride and Acceptance",
                "Sil'dihn Subterrane: A Spot in the Sunlight",
                "Sil'dihn Subterrane: A Key Memory",
                "Sil'dihn Subterrane: In Father's Stead",
                "Sil'dihn Subterrane: Ul'dah's Sin to Bear",
                "Sil'dihn Subterrane: To Learn More of Myrrh",
                "Sil'dihn Subterrane: Ul'dah and Sil'dih",
                "Sil'dihn Subterrane: Raising the Flags",
                "Sil'dihn Subterrane: My Mother's Eyes",
                "Sil'dihn Subterrane: The Thorne Legacy",
                "Sil'dihn Subterrane: In Parchment We Trust",
                "Mount Rokkon: Gift of the Onmyoji",
                "Mount Rokkon: The Crimson Sword",
                "Mount Rokkon: A Tale of Dead Men",
                "Mount Rokkon: Forging a Legacy",
                "Mount Rokkon: The Luthier and the Songstress",
                "Mount Rokkon: Lost to Avarice",
                "Mount Rokkon: Beyond the Lanterns' Light",
                "Mount Rokkon: The Common Man's Courage",
                "Mount Rokkon: Sound of the Stone",
                "Mount Rokkon: The Seal of Silence",
                "Mount Rokkon: Seasons of the Fleeting",
                "Mount Rokkon: The Ogiseru's Fate",
                "Aloalo Island: A Not-quite Deserted Island",
                "Aloalo Island: The First Settlers of Aloalo Island",
                "Aloalo Island: God of Heaven and Sea",
                "Aloalo Island: A Noxious Gift",
                "Aloalo Island: The Roots of Arcanima",
                "Aloalo Island: Under the Boughs of the Great Tree",
                "Aloalo Island: A Dear Friend",
                "Aloalo Island: Fish for the Mind",
                "Aloalo Island: A Familiar History",
                "Aloalo Island: The Remnants of Faith",
                "Aloalo Island: A Lalafell or a Fish?",
                "Aloalo Island: Wellspring of Golden Memories",
            ]
        
        return sorted(routes)

    @staticmethod
    def eureka_nm_fates() -> List[str]:
        return [
            "Anemos: Unsafety Dance",
            "Anemos: The Shadow over Anemos",
            "Anemos: Teles House",
            "Anemos: The Swarm Never Sets",
            "Anemos: One Missed Callisto",
            "Anemos: By Numbers",
            "Anemos: Disinherit the Wind",
            "Anemos: Prove Your Amemettle",
            "Anemos: Caym What May",
            "Anemos: The Killing of a Sacred Bombadier",
            "Anemos: Short Serket 2",
            "Anemos: Don't Judge Me, Morbol",
            "Anemos: When You Ride Alone",
            "Anemos: Sing, Muse",
            "Anemos: Simurghasbord",
            "Anemos: To the Mat",
            "Anemos: Wine and Honey",
            "Anemos: I Amarok",
            "Anemos: Drama Lamashtu",
            "Anemos: Wail in the Willows",
            "Pagos: Eternity",
            "Pagos: Cairn Blight 451",
            "Pagos: Ash the Magic Dragon",
            "Pagos: Conqueror Worm",
            "Pagos: Melting Point",
            "Pagos: The Wobbler in Darkness",
            "Pagos: Does It Have to Be a Snowman",
            "Pagos: Disorder in the Court",
            "Pagos: Cows for Concern",
            "Pagos: Morte Arthro",
            "Pagos: Brothers",
            "Pagos: Apocalypse Cow",
            "Pagos: Third Impact",
            "Pagos: Eye of Horus",
            "Pagos: Eye Scream for Ice Cream",
            "Pagos: Cassie and the Copycats",
            "Pagos: Louhi on Ice",
            "Pyros: Medias Res",
            "Pyros: High Voltage",
            "Pyros: On the Non-existent",
            "Pyros: Creepy Doll",
            "Pyros: Quiet, Please",
            "Pyros: Up and Batym",
            "Pyros: Rondo Aetolus",
            "Pyros: Scorchpion King",
            "Pyros: Burning Hunger",
            "Pyros: Dry Iris",
            "Pyros: Thirty Whacks",
            "Pyros: Put Up Your Dux",
            "Pyros: You Do Know Jack",
            "Pyros: Mister Bright-eyes",
            "Pyros: Haunter of the Dark",
            "Pyros: Heavens' Warg",
            "Pyros: Lost Epic",
            "Hydatos: I Ink, Therefore I Am",
            "Hydatos: From Tusk till Dawn",
            "Hydatos: Bullheaded Berserker",
            "Hydatos: Mad, Bad, and Fabulous to Know",
            "Hydatos: Fearful Symmetry",
            "Hydatos: Crawling Chaos",
            "Hydatos: Duty-free",
            "Hydatos: Leukewarm Reception",
            "Hydatos: Robber Barong",
            "Hydatos: Stone-cold Killer",
            "Hydatos: Crystalline Provenance",
            "Hydatos: I Don't Want to Believe",
            #"Hydatos: The Baldesion Arsenal: Expedition Support" # Excluded so as not to grief BA parties.
        ]
    
    @staticmethod
    def eureka_bunny_fates() -> List[str]:
        return [
            "Pagos: Down the Rabbit Hole",
            "Pagos: Curiouser and Curiouser",
            "Pyros: We're All Mad Here",
            "Pyros: Uncommon Nonsense",
            "Hydatos: Drink Me",
        ]

    @staticmethod
    def eureka_bunny_coffers() -> List[str]:
        return [
            "Bronze",
            "Silver",
            "Gold",
        ]

    @staticmethod
    def bozja_fates() -> List[str]:
        return [
            "the Bozjan Southern Front: All Pets Are Off",
            "the Bozjan Southern Front: Brought to Heal",
            "the Bozjan Southern Front: Can Carnivorous Plants Bloom Even on a Battlefield?",
            "the Bozjan Southern Front: Conflicting with the First Law",
            "the Bozjan Southern Front: More Machine Now than Man",
            "the Bozjan Southern Front: None of Them Knew They Were Robots",
            "the Bozjan Southern Front: Seeq and Destroy",
            "the Bozjan Southern Front: Sneak and Spell",
            "the Bozjan Southern Front: The Beasts Must Die",
            "the Bozjan Southern Front: Unrest for the Wicked",
            "the Bozjan Southern Front: Heavy Boots of Lead",
            "the Bozjan Southern Front: Help Wanted",
            "the Bozjan Southern Front: No Camping Allowed",
            "the Bozjan Southern Front: Parts and Recreation",
            "the Bozjan Southern Front: Pyromancer Supreme",
            "the Bozjan Southern Front: Red (Chocobo) Alert",
            "the Bozjan Southern Front: Scavengers of Man's Sorrow",
            "the Bozjan Southern Front: The Element of Supplies",
            "the Bozjan Southern Front: The Monster Mash",
            "the Bozjan Southern Front: Unicorn Flakes",
            "the Bozjan Southern Front: Demonstrably Demonic",
            "the Bozjan Southern Front: Desperately Seeking Something",
            "the Bozjan Southern Front: For Absent Friends",
            "the Bozjan Southern Front: I'm a Mechanical Man",
            "the Bozjan Southern Front: Let Slip the Dogs of War",
            "the Bozjan Southern Front: Murder Death Kill",
            "the Bozjan Southern Front: My Family and Other Animals",
            "the Bozjan Southern Front: Of Steel and Flame",
            "the Bozjan Southern Front: Supplies Party",
            "the Bozjan Southern Front: The War Against the Machines",
            "the Bozjan Southern Front: The Wild Bunch",
            "the Bozjan Southern Front: Waste the Rainbow",
            "Zadnor: A Wrench in the Reconnaissance Effort",
            "Zadnor: An Immoral Dilemma",
            "Zadnor: Another Pilot Episode",
            "Zadnor: Breaking the Ice",
            "Zadnor: Deadly Divination",
            "Zadnor: Meet the Puppetmaster",
            "Zadnor: Of Beasts and Braggadocio",
            "Zadnor: Parts and Parcel",
            "Zadnor: A Just Pursuit",
            "Zadnor: An End to Atrocities",
            "Zadnor: Challenge Accepted",
            "Zadnor: Demented Mentor",
            "Zadnor: Sever the Strings",
            "Zadnor: Supersoldier Rising",
            "Zadnor: Tanking Up",
            "Zadnor: Th'uban the Terrible",
            "Zadnor: A Relic Unleashed",
            "Zadnor: Attack of the Machines",
            "Zadnor: Attack of the Supersoldiers",
            "Zadnor: Hypertuned Havoc",
            "Zadnor: Mean-spirited",
            "Zadnor: Seeq and You Will Find",
            "Zadnor: Still Only Counts as One",
            "Zadnor: The Beasts Are Back",
            "Zadnor: The Student Becalms the Master",
            "Zadnor: When Mages Rage",
        ]
    
    @staticmethod
    def bozja_ce_fates() -> List[str]:
        return [
            "the Bozjan Southern Front: Kill It with Fire",
            "the Bozjan Southern Front: The Baying of the Hound(s)",
            "the Bozjan Southern Front: The Shadow of Death's Hand",
            "the Bozjan Southern Front: Vigil for the Lost",
            "the Bozjan Southern Front: Patriot Games",
            "the Bozjan Southern Front: The Final Furlong",
            "the Bozjan Southern Front: The Fires of War",
            "the Bozjan Southern Front: The Hunt for Red Choctober",
            "the Bozjan Southern Front: Metal Fox Chaos",
            "the Bozjan Southern Front: Rise of the Robots",
            "the Bozjan Southern Front: Trampled under Hoof",
            "the Bozjan Southern Front: Where Strode the Behemoth",
            "Zadnor: A Familiar Face",
            "Zadnor: From Beyond the Grave",
            "Zadnor: On Serpents' Wings",
            "Zadnor: With Diremite and Main",
            "Zadnor: Here Comes the Cavalry",
            "Zadnor: Never Cry Wolf",
            "Zadnor: There Would Be Blood",
            "Zadnor: Time to Burn",
            "Zadnor: Feeling the Burn",
            "Zadnor: Lean, Mean, Magitek Machines",
            "Zadnor: Looks to Die For",
            "Zadnor: Worn to a Shadow",
        ]
    
    @staticmethod
    def bozja_duel_fates() -> List[str]:
        return [
            "the Bozjan Southern Front: Aces High",
            "the Bozjan Southern Front: Beast of Man",
            "the Bozjan Southern Front: And the Flames Went Higher",
            "Zadnor: The Broken Blade",
            "Zadnor: Head of the Snake",
            "Zadnor: Taking the Lyon's Share",
        ]

    @staticmethod
    def masked_carnivale_range() -> range:
        return range(1,4)
    
    @staticmethod
    def masked_carnivale_weekly_targets() -> List[str]:
        return [
            "Novice",
            "Moderate",
            "Advanced",
        ]

    @staticmethod
    def masked_carnivale_completion_times() -> List[str]:
        return [
            "Standard",
            "Ideal",
        ]

    def masked_carnivale(self) -> List[str]:
        masked_carnivale = [
            "All's Well That Starts Well",
            "Much Ado About Pudding",
            "Waiting for Golem",
            "Gentlemen Prefer Swords",
            "The Threepenny Turtles",
            "Eye Society",
            "A Chorus Slime",
            "Bomb-edy of Errors",
            "To Kill a Mockingslime",
            "A Little Knight Music",
            "Some Like It Excruciatingly Hot",
            "The Plant-om of the Opera",
            "Beauty and a Beast",
            "Blobs in the Woods",
            "The Me Nobody Nodes",
            "Sunset Bull-evard",
            "The Sword of Music",
            "Midsummer Night's Explosion",
            "On a Clear Day You Can Smell Forever",
            "Miss Typhon",
            "Chimera on a Hot Tin Roof",
            "Here Comes the Boom",
            "Behemoths and Broomsticks",
            "Amazing Technicolor Pit Fiends",
            "Dirty Rotten Azulmagia",
        ]

        heavensward_masked_carnivale = [
            "Papa Mia",
            "Lock up Your Snorters",
            "Dangerous When Dead",
            "Red, Fraught, and Blue",
            "The Catch of the Siegfried",
        ]

        stormblood_masked_carnivale = [
            "Anything Gogo's",
        ]

        shadowbringers_masked_carnivale = [
            "A Golden Opportunity",
        ]

        if self.has_level_60_or_higher:
            masked_carnivale.extend(heavensward_masked_carnivale)

        if self.has_level_70_or_higher:
            masked_carnivale.extend(stormblood_masked_carnivale)

        if self.has_level_80_or_higher:
            masked_carnivale.extend(shadowbringers_masked_carnivale)

        return sorted(masked_carnivale)
    
    @staticmethod
    def gathering_collectables_count_range() -> range:
        return range(3,13)
    
    def gathering_collectables(self) -> List[str]:
        gathering_collectables = list()

        heavensward_mining_collectables = [
            "Rarefied Mythrite Sand",
            "Rarefied Pyrite",
            "Rarefied Chalcocite",
            "Rarefied Limonite",
            "Rarefied Abalathian Spring Water",
            "Rarefied Aurum Regis Sand",
        ]

        heavensward_botany_collectables = [
            "Rarefied Rainbow Cotton Boll",
            "Rarefied Dark Chestnut Sap",
            "Rarefied Dark Chestnut Log",
            "Rarefied Dark Chestnut Branch",
            "Rarefied Dark Chestnut",
            "Rarefied Dark Chestnut Resin",
        ]

        stormblood_mining_collectables = [
            "Rarefied Gyr Abanian Mineral Water",
            "Rarefied Raw Triphane",
            "Rarefied Raw Star Spinel",
            "Rarefied Raw Kyanite",
            "Rarefied Raw Azurite",
            "Rarefied Silvergrace Ore",
        ]

        stormblood_botany_collectables = [
            "Rarefied Bloodhemp",
            "Rarefied Larch Log",
            "Rarefied Shiitake Mushroom",
            "Rarefied Larch Sap",
            "Rarefied Pine Resin",
            "Rarefied Pine Log",
        ]

        shadowbringers_mining_collectables = [
            "Rarefied Bluespirit Ore",
            "Rarefied Titancopper Ore",
            "Rarefied Raw Lazurite",
            "Rarefied Raw Petalite",
            "Rarefied Sea Salt",
            "Rarefied Reef Rock",
            "Rarefied Manasilver Sand",
            "Rarefied Raw Onyx",
            "Rarefied Gyr Abanian Alumen",
            "Rarefied Tungsten Ore",
        ]

        shadowbringers_botany_collectables = [
            "Rarefied Bright Flax",
            "Rarefied Pixie Apple",
            "Rarefied White Oak Log",
            "Rarefied Miracle Apple Log",
            "Rarefied Sandteak Log",
            "Rarefied Kelp",
            "Rarefied Night Pepper",
            "Rarefied Amber Cloves",
            "Rarefied Urunday Log",
            "Rarefied Coral",
        ]

        endwalker_mining_collectables = [
            "Rarefied Raw Ametrine",
            "Rarefied High Durium Ore",
            "Rarefied Bismuth Ore",
            "Rarefied Sharlayan Rock Salt",
            "Rarefied Phrygian Gold Ore",
            "Rarefied Blue Zircon",
            "Rarefied Eblan Alumen",
            "Rarefied Chloroschist",
            "Rarefied Pewter Ore",
            "Rarefied Annite",
        ]

        endwalker_botany_collectables = [
            "Rarefied Palm Log",
            "Rarefied Thavnairian Perilla Leaf",
            "Rarefied Red Pine Log",
            "Rarefied Coconut",
            "Rarefied Sykon",
            "Rarefied Dark Rye",
            "Rarefied Elder Nutmeg",
            "Rarefied Ironwood Log",
            "Rarefied AR-Caean Cotton Boll",
            "Rarefied Iceberg Lettuce",
        ]

        dawntrail_mining_collectables = [
            "Rarefied Raw Ihuykanite",
            "Rarefied Raw Dark Amber",
            "Rarefied Titanium Gold Ore",
            "Rarefied White Gold Ore",
            "Rarefied Magnesite Ore",
            "Rarefied Artificial Volcanic Rock",
            "Rarefied Ash Soil",
            "Rarefied Ra'Kaznar Ore",
        ]

        dawntrail_botany_collectables = [
            "Rarefied Kozama'uka Chamomile",
            "Rarefied Mountain Flax",
            "Rarefied Sweet Kukuru Bean",
            "Rarefied Acacia Bark",
            "Rarefied Dark Mahogany Log",
            "Rarefied Wild Agave",
            "Rarefied Windsbalm Bay Leaf",
            "Rarefied Acacia Log",
        ]

        if self.has_heavensward:
            if "Miner" in self.playable_jobs:
                gathering_collectables.extend(heavensward_mining_collectables)

            if "Botanist" in self.playable_jobs:
                gathering_collectables.extend(heavensward_botany_collectables)

        if self.has_stormblood:
            if "Miner" in self.playable_jobs:
                gathering_collectables.extend(stormblood_mining_collectables)

            if "Botanist" in self.playable_jobs:
                gathering_collectables.extend(stormblood_botany_collectables)

        if self.has_shadowbringers:
            if "Miner" in self.playable_jobs:
                gathering_collectables.extend(shadowbringers_mining_collectables)

            if "Botanist" in self.playable_jobs:
                gathering_collectables.extend(shadowbringers_botany_collectables)

        if self.has_endwalker:
            if "Miner" in self.playable_jobs:
                gathering_collectables.extend(endwalker_mining_collectables)

            if "Botanist" in self.playable_jobs:
                gathering_collectables.extend(endwalker_botany_collectables)

        if self.has_dawntrail:
            if "Miner" in self.playable_jobs:
                gathering_collectables.extend(dawntrail_mining_collectables)

            if "Botanist" in self.playable_jobs:
                gathering_collectables.extend(dawntrail_botany_collectables)

        return sorted(gathering_collectables)
    
    @staticmethod
    def firmament_gathering_collectables_count_range() -> range:
        return range(12,25)

    def firmament_gathering_collectables(self) -> List[str]:
        firmament_gathering_collectables = list()

        miner_collectables = [
            "Grade 4 Skybuilders' Iron Ore",
            "Grade 4 Skybuilders' Iron Sand",
            "Grade 4 Skybuilders' Ore",
            "Grade 4 Skybuilders' Rock Salt",
            "Grade 4 Skybuilders' Mythrite Sand",
            "Grade 4 Skybuilders' Electrum Ore",
            "Grade 4 Skybuilders' Alumen",
            "Grade 4 Skybuilders' Spring Water",
            "Grade 4 Skybuilders' Gold Sand",
            "Grade 4 Skybuilders' Ragstone",
        ]

        miner_lv80_collectables = [
            "Grade 4 Skybuilders' Gold Ore",
            "Grade 4 Skybuilders' Finest Rock Salt",
            "Grade 4 Skybuilders' Truespring Water",
            "Grade 4 Skybuilders' Mineral Sand",
            "Grade 4 Skybuilders' Bluespirit Ore",
        ]

        botanist_collectables = [
            "Grade 4 Skybuilders' Switch",
            "Grade 4 Skybuilders' Hemp",
            "Grade 4 Skybuilders' Mahogany Log",
            "Grade 4 Skybuilders' Sesame",
            "Grade 4 Skybuilders' Cotton Boll",
            "Grade 4 Skybuilders' Spruce Log",
            "Grade 4 Skybuilders' Mistletoe",
            "Grade 4 Skybuilders' Toad",
            "Grade 4 Skybuilders' Vine",
            "Grade 4 Skybuilders' Tea Leaves",
        ]

        botanist_lv80_collectables = [
            "Grade 4 Skybuilders' White Cedar Log",
            "Grade 4 Skybuilders' Primordial Resin",
            "Grade 4 Skybuilders' Wheat",
            "Grade 4 Skybuilders' Gossamer Cotton Boll",
            "Grade 4 Skybuilders' Tortoise",
        ]

        if self.has_level_80_or_higher:
            miner_collectables.extend(miner_lv80_collectables)
            botanist_collectables.extend(botanist_lv80_collectables)

        if self.has_heavensward:
            if "Miner" in self.playable_jobs:
                firmament_gathering_collectables.extend(miner_collectables)

            if "Botanist" in self.playable_jobs:
                firmament_gathering_collectables.extend(botanist_collectables)

        return sorted(firmament_gathering_collectables)

    def firmament_high_tier_gathering_collectables(self) -> List[str]:
        firmament_high_tier_gathering_collectables = list()

        high_tier_miner_collectables = [
            "Grade 4 Artisanal Skybuilders' Cloudstone",
            "Grade 4 Artisanal Skybuilders' Spring Water",
            "Grade 4 Artisanal Skybuilders' Ice Stalagmite",
            "Grade 4 Artisanal Skybuilders' Silex",
            "Grade 4 Artisanal Skybuilders' Prismstone",
            "Grade 4 Skybuilders' Umbral Flarerock",
            "Grade 4 Skybuilders' Umbral Levinsand",
        ]

        high_tier_botanist_collectables = [
            "Grade 4 Artisanal Skybuilders' Log",
            "Grade 4 Artisanal Skybuilders' Raspberry",
            "Grade 4 Artisanal Skybuilders' Caiman",
            "Grade 4 Artisanal Skybuilders' Cocoon",
            "Grade 4 Artisanal Skybuilders' Barbgrass",
            "Grade 4 Skybuilders' Umbral Galewood Branch",
            "Grade 4 Skybuilders' Umbral Dirtleaf",
        ]

        if self.has_heavensward and self.has_level_80_or_higher:
            if "Miner" in self.playable_jobs:
                firmament_high_tier_gathering_collectables.extend(high_tier_miner_collectables)

            if "Botanist" in self.playable_jobs:
                firmament_high_tier_gathering_collectables.extend(high_tier_botanist_collectables)

        return sorted(firmament_high_tier_gathering_collectables)

    @staticmethod
    def diadem_enemies() -> List[str]:
        return [
            "Diadem Beast",
            "Diadem Golem",
            "Diadem Ice Bomb",
            "Diadem Zoblyn",
            "Diadem Bloated Bulb",
            "Diadem Icetrap",
            "Diadem Melia",
            "Diadem Werewood",
            "Proto-noctilucale",
        ]

    @staticmethod
    def fishing_collectables_count_range() -> range:
        return range(3,13)
    
    def fishing_collectables(self) -> List[str]:
        fishing_collectables = list()

        heavensward_fishing_collectables = [
            "Icepick",
            "Noontide Oscar",
            "Weston Bowfin",
            "Illuminati Perch",
            "Moogle Spirit",
            "Dravanian Smelt",
            "Vampiric Tapestry",
            "Stupendemys",
        ]

        heavensward_timed_fishing_collectables = [
            "Glacier Core", # Weather
            "Whilom Catfish", # Weather
            "Sorcerer Fish", # Time
            "Bubble Eye", # Time
            "Dravanian Squeaker", # Time
            "Warmwater Bichir", # Time
            "Thunderbolt Eel", # Time
            "Tiny Axolotl", # Time
            "Capelin", # Time
            "Loosetongue", # Time
            "Barreleye", # Weather
            "Amber Salamander", # Time
        ]

        heavensward_unreasonable_fishing_collectables = []

        stormblood_fishing_collectables = [
            "Velodyna Grass Carp",
            "Butterfly Fish",
            "Yanxian Koi",
            "Mitsukuri Shark",
            "Silken Sunfish",
            "Eternal Eye",
            "Cherubfish",
            "Mosasaur",
            "Soul of the Stallion",
            "Fangshi",
            "Thousandfang",
            "Tao Bitterling",
            "Samurai Fish",
            "Daio Squid",
            "Ala Mhigan Ribbon",
        ]

        stormblood_timed_fishing_collectables = [
            "Killifish", # Weather
            "Seraphim", # Time
            "Deemster", # Weather
            "Silken Koi", # Weather
        ]

        stormblood_unreasonable_fishing_collectables = [
            "Wraithfish", # Time + Weather
            "Swordfish", # Time + Weather
            "Sculptor", # Time + Weather
            "Hak Bitterling", # Time + Weather
        ]

        shadowbringers_fishing_collectables = [
            "Albino Caiman",
            "Little Bismarck",
            "Bothriolepis",
            "Weedy Seadragon",
            "Golden Lobster",
            "Rak'tika Goby",
            "Elder Pixie",
            "Viis Ear",
            "Blue Mountain Bubble",
            "Eryops",
            "Winged Hatchetfish",
            "Pancake Octopus",
            "Ondo Harpoon",
        ]

        shadowbringers_timed_fishing_collectables = [
            "Diamond Pipira", # Time
            "Toadhead", # Weather
            "Platinum Guppy", # Weather
        ]

        shadowbringers_unreasonable_fishing_collectables = [
            "Aapoak", # Time + Weather
            "Darkdweller", # Time + Weather
            "Thorned Lizard", # Time + Weather
            "Henodus", # Time + Weather
        ]

        endwalker_fishing_collectables = [
            "Topminnow",
            "Othardian Wrasse",
            "Shogun's Kabuto",
            "Pipefish",
            "Seema Duta",
            "Pantherscale Grouper",
            "Xiphactinus",
            "Kitefin Shark",
            "Tebqeyiq Smelt",
            "Fleeting Brand",
            "Forgeflame",
            "Banana Eel",
            "Echinos",
            "Foun Myhk",
        ]

        endwalker_timed_fishing_collectables = [
            "Phallaina", # Time
            "Mangar", # Weather
            "Lunar Deathworm", # Weather
            "Basilosaurus", # Weather
        ]

        endwalker_unreasonable_fishing_collectables = [
            "Red Drum", # Time + Weather
            "Labyrinthos Tilapia", # Time + Weather
        ]

        dawntrail_fishing_collectables = [
            "Zorlortor",
            "Purussaurus",
            "Piraputanga",
            "Plattershell",
            "Mirror Carp",
            "Glittergill",
            "Moxutural Gar",
            "Toari Sucker",
            "Wivre Cod",
            "Iq Rrax Crab",
            "Goldgrouper",
            "Zorgor Condor",
            "Hydro Louvar",
            "Cloud Wasp",
        ]

        dawntrail_timed_fishing_collectables = [
            "Copper Shark", # Weather
            "Chain Shark", # Time
            "Yellow Peacock Bass", # Time
            "Urqofrog", # Time
        ]

        dawntrail_unreasonable_fishing_collectables = []

        if self.has_heavensward:
            fishing_collectables.extend(heavensward_fishing_collectables)
            
            if self.include_time_consuming_objectives:
                fishing_collectables.extend(heavensward_timed_fishing_collectables)

            if self.unreasonable_tasks_enabled:
                fishing_collectables.extend(heavensward_unreasonable_fishing_collectables)

        if self.has_stormblood:
            fishing_collectables.extend(stormblood_fishing_collectables)

            if self.include_time_consuming_objectives:
                fishing_collectables.extend(stormblood_timed_fishing_collectables)

            if self.unreasonable_tasks_enabled:
                fishing_collectables.extend(stormblood_unreasonable_fishing_collectables)

        if self.has_shadowbringers:
            fishing_collectables.extend(shadowbringers_fishing_collectables)

            if self.include_time_consuming_objectives:
                fishing_collectables.extend(shadowbringers_timed_fishing_collectables)

            if self.unreasonable_tasks_enabled:
                fishing_collectables.extend(shadowbringers_unreasonable_fishing_collectables)

        if self.has_endwalker:
            fishing_collectables.extend(endwalker_fishing_collectables)

            if self.include_time_consuming_objectives:
                fishing_collectables.extend(endwalker_timed_fishing_collectables)

            if self.unreasonable_tasks_enabled:
                fishing_collectables.extend(endwalker_unreasonable_fishing_collectables)

        if self.has_dawntrail:
            fishing_collectables.extend(dawntrail_fishing_collectables)

            if self.include_time_consuming_objectives:
                fishing_collectables.extend(dawntrail_timed_fishing_collectables)

            if self.unreasonable_tasks_enabled:
                fishing_collectables.extend(dawntrail_unreasonable_fishing_collectables)

        return sorted(fishing_collectables)

    @staticmethod
    def firmament_fishing_collectables_count_range() -> range:
        return range(3,7)

    def firmament_fishing_collectables(self) -> List[str]:
        firmament_fishing_collectables = list()

        fisher_collectables = [
            "Grade 4 Skybuilders' Zagas Khaal",
            "Grade 4 Skybuilders' Goldsmith Crab",
            "Grade 4 Skybuilders' Common Bitterling",
            "Grade 4 Skybuilders' Skyloach",
            "Grade 4 Skybuilders' Glacier Core",
            "Grade 4 Skybuilders' Kissing Fish",
            "Grade 4 Skybuilders' Cavalry Catfish",
            "Grade 4 Skybuilders' Manasail",
            "Grade 4 Skybuilders' Starflower",
            "Grade 4 Skybuilders' Cyan Crab",
            "Grade 4 Skybuilders' Fickle Krait",
            "Grade 4 Skybuilders' Proto-hropken",
        ]

        fisher_lv80_collectables = [
            "Grade 4 Skybuilders' Ghost Faerie",
            "Grade 4 Skybuilders' Ashfish",
            "Grade 4 Skybuilders' Whitehorse",
            "Grade 4 Skybuilders' Ocean Cloud",
            "Grade 4 Skybuilders' Black Fanfish",
            "Grade 4 Skybuilders' Sunfish",
        ]

        if self.has_level_80_or_higher:
            fisher_collectables.extend(fisher_lv80_collectables)

        if self.has_heavensward:
            firmament_fishing_collectables.extend(fisher_collectables)

        return sorted(firmament_fishing_collectables)
    
    def firmament_high_tier_fishing_collectables(self) -> List[str]:
        firmament_high_tier_fishing_collectables = list()

        high_tier_fisher_collectables = [
            "Grade 4 Artisanal Skybuilders' Sweatfish",
            "Grade 4 Artisanal Skybuilders' Sculptor",
            "Grade 4 Artisanal Skybuilders' Little Thalaos",
            "Grade 4 Artisanal Skybuilders' Lightning Chaser",
            "Grade 4 Artisanal Skybuilders' Marrella",
            "Grade 4 Artisanal Skybuilders' Crimson Namitaro",
            "Grade 4 Artisanal Skybuilders' Griffin",
            "Grade 4 Artisanal Skybuilders' Meganeura",
        ]

        if self.has_heavensward and self.has_level_80_or_higher:
                firmament_high_tier_fishing_collectables.extend(high_tier_fisher_collectables)

        return sorted(firmament_high_tier_fishing_collectables)

    def big_fish(self) -> List[str]:
        big_fish = [
            "Goldenfin",
            "Octomammoth",
            "Zalera",
            "Beguiler Chub",
            "Great Gudgeon",
            "Gigantshark",
            "High Perch",
            "Crystal Perch",
            "Caterwauler",
            "Oschon's Print",
            "Syldra",
            "Silver Sovereign",
            "Sabertooth Cod",
            "Jacques the Snipper",
            "Faerie Queen",
            "Meteor Survivor",
            "Cupfish",
            "The Greatest Bream in the World",
            "Shark Tuna",
            "Bombardfish",
            "The Old Man in the Sea",
            "The Salter",
            "The Drowned Sniper",
            "The Terpsichorean",
            "Mirrorscale",
            "Imperial Goldfish",
            "Armorer",
            "Junkmonger",
            "Navigator's Brand",
            "The Lone Ripper",
            "Helmsman's Hand",
            "Frilled Shark",
            "The Captain's Chalice",
            "Toramafish",
            "Joan of Trout",
            "Worm of Nym",
            "King of the Spring",
            "Thundergut",
            "Twitchbeard",
            "Stormdancer",
            "Bloody Brewer",
            "Matron Carp",
            "Carp Diem",
            "Chirurgeon",
            "Ghost Carp",
            "Levinlight",
            "Bloodbath",
            "The Green Jester",
            "Dark Ambusher",
            "Moldva",
            "The Assassin",
            "Sylphsbane",
            "Blue Widow",
            "Judgeray",
            "Shadowstreak",
            "Cornelia",
            "Son of Levin",
            "The Gobfather",
            "Vip Viper",
            "Floating Boulder",
            "The Grinner",
            "The Sinker",
            "Sweetnewt",
            "Glimmerscale",
            "Mud Golem",
            "Rivet Oyster",
            "Pirate's Bane",
            "Fingers",
            "Dirty Herry",
            "Dream Goby",
            "Slime King",
            "Old Softie",
            "Dark Knight",
            "Marrow Sucker",
            "Mud Pilgrim",
            "The Warden's Wand",
            "The Thousand-year Itch",
            "Olgoi-Khorkhoi",
            "Magic Carpet",
            "Old Hollow Eyes",
            "Discobolus",
            "Iron Noose",
            "Hannibal",
            "Spearnose",
            "The Matriarch",
            "Anomalocaris",
            "Charon's Lantern",
            "Daniffen's Mark",
            "Dawn Maiden",
            "Starbright",
            "Mahar",
            "Aetherlouse",
            "Void Bass",
            "Ninja Betta",
            "Ignus Horn",
            "Blood Red Bonytongue",
            "Canavan",
            "Namitaro",
            "Endoceras",
            "Helicoprion",
            "Kuno the Killer",
            "Shonisaurus",
            "Nepto Dragon",
        ]

        heavensward_big_fish = [
            "Fat Purse",
            "La Reale",
            "Bishopfish",
            "Hailfinder",
            "Captain Nemo",
            "Flarefish",
            "Merciless",
            "Inkfish",
            "Cirrostratus",
            "Basking Shark",
            "The Second One",
            "Paikiller",
            "Scaleripper",
            "Riddle",
            "The Lord of Lords",
            "Meteortoise",
            "The Dreamweaver",
            "Hraesvelgr's Tear",
            "Twin-tongued Carp",
            "Vidofnir",
            "Moggle Mogpom",
            "The Soul of the Martyr",
            "Dimorphodon",
            "Bloodchaser",
            "Thousand Fin",
            "The Ewer King",
            "Bobgoblin Bass",
            "Madam Butterfly",
            "The Speaker",
            "Augmented High Allagan Helmet",
            "Aetherochemical Compound #666",
            "Aphotic Pirarucu",
            "Ceti",
            "Allagan Bladeshark",
            "Crystal Pigeon",
            "Hundred-eyed Axolotl",
            "Armor Fish",
            "Problematicus",
            "Opabinia",
            "Raimdellopterus",
            "Charibenet",
            "Sea Butterfly",
        ]

        stormblood_big_fish = [
            "Downstream Loach",
            "Sapphire Fan",
            "Corpse Chub",
            "The Archbishop",
            "Hardhead Trout",
            "Hookstealer",
            "Watcher Catfish",
            "Bloodtail Zombie",
            "Bondsplitter",
            "The Last Tear",
            "Lily of the Veil",
            "Hemon",
            "Moksha",
            "The Undecided",
            "Diamond-eye",
            "Rising Dragon",
            "The Gambler",
            "Princess Killifish",
            "Ku'er",
            "The Vegetarian",
            "Pinhead",
            "Argonautica",
            "The Winter Queen",
            "Seven Stars",
            "Rakshasa",
            "Hermit's End",
            "Suiten Ippeki",
            "Hagoromo Koi",
            "The Unraveled Bow",
            "Pomegranate Trout",
            "Glarramundi",
            "Axelrod",
            "Hagoromo Bijin",
            "Banderole",
            "Duskfish",
            "Nhaama's Treasure",
            "Yat Khan",
            "Garden Skipper",
            "The Word of God",
            "Blade Skipper",
            "Drepanaspis",
            "The Unconditional",
            "Warden of the Seven Hues",
            "Xenacanthus",
            "Stethacanthus",
            "The Ruby Dragon",
        ]

        shadowbringers_big_fish = [
            "Loose Pendant",
            "The Sinsteeped",
            "Aster Trivi",
            "Winged Dame",
            "Sweetheart",
            "The Unforgiven",
            "Python Discus",
            "Moonlight Guppy",
            "The Jaws of Undeath",
            "White Ronso",
            "Bronze Sole",
            "Steel Fan",
            "Henodus Grandis",
            "Steel Razor",
            "Shadeshifter",
            "Giant Taimen",
            "The Horned King",
            "Nabaath Saw",
            "Ambling Caltrop",
            "Leannisg",
            "The Sound of Fury",
            "Gold Hammer",
            "Sunken Tome",
            "Fae Rainbow",
            "Dammroen Herring",
            "Celestial",
            "Priest of Yx'Lokwa",
            "Golden Pipira",
            "Recordkiller",
            "Black Jet",
            "Pearl Pipira",
            "Deephaunt",
            "Mora Tecta",
            "Starchaser",
            "The Ondotaker",
            "The Mother of All Pancakes",
            "Ondo Sigh",
            "Opal Shrimp",
            "Maru Crab",
            "Listracanthus",
            "Aquamaton",
            "Cinder Surprise",
            "Ealad Skaan",
            "Greater Serpent of Ronka",
            "Lancetfish",
        ]

        endwalker_big_fish = [
            "Aetherolectric Guitarfish",
            "Greatsword Snook",
            "Catastrophizer",
            "Jumbo Snook",
            "Swampsucker Bowfin",
            "Mossgill Salmon",
            "Earful",
            "Lale Crab",
            "Hippo Frog",
            "Bigcuda",
            "Browned Banana Eel",
            "Vidyutvat Wrasse",
            "Sovereign Shadow",
            "Rimepike",
            "Disappirarucu",
            "Frozen Regotoise",
            "Foun Ahlm",
            "Starscryer",
            "Forbiddingway",
            "Argonauta argo",
            "Cosmic Haze",
            "Planetes",
            "Antheian Dahlia",
            "Basilosaurus Rex",
            "Onyx Knifefish",
            "Eehs Fan",
            "Wakeful Warden",
            "Gilt Dermogenys",
            "Mayaman",
            "Starscale Ephemeris",
            "Chlorophos Deathworm",
            "Durdina Fish",
            "E.B.E.-852738",
            "Circuit Tilapia",
            "Hyphalosaurus",
            "Gharlichthys",
            "Snowy Parexus",
            "Lopoceras Elegans",
            "Furcacauda",
            "Sidereal Whale",
        ]

        dawntrail_big_fish = [
            "Icuvlo's Barter",
            "Moongripper",
            "Cazuela Crab",
            "Ilyon Asoh Cichlid",
            "Stardust Sleeper",
            "Hwittayoanaan Cichlid",
            "Thunderswift Trout",
            "Pixel Loach",
        ]

        if self.has_heavensward:
            big_fish.extend(heavensward_big_fish)

        if self.has_stormblood:
            big_fish.extend(stormblood_big_fish)

        if self.has_shadowbringers:
            big_fish.extend(shadowbringers_big_fish)

        if self.has_endwalker:
            big_fish.extend(endwalker_big_fish)

        if self.has_dawntrail:
            big_fish.extend(dawntrail_big_fish)

        return sorted(big_fish)

    @staticmethod
    def crafting_collectables_count_range() -> range:
        return range(3,13)
    
    def crafting_collectables(self) -> List[str]:
        crafting_collectables = list()

        heavensward_carpenter_collectables = [
            "Rarefied Cedar Longbow",
            "Rarefied Cedar Fishing Rod",
            "Rarefied Holy Cedar Spinning Wheel",
            "Rarefied Dark Chestnut Rod",
            "Rarefied Hallowed Chestnut Ring",
            "Rarefied Birch Signum",
        ]

        heavensward_blacksmith_collectables = [
            "Rarefied Mythrite Katzbalger",
            "Rarefied Mythrite Pugiones",
            "Rarefied Mythrite halfheart Saw",
            "Rarefied Titanium Creasing Knife",
            "Rarefied Titanium Mortar",
            "Rarefied Adamantite Bill",
        ]

        heavensward_armorer_collectables = [
            "Rarefied Mythrite Sallet",
            "Rarefied Mythrite Hauberk",
            "Rarefied Mythrite Bladed Lantern Shield",
            "Rarefied Titanium Frypan",
            "Rarefied Titanium Vambraces",
            "Rarefied Adamantite Scutum",
        ]

        heavensward_goldsmith_collectables = [
            "Rarefied Mythrite Goggles",
            "Rarefied Mythrite Bangle",
            "Rarefied Mythrite Needle",
            "Rarefied Hardsilver Monocle",
            "Rarefied Hardsilver Pole",
            "Rarefied Aurum Regis Earrings",
        ]

        heavensward_leatherworker_collectables = [
            "Rarefied Archaeoskin Belt",
            "Rarefied Archaeoskin Cloche",
            "Rarefied Wyvernskin Mask",
            "Rarefied Dhalmelskin Coat",
            "Rarefied Dragonskin Ring",
            "Rarefied Serpentskin Hat",
        ]

        heavensward_weaver_collectables = [
            "Rarefied Rainbow Bolero",
            "Rarefied Rainbow Ribbon",
            "Rarefied Holy Rainbow Hat",
            "Rarefied Ramie Turban",
            "Rarefied Hallowed Ramie Doublet",
            "Rarefied Chimerical Felt Cyclas",
        ]

        heavensward_alchemist_collectables = [
            "Rarefied Archaeoskin Grimoire",
            "Rarefied Archaeoskin Codex",
            "Rarefied Dissolvent",
            "Rarefied Dhalmelskin Codex",
            "Rarefied Max-Potion",
            "Rarefied Book of Aurum Regis",
        ]

        heavensward_culinarian_collectables = [
            "Rarefied Dhalmel Gratin",
            "Rarefied Sohm Al Tart",
            "Rarefied Sauteed Porcini",
            "Rarefied Royal Eggs",
            "Rarefied Peperoncino",
            "Rarefied Marron Glace",
        ]

        stormblood_carpenter_collectables = [
            "Rarefied Beech Composite Bow",
            "Rarefied Larch Necklace",
            "Rarefied Pine Cane",
            "Rarefied Persimmon Bracelets",
            "Rarefied Zelkova Spinning Wheel",
        ]

        stormblood_blacksmith_collectables = [
            "Rarefied High Steel Guillotine",
            "Rarefied High Steel Claw Hammer",
            "Rarefied Doman Iron Uchigatana",
            "Rarefied Doman Steel Patas",
            "Rarefied Molybdenum Pliers",
        ]

        stormblood_armorer_collectables = [
            "Rarefied High Steel Thermal Alembic",
            "Rarefied High Steel Plate Belt",
            "Rarefied Doman Iron Greaves",
            "Rarefied Doman Steel Tabard",
            "Rarefied Molybdenum Headgear",
        ]

        stormblood_goldsmith_collectables = [
            "Rarefied Koppranickel Planisphere",
            "Rarefied Koppranickel Necklace",
            "Rarefied Durium Chaplets",
            "Rarefied Durium Rod",
            "Rarefied Palladium Needle",
        ]

        stormblood_leatherworker_collectables = [
            "Rarefied Gaganaskin Shoes",
            "Rarefied Gyuki Leather Jacket",
            "Rarefied Tigerskin Tricorne",
            "Rarefied Marid Leather Corset",
            "Rarefied Gazelleskin Armguards",
        ]

        stormblood_weaver_collectables = [
            "Rarefied Bloodhempen Skirt",
            "Rarefied Ruby Cotton Gilet",
            "Rarefied Kudzu Hat",
            "Rarefied Serge Hose",
            "Rarefied Twinsilk Apron",
        ]

        stormblood_alchemist_collectables = [
            "Rarefied Koppranickel Index",
            "Rarefied Reisui",
            "Rarefied Tigerskin Grimoire",
            "Rarefied Growth Formula",
            "Rarefied Gazelleskin Codex",
        ]

        stormblood_culinarian_collectables = [
            "Rarefied Baklava",
            "Rarefied Shorlog",
            "Rarefied Tempura Platter",
            "Rarefied Persimmon Pudding",
            "Rarefied Chirashi-zushi",
        ]

        shadowbringers_carpenter_collectables = [
            "Rarefied White Oak Partisan",
            "Rarefied Applewood Staff",
            "Rarefied White Ash Earrings",
            "Rarefied Sandteak Fauchard",
            "Rarefied Lignum Vitae Grinding Wheel",
        ]

        shadowbringers_blacksmith_collectables = [
            "Rarefied Deepgold Anelace",
            "Rarefied Deepgold Culinary Knife",
            "Rarefied Bluespirit Gunblade",
            "Rarefied Titanbronze Pickaxe",
            "Rarefied Mythril Hatchet",
        ]

        shadowbringers_armorer_collectables = [
            "Rarefied Deepgold Cuirass",
            "Rarefied Deepgold Wings",
            "Rarefied Bluespirit Gauntlets",
            "Rarefied Titanbronze Tower Shield",
            "Rarefied Mythril Alembic",
        ]

        shadowbringers_goldsmith_collectables = [
            "Rarefied Stonegold Degen",
            "Rarefied Stonegold Orrery",
            "Rarefied Manasilver Ear Cuffs",
            "Rarefied Titanbronze Headgear",
            "Rarefied Mythril Ring",
        ]

        shadowbringers_leatherworker_collectables = [
            "Rarefied Smilodonskin Trousers",
            "Rarefied Gliderskin Thighboots",
            "Rarefied Atrociraptorskin Cap",
            "Rarefied Zonureskin Fingerless Gloves",
            "Rarefied Swallowskin Coat",
        ]

        shadowbringers_weaver_collectables = [
            "Rarefied Brightlinen Himation",
            "Rarefied Iridescent Top",
            "Rarefied Pixie Cotton Hood",
            "Rarefied Ovim Wool Tunic",
            "Rarefied Dwarven Cotton Beret",
        ]

        shadowbringers_alchemist_collectables = [
            "Rarefied Alkahest",
            "Rarefied Gliderskin Grimoire",
            "Rarefied Bluespirit Codex",
            "Rarefied Syrup",
            "Rarefied Dwarven Mythrile Grimoire",
        ]

        shadowbringers_culinarian_collectables = [
            "Rarefied Grilled Rail",
            "Rarefied Spaghetti al Nero",
            "Rarefied Popotoes au Gratin",
            "Rarefied Espresso con Panna",
            "Rarefied Lemonade",
        ]

        endwalker_carpenter_collectables = [
            "Rarefied Horse Chestnut Kasa",
            "Rarefied Palm Bracelet",
            "Rarefied Red Pine Spinning Wheel",
            "Rarefied Ironwood Grinding Wheel",
            "Rarefied Integral Armillae",
            "Rarefied Integral Fishing Rod",
        ]

        endwalker_blacksmith_collectables = [
            "Rarefied High Durium Pistol",
            "Rarefied High Durium Greatsword",
            "Rarefied Bismuth Sledgehammer",
            "Rarefied Manganese Cross-pein Hammer",
            "Rarefied Chondrite Culinary Knife",
            "Rarefied Chondrite Lapidary Hammer",
        ]

        endwalker_armorer_collectables = [
            "Rarefied High Durium Knuckles",
            "Rarefied High Durium Kite Shield",
            "Rarefied Bismuth Fat Cat Frypan",
            "Rarefied Manganese Armor of the Behemoth King",
            "Rarefied Chondrite Sollerets",
            "Rarefied Chondrite Alembic",
        ]

        endwalker_goldsmith_collectables = [
            "Rarefied High Durium Milpreves",
            "Rarefied Pewter Choker",
            "Rarefied Phrygian Earring",
            "Rarefied Manganese Horn of the Last Unicorn",
            "Rarefied Star Quartz Choker",
            "Rarefied Chondrite Needle",
        ]

        endwalker_leatherworker_collectables = [
            "Rarefied Gajaskin Shoes",
            "Rarefied Luncheon Toadskin Hose",
            "Rarefied Saigaskin Gloves",
            "Rarefied Kumbhiraskin Shoes",
            "Rarefied Ophiotauroskin Top",
            "Rarefied Ophiotauroskin Halfgloves",
        ]

        endwalker_weaver_collectables = [
            "Rarefied Darkhempen Hat",
            "Rarefied Almasty Serge Gloves",
            "Rarefied Snow Linen Doublet",
            "Rarefied Scarlet Moko Wedge Cap",
            "Rarefied AR-Caean Velvet Bottoms",
            "Rarefied AR-Caean Velvet Work Cap",
        ]

        endwalker_alchemist_collectables = [
            "Rarefied Gajaskin Codex",
            "Rarefied Luncheon Toadskin Grimoire",
            "Rarefied Moon Gel",
            "Rarefied Enchanted Manganese Ink",
            "Rarefied Draught",
            "Rarefied Ophiotauroskin Magitek Codex",
        ]

        endwalker_culinarian_collectables = [
            "Rarefied Archon Loaf",
            "Rarefied King Crab Cake",
            "Rarefied Happiness Juice",
            "Rarefied Giant Haddock Dip",
            "Rarefied Giant Popoto Pancakes",
            "Rarefied Sykon Bavarois",
        ]

        dawntrail_carpenter_collectables = [
            "Rarefied Ginseng Earrings",
            "Rarefied Ceiba Spear",
            "Rarefied Dark Mahogany Necklace",
            "Rarefied Acacia Rod",
            "Rarefied Claro Walnut Grinding Wheel",
            "Rarefied Claro Walnut Fishing Rod",
        ]

        dawntrail_blacksmith_collectables = [
            "Rarefied Mountain Chromite Fists",
            "Rarefied Ruthenium War Axe",
            "Rarefied Cobalt Tungsten Scimitars",
            "Rarefied Titanium Gold Mortar",
            "Rarefied Ra'Kaznar War Scythe",
            "Rarefied Ra'Kaznar Round Knife",
        ]

        dawntrail_armorer_collectables = [
            "Rarefied Mountain Chromite Alembic",
            "Rarefied Ruthenium Sabatons",
            "Rarefied Cobalt Tungsten Chocobo Frypan",
            "Rarefied Titanium Gold Thorned Corselet",
            "Rarefied Ra'Kaznar Greaves",
            "Rarefied Ra'Kaznar Ring",
        ]

        dawntrail_goldsmith_collectables = [
            "Rarefied Lar Longbow",
            "Rarefied Ihuykanite Circlet",
            "Rarefied Cobalt Tungsten Tuck",
            "Rarefied White Gold Choker",
            "Rarefied Ra'Kaznar Orrery",
            "Rarefied Black Star Earrings",
        ]

        dawntrail_leatherworker_collectables = [
            "Rarefied Loboskin Fingerless Gloves",
            "Rarefied Crocodileskin Leggings",
            "Rarefied Br'aaxskin Armlets",
            "Rarefied Gomphotherium Brais",
            "Rarefied Gargantuaskin Trousers",
            "Rarefied Gargantuaskin Hat",
        ]

        dawntrail_weaver_collectables = [
            "Rarefied Snow Cotton Beret",
            "Rarefied Mountain Linen Top",
            "Rarefied Sarcenet Kecks",
            "Rarefied Rroneek Serge Hat",
            "Rarefied Thunderyards Silk Gloves",
            "Rarefied Thunderyards Silk Culottes",
        ]

        dawntrail_alchemist_collectables = [
            "Rarefied Loboskin Grimoire",
            "Rarefied Gemsap of Dexterity",
            "Rarefied Br'aaxskin Codex",
            "Rarefied Cunning Craftsman's Tisane",
            "Rarefied Gemdraught of Vitality",
            "Rarefied Claro Walnut Flat Brush",
        ]

        dawntrail_culinarian_collectables = [
            "Rarefied Boiled Alpaca Steak",
            "Rarefied Banana Ponzecake",
            "Rarefied Turali Pineapple Ponzecake",
            "Rarefied Salmon Jerky",
            "Rarefied Stuffed Peppers",
            "Rarefied Tacos de Carne Asada",
        ]

        if self.has_heavensward:
            if "Carpenter" in self.playable_jobs:
                crafting_collectables.extend(heavensward_carpenter_collectables)

            if "Blacksmith" in self.playable_jobs:
                crafting_collectables.extend(heavensward_blacksmith_collectables)

            if "Armorer" in self.playable_jobs:
                crafting_collectables.extend(heavensward_armorer_collectables)

            if "Goldsmith" in self.playable_jobs:
                crafting_collectables.extend(heavensward_goldsmith_collectables)

            if "Leatherworker" in self.playable_jobs:
                crafting_collectables.extend(heavensward_leatherworker_collectables)

            if "Weaver" in self.playable_jobs:
                crafting_collectables.extend(heavensward_weaver_collectables)

            if "Alchemist" in self.playable_jobs:
                crafting_collectables.extend(heavensward_alchemist_collectables)

            if "Culinarian" in self.playable_jobs:
                crafting_collectables.extend(heavensward_culinarian_collectables)

        if self.has_stormblood:
            if "Carpenter" in self.playable_jobs:
                crafting_collectables.extend(stormblood_carpenter_collectables)

            if "Blacksmith" in self.playable_jobs:
                crafting_collectables.extend(stormblood_blacksmith_collectables)

            if "Armorer" in self.playable_jobs:
                crafting_collectables.extend(stormblood_armorer_collectables)

            if "Goldsmith" in self.playable_jobs:
                crafting_collectables.extend(stormblood_goldsmith_collectables)

            if "Leatherworker" in self.playable_jobs:
                crafting_collectables.extend(stormblood_leatherworker_collectables)

            if "Weaver" in self.playable_jobs:
                crafting_collectables.extend(stormblood_weaver_collectables)

            if "Alchemist" in self.playable_jobs:
                crafting_collectables.extend(stormblood_alchemist_collectables)

            if "Culinarian" in self.playable_jobs:
                crafting_collectables.extend(stormblood_culinarian_collectables)

        if self.has_shadowbringers:
            if "Carpenter" in self.playable_jobs:
                crafting_collectables.extend(shadowbringers_carpenter_collectables)

            if "Blacksmith" in self.playable_jobs:
                crafting_collectables.extend(shadowbringers_blacksmith_collectables)

            if "Armorer" in self.playable_jobs:
                crafting_collectables.extend(shadowbringers_armorer_collectables)

            if "Goldsmith" in self.playable_jobs:
                crafting_collectables.extend(shadowbringers_goldsmith_collectables)

            if "Leatherworker" in self.playable_jobs:
                crafting_collectables.extend(shadowbringers_leatherworker_collectables)

            if "Weaver" in self.playable_jobs:
                crafting_collectables.extend(shadowbringers_weaver_collectables)

            if "Alchemist" in self.playable_jobs:
                crafting_collectables.extend(shadowbringers_alchemist_collectables)

            if "Culinarian" in self.playable_jobs:
                crafting_collectables.extend(shadowbringers_culinarian_collectables)

        if self.has_endwalker:
            if "Carpenter" in self.playable_jobs:
                crafting_collectables.extend(endwalker_carpenter_collectables)

            if "Blacksmith" in self.playable_jobs:
                crafting_collectables.extend(endwalker_blacksmith_collectables)

            if "Armorer" in self.playable_jobs:
                crafting_collectables.extend(endwalker_armorer_collectables)

            if "Goldsmith" in self.playable_jobs:
                crafting_collectables.extend(endwalker_goldsmith_collectables)

            if "Leatherworker" in self.playable_jobs:
                crafting_collectables.extend(endwalker_leatherworker_collectables)

            if "Weaver" in self.playable_jobs:
                crafting_collectables.extend(endwalker_weaver_collectables)

            if "Alchemist" in self.playable_jobs:
                crafting_collectables.extend(endwalker_alchemist_collectables)

            if "Culinarian" in self.playable_jobs:
                crafting_collectables.extend(endwalker_culinarian_collectables)

        if self.has_dawntrail:
            if "Carpenter" in self.playable_jobs:
                crafting_collectables.extend(dawntrail_carpenter_collectables)

            if "Blacksmith" in self.playable_jobs:
                crafting_collectables.extend(dawntrail_blacksmith_collectables)

            if "Armorer" in self.playable_jobs:
                crafting_collectables.extend(dawntrail_armorer_collectables)

            if "Goldsmith" in self.playable_jobs:
                crafting_collectables.extend(dawntrail_goldsmith_collectables)

            if "Leatherworker" in self.playable_jobs:
                crafting_collectables.extend(dawntrail_leatherworker_collectables)

            if "Weaver" in self.playable_jobs:
                crafting_collectables.extend(dawntrail_weaver_collectables)

            if "Alchemist" in self.playable_jobs:
                crafting_collectables.extend(dawntrail_alchemist_collectables)

            if "Culinarian" in self.playable_jobs:
                crafting_collectables.extend(dawntrail_culinarian_collectables)

        return sorted(crafting_collectables)
    
    def firmament_crafting_collectables(self) -> List[str]:
        firmament_crafting_collectables = list()

        carpenter_collectables = [
            "Grade 4 Skybuilders' Plywood",
            "Grade 4 Skybuilders' Crate",
            "Grade 4 Skybuilders' Spinning Wheel",
        ]

        carpenter_lv70_collectables = [
            "Grade 4 Skybuilders' Stepladder",
        ]

        carpenter_lv80_collectables = [
            "Grade 4 Skybuilders' Bed",
        ]

        blacksmith_collectables = [
            "Grade 4 Skybuilders' Alloy",
            "Grade 4 Skybuilders' Nails",
            "Grade 4 Skybuilders' Hatchet",
        ]

        blacksmith_lv70_collectables = [
            "Grade 4 Skybuilders' Crosscut Saw",
        ]

        blacksmith_lv80_collectables = [
            "Grade 4 Skybuilders' Oven",
        ]

        armorer_collectables = [
            "Grade 4 Skybuilders' Steel Plate",
            "Grade 4 Skybuilders' Rivets",
            "Grade 4 Skybuilders' Cookpot",
        ]

        armorer_lv70_collectables = [
            "Grade 4 Skybuilders' Mesail",
        ]

        armorer_lv80_collectables = [
            "Grade 4 Skybuilders' Lamppost",
        ]

        goldsmith_collectables = [
            "Grade 4 Skybuilders' Ingot",
            "Grade 4 Skybuilders' Rings",
            "Grade 4 Skybuilders' Embroidery Frame",
        ]

        goldsmith_lv70_collectables = [
            "Grade 4 Skybuilders' Stone",
        ]

        goldsmith_lv80_collectables = [
            "Grade 4 Skybuilders' Brazier",
        ]

        leatherworker_collectables = [
            "Grade 4 Skybuilders' Leather",
            "Grade 4 Skybuilders' Leather Straps",
            "Grade 4 Skybuilders' Leather Sack", 
        ]

        leatherworker_lv70_collectables = [
            "Grade 4 Skybuilders' Longboots",
        ]

        leatherworker_lv80_collectables = [
            "Grade 4 Skybuilders' Overalls",
        ]

        weaver_collectables = [
            "Grade 4 Skybuilders' Rope",
            "Grade 4 Skybuilders' Cloth",
            "Grade 4 Skybuilders' Broom",
        ]

        weaver_lv70_collectables = [
            "Grade 4 Skybuilders' Gloves",
        ]

        weaver_lv80_collectables = [
            "Grade 4 Skybuilders' Awning",
        ]

        alchemist_collectables = [
            "Grade 4 Skybuilders' Ink",
            "Grade 4 Skybuilders' Plant Oil",
            "Grade 4 Skybuilders' Holy Water",
        ]

        alchemist_lv70_collectables = [
            "Grade 4 Skybuilders' Soap",
        ]

        alchemist_lv80_collectables = [
            "Grade 4 Skybuilders' Growth Formula",
        ]

        culinarian_collectables = [
            "Grade 4 Skybuilders' Hemp Milk",
            "Grade 4 Skybuilders' Sesame Cookie",
            "Grade 4 Skybuilders' Tea",
        ]

        culinarian_lv70_collectables = [
            "Grade 4 Skybuilders' All-purpose Infusion",
        ]

        culinarian_lv80_collectables = [
            "Grade 4 Skybuilders' Stew",
        ]

        if self.has_level_70_or_higher:
            carpenter_collectables.extend(carpenter_lv70_collectables)
            armorer_collectables.extend(armorer_lv70_collectables)
            blacksmith_collectables.extend(blacksmith_lv70_collectables)
            goldsmith_collectables.extend(goldsmith_lv70_collectables)
            leatherworker_collectables.extend(leatherworker_lv70_collectables)
            weaver_collectables.extend(weaver_lv70_collectables)
            alchemist_collectables.extend(alchemist_lv70_collectables)
            culinarian_collectables.extend(culinarian_lv70_collectables)

        if self.has_level_80_or_higher:
            carpenter_collectables.extend(carpenter_lv80_collectables)
            armorer_collectables.extend(armorer_lv80_collectables)
            blacksmith_collectables.extend(blacksmith_lv80_collectables)
            goldsmith_collectables.extend(goldsmith_lv80_collectables)
            leatherworker_collectables.extend(leatherworker_lv80_collectables)
            weaver_collectables.extend(weaver_lv80_collectables)
            alchemist_collectables.extend(alchemist_lv80_collectables)
            culinarian_collectables.extend(culinarian_lv80_collectables)


        if self.has_heavensward:
            if "Carpenter" in self.playable_jobs:
                firmament_crafting_collectables.extend(carpenter_collectables)

            if "Blacksmith" in self.playable_jobs:
                firmament_crafting_collectables.extend(blacksmith_collectables)

            if "Armorer" in self.playable_jobs:
                firmament_crafting_collectables.extend(armorer_collectables)

            if "Goldsmith" in self.playable_jobs:
                firmament_crafting_collectables.extend(goldsmith_collectables)

            if "Leatherworker" in self.playable_jobs:
                firmament_crafting_collectables.extend(leatherworker_collectables)

            if "Weaver" in self.playable_jobs:
                firmament_crafting_collectables.extend(weaver_collectables)

            if "Alchemist" in self.playable_jobs:
                firmament_crafting_collectables.extend(alchemist_collectables)

            if "Culinarian" in self.playable_jobs:
                firmament_crafting_collectables.extend(culinarian_collectables)

        return sorted(firmament_crafting_collectables)

    def firmament_high_tier_crafting_collectables(self) -> List[str]:
        firmament_high_tier_crafting_collectables = list()

        high_tier_carpenter_collectables = [
            "Grade 4 Artisanal Skybuilders' Icebox",
        ]

        high_tier_blacksmith_collectables = [
            "Grade 4 Artisanal Skybuilders' Chocobo Weathervane",
        ]

        high_tier_armorer_collectables = [
            "Grade 4 Artisanal Skybuilders' Company Chest",
        ]

        high_tier_goldsmith_collectables = [
            "Grade 4 Artisanal Skybuilders' Astroscope",
        ]

        high_tier_leatherworker_collectables = [
            "Grade 4 Artisanal Skybuilders' Tool Belt",
        ]

        high_tier_weaver_collectables = [
            "Grade 4 Artisanal Skybuilders' Vest",
        ]

        high_tier_alchemist_collectables = [
            "Grade 4 Artisanal Skybuilders' Tincture",
        ]

        high_tier_culinarian_collectables = [
            "Grade 4 Artisanal Skybuilders' Sorbet",
        ]

        if self.has_heavensward and self.has_level_80_or_higher:
            if "Carpenter" in self.playable_jobs:
                firmament_high_tier_crafting_collectables.extend(high_tier_carpenter_collectables)

            if "Blacksmith" in self.playable_jobs:
                firmament_high_tier_crafting_collectables.extend(high_tier_blacksmith_collectables)

            if "Armorer" in self.playable_jobs:
                firmament_high_tier_crafting_collectables.extend(high_tier_armorer_collectables)

            if "Goldsmith" in self.playable_jobs:
                firmament_high_tier_crafting_collectables.extend(high_tier_goldsmith_collectables)

            if "Leatherworker" in self.playable_jobs:
                firmament_high_tier_crafting_collectables.extend(high_tier_leatherworker_collectables)

            if "Weaver" in self.playable_jobs:
                firmament_high_tier_crafting_collectables.extend(high_tier_weaver_collectables)

            if "Alchemist" in self.playable_jobs:
                firmament_high_tier_crafting_collectables.extend(high_tier_alchemist_collectables)

            if "Culinarian" in self.playable_jobs:
                firmament_high_tier_crafting_collectables.extend(high_tier_culinarian_collectables)

        return sorted(firmament_high_tier_crafting_collectables)

    @staticmethod
    def crystalline_conflict_match_counts() -> range:
        return range(1,6)
    
    @staticmethod
    def pvp_kill_counts() -> range:
        return range(2,6)

    @staticmethod
    def pvp_assist_counts() -> range:
        return range(5,11)

    @staticmethod
    def gate_count() -> range:
        return range(3,7)

    @staticmethod
    def gate_tasks() -> List[str]:
        gates = [
            "Successfully complete the GATE 'The Slice Is Right'",
            "Record a perfect score in the GATE 'Air Force One'",
            "Obtain all cactuars in the GATE 'Leap of Faith'",
            "Successfully complete the GATE 'Any Way the Wind Blows'",
            "Complete the GATE 'Cliffhanger' without being knocked back by any explosives",
        ]

        return sorted(gates)

    def triple_triad_opponents(self) -> List[str]:
        opponents = [
            "Memeroon",
            "Jonas of the Three Spades",
            "Maisenta",
            "Roger",
            "Guhtwint of the Three Diamonds",
            "Mother Miounne",
            "Wymond",
            "Momodi",
            "F'hobhas",
            "Triple Triad Master",
            "Joellaut",
            "Aurifort of the Three Clubs",
            "Piralnaut",
            "Trachtoum",
            "Mimidoa",
            "Baderon",
            "Fufulupa",
            "Helmhart",
            "Ourdilic",
            "Ruhtwyda of the Three Hearts",
            "Marcette",
            "Buscarron",
            "Sezul Totoloc",
            "Landenel",
            "King Elmer III",
            "Vorsaile Heuloix",
            "Swift",
            "Hab",
            "Indolent Imperial",
            "Rowena",
            "Gegeruju",
            "R'ashaht Rhiki",
            "Lewena",
            "Noes",
            "Yellow Moon",
            "Wawalago",
            "Yayake",
            "Gibrillont",
            "Wyra 'Greenhands' Lyehga",
            "Prideful Stag",
            "Nell Half-full",
            "Flichoirel the Lordling",
            "Hall Overseer",
        ]

        heavensward_opponents = [
            "Marcechamp",
            "Marielle",
            "Midnight Dew",
            "Idle Imperial",
            "Mogmill",
            "Dominiac",
            "Linu Vali",
            "Vath Deftarm",
            "Elaisse",
            "Laniaitte",
            "Voracious Vath",
            "Seika",
            "Tapklix",
            "Redbill Storeboy",
            "Klynthota",
            "House Fortemps Manservant",
            "Master Mogzin",
            "O'kalkaya",
            "Mordyn",
        ]

        stormblood_opponents = [
            "Ercanbald",
            "Kotokaze",
            "Kaizan",
            "Tsuzura",
            "Gyoei",
            "Nigen",
            "Ogodei",
            "Munglig",
            "Kiuka",
            "Garima",
            "Imperial Deserter",
            "Umber Torrent",
            "Hachinan",
            "Masatsuchi",
            "Isobe",
            "Yusui",
            "Kikimo",
            "Ushiogi",
            "Botan",
            "Mero Roggo",
            "Hokushin",
            "Hetsukaze",
            "Ironworks Hand",
        ]

        shadowbringers_opponents = [
            "Glynard",
            "Gyuf Uin",
            "Hargra",
            "Drery",
            "Ibenart",
            "Lamlyn",
            "Saushs Koal",
            "Grewenn",
            "Eo Sigun",
            "Redard",
            "Hanagasa",
            "Cobleva",
            "Furtive Former Imperial",
            "Arsieu",
            "Lewto-Sue",
            "Droyn",
            "Sladkey",
        ]

        endwalker_opponents = [
            "Aiglephine",
            "Qetanur",
            "Worldly Imperial",
            "Mehryde",
            "Cheatingway",
            "Celia",
            "Prudence",
            "Ghasa",
            "Kilfufu",
            "Gamingway",
            "Ruissenaud",
            "Tokimori",
            "Ylaire",
            "Maillart",
        ]

        dawntrail_opponents = [
            "Nyikweni",
            "Wopli",
            "Warsowok",
            "Br'uk Noq'",
            "Luwyawa",
            "Uataaye",
            "Larisa",
            "Gavoll Ja",
            "Pawkukwe",
            "Miitso",
        ]

        if self.has_heavensward:
            opponents.extend(heavensward_opponents)

        if self.has_stormblood:
            opponents.extend(stormblood_opponents)

        if self.has_shadowbringers:
            opponents.extend(shadowbringers_opponents)

        if self.has_endwalker:
            opponents.extend(endwalker_opponents)

        if self.has_dawntrail:
            opponents.extend(dawntrail_opponents)

        return sorted(opponents)

    def triple_triad_card_from_opponent_common(self) -> List[str]:
        cards = list()

        one_star_cards = [
            "Tonberry Triple Triad card from Memeroon",
            "Spriggan Triple Triad card from Triple Triad Master",
            "Pudding Triple Triad card from Roger",
            "Coblyn Triple Triad card from Maisenta or Wymond",
            "Morbol Triple Triad card from Roger",
            "Ahriman Triple Triad card from Ourdilic",
            "Goobbue Triple Triad card from Mother Miounne or Aurifort Of The Three Clubs",
            "Chocobo Triple Triad card from Guhtwint of the Three Diamonds",
            "Amalj'aa Triple Triad card from Memeroon",
            "Ixal Triple Triad card from Joellaut or Jonas Of The Three Spades",
            "Sylph Triple Triad card from Maisenta",
            "Sahagin Triple Triad card from Baderon",
            "Moogle Triple Triad card from Trachtoum or Jonas Of The Three Spades",
            "Apkallu Triple Triad card from Wyra 'Greenhands' Lyehga",
            "Colibri Triple Triad card from Flichoirel The Lordling",
        ]

        two_star_cards = [
            "Siren Triple Triad card from Mimidoa",
            "Ultros & Typhon Triple Triad card from Helmhart",
            "Demon Wall Triple Triad card from Buscarron",
            "Succubus Triple Triad card from Piralnaut",
            "Chimera Triple Triad card from Fufulupa",
            "Blue Dragon Triple Triad card from Ourdilic",
            "Scarface Bugaal Ja Triple Triad card from Aurifort Of The Three Clubs or Guhtwint Of The Three Diamonds",
            "Momodi Modi Triple Triad card from Momodi",
            "Baderon Tenfingers Triple Triad card from Baderon",
            "Mother Miounne Triple Triad card from Mother Miounne",
            "Rhitahtyn sas Arvina Triple Triad card from Indolent Imperial",
            "Biggs & Wedge Triple Triad card from Mimidoa or Sezul Totoloc",
            "Gerolt Triple Triad card from Rowena or Helmhart",
            "Frixio Triple Triad card from Piralnaut or Marcette",
            "Mutamix Bubblypots Triple Triad card from F'hobhas",
            "Memeroon Triple Triad card from Memeroon",
            "Lost Lamb Triple Triad card from Prideful Stag",
            "Magitek Colossus Triple Triad card from Hall Overseer",
        ]

        three_star_cards = [
            "Behemoth Triple Triad card from Ourdilic or Sezul Totoloc",
            "Ifrit Triple Triad card from Swift",
            "Titan Triple Triad card from Trachtoum or Landenel",
            "Garuda Triple Triad card from Marcette",
            "Good King Moggle Mog XII Triple Triad card from Vorsaile Heuloix",
            "Raya-O-Senna & A-Ruhn-Senna Triple Triad card from Buscarron",
            "Godbert Manderville Triple Triad card from Hab, King Elmer III, or Ruhtwyda Of The Three Hearts",
            "Thancred Triple Triad card from Fufulupa or Hab",
            "Nero tol Scaeva Triple Triad card from Indolent Imperial",
            "Papalymo & Yda Triple Triad card from Vorsaile Heuloix or Buscarron",
            "Y'shtola Triple Triad card from R'ashaht Rhiki or Gegeruju",
            "Urianger Triple Triad card from Ruhtwyda Of The Three Hearts",
            "Brendt, Brennan, & Bremondt Triple Triad card from Nell Half-full",
        ]

        heavensward_one_star_cards = [
            "Gaelicat Triple Triad card from Noes",
            "Deepeye Triple Triad card from Dominiac",
        ]

        heavensward_two_star_cards = [
            "Vanu Vanu Triple Triad card from Mogmill",
            "Gnath Triple Triad card from Mogmill",
            "Yugiri Mistwalker Triple Triad card from Yellow Moon",
            "Fat Chocobo Triple Triad card from Vath Deftarm",
            "Archaeornis Triple Triad card from Elaisse",
            "Paissa Triple Triad card from Laniaitte",
            "Dhalmel Triple Triad card from Laniaitte",
            "Bandersnatch Triple Triad card from Voracious Vath",
            "Crawler Triple Triad card from Seika",
            "Poroggo Triple Triad card from Seika",
            "Honoroit Triple Triad card from House Fortemps Manservant",
            "Lolorito Nanarito Triple Triad card from Wymond",
            "Gibrillont Triple Triad card from Elaisse",
            "Laniaitte de Haillenarte Triple Triad card from Marielle",
            "Rhoswen Triple Triad card from O'kalkaya",
            "Carvallain de Gorgagne Triple Triad card from Mordyn",   
        ]

        heavensward_three_star_cards = [
            "Good King Moggle Mog XII Triple Triad card from Vorsaile Heuloix or Master Mogzin",
            "Griffin Triple Triad card from Dominiac",
            "Estinien Triple Triad card from Gibrillont",
            "Lucia goe Junius Triple Triad card from Wawalago",
            "Ysayle Triple Triad card from Marcechamp",
            "Hilda Triple Triad card from Idle Imperial",
            "Matoya Triple Triad card from Midnight Dew",
            "Count Edmont de Fortemps Triple Triad card from Marielle",
            "Byblos Triple Triad card from Mero Roggo",
            "Vedrfolnir Triple Triad card from Mogmill",
            "Coeurlregina Triple Triad card from Voracious Vath or Vath Deftarm",
            "Belladonna Triple Triad card from Midnight Dew",
            "Echidna Triple Triad card from Redbill Storeboy",
            "Pipin Tarupin Triple Triad card from Swift",
            "Moglin Triple Triad card from Mogmill",
            "Roundrox Triple Triad card from Tapklix or Seika",
            "Brachiosaur Triple Triad card from Linu Vali",
            "Darkscale Triple Triad card from Master Mogzin",
            "Kraken Triple Triad card from Mordyn",
            "Vicegerent to the Warden Triple Triad card from Yayake",
            "Manxome Molaa Ja Ja Triple Triad card from Memeroon",
            "Ferdiad Triple Triad card from Redbill Storeboy",
            "Calcabrina Triple Triad card from Mero Roggo",
            "Kuribu Triple Triad card from Noes",
            "Phlegethon Triple Triad card from Klynthota",
            "Artoirel de Fortemps Triple Triad card from House Fortemps Manservant",
            "Emmanellain de Fortemps Triple Triad card from House Fortemps Manservant",
            "Kal Myhk Triple Triad card from Master Mogzin",
            "Waukkeon Triple Triad card from Linu Vali",
            "Curator Triple Triad card from Idle Imperial",
            "Mistbeard Triple Triad card from O'kalkaya",
            "Strix Triple Triad card from Mero Roggo",
            "Tozol Huatotl Triple Triad card from Sezul Totoloc",
            "Alexander Prime Triple Triad card from Tapklix",
        ]

        stormblood_one_star_cards = [
            "Namazu Triple Triad card from Gyoei",
            "Koja Triple Triad card from Masatsuchi",
            "Wanyudo & Katasharin Triple Triad card from Ushiogi",
            "Karakuri Hanya Triple Triad card from Hokushin",
        ]

        stormblood_two_star_cards = [
            "Kojin Triple Triad card from Tsuzura",
            "Ananta Triple Triad card from Garima",
            "M'naago Triple Triad card from Ercanbald",
            "Kotokaze Triple Triad card from Kotokaze",
            "Qiqirn Meateater Triple Triad card from Garima",
            "Ango Triple Triad card from Isobe",
            "Tansui Triple Triad card from Yusui",
            "Hatamoto Triple Triad card from ushiogi",
            "Yukinko Triple Triad card from Botan",
            "Dvergr Triple Triad card from Hetsukaze",
            "Ejika Tsunjika Triple Triad card from Hetsukaze",
        ]

        stormblood_three_star_cards = [
            "Griffin Triple Triad card from Dominiac or Ercanbald",
            "Mammoth Triple Triad card from Munglig, Nigen, or Ogodei",
            "Phoebad Triple Triad card from Umber Torrent",
            "Grynewaht Triple Triad card from Imperial Deserter",
            "Rasho Triple Triad card from Kaizan",
            "Cirina Triple Triad card from Nigen",
            "Magnai Triple Triad card from Ogodei",
            "Sadu Triple Triad card from Munglig",
            "Fordola rem Lupis Triple Triad card from Imperial Deserter",
            "Rofocale Triple Triad card from Hanagasa",
            "Arenvald Lentinus Triple Triad card from Umber Torrent",
            "Lupin Triple Triad card from Masatsuchi",
            "Hiruko Triple Triad card from Ushiogi",
            "Happy Bunny Triple Triad card from Botan",
            "Louhi Triple Triad card from Botan",
            "Asahi sas Brutus Triple Triad card from Hachinan",
            "Pazuzu Triple Triad card from Botan",
            "Penthesilea Triple Triad card from Hetsukaze",
            "Alpha Triple Triad card from Ironworks Hand",
            "Provenance Watcher Triple Triad card from Hetsukaze",
        ]

        shadowbringers_one_star_cards = [
            "Amaro Triple Triad card from Glynard",
            "Evil Weapon Triple Triad card from Drery",
            "Lord and Lady Chai Triple Triad card from Ibenart",
            "Porxie Triple Triad card from Eo Sigun",
            "Qitari Triple Triad card from Redard",
            "Dwarf Triple Triad card from Cobleva",
        ]

        shadowbringers_two_star_cards = [
            "Gigatender Triple Triad card from Drery",
            "Feo Ul Triple Triad card from Gyuf Uin",
            "Runar Triple Triad card from Hargra",
            "Grenoldt Triple Triad card from Saushs Koal",
            "Nu Mou Triple Triad card from Eo Sigun",
            "Rolling Tankard Triple Triad card from Cobleva",
        ]

        shadowbringers_three_star_cards = [
            "Lyna Triple Triad card from Lamlyn",
            "Jongleurs of Eulmore Triple Triad card from Grewenn",
            "Batsquatch Triple Triad card from Redard",
            "Dawon Triple Triad card from Arsieu",
            "Adrammelech Triple Triad card from Arsieu",
            "Azulmagia Triple Triad card from Droyn",
            "Siegfried Triple Triad card from Droyn",
            "4th-make Shemhazai Triple Triad card from Sladkey",
            "4th-make Cuchulainn Triple Triad card from Sladkey",
        ]

        endwalker_one_star_cards = [
            "Troll Triple Triad card from Aiglephine",
            "Pisaca Triple Triad card from Qetanur",
            "Hippo Cart Triple Triad card from Ghasa",
            "Dreamingway Triple Triad card from Gamingway",
            "Okuri Chochin Triple Triad card from Tokimori",
        ]

        endwalker_two_star_cards = [
            "Arkasodara Triple Triad card from Mehryde",
            "Loporrit Triple Triad card from Cheatingway",
            "Argos Triple Triad card from Cheatingway",
            "Geryon the Steer Triple Triad card from Kilfufu",
        ]

        endwalker_three_star_cards = [
            "Fourchenault Leveilleur Triple Triad card from Celia",
            "Rhalgr Triple Triad card from Prudence",
            "Azeyma Triple Triad card from Prudence",
            "Proto-Carbuncle Triple Triad card from Ruissenaud",
            "Nophica Triple Triad card from Ylaire",
            "Althyk Triple Triad card from Ylaire",
            "Nymeia Triple Triad card from Ylaire",
            "Thaliak Triple Triad card from Maillart",
            "Llymlaen Triple Triad card from Maillart",
        ]

        dawntrail_one_star_cards = [
            "Pelupelu Triple Triad card from Nyikweni",
            "Alpaca Triple Triad card from Wopli",
        ]

        dawntrail_two_star_cards = [
            "Moblin Triple Triad card from Warsowok",
            "Branchbearer Triple Triad card from Br'uk Noq'",
            "Rroneek Triple Triad card from Luwyawa",
            "Sentry R8 Triple Triad card from Uataaye",
            "Outrunner Triple Triad card from Larisa",
        ]

        dawntrail_three_star_cards = [
            "Gulool Ja Ja Triple Triad card from Gavoll Ja",
            "Ark Angel TT Triple Triad card from Pawkukwe",
            "Ark Angel GK Triple Triad card from Pawkukwe",
            "Ark Angel HM Triple Triad card from Miitso",
            "Ark Angel EV Triple Triad card from Miitso",
        ]

        cards.extend(one_star_cards)
        cards.extend(two_star_cards)
        cards.extend(three_star_cards)

        if self.has_heavensward:
            cards.extend(heavensward_one_star_cards)
            cards.extend(heavensward_two_star_cards)
            cards.extend(heavensward_three_star_cards)

        if self.has_stormblood:
            cards.extend(stormblood_one_star_cards)
            cards.extend(stormblood_two_star_cards)
            cards.extend(stormblood_three_star_cards)

        if self.has_shadowbringers:
            cards.extend(shadowbringers_one_star_cards)
            cards.extend(shadowbringers_two_star_cards)
            cards.extend(shadowbringers_three_star_cards)

        if self.has_endwalker:
            cards.extend(endwalker_one_star_cards)
            cards.extend(endwalker_two_star_cards)
            cards.extend(endwalker_three_star_cards)

        if self.has_dawntrail:
            cards.extend(dawntrail_one_star_cards)
            cards.extend(dawntrail_two_star_cards)
            cards.extend(dawntrail_three_star_cards)

        return sorted(cards)

    def triple_triad_card_from_opponent_rare(self) -> List[str]:
        cards = list()

        four_star_cards = [
            "Odin Triple Triad card from Landenel",
            "Ramuh Triple Triad card from Vorsaile Heuloix",
            "Leviathan Triple Triad card from R'ashaht Rhiki",
            "Minfilia Triple Triad card from Gegeruju",
            "Cid Garlond Triple Triad card from Sezul Totoloc",
            "Alphinaud & Alisaie Triple Triad card from Swift or Joellaut",
            "Louisoix Leveilleur Triple Triad card from Rowena",
            "Nael van Darnus Triple Triad card from Flichoirel The Lordling",
        ]

        five_star_cards = [
            "Bahamut Triple Triad card from King Elmer III",
            "Hildibrand & Nashu Mhakaracca Triple Triad card from Hab",
            "Gaius van Baelsar Triple Triad card from Indolent Imperial",
            "Merlwyb Bloefhiswyn Triple Triad card from Mordyn, O'kalkaya, or R'ashaht Rhiki",
            "Kan-E-Senna Triple Triad card from Vorsaile Heuloix",
            "Raubahn Aldynn Triple Triad card from Swift",
            "Onion Knight Triple Triad card from Lewena",
            "Bartz Klauser Triple Triad card from Lewena",
            "Terra Branford Triple Triad card from Lewena or Hall Overseer",
        ]

        heavensward_four_star_cards = [
            "Aymeric Triple Triad card from Yayake",
            "Ravana Triple Triad card from Vath Deftarm",
            "Bismarck Triple Triad card from Linu Vali",
            "Xande Triple Triad card from Klynthota",
            "Brute Justice Triple Triad card from Tapklix",
            "Unei & Doga Triple Triad card from Klynthota",
            "Tiamat Triple Triad card from Idle Imperial",
            "Calofisteri Triple Triad card from Redbill Storeboy",
            "Diabolos Hollow Triple Triad card from Redbill Storeboy",
        ]

        heavensward_five_star_cards = [
            "Regula van Hydrus Triple Triad card from Idle Imperial",
            "Cloud of Darkness Triple Triad card from Klynthota",
            "Hraesvelgr Triple Triad card from Master Mogzin",
        ]

        stormblood_four_star_cards = [
            "Shinryu Triple Triad card from Ironworks Hand",
            "Yotsuyu Triple Triad card from Imperial Deserter",
            "Argath Thadalfus Triple Triad card from Hanagasa",
            "Hancock Triple Triad card from Kikimo",
            "Great Gold Whisker Triple Triad card from Gyoei",
        ]

        stormblood_five_star_cards = [
            "Zenos yae Galvus Triple Triad card from Hachinan",
            "Hien Triple Triad card from Kiuka",
            "Hisui & Kurenai Triple Triad card from Isobe",
            "Yiazmat Triple Triad card from Hanagasa",
            "Omega Triple Triad card from Ironworks Hand",
            "Yojimbo & Daigoro Triple Triad card from Hokushin",
            "Ultima, the High Seraph Triple Triad card from Hanagasa",
            "Stormblood Alphinaud & Alisaie Triple Triad card from Mero Roggo",
        ]

        shadowbringers_four_star_cards = [
            "Shadowbringers Y'shtola Triple Triad card from Hargra",
            "Ran'jit Triple Triad card from Grewenn",
            "Sapphire Weapon Triple Triad card from Furtive Former Imperial",
            "Ryne Triple Triad card from Lewto-Sue",
            "Gaia Triple Triad card from Lewto-Sue",
        ]

        shadowbringers_five_star_cards = []

        endwalker_four_star_cards = [
            "Quintus van Cinna Triple Triad card from Worldly Imperial",
            "Endwalker Alphinaud & Alisaie Triple Triad card from Celia",
            "Themis Triple Triad card from Ruissenaud",
        ]

        endwalker_five_star_cards = []

        dawntrail_four_star_cards = []

        dawntrail_five_star_cards = []

        cards.extend(four_star_cards)
        cards.extend(five_star_cards)

        if self.has_heavensward:
            cards.extend(heavensward_four_star_cards)
            cards.extend(heavensward_five_star_cards)

        if self.has_stormblood:
            cards.extend(stormblood_four_star_cards)
            cards.extend(stormblood_five_star_cards)

        if self.has_shadowbringers:
            cards.extend(shadowbringers_four_star_cards)
            cards.extend(shadowbringers_five_star_cards)

        if self.has_endwalker:
            cards.extend(endwalker_four_star_cards)
            cards.extend(endwalker_five_star_cards)

        if self.has_dawntrail:
            cards.extend(dawntrail_four_star_cards)
            cards.extend(dawntrail_five_star_cards)

        return sorted(cards)

    @staticmethod
    def high_low_range() -> range:
        return range(2,6)


# Archipelago Options
class FinalFantasyXIVContentTypesAllowed(OptionSet):
    """
    Indicates what possible Final Fantasy XIV content types the player would like to include.

    Note: Opting in to Unreasonable Tasks adds extra objectives to several different content types, 
    which could potentially take multiple days or weeks to even make an attempt.
    """

    display_name = "Final Fantasy XIV Allowed Content Types"
    valid_keys = [
        # Battle Content
        "FATEs",
        "Guildhests",
        "Treasure Hunt",
        "The Hunt",
        "Dungeons",
        "Trials",
        "Extreme Trials",
        "Normal Raids",
        "Savage Raids",
        "Alliance Raids",
        "Chaotic Alliance Raids",
        "Deep Dungeons",
        "Variant Dungeons",
        "Adventuring Forays",
        "Limited Jobs",
        # PvP
        "Crystalline Conflict",
        "Frontline",
        "Rival Wings",
        # Non-combat
        "Gathering",
        "Fishing",
        "Crafting",
        "Jumping Puzzles",
        "Gold Saucer",
        "Triple Triad",
        "Minigames",
        # Special
        "Unreasonable Tasks",
    ]

    default = valid_keys


class FinalFantasyXIVExpansionsAccessible(OptionSet):
    """
    Indicates which Final Fantasy XIV expansions the player has access to.
    """

    display_name = "Final Fantasy XIV Expansions Accessible"
    valid_keys = [
        "Heavensward",
        "Stormblood",
        "Shadowbringers",
        "Endwalker",
        "Dawntrail",
    ]

    default = valid_keys


class FinalFantasyXIVPlayableJobs(OptionSet):
    """
    Indicates what jobs the player has unlocked to be considered for challenges.

    It is recommended to only enable jobs which are of a sufficient level to participate in content of
    the latest expansion that will be allowed, or that can be leveled to that point over the course
    of your game.

    Combat objectives expect a minimum of two non-limited combat jobs to be enabled.
    """

    display_name = "Final Fantasy XIV Playable Jobs"
    valid_keys = [
        # Combat
        "Paladin",
        "Warrior",
        "Dark Knight",
        "Gunbreaker",
        "White Mage",
        "Scholar",
        "Astrologian",
        "Sage",
        "Monk",
        "Dragoon",
        "Ninja",
        "Samurai",
        "Reaper",
        "Viper",
        "Bard",
        "Machinist",
        "Dancer",
        "Black Mage",
        "Summoner",
        "Red Mage",
        "Pictomancer",
        # Limited Jobs
        "Blue Mage",
        # "Beastmaster",
        # Crafting
        "Carpenter",
        "Blacksmith",
        "Armorer",
        "Goldsmith",
        "Leatherworker",
        "Weaver",
        "Alchemist",
        "Culinarian",
        # Gathering
        "Miner",
        "Botanist",
        "Fisher",
    ]

    default = valid_keys
