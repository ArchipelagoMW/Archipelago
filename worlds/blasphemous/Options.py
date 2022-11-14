from Options import Choice, Toggle, DefaultOnToggle, DeathLink


class CherubShuffle(DefaultOnToggle):
    """Shuffles Children of Moonlight into the item pool."""
    display_name = "Shuffle Children of Moonlight"


class LifeShuffle(DefaultOnToggle):
    """Shuffles life upgrades from the Lady of the Six Sorrows into the item pool."""
    display_name = "Shuffle Life Upgrades"


class FervourShuffle(DefaultOnToggle):
    """Shuffles fervour upgrades from the Oil of the Pilgrims into the item pool."""
    display_name = "Shuffle Fervour Upgrades"


class SwordShuffle(DefaultOnToggle):
    """Shuffles Mea Culpa upgrades from the Mea Culpa Altars into the item pool."""
    display_name = "Shuffle Mea Culpa Upgrades"


class BlessingShuffle(DefaultOnToggle):
    """Shuffles blessings from the Lake of Silent Pilgrims into the item pool."""
    display_name = "Shuffle Blessings"


class DungeonShuffle(DefaultOnToggle):
    """Shuffles rewards from completing Confessor Dungeons into the item pool."""
    display_name = "Shuffle Dungeon Rewards"


class TirsoShuffle(DefaultOnToggle):
    """Shuffles rewards from delivering herbs to Tirso into the item pool."""
    display_name = "Shuffle Tirso's Rewards"


class MiriamShuffle(DefaultOnToggle):
    """Shuffles the prayer given by Miriam into the item pool."""
    display_name = "Shuffle Miriram's Reward"


class RedentoShuffle(DefaultOnToggle):
    """Shuffles rewards from assisting Redento into the item pool."""
    display_name = "Shuffle Redento's Rewards"


class JocineroShuffle(DefaultOnToggle):
    """Shuffles rewards from rescuing 20 and 38 Children of Moonlight into the item pool."""
    display_name = "Shuffle Jocinero's Rewards"


class AltasgraciasShuffle(DefaultOnToggle):
    """Shuffles the reward given by Altasgracias and the item left behind by them into the item pool."""
    display_name = "Shuffle Altasgracias' Rewards"


class TentudiaShuffle(DefaultOnToggle):
    """Shuffles the rewards from delivering Tentudia's remains to Lvdovico into the item pool."""
    display_name = "Shuffle Lvdovico's Rewards"


class GeminoShuffle(DefaultOnToggle):
    """Shuffles the rewards from Gemino's quest and the hidden tomb into the item pool."""
    display_name = "Shuffle Gemino's Rewards"


class GuiltShuffle(DefaultOnToggle):
    """Shuffles the Weight of True Guilt into the item pool."""
    display_name = "Shuffle Immaculate Bead"


class OssuaryShuffle(DefaultOnToggle):
    """Shuffles the rewards from delivering bones to the Ossuary into the item pool."""
    display_name = "Shuffle Ossuary Rewards"


class BossShuffle(DefaultOnToggle):
    """Shuffles the Tears of Atonement from defeating bosses into the item pool."""
    display_name = "Shuffle Boss Tears"


class WoundShuffle(DefaultOnToggle):
    """Shuffles the Holy Wounds required to pass the Bridge of the Three Cavalries into the item pool."""
    display_name = "Shuffle Holy Wounds"


class MaskShuffle(DefaultOnToggle):
    """Shuffles the masks required to use the elevator in Archcathedral Rooftops into the item pool."""
    display_name = "Shuffle Masks"


class HerbShuffle(DefaultOnToggle):
    """Shuffles the herbs required for Tirso's quest into the item pool."""
    display_name = "Shuffle Herbs"


class ChurchShuffle(DefaultOnToggle):
    """Shuffles the rewards from donating 5,000 and 50,000 Tears of Atonement to the Church in Albero into the item pool."""
    display_name = "Shuffle Donation Rewards"


class ShopShuffle(DefaultOnToggle):
    """Shuffles the items sold in Candelaria's shops into the item pool."""
    display_name = "Shuffle Shop Items"


class ThornShuffle(DefaultOnToggle):
    """Shuffles the Thorn given by Deogracias and all Thorn upgrades into the item pool."""
    display_name = "Shuffle Thorn"


class CandleShuffle(DefaultOnToggle):
    """Shuffles the Beads of Wax and their upgrades into the item pool."""
    display_name = "Shuffle Candles"


blasphemous_options = {
    "cherub_shuffle" : CherubShuffle,
    "life_shuffle" : LifeShuffle,
    "fervour_shuffle" : FervourShuffle,
    "sword_shuffle" : SwordShuffle,
    "blessing_shuffle" : BlessingShuffle,
    "dungeon_shuffle" : DungeonShuffle,
    "tirso_shuffle" : TirsoShuffle,
    "miriam_shuffle" : MiriamShuffle,
    "redento_shuffle" : RedentoShuffle,
    "jocinero_shuffle" : JocineroShuffle,
    "altasgracias_shuffle" : AltasgraciasShuffle,
    "tentudia_shuffle" : TentudiaShuffle,
    "gemino_shuffle" : GeminoShuffle,
    "guilt_shuffle" : GuiltShuffle,
    "ossuary_shuffle" : OssuaryShuffle,
    "boss_shuffle" : BossShuffle,
    "wound_shuffle" : WoundShuffle,
    "mask_shuffle" : MaskShuffle,
    "herb_shuffle" : HerbShuffle,
    "church_shuffle" : ChurchShuffle,
    "shop_shuffle" : ShopShuffle,
    "thorn_shuffle" : ThornShuffle,
    "candle_shuffle" : CandleShuffle
}