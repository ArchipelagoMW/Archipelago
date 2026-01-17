from .Abilities import ActionAbility, ReactionAbility, SupportAbility, MovementAbility
from .Birthday import Month
from .Items import Items
from .RandomizedUnits import RandomizedUnit
from .SourceUnit import SourceUnit
from .SpriteSet import SpriteSet
from .Job import Job, UnlockedJob
from worlds.fftii.patchersuite.Unit import UnitGender


class RandomizedMapping:
    source_unit: SourceUnit
    destination_unit: type[RandomizedUnit] | RandomizedUnit
    battle_level: int = 0

    def __init__(self, source_unit: SourceUnit = None, destination_unit: RandomizedUnit | type[RandomizedUnit] = None):
        self.source_unit = source_unit
        self.destination_unit = destination_unit

    def to_json(self):
        return {
            "SourceUnit": self.source_unit.to_json(),
            "DestinationUnit": self.destination_unit.to_json()
        }

    @classmethod
    def from_json(cls, json_data):
        source_unit = SourceUnit(
            SpriteSet(json_data["SourceUnit"]["SpriteSet"]),
            Job(json_data["SourceUnit"]["Job"]),
            UnitGender(json_data["SourceUnit"]["Gender"])
        )
        destination_unit = RandomizedUnit()
        destination_unit.job = Job(json_data["DestinationUnit"]["Job"])
        destination_unit.sprite_set = SpriteSet(json_data["DestinationUnit"]["SpriteSet"])
        destination_unit.gender = UnitGender(json_data["DestinationUnit"]["Gender"])
        destination_unit.birthday_month = Month(json_data["DestinationUnit"]["BirthdayMonth"])
        destination_unit.birthday_day = json_data["DestinationUnit"]["BirthdayDay"]
        destination_unit.brave = json_data["DestinationUnit"]["Brave"]
        destination_unit.faith = json_data["DestinationUnit"]["Faith"]
        destination_unit.unlocked_job = UnlockedJob(json_data["DestinationUnit"]["UnlockedJob"])
        destination_unit.unlocked_job_level = json_data["DestinationUnit"]["UnlockedJobLevel"]
        destination_unit.primary = ActionAbility(json_data["DestinationUnit"]["Primary"])
        destination_unit.secondary = ActionAbility(json_data["DestinationUnit"]["Secondary"])
        destination_unit.reaction = ReactionAbility(json_data["DestinationUnit"]["Reaction"])
        destination_unit.support = SupportAbility(json_data["DestinationUnit"]["Support"])
        destination_unit.movement = MovementAbility(json_data["DestinationUnit"]["Movement"])
        destination_unit.right_hand = Items(json_data["DestinationUnit"]["RightHand"])
        destination_unit.left_hand = Items(json_data["DestinationUnit"]["LeftHand"])
        destination_unit.head = Items(json_data["DestinationUnit"]["Head"])
        destination_unit.body = Items(json_data["DestinationUnit"]["Body"])
        destination_unit.accessory = Items(json_data["DestinationUnit"]["Accessory"])
        return RandomizedMapping(source_unit, destination_unit)

    def __repr__(self):
        return f"{self.source_unit} -- {self.destination_unit}"