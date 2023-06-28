from BaseClasses import Location
import typing


class AdvData(typing.NamedTuple):
    id: typing.Optional[int]
    region: str


class TLNAdvancement(Location):
    game: str = "TLN"


tlnLocTable = {
    "Stage 0: Red Key": AdvData(120001, "Stage 00"),
    "Stage 0: HP Up": AdvData(120002, "Stage 00"),
    "Stage 0: MP Up": AdvData(120003, "Stage 00"),
    "Stage 0: Knife Up": AdvData(120004, "Stage 00"),
    "Stage 0: Time Up": AdvData(120005, "Stage 00"),
    "Stage 0: Auto Aim": AdvData(120038, "Stage 00"), # Forgot to add this and I don't want to redo the IDs lol
    "Stage 0: Sliding Knife Ability": AdvData(120006, "Stage 00"),
    "Stage 0: Stun Knife Spell": AdvData(120007, "Stage 00"),

    "Stage 1: Yellow Key": AdvData(120008, "Stage 01"),
    "Stage 1: HP Up": AdvData(120009, "Stage 01"),
    "Stage 1: MP Up": AdvData(120010, "Stage 01"),
    "Stage 1: Knife Up": AdvData(120011, "Stage 01"),
    "Stage 1: Time Up": AdvData(120012, "Stage 01"),
    "Stage 1: Double Jump Ability": AdvData(120013, "Stage 01"),
    "Stage 1: Chainsaw Spell": AdvData(120014, "Stage 01"),

    "Stage 2: Green Key": AdvData(120015, "Stage 02"),
    "Stage 2: HP Up": AdvData(120016, "Stage 02"),
    "Stage 2: MP Up": AdvData(120017, "Stage 02"),
    "Stage 2: Knife Up": AdvData(120018, "Stage 02"),
    "Stage 2: Time Up": AdvData(120019, "Stage 02"),
    "Stage 2: Grip Knife Ability": AdvData(120020, "Stage 02"),
    "Stage 2: Thousand Daggers Spell": AdvData(120021, "Stage 02"),

    "Stage 3: HP Up": AdvData(120022, "Stage 03"),
    "Stage 3: MP Up": AdvData(120023, "Stage 03"),
    "Stage 3: Knife Up": AdvData(120024, "Stage 03"),
    "Stage 3: Time Up": AdvData(120025, "Stage 03"),
    "Stage 4: Screw Knife Ability": AdvData(120026, "Stage 03"),
    "Stage 4: Shield Dagger Spell": AdvData(120027, "Stage 03"),

    "Stage 4: Blue Key": AdvData(120028, "Stage 04"),
    "Stage 4: Purple Key": AdvData(120029, "Stage 04"),
    "Stage 4: HP Up": AdvData(120030, "Stage 04"),
    "Stage 4: MP Up": AdvData(120031, "Stage 04"),
    "Stage 4: Knife Up": AdvData(120032, "Stage 04"),
    "Stage 4: Time Up": AdvData(120033, "Stage 04"),
    "Stage 4: Lost Holy Sword Spell": AdvData(120034, "Stage 04"),

    "Stage 5: Ice Magatama Ability": AdvData(120035, "Stage 05"),
    "Stage 5: Dash Ability": AdvData(120036, "Stage 05"),
    "Stage 5: Bound Knife Spell": AdvData(120037, "Stage 05"),
}
