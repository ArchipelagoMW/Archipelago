# Small subfile to handle gifting info such as desired traits and giftbox management
import typing


async def update_object(ctx, key: str, value: typing.Dict):
    await ctx.send_msgs([
        {
            "cmd": "Set",
            "key": key,
            "default": {},
            "want_reply": False,
            "operations": [
                {"operation": "update", "value": value}
            ]
        }
    ])


async def pop_object(ctx, key: str, value: str):
    await ctx.send_msgs([
        {
            "cmd": "Set",
            "key": key,
            "default": {},
            "want_reply": False,
            "operations": [
                {"operation": "pop", "value": value}
            ]
        }
    ])


async def initialize_giftboxes(ctx, giftbox_key: str, motherbox_key: str, is_open: bool):
    ctx.set_notify(motherbox_key, giftbox_key)
    await update_object(ctx, f"Giftboxes;{ctx.team}", {f"{ctx.slot}":
        {
            "IsOpen": is_open,
            **kdl3_gifting_options
        }})
    ctx.gifting = is_open


kdl3_gifting_options = {
    "AcceptsAnyGift": True,
    "DesiredTraits": [
        "Consumable", "Food", "Drink", "Candy", "Tomato",
        "Invincible", "Life", "Heal", "Health", "Trap",
        "Goo", "Gel", "Slow", "Slowness", "Eject", "Removal"
    ]
}

kdl3_gifts = {
    1: {
        "Item": {
            "Name": "1-Up",
            "Amount": 1,
            "Value": 400000
        },
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Life",
                "Quality": 1,
                "Duration": 1
            }
        ]
    },
    2: {
        "Item": {
            "Name": "Maxim Tomato",
            "Amount": 1,
            "Value": 500000
        },
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 5,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 5,
                "Duration": 1,
            },
            {
                "Trait": "Food",
                "Quality": 5,
                "Duration": 1,
            },
            {
                "Trait": "Tomato",
                "Quality": 5,
                "Duration": 1,
            }
        ]
    },
    3: {
        "Item": {
            "Name": "Energy Drink",
            "Amount": 1,
            "Value": 100000
        },
        "Traits": [
            {
                "Trait": "Consumable",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Heal",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Drink",
                "Quality": 1,
                "Duration": 1,
            },
        ]
    },
    5: {
        "Item": {
            "Name": "Small Star Piece",
            "Amount": 1,
            "Value": 10000
        },
        "Traits": [
            {
                "Trait": "Currency",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Money",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Star",
                "Quality": 1,
                "Duration": 1
            }
        ]
    },
    6: {
        "Item": {
            "Name": "Medium Star Piece",
            "Amount": 1,
            "Value": 30000
        },
        "Traits": [
            {
                "Trait": "Currency",
                "Quality": 3,
                "Duration": 1,
            },
            {
                "Trait": "Money",
                "Quality": 3,
                "Duration": 1,
            },
            {
                "Trait": "Star",
                "Quality": 3,
                "Duration": 1
            }
        ]
    },
    7: {
        "Item": {
            "Name": "Large Star Piece",
            "Amount": 1,
            "Value": 50000
        },
        "Traits": [
            {
                "Trait": "Currency",
                "Quality": 5,
                "Duration": 1,
            },
            {
                "Trait": "Money",
                "Quality": 5,
                "Duration": 1,
            },
            {
                "Trait": "Star",
                "Quality": 5,
                "Duration": 1
            }
        ]
    },
}

kdl3_trap_gifts = {
    0: {
        "Item": {
            "Name": "Gooey Bag",
            "Amount": 1,
            "Value": 10000
        },
        "Traits": [
            {
                "Trait": "Trap",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Goo",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Gel",
                "Quality": 1,
                "Duration": 1
            }
        ]
    },
    1: {
        "Item": {
            "Name": "Slowness",
            "Amount": 1,
            "Value": 10000
        },
        "Traits": [
            {
                "Trait": "Trap",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Slow",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Slowness",
                "Quality": 1,
                "Duration": 1
            }
        ]
    },
    2: {
        "Item": {
            "Name": "Eject Ability",
            "Amount": 1,
            "Value": 10000
        },
        "Traits": [
            {
                "Trait": "Trap",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Eject",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Removal",
                "Quality": 1,
                "Duration": 1
            }
        ]
    },
    3: {
        "Item": {
            "Name": "Bad Meal",
            "Amount": 1,
            "Value": 10000
        },
        "Traits": [
            {
                "Trait": "Trap",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Damage",
                "Quality": 1,
                "Duration": 1,
            },
            {
                "Trait": "Food",
                "Quality": 1,
                "Duration": 1
            }
        ]
    },
}
