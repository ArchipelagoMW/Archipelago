from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class StellarisArchipelagoOptions:
    stellaris_dlc_owned: StellarisDLCOwned


class StellarisGame(Game):
    name = "Stellaris"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = StellarisArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play an Empire with the following Trait: TRAIT",
                data={
                    "TRAIT": (self.traits, 1)
                },
            ),
            GameObjectiveTemplate(
                label="Play an Empire with the following Origin: ORIGIN",
                data={
                    "ORIGIN": (self.origins, 1)
                },
            ),
            GameObjectiveTemplate(
                label="Play an Empire with the following Ethics: Fanatic ETHICS",
                data={
                    "ETHICS": (self.ethics, 1)
                },
            ),
            GameObjectiveTemplate(
                label="Play an Empire with the following Authority: AUTHORITY",
                data={
                    "AUTHORITY": (self.authorities, 1)
                },
            ),
            GameObjectiveTemplate(
                label="Play an Empire with the following Civic: CIVIC",
                data={
                    "CIVIC": (self.civics, 1)
                },
            ),
            GameObjectiveTemplate(
                label="Play as the EMPIRE",
                data={
                    "EMPIRE": (self.preset_empires, 1)
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Have COUNT active SHIP Ships",
                data={
                    "COUNT": (self.civilian_ship_count_range, 1),
                    "SHIP": (self.civilian_ship_types, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Colonize COUNTx WORLD",
                data={
                    "COUNT": (self.colony_count_range, 1),
                    "WORLD": (self.habitable_worlds, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Survey COUNTx WORLD",
                data={
                    "COUNT": (self.survey_world_count_range, 1),
                    "WORLD": (self.uninhabitable_worlds, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Survey COUNTx STAR System",
                data={
                    "COUNT": (self.survey_star_count_range, 1),
                    "STAR": (self.stars, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Encounter a Fallen Empire",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Win a war against a Fallen Empire",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="ACCEPTDENY a request, task, or demand from a Fallen Empire",
                data={
                    "ACCEPTDENY": (self.accept_deny, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Receive a gift from a Fallen Empire",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Obtain COUNT Relics",
                data={
                    "COUNT": (self.relic_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Construct COUNTx Observation Post",
                data={
                    "COUNT": (self.observation_post_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Interact with a Pre-FTL Civilation by DIPLOMACY",
                data={
                    "DIPLOMACY": (self.pre_ftl_diplomacy, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Have COUNT pops with RIGHTS",
                data={
                    "COUNT": (self.population_count_range, 1),
                    "RIGHTS": (self.rights, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Complete the TREE Tradition Tree",
                data={
                    "TREE": (self.tradition_trees, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Unlock the PERK Perk",
                data={
                    "PERK": (self.ascension_perks, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Research TECH",
                data={
                    "TECH": (self.rare_tech, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Enable the EDICT edict for 10 years",
                data={
                    "EDICT": (self.edicts, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Have 100% approval from a Faction with the following Ethics: ETHICS",
                data={
                    "ETHICS": (self.ethics, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Enable the following Policy: POLICY",
                data={
                    "POLICY": (self.policies, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Hit the Resource Cap for RESOURCE",
                data={
                    "RESOURCE": (self.stored_resources, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Have an income of COUNT RESOURCE per month",
                data={
                    "COUNT": (self.basic_resource_income_range, 1),
                    "RESOURCE": (self.basis_resources, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Have an income of COUNT RESOURCE per month",
                data={
                    "COUNT": (self.advanced_resource_income_range, 1),
                    "RESOURCE": (self.advanced_resources, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Have an income of COUNT RESOURCE per month",
                data={
                    "COUNT": (self.strategic_resource_income_range, 1),
                    "RESOURCE": (self.strategic_resources, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Have an income of COUNT RESOURCE per month",
                data={
                    "COUNT": (self.rare_resource_income_range, 1),
                    "RESOURCE": (self.rare_resources, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Have an income of COUNT RESOURCE per month",
                data={
                    "COUNT": (self.advanced_resource_income_range, 1),
                    "RESOURCE": (self.research_types, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=33,
            ),
            GameObjectiveTemplate(
                label="Have COUNTx BUILDING in your empire",
                data={
                    "COUNT": (self.building_empire_count_range, 1),
                    "BUILDING": (self.buildings, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=50,
            ),
            GameObjectiveTemplate(
                label="Have COUNTx BUILDING on one planet",
                data={
                    "COUNT": (self.building_planet_count_range, 1),
                    "BUILDING": (self.buildings, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=50,
            ),
            GameObjectiveTemplate(
                label="Have COUNTx BUILDING in your empire",
                data={
                    "COUNT": (self.unique_building_count_range, 1),
                    "BUILDING": (self.unique_buildings, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=50,
            ),
            GameObjectiveTemplate(
                label="Have the following Empire Unique Building: BUILDING",
                data={
                    "BUILDING": (self.empire_unique_buildings, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=50,
            ),
            GameObjectiveTemplate(
                label="Have COUNTx DISTRICT on one planet",
                data={
                    "COUNT": (self.district_planet_count_range, 1),
                    "DISTRICT": (self.districts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=50,
            ),
            GameObjectiveTemplate(
                label="Have COUNTx DISTRICT in your empire",
                data={
                    "COUNT": (self.district_empire_count_range, 1),
                    "DISTRICT": (self.districts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=50,
            ),
            GameObjectiveTemplate(
                label="Have COUNT JOB pops",
                data={
                    "COUNT": (self.population_count_range, 1),
                    "JOB": (self.jobs, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Have COUNT DESIGNATION Worlds using auto designations",
                data={
                    "COUNT": (self.planet_count_range, 1),
                    "DESIGNATION": (self.planet_designations, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Have COUNT Active Gateways in your empire",
                data={
                    "COUNT": (self.gateway_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Have COUNT MODULE Modules in your empire",
                data={
                    "COUNT": (self.module_count_range, 1),
                    "MODULE": (self.modules, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Have COUNTx BUILDING in your empire",
                data={
                    "COUNT": (self.starbase_building_count_range, 1),
                    "BUILDING": (self.starbase_buildings, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Have COUNTx LEVEL in your empire",
                data={
                    "COUNT": (self.starbase_count_range, 1),
                    "LEVEL": (self.starbase_levels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Have COUNT Defense Platforms in your empire",
                data={
                    "COUNT": (self.defense_platform_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=50,
            ),
            GameObjectiveTemplate(
                label="Own COUNTx HOLDING in other empires",
                data={
                    "COUNT": (self.holding_count_range, 1),
                    "HOLDING": (self.holdings, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Have the following Diplomatic Agreement with COUNT other empires: AGREEMENT",
                data={
                    "COUNT": (self.diplomacy_count_range, 1),
                    "AGREEMENT": (self.diplomatic_agreements, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Perform the following Diplomatic Action COUNT times: ACTION",
                data={
                    "COUNT": (self.diplomacy_count_range, 1),
                    "ACTION": (self.diplomatic_actions, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Have RELATION Relations with COUNT other empires",
                data={
                    "RELATION": (self.relations, 1),
                    "COUNT": (self.diplomacy_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Be a founding member of the Galactic Community",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Successfully support the following Resolution in the Galactic Community: RESOLUTION",
                data={
                    "RESOLUTION": (self.resolutions, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Be a member of a Level LEVEL TYPE Federation",
                data={
                    "LEVEL": (self.federation_level_range, 1),
                    "TYPE": (self.federation_types, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Participate in a 'OPERATION' Operation with your Federation",
                data={
                    "OPERATION": (self.operations, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Be a member of Federation with the following Law: LAW",
                data={
                    "LAW": (self.federation_laws, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Have COUNT Subject Empire(s)",
                data={
                    "COUNT": (self.subject_empire_count_range, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=66,
            ),
            GameObjectiveTemplate(
                label="Have COUNT Subject Empire(s) with the following Terms: TERMS",
                data={
                    "COUNT": (self.subject_empire_count_range, 1),
                    "TERMS": (self.subject_terms, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=66,
            ),
            GameObjectiveTemplate(
                label="Have COUNT Subject Empire(s) with the following Type: TYPE",
                data={
                    "COUNT": (self.subject_empire_count_range, 1),
                    "TYPE": (self.subject_types, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=66,
            ),
            GameObjectiveTemplate(
                label="Win a war in which one side has the following War Goal: GOAL",
                data={
                    "GOAL": (self.wargoals, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Have COUNT Capacity worth of SHIPs",
                data={
                    "COUNT": (self.naval_capacity_range, 1),
                    "SHIP": (self.ship_sizes, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Have COUNT Capacity worth of SHIPs in one fleet",
                data={
                    "COUNT": (self.fleet_capacity_range, 1),
                    "SHIP": (self.ship_sizes, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Have LEVEL or better CATEGORY Intel on COUNT empires",
                data={
                    "LEVEL": (self.intel_levels, 1),
                    "CATEGORY": (self.intel_categories, 1),
                    "COUNT": (self.diplomacy_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Perform the following Operation against another empire or Pre-FTL Civilization: OPERATION",
                data={
                    "OPERATION": (self.operations, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=100,
            ),
        ]

        if self.has_dlc_utopia:
            templates.append(
                GameObjectiveTemplate(
                    label="Add TRAIT trait to COUNT pops",
                    data={
                        "TRAIT": (self.traits_advanced_genetics, 1),
                        "COUNT": (self.population_count_range, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=100,
                )
            )

        if self.has_dlc_utopia or self.has_dlc_the_machine_age:
            templates.append(
                GameObjectiveTemplate(
                    label="Add TRAIT trait to COUNT pops",
                    data={
                        "TRAIT": (self.traits_cyborg, 1),
                        "COUNT": (self.population_count_range, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=100,
                )
            )

        if self.has_dlc_leviathans or self.has_dlc_distant_stars or self.has_dlc_ancient_relics or self.has_dlc_aquatics:
            templates.append(
                GameObjectiveTemplate(
                    label="Have a Leviathan with TRAIT",
                    data={
                        "TRAIT": (self.traits_organic_leviathan, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=100,
                )
            )

        if self.has_dlc_the_machine_age:
            templates.append(
                GameObjectiveTemplate(
                    label="Have a Leviathan with TRAIT",
                    data={
                        "TRAIT": (self.traits_mechanical_leviatan, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=100,
                )
            )

        if self.has_dlc_nemesis:
            templates.append(
                GameObjectiveTemplate(
                    label="Win as the Crisis",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=10,
                )
            )

        if self.has_dlc_distant_stars:
            templates.append(
                GameObjectiveTemplate(
                    label="Open an L-Gate",
                    data=dict(),
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=50,
                )
            )

        if len(self.megastructures()):
            templates.append(
                GameObjectiveTemplate(
                    label="Construct or repair a complete MEGASTRUCTURE",
                    data={
                        "MEGASTRUCTURE": (self.megastructures, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=25,
                ),
            )

        if self.has_dlc_federations or self.has_dlc_nemesis:
            templates.append(
                GameObjectiveTemplate(
                    label="Be on the galactic / imperial council while its size is SIZE or less",
                    data={
                        "SIZE": (self.galactic_council_size_range, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=100,
                )
            )

        if self.has_dlc_nemesis:
            templates.extend([
                GameObjectiveTemplate(
                    label="Become the Custodian of the Galactic Community",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=50,
                ),
                GameObjectiveTemplate(
                    label="Become the Emperor of the Galactic Empire",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=25,
                ),
            ])

        if self.has_dlc_apocalypse or self.has_dlc_the_machine_age or self.has_dlc_federations or self.has_dlc_nemesis:
            templates.append(
                GameObjectiveTemplate(
                    label="Build a SHIP",
                    data={
                        "SHIP": (self.colossal_ship_types, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=40,
                )
            )

        if self.has_dlc_apocalypse or self.has_dlc_the_machine_age:
            templates.append(
                GameObjectiveTemplate(
                    label="Build a Colossus with a WEAPON",
                    data={
                        "WEAPON": (self.colossus_weapons, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=10,
                )
            )

        return templates

    @property
    def dlc_owned(self) -> List[str]:
        return sorted(self.archipelago_options.stellaris_dlc_owned.value)

    @property
    def has_dlc_grand_archive(self) -> bool:
        return "Grand Archive" in self.dlc_owned

    @property
    def has_dlc_cosmic_storms(self) -> bool:
        return "Cosmic Storms" in self.dlc_owned

    @property
    def has_dlc_the_machine_age(self) -> bool:
        return "The Machine Age" in self.dlc_owned

    @property
    def has_dlc_astral_planes(self) -> bool:
        return "Astral Planes" in self.dlc_owned

    @property
    def has_dlc_galactic_paragons(self) -> bool:
        return "Galactic Paragons" in self.dlc_owned

    @property
    def has_dlc_first_contact(self) -> bool:
        return "First Contact" in self.dlc_owned

    @property
    def has_dlc_toxoids(self) -> bool:
        return "Toxoids" in self.dlc_owned

    @property
    def has_dlc_overlord(self) -> bool:
        return "Overlord" in self.dlc_owned

    @property
    def has_dlc_aquatics(self) -> bool:
        return "Aquatics" in self.dlc_owned

    @property
    def has_dlc_nemesis(self) -> bool:
        return "Nemesis" in self.dlc_owned

    @property
    def has_dlc_necroids(self) -> bool:
        return "Necroids" in self.dlc_owned

    @property
    def has_dlc_federations(self) -> bool:
        return "Federations" in self.dlc_owned

    @property
    def has_dlc_lithoids(self) -> bool:
        return "Lithoids" in self.dlc_owned

    @property
    def has_dlc_ancient_relics(self) -> bool:
        return "Ancient Relics" in self.dlc_owned

    @property
    def has_dlc_megacorp(self) -> bool:
        return "Megacorp" in self.dlc_owned

    @property
    def has_dlc_distant_stars(self) -> bool:
        return "Distant Stars" in self.dlc_owned

    @property
    def has_dlc_apocalypse(self) -> bool:
        return "Apocalypse" in self.dlc_owned

    @property
    def has_dlc_humanoids(self) -> bool:
        return "Humanoids" in self.dlc_owned

    @property
    def has_dlc_synthetic_dawn(self) -> bool:
        return "Synthetic Dawn" in self.dlc_owned

    @property
    def has_dlc_utopia(self) -> bool:
        return "Utopia" in self.dlc_owned

    @property
    def has_dlc_leviathans(self) -> bool:
        return "Leviathans" in self.dlc_owned

    @property
    def has_dlc_plantoids(self) -> bool:
        return "Plantoids" in self.dlc_owned

    @functools.cached_property
    def traits_base(self) -> List[str]:
        return [
            "Agrarian",
            "Ingenious",
            "Industrious",
            "Intelligent",
            "Thrifty",
            "Natural Engineers",
            "Natural Physicists",
            "Natural Sociologists",
            "Extremely Adaptive",
            "Adaptive",
            "Nonadaptive",
            "Rapid Breeders",
            "Slow Breeders",
            "Talented",
            "Quick Learners",
            "Slow Learners",
            "Traditional",
            "Quarrelsome",
            "Docile",
            "Unruly",
            "Very Strong",
            "Strong",
            "Weak",
            "Nomadic",
            "Sedentary",
            "Communal",
            "Solitary",
            "Charismatic",
            "Repugnant",
            "Conformists",
            "Deviants",
            "Venerable",
            "Enduring",
            "Fleeting",
            "Decadent",
            "Resilient",
            "Conservationist",
            "Wasteful",
        ]

    @functools.cached_property
    def traits_aquatics(self) -> List[str]:
        return [
            "Aquatic",
        ]

    @functools.cached_property
    def traits_plantoids(self) -> List[str]:
        return [
            "Phototrophic",
            "Radiotrophic",
            "Budding",
            "Invasive Species",
        ]

    @functools.cached_property
    def traits_humanoids(self) -> List[str]:
        return [
            "Existential Iteroparity",
            "Psychological Infertility",
            "Jinxed",
        ]

    @functools.cached_property
    def traits_toxoids(self) -> List[str]:
        return [
            "Incubators",
            "Inorganic Breath",
            "Noxious",
            "Dedicated Miner",
            "Farm Appendages",
            "Technical Talent",
            "Commercial Genius",
            "Crafted Smiles",
            "Augmented Intelligence",
            "Expressed Tradition",
            "Juiced Power",
            "Low Maintenance",
            "Spliced Adaptability",
            "Gene Mentorship",
            "Fleeting Excellence",
            "Elevator Synapses",
            "Pre-Planned Growth",
            "Excessive Endurance",
        ]

    @functools.cached_property
    def traits_the_machine_age(self) -> List[str]:
        return [
            "Ritualistic Implants",
            "Augmentations of the Choir",
            "Augmentations of the Commune",
            "Augmentations of the Fellowship",
            "Augmentations of the Templars",
        ]

    @functools.cached_property
    def traits_utopia(self) -> List[str]:
        return [
            "Hive-Minded",
        ]

    @functools.cached_property
    def traits_lithoids(self) -> List[str]:
        return [
            "Lithoid",
            "Gaseous Byproducts",
            "Scintillating Skin",
            "Volatile Excretions",
            "Crystalizations",
        ]

    def traits(self) -> List[str]:
        traits: List[str] = self.traits_base[:]

        if self.has_dlc_aquatics:
            traits.extend(self.traits_aquatics)

        if self.has_dlc_plantoids:
            traits.extend(self.traits_plantoids)

        if self.has_dlc_humanoids:
            traits.extend(self.traits_humanoids)

        if self.has_dlc_toxoids:
            traits.extend(self.traits_toxoids)

        if self.has_dlc_the_machine_age:
            traits.extend(self.traits_the_machine_age)

        if self.has_dlc_utopia:
            traits.extend(self.traits_utopia)

        if self.has_dlc_lithoids:
            traits.extend(self.traits_lithoids)

        return sorted(traits)

    @functools.cached_property
    def origin_base(self) -> List[str]:
        return [
            "Prosperous Unification",
            "Galactic Doorstep",
            "Lost Colony",
        ]

    @functools.cached_property
    def origin_utopia(self) -> List[str]:
        return [
            "Mechanist",
            "Syncretic Evolution",
            "Tree of Life",
        ]

    @functools.cached_property
    def origin_apocalypse(self) -> List[str]:
        return [
            "Life-Seeded",
            "Post-Apocalyptic",
        ]

    @functools.cached_property
    def origin_ancient_relics_or_federations(self) -> List[str]:
        return [
            "Remnants",
        ]

    @functools.cached_property
    def origin_federations(self) -> List[str]:
        return [
            "Shattered Ring",
            "Void Dwellers",
            "Scion",
            "On the Shoulders of Giants",
            "Common Ground",
            "Hegemon",
            "Doomsday",
        ]

    @functools.cached_property
    def origin_lithoids(self) -> List[str]:
        return [
            "Calamitous Birth",
        ]

    @functools.cached_property
    def origin_synthetic_dawn(self) -> List[str]:
        return [
            "Resource Consolidation",
        ]

    @functools.cached_property
    def origin_necroids(self) -> List[str]:
        return [
            "Necrophage",
        ]

    @functools.cached_property
    def origin_humanoids(self) -> List[str]:
        return [
            "Clone Army",
        ]

    @functools.cached_property
    def origin_aquatics(self) -> List[str]:
        return [
            "Here Be Dragons",
            "Ocean Paradise",
        ]

    @functools.cached_property
    def origin_overlord(self) -> List[str]:
        return [
            "Progenitor Hive",
            "Subterranean",
            "Slingshot to the Stars",
            "Teachers of the Shroud",
            "Imperial Fiefdom",
        ]

    @functools.cached_property
    def origin_toxoids(self) -> List[str]:
        return [
            "Overtuned",
            "Knights of the Toxic God",
        ]

    @functools.cached_property
    def origin_first_contact(self) -> List[str]:
        return [
            "Payback",
            "Broken Shackles",
            "Fear of the Dark",
        ]

    @functools.cached_property
    def origin_galactic_paragons(self) -> List[str]:
        return [
            "Under One Rule",
        ]

    @functools.cached_property
    def origin_plantoids(self) -> List[str]:
        return [
            "Fruitful Partnership",
        ]

    @functools.cached_property
    def origin_astral_planes(self) -> List[str]:
        return [
            "Riftworld",
        ]

    @functools.cached_property
    def origin_the_machine_age(self) -> List[str]:
        return [
            "Cybernetic Creed",
            "Synthetic Fertility",
            "Arc Welders",
        ]

    @functools.cached_property
    def origin_cosmic_storms(self) -> List[str]:
        return [
            "Storm Chasers",
        ]

    @functools.cached_property
    def origin_grand_archive(self) -> List[str]:
        return [
            "Treasure Hunters",
            "Primal Calling",
        ]

    def origins(self) -> List[str]:
        origins: List[str] = self.origin_base[:]

        if self.has_dlc_utopia:
            origins.extend(self.origin_utopia)

        if self.has_dlc_apocalypse:
            origins.extend(self.origin_apocalypse)

        if self.has_dlc_ancient_relics or self.has_dlc_federations:
            origins.extend(self.origin_ancient_relics_or_federations)

        if self.has_dlc_federations:
            origins.extend(self.origin_federations)

        if self.has_dlc_lithoids:
            origins.extend(self.origin_lithoids)

        if self.has_dlc_synthetic_dawn:
            origins.extend(self.origin_synthetic_dawn)

        if self.has_dlc_necroids:
            origins.extend(self.origin_necroids)

        if self.has_dlc_humanoids:
            origins.extend(self.origin_humanoids)

        if self.has_dlc_aquatics:
            origins.extend(self.origin_aquatics)

        if self.has_dlc_overlord:
            origins.extend(self.origin_overlord)

        if self.has_dlc_toxoids:
            origins.extend(self.origin_toxoids)

        if self.has_dlc_first_contact:
            origins.extend(self.origin_first_contact)

        if self.has_dlc_galactic_paragons:
            origins.extend(self.origin_galactic_paragons)

        if self.has_dlc_plantoids:
            origins.extend(self.origin_plantoids)

        if self.has_dlc_astral_planes:
            origins.extend(self.origin_astral_planes)

        if self.has_dlc_the_machine_age:
            origins.extend(self.origin_the_machine_age)

        if self.has_dlc_cosmic_storms:
            origins.extend(self.origin_cosmic_storms)

        if self.has_dlc_grand_archive:
            origins.extend(self.origin_grand_archive)

        return sorted(origins)

    @staticmethod
    def ethics() -> List[str]:
        return [
            "Egalitarian",
            "Materialists",
            "Pacifist",
            "Xenophile",
            "Authoritarian",
            "Spiritualist",
            "Militarist",
            "Xenophobe",
        ]

    @functools.cached_property
    def authorities_base(self) -> List[str]:
        return [
            "Democratic",
            "Oligarchic",
            "Dictatorial",
            "Imperial",
        ]

    @functools.cached_property
    def authorities_utopia(self) -> List[str]:
        return [
            "Hive Mind",
        ]

    @functools.cached_property
    def authorities_synthetic_dawn_or_the_machine_age(self) -> List[str]:
        return [
            "Machine Intelligence",
        ]

    @functools.cached_property
    def authorities_megacorp(self) -> List[str]:
        return [
            "Corporate",
        ]

    def authorities(self) -> List[str]:
        authorities: List[str] = self.authorities_base[:]

        if self.has_dlc_utopia:
            authorities.extend(self.authorities_utopia)

        if self.has_dlc_synthetic_dawn or self.has_dlc_the_machine_age:
            authorities.extend(self.authorities_synthetic_dawn_or_the_machine_age)

        if self.has_dlc_megacorp:
            authorities.extend(self.authorities_megacorp)

        return sorted(authorities)

    @functools.cached_property
    def civics_base(self) -> List[str]:
        return [
            "Cutthroat Politics",
            "Efficient Bureaucracy",
            "Functional Architecture",
            "Mining Guilds",
            "Agrarian Idyll",
            "Aristocratic Elite",
            "Beacon of Liberty",
            "Citizen Service",
            "Corporate Dominion",
            "Corvee System",
            "Distinguished Admiralty",
            "Environmentalist",
            "Exalted Priesthood",
            "Feudal Society",
            "Free Haven",
            "Idealistic Foundation",
            "Imperial Cult",
            "Meritocracy",
            "Nationalistic Zeal",
            "Parliamentary System",
            "Philosopher King",
            "Police State",
            "Shadow Council",
            "Slaver Guilds",
            "Technocracy",
            "Warrior Culture",
            "Inward Perfection",
        ]

    @functools.cached_property
    def civics_plantoids(self) -> List[str]:
        return [
            "Catalytic Processing",
            "Idyllic Bloom",
        ]

    @functools.cached_property
    def civics_humanoids(self) -> List[str]:
        return [
            "Masterful Crafters",
            "Pleasure Seekers",
            "Pompous Purists",
        ]

    @functools.cached_property
    def civics_megacorp(self) -> List[str]:
        return [
            "Byzantine Bureaucracy",
            "Merchant Guilds",
            "Shared Burdens",
            "Selective Kinship",
            "Diplomatic Corps",
            "Franchising",
            "Free Traders",
            "Private Prospectors",
            "Trading Posts",
            "Brand Loyalty",
            "Gospel of the Masses",
            "Indentured Assets",
            "Media Conglomerate",
            "Naval Contractors",
            "Private Military Companies",
            "Ruthless Competition",
            "Worker Cooperative",
            "Criminal Heritage",
        ]

    @functools.cached_property
    def civics_necroids(self) -> List[str]:
        return [
            "Death Cult",
            "Memorialists",
            "Reanimators",
        ]

    @functools.cached_property
    def civics_toxoids(self) -> List[str]:
        return [
            "Scavengers",
            "Mutagenic Spas",
            "Lubrication Tanks",
            "Relentless Industrialists",
        ]

    @functools.cached_property
    def civics_first_contact(self) -> List[str]:
        return [
            "Eager Explorers",
        ]

    @functools.cached_property
    def civics_galactic_paragons(self) -> List[str]:
        return [
            "Heroic Past",
            "Vaults of Knowledge",
            "Crusader Spirit",
            "Oppressive Autocracy",
        ]

    @functools.cached_property
    def civics_astral_planes(self) -> List[str]:
        return [
            "Dimensional Worship",
            "Hyperspace Specialty",
            "Dark Consortium",
            "Sovereign Guardianship",
        ]

    @functools.cached_property
    def civics_the_machine_age(self) -> List[str]:
        return [
            "Genesis Guides",
            "Rapid Replicator",
            "Static Research Analysis",
            "Warbots",
            "Natural Design",
            "Diplomatic Protocols",
            "Genesis Architects",
            "Obsessional Directive",
            "Tactical Algorithms",
        ]

    @functools.cached_property
    def civics_cosmic_storms(self) -> List[str]:
        return [
            "Astrometeorology",
            "Storm Devotion",
            "Planetscapers",
        ]

    @functools.cached_property
    def civics_utopia(self) -> List[str]:
        return [
            "Fanatic Purifiers",
            "Ascetic",
            "Divided Attention",
            "Elevational Contemplations",
            "Natural Neural Network",
            "One Mind",
            "Pooled Knowledge",
            "Strength of Legions",
            "Subspace Ephapse",
            "Subsumed Will",
            "Devouring Swarm",
        ]

    @functools.cached_property
    def civics_apocalypse(self) -> List[str]:
        return [
            "Barbaric Despoilers",
        ]

    @functools.cached_property
    def civics_aquatics(self) -> List[str]:
        return [
            "Anglers",
            "Marine Machines",
        ]

    @functools.cached_property
    def civics_grand_archive(self) -> List[str]:
        return [
            "Galactic Curators",
            "Beastmasters",
        ]

    @functools.cached_property
    def civics_synthetic_dawn(self) -> List[str]:
        return [
            "Determined Exterminator",
            "Driven Assimilator",
            "Rogue Servitor",
        ]

    @functools.cached_property
    def civics_utopia_or_astral_planes(self) -> List[str]:
        return [
            "Ascensionists",
        ]

    @functools.cached_property
    def civics_megacorp_and_utopia_or_astral_planes(self) -> List[str]:
        return [
            "Gigacorp",
        ]

    @functools.cached_property
    def civics_megacorp_and_plantoids(self) -> List[str]:
        return [
            "Catalytic Recyclers",
        ]

    @functools.cached_property
    def civics_megacorp_and_humanoids(self) -> List[str]:
        return [
            "Corporate Hedonism",
            "Mastercraft Inc.",
        ]

    @functools.cached_property
    def civics_megacorp_and_federations(self) -> List[str]:
        return [
            "Public Relations Specialists",
        ]

    @functools.cached_property
    def civics_megacorp_and_necroids(self) -> List[str]:
        return [
            "Corporate Death Cult",
            "Permanent Employment",
        ]

    @functools.cached_property
    def civics_megacorp_and_toxoids(self) -> List[str]:
        return [
            "Mutagenic Luxury",
            "Luxury Lubrication Pools",
            "Refurbishment Division",
            "Shareholder Values",
        ]

    @functools.cached_property
    def civics_megacorp_and_first_contact(self) -> List[str]:
        return [
            "Privatized Exploration",
        ]

    @functools.cached_property
    def civics_megacorp_and_galactic_paragons(self) -> List[str]:
        return [
            "Precision Cogs",
            "Knowledge Mentorship",
            "Letters of Marque",
            "Pharma State",
        ]

    @functools.cached_property
    def civics_megacorp_and_astral_planes(self) -> List[str]:
        return [
            "Dimensional Enterprise",
            "Hyperspace Traders",
            "Corporate Protectorate",
            "Shadow Corporation",
        ]

    @functools.cached_property
    def civics_megacorp_and_the_machine_age(self) -> List[str]:
        return [
            "Astrogenesis Technologies",
            "Augmentation Bazaars",
        ]

    @functools.cached_property
    def civics_megacorp_and_cosmic_storms(self) -> List[str]:
        return [
            "Weather Exploitation",
            "Storm Inluencers",
            "Geo-Engineering",
        ]

    @functools.cached_property
    def civics_megacorp_and_aquatics(self) -> List[str]:
        return [
            "Trawling Operations",
            "Maritime Robotics",
        ]

    @functools.cached_property
    def civics_megacorp_and_grand_archive(self) -> List[str]:
        return [
            "Antiquarian Expertise",
            "Space Ranchers",
        ]

    @functools.cached_property
    def civics_utopia_and_plantoids(self) -> List[str]:
        return [
            "Organic Reprocessing",
            "Mycorrhizal Ideal",
        ]

    @functools.cached_property
    def civics_utopia_and_lithoids(self) -> List[str]:
        return [
            "Void Hive",
            "Terravore",
        ]

    @functools.cached_property
    def civics_utopia_and_federations(self) -> List[str]:
        return [
            "Empath",
        ]

    @functools.cached_property
    def civics_utopia_and_necroids(self) -> List[str]:
        return [
            "Cordyceptic Drones",
            "Memorialist",
        ]

    @functools.cached_property
    def civics_utopia_and_toxoids(self) -> List[str]:
        return [
            "Permutation Pools",
        ]

    @functools.cached_property
    def civics_utopia_and_galactic_paragons(self) -> List[str]:
        return [
            "Autonomous Drones",
            "Neural Vaults",
        ]

    @functools.cached_property
    def civics_utopia_and_astral_planes(self) -> List[str]:
        return [
            "Hyperspace Synchronicity",
            "Guardian Cluster",
        ]

    @functools.cached_property
    def civics_utopia_and_the_machine_age(self) -> List[str]:
        return [
            "Genesis Symbiotes",
            "Innate Design",
        ]

    @functools.cached_property
    def civics_utopia_and_cosmic_storms(self) -> List[str]:
        return [
            "Climate Modeling",
            "Cultivation Drones",
        ]

    @functools.cached_property
    def civics_utopia_and_first_contact(self) -> List[str]:
        return [
            "Stargazers",
        ]

    @functools.cached_property
    def civics_utopia_and_grand_archive(self) -> List[str]:
        return [
            "Caretaker Network",
            "Wild Swarm",
        ]

    @functools.cached_property
    def civics_synthetic_dawn_or_the_machine_age(self) -> List[str]:
        return [
            "Built to Last",
            "Constructobot",
            "Delegated Functions",
            "Factory Overclocking",
            "Introspective",
            "Maintenance Protocols",
            "OTA Updates",
            "Rapid Replicator",
            "Rockbreakers",
            "Static Research Analysis",
            "Unitary Cohesion",
            "Warbots",
            "Zero-Waste Protocols",
        ]

    @functools.cached_property
    def civics_utopia_or_astral_planes_and_synthetic_dawn_or_the_machine_age(self) -> List[str]:
        return [
            "Elevational Hypotheses",
        ]

    @functools.cached_property
    def civics_plantoids_and_synthetic_dawn_or_the_machine_age(self) -> List[str]:
        return [
            "Organic Retrofitting",
        ]

    @functools.cached_property
    def civics_megacorp_and_synthetic_dawn_or_the_machine_age(self) -> List[str]:
        return [
            "Astro-Mining Drones",
        ]

    @functools.cached_property
    def civics_necroids_and_synthetic_dawn_or_the_machine_age(self) -> List[str]:
        return [
            "Memorialist",
        ]

    @functools.cached_property
    def civics_nemesis_and_synthetic_dawn_or_the_machine_age(self) -> List[str]:
        return [
            "Spyware Directives",
        ]

    @functools.cached_property
    def civics_toxoids_and_synthetic_dawn_or_the_machine_age(self) -> List[str]:
        return [
            "Hyper Lubrication Basin",
        ]

    @functools.cached_property
    def civics_first_contact_and_synthetic_dawn_or_the_machine_age(self) -> List[str]:
        return [
            "Exploration Protocols",
        ]

    @functools.cached_property
    def civics_galactic_paragons_and_synthetic_dawn_or_the_machine_age(self) -> List[str]:
        return [
            "Experience Cache",
            "Soverign Circuits",
        ]

    @functools.cached_property
    def civics_astral_planes_and_synthetic_dawn_or_the_machine_age(self) -> List[str]:
        return [
            "Hyperspace Synchronicity",
            "Guardian Matrix",
        ]

    @functools.cached_property
    def civics_cosmic_storms_and_synthetic_dawn_or_the_machine_age(self) -> List[str]:
        return [
            "Climate Modeling",
            "Gardening Protocols",
        ]

    @functools.cached_property
    def civics_grand_archive_and_synthetic_dawn_or_the_machine_age(self) -> List[str]:
        return [
            "Caretaker Network",
            "Biodrones",
        ]

    def civics(self) -> List[str]:
        civics: List[str] = self.civics_base[:]

        if self.has_dlc_plantoids:
            civics.extend(self.civics_plantoids)
        if self.has_dlc_humanoids:
            civics.extend(self.civics_humanoids)
        if self.has_dlc_megacorp:
            civics.extend(self.civics_megacorp)
        if self.has_dlc_necroids:
            civics.extend(self.civics_necroids)
        if self.has_dlc_toxoids:
            civics.extend(self.civics_toxoids)
        if self.has_dlc_first_contact:
            civics.extend(self.civics_first_contact)
        if self.has_dlc_galactic_paragons:
            civics.extend(self.civics_galactic_paragons)
        if self.has_dlc_astral_planes:
            civics.extend(self.civics_astral_planes)
        if self.has_dlc_the_machine_age:
            civics.extend(self.civics_the_machine_age)
        if self.has_dlc_cosmic_storms:
            civics.extend(self.civics_cosmic_storms)
        if self.has_dlc_utopia:
            civics.extend(self.civics_utopia)
        if self.has_dlc_apocalypse:
            civics.extend(self.civics_apocalypse)
        if self.has_dlc_aquatics:
            civics.extend(self.civics_aquatics)
        if self.has_dlc_grand_archive:
            civics.extend(self.civics_grand_archive)
        if self.has_dlc_synthetic_dawn:
            civics.extend(self.civics_synthetic_dawn)
        if self.has_dlc_utopia or self.has_dlc_astral_planes:
            civics.extend(self.civics_utopia_or_astral_planes)
        if self.has_dlc_megacorp and (self.has_dlc_utopia or self.has_dlc_astral_planes):
            civics.extend(self.civics_megacorp_and_utopia_or_astral_planes)
        if self.has_dlc_megacorp and self.has_dlc_plantoids:
            civics.extend(self.civics_megacorp_and_plantoids)
        if self.has_dlc_megacorp and self.has_dlc_humanoids:
            civics.extend(self.civics_megacorp_and_humanoids)
        if self.has_dlc_megacorp and self.has_dlc_federations:
            civics.extend(self.civics_megacorp_and_federations)
        if self.has_dlc_megacorp and self.has_dlc_necroids:
            civics.extend(self.civics_megacorp_and_necroids)
        if self.has_dlc_megacorp and self.has_dlc_toxoids:
            civics.extend(self.civics_megacorp_and_toxoids)
        if self.has_dlc_megacorp and self.has_dlc_first_contact:
            civics.extend(self.civics_megacorp_and_first_contact)
        if self.has_dlc_megacorp and self.has_dlc_galactic_paragons:
            civics.extend(self.civics_megacorp_and_galactic_paragons)
        if self.has_dlc_megacorp and self.has_dlc_astral_planes:
            civics.extend(self.civics_megacorp_and_astral_planes)
        if self.has_dlc_megacorp and self.has_dlc_the_machine_age:
            civics.extend(self.civics_megacorp_and_the_machine_age)
        if self.has_dlc_megacorp and self.has_dlc_cosmic_storms:
            civics.extend(self.civics_megacorp_and_cosmic_storms)
        if self.has_dlc_megacorp and self.has_dlc_aquatics:
            civics.extend(self.civics_megacorp_and_aquatics)
        if self.has_dlc_megacorp and self.has_dlc_grand_archive:
            civics.extend(self.civics_megacorp_and_grand_archive)
        if self.has_dlc_utopia and self.has_dlc_plantoids:
            civics.extend(self.civics_utopia_and_plantoids)
        if self.has_dlc_utopia and self.has_dlc_lithoids:
            civics.extend(self.civics_utopia_and_lithoids)
        if self.has_dlc_utopia and self.has_dlc_federations:
            civics.extend(self.civics_utopia_and_federations)
        if self.has_dlc_utopia and self.has_dlc_necroids:
            civics.extend(self.civics_utopia_and_necroids)
        if self.has_dlc_utopia and self.has_dlc_toxoids:
            civics.extend(self.civics_utopia_and_toxoids)
        if self.has_dlc_utopia and self.has_dlc_galactic_paragons:
            civics.extend(self.civics_utopia_and_galactic_paragons)
        if self.has_dlc_utopia and self.has_dlc_astral_planes:
            civics.extend(self.civics_utopia_and_astral_planes)
        if self.has_dlc_utopia and self.has_dlc_the_machine_age:
            civics.extend(self.civics_utopia_and_the_machine_age)
        if self.has_dlc_utopia and self.has_dlc_cosmic_storms:
            civics.extend(self.civics_utopia_and_cosmic_storms)
        if self.has_dlc_utopia and self.has_dlc_first_contact:
            civics.extend(self.civics_utopia_and_first_contact)
        if self.has_dlc_utopia and self.has_dlc_grand_archive:
            civics.extend(self.civics_utopia_and_grand_archive)
        if self.has_dlc_synthetic_dawn or self.has_dlc_the_machine_age:
            civics.extend(self.civics_synthetic_dawn_or_the_machine_age)
        if (self.has_dlc_utopia or self.has_dlc_astral_planes) and (self.has_dlc_synthetic_dawn or self.has_dlc_the_machine_age):
            civics.extend(self.civics_utopia_or_astral_planes_and_synthetic_dawn_or_the_machine_age)
        if self.has_dlc_plantoids and (self.has_dlc_synthetic_dawn or self.has_dlc_the_machine_age):
            civics.extend(self.civics_plantoids_and_synthetic_dawn_or_the_machine_age)
        if self.has_dlc_megacorp and (self.has_dlc_synthetic_dawn or self.has_dlc_the_machine_age):
            civics.extend(self.civics_megacorp_and_synthetic_dawn_or_the_machine_age)
        if self.has_dlc_necroids and (self.has_dlc_synthetic_dawn or self.has_dlc_the_machine_age):
            civics.extend(self.civics_necroids_and_synthetic_dawn_or_the_machine_age)
        if self.has_dlc_nemesis and (self.has_dlc_synthetic_dawn or self.has_dlc_the_machine_age):
            civics.extend(self.civics_nemesis_and_synthetic_dawn_or_the_machine_age)
        if self.has_dlc_toxoids and (self.has_dlc_synthetic_dawn or self.has_dlc_the_machine_age):
            civics.extend(self.civics_toxoids_and_synthetic_dawn_or_the_machine_age)
        if self.has_dlc_first_contact and (self.has_dlc_synthetic_dawn or self.has_dlc_the_machine_age):
            civics.extend(self.civics_first_contact_and_synthetic_dawn_or_the_machine_age)
        if self.has_dlc_galactic_paragons and (self.has_dlc_synthetic_dawn or self.has_dlc_the_machine_age):
            civics.extend(self.civics_galactic_paragons_and_synthetic_dawn_or_the_machine_age)
        if self.has_dlc_astral_planes and (self.has_dlc_synthetic_dawn or self.has_dlc_the_machine_age):
            civics.extend(self.civics_astral_planes_and_synthetic_dawn_or_the_machine_age)
        if self.has_dlc_cosmic_storms and (self.has_dlc_synthetic_dawn or self.has_dlc_the_machine_age):
            civics.extend(self.civics_cosmic_storms_and_synthetic_dawn_or_the_machine_age)
        if self.has_dlc_grand_archive and (self.has_dlc_synthetic_dawn or self.has_dlc_the_machine_age):
            civics.extend(self.civics_grand_archive_and_synthetic_dawn_or_the_machine_age)

        return sorted(civics)

    @functools.cached_property
    def preset_empires_base(self) -> List[str]:
        return [
            "United Nations of Earth",
            "Commonwealth of Man",
            "Tzynn Empire",
            "Kingdom of Yondarim",
            "Glebsig Foundation",
            "Jehetma Dominion",
            "Scyldari Confederacy",
            "Kel-Azaan Republic",
            "Blorg Commonality",
        ]

    @functools.cached_property
    def preset_empires_synthetic_dawn(self) -> List[str]:
        return [
            "Earth Custodianship",
            "XT-489 Eliminator",
            "Voor Technocracy",
        ]

    @functools.cached_property
    def preset_empires_plantoids(self) -> List[str]:
        return [
            "Blooms of Gaea",
            "Maweer Caretakers",
        ]

    @functools.cached_property
    def preset_empires_utopia(self) -> List[str]:
        return [
            "Xanid Suzerainty",
            "Lokken Mechanists",
            "Ix'Idar Star Collective",
            "Tebrid Homolog",
        ]

    @functools.cached_property
    def preset_empires_megacorp(self) -> List[str]:
        return [
            "Orbis Customer Synergies",
            "Chinorr Combine",
            "Hazbuzan Syndicate",
            "Federated Theian Preservers",
        ]

    @functools.cached_property
    def preset_empires_lithoids(self) -> List[str]:
        return [
            "Keepers of Ave'brenn",
            "Pasharti Absorbers",
        ]

    @functools.cached_property
    def preset_empires_necroids(self) -> List[str]:
        return [
            "Sathyrelian Bliss",
        ]

    @functools.cached_property
    def preset_empires_aquatics(self) -> List[str]:
        return [
            "Gorthikan Alliance",
        ]

    @functools.cached_property
    def preset_empires_toxoids(self) -> List[str]:
        return [
            "Rotoavuul High Suzerainty",
            "Roccan Resistance",
        ]

    @functools.cached_property
    def preset_empires_first_contact(self) -> List[str]:
        return [
            "Free Peoples of the Fall",
            "Certeran Covenant",
        ]

    @functools.cached_property
    def preset_empires_astral_planes(self) -> List[str]:
        return [
            "Guardianship of Nyrr",
            "Basidrix Cyber Ecclesia",
        ]

    @functools.cached_property
    def preset_empires_the_machine_age(self) -> List[str]:
        return [
            "Lacertan Techno-Protectorate",
            "Sunbuilt Uplifters",
            "Yatunan Radicals",
        ]

    @functools.cached_property
    def preset_empires_cosmic_storms(self) -> List[str]:
        return [
            "Oviron Lodge",
        ]

    @functools.cached_property
    def preset_empires_grand_archive(self) -> List[str]:
        return [
            "Graparx Primal Stalkers",
            "Iferyx Amalgamated Fleets",
        ]

    def preset_empires(self) -> List[str]:
        preset_empires: List[str] = self.preset_empires_base[:]

        if self.has_dlc_synthetic_dawn:
            preset_empires.extend(self.preset_empires_synthetic_dawn)
        if self.has_dlc_plantoids:
            preset_empires.extend(self.preset_empires_plantoids)
        if self.has_dlc_utopia:
            preset_empires.extend(self.preset_empires_utopia)
        if self.has_dlc_megacorp:
            preset_empires.extend(self.preset_empires_megacorp)
        if self.has_dlc_lithoids:
            preset_empires.extend(self.preset_empires_lithoids)
        if self.has_dlc_necroids:
            preset_empires.extend(self.preset_empires_necroids)
        if self.has_dlc_aquatics:
            preset_empires.extend(self.preset_empires_aquatics)
        if self.has_dlc_toxoids:
            preset_empires.extend(self.preset_empires_toxoids)
        if self.has_dlc_first_contact:
            preset_empires.extend(self.preset_empires_first_contact)
        if self.has_dlc_astral_planes:
            preset_empires.extend(self.preset_empires_astral_planes)
        if self.has_dlc_the_machine_age:
            preset_empires.extend(self.preset_empires_the_machine_age)
        if self.has_dlc_cosmic_storms:
            preset_empires.extend(self.preset_empires_cosmic_storms)
        if self.has_dlc_grand_archive:
            preset_empires.extend(self.preset_empires_grand_archive)

        return sorted(preset_empires)

    @functools.cached_property
    def traits_advanced_genetics_base(self) -> List[str]:
        return [
            "Delicious",
            "Felsic",
            "Natural Machinist",
            "Nerve Stapled",
            "Vat-Grown",
            "Erudite",
            "Fertile",
            "Robust",
        ]

    @functools.cached_property
    def traits_advanced_genetics_toxoids(self) -> List[str]:
        return [
            "Exotic Metabolism",
        ]

    def traits_advanced_genetics(self) -> List[str]:
        traits_advanced_genetics: List[str] = self.traits_advanced_genetics_base[:]

        if self.has_dlc_toxoids:
            traits_advanced_genetics.extend(self.traits_advanced_genetics_toxoids)

        return sorted(traits_advanced_genetics)

    @staticmethod
    def traits_organic_leviathan() -> List[str]:
        return [
            "Drake-Scaled",
            "Polymelic",
            "Voidling",
        ]

    @functools.cached_property
    def traits_cyborg_base(self) -> List[str]:
        return [
            "Universal Augmentations",
            "Superconductive",
            "Power Drills",
            "Harvesters",
            "Double Jointed",
            "Durable",
            "Efficient Processors",
            "Enhanced Memory",
            "Learning Algorithms",
            "Logic Engines",
            "Loyalty Circuits",
            "Streamlined Protocols",
            "Trading Algorithms",
        ]

    @functools.cached_property
    def traits_cyborg_the_machine_age(self) -> List[str]:
        return [
            "Embellished Augments",
            "Integrated Weaponry",
            "Bionic Engineers",
            "Bionic Physicists",
            "Bionic Sociologists",
            "Dry Climate Mods",
            "Wet Climate Mods",
            "Frozen Climate Mods",
        ]

    def traits_cyborg(self) -> List[str]:
        traits_cyborg: List[str] = self.traits_cyborg_base[:]

        if self.has_dlc_the_machine_age:
            traits_cyborg.extend(self.traits_cyborg_the_machine_age)

        return sorted(traits_cyborg)

    @staticmethod
    def traits_mechanical_leviatan() -> List[str]:
        return [
            "Ancient Deadnought",
            "Enigmatic Fortress",
            "Infinity Sphere",
            "Scavenger Bot",
        ]

    @staticmethod
    def population_count_range() -> range:
        return range(10, 51)

    @staticmethod
    def civilian_ship_count_range() -> range:
        return range(3, 9)

    @staticmethod
    def civilian_ship_types() -> List[str]:
        return [
            "Science",
            "Construction",
            "Transport",
        ]

    @staticmethod
    def habitable_worlds() -> List[str]:
        return [
            "Desert World",
            "Arid World",
            "Savanna World",
            "Ocean World",
            "Continental World",
            "Tropical World",
            "Arctic World",
            "Alpine World",
            "Tundra World",
            "Gaia World",
            "Tomb World",
            "Relic World",
            "Ring World",
            "Orbital Habitat",
        ]

    @staticmethod
    def colony_count_range() -> range:
        return range(1, 4)

    @functools.cached_property
    def uninhabitable_worlds_base(self) -> List[str]:
        return [
            "Asteroid",
            "Ice Asteroid",
            "Crystaline Asteroid",
            "Barren World",
            "Barren World (Cold)",
            "Broken World",
            "Frozen World",
            "Gas Giant",
            "Molten World",
            "Toxic World",
        ]

    @functools.cached_property
    def uninhabitable_worlds_astral_planes(self) -> List[str]:
        return [
            "Astral Scar",
        ]

    def uninhabitable_worlds(self) -> List[str]:
        uninhabitable_worlds: List[str] = self.uninhabitable_worlds_base[:]

        if self.has_dlc_astral_planes:
            uninhabitable_worlds.extend(self.uninhabitable_worlds_astral_planes)

        return sorted(uninhabitable_worlds)

    @staticmethod
    def survey_world_count_range() -> range:
        return range(5, 11)

    @staticmethod
    def stars() -> List[str]:
        return [
            "Class B",
            "Class A",
            "Class F",
            "Class G",
            "Class K",
            "Class M",
            "Class M Red Giant",
            "Class T Brown Dwarf",
            "Pulsar",
            "Black Hole",
            "Neutron Star",
        ]

    @staticmethod
    def survey_star_count_range() -> range:
        return range(1, 4)

    @staticmethod
    def relic_count_range() -> range:
        return range(1, 7)

    @staticmethod
    def observation_post_count_range() -> range:
        return range(1, 5)

    @functools.cached_property
    def pre_ftl_diplomacy_base(self) -> List[str]:
        return [
            "Passive Observation",
            "Aggressive Observation",
            "Revealing Our Presence",
            "Offering Societal Guidance",
            "Providing Technology",
            "Invading",
        ]

    @functools.cached_property
    def pre_ftl_diplomacy_first_contact(self) -> List[str]:
        return [
            "Forming a Commercial Agreement",
        ]

    def pre_ftl_diplomacy(self) -> List[str]:
        pre_ftl_diplomacy: List[str] = self.pre_ftl_diplomacy_base[:]

        if self.has_dlc_first_contact:
            pre_ftl_diplomacy.extend(self.pre_ftl_diplomacy_first_contact)

        return sorted(pre_ftl_diplomacy)

    @staticmethod
    def accept_deny() -> List[str]:
        return [
            "Accept",
            "Deny",
        ]

    @functools.cached_property
    def rights_base(self) -> List[str]:
        return [
            "Citizenship -- Full Citizenship",
            "Citizenship -- Residence",
            "Citizenship -- Slaves",
            "Citizenship -- Servitude",
            "Citizenship -- Undersirables",
            "Citizenship -- Machine Integration",
            "Citizenship -- Bio-Trophy",
            "Living Standards -- Chemical Bliss",
            "Living Standards -- Utopian Abundance",
            "Living Standards -- Social Welfare",
            "Living Standards -- Academic Privilege",
            "Living Standards -- Decent Conditions",
            "Living Standards -- Stratified Economy",
            "Living Standards -- Basic Subsistence",
            "Living Standards -- Non-Existent",
            "Military Service -- Full Military Service",
            "Military Service -- Soldiers Only",
            "Military Service -- Exempt",
            "Colonization Rights -- Colonization Forbidden",
            "Colonization Rights -- Colonization Allowed",
            "Population Controls -- Population Controls Enabled",
            "Population Controls -- No Population Controls",
            "Migration Controls -- Migration Controls Enabled",
            "Migration Controls -- No Migration Controls",
            "Slavery Type -- Chattel Slavery",
            "Purge Type -- Displacement",
            "Purge Type -- Extermination",
        ]

    @functools.cached_property
    def rights_utopia(self) -> List[str]:
        return [
            "Citizenship -- Assimilation",
            "Slavery Type -- Battle Thralls",
            "Slavery Type -- Domestic Servitude",
            "Slavery Type -- Indetured Servitude",
            "Slavery Type -- Livestock",
            "Purge Type -- Neutering",
            "Purge Type -- Forced Labor",
            "Purge Type -- Processing",
        ]

    @functools.cached_property
    def rights_megacorp(self) -> List[str]:
        return [
            "Living Standards -- Shared Burden",
            "Living Standards -- Employee Ownership",
        ]

    @functools.cached_property
    def rights_humanoids(self) -> List[str]:
        return [
            "Living Standards -- Decadent Lifestyle",
        ]

    @functools.cached_property
    def rights_synthetic_dawn(self) -> List[str]:
        return [
            "Slavery Type -- Grid Amalgamation",
        ]

    @functools.cached_property
    def rights_the_machine_age(self) -> List[str]:
        return [
            "Slavery Type -- Sapient Specimens",
            "Purge Type -- Maximize",
            "Purge Type -- Synaptic Service",
        ]

    @functools.cached_property
    def rights_synthetic_dawn_or_the_machine_age(self) -> List[str]:
        return [
            "Purge Type -- Chemical Processing",
        ]

    @functools.cached_property
    def rights_necroids(self) -> List[str]:
        return [
            "Purge Type -- Necrophage",
        ]

    def rights(self) -> List[str]:
        rights: List[str] = self.rights_base[:]

        if self.has_dlc_utopia:
            rights.extend(self.rights_utopia)
        if self.has_dlc_megacorp:
            rights.extend(self.rights_megacorp)
        if self.has_dlc_humanoids:
            rights.extend(self.rights_humanoids)
        if self.has_dlc_synthetic_dawn:
            rights.extend(self.rights_synthetic_dawn)
        if self.has_dlc_the_machine_age:
            rights.extend(self.rights_the_machine_age)
        if self.has_dlc_synthetic_dawn or self.has_dlc_the_machine_age:
            rights.extend(self.rights_synthetic_dawn_or_the_machine_age)
        if self.has_dlc_necroids:
            rights.extend(self.rights_necroids)

        return sorted(rights)

    @functools.cached_property
    def tradition_trees_base(self) -> List[str]:
        return [
            "Adaptability",
            "Diplomacy",
            "Discovery",
            "Domination",
            "Expansion",
            "Harmony / Synchronicity",
            "Merchantile",
            "Prosperity",
            "Supremacy",
        ]

    @functools.cached_property
    def tradition_trees_apocalypse_or_overlord(self) -> List[str]:
        return [
            "Unyielding",
        ]

    @functools.cached_property
    def tradition_trees_synthetic_dawn_or_the_machine_age(self) -> List[str]:
        return [
            "Versatility",
        ]

    @functools.cached_property
    def tradition_trees_humanoids(self) -> List[str]:
        return [
            "Enmity",
        ]

    @functools.cached_property
    def tradition_trees_federations(self) -> List[str]:
        return [
            "Politics",
        ]

    @functools.cached_property
    def tradition_trees_nemesis(self) -> List[str]:
        return [
            "Subterfuge",
        ]

    @functools.cached_property
    def tradition_trees_galactic_paragons(self) -> List[str]:
        return [
            "Aptitude",
            "Statecraft",
        ]

    @functools.cached_property
    def tradition_trees_grand_archive(self) -> List[str]:
        return [
            "Archivism",
            "Domestication",
        ]

    @functools.cached_property
    def tradition_trees_utopia(self) -> List[str]:
        return [
            "Genetics",
            "Psionics",
        ]

    @functools.cached_property
    def tradition_trees_utopia_or_the_machine_age(self) -> List[str]:
        return [
            "Cybernetics",
        ]

    @functools.cached_property
    def tradition_trees_utopia_the_machine_age_or_synthetic_dawn(self) -> List[str]:
        return [
            "Synthetics",
        ]

    @functools.cached_property
    def tradition_trees_the_machine_age(self) -> List[str]:
        return [
            "Modularity",
            "Nanotech",
            "Virtuality",
        ]

    def tradition_trees(self) -> List[str]:
        tradition_trees: List[str] = self.tradition_trees_base[:]

        if self.has_dlc_apocalypse or self.has_dlc_overlord:
            tradition_trees.extend(self.tradition_trees_apocalypse_or_overlord)
        if self.has_dlc_synthetic_dawn or self.has_dlc_the_machine_age:
            tradition_trees.extend(self.tradition_trees_synthetic_dawn_or_the_machine_age)
        if self.has_dlc_humanoids:
            tradition_trees.extend(self.tradition_trees_humanoids)
        if self.has_dlc_federations:
            tradition_trees.extend(self.tradition_trees_federations)
        if self.has_dlc_nemesis:
            tradition_trees.extend(self.tradition_trees_nemesis)
        if self.has_dlc_galactic_paragons:
            tradition_trees.extend(self.tradition_trees_galactic_paragons)
        if self.has_dlc_grand_archive:
            tradition_trees.extend(self.tradition_trees_grand_archive)
        if self.has_dlc_utopia:
            tradition_trees.extend(self.tradition_trees_utopia)
        if self.has_dlc_utopia or self.has_dlc_the_machine_age:
            tradition_trees.extend(self.tradition_trees_utopia_or_the_machine_age)
        if self.has_dlc_utopia and (self.has_dlc_the_machine_age or self.has_dlc_synthetic_dawn):
            tradition_trees.extend(self.tradition_trees_utopia_the_machine_age_or_synthetic_dawn)
        if self.has_dlc_the_machine_age:
            tradition_trees.extend(self.tradition_trees_the_machine_age)

        return sorted(tradition_trees)

    @functools.cached_property
    def ascension_perks_base(self) -> List[str]:
        return [
            "Executive Vigor",
            "Interstellar Dominion",
            "Mastery of Nature",
            "Technological Ascendancy",
            "Transcendant Learning",
            "Imperial Prerogative",
            "One Vision",
            "Shared Destiny",
            "Consecrated Worlds",
            "Eternal Vigilance",
            "Grasp the Void",
            "World Shaper",
            "Galactic Force Projection",
            "Defender of the Galaxy",
            "Galactic Contender",
        ]

    @functools.cached_property
    def ascension_perks_megacorp(self) -> List[str]:
        return [
            "Universal Transactions",
            "Xeno-Compatibility",
            "Galactic Wonders",
            "Arcology Project",
        ]

    @functools.cached_property
    def ascension_perks_apocalypse(self) -> List[str]:
        return [
            "Nihilistic Acquisition",
            "Enigmatic Engineering",
            "Colossus Project",
        ]

    @functools.cached_property
    def ascension_perks_overlord(self) -> List[str]:
        return [
            "Lord of War",
        ]

    @functools.cached_property
    def ascension_perks_necroids(self) -> List[str]:
        return [
            "Mechromancy",
        ]

    @functools.cached_property
    def ascension_perks_ancient_relics(self) -> List[str]:
        return [
            "Archaeo-Engineers",
        ]

    @functools.cached_property
    def ascension_perks_aquatics(self) -> List[str]:
        return [
            "Hydrocentric",
        ]

    @functools.cached_property
    def ascension_perks_toxoids(self) -> List[str]:
        return [
            "Detox",
        ]

    @functools.cached_property
    def ascension_perks_utopia(self) -> List[str]:
        return [
            "Voidborne",
            "Hive Worlds",
            "Master Builders",
            "Engineered Evolution",
            "Mind over Matter",
        ]

    @functools.cached_property
    def ascension_perks_synthetic_dawn(self) -> List[str]:
        return [
            "Machine Worlds",
        ]

    @functools.cached_property
    def ascension_perks_utopia_or_megacorp(self) -> List[str]:
        return [
            "Galactic Wonders",
        ]

    @functools.cached_property
    def ascension_perks_utopia_or_the_machine_age(self) -> List[str]:
        return [
            "Synthetic Evolution",
            "The Flesh is Weak / Organo-Machine Interfacing",
        ]

    @functools.cached_property
    def ascension_perks_synthetic_dawn_or_the_machine_age(self) -> List[str]:
        return [
            "Synthetic Age",
        ]

    @functools.cached_property
    def ascension_perks_nemesis(self) -> List[str]:
        return [
            "Galactic Nemesis",
        ]

    @functools.cached_property
    def ascension_perks_the_machine_age(self) -> List[str]:
        return [
            "Cosmogenesis",
            "Modularity",
            "Nanotech",
            "Virtuality",
        ]

    def ascension_perks(self) -> List[str]:
        ascension_perks: List[str] = self.ascension_perks_base[:]

        if self.has_dlc_megacorp:
            ascension_perks.extend(self.ascension_perks_megacorp)
        if self.has_dlc_apocalypse:
            ascension_perks.extend(self.ascension_perks_apocalypse)
        if self.has_dlc_overlord:
            ascension_perks.extend(self.ascension_perks_overlord)
        if self.has_dlc_necroids:
            ascension_perks.extend(self.ascension_perks_necroids)
        if self.has_dlc_ancient_relics:
            ascension_perks.extend(self.ascension_perks_ancient_relics)
        if self.has_dlc_aquatics:
            ascension_perks.extend(self.ascension_perks_aquatics)
        if self.has_dlc_toxoids:
            ascension_perks.extend(self.ascension_perks_toxoids)
        if self.has_dlc_utopia:
            ascension_perks.extend(self.ascension_perks_utopia)
        if self.has_dlc_synthetic_dawn:
            ascension_perks.extend(self.ascension_perks_synthetic_dawn)
        if self.has_dlc_utopia or self.has_dlc_megacorp:
            ascension_perks.extend(self.ascension_perks_utopia_or_megacorp)
        if self.has_dlc_utopia or self.has_dlc_the_machine_age:
            ascension_perks.extend(self.ascension_perks_utopia_or_the_machine_age)
        if self.has_dlc_synthetic_dawn or self.has_dlc_the_machine_age:
            ascension_perks.extend(self.ascension_perks_synthetic_dawn_or_the_machine_age)
        if self.has_dlc_nemesis:
            ascension_perks.extend(self.ascension_perks_nemesis)
        if self.has_dlc_the_machine_age:
            ascension_perks.extend(self.ascension_perks_the_machine_age)

        return sorted(ascension_perks)

    @functools.cached_property
    def rare_tech_base(self) -> List[str]:
        return [
            "Synchronized Defenses",
            "Autonomous Ship Intellects",
            "Curator Archaeology Lab",
            "Planetary Shields",
            "Speculative Hyperlane Breaching",
            "Subspace Drive",
            "Wormhole Stabilization",
            "Gateway Activation",
            "Gateway Construction",
            "Nutrient Replication",
            "Bio-Reactor",
            "Advanced Bio-Reactor",
            "Selected Lineages",
            "Capacity Boosters",
            "Targeted Gene Expressions",
            "Morphogenetic Field Mastery",
            "Gene Banks",
            "Subdermal Stimulation",
            "Tracking Implants",
            "Tomb World Adaptation",
            "Penal Colonies",
            "Galactic Markets",
            "Galactic Commerce Hub",
            "Interstellar Commerce Nexus",
            "Ascension Theory",
            "Psionic Theory",
            "Zro Distillation",
            "Telepathy",
            "Thought Enforcement",
            "Precognition Interface",
            "Construction Templates",
            "Fungible Circuitry",
            "Nanite Assemblers",
            "Robotic Assembly Systems",
            "Mega-Assembly Systems",
            "Improved Structural Integrity",
            "Modular Engineering",
            "Corps of Engineers",
            "Mega-Engineering",
            "Improved Titan Hulls",
            "Advanced Corvette Hulls",
            "Advanced Destroyer Hulls",
            "Advanced Cruiser Hulls",
            "Advanced Battleship Hulls",
            "Advanced Titan Hulls",
            "Sapient Combat Simulations",
            "Jump Drive",
            "Psi Jump Drives",
            "Artificial Administration",
            "L-Gate Insight",
        ]

    @functools.cached_property
    def rare_tech_first_contact(self) -> List[str]:
        return [
            "Detection Array",
            "Advanced Detection Algorithms",
            "Basic Cloaking Fields",
            "Advanced Cloaking Fields",
            "Elite Cloaking Fields",
            "Dark Matter Cloaking Fields",
            "Dark Matter Detection",
            "Psi-Phase Field Generator",
        ]

    @functools.cached_property
    def rare_tech_the_machine_age(self) -> List[str]:
        return [
            "Dyson Swarm",
            "Exponential Learning Theory",
            "Gravitic Brush",
            "Theoretical Infinity Thesis",
            "The Rules of Reality",
            "Quantum Innovation Nexus",
            "Transcendantal Innovation",
            "Transcendant Innovation Department",
            "Nascent Universes",
            "Synaptic Resonator",
            "Synaptic Validator",
            "Shrinkspace Depot",
            "Extra-Dimensional Depot",
            "Class-3 Singularity",
            "Class-4 Singularity",
            "Nourishment Complex",
            "Nourishment Center",
            "Molecular Revitalization Institute",
            "Bioregeneration Institute",
            "Synaptic Preserver",
            "Synaptic Sustainer",
            "Aspis Bastion",
            "Aspis Complex",
            "Virtual Bliss Plaza",
            "Omni-Bliss Nexus",
            "Fractal Administration Processes",
            "Quantic Administration Processes",
            "Sky Dome",
            "Empyrean Dome",
            "Justice Complex",
            "Ziggurat of Justice",
            "Synaptic Cogitator",
            "Robot Manufacturing Nexus",
            "Robot Quantum Production Hub",
            "Affluence Emporium",
            "Affluence Center",
            "Arc Furnace",
            "Scalable Reservoir Computing",
            "Quantum Drilling Plant",
            "Quantum Drilling Hub",
            "Dimensional Replicator",
            "Dimensional Fabricator",
            "Hyper-Forge",
            "Auto-Forge",
            "Riddle Escort",
            "Enigma Battlecruiser",
            "Paradox Titan",
            "Applied Infinity Thesis",
        ]

    @functools.cached_property
    def rare_tech_astral_planes(self) -> List[str]:
        return [
            "Rift Sphere",
        ]

    @functools.cached_property
    def rare_tech_apocalypse(self) -> List[str]:
        return [
            "Global Pacification",
            "Neutron Sweeping",
            "Divine Stimulus",
            "Core Cracking",
            "Atmospheric Nanobot Dispersal",
        ]

    @functools.cached_property
    def rare_tech_overlord(self) -> List[str]:
        return [
            "Hyper Relays",
            "Quantum Catapult",
        ]

    @functools.cached_property
    def rare_tech_cosmic_storms(self) -> List[str]:
        return [
            "Advanced Storm Manipulation",
        ]

    @functools.cached_property
    def rare_tech_plantoids(self) -> List[str]:
        return [
            "Botanical Transgenesis",
        ]

    @functools.cached_property
    def rare_tech_lithoids(self) -> List[str]:
        return [
            "Silicate Transgenesis",
        ]

    @functools.cached_property
    def rare_tech_leviathans_distant_stars_ancient_relics_or_aquatics(self) -> List[str]:
        return [
            "Leviathan Transgenesis",
        ]

    @functools.cached_property
    def rare_tech_utopia(self) -> List[str]:
        return [
            "Science Nexus",
            "Sentry Array",
            "Gene Seed Purification",
            "Habitat Expansion",
            "Advanced Space Habitation",
            "Advanced Node Culling",
        ]

    @functools.cached_property
    def rare_tech_federations(self) -> List[str]:
        return [
            "Mega Shipyard",
            "Juggernaut",
        ]

    @functools.cached_property
    def rare_tech_megacorp(self) -> List[str]:
        return [
            "Strategic Coordination Center",
            "Interstellar Assembly",
            "Mega Art Installation",
        ]

    @functools.cached_property
    def rare_tech_ancient_relics(self) -> List[str]:
        return [
            "Archaeostudies",
            "Arcane Deciphering",
            "Curated Archaeology Lab",
            "Ancient Suspension Field",
            "Ancient Pulse Armor",
            "Ancient Target Scrambler",
            "Ancient Ruination Glare",
            "Devolving Beam",
            "Ancient Macro Batteries",
            "Ancient Cavitation Collapser",
            "Ancient Defensive Web Slinger",
            "Ancient Nano-Missile Cloud Launcher",
            "Ancient Saturator Artillery",
            "Ancient Drill Drones",
            "Ancient Rampart",
            "Ancient Shield Overcharger",
            "Ancient Refinery",
        ]

    @functools.cached_property
    def rare_tech_the_machine_age_or_synthetic_dawn(self) -> List[str]:
        return [
            "Biomechanics",
            "Advanced Node Reformatting",
        ]

    @functools.cached_property
    def rare_tech_distant_stars(self) -> List[str]:
        return [
            "Nanite Transmutation",
            "L-Gate Activation",
        ]

    def rare_tech(self) -> List[str]:
        rare_tech: List[str] = self.rare_tech_base[:]

        if self.has_dlc_first_contact:
            rare_tech.extend(self.rare_tech_first_contact)
        if self.has_dlc_the_machine_age:
            rare_tech.extend(self.rare_tech_the_machine_age)
        if self.has_dlc_astral_planes:
            rare_tech.extend(self.rare_tech_astral_planes)
        if self.has_dlc_apocalypse:
            rare_tech.extend(self.rare_tech_apocalypse)
        if self.has_dlc_overlord:
            rare_tech.extend(self.rare_tech_overlord)
        if self.has_dlc_cosmic_storms:
            rare_tech.extend(self.rare_tech_cosmic_storms)
        if self.has_dlc_plantoids:
            rare_tech.extend(self.rare_tech_plantoids)
        if self.has_dlc_lithoids:
            rare_tech.extend(self.rare_tech_lithoids)
        if self.has_dlc_leviathans or self.has_dlc_distant_stars or self.has_dlc_ancient_relics or self.has_dlc_aquatics:
            rare_tech.extend(self.rare_tech_leviathans_distant_stars_ancient_relics_or_aquatics)
        if self.has_dlc_utopia:
            rare_tech.extend(self.rare_tech_utopia)
        if self.has_dlc_federations:
            rare_tech.extend(self.rare_tech_federations)
        if self.has_dlc_megacorp:
            rare_tech.extend(self.rare_tech_megacorp)
        if self.has_dlc_ancient_relics:
            rare_tech.extend(self.rare_tech_ancient_relics)
        if self.has_dlc_the_machine_age or self.has_dlc_synthetic_dawn:
            rare_tech.extend(self.rare_tech_the_machine_age_or_synthetic_dawn)
        if self.has_dlc_distant_stars:
            rare_tech.extend(self.rare_tech_distant_stars)

        return sorted(rare_tech)

    @functools.cached_property
    def edicts_base(self) -> List[str]:
        return [
            "Fortify the Border",
            "Nutritional Plentitude / Expanded Breeding Program",
            "Fleet Supremacy",
            "Capacity Subsidies",
            "Mining Subsidies",
            "Farming Subsidies",
            "Forge Subsidies",
            "Industrial Subsidies",
            "Synaptic Reinforcement",
            "Tracking Implants",
            "Thought Enforcement",
            "Bureau of Espionage",
            "Observation Instinct",
            "Covert Analysis Algorithm",
            "Map the Stars",
            "Diplomatic Grants",
            "Industrial Maintenance",
            "Research Subsidies",
            "Extended Shifts",
            "Drone Overdrive",
            "Enhanced Surveillance",
            "Greater Than Ourselves",
            "Evacuation Protocols",
            "Damn the Consequences",
            "Encourage Political Thought",
            "Information Quarantine",
            "Peace Festivals",
            "Veneration of Saints",
            "Land of Opportunity",
            "A Grand Fleet",
            "Desperate Measures",
            "Fortress Proclamation",
            "Omnifarious Acquisition",
            "Scientific Revolution",
            "Will to Power",
            "Hearts and Minds",
            "Architectural Renaissance",
            "Terraforming Gases",
            "Crystalline Sensors",
            "Volatile Land Clearance",
            "Exotic Gases as Fuel",
            "Exotic Gases for Shield Boosters",
            "Focusing Crystals",
            "Volatile Ammunition",
            "Volatile Explosives",
            "Volatile Reactive Armor",
            "Living Metal Mega-Construction",
            "Nanite Actuators",
            "Sight Beyond Sight",
            "Zro Additives",
            "Zro Catalysis",
            "Inner Focus",
            "Education Campaign",
            "Recycling Campaign",
            "Fear Campaign",
            "Machine Learning Campaign",
            "Learning Campaign",
            "War Drone Campaign",
            "Automated Disinfection",
        ]

    @functools.cached_property
    def edicts_cosmic_storms(self) -> List[str]:
        return [
            "Storm Attraction Field",
            "Storm Repulsion Field",
            "Hunker Down Protocols",
        ]

    @functools.cached_property
    def edicts_grand_archive(self) -> List[str]:
        return [
            "Decentralized Research",
            "Beasts of Burden",
            "Crack the Whip",
            "Creature Welfare",
            "Space Fauna Exhibition",
            "Biological Overdrive",
            "Exotic Neural Network",
            "Self-Preservation Instincts",
        ]

    @functools.cached_property
    def edicts_megacorp(self) -> List[str]:
        return [
            "Numistic Visualization",
        ]

    @functools.cached_property
    def edicts_the_machine_age(self) -> List[str]:
        return [
            "Legislative Chorus",
            "Self-Preservation Override",
            "Battle Royale",
            "Stately Acclaim",
            "Self-Indictment Protocol",
            "Love Letter Virus",
            "Levied Experience",
            "Neurocasted Spectacles",
            "Customer Insights",
            "Rolling Updates",
            "Hive Mind Outreach",
            "Hyper-Stimulants",
            "Integrated Mega-Construction",
            "Aggregated Memory",
            "Choral Harmony",
            "A Virtuous Hammering",
            "The Crusade of Steel",
            "The Labored Masses",
            "The Song of Knowledge",
            "Lessons of Harmony",
            "Coordinated Nanocomplexes",
            "Nano-Operated Supply Chains",
            "Nanoconnected Generators",
        ]

    @functools.cached_property
    def edicts_astral_planes(self) -> List[str]:
        return [
            "Shadow Matrix",
            "Baryonic Insight",
            "Obsidian Veil",
            "Dark Matter Forging",
            "Dark Matter Unraveling",
            "Astral Binding",
            "Astral Shielding",
            "Dimensional Artificing",
            "Astral Cloaking",
        ]

    @functools.cached_property
    def edicts_necroids(self) -> List[str]:
        return [
            "Harmony",
            "Togetherness",
            "Bounty",
        ]

    def edicts(self) -> List[str]:
        edicts: List[str] = self.edicts_base[:]

        if self.has_dlc_cosmic_storms:
            edicts.extend(self.edicts_cosmic_storms)
        if self.has_dlc_grand_archive:
            edicts.extend(self.edicts_grand_archive)
        if self.has_dlc_megacorp:
            edicts.extend(self.edicts_megacorp)
        if self.has_dlc_the_machine_age:
            edicts.extend(self.edicts_the_machine_age)
        if self.has_dlc_astral_planes:
            edicts.extend(self.edicts_astral_planes)
        if self.has_dlc_necroids:
            edicts.extend(self.edicts_necroids)

        return sorted(edicts)

    @functools.cached_property
    def policies_base(self) -> List[str]:
        return [
            "Diplomatic Stance -- Cooperative",
            "Diplomatic Stance -- Expansionist",
            "Diplomatic Stance -- Isolationist",
            "Diplomatic Stance -- Belligerent",
            "Diplomatic Stance -- Mercantile",
            "Diplomatic Stance -- Supremacist",
            "Diplomatic Stance -- Antagonistic",
            "Diplomatic Stance -- Purification",
            "Diplomatic Stance -- Hunger",
            "Diplomatic Stance -- Extermination",
            "First Contact Protocol -- Proactive",
            "First Contact Protocol -- Cautious",
            "First Contact Protocol -- Aggressive",
            "War Philosophy -- Unrestricted Wars",
            "War Philosophy -- Liberation Wars",
            "War Philosophy -- Defensive Wars",
            "Subjugation War Terms -- Oppressive",
            "Subjugation War Terms -- Balanced",
            "Subjugation War Terms -- Benevolent",
            "War Doctrine -- Defense in Depth",
            "War Doctrine -- Hit and Run",
            "War Doctrine -- Rapid Deployment",
            "War Doctrine -- No Retreat",
            "Orbital Bombardment -- Selective",
            "Orbital Bombardment -- Indiscriminate",
            "Orbital Bombardment -- Armageddon",
            "Pre-FTL Interface -- Non-Interference",
            "Pre-FTL Interface -- Subtle Interference",
            "Pre-FTL Interface -- Active Interference",
            "Pre-FTL Interface -- Aggressive Interference",
            "Pre-FTL Enlightenment -- Prohibited",
            "Pre-FTL Enlightenment -- Covert Only",
            "Pre-FTL Enlightenment -- Allowed",
            "Resettlement -- Prohibited",
            "Resettlement -- Allowed",
            "Land Appropriation -- Prohibited",
            "Land Appropriation -- Allowed",
            "Leader Enhancement -- Natural Selection",
            "Leader Enhancement -- Selected Lineages",
            "Leader Enhancement -- Capacity Boosters",
            "Initial Border Status -- Open",
            "Initial Border Status -- Closed",
            "Economic Policy -- Civilian Economy",
            "Economic Policy -- Mixed Economy",
            "Economic Policy -- Militarized Economy",
            "Trade Policy -- Wealth Creation",
            "Trade Policy -- Consumer Benefits",
            "Trade Policy -- Marketplace of Ideas",
            "Trade Policy -- Mutual Aid",
            "Trade Policy -- Trade League",
            "Trade Policy -- Holy Covenant",
            "Production Policy -- Balanced Production",
            "Production Policy -- Extraction Focus",
            "Production Policy -- Manufacturing Focus",
            "Artificial Intelligence -- Citizen Rights",
            "Artificial Intelligence -- Servitude",
            "Artificial Intelligence -- Outlawed",
            "Robotic Workers -- Outlawed",
            "Robotic Workers -- Allowed",
            "Pre-Sapients -- Protected",
            "Pre-Sapients -- Tolerated",
            "Pre-Sapients -- Extermination",
            "Debris -- Research Debris",
            "Debris -- Scavenge Debris",
            "Debris -- Research & Salvage Debris",
            "Refugees -- No Refugees",
            "Refugees -- Citizen Species Only",
            "Refugees -- Refugees Welcome",
            "Slavery -- Prohibited",
            "Slavery -- Allowed",
            "Purge -- Prohibited",
            "Purge -- Displacement Only",
            "Purge -- Allowed",
        ]

    @functools.cached_property
    def policies_megacorp(self) -> List[str]:
        return [
            "Subjugation War Terms -- Hostile Takeover",
            "Subjugation War Terms -- Standard Acquisition",
            "Subjugation War Terms -- Negotiated Synergy",
        ]

    @functools.cached_property
    def policies_utopia(self) -> List[str]:
        return [
            "Pre-Sapients -- Hunted",
        ]

    @functools.cached_property
    def policies_grand_archive(self) -> List[str]:
        return [
            "Space Fauna Growth -- Controlled",
            "Space Fauna Growth -- Excessive",
            "Metabolic Regulation -- No Regulation",
            "Metabolic Regulation -- Nutrient Rationing",
            "Metabolic Regulation -- Growth Accelerant",
            "Exhibition Focus -- Equal Focus",
            "Exhibition Focus -- Aesthetic Wonders Focus",
            "Exhibition Focus -- Galactic History Focus",
            "Exhibition Focus -- Xeno Geology Focus",
        ]

    @functools.cached_property
    def policies_toxoids(self) -> List[str]:
        return [
            "Knightly Duties -- Questing Knights",
            "Knightly Duties -- Knight Commanders",
            "Knightly Duties -- Courtly Knights",
            "Knightly Duties -- Herald Knights",
            "Industrialism -- Full Steam Ahead",
            "Industrialism -- For Science!",
            "Industrialism -- Cleanup",
        ]

    @functools.cached_property
    def policies_the_machine_age(self) -> List[str]:
        return [
            "Cyberization Standards -- Full Cyberization",
            "Cyberization Standards -- Limited Cybernetic",
            "Synthetic Identities -- Identity Copies",
            "Synthetic Identities -- Identity Fusion",
            "Synthetic Identities -- Identity Initialization",
            "Virtual Focus -- Virtual Research Focus",
            "Virtual Focus -- Virtual Unity Focus",
            "Virtual Focus -- Virtual Leader Focus",
            "Computation Core Focus -- Production Streamlining",
            "Computation Core Focus -- Stability Analysis",
            "Computation Core Focus -- Research Processes",
        ]

    def policies(self) -> List[str]:
        policies: List[str] = self.policies_base[:]

        if self.has_dlc_megacorp:
            policies.extend(self.policies_megacorp)
        if self.has_dlc_utopia:
            policies.extend(self.policies_utopia)
        if self.has_dlc_grand_archive:
            policies.extend(self.policies_grand_archive)
        if self.has_dlc_toxoids:
            policies.extend(self.policies_toxoids)
        if self.has_dlc_the_machine_age:
            policies.extend(self.policies_the_machine_age)

        return sorted(policies)

    @functools.cached_property
    def stored_resources_base(self) -> List[str]:
        return [
            "Energy Credits",
            "Minerals",
            "Food",
            "Alloys",
            "Consumer Goods",
            "Exotic Gases",
            "Rare Crystals",
            "Volatile Motes",
            "Zro",
            "Dark Matter",
            "Living Metal",
            "Nanites",
            "Influence",
            "Unity",
        ]

    @functools.cached_property
    def stored_resources_ancient_relics(self) -> List[str]:
        return [
            "Minor Artifacts",
        ]

    @functools.cached_property
    def stored_resources_astral_planes(self) -> List[str]:
        return [
            "Astral Threads",
        ]

    def stored_resources(self) -> List[str]:
        stored_resources: List[str] = self.stored_resources_base[:]

        if self.has_dlc_ancient_relics:
            stored_resources.extend(self.stored_resources_ancient_relics)
        if self.has_dlc_astral_planes:
            stored_resources.extend(self.stored_resources_astral_planes)

        return sorted(stored_resources)

    @staticmethod
    def basis_resources() -> List[str]:
        return [
            "Energy Credits",
            "Minerals",
            "Food",
        ]

    @staticmethod
    def basic_resource_income_range() -> range:
        return range(300, 501)

    @staticmethod
    def advanced_resources() -> List[str]:
        return [
            "Alloys",
            "Consumer Goods",
        ]

    @staticmethod
    def advanced_resource_income_range() -> range:
        return range(100, 251)

    @staticmethod
    def strategic_resources() -> List[str]:
        return [
            "Exotic Gases",
            "Rare Crystals",
            "Volatile Motes",
            "Unity",
            "Trade Value",
        ]

    @staticmethod
    def strategic_resource_income_range() -> range:
        return range(10, 51)

    @staticmethod
    def rare_resources() -> List[str]:
        return [
            "Zro",
            "Dark Matter",
            "Living Metal",
            "Nanites",
            "Influence",
        ]

    @staticmethod
    def rare_resource_income_range() -> range:
        return range(5, 11)

    @staticmethod
    def research_types() -> List[str]:
        return [
            "Physics",
            "Society",
            "Engineering",
        ]

    @functools.cached_property
    def buildings_base(self) -> List[str]:
        return [
            "Research Labs",
            "Research Complexes",
            "Advanced Research Complexes",
            "Administrative Offices",
            "Administrative Park",
            "Administrative Complex",
            "Temple",
            "Holotemple",
            "Sacred Nexus",
            "Sacrificial Temple",
            "Grim Holotemple",
            "Temple of Grand Sacrifice",
            "Synaptic Nodes",
            "Synaptic Clusters",
            "Confluence of Thought",
            "Uplink Node",
            "Network Junction",
            "System Conflux",
            "Organic Sanctuary",
            "Organic Paradise",
            "Holo-Theatres",
            "Hyper-Entertainment Forums",
            "Commercial Zones",
            "Commerce Megaplexes",
            "Hydroponics Farms",
            "Luxury Residences",
            "Paradise Dome",
            "Communal Housing",
            "Utopian Communal Housing",
            "Hive Warren",
            "Expanded Warren",
            "Drone Storage",
            "Upgraded Drone Storage",
            "Stronghold",
            "Fortress",
            "Precinct Houses",
            "Hall of Judgment",
            "Sentinel Posts",
            "Chemical Plants",
            "Exotic Gas Refineries",
            "Synthetic Crystal Plants",
            "Kha'lanka Crystal Plant",
        ]

    @functools.cached_property
    def buildings_the_machine_age(self) -> List[str]:
        return [
            "Nanite Research Facility",
            "Nanite Research Complex",
            "Nanotech Cauldron",
        ]

    def buildings(self) -> List[str]:
        buildings: List[str] = self.buildings_base[:]

        if self.has_dlc_the_machine_age:
            buildings.extend(self.buildings_the_machine_age)

        return sorted(buildings)

    @staticmethod
    def building_empire_count_range() -> range:
        return range(5, 21)

    @staticmethod
    def building_planet_count_range() -> range:
        return range(3, 6)

    @functools.cached_property
    def unique_buildings_base(self) -> List[str]:
        return [
            "Autochiton Monument",
            "Heritage Site",
            "Hypercomms Forum",
            "Energy Grid",
            "Energy Nexus",
            "Betharian Power Plant",
            "Mineral Purification Plants",
            "Mineral Purification Hubs",
            "Food Processing Facilities",
            "Food Processing Centers",
            "Bio-Reactor",
            "Advanced Bio-Reactor",
            "Alloy Foundries",
            "Alloy Mega-Forges",
            "Alloy Nano-Plants",
            "Civilian Industries",
            "Civilian Fabricators",
            "Civilian Repli-Complexes",
            "Robot Assembly Plant",
            "Robot Assembly Complex",
            "Planetary Shield Generator",
            "Gene Clinics",
            "Cyto-Revitalization Centers",
            "Galactic Stock Exchange",
            "Ministry of Production / Resource Processing Center",
            "Alien Zoo",
            "Slave Processing Facility",
            "Noble Estates",
            "Ranger Lodge",
        ]

    @functools.cached_property
    def unique_buildings_megacorp(self) -> List[str]:
        return [
            "Corporate Culture Site",
            "Business Management Nexus",
            "Synergy Forum",
            "Numistic Shrine",
            "Waste Reprocessing Center",
        ]

    @functools.cached_property
    def unique_buildings_utopia(self) -> List[str]:
        return [
            "Sensorium Site",
            "Sensorium Center",
            "Sensorium Complex",
            "Spawning Pools",
            "Clone Vats",
            "Psi Corps",
        ]

    @functools.cached_property
    def unique_buildings_synthetic_dawn_or_the_machine_age(self) -> List[str]:
        return [
            "Simulation Site",
            "Simulation Center",
            "Simulation Complex",
            "Machine Assembly Plants",
            "Machine Assembly Complex",
        ]

    @functools.cached_property
    def unique_buildings_necroids(self) -> List[str]:
        return [
            "Sanctuary of Repose",
            "Pillar of Quietus",
            "Galactic Memorial",
            "Dread Encampment",
            "Posthumous Employment Center",
            "Chamber of Elevation",
            "House of Apotheosis",
        ]

    @functools.cached_property
    def unique_buildings_overlord(self) -> List[str]:
        return [
            "Offspring Nest",
        ]

    @functools.cached_property
    def unique_buildings_utopia_or_the_machine_age(self) -> List[str]:
        return [
            "Augmentation Center",
        ]

    @functools.cached_property
    def unique_buildings_ancient_relics(self) -> List[str]:
        return [
            "Ancient Refinery",
            "Vultaum Reality Computer",
            "Baol Organic Plant",
        ]

    @functools.cached_property
    def unique_buildings_galactic_paragons(self) -> List[str]:
        return [
            "Contained Ecosphere",
            "Murmuring Monolith",
            "Vaults of Knowledge",
        ]

    @functools.cached_property
    def unique_buildings_astral_planes(self) -> List[str]:
        return [
            "Astral Siphon",
            "Astral Funnel",
            "Astral Nexus",
        ]

    @functools.cached_property
    def unique_buildings_cosmic_storms(self) -> List[str]:
        return [
            "Storm Attraction Center",
            "Advanced Storm Attraction Center",
            "Storm Repulsion Center",
            "Advanced Storm Repulsion Center",
            "Storm Relief Center",
            "Storm Nulifier",
            "Astrometeorology Observatory",
            "Storm Summoning Theater",
            "Storm Holo Hall",
            "Storm Grand Theater",
        ]

    @functools.cached_property
    def unique_buildings_toxoids(self) -> List[str]:
        return [
            "Coordinated Fulfillment Center",
            "Universal Productivity Alignment Facility",
            "Mutagenic Spa",
            "Mutagenic Permutation Pool",
            "Hyper Lubrication Basin",
            "Order's Keep",
            "Order's Castle",
        ]

    @functools.cached_property
    def unique_buildings_the_machine_age(self) -> List[str]:
        return [
            "Augmentation Bazaar",
            "Genomic Services Center/Genomic Safeguard Warren",
            "Identity Repository",
            "Abandoned Gene Clinic",
            "Amphitheater of the Mind",
            "The Grand Concert Hall of the Mind",
            "Sanctuary of Toil",
            "Grand Cathedral of Toil",
            "Forge of the Fellowship",
            "Grand Forge of the Fellowship",
            "Battlements of Steel",
            "The Grand Battlements of Steel",
            "Sanctum of Augmentation",
            "United Sanctum of Augmentation",
        ]

    @functools.cached_property
    def unique_buildings_plantoids(self) -> List[str]:
        return [
            "Gaia Seeder -- Phase 1",
            "Gaia Seeder -- Phase 2",
            "Gaia Seeder -- Phase 3",
            "Gaia Seeder -- Final Phase",
        ]

    @functools.cached_property
    def unique_buildings_humanoids(self) -> List[str]:
        return [
            "Ancient Clone Vat",
        ]

    def unique_buildings(self) -> List[str]:
        unique_buildings: List[str] = self.unique_buildings_base[:]

        if self.has_dlc_megacorp:
            unique_buildings.extend(self.unique_buildings_megacorp)
        if self.has_dlc_utopia:
            unique_buildings.extend(self.unique_buildings_utopia)
        if self.has_dlc_synthetic_dawn or self.has_dlc_the_machine_age:
            unique_buildings.extend(self.unique_buildings_synthetic_dawn_or_the_machine_age)
        if self.has_dlc_necroids:
            unique_buildings.extend(self.unique_buildings_necroids)
        if self.has_dlc_overlord:
            unique_buildings.extend(self.unique_buildings_overlord)
        if self.has_dlc_utopia or self.has_dlc_the_machine_age:
            unique_buildings.extend(self.unique_buildings_utopia_or_the_machine_age)
        if self.has_dlc_ancient_relics:
            unique_buildings.extend(self.unique_buildings_ancient_relics)
        if self.has_dlc_galactic_paragons:
            unique_buildings.extend(self.unique_buildings_galactic_paragons)
        if self.has_dlc_astral_planes:
            unique_buildings.extend(self.unique_buildings_astral_planes)
        if self.has_dlc_cosmic_storms:
            unique_buildings.extend(self.unique_buildings_cosmic_storms)
        if self.has_dlc_toxoids:
            unique_buildings.extend(self.unique_buildings_toxoids)
        if self.has_dlc_the_machine_age:
            unique_buildings.extend(self.unique_buildings_the_machine_age)
        if self.has_dlc_plantoids:
            unique_buildings.extend(self.unique_buildings_plantoids)
        if self.has_dlc_humanoids:
            unique_buildings.extend(self.unique_buildings_humanoids)

        return sorted(unique_buildings)

    @staticmethod
    def unique_building_count_range() -> range:
        return range(2, 6)

    @functools.cached_property
    def empire_unique_buildings_base(self) -> List[str]:
        return [
            "Embassy Complex",
            "Grand Embassy Complex",
            "Military Academy",
            "Research Institute / Planetary Supercomputer",
            "Auto-Curating Vault / Vault of Acquisitions / Alpha Hub",
            "Citadel of Faith",
            "Omega Alignment",
        ]

    @functools.cached_property
    def empire_unique_buildings_leviathans(self) -> List[str]:
        return [
            "Ministry of Culture",
        ]

    @functools.cached_property
    def empire_unique_buildings_the_machine_age(self) -> List[str]:
        return [
            "Identity Complex",
            "Cyberdome",
            "Expanded Reactor",
            "Neural Stabilizer",
            "Synaptic Cogitator",
            "Synaptic Overclocker",
            "Synaptic Preserver",
            "Synaptic Resonator",
            "Synaptic Sustainer",
            "Synaptic Validator",
        ]

    @functools.cached_property
    def empire_unique_buildings_utopia(self) -> List[str]:
        return [
            "Sanctum of the Composer",
            "Sanctum of the Eater",
            "Sanctum of the Instrument",
            "Sanctum of the Whisperers",
        ]

    @functools.cached_property
    def empire_unique_buildings_ancient_relics(self) -> List[str]:
        return [
            "Faculty of Archaeostudies",
            "First League Filing Offices",
        ]

    def empire_unique_buildings(self) -> List[str]:
        empire_unique_buildings: List[str] = self.empire_unique_buildings_base[:]

        if self.has_dlc_leviathans:
            empire_unique_buildings.extend(self.empire_unique_buildings_leviathans)
        if self.has_dlc_the_machine_age:
            empire_unique_buildings.extend(self.empire_unique_buildings_the_machine_age)
        if self.has_dlc_utopia:
            empire_unique_buildings.extend(self.empire_unique_buildings_utopia)
        if self.has_dlc_ancient_relics:
            empire_unique_buildings.extend(self.empire_unique_buildings_ancient_relics)

        return sorted(empire_unique_buildings)

    @functools.cached_property
    def districts_base(self) -> List[str]:
        return [
            "City / Hive / Nexus",
            "Industrial / Coordination / Trade",
            "Resort",
            "Prison",
            "Prison Industrial",
            "Slave Domicile",
            "Battle Thrall",
            "Generator",
            "Minin",
            "Agriculture",
            "Residential Arcology",
            "Foundry Arcology",
            "Factory Arcology",
            "Leisure Arcology",
            "Sanctuary Arcology",
            "Administrative Arcology",
            "Ecclesiastical Arcology",
            "City Segment",
            "Hive",
        ]

    @functools.cached_property
    def districts_utopia_or_federations(self) -> List[str]:
        return [
            "Habitation",
            "Order's Demesne",
            "Industrial",
            "Zero-G Research",
            "Reactor",
            "Astro-Mining",
        ]

    @functools.cached_property
    def districts_the_machine_age(self) -> List[str]:
        return [
            "Neural Gate",
            "Ampliative Speculator",
        ]

    def districts(self) -> List[str]:
        districts: List[str] = self.districts_base[:]

        if self.has_dlc_utopia or self.has_dlc_federations:
            districts.extend(self.districts_utopia_or_federations)
        if self.has_dlc_the_machine_age:
            districts.extend(self.districts_the_machine_age)

        return sorted(districts)

    @staticmethod
    def district_planet_count_range() -> range:
        return range(5, 11)

    @staticmethod
    def district_empire_count_range() -> range:
        return range(25, 51)

    @staticmethod
    def jobs() -> List[str]:
        return [
            "Administrator",
            "Culture Worker",
            "Researcher",
            "Miner",
            "Politician",
            "Pop Assembler",
            "Entertainer",
            "Metallurgist",
            "Artisan",
            "Farmer",
            "Technician",
            "Merchant",
            "Trader",
            "Gas Refiner",
            "Translucer",
            "Chemist",
            "Enforcer",
            "Doctor",
            "Aumentor",
            "Soldier",
            "Bath Attendant",
            "Livestock",
            "Grid Amalamated",
            "Knight",
            "Squire",
        ]

    @functools.cached_property
    def planet_designations_base(self) -> List[str]:
        return [
            "Colony",
            "Generator",
            "Mining",
            "Agri / Hydroponics",
            "Fortress",
            "Tech / Research",
            "Rural",
            "Fringe",
            "Urban / Nest / Machine",
            "Forge / Foundry",
            "Factory",
            "Industrial",
            "Refinery",
            "Unification / Ecclesiastical / Sanctuary",
            "Resort",
            "Penal",
            "Thrall",
            "Ecumenopolis",
            "Ring",
            "Commercial / Trade",
            "Habitat",
        ]

    @functools.cached_property
    def planet_designations_synthetic_dawn(self) -> List[str]:
        return [
            "Gestation",
        ]

    @functools.cached_property
    def planet_designations_synthetic_dawn_or_the_machine_age(self) -> List[str]:
        return [
            "Machine",
        ]

    @functools.cached_property
    def planet_designations_the_machine_age(self) -> List[str]:
        return [
            "Nanotech",
        ]

    @functools.cached_property
    def planet_designations_utopia(self) -> List[str]:
        return [
            "Hive",
        ]

    def planet_designations(self) -> List[str]:
        planet_designations: List[str] = self.planet_designations_base[:]

        if self.has_dlc_synthetic_dawn:
            planet_designations.extend(self.planet_designations_synthetic_dawn)
        if self.has_dlc_synthetic_dawn or self.has_dlc_the_machine_age:
            planet_designations.extend(self.planet_designations_synthetic_dawn_or_the_machine_age)
        if self.has_dlc_the_machine_age:
            planet_designations.extend(self.planet_designations_the_machine_age)
        if self.has_dlc_utopia:
            planet_designations.extend(self.planet_designations_utopia)

        return sorted(planet_designations)

    @staticmethod
    def planet_count_range() -> range:
        return range(1, 6)

    @staticmethod
    def gateway_count_range() -> range:
        return range(2, 6)

    @functools.cached_property
    def modules_base(self) -> List[str]:
        return [
            "Anchorage",
            "Defense Guns / Gun Battery",
            "Defense Batteries / Torpedo Battery",
            "Defense Hangers / Hangar Bay",
            "Vivarium Tank",
            "Shipyard",
            "Hatchery / Beastport",
            "Trade Hub",
            "Solar Panel Network",
            "Astro-Mining Bay",
            "Detection Array",
            "Ancient Rampart",
        ]

    @functools.cached_property
    def modules_overlord(self) -> List[str]:
        return [
            "Habitation",
        ]

    def modules(self) -> List[str]:
        modules: List[str] = self.modules_base[:]

        if self.has_dlc_overlord:
            modules.extend(self.modules_overlord)

        return sorted(modules)

    @staticmethod
    def module_count_range() -> range:
        return range(6, 31)

    @functools.cached_property
    def starbase_buildings_base(self) -> List[str]:
        return [
            "Resource Silo",
            "Target Uplink Computer",
            "Communications Jammer",
            "Disruption Field Generator",
            "Crew Quarters / Crew Gestation Chambers / Service Umbilicals",
            "Fleet Academy / Battle Simulators",
            "Naval Logistics Office",
            "Hydroponics Bay",
            "Mining Bay",
            "Nebula Refinery",
            "Transit Hub",
            "Listening Post",
            "Black Hole Observatory",
            "Hyperlane Registrar",
            "Offworld Trading Company",
            "Deep Space Black Site",
            "Defense-Grid Supercomputer",
            "Command Center",
            "Astro-Mining Hub",
            "Cordyceptic Reanimation Facility",
            "Reloading Bay",
            "Dimensional Shrine",
        ]

    @functools.cached_property
    def starbase_buildings_overlord(self) -> List[str]:
        return [
            "Climate Optimization Stations",
            "Low Gravity Mega-Refiners",
            "Stratospheric Ionization Elements",
            "Alloy Processing Facilities",
            "Orbital Logistics Systems",
            "The Giga-Mall",
            "Orbital Filling System",
            "Synaptic Relays",
            "Orbital Maintenance Drops",
            "Orbital Garden",
            "Orbital Shield Generator",
            "Salvage Works",
            "Mercenary Garrison",
            "Shroud Beacon",
        ]

    @functools.cached_property
    def starbase_buildings_apocalypse_or_the_machine_age(self) -> List[str]:
        return [
            "Titan Assembly Yards",
        ]

    @functools.cached_property
    def starbase_buildings_apocalypse_or_federations_or_nemesis(self) -> List[str]:
        return [
            "Colossal Assembly Yards",
        ]

    @functools.cached_property
    def starbase_buildings_ancient_relics(self) -> List[str]:
        return [
            "Ancient Shield Overcharger",
        ]

    @functools.cached_property
    def starbase_buildings_galactic_paragons(self) -> List[str]:
        return [
            "Interstellar Recruitment Office",
        ]

    @functools.cached_property
    def starbase_buildings_first_contact(self) -> List[str]:
        return [
            "Dark Matter Resonance Chamber",
        ]

    @functools.cached_property
    def starbase_buildings_aquatics(self) -> List[str]:
        return [
            "Ice Mining Station",
        ]

    @functools.cached_property
    def starbase_buildings_the_machine_age(self) -> List[str]:
        return [
            "Nanite Harvester",
        ]

    @functools.cached_property
    def starbase_buildings_cosmic_storms(self) -> List[str]:
        return [
            "Voidlure",
            "Storm Attraction Array",
            "Storm Repulsion Array",
        ]

    @functools.cached_property
    def starbase_buildings_leviathans_or_distant_stars_or_grand_archive(self) -> List[str]:
        return [
            "Curator Think Tank",
        ]

    @functools.cached_property
    def starbase_buildings_leviathans(self) -> List[str]:
        return [
            "Art College",
            "Trader Proxy Office",
        ]

    def starbase_buildings(self) -> List[str]:
        starbase_buildings: List[str] = self.starbase_buildings_base[:]

        if self.has_dlc_overlord:
            starbase_buildings.extend(self.starbase_buildings_overlord)
        if self.has_dlc_apocalypse or self.has_dlc_the_machine_age:
            starbase_buildings.extend(self.starbase_buildings_apocalypse_or_the_machine_age)
        if self.has_dlc_apocalypse or self.has_dlc_federations or self.has_dlc_nemesis:
            starbase_buildings.extend(self.starbase_buildings_apocalypse_or_federations_or_nemesis)
        if self.has_dlc_ancient_relics:
            starbase_buildings.extend(self.starbase_buildings_ancient_relics)
        if self.has_dlc_galactic_paragons:
            starbase_buildings.extend(self.starbase_buildings_galactic_paragons)
        if self.has_dlc_first_contact:
            starbase_buildings.extend(self.starbase_buildings_first_contact)
        if self.has_dlc_aquatics:
            starbase_buildings.extend(self.starbase_buildings_aquatics)
        if self.has_dlc_the_machine_age:
            starbase_buildings.extend(self.starbase_buildings_the_machine_age)
        if self.has_dlc_cosmic_storms:
            starbase_buildings.extend(self.starbase_buildings_cosmic_storms)
        if self.has_dlc_leviathans or self.has_dlc_distant_stars or self.has_dlc_grand_archive:
            starbase_buildings.extend(self.starbase_buildings_leviathans_or_distant_stars_or_grand_archive)
        if self.has_dlc_leviathans:
            starbase_buildings.extend(self.starbase_buildings_leviathans)

        return sorted(starbase_buildings)

    @staticmethod
    def starbase_building_count_range() -> range:
        return range(1, 6)

    @functools.cached_property
    def megastructures_base(self) -> List[str]:
        return list()

    @functools.cached_property
    def megastructures_utopia(self) -> List[str]:
        return [
            "Science Nexus",
            "Sentry Array",
            "Ring World",
            "Dyson Sphere",
        ]

    @functools.cached_property
    def megastructures_megacorp(self) -> List[str]:
        return [
            "Mega Art Installation",
            "Strategic Coordination Center",
            "Interstellar Assembly",
            "Matter Decompressor",
        ]

    @functools.cached_property
    def megastructures_federations(self) -> List[str]:
        return [
            "Mega Shipyard",
        ]

    @functools.cached_property
    def megastructures_overlord(self) -> List[str]:
        return [
            "Quantum Catapult",
        ]

    @functools.cached_property
    def megastructures_the_machine_age(self) -> List[str]:
        return [
            "Arc Furnace",
            "Dyson Swarm",
            "Synaptic Lathe",
        ]

    @functools.cached_property
    def megastructures_grand_archive(self) -> List[str]:
        return [
            "Grand Archive",
        ]

    def megastructures(self) -> List[str]:
        megastructures: List[str] = self.megastructures_base[:]

        if self.has_dlc_utopia:
            megastructures.extend(self.megastructures_utopia)
        if self.has_dlc_megacorp:
            megastructures.extend(self.megastructures_megacorp)
        if self.has_dlc_federations:
            megastructures.extend(self.megastructures_federations)
        if self.has_dlc_overlord:
            megastructures.extend(self.megastructures_overlord)
        if self.has_dlc_the_machine_age:
            megastructures.extend(self.megastructures_the_machine_age)
        if self.has_dlc_grand_archive:
            megastructures.extend(self.megastructures_grand_archive)

        return sorted(megastructures)

    @staticmethod
    def starbase_levels() -> List[str]:
        return [
            "Starport",
            "Starhold",
            "Star Fortress",
            "Citadel",
        ]

    @staticmethod
    def starbase_count_range() -> range:
        return range(5, 16)

    @staticmethod
    def defense_platform_count_range() -> range:
        return range(15, 151)

    @functools.cached_property
    def holdings_base(self) -> List[str]:
        return [
            "Overlord Garrison",
            "Aid Agency",
            "Emporium",
            "Noble Chateaus",
            "Recruitment Office",
            "Ranger Lodge",
        ]

    @functools.cached_property
    def holdings_overlord(self) -> List[str]:
        return [
            "Orbital Assembly Complex",
            "Satellite Campus",
            "Ministry of Truth",
            "Ministry of Energy",
            "Ministry of Extraction",
            "Ministry of Acquisition",
            "Splinter Hive",
            "Distributed Processing",
            "Ministry of Science",
            "Offworld Foundry",
            "Vigil Command",
            "Offspring Nest",
        ]

    @functools.cached_property
    def holdings_utopia(self) -> List[str]:
        return [
            "Tree of Life Sapling",
        ]

    @functools.cached_property
    def holdings_plantoids(self) -> List[str]:
        return [
            "Gaia Seeder Outpost",
        ]

    @functools.cached_property
    def holdings_megacorp(self) -> List[str]:
        return [
            "Communal Housing Outreach",
            "Franchise Headquarters",
            "Mercenary Liaison Office",
            "Virtual Entertainment Studios",
            "Private Military Industries",
            "Private Mining Consortium",
            "Fast Food Chain",
            "Amusement Megaplex",
            "Commercial Forum",
            "Private Research Enterprises",
            "Public Relations Firm",
            "Temple of Prosperity",
            "Corporate Embassy",
            "Pirate Free Haven",
            "Concealed Drug Labs",
            "Wrecking Yards",
            "Wildcat Mining Operations",
            "Bio-Reprocessing Plants",
            "Underground Clubs",
            "Smuggler's Port",
            "Illicit Research Labs",
            "Syndicate Front Corporations",
            "Subversive Shrine",
            "Disinformation Center",
            "Executive Retreat",
            "Xeno-Outreach Agency",
        ]

    @functools.cached_property
    def holdings_synthetic_dawn(self) -> List[str]:
        return [
            "Organic Haven",
        ]

    @functools.cached_property
    def holdings_lithoids(self) -> List[str]:
        return [
            "Experimental Crater",
        ]

    @functools.cached_property
    def holdings_necroids(self) -> List[str]:
        return [
            "Sacrificial Shrine",
            "Dread Outpost",
        ]

    @functools.cached_property
    def holdings_megacorp_or_necroids(self) -> List[str]:
        return [
            "Reemployment Center",
        ]

    @functools.cached_property
    def holdings_toxoids(self) -> List[str]:
        return [
            "Order's Commandery",
            "Mutagenic Spa",
            "Mutagenic Permutation Pool",
            "Hyper Lubrication Basin",
        ]

    @functools.cached_property
    def holdings_the_machine_age(self) -> List[str]:
        return [
            "Genomic Services Outreach",
        ]

    @functools.cached_property
    def holdings_megacorp_and_nemesis(self) -> List[str]:
        return [
            "Imperial Concession Port",
        ]

    @functools.cached_property
    def holdings_megacorp_and_toxoids(self) -> List[str]:
        return [
            "Knightly Fair Grounds",
        ]

    @functools.cached_property
    def holdings_megacorp_and_galactic_paragons(self) -> List[str]:
        return [
            "Corporate Clinic",
        ]

    @functools.cached_property
    def holdings_megacorp_and_the_machine_age(self) -> List[str]:
        return [
            "Offworld Implant Hub",
            "AI Emporium",
            "Clear Thought Clinic",
        ]

    def holdings(self) -> List[str]:
        holdings: List[str] = self.holdings_base[:]

        if self.has_dlc_overlord:
            holdings.extend(self.holdings_overlord)
        if self.has_dlc_utopia:
            holdings.extend(self.holdings_utopia)
        if self.has_dlc_plantoids:
            holdings.extend(self.holdings_plantoids)
        if self.has_dlc_megacorp:
            holdings.extend(self.holdings_megacorp)
        if self.has_dlc_synthetic_dawn:
            holdings.extend(self.holdings_synthetic_dawn)
        if self.has_dlc_lithoids:
            holdings.extend(self.holdings_lithoids)
        if self.has_dlc_necroids:
            holdings.extend(self.holdings_necroids)
        if self.has_dlc_megacorp and self.has_dlc_necroids:
            holdings.extend(self.holdings_megacorp_or_necroids)
        if self.has_dlc_toxoids:
            holdings.extend(self.holdings_toxoids)
        if self.has_dlc_the_machine_age:
            holdings.extend(self.holdings_the_machine_age)
        if self.has_dlc_megacorp and self.has_dlc_nemesis:
            holdings.extend(self.holdings_megacorp_and_nemesis)
        if self.has_dlc_megacorp and self.has_dlc_toxoids:
            holdings.extend(self.holdings_megacorp_and_toxoids)
        if self.has_dlc_megacorp and self.has_dlc_galactic_paragons:
            holdings.extend(self.holdings_megacorp_and_galactic_paragons)
        if self.has_dlc_megacorp and self.has_dlc_the_machine_age:
            holdings.extend(self.holdings_megacorp_and_the_machine_age)

        return sorted(holdings)

    @staticmethod
    def holding_count_range() -> range:
        return range(1, 6)

    @staticmethod
    def diplomatic_agreements() -> List[str]:
        return [
            "Embassy",
            "Non-Aggression Pact",
            "Commercial Pact",
            "Research Agreement",
            "Migration Treaty",
            "Guarantee Independence",
            "Defensive Pact",
            "Rivalry",
        ]

    @staticmethod
    def diplomacy_count_range() -> range:
        return range(1, 4)

    @staticmethod
    def diplomatic_actions() -> List[str]:
        return [
            "Recall Embassy",
            "Break Non-Aggression Pact",
            "Break Commercial Pact",
            "Break Migration Treaty",
            "Revoke Guarantee",
            "Break Defensive Pact",
            "End Rivalry",
            "Improve Relations",
            "Harm Relations",
            "Build Spy Network",
            "Make Claims",
            "Declar War",
            "Open Borders",
            "Close Borders",
            "Insult",
        ]

    @staticmethod
    def relations() -> List[str]:
        return [
            "Terrible",
            "Tense",
            "Neutral",
            "Positive",
            "Excellent",
        ]

    @functools.cached_property
    def resolutions_base(self) -> List[str]:
        return [
            "Buzzword Standardization",
            "Leveraged Privateering",
            "Underdeveloped System Utilization",
            "Regulatory Facilitation",
            "Collective Waste Management",
            "Building a Better Tomorrow",
            "Charter of Worker's Rights",
            "Five Year Plans",
            "Greater Than Ourselves",
            "Pangalactic Recycling Initiatives",
            "Natural Sanctuaries",
            "Integrated Gardens",
            "Cooperative Research Channels",
            "Astral Studies Network",
            "Advanced Xenostudies",
            "Comfort the Fallen",
            "Tithe of the Soulless",
            "Right to Work",
            "The Readied Shield",
            "Military Readiness Act",
            "The Enemy of My Enemy",
            "Guardian Angels Act",
            "Reverence for Life",
            "Independent Tribunals",
            "Minor Economic Sanctions",
            "Minor Administrative Sanctions",
            "Minor Research Sanctions",
            "Minor Military Sanctions",
        ]

    @functools.cached_property
    def resolutions_federations(self) -> List[str]:
        return [
            "Holistic Asset Coordination",
            "Profit Maximizaiton Engines",
            "Environmental Ordinance Waivers",
            "Project Cornucopia",
            "Balance in the Middle",
            "Universal Prosperity Mandate",
            "Environmental Control Board",
            "The Paradise Initiative",
            "Ethical Guideline Refactoring",
            "Extradimensional Experimentation",
            "Silence the Soulless",
            "A Defined Purpose",
            "Castigation Proclamation",
            "Renegade Containment Doctrine",
            "Last Resort Doctrine",
            "Demobilization Initiative",
            "Space Amoeba Protection Act",
            "Tiyanki Conservation Act",
            "Tiyanki Pest Control",
            "Cutholoid Eradication",
            "Voidworm Eradication",
            "Denouncement",
            "Constitutional Immunity",
            "Champions of the Community",
            "Developmental Aides",
            "Galactic Threats",
            "Enable Council Veto Power",
            "Remove Council Denouncement Power",
            "Permanent Council Seat",
        ]

    @functools.cached_property
    def resolutions_overlord(self) -> List[str]:
        return [
            "Security Contractors",
            "High Consequence Protection",
            "Neutral Defenders",
            "Regulated Growth",
            "Ensured Sovereignty",
            "A Voice for All",
            "Administrative Insight",
            "Borderless Authority",
            "Personal Oversight",
        ]

    @functools.cached_property
    def resolutions_overlord_and_federations(self) -> List[str]:
        return [
            "Galactic Risk Management",
            "Corporate Peacekeeping",
        ]

    @functools.cached_property
    def resolutions_cosmic_storms(self) -> List[str]:
        return [
            "Storm Knowledge Sharing",
            "Storm Surveying Initiative",
            "Galactic Storm Management",
            "Advanced Storm Studies",
            "Galactic Emergency Relief",
            "Storm Movement Mandate",
        ]

    @functools.cached_property
    def resolutions_federations_and_cosmic_storms(self) -> List[str]:
        return [
            "Storm Utilization Protocols",
            "Storm Manipulation Mandate",
            "Storm Manipulation Controls",
            "Storm Preservation Initiative",
        ]

    @functools.cached_property
    def resolutions_federations_and_megacorp(self) -> List[str]:
        return [
            "Ban Organic Slave Trade",
            "Ban Sentient Slave Trade",
        ]

    @functools.cached_property
    def resolutions_first_contact(self) -> List[str]:
        return [
            "Equal Standing Act",
            "Non-Interference Act",
            "Exploitation Act",
        ]

    @functools.cached_property
    def resolutions_nemesis(self) -> List[str]:
        return [
            "Nominate Custodian",
            "Crisis Declaration",
            "Extend Custodianship",
            "Remove Custodianship Term Limit",
            "End Custodianship",
            "Galactic Mobilization",
            "Introduce Galactic Standard",
            "Anti-Piracy Initiative",
            "A United Front",
            "Proclaim the Galactic Imperium",
            "Galactic Defense Force",
            "GDF Expansion",
            "Interstellar Navigation Agency",
            "Galactic Trade Organization",
            "GALPOL",
            "Imperial Council by Election",
            "Imperial Council by Appointment",
            "Imperial Council by Triad of Advancement",
            "Imperial Crusade",
            "Pax Galactica",
            "Imperial Armada",
            "Imperial Armada Expansion",
            "Imperial Legions",
            "Imperial Navigation Agency",
            "Imperial Security Directorate",
            "Imperial Charter",
        ]

    def resolutions(self) -> List[str]:
        resolutions: List[str] = self.resolutions_base[:]

        if self.has_dlc_federations:
            resolutions.extend(self.resolutions_federations)
        if self.has_dlc_overlord:
            resolutions.extend(self.resolutions_overlord)
        if self.has_dlc_overlord and self.has_dlc_federations:
            resolutions.extend(self.resolutions_overlord_and_federations)
        if self.has_dlc_cosmic_storms:
            resolutions.extend(self.resolutions_cosmic_storms)
        if self.has_dlc_federations and self.has_dlc_cosmic_storms:
            resolutions.extend(self.resolutions_federations_and_cosmic_storms)
        if self.has_dlc_federations and self.has_dlc_megacorp:
            resolutions.extend(self.resolutions_federations_and_megacorp)
        if self.has_dlc_first_contact:
            resolutions.extend(self.resolutions_first_contact)
        if self.has_dlc_nemesis:
            resolutions.extend(self.resolutions_nemesis)

        return sorted(resolutions)

    @staticmethod
    def galactic_council_size_range() -> range:
        return range(1, 6)

    @functools.cached_property
    def federation_types_base(self) -> List[str]:
        return [
            "Galactic Union",
        ]

    @functools.cached_property
    def federation_types_federations(self) -> List[str]:
        return [
            "Trade League",
            "Research Cooperative",
            "Military Alliance",
            "Hegemony",
            "Holy Covenant",
        ]

    def federation_types(self) -> List[str]:
        federation_types: List[str] = self.federation_types_base[:]

        if self.has_dlc_federations:
            federation_types.extend(self.federation_types_federations)

        return sorted(federation_types)

    @staticmethod
    def federation_level_range() -> range:
        return range(1, 6)

    @staticmethod
    def joint_operations() -> List[str]:
        return [
            "Ephemeral Puzzle",
            "Logistics Remodelling",
            "Joint Military Exercises",
            "A Celebration of Unity and Leadership",
            "Federation Ecumenical Council",
        ]

    @functools.cached_property
    def federation_laws_base(self) -> List[str]:
        return [
            "Federation Centralization -- Minimal",
            "Federation Centralization -- Low",
            "Federation Centralization -- Medium",
            "Federation Centralization -- High",
            "Federation Centralization -- Very High",
            "Fleet Contribution -- None",
            "Fleet Contribution -- Low",
            "Fleet Contribution -- Medium",
            "Fleet Contribution -- High",
            "Succession Type -- Rotation",
            "Succession Type -- Strongest",
            "Succession Power -- Economy",
            "Succession Power -- Diplomatic Weight",
            "Succession Term -- 10 Years",
            "Succession Term -- 20 Years",
            "Succession Term -- 30 Years",
            "Succession Term -- 40 Years",
            "Succession Term -- Status Change",
        ]

    @functools.cached_property
    def federation_laws_federations(self) -> List[str]:
        return [
            "Federation Fleet Construction -- Everyone",
            "Federation Fleet Construction -- Only Leader",
            "Succession Type -- Random",
            "Succession Type -- Challenge",
            "Succession Power -- Technology",
            "Succession Power -- Fleets",
            "Challenge -- Arena Combat",
            "Challenge -- Psionic Battle",
            "Challenge -- Golden Rule",
            "Challenge -- Thesis Defense",
            "Challenge -- Spiritual Conclave",
            "Can Subjects Join -- No",
            "Can Subjects Join -- Yes",
            "Vote Weight -- Equal",
            "Vote Weight -- Diplomatic",
            "War Declaration -- Unanimous Vote",
            "War Declaration -- Majority Vote",
            "War Declaration -- President Decides",
            "Invite Members -- Unanimous Vote",
            "Invite Members -- Majority Vote",
            "Invite Members -- President Decides",
            "Kick Members -- Majority Vote",
            "Kick Members -- President Decides",
            "Free Migration -- Disabled",
            "Free Migration -- Enabled",
            "Separate Treaties -- Allowed",
            "Separate Treaties -- Prohibited",
        ]

    def federation_laws(self) -> List[str]:
        federation_laws: List[str] = self.federation_laws_base[:]

        if self.has_dlc_federations:
            federation_laws.extend(self.federation_laws_federations)

        return sorted(federation_laws)

    @staticmethod
    def subject_empire_count_range() -> range:
        return range(1, 4)

    @staticmethod
    def subject_terms() -> List[str]:
        return [
            "Integration Permitted",
            "Integration Prohibited",
            "Limited Diplomacy",
            "Restricted Voting",
            "Independent Diplomacy",
            "Expansion Prohibited",
            "Expansion Regulated",
            "Expansion Permitted",
            "Overlord Conflicts -- None",
            "Overlord Conflicts -- Defensive",
            "Overlord Conflicts -- Offensive",
            "Overlord Conflicts -- All",
            "Subject Conflicts -- None",
            "Subject Conflicts -- Defensive",
            "Subject Conflicts -- Offensive",
            "Subject Conflicts -- All",
            "Holdings Limit -- 0",
            "Holdings Limit -- 1",
            "Holdings Limit -- 2",
            "Holdings Limit -- 3",
            "Holdings Limit -- 4",
            "Independent Sensors",
            "Unified Sensors",
        ]

    @staticmethod
    def subject_types() -> List[str]:
        return [
            "Vassal",
            "Protectorate",
            "Tributary",
            "Subsidary",
            "Bulwark",
            "Prospectorium",
            "Scholarium",
        ]

    @functools.cached_property
    def wargoals_base(self) -> List[str]:
        return [
            "Conquer",
            "Counterattack",
            "Impose Ideology",
            "Plunder",
            "Vassalize",
            "Make Tributary / Subsidiary",
            "Independence",
            "Secret Fealty",
            "End Threat",
        ]

    @functools.cached_property
    def wargoals_federations(self) -> List[str]:
        return [
            "Humiliate",
            "Establish Hegemony",
            "Leave Hegemony",
            "Preemptive War",
        ]

    @functools.cached_property
    def wargoals_nemesis(self) -> List[str]:
        return [
            "Imperial Rebuke",
            "Council Seat",
            "Bring Into Fold",
            "Force Into Imperium",
            "Restore Community",
            "Crisis War",
        ]

    @functools.cached_property
    def wargoals_megacorp(self) -> List[str]:
        return [
            "Expel Corporation",
            "Seize Assets",
        ]

    @functools.cached_property
    def wargoals_apocalypse(self) -> List[str]:
        return [
            "Total War",
        ]

    def wargoals(self) -> List[str]:
        wargoals: List[str] = self.wargoals_base[:]

        if self.has_dlc_federations:
            wargoals.extend(self.wargoals_federations)
        if self.has_dlc_nemesis:
            wargoals.extend(self.wargoals_nemesis)
        if self.has_dlc_megacorp:
            wargoals.extend(self.wargoals_megacorp)
        if self.has_dlc_apocalypse:
            wargoals.extend(self.wargoals_apocalypse)

        return sorted(wargoals)

    @staticmethod
    def ship_sizes() -> List[str]:
        return [
            "Corvette",
            "Destroyer",
            "Cruiser",
            "Battleship",
            "Titan",
        ]

    @staticmethod
    def naval_capacity_range() -> range:
        return range(100, 251)

    @staticmethod
    def fleet_capacity_range() -> range:
        return range(40, 101)

    @functools.cached_property
    def colossal_ship_types_base(self) -> List[str]:
        return list()

    @functools.cached_property
    def colossal_ship_types_apocalypse_or_the_machine_age(self) -> List[str]:
        return [
            "Colossus",
        ]

    @functools.cached_property
    def colossal_ship_types_federations(self) -> List[str]:
        return [
            "Juggernaut",
        ]

    @functools.cached_property
    def colossal_ship_types_nemesis(self) -> List[str]:
        return [
            "Star-Eater",
        ]

    def colossal_ship_types(self) -> List[str]:
        colossal_ship_types: List[str] = self.colossal_ship_types_base[:]

        if self.has_dlc_apocalypse or self.has_dlc_the_machine_age:
            colossal_ship_types.extend(self.colossal_ship_types_apocalypse_or_the_machine_age)
        if self.has_dlc_federations:
            colossal_ship_types.extend(self.colossal_ship_types_federations)
        if self.has_dlc_nemesis:
            colossal_ship_types.extend(self.colossal_ship_types_nemesis)

        return sorted(colossal_ship_types)

    @functools.cached_property
    def colossus_weapons_base(self) -> List[str]:
        return [
            "Global Pacifier",
            "World Cracker",
            "Neutron Sweep",
            "Divine Enforcer",
        ]

    @functools.cached_property
    def colossus_weapons_synthetic_dawn(self) -> List[str]:
        return [
            "Nanobot Diffuser",
        ]

    @functools.cached_property
    def colossus_weapons_ancient_relics(self) -> List[str]:
        return [
            "Devolving Beam",
        ]

    @functools.cached_property
    def colossus_weapons_aquatics(self) -> List[str]:
        return [
            "Deluge Machine",
        ]

    def colossus_weapons(self) -> List[str]:
        colossus_weapons: List[str] = self.colossus_weapons_base[:]

        if self.has_dlc_synthetic_dawn:
            colossus_weapons.extend(self.colossus_weapons_synthetic_dawn)
        if self.has_dlc_ancient_relics:
            colossus_weapons.extend(self.colossus_weapons_ancient_relics)
        if self.has_dlc_aquatics:
            colossus_weapons.extend(self.colossus_weapons_aquatics)

        return sorted(colossus_weapons)

    @staticmethod
    def intel_levels() -> List[str]:
        return [
            "Low",
            "Medium",
            "High",
            "Full",
        ]

    @staticmethod
    def intel_categories() -> List[str]:
        return [
            "Government",
            "Diplomacy",
            "Economy",
            "Technology",
            "Military",
        ]

    @functools.cached_property
    def operations_base(self) -> List[str]:
        return [
            "Plant Advanced Knowledge",
            "Infiltrate Government",
            "Infiltrate Hive",
            "Gather Information",
        ]

    @functools.cached_property
    def operations_utopia_or_first_contact(self) -> List[str]:
        return [
            "Indoctrinate Society",
        ]

    @functools.cached_property
    def operations_first_contact(self) -> List[str]:
        return [
            "Increase Awareness",
            "Spread Disinformation",
        ]

    @functools.cached_property
    def operations_nemesis(self) -> List[str]:
        return [
            "Spark Diplomatic Incident",
            "Prepare Sleeper Cells",
            "Acquire Asset",
            "Extort Favors",
            "Smear Campaign",
            "Steal Technology",
            "Sabotage Starbase",
            "Arm Privateers",
            "Crisis Beacon",
            "Imperium: Weaken Imperial Authority",
            "Imperium: Target Seditionists",
            "Imperium: Spark Rebellion",
        ]

    def operations(self) -> List[str]:
        operations: List[str] = self.operations_base[:]

        if self.has_dlc_utopia or self.has_dlc_first_contact:
            operations.extend(self.operations_utopia_or_first_contact)
        if self.has_dlc_first_contact:
            operations.extend(self.operations_first_contact)
        if self.has_dlc_nemesis:
            operations.extend(self.operations_nemesis)

        return sorted(operations)


# Archipelago Options
class StellarisDLCOwned(OptionSet):
    """
    Indicates which Stellaris DLC the player owns, if any.
    """

    display_name = "Stellaris DLC Owned"
    valid_keys = [
        "Grand Archive",
        "Cosmic Storms",
        "The Machine Age",
        "Astral Planes",
        "Galactic Paragons",
        "First Contact",
        "Toxoids",
        "Overlord",
        "Aquatics",
        "Nemesis",
        "Necroids",
        "Federations",
        "Lithoids",
        "Ancient Relics",
        "Megacorp",
        "Distant Stars",
        "Apocalypse",
        "Humanoids",
        "Synthetic Dawn",
        "Utopia",
        "Leviathans",
        "Plantoids",
    ]

    default = valid_keys
