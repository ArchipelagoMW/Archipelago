from .. import SVTestBase
from ... import options


class TestNoGingerIslandCraftingRecipesAreRequired(SVTestBase):
    options = {
        options.Goal.internal_name: options.Goal.option_craft_master,
        options.Craftsanity.internal_name: options.Craftsanity.option_all,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true,
        options.Mods.internal_name: frozenset(options.Mods.valid_keys)
    }

    @property
    def run_default_tests(self) -> bool:
        return True
