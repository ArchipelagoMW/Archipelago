from BaseClasses import CollectionState

class logic_helpers:
    player: int


    def __init__(self, world):
        self.player = world.player
        self.fuwa_open = False
        self.light_switch_default = world.light_switch_default
        self.sun_switch_default = world.sun_switch_default
        self.star_switch_default = world.star_switch_default
        self.aqua_switch_default = world.aqua_switch_default
        self.moon_switch_default = world.moon_switch_default

        self.light_gate = world.light_gate
        self.sun_gate = world.sun_gate
        self.star_gate = world.star_gate
        self.aqua_gate = world.aqua_gate
        self.moon_gate = world.moon_gate

        if world.options.early_fuwa.value == 1:
           self.fuwa_open = True

        if world.options.phantom_spells.value == 0:
           self.phantom_open = True

    def fuwa_access(self, state: CollectionState) -> bool:
        return (state.has_all({"Light Spell", "Sun Spell", "Star Spell", "Aqua Spell", "Moon Spell"}, self.player) or self.fuwa_open)

    def phantom_spells(self, state: CollectionState) -> bool:
        return (state.has_all({"Light Spell", "Sun Spell", "Star Spell", "Aqua Spell", "Moon Spell"}, self.player) or self.phantom_open)

    def has_early_health(self, state: CollectionState) -> bool:
            return state.has("Life Bottle", self.player, 2)

    def light_switch_on(self, state: CollectionState) -> bool:
        if self.light_switch_default == 0:
            return state.has("Light Switch", self.player)
        else:
            return True

    def sun_switch_on(self, state: CollectionState) -> bool:
        if self.sun_switch_default == 0:
            return state.has("Sun Switch", self.player)
        else:
            return True

    def sun_switch_off(self, state: CollectionState) -> bool:
        if self.sun_switch_default == 1:
            return state.has("Sun Switch", self.player)
        else:
            return True

    def star_switch_on(self, state: CollectionState) -> bool:
        if self.star_switch_default == 0:
            return state.has("Star Switch", self.player)
        else:
            return True

    def star_switch_off(self, state: CollectionState) -> bool:
        if self.star_switch_default == 1:
            return state.has("Star Switch", self.player)
        else:
            return True

    def aqua_switch_on(self, state: CollectionState) -> bool:
        if self.aqua_switch_default == 0:
            return state.has("Aqua Switch", self.player)
        else:
            return True

    def aqua_switch_off(self, state: CollectionState) -> bool:
        if self.aqua_switch_default == 1:
            return state.has("Aqua Switch", self.player)
        else:
            return True

    def moon_switch_on(self, state: CollectionState) -> bool:
        if self.moon_switch_default == 0:
            return state.has("Moon Switch", self.player)
        else:
            return True

    def moon_switch_off(self, state: CollectionState) -> bool:
        if self.moon_switch_default == 1:
            return state.has("Moon Switch", self.player)
        else:
            return True

    def can_fight_boss(self, state: CollectionState) -> bool:
        return (state.has_group("Swords", self.player, 1) or state.has_group("Projectiles", self.player, 1)) and self.has_early_health

    def has_good_projectile(self, state: CollectionState) -> bool:
        return state.has_group("Projectiles", self.player, 1)

    def can_fight_final_boss(self, state: CollectionState) -> bool:
        return state.has_group("Armor", self.player, 1) and self.has_early_health and self.phantom_spells
    