if __name__ == "__main__":
    import ModuleUpdate

    ModuleUpdate.update()


import argparse
import logging
import os
import threading
import typing

from kvui import ThemedApp, ScrollBox, ContainerLayout, ToggleButton, TooltipLabel, dp, MDBoxLayout, MDLabel
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.textfield.textfield import MDTextField
from kivy.lang.builder import Builder
from kivy.clock import Clock

import Utils
from Utils import parse_yamls
from worlds.AutoWorld import AutoWorldRegister

logger = logging.getLogger("APWorldInfo")

DASHBOARD_KEY = "__dashboard__"


class GameButton(ToggleButton):
    """A toggle button representing a game in the left panel list."""

    game_key: str


class APWorldInfo(ThemedApp):
    base_title: str = "Archipelago APWorld Info"
    container: ContainerLayout
    game_list: ScrollBox
    detail_panel: ScrollBox
    current_selection: str = ""
    _search_event = None
    _all_buttons: typing.List[GameButton]
    _analysis_running: bool = False

    def build(self):
        self.set_colors()
        self.container = Builder.load_file(Utils.local_path("data", "apworldinfo.kv"))
        self.root = self.container
        self.game_list = self.container.ids.game_list
        self.detail_panel = self.container.ids.detail_panel
        self._all_buttons = []

        self._build_game_list()
        self._select_button(DASHBOARD_KEY)

        return self.container

    def _build_game_list(self):
        """Build the left panel list of game buttons."""
        layout = self.game_list.layout
        self._add_game_button(layout, "Dashboard", DASHBOARD_KEY)

        for name, cls in sorted(AutoWorldRegister.world_types.items(), key=lambda x: x[0].lower()):
            if cls.hidden or len(cls.item_names) == 0:
                continue
            self._add_game_button(layout, name, name)

    def _add_game_button(self, layout: MDBoxLayout, display_name: str, game_key: str):
        """Create and add a single GameButton to the list."""
        btn_text = MDButtonText(
            text=display_name, size_hint_y=None, width=dp(190), pos_hint={"x": 0.03, "center_y": 0.5}
        )
        btn_text.text_size = (btn_text.width, None)
        btn_text.bind(
            width=lambda *x, t=btn_text: t.setter("text_size")(t, (t.width, None)),
            texture_size=lambda *x, t=btn_text: t.setter("height")(t, t.texture_size[1]),
        )
        btn = GameButton(
            btn_text, size_hint_x=None, width=dp(190), theme_width="Custom", radius=(dp(5), dp(5), dp(5), dp(5))
        )
        btn.game_key = game_key
        btn.bind(on_release=lambda b: self._on_game_selected(b))
        layout.add_widget(btn)
        self._all_buttons.append(btn)

    def _on_game_selected(self, btn: GameButton):
        """Handle selection of a game button."""
        if self.current_selection == btn.game_key:
            btn.state = "down"
            return

        for b in self._all_buttons:
            if b.game_key == self.current_selection:
                b.state = "normal"
                break

        self.current_selection = btn.game_key
        self._show_detail(btn.game_key)

    def _select_button(self, game_key: str):
        """Programmatically select a button by game key."""
        for btn in self._all_buttons:
            if btn.game_key == game_key:
                btn.state = "down"
                self.current_selection = game_key
                self._show_detail(game_key)
                return

    def _show_detail(self, game_key: str):
        """Populate the right detail panel for the given selection."""
        layout = self.detail_panel.layout
        layout.clear_widgets()

        if game_key == DASHBOARD_KEY:
            self._show_dashboard(layout)
        else:
            self._show_game_detail(layout, game_key)

    def _show_dashboard(self, layout: MDBoxLayout):
        """Show the Dashboard view: player files overview."""
        title_row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(40),
            padding=[dp(20), dp(16), dp(20), 0],
            spacing=dp(10),
        )
        title_row.add_widget(
            MDLabel(
                text="Player Files",
                font_style="Title",
                role="medium",
                theme_text_color="Custom",
                text_color=self.theme_cls.primaryColor,
            )
        )
        reload_btn = MDButton(
            MDButtonText(text="Reload"),
            style="text",
            size_hint_x=None,
            pos_hint={"center_y": 0.5},
            on_press=lambda *_: self._reload_dashboard(),
        )
        title_row.add_widget(reload_btn)
        analyze_btn = MDButton(
            MDButtonText(text="Analyze"),
            style="text",
            size_hint_x=None,
            pos_hint={"center_y": 0.5},
            on_press=lambda *_: self._run_analysis(),
        )
        title_row.add_widget(analyze_btn)
        layout.add_widget(title_row)

        header_row = MDBoxLayout(
            orientation="horizontal", size_hint_y=None, height=dp(28), padding=[dp(20), 0, dp(20), 0]
        )
        estimate_tooltip = (
            "Item and location counts are estimates based on the full set defined by each game.<br>"
            "Actual counts may differ depending on player options.<br>"
            "Use Analyze for accurate counts from a partial generation."
        )
        for text, hint_x in [("File / Game", 0.4), ("Items (est.)", 0.2), ("Locations (est.)", 0.2), ("Weight", 0.2)]:
            if "(est.)" in text:
                header_row.add_widget(
                    TooltipLabel(
                        text=f"[ref=0|{estimate_tooltip}]{text}[/ref]",
                        font_style="Label",
                        role="large",
                        bold=True,
                        size_hint_x=hint_x,
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primaryColor,
                    )
                )
            else:
                header_row.add_widget(
                    MDLabel(
                        text=text,
                        font_style="Label",
                        role="large",
                        bold=True,
                        size_hint_x=hint_x,
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primaryColor,
                    )
                )
        layout.add_widget(header_row)

        self._populate_player_files(layout)

    def _reload_dashboard(self):
        """Reload the dashboard view."""
        if self.current_selection == DASHBOARD_KEY:
            self._show_detail(DASHBOARD_KEY)

    def _populate_player_files(self, layout: MDBoxLayout):
        """Read and display player file info."""
        try:
            from settings import get_settings

            generator_settings = get_settings().generator
            player_files_path = generator_settings.player_files_path
        except Exception:
            layout.add_widget(self._make_error_row("Could not read player files path from settings."))
            return

        if not os.path.isdir(player_files_path):
            layout.add_widget(self._make_error_row(f"Player files directory not found: {player_files_path}"))
            return

        try:
            meta_file_path = os.path.join(player_files_path, generator_settings.meta_file_path)
            weights_file_path = os.path.join(player_files_path, generator_settings.weights_file_path)
        except Exception:
            meta_file_path = ""
            weights_file_path = ""

        found_files = False
        for file in sorted(os.scandir(player_files_path), key=lambda f: f.name.casefold()):
            fname = file.name
            if not file.is_file() or fname.startswith(".") or fname.lower().endswith(".ini"):
                continue
            full_path = os.path.join(player_files_path, fname)
            if full_path in {meta_file_path, weights_file_path}:
                continue

            found_files = True
            self._add_player_file_rows(layout, fname, full_path)

        if not found_files:
            layout.add_widget(self._make_info_row(f"No player files found in: {player_files_path}"))
            layout.add_widget(self._make_info_row("Add .yaml files to the Players folder and click Reload."))

    def _add_player_file_rows(self, layout: MDBoxLayout, fname: str, path: str):
        """Parse a single player file and add rows for each game found."""

        header = MDBoxLayout(
            orientation="horizontal", size_hint_y=None, height=dp(28), padding=[dp(20), dp(4), dp(20), 0]
        )
        header.add_widget(
            MDLabel(
                text=fname,
                font_style="Body",
                role="medium",
                bold=True,
                theme_text_color="Custom",
                text_color=self.theme_cls.primaryColor,
            )
        )
        layout.add_widget(header)

        try:
            with open(path, "rb") as f:
                yaml_text = str(f.read(), "utf-8-sig")
            yamls = tuple(parse_yamls(yaml_text))
        except Exception as e:
            layout.add_widget(self._make_error_row(f"  Error reading file: {e}"))
            return

        for doc_idx, yaml_doc in enumerate(yamls):
            if yaml_doc is None:
                continue
            game = yaml_doc.get("game", None)
            if game is None:
                layout.add_widget(self._make_error_row(f"  Slot {doc_idx + 1}: No game specified"))
                continue

            if isinstance(game, str):
                self._add_player_game_row(layout, game, doc_idx, len(yamls))
            elif isinstance(game, dict):
                total_weight = sum(int(w) for w in game.values() if int(w) > 0)
                for game_name, weight in game.items():
                    weight = int(weight)
                    if weight <= 0:
                        continue
                    percentage = (weight / total_weight * 100) if total_weight > 0 else 0
                    self._add_player_game_row(layout, game_name, doc_idx, len(yamls), weight_text=f"{percentage:.0f}%")
            else:
                layout.add_widget(self._make_error_row(f"  Slot {doc_idx + 1}: Invalid game value"))

    def _add_player_game_row(
        self, layout: MDBoxLayout, game_name: str, doc_idx: int, total_docs: int, weight_text: str = ""
    ):
        """Add a row for a single game entry within a player file."""
        world_types = AutoWorldRegister.world_types
        prefix = f"  Slot {doc_idx + 1}: " if total_docs > 1 else "  "

        if game_name not in world_types:
            layout.add_widget(self._make_error_row(f"{prefix}{game_name}: Unknown game"))
            return

        cls = world_types[game_name]
        row = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(26), padding=[dp(20), 0, dp(20), 0])
        row.add_widget(
            MDLabel(
                text=f"{prefix}{game_name}",
                font_style="Body",
                role="small",
                size_hint_x=0.4,
                theme_text_color="Custom",
                text_color=self.theme_cls.primaryColor,
            )
        )
        row.add_widget(
            MDLabel(
                text=str(len(cls.item_names)),
                font_style="Body",
                role="small",
                size_hint_x=0.2,
                theme_text_color="Custom",
                text_color=self.theme_cls.primaryColor,
            )
        )
        row.add_widget(
            MDLabel(
                text=str(len(cls.location_names)),
                font_style="Body",
                role="small",
                size_hint_x=0.2,
                theme_text_color="Custom",
                text_color=self.theme_cls.primaryColor,
            )
        )
        row.add_widget(
            MDLabel(
                text=weight_text,
                font_style="Body",
                role="small",
                size_hint_x=0.2,
                theme_text_color="Custom",
                text_color=self.theme_cls.primaryColor,
            )
        )
        layout.add_widget(row)

    def _show_game_detail(self, layout: MDBoxLayout, game_name: str):
        """Show detail info for a specific installed APWorld."""
        world_types = AutoWorldRegister.world_types
        if game_name not in world_types:
            layout.add_widget(self._make_error_row(f"Unknown game: {game_name}"))
            return

        cls = world_types[game_name]
        primary = self.theme_cls.primaryColor

        layout.add_widget(
            MDLabel(
                text=game_name,
                font_style="Headline",
                role="small",
                size_hint_y=None,
                height=dp(44),
                padding=[dp(20), dp(16), dp(20), 0],
                theme_text_color="Custom",
                text_color=primary,
            )
        )

        estimate_tooltip = (
            "Item and location counts are estimates based on the full set defined by the game.<br>"
            "Actual counts may differ depending on player options.<br>"
            "Use Analyze on the Dashboard for accurate counts."
        )
        info = [
            ("Version", f"v{cls.world_version.as_simple_string()}"),
            ("Items (est.)", str(len(cls.item_names))),
            ("Locations (est.)", str(len(cls.location_names))),
        ]
        for label_text, value_text in info:
            row = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(30), padding=[dp(20), 0, dp(20), 0])
            if "(est.)" in label_text:
                row.add_widget(
                    TooltipLabel(
                        text=f"[ref=0|{estimate_tooltip}]{label_text}[/ref]",
                        font_style="Body",
                        role="medium",
                        bold=True,
                        size_hint_x=0.3,
                        theme_text_color="Custom",
                        text_color=primary,
                    )
                )
            else:
                row.add_widget(
                    MDLabel(
                        text=label_text,
                        font_style="Body",
                        role="medium",
                        bold=True,
                        size_hint_x=0.3,
                        theme_text_color="Custom",
                        text_color=primary,
                    )
                )
            row.add_widget(
                MDLabel(
                    text=value_text,
                    font_style="Body",
                    role="medium",
                    size_hint_x=0.7,
                    theme_text_color="Custom",
                    text_color=primary,
                )
            )
            layout.add_widget(row)

        self._show_game_player_files(layout, game_name)

    def _show_game_player_files(self, layout: MDBoxLayout, game_name: str):
        """Show which player files reference this game."""
        try:
            from settings import get_settings

            generator_settings = get_settings().generator
            player_files_path = generator_settings.player_files_path
        except Exception:
            return

        if not os.path.isdir(player_files_path):
            return

        try:
            meta_file_path = os.path.join(player_files_path, generator_settings.meta_file_path)
            weights_file_path = os.path.join(player_files_path, generator_settings.weights_file_path)
        except Exception:
            meta_file_path = ""
            weights_file_path = ""

        references = []
        for file in sorted(os.scandir(player_files_path), key=lambda f: f.name.casefold()):
            fname = file.name
            if not file.is_file() or fname.startswith(".") or fname.lower().endswith(".ini"):
                continue
            full_path = os.path.join(player_files_path, fname)
            if full_path in {meta_file_path, weights_file_path}:
                continue

            try:
                with open(full_path, "rb") as f:
                    yaml_text = str(f.read(), "utf-8-sig")
                for yaml_doc in parse_yamls(yaml_text):
                    if yaml_doc is None:
                        continue
                    game = yaml_doc.get("game", None)
                    if isinstance(game, str) and game == game_name:
                        references.append(fname)
                        break
                    elif isinstance(game, dict) and game_name in game:
                        weight = int(game[game_name])
                        if weight > 0:
                            total = sum(int(w) for w in game.values() if int(w) > 0)
                            pct = (weight / total * 100) if total > 0 else 0
                            references.append(f"{fname} ({pct:.0f}%)")
                            break
            except Exception:
                continue

        if references:
            layout.add_widget(MDBoxLayout(size_hint_y=None, height=dp(10)))

            layout.add_widget(
                MDLabel(
                    text="Referenced in Player Files",
                    font_style="Title",
                    role="small",
                    size_hint_y=None,
                    height=dp(32),
                    padding=[dp(20), 0, dp(20), 0],
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primaryColor,
                )
            )
            for ref in references:
                row = MDBoxLayout(
                    orientation="horizontal", size_hint_y=None, height=dp(26), padding=[dp(30), 0, dp(20), 0]
                )
                row.add_widget(
                    MDLabel(
                        text=ref,
                        font_style="Body",
                        role="small",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primaryColor,
                    )
                )
                layout.add_widget(row)

    def _run_analysis(self):
        """Start partial generation analysis in a background thread."""
        if self._analysis_running:
            return
        self._analysis_running = True

        layout = self.detail_panel.layout
        self._analysis_spacer = MDBoxLayout(size_hint_y=None, height=dp(16))
        layout.add_widget(self._analysis_spacer)
        self._analysis_status_label = MDLabel(
            text="Running generation analysis...",
            font_style="Title",
            role="small",
            size_hint_y=None,
            height=dp(32),
            padding=[dp(20), 0, dp(20), 0],
            theme_text_color="Custom",
            text_color=self.theme_cls.primaryColor,
        )
        layout.add_widget(self._analysis_status_label)

        thread = threading.Thread(target=self._do_analysis, daemon=True)
        thread.start()

    def _do_analysis(self):
        """Run partial generation pipeline (background thread). Collects counts, then schedules UI update."""
        results: typing.Dict[str, typing.Any] = {"players": [], "error": None}
        try:
            args, seed = self._build_args_from_yamls()
            if args is None:
                results["error"] = seed
                return

            player_results = self._run_partial_generation(args, seed)
            results["players"] = player_results
        except Exception as e:
            logger.exception("Analysis failed")
            results["error"] = str(e)
        finally:
            self._analysis_running = False
            Clock.schedule_once(lambda dt: self._show_analysis_results(results))

    def _build_args_from_yamls(self) -> typing.Tuple[typing.Optional[argparse.Namespace], typing.Any]:
        """
        Read player YAML files and build an args Namespace, replicating Generate.main() logic.
        Returns (args, seed) on success, or (None, error_message) on failure.
        """
        from collections import Counter
        from BaseClasses import PlandoOptions, get_seed
        from Generate import roll_settings, read_weights_yamls, handle_name

        from settings import get_settings

        generator_settings = get_settings().generator
        player_files_path = generator_settings.player_files_path

        if not os.path.isdir(player_files_path):
            return None, f"Player files directory not found: {player_files_path}"

        try:
            meta_file_path = os.path.join(player_files_path, generator_settings.meta_file_path)
            weights_file_path = os.path.join(player_files_path, generator_settings.weights_file_path)
        except Exception:
            meta_file_path = ""
            weights_file_path = ""

        weights_cache: typing.Dict[str, typing.Tuple] = {}
        if weights_file_path and os.path.exists(weights_file_path):
            try:
                weights_cache[weights_file_path] = read_weights_yamls(weights_file_path)
            except Exception as e:
                logger.warning(f"Could not read weights file: {e}")

        meta_weights = None
        if meta_file_path and os.path.exists(meta_file_path):
            try:
                meta_weights = read_weights_yamls(meta_file_path)[-1]
                if "meta_description" in meta_weights:
                    del meta_weights["meta_description"]
                else:
                    meta_weights = None
            except Exception:
                meta_weights = None

        player_id = 1
        player_files: typing.Dict[int, str] = {}
        errors: typing.List[str] = []

        for file in sorted(os.scandir(player_files_path), key=lambda f: f.name.casefold()):
            fname = file.name
            if not file.is_file() or fname.startswith(".") or fname.lower().endswith(".ini"):
                continue
            full_path = os.path.join(player_files_path, fname)
            if full_path in {meta_file_path, weights_file_path}:
                continue
            try:
                weights_for_file = []
                for doc_idx, yaml_doc in enumerate(read_weights_yamls(full_path)):
                    if yaml_doc is not None:
                        weights_for_file.append(yaml_doc)
                weights_cache[fname] = tuple(weights_for_file)
            except Exception as e:
                errors.append(f"File {fname}: {e}")

        weights_cache = {k: v for k, v in sorted(weights_cache.items(), key=lambda x: x[0].casefold())}
        for filename, yaml_data in weights_cache.items():
            if filename not in {meta_file_path, weights_file_path}:
                for _ in yaml_data:
                    player_files[player_id] = filename
                    player_id += 1

        num_players = max(player_id - 1, 0)
        if num_players == 0:
            return None, "No player files found."

        if meta_weights:
            import Options

            for category_name, category_dict in meta_weights.items():
                for key in category_dict:
                    from Generate import roll_meta_option

                    option = roll_meta_option(key, category_name, category_dict)
                    if option is not None:
                        for path in weights_cache:
                            for yaml_doc in weights_cache[path]:
                                if category_name is None:
                                    for category in yaml_doc:
                                        if (
                                            category in AutoWorldRegister.world_types
                                            and key in Options.CommonOptions.type_hints
                                        ):
                                            yaml_doc[category][key] = option
                                elif category_name not in yaml_doc:
                                    pass
                                elif key == "triggers":
                                    if "triggers" not in yaml_doc[category_name]:
                                        yaml_doc[category_name][key] = []
                                    for trigger in option:
                                        yaml_doc[category_name][key].append(trigger)
                                else:
                                    yaml_doc[category_name][key] = option

        seed = get_seed(42)
        args = argparse.Namespace()
        args.multi = num_players
        args.race = False
        args.outputpath = None
        args.outputname = "analysis"
        args.skip_output = True
        args.spoiler = 0
        args.spoiler_only = False
        args.csv_output = False
        args.skip_prog_balancing = True
        args.plando = PlandoOptions.bosses
        args.sprite = dict.fromkeys(range(1, num_players + 1), None)
        args.sprite_pool = dict.fromkeys(range(1, num_players + 1), None)
        args.name = {}
        args.game = {}

        player_path_cache: typing.Dict[int, str] = {}
        for player in range(1, num_players + 1):
            player_path_cache[player] = player_files.get(player, weights_file_path if weights_file_path else "")

        name_counter: Counter = Counter()
        player = 1
        while player <= num_players:
            path = player_path_cache[player]
            if not path or path not in weights_cache:
                errors.append(f"No weights specified for player {player}")
                player += 1
                continue

            for yaml_doc in weights_cache[path]:
                try:
                    settings_object = roll_settings(yaml_doc, args.plando)
                    for k, v in vars(settings_object).items():
                        if v is not None:
                            try:
                                getattr(args, k)[player] = v
                            except AttributeError:
                                setattr(args, k, {player: v})
                    if player not in args.name:
                        args.name[player] = os.path.splitext(os.path.split(path)[-1])[0]
                    args.name[player] = handle_name(args.name[player], player, name_counter)
                except Exception as e:
                    errors.append(f"Player {player} ({path}): {e}")
                    if player not in args.game:
                        args.game[player] = None
                    if player not in args.name:
                        args.name[player] = f"Player{player}"
                player += 1

        failed_players = {p for p in range(1, num_players + 1) if args.game.get(p) is None}
        if failed_players and len(failed_players) == num_players:
            return None, "All player files failed to parse:\n" + "\n".join(errors)

        if failed_players:
            good_players = sorted(set(range(1, num_players + 1)) - failed_players)
            new_args = argparse.Namespace()
            new_args.multi = len(good_players)
            new_args.race = args.race
            new_args.outputpath = args.outputpath
            new_args.outputname = args.outputname
            new_args.skip_output = args.skip_output
            new_args.spoiler = args.spoiler
            new_args.spoiler_only = args.spoiler_only
            new_args.csv_output = args.csv_output
            new_args.skip_prog_balancing = args.skip_prog_balancing
            new_args.plando = args.plando
            new_args.name = {}
            new_args.game = {}
            new_args.sprite = {}
            new_args.sprite_pool = {}

            for new_id, old_id in enumerate(good_players, start=1):
                new_args.name[new_id] = args.name.get(old_id, f"Player{old_id}")
                new_args.game[new_id] = args.game[old_id]
                new_args.sprite[new_id] = args.sprite.get(old_id)
                new_args.sprite_pool[new_id] = args.sprite_pool.get(old_id)

            for k, v in vars(args).items():
                if k in (
                    "multi",
                    "race",
                    "outputpath",
                    "outputname",
                    "skip_output",
                    "spoiler",
                    "spoiler_only",
                    "csv_output",
                    "skip_prog_balancing",
                    "plando",
                    "name",
                    "game",
                    "sprite",
                    "sprite_pool",
                ):
                    continue
                if isinstance(v, dict):
                    remapped = {}
                    for new_id, old_id in enumerate(good_players, start=1):
                        if old_id in v:
                            remapped[new_id] = v[old_id]
                    setattr(new_args, k, remapped)
                else:
                    setattr(new_args, k, v)

            args = new_args

        return args, seed

    def _run_partial_generation(self, args: argparse.Namespace, seed: int) -> typing.List[typing.Dict]:
        """Run Main.py steps 1-26 (through pre_fill) and extract per-player counts."""
        from BaseClasses import CollectionState, MultiWorld, LocationProgressType
        from Options import StartInventoryPool
        from worlds import AutoWorld
        from worlds.generic.Rules import exclusion_rules, locality_rules
        from Fill import parse_planned_blocks, distribute_planned_blocks, resolve_early_locations_for_planned

        multiworld = MultiWorld(args.multi)
        multiworld.set_seed(seed, args.race, str(args.outputname) if args.outputname else None)
        multiworld.plando_options = args.plando
        multiworld.game = args.game.copy()
        multiworld.player_name = args.name.copy()
        multiworld.sprite = args.sprite.copy()
        multiworld.sprite_pool = args.sprite_pool.copy()

        multiworld.set_options(args)
        multiworld.set_item_links()
        multiworld.state = CollectionState(multiworld)

        AutoWorld.call_all(multiworld, "generate_early")

        for player in multiworld.player_ids:
            for item_name, count in multiworld.worlds[player].options.start_inventory.value.items():
                for _ in range(count):
                    multiworld.push_precollected(multiworld.create_item(item_name, player))
            for item_name, count in getattr(
                multiworld.worlds[player].options, "start_inventory_from_pool", StartInventoryPool({})
            ).value.items():
                for _ in range(count):
                    multiworld.push_precollected(multiworld.create_item(item_name, player))
                early = multiworld.early_items[player].get(item_name, 0)
                if early:
                    multiworld.early_items[player][item_name] = max(0, early - count)
                    remaining_count = count - early
                    if remaining_count > 0:
                        local_early = multiworld.local_early_items[player].get(item_name, 0)
                        if local_early:
                            multiworld.early_items[player][item_name] = max(0, local_early - remaining_count)

            multiworld.worlds[player].options.non_local_items.value -= multiworld.worlds[
                player
            ].options.local_items.value
            multiworld.worlds[player].options.non_local_items.value -= set(multiworld.local_early_items[player])

        if multiworld.players == 1:
            multiworld.worlds[1].options.non_local_items.value = set()
            multiworld.worlds[1].options.local_items.value = set()

        AutoWorld.call_all(multiworld, "create_regions")
        AutoWorld.call_all(multiworld, "create_items")
        AutoWorld.call_all(multiworld, "set_rules")

        for player in multiworld.player_ids:
            exclusion_rules(multiworld, player, multiworld.worlds[player].options.exclude_locations.value)
            multiworld.worlds[player].options.priority_locations.value -= multiworld.worlds[
                player
            ].options.exclude_locations.value
            for location_name in list(multiworld.worlds[player].options.priority_locations.value):
                try:
                    location = multiworld.get_location(location_name, player)
                except KeyError:
                    continue
                if location.progress_type != LocationProgressType.EXCLUDED:
                    location.progress_type = LocationProgressType.PRIORITY

        if multiworld.players > 1:
            locality_rules(multiworld)

        multiworld.plando_item_blocks = parse_planned_blocks(multiworld)
        AutoWorld.call_all(multiworld, "connect_entrances")
        AutoWorld.call_all(multiworld, "generate_basic")

        fallback_inventory = StartInventoryPool({})
        depletion_pool = {
            player: getattr(
                multiworld.worlds[player].options, "start_inventory_from_pool", fallback_inventory
            ).value.copy()
            for player in multiworld.player_ids
        }
        target_per_player = {
            player: sum(target_items.values()) for player, target_items in depletion_pool.items() if target_items
        }
        if target_per_player:
            new_itempool = []
            for item in multiworld.itempool:
                if depletion_pool[item.player].get(item.name, 0):
                    depletion_pool[item.player][item.name] -= 1
                else:
                    new_itempool.append(item)
            for player, target in target_per_player.items():
                unfound_items = {item: count for item, count in depletion_pool[player].items() if count}
                needed_items = target_per_player[player] - sum(unfound_items.values())
                new_itempool += [multiworld.worlds[player].create_filler() for _ in range(needed_items)]
            multiworld.itempool[:] = new_itempool

        multiworld.link_items()
        if any(world.options.item_links for world in multiworld.worlds.values()):
            multiworld._all_state = None

        resolve_early_locations_for_planned(multiworld)
        distribute_planned_blocks(
            multiworld, [x for player in multiworld.plando_item_blocks for x in multiworld.plando_item_blocks[player]]
        )

        AutoWorld.call_all(multiworld, "pre_fill")

        player_results = []
        for player in multiworld.player_ids:
            game = multiworld.game.get(player, "Unknown")
            name = multiworld.player_name.get(player, f"Player{player}")
            all_locations = [
                loc for loc in multiworld.get_locations() if loc.player == player and loc.address is not None
            ]
            filled = [loc for loc in all_locations if loc.item is not None]
            pool_items = [item for item in multiworld.itempool if item.player == player]
            precollected = multiworld.precollected_items.get(player, [])

            player_results.append(
                {
                    "player": player,
                    "name": name,
                    "game": game,
                    "locations": len(all_locations),
                    "pool_items": len(pool_items),
                    "prefilled": len(filled),
                    "precollected": len(precollected),
                    "error": None,
                }
            )

        del multiworld
        return player_results

    def _show_analysis_results(self, results: typing.Dict[str, typing.Any]):
        """Display analysis results in the detail panel (called on main thread)."""
        if self.current_selection != DASHBOARD_KEY:
            return

        layout = self.detail_panel.layout
        primary = self.theme_cls.primaryColor

        if hasattr(self, "_analysis_spacer") and self._analysis_spacer.parent:
            layout.remove_widget(self._analysis_spacer)
        if hasattr(self, "_analysis_status_label") and self._analysis_status_label.parent:
            layout.remove_widget(self._analysis_status_label)

        if results["error"]:
            layout.add_widget(MDBoxLayout(size_hint_y=None, height=dp(16)))
            layout.add_widget(
                MDLabel(
                    text="Generation Analysis",
                    font_style="Title",
                    role="small",
                    size_hint_y=None,
                    height=dp(32),
                    padding=[dp(20), 0, dp(20), 0],
                    theme_text_color="Custom",
                    text_color=primary,
                )
            )
            layout.add_widget(self._make_error_row(f"Analysis failed: {results['error']}"))
            return

        players = results.get("players", [])
        if not players:
            return

        layout.add_widget(MDBoxLayout(size_hint_y=None, height=dp(16)))
        layout.add_widget(
            MDLabel(
                text="Generation Analysis",
                font_style="Title",
                role="small",
                size_hint_y=None,
                height=dp(32),
                padding=[dp(20), 0, dp(20), 0],
                theme_text_color="Custom",
                text_color=primary,
            )
        )

        columns = [
            ("Slot / Game", 0.35),
            ("Locations", 0.15),
            ("Pool Items", 0.15),
            ("Pre-filled", 0.15),
            ("Start Inv.", 0.2),
        ]
        header_row = MDBoxLayout(
            orientation="horizontal", size_hint_y=None, height=dp(28), padding=[dp(20), 0, dp(20), 0]
        )
        for text, hint_x in columns:
            header_row.add_widget(
                MDLabel(
                    text=text,
                    font_style="Label",
                    role="large",
                    bold=True,
                    size_hint_x=hint_x,
                    theme_text_color="Custom",
                    text_color=primary,
                )
            )
        layout.add_widget(header_row)

        totals = {"locations": 0, "pool_items": 0, "prefilled": 0, "precollected": 0}
        for p in players:
            if p["error"]:
                layout.add_widget(self._make_error_row(f"  P{p['player']} ({p['game']}): {p['error']}"))
                continue

            slot_text = f"  P{p['player']}: {p['game']}"
            row = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(26),
                padding=[dp(20), 0, dp(20), 0],
            )
            for text, hint_x in [
                (slot_text, 0.35),
                (str(p["locations"]), 0.15),
                (str(p["pool_items"]), 0.15),
                (str(p["prefilled"]), 0.15),
                (str(p["precollected"]), 0.2),
            ]:
                row.add_widget(
                    MDLabel(
                        text=text,
                        font_style="Body",
                        role="small",
                        size_hint_x=hint_x,
                        theme_text_color="Custom",
                        text_color=primary,
                    )
                )
            layout.add_widget(row)

            totals["locations"] += p["locations"]
            totals["pool_items"] += p["pool_items"]
            totals["prefilled"] += p["prefilled"]
            totals["precollected"] += p["precollected"]

        totals_row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(28),
            padding=[dp(20), dp(4), dp(20), 0],
        )
        for text, hint_x in [
            ("  Total", 0.35),
            (str(totals["locations"]), 0.15),
            (str(totals["pool_items"]), 0.15),
            (str(totals["prefilled"]), 0.15),
            (str(totals["precollected"]), 0.2),
        ]:
            totals_row.add_widget(
                MDLabel(
                    text=text,
                    font_style="Body",
                    role="small",
                    bold=True,
                    size_hint_x=hint_x,
                    theme_text_color="Custom",
                    text_color=primary,
                )
            )
        layout.add_widget(totals_row)

    def on_search_text(self, instance: MDTextField, text: str):
        """Debounced search callback — called by the MDTextField's set_text property."""
        if self._search_event is not None:
            self._search_event.cancel()
        self._search_event = Clock.schedule_once(lambda dt: self._filter_game_list(text), 0.2)

    def _filter_game_list(self, search_text: str):
        """Show/hide game buttons based on search text."""
        layout = self.game_list.layout
        layout.clear_widgets()
        search_lower = search_text.lower().strip()

        for btn in self._all_buttons:
            if btn.game_key == DASHBOARD_KEY:
                # Always show Dashboard
                layout.add_widget(btn)
            elif not search_lower or search_lower in btn.game_key.lower():
                layout.add_widget(btn)

    @staticmethod
    def _make_error_row(text: str) -> MDBoxLayout:
        """Create a row displaying an error message in red."""
        row = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(26), padding=[dp(20), 0, dp(20), 0])
        row.add_widget(
            MDLabel(
                text=text, font_style="Body", role="small", theme_text_color="Custom", text_color=(0.8, 0.3, 0.3, 1)
            )
        )
        return row

    @staticmethod
    def _make_info_row(text: str) -> MDBoxLayout:
        """Create a row displaying an informational message in subdued text."""
        row = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(26), padding=[dp(20), 0, dp(20), 0])
        row.add_widget(
            MDLabel(
                text=text, font_style="Body", role="small", theme_text_color="Custom", text_color=(0.6, 0.6, 0.6, 1)
            )
        )
        return row


def launch():
    APWorldInfo().run()


if __name__ == "__main__":
    Utils.init_logging("APWorldInfo")
    launch()
