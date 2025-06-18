# Small subfile to handle gifting info such as desired traits and giftbox management
import typing

if typing.TYPE_CHECKING:
    from SNIClient import SNIContext


async def update_object(ctx: "SNIContext", key: str, value: typing.Dict[str, typing.Any]) -> None:
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


async def pop_object(ctx: "SNIContext", key: str, value: str) -> None:
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


async def initialize_giftboxes(ctx: "SNIContext", giftbox_key: str, motherbox_key: str, is_open: bool) -> None:
    ctx.set_notify(motherbox_key, giftbox_key)
    await update_object(ctx, f"Giftboxes;{ctx.team}", {f"{ctx.slot}":
                                                       {
                                                           "is_open": is_open,
                                                           **kdl3_gifting_options
                                                       }})
    await update_object(ctx, f"Giftbox;{ctx.team};{ctx.slot}", {})
    ctx.client_handler.gifting = is_open


kdl3_gifting_options = {
    "accepts_any_gift": True,
    "desired_traits": [
        "Consumable", "Food", "Drink", "Candy", "Tomato",
        "Invincible", "Life", "Heal", "Health", "Trap",
        "Goo", "Gel", "Slow", "Slowness", "Eject", "Removal"
    ],
    "minimum_gift_version": 3,
}

kdl3_gifts = {
    1: {
        "item_name": "1-Up",
        "amount": 1,
        "item_value": 400000,
        "traits": [
            {
                "trait": "Consumable",
                "quality": 1,
                "duration": 1,
            },
            {
                "trait": "Life",
                "quality": 1,
                "duration": 1
            }
        ]
    },
    2: {
        "item_name": "Maxim Tomato",
        "amount": 1,
        "item_value": 500000,
        "traits": [
            {
                "trait": "Consumable",
                "quality": 5,
                "duration": 1,
            },
            {
                "trait": "Heal",
                "quality": 5,
                "duration": 1,
            },
            {
                "trait": "Food",
                "quality": 5,
                "duration": 1,
            },
            {
                "trait": "Tomato",
                "quality": 5,
                "duration": 1,
            },
            {
                "trait": "Vegetable",
                "quality": 5,
                "duration": 1,
            }
        ]
    },
    3: {
        "item_name": "Energy Drink",
        "amount": 1,
        "item_value": 100000,
        "traits": [
            {
                "trait": "Consumable",
                "quality": 1,
                "duration": 1,
            },
            {
                "trait": "Heal",
                "quality": 1,
                "duration": 1,
            },
            {
                "trait": "Drink",
                "quality": 1,
                "duration": 1,
            },
        ]
    },
    5: {
        "item_name": "Small Star Piece",
        "amount": 1,
        "item_value": 10000,
        "traits": [
            {
                "trait": "Currency",
                "quality": 1,
                "duration": 1,
            },
            {
                "trait": "Money",
                "quality": 1,
                "duration": 1,
            },
            {
                "trait": "Star",
                "quality": 1,
                "duration": 1
            }
        ]
    },
    6: {
        "item_name": "Medium Star Piece",
        "amount": 1,
        "item_value": 30000,
        "traits": [
            {
                "trait": "Currency",
                "quality": 3,
                "duration": 1,
            },
            {
                "trait": "Money",
                "quality": 3,
                "duration": 1,
            },
            {
                "trait": "Star",
                "quality": 3,
                "duration": 1
            }
        ]
    },
    7: {
        "item_name": "Large Star Piece",
        "amount": 1,
        "item_value": 50000,
        "traits": [
            {
                "trait": "Currency",
                "quality": 5,
                "duration": 1,
            },
            {
                "trait": "Money",
                "quality": 5,
                "duration": 1,
            },
            {
                "trait": "Star",
                "quality": 5,
                "duration": 1
            }
        ]
    },
}

kdl3_trap_gifts = {
    0: {
        "item_name": "Gooey Bag",
        "amount": 1,
        "item_value": 10000,
        "traits": [
            {
                "trait": "Trap",
                "quality": 1,
                "duration": 1,
            },
            {
                "trait": "Goo",
                "quality": 1,
                "duration": 1,
            },
            {
                "trait": "Gel",
                "quality": 1,
                "duration": 1
            }
        ]
    },
    1: {
        "item_name": "Slowness",
        "amount": 1,
        "item_value": 10000,
        "traits": [
            {
                "trait": "Trap",
                "quality": 1,
                "duration": 1,
            },
            {
                "trait": "Slow",
                "quality": 1,
                "duration": 1,
            },
            {
                "trait": "Slowness",
                "quality": 1,
                "duration": 1
            }
        ]
    },
    2: {
        "item_name": "Eject Ability",
        "amount": 1,
        "item_value": 10000,
        "traits": [
            {
                "trait": "Trap",
                "quality": 1,
                "duration": 1,
            },
            {
                "trait": "Eject",
                "quality": 1,
                "duration": 1,
            },
            {
                "trait": "Removal",
                "quality": 1,
                "duration": 1
            }
        ]
    },
    3: {
        "item_name": "Bad Meal",
        "amount": 1,
        "item_value": 10000,
        "traits": [
            {
                "trait": "Trap",
                "quality": 1,
                "duration": 1,
            },
            {
                "trait": "Damage",
                "quality": 1,
                "duration": 1,
            },
            {
                "trait": "Food",
                "quality": 1,
                "duration": 1
            }
        ]
    },
}
