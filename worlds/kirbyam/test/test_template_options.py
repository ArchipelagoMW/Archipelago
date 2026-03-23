from pathlib import Path
from tempfile import TemporaryDirectory

from Utils import parse_yaml


def test_kirbyam_template_hides_non_shipping_goal_choices() -> None:
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

            assert "dark_mind" in goal_weights
            assert "100" not in goal_weights
            assert "debug" not in goal_weights
    finally:
        worlds.AutoWorld.AutoWorldRegister.world_types = old_world_types
