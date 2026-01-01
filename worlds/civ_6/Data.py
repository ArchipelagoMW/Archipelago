from typing import Dict, List

from .ItemData import (
    CivVIBoostData,
    CivicPrereqData,
    ExistingItemData,
    GoodyHutRewardData,
    NewItemData,
    TechPrereqData,
)


def get_boosts_data() -> List[CivVIBoostData]:
    from .data.boosts import boosts

    return boosts


def get_era_required_items_data() -> Dict[str, List[str]]:
    from .data.era_required_items import era_required_items

    return era_required_items


def get_existing_civics_data() -> List[ExistingItemData]:
    from .data.existing_civics import existing_civics

    return existing_civics


def get_existing_techs_data() -> List[ExistingItemData]:
    from .data.existing_tech import existing_tech

    return existing_tech


def get_goody_hut_rewards_data() -> List[GoodyHutRewardData]:
    from .data.goody_hut_rewards import reward_data

    return reward_data


def get_new_civic_prereqs_data() -> List[CivicPrereqData]:
    from .data.new_civic_prereqs import new_civic_prereqs

    return new_civic_prereqs


def get_new_civics_data() -> List[NewItemData]:
    from .data.new_civics import new_civics

    return new_civics


def get_new_tech_prereqs_data() -> List[TechPrereqData]:
    from .data.new_tech_prereqs import new_tech_prereqs

    return new_tech_prereqs


def get_new_techs_data() -> List[NewItemData]:
    from .data.new_tech import new_tech

    return new_tech


def get_progressive_districts_data() -> Dict[str, List[str]]:
    from .data.progressive_districts import progressive_districts

    return progressive_districts
