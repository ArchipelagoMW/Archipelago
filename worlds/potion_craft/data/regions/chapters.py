from rule_builder.rules import Has
from .. import RegionTypeEnum, ConnectionTypeEnum
from ..items import PotionEffectType


class ChapterRegions(RegionTypeEnum):
    CHAPTER_1 = ("Chapter 1",)
    CHAPTER_2 = ("Chapter 2",)
    CHAPTER_3 = ("Chapter 3",)
    CHAPTER_4 = ("Chapter 4",)
    CHAPTER_5 = ("Chapter 5",)
    CHAPTER_6 = ("Chapter 6",)
    CHAPTER_7 = ("Chapter 7",)
    CHAPTER_8 = ("Chapter 8",)
    CHAPTER_9 = ("Chapter 9",)
    CHAPTER_10 = ("Chapter 10",)

    CHAPTER_1_GOALS = ("Chapter 1 Goals",)
    CHAPTER_2_GOALS = ("Chapter 2 Goals",)
    CHAPTER_3_GOALS = ("Chapter 3 Goals",)
    CHAPTER_4_GOALS = ("Chapter 4 Goals",)
    CHAPTER_5_GOALS = ("Chapter 5 Goals",)
    CHAPTER_6_GOALS = ("Chapter 6 Goals",)
    CHAPTER_7_GOALS = ("Chapter 7 Goals",)
    CHAPTER_8_GOALS = ("Chapter 8 Goals",)
    CHAPTER_9_GOALS = ("Chapter 9 Goals",)
    CHAPTER_10_GOALS = ("Chapter 10 Goals",)

class ChapterConnections(ConnectionTypeEnum):
    GOALS_1 = ("Goals 1", ChapterRegions.CHAPTER_1, ChapterRegions.CHAPTER_1_GOALS)
    GOALS_2 = ("Goals 2", ChapterRegions.CHAPTER_2, ChapterRegions.CHAPTER_2_GOALS)
    GOALS_3 = ("Goals 3", ChapterRegions.CHAPTER_3, ChapterRegions.CHAPTER_3_GOALS)
    GOALS_4 = ("Goals 4", ChapterRegions.CHAPTER_4, ChapterRegions.CHAPTER_4_GOALS)
    GOALS_5 = ("Goals 5", ChapterRegions.CHAPTER_5, ChapterRegions.CHAPTER_5_GOALS)
    GOALS_6 = ("Goals 6", ChapterRegions.CHAPTER_6, ChapterRegions.CHAPTER_6_GOALS)
    GOALS_7 = ("Goals 7", ChapterRegions.CHAPTER_7, ChapterRegions.CHAPTER_7_GOALS)
    GOALS_8 = ("Goals 8", ChapterRegions.CHAPTER_8, ChapterRegions.CHAPTER_8_GOALS)
    GOALS_9 = ("Goals 9", ChapterRegions.CHAPTER_9, ChapterRegions.CHAPTER_9_GOALS)
    GOALS_10 = ("Goals 10", ChapterRegions.CHAPTER_10, ChapterRegions.CHAPTER_10_GOALS)

    CHAPTER_1_COMPLETE = ("Chapter 1 Complete", ChapterRegions.CHAPTER_1, ChapterRegions.CHAPTER_2,
                          Has(PotionEffectType.HEALING.value) & Has(PotionEffectType.FROST.value) & Has(PotionEffectType.POISON.value) & Has(PotionEffectType.FIRE.value))
    CHAPTER_2_COMPLETE = ("Chapter 2 Complete", ChapterRegions.CHAPTER_2, ChapterRegions.CHAPTER_3,
                          Has(PotionEffectType.EXPLOSION.value) & Has(PotionEffectType.WILD_GROWTH.value) & Has(
        PotionEffectType.STRENGTH.value) & Has(PotionEffectType.DEXTERITY.value) & Has(PotionEffectType.SWIFTNESS.value))
    CHAPTER_3_COMPLETE = ("Chapter 3 Complete", ChapterRegions.CHAPTER_3, ChapterRegions.CHAPTER_4)
    CHAPTER_4_COMPLETE = ("Chapter 4 Complete", ChapterRegions.CHAPTER_4, ChapterRegions.CHAPTER_5)
    CHAPTER_5_COMPLETE = ("Chapter 5 Complete", ChapterRegions.CHAPTER_5, ChapterRegions.CHAPTER_6)
    CHAPTER_6_COMPLETE = ("Chapter 6 Complete", ChapterRegions.CHAPTER_6, ChapterRegions.CHAPTER_7)
    CHAPTER_7_COMPLETE = ("Chapter 7 Complete", ChapterRegions.CHAPTER_7, ChapterRegions.CHAPTER_8)
    CHAPTER_8_COMPLETE = ("Chapter 8 Complete", ChapterRegions.CHAPTER_8, ChapterRegions.CHAPTER_9)
    CHAPTER_9_COMPLETE = ("Chapter 9 Complete", ChapterRegions.CHAPTER_9, ChapterRegions.CHAPTER_10)