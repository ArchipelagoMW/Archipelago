from __future__ import annotations
import asyncio
import os
import re
import sys
import time
import typing
from typing import Any, Optional

import requests
from worlds import AutoWorldRegister, network_data_package
from worlds.LauncherComponents import icon_paths
import json
import traceback


import ModuleUpdate
ModuleUpdate.update()

import Utils

from NetUtils import ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, server_loop
from MultiServer import mark_raw

tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext, TrackerCommandProcessor
    ClientCommandProcessor = TrackerCommandProcessor
    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import CommonContext as SuperContext

if typing.TYPE_CHECKING:
    import kvui

class ManualClientCommandProcessor(ClientCommandProcessor):
    def _cmd_resync(self) -> bool:
        """Manually trigger a resync."""
        self.output("Syncing items.")
        self.ctx.syncing = True
        return True

    @mark_raw
    def _cmd_send(self, location_name: str) -> bool:
        """Send a check"""
        names = self.ctx.location_names_to_id.keys()
        location_name, usable, response = Utils.get_intended_text(
            location_name,
            names
        )
        if usable:
            location_id = self.ctx.location_names_to_id[location_name]
            self.ctx.locations_checked.append(location_id)
            self.ctx.syncing = True
        else:
            self.output(response)
            return False





class ManualContext(SuperContext):
    command_processor = ManualClientCommandProcessor
    game = None  # this is changed in server_auth below based on user input
    items_handling = 0b111  # full remote
    tags = {"AP"}

    location_table = {}
    item_table = {}
    region_table = {}
    category_table = {}

    tracker_reachable_locations = []
    tracker_reachable_events = []

    set_deathlink = False
    last_death_link = 0
    deathlink_out = False

    search_term = ""

    colors = {
        'location_default': [219/255, 218/255, 213/255, 1],
        'location_in_logic': [2/255, 242/255, 42/255, 1],
        'category_even_default': [0.5, 0.5, 0.5, 0.1],
        'category_odd_default': [1.0, 1.0, 1.0, 0.0],
        'category_in_logic': [2/255, 82/255, 2/255, 1],
        'deathlink_received': [1, 0, 0, 1],
        'deathlink_primed': [1, 1, 1, 1],
        'deathlink_sent': [0, 1, 0, 1],
        'game_select_button': [200/255, 200/255, 200/255, 1],
        'header_background': [15/255, 80/255, 112/255, 1]
    }

    def __init__(self, server_address, password, game, player_name) -> None:
        super(ManualContext, self).__init__(server_address, password)

        if tracker_loaded:
            super().set_callback(self.on_tracker_updated) # Universal Tracker takes this func and calls it when updateTracker is called
            if hasattr(self, "set_events_callback"):
                super().set_events_callback(self.on_tracker_events) # Universal Tracker takes this func and calls it when events are calculated

        self.send_index: int = 0
        self.syncing = False
        self.game = game
        self.username = player_name

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(ManualContext, self).server_auth(password_requested)

        if "Manual_" not in self.ui.game_bar_text.text:
            raise Exception("The Manual client can only be used for Manual games.")

        self.game = self.ui.game_bar_text.text

        world = AutoWorldRegister.world_types.get(self.game)
        if not self.location_table and not self.item_table and world is None:
            raise Exception(f"Cannot load {self.game}, please add the apworld to lib/worlds/")

        data_package = network_data_package["games"].get(self.game, {})

        self.update_ids(data_package)

        if world is not None and hasattr(world, "victory_names"):
            self.victory_names = world.victory_names
            self.goal_location = self.get_location_by_name(world.victory_names[0])
        else:
            self.victory_names = ["__Manual Game Complete__"]
            self.goal_location = self.get_location_by_name("__Manual Game Complete__")

        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(ManualContext, self).connection_closed()

    @property
    def suggested_game(self) -> str:
        if self.game:
            return self.game
        from .Game import game_name  # This will at least give us the name of a manual they've installed
        return Utils.persistent_load().get("client", {}).get("last_manual_game", game_name)

    def get_location_by_name(self, name) -> dict[str, Any]:
        location = self.location_table.get(name)
        if not location:
            # It is absolutely possible to pull categories from the data_package via self.update_game. I have not done this yet.
            location = AutoWorldRegister.world_types[self.game].location_name_to_location.get(name, {"name": name})
        return location

    def get_location_by_id(self, id) -> dict[str, Any]:
        name = self.location_names.lookup_in_game(id)
        return self.get_location_by_name(name)

    def get_item_by_name(self, name):
        item = self.item_table.get(name)
        if not item:
            item = AutoWorldRegister.world_types[self.game].item_name_to_item.get(name, {"name": name})
        return item

    def get_item_by_id(self, id):
        name = self.item_names.lookup_in_game(id)
        return self.get_item_by_name(name)

    def update_ids(self, data_package) -> None:
        self.location_names_to_id = data_package['location_name_to_id']
        self.item_names_to_id = data_package['item_name_to_id']

    def update_data_package(self, data_package: dict):
        super().update_data_package(data_package)
        for game, game_data in data_package["games"].items():
            if game == self.game:
                self.update_ids(game_data)

    def set_search(self, search_term: str):
        self.search_term = search_term

    def clear_search(self):
        self.search_term = ""

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super(ManualContext, self).shutdown()

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)

        if cmd in {"Connected", "DataPackage"}:
            if cmd == "Connected":
                Utils.persistent_store("client", "last_manual_game", self.game)
                if args.get("slot_data"):
                    goal = args["slot_data"].get("goal")
                    if goal and goal < len(self.victory_names):
                        self.goal_location = self.get_location_by_name(self.victory_names[goal])
                    if args['slot_data'].get('death_link'):
                        self.ui.enable_death_link()
                        self.set_deathlink = True
                        self.last_death_link = 0
                    logger.info(f"Slot data: {args['slot_data']}")

            self.ui.build_tracker_and_locations_table()
            self.ui.request_update_tracker_and_locations_table(update_highlights=True)
        elif cmd in {"ReceivedItems"}:
            self.ui.request_update_tracker_and_locations_table(update_highlights=True)
        elif cmd in {"RoomUpdate"}:
            self.ui.request_update_tracker_and_locations_table(update_highlights=False)

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        super().on_deathlink(data)
        self.ui.death_link_button.text = f"Death Link: {data['source']}"
        self.ui.death_link_button.background_color = self.colors['deathlink_received']

    def on_tracker_updated(self, reachable_locations: list[str]):
        self.tracker_reachable_locations = reachable_locations
        self.ui.request_update_tracker_and_locations_table(update_highlights=True)

    def on_tracker_events(self, events: list[str]):
        self.tracker_reachable_events = events
        if events:
            self.ui.request_update_tracker_and_locations_table(update_highlights=True)

    def handle_connection_loss(self, msg: str) -> None:
        """Helper for logging and displaying a loss of connection. Must be called from an except block."""
        exc_info = sys.exc_info()
        logger.exception(msg, exc_info=exc_info, extra={'compact_gui': True})
        tracker_error = False
        e = exc_info[2]
        formatted_tb = ''.join(traceback.format_tb(e))
        while e:
            if '/tracker/' in e.tb_frame.f_code.co_filename:
                tracker_error = True
                break
            e = e.tb_next

        if tracker_error:
            self._messagebox_connection_loss = self.gui_error(
                "A Universal Tracker error has occurred. Please ensure that your version of UT matches your version of Archipelago.",
                formatted_tb)
        else:
            self._messagebox_connection_loss = self.gui_error(msg, formatted_tb)

    def run_gui(self):
        """Import kivy UI system from make_gui() and start running it as self.ui_task."""
        if hasattr(SuperContext, "make_gui"):
            # Call the real one if it exists
            return super().run_gui()

        # This is a copy of 0.5.1's run_gui, because backporting is easier than the alternative.
        # This entire function can be removed once 0.5.1 is the old enough.
        ui_class = self.make_gui()
        self.ui = ui_class(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def make_gui(self) -> typing.Type["kvui.GameManager"]:
        if hasattr(SuperContext, "make_gui"):
            ui = super().make_gui()  # before the kivy imports so kvui gets loaded first
        else:
            from kvui import GameManager
            ui = GameManager

        from kivy.metrics import dp
        from kivy.uix.button import Button
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.dropdown import DropDown
        from kivy.uix.gridlayout import GridLayout
        from kivy.uix.label import Label
        from kivy.uix.layout import Layout
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.spinner import Spinner, SpinnerOption
        from kivy.uix.textinput import TextInput
        from kivy.uix.treeview import TreeView, TreeViewNode, TreeViewLabel
        from kivy.core.window import Window
        from kivy.lang import Builder
        from kivy.properties import ColorProperty

        class ManualTabLayout(BoxLayout):
            pass

        class ManualControlsLayout(BoxLayout):
            pass

        class TrackerAndLocationsLayout(GridLayout):
            pass

        class TrackerLayoutScrollable(ScrollView):
            pass

        class LocationsLayoutScrollable(ScrollView):
            pass

        class TreeViewButton(Button, TreeViewNode):
            victory: bool = False
            id: int = None

        class TreeViewScrollView(ScrollView, TreeViewNode):
            pass

        class GameSelectOption(SpinnerOption):
            background_color = self.colors['game_select_button']

        class GameSelectDropDown(DropDown):
            # If someone can figure out how to give this a solid background, I'd be very happy.
            pass

        Builder.load_string(
        """

<ManualControlsStyledLayout>:
    canvas:
        Color:
            rgba: root.background_color
        Rectangle:
            pos: self.pos
            size: self.size

        """)

        class ManualControlsStyledLayout(BoxLayout):
            background_color = ColorProperty()

        class ManualManager(ui):
            base_title = "Archipelago Manual Client"
            listed_items = {"(No Category)": []}
            item_categories = ["(No Category)"]
            listed_locations = {"(No Category)": []}
            location_categories = ["(No Category)"]

            active_item_accordion = 0
            active_location_accordion = 0

            update_requested_time: Optional[float] = None
            update_requested_highlights: bool = False

            ctx: ManualContext

            def __init__(self, ctx):
                super().__init__(ctx)

            def build(self) -> Layout:
                super().build()

                self.manual_game_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(30))

                game_bar_label = Label(text="Manual Game ID", size=(dp(150), dp(30)), size_hint_y=None, size_hint_x=None)
                manuals = [w for w in AutoWorldRegister.world_types.keys() if "Manual_" in w]
                manuals.sort()  # Sort by alphabetical order, not load order
                self.manual_game_layout.add_widget(game_bar_label)
                self.game_bar_text = Spinner(text=self.ctx.suggested_game, size_hint_y=None, height=dp(30), sync_height=True,
                                             values=manuals, option_cls=GameSelectOption, dropdown_cls=GameSelectDropDown)
                self.manual_game_layout.add_widget(self.game_bar_text)

                self.grid.add_widget(self.manual_game_layout, 3)

                panel = self.add_client_tab("Manual", ManualTabLayout(orientation="vertical"))

                self.controls_panel = ManualControlsLayout(orientation="horizontal", size_hint_y=None, height=dp(40))
                self.tracker_and_locations_panel = TrackerAndLocationsLayout(cols = 2)

                panel.content.add_widget(self.controls_panel)
                panel.content.add_widget(self.tracker_and_locations_panel)

                self.build_tracker_and_locations_table()

                return self.container

            def clear_lists(self):
                self.listed_items = {"(No Category)": []}
                self.item_categories = ["(No Category)"]
                self.listed_locations = {"(No Category)": [], "(Hinted)": []}
                self.location_categories = ["(No Category)", "(Hinted)"]

            def set_active_item_accordion(self, instance):
                index = 0

                for widget in self.children:
                    if widget == instance:
                        self.active_item_accordion = index
                        return

                    index += 1

            def set_active_location_accordion(self, instance):
                index = 0

                for widget in self.children:
                    if widget == instance:
                        self.active_item_accordion = index
                        return

                    index += 1

            def enable_death_link(self):
                if not hasattr(self, "death_link_button"):
                    self.death_link_button = Button(text="Death Link: Primed",
                                                size_hint_x=None, width=150)
                    self.connect_layout.add_widget(self.death_link_button)
                    self.death_link_button.bind(on_release=self.send_death_link)

            def send_death_link(self, *args):
                if self.ctx.last_death_link:
                    self.ctx.last_death_link = 0
                    self.death_link_button.text = "Death Link: Primed"
                    self.death_link_button.background_color = self.ctx.colors['deathlink_primed']
                else:
                    self.ctx.deathlink_out = True
                    self.death_link_button.text = "Death Link: Sent"
                    self.death_link_button.background_color = self.ctx.colors['deathlink_sent']

            def update_hints(self):
                super().update_hints()
                rebuild = False
                for hint in self.ctx.stored_data.get(f"_read_hints_{self.ctx.team}_{self.ctx.slot}", []):
                    if hint["finding_player"] == self.ctx.slot:
                        if hint["location"] in self.ctx.missing_locations:
                            location = self.ctx.get_location_by_id(hint["location"])
                            location["category"] = location.get("category", [])
                            if "(Hinted)" not in location["category"]:
                                location["category"].append("(Hinted)")
                                rebuild = True

                if rebuild:
                    self.build_tracker_and_locations_table()
                self.request_update_tracker_and_locations_table()

            def update_search_from_input(self, instance, text: str):
                self.ctx.set_search(text)
                self.request_update_tracker_and_locations_table() # if we want search to be "snappier", we can just make this update

            def clear_search_input(self):
                self.search_textbox.text = ""
                self.ctx.clear_search()
                self.request_update_tracker_and_locations_table() # if we want search to be "snappier", we can just make this update

            def build_tracker_and_locations_table(self):
                self.controls_panel.clear_widgets()
                self.tracker_and_locations_panel.clear_widgets()

                if not self.ctx.server or not self.ctx.auth:
                    self.tracker_and_locations_panel.add_widget(
                                Label(text="Waiting for connection...", size_hint_y=None, height=50, outline_width=1))
                    return

                self.clear_lists()

                # build tab-specific controls above the two tracker columns
                controls_styled_layout = ManualControlsStyledLayout(orientation="horizontal", size_hint_y=None, height=dp(40), padding=dp(5), background_color=self.ctx.colors["header_background"])
                search_layout = BoxLayout(orientation="horizontal", size_hint=(None, None), width=dp(320), height=dp(30), spacing=dp(2))
                search_label = Label(text="Search:", size_hint=(None, None), width=dp(55), height=dp(30), bold=True)
                self.search_textbox = TextInput(size_hint=(None, None), width=dp(200), height=dp(30), multiline=False, write_tab=False)
                self.search_textbox.bind(text = self.update_search_from_input)
                search_button = Button(size_hint=(None, None), width=dp(50), height=dp(30), text="Clear")
                search_button.bind(on_release=lambda *args: self.clear_search_input())

                controls_styled_layout.add_widget(search_layout)
                search_layout.add_widget(search_label)
                search_layout.add_widget(self.search_textbox)
                search_layout.add_widget(search_button)
                self.controls_panel.add_widget(controls_styled_layout)

                # seed all category names to start
                for item in self.ctx.item_table.values() or AutoWorldRegister.world_types[self.ctx.game].item_name_to_item.values():
                    if "category" in item and len(item["category"]) > 0:
                        for category in item["category"]:
                            category_settings = self.ctx.category_table.get(category) or getattr(AutoWorldRegister.world_types[self.ctx.game], "category_table", {}).get(category, {})
                            if "hidden" in category_settings and category_settings["hidden"]:
                                continue
                            if category not in self.item_categories:
                                self.item_categories.append(category)

                            if category not in self.listed_items:
                                self.listed_items[category] = []


                # Items are not received on connect, so don't bother attempting to work with received items here

                if not self.ctx.location_table and not hasattr(AutoWorldRegister.world_types[self.ctx.game], 'location_name_to_location'):
                    raise Exception("The apworld for %s is too outdated for this client. Please update it." % (self.ctx.game))

                for location_id in self.ctx.missing_locations:
                    # holy nesting, wow
                    location_name = self.ctx.location_names.lookup_in_game(location_id)
                    location = self.ctx.get_location_by_name(location_name)

                    if not location:
                        continue

                    if "category" in location and len(location["category"]) > 0:
                        for category in location["category"]:
                            category_settings = self.ctx.category_table.get(category) or getattr(AutoWorldRegister.world_types[self.ctx.game], "category_table", {}).get(category, {})
                            if "hidden" in category_settings and category_settings["hidden"]:
                                continue
                            if category not in self.location_categories:
                                self.location_categories.append(category)

                            if category not in self.listed_locations:
                                self.listed_locations[category] = []

                            self.listed_locations[category].append(location_id)
                    else: # leave it in the generic category
                        self.listed_locations["(No Category)"].append(location_id)

                victory_location =  self.ctx.goal_location
                victory_categories = set(victory_location.get("category", []))

                for category in victory_categories:
                    if category not in self.location_categories:
                        self.location_categories.append(category)

                    if category not in self.listed_locations:
                        self.listed_locations[category] = []

                if not victory_categories:
                    victory_categories.add("(No Category)")

                for category in self.listed_locations:
                    self.listed_locations[category].sort()

                items_length = len(self.ctx.items_received)
                tracker_panel_scrollable = TrackerLayoutScrollable(do_scroll=(False, True), bar_width=10)
                tracker_panel = TreeView(root_options=dict(text="Items Received (%d)" % (items_length)), size_hint_y=None)
                tracker_panel.bind(minimum_height=tracker_panel.setter('height'))

                # Since items_received is not available on connect, don't bother building item labels here
                for item_category in sorted(self.listed_items.keys()):
                    category_tree = tracker_panel.add_node(
                        TreeViewLabel(text = "%s (%s)" % (item_category, len(self.listed_items[item_category])))
                    )

                    category_scroll = tracker_panel.add_node(TreeViewScrollView(size_hint=(1, None), size=(Window.width / 2, 250)), category_tree)
                    category_layout = GridLayout(cols=1, size_hint_y=None)
                    category_layout.bind(minimum_height = category_layout.setter('height'))
                    category_scroll.add_widget(category_layout)

                locations_length = len(self.ctx.missing_locations)
                locations_panel_scrollable = LocationsLayoutScrollable(do_scroll=(False, True), bar_width=10)
                locations_panel = TreeView(root_options=dict(text="Remaining Locations (%d)" % (locations_length + 1)), size_hint_y=None)
                locations_panel.bind(minimum_height=locations_panel.setter('height'))

                # This seems like a redundant copy of the same check above?
                if not self.ctx.location_table and not hasattr(AutoWorldRegister.world_types[self.ctx.game], 'location_name_to_location'):
                    raise Exception("The apworld for %s is too outdated for this client. Please update it." % (self.ctx.game))

                for location_category in sorted(self.listed_locations.keys()):
                    locations_in_category = len(self.listed_locations[location_category])

                    if (location_category in victory_categories) or \
                        (not victory_categories and location_category == "(No Category)"):
                        locations_in_category += 1

                    category_tree = locations_panel.add_node(
                        TreeViewLabel(text = "%s (%s)" % (location_category, locations_in_category))
                    )

                    category_scroll = locations_panel.add_node(TreeViewScrollView(size_hint=(1, None), size=(Window.width / 2, 250)), category_tree)
                    category_layout = GridLayout(cols=1, size_hint_y=None)
                    category_layout.bind(minimum_height = category_layout.setter('height'))
                    category_scroll.add_widget(category_layout)

                    for location_id in self.listed_locations[location_category]:
                        location_button = TreeViewButton(text=self.ctx.location_names.lookup_in_game(location_id), size_hint=(None, None), height=30, width=400)
                        location_button.bind(on_release=lambda *args, loc_id=location_id: self.location_button_callback(loc_id, *args))
                        location_button.id = location_id
                        category_layout.add_widget(location_button)

                    # if this is the category that Victory is in, display the Victory button
                    # if ("category" in victory_location_data and location_category in victory_location_data["category"]) or \
                    #     ("category" not in victory_location_data and location_category == "(No Category)"):
                    if location_category in victory_categories:
                        # Add the Victory location to be marked at any point, which is why locations length has 1 added to it above
                        victory_text = "VICTORY! (seed finished)" if victory_location["name"] == "__Manual Game Complete__" else "GOAL: " + victory_location["name"]
                        location_button = TreeViewButton(text=victory_text, size_hint=(None, None), height=dp(30), width=dp(400))
                        location_button.victory = True
                        location_button.bind(on_release=self.victory_button_callback)
                        category_layout.add_widget(location_button)

                tracker_panel_scrollable.add_widget(tracker_panel)
                locations_panel_scrollable.add_widget(locations_panel)
                self.tracker_and_locations_panel.add_widget(tracker_panel_scrollable)
                self.tracker_and_locations_panel.add_widget(locations_panel_scrollable)

            def check_for_requested_update(self):
                current_time = time.time()

                # wait 0.25 seconds before executing update, in case there are multiple update requests coming in
                if self.update_requested_time and current_time - self.update_requested_time >= 0.25:
                    self.update_requested_time = None
                    self.update_tracker_and_locations_table(self.update_requested_highlights)
                    self.update_requested_highlights = False

            def request_update_tracker_and_locations_table(self, update_highlights=False):
                self.update_requested_time = time.time()
                self.update_requested_highlights = update_highlights or self.update_requested_highlights # if any of the requests wanted highlights, do highlight

            def update_tracker_and_locations_table(self, update_highlights=False):
                items_length = len(self.ctx.items_received)
                locations_length = len(self.ctx.missing_locations)

                if self.ctx.search_term:
                    items_length = len([
                        i for i in self.ctx.items_received
                            if self.ctx.search_term.lower() in self.ctx.item_names.lookup_in_game(i.item).lower()
                    ])

                    locations_length = len([
                        l for l in self.ctx.missing_locations
                            if self.ctx.search_term.lower() in self.ctx.location_names.lookup_in_game(l).lower()
                    ])

                for _, child in enumerate(self.tracker_and_locations_panel.children):
                    #
                    # Structure of items:
                    # TrackerLayoutScrollable -> TreeView -> TreeViewLabel, TreeViewScrollView -> GridLayout -> Label
                    #        item tracker     -> category -> category label, category scroll   -> label col  -> item
                    #
                    if type(child) is TrackerLayoutScrollable:
                        treeview = child.children[0] # TreeView
                        treeview_nodes = treeview.iterate_all_nodes()

                        items_received_label = next(treeview_nodes) # always the first node
                        items_received_label.text = "Items Received (%s)" % (items_length)

                        # loop for each category in listed items and get the label + scrollview
                        for x in range(0, len(self.item_categories)):
                            category_label = next(treeview_nodes) # TreeViewLabel for category
                            category_scrollview = next(treeview_nodes) # TreeViewScrollView for housing category's grid layout

                            old_category_text = category_label.text

                            if type(category_label) is TreeViewLabel and type(category_scrollview) is TreeViewScrollView:
                                category_grid = category_scrollview.children[0] # GridLayout

                                category_name = re.sub(r"\s\(\d+\)$", "", category_label.text)
                                category_count = 0
                                category_unique_name_count = 0

                                existing_item_labels = []
                                bold_item_labels = []

                                # for items that were already listed, determine if the qty changed. if it did, add them to the list to be bolded
                                for item in category_grid.children:
                                    if type(item) is Label:
                                        # Get the item name from the item Label, minus quantity, then do a lookup for count
                                        old_item_text = item.text
                                        item_name = re.sub(r"\s\(\d+\)$", "", item.text)
                                        item_id = self.ctx.item_names_to_id[item_name]
                                        item_count = len(list(i for i in self.ctx.items_received if i.item == item_id))

                                        # if the player is searching for text and the item name doesn't contain it, skip it
                                        if self.ctx.search_term and not self.ctx.search_term.lower() in item_name.lower():
                                            item.width = 0
                                            item.height = 0
                                            item.opacity = 0
                                        else:
                                            item.width = dp(400)
                                            item.height = dp(30)
                                            item.opacity = 1

                                            if item_count > 0:
                                                category_count += item_count
                                                category_unique_name_count += 1

                                        # Update the label quantity
                                        item.text="%s (%s)" % (item_name, item_count)

                                        if update_highlights and (old_item_text != item.text):
                                            bold_item_labels.append(item_name)

                                        existing_item_labels.append(item_name)

                                # instead of reusing existing item listings, clear it all out and re-draw with the sorted list
                                category_grid.clear_widgets()
                                self.listed_items[category_name].clear()
                                category_count = 0
                                category_unique_name_count = 0

                                # Label (for all item listings)
                                sorted_items_received = sorted([
                                    i.item for i in self.ctx.items_received
                                ])

                                for network_item in sorted_items_received:
                                    item_name = self.ctx.item_names.lookup_in_game(network_item)
                                    item_data = self.ctx.get_item_by_name(item_name)

                                    # if the player is searching for text and the item name doesn't contain it, skip it
                                    if self.ctx.search_term and not self.ctx.search_term.lower() in item_name.lower():
                                        continue

                                    if "category" not in item_data or not item_data["category"]:
                                        item_data["category"] = ["(No Category)"]

                                    if category_name in item_data["category"] and network_item not in self.listed_items[category_name]:
                                        item_count = len(list(i for i in self.ctx.items_received if i.item == network_item))
                                        item_text = Label(text="%s (%s)" % (item_name, item_count),
                                                    size_hint=(None, None), height=dp(30), width=dp(400), bold=True)

                                        # if the item was previously listed and was bold, or if it wasn't previously listed at all, make it bold
                                        item_text.bold = (update_highlights and (item_name in bold_item_labels or item_name not in existing_item_labels))

                                        category_grid.add_widget(item_text)
                                        self.listed_items[category_name].append(network_item)

                                        category_count += item_count
                                        category_unique_name_count += 1

                            scrollview_height = 30 * category_unique_name_count

                            if scrollview_height > 250:
                                scrollview_height = 250

                            if scrollview_height < 10:
                                scrollview_height = 50

                            category_name = re.sub(r"\s\(\d+\)$", "", category_label.text)
                            category_label.text = "%s (%s)" % (category_name, category_count)

                            if update_highlights:
                                category_label.bold = True if old_category_text != category_label.text else False

                            category_scrollview.size=(Window.width / 2, scrollview_height)

                    #
                    # Structure of locations:
                    # LocationsLayoutScrollable -> TreeView -> TreeViewLabel, TreeViewScrollView -> GridLayout -> Button
                    #      location tracker     -> category -> category label, category scroll   -> label col  -> location
                    #
                    if type(child) is LocationsLayoutScrollable:
                        treeview = child.children[0] # TreeView
                        treeview_nodes = treeview.iterate_all_nodes()

                        locations_remaining_label = next(treeview_nodes) # always the first node
                        locations_remaining_label.text = "Remaining Locations (%d)" % (locations_length)

                        # loop for each category in listed items and get the label + scrollview
                        for x in range(0, len(self.location_categories)):
                            category_label = next(treeview_nodes) # TreeViewLabel for category
                            category_scrollview = next(treeview_nodes) # TreeViewScrollView for housing category's grid layout

                            if type(category_label) is TreeViewLabel and type(category_scrollview) is TreeViewScrollView:
                                category_grid = category_scrollview.children[0] # GridLayout

                                category_name = re.sub(r"\s\(\d+\/?(\d+)?\)$", "", category_label.text)
                                category_count = 0
                                reachable_count = 0

                                buttons_to_remove = []

                                # since victory is handled more briefly below, need to pull show/hide into functions here to reuse
                                def show_button_during_search(btn: TreeViewButton):
                                    btn.width = dp(400)
                                    btn.height = dp(30)
                                    btn.opacity = 1
                                    btn.disabled = False

                                def hide_button_during_search(btn: TreeViewButton):
                                    btn.width = 0
                                    btn.height = 0
                                    btn.opacity = 0
                                    btn.disabled = True

                                # Label (for existing item listings)
                                for location_button in category_grid.children:
                                    if type(location_button) is TreeViewButton:
                                        # should only be true for the victory location button, which has different text
                                        if location_button.text not in (self.ctx.location_table or AutoWorldRegister.world_types[self.ctx.game].location_name_to_location):
                                            # if the player is searching for text and the location name doesn't contain it, hide and disable it
                                            if self.ctx.search_term and not self.ctx.search_term.lower() in location_button.text.lower():
                                                hide_button_during_search(location_button)
                                            else:
                                                show_button_during_search(location_button)
                                                category_count += 1

                                                if location_button.victory and "__Victory__" in self.ctx.tracker_reachable_events:
                                                    location_button.background_color = self.ctx.colors['location_in_logic']
                                                    reachable_count += 1

                                                continue

                                        if location_button.id and location_button.id not in self.ctx.missing_locations:
                                            import logging

                                            logging.info("location button being removed: " + location_button.text)
                                            buttons_to_remove.append(location_button)
                                            continue

                                        was_reachable = False

                                        if location_button.text in self.ctx.tracker_reachable_locations:
                                            location_button.background_color = self.ctx.colors['location_in_logic']
                                            was_reachable = True
                                        else:
                                            location_button.background_color = self.ctx.colors['location_default']

                                        # if the player is searching for text and the location name doesn't contain it, hide and disable it
                                        if self.ctx.search_term and not self.ctx.search_term.lower() in location_button.text.lower():
                                            hide_button_during_search(location_button)
                                        else:
                                            show_button_during_search(location_button)

                                            if was_reachable:
                                                reachable_count += 1

                                            category_count += 1

                                for location_button in buttons_to_remove:
                                    location_button.parent.remove_widget(location_button)

                                scrollview_height = 30 * category_count

                                if scrollview_height > 250:
                                    scrollview_height = 250

                                if scrollview_height < 10:
                                    scrollview_height = 50

                                count_text = category_count

                                if tracker_loaded:
                                    count_text = "{}/{}".format(reachable_count, category_count)

                                category_name = re.sub(r"\s\(\d+\/?(\d+)?\)$", "", category_label.text)
                                category_label.text = "%s (%s)" % (category_name, count_text)

                                if reachable_count > 0:
                                    # treeviewlabels don't have background color. because #justkivythings.
                                    category_label.even_color = self.ctx.colors['category_in_logic']
                                    category_label.odd_color = self.ctx.colors['category_in_logic']
                                else:
                                    category_label.even_color = self.ctx.colors['category_even_default']
                                    category_label.odd_color = self.ctx.colors['category_odd_default']

                                category_scrollview.size=(Window.width / 2, scrollview_height)

            def location_button_callback(self, location_id, button):
                if button.text not in self.ctx.location_names_to_id:
                    raise Exception("Locations were not loaded correctly. Please reconnect your client.")

                if location_id:
                    self.ctx.locations_checked.append(location_id)
                    self.ctx.syncing = True
                    button.parent.remove_widget(button)

                    # message = [{"cmd": 'LocationChecks', "locations": [location_id]}]
                    # self.ctx.send_msgs(message)

            def victory_button_callback(self, button):
                self.ctx.items_received.append("__Victory__")
                self.ctx.syncing = True

        return ManualManager

async def game_watcher_manual(ctx: ManualContext):
    while not ctx.exit_event.is_set():
        if ctx.ui:
            ctx.ui.check_for_requested_update()

        if ctx.syncing == True:
            sync_msg = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False

        if ctx.set_deathlink:
            ctx.set_deathlink = False
            await ctx.update_death_link(True)

        if ctx.deathlink_out:
            ctx.deathlink_out = False
            await ctx.send_death()

        sending = []
        victory = ("__Victory__" in ctx.items_received)
        ctx.locations_checked = sending
        message = [{"cmd": 'LocationChecks', "locations": sending}]
        await ctx.send_msgs(message)
        if not ctx.finished_game and victory:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        await asyncio.sleep(0.1)


def read_apmanual_file(apmanual_file):
    from base64 import b64decode

    with open(apmanual_file, 'r') as f:
        return json.loads(b64decode(f.read()))


async def main(args):
    config_file = {}
    if args.apmanual_file:
        config_file = read_apmanual_file(args.apmanual_file)
    ctx = ManualContext(args.connect, args.password, config_file.get("game"), config_file.get("player_name"))
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    ctx.item_table = config_file.get("items", {})
    ctx.location_table = config_file.get("locations", {})
    ctx.region_table = config_file.get("regions", {})
    ctx.category_table = config_file.get("categories", {})

    if tracker_loaded:
        ctx.run_generator()
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()
    progression_watcher = asyncio.create_task(
        game_watcher_manual(ctx), name="ManualProgressionWatcher")

    await ctx.exit_event.wait()
    ctx.server_address = None

    await progression_watcher

    await ctx.shutdown()

def launch() -> None:
    import colorama

    parser = get_base_parser(description="Manual Client, for operating a Manual game in Archipelago.")
    parser.add_argument('apmanual_file', default="", type=str, nargs="?",
                        help='Path to an APMANUAL file')

    args = sys.argv[1:]
    if "Manual Client" in args:
        args.remove("Manual Client")
    args, rest = parser.parse_known_args(args=args)
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()

    if not os.path.exists(icon_paths["manual"]):
        # Download the icon for next time
        icon_url = "https://manualforarchipelago.github.io/ManualBuilder/images/ap-manual-discord-logo-square-96x96.png"
        with open(icon_paths["manual"], 'wb') as f:
            f.write(requests.get(icon_url).content)

if __name__ == '__main__':
    launch()
