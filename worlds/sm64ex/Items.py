from BaseClasses import Item


class SM64Item(Item):
    game: str = "Super Mario 64"


generic_item_table = {
    "Power Star": 3626000,
    "Basement Key": 3626178,
    "Second Floor Key": 3626179,
    "Progressive Key": 3626180,
    "Wing Cap": 3626181,
    "Metal Cap": 3626182,
    "Vanish Cap": 3626183,
    "1Up Mushroom": 3626184
}

cannon_item_table = {
    "Cannon Unlock BoB": 3626200,
    "Cannon Unlock WF": 3626201,
    "Cannon Unlock JRB": 3626202,
    "Cannon Unlock CCM": 3626203,
    "Cannon Unlock SSL": 3626207,
    "Cannon Unlock SL": 3626209,
    "Cannon Unlock WDW": 3626210,
    "Cannon Unlock TTM": 3626211,
    "Cannon Unlock THI": 3626212,
    "Cannon Unlock RR": 3626214
}

item_table = {**generic_item_table, **cannon_item_table}