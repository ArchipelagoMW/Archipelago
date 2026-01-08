from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class FourteenMinesweeperVariantsArchipelagoOptions:
    fourteen_minesweeper_variants_include_combos_and_bonus_variants: (
        FourteenMinesweeperVariantsIncludeCombosAndBonusVariants
    )


class FourteenMinesweeperVariantsGame(Game):
    name = "14 Minesweeper Variants"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = FourteenMinesweeperVariantsArchipelagoOptions

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
                    "VARIANT": (self.variants_single, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Perfect SIZE VARIANT board",
                data={
                    "SIZE": (self.sizes, 1),
                    "VARIANT": (self.variants_single, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

        if self.include_combinations_and_bonus_variants:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete SIZE VARIANT board",
                    data={
                        "SIZE": (self.sizes, 1),
                        "VARIANT": (self.variants_combined, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Perfect SIZE VARIANT board",
                    data={
                        "SIZE": (self.sizes, 1),
                        "VARIANT": (self.variants_combined, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        return templates

    @property
    def include_combinations_and_bonus_variants(self) -> bool:
        return bool(self.archipelago_options.fourteen_minesweeper_variants_include_combos_and_bonus_variants.value)

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
            "[Q] Quad",
            "[C] Connected",
            "[T] Triplet",
            "[O] Outside",
            "[D] Dual",
            "[S] Snake",
            "[B] Balance",
        ]

        if self.include_combinations_and_bonus_variants:
            variants.extend([
                "[T'] Triplet'",
                "[D'] Battleship",
                "[A] Anti-knight",
                "[H] Horizontal",
            ])

        return variants

    def variants_right(self) -> List[str]:
        variants: List[str] = [
            "[M] Multiple",
            "[L] Liar",
            "[W] Wall",
            "[N] Negation",
            "[X] Cross",
            "[P] Partition",
            "[E] Eyesight",
        ]

        if self.include_combinations_and_bonus_variants:
            variants.extend([
                "[X'] Mini Cross",
                "[K] Knight",
                "[W'] Longest Wall",
                "[E'] Eyesight'",
            ])

        return variants

    def variants_single(self) -> List[str]:
        variants: List[str] = [
            "[V] Vanilla",
            "[#] Hashtag",
        ]

        variants.extend(self.variants_left())
        variants.extend(self.variants_right())

        if self.include_combinations_and_bonus_variants:
            variants.append("[#'] Hashtag'")

        return sorted(variants)

    def variants_combined(self) -> List[str]:
        variants: List[str] = [
            "[C] Connected + [D] Dual",
            "[C] Connected + [Q] Quad",
            "[C] Connected + [T] Triplet",
            "[O] Outside + [Q] Quad",
            "[O] Outside + [T] Triplet",
            "[Q] Quad + [T] Triplet",
            "[L] Liar + [M] Multiple",
            "[M] Multiple + [X] Cross",
            "[M] Multiple + [N] Negation",
            "[N] Negation + [X] Cross",
            "[U] Unary + [W] Wall",
        ]

        for variant_left in self.variants_left():
            for variant_right in self.variants_right():
                variants.append(f"{variant_left} + {variant_right}")

            variants.append(f"{variant_left} + [#] Hashtag")
            variants.append(f"{variant_left} + [#'] Hashtag'")

        return sorted(variants)


# Archipelago Options
class FourteenMinesweeperVariantsIncludeCombosAndBonusVariants(Toggle):
    """
    Indicates whether to include combinations and bonus variants in 14 Minesweeper Variants objectives.
    """

    display_name = "14 Minesweeper Variants Include Combos and Bonus Variants"
