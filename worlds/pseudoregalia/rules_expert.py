from .rules_hard import PseudoregaliaHardRules
from .constants.versions import MAP_PATCH


class PseudoregaliaExpertRules(PseudoregaliaHardRules):
    def __init__(self, world) -> None:
        super().__init__(world)

        region_clauses = {
            "Bailey Lower -> Bailey Upper": lambda state:
                self.has_slide(state),
            "Tower Remains -> The Great Door": lambda state:
                # get to top of tower
                self.has_slide(state)  # ultras from right tower directly to pole
                and (
                    self.get_clings(state, 2)
                    or self.get_kicks(state, 2))
                or self.can_gold_ultra(state) and self.get_kicks(state, 1) and self.has_plunge(state),
            # "Theatre Main -> Theatre Outside Scythe Corridor": lambda state:
                # there's certainly some routes besides the gem route that should be expert/lunatic
            "Theatre Main -> Castle => Theatre (Front)": lambda state:
                self.has_slide(state),
            "Theatre Pillar => Bailey -> Theatre Pillar": lambda state:
                self.has_slide(state)
                or self.get_clings(state, 2),
            "Castle => Theatre Pillar -> Theatre Pillar": lambda state:
                self.get_kicks(state, 1)
                or self.get_clings(state, 2)
                or self.has_slide(state),
            "Theatre Pillar -> Theatre Main": lambda state:
                self.has_slide(state) and self.kick_or_plunge(state, 3),
            "Theatre Outside Scythe Corridor -> Dungeon Escape Upper": lambda state:
                self.navigate_darkrooms(state) and self.has_slide(state),
            "Theatre Outside Scythe Corridor -> Keep Main": lambda state:
                self.has_slide(state),

            "Dungeon Escape Lower -> Dungeon Escape Upper": lambda state:
                self.can_gold_ultra(state) and self.get_kicks(state, 1),
            "Dungeon Escape Upper -> Theatre Outside Scythe Corridor": lambda state:
                self.has_slide(state),
            "Castle Main -> Castle => Theatre Pillar": lambda state:
                self.has_slide(state),
            "Castle Main -> Castle Spiral Climb": lambda state:
                self.can_gold_ultra(state)
                or self.has_slide(state) and self.kick_or_plunge(state, 1),
            "Castle Spiral Climb -> Castle High Climb": lambda state:
                self.can_gold_slide_ultra(state)
                or self.has_slide(state) and self.kick_or_plunge(state, 1)
                or self.get_kicks(state, 2),
            "Castle Spiral Climb -> Castle By Scythe Corridor": lambda state:
                self.kick_or_plunge(state, 4),
            "Castle By Scythe Corridor -> Castle => Theatre (Front)": lambda state:
                self.can_gold_ultra(state) and self.get_kicks(state, 2)
                or self.has_slide(state) and self.kick_or_plunge(state, 3),
            "Castle By Scythe Corridor -> Castle High Climb": lambda state:
                self.has_slide(state)
                or self.kick_or_plunge(state, 2),
            "Castle => Theatre (Front) -> Castle By Scythe Corridor": lambda state:
                self.can_gold_slide_ultra(state)
                or self.has_slide(state) and self.get_kicks(state, 1)
                or self.get_kicks(state, 3),
            "Castle => Theatre (Front) -> Castle Moon Room": lambda state:
                self.has_slide(state),
            "Castle => Theatre (Front) -> Theatre Main": lambda state:
                self.can_gold_slide_ultra(state)
                or self.has_slide(state) and self.kick_or_plunge(state, 1),
            "Library Main -> Library Top": lambda state:
                self.has_plunge(state)
                or self.has_slide(state),
            "Library Greaves -> Library Back": lambda state:
                self.can_attack(state) and self.has_slide(state),
            "Library Back -> Library Top": lambda state:
                self.has_slide(state),
            "Library Top -> Library Back": lambda state:
                self.get_kicks(state, 2),
            "Keep Main -> Keep Throne Room": lambda state:
                self.has_breaker(state)
                and (
                    self.get_clings(state, 4)
                    or self.get_clings(state, 2) and self.get_kicks(state, 1)
                    or self.get_clings(state, 2) and self.has_slide(state)
                    or self.can_bounce(state) and self.kick_or_plunge(state, 3)
                    or self.has_slide(state) and self.get_kicks(state, 3)),
            "Keep Main -> Keep => Underbelly": lambda state:
                self.has_slide(state),
            "Keep Main -> Keep (Northeast) => Castle": lambda state:
                self.has_slide(state),
            "Keep Main -> Theatre Outside Scythe Corridor": lambda state:
                self.has_slide(state),
            "Underbelly => Dungeon -> Underbelly Ascendant Light": lambda state:
                self.get_kicks(state, 1) and self.has_slide(state),
            "Underbelly Light Pillar -> Underbelly => Dungeon": lambda state:
                self.has_slide(state) and self.get_kicks(state, 2)
                or self.can_gold_ultra(state) and self.get_kicks(state, 1) and self.has_plunge(state)
                or self.has_plunge(state) and self.get_kicks(state, 2),
            "Underbelly Light Pillar -> Underbelly Ascendant Light": lambda state:
                self.has_plunge(state) and self.get_kicks(state, 1)
                or self.has_slide(state) and self.can_attack(state)
                or self.can_gold_ultra(state) and self.get_kicks(state, 3) and self.get_clings(state, 4),
            "Underbelly Ascendant Light -> Underbelly => Dungeon": lambda state:
                self.get_kicks(state, 1)
                and (
                    self.has_slide(state)
                    or self.has_plunge(state)),
            "Underbelly Main Lower -> Underbelly By Heliacal": lambda state:
                self.has_slide(state),
            "Underbelly Main Lower -> Underbelly Main Upper": lambda state:
                self.get_kicks(state, 2)
                or self.get_kicks(state, 1) and self.get_clings(state, 2)
                or self.has_slide(state) and self.get_clings(state, 4)
                or self.can_gold_slide_ultra(state) and self.get_kicks(state, 1) and self.has_breaker(state),
            "Underbelly Main Upper -> Underbelly Light Pillar": lambda state:
                self.has_breaker(state)
                and (
                    self.has_slide(state)
                    or self.get_kicks(state, 1))
                or self.has_slide(state)
                and (
                    self.kick_or_plunge(state, 3)
                    or self.get_clings(state, 6))
                or self.can_gold_ultra(state) and self.kick_or_plunge(state, 2),
            "Underbelly Main Upper -> Underbelly By Heliacal": lambda state:
                self.has_breaker(state)
                and (
                    self.has_slide(state) and self.get_kicks(state, 2)
                    or self.get_kicks(state, 3)),
            "Underbelly By Heliacal -> Underbelly Main Upper": lambda state:
                self.has_plunge(state)
                or self.has_breaker(state)
                and (
                    self.has_slide(state)
                    or self.get_clings(state, 2)
                    or self.get_kicks(state, 1))
                or self.has_slide(state)
                and (
                    self.get_clings(state, 2)
                    or self.get_kicks(state, 2)),
        }

        location_clauses = {
            "Empty Bailey - Cheese Bell": lambda state:
                self.has_slide(state) and self.get_kicks(state, 1),
            "Empty Bailey - Center Steeple": lambda state:
                self.get_kicks(state, 1)
                or self.has_slide(state),
            "Twilight Theatre - Soul Cutter": lambda state:
                self.can_strikebreak(state) and self.has_slide(state),
            "Twilight Theatre - Corner Beam": lambda state:
                self.get_kicks(state, 3)
                or self.has_slide(state)
                and (
                    self.kick_or_plunge(state, 2)
                    or self.get_clings(state, 2)),
            "Twilight Theatre - Locked Door": lambda state:
                self.has_small_keys(state) and self.has_slide(state),
            "Twilight Theatre - Back Of Auditorium": lambda state:
                self.has_slide(state),  # super annoying ultrahops
            "Twilight Theatre - Center Stage": lambda state:
                self.can_soulcutter(state) and self.get_clings(state, 4),
            "Tower Remains - Cling Gem": lambda state:
                self.has_slide(state),
            "Tower Remains - Cling Gem 1": lambda state:
                self.has_slide(state),
            "Tower Remains - Cling Gem 2": lambda state:
                self.has_slide(state),
            "Tower Remains - Cling Gem 3": lambda state:
                self.has_slide(state),

            "Dilapidated Dungeon - Dark Orbs": lambda state:
                self.can_gold_slide_ultra(state) and self.get_kicks(state, 1)
                or self.has_slide(state)
                and (
                    self.can_bounce(state)
                    or self.get_kicks(state, 2)),
            "Dilapidated Dungeon - Past Poles": lambda state:
                self.has_slide(state) and self.get_kicks(state, 1),
            "Dilapidated Dungeon - Rafters": lambda state:
                self.kick_or_plunge(state, 2)
                or self.can_gold_ultra(state) and self.kick_or_plunge(state, 1)
                or self.can_bounce(state) and self.get_clings(state, 2),
            "Castle Sansa - Floater In Courtyard": lambda state:
                self.can_bounce(state) and self.has_slide(state)
                or self.can_gold_ultra(state) and self.get_kicks(state, 1)
                or self.has_slide(state) and self.kick_or_plunge(state, 2)
                or self.get_kicks(state, 3)
                or self.get_clings(state, 2),
            "Castle Sansa - Platform In Main Halls": lambda state:
                self.has_slide(state),
            "Castle Sansa - Tall Room Near Wheel Crawlers": lambda state:
                self.can_gold_ultra(state),
            "Castle Sansa - Alcove Near Dungeon": lambda state:
                self.has_slide(state),
            "Castle Sansa - Balcony": lambda state:
                self.get_kicks(state, 3)
                or self.has_plunge(state) and self.get_kicks(state, 1)
                or self.has_slide(state),
            "Castle Sansa - Corner Corridor": lambda state:
                self.get_kicks(state, 2) and self.has_slide(state),
            "Castle Sansa - Wheel Crawlers": lambda state:
                self.kick_or_plunge(state, 1)
                or self.has_slide(state),
            "Castle Sansa - Alcove Near Scythe Corridor": lambda state:
                self.kick_or_plunge(state, 3)
                or self.has_slide(state) and self.get_kicks(state, 1)
                or self.can_gold_ultra(state) and self.has_plunge(state),
            "Castle Sansa - Near Theatre Front": lambda state:
                self.can_gold_slide_ultra(state)
                or self.has_slide(state) and self.get_kicks(state, 1)
                or self.get_clings(state, 4),
            "Castle Sansa - High Climb From Courtyard": lambda state:
                self.can_attack(state) and self.get_kicks(state, 1)
                or self.get_clings(state, 2) and self.get_kicks(state, 1)
                or self.has_slide(state),
            "Listless Library - Upper Back": lambda state:
                self.can_attack(state) and self.has_slide(state),
            "Listless Library - Locked Door Across": lambda state:
                self.has_slide(state),
            "Listless Library - Locked Door Left": lambda state:
                self.kick_or_plunge(state, 2)
                or self.has_slide(state) and self.kick_or_plunge(state, 1),
            "Sansa Keep - Strikebreak": lambda state:
                self.has_breaker(state) and self.has_slide(state)
                or self.can_strikebreak(state) and self.has_plunge(state),
            "Sansa Keep - Near Theatre": lambda state:
                self.has_slide(state),
            "The Underbelly - Rafters Near Keep": lambda state:
                self.has_slide(state),
            "The Underbelly - Main Room": lambda state:
                self.has_slide(state)
                or self.get_kicks(state, 1),
            "The Underbelly - Alcove Near Light": lambda state:
                self.get_kicks(state, 1) and self.has_slide(state),
            "The Underbelly - Building Near Little Guy": lambda state:
                self.get_kicks(state, 1)
                or self.has_slide(state),
            "The Underbelly - Strikebreak Wall": lambda state:
                self.can_strikebreak(state)
                and (
                    self.get_kicks(state, 1) and self.has_plunge(state)
                    or self.has_slide(state) and self.get_kicks(state, 2)
                    or self.can_gold_ultra(state) and self.get_clings(state, 2)),
            "The Underbelly - Surrounded By Holes": lambda state:
                self.can_soulcutter(state) and self.has_slide(state)
                or self.has_slide(state) and self.get_kicks(state, 1) and self.has_plunge(state),

            "Castle Sansa - Bubblephobic Goatling": lambda state:
                self.has_slide(state),

            "Twilight Theatre - Stage Right Stool": lambda state:
                self.can_soulcutter(state) and self.has_slide(state),

            "The Underbelly - Note on a Ledge": lambda state:
                self.has_slide(state),
            "The Underbelly - Note in the Big Room": lambda state:
                self.has_slide(state)
                or self.get_clings(state, 6),
        }

        # logic differences due to geometry changes between versions
        if self.world.options.game_version == MAP_PATCH:
            region_clauses["Bailey Upper -> Tower Remains"] = (lambda state:
                self.has_slide(state)
                and (
                    self.can_bounce(state)
                    or self.get_kicks(state, 1)))
            region_clauses["Dungeon => Castle -> Dungeon Strong Eyes"] = (lambda state:
                self.has_breaker(state) and self.has_slide(state))
            region_clauses["Dungeon Strong Eyes -> Dungeon => Castle"] = (lambda state:
                self.can_attack(state) and self.has_slide(state))
            location_clauses["Dilapidated Dungeon - Strong Eyes"] = (lambda state:
                self.has_slide(state))
        else:
            region_clauses["Bailey Upper -> Tower Remains"] = (lambda state:
                self.has_slide(state))
            location_clauses["Dilapidated Dungeon - Strong Eyes"] = (lambda state:
                self.get_clings(state, 2)
                or self.has_slide(state) and self.get_kicks(state, 1))

        self.apply_clauses(region_clauses, location_clauses)

    def set_pseudoregalia_rules(self) -> None:
        super().set_pseudoregalia_rules()
