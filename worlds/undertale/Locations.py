from BaseClasses import Location
import typing


class AdvData(typing.NamedTuple):
    id: typing.Optional[int]
    region: str


class UndertaleAdvancement(Location):
    game: str = "Undertale"

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.event = not address


advancement_table = {
    "Snowman": AdvData(67000, 'Snowdin Forest'),
    "Nicecream Snowdin": AdvData(67001, 'Snowdin Forest'),
    "Nicecream Waterfall": AdvData(67002, 'Waterfall'),
    "Nicecream Punch Card": AdvData(67003, 'Waterfall'),
    "Quiche Bench": AdvData(67004, 'Waterfall'),
    "Tutu Hidden": AdvData(67005, 'Waterfall'),
    "Card Reward": AdvData(67006, 'Waterfall'),
    "Grass Shoes": AdvData(67007, 'Waterfall'),
    "Noodles Fridge": AdvData(67008, 'Hotland'),
    "Pan Hidden": AdvData(67009, 'Hotland'),
    "Apron Hidden": AdvData(67010, 'Hotland'),
    "Trash Burger": AdvData(67011, 'Waterfall'),
    "Present Knife": AdvData(67012, 'New Home'),
    "Present Locket": AdvData(67013, 'New Home'),
    "Candy 1": AdvData(67014, 'Ruins'),
    "Candy 2": AdvData(67015, 'Ruins'),
    "Candy 3": AdvData(67016, 'Ruins'),
    "Candy 4": AdvData(67017, 'Ruins'),
    "Donut Sale": AdvData(67018, 'Ruins'),
    "Cider Sale": AdvData(67019, 'Ruins'),
    "Ribbon Cracks": AdvData(67020, 'Ruins'),
    "Toy Knife Edge": AdvData(67021, 'Ruins'),
    "B.Scotch Pie Given": AdvData(67022, 'Ruins'),
    "Astro 1": AdvData(67023, 'Waterfall'),
    "Astro 2": AdvData(67024, 'Waterfall'),
    "Dog Sale 1": AdvData(67026, 'Hotland'),
    "Cat Sale": AdvData(67027, 'Hotland'),
    "Dog Sale 2": AdvData(67028, 'Hotland'),
    "Dog Sale 3": AdvData(67029, 'Hotland'),
    "Dog Sale 4": AdvData(67030, 'Hotland'),
    "Chisps Machine": AdvData(67031, 'True Lab'),
    "Hush Trade": AdvData(67032, 'Hotland'),
    "Letter Quest": AdvData(67033, 'Snowdin Town'),
    "Bunny 1": AdvData(67034, 'Snowdin Town'),
    "Bunny 2": AdvData(67035, 'Snowdin Town'),
    "Bunny 3": AdvData(67036, 'Snowdin Town'),
    "Bunny 4": AdvData(67037, 'Snowdin Town'),
    "Gerson 1": AdvData(67038, 'Waterfall'),
    "Gerson 2": AdvData(67039, 'Waterfall'),
    "Gerson 3": AdvData(67040, 'Waterfall'),
    "Gerson 4": AdvData(67041, 'Waterfall'),
    "Bratty Catty 1": AdvData(67042, 'Hotland'),
    "Bratty Catty 2": AdvData(67043, 'Hotland'),
    "Bratty Catty 3": AdvData(67044, 'Hotland'),
    "Bratty Catty 4": AdvData(67045, 'Hotland'),
    "Burgerpants 1": AdvData(67046, 'Hotland'),
    "Burgerpants 2": AdvData(67047, 'Hotland'),
    "Burgerpants 3": AdvData(67048, 'Hotland'),
    "Burgerpants 4": AdvData(67049, 'Hotland'),
    "TemmieShop 1": AdvData(67050, 'Waterfall'),
    "TemmieShop 2": AdvData(67051, 'Waterfall'),
    "TemmieShop 3": AdvData(67052, 'Waterfall'),
    "TemmieShop 4": AdvData(67053, 'Waterfall'),
}

exclusion_table = {
    "pacifist": {
    },
    "neutral": {
        "Letter Quest",
        "Dog Sale 1",
        "Cat Sale",
        "Dog Sale 2",
        "Dog Sale 3",
        "Dog Sale 4",
        "Chisps Machine",
        "Hush Trade",
    },
    "genocide": {
        "Letter Quest",
        "Dog Sale 1",
        "Cat Sale",
        "Dog Sale 2",
        "Dog Sale 3",
        "Dog Sale 4",
        "Chisps Machine",
        "Nicecream Snowdin",
        "Nicecream Waterfall",
        "Nicecream Punch Card",
        "Card Reward",
        "Apron Hidden",
        "Hush Trade",
    },
}

events_table = {
}

lookup_id_to_name: typing.Dict[int, str] = {data.id: item_name for item_name, data in advancement_table.items() if data.id}