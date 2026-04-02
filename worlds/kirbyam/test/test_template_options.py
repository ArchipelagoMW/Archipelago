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


def test_goal_from_any_coerces_legacy_values() -> None:
    """Legacy goal values (removed in v0.0.12) must coerce to Dark Mind, not raise."""
    from worlds.kirbyam.options import Goal

    # Legacy integer option values (option_100=1, option_debug=2)
    assert Goal.from_any(1).value == Goal.option_dark_mind
    assert Goal.from_any(2).value == Goal.option_dark_mind
    # Unquoted YAML `100:` is parsed as int(100) by ruamel/pyyaml; must also coerce
    assert Goal.from_any(100).value == Goal.option_dark_mind

    # Legacy string template keys
    assert Goal.from_any("1").value == Goal.option_dark_mind
    assert Goal.from_any("2").value == Goal.option_dark_mind
    assert Goal.from_any("100").value == Goal.option_dark_mind
    assert Goal.from_any("debug").value == Goal.option_dark_mind
    assert Goal.from_any("DEBUG").value == Goal.option_dark_mind

    # Current valid value still works
    assert Goal.from_any("dark_mind").value == Goal.option_dark_mind
    assert Goal.from_any(0).value == Goal.option_dark_mind
