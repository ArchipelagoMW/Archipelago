from dataclasses import dataclass

from .game_item import Source


@dataclass(frozen=True, kw_only=True)
class RecipeSource(Source):

    def __repr__(self):
        return f"RecipeSource"


@dataclass(frozen=True, kw_only=True)
class StarterSource(RecipeSource):

    def __repr__(self):
        return f"StarterSource"


@dataclass(frozen=True, kw_only=True)
class ArchipelagoSource(RecipeSource):
    ap_items: tuple[str, ...]

    def __repr__(self):
        return f"ArchipelagoSource {self.ap_items}"


@dataclass(frozen=True, kw_only=True)
class LogicSource(RecipeSource):
    logic_rule: str

    def __repr__(self):
        return f"LogicSource {self.logic_rule}"


@dataclass(frozen=True, kw_only=True)
class QueenOfSauceSource(RecipeSource):
    year: int
    season: str
    day: int

    def __repr__(self):
        return f"QueenOfSauceSource at year {self.year} {self.season} {self.day}"


@dataclass(frozen=True, kw_only=True)
class QuestSource(RecipeSource):
    quest: str

    def __repr__(self):
        return f"QuestSource at quest {self.quest}"


@dataclass(frozen=True, kw_only=True)
class FriendshipSource(RecipeSource):
    friend: str
    hearts: int

    def __repr__(self):
        return f"FriendshipSource at {self.friend} {self.hearts} <3"


@dataclass(frozen=True, kw_only=True)
class CutsceneSource(FriendshipSource):
    region: str

    def __repr__(self):
        return f"CutsceneSource at {self.region}"


@dataclass(frozen=True, kw_only=True)
class SkillSource(RecipeSource):
    skill: str
    level: int

    def __repr__(self):
        return f"SkillSource at level {self.level} {self.skill}"


@dataclass(frozen=True, kw_only=True)
class SkillCraftsanitySource(SkillSource):

    def __repr__(self):
        return f"SkillCraftsanitySource at level {self.level} {self.skill}"


@dataclass(frozen=True, kw_only=True)
class MasterySource(RecipeSource):
    skill: str

    def __repr__(self):
        return f"MasterySource {self.skill}"


@dataclass(frozen=True, kw_only=True)
class SpecialOrderSource(RecipeSource):
    special_order: str

    def __repr__(self):
        return f"SpecialOrderSource from {self.special_order}"
