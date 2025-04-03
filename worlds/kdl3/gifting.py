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
                                                           "IsOpen": is_open,
                                                           **kdl3_gifting_options
                                                       }})
    ctx.client_handler.gifting = is_open


kdl3_gifting_options = {
    "AcceptsAnyGift": True,
    "DesiredTraits": [
        "Consumable", "Food", "Drink", "Candy", "Tomato",
        "Invincible", "Life", "Heal", "Health", "Trap",
        "Goo", "Gel", "Slow", "Slowness", "Eject", "Removal"
    ],
    "MinimumGiftVersion": 2,
}

kdl3_gifts = {
    1: {
        "ItemName": "1-Up",
        "Amount": 1,
        "ItemValue": 400000,
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
        "ItemName": "Maxim Tomato",
        "Amount": 1,
        "ItemValue": 500000,
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
            },
            {
                "Trait": "Vegetable",
                "Quality": 5,
                "Duration": 1,
            }
        ]
    },
    3: {
        "ItemName": "Energy Drink",
        "Amount": 1,
        "ItemValue": 100000,
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
        "ItemName": "Small Star Piece",
        "Amount": 1,
        "ItemValue": 10000,
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
        "ItemName": "Medium Star Piece",
        "Amount": 1,
        "ItemValue": 30000,
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
        "ItemName": "Large Star Piece",
        "Amount": 1,
        "ItemValue": 50000,
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
        "ItemName": "Gooey Bag",
        "Amount": 1,
        "ItemValue": 10000,
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
        "ItemName": "Slowness",
        "Amount": 1,
        "ItemValue": 10000,
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
        "ItemName": "Eject Ability",
        "Amount": 1,
        "ItemValue": 10000,
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
        "ItemName": "Bad Meal",
        "Amount": 1,
        "ItemValue": 10000,
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
