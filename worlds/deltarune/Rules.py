from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import CanReachLocation, CanReachRegion, Has
from worlds.deltarune.Options import (
    AnnoyingFarmingAsLogic,
    ChosenRoute,
    NoHitAsLogic,
    SpeedrunGlitchesAsLogic,
    UnlockCharacters,
    UnlockFunGangActions,
)
from worlds.deltarune.Items import ItemGroups, items, ItemIDs, glitched_item_name
from worlds.deltarune.Regions import Regions
from worlds.deltarune.Locations import LocationIDs, locations

if TYPE_CHECKING:
    from . import DeltaruneWorld

have_kris = Has(items[ItemIDs.kris]) | OptionFilter(UnlockCharacters, UnlockCharacters.option_true, operator="ne")
have_ralsei = Has(items[ItemIDs.ralsei]) | OptionFilter(UnlockCharacters, UnlockCharacters.option_false, operator="eq")
have_susie = Has(items[ItemIDs.susie]) | OptionFilter(UnlockCharacters, UnlockCharacters.option_false, operator="eq")
have_noelle = Has(items[ItemIDs.noelle]) | OptionFilter(UnlockCharacters, UnlockCharacters.option_false, operator="eq")

have_kris_or_susie = have_kris | have_susie
have_kris_or_ralsei = have_kris | have_ralsei
have_kris_susie_or_ralsei = have_kris | have_susie | have_ralsei
have_kris_susie_and_ralsei = have_kris & have_susie & have_ralsei
have_kris_or_noelle = have_kris | have_noelle
have_kris_and_susie = have_kris & have_susie
have_kris_and_ralsei = have_kris & have_ralsei
have_susie_or_ralsei = have_susie | have_ralsei

have_actions = Has(items[ItemIDs.s_r_n_actions]) | OptionFilter(UnlockFunGangActions, 0)

speedrun_glitch_logic = Has(glitched_item_name) | [
    OptionFilter(SpeedrunGlitchesAsLogic, SpeedrunGlitchesAsLogic.option_true)
]
nohit_logic = Has(glitched_item_name) | [OptionFilter(NoHitAsLogic, NoHitAsLogic.option_true)]
annoying_farming_logic = Has(glitched_item_name) | [
    OptionFilter(AnnoyingFarmingAsLogic, AnnoyingFarmingAsLogic.option_true)
]

def have_thornring(world: "DeltaruneWorld"):
    return Has(items[ItemIDs.thornring]) | Has(
        items[ItemIDs.progressive_noelle_weapons],
        world.get_weapon_progression_index(ItemGroups.noelle_weapons, ItemIDs.thornring),
    )


def can_snowgrave(world: "DeltaruneWorld"):
    return have_noelle & have_thornring(world)

### RECRUITMENT GENERIC LOGIC
can_recruit_with_violence_ralsei = have_ralsei
can_recruit_with_violence_susie = have_susie
can_recruit_with_violence_noelle = have_noelle
can_spam_spare = have_kris_susie_or_ralsei & annoying_farming_logic
can_spam_spare_kris_and_ralsei_only = have_kris_or_ralsei & annoying_farming_logic
can_act_spare_susie = have_susie & have_actions
can_act_spare_ralsei = have_ralsei & have_actions


### CHAPTER 1 RECRUITMENT
can_recruit_ruddin = have_kris | can_recruit_with_violence_ralsei
can_recruit_hathy = have_kris | can_recruit_with_violence_ralsei
can_recruit_jigsawry = (
    have_kris_and_ralsei
    | (CanReachRegion(Regions.ch1_card_castle) & (have_kris | can_recruit_with_violence_ralsei))
    | (CanReachRegion(Regions.ch1_forest) & have_kris_or_ralsei)
)
can_recruit_ponman = (
    have_kris_and_ralsei
    | (CanReachRegion(Regions.ch1_card_castle) & (have_kris | can_recruit_with_violence_ralsei))
    | (CanReachRegion(Regions.ch1_forest) & have_kris_or_ralsei)
)
can_recruit_rabbick = have_kris | can_recruit_with_violence_ralsei
can_recruit_bloxer = have_kris | can_recruit_with_violence_ralsei
can_recruit_head_hathy = have_kris | can_recruit_with_violence_ralsei
can_recruit_rudinn_ranger = have_kris | can_recruit_with_violence_ralsei

### CHAPTER 1 LOST
can_lose_chapter1 = have_kris_or_ralsei

### CHAPTER 2 RECRUITMENT

can_recruit_werewire = have_kris | can_act_spare_susie | have_ralsei | can_spam_spare
can_recruit_tasque = have_kris | can_act_spare_susie | can_recruit_with_violence_ralsei | can_spam_spare
can_recruit_virovirokun = have_kris | can_act_spare_susie | can_recruit_with_violence_ralsei | can_spam_spare
can_recruit_poppup = (
    have_kris
    | can_recruit_with_violence_noelle
    | can_act_spare_susie
    | can_recruit_with_violence_ralsei
    | can_spam_spare
)
can_recruit_ambuy_lance = (
    have_kris_and_susie
    | have_kris_and_ralsei
    | can_recruit_with_violence_noelle
    | can_act_spare_susie
    | can_recruit_with_violence_ralsei
    | can_spam_spare
)
can_recruit_maus = (
    have_kris
    | can_recruit_with_violence_noelle
    | can_act_spare_susie
    | can_recruit_with_violence_ralsei
    | can_spam_spare
)
can_recruit_swatchling = have_kris | can_act_spare_susie | can_act_spare_ralsei
can_recruit_tasque_manager = (
    have_kris
    | can_act_spare_susie
    | can_recruit_with_violence_ralsei
    | can_spam_spare
    | (
        have_kris_susie_or_ralsei
        & OptionFilter(
            ChosenRoute,
            [ChosenRoute.option_all_recruits, ChosenRoute.option_both_all_recruits_and_weird_route],
            operator="in",
        )
    )
)
can_recruit_mauswheel = have_kris | can_act_spare_susie
can_recruit_werewerewire = have_kris | can_act_spare_susie | can_recruit_with_violence_ralsei | can_spam_spare

### CHAPTER 2 LOST
can_lost_chapter2 = have_kris_susie_or_ralsei
can_lost_chapter2_with_noelle = have_noelle | (have_kris & Has(glitched_item_name))

### CHAPTER 3 RECRUITMENT
can_recruit_shadowguy = have_kris | can_act_spare_susie | can_recruit_with_violence_ralsei | can_spam_spare
can_recruit_pippins = have_kris | can_act_spare_susie | can_recruit_with_violence_ralsei | can_spam_spare
can_recruit_shuttah = have_kris_susie_or_ralsei
can_recruit_water_cooler = have_kris | can_act_spare_susie | can_recruit_with_violence_ralsei | can_spam_spare
can_recruit_zapper = have_kris | can_act_spare_susie | can_recruit_with_violence_ralsei | can_spam_spare

### CHAPTER 3 LOST
can_lost_chapter3 = have_kris_susie_or_ralsei

### CHAPTER 4 RECRUITMENT
can_recruit_guei = have_kris | can_act_spare_susie | can_recruit_with_violence_ralsei | can_spam_spare
can_recruit_balthizard = have_kris | can_act_spare_susie | can_recruit_with_violence_ralsei | can_spam_spare
can_recruit_bibliox = have_kris | can_act_spare_susie | can_recruit_with_violence_ralsei | can_spam_spare
can_recruit_mizzle = have_kris | can_act_spare_susie | can_act_spare_ralsei | can_spam_spare
can_recruit_miss_mizzle = have_kris | can_act_spare_susie | can_act_spare_ralsei | can_spam_spare
can_recruit_wicabel = have_kris | can_act_spare_susie | can_recruit_with_violence_ralsei | can_spam_spare
can_recruit_winglade = have_kris | can_act_spare_susie | can_recruit_with_violence_ralsei | can_spam_spare
can_recruit_organikk = have_kris | can_act_spare_susie | can_recruit_with_violence_ralsei | can_spam_spare

### CHAPTER 4 LOST
can_lost_chapter4 = have_kris_susie_or_ralsei

### CHAPTER 5 RECRUITMENT
can_recruit_floradinn = have_kris | can_recruit_with_violence_susie | can_recruit_with_violence_ralsei | can_spam_spare
can_recruit_sheary = have_kris | can_recruit_with_violence_susie | can_recruit_with_violence_ralsei | can_spam_spare
can_recruit_netskie = have_kris | can_recruit_with_violence_susie | can_recruit_with_violence_ralsei | can_spam_spare
can_recruit_shi = have_kris | can_recruit_with_violence_susie | can_recruit_with_violence_ralsei | can_spam_spare
can_recruit_leafling = have_kris | can_recruit_with_violence_susie | can_recruit_with_violence_ralsei | can_spam_spare
can_recruit_kawkaw = have_kris | can_recruit_with_violence_susie | can_recruit_with_violence_ralsei | can_spam_spare
can_recruit_shinobeetle = (
    have_kris | can_recruit_with_violence_susie | can_recruit_with_violence_ralsei | can_spam_spare
)
can_recruit_terakota = have_kris | can_recruit_with_violence_susie | can_recruit_with_violence_ralsei | can_spam_spare

### CHAPTER 4 LOST
can_lost_chapter5 = have_kris_susie_or_ralsei
