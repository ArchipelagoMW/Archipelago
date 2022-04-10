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
    "Snowman": AdvData(79000, 'Snowdin Forest'),
    "Nicecream Snowdin": AdvData(79001, 'Snowdin Forest'),
    "Nicecream Waterfall": AdvData(79002, 'Waterfall'),
    "Nicecream Punch Card": AdvData(79003, 'Waterfall'),
    "Quiche Bench": AdvData(79004, 'Waterfall'),
    "Tutu Hidden": AdvData(79005, 'Waterfall'),
    "Card Reward": AdvData(79006, 'Waterfall'),
    "Grass Shoes": AdvData(79007, 'Waterfall'),
    "Noodles Fridge": AdvData(79008, 'Hotland'),
    "Pan Hidden": AdvData(79009, 'Hotland'),
    "Apron Hidden": AdvData(79010, 'Hotland'),
    "Trash Burger": AdvData(79011, 'Core'),
    "Present Knife": AdvData(79012, 'New Home'),
    "Present Locket": AdvData(79013, 'New Home'),
    "Candy 1": AdvData(79014, 'Ruins'),
    "Candy 2": AdvData(79015, 'Ruins'),
    "Candy 3": AdvData(79016, 'Ruins'),
    "Candy 4": AdvData(79017, 'Ruins'),
    "Donut Sale": AdvData(79018, 'Ruins'),
    "Cider Sale": AdvData(79019, 'Ruins'),
    "Ribbon Cracks": AdvData(79020, 'Ruins'),
    "Toy Knife Edge": AdvData(79021, 'Ruins'),
    "B.Scotch Pie Given": AdvData(79022, 'Ruins'),
    "Astro 1": AdvData(79023, 'Waterfall'),
    "Astro 2": AdvData(79024, 'Waterfall'),
    "Dog Sale 1": AdvData(79026, 'Hotland'),
    "Cat Sale": AdvData(79027, 'Hotland'),
    "Dog Sale 2": AdvData(79028, 'Hotland'),
    "Dog Sale 3": AdvData(79029, 'Hotland'),
    "Dog Sale 4": AdvData(79030, 'Hotland'),
    "Chisps Machine": AdvData(79031, 'True Lab'),
    "Hush Trade": AdvData(79032, 'Hotland'),
    "Letter Quest": AdvData(79033, 'Snowdin Town'),
    "Bunny 1": AdvData(79034, 'Snowdin Town'),
    "Bunny 2": AdvData(79035, 'Snowdin Town'),
    "Bunny 3": AdvData(79036, 'Snowdin Town'),
    "Bunny 4": AdvData(79037, 'Snowdin Town'),
    "Gerson 1": AdvData(79038, 'Waterfall'),
    "Gerson 2": AdvData(79039, 'Waterfall'),
    "Gerson 3": AdvData(79040, 'Waterfall'),
    "Gerson 4": AdvData(79041, 'Waterfall'),
    "Bratty Catty 1": AdvData(79042, 'Hotland'),
    "Bratty Catty 2": AdvData(79043, 'Hotland'),
    "Bratty Catty 3": AdvData(79044, 'Hotland'),
    "Bratty Catty 4": AdvData(79045, 'Hotland'),
    "Burgerpants 1": AdvData(79046, 'Hotland'),
    "Burgerpants 2": AdvData(79047, 'Hotland'),
    "Burgerpants 3": AdvData(79048, 'Hotland'),
    "Burgerpants 4": AdvData(79049, 'Hotland'),
    "TemmieShop 1": AdvData(79050, 'Waterfall'),
    "TemmieShop 2": AdvData(79051, 'Waterfall'),
    "TemmieShop 3": AdvData(79052, 'Waterfall'),
    "TemmieShop 4": AdvData(79053, 'Waterfall'),
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