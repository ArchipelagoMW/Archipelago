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
    skills_required: typing.List[SkillRequirement] = []
    regions_required: typing.List[RegionAccessRequirement] = []
    items_required: typing.List[ItemRequirement] = []

