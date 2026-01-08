from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class FourteenMinesweeperVariants2ArchipelagoOptions:
    fourteen_minesweeper_variants_2_include_combos_and_bonus_variants: (
        FourteenMinesweeperVariants2IncludeCombosAndBonusVariants
    )


class FourteenMinesweeperVariants2Game(Game):
    name = "14 Minesweeper Variants 2"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = FourteenMinesweeperVariants2ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play on MODE",
                data={
                    "MODE": (self.modes, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Play on MODE with Fragile Star",
                data={
                    "MODE": (self.modes, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Complete SIZE VARIANT board",
                data={
                    "SIZE": (self.sizes, 1),
                    "VARIANT": (self.variants, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=23,
            ),
            GameObjectiveTemplate(
                label="Complete SIZE VARIANT board + [2#] Hashtag board",
                data={
                    "SIZE": (self.sizes, 1),
                    "VARIANT": (self.variants_secondary, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Perfect SIZE VARIANT board",
                data={
                    "SIZE": (self.sizes, 1),
                    "VARIANT": (self.variants, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=7,
            ),
            GameObjectiveTemplate(
                label="Perfect SIZE VARIANT board + [2#] Hashtag board",
                data={
                    "SIZE": (self.sizes, 1),
                    "VARIANT": (self.variants_secondary, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

        if self.include_combinations_and_bonus_variants:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete SIZE VARIANT_LEFT + VARIANT_RIGHT board",
                    data={
                        "SIZE": (self.sizes, 1),
                        "VARIANT_LEFT": (self.variants_left, 1),
                        "VARIANT_RIGHT": (self.variants_right, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=8,
                ),
                GameObjectiveTemplate(
                    label="Complete SIZE VARIANT board",
                    data={
                        "SIZE": (self.sizes, 1),
                        "VARIANT": (self.variants_double_right, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Complete SIZE VARIANT_LEFT + VARIANT_DOUBLE_RIGHT board",
                    data={
                        "SIZE": (self.sizes, 1),
                        "VARIANT_LEFT": (self.variants_left, 1),
                        "VARIANT_DOUBLE_RIGHT": (self.variants_double_right, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Complete SIZE VARIANT_LEFT + VARIANT_SECONDARY + [2#] Hashtag board",
                    data={
                        "SIZE": (self.sizes, 1),
                        "VARIANT_LEFT": (self.variants_left, 1),
                        "VARIANT_SECONDARY": (self.variants_secondary, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete SIZE VARIANT board",
                    data={
                        "SIZE": (self.sizes, 1),
                        "VARIANT": (self.variants_double_left, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Complete SIZE VARIANT board",
                    data={
                        "SIZE": (self.sizes, 1),
                        "VARIANT": (self.variants_solo, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete SIZE VARIANT_LEFT + VARIANT_RIGHT board",
                    data={
                        "SIZE": (self.sizes, 1),
                        "VARIANT_LEFT": (self.variants_left_no_bonus, 1),
                        "VARIANT_RIGHT": (self.variants_right_one, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete SIZE VARIANT_LEFT + VARIANT_RIGHT board",
                    data={
                        "SIZE": (self.sizes, 1),
                        "VARIANT_LEFT": (self.variants_left_one, 1),
                        "VARIANT_RIGHT": (self.variants_right_no_bonus, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Perfect SIZE VARIANT_LEFT + VARIANT_RIGHT board",
                    data={
                        "SIZE": (self.sizes, 1),
                        "VARIANT_LEFT": (self.variants_left, 1),
                        "VARIANT_RIGHT": (self.variants_right, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Perfect SIZE VARIANT board",
                    data={
                        "SIZE": (self.sizes, 1),
                        "VARIANT": (self.variants_double_right, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Perfect SIZE VARIANT_LEFT + VARIANT_DOUBLE_RIGHT board",
                    data={
                        "SIZE": (self.sizes, 1),
                        "VARIANT_LEFT": (self.variants_left, 1),
                        "VARIANT_DOUBLE_RIGHT": (self.variants_double_right, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Perfect SIZE VARIANT_LEFT + VARIANT_SECONDARY + [2#] Hashtag board",
                    data={
                        "SIZE": (self.sizes, 1),
                        "VARIANT_LEFT": (self.variants_left, 1),
                        "VARIANT_SECONDARY": (self.variants_secondary, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Perfect SIZE VARIANT board",
                    data={
                        "SIZE": (self.sizes, 1),
                        "VARIANT": (self.variants_double_left, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Perfect SIZE VARIANT board",
                    data={
                        "SIZE": (self.sizes, 1),
                        "VARIANT": (self.variants_solo, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Perfect SIZE VARIANT_LEFT + VARIANT_RIGHT board",
                    data={
                        "SIZE": (self.sizes, 1),
                        "VARIANT_LEFT": (self.variants_left_no_bonus, 1),
                        "VARIANT_RIGHT": (self.variants_right_one, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Perfect SIZE VARIANT_LEFT + VARIANT_RIGHT board",
                    data={
                        "SIZE": (self.sizes, 1),
                        "VARIANT_LEFT": (self.variants_left_one, 1),
                        "VARIANT_RIGHT": (self.variants_right_no_bonus, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            ])

        return templates

    @property
    def include_combinations_and_bonus_variants(self) -> bool:
        return bool(self.archipelago_options.fourteen_minesweeper_variants_2_include_combos_and_bonus_variants.value)

    @staticmethod
    def modes() -> List[str]:
        return [
            "Expert Mode",
            "Ultimate Mode",
        ]

    @staticmethod
    def sizes() -> List[str]:
        return [
            "a 5x5",
            "a 6x6",
            "a 7x7",
            "an 8x8",
        ]

    def variants_left(self) -> List[str]:
        variants: List[str] = [
            "[2H] Horizontal",
            "[2C] Connected",
            "[2S] Segment",
            "[2G] Group",
            "[2F] Flowers",
            "[2B] Bridge",
            "[2T] Triplet",
        ]

        if self.include_combinations_and_bonus_variants:
            variants.extend([
                "[2Z] Zero-sum",
                "[2G'] Group'",
            ])

        return variants

    @staticmethod
    def variants_left_no_bonus() -> List[str]:
        variants: List[str] = [
            "[2H] Horizontal",
            "[2C] Connected",
            "[2S] Segment",
            "[2G] Group",
            "[2F] Flowers",
            "[2B] Bridge",
            "[2T] Triplet",
        ]

        return variants

    @staticmethod
    def variants_double_left() -> List[str]:
        return [
            "[2G] Group + [2H] Horizontal",
            "[2C] Connected + [2H] Horizontal",
            "[2C] Connected + [2G] Group",
            "[2F] Flowers + [2G] Group",
            "[2F] Flowers + [2H] Horizontal",
            "[2C] Connected + [2F] Flowers",
            "[2B] Bridge + [2H] Horizontal",
            "[2G] Group + [R+] Mine Count+",
        ]

    def variants_right(self) -> List[str]:
        variants: List[str] = [
            "[2X] Cross",
            "[2D] Deviation",
            "[2P] Product",
            "[2E] Encrypted",
            "[2M] Modulo",
            "[2A] Area",
            "[2L] Liar",
        ]

        if self.include_combinations_and_bonus_variants:
            variants.extend([
                "[2X'] Cross'",
                "[2I] Incompleteness",
            ])

        return variants

    @staticmethod
    def variants_right_no_bonus() -> List[str]:
        variants: List[str] = [
            "[2X] Cross",
            "[2D] Deviation",
            "[2P] Product",
            "[2E] Encrypted",
            "[2M] Modulo",
            "[2A] Area",
            "[2L] Liar",
        ]

        return variants

    @staticmethod
    def variants_double_right() -> List[str]:
        return [
            "[2E] Encrypted + [2X] Cross",
            "[2E] Encrypted + [2D] Deviation",
            "[2E] Encrypted + [2M] Modulo",
            "[2E] Encrypted + [2A] Area",
            "[2E] Encrypted + [2P] Product",
            "[2L] Liar + [2X] Cross",
            "[2L] Liar + [2D] Deviation",
            "[2L] Liar + [2M] Modulo",
            "[2L] Liar + [2A] Area",
            "[2L] Liar + [2P] Product",
        ]

    def variants(self) -> List[str]:
        return sorted(["[V] Vanilla"] + self.variants_left() + self.variants_right())

    @staticmethod
    def variants_secondary() -> List[str]:
        return [
            "[2L] Liar",
            "[2E] Encrypted",
        ]

    @staticmethod
    def variants_solo() -> List[str]:
        return [
            "[2E'] Self-Referential",
            "[2E^] Encrypted^",
            "[2L'] Liar'",
            "[2E] Encrypted + [2L] Liar",
        ]

    @staticmethod
    def variants_left_one() -> List[str]:
        return [
            "[1Q] Quad",
            "[1C] Connected",
            "[1T] Triplet",
            "[1O] Outside",
            "[1D] Dual",
            "[1S] Snake",
            "[1B] Balance",
        ]

    @staticmethod
    def variants_right_one() -> List[str]:
        return [
            "[1M] Multiple",
            "[1L] Liar",
            "[1W] Wall",
            "[1N] Negation",
            "[1X] Cross",
            "[1P] Partition",
            "[1E] Eyesight",
        ]


# Archipelago Options
class FourteenMinesweeperVariants2IncludeCombosAndBonusVariants(Toggle):
    """
    Indicates whether to include combinations and bonus variants in 14 Minesweeper Variants 2 objectives.
    """

    display_name = "14 Minesweeper Variants 2 Include Combos and Bonus Variants"
