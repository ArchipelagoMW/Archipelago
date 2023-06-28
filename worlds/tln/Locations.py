from BaseClasses import Location
import typing


class AdvData(typing.NamedTuple):
    id: typing.Optional[int]
    region: str


class TLNAdvancement(Location):
    game: str = "TLN"


tlnLocTable = {
    "Stage 0: Red Key": AdvData(210001, "Stage 00"),
    "Stage 0: HP Up": AdvData(210002, "Stage 00"),
    "Stage 0: MP Up": AdvData(210003, "Stage 00"),
    "Stage 0: Knife Up": AdvData(210004, "Stage 00"),
    "Stage 0: Time Up": AdvData(210005, "Stage 00"),
    "Stage 0: Auto Aim": AdvData(210038, "Stage 00"), # Forgot to add this and I don't want to redo the IDs lol
    "Stage 0: Sliding Knife Ability": AdvData(210006, "Stage 00"),
    "Stage 0: Stun Knife Spell": AdvData(210007, "Stage 00"),

    "Stage 1: Yellow Key": AdvData(210008, "Stage 01"),
    "Stage 1: HP Up": AdvData(210009, "Stage 01"),
    "Stage 1: MP Up": AdvData(210010, "Stage 01"),
    "Stage 1: Knife Up": AdvData(210011, "Stage 01"),
    "Stage 1: Time Up": AdvData(210012, "Stage 01"),
    "Stage 1: Double Jump Ability": AdvData(210013, "Stage 01"),
    "Stage 1: Chainsaw Spell": AdvData(210014, "Stage 01"),

    "Stage 2: Green Key": AdvData(210015, "Stage 02"),
    "Stage 2: HP Up": AdvData(210016, "Stage 02"),
    "Stage 2: MP Up": AdvData(210017, "Stage 02"),
    "Stage 2: Knife Up": AdvData(210018, "Stage 02"),
    "Stage 2: Time Up": AdvData(210019, "Stage 02"),
    "Stage 2: Grip Knife Ability": AdvData(210020, "Stage 02"),
    "Stage 2: Thousand Daggers Spell": AdvData(210021, "Stage 02"),

    "Stage 3: HP Up": AdvData(210022, "Stage 03"),
    "Stage 3: MP Up": AdvData(210023, "Stage 03"),
    "Stage 3: Knife Up": AdvData(210024, "Stage 03"),
    "Stage 3: Time Up": AdvData(210025, "Stage 03"),
    "Stage 4: Screw Knife Ability": AdvData(210026, "Stage 03"),
    "Stage 4: Shield Dagger Spell": AdvData(210027, "Stage 03"),

    "Stage 4: Blue Key": AdvData(210028, "Stage 04"),
    "Stage 4: Purple Key": AdvData(210029, "Stage 04"),
    "Stage 4: HP Up": AdvData(210030, "Stage 04"),
    "Stage 4: MP Up": AdvData(210031, "Stage 04"),
    "Stage 4: Knife Up": AdvData(210032, "Stage 04"),
    "Stage 4: Time Up": AdvData(210033, "Stage 04"),
    "Stage 4: Lost Holy Sword Spell": AdvData(210034, "Stage 04"),

    "Stage 5: Ice Magatama Ability": AdvData(210035, "Stage 05"),
    "Stage 5: Dash Ability": AdvData(210036, "Stage 05"),
    "Stage 5: Bound Knife Spell": AdvData(210037, "Stage 05"),
}
