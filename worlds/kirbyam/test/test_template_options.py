from pathlib import Path
from tempfile import TemporaryDirectory

from Utils import parse_yaml


def test_kirbyam_template_surface_options_visibility() -> None:
    import worlds.AutoWorld
    from Options import generate_yaml_templates
    from worlds.AutoWorld import AutoWorldRegister
    from worlds.kirbyam import KirbyAmWorld

    old_world_types = AutoWorldRegister.world_types
    try:
        AutoWorldRegister.world_types = {KirbyAmWorld.game: KirbyAmWorld}

        with TemporaryDirectory("archipelago_kirbyam_template") as temp_dir:
            generate_yaml_templates(temp_dir)

            generated_file = Path(temp_dir) / "Kirby & The Amazing Mirror.yaml"
            assert generated_file.exists()

            with generated_file.open(encoding="utf-8") as f:
                content = f.read()
                data = parse_yaml(content)

            requires_game_version = data["requires"]["game"][KirbyAmWorld.game]
            game_block = data["Kirby & The Amazing Mirror"]
            goal_weights = game_block["goal"]
            shard_weights = game_block["shards"]
            ability_weights = game_block["ability_randomization_mode"]
            assert "starting_kirby_color" in game_block, (
                "'starting_kirby_color' option is missing from the generated template"
            )
            color_weights = game_block["starting_kirby_color"]

            assert "dark_mind" in goal_weights
            assert "100" not in goal_weights
            assert "debug" not in goal_weights

            assert "vanilla" in shard_weights
            assert "completely_random" in shard_weights
            assert "shuffle" not in shard_weights

            assert "off" in ability_weights
            assert "shuffled" in ability_weights
            assert "completely_random" not in ability_weights
            assert "no_extra_lives" in game_block
            assert "ability_randomization_no_ability_weight" in game_block
            assert "starting_kirby_color" in game_block
            assert "pink" in color_weights
            assert "random_color" in color_weights

            assert "100% Save File" not in content
            assert "DEBUG: Testing-only goal" not in content
            assert "KirbyAM DeathLink uses native Kirby HP semantics" not in content
            assert "Supported color names" in content
            assert "Non-Pink colors become visible" in content
            assert requires_game_version == KirbyAmWorld.world_version.as_simple_string()

            assert "local_items" in game_block
            assert "non_local_items" in game_block
            assert "start_inventory" in game_block
            assert "start_hints" in game_block
            assert "start_location_hints" in game_block
            assert "exclude_locations" in game_block
            assert "priority_locations" in game_block
            assert "item_links" in game_block
            assert "plando_items" in game_block
    finally:
        worlds.AutoWorld.AutoWorldRegister.world_types = old_world_types

