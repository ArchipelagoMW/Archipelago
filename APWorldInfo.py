if __name__ == "__main__":
    import ModuleUpdate

    ModuleUpdate.update()

import argparse
import logging
import os
from typing import Any

import Utils
from settings import get_settings

logger = logging.getLogger("APWorldInfo")


def get_all_world_info() -> list[dict[str, Any]]:
    """Get basic info for all installed, non-hidden worlds."""
    from worlds.AutoWorld import AutoWorldRegister

    world_info = []
    for name, cls in sorted(AutoWorldRegister.world_types.items()):
        if cls.hidden or len(cls.item_names) == 0:
            continue
        world_info.append(
            {
                "game": name,
                "version": cls.world_version.as_simple_string(),
                "items": len(cls.item_names),
                "locations": len(cls.location_names),
                "cls": cls,
            }
        )
    return world_info


def scan_player_yamls(
    player_path: str,
) -> tuple[
    dict[str, list[dict[str, Any]]],
    list[dict[str, Any]] | None,
    list[dict[str, str]],
]:
    """
    Scan Players folder for YAML files and group by game.
    Also loads weights.yaml separately if it exists (matching Generate.py behavior).

    Returns: (
        {game_name: [{'filename': str, 'name': str, 'yaml': dict, 'path': str}, ...]},
        weights_configs or None,  # Configs from weights.yaml if it exists
        parse_errors  # List of {'filename': str, 'error': str} for files that failed to parse
    )
    """
    from Utils import parse_yamls

    yamls_by_game: dict[str, list[dict[str, Any]]] = {}
    parse_errors: list[dict[str, str]] = []

    if not os.path.isdir(player_path):
        return yamls_by_game, None, parse_errors

    for file in os.scandir(player_path):
        if not file.is_file():
            continue
        fname = file.name
        if fname.startswith(".") or fname.lower().endswith(".ini"):
            continue
        # Skip weights.yaml and meta.yaml in main loop (matches Generate.py line 128)
        if fname in ("weights.yaml", "meta.yaml"):
            continue

        try:
            with open(file.path, "rb") as f:
                content = str(f.read(), "utf-8-sig")

            for doc in parse_yamls(content):
                if doc is None:
                    continue
                game = doc.get("game")
                # Handle weighted game option (e.g., game: {Archipelago: 50, ChecksFinder: 50})
                if isinstance(game, dict):
                    if game:
                        # Pick the game with highest weight for display purposes
                        game = max(game.keys(), key=lambda k: game[k] if isinstance(game[k], (int, float)) else 0)
                    else:
                        continue
                elif not game or not isinstance(game, str):
                    continue

                player_name = doc.get("name", os.path.splitext(fname)[0])

                if game not in yamls_by_game:
                    yamls_by_game[game] = []
                yamls_by_game[game].append(
                    {
                        "filename": fname,
                        "name": player_name,
                        "yaml": doc,
                        "path": file.path,
                    }
                )
        except Exception as e:
            parse_errors.append({"filename": fname, "error": str(e)})
            continue

    # Load weights.yaml separately (matches Generate.py lines 99-105)
    weights_configs: list[dict[str, Any]] | None = None
    weights_path = os.path.join(player_path, "weights.yaml")
    if os.path.isfile(weights_path):
        try:
            with open(weights_path, "rb") as f:
                content = str(f.read(), "utf-8-sig")
            weights_docs = list(parse_yamls(content))
            weights_configs = []
            for doc in weights_docs:
                if doc is None:
                    continue
                game = doc.get("game")
                # Handle weighted game option (e.g., game: {Archipelago: 1})
                if isinstance(game, dict) and game:
                    game = max(game.keys(), key=lambda k: game[k] if isinstance(game[k], (int, float)) else 0)
                if game and isinstance(game, str):
                    weights_configs.append(
                        {
                            "filename": "weights.yaml",
                            "name": doc.get("name", "Player{number}"),
                            "game": game,
                            "yaml": doc,
                            "path": weights_path,
                            "is_weights_file": True,
                        }
                    )
            if not weights_configs:
                weights_configs = None
        except Exception as e:
            parse_errors.append({"filename": "weights.yaml", "error": str(e)})

    return yamls_by_game, weights_configs, parse_errors


def get_config_item_location_counts(game: str, yaml_data: dict) -> tuple[int, int]:
    """
    Run partial generation to get accurate item/location counts for a config.
    Uses roll_settings from Generate.py to properly resolve triggers and linked_options.
    Returns: (item_count, location_count) or (-1, -1) on failure.
    """
    import random

    from BaseClasses import CollectionState, MultiWorld, PlandoOptions
    from Generate import roll_settings
    from worlds.AutoWorld import AutoWorldRegister, call_single

    if game not in AutoWorldRegister.world_types:
        return (-1, -1)

    world_type = AutoWorldRegister.world_types[game]

    try:
        # Save random state and use fixed seed for deterministic option rolling
        random_state = random.getstate()
        random.seed(0)

        # Use roll_settings to properly resolve all options including triggers/linked_options
        plando_options = PlandoOptions.connections | PlandoOptions.bosses
        settings = roll_settings(yaml_data, plando_options)

        # Restore random state
        random.setstate(random_state)

        # Create minimal multiworld
        multiworld = MultiWorld(1)
        multiworld.game = {1: game}
        multiworld.player_name = {1: settings.name if settings.name else "Info"}
        multiworld.set_seed(0)
        multiworld.plando_options = plando_options

        # Initialize world instance
        multiworld.worlds[1] = world_type(multiworld, 1)

        # Build options from rolled settings (same pattern as MultiWorld.set_options)
        options_dataclass = world_type.options_dataclass
        options_dict = {option_key: getattr(settings, option_key) for option_key in options_dataclass.type_hints}
        multiworld.worlds[1].options = options_dataclass(**options_dict)

        # Initialize state and run generation steps
        multiworld.state = CollectionState(multiworld)
        call_single(multiworld, "generate_early", 1)
        call_single(multiworld, "create_regions", 1)
        call_single(multiworld, "create_items", 1)

        # Count results
        items = len(multiworld.itempool)
        locations = len([loc for loc in multiworld.get_locations(1) if not loc.is_event])

        return (items, locations)

    except Exception as e:
        logger.warning(f"Could not get config counts for {game}: {e}")
        import traceback

        logger.debug(traceback.format_exc())
        return (-1, -1)


def print_world_info() -> None:
    """Print world info to console (CLI mode)."""
    worlds = get_all_world_info()

    if not worlds:
        print("No worlds found.")
        return

    # Calculate column widths
    longest_name = max(len(w["game"]) for w in worlds)
    version_width = max(len(w["version"]) for w in worlds)
    item_width = len(str(max(w["items"] for w in worlds)))
    loc_width = len(str(max(w["locations"] for w in worlds)))

    print(f"\nFound {len(worlds)} World Types:\n")
    print("(Possible Items/Locations = all defined in the world; actual counts depend on options)\n")
    print(
        f" {'Game':{longest_name}} | {'Version':{version_width}} | "
        f"{'Possible Items':>{item_width + 14}} | {'Possible Locations':>{loc_width + 18}}"
    )
    print("-" * (longest_name + version_width + item_width + loc_width + 41))

    for w in worlds:
        print(
            f" {w['game']:{longest_name}} | v{w['version']:{version_width}} | "
            f"Possible Items: {w['items']:{item_width}} | Possible Locations: {w['locations']:{loc_width}}"
        )

    # Always scan for player configs
    settings = get_settings()
    player_path = settings.generator.player_files_path

    if player_path and os.path.isdir(player_path):
        yamls_by_game, weights_configs, parse_errors = scan_player_yamls(player_path)
        player_data: list[dict[str, Any]] = []

        # Display parse errors first if any
        if parse_errors:
            print(f"\n\n{'=' * 60}")
            print("YAML PARSE ERRORS")
            print(f"{'=' * 60}")
            print("\nThe following files could not be parsed:\n")
            for err in parse_errors:
                print(f"  {err['filename']}:")
                # Indent the error message for readability
                error_lines = err["error"].split("\n")
                for line in error_lines[:3]:  # Show first 3 lines of error
                    print(f"    {line}")
                if len(error_lines) > 3:
                    print(f"    ... ({len(error_lines) - 3} more lines)")
            print()

        if yamls_by_game:
            # Build player overview with counts
            for game, configs in yamls_by_game.items():
                for cfg in configs:
                    items, locs = get_config_item_location_counts(game, cfg["yaml"])
                    player_data.append(
                        {
                            "name": cfg["name"],
                            "game": game,
                            "filename": cfg["filename"],
                            "items": items if items >= 0 else 0,
                            "locations": locs if locs >= 0 else 0,
                        }
                    )

            # Calculate totals
            total_items = sum(p["items"] for p in player_data)
            total_locations = sum(p["locations"] for p in player_data)

            # Print overview
            print(f"\n\n{'=' * 60}")
            print(f"MULTIWORLD OVERVIEW")
            print(f"{'=' * 60}")
            print(f"\nPlayers: {len(player_data)}")
            print(f"Total Items: {total_items}")
            print(f"Total Locations: {total_locations}")

            # Player table
            if player_data:
                name_width = max(len(p["name"]) for p in player_data)
                game_width = max(len(p["game"]) for p in player_data)
                item_width = len(str(max(p["items"] for p in player_data)))
                loc_width = len(str(max(p["locations"] for p in player_data)))

                print(
                    f"\n {'Player':{name_width}} | {'Game':{game_width}} | {'Items':>{item_width + 7}} | {'Locations':>{loc_width + 11}}"
                )
                print("-" * (name_width + game_width + item_width + loc_width + 30))

                for p in sorted(player_data, key=lambda x: x["name"].lower()):
                    print(
                        f" {p['name']:{name_width}} | {p['game']:{game_width}} | "
                        f"Items: {p['items']:{item_width}} | Locations: {p['locations']:{loc_width}}"
                    )

            # Detailed breakdown by game
            print(f"\n\nPlayer Configurations Found in '{player_path}':\n")

            for game, configs in sorted(yamls_by_game.items()):
                print(f"\n  {game}:")
                for cfg in configs:
                    # Show player name as heading
                    player_name = cfg["name"]
                    # Find the cached data
                    cached = next((p for p in player_data if p["name"] == player_name and p["game"] == game), None)
                    if cached and cached["items"] > 0:
                        print(f"    [{player_name}] ({cfg['filename']})")
                        print(f"      Items: {cached['items']}, Locations: {cached['locations']}")
                    else:
                        # Fall back to base counts
                        from worlds.AutoWorld import AutoWorldRegister

                        if game in AutoWorldRegister.world_types:
                            cls = AutoWorldRegister.world_types[game]
                            print(f"    [{player_name}] ({cfg['filename']})")
                            print(
                                f"      Items: {len(cls.item_names)}, Locations: {len(cls.location_names)} (possible)"
                            )

        # Display weights.yaml if present
        if weights_configs:
            configured_players = settings.generator.players
            individual_count = len(player_data) if yamls_by_game else 0

            print(f"\n\n{'=' * 60}")
            print("GENERIC WEIGHTS FILE (weights.yaml)")
            print(f"{'=' * 60}")
            print("\nNote: Fallback weights for players without individual YAML files.")
            print(f"  Configured players in host.yaml: {configured_players} (0 = infer from files)")
            print(f"  Individual player files found: {individual_count}")
            if configured_players > 0:
                additional_players = max(0, configured_players - individual_count)
                print(f"  Additional players using weights.yaml: {additional_players}")

            for cfg in weights_configs:
                game = cfg["game"]
                items, locs = get_config_item_location_counts(game, cfg["yaml"])
                print(f"\n  {game}:")
                print(f"    Template name: {cfg['name']}")
                if items >= 0:
                    print(f"    Items: {items}, Locations: {locs} (per player)")
                else:
                    print(f"    Could not calculate counts")


def run_gui() -> None:
    """Launch the Kivy GUI."""
    from kvui import ThemedApp, ScrollBox, MainLayout, ContainerLayout, dp, MDLabel, ToggleButton
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivymd.uix.button import MDButtonText
    from kivymd.uix.divider import MDDivider
    from kivy.lang.builder import Builder

    class WorldButton(ToggleButton):
        world_data: dict

    class APWorldInfoApp(ThemedApp):
        base_title: str = "APWorld Info"
        current_game: str = ""
        yamls_by_game: dict[str, list[dict[str, Any]]] = {}
        weights_configs: list[dict[str, Any]] | None = None
        parse_errors: list[dict[str, str]] = []

        def __init__(self):
            self.title = f"{self.base_title} - Archipelago {Utils.__version__}"
            self.icon = r"data/icon.png"
            self.title_row = None
            self.title_label = None
            super().__init__()

        def build(self):
            self.set_colors()
            self.container = Builder.load_file(Utils.local_path("data/apworldinfo.kv"))
            self.root = self.container

            self.scrollbox = self.container.ids.scrollbox
            self.info_layout = self.container.ids.info_layout

            # Load player yamls
            settings = get_settings()
            player_path = settings.generator.player_files_path
            if player_path and os.path.isdir(player_path):
                self.yamls_by_game, self.weights_configs, self.parse_errors = scan_player_yamls(player_path)

            # Populate world list
            worlds = get_all_world_info()

            def on_world_select(btn: WorldButton):
                # Deselect others (including overview button)
                for child in self.scrollbox.layout.children:
                    if isinstance(child, (WorldButton, ToggleButton)) and child != btn:
                        child.state = "normal"
                btn.state = "down"
                self.show_world_details(btn.world_data)

            def on_overview_select(btn):
                # Deselect all world buttons
                for child in self.scrollbox.layout.children:
                    if isinstance(child, WorldButton):
                        child.state = "normal"
                btn.state = "down"
                self.show_overview()

            # Add Overview button at the top
            overview_text = MDButtonText(
                text="Overview", size_hint_y=None, width=dp(200), pos_hint={"x": 0.03, "center_y": 0.5}
            )
            overview_btn = ToggleButton(
                overview_text, size_hint_x=None, width=dp(200), theme_width="Custom", radius=(dp(5),) * 4
            )
            overview_btn.bind(on_release=on_overview_select)
            self.scrollbox.layout.add_widget(overview_btn)
            self.overview_btn = overview_btn

            for w in worlds:
                btn_text = MDButtonText(
                    text=w["game"], size_hint_y=None, width=dp(200), pos_hint={"x": 0.03, "center_y": 0.5}
                )
                btn = WorldButton(btn_text, size_hint_x=None, width=dp(200), theme_width="Custom", radius=(dp(5),) * 4)
                btn.world_data = w
                btn.bind(on_release=on_world_select)
                self.scrollbox.layout.add_widget(btn)

            # Show overview on startup
            self.overview_btn.state = "down"
            self.show_overview()

            return self.container

        def _create_title_row(self, title_text: str):
            """Create or update the title row with Refresh button."""
            from kivymd.uix.button import MDButton

            # Create the row only once, then reuse it
            if self.title_row is None:
                self.title_row = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(50), spacing=dp(10))

                self.title_label = MDLabel(
                    text=f"[b]{title_text}[/b]",
                    markup=True,
                    font_style="Title",
                    role="large",
                    size_hint_x=1,
                )
                self.title_row.add_widget(self.title_label)

                def on_refresh(btn):
                    # Reload player yamls
                    settings = get_settings()
                    player_path = settings.generator.player_files_path
                    if player_path and os.path.isdir(player_path):
                        self.yamls_by_game, self.weights_configs, self.parse_errors = scan_player_yamls(player_path)
                    else:
                        self.yamls_by_game = {}
                        self.weights_configs = None
                        self.parse_errors = []

                    # Refresh the current view
                    if self.overview_btn.state == "down":
                        self.show_overview()
                    else:
                        # Find which world is selected and refresh it
                        for child in self.scrollbox.layout.children:
                            if isinstance(child, WorldButton) and child.state == "down":
                                self.show_world_details(child.world_data)
                                break

                refresh_text = MDButtonText(text="Refresh", pos_hint={"center_y": 0.5})
                refresh_btn = MDButton(
                    refresh_text,
                    size_hint_x=None,
                    width=dp(100),
                    theme_width="Custom",
                    radius=(dp(5),) * 4,
                )
                refresh_btn.bind(on_release=on_refresh)
                self.title_row.add_widget(refresh_btn)
            else:
                # Just update the title text
                self.title_label.text = f"[b]{title_text}[/b]"

            # Remove from parent if it has one (so we can re-add it)
            if self.title_row.parent:
                self.title_row.parent.remove_widget(self.title_row)

            return self.title_row

        def show_overview(self):
            """Display multiworld overview with all players and totals."""
            self.info_layout.clear_widgets()

            # Title row with Refresh button
            title_row = self._create_title_row("Multiworld Overview")
            self.info_layout.add_widget(title_row)

            # Display parse errors at the top if any
            if self.parse_errors:
                self.info_layout.add_widget(MDDivider())

                error_title = MDLabel(
                    text="[b][color=#ff6b6b]YAML Parse Errors[/color][/b]",
                    markup=True,
                    size_hint_y=None,
                    height=dp(30),
                )
                self.info_layout.add_widget(error_title)

                error_note = MDLabel(
                    text="  The following files could not be parsed:",
                    size_hint_y=None,
                    height=dp(25),
                    theme_text_color="Secondary",
                )
                self.info_layout.add_widget(error_note)

                for err in self.parse_errors:
                    filename_label = MDLabel(
                        text=f"  [color=#ff6b6b]{err['filename']}[/color]",
                        markup=True,
                        size_hint_y=None,
                        height=dp(25),
                    )
                    self.info_layout.add_widget(filename_label)

                    # Show first line of error message
                    error_msg = err["error"].split("\n")[0]
                    if len(error_msg) > 80:
                        error_msg = error_msg[:77] + "..."
                    error_label = MDLabel(
                        text=f"    {error_msg}",
                        size_hint_y=None,
                        height=dp(20),
                        theme_text_color="Secondary",
                    )
                    self.info_layout.add_widget(error_label)

            if not self.yamls_by_game and not self.weights_configs and not self.parse_errors:
                no_configs = MDLabel(
                    text="No player configurations found in Players folder.",
                    size_hint_y=None,
                    height=dp(30),
                )
                self.info_layout.add_widget(no_configs)
                return

            # Build player data with counts
            player_data: list[dict[str, Any]] = []
            if self.yamls_by_game:
                for game, configs in self.yamls_by_game.items():
                    for cfg in configs:
                        items, locs = get_config_item_location_counts(game, cfg["yaml"])
                        player_data.append(
                            {
                                "name": cfg["name"],
                                "game": game,
                                "items": items if items >= 0 else 0,
                                "locations": locs if locs >= 0 else 0,
                            }
                        )

            if player_data:
                # Calculate totals
                total_items = sum(p["items"] for p in player_data)
                total_locations = sum(p["locations"] for p in player_data)

                self.info_layout.add_widget(MDDivider())

                # Summary stats
                summary_title = MDLabel(text="[b]Summary[/b]", markup=True, size_hint_y=None, height=dp(30))
                self.info_layout.add_widget(summary_title)

                players_label = MDLabel(text=f"  Players: {len(player_data)}", size_hint_y=None, height=dp(25))
                items_label = MDLabel(text=f"  Total Items: {total_items}", size_hint_y=None, height=dp(25))
                locs_label = MDLabel(text=f"  Total Locations: {total_locations}", size_hint_y=None, height=dp(25))
                self.info_layout.add_widget(players_label)
                self.info_layout.add_widget(items_label)
                self.info_layout.add_widget(locs_label)

                self.info_layout.add_widget(MDDivider())

                # Player list
                list_title = MDLabel(text="[b]Players[/b]", markup=True, size_hint_y=None, height=dp(30))
                self.info_layout.add_widget(list_title)

                for p in sorted(player_data, key=lambda x: str(x["name"]).lower()):
                    player_label = MDLabel(
                        text=f"  [b]{p['name']}[/b] - {p['game']}",
                        markup=True,
                        size_hint_y=None,
                        height=dp(25),
                    )
                    self.info_layout.add_widget(player_label)

                    counts_label = MDLabel(
                        text=f"    Items: {p['items']}, Locations: {p['locations']}",
                        size_hint_y=None,
                        height=dp(20),
                    )
                    self.info_layout.add_widget(counts_label)

            # Display weights.yaml section if present
            if self.weights_configs:
                settings = get_settings()
                configured_players = settings.generator.players
                individual_count = len(player_data)

                self.info_layout.add_widget(MDDivider())

                weights_title = MDLabel(
                    text="[b]Generic Weights File (weights.yaml)[/b]",
                    markup=True,
                    size_hint_y=None,
                    height=dp(30),
                )
                self.info_layout.add_widget(weights_title)

                note_label = MDLabel(
                    text="  Fallback weights for players without individual YAML files.",
                    size_hint_y=None,
                    height=dp(25),
                    theme_text_color="Secondary",
                )
                self.info_layout.add_widget(note_label)

                config_label = MDLabel(
                    text=f"  Configured players: {configured_players} (0 = infer from files)",
                    size_hint_y=None,
                    height=dp(25),
                )
                self.info_layout.add_widget(config_label)

                individual_label = MDLabel(
                    text=f"  Individual player files: {individual_count}",
                    size_hint_y=None,
                    height=dp(25),
                )
                self.info_layout.add_widget(individual_label)

                if configured_players > 0:
                    additional = max(0, configured_players - individual_count)
                    additional_label = MDLabel(
                        text=f"  Additional players using weights: {additional}",
                        size_hint_y=None,
                        height=dp(25),
                    )
                    self.info_layout.add_widget(additional_label)

                for cfg in self.weights_configs:
                    game = cfg["game"]
                    items, locs = get_config_item_location_counts(game, cfg["yaml"])

                    game_label = MDLabel(
                        text=f"\n  [b]{game}[/b]",
                        markup=True,
                        size_hint_y=None,
                        height=dp(30),
                    )
                    self.info_layout.add_widget(game_label)

                    template_label = MDLabel(
                        text=f"    Template name: {cfg['name']}",
                        size_hint_y=None,
                        height=dp(25),
                    )
                    self.info_layout.add_widget(template_label)

                    if items >= 0:
                        counts_text = f"    Items: {items}, Locations: {locs} (per player)"
                    else:
                        counts_text = "    Could not calculate counts"

                    weights_counts_label = MDLabel(
                        text=counts_text,
                        size_hint_y=None,
                        height=dp(25),
                    )
                    self.info_layout.add_widget(weights_counts_label)

        def show_world_details(self, world_data: dict):
            """Display details for selected world."""
            self.info_layout.clear_widgets()
            game = world_data["game"]

            # Title row with Refresh button
            title_row = self._create_title_row(game)
            self.info_layout.add_widget(title_row)

            # Version
            version_label = MDLabel(text=f"Version: {world_data['version']}", size_hint_y=None, height=dp(30))
            self.info_layout.add_widget(version_label)

            self.info_layout.add_widget(MDDivider())

            # Base stats - these are all possible items/locations defined in the world
            stats_title = MDLabel(text="[b]Possible Items/Locations[/b]", markup=True, size_hint_y=None, height=dp(30))
            self.info_layout.add_widget(stats_title)

            note_label = MDLabel(
                text="  (All defined in world; actual counts depend on options)",
                size_hint_y=None,
                height=dp(20),
                theme_text_color="Secondary",
            )
            self.info_layout.add_widget(note_label)

            items_label = MDLabel(text=f"  Items: {world_data['items']}", size_hint_y=None, height=dp(25))
            locs_label = MDLabel(text=f"  Locations: {world_data['locations']}", size_hint_y=None, height=dp(25))
            self.info_layout.add_widget(items_label)
            self.info_layout.add_widget(locs_label)

            # Config section if yamls exist for this game
            if game in self.yamls_by_game:
                self.info_layout.add_widget(MDDivider())

                config_title = MDLabel(
                    text="[b]Player Configurations[/b]", markup=True, size_hint_y=None, height=dp(30)
                )
                self.info_layout.add_widget(config_title)

                for cfg in self.yamls_by_game[game]:
                    player_name = cfg["name"]
                    items, locs = get_config_item_location_counts(game, cfg["yaml"])

                    # Player name as heading
                    name_label = MDLabel(
                        text=f"  [b]{player_name}[/b] ({cfg['filename']})",
                        markup=True,
                        size_hint_y=None,
                        height=dp(25),
                    )
                    self.info_layout.add_widget(name_label)

                    if items >= 0:
                        cfg_text = f"    Items: {items}, Locations: {locs}"
                    else:
                        cfg_text = f"    Items: {world_data['items']}, Locations: {world_data['locations']} (possible)"

                    cfg_label = MDLabel(text=cfg_text, size_hint_y=None, height=dp(25))
                    self.info_layout.add_widget(cfg_label)

    APWorldInfoApp().run()


def can_use_gui() -> bool:
    """Check if GUI can be used (display available and not in WSL with software rendering)."""
    import sys

    # Windows always has GUI available
    if sys.platform == "win32":
        return True

    # macOS always has GUI available
    if sys.platform == "darwin":
        return True

    # Linux: Check if display is available
    display = os.environ.get("DISPLAY")
    wayland = os.environ.get("WAYLAND_DISPLAY")
    if not display and not wayland:
        return False

    # Check for WSL with known OpenGL issues
    try:
        uname_release = os.uname().release.lower()
    except AttributeError:
        # os.uname() not available on Windows
        return True

    if "microsoft" in uname_release or "wsl" in uname_release:
        # Check if LIBGL_ALWAYS_SOFTWARE is set (software rendering)
        if os.environ.get("LIBGL_ALWAYS_SOFTWARE"):
            return False
        # Try to detect if we have proper GPU acceleration
        try:
            import subprocess

            result = subprocess.run(["glxinfo"], capture_output=True, text=True, timeout=5)
            if "softpipe" in result.stdout or "llvmpipe" in result.stdout:
                # Software rendering detected
                return False
        except Exception:
            pass  # glxinfo not available, try GUI anyway

    return True


def launch(*args) -> None:
    """Entry point for launcher."""
    parser = argparse.ArgumentParser(description="Display information about installed APWorlds.")
    parser.add_argument("--no-gui", action="store_true", help="Run in CLI mode instead of GUI")
    parser.add_argument("--gui", action="store_true", help="Force GUI mode even if display issues detected")
    parsed = parser.parse_args(args if args else None)

    if parsed.no_gui:
        print_world_info()
    elif parsed.gui or can_use_gui():
        try:
            run_gui()
        except Exception as e:
            logger.warning(f"GUI failed to start: {e}")
            logger.info("Falling back to CLI mode...")
            print_world_info()
    else:
        logger.info("GUI not available (no display or software rendering detected), using CLI mode.")
        print_world_info()


if __name__ == "__main__":
    Utils.init_logging("APWorldInfo")
    launch()
