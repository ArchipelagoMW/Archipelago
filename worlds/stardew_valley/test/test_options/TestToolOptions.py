import itertools
from collections import Counter

from BaseClasses import ItemClassification
from ...options import ToolProgression, StartWithout
from ...strings.tool_names import ToolMaterial, Tool, APTool
from ...test.bases import SVTestBase

TOOLS = {"Hoe", "Pickaxe", "Axe", "Watering Can", "Trash Can", "Fishing Rod"}


class TestToolProgression(SVTestBase):
    options = {
        ToolProgression.internal_name: ToolProgression.option_progressive,
        StartWithout.internal_name: StartWithout.preset_none,
    }

    def test_given_progressive_when_generate_then_tool_upgrades_are_locations(self):
        locations = set(self.get_real_location_names())
        for material, tool in itertools.product(ToolMaterial.tiers.values(),
                                                [Tool.hoe, Tool.pickaxe, Tool.axe, Tool.watering_can, Tool.trash_can]):
            if material == ToolMaterial.basic:
                continue
            self.assertIn(f"{material} {tool} Upgrade", locations)
        self.assertIn("Purchase Training Rod", locations)
        self.assertIn("Bamboo Pole Cutscene", locations)
        self.assertIn("Purchase Fiberglass Rod", locations)
        self.assertIn("Purchase Iridium Rod", locations)

    def test_given_progressive_when_generate_then_last_trash_can_is_classified_differently(self):
        trash_cans = self.get_items_by_name(APTool.trash_can)
        progressive_count = sum([1 for item in trash_cans if item.classification == ItemClassification.progression])
        special_count = sum([1 for item in trash_cans if item.classification == ItemClassification.useful])

        self.assertEqual(3, progressive_count)
        self.assertEqual(1, special_count)

    def test_given_progressive_when_generate_then_last_trash_can_changes_classification_post_fill(self):
        trash_can, post_fill_classification = next((classification_to_update
                                                    for classification_to_update in self.world.classifications_to_override_post_fill
                                                    if classification_to_update[0].name == APTool.trash_can),
                                                   (None, None))

        self.assertEqual(post_fill_classification, ItemClassification.progression_skip_balancing)
        self.assertEqual(Counter(), trash_can.events_to_collect)
