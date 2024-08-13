from typing import *
import asyncio
import logging

from BaseClasses import ItemClassification
from NetUtils import JSONMessagePart
from kvui import GameManager, HoverBehavior, ServerToolTip, KivyJSONtoTextParser
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, BooleanProperty

from worlds.sc2.client import SC2Context, calc_unfinished_nodes, force_settings_save_on_close
from worlds.sc2.item_descriptions import item_descriptions
from worlds.sc2.mission_tables import lookup_id_to_mission, campaign_race_exceptions, \
    SC2Mission, SC2Race
from worlds.sc2.locations import LocationType, lookup_location_id_to_type, lookup_location_id_to_flags
from worlds.sc2.options import LocationInclusion
from worlds.sc2 import SC2World


class HoverableButton(HoverBehavior, Button):
    pass


class MissionButton(HoverableButton):
    tooltip_text = StringProperty("Test")
    is_exit = BooleanProperty(False)
    is_goal = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        super(HoverableButton, self).__init__(*args, **kwargs)
        self.layout = FloatLayout()
        self.popuplabel = ServerToolTip(text=self.text, markup=True)
        self.popuplabel.padding = [5, 2, 5, 2]
        self.layout.add_widget(self.popuplabel)

    def on_enter(self):
        self.popuplabel.text = self.tooltip_text

        if self.ctx.current_tooltip:
            App.get_running_app().root.remove_widget(self.ctx.current_tooltip)

        if self.tooltip_text == "":
            self.ctx.current_tooltip = None
        else:
            App.get_running_app().root.add_widget(self.layout)
            self.ctx.current_tooltip = self.layout

    def on_leave(self):
        self.ctx.ui.clear_tooltip()

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
        if item_name not in item_descriptions:
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
    logging_pairs = [
        ("Client", "Archipelago"),
        ("Starcraft2", "Starcraft2"),
    ]
    base_title = "Archipelago Starcraft 2 Client"

    campaign_panel: Optional[MultiCampaignLayout] = None
    campaign_scroll_panel: Optional[CampaignScroll] = None
    last_checked_locations: Set[int] = set()
    last_data_out_of_date = False
    mission_id_to_button: Dict[int, MissionButton] = {}
    launching: Union[bool, int] = False  # if int -> mission ID
    refresh_from_launching = True
    first_check = True
    first_mission = ""
    ctx: SC2Context

    def __init__(self, ctx: SC2Context, startup_warnings: List[str]) -> None:
        super().__init__(ctx)
        self.json_to_kivy_parser = SC2JSONtoKivyParser(ctx)
        self.startup_warnings = startup_warnings
        self.minimized = False
        from kivy.core.window import Window
        Window.bind(on_maximize=self.on_maximize)
        Window.bind(on_minimize=self.on_minimize)
        Window.bind(on_restore=self.on_restore)

    def on_start(self) -> None:
        super().on_start()
        for startup_warning in self.startup_warnings:
            logging.getLogger("Starcraft2").warning(f"Startup WARNING: {startup_warning}")

    def on_maximize(self, window) -> None:
        SC2World.settings.window_maximized = True
        force_settings_save_on_close()

    def on_minimize(self, window) -> None:
        self.minimized = True

    def on_restore(self, window) -> None:
        if self.minimized:
            self.minimized = False
        else:
            # Restoring from maximized
            SC2World.settings.window_maximized = False
            force_settings_save_on_close()
    
    def clear_tooltip(self) -> None:
        if self.ctx.current_tooltip:
            App.get_running_app().root.remove_widget(self.ctx.current_tooltip)

        self.ctx.current_tooltip = None

    def build(self):
        container = super().build()

        panel = TabbedPanelItem(text="Starcraft 2 Launcher")
        panel.content = CampaignScroll()
        self.campaign_scroll_panel = panel.content
        self.campaign_panel = MultiCampaignLayout()
        panel.content.add_widget(self.campaign_panel)

        self.tabs.add_widget(panel)

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
        
        needs_redraw = (
            self.last_checked_locations != self.ctx.checked_locations
            or not self.refresh_from_launching
            or self.last_data_out_of_date != self.ctx.data_out_of_date
            or self.first_check
        )
        if not needs_redraw:
            return

        assert self.campaign_panel is not None
        self.refresh_from_launching = True

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

        # if self.ctx.slot_data_version >= 4 and self.ctx.mission_order:
        self.last_checked_locations = self.ctx.checked_locations.copy()
        self.first_check = False

        self.mission_id_to_button = {}

        available_missions, available_layouts, available_campaigns, unfinished_missions = calc_unfinished_nodes(self.ctx)

        multi_campaign_layout_height = 0

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
                        is_layout_exit = mission_id in layout.exits
                        is_campaign_exit = mission_id in campaign.exits

                        text, tooltip = self.mission_text(
                            self.ctx, mission_id, mission_obj,
                            layout_idx, is_layout_exit, layout.name,
                            campaign_idx, is_campaign_exit, campaign.name,
                            available_missions, available_layouts, available_campaigns, unfinished_missions
                        )

                        mission_button = MissionButton(text=text, size_hint_y=None, height=MISSION_BUTTON_HEIGHT)

                        if mission_id in self.ctx.final_mission_ids:
                            mission_button.is_goal = True
                        if is_layout_exit or is_campaign_exit:
                            mission_button.is_exit = True

                        mission_race = mission_obj.race
                        if mission_race == SC2Race.ANY:
                            mission_race = mission_obj.campaign.race
                        race = campaign_race_exceptions.get(mission_obj, mission_race)
                        racial_colors = {
                            SC2Race.TERRAN: (0.24, 0.84, 0.68),
                            SC2Race.ZERG: (1, 0.65, 0.37),
                            SC2Race.PROTOSS: (0.55, 0.7, 1)
                        }
                        if race in racial_colors:
                            mission_button.background_color = racial_colors[race]
                        mission_button.tooltip_text = tooltip
                        mission_button.bind(on_press=self.mission_callback)
                        self.mission_id_to_button[mission_id] = mission_button
                        category_panel.add_widget(mission_button)

                    # layout_panel.add_widget(Label(text=""))
                    column_panel.add_widget(category_panel)
                layout_panel.add_widget(column_panel)
                mission_layout.add_widget(layout_panel)
            campaign_layout.add_widget(mission_layout)
            self.campaign_panel.add_widget(campaign_layout)
        self.campaign_panel.height = multi_campaign_layout_height

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

        text = mission_obj.mission_name
        tooltip: str = ""
        remaining_locations, plando_locations, remaining_count = self.sort_unfinished_locations(mission_id)
        parent_locked = campaign_id not in available_campaigns or layout_id not in available_layouts[campaign_id]

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
            if parent_locked:
                text = f"[color={COLOR_PARENT_LOCKED}]{text}[/color]"
                if campaign_id not in available_campaigns:
                    tooltip += "To unlock this campaign, "
                    rule_tooltip = campaign_rule.tooltip(0, lookup_id_to_mission)
                else:
                    tooltip += "To unlock this region, "
                    rule_tooltip = layout_rule.tooltip(0, lookup_id_to_mission)
            else:
                text = f"[color={COLOR_MISSION_LOCKED}]{text}[/color]"
                tooltip += "To unlock this mission, "
                rule_tooltip = mission_rule.tooltip(0, lookup_id_to_mission)
            tooltip += rule_tooltip.replace(rule_tooltip[0], rule_tooltip[0].lower(), 1)

        # Mark exit missions
        exit_for: str = ""
        if is_layout_exit:
            exit_for += layout_name if layout_name else "this region"
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
            elif parent_locked:
                text = f"[color={COLOR_FINAL_PARENT_LOCKED}]{mission_obj.mission_name}[/color]"
            else:
                text = f"[color={COLOR_MISSION_FINAL_LOCKED}]{mission_obj.mission_name}[/color]"
            if tooltip and not exit_for:
                tooltip += "\n\n"
            elif exit_for:
                tooltip += "\n"
            tooltip += f"[color={COLOR_FINAL_MISSION_REMINDER}]Required to beat the world[/color]"

        # Populate remaining location list
        if remaining_count > 0:
            if tooltip:
                tooltip += "\n\n"
            tooltip += f"[b][color={COLOR_MISSION_IMPORTANT}]Uncollected locations[/color][/b]"
            last_location_type = LocationType.VICTORY
            for location_type, location_name, _ in remaining_locations:
                if location_type != last_location_type:
                    tooltip += f"\n[color={COLOR_MISSION_IMPORTANT}]{self.get_location_type_title(location_type)}:[/color]"
                    last_location_type = location_type
                if location_type == LocationType.VICTORY:
                    victory_loc = location_name.replace(":", f":[color={COLOR_VICTORY_LOCATION}]")
                    tooltip += f"\n- {victory_loc}[/color]"
                else:
                    tooltip += f"\n- {location_name}"
            if len(plando_locations) > 0:
                tooltip += f"\n[b]Plando:[/b]\n- "
                tooltip += "\n- ".join(plando_locations)

        tooltip = f"[b]{text}[/b]\n" + tooltip
        return text, tooltip
        

    def mission_callback(self, button: MissionButton) -> None:
        if not self.launching:
            mission_id: int = next(k for k, v in self.mission_id_to_button.items() if v == button)
            if self.ctx.play_mission(mission_id):
                self.launching = mission_id
                Clock.schedule_once(self.finish_launching, 10)

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
        elif self.ctx.location_inclusions[location_type] == LocationInclusion.option_resources:
            title += " (Resources)"
        else:
            title += ""
        return title

def start_gui(context: SC2Context, startup_warnings: List[str]):
    context.ui = SC2Manager(context, startup_warnings)
    context.ui_task = asyncio.create_task(context.ui.async_run(), name="UI")
    import pkgutil
    data = pkgutil.get_data(SC2World.__module__, "starcraft2.kv").decode()
    Builder.load_string(data)
