def total_hearts(player: int, state, count: int) -> bool:
    return state.has("HeartPiece", player, count - 2)


def has_megasword(player: int, state) -> bool:
    return (
        state.has_any(("ItemMegaSword", "Reverse Progressive Sword",), player)
        or state.has("Progressive Sword", player, 3)
        )


def has_brokensword(player: int, state) -> bool:
    return (
        state.has_any(("ItemBrokenSword", "Progressive Sword",), player)
        or state.has("Reverse Progressive Sword", player, 3)
        )


def has_darkroom(player: int, state, value: int, darkrooms: int) -> bool:
    return darkrooms >= value or state.has("ItemFlashLight", player)


def can_passBoxes(player: int, state) -> bool:
    return (
        state.has_all(("has_sword", "ItemGrinder",), player)
        or state.has("ItemCoffee", player)
        )


def can_openChest(player: int, state) -> bool:
    return state.has_any(("has_sword", "ItemWateringCan",), player)
