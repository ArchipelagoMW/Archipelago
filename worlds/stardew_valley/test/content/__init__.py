import unittest
from typing import ClassVar, Tuple

from ...content import content_packs, ContentPack, StardewContent, unpack_content, StardewFeatures, feature

default_features = StardewFeatures(
    feature.booksanity.BooksanityDisabled(),
    feature.cropsanity.CropsanityDisabled(),
    feature.fishsanity.FishsanityNone(),
    feature.friendsanity.FriendsanityNone(),
    feature.skill_progression.SkillProgressionVanilla(),
)


class SVContentPackTestBase(unittest.TestCase):
    vanilla_packs: ClassVar[Tuple[ContentPack]] = (content_packs.pelican_town, content_packs.the_desert, content_packs.the_farm, content_packs.the_mines)
    mods: ClassVar[Tuple[str]] = ()

    content: ClassVar[StardewContent]

    @classmethod
    def setUpClass(cls) -> None:
        packs = cls.vanilla_packs + tuple(content_packs.by_mod[mod] for mod in cls.mods)
        cls.content = unpack_content(default_features, packs)
