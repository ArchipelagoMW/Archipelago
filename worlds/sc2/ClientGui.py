from typing import *
import asyncio

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
from kivy.properties import StringProperty

from .Client import SC2Context, calc_unfinished_missions, parse_unlock
from .MissionTables import (lookup_id_to_mission, lookup_name_to_mission, campaign_race_exceptions, SC2Mission, SC2Race,
                            SC2Campaign)
from .Locations import LocationType, lookup_location_id_to_type
from .Options import LocationInclusion
from . import SC2World, get_first_mission


class HoverableButton(HoverBehavior, Button):
    pass


class MissionButton(HoverableButton):
    tooltip_text = StringProperty("Test")

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
    pass

class MultiCampaignLayout(GridLayout):
    pass

class CampaignLayout(GridLayout):
    pass

class MissionLayout(GridLayout):
    pass

class MissionCategory(GridLayout):
    pass


class SC2JSONtoKivyParser(KivyJSONtoTextParser):
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

    campaign_panel: Optional[CampaignLayout] = None
    last_checked_locations: Set[int] = set()
    mission_id_to_button: Dict[int, MissionButton] = {}
    launching: Union[bool, int] = False  # if int -> mission ID
    refresh_from_launching = True
    first_check = True
    first_mission = ""
    ctx: SC2Context

    def __init__(self, ctx) -> None:
        super().__init__(ctx)
        self.json_to_kivy_parser = SC2JSONtoKivyParser(ctx)

    def clear_tooltip(self) -> None:
        if self.ctx.current_tooltip:
            App.get_running_app().root.remove_widget(self.ctx.current_tooltip)

        self.ctx.current_tooltip = None

    def build(self):
        container = super().build()

        panel = self.add_client_tab("Starcraft 2 Launcher", CampaignScroll())
        self.campaign_panel = MultiCampaignLayout()
        panel.content.add_widget(self.campaign_panel)

        Clock.schedule_interval(self.build_mission_table, 0.5)

        return container

    def build_mission_table(self, dt) -> None:
        if (not self.launching and (not self.last_checked_locations == self.ctx.checked_locations or
                                    not self.refresh_from_launching)) or self.first_check:
            assert self.campaign_panel is not None
            self.refresh_from_launching = True

            self.campaign_panel.clear_widgets()
            if self.ctx.mission_req_table:
                self.last_checked_locations = self.ctx.checked_locations.copy()
                self.first_check = False
                self.first_mission = get_first_mission(self.ctx.mission_req_table)

                self.mission_id_to_button = {}

                available_missions, unfinished_missions = calc_unfinished_missions(self.ctx)

                multi_campaign_layout_height = 0

                for campaign, missions in sorted(self.ctx.mission_req_table.items(), key=lambda item: item[0].id):
                    categories: Dict[str, List[str]] = {}

                    # separate missions into categories
                    for mission_index in missions:
                        mission_info = self.ctx.mission_req_table[campaign][mission_index]
                        if mission_info.category not in categories:
                            categories[mission_info.category] = []

                        categories[mission_info.category].append(mission_index)

                    max_mission_count = max(len(categories[category]) for category in categories)
                    if max_mission_count == 1:
                        campaign_layout_height = 115
                    else:
                        campaign_layout_height = (max_mission_count + 2) * 50
                    multi_campaign_layout_height += campaign_layout_height
                    campaign_layout = CampaignLayout(size_hint_y=None, height=campaign_layout_height)
                    if campaign != SC2Campaign.GLOBAL:
                        campaign_layout.add_widget(
                            Label(text=campaign.campaign_name, size_hint_y=None, height=25, outline_width=1)
                        )
                    mission_layout = MissionLayout()

                    for category in categories:
                        category_name_height = 0
                        category_spacing = 3
                        if category.startswith('_'):
                            category_display_name = ''
                        else:
                            category_display_name = category
                            category_name_height += 25
                            category_spacing = 10
                        category_panel = MissionCategory(padding=[category_spacing,6,category_spacing,6])
                        category_panel.add_widget(
                            Label(text=category_display_name, size_hint_y=None, height=category_name_height, outline_width=1))

                        for mission in categories[category]:
                            text: str = mission
                            tooltip: str = ""
                            mission_obj: SC2Mission = lookup_name_to_mission[mission]
                            mission_id: int = mission_obj.id
                            mission_data = self.ctx.mission_req_table[campaign][mission]
                            remaining_locations, plando_locations, remaining_count = self.sort_unfinished_locations(mission)
                            # Map has uncollected locations
                            if mission in unfinished_missions:
                                if self.any_valuable_locations(remaining_locations):
                                    text = f"[color=6495ED]{text}[/color]"
                                else:
                                    text = f"[color=A0BEF4]{text}[/color]"
                            elif mission in available_missions:
                                text = f"[color=FFFFFF]{text}[/color]"
                            # Map requirements not met
                            else:
                                text = f"[color=a9a9a9]{text}[/color]"
                                tooltip = f"Requires: "
                                if mission_data.required_world:
                                    tooltip += ", ".join(list(self.ctx.mission_req_table[parse_unlock(req_mission).campaign])[parse_unlock(req_mission).connect_to - 1] for
                                                            req_mission in
                                                            mission_data.required_world)

                                    if mission_data.number:
                                        tooltip += " and "
                                if mission_data.number:
                                    tooltip += f"{self.ctx.mission_req_table[campaign][mission].number} missions completed"

                            if mission_id == self.ctx.final_mission:
                                if mission in available_missions:
                                    text = f"[color=FFBC95]{mission}[/color]"
                                else:
                                    text = f"[color=D0C0BE]{mission}[/color]"
                                if tooltip:
                                    tooltip += "\n"
                                tooltip += "Final Mission"

                            if remaining_count > 0:
                                if tooltip:
                                    tooltip += "\n\n"
                                tooltip += f"-- Uncollected locations --"
                                for loctype in LocationType:
                                    if len(remaining_locations[loctype]) > 0:
                                        if loctype == LocationType.VICTORY:
                                            tooltip += f"\n- {remaining_locations[loctype][0]}"
                                        else:
                                            tooltip += f"\n{self.get_location_type_title(loctype)}:\n- "
                                            tooltip += "\n- ".join(remaining_locations[loctype])
                                if len(plando_locations) > 0:
                                    tooltip += f"\nPlando:\n- "
                                    tooltip += "\n- ".join(plando_locations)
                            
                            MISSION_BUTTON_HEIGHT = 50
                            for pad in range(mission_data.ui_vertical_padding):
                                column_spacer = Label(text='', size_hint_y=None, height=MISSION_BUTTON_HEIGHT)
                                category_panel.add_widget(column_spacer)
                            mission_button = MissionButton(text=text, size_hint_y=None, height=MISSION_BUTTON_HEIGHT)
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

                        category_panel.add_widget(Label(text=""))
                        mission_layout.add_widget(category_panel)
                    campaign_layout.add_widget(mission_layout)
                    self.campaign_panel.add_widget(campaign_layout)
                self.campaign_panel.height = multi_campaign_layout_height

        elif self.launching:
            assert self.campaign_panel is not None
            self.refresh_from_launching = False

            self.campaign_panel.clear_widgets()
            self.campaign_panel.add_widget(Label(text="Launching Mission: " +
                                                        lookup_id_to_mission[self.launching].mission_name))
            if self.ctx.ui:
                self.ctx.ui.clear_tooltip()

    def mission_callback(self, button: MissionButton) -> None:
        if not self.launching:
            mission_id: int = next(k for k, v in self.mission_id_to_button.items() if v == button)
            if self.ctx.play_mission(mission_id):
                self.launching = mission_id
                Clock.schedule_once(self.finish_launching, 10)

    def finish_launching(self, dt):
        self.launching = False
    
    def sort_unfinished_locations(self, mission_name: str) -> Tuple[Dict[LocationType, List[str]], List[str], int]:
        locations: Dict[LocationType, List[str]] = {loctype: [] for loctype in LocationType}
        count = 0
        for loc in self.ctx.locations_for_mission(mission_name):
            if loc in self.ctx.missing_locations:
                count += 1
                locations[lookup_location_id_to_type[loc]].append(self.ctx.location_names.lookup_in_game(loc))

        plando_locations = []
        for plando_loc in self.ctx.plando_locations:
            for loctype in LocationType:
                if plando_loc in locations[loctype]:
                    locations[loctype].remove(plando_loc)
                    plando_locations.append(plando_loc)

        return locations, plando_locations, count

    def any_valuable_locations(self, locations: Dict[LocationType, List[str]]) -> bool:
        for loctype in LocationType:
            if len(locations[loctype]) > 0 and self.ctx.location_inclusions[loctype] == LocationInclusion.option_enabled:
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

def start_gui(context: SC2Context):
    context.ui = SC2Manager(context)
    context.ui_task = asyncio.create_task(context.ui.async_run(), name="UI")
    import pkgutil
    data = pkgutil.get_data(SC2World.__module__, "Starcraft2.kv").decode()
    Builder.load_string(data)
