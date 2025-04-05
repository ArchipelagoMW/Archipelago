from dataclasses import dataclass
import os
import io
from typing import TYPE_CHECKING, Dict, List, Optional, cast
import zipfile
from BaseClasses import Location
from worlds.Files import APContainer, AutoPatchRegister

from .Enum import CivVICheckType
from .Locations import CivVILocation, CivVILocationData

if TYPE_CHECKING:
    from . import CivVIWorld


# Python fstrings don't allow backslashes, so we use this workaround
nl = "\n"
tab = "\t"
apo = "\'"


@dataclass
class CivTreeItem:
    name: str
    cost: int
    ui_tree_row: int


class CivVIContainer(APContainer, metaclass=AutoPatchRegister):
    """
    Responsible for generating the dynamic mod files for the Civ VI multiworld
    """
    game: Optional[str] = "Civilization VI"
    patch_file_ending = ".apcivvi"

    def __init__(self, patch_data: Dict[str, str] | io.BytesIO, base_path: str = "", output_directory: str = "",
                 player: Optional[int] = None, player_name: str = "", server: str = ""):
        if isinstance(patch_data, io.BytesIO):
            super().__init__(patch_data, player, player_name, server)
        else:
            self.patch_data = patch_data
            self.file_path = base_path
            container_path = os.path.join(output_directory, base_path + ".apcivvi")
            super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        for filename, yml in self.patch_data.items():
            opened_zipfile.writestr(filename, yml)
        super().write_contents(opened_zipfile)

def sanitize_value(value: str) -> str:
  """Removes values that can cause issues in XML"""
  return value.replace('"', "'").replace('&', 'and')


def get_cost(world: 'CivVIWorld', location: CivVILocationData) -> int:
    """
    Returns the cost of the item based on the game options
    """
    # Research cost is between 50 and 150 where 100 equals the default cost
    multiplier = world.options.research_cost_multiplier / 100
    return int(world.location_table[location.name].cost * multiplier)


def get_formatted_player_name(world: 'CivVIWorld', player: int) -> str:
    """
    Returns the name of the player in the world
    """
    if player != world.player:
        return sanitize_value(f"{world.multiworld.player_name[player]}{apo}s")
    return "Your"


def get_advisor_type(world: 'CivVIWorld', location: Location) -> str:
    if world.options.advisor_show_progression_items and location.item and location.item.advancement:
        return "ADVISOR_PROGRESSIVE"
    return "ADVISOR_GENERIC"


def generate_new_items(world: 'CivVIWorld') -> str:
    """
    Generates the XML for the new techs/civics as well as the blockers used to prevent players from researching their own items
    """
    locations: List[CivVILocation] = cast(List[CivVILocation], world.multiworld.get_filled_locations(world.player))
    techs = [location for location in locations if location.location_type ==
             CivVICheckType.TECH]
    civics = [location for location in locations if location.location_type ==
              CivVICheckType.CIVIC]

    boost_techs = []
    boost_civics = []

    if world.options.boostsanity:
        boost_techs = [location for location in locations if location.location_type == CivVICheckType.BOOST and location.name.split("_")[1] == "TECH"]
        boost_civics = [location for location in locations if location.location_type == CivVICheckType.BOOST and location.name.split("_")[1] == "CIVIC"]
        techs += boost_techs
        civics += boost_civics

    return f"""<?xml version="1.0" encoding="utf-8"?>
<GameInfo>
  <Types>
    <Row Type="TECH_BLOCKER" Kind="KIND_TECH" />
    <Row Type="CIVIC_BLOCKER" Kind="KIND_CIVIC" />
  {"".join([f'{tab}<Row Type="{tech.name}" Kind="KIND_TECH" />{nl}' for
           tech in techs])}
  {"".join([f'{tab}<Row Type="{civic.name}" Kind="KIND_CIVIC" />{nl}' for
            civic in civics])}
  </Types>
  <Technologies>
      <Row TechnologyType="TECH_BLOCKER" Name="TECH_BLOCKER" EraType="ERA_ANCIENT" UITreeRow="0" Cost="99999" AdvisorType="ADVISOR_GENERIC" Description="Archipelago Tech created to prevent players from researching their own tech. If you can read this, then congrats you have reached the end of your tree before beating the game!"/>
{"".join([f'{tab}<Row TechnologyType="{location.name}" '
                f'Name="{get_formatted_player_name(world, location.item.player)} '
                f'{sanitize_value(location.item.name)}" '
                f'EraType="{world.location_table[location.name].era_type}" '
                f'UITreeRow="{world.location_table[location.name].uiTreeRow}" '
                f'Cost="{get_cost(world, world.location_table[location.name])}" '
                f'Description="{location.name}" '
                f'AdvisorType="{get_advisor_type(world, location)}"'
                f'/>{nl}'
                for location in techs if location.item])}
  </Technologies>
  <TechnologyPrereqs>
  {"".join([f'{tab}<Row Technology="{location.name}" PrereqTech="TECH_BLOCKER" />{nl}' for location in boost_techs])}
  </TechnologyPrereqs>
  <Civics>
      <Row CivicType="CIVIC_BLOCKER" Name="CIVIC_BLOCKER" EraType="ERA_ANCIENT" UITreeRow="0" Cost="99999" AdvisorType="ADVISOR_GENERIC" Description="Archipelago Civic created to prevent players from researching their own civics. If you can read this, then congrats you have reached the end of your tree before beating the game!"/>
{"".join([f'{tab}<Row CivicType="{location.name}" '
                    f'Name="{get_formatted_player_name(world, location.item.player)} '
                    f'{sanitize_value(location.item.name)}" '
                    f'EraType="{world.location_table[location.name].era_type}" '
                    f'UITreeRow="{world.location_table[location.name].uiTreeRow}" '
                    f'Cost="{get_cost(world, world.location_table[location.name])}" '
                    f'Description="{location.name}" '
                    f'AdvisorType="{get_advisor_type(world, location)}"'
                    f'/>{nl}'
                    for location in civics if location.item])}
  </Civics>
  <CivicPrereqs>
  {"".join([f'{tab}<Row Civic="{location.name}" PrereqCivic="CIVIC_BLOCKER" />{nl}' for location in boost_civics])}
  </CivicPrereqs>

  <Civics_XP2>
    {"".join([f'{tab}<Row CivicType="{location.name}" HiddenUntilPrereqComplete="true" RandomPrereqs="false"/>{nl}' for location in civics if world.options.hide_item_names])}
  </Civics_XP2>

  <Technologies_XP2>
    {"".join([f'{tab}<Row TechnologyType="{location.name}" HiddenUntilPrereqComplete="true" RandomPrereqs="false"/>{nl}' for location in techs if world.options.hide_item_names])}
  </Technologies_XP2>

</GameInfo>
    """


def generate_setup_file(world: 'CivVIWorld') -> str:
    """
    Generates the Lua for the setup file. This sets initial variables and state that affect gameplay around Progressive Eras
    """
    setup = "-- Setup"
    if world.options.progression_style == "eras_and_districts":
        setup += f"""
    -- Init Progressive Era Value if it hasn't been set already
    if Game.GetProperty("MaxAllowedEra") == nil then
      print("Setting MaxAllowedEra to 0")
      Game.SetProperty("MaxAllowedEra", 0)
    end
    """

    if world.options.boostsanity:
        setup += f"""
    -- Init Boosts
    if Game.GetProperty("BoostsAsChecks") == nil then
      print("Setting Boosts As Checks to True")
      Game.SetProperty("BoostsAsChecks", true)
    end
    """
    return setup


def generate_goody_hut_sql(world: 'CivVIWorld') -> str:
    """
    Generates the SQL for the goody huts or an empty string if they are disabled since the mod expects the file to be there
    """

    if world.options.shuffle_goody_hut_rewards:
        return f"""
        UPDATE GoodyHutSubTypes SET Description = NULL WHERE GoodyHut NOT IN ('METEOR_GOODIES', 'GOODYHUT_SAILOR_WONDROUS', 'DUMMY_GOODY_BUILDIER') AND Weight > 0;

INSERT INTO Modifiers
                (ModifierId, ModifierType, RunOnce, Permanent, SubjectRequirementSetId)
SELECT ModifierID||'_AI', ModifierType, RunOnce, Permanent, 'PLAYER_IS_AI'
FROM Modifiers
WHERE EXISTS (
        SELECT ModifierId
        FROM GoodyHutSubTypes
        WHERE Modifiers.ModifierId = GoodyHutSubTypes.ModifierId AND GoodyHutSubTypes.GoodyHut NOT IN ('METEOR_GOODIES', 'GOODYHUT_SAILOR_WONDROUS', 'DUMMY_GOODY_BUILDIER') AND GoodyHutSubTypes.Weight > 0);

INSERT INTO ModifierArguments
                (ModifierId, Name, Type, Value)
SELECT ModifierID||'_AI', Name, Type, Value
FROM ModifierArguments
WHERE EXISTS (
        SELECT ModifierId
        FROM GoodyHutSubTypes
        WHERE ModifierArguments.ModifierId = GoodyHutSubTypes.ModifierId AND GoodyHutSubTypes.GoodyHut NOT IN ('METEOR_GOODIES', 'GOODYHUT_SAILOR_WONDROUS', 'DUMMY_GOODY_BUILDIER') AND GoodyHutSubTypes.Weight > 0);

UPDATE GoodyHutSubTypes
SET ModifierID = ModifierID||'_AI'
WHERE GoodyHut NOT IN ('METEOR_GOODIES', 'GOODYHUT_SAILOR_WONDROUS', 'DUMMY_GOODY_BUILDIER') AND Weight > 0;

      """
    return "-- Goody Huts are disabled, no changes needed"


def generate_update_boosts_sql(world: 'CivVIWorld') -> str:
    """
    Generates the SQL for existing boosts in boostsanity or an empty string if they are disabled since the mod expects the file to be there
    """

    if world.options.boostsanity:
        return f"""
UPDATE Boosts
SET TechnologyType = 'BOOST_' || TechnologyType
WHERE TechnologyType IS NOT NULL;
UPDATE Boosts
SET CivicType = 'BOOST_' || CivicType
WHERE CivicType IS NOT NULL AND CivicType NOT IN ('CIVIC_CORPORATE_LIBERTARIANISM', 'CIVIC_DIGITAL_DEMOCRACY', 'CIVIC_SYNTHETIC_TECHNOCRACY', 'CIVIC_NEAR_FUTURE_GOVERNANCE');
        """
    return "-- Boostsanity is disabled, no changes needed"
