def party(state, player):
    party = 0
    if state.has(("Pinn",player)) party += 1
    if state.has(("Kani",player)) party += 1
    if state.has(("Geo",player)) party += 1
    if state.has(("Liza",player)) party += 1
    if state.has(("Jeff",player)) party += 1
    if state.has(("Wink",player)) party += 1
    if state.has(("Shane",player)) party += 1
    return party

def red(state, player):
    return (
        state.has(("Yellow Key",player)) 
        or (state.has("Green Key",player) and StateLogic.green(state,player)) 
        or (state.has("Red Key",player) and state.has("Blue Key",player) and StateLogic.blue1(state,player)) 
        or (state.has("Blue Key",player) and StateLogic.blue2(state,player))
    )
    
def red2(state, player):
    return (
        state.has(("Yellow Key",player))
        or (state.has("Blue Key",player) and StateLogic.blue2(state,player))
        or (state.has("Green Key",player) and StateLogic.yellow(state,player))
        or (state.has("Red Key",player) and state.has("MemFinder",player))
    )