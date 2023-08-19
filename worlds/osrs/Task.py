import typing


class SkillRequirement:
    skill: str
    level: int


class RegionAccessRequirement:
    region: str


class ItemRequirement:
    item_name: str
    count: int = 1


class OSRSTask:
    task_name: str
    task_category: str
    location_id: int
    regions_required: typing.List[RegionAccessRequirement] = []
    skills_required: typing.List[SkillRequirement] = []
    items_required: typing.List[ItemRequirement] = []

