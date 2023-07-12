from BaseClasses import CollectionState


def has_unlocked_button(state: CollectionState, player: int) -> bool:
    if getattr(state.multiworld, "hard_mode")[player]:
        return state.has("Button Activation", player)

    return True
