from ... import options
from ...mods.mod_data import ModNames
from ..bases import SVTestBase


class TestNoGingerIslandCraftingRecipesAreRequired(SVTestBase):
    options = {  # noqa: RUF012
        options.Goal.internal_name: options.Goal.option_craft_master,
        options.Craftsanity.internal_name: options.Craftsanity.option_all,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true,
        options.Mods.internal_name: frozenset(ModNames.enabled_mods_except_invalid_combinations()),
    }


class TestNoGingerIslandCookingRecipesAreRequired(SVTestBase):
    options = {  # noqa: RUF012
        options.Goal.internal_name: options.Goal.option_gourmet_chef,
        options.Cooksanity.internal_name: options.Cooksanity.option_all,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true,
        options.Mods.internal_name: frozenset(ModNames.enabled_mods_except_invalid_combinations()),
    }
