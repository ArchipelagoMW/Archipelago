from .rules_expert import PseudoregaliaExpertRules
from .constants.versions import MAP_PATCH


class PseudoregaliaLunaticRules(PseudoregaliaExpertRules):
    def __init__(self, world) -> None:
        super().__init__(world)

        region_clauses = {
            "Tower Remains -> The Great Door": lambda state:
                self.can_gold_ultra(state) and self.get_kicks(state, 1)
                or self.has_slide(state) and self.get_kicks(state, 1) and self.has_plunge(state)
                or self.has_plunge(state) and self.get_kicks(state, 2),
            "Bailey Lower -> Bailey Upper": lambda state:
                self.can_bounce(state),
            "Theatre Pillar -> Theatre Main": lambda state:
                self.get_kicks(state, 2),  # bubble route
            "Dungeon Escape Lower -> Dungeon Escape Upper": lambda state:
                self.can_gold_ultra(state) and self.has_plunge(state),
            "Castle Main -> Castle => Theatre Pillar": lambda state:
                self.has_plunge(state),
            "Castle Spiral Climb -> Castle By Scythe Corridor": lambda state:
                self.get_kicks(state, 3),
            "Castle By Scythe Corridor -> Castle => Theatre (Front)": lambda state:
                self.can_gold_ultra(state) and self.kick_or_plunge(state, 2),
            "Castle => Theatre (Front) -> Castle By Scythe Corridor": lambda state:
                self.can_slidejump(state),
            "Library Main -> Library Top": lambda state:
                self.get_kicks(state, 1)
                or self.get_clings(state, 2),
            "Library Top -> Library Back": lambda state:
                self.can_bounce(state) and self.get_kicks(state, 1) and self.has_plunge(state),
            "Keep Main -> Keep Throne Room": lambda state:
                self.has_breaker(state) and self.has_slide(state) and self.kick_or_plunge(state, 3)
                or self.has_breaker(state) and self.get_clings(state, 2)
                or (
                    self.can_gold_ultra(state)
                    and self.can_bounce(state)
                    and self.get_kicks(state, 1)
                    and self.has_plunge(state)
                    and self.can_soulcutter(state)),
            "Underbelly Main Lower -> Underbelly Main Upper": lambda state:
                self.get_kicks(state, 1),
        }

        location_clauses = {
            # "Twilight Theatre - Center Stage": lambda state:
            #     TODO: theoretical logic for soulcutterless or gemless
            "Dilapidated Dungeon - Past Poles": lambda state:
                self.get_kicks(state, 1) and self.has_plunge(state)
                or self.has_breaker(state) and self.has_plunge(state) and self.has_slide(state),
            "Dilapidated Dungeon - Rafters": lambda state:
                self.can_gold_ultra(state)
                or self.has_slide(state) and self.has_plunge(state),
            "Castle Sansa - Floater In Courtyard": lambda state:
                self.has_slide(state) and self.get_kicks(state, 1),
            "Castle Sansa - Platform In Main Halls": lambda state:
                self.can_bounce(state),
            "Castle Sansa - Corner Corridor": lambda state:
                self.can_gold_slide_ultra(state) and self.get_kicks(state, 1)
                or self.has_slide(state) and self.get_kicks(state, 1) and self.has_plunge(state),
            "Castle Sansa - Near Theatre Front": lambda state:
                self.has_slide(state)
                or self.get_clings(state, 2),
            "Sansa Keep - Levers Room": lambda state: True,
            "Listless Library - Upper Back": lambda state:
                self.has_plunge(state),
        }

        # logic differences due to geometry changes between versions
        if self.world.options.game_version == MAP_PATCH:
            region_clauses["Bailey Upper -> Tower Remains"] = (lambda state:
                self.can_slidejump(state) and self.has_plunge(state))
        else:
            location_clauses["Dilapidated Dungeon - Strong Eyes"] = (lambda state:
                self.has_slide(state) and self.kick_or_plunge(state, 1))


        self.apply_clauses(region_clauses, location_clauses)

    def set_pseudoregalia_rules(self) -> None:
        super().set_pseudoregalia_rules()
