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

            game_block = data["Kirby & The Amazing Mirror"]
            goal_weights = game_block["goal"]
            shard_weights = game_block["shards"]
            ability_weights = game_block["enemy_copy_ability_randomization"]

            assert "dark_mind" in goal_weights
            assert "100" not in goal_weights
            assert "debug" not in goal_weights

            assert "vanilla" in shard_weights
            assert "completely_random" in shard_weights
            assert "shuffle" not in shard_weights

            assert "vanilla" in ability_weights
            assert "shuffled" in ability_weights
            assert "completely_random" not in ability_weights

            assert "100% Save File" not in content
            assert "DEBUG: Testing-only goal" not in content
            assert "KirbyAM DeathLink uses native Kirby HP semantics" not in content

            assert "local_items" not in game_block
            assert "non_local_items" not in game_block
            assert "start_inventory" not in game_block
            assert "start_hints" not in game_block
            assert "start_location_hints" not in game_block
            assert "exclude_locations" not in game_block
            assert "priority_locations" not in game_block
            assert "item_links" not in game_block
            assert "plando_items" not in game_block
    finally:
        worlds.AutoWorld.AutoWorldRegister.world_types = old_world_types
