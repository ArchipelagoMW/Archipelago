from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet, Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class SlayTheSpireArchipelagoOptions:
    slay_the_spire_modes: SlayTheSpireModes
    slay_the_spire_characters: SlayTheSpireCharacters
    slay_the_spire_downfall_characters: SlayTheSpireDownfallCharacters
    slay_the_spire_custom_characters: SlayTheSpireCustomCharacters
    slay_the_spire_custom_modes: SlayTheSpireCustomModes
    slay_the_spire_custom_modifiers: SlayTheSpireCustomModifiers
    slay_the_spire_ascension_levels: SlayTheSpireAscensionLevels
    slay_the_spire_include_act_4: SlayTheSpireIncludeAct4


class SlayTheSpireGame(Game):
    name = "Slay the Spire"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = SlayTheSpireArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Beat Act 3 on Ascension LEVEL as CHARACTER in MODE mode",
                data={
                    "LEVEL": (self.ascension_levels, 1),
                    "CHARACTER": (self.characters, 1),
                    "MODE": (self.modes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
        ]

        if self.include_custom_mode:
            templates.append(
                GameObjectiveTemplate(
                    label="Beat Act 3 on Ascension LEVEL as CHARACTER with the following Modifiers: MODIFIERS",
                    data={
                        "LEVEL": (self.ascension_levels, 1),
                        "CHARACTER": (self.characters, 1),
                        "MODIFIERS": (self.modifiers_3_weighted, 3),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
            )

        if self.include_act_4:
            templates.append(
                GameObjectiveTemplate(
                    label="Defeat the Heart on Ascension LEVEL as CHARACTER in MODE mode",
                    data={
                        "LEVEL": (self.ascension_levels, 1),
                        "CHARACTER": (self.characters, 1),
                        "MODE": (self.modes, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            )

            if "Downfall" in self.modes():
                templates.append(
                    GameObjectiveTemplate(
                        label="Defeat Neow on Ascension LEVEL as CHARACTER in MODE mode",
                        data={
                            "LEVEL": (self.ascension_levels, 1),
                            "CHARACTER": (self.characters, 1),
                            "MODE": (self.modes, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    ),
                )

            if self.include_custom_mode:
                templates.append(
                    GameObjectiveTemplate(
                        label="Defeat the Heart on Ascension LEVEL as CHARACTER with the following Modifiers: MODIFIERS",
                        data={
                            "LEVEL": (self.ascension_levels, 1),
                            "CHARACTER": (self.characters, 1),
                            "MODIFIERS": (self.modifiers_3_weighted, 3),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=3,
                    ),
                )

                if "Downfall" in self.modes():
                    templates.append(
                        GameObjectiveTemplate(
                            label="Defeat Neow on Ascension LEVEL as CHARACTER with the following Modifiers: MODIFIERS",
                            data={
                                "LEVEL": (self.ascension_levels, 1),
                                "CHARACTER": (self.characters, 1),
                                "MODIFIERS": (self.modifiers_3_weighted, 3),
                            },
                            is_time_consuming=False,
                            is_difficult=False,
                            weight=1,
                        ),
                    )

        return templates

    @property
    def selected_modes(self) -> List[str]:
        return sorted(self.archipelago_options.slay_the_spire_modes.value)

    @property
    def include_custom_mode(self) -> bool:
        return "Custom" in self.selected_modes

    @property
    def base_characters(self) -> List[str]:
        return sorted(self.archipelago_options.slay_the_spire_characters.value)

    @property
    def downfall_characters(self) -> List[str]:
        return sorted(self.archipelago_options.slay_the_spire_downfall_characters.value)

    @property
    def custom_characters(self) -> List[str]:
        return sorted(self.archipelago_options.slay_the_spire_custom_characters.value)

    @property
    def custom_modes(self) -> List[str]:
        return sorted(self.archipelago_options.slay_the_spire_custom_modes.value)

    @property
    def custom_modifiers(self) -> List[str]:
        return sorted(self.archipelago_options.slay_the_spire_custom_modifiers.value)

    def ascension_levels(self) -> List[str]:
        return sorted(self.archipelago_options.slay_the_spire_ascension_levels.value)

    @property
    def include_act_4(self) -> bool:
        return bool(self.archipelago_options.slay_the_spire_include_act_4.value)

    def characters(self) -> List[str]:
        characters: List[str] = self.base_characters[:]

        if "Downfall" in self.modes():
            characters.extend(self.downfall_characters)
        if len(self.custom_characters):
            characters.extend(self.custom_characters)

        return sorted(characters)

    def modes(self) -> List[str]:
        modes: List[str] = self.selected_modes[:]

        if "Custom" in modes:
            modes.remove("Custom")

        if self.include_custom_mode and len(self.custom_modes):
            modes.extend(self.custom_modes)

        return sorted(modes)

    @functools.cached_property
    def modifiers_base(self) -> List[str]:
        return [
            "Draft",
            "Draft",
            "Draft",
            "Draft",
            "Sealed Deck",
            "Sealed Deck",
            "Sealed Deck",
            "Sealed Deck",
            # "Endless",
            # "Blight Chests",
            "Hoarder",
            "Hoarder",
            "Insanity",
            "Insanity",
            "Insanity",
            "Insanity",
            "Chimera",
            "Chimera",
            "Praise Snecko",
            "Praise Snecko",
            "Shiny",
            "Shiny",
            "Shiny",
            "Specialized",
            "Specialized",
            "Specialized",
            "Specialized",
            "Vintage",
            "Vintage",
            "Vintage",
            "Controlled Chaos",
            "Controlled Chaos",
            "Inception",
            "Inception",
            "All Star",
            "All Star",
            "Diverse",
            "Red Cards",
            "Green Cards",
            "Blue Cards",
            "Purple Cards",
            "Colorless Cards",
            "Heirloom",
            "Heirloom",
            "Time Dilation",
            "Time Dilation",
            "Flight",
            "Flight",
            "My True Form",
            "My True Form",
            "Deadly Events",
            "Deadly Events",
            "Binary",
            "Binary",
            "One Hit Wonder",
            "One Hit Wonder",
            "Cursed Run",
            "Cursed Run",
            "Big Game Hunter",
            "Big Game Hunter",
            "Lethality",
            "Lethality",
            "Midas",
            "Midas",
            "Night Terrors",
            "Night Terrors",
            "Terminal",
            "Terminal",
            "Certain Future",
            "Certain Future",
            "Starter Deck",
            "Starter Deck",
        ]

    def modifiers(self) -> List[str]:
        modifiers: List[str] = self.modifiers_base[:]

        if len(self.custom_modifiers):
            modifiers.extend(self.custom_modifiers)

        return sorted(modifiers)

    def modifiers_3_weighted(self) -> List[str]:
        modifiers: List[str] = self.modifiers_base[:]
        modifiers_selected: List[str] = list()

        while len(modifiers_selected) < 3:
            modifier = self.random.choice(modifiers)

            if modifier not in modifiers_selected:
                modifiers_selected.append(modifier)

        return modifiers_selected


# Archipelago Options
class SlayTheSpireModes(OptionSet):
    """
    Indicates which Slay the Spire Modes should be considered when generating objectives.
    """

    display_name = "Slay the Spire Modes"
    valid_keys = [
        "Standard",
        "Downfall",
        "Custom",
    ]

    default = valid_keys


class SlayTheSpireCharacters(OptionSet):
    """
    Indicates which Slay the Spire Characters should be considered when generating objectives.
    """

    display_name = "Slay the Spire Characters"
    valid_keys = [
        "The Ironclad",
        "The Silent",
        "The Defect",
        "The Watcher",
    ]

    default = valid_keys


class SlayTheSpireDownfallCharacters(OptionSet):
    """
    Indicates which Slay the Spire Downfall Characters should be considered when generating objectives.
    """

    display_name = "Slay the Spire Downfall Characters"
    valid_keys = [
        "The Slime Boss",
        "The Guardian",
        "The Hexaghost",
        "The Automaton",
        "The Champ",
        "The Collector",
        "The Gremlins",
        "The Snecko",
    ]

    default = valid_keys


class SlayTheSpireCustomCharacters(OptionSet):
    """
    Indicates which Slay the Spire Custom Characters should be considered when generating objectives.
    """

    display_name = "Slay the Spire Custom Characters"

    default = list()


class SlayTheSpireCustomModes(OptionSet):
    """
    Indicates which Slay the Spire Custom Modes should be considered when generating objectives.
    """

    display_name = "Slay the Spire Custom Modes"

    default = list()


class SlayTheSpireCustomModifiers(OptionSet):
    """
    Indicates which Slay the Spire Custom Modifiers should be considered when generating objectives.
    """

    display_name = "Slay the Spire Custom Modifiers"

    default = list()


class SlayTheSpireAscensionLevels(OptionSet):
    """
    Indicates which Slay the Spire Ascension Levels should be considered when generating objectives.
    """

    display_name = "Slay the Spire Ascension Levels"
    valid_keys = [str(i) for i in range(0, 21)]

    default = valid_keys


class SlayTheSpireIncludeAct4(Toggle):
    """
    Indicates whether Slay the Spire Act 4 should be considered when generating objectives.
    """

    display_name = "Slay the Spire Include Act 4"
