from .rules_normal import PseudoregaliaNormalRules
from .constants.versions import MAP_PATCH


class PseudoregaliaHardRules(PseudoregaliaNormalRules):
    def __init__(self, world) -> None:
        super().__init__(world)

        region_clauses = {
            "Bailey Lower -> Bailey Upper": lambda state:
                self.has_plunge(state)
                or self.get_clings(state, 2),
            "Tower Remains -> The Great Door": lambda state:
                self.can_attack(state) and self.get_clings(state, 2),
            "Theatre Main -> Theatre Pillar": lambda state:
                self.get_kicks(state, 1),
            "Theatre Main -> Theatre Outside Scythe Corridor": lambda state:
                self.get_clings(state, 4),
            "Theatre Pillar => Bailey -> Theatre Pillar": lambda state:
                self.get_kicks(state, 1)
                or self.can_slidejump(state),
            "Castle => Theatre Pillar -> Theatre Pillar": lambda state:
                self.can_slidejump(state),
            "Theatre Pillar -> Theatre Main": lambda state:
                self.can_slidejump(state) and self.kick_or_plunge(state, 3),
            "Theatre Outside Scythe Corridor -> Theatre Main": lambda state:
                self.get_clings(state, 4),

            "Dungeon Escape Lower -> Dungeon Escape Upper": lambda state:
                self.get_clings(state, 4)
                or self.kick_or_plunge(state, 2),
            "Castle Main -> Castle => Theatre Pillar": lambda state:
                self.get_clings(state, 2)
                or self.get_kicks(state, 1),
            "Castle Main -> Castle Spiral Climb": lambda state:
                self.get_clings(state, 2)
                or self.kick_or_plunge(state, 2)
                or self.can_slidejump(state) and self.has_plunge(state),
            "Castle Spiral Climb -> Castle High Climb": lambda state:
                self.kick_or_plunge(state, 3)
                or self.knows_obscure(state) and self.can_attack(state) and self.can_slidejump(state),
            "Castle By Scythe Corridor -> Castle Spiral Climb": lambda state:
                self.get_kicks(state, 3),
            "Castle By Scythe Corridor -> Castle => Theatre (Front)": lambda state:
                self.get_clings(state, 6),
            "Castle By Scythe Corridor -> Castle High Climb": lambda state:
                self.get_kicks(state, 3) and self.has_breaker(state)
                or self.get_kicks(state, 1) and self.has_plunge(state),
            "Castle => Theatre (Front) -> Castle Moon Room": lambda state:
                self.get_kicks(state, 4),
            "Castle => Theatre (Front) -> Theatre Main": lambda state:  # TODO double check for hard logic
                self.get_clings(state, 4),
            "Library Main -> Library Top": lambda state:
                self.get_clings(state, 4)
                or self.knows_obscure(state) and self.kick_or_plunge(state, 2),
            "Library Greaves -> Library Back": lambda state:
                self.can_attack(state) and self.get_kicks(state, 1),
            "Library Back -> Library Top": lambda state:
                self.get_kicks(state, 1)
                or self.get_clings(state, 2),
            "Library Top -> Library Back": lambda state:
                self.get_clings(state, 2)
                or self.get_kicks(state, 3)
                or self.get_kicks(state, 2) and self.has_plunge(state) and self.can_bounce(state),
            "Keep Main -> Keep Locked Room": lambda state: True,
                # Note for trackers: This is accessible with nothing but not in logic.
                # Cutting the platform or hitting the lever make this harder and are irreversible.
                # On Hard and above, the player is expected to not do either.
            "Keep Main -> Keep Sunsetter": lambda state: True,
                # See "Keep Main -> Keep Locked Room".
            "Keep Main -> Keep Throne Room": lambda state:
                self.has_breaker(state) and self.get_clings(state, 6)
                and (
                    self.has_plunge(state)
                    or self.get_kicks(state, 2)
                    or self.get_kicks(state, 1) and self.knows_obscure(state))
                or self.has_breaker(state) and self.has_plunge(state) and self.get_kicks(state, 4)
                or self.can_bounce(state) and self.get_kicks(state, 3),
            "Keep Main -> Keep (Northeast) => Castle": lambda state:
                self.get_kicks(state, 1),
            "Underbelly => Dungeon -> Underbelly Ascendant Light": lambda state:
                self.get_clings(state, 2),
            "Underbelly Light Pillar -> Underbelly Ascendant Light": lambda state:
                self.knows_obscure(state)
                and (
                    self.can_attack(state) and self.get_kicks(state, 2)
                    or self.has_plunge(state) and self.get_clings(state, 2)),
            "Underbelly Main Lower -> Underbelly Hole": lambda state:
                self.has_plunge(state) and self.get_clings(state, 4),
            "Underbelly Main Lower -> Underbelly By Heliacal": lambda state:
                self.has_slide(state) and self.get_kicks(state, 2),
            "Underbelly Main Lower -> Underbelly Main Upper": lambda state:
                self.knows_obscure(state)
                and (
                    self.has_plunge(state) and self.get_kicks(state, 1)
                    or self.has_plunge(state) and self.get_clings(state, 4)
                    or self.get_kicks(state, 2) and self.get_clings(state, 2)),
            "Underbelly Main Upper -> Underbelly Light Pillar": lambda state:
                self.knows_obscure(state)
                and (
                    self.has_breaker(state) and self.get_clings(state, 2)
                    or self.can_slidejump(state) and self.get_kicks(state, 1) and self.has_plunge(state)),
            "Underbelly Main Upper -> Underbelly By Heliacal": lambda state:
                self.has_breaker(state)
                and (
                    state.has("Ascendant Light", self.player)
                    or self.get_clings(state, 2) and self.kick_or_plunge(state, 1)
                    or self.kick_or_plunge(state, 4)
                    or self.knows_obscure(state) and self.get_clings(state, 4)),
            "Underbelly => Bailey -> Bailey Upper": lambda state:
                self.get_kicks(state, 3)
                or self.can_slidejump(state) and self.get_kicks(state, 1),
            "Underbelly => Bailey -> Underbelly Main Lower": lambda state: 
                self.get_clings(state, 2),
            "Underbelly Hole -> Underbelly Main Lower": lambda state:
                self.has_plunge(state)
                and (
                    self.get_kicks(state, 1)
                    or self.get_clings(state, 4)),
        }

        location_clauses = {
            "Empty Bailey - Cheese Bell": lambda state:
                self.get_kicks(state, 3)
                or self.get_clings(state, 6),
            "Empty Bailey - Center Steeple": lambda state:
                self.get_kicks(state, 2) and self.has_breaker(state),
            "Twilight Theatre - Soul Cutter": lambda state:
                self.can_strikebreak(state) and self.can_slidejump(state),
            "Twilight Theatre - Corner Beam": lambda state:
                self.get_clings(state, 2)
                and (
                    self.kick_or_plunge(state, 1)
                    or self.can_slidejump(state)),
            "Twilight Theatre - Locked Door": lambda state:
                self.has_small_keys(state) and self.get_clings(state, 4),
            "Twilight Theatre - Back Of Auditorium": lambda state:
                self.can_slidejump(state),
            "Twilight Theatre - Center Stage": lambda state:  # i don't feel super confident about this
                self.can_soulcutter(state) and self.get_clings(state, 6)
                and self.kick_or_plunge(state, 1) and self.can_slidejump(state),
                # TODO remove notes
                # leftside: soulcutter+(cling|3kickor)
                # rightside: cling only technical but probably add some vertical for nicety, plus whatever the clingless lunatic route is
                # middle: (getting to back area needs: cling, 5kickor, scythe entrance)
                    # silly doorframe shit: cling
                    # shortcut: ultra + 1kickor + cling
                    # arena: breaker + (3kickor, cling)
            "Tower Remains - Cling Gem": lambda state:
                self.get_clings(state, 2),  # ride from back of right tower to ledge
            "Tower Remains - Cling Gem 1": lambda state:
                self.get_clings(state, 2),
            "Tower Remains - Cling Gem 2": lambda state:
                self.get_clings(state, 2),
            "Tower Remains - Cling Gem 3": lambda state:
                self.get_clings(state, 2),

            "Dilapidated Dungeon - Dark Orbs": lambda state:
                self.get_clings(state, 6)
                or self.get_kicks(state, 1) and self.can_bounce(state)
                or self.can_slidejump(state) and self.has_plunge(state) and self.can_bounce(state)
                or self.get_kicks(state, 3) and self.has_plunge(state),
            "Dilapidated Dungeon - Past Poles": lambda state:
                self.get_clings(state, 2)
                or self.get_kicks(state, 2)
                or self.knows_obscure(state) and self.can_slidejump(state) and self.get_kicks(state, 1),
            "Dilapidated Dungeon - Rafters": lambda state:
                self.get_clings(state, 6)
                or self.get_kicks(state, 1) and self.has_plunge(state)
                or self.get_kicks(state, 1) and self.can_bounce(state),
            "Castle Sansa - Floater In Courtyard": lambda state:
                self.kick_or_plunge(state, 4)
                or self.get_clings(state, 2) and self.has_plunge(state)
                or self.get_clings(state, 4),
            "Castle Sansa - Platform In Main Halls": lambda state:
                self.kick_or_plunge(state, 1),
            "Castle Sansa - Tall Room Near Wheel Crawlers": lambda state:
                self.get_clings(state, 2)
                or self.get_kicks(state, 1)
                or self.knows_obscure(state) and self.can_slidejump(state) and self.has_plunge(state),
            "Castle Sansa - Balcony": lambda state:
                self.can_slidejump(state) and self.get_kicks(state, 1),
            "Castle Sansa - Corner Corridor": lambda state:
                self.get_kicks(state, 3),
            "Castle Sansa - Wheel Crawlers": lambda state:
                self.get_kicks(state, 1)
                or self.can_slidejump(state) and self.has_plunge(state),
            "Castle Sansa - Alcove Near Scythe Corridor": lambda state:
                self.get_clings(state, 4)
                or self.has_plunge(state) and self.get_clings(state, 2)
                or self.get_kicks(state, 2) and self.has_plunge(state),
            "Castle Sansa - Near Theatre Front": lambda state:
                self.get_clings(state, 6)
                or self.get_clings(state, 2) and self.get_kicks(state, 1),
            "Castle Sansa - High Climb From Courtyard": lambda state:
                self.get_clings(state, 6)
                or self.has_plunge(state) and self.can_slidejump(state),
            "Listless Library - Upper Back": lambda state:
                self.can_attack(state) and self.get_clings(state, 4),
            "Listless Library - Locked Door Across": lambda state:
                self.kick_or_plunge(state, 1),
            "Listless Library - Locked Door Left": lambda state:
                self.get_kicks(state, 2),
            "Sansa Keep - Strikebreak": lambda state:
                self.has_breaker(state) and self.get_kicks(state, 1)
                and (
                    self.has_slide(state)
                    or self.can_strikebreak(state)),
            "The Underbelly - Rafters Near Keep": lambda state:
                self.kick_or_plunge(state, 1)
                or self.get_clings(state, 2),
            "The Underbelly - Main Room": lambda state:
                self.can_slidejump(state),
            "The Underbelly - Alcove Near Light": lambda state:
                self.get_kicks(state, 3)
                or self.get_kicks(state, 2) and self.can_slidejump(state),
            "The Underbelly - Building Near Little Guy": lambda state:
                self.get_kicks(state, 2),
            "The Underbelly - Strikebreak Wall": lambda state:
                self.can_strikebreak(state)
                and (
                    self.can_bounce(state)
                    or self.kick_or_plunge(state, 3)),
            "The Underbelly - Surrounded By Holes": lambda state:
                self.has_plunge(state) and self.get_clings(state, 6),

            "Castle Sansa - Bubblephobic Goatling": lambda state:
                self.get_kicks(state, 1)
                or self.get_clings(state, 2),
            "Twilight Theatre - Murderous Goatling": lambda state:
                self.get_kicks(state, 1),

            "Twilight Theatre - Stage Right Stool": lambda state:
                self.knows_obscure(state) and self.can_soulcutter(state) and self.can_slidejump(state),

            "The Underbelly - Note on a Ledge": lambda state:
                self.can_slidejump(state),
            "The Underbelly - Note in the Big Room": lambda state:
                self.kick_or_plunge(state, 2)
                or self.get_clings(state, 6) and self.get_kicks(state, 1),
        }

        # logic differences due to geometry changes between versions
        if self.world.options.game_version == MAP_PATCH:
            region_clauses["Bailey Upper -> Tower Remains"] = (lambda state:
                self.kick_or_plunge(state, 3)
                or self.get_kicks(state, 2) and self.can_bounce(state))
            region_clauses["Dungeon => Castle -> Dungeon Strong Eyes"] = (lambda state:
                self.knows_obscure(state) and self.has_breaker(state) and self.get_clings(state, 2))
            region_clauses["Dungeon Strong Eyes -> Dungeon => Castle"] = (lambda state:
                self.knows_obscure(state)
                and (
                    self.has_plunge(state)
                    or self.has_breaker(state) and self.get_kicks(state, 1)
                    or self.has_breaker(state) and self.can_slidejump(state)))
        else:
            region_clauses["Bailey Upper -> Tower Remains"] = (lambda state:
                self.kick_or_plunge(state, 3))
            location_clauses["Dilapidated Dungeon - Strong Eyes"] = (lambda state:
                self.knows_obscure(state) and self.get_clings(state, 2) and self.kick_or_plunge(state, 2))

        self.apply_clauses(region_clauses, location_clauses)

    def set_pseudoregalia_rules(self) -> None:
        super().set_pseudoregalia_rules()
