from typing import *
import asyncio
import logging

from BaseClasses import ItemClassification
from NetUtils import JSONMessagePart
from kvui import GameManager, HoverBehavior, ServerToolTip, KivyJSONtoTextParser, LogtoUI
from kivy.app import App
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.tooltip import MDTooltip
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, BooleanProperty, NumericProperty

from .client import SC2Context, calc_unfinished_nodes, is_mission_available, compute_received_items, STARCRAFT2
from .item.item_descriptions import item_descriptions
from .item.item_annotations import ITEM_NAME_ANNOTATIONS
from .mission_order.entry_rules import RuleData, SubRuleRuleData, ItemRuleData
from .mission_tables import lookup_id_to_mission, campaign_race_exceptions, \
    SC2Mission, SC2Race
from .locations import LocationType, lookup_location_id_to_type, lookup_location_id_to_flags
from .options import LocationInclusion, MissionOrderScouting
from . import SC2World


class HoverableButton(HoverBehavior, Button):
    pass


class MissionButton(HoverableButton, MDTooltip):
    tooltip_text = StringProperty("Test")
    mission_id = NumericProperty(-1)
    is_exit = BooleanProperty(False)
    is_goal = BooleanProperty(False)
    showing_tooltip = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        super(HoverableButton, self).__init__(**kwargs)
        self._tooltip = ServerToolTip(text=self.text, markup=True)
        self._tooltip.padding = [5, 2, 5, 2]

    def on_enter(self):
        self._tooltip.text = self.tooltip_text

        if self.tooltip_text != "":
            self.display_tooltip()

    def on_leave(self):
        self.remove_tooltip()
    
    def display_tooltip(self, *args):
        self.showing_tooltip = True
        return super().display_tooltip(*args)
    
    def remove_tooltip(self, *args):
        self.showing_tooltip = False
        return super().remove_tooltip(*args)

    @property
    def ctx(self) -> SC2Context:
        return App.get_running_app().ctx

class CampaignScroll(ScrollView):
    border_on = BooleanProperty(False)

class MultiCampaignLayout(GridLayout):
    pass

class DownloadDataWarningMessage(Label):
    pass

class CampaignLayout(GridLayout):
    pass

class RegionLayout(GridLayout):
    pass

class ColumnLayout(GridLayout):
    pass

class MissionLayout(GridLayout):
    pass

class MissionCategory(GridLayout):
    pass


class SC2JSONtoKivyParser(KivyJSONtoTextParser):
    def _handle_item_name(self, node: JSONMessagePart):
        item_name = node["text"]
        if self.ctx.slot_info[node["player"]].game != STARCRAFT2 or item_name not in item_descriptions:
            return super()._handle_item_name(node)

        flags = node.get("flags", 0)
        item_types = []
        if flags & ItemClassification.progression:
            item_types.append("progression")
        if flags & ItemClassification.useful:
            item_types.append("useful")
        if flags & ItemClassification.trap:
            item_types.append("trap")
        if not item_types:
            item_types.append("normal")

        # TODO: Some descriptions are too long and get cut off. Is there a general solution or does someone need to manually check every description?
        desc = item_descriptions[item_name].replace(". \n", ".<br>").replace(". ", ".<br>").replace("\n", "<br>")
        annotation = ITEM_NAME_ANNOTATIONS.get(item_name)
        if annotation is not None:
            desc = f"{annotation}<br>{desc}"
        ref = "Item Class: " + ", ".join(item_types) + "<br><br>" + desc
        node.setdefault("refs", []).append(ref)
        return super(KivyJSONtoTextParser, self)._handle_item_name(node)

    def _handle_text(self, node: JSONMessagePart):
        if node.get("keep_markup", False):
            for ref in node.get("refs", []):
                node["text"] = f"[ref={self.ref_count}|{ref}]{node['text']}[/ref]"
                self.ref_count += 1
            return super(KivyJSONtoTextParser, self)._handle_text(node)
        else:
            return super()._handle_text(node)


class SC2Manager(GameManager):
    base_title = "Archipelago Starcraft 2 Client"

    campaign_panel: Optional[MultiCampaignLayout] = None
    campaign_scroll_panel: Optional[CampaignScroll] = None
    last_checked_locations: Set[int] = set()
    last_items_received: List[int] = []
    last_shown_tooltip: int = -1
    last_data_out_of_date = False
    mission_buttons: List[MissionButton] = []
    launching: Union[bool, int] = False  # if int -> mission ID
    refresh_from_launching = True
    first_check = True
    first_mission = ""
    button_colors: Dict[SC2Race, Tuple[float, float, float]] = {}
    ctx: SC2Context

    def __init__(self, ctx: SC2Context) -> None:
        super().__init__(ctx)
        self.json_to_kivy_parser = SC2JSONtoKivyParser(ctx)
        self.minimized = False

    def on_start(self) -> None:
        from . import gui_config
        warnings, window_width, window_height = gui_config.get_window_defaults()
        from kivy.core.window import Window
        original_size_x, original_size_y = Window.size
        Window.size = window_width, window_height
        Window.left -= max((window_width - original_size_x) // 2, 0)
        Window.top -= max((window_height - original_size_y) // 2, 0)
        # Add the logging handler manually here instead of using `logging_pairs` to avoid adding 2 unnecessary tabs
        logging.getLogger("Starcraft2").addHandler(LogtoUI(self.log_panels["All"].on_log))
        for startup_warning in warnings:
            logging.getLogger("Starcraft2").warning(f"Startup WARNING: {startup_warning}")
        for race in (SC2Race.TERRAN, SC2Race.PROTOSS, SC2Race.ZERG):
            errors, color = gui_config.get_button_color(race.name)
            self.button_colors[race] = color
            for error in errors:
                logging.getLogger("Starcraft2").warning(f"{race.name.title()} button color setting: {error}")

    def clear_tooltip(self) -> None:
        for button in self.mission_buttons:
            button.remove_tooltip()

    def shown_tooltip(self) -> int:
        for button in self.mission_buttons:
            if button.showing_tooltip:
                return button.mission_id
        return -1

    def build(self):
        container = super().build()

        panel = self.add_client_tab("Starcraft 2 Launcher", CampaignScroll())
        self.campaign_scroll_panel = panel.content
        self.campaign_panel = MultiCampaignLayout()
        panel.content.add_widget(self.campaign_panel)

        Clock.schedule_interval(self.build_mission_table, 0.5)

        return container

    def build_mission_table(self, dt) -> None:
        if self.launching:
            assert self.campaign_panel is not None
            self.refresh_from_launching = False

            self.campaign_panel.clear_widgets()
            self.campaign_panel.add_widget(Label(
                text="Launching Mission: " + lookup_id_to_mission[self.launching].mission_name
            ))
            if self.ctx.ui:
                self.ctx.ui.clear_tooltip()
            return
        
        sorted_items_received = sorted([item.item for item in self.ctx.items_received])
        shown_tooltip = self.shown_tooltip()
        hovering_tooltip = (
            self.last_shown_tooltip != -1
            and self.last_shown_tooltip == shown_tooltip
        )
        data_changed = (
            self.last_checked_locations != self.ctx.checked_locations
            or self.last_items_received != sorted_items_received
        )
        needs_redraw = (
            data_changed
            and not hovering_tooltip
            or not self.refresh_from_launching
            or self.last_data_out_of_date != self.ctx.data_out_of_date
            or self.first_check
        )
        self.last_shown_tooltip = shown_tooltip
        if not needs_redraw:
            return

        assert self.campaign_panel is not None
        self.refresh_from_launching = True

        self.clear_tooltip()
        self.campaign_panel.clear_widgets()
        if self.ctx.data_out_of_date:
            self.campaign_panel.add_widget(Label(text="", padding=[0, 5, 0, 5]))
            warning_label = DownloadDataWarningMessage(
                text="Map/Mod data is out of date. Run /download_data in the client",
                padding=[0, 25, 0, 25],
            )
            self.campaign_scroll_panel.border_on = True
            self.campaign_panel.add_widget(warning_label)
        else:
            self.campaign_scroll_panel.border_on = False
        self.last_data_out_of_date = self.ctx.data_out_of_date
        if len(self.ctx.custom_mission_order) == 0:
            self.campaign_panel.add_widget(Label(text="Connect to a world to see a mission layout here."))
            return

        self.last_checked_locations = self.ctx.checked_locations.copy()
        self.last_items_received = sorted_items_received
        self.first_check = False

        self.mission_buttons = []

        available_missions, available_layouts, available_campaigns, unfinished_missions = calc_unfinished_nodes(self.ctx)

        # The MultiCampaignLayout widget needs a default height of 15 (set in the .kv) to display the above Labels correctly
        multi_campaign_layout_height = 15

        # Fetching IDs of all the locations with hints  
        self.hints_to_highlight = []
        hints = self.ctx.stored_data.get(f"_read_hints_{self.ctx.team}_{self.ctx.slot}")
        if hints:
            for hint in hints:
                if hint['finding_player'] == self.ctx.slot and not hint['found']:
                    self.hints_to_highlight.append(hint['location'])

        MISSION_BUTTON_HEIGHT = 50
        MISSION_BUTTON_PADDING = 6
        for campaign_idx, campaign in enumerate(self.ctx.custom_mission_order):
            longest_column = max(len(col) for layout in campaign.layouts for col in layout.missions)
            if longest_column == 1:
                campaign_layout_height = 115
            else:
                campaign_layout_height = (longest_column + 2) * (MISSION_BUTTON_HEIGHT + MISSION_BUTTON_PADDING)
            multi_campaign_layout_height += campaign_layout_height
            campaign_layout = CampaignLayout(size_hint_y=None, height=campaign_layout_height)
            campaign_layout.add_widget(
                Label(text=campaign.name, size_hint_y=None, height=25, outline_width=1)
            )
            mission_layout = MissionLayout(padding=[10,0,10,0])
            for layout_idx, layout in enumerate(campaign.layouts):
                layout_panel = RegionLayout()
                layout_panel.add_widget(
                    Label(text=layout.name, size_hint_y=None, height=25, outline_width=1))
                column_panel = ColumnLayout()

                for column in layout.missions:
                    category_panel = MissionCategory(padding=[3,MISSION_BUTTON_PADDING,3,MISSION_BUTTON_PADDING])
                    
                    for mission in column:
                        mission_id = mission.mission_id

                        # Empty mission slots
                        if mission_id == -1:
                            column_spacer = Label(text='', size_hint_y=None, height=MISSION_BUTTON_HEIGHT)
                            category_panel.add_widget(column_spacer)
                            continue

                        mission_obj = lookup_id_to_mission[mission_id]
                        mission_finished = self.ctx.is_mission_completed(mission_id)
                        is_layout_exit = mission_id in layout.exits and not mission_finished
                        is_campaign_exit = mission_id in campaign.exits and not mission_finished

                        text, tooltip = self.mission_text(
                            self.ctx, mission_id, mission_obj,
                            layout_idx, is_layout_exit, layout.name,
                            campaign_idx, is_campaign_exit, campaign.name,
                            available_missions, available_layouts, available_campaigns, unfinished_missions
                        )

                        mission_button = MissionButton(text=text, size_hint_y=None, height=MISSION_BUTTON_HEIGHT)

                        mission_button.mission_id = mission_id

                        if mission_id in self.ctx.final_mission_ids:
                            mission_button.is_goal = True
                        if is_layout_exit or is_campaign_exit:
                            mission_button.is_exit = True

                        mission_race = mission_obj.race
                        if mission_race == SC2Race.ANY:
                            mission_race = mission_obj.campaign.race
                        race = campaign_race_exceptions.get(mission_obj, mission_race)
                        if race in self.button_colors:
                            mission_button.background_color = self.button_colors[race]
                        mission_button.tooltip_text = tooltip
                        mission_button.bind(on_press=self.mission_callback)
                        self.mission_buttons.append(mission_button)
                        category_panel.add_widget(mission_button)

                    # layout_panel.add_widget(Label(text=""))
                    column_panel.add_widget(category_panel)
                layout_panel.add_widget(column_panel)
                mission_layout.add_widget(layout_panel)
            campaign_layout.add_widget(mission_layout)
            self.campaign_panel.add_widget(campaign_layout)
        self.campaign_panel.height = multi_campaign_layout_height

        # For some reason the AP HoverBehavior won't send an enter event if a button spawns under the cursor,
        # so manually send an enter event if a button is hovered immediately
        for button in self.mission_buttons:
            if button.hovered:
                button.dispatch("on_enter")
                break

    def mission_text(
        self, ctx: SC2Context, mission_id: int, mission_obj: SC2Mission,
        layout_id: int, is_layout_exit: bool, layout_name: str, campaign_id: int, is_campaign_exit: bool, campaign_name: str,
        available_missions: List[int], available_layouts: Dict[int, List[int]], available_campaigns: List[int],
        unfinished_missions: List[int]
    ) -> Tuple[str, str]:
        COLOR_MISSION_IMPORTANT = "6495ED" # blue
        COLOR_MISSION_UNIMPORTANT = "A0BEF4" # lighter blue
        COLOR_MISSION_CLEARED = "FFFFFF" # white
        COLOR_MISSION_LOCKED = "A9A9A9" # gray
        COLOR_PARENT_LOCKED = "848484" # darker gray
        COLOR_MISSION_FINAL = "FFBC95" # orange
        COLOR_MISSION_FINAL_LOCKED = "D0C0BE" # gray + orange
        COLOR_FINAL_PARENT_LOCKED = "D0C0BE" # gray + orange
        COLOR_FINAL_MISSION_REMINDER = "FF5151" # light red
        COLOR_VICTORY_LOCATION = "FFC156" # gold
        COLOR_TOOLTIP_DONE = "51FF51" # light green
        COLOR_TOOLTIP_NOT_DONE = "FF5151" # light red

        text = mission_obj.mission_name
        tooltip: str = ""
        remaining_locations, plando_locations, remaining_count = self.sort_unfinished_locations(mission_id)
        campaign_locked = campaign_id not in available_campaigns
        layout_locked = layout_id not in available_layouts[campaign_id]

        # Map has uncollected locations
        if mission_id in unfinished_missions:
            if self.any_valuable_locations(remaining_locations):
                text = f"[color={COLOR_MISSION_IMPORTANT}]{text}[/color]"
            else:
                text = f"[color={COLOR_MISSION_UNIMPORTANT}]{text}[/color]"
        elif mission_id in available_missions:
            text = f"[color={COLOR_MISSION_CLEARED}]{text}[/color]"
        # Map requirements not met
        else:
            mission_rule, layout_rule, campaign_rule = ctx.mission_id_to_entry_rules[mission_id]
            mission_has_rule = mission_rule.amount > 0
            layout_has_rule = layout_rule.amount > 0
            extra_reqs = False
            if campaign_locked:
                text = f"[color={COLOR_PARENT_LOCKED}]{text}[/color]"
                tooltip += "To unlock this campaign, "
                shown_rule = campaign_rule
                extra_reqs = layout_has_rule or mission_has_rule
            elif layout_locked:
                text = f"[color={COLOR_PARENT_LOCKED}]{text}[/color]"
                tooltip += "To unlock this questline, "
                shown_rule = layout_rule
                extra_reqs = mission_has_rule
            else:
                text = f"[color={COLOR_MISSION_LOCKED}]{text}[/color]"
                tooltip += "To unlock this mission, "
                shown_rule = mission_rule
            rule_tooltip = shown_rule.tooltip(0, lookup_id_to_mission, COLOR_TOOLTIP_DONE, COLOR_TOOLTIP_NOT_DONE)
            tooltip += rule_tooltip.replace(rule_tooltip[0], rule_tooltip[0].lower(), 1)
            extra_word = "are"
            if shown_rule.shows_single_rule():
                extra_word = "is"
                tooltip += "."
            if extra_reqs:
                tooltip += f"\nThis mission has additional requirements\nthat will be shown once the above {extra_word} met."

        # Mark exit missions
        exit_for: str = ""
        if is_layout_exit:
            exit_for += layout_name if layout_name else "this questline"
        if is_campaign_exit:
            if exit_for:
                exit_for += " and "
            exit_for += campaign_name if campaign_name else "this campaign"
        if exit_for:
            if tooltip:
                tooltip += "\n\n"
            tooltip += f"Required to beat {exit_for}"

        # Mark goal missions
        if mission_id in self.ctx.final_mission_ids:
            if mission_id in available_missions:
                text = f"[color={COLOR_MISSION_FINAL}]{mission_obj.mission_name}[/color]"
            elif campaign_locked or layout_locked:
                text = f"[color={COLOR_FINAL_PARENT_LOCKED}]{mission_obj.mission_name}[/color]"
            else:
                text = f"[color={COLOR_MISSION_FINAL_LOCKED}]{mission_obj.mission_name}[/color]"
            if tooltip and not exit_for:
                tooltip += "\n\n"
            elif exit_for:
                tooltip += "\n"
            if any(location_type == LocationType.VICTORY for (location_type, _, _) in remaining_locations):
                tooltip += f"[color={COLOR_FINAL_MISSION_REMINDER}]Required to beat the world[/color]"
            else:
                tooltip += "This goal mission is already beaten.\nBeat the remaining goal missions to beat the world."

        # Populate remaining location list
        if remaining_count > 0:
            if tooltip:
                tooltip += "\n\n"
            tooltip += f"[b][color={COLOR_MISSION_IMPORTANT}]Uncollected locations[/color][/b]"
            last_location_type = LocationType.VICTORY
            victory_printed = False

            if self.ctx.mission_order_scouting != MissionOrderScouting.option_none:
                mission_available =  mission_id in available_missions

                scoutable = self.is_scoutable(remaining_locations, mission_available, layout_locked, campaign_locked)
            else:
                scoutable = False

            for location_type, location_name, _ in remaining_locations:
                if location_type in (LocationType.VICTORY, LocationType.VICTORY_CACHE) and victory_printed:
                    continue
                if location_type != last_location_type:
                    tooltip += f"\n[color={COLOR_MISSION_IMPORTANT}]{self.get_location_type_title(location_type)}:[/color]"
                    last_location_type = location_type
                if location_type == LocationType.VICTORY:
                    victory_count = len([loc for loc in remaining_locations if loc[0] in (LocationType.VICTORY, LocationType.VICTORY_CACHE)])
                    victory_loc = location_name.replace(":", f":[color={COLOR_VICTORY_LOCATION}]")
                    if victory_count > 1:
                        victory_loc += f' ({victory_count})'
                    tooltip += f"\n- {victory_loc}[/color]"
                    victory_printed = True
                else:
                    tooltip += f"\n- {location_name}"
                if scoutable:
                    tooltip += self.handle_scout_display(location_name)
            if len(plando_locations) > 0:
                tooltip += "\n[b]Plando:[/b]\n- "
                tooltip += "\n- ".join(plando_locations)

        tooltip = f"[b]{text}[/b]\n" + tooltip

        #If the mission has any hints pointing to a check, add asterisks around the mission name
        if any(tuple(x in self.hints_to_highlight for x in self.ctx.locations_for_mission_id(mission_id))):
            text = "* " + text + " *"

        return text, tooltip
        

    def mission_callback(self, button: MissionButton) -> None:
        if button.last_touch.button == 'right':
            self.open_mission_menu(button)
            return
        if not self.launching:
            mission_id: int = button.mission_id
            if self.ctx.play_mission(mission_id):
                self.launching = mission_id
                Clock.schedule_once(self.finish_launching, 10)

    def open_mission_menu(self, button: MissionButton) -> None:
        # Will be assigned later, used to close menu in callbacks
        menu = None
        mission_id = button.mission_id

        def copy_mission_name():
            Clipboard.copy(lookup_id_to_mission[mission_id].mission_name)
            menu.dismiss()

        menu_items = [
            {
                "text": "Copy Mission Name",
                "on_release": copy_mission_name,
            }
        ]
        width_override = None

        hinted_item_ids = Counter()
        hints = self.ctx.stored_data.get(f"_read_hints_{self.ctx.team}_{self.ctx.slot}")
        if hints:
            for hint in hints:
                if hint['receiving_player'] == self.ctx.slot and not hint['found']:
                    hinted_item_ids[hint['item']] += 1

        if not self.ctx.is_mission_completed(mission_id) and not is_mission_available(self.ctx, mission_id):
            # Uncompleted and inaccessible missions can have items hinted if they're needed
            # The inaccessible restriction is to ensure users don't waste hints on missions that they can already access
            items_needed = self.resolve_items_needed(mission_id)
            received_items = compute_received_items(self.ctx)
            for item_id, amount in items_needed.items():
                # If we have already received or hinted enough of this item, skip it
                if received_items[item_id] + hinted_item_ids[item_id] >= amount:
                    continue
                if width_override is None:
                    width_override = dp(500)
                item_name = self.ctx.item_names.lookup_in_game(item_id)
                label_text = f"Hint Required Item: {item_name}"

                def hint_and_close():
                    self.ctx.command_processor(self.ctx)(f"!hint {item_name}")
                    menu.dismiss()

                menu_items.append({
                    "text": label_text,
                    "on_release": hint_and_close,
                })

        menu = MDDropdownMenu(
            caller=button,
            items=menu_items,
            **({"width": width_override} if width_override else {}),
        )
        menu.open()

    def resolve_items_needed(self, mission_id: int) -> Counter[int]:
        def resolve_rule_to_items(rule: RuleData) -> Counter[int]:
            if isinstance(rule, SubRuleRuleData):
                all_items = Counter()
                for sub_rule in rule.sub_rules:
                    # Take max of each item across all sub-rules
                    all_items |= resolve_rule_to_items(sub_rule)
                return all_items
            elif isinstance(rule, ItemRuleData):
                return Counter(rule.item_ids)
            else:
                return Counter()

        rules = self.ctx.mission_id_to_entry_rules[mission_id]
        # Take max value of each item across all rules using '|'
        return (resolve_rule_to_items(rules.mission_rule) |
                resolve_rule_to_items(rules.layout_rule) |
                resolve_rule_to_items(rules.campaign_rule))

    def finish_launching(self, dt):
        self.launching = False
    
    def sort_unfinished_locations(self, mission_id: int) -> Tuple[List[Tuple[LocationType, str, int]], List[str], int]:
        locations: List[Tuple[LocationType, str, int]] = []
        location_name_to_index: Dict[str, int] = {}
        for loc in self.ctx.locations_for_mission_id(mission_id):
            if loc in self.ctx.missing_locations:
                location_name = self.ctx.location_names.lookup_in_game(loc)
                location_name_to_index[location_name] = len(locations)
                locations.append((
                    lookup_location_id_to_type[loc],
                    location_name,
                    loc,
                ))
        count = len(locations)

        plando_locations = []
        elements_to_remove: Set[Tuple[LocationType, str, int]] = set()
        for plando_loc_name in self.ctx.plando_locations:
            if plando_loc_name in location_name_to_index:
                elements_to_remove.add(locations[location_name_to_index[plando_loc_name]])
                plando_locations.append(plando_loc_name)
        for element in elements_to_remove:
            locations.remove(element)

        return sorted(locations), plando_locations, count

    def any_valuable_locations(self, locations: List[Tuple[LocationType, str, int]]) -> bool:
        for location_type, _, location_id in locations:
            if (self.ctx.location_inclusions[location_type] == LocationInclusion.option_enabled
                and all(
                    self.ctx.location_inclusions_by_flag[flag] == LocationInclusion.option_enabled
                    for flag in lookup_location_id_to_flags[location_id].values()
                )
            ):
                return True
        return False

    def get_location_type_title(self, location_type: LocationType) -> str:
        title = location_type.name.title().replace("_", " ")
        if self.ctx.location_inclusions[location_type] == LocationInclusion.option_disabled:
            title += " (Nothing)"
        elif self.ctx.location_inclusions[location_type] == LocationInclusion.option_filler:
            title += " (Filler)"
        else:
            title += ""
        return title
    
    def is_scoutable(self, remaining_locations, mission_available: bool, layout_locked: bool, campaign_locked: bool) -> bool:
        if self.ctx.mission_order_scouting == MissionOrderScouting.option_all:
            return True
        elif self.ctx.mission_order_scouting == MissionOrderScouting.option_campaign and not campaign_locked:
            return True
        elif self.ctx.mission_order_scouting == MissionOrderScouting.option_layout and not layout_locked:
            return True
        elif self.ctx.mission_order_scouting == MissionOrderScouting.option_available and mission_available:
            return True
        elif self.ctx.mission_order_scouting == MissionOrderScouting.option_completed and len([loc for loc in remaining_locations if loc[0] in (LocationType.VICTORY, LocationType.VICTORY_CACHE)]) == 0:
            # Assuming that when a mission is completed, all victory location are removed 
            return True
        else:
            return False

    def handle_scout_display(self, location_name: str) -> str:
        if self.ctx.mission_item_classification is None:
            return ""
        # Only one information is provided for the victory locations of a mission
        if " Cache (" in location_name:
            location_name = location_name.split(" Cache")[0]
        item_classification_key = self.ctx.mission_item_classification[location_name]
        if ((ItemClassification.progression & item_classification_key)
            and (ItemClassification.useful & item_classification_key)
        ):
            # Uncommon, but some games do this to show off that an item is super-important
            # This can also happen on a victory display if the cache holds both progression and useful
            return " [color=AF99EF](Useful+Progression)[/color]"
        if ItemClassification.progression & item_classification_key:
            return " [color=AF99EF](Progression)[/color]"
        if ItemClassification.useful & item_classification_key:
            return " [color=6D8BE8](Useful)[/color]"
        if SC2World.settings.show_traps and ItemClassification.trap & item_classification_key:
            return " [color=FA8072](Trap)[/color]"
        return " [color=00EEEE](Filler)[/color]"


def start_gui(context: SC2Context):
    context.ui = SC2Manager(context)
    context.ui_task = asyncio.create_task(context.ui.async_run(), name="UI")
    import pkgutil
    data = pkgutil.get_data(SC2World.__module__, "starcraft2.kv").decode()
    Builder.load_string(data)
