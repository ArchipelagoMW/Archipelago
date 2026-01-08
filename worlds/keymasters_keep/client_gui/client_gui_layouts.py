import random

from typing import Any, Dict, List, Optional, Tuple

from kivy.core.clipboard import Clipboard

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from kivy.utils import escape_markup

from ..client import KeymastersKeepContext
from ..data.description_data import item_descriptions, unknown_item_descriptions
from ..data.location_data import KeymastersKeepLocationData, location_data

from ..data.mapping_data import (
    color_to_hex_codes,
    item_classification_to_colors,
    item_classification_to_rarities,
    key_item_to_colors,
    label_mapping,
    region_to_unlock_location_and_item,
    shopkeeper_greetings,
)

from ..enums import (
    KeymastersKeepGoals,
    KeymastersKeepItems,
    KeymastersKeepLocations,
    KeymastersKeepRegions,
    KeymastersKeepShops,
    KeymastersKeepShopkeepers,
)


def key_to_markup_text(key: KeymastersKeepItems) -> str:
    colors: Tuple[str, str] = [color_to_hex_codes[color] for color in key_item_to_colors[key]]

    return (
        f"[font=Arial][color={colors[0]}]█[/color][color={colors[1]}]█[/color][color={colors[0]}]█[/color][/font] "
        f"{key.value}"
    )


class NotConnectedLayout(BoxLayout):
    ctx: KeymastersKeepContext

    def __init__(self, ctx: KeymastersKeepContext) -> None:
        super().__init__(orientation="horizontal", size_hint_y=0.08)

        self.ctx = ctx

        self.add_widget(
            Label(text="Please connect to an Archipelago server first to view this tab.", font_size="24dp")
        )

    def show(self):
        self.opacity = 1.0
        self.size_hint_y = 0.08
        self.disabled = False

    def hide(self):
        self.opacity = 0.0
        self.size_hint_y = None
        self.height = "0dp"
        self.disabled = True


class KeepAreaLayout(BoxLayout):
    ctx: KeymastersKeepContext

    area: KeymastersKeepRegions
    is_shop: bool

    unlock_button: Button
    locked_by_button: Button

    def __init__(
        self,
        ctx: KeymastersKeepContext,
        area: KeymastersKeepRegions,
        locked_by: Optional[List[KeymastersKeepItems]],
    ) -> None:
        super().__init__(orientation="horizontal", size_hint_y=None, height="40dp", spacing="8dp")

        self.ctx = ctx

        self.area = area
        self.is_shop = area in ctx.shop_data

        self.unlock_button = Button(
            text="Locked",
            width="100dp",
            size_hint_x=None,
            halign="left",
            disabled=bool(locked_by),
        )

        if locked_by is None:
            self.unlock_button.text = "Unlock"

        self.unlock_button.bind(on_press=self.on_unlock_button_press)

        self.add_widget(self.unlock_button)

        area_label: Label = Label(
            text=f"[b]{area.value}[/b]",
            markup=True,
            size_hint_x=0.15,
            size_hint_y=None,
            height="40dp",
            halign="left",
            valign="middle",
        )

        area_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.add_widget(area_label)

        self.locked_by_button: Button = Button(
            text="",
            markup=True,
            size_hint_x=0.77,
            size_hint_y=None,
            height="40dp",
            halign="left",
            valign="middle",
            background_normal="",
            background_color=(0, 0, 0, 0)
        )

        if bool(locked_by):
            self.locked_by_button.text = "[b]Needs:[/b]  " + "    ".join(
                [key_to_markup_text(key) for key in locked_by]
            )

        self.locked_by_button.bind(size=lambda btn, size: setattr(btn, "text_size", size))

        self.add_widget(self.locked_by_button)

    def update(self, locked_by: Optional[List[KeymastersKeepItems]], unlocked: bool) -> None:
        if locked_by:
            self.unlock_button.disabled = True
            self.unlock_button.text = "Locked"

            self.locked_by_button.text = "[b]Needs:[/b]  " + "    ".join(
                [key_to_markup_text(key) for key in locked_by]
            )
        elif unlocked:
            self.unlock_button.disabled = True
            self.unlock_button.text = "Unlocked!"

            if self.is_shop:
                shop: KeymastersKeepShops = self.ctx.shop_data[self.area]["shop"]

                shop_item_count: int = len(self.ctx.shop_data[self.area]["shop_items"])

                shop_items_purchased_count: int = len(self.ctx.game_state["shop_items_purchased"][shop])
                shop_items_available_count: int = shop_item_count - shop_items_purchased_count

                label: str
                if shop_items_available_count:
                    if not shop_items_purchased_count:
                        label = f"{shop_items_available_count} item(s) for sale"
                    else:
                        label = f"{shop_items_available_count} item(s) for sale ({shop_items_purchased_count} purchased)"
                else:
                    label = f"Sold out!"

                self.locked_by_button.text = f"[b]Shop:[/b]  {shop.value}    [color=00FA9A]{label}[/color]"

                if shop_items_available_count:
                    self.locked_by_button.bind(on_press=self.on_switch_to_shops_tab_click)
                else:
                    self.locked_by_button.bind(on_press=lambda _: None)
            else:
                game: str = self.ctx.area_games[self.area.value]

                trial_count: int = len(self.ctx.area_trials[self.area])

                trial_available_count: int = len(self.ctx.game_state["trials_available"][self.area])
                trial_completed_count: int = trial_count - trial_available_count

                label: str
                if trial_available_count:
                    if not trial_completed_count:
                        label = f"{trial_available_count} available trial(s)"
                    else:
                        label = f"{trial_available_count} available trial(s) ({trial_completed_count} complete)"
                else:
                    label = f"Area complete!"

                self.locked_by_button.text = f"[b]Game:[/b]  {game}    [color=00FA9A]{label}[/color]"

                if trial_available_count:
                    self.locked_by_button.bind(on_press=self.on_switch_to_available_trials_tab_click)
                else:
                    self.locked_by_button.bind(on_press=lambda _: None)
        else:
            self.unlock_button.disabled = False
            self.unlock_button.text = "Unlock"

            self.locked_by_button.text = ""

    def on_unlock_button_press(self, _) -> None:
        self.unlock_button.disabled = True

        unlock_location: KeymastersKeepLocations
        unlock_location, _ = region_to_unlock_location_and_item[self.area]

        unlock_location_data: KeymastersKeepLocationData = location_data[unlock_location]

        self.ctx.complete_location(unlock_location_data.archipelago_id)

        if self.ctx.shops and self.is_shop:
            shop_item_location_ids: List[int] = [
                data["location_data"].archipelago_id for data in self.ctx.shop_data[self.area]["shop_items"].values()
            ]

            self.ctx.create_hints_for(shop_item_location_ids)

    def on_switch_to_available_trials_tab_click(self, _) -> None:
        self.ctx.ui.available_trials_tab.on_release()

    def on_switch_to_shops_tab_click(self, _) -> None:
        self.ctx.ui.shops_tab.on_release()


class KeepAreasLayout(ScrollView):
    ctx: KeymastersKeepContext

    layout: BoxLayout

    area_layouts: Dict[KeymastersKeepRegions, KeepAreaLayout]

    def __init__(
        self,
        ctx: KeymastersKeepContext,
        areas_locked_by: Dict[KeymastersKeepRegions, Optional[List[KeymastersKeepItems]]],
    ) -> None:
        super().__init__(size_hint=(0.7, 1.0))

        self.ctx = ctx

        self.layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter("height"))

        self.area_layouts = dict()

        title_label: Label = Label(
            text="[b]Keep Areas[/b]",
            markup=True,
            font_size="20dp",
            size_hint_y=None,
            height="40dp",
            halign="left",
            valign="middle",
        )

        title_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.layout.add_widget(title_label)

        area: KeymastersKeepRegions
        locked_by: Optional[List[KeymastersKeepItems]]
        for area, locked_by in areas_locked_by.items():
            area_layout: KeepAreaLayout = KeepAreaLayout(self.ctx, area, locked_by)

            self.layout.add_widget(area_layout)
            self.area_layouts[area] = area_layout

        self.add_widget(self.layout)

    def update(
        self,
        areas_locked_by: Dict[KeymastersKeepRegions, Optional[List[KeymastersKeepItems]]],
        areas_unlocked: Dict[KeymastersKeepRegions, bool],
    ) -> None:
        area: KeymastersKeepRegions
        locked_by: Optional[List[KeymastersKeepItems]]
        for area, locked_by in areas_locked_by.items():
            self.area_layouts[area].update(locked_by, areas_unlocked[area])


class MagicKeyLabel(Label):
    ctx: KeymastersKeepContext

    def __init__(self, ctx: KeymastersKeepContext, key: KeymastersKeepItems):
        super().__init__(
            text=key_to_markup_text(key),
            markup=True,
            size_hint_y=None,
            height="24dp",
            halign="left",
            valign="middle",
        )

        self.ctx = ctx

        self.bind(size=lambda label, size: setattr(label, "text_size", size))

    def set_received(self, received: bool) -> None:
        if received:
            self.opacity = 1.0
        else:
            self.opacity = 0.25


class MagicKeyTrackerLayout(ScrollView):
    ctx: KeymastersKeepContext

    layout: BoxLayout

    key_labels: Dict[KeymastersKeepItems, MagicKeyLabel]

    def __init__(self, ctx: KeymastersKeepContext, magic_keys: Dict[KeymastersKeepItems, bool]):
        super().__init__(size_hint=(0.12, 1.0))

        self.ctx = ctx

        self.layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter("height"))

        self.key_labels = dict()

        title_label: Label = Label(
            text="[b]Magic Key Tracker[/b]",
            markup=True,
            font_size="20dp",
            size_hint_y=None,
            height="40dp",
            halign="left",
            valign="middle",
        )

        title_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.layout.add_widget(title_label)

        key: KeymastersKeepItems
        received: bool
        for key, received in magic_keys.items():
            key_label: MagicKeyLabel = MagicKeyLabel(self.ctx, key)
            key_label.set_received(received)

            self.layout.add_widget(key_label)
            self.key_labels[key] = key_label

        self.add_widget(self.layout)

    def update(self, magic_keys: Dict[KeymastersKeepItems, bool]) -> None:
        key: KeymastersKeepItems
        received: bool
        for key, received in magic_keys.items():
            self.key_labels[key].set_received(received)


class SeedInformationGoalLayout(ScrollView):
    ctx: KeymastersKeepContext

    layout: BoxLayout

    artifacts_label: Label
    unlock_challenge_chamber_button: Button

    magic_keys_label: Label

    claim_victory_button: Button

    def __init__(self, ctx: KeymastersKeepContext):
        super().__init__(size_hint=(0.18, 1.0))

        self.ctx = ctx

        self.layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter("height"))

        # Seed Information
        seed_information_title_label: Label = Label(
            text="[b]Seed Information[/b]",
            markup=True,
            font_size="20dp",
            size_hint_y=None,
            height="40dp",
            halign="left",
            valign="middle",
        )

        seed_information_title_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.layout.add_widget(seed_information_title_label)

        lm: Dict[Any, str] = label_mapping

        game_medley_mode_label: str = lm[self.ctx.game_medley_mode]

        if self.ctx.game_medley_mode:
            game_medley_mode_label += f" ({self.ctx.game_medley_percentage_chance}% chance)"

        label_text: str = (
            f"Keep Areas: [color=00FA9A]{len(self.ctx.area_trials) + len(self.ctx.shop_data)}[/color]\n"
            f"Magic Keys: [color=00FA9A]{self.ctx.magic_keys_total}[/color]\n"
            f"Unlocked Areas: [color=00FA9A]{self.ctx.unlocked_areas}[/color]\n"
            f"Lock Magic Keys (Minimum): [color=00FA9A]{self.ctx.lock_magic_keys_minimum}[/color]\n"
            f"Lock Magic Keys (Maximum): [color=00FA9A]{self.ctx.lock_magic_keys_maximum}[/color]\n"
            f"Area Trials (Minimum): [color=00FA9A]{self.ctx.area_trials_minimum}[/color]\n"
            f"Area Trials (Maximum): [color=00FA9A]{self.ctx.area_trials_maximum}[/color]\n\n"
            f"Shops: [color=00FA9A]{lm[self.ctx.shops]}[/color]\n"
        )

        if self.ctx.shops:
            label_text += (
                f"Shops Chance: [color=00FA9A]{self.ctx.shops_percentage_chance}%[/color]\n"
                f"Shop Items (Minimum): [color=00FA9A]{self.ctx.shop_items_minimum}[/color]\n"
                f"Shop Items (Maximum): [color=00FA9A]{self.ctx.shop_items_maximum}[/color]\n"
                f"Shop Items Progression Chance: [color=00FA9A]{self.ctx.shop_items_progression_percentage_chance}%[/color]\n"
                f"Shop Hints: [color=00FA9A]{lm[self.ctx.shop_hints]}[/color]\n\n"
            )

        label_text += (
            f"Game Medley Mode: [color=00FA9A]{game_medley_mode_label}[/color]\n\n"
            f"Include 18+ / Unrated Games: [color=00FA9A]{lm[self.ctx.include_adult_only_or_unrated_games]}[/color]\n"
            f"Include Modern Console Games: [color=00FA9A]{lm[self.ctx.include_modern_console_games]}[/color]\n"
            f"Include Difficult Objectives: [color=00FA9A]{lm[self.ctx.include_difficult_objectives]}[/color]\n"
            f"Include Time Consuming Objectives: [color=00FA9A]{lm[self.ctx.include_time_consuming_objectives]}[/color]\n\n"
            f"Hints Reveal Objectives: [color=00FA9A]{lm[self.ctx.hints_reveal_objectives]}[/color]"
        )

        seed_information_content_label: Label = Label(
            text=label_text,
            markup=True,
            size_hint_y=None,
            height="320dp",
            halign="left",
            valign="top",
        )

        seed_information_content_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.layout.add_widget(seed_information_content_label)

        self.add_widget(self.layout)

        # Goal
        goal_title_label: Label = Label(
            text="[b]Goal[/b]",
            markup=True,
            font_size="20dp",
            size_hint_y=None,
            height="40dp",
            halign="left",
            valign="middle",
        )

        goal_title_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.layout.add_widget(goal_title_label)

        if self.ctx.goal == KeymastersKeepGoals.KEYMASTERS_CHALLENGE:
            goal_description_label: Label = Label(
                text=(
                    "[b]Keymaster's Challenge[/b]\nRetrieve Artifacts of Resolve to unlock the Keymaster's Challenge "
                    "Chamber and beat the ultimate challenge!"
                ),
                markup=True,
                size_hint_y=None,
                height="90dp",
                halign="left",
                valign="middle",
            )

            goal_description_label.bind(size=lambda label, size: setattr(label, "text_size", size))

            self.layout.add_widget(goal_description_label)

            self.artifacts_label: Label = Label(
                text=(
                    f"[b]Artifacts of Resolve[/b]\n"
                    f"Retrieved [color=00FA9A]{self.ctx.game_state['artifact_of_resolve_received']}[/color] of "
                    f"[color=00FA9A]{self.ctx.artifacts_of_resolve_required}[/color] needed "
                    f"([color=888888]{self.ctx.artifacts_of_resolve_total} total[/color])"
                ),
                markup=True,
                size_hint_y=None,
                height="60dp",
                halign="left",
                valign="middle",
            )

            self.artifacts_label.bind(size=lambda label, size: setattr(label, "text_size", size))

            self.layout.add_widget(self.artifacts_label)

            self.unlock_challenge_chamber_button = Button(
                text="Unlock Challenge Chamber",
                size_hint_y=None,
                height="40dp",
                disabled=True,
            )

            self.unlock_challenge_chamber_button.bind(on_press=self.on_unlock_challenge_chamber_button_press)

            self.layout.add_widget(self.unlock_challenge_chamber_button)

        elif self.ctx.goal == KeymastersKeepGoals.MAGIC_KEY_HEIST:
            goal_description_label: Label = Label(
                text="[b]Magic Key Heist[/b]\nRetrieve Magic Keys throughout the Keymaster's Keep and escape!",
                markup=True,
                size_hint_y=None,
                height="90dp",
                halign="left",
                valign="middle",
            )

            goal_description_label.bind(size=lambda label, size: setattr(label, "text_size", size))

            self.layout.add_widget(goal_description_label)

            self.magic_keys_label: Label = Label(
                text=(
                    f"[b]Magic Keys[/b]\n"
                    f"Retrieved [color=00FA9A]{self.ctx.game_state['magic_keys_received']}[/color] of "
                    f"[color=00FA9A]{self.ctx.magic_keys_required}[/color] needed "
                    f"([color=888888]{self.ctx.magic_keys_total} total[/color])"
                ),
                markup=True,
                size_hint_y=None,
                height="60dp",
                halign="left",
                valign="middle",
            )

            self.magic_keys_label.bind(size=lambda label, size: setattr(label, "text_size", size))

            self.layout.add_widget(self.magic_keys_label)

        self.claim_victory_button = Button(
            text="Claim Victory!",
            size_hint_y=None,
            height="40dp",
            disabled=True,
        )

        self.claim_victory_button.bind(on_press=self.on_claim_victory_button_press)

        self.layout.add_widget(self.claim_victory_button)

    def update(self) -> None:
        if self.ctx.goal == KeymastersKeepGoals.KEYMASTERS_CHALLENGE:
            self.artifacts_label.text = (
                f"[b]Artifacts of Resolve[/b]\n"
                f"Retrieved [color=00FA9A]{self.ctx.game_state['artifact_of_resolve_received']}[/color] of "
                f"[color=00FA9A]{self.ctx.artifacts_of_resolve_required}[/color] needed "
                f"([color=888888]{self.ctx.artifacts_of_resolve_total} total[/color])"
            )

            if self.ctx.game_state["artifact_of_resolve_received"] >= self.ctx.artifacts_of_resolve_required:
                if self.ctx.game_state["goal_challenge_chamber_unlocked"]:
                    self.unlock_challenge_chamber_button.disabled = True
                    self.unlock_challenge_chamber_button.text = "Challenge Chamber Unlocked!"
                else:
                    self.unlock_challenge_chamber_button.disabled = False
            else:
                self.unlock_challenge_chamber_button.disabled = True
        elif self.ctx.goal == KeymastersKeepGoals.MAGIC_KEY_HEIST:
            self.magic_keys_label.text = (
                f"[b]Magic Keys[/b]\n"
                f"Retrieved [color=00FA9A]{self.ctx.game_state['magic_keys_received']}[/color] of "
                f"[color=00FA9A]{self.ctx.magic_keys_required}[/color] needed "
                f"([color=888888]{self.ctx.magic_keys_total} total[/color])"
            )

        if self.ctx.goal_completed:
            self.claim_victory_button.disabled = True
            self.claim_victory_button.text = "Victory!"
        elif self.ctx.game_state["goal_can_claim_victory"]:
            self.claim_victory_button.disabled = False
        else:
            self.claim_victory_button.disabled = True

    def on_unlock_challenge_chamber_button_press(self, _) -> None:
        self.unlock_challenge_chamber_button.disabled = True

        self.ctx.complete_location(
            location_data[KeymastersKeepLocations.THE_KEYMASTERS_CHALLENGE_CHAMBER_UNLOCK].archipelago_id
        )

    def on_claim_victory_button_press(self, _) -> None:
        self.claim_victory_button.disabled = True
        self.ctx.complete_goal()


class KeymastersKeepTabLayout(BoxLayout):
    ctx: KeymastersKeepContext

    layout_content: BoxLayout

    layout_content_keep_areas: KeepAreasLayout
    layout_content_magic_key_tracker: MagicKeyTrackerLayout
    layout_content_seed_information_goal: SeedInformationGoalLayout

    layout_not_connected: BoxLayout

    def __init__(self, ctx: KeymastersKeepContext) -> None:
        super().__init__(orientation="vertical")

        self.ctx = ctx

        self.layout_not_connected = NotConnectedLayout(self.ctx)
        self.add_widget(self.layout_not_connected)

        self.layout_content = BoxLayout(orientation="horizontal", spacing="16dp", padding=["8dp", "0dp"])
        self.add_widget(self.layout_content)

        self.update()

    def update(self) -> None:
        if not self.ctx.is_game_state_initialized:
            self.layout_not_connected.show()
            self.layout_content.clear_widgets()

            return

        self.layout_not_connected.hide()

        if not len(self.layout_content.children):
            self.layout_content_keep_areas = KeepAreasLayout(self.ctx, self.ctx.game_state["areas_locked_by"])
            self.layout_content.add_widget(self.layout_content_keep_areas)

            self.layout_content_magic_key_tracker = MagicKeyTrackerLayout(self.ctx, self.ctx.game_state["magic_keys"])
            self.layout_content.add_widget(self.layout_content_magic_key_tracker)

            self.layout_content_seed_information_goal = SeedInformationGoalLayout(self.ctx)
            self.layout_content.add_widget(self.layout_content_seed_information_goal)

        self.layout_content_keep_areas.update(
            self.ctx.game_state["areas_locked_by"], self.ctx.game_state["areas_unlocked"]
        )

        self.layout_content_magic_key_tracker.update(self.ctx.game_state["magic_keys"])
        self.layout_content_seed_information_goal.update()


class TrialAreaLabel(Label):
    ctx: KeymastersKeepContext

    area: KeymastersKeepRegions

    def __init__(self, ctx: KeymastersKeepContext, area: KeymastersKeepRegions) -> None:
        super().__init__(
            text=f"[b]{area.value}[/b]",
            markup=True,
            font_size="32dp",
            size_hint_y=None,
            height="70dp",
            halign="left",
            valign="bottom",
        )

        self.ctx = ctx
        self.area = area

        self.bind(size=lambda label, size: setattr(label, "text_size", size))

    def show(self) -> None:
        self.opacity = 1.0
        self.height = "70dp"
        self.disabled = False

    def hide(self) -> None:
        self.opacity = 0.0
        self.height = "0dp"
        self.disabled = True


class TrialGameLabel(Label):
    ctx: KeymastersKeepContext

    area: KeymastersKeepRegions

    def __init__(self, ctx: KeymastersKeepContext, area: KeymastersKeepRegions) -> None:
        super().__init__(
            text=f"[b]{ctx.area_games[area.value]}[/b]",
            markup=True,
            font_size="18dp",
            size_hint_y=None,
            height="40dp",
            halign="left",
            valign="middle",
        )

        if ctx.area_game_optional_constraints[area.value]:
            optional_constraints: str = "  /  ".join(ctx.area_game_optional_constraints[area.value])
            self.text += f"    [color=888888] Optional Conditions:  {optional_constraints}[/color]"

        self.ctx = ctx
        self.area = area

        self.bind(size=lambda label, size: setattr(label, "text_size", size))

    def show(self) -> None:
        self.opacity = 1.0
        self.height = "40dp"
        self.disabled = False

    def hide(self) -> None:
        self.opacity = 0.0
        self.height = "0dp"
        self.disabled = True


class TrialLabel(Label):
    pass


class AvailableTrialLayout(BoxLayout):
    ctx: KeymastersKeepContext

    area: KeymastersKeepRegions
    trial: KeymastersKeepLocationData

    unlock_button: Button
    complete_button: Button
    copy_button: Button

    def __init__(
        self,
        ctx: KeymastersKeepContext,
        area: KeymastersKeepRegions,
        trial: KeymastersKeepLocationData,
    ) -> None:
        super().__init__(orientation="horizontal", size_hint_y=None, height="40dp", spacing="8dp")

        self.ctx = ctx

        self.area = area
        self.trial = trial

        self.unlock_button = Button(
            text=" ",
            width="16dp",
            size_hint_x=None,
            halign="left",
        )

        self.unlock_button.bind(on_press=self.on_unlock_button_press)

        self.add_widget(self.unlock_button)

        self.complete_button = Button(
            text="Complete",
            width="88dp",
            size_hint_x=None,
            halign="left",
            disabled=True,
        )

        self.complete_button.bind(on_press=self.on_complete_button_press)

        self.add_widget(self.complete_button)

        self.copy_button = Button(
            text="Copy",
            width="56dp",
            size_hint_x=None,
            halign="left",
        )

        self.copy_button.bind(on_press=self.on_copy_button_press)

        self.add_widget(self.copy_button)

        trial_objective: str = self.ctx.area_trial_game_objectives[self.trial.name]

        trial_label: TrialLabel = TrialLabel(
            text=f"[b]{self.trial.name}[/b]\n[color=bbbbbb]{escape_markup(trial_objective)}[/color]",
            markup=True,
            size_hint_y=None,
            height="40dp",
            halign="left",
            valign="middle",
        )

        trial_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.add_widget(trial_label)

    def show(self) -> None:
        self.opacity = 1.0
        self.height = "40dp"
        self.disabled = False

    def hide(self) -> None:
        self.opacity = 0.0
        self.height = "0dp"
        self.disabled = True

    def on_unlock_button_press(self, _) -> None:
        if self.complete_button.disabled:
            self.complete_button.disabled = False
        else:
            self.complete_button.disabled = True

    def on_complete_button_press(self, _) -> None:
        self.complete_button.disabled = True
        self.ctx.complete_location(self.trial.archipelago_id)

    def on_copy_button_press(self, _) -> None:
        Clipboard.copy(self.ctx.area_trial_game_objectives[self.trial.name])


class GoalAreaLabel(Label):
    ctx: KeymastersKeepContext

    def __init__(self, ctx: KeymastersKeepContext) -> None:
        super().__init__(
            text=f"[b]{KeymastersKeepRegions.THE_KEYMASTERS_CHALLENGE_CHAMBER.value}[/b]",
            markup=True,
            font_size="32dp",
            size_hint_y=None,
            height="70dp",
            halign="left",
            valign="bottom",
        )

        self.ctx = ctx

        self.bind(size=lambda label, size: setattr(label, "text_size", size))

    def show(self) -> None:
        self.opacity = 1.0
        self.height = "70dp"
        self.disabled = False

    def hide(self) -> None:
        self.opacity = 0.0
        self.height = "0dp"
        self.disabled = True


class GoalGameLabel(Label):
    ctx: KeymastersKeepContext

    def __init__(self, ctx: KeymastersKeepContext) -> None:
        super().__init__(
            text=f"[b]{ctx.goal_game}[/b]",
            markup=True,
            font_size="18dp",
            size_hint_y=None,
            height="40dp",
            halign="left",
            valign="middle",
        )

        if ctx.goal_game_optional_constraints:
            optional_constraints: str = "  /  ".join(ctx.goal_game_optional_constraints)
            self.text += f"    [color=888888] Optional Conditions:  {optional_constraints}[/color]"

        self.ctx = ctx

        self.bind(size=lambda label, size: setattr(label, "text_size", size))

    def show(self) -> None:
        self.opacity = 1.0
        self.height = "40dp"
        self.disabled = False

    def hide(self) -> None:
        self.opacity = 0.0
        self.height = "0dp"
        self.disabled = True


class AvailableGoalTrialLayout(BoxLayout):
    ctx: KeymastersKeepContext

    unlock_button: Button
    complete_button: Button
    copy_button: Button

    def __init__(self, ctx: KeymastersKeepContext) -> None:
        super().__init__(orientation="horizontal", size_hint_y=None, height="40dp", spacing="8dp")

        self.ctx = ctx

        self.unlock_button = Button(
            text=" ",
            width="16dp",
            size_hint_x=None,
            halign="left",
        )

        self.unlock_button.bind(on_press=self.on_unlock_button_press)

        self.add_widget(self.unlock_button)

        self.complete_button = Button(
            text="Complete",
            width="88dp",
            size_hint_x=None,
            halign="left",
            disabled=True,
        )

        self.complete_button.bind(on_press=self.on_complete_button_press)

        self.add_widget(self.complete_button)

        self.copy_button = Button(
            text="Copy",
            width="56dp",
            size_hint_x=None,
            halign="left",
        )

        self.copy_button.bind(on_press=self.on_copy_button_press)

        self.add_widget(self.copy_button)

        trial_name: str = KeymastersKeepLocations.THE_KEYMASTERS_CHALLENGE_CHAMBER_VICTORY.value
        trial_objective: str = self.ctx.goal_trial_game_objective

        trial_label: TrialLabel = TrialLabel(
            text=f"[b]{trial_name}[/b]\n[color=bbbbbb]{escape_markup(trial_objective)}[/color]",
            markup=True,
            size_hint_y=None,
            height="40dp",
            halign="left",
            valign="middle",
        )

        trial_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.add_widget(trial_label)

    def show(self) -> None:
        self.opacity = 1.0
        self.height = "40dp"
        self.disabled = False

    def hide(self) -> None:
        self.opacity = 0.0
        self.height = "0dp"
        self.disabled = True

    def on_unlock_button_press(self, _) -> None:
        if self.complete_button.disabled:
            self.complete_button.disabled = False
        else:
            self.complete_button.disabled = True

    def on_complete_button_press(self, _) -> None:
        self.complete_button.disabled = True

        self.ctx.complete_location(
            location_data[KeymastersKeepLocations.THE_KEYMASTERS_CHALLENGE_CHAMBER_VICTORY].archipelago_id
        )

    def on_copy_button_press(self, _) -> None:
        Clipboard.copy(self.ctx.goal_trial_game_objective)


class AvailableTrialsLayout(ScrollView):
    ctx: KeymastersKeepContext

    layout: BoxLayout

    no_trials_label: Label

    area_labels: Dict[KeymastersKeepRegions, TrialAreaLabel]
    game_labels: Dict[KeymastersKeepRegions, TrialGameLabel]
    available_trial_layouts: Dict[KeymastersKeepRegions, List[AvailableTrialLayout]]

    goal_area_label: GoalAreaLabel
    goal_game_label: GoalGameLabel
    goal_trial_layout: AvailableGoalTrialLayout

    def __init__(
        self,
        ctx: KeymastersKeepContext,
    ) -> None:
        super().__init__(size_hint=(0.7, 1.0))

        self.ctx = ctx

        self.layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter("height"))

        self.area_labels = dict()
        self.game_labels = dict()
        self.available_trial_layouts = dict()

        self.no_trials_label = Label(
            text="No trials are currently available. Unlock keep areas to uncover more!",
            font_size="18dp",
            size_hint_y=None,
            height="30dp",
            halign="left",
            valign="middle",
        )

        self.no_trials_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.layout.add_widget(self.no_trials_label)

        if self.ctx.goal == KeymastersKeepGoals.KEYMASTERS_CHALLENGE:
            self.goal_area_label = GoalAreaLabel(self.ctx)
            self.goal_area_label.hide()

            self.layout.add_widget(self.goal_area_label)

            self.goal_game_label = GoalGameLabel(self.ctx)
            self.goal_game_label.hide()

            self.layout.add_widget(self.goal_game_label)

            self.goal_trial_layout = AvailableGoalTrialLayout(self.ctx)
            self.goal_trial_layout.hide()

            self.layout.add_widget(self.goal_trial_layout)

        area: KeymastersKeepRegions
        trials: List[KeymastersKeepLocationData]
        for area, trials in self.ctx.area_trials.items():
            area_label: TrialAreaLabel = TrialAreaLabel(self.ctx, area)
            area_label.hide()

            self.layout.add_widget(area_label)
            self.area_labels[area] = area_label

            game_label: TrialGameLabel = TrialGameLabel(self.ctx, area)
            game_label.hide()

            self.layout.add_widget(game_label)
            self.game_labels[area] = game_label

            trial: KeymastersKeepLocationData
            for trial in trials:
                available_trial_layout: AvailableTrialLayout = AvailableTrialLayout(self.ctx, area, trial)
                available_trial_layout.hide()

                self.layout.add_widget(available_trial_layout)

                if area not in self.available_trial_layouts:
                    self.available_trial_layouts[area] = list()

                self.available_trial_layouts[area].append(available_trial_layout)

        self.add_widget(self.layout)

    def update(self) -> None:
        # No Trials Label
        at_least_one_unlocked_area: bool = False
        at_least_one_available_trial: bool = False

        area: KeymastersKeepRegions
        unlocked: bool
        for area, unlocked in self.ctx.game_state["areas_unlocked"].items():
            if area in self.ctx.shop_data:
                continue

            if unlocked:
                at_least_one_unlocked_area = True

                for _ in self.ctx.game_state["trials_available"][area]:
                    at_least_one_available_trial = True
                    break

        if self.ctx.goal == KeymastersKeepGoals.KEYMASTERS_CHALLENGE:
            unlocked: bool = self.ctx.game_state["goal_challenge_chamber_unlocked"]
            has_available_trial: bool = not self.ctx.game_state["goal_can_claim_victory"]

            if unlocked and has_available_trial:
                at_least_one_unlocked_area = True
                at_least_one_available_trial = True

        if not at_least_one_unlocked_area or not at_least_one_available_trial:
            self.no_trials_label.opacity = 1.0
            self.no_trials_label.height = "30dp"
            self.no_trials_label.disabled = False

            if self.ctx.game_state["trial_count"] >= self.ctx.game_state["trial_count_total"]:
                self.no_trials_label.text = "You have completed all trials! Congratulations!"
        else:
            self.no_trials_label.opacity = 0.0
            self.no_trials_label.height = "0dp"
            self.no_trials_label.disabled = True

        # Goal Area Label, Game Label and Trial Layout
        if self.ctx.goal == KeymastersKeepGoals.KEYMASTERS_CHALLENGE:
            unlocked: bool = self.ctx.game_state["goal_challenge_chamber_unlocked"]
            has_available_trial: bool = not self.ctx.game_state["goal_can_claim_victory"]

            if unlocked and has_available_trial:
                self.goal_area_label.show()
                self.goal_game_label.show()
                self.goal_trial_layout.show()
            else:
                self.goal_area_label.hide()
                self.goal_game_label.hide()
                self.goal_trial_layout.hide()

        # Area Labels, Game Labels and Available Trials
        area: KeymastersKeepRegions
        for area in self.area_labels:
            unlocked: bool = self.ctx.game_state["areas_unlocked"][area]
            has_available_trials: bool = bool(self.ctx.game_state["trials_available"][area])

            if unlocked and has_available_trials:
                self.area_labels[area].show()
                self.game_labels[area].show()

                available_trial_layout: AvailableTrialLayout
                for available_trial_layout in self.available_trial_layouts[area]:
                    if available_trial_layout.trial.archipelago_id in self.ctx.game_state["trials_available"][area]:
                        available_trial_layout.show()
                    else:
                        available_trial_layout.hide()
            else:
                self.area_labels[area].hide()
                self.game_labels[area].hide()

                available_trial_layout: AvailableTrialLayout
                for available_trial_layout in self.available_trial_layouts[area]:
                    available_trial_layout.hide()


class TrialsTabLayout(BoxLayout):
    ctx: KeymastersKeepContext

    layout_content: BoxLayout

    layout_content_available_trials: AvailableTrialsLayout

    layout_not_connected: BoxLayout

    def __init__(self, ctx: KeymastersKeepContext) -> None:
        super().__init__(orientation="vertical")

        self.ctx = ctx

        self.layout_not_connected = NotConnectedLayout(self.ctx)
        self.add_widget(self.layout_not_connected)

        self.layout_content = BoxLayout(orientation="horizontal", spacing="16dp", padding=["8dp", "0dp"])
        self.add_widget(self.layout_content)

        self.update()

    def update(self) -> None:
        if not self.ctx.is_game_state_initialized:
            self.layout_not_connected.show()
            self.layout_content.clear_widgets()

            return

        self.layout_not_connected.hide()

        if not len(self.layout_content.children):
            self.layout_content_available_trials = AvailableTrialsLayout(self.ctx)
            self.layout_content.add_widget(self.layout_content_available_trials)

        self.layout_content_available_trials.update()


class CompletedGoalTrialLayout(BoxLayout):
    ctx: KeymastersKeepContext

    copy_button: Button

    def __init__(self, ctx: KeymastersKeepContext) -> None:
        super().__init__(orientation="horizontal", size_hint_y=None, height="40dp", spacing="8dp")

        self.ctx = ctx

        self.copy_button = Button(
            text="Copy",
            width="56dp",
            size_hint_x=None,
            halign="left",
        )

        self.copy_button.bind(on_press=self.on_copy_button_press)

        self.add_widget(self.copy_button)

        trial_name: str = KeymastersKeepLocations.THE_KEYMASTERS_CHALLENGE_CHAMBER_VICTORY.value
        trial_objective: str = self.ctx.goal_trial_game_objective

        trial_label: TrialLabel = TrialLabel(
            text=f"[b]{trial_name}[/b]\n[color=bbbbbb]{escape_markup(trial_objective)}[/color]",
            markup=True,
            size_hint_y=None,
            height="40dp",
            halign="left",
            valign="middle",
        )

        trial_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.add_widget(trial_label)

    def show(self) -> None:
        self.opacity = 1.0
        self.height = "40dp"
        self.disabled = False

    def hide(self) -> None:
        self.opacity = 0.0
        self.height = "0dp"
        self.disabled = True

    def on_copy_button_press(self, _) -> None:
        Clipboard.copy(self.ctx.goal_trial_game_objective)


class CompletedTrialLayout(BoxLayout):
    ctx: KeymastersKeepContext

    area: KeymastersKeepRegions
    trial: KeymastersKeepLocationData

    copy_button: Button

    def __init__(
        self,
        ctx: KeymastersKeepContext,
        area: KeymastersKeepRegions,
        trial: KeymastersKeepLocationData,
    ) -> None:
        super().__init__(orientation="horizontal", size_hint_y=None, height="40dp", spacing="8dp")

        self.ctx = ctx

        self.area = area
        self.trial = trial

        self.copy_button = Button(
            text="Copy",
            width="56dp",
            size_hint_x=None,
            halign="left",
        )

        self.copy_button.bind(on_press=self.on_copy_button_press)

        self.add_widget(self.copy_button)

        trial_objective: str = self.ctx.area_trial_game_objectives[self.trial.name]

        trial_label: TrialLabel = TrialLabel(
            text=f"[b]{self.trial.name}[/b]\n[color=bbbbbb]{escape_markup(trial_objective)}[/color]",
            markup=True,
            size_hint_y=None,
            height="40dp",
            halign="left",
            valign="middle",
        )

        trial_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.add_widget(trial_label)

    def show(self) -> None:
        self.opacity = 1.0
        self.height = "40dp"
        self.disabled = False

    def hide(self) -> None:
        self.opacity = 0.0
        self.height = "0dp"
        self.disabled = True

    def on_copy_button_press(self, _) -> None:
        Clipboard.copy(self.ctx.area_trial_game_objectives[self.trial.name])


class CompletedTrialsLayout(ScrollView):
    ctx: KeymastersKeepContext

    layout: BoxLayout

    no_trials_label: Label

    area_labels: Dict[KeymastersKeepRegions, TrialAreaLabel]
    game_labels: Dict[KeymastersKeepRegions, TrialGameLabel]
    completed_trial_layouts: Dict[KeymastersKeepRegions, List[CompletedTrialLayout]]

    goal_area_label: GoalAreaLabel
    goal_game_label: GoalGameLabel
    goal_trial_layout: CompletedGoalTrialLayout

    def __init__(self, ctx: KeymastersKeepContext) -> None:
        super().__init__(size_hint=(0.7, 1.0))

        self.ctx = ctx

        self.layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter("height"))

        self.area_labels = dict()
        self.game_labels = dict()
        self.completed_trial_layouts = dict()

        self.no_trials_label = Label(
            text="You haven't completed any trials yet. Once you do, they'll appear here!",
            font_size="18dp",
            size_hint_y=None,
            height="30dp",
            halign="left",
            valign="middle",
        )

        self.no_trials_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.layout.add_widget(self.no_trials_label)

        if self.ctx.goal == KeymastersKeepGoals.KEYMASTERS_CHALLENGE:
            self.goal_area_label = GoalAreaLabel(self.ctx)
            self.goal_area_label.hide()

            self.layout.add_widget(self.goal_area_label)

            self.goal_game_label = GoalGameLabel(self.ctx)
            self.goal_game_label.hide()

            self.layout.add_widget(self.goal_game_label)

            self.goal_trial_layout = CompletedGoalTrialLayout(self.ctx)
            self.goal_trial_layout.hide()

            self.layout.add_widget(self.goal_trial_layout)

        area: KeymastersKeepRegions
        trials: List[KeymastersKeepLocationData]
        for area, trials in self.ctx.area_trials.items():
            area_label: TrialAreaLabel = TrialAreaLabel(self.ctx, area)
            area_label.hide()

            self.layout.add_widget(area_label)
            self.area_labels[area] = area_label

            game_label: TrialGameLabel = TrialGameLabel(self.ctx, area)
            game_label.hide()

            self.layout.add_widget(game_label)
            self.game_labels[area] = game_label

            trial: KeymastersKeepLocationData
            for trial in trials:
                completed_trial_layout: CompletedTrialLayout = CompletedTrialLayout(self.ctx, area, trial)
                completed_trial_layout.hide()

                self.layout.add_widget(completed_trial_layout)

                if area not in self.completed_trial_layouts:
                    self.completed_trial_layouts[area] = list()

                self.completed_trial_layouts[area].append(completed_trial_layout)

        self.add_widget(self.layout)

    def update(self) -> None:
        # No Trials Label
        at_least_one_completed_trial: bool = self.ctx.game_state["trial_count"] > 0

        if not at_least_one_completed_trial:
            self.no_trials_label.opacity = 1.0
            self.no_trials_label.height = "30dp"
            self.no_trials_label.disabled = False
        else:
            self.no_trials_label.opacity = 0.0
            self.no_trials_label.height = "0dp"
            self.no_trials_label.disabled = True

        # Goal Area Label, Game Label and Trial Layout
        if self.ctx.goal == KeymastersKeepGoals.KEYMASTERS_CHALLENGE:
            unlocked: bool = self.ctx.game_state["goal_challenge_chamber_unlocked"]
            has_completed_trial: bool = self.ctx.game_state["goal_can_claim_victory"]

            if unlocked and has_completed_trial:
                self.goal_area_label.show()
                self.goal_game_label.show()
                self.goal_trial_layout.show()
            else:
                self.goal_area_label.hide()
                self.goal_game_label.hide()
                self.goal_trial_layout.hide()

        # Area Labels, Game Labels and Completed Trials
        area: KeymastersKeepRegions
        for area in self.area_labels:
            unlocked: bool = self.ctx.game_state["areas_unlocked"][area]

            has_completed_trials: bool = (
                len(self.ctx.game_state["trials_available"][area]) < len(self.ctx.area_trials[area])
            )

            if unlocked and has_completed_trials:
                self.area_labels[area].show()
                self.game_labels[area].show()

                completed_trial_layout: CompletedTrialLayout
                for completed_trial_layout in self.completed_trial_layouts[area]:
                    if completed_trial_layout.trial.archipelago_id not in self.ctx.game_state["trials_available"][area]:
                        completed_trial_layout.show()
                    else:
                        completed_trial_layout.hide()
            else:
                self.area_labels[area].hide()
                self.game_labels[area].hide()

                completed_trial_layout: CompletedTrialLayout
                for completed_trial_layout in self.completed_trial_layouts[area]:
                    completed_trial_layout.hide()


class TrialsCompletedTabLayout(BoxLayout):
    ctx: KeymastersKeepContext

    layout_content: BoxLayout

    layout_content_completed_trials: CompletedTrialsLayout

    layout_not_connected: BoxLayout

    def __init__(self, ctx: KeymastersKeepContext) -> None:
        super().__init__(orientation="vertical")

        self.ctx = ctx

        self.layout_not_connected = NotConnectedLayout(self.ctx)
        self.add_widget(self.layout_not_connected)

        self.layout_content = BoxLayout(orientation="horizontal", spacing="16dp", padding=["8dp", "0dp"])
        self.add_widget(self.layout_content)

        self.update()

    def update(self) -> None:
        if not self.ctx.is_game_state_initialized:
            self.layout_not_connected.show()
            self.layout_content.clear_widgets()

            return

        self.layout_not_connected.hide()

        if not len(self.layout_content.children):
            self.layout_content_completed_trials = CompletedTrialsLayout(self.ctx)
            self.layout_content.add_widget(self.layout_content_completed_trials)

        self.layout_content_completed_trials.update()


class ShopLabel(Label):
    ctx: KeymastersKeepContext

    shop: KeymastersKeepShops

    def __init__(self, ctx: KeymastersKeepContext, shop: KeymastersKeepShops) -> None:
        super().__init__(
            text=f"[b]{shop.value}[/b]",
            markup=True,
            font_size="32dp",
            size_hint_y=None,
            height="70dp",
            halign="left",
            valign="bottom",
        )

        self.ctx = ctx
        self.shop = shop

        self.bind(size=lambda label, size: setattr(label, "text_size", size))

    def show(self) -> None:
        self.opacity = 1.0
        self.height = "70dp"
        self.disabled = False

    def hide(self) -> None:
        self.opacity = 0.0
        self.height = "0dp"
        self.disabled = True


class ShopkeeperLabel(Label):
    ctx: KeymastersKeepContext

    shopkeeper: KeymastersKeepShopkeepers

    def __init__(self, ctx: KeymastersKeepContext, shopkeeper: KeymastersKeepShopkeepers) -> None:
        super().__init__(
            text=f"[b]Shopkeeper:[/b] {shopkeeper.value}",
            markup=True,
            font_size="18dp",
            size_hint_y=None,
            height="30dp",
            halign="left",
            valign="middle",
        )

        self.ctx = ctx
        self.shopkeeper = shopkeeper

        self.bind(size=lambda label, size: setattr(label, "text_size", size))

    def show(self) -> None:
        self.opacity = 1.0
        self.height = "30dp"
        self.disabled = False

    def hide(self) -> None:
        self.opacity = 0.0
        self.height = "0dp"
        self.disabled = True


class ShopkeeperGreetingLabel(Label):
    ctx: KeymastersKeepContext

    shopkeeper: KeymastersKeepShopkeepers

    def __init__(self, ctx: KeymastersKeepContext, shopkeeper: KeymastersKeepShopkeepers) -> None:
        super().__init__(
            text=f"[color=888888]\"{shopkeeper_greetings[shopkeeper]}\"[/color]",
            markup=True,
            font_size="14dp",
            size_hint_y=None,
            height="40dp",
            halign="left",
            valign="top",
        )

        self.ctx = ctx
        self.shopkeeper = shopkeeper

        self.bind(size=lambda label, size: setattr(label, "text_size", size))

    def show(self) -> None:
        self.opacity = 1.0
        self.height = "40dp"
        self.disabled = False

    def hide(self) -> None:
        self.opacity = 0.0
        self.height = "0dp"
        self.disabled = True


class ShopItemLayout(BoxLayout):
    ctx: KeymastersKeepContext

    shop: KeymastersKeepShops
    shop_location_name: str
    shop_item_data: Dict[str, Any]

    shop_item_label: Label

    item_text: str
    item_description: str

    purchase_button: Button

    def __init__(
        self,
        ctx: KeymastersKeepContext,
        shop: KeymastersKeepShops,
        shop_location_name: str,
        shop_item_data: Dict[str, Any],
    ) -> None:
        super().__init__(orientation="horizontal", size_hint_y=None, height="40dp", spacing="8dp")

        self.ctx = ctx

        self.shop = shop
        self.shop_location_name = shop_location_name
        self.shop_item_data = shop_item_data

        self.purchase_button = Button(
            text="Purchase",
            width="100dp",
            size_hint_x=None,
            halign="left",
            disabled=True,
        )

        self.purchase_button.bind(on_press=self.on_purchase_button_press)

        self.add_widget(self.purchase_button)

        self.item_text = f"[color={item_classification_to_colors[self.shop_item_data['item']['classification']]}][b]{self.shop_item_data['item']['name']}[/b][/color]    "
        self.item_text += f"[b]Rarity:[/b] {item_classification_to_rarities[self.shop_item_data['item']['classification']]}    "

        player_data: Dict[str, Any] = self.shop_item_data["item"]["player"]
        self.item_text += f"[b]Original Owner:[/b] [color=EE00EE]{player_data['name']}[/color] of [color=6D8BE8]{player_data['game']}[/color]    "

        self.item_text += f"[b]Price:[/b] 1x  [color=00FF7F]{self.shop_item_data['relic'].value}[/color]"

        self.item_description: str = random.choice(unknown_item_descriptions)

        if player_data["game"] in item_descriptions:
            if self.shop_item_data["item"]["name"] in item_descriptions[player_data["game"]]:
                self.item_description = item_descriptions[player_data["game"]][self.shop_item_data["item"]["name"]]

        self.shop_item_label = Label(
            text=f"{self.item_text}\n[color=bbbbbb]{self.item_description}[/color]",
            markup=True,
            size_hint_y=None,
            height="40dp",
            halign="left",
            valign="middle",
        )

        self.shop_item_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.add_widget(self.shop_item_label)

    def show(self) -> None:
        self.opacity = 1.0
        self.height = "40dp"
        self.disabled = False

    def hide(self) -> None:
        self.opacity = 0.0
        self.height = "0dp"
        self.disabled = True

    def on_purchase_button_press(self, _) -> None:
        self.purchase_button.disabled = True
        self.ctx.complete_location(self.shop_item_data["location_data"].archipelago_id)

    def update(self):
        if self.shop_item_data["relic"] not in self.ctx.game_state["relics"]:
            return

        shop_item_is_purchaseable: bool = self.ctx.game_state["relics"][self.shop_item_data["relic"]]
        shop_item_was_purchased: bool = self.shop_item_data["location_data"].archipelago_id in self.ctx.game_state["shop_items_purchased"][self.shop]

        if shop_item_was_purchased:
            self.purchase_button.disabled = True
            self.purchase_button.text = "Purchased!"

            self.shop_item_label.text = f"[s]{self.item_text}\n[color=bbbbbb]{self.item_description}[/color][/s]"
        elif shop_item_is_purchaseable:
            self.purchase_button.disabled = False
            self.purchase_button.text = "Purchase"

            self.shop_item_label.text = f"{self.item_text}\n[color=bbbbbb]{self.item_description}[/color]"
        else:
            self.purchase_button.disabled = True
            self.purchase_button.text = "Need Relic"

            self.shop_item_label.text = f"{self.item_text}\n[color=bbbbbb]{self.item_description}[/color]"


class ShopItemSpacer(Widget):
    def __init__(self) -> None:
        super().__init__(size_hint_y=None, height="8dp")

    def show(self) -> None:
        self.opacity = 1.0
        self.height = "8dp"
        self.disabled = False

    def hide(self) -> None:
        self.opacity = 0.0
        self.height = "0dp"
        self.disabled = True


class ShopsLayout(ScrollView):
    ctx: KeymastersKeepContext

    layout: BoxLayout

    no_shop_label: Label

    shop_labels: Dict[Tuple[KeymastersKeepRegions, KeymastersKeepShops], ShopLabel]
    shopkeeper_labels: Dict[KeymastersKeepShopkeepers, ShopkeeperLabel]
    shopkeeper_greeting_labels: Dict[KeymastersKeepShopkeepers, ShopkeeperGreetingLabel]
    shop_item_layouts: Dict[KeymastersKeepShops, List[ShopItemLayout]]
    shop_item_spacers: Dict[KeymastersKeepShops, List[ShopItemSpacer]]

    def __init__(
        self,
        ctx: KeymastersKeepContext,
    ) -> None:
        super().__init__(size_hint=(0.7, 1.0))

        self.ctx = ctx

        self.layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter("height"))

        self.shop_labels = dict()
        self.shopkeeper_labels = dict()
        self.shopkeeper_greeting_labels = dict()
        self.shop_item_layouts = dict()
        self.shop_item_spacers = dict()

        no_shop_label_text: str = "No shops have been discovered yet. Unlock keep areas to uncover more!"

        if not self.ctx.shops:
            no_shop_label_text = "Shops are disabled for this seed. No shops will be found."

        self.no_shop_label = Label(
            text=no_shop_label_text,
            font_size="18dp",
            size_hint_y=None,
            height="30dp",
            halign="left",
            valign="middle",
        )

        self.no_shop_label.bind(size=lambda label, size: setattr(label, "text_size", size))

        self.layout.add_widget(self.no_shop_label)

        area: KeymastersKeepRegions
        data: Dict[str, Any]
        for area, data in self.ctx.shop_data.items():
            shop_label: ShopLabel = ShopLabel(self.ctx, data["shop"])
            shop_label.hide()

            self.layout.add_widget(shop_label)
            self.shop_labels[area, data["shop"]] = shop_label

            shopkeeper_label: ShopkeeperLabel = ShopkeeperLabel(self.ctx, data["shopkeeper"])
            shopkeeper_label.hide()

            self.layout.add_widget(shopkeeper_label)
            self.shopkeeper_labels[data["shopkeeper"]] = shopkeeper_label

            shopkeeper_greeting_label: ShopkeeperGreetingLabel = ShopkeeperGreetingLabel(self.ctx, data["shopkeeper"])
            shopkeeper_greeting_label.hide()

            self.layout.add_widget(shopkeeper_greeting_label)
            self.shopkeeper_greeting_labels[data["shopkeeper"]] = shopkeeper_greeting_label

            location_name: str
            shop_item_data: Dict[str, Any]
            for location_name, shop_item_data in data["shop_items"].items():
                shop_item_layout: ShopItemLayout = ShopItemLayout(self.ctx, data["shop"], location_name, shop_item_data)
                shop_item_layout.hide()

                self.layout.add_widget(shop_item_layout)

                if data["shop"] not in self.shop_item_layouts:
                    self.shop_item_layouts[data["shop"]] = list()

                self.shop_item_layouts[data["shop"]].append(shop_item_layout)

                shop_item_spacer: ShopItemSpacer = ShopItemSpacer()
                shop_item_spacer.hide()

                self.layout.add_widget(shop_item_spacer)

                if data["shop"] not in self.shop_item_spacers:
                    self.shop_item_spacers[data["shop"]] = list()

                self.shop_item_spacers[data["shop"]].append(shop_item_spacer)

        self.add_widget(self.layout)

    def update(self) -> None:
        at_least_one_shop_discovered: bool = False

        area: KeymastersKeepRegions
        unlocked: bool
        for area, unlocked in self.ctx.game_state["areas_unlocked"].items():
            if area not in self.ctx.shop_data:
                continue

            if unlocked:
                at_least_one_shop_discovered = True
                break

        if not at_least_one_shop_discovered:
            self.no_shop_label.opacity = 1.0
            self.no_shop_label.height = "30dp"
            self.no_shop_label.disabled = False
        else:
            self.no_shop_label.opacity = 0.0
            self.no_shop_label.height = "0dp"
            self.no_shop_label.disabled = True

        area: KeymastersKeepRegions
        shop: KeymastersKeepShops
        for area, shop in self.shop_labels:
            unlocked: bool = self.ctx.game_state["areas_unlocked"][area]

            if unlocked:
                self.shop_labels[(area, shop)].show()
                self.shopkeeper_labels[self.ctx.shop_data[area]["shopkeeper"]].show()
                self.shopkeeper_greeting_labels[self.ctx.shop_data[area]["shopkeeper"]].show()

                shop_item_layout: ShopItemLayout
                for shop_item_layout in self.shop_item_layouts[shop]:
                    shop_item_layout.update()
                    shop_item_layout.show()

                shop_item_spacer: ShopItemSpacer
                for shop_item_spacer in self.shop_item_spacers[shop]:
                    shop_item_spacer.show()
            else:
                self.shop_labels[(area, shop)].hide()
                self.shopkeeper_labels[self.ctx.shop_data[area]["shopkeeper"]].hide()
                self.shopkeeper_greeting_labels[self.ctx.shop_data[area]["shopkeeper"]].hide()

                shop_item_layout: ShopItemLayout
                for shop_item_layout in self.shop_item_layouts[shop]:
                    shop_item_layout.hide()
                    shop_item_layout.update()

                shop_item_spacer: ShopItemSpacer
                for shop_item_spacer in self.shop_item_spacers[shop]:
                    shop_item_spacer.hide()


class ShopsTabLayout(BoxLayout):
    ctx: KeymastersKeepContext

    layout_content: BoxLayout

    layout_content_shops: ShopsLayout

    layout_not_connected: BoxLayout

    def __init__(self, ctx: KeymastersKeepContext) -> None:
        super().__init__(orientation="vertical")

        self.ctx = ctx

        self.layout_not_connected = NotConnectedLayout(self.ctx)
        self.add_widget(self.layout_not_connected)

        self.layout_content = BoxLayout(orientation="horizontal", spacing="16dp", padding=["8dp", "0dp"])
        self.add_widget(self.layout_content)

        self.update()

    def update(self) -> None:
        if not self.ctx.is_game_state_initialized:
            self.layout_not_connected.show()
            self.layout_content.clear_widgets()

            return

        self.layout_not_connected.hide()

        if not len(self.layout_content.children):
            self.layout_content_shops = ShopsLayout(self.ctx)
            self.layout_content.add_widget(self.layout_content_shops)

        self.layout_content_shops.update()
