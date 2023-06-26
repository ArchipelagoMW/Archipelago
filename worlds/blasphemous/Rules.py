from worlds.generic.Rules import set_rule, add_rule
from worlds.AutoWorld import LogicMixin


class BlasphemousLogic(LogicMixin):
    def _blaphemous_total_fervour(self, player) -> int:
        totalFervour: int = 60 + (20 * self.count("Fervour Upgrade", player)) + (10 * self.count("Bead of Blue Wax", player))

        return totalFervour

    def _blasphemous_aubade(self, player):
        return self.has("Aubade of the Nameless Guardian", player) if self._blaphemous_total_fervour(player) >= 90 else False
    
    def _blasphemous_tirana(self, player):
        return self.has("Tirana of the Celestial Bastion", player) if self._blaphemous_total_fervour(player) >= 90 else False
    
    def _blasphemous_pillar(self, player):
        return self.has_any({"Debla of the Lights", "Taranto to my Sister", "Cloistered Ruby"}, player)
    
    def _blasphemous_charge_beam(self, player):
        return self.has("Charged Skill", player, 3)

    def _blasphemous_can_air_stall(self, logic, player):
        return self.has("Ranged Skill", player) if logic.value >= 1 else False
    
    def _blasphemous_can_dawn_jump(self, logic, player):
        return self.has_all({"Brilliant Heart of Dawn", "Dash Ability"}, player) if logic.value >= 1 else False

    def _blasphemous_can_water_jump(self, player):
        return self.has_any({"Nail Uprooted from Dirt", "Purified Hand of the Nun"}, player)
    
    def _blasphemous_can_break_holes(self, player):
        return self.has_any({"Charged Skill", "Dive Skill"}, player) or \
            (self.has("Lunge Skill", player, 3) and \
                self.has("Dash Ability", player)) or \
                    self.has_group("prayer", player) or \
                        self._blasphemous_aubade(player) or \
                            self._blasphemous_tirana(player)
    
    def _blasphemous_can_break_tirana(self, logic, player):
        return self._blasphemous_tirana(player) if logic.value >= 2 else False

    def _blasphemous_can_dive_laser(self, logic, player):
        return self.has("Dive Skill", player, 3) if logic.value >= 2 else False
    
    def _blasphemous_can_walk_on_root(self, player):
        return self.has("Three Gnarled Tongues", player)
    
    def _blasphemous_can_climb_on_root(self, player):
        return self.has_all({"Three Gnarled Tongues", "Wall Climb Ability"}, player)
    
    def _blasphemous_can_survive_poison(self, logic, player, number: int):
        if number == 1:
            if logic.value >= 2:
                return True
            elif logic.value == 1:
                return self.has_any({"Silvered Lung of Dolphos", "Tiento to your Thorned Hairs"}, player)
            elif logic.value == 0:
                return self.has("Silvered Lung of Dolphos", player)
        elif number == 2:
            if logic.value >= 1:
                return self.has_any({"Silvered Lung of Dolphos", "Tiento to your Thorned Hairs"}, player)
            else:
                return self.has("Silvered Lung of Dolphos", player)
        elif number == 3:
            if logic.value >= 2 and self._blaphemous_total_fervour(player) >= 120:
                return self.has_any({"Silvered Lung of Dolphos", "Tiento to your Thorned Hairs"}, player)
            else:
                return self.has("Silvered Lung of Dolphos", player)
        
    def _blasphemous_can_enemy_bounce(self, logic, enemy): # TODO
        return self._blasphemous_enemy_skips_allowed(logic, enemy)
    
    def _blasphemous_can_enemy_upslash(self, logic, enemy, player):
        return self.has("Combo Skill", player, 2) and \
            self._blasphemous_enemy_skips_allowed(logic, enemy)
    
    def _blasphemous_can_cross_gap(self, logic, player, number: int):
        if number == 1:
            return self.has_any({"Purified Hand of the Nun", "The Young Mason's Wheel"}, player) or \
                self._blasphemous_can_dawn_jump(logic, player) or \
                    self._blasphemous_can_air_stall(logic, player)
        elif number == 2:
            return self.has_any({"Purified Hand of the Nun", "The Young Mason's Wheel"}, player) or \
                self._blasphemous_can_dawn_jump(logic, player)
        elif number == 3:
            return self.has("Purified Hand of the Nun", player) or \
                self._blasphemous_can_dawn_jump(logic, player) or \
                    (self.has("The Young Mason's Wheel", player) and \
                        self._blasphemous_can_air_stall(logic, player))
        elif number == 4:
            return self.has("Purified Hand of the Nun", player) or \
                self._blasphemous_can_dawn_jump(logic, player)
        elif number == 5:
            return self.has("Purified Hand of the Nun", player) or \
                (self._blasphemous_can_dawn_jump(logic, player) and \
                    self._blasphemous_can_air_stall(logic, player))
        elif number == 6:
            return self.has("Purified Hand of the Nun", player)
        elif number == 7:
            return self.has("Purified Hand of the Nun", player) and \
                (self._blasphemous_can_dawn_jump(logic, player) or \
                    self.has("The Young Mason's Wheel", player) or \
                        self._blasphemous_can_air_stall(logic, player))
        elif number == 8:
            return self.has("Purified Hand of the Nun", player) and \
                (self._blasphemous_can_dawn_jump(logic, player) or \
                    self.has("The Young Mason's Wheel", player))
        elif number == 9:
            return self.has("Purified Hand of the Nun", player) and \
                (self._blasphemous_can_dawn_jump(logic, player) or \
                    self.has("The Young Mason's Wheel", player) and \
                        self._blasphemous_can_air_stall(logic, player))
        elif number == 10:
            return self.has("Purified Hand of the Nun", player) and \
                self._blasphemous_can_dawn_jump(logic, player)
        elif number == 11:
            return self.has("Purified Hand of the Nun", player) and \
                self._blasphemous_can_dawn_jump(logic, player) and \
                    self._blasphemous_can_air_stall(logic, player)
    
    def _blasphemous_can_ride_albero_elevator(self, player):
        return self.has("D02Z02S11[NW]", player) or \
            self.has("D02Z02S11[NE]", player) or \
                self.has("D02Z02S11[W]", player) or \
                    self.has("D02Z02S11[E]", player) or \
                        self.has("D02Z02S11[SE]", player)
        
    def _blasphemous_opened_dc_gate_w(self, player):
        return self.has("D01Z05S24[W]", player) or \
            self.has("D01Z05S24[E]", player)
    
    def _blasphemous_opened_dc_gate_e(self, player):
        return self.has("D01Z05S12[W]", player) or \
            self.has("D01Z05S12[E]", player)
    
    def _blasphemous_opened_dc_ladder(self, player):
        return self.has("D01Z05S20[W]", player) or \
            self.has("D01Z05S20[N]", player)
    
    def _blasphemous_opened_wotw_cave(self, player):
        return self.has("D02Z01S06[E]", player) or \
            self.has("Wall Climb Ability", player) and \
                (self.has("D02Z01S06[W]", player) or \
                    self.has("D02Z01S06[Cherubs]", player))
    
    def _blasphemous_rode_gotp_elevator(self, player):
        return self.has("D02Z02S11[NW]", player) or \
            self.has("D02Z02S11[NE]", player) or \
                self.has("D02Z02S11[W]", player) or \
                    self.has("D02Z02S11[E]", player) or \
                        self.has("D02Z02S11[SE]", player)
    
    def _blasphemous_opened_convent_ladder(self, player):
        return self.has("D02Z03S11[S]", player) or \
            self.has("D02Z03S11[W]", player) or \
                self.has("D02Z03S11[NW]", player) or \
                    self.has("D02Z03S11[E]", player) or \
                        self.has("D02Z03S11[NE]", player)
    
    def _blasphemous_broke_jondo_bell_w(self, player):
        return self.has("D03Z02S09[S]", player) or \
            self.has("D03Z02S09[W]", player) and \
                self.has("Dash Ability", player) or \
                    self.has("D03Z02S09[N]", player) or \
                        self.has("D03Z02S09[Cherubs]", player)
    
    def _blasphemous_broke_jondo_bell_e(self, logic, enemy, player):
        return self.has("D03Z02S05[S]", player) or \
            self.has("D03Z02S05[E]", player) or \
                self.has("D03Z02S05[W]", player) and \
                    (self._blasphemous_can_cross_gap(logic, player, 5) or \
                        self._blasphemous_can_enemy_bounce(logic, enemy) and \
                            self._blasphemous_can_cross_gap(logic, player, 3))
    
    def _blasphemous_opened_mom_ladder(self, player):
        return self.has("D04Z02S06[NW]", player) or \
            self.has("D04Z02S06[NE]", player) or \
                self.has("D04Z02S06[N]", player) or \
                    self.has("D04Z02S06[S]", player)
    
    def _blasphemous_opened_tsc_gate(self, player):
        return self.has("D05Z02S11[W]", player) or \
            self.has("D05Z02S11[Cherubs]", player)
    
    def _blasphemous_opened_ar_ladder(self, player):
        return self.has("D06Z01S23[Sword]", player) or \
            self.has("D06Z01S23[E]", player) or \
                self.has("D06Z01S23[S]", player) or \
                    self.has("D06Z01S23[Cherubs]", player)
    
    def _blasphemous_broke_bottc_statue(self, player):
        return self.has("D08Z01S02[NE]", player) or \
            self.has("D08Z01S02[SE]", player)
    
    def _blasphemous_opened_wothp_gate(self, player):
        return self.has("D09Z01S05[W]", player) or \
            self.has("D09Z01S05[SE]", player) or \
                self.has("D09Z01S05[NE]", player)

    def _blasphemous_opened_botss_ladder(self, player):
        return self.has("D17Z01S04[N]", player) or \
            self.has("D17Z01S04[FrontR]", player)
    
    def _blasphemous_upwarp_skips_allowed(self, logic):
        return True if logic.value >= 2 else False
        
    def _blasphemous_mourning_skips_allowed(self, logic):
        return True if logic.value >= 2 else False
        
    def _blasphemous_enemy_skips_allowed(self, logic, enemy):
        return True if logic.value >= 2 and enemy.value == 0 else False
        
    def _blasphemous_unknown_skips_allowed(self):
        return False
    
    def _blasphemous_precise_skips_allowed(self):
        return False

    
    def _blasphemous_can_beat_boss(self, boss: str, logic, player):
        def has_boss_strength(name: str) -> bool:
            silver: int = self.count("Quicksilver", player) if self.has("D01Z05S27[E]", player) else 0
            flasks: int = self.count("Empty Bile Flask", player) if \
                (self.has("D01Z05S18[E]", player) or self.has("D02Z02S09[E]", player) or \
                self.has("D03Z02S14[E]", player) or self.has("D03Z03S03[SE]", player) or \
                self.has("D04Z02S13[W]", player) or self.has("D05Z01S12[E]", player) or \
                self.has("D20Z01S08[W]", player)) else 0

            playerStrength: float = self.count("Life Upgrade", player) * 0.25 / 6 + \
                self.count("Mea Culpa Upgrade", player) * 0.25 / 7 + self.count("Fervour Upgrade", player) * 0.20 / 6 \
                + flasks * 0.15 / 8 + silver * 0.15 / 5
            
            bossStrength: float

            if name == "warden":
                bossStrength = -0.10
            elif name == "ten-piedad":
                bossStrength = 0.05
            elif name == "charred-visage":
                bossStrength = 0.20
            elif name == "tres-angustias":
                bossStrength = 0.15
            elif name == "esdras":
                bossStrength = 0.25
            elif name == "melquiades":
                bossStrength = 0.25
            elif name == "exposito":
                bossStrength = 0.30
            elif name == "quirce":
                bossStrength = 0.35
            elif name == "crisanta":
                bossStrength = 0.50
            elif name == "isidora":
                bossStrength = 0.70
            elif name == "sierpes":
                bossStrength = 0.70
            elif name == "amanecida":
                bossStrength = 0.60
            elif name == "laudes":
                bossStrength = 0.60
            elif name == "perpetua":
                bossStrength = -0.05
            elif name == "legionary":
                bossStrength = 0.20

            return playerStrength >= (bossStrength - 0.10 if logic.value >= 2 else (bossStrength if logic.value >= 1 else bossStrength + 0.10))
        
        if boss == "Brotherhood":
            return has_boss_strength("warden") and \
                (self.has("D17Z01S11[W]", player) or \
                    self.has("D17Z01S11[E]", player))
        elif boss == "Mercy":
            return has_boss_strength("ten-piedad") and \
                (self.has("D01Z04S18[W]", player) or \
                    self.has("D01Z04S18[E]", player))
        elif boss == "Convent":
            return has_boss_strength("charred-visage") and \
                (self.has("D02Z03S20[W]", player) or \
                    self.has("D02Z03S20[E]", player))
        elif boss == "Grievance":
            return has_boss_strength("tres-angustias") and \
                self.has_any({"Wall Climb Ability", "Purified Hand of the Nun"}, player) and \
                    (self.has("D03Z03S15[W]", player) or \
                        self.has("D03Z03S15[E]", player))
        elif boss == "Bridge":
            return has_boss_strength("esdras") and \
                (self.has("D08Z01S01[W]", player) or \
                    self.has("D08Z01S01[E]", player))
        elif boss == "Mothers":
            return has_boss_strength("melquiades") and \
                (self.has("D04Z02S22[W]", player) or \
                    self.has("D04Z02S22[E]", player))
        elif boss == "Canvases":
            return has_boss_strength("exposito") and \
                (self.has("D05Z02S14[W]", player) or \
                    self.has("D05Z02S14[E]", player))
        elif boss == "Prison":
            return has_boss_strength("quirce") and \
                (self.has("D09Z01S03[W]", player) or \
                    self.has("D09Z01S03[N]", player))
        elif boss == "Rooftops":
            return has_boss_strength("crisanta") and \
                (self.has("D06Z01S25[W]", player) or \
                    self.has("D06Z01S25[E]", player))
        elif boss == "Ossuary":
            return has_boss_strength("isidora") and \
                self.has("D01BZ08S01[W]", player)
        elif boss == "Mourning":
            return has_boss_strength("sierpes") and \
                self.has("D20Z02S08[E]", player)
        elif boss == "Graveyard":
            return has_boss_strength("amanecida") and \
                self.has("D01BZ07S01[Santos]", player) and \
                    self.has("D02Z03S23[E]", player) and \
                        self.has("D02Z02S14[W]", player) and \
                            self.has("Wall Climb Ability", player)
        elif boss == "Jondo":
            return has_boss_strength("amanecida") and \
                self.has("D01BZ07S01[Santos]", player) and \
                    (self.has("D20Z01S05[W]", player) or \
                        self.has("D20Z01S05[E]", player)) and \
                            (self.has("D03Z01S03[W]", player) or \
                                self.has("D03Z01S03[SW]", player))
        elif boss == "Patio":
            return has_boss_strength("amanecida") and \
                self.has("D01BZ07S01[Santos]", player) and \
                    self.has("D06Z01S18[E]", player) and \
                        (self.has("D04Z01S04[W]", player) or \
                            self.has("D04Z01S04[E]", player)) or \
                                self.has("D04Z01S04[Cherubs]", player)
        elif boss == "Wall":
            return has_boss_strength("amanecida") and \
                self.has("D01BZ07S01[Santos]", player) and \
                    self.has("D09BZ01S01[Cell24]", player) and \
                        (self.has("D09Z01S01[W]", player) or \
                            self.has("D09Z01S01[E]", player))
        elif boss == "Hall":
            return has_boss_strength("laudes") and \
                (self.has("D08Z03S03[W]", player) or \
                    self.has("D08Z03S03[E]", player))
        elif boss == "Perpetua":
            return has_boss_strength("perpetua")
        elif boss == "Legionary":
            return has_boss_strength("legionary")
        
    def _blasphemous_guilt_rooms(self, player, number: int):
        total: int = 0

        if self.has("D01Z04S17[W]", player):
            total += 1
        if self.has("D02Z02S06[E]", player):
            total += 1
        if self.has("D03Z03S14[W]", player):
            total += 1
        if self.has("D04Z02S17[W]", player):
            total += 1
        if self.has("D05Z01S17[W]", player):
            total += 1
        if self.has("D09Z01S13[E]", player):
            total += 1
        if self.has("D17Z01S12[E]", player):
            total += 1

        return True if total >= number else False

    def _blasphemous_sword_rooms(self, player, number: int):
        total: int = 0

        if self.has("D01Z02S06[W]", player) or self.has("D01Z02S06[E]", player):
            total += 1
        if self.has("D01Z05S24[W]", player) or self.has("D01Z05S24[E]", player):
            total += 1
        if self.has("D02Z03S13[W]", player):
            total += 1
        if self.has("D04Z02S12[W]", player):
            total += 1
        if self.has("D05Z01S13[E]", player):
            total += 1
        if self.has("D06Z01S11[W]", player):
            total += 1
        if self.has("D17Z01S08[E]", player):
            total += 1

        return True if total >= number else False
    
    def _blasphemous_redento(self, world, player, number: int):
        if number == 1:
            return self.has("D03Z01S03[W]", player) or \
                self.has("D03Z01S03[SW]", player)
        elif number == 2:
            return (self.has("D03Z01S03[W]", player) or \
                self.has("D03Z01S03[SW]", player)) and \
                    self.has("OpenedBOTSSLadder", player)
        elif number == 3:
            return (self.has("D03Z01S03[W]", player) or \
                self.has("D03Z01S03[SW]", player)) and \
                    self.has("OpenedBOTSSLadder", player) and \
                            self.can_reach(world.multiworld.get_region("D01Z03S06", player))
        elif number == 4:
            return (self.has("D03Z01S03[W]", player) or \
                self.has("D03Z01S03[SW]", player)) and \
                    self.has("OpenedBOTSSLadder", player) and \
                            self.can_reach(world.multiworld.get_region("D01Z03S06", player)) and \
                                self.can_reach(world.multiworld.get_region("D04Z01S04", player))
        elif number == 5:
            return (self.has("D03Z01S03[W]", player) or \
                self.has("D03Z01S03[SW]", player)) and \
                    self.has("OpenedBOTSSLadder", player) and \
                            self.can_reach(world.multiworld.get_region("D01Z03S06", player)) and \
                                self.can_reach(world.multiworld.get_region("D04Z01S04", player)) and \
                                    self.can_reach(world.multiworld.get_region("D04Z02S20", player)) and \
                                        self.has_all({"Little Toe made of Limestone", "Big Toe made of Limestone", "Fourth Toe made of Limestone"}, player) and \
                                            self.has("Knot of Rosary Rope", player) and \
                                                self.has("D17Z01S09[E]", player)

    def _blasphemous_miriam(self, player):
        return self.has("D02Z03S24[E]", player) and \
            self.has("D03Z03S19[E]", player) and \
                self.has("D04Z04S02[W]", player) and \
                    self.has("D05Z01S24[E]", player) and \
                        self.has("D06Z01S26[W]", player)
        
    def _blasphemous_amanecida_rooms(self, world, logic, player, number: int):
        total: int = 0

        if self._blasphemous_can_beat_boss("Graveyard", logic, player):
            total += 1
        if self._blasphemous_can_beat_boss("Jondo", logic, player):
            total += 1
        if self._blasphemous_can_beat_boss("Patio", logic, player):
            total += 1
        if self._blasphemous_can_beat_boss("Wall", logic, player):
            total += 1

        return True if total >= number else False
    
    def _blasphemous_chalice_rooms(self, player, number: int):
        total: int = 0

        if self.has("D03Z01S01[W]", player) or self.has("D03Z01S01[NE]", player) or self.has("D03Z01S01[S]", player):
            total += 1
        if self.has("D05Z02S01[W]", player) or self.has("D05Z02S01[E]", player):
            total += 1
        if self.has("D09Z01S07[SW]", player) or self.has("D09Z01S07[SE]", player) or self.has("D09Z01S07[W]", player) or self.has("D09Z01S07[E]", player):
            total += 1

        return True if total >= number else False


def rules(blasphemousworld):
    world = blasphemousworld.multiworld
    player = blasphemousworld.player
    difficulty = world.difficulty[player]
    enemy = world.enemy_randomizer[player]


    # D01Z01S01 (The Holy Line)
    # No items
    # Doors
    set_rule(world.get_entrance("D01Z01S01[S]", player),
        lambda state: state._blasphemous_can_break_holes(player) or \
            state.has("Purified Hand of the Nun", player))


    # D01Z01S02 (The Holy Line)
    # Items
    set_rule(world.get_location("THL: Across blood platforms", player),
        lambda state: state.has_any({"Blood Perpetuated in Sand", "Purified Hand of the Nun"}, player))
    # No doors


    # D01Z01S03 (The Holy Line)
    # Items
    set_rule(world.get_location("THL: Underground chest", player),
        lambda state: state.has_all({"Blood Perpetuated in Sand", "Dash Ability"}, player) and \
            state._blasphemous_can_water_jump(player))
    # No doors


    # D01Z02S01 (Albero)
    # Items
    set_rule(world.get_location("Albero: Bless Linen Cloth", player),
        lambda state: state.has("Linen Cloth", player))
    set_rule(world.get_location("Albero: Bless Hatched Egg", player),
        lambda state: state.has("Hatched Egg of Deformity", player))
    set_rule(world.get_location("Albero: Bless Severed Hand", player),
        lambda state: state.has("Severed Hand", player))
    # No doors


    # D01Z02S02 (Albero)
    # Items
    set_rule(world.get_location("Albero: Tirso's 1st reward", player),
        lambda state: state.has_group("tirso", player, 1))
    set_rule(world.get_location("Albero: Tirso's 2nd reward", player),
        lambda state: state.has_group("tirso", player, 2))
    set_rule(world.get_location("Albero: Tirso's 3rd reward", player),
        lambda state: state.has_group("tirso", player, 3))
    set_rule(world.get_location("Albero: Tirso's 4th reward", player),
        lambda state: state.has_group("tirso", player, 4))
    set_rule(world.get_location("Albero: Tirso's 5th reward", player),
        lambda state: state.has_group("tirso", player, 5))
    set_rule(world.get_location("Albero: Tirso's 6th reward", player),
        lambda state: state.has_group("tirso", player, 6))
    set_rule(world.get_location("Albero: Tirso's final reward", player),
        lambda state: state.has_group("tirso", player, 6) and \
            state._blasphemous_can_beat_boss("Mercy", difficulty, player) and \
                state._blasphemous_can_beat_boss("Convent", difficulty, player) and \
                    state._blasphemous_can_beat_boss("Grievance", difficulty, player) and \
                        state._blasphemous_can_beat_boss("Mothers", difficulty, player) and \
                            state._blasphemous_can_beat_boss("Canvases", difficulty, player) and \
                                state._blasphemous_can_beat_boss("Prison", difficulty, player))
    # No doors


    # D01Z02S03 (Albero)
    # Items
    set_rule(world.get_location("Albero: Child of Moonlight", player),
        lambda state: state.has("RodeGOTPElevator", player) or \
            state._blasphemous_pillar(player) or \
                state.has("Cante Jondo of the Three Sisters", player) or \
                    state.has("D01Z02S03[NW]", player) and \
                        (state._blasphemous_can_cross_gap(difficulty, player, 2) or \
                            state.has("Lorquiana", player) or \
                                state._blasphemous_aubade(player) or \
                                    state.has("Cantina of the Blue Rose", player) or \
                                        state._blasphemous_can_air_stall(difficulty, player) or \
                                            state._blasphemous_charge_beam(player)))
    set_rule(world.get_location("Albero: Lvdovico's 1st reward", player),
        lambda state: state.has_group("tentudia", player, 1))
    set_rule(world.get_location("Albero: Lvdovico's 2nd reward", player),
        lambda state: state.has_group("tentudia", player, 2))
    set_rule(world.get_location("Albero: Lvdovico's 3rd reward", player),
        lambda state: state.has_group("tentudia", player, 3))
    set_rule(world.get_location("Albero: First gift for Cleofas", player),
        lambda state: state.has("D04Z02S10[W]", player))
    # Doors
    set_rule(world.get_entrance("D01Z02S03[NW]", player),
        lambda state: state.has("D02Z02S11[NW]", player) or \
            state.has("D02Z02S11[NE]", player) or \
                state.has("D02Z02S11[W]", player) or \
                    state.has("D02Z02S11[E]", player) or \
                        state.has("D02Z02S11[SE]", player))
    set_rule(world.get_entrance("D01Z02S03[church]", player),
        lambda state: state._blasphemous_can_beat_boss("Mercy", difficulty, player) or \
            state._blasphemous_can_beat_boss("Convent", difficulty, player) or \
                state._blasphemous_can_beat_boss("Grievance", difficulty, player))


    # D01BZ04S01 (Albero: Inside church)
    # Items
    set_rule(world.get_location("Albero: Final gift for Cleofas", player),
        lambda state: state.has_group("marks", player, 3) and \
            state.has("Cord of the True Burying", player) and \
                state.has("D04Z02S10[W]", player) and \
                    state.has("D06Z01S18[E]", player))
    # No doors


    # D01BZ06S01 (Ossuary)
    # Items
    set_rule(world.get_location("Ossuary: 1st reward", player),
        lambda state: state.has_group("bones", player, 4))
    set_rule(world.get_location("Ossuary: 2nd reward", player),
        lambda state: state.has_group("bones", player, 8))
    set_rule(world.get_location("Ossuary: 3rd reward", player),
        lambda state: state.has_group("bones", player, 12))
    set_rule(world.get_location("Ossuary: 4th reward", player),
        lambda state: state.has_group("bones", player, 16))
    set_rule(world.get_location("Ossuary: 5th reward", player),
        lambda state: state.has_group("bones", player, 20))
    set_rule(world.get_location("Ossuary: 6th reward", player),
        lambda state: state.has_group("bones", player, 24))
    set_rule(world.get_location("Ossuary: 7th reward", player),
        lambda state: state.has_group("bones", player, 28))
    set_rule(world.get_location("Ossuary: 8th reward", player),
        lambda state: state.has_group("bones", player, 32))
    set_rule(world.get_location("Ossuary: 9th reward", player),
        lambda state: state.has_group("bones", player, 36))
    set_rule(world.get_location("Ossuary: 10th reward", player),
        lambda state: state.has_group("bones", player, 40))
    set_rule(world.get_location("Ossuary: 11th reward", player),
        lambda state: state.has_group("bones", player, 44))
    # Doors
    set_rule(world.get_entrance("D01BZ06S01[E]", player),
        lambda state: state.has_group("bones", player, 30))


    # D01BZ08S01 (Isidora)
    # Items
    set_rule(world.get_location("Ossuary: Isidora, Voice of the Dead", player),
        lambda state: state._blasphemous_can_beat_boss("Ossuary", difficulty, player))
    # No doors


    # D01Z03S01 (Wasteland of the Buried Churches)
    # Items
    set_rule(world.get_location("WotBC: Lower log path", player),
        lambda state: state.has("D01Z03S01[SE]", player))
    # No doors


    # D01Z03S02 (Wasteland of the Buried Churches)
    # Items
    set_rule(world.get_location("WotBC: Hidden alcove", player),
        lambda state: state.has("Dash Ability", player))
    # No doors (shouldn't there be one though?)


    # D01Z03S03 (Wasteland of the Buried Churches)
    # No items
    # Doors
    set_rule(world.get_entrance("D01Z03S03[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D01Z03S05 (Wasteland of the Buried Churches)
    # Items
    set_rule(world.get_location("WotBC: Under broken bridge", player),
        lambda state: state.has_any({"Blood Perpetuated in Sand", "Boots of Pleading"}, player) or \
            state._blasphemous_can_cross_gap(difficulty, player, 3))
    # Doors
    set_rule(world.get_entrance("D01Z03S05[Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D01Z03S06 (Wasteland of the Buried Churches)
    # Items
    set_rule(world.get_location("WotBC: 3rd meeting with Redento", player),
        lambda state: state._blasphemous_redento(blasphemousworld, player, 3))
    # No doors


    # D01Z03S07 (Wasteland of the Buried Churches)
    # Items
    set_rule(world.get_location("WotBC: Cliffside Child of Moonlight", player),
        lambda state: state._blasphemous_can_cross_gap(difficulty, player, 1) or \
            state._blasphemous_aubade(player) or \
                state._blasphemous_charge_beam(player) or \
                    state.has_any({"Lorquiana", "Cante Jondo of the Three Sisters", "Cantina of the Blue Rose", "Cloistered Ruby"}, player))
    # Doors
    set_rule(world.get_entrance("D01Z03S07[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))

    
    # D01Z04S01 (Mercy Dreams)
    # No items
    # Doors
    set_rule(world.get_entrance("D01Z04S01[SE]", player),
        lambda state: state.has("D01Z04S01[S]", player))
    set_rule(world.get_entrance("D01Z04S01[S]", player),
        lambda state: state.has("D01Z04S01[SE]", player))


    # D01Z04S09 (Mercy Dreams)
    # No items
    # Doors
    set_rule(world.get_entrance("D01Z04S09[W]", player),
        lambda state: state.has("OpenedDCGateE", player))


    # D01Z04S13 (Mercy Dreams)
    # Items
    set_rule(world.get_location("MD: Behind gate to TSC", player),
        lambda state: state.has("D01Z04S13[SE]", player) or \
            state._blasphemous_can_dive_laser(difficulty, player) and \
                (state._blasphemous_can_air_stall(difficulty, player) or \
                    state.has_any({"The Young Mason's Wheel", "Purified Hand of the Nun"}, player) or \
                        state._blasphemous_can_enemy_bounce(difficulty, enemy)))
    # Doors
    set_rule(world.get_entrance("D01Z04S13[SE]", player),
        lambda state: state._blasphemous_can_dive_laser(difficulty, player) and \
            (state._blasphemous_can_air_stall(difficulty, player) or \
                state.has_any({"The Young Mason's Wheel", "Purified Hand of the Nun"}, player) or \
                    state._blasphemous_can_enemy_bounce(difficulty, enemy)))


    # D01Z04S14 (Mercy Dreams)
    # Items
    set_rule(world.get_location("MD: Sliding challenge", player),
        lambda state: state.has("Dash Ability", player))
    # No doors


    # D01Z04S15 (Mercy Dreams)
    # No items
    # Doors
    set_rule(world.get_entrance("D01Z04S15[W]", player),
        lambda state: state.has("D01Z04S15[E]", player) or \
            state.has("D01Z04S15[SW]", player) or \
                state.has("D01Z04S15[SE]", player))
    set_rule(world.get_entrance("D01Z04S15[E]", player),
        lambda state: state.has("D01Z04S15[W]", player) or \
            state.has("D01Z04S15[SW]", player) or \
                state.has("D01Z04S15[SE]", player))
    set_rule(world.get_entrance("D01Z04S15[SW]", player),
        lambda state: state.has("D01Z04S15[W]", player) or \
            state.has("D01Z04S15[E]", player) or \
                state.has("D01Z04S15[SE]", player))
    set_rule(world.get_entrance("D01Z04S15[SE]", player),
        lambda state: state.has("D01Z04S15[W]", player) or \
            state.has("D01Z04S15[E]", player) or \
                state.has("D01Z04S15[SW]", player))


    # D01Z04S16 (Mercy Dreams)
    # Items
    set_rule(world.get_location("MD: Cave Child of Moonlight", player),
        lambda state: state.has_any({"Purified Hand of the Nun", "Cante Jondo of the Three Sisters"}, player) or \
            state._blasphemous_pillar(player) or \
                state._blasphemous_tirana(player))
    # No doors


    # D01Z04S18 (Ten Piedad)
    # Items
    set_rule(world.get_location("MD: Ten Piedad", player),
        lambda state: state._blasphemous_can_beat_boss("Mercy", difficulty, player))
    # Doors
    set_rule(world.get_entrance("D01Z04S18[W]", player),
        lambda state: state._blasphemous_can_beat_boss("Mercy", difficulty, player))
    set_rule(world.get_entrance("D01Z04S18[E]", player),
        lambda state: state._blasphemous_can_beat_boss("Mercy", difficulty, player))


    # D01Z05S02 (Desecrated Cistern)
    # No items
    # Doors
    set_rule(world.get_entrance("D01Z05S02[S]", player),
        lambda state: state.has("OpenedDCLadder", player))


    # D01Z05S05 (Desecrated Cistern)
    # Items
    set_rule(world.get_location("DC: Hidden alcove near fountain", player),
        lambda state: state.has("Dash Ability", player) and \
            state._blasphemous_can_water_jump(player))
    # No doors


    # D01Z05S06 (Desecrated Cistern)
    # Items
    set_rule(world.get_location("DC: Upper east tunnel chest", player),
        lambda state: state.has("D01Z05S06[Cherubs]", player) or \
            state._blasphemous_can_water_jump(player))
    set_rule(world.get_location("DC: Upper east Child of Moonlight", player),
        lambda state: state.has("D01Z05S06[Cherubs]", player) or \
            state._blasphemous_can_water_jump(player) or \
                state._blasphemous_pillar(player) or \
                    state.has("Cante Jondo of the Three Sisters", player) or \
                        state._blasphemous_aubade(player) or \
                            state._blasphemous_tirana(player) or \
                                state._blasphemous_can_air_stall(difficulty, player))
    # No doors


    # D01Z05S12 (Desecrated Cistern)
    # Event
    set_rule(world.get_location("OpenedDCGateE", player),
        lambda state: state._blasphemous_opened_dc_gate_e(player))


    # D01Z05S13 (Desecrated Cistern)
    # Items
    set_rule(world.get_location("DC: Child of Moonlight, behind pillar", player),
        lambda state: state.has("D01Z05S13[SW]", player) or \
            state.has("D01Z05S13[E]", player) and \
                state._blasphemous_can_survive_poison(difficulty, player, 3) and \
                    state._blasphemous_can_water_jump(player))
    # Doors
    set_rule(world.get_entrance("D01Z05S13[SW]", player),
        lambda state: state.has("D01Z05S13[E]", player))
    add_rule(world.get_entrance("D01Z05S13[SW]", player),
        lambda state: state._blasphemous_can_survive_poison(difficulty, player, 3) and \
            state._blasphemous_can_water_jump(player))
    set_rule(world.get_entrance("D01Z05S13[N]", player),
        lambda state: state.has("D01Z05S13[E]", player))
    add_rule(world.get_entrance("D01Z05S13[N]", player),
        lambda state: state._blasphemous_can_survive_poison(difficulty, player, 3) and \
            state._blasphemous_can_water_jump(player))


    # D01Z05S17 (Desecrated Cistern)
    # Items
    set_rule(world.get_location("DC: High ledge near elevator shaft", player),
        lambda state: state.has("D01Z05S17[E]", player) or \
            state._blasphemous_can_water_jump(player) or \
                state._blasphemous_can_cross_gap(difficulty, player, 5))
    # Doors
    set_rule(world.get_entrance("D01Z05S17[E]", player),
        lambda state: state.has("Dash Ability", player) and \
            (state._blasphemous_can_water_jump(player) or \
                state._blasphemous_can_cross_gap(difficulty, player, 5)))
    

    # D01Z05S20 (Desecrated Cistern)
    # Event
    set_rule(world.get_location("OpenedDCLadder", player),
        lambda state: state._blasphemous_opened_dc_ladder(player))


    # D01Z05S21 (Desecrated Cistern)
    # No items
    # Doors
    set_rule(world.get_entrance("D01Z05S21[Reward]", player),
        lambda state: state.has("Shroud of Dreamt Sins", player))


    # D01Z05S23 (Desecrated Cistern)
    # No items
    # Doors
    set_rule(world.get_entrance("D01Z05S23[W]", player),
        lambda state: state._blasphemous_chalice_rooms(player, 3) and \
            state.has("Chalice of Inverted Verses", player))
    

    # D01Z05S24 (Desecrated Cistern)
    # Event
    set_rule(world.get_location("OpenedDCGateW", player),
        lambda state: state._blasphemous_opened_dc_gate_w(player))


    # D01Z05S25 (Desecrated Cistern)
    # Items
    set_rule(world.get_location("DC: Elevator shaft ledge", player),
        lambda state: state.has("Linen of Golden Thread", player))
    set_rule(world.get_location("DC: Elevator shaft Child of Moonlight", player),
        lambda state: state.has("Linen of Golden Thread", player) or \
            (state._blasphemous_pillar(player) and \
                (state.has("D01Z05S25[E]", player) or \
                    state.has("D01Z05S25[W]", player) and \
                        (state._blasphemous_can_walk_on_root(player) or \
                            state._blasphemous_can_cross_gap(difficulty, player, 3)))))
    # Doors
    set_rule(world.get_entrance("D01Z05S25[NE]", player),
        lambda state: state.has("Linen of Golden Thread", player) or \
            state.has("D01Z05S25[SW]", player) or \
                state.has("D01Z05S25[SE]", player))
    set_rule(world.get_entrance("D01Z05S25[W]", player),
        lambda state: (state.has("Linen of Golden Thread", player) and \
            (state._blasphemous_can_walk_on_root(player) or \
                state.has("Purified Hand of the Nun", player) or \
                    state._blasphemous_can_air_stall(difficulty, player))) or \
                        (state.has("D01Z05S25[E]", player) and \
                            (state._blasphemous_can_walk_on_root(player) or \
                                state._blasphemous_can_cross_gap(difficulty, player, 3))))
    set_rule(world.get_entrance("D01Z05S25[E]", player),
        lambda state: state._blasphemous_can_break_tirana(difficulty, player) and \
            (state.has("Linen of Golden Thread", player) or \
                state.has("D01Z05S25[W]", player) and \
                    (state._blasphemous_can_walk_on_root(player) or \
                        state._blasphemous_can_cross_gap(difficulty, player, 3))))
    set_rule(world.get_entrance("D01Z05S25[SW]", player),
        lambda state: state.has("D01Z05S25[SE]", player) or \
            state.has("D01Z05S25[NE]", player) or \
                state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D01Z05S25[SE]", player),
        lambda state: state.has("D01Z05S25[SW]", player) or \
            state.has("D01Z05S25[NE]", player) or \
                state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D01Z05S25[EchoesW]", player),
        lambda state: state.has("D01Z05S25[EchoesE]", player))
    add_rule(world.get_entrance("D01Z05S25[EchoesW]", player),
        lambda state: (state.has("D01Z05S25[EchoesE]", player) and \
            (state.has("Blood Perpetuated in Sand", player) or \
                state._blasphemous_can_cross_gap(difficulty, player, 8))) or \
                    state.has_all({"Linen of Golden Thread", "Purified Hand of the Nun"}, player))
    set_rule(world.get_entrance("D01Z05S25[EchoesE]", player),
        lambda state: state.has("D01Z05S25[EchoesW]", player))
    add_rule(world.get_entrance("D01Z05S25[EchoesE]", player),
        lambda state: (state.has("D01Z05S25[EchoesW]", player) and \
            (state.has("Blood Perpetuated in Sand", player) or \
                state._blasphemous_can_cross_gap(difficulty, player, 8))) or \
                    state.has_all({"Linen of Golden Thread", "Purified Hand of the Nun"}, player))


    # D01Z06S01 (Petrous)
    # No items
    # Doors
    set_rule(world.get_entrance("D01Z06S01[Santos]", player),
        lambda state: state.has("Petrified Bell", player))


    # D02Z01S01 (Where Olive Trees Wither)
    # Items
    set_rule(world.get_location("WOTW: Below Prie Dieu", player),
        lambda state: state.has("D02Z01S01[W]", player) or \
            state.has("D02Z01S01[CherubsL]", player) or \
                state.has("D02Z01S01[SW]", player) or \
                    state.has("D02Z01S01[CherubsR]", player) or \
                        state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))
    set_rule(world.get_location("WOTW: Gemino's gift", player),
        lambda state: state.has("D02Z01S01[W]", player) or \
            state.has("D02Z01S01[CherubsL]", player) or \
                state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player) or \
                    ((state.has("D02Z01S01[SW]", player) or \
                        state.has("D02Z01S01[CherubsR]", player)) and \
                            state._blasphemous_can_dawn_jump(difficulty, player)))
    set_rule(world.get_location("WOTW: Gemino's reward", player),
        lambda state: state.has("Golden Thimble Filled with Burning Oil", player) and \
            (state.has("D02Z01S01[W]", player) or \
                state.has("D02Z01S01[CherubsL]", player) or \
                    state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player) or \
                        ((state.has("D02Z01S01[SW]", player) or \
                            state.has("D02Z01S01[CherubsR]", player)) and \
                                state._blasphemous_can_dawn_jump(difficulty, player))))
    # Doors
    set_rule(world.get_entrance("D02Z01S01[SW]", player),
        lambda state: state.has("OpenedWOTWCave", player) and \
            (state.has("D02Z01S01[W]", player) or \
                state.has("D02Z01S01[CherubsL]", player) or \
                    state.has("D02Z01S01[CherubsR]", player) or \
                        state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)))
    set_rule(world.get_entrance("D02Z01S01[W]", player),
        lambda state: state.has("D02Z01S01[CherubsL]", player) or \
            state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player) or \
                ((state.has("D02Z01S01[SW]", player) or \
                    state.has("D02Z01S01[CherubsR]", player)) and \
                        state._blasphemous_can_dawn_jump(difficulty, player)))


    # D02Z01S02 (Where Olive Trees Wither)
    # Items
    set_rule(world.get_location("WOTW: Upper east Child of Moonlight", player),
        lambda state: state.has("D02Z01S02[NE]", player) or \
            (state.has("D02Z01S02[NW]", player) or \
                state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)) and \
                    (state._blasphemous_can_walk_on_root(player) or \
                        state._blasphemous_can_cross_gap(difficulty, player, 4) or \
                            state._blasphemous_pillar(player)))
    # Doors
    set_rule(world.get_entrance("D02Z01S02[NW]", player),
        lambda state: state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player) or \
            (state.has("D02Z01S02[NE]", player) and \
                state._blasphemous_can_walk_on_root(player) and \
                    state._blasphemous_can_cross_gap(difficulty, player, 5)))
    set_rule(world.get_entrance("D02Z01S02[NE]", player),
        lambda state: (state.has("Purified Hand of the Nun", player) and \
            state._blasphemous_can_enemy_bounce(difficulty, enemy)) or \
                (state.has("D02Z01S02[NW]", player) or \
                    state.has("Wall Climb Ability", player) or \
                        state.has("Purified Hand of the Nun", player)) and \
                            (state._blasphemous_can_walk_on_root(player) or \
                                state._blasphemous_can_cross_gap(difficulty, player, 10)))
    set_rule(world.get_entrance("D02Z01S02[]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D02Z01S03 (Where Olive Trees Wither)
    # No items
    # Doors
    set_rule(world.get_entrance("D02Z01S03[W]", player),
        lambda state: state.has("D02Z01S03[SE]", player) or \
            state.has("D02Z01S03[Cherubs]", player) or \
                state.has("Wall Climb Ability", player))
    set_rule(world.get_entrance("D02Z01S03[SE]", player),
        lambda state: state.has("D02Z01S03[W]", player) or \
            state.has("D02Z01S03[Cherubs]", player) or \
                state.has("Wall Climb Ability", player))


    # D02Z01S04 (Where Olive Trees Wither)
    # Items
    set_rule(world.get_location("WOTW: Gift for the tomb", player),
        lambda state: state.has("Golden Thimble Filled with Burning Oil", player) and \
            (state.has("D02Z01S01[W]", player) or \
                state.has("D02Z01S01[CherubsL]", player) or \
                    state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player) or \
                        ((state.has("D02Z01S01[SW]", player) or \
                            state.has("D02Z01S01[CherubsR]", player)) and \
                                state._blasphemous_can_dawn_jump(difficulty, player))))
    # Doors
    set_rule(world.get_entrance("D02Z01S04[-N]", player),
        lambda state: state.has("Golden Thimble Filled with Burning Oil", player) and \
            (state.has("D02Z01S01[W]", player) or \
                state.has("D02Z01S01[CherubsL]", player) or \
                    state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player) or \
                        ((state.has("D02Z01S01[SW]", player) or \
                            state.has("D02Z01S01[CherubsR]", player)) and \
                                state._blasphemous_can_dawn_jump(difficulty, player))))


    # D02Z01S06 (Where Olive Trees Wither)
    # Items
    set_rule(world.get_location("WOTW: Underground ledge", player),
        lambda state: state.has_all({"Wall Climb Ability", "Blood Perpetuated in Sand"}, player) and \
            (state.has("Dash Ability", player) or \
                state.has("D02Z01S06[Cherubs]", player)) or \
                    state.has("Purified Hand of the Nun", player) and \
                        (state.has("D02Z01S06[Cherubs]", player) or \
                            state.has("D02Z01S06[E]", player) or \
                                state.has_any({"Wall Climb Ability", "Dash Ability"}, player)))
    set_rule(world.get_location("WOTW: Underground Child of Moonlight", player),
        lambda state: (state.has("D02Z01S06[W]", player) or \
            state.has("Dash Ability", player) or \
                state.has_all({"Purified Hand of the Nun", "Wall Climb Ability"}, player)) and \
                    (state._blasphemous_pillar(player) or \
                        state.has("Cante Jondo of the Three Sisters", player)) or \
                            (state.has("D02Z01S06[W]", player) or \
                                state.has_any({"Purified Hand of the Nun", "Dash Ability"}, player)) and \
                                    state.has("Wall Climb Ability", player) and \
                                        (state.has_any({"Lorquiana", "Cantina of the Blue Rose"}, player) or \
                                            state._blasphemous_aubade(player) or \
                                                state._blasphemous_can_air_stall(difficulty, player)))
    # Doors
    set_rule(world.get_entrance("D02Z01S06[W]", player),
        lambda state: state.has("Dash Ability", player) or \
            state.has_all({"Purified Hand of the Nun", "Wall Climb Ability"}, player))
    set_rule(world.get_entrance("D02Z01S06[E]", player),
        lambda state: state.has("Wall Climb Ability", player))
    # Event
    set_rule(world.get_location("OpenedWOTWCave", player),
        lambda state: state._blasphemous_opened_wotw_cave(player))


    # D02Z01S08 (Where Olive Trees Wither)
    # Items
    set_rule(world.get_location("WOTW: Underground tomb", player),
        lambda state: state.has("Dried Flowers bathed in Tears", player))
    # No doors


    # D02Z01S09 (Where Olive Trees Wither)
    # Items
    set_rule(world.get_location("WOTW: Upper east statue", player),
        lambda state: state._blasphemous_can_walk_on_root(player) or \
            state._blasphemous_can_cross_gap(difficulty, player, 11) or \
                state.has("Purified Hand of the Nun", player) and \
                    state._blasphemous_can_enemy_bounce(difficulty, enemy))
    # Doors
    set_rule(world.get_entrance("D02Z01S09[-CherubsL]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D02Z01S09[-CherubsR]", player),
        lambda state: state.has("Linen of Golden Thread", player) and \
            (state._blasphemous_can_walk_on_root(player) or \
                state._blasphemous_can_cross_gap(difficulty, player, 2) or \
                    state._blasphemous_can_enemy_bounce(difficulty, enemy) and \
                        state._blasphemous_can_air_stall(difficulty, player)))


    # D02Z02S01 (Graveyard of the Peaks)
    # No items
    # Doors
    set_rule(world.get_entrance("D02Z02S01[W]", player),
        lambda state: state.has("D02Z02S01[NW]", player) or \
            state.has("D02Z02S01[Cherubs]", player) or \
                state.has("Dash Ability", player))
    set_rule(world.get_entrance("D02Z02S01[NW]", player),
        lambda state: state.has("D02Z02S01[Cherubs]", player) or \
            state.has("Wall Climb Ability", player) and \
                (state.has("D02Z02S01[W]", player) or \
                    state.has("Dash Ability", player)))
    set_rule(world.get_entrance("D02Z02S01[E]", player),
        lambda state: state.has("D02Z02S01[NW]", player) or \
            state.has("D02Z02S01[Cherubs]", player) or \
                state.has_any({"Wall Climb Ability", "Dash Ability"}, player))


    # D02Z02S02 (Graveyard of the Peaks)
    # Items
    set_rule(world.get_location("GotP: Center shaft Child of Moonlight", player),
        lambda state: state.has("D02Z02S02[CherubsL]", player) or \
            state.has("D02Z02S02[CherubsR]", player) or \
                ((state.has("D02Z02S02[NW]", player) or \
                    state.has("D02Z02S02[NE]", player) or \
                        state.has("Wall Climb Ability", player)) and \
                            (state.has_any({"Purified Hand of the Nun", "Cante Jondo of the Three Sisters"}, player) or \
                                state._blasphemous_pillar(player) or \
                                    state._blasphemous_tirana(player) or \
                                        state._blasphemous_can_dive_laser(difficulty, player))))
    # Doors
    set_rule(world.get_entrance("D02Z02S02[NW]", player),
        lambda state: state.has("D02Z02S02[NE]", player) or \
            state.has("D02Z02S02[CherubsL]", player) or \
                state.has("D02Z02S02[CherubsR]", player) or \
                    state.has("Wall Climb Ability", player))
    set_rule(world.get_entrance("D02Z02S02[NE]", player),
        lambda state: state.has("D02Z02S02[NW]", player) or \
            state.has("D02Z02S02[CherubsL]", player) or \
                state.has("D02Z02S02[CherubsR]", player) or \
                    state.has("Wall Climb Ability", player))
    set_rule(world.get_entrance("D02Z02S02[-CherubsR]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D02Z02S03 (Graveyard of the Peaks)
    # Items
    set_rule(world.get_location("GotP: Lower east shaft", player),
        lambda state: state.has("D02Z02S03[NW]", player) or \
            state.has("D02Z02S03[NE]", player) or \
                state.has("Wall Climb Ability", player) or \
                    state._blasphemous_can_cross_gap(difficulty, player, 2))
    set_rule(world.get_location("GotP: Center east shaft", player),
        lambda state: state.has("D02Z02S03[NW]", player) or \
            state.has("D02Z02S03[NE]", player) or \
                state.has_any({"Wall Climb Ability", "Purified Hand of the Nun"}, player))
    set_rule(world.get_location("GotP: Upper east shaft", player),
        lambda state: (state._blasphemous_can_climb_on_root(player) and \
            state.has("Purified Hand of the Nun", player)) or \
                (state.has("Blood Perpetuated in Sand", player) and \
                    (state.has("Purified Hand of the Nun", player) or \
                        state._blasphemous_can_climb_on_root(player))))
    # Doors
    set_rule(world.get_entrance("D02Z02S03[NW]", player),
        lambda state: state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player) or \
            state.has("D02Z02S03[NE]", player) and \
                state._blasphemous_can_walk_on_root(player))
    set_rule(world.get_entrance("D02Z02S03[NE]", player),
        lambda state: state.has("Wall Climb Ability", player) and \
            (state._blasphemous_can_cross_gap(difficulty, player, 11) or \
                (state.has("Blood Perpetuated in Sand", player) and \
                    (state._blasphemous_can_walk_on_root(player) or \
                        state._blasphemous_can_cross_gap(difficulty, player, 7))) or \
                            (state._blasphemous_can_walk_on_root(player) and \
                                (state.has("Purified Hand of the Nun", player) or \
                                    state._blasphemous_can_air_stall(difficulty, player)))))
    set_rule(world.get_entrance("D02Z02S03[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D02Z02S04 (Graveyard of the Peaks)
    # Items
    set_rule(world.get_location("GotP: Lower west shaft", player),
        lambda state: state.has("D02Z02S04[E]", player))
    set_rule(world.get_location("GotP: Upper west shaft", player),
        lambda state: state.has("D02Z02S04[NE]", player) or \
            ((state.has("D02Z02S04[W]", player) or \
                state.has("D02Z02S04[E]", player) and \
                    state.has("Dash Ability", player)) and \
                        (state.has("Purified Hand of the Nun", player) or \
                            state.has("Wall Climb Ability", player))) or \
                                (state.has("D02Z02S04[SE]", player) and \
                                    (state.has("Wall Climb Ability", player) or \
                                        state.has("Purified Hand of the Nun", player) and \
                                            state._blasphemous_can_enemy_upslash(difficulty, enemy, player))))
    set_rule(world.get_location("GotP: West shaft Child of Moonlight", player),
        lambda state: (state.has("D02Z02S04[NE]", player) or \
            state.has("D02Z02S04[W]", player) or \
                state.has("D02Z02S04[E]", player) and \
                    state.has("Dash Ability", player) or \
                        state.has("D02Z02S04[SE]", player) and \
                            (state.has("Wall Climb Ability", player) or \
                                state.has("Purified Hand of the Nun", player) and \
                                    state._blasphemous_can_enemy_upslash(difficulty, enemy, player))) and \
                                        (state.has("Blood Perpetuated in Sand", player) and \
                                            state.has("Dash Ability", player) or \
                                                state.has("Purified Hand of the Nun", player) and \
                                                    state._blasphemous_can_enemy_bounce(difficulty, enemy) or \
                                                        state.has_any({"Lorquiana", "Cante Jondo of the Three Sisters", "Verdiales of the Forsaken Hamlet", "Cantina of the Blue Rose"}, player) or \
                                                            state._blasphemous_aubade(player)) or \
                                                                (state.has("D02Z02S04[NE]", player) or \
                                                                    state.has("D02Z02S04[W]", player) or \
                                                                        state.has("D02Z02S04[E]", player) and \
                                                                            state.has("Dash Ability", player) or \
                                                                                state.has("D02Z02S04[SE]", player)) and \
                                                                                    state._blasphemous_pillar(player))
    # Doors
    set_rule(world.get_entrance("D02Z02S04[W]", player),
        lambda state: state.has("D02Z02S04[NE]", player) or \
            state.has("D02Z02S04[E]", player) and \
                state.has("Dash Ability", player) or \
                    state.has("D02Z02S04[SE]", player) and \
                        (state.has("Wall Climb Ability", player) or \
                            state.has("Purified Hand of the Nun", player) and \
                                state._blasphemous_can_enemy_upslash(difficulty, enemy, player)))
    set_rule(world.get_entrance("D02Z02S04[SE]", player),
        lambda state: state.has("D02Z02S04[NE]", player) or \
            state.has("D02Z02S04[W]", player) or \
                state.has("Dash Ability", player))
    set_rule(world.get_entrance("D02Z02S04[NE]", player),
        lambda state: ((state.has("D02Z02S04[W]", player) or \
            state.has("D02Z02S04[E]", player) and \
                state.has("Dash Ability", player)) and \
                    state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)) or \
                        (state.has("D02Z02S04[SE]", player) and \
                            (state.has("Wall Climb Ability", player) or \
                                state.has("Purified Hand of the Nun", player) and \
                                    state._blasphemous_can_enemy_upslash(difficulty, enemy, player))))
    set_rule(world.get_entrance("D02Z02S04[-CherubsL]", player),
        lambda state: state.has("Linen of Golden Thread", player) and \
            (state.has("D02Z02S04[NE]", player) or \
                state.has("D02Z02S04[W]", player) or \
                    state.has("D02Z02S04[SE]", player) or \
                        state.has("Dash Ability", player)))


    # D02Z02S05 (Graveyard of the Peaks)
    # Items
    set_rule(world.get_location("GotP: Center shaft ledge", player),
        lambda state: state.has("D02Z02S05[NW]", player) or \
            state.has("Wall Climb Ability", player))
    # Doors
    set_rule(world.get_entrance("D02Z02S05[W]", player),
        lambda state: state.has("Purified Hand of the Nun", player) and \
            state._blasphemous_can_enemy_bounce(difficulty, enemy))
    set_rule(world.get_entrance("D02Z02S05[E]", player),
        lambda state: state.has("D02Z02S05[NW]", player) or \
            state.has("D02Z02S05[E]", player) or \
                state.has("Wall Climb Ability", player))
    set_rule(world.get_entrance("D02Z02S05[NW]", player),
        lambda state: state.has("D02Z02S05[NW]", player) or \
            state.has("Wall Climb Ability", player))
    set_rule(world.get_entrance("D02Z02S05[-CherubsL]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D02Z02S05[-CherubsR]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D02Z02S08 (Graveyard of the Peaks)
    # Items
    set_rule(world.get_location("GotP: Shop cave hidden hole", player),
        lambda state: state.has("D02Z02S08[CherubsR]", player) or \
            state.has("Blood Perpetuated in Sand", player) or \
                state._blasphemous_can_break_holes(player) or \
                    state._blasphemous_can_cross_gap(difficulty, player, 8))
    set_rule(world.get_location("GotP: Shop cave Child of Moonlight", player),
        lambda state: state.has("D02Z02S08[CherubsR]", player) or \
            state.has("Blood Perpetuated in Sand", player) or \
                state._blasphemous_pillar(player) or \
                    state._blasphemous_can_cross_gap(difficulty, player, 8))
    # No doors


    # D02Z02S11 (Graveyard of the Peaks)
    # No items
    # Doors
    set_rule(world.get_entrance("D02Z02S11[E]", player),
        lambda state: state.has("D02Z02S11[NW]", player) or \
            state.has("D02Z02S11[NE]", player) or \
                state._blasphemous_can_cross_gap(difficulty, player, 6))
    set_rule(world.get_entrance("D02Z02S11[NW]", player),
        lambda state: state.has("D02Z02S11[NE]", player))
    set_rule(world.get_entrance("D02Z02S11[NE]", player),
        lambda state: state.has("D02Z02S11[NW]", player))
    set_rule(world.get_entrance("D02Z02S11[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D02Z02S14 (Graveyard of the Peaks)
    # Items
    set_rule(world.get_location("GotP: Amanecida of the Bejeweled Arrow", player),
        lambda state: state._blasphemous_can_beat_boss("Graveyard", difficulty, player))
    # Doors
    set_rule(world.get_entrance("D02Z02S14[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D02Z03S02 (Convent of Our Lady of the Charred Visage)
    # No items
    # Doors
    set_rule(world.get_entrance("D02Z03S02[W]", player),
        lambda state: state.has("D02Z03S02[NW]", player) or \
            state.has("D02Z03S02[NE]", player) or \
                state.has("D02Z03S02[N]", player) or \
                    state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))
    set_rule(world.get_entrance("D02Z03S02[NW]", player),
        lambda state: state.has("D02Z03S02[NE]", player) or \
            state.has("D02Z03S02[N]", player))
    set_rule(world.get_entrance("D02Z03S02[NE]", player),
        lambda state: state.has("D02Z03S02[NW]", player) or \
            state.has("D02Z03S02[N]", player))
    set_rule(world.get_entrance("D02Z03S02[N]", player),
        lambda state: state.has("D02Z03S02[NW]", player) or \
            state.has("D02Z03S02[NE]", player))
    add_rule(world.get_entrance("D02Z03S02[N]", player),
        lambda state: state.has("OpenedConventLadder", player))


    # D02Z03S03 (Convent of Our Lady of the Charred Visage)
    # Items
    set_rule(world.get_location("CoOLotCV: Snowy window ledge", player),
        lambda state: state.has("D02Z03S03[NW]", player) or \
            state.has("Blood Perpetuated in Sand", player) or \
                state._blasphemous_can_cross_gap(difficulty, player, 3))
    # Doors
    set_rule(world.get_entrance("D02Z03S03[NW]", player),
        lambda state: state.has("Blood Perpetuated in Sand", player) or \
            state._blasphemous_can_cross_gap(difficulty, player, 3))


    # D02Z03S05 (Convent of Our Lady of the Charred Visage)
    # Items
    set_rule(world.get_location("CoOLotCV: Center miasma room", player),
        lambda state: state.has("Dash Ability", player) and \
            (state.has("D02Z03S05[S]", player) or \
                state.has("D02Z03S05[NE]", player) or \
                    state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player)))
    # Doors
    set_rule(world.get_entrance("D02Z03S05[S]", player),
        lambda state: state.has("D02Z03S05[NE]", player) or \
            state.has("Wall Climb Ability", player))
    set_rule(world.get_entrance("D02Z03S05[NE]", player),
        lambda state: state.has("D02Z03S05[S]", player) or \
            state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))


    # D02Z03S10 (Convent of Our Lady of the Charred Visage)
    # No items
    # Doors
    set_rule(world.get_entrance("D02Z03S10[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    

    # D02Z03S11 (Convent of Our Lady of the Charred Visage)
    # Event
    set_rule(world.get_location("OpenedConventLadder", player),
        lambda state: state._blasphemous_opened_convent_ladder(player))


    # D02Z03S12 (Convent of Our Lady of the Charred Visage)
    # Items
    set_rule(world.get_location("CoOLotCV: Lower west statue", player),
        lambda state: state._blasphemous_can_survive_poison(difficulty, player, 1) and \
            state.has("Dash Ability", player))
    # No doors


    # D02Z03S18 (Convent of Our Lady of the Charred Visage)
    # No items
    # Doors
    set_rule(world.get_entrance("D02Z03S18[NW]", player),
        lambda state: state.has("D02Z03S18[NE]", player) or \
            state.has("Wall Climb Ability", player))
    set_rule(world.get_entrance("D02Z03S18[NE]", player),
        lambda state: state.has("D02Z03S18[NW]", player) or \
            state.has("Wall Climb Ability", player))


    # D02Z03S20 (Convent of Our Lady of the Charred Visage)
    # Items
    set_rule(world.get_location("CoOLotCV: Our Lady of the Charred Visage", player),
        lambda state: state._blasphemous_can_beat_boss("Convent", difficulty, player))
    # Doors
    set_rule(world.get_entrance("D02Z03S20[W]", player),
        lambda state: state._blasphemous_can_beat_boss("Convent", difficulty, player))
    set_rule(world.get_entrance("D02Z03S20[E]", player),
        lambda state: state._blasphemous_can_beat_boss("Convent", difficulty, player))


    # D02Z03S21 (Convent of Our Lady of the Charred Visage)
    # Items
    set_rule(world.get_location("CoOLotCV: Fountain of burning oil", player),
        lambda state: state.has("Empty Golden Thimble", player))
    # No doors


    # D03Z01S01 (Mountains of the Endless Dusk)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z01S01[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D03Z01S02 (Mountains of the Endless Dusk)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z01S02[W]", player),
        lambda state: state.has("Wall Climb Ability", player) or \
            state._blasphemous_can_cross_gap(difficulty, player, 3))
    set_rule(world.get_entrance("D03Z01S02[E]", player),
        lambda state: state.has("Wall Climb Ability", player) or \
            state._blasphemous_can_cross_gap(difficulty, player, 7))


    # D03Z01S03 (Mountains of the Endless Dusk)
    # Items
    set_rule(world.get_location("MotED: Platform above chasm", player),
        lambda state: state.has_any({"Blood Perpetuated in Sand", "Purified Hand of the Nun"}, player) and \
            (state.has("D03Z01S03[W]", player) or \
                state.has("D03Z01S03[SW]", player) or \
                    state._blasphemous_can_cross_gap(difficulty, player, 9)))
    set_rule(world.get_location("MotED: 1st meeting with Redento", player),
        lambda state: state.has("D03Z01S03[W]", player) or \
            state.has("D03Z01S03[SW]", player) or \
                state._blasphemous_can_cross_gap(difficulty, player, 9))
    set_rule(world.get_location("MotED: Child of Moonlight, above chasm", player),
        lambda state: state.has("D03Z01S03[W]", player) or \
            state.has("D03Z01S03[SW]", player) or \
                state._blasphemous_can_cross_gap(difficulty, player, 9))
    set_rule(world.get_location("MotED: Amanecida of the Golden Blades", player),
        lambda state: state._blasphemous_can_beat_boss("Jondo", difficulty, player) and \
            (state.has("D03Z01S03[W]", player) or \
                state.has("D03Z01S03[SW]", player) or \
                    state._blasphemous_can_cross_gap(difficulty, player, 9)))
    # Doors
    set_rule(world.get_entrance("D03Z01S03[W]", player),
        lambda state: state.has("Wall Climb Ability", player) and \
            (state.has("D03Z01S03[SW]", player) or \
                state._blasphemous_can_cross_gap(difficulty, player, 9)))
    set_rule(world.get_entrance("D03Z01S03[E]", player),
        lambda state: state.has("Wall Climb Ability", player))
    set_rule(world.get_entrance("D03Z01S03[SW]", player),
        lambda state: state.has("D03Z01S03[W]", player) or \
            state._blasphemous_can_cross_gap(difficulty, player, 9))
    set_rule(world.get_entrance("D03Z01S03[-WestL]", player),
        lambda state: state.has("Linen of Golden Thread", player) and \
            (state.has("D03Z01S03[W]", player) or \
                state.has("D03Z01S03[SW]", player) or \
                    state._blasphemous_can_cross_gap(difficulty, player, 9)))
    set_rule(world.get_entrance("D03Z01S03[-WestR]", player),
        lambda state: state.has("Linen of Golden Thread", player) and \
            (state.has("D03Z01S03[W]", player) or \
                state.has("D03Z01S03[SW]", player) or \
                    state._blasphemous_can_cross_gap(difficulty, player, 9)))
    set_rule(world.get_entrance("D03Z01S03[-EastL]", player),
        lambda state: state.has("Linen of Golden Thread", player) and \
            (state.has("D03Z01S03[W]", player) or \
                state.has("D03Z01S03[SW]", player) or \
                    state._blasphemous_can_cross_gap(difficulty, player, 5)))
    set_rule(world.get_entrance("D03Z01S03[-EastR]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D03Z01S04 (Mountains of the Endless Dusk)
    # Items
    set_rule(world.get_location("MotED: Blood platform alcove", player),
        lambda state: state.has_any({"Blood Perpetuated in Sand", "Purified Hand of the Nun"}, player) or \
            state._blasphemous_upwarp_skips_allowed(difficulty))
    # No doors


    # D03Z01S06 (Mountains of the Endless Dusk)
    # Items
    set_rule(world.get_location("MotED: Perpetva", player),
        lambda state: state._blasphemous_can_beat_boss("Perpetua", difficulty, player))
    set_rule(world.get_location("MotED: Egg hatching", player),
        lambda state: state._blasphemous_can_beat_boss("Perpetua", difficulty, player) and \
            state.has("Egg of Deformity", player))
    # Doors
    set_rule(world.get_entrance("D03Z01S06[W]", player),
        lambda state: state._blasphemous_can_beat_boss("Perpetua", difficulty, player))
    set_rule(world.get_entrance("D03Z01S06[E]", player),
        lambda state: state._blasphemous_can_beat_boss("Perpetua", difficulty, player))


    # D03Z02S01 (Jondo)
    # Items
    set_rule(world.get_location("Jondo: Upper east chest", player),
        lambda state: state.has("D03Z02S01[Cherubs]", player) or \
            state._blasphemous_can_climb_on_root(player) or \
                state._blasphemous_can_cross_gap(difficulty, player, 8) or \
                    state.has("Purified Hand of the Nun", player) and \
                        state._blasphemous_can_enemy_bounce(difficulty, enemy))
    # Doors
    set_rule(world.get_entrance("D03Z02S01[W]", player),
        lambda state: state.has("Wall Climb Ability", player) or \
            state.has("Purified Hand of the Nun", player) and \
                state._blasphemous_can_enemy_bounce(difficulty, enemy))
    set_rule(world.get_entrance("D03Z02S01[N]", player),
        lambda state: state.has("Wall Climb Ability", player) or \
            state.has("Purified Hand of the Nun", player))


    # D03Z02S02 (Jondo)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z02S02[W]", player),
        lambda state: state.has("D03Z02S02[CherubsL]", player) or \
            state.has("Purified Hand of the Nun", player) and \
                (state.has("D03Z02S02[E]", player) or \
                    state.has("D03Z02S02[CherubsR]", player) or \
                        state.has("Wall Climb Ability", player) or \
                            state._blasphemous_can_enemy_bounce(difficulty, enemy)))
    set_rule(world.get_entrance("D03Z02S02[E]", player),
        lambda state: state.has("Wall Climb Ability", player) or \
            state.has("Purified Hand of the Nun", player) and \
                state._blasphemous_can_enemy_bounce(difficulty, enemy))
    
    # D03Z02S03 (Jondo)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z02S03[W]", player),
        lambda state: state.has("Dash Ability", player) and \
            (state.has("D03Z02S03[E]", player) or \
                state.has("D03Z02S03[N]", player) or \
                    state.has("D03Z02S03[SE2]", player)))
    set_rule(world.get_entrance("D03Z02S03[E]", player),
        lambda state: (state._blasphemous_can_air_stall(difficulty, player) or \
                state.has_any({"Purified Hand of the Nun", "Boots of Pleading"}, player)) and \
                (state.has("Dash Ability", player) or \
                    state.has("D03Z02S03[N]", player) or \
                        state.has("D03Z02S03[SE2]", player)))
    set_rule(world.get_entrance("D03Z02S03[N]", player),
        lambda state: state.has("D03Z02S03[W]", player) and \
            state.has("Dash Ability", player) or \
                state.has("D03Z02S03[E]", player) or \
                    state.has("D03Z02S03[SE2]", player))
    set_rule(world.get_entrance("D03Z02S03[SE2]", player),
        lambda state: state.has("D03Z02S03[W]", player) and \
            state.has("Dash Ability", player) or \
                state.has("D03Z02S03[E]", player) or \
                    state.has("D03Z02S03[N]", player))
    set_rule(world.get_entrance("D03Z02S03[SW]", player),
        lambda state: state.has("D03Z02S03[SE]", player) or \
            state.has("D03Z02S03[SSL]", player) or \
                state.has("D03Z02S03[SSR]", player) or \
                    state.has("BrokeJondoBellW", player) and \
                        state.has("BrokeJondoBellE", player) and \
                            (state.has("D03Z02S03[W]", player) and \
                                state.has("Dash Ability", player) or \
                                    state.has("D03Z02S03[E]", player) or \
                                        state.has("D03Z02S03[N]", player) or \
                                            state.has("D03Z02S03[SE2]", player)))
    set_rule(world.get_entrance("D03Z02S03[SE]", player),
        lambda state: state.has("D03Z02S03[SW]", player) or \
            state.has("D03Z02S03[SSL]", player) or \
                state.has("D03Z02S03[SSR]", player) or \
                    state.has("BrokeJondoBellW", player) and \
                        state.has("BrokeJondoBellE", player) and \
                            (state.has("D03Z02S03[W]", player) and \
                                state.has("Dash Ability", player) or \
                                    state.has("D03Z02S03[E]", player) or \
                                        state.has("D03Z02S03[N]", player) or \
                                            state.has("D03Z02S03[SE2]", player)))
    set_rule(world.get_entrance("D03Z02S03[SSL]", player),
        lambda state: state.has("D03Z02S03[SW]", player) or \
            state.has("D03Z02S03[SE]", player) or \
                state.has("D03Z02S03[SSR]", player) or \
                    state.has("BrokeJondoBellW", player) and \
                        state.has("BrokeJondoBellE", player) and \
                            (state.has("D03Z02S03[W]", player) and \
                                state.has("Dash Ability", player) or \
                                    state.has("D03Z02S03[E]", player) or \
                                        state.has("D03Z02S03[N]", player) or \
                                            state.has("D03Z02S03[SE2]", player)))
    set_rule(world.get_entrance("D03Z02S03[SSC]", player),
        lambda state: state.has("D03Z02S03[SW]", player) or \
            state.has("D03Z02S03[SE]", player) or \
                state.has("D03Z02S03[SSL]", player) or \
                    state.has("D03Z02S03[SSR]", player) or \
                        state.has("BrokeJondoBellW", player) and \
                            state.has("BrokeJondoBellE", player) and \
                                (state.has("D03Z02S03[W]", player) and \
                                    state.has("Dash Ability", player) or \
                                        state.has("D03Z02S03[E]", player) or \
                                            state.has("D03Z02S03[N]", player) or \
                                                state.has("D03Z02S03[SE2]", player)))
    set_rule(world.get_entrance("D03Z02S03[SSR]", player),
        lambda state: state.has("D03Z02S03[SW]", player) or \
            state.has("D03Z02S03[SE]", player) or \
                state.has("D03Z02S03[SSL]", player) or \
                    state.has("BrokeJondoBellW", player) and \
                        state.has("BrokeJondoBellE", player) and \
                            (state.has("D03Z02S03[W]", player) and \
                                state.has("Dash Ability", player) or \
                                    state.has("D03Z02S03[E]", player) or \
                                        state.has("D03Z02S03[N]", player) or \
                                            state.has("D03Z02S03[SE2]", player)))


    # D03Z02S04 (Jondo)
    # Items
    set_rule(world.get_location("Jondo: Lower east under chargers", player),
        lambda state: state.has("D03Z02S04[NE]", player) or \
            state.has("D03Z02S04[S]", player) or \
                state.has("Wall Climb Ability", player))
    # Doors
    set_rule(world.get_entrance("D03Z02S04[NW]", player),
        lambda state: state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))
    set_rule(world.get_entrance("D03Z02S04[NE]", player),
        lambda state: state.has("Wall Climb Ability", player) or \
            (state.has("D03Z02S04[S]", player) and \
                state.has("Purified Hand of the Nun", player)))
    set_rule(world.get_entrance("D03Z02S04[S]", player),
        lambda state: state.has("D03Z02S04[NE]", player) or \
            state.has("Wall Climb Ability", player))


    # D03Z02S05 (Jondo)
    # Items
    set_rule(world.get_location("Jondo: Upper east Child of Moonlight", player),
        lambda state: state.has("D03Z02S05[E]", player) or \
            state.has("D03Z02S05[S]", player) or \
                state._blasphemous_can_cross_gap(difficulty, player, 5) or \
                    (state._blasphemous_can_enemy_bounce(difficulty, enemy) and \
                        state._blasphemous_can_cross_gap(difficulty, player, 3)))
    # Doors
    set_rule(world.get_entrance("D03Z02S05[E]", player),
        lambda state: state.has("D03Z02S05[S]", player) or \
            state._blasphemous_can_cross_gap(difficulty, player, 5) or \
                (state._blasphemous_can_enemy_bounce(difficulty, enemy) and \
                    state._blasphemous_can_cross_gap(difficulty, player, 3)))
    set_rule(world.get_entrance("D03Z02S05[S]", player),
        lambda state: state.has("D03Z02S05[E]", player) or \
            state._blasphemous_can_cross_gap(difficulty, player, 5) or \
                (state._blasphemous_can_enemy_bounce(difficulty, enemy) and \
                    state._blasphemous_can_cross_gap(difficulty, player, 3)))
    # Event
    set_rule(world.get_location("BrokeJondoBellE", player),
        lambda state: state._blasphemous_broke_jondo_bell_e(difficulty, enemy, player))


    # D03Z02S07 (Jondo)
    # Items
    set_rule(world.get_location("Jondo: Lower west lift alcove", player),
        lambda state: state.has("Dash Ability", player))
    # No doors


    # D03Z02S08 (Jondo)
    # Items
    set_rule(world.get_location("Jondo: Lower west bell alcove", player),
        lambda state: state.has("D03Z02S08[N]", player) or \
            state.has("D03Z02S08[W]", player) or \
                state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))
    # Doors
    set_rule(world.get_entrance("D03Z02S08[W]", player),
        lambda state: state.has("D03Z02S08[N]", player) or \
            state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))
    set_rule(world.get_entrance("D03Z02S08[N]", player),
        lambda state: state.has("D03Z02S08[W]", player) or \
            state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))


    # D03Z02S09 (Jondo)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z02S09[W]", player),
        lambda state: state.has("Dash Ability", player))
    set_rule(world.get_entrance("D03Z02S09[N]", player),
        lambda state: state.has("D03Z02S09[S]", player) or \
            state.has("D03Z02S09[Cherubs]", player) or \
                state.has("Dash Ability", player))
    set_rule(world.get_entrance("D03Z02S09[S]", player),
        lambda state: state.has("D03Z02S09[N]", player) or \
            state.has("D03Z02S09[Cherubs]", player) or \
                state.has("Dash Ability", player))
    # Event
    set_rule(world.get_location("BrokeJondoBellW", player),
        lambda state: state._blasphemous_broke_jondo_bell_w(player))


    # D03Z02S10 (Jondo)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z02S10[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D03Z02S11 (Jondo)
    # Items
    set_rule(world.get_location("Jondo: Spike tunnel statue", player),
        lambda state: state.has("Dash Ability", player) and \
            (state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player) or \
                state.has("D03Z02S11[E]", player) and \
                    state._blasphemous_can_cross_gap(difficulty, player, 2)))
    set_rule(world.get_location("Jondo: Spike tunnel Child of Moonlight", player),
        lambda state: state.has("Dash Ability", player) and \
            (state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player) or \
                state.has("D03Z02S11[W]", player) and \
                    (state._blasphemous_can_cross_gap(difficulty, player, 2) and \
                        state._blasphemous_can_enemy_bounce(difficulty, enemy) or \
                            state._blasphemous_can_cross_gap(difficulty, player, 3)) or \
                                state.has("D03Z02S11[E]", player) and \
                                    (state._blasphemous_can_cross_gap(difficulty, player, 1) or \
                                        state._blasphemous_can_enemy_bounce(difficulty, enemy))))
    # Doors
    set_rule(world.get_entrance("D03Z02S11[W]", player),
        lambda state: state.has("Dash Ability", player) and \
            (state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player) or \
                state._blasphemous_can_cross_gap(difficulty, player, 2)))
    set_rule(world.get_entrance("D03Z02S11[E]", player),
        lambda state: state.has("Dash Ability", player) and \
            state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))

    # D03Z02S13 (Jondo)
    # Items
    set_rule(world.get_location("Jondo: Upper west tree root", player),
        lambda state: state._blasphemous_can_walk_on_root(player) or \
            state._blasphemous_can_cross_gap(difficulty, player, 3))
    # Doors
    set_rule(world.get_entrance("D03Z02S13[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D03Z03S01 (Grievance Ascends)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z03S01[NL]", player),
        lambda state: state.has("D03Z03S01[NR]", player) or \
            state.has("D03Z03S01[NC]", player) or \
                state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))
    set_rule(world.get_entrance("D03Z03S01[NR]", player),
        lambda state: state.has("D03Z03S01[NL]", player) or \
            state.has("D03Z03S01[NC]", player) or \
                state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))


    # D03Z03S02 (Grievance Ascends)
    # Items
    set_rule(world.get_location("GA: Lower west ledge", player),
        lambda state: state._blasphemous_can_survive_poison(difficulty, player, 1))
    # Doors
    set_rule(world.get_entrance("D03Z03S02[W]", player),
        lambda state: state.has("D03Z03S02[NE]", player) or \
            state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))
    set_rule(world.get_entrance("D03Z03S02[NE]", player),
        lambda state: state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))


    # D03Z03S03 (Grievance Ascends)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z03S03[W]", player),
        lambda state: state.has("D03Z03S03[NE]", player))
    set_rule(world.get_entrance("D03Z03S03[NE]", player),
        lambda state: state.has("D03Z03S03[W]", player))


    # D03Z03S04 (Grievance Ascends)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z03S04[NW]", player),
        lambda state: state.has("D03Z03S04[NE]", player) or \
            state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player) and \
                (state.has("D03Z03S04[E]", player) or \
                    state.has("D03Z03S04[SW]", player) or \
                        state.has("Blood Perpetuated in Sand", player) or \
                            state._blasphemous_can_cross_gap(difficulty, player, 10)))
    set_rule(world.get_entrance("D03Z03S04[NE]", player),
        lambda state: state.has("Wall Climb Ability", player) and \
            (state.has("D03Z03S04[NW]", player) or \
                state.has("D03Z03S04[E]", player) or \
                    state.has("D03Z03S04[SW]", player) or \
                        state.has("Blood Perpetuated in Sand", player) or \
                            state._blasphemous_can_cross_gap(difficulty, player, 10)))
    set_rule(world.get_entrance("D03Z03S04[E]", player),
        lambda state: state.has("D03Z03S04[NW]", player) or \
            state.has("D03Z03S04[NE]", player) or \
                state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player) and \
                    (state.has("D03Z03S04[SW]", player) or \
                        state.has("Blood Perpetuated in Sand", player) or \
                            state._blasphemous_can_cross_gap(difficulty, player, 10)))
    set_rule(world.get_entrance("D03Z03S04[SW]", player),
        lambda state: state.has("D03Z03S04[NW]", player) or \
            state.has("D03Z03S04[NE]", player) or \
                state.has("D03Z03S04[E]", player) or \
                    state.has("Blood Perpetuated in Sand", player) or \
                        state._blasphemous_can_cross_gap(difficulty, player, 10))
    set_rule(world.get_entrance("D03Z03S04[SE]", player),
        lambda state: state.has("Blood Perpetuated in Sand", player))
    set_rule(world.get_entrance("D03Z03S04[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D03Z03S05 (Grievance Ascends)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z03S05[NW]", player),
        lambda state: state.has("D03Z03S05[NE]", player))
    set_rule(world.get_entrance("D03Z03S05[NE]", player),
        lambda state: state.has("D03Z03S05[NW]", player))
    set_rule(world.get_entrance("D03Z03S05[SW]", player),
        lambda state: state.has("D03Z03S05[SE]", player) or \
            state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D03Z03S05[SE]", player),
        lambda state: state.has("D03Z03S05[SW]", player) or \
            state.has("Linen of Golden Thread", player))


    # D03Z03S06 (Grievance Ascends)
    # Items
    set_rule(world.get_location("GA: Miasma room floor", player),
        lambda state: state._blasphemous_can_survive_poison(difficulty, player, 1))
    set_rule(world.get_location("GA: Miasma room treasure", player),
        lambda state: state.has("Wall Climb Ability", player))
    set_rule(world.get_location("GA: Miasma room Child of Moonlight", player),
        lambda state: state.has("Wall Climb Ability", player))
    # No doors


    # D03Z03S07 (Grievance Ascends)
    # No items
    # Doors
    set_rule(world.get_entrance("D03Z03S07[NW]", player),
        lambda state: state.has("D03Z03S07[NE]", player) or \
            state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))
    set_rule(world.get_entrance("D03Z03S07[NE]", player),
        lambda state: state.has("D03Z03S07[NE]", player) or \
            state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))


    # D03Z03S08 (Grievance Ascends)
    # Items
    set_rule(world.get_location("GA: End of blood bridge", player),
        lambda state: state.has("Blood Perpetuated in Sand", player) or \
            state._blasphemous_can_cross_gap(difficulty, player, 11))
    set_rule(world.get_location("GA: Blood bridge Child of Moonlight", player),
        lambda state: (state.has("Blood Perpetuated in Sand", player) or \
            state._blasphemous_can_cross_gap(difficulty, player, 11)) and \
                (state.has_any({"Purified Hand of the Nun", "Cante Jondo of the Three Sisters", "Verdiales of the Forsaken Hamlet"}, player) or \
                    state._blasphemous_pillar(player) or \
                        state._blasphemous_tirana(player) or \
                            state._blasphemous_aubade(player) and \
                                state._blasphemous_can_air_stall(difficulty, player)))
    # Doors
    set_rule(world.get_entrance("D03Z03S08[-CherubsL]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D03Z03S08[-CherubsR]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D03Z03S09 (Grievance Ascends)
    # Items
    set_rule(world.get_location("GA: Lower east Child of Moonlight", player),
        lambda state: state._blasphemous_can_climb_on_root(player) or \
            state.has_any({"Purified Hand of the Nun", "Lorquiana", "Zarabanda of the Safe Haven", "Cante Jondo of the Three Sisters"}, player) or \
                state._blasphemous_pillar(player) or \
                    state._blasphemous_aubade(player) or \
                        state._blasphemous_tirana(player))
    # No doors


    # D03Z03S10 (Grievance Ascends)
    # Items
    set_rule(world.get_location("GA: Altasgracias' gift", player),
        lambda state: state.has_group("egg", player, 3))
    set_rule(world.get_location("GA: Empty giant egg", player),
        lambda state: state.has_group("egg", player, 3) and \
            state.has("Hatched Egg of Deformity", player) and \
                (state.has("D01Z02S01[W]", player) or \
                    state.has("D01Z02S01[E]", player)))
    # No doors


    # D03Z03S15 (Grievance Ascends)
    # Items
    set_rule(world.get_location("GA: Tres Angustias", player),
        lambda state: state._blasphemous_can_beat_boss("Grievance", difficulty, player))
    # Doors
    set_rule(world.get_entrance("D03Z03S15[W]", player),
        lambda state: state._blasphemous_can_beat_boss("Grievance", difficulty, player))
    set_rule(world.get_entrance("D03Z03S15[E]", player),
        lambda state: state._blasphemous_can_beat_boss("Grievance", difficulty, player))


    # D04Z01S01 (Patio of the Silent Steps)
    # Items
    set_rule(world.get_location("PotSS: First area ledge", player),
        lambda state: state.has("D04Z01S01[NE]", player) or \
            state.has("D04Z01S01[N]", player) or \
                state._blasphemous_can_cross_gap(difficulty, player, 3))
    # Doors
    set_rule(world.get_entrance("D04Z01S01[NE]", player),
        lambda state: state.has("D04Z01S01[N]", player) or \
            state._blasphemous_can_cross_gap(difficulty, player, 3))
    set_rule(world.get_entrance("D04Z01S01[N]", player),
        lambda state: state.has("D04Z01S01[NE]", player) or \
            state._blasphemous_can_cross_gap(difficulty, player, 3))


    # D04Z01S02 (Patio of the Silent Steps)
    # Items
    set_rule(world.get_location("PotSS: Second area ledge", player),
        lambda state: state._blasphemous_can_climb_on_root(player) or \
            state._blasphemous_can_cross_gap(difficulty, player, 3))
    # No doors


    # D04Z01S03 (Patio of the Silent Steps)
    # Items
    set_rule(world.get_location("PotSS: Third area upper ledge", player),
        lambda state: state._blasphemous_can_walk_on_root(player) or \
            state._blasphemous_can_cross_gap(difficulty, player, 3))
    # No doors


    # D04Z01S04 (Patio of the Silent Steps)
    # Items
    set_rule(world.get_location("PotSS: 4th meeting with Redento", player),
        lambda state: state._blasphemous_redento(blasphemousworld, player, 4))
    # No doors


    # D04Z01S05 (Patio of the Silent Steps)
    # No items
    # Doors
    set_rule(world.get_entrance("D04Z01S05[N]", player),
        lambda state: (state.has("Blood Perpetuated in Sand", player) and \
            state._blasphemous_can_climb_on_root(player)) or \
                state.has("Purified Hand of the Nun", player) and \
                    (state.has("Blood Perpetuated in Sand", player) or \
                        state._blasphemous_can_climb_on_root(player)))
    set_rule(world.get_entrance("D04Z01S05[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D04Z01S06 (Patio of the Silent Steps)
    # No items
    # Doors
    set_rule(world.get_entrance("D04Z01S06[E]", player),
        lambda state: state.has("Purified Hand of the Nun", player))
    set_rule(world.get_entrance("D04Z01S06[Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D04Z02S01 (Mother of Mothers)
    # Items
    if world.purified_hand[player]:
        set_rule(world.get_location("MoM: Western room ledge", player),
            lambda state: state.has("D04Z02S01[N]", player) or \
                state.has("D04Z02S01[NE]", player) and \
                    state.has("Dash Ability", player) and \
                        state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))
    set_rule(world.get_location("MoM: Lower west Child of Moonlight", player),
        lambda state: state.has("D04Z02S01[N]", player) or \
            state._blasphemous_pillar(player) or \
                state.has("D04Z02S01[NE]", player) and \
                    state.has("Dash Ability", player) and \
                        (state.has("Wall Climb Ability", player) or \
                            state._blasphemous_can_cross_gap(difficulty, player, 1)))
    # Doors
    set_rule(world.get_entrance("D04Z02S01[N]", player),
        lambda state: state.has("D04Z02S04[NE]", player) and \
            state.has("Dash Ability", player) and \
                state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))
    set_rule(world.get_entrance("D04Z02S01[NE]", player),
        lambda state: state.has("D04Z02S01[N]", player) or \
            state.has("Dash Ability", player) and \
                state._blasphemous_can_cross_gap(difficulty, player, 1))


    # D04Z02S02 (Mother of Mothers)
    # No items
    # Doors
    set_rule(world.get_entrance("D04Z02S02[NE]", player),
        lambda state: (state.has("Purified Hand of the Nun", player) and \
            state._blasphemous_upwarp_skips_allowed(difficulty)) or \
                (state.has("Purified Hand of the Nun", player) and \
                    state._blasphemous_can_enemy_upslash(difficulty, enemy, player)) or \
                        (state._blasphemous_can_enemy_upslash(difficulty, enemy, player) and \
                            state._blasphemous_upwarp_skips_allowed(difficulty) and \
                                (state.has("Wall Climb Ability", player) or \
                                    state.has("D04Z02S02[N]", player))))
    set_rule(world.get_entrance("D04Z02S02[N]", player),
        lambda state: state.has("D04Z02S02[NE]", player) or \
            state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))


    # D04Z02S04 (Mother of Mothers)
    # No items
    # Doors
    set_rule(world.get_entrance("D04Z02S04[NW]", player),
        lambda state: state.has("D04Z02S04[NE]", player) or \
            state.has("D04Z02S04[N]", player) or \
                state.has("D04Z02S04[Cherubs]", player) or \
                    state.has_all({"Purified Hand of the Nun", "Wall Climb Ability"}, player))
    set_rule(world.get_entrance("D04Z02S04[NE]", player),
        lambda state: state.has("D04Z02S04[NW]", player) or \
            state.has("D04Z02S04[N]", player) or \
                state.has("D04Z02S04[Cherubs]", player) or \
                    state.has_all({"Purified Hand of the Nun", "Wall Climb Ability"}, player))
    set_rule(world.get_entrance("D04Z02S04[N]", player),
        lambda state: (state.has("D04Z02S04[NW]", player) or \
            state.has("D04Z02S04[NE]", player) or \
                state.has("D04Z02S04[Cherubs]", player) or \
                    state.has_all({"Purified Hand of the Nun", "Wall Climb Ability"}, player)) and \
                        state.has("OpenedMOMLadder", player))


    # D04Z02S06 (Mother of Mothers)
    # Items
    set_rule(world.get_location("MoM: Outside Cleofas' room", player),
        lambda state: state.has("D04Z02S06[NW]", player) or \
            state.has("D04Z02S06[N]", player) or \
                state.has("D04Z02S06[NE]", player) or \
                    state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))
    # Doors
    set_rule(world.get_entrance("D04Z02S06[NW]", player),
        lambda state: state.has("D04Z02S06[N]", player) or \
            state.has("D04Z02S06[NE]", player) or \
                state.has("Wall Climb Ability", player))
    set_rule(world.get_entrance("D04Z02S06[N]", player),
        lambda state: (state.has("D04Z02S06[NW]", player) or \
            state.has("D04Z02S06[NE]", player) or \
                state.has("Wall Climb Ability", player)) and \
                    state.has("OpenedARLadder", player))
    set_rule(world.get_entrance("D04Z02S06[NE]", player),
        lambda state: state.has("D04Z02S06[NW]", player) or \
            state.has("D04Z02S06[N]", player) or \
                state.has("Wall Climb Ability", player))
    set_rule(world.get_entrance("D04Z02S06[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    # Event
    set_rule(world.get_location("OpenedMOMLadder", player),
        lambda state: state._blasphemous_opened_mom_ladder(player))


    # D04Z02S07 (Mother of Mothers)
    # Items
    set_rule(world.get_location("MoM: East chandelier platform", player),
        lambda state: state.has("Blood Perpetuated in Sand", player) or \
            state._blasphemous_can_cross_gap(difficulty, player, 3))
    # No doors


    # D04Z02S09 (Mother of Mothers)
    # No items
    # Doors
    set_rule(world.get_entrance("D04Z02S09[NE]", player),
        lambda state: state.has("Blood Perpetuated in Sand", player))


    # D04Z02S16 (Mother of Mothers)
    # Items
    set_rule(world.get_location("MoM: Giant chandelier statue", player),
        lambda state: state.has("Wall Climb Ability", player) and \
            state.has_any({"Blood Perpetuated in Sand", "Purified Hand of the Nun"}, player))
    # Doors
    set_rule(world.get_entrance("D04Z02S16[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D04Z02S20 (Mother of Mothers)
    # No items
    # Doors
    set_rule(world.get_entrance("D04Z02S20[Redento]", player),
        lambda state: state._blasphemous_redento(blasphemousworld, player, 5))


    # D04Z02S21 (Mother of Mothers)
    # No items
    # Doors
    set_rule(world.get_entrance("D04Z02S21[W]", player),
        lambda state: state.has("D04Z02S21[NE]", player) or \
            state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))
    set_rule(world.get_entrance("D04Z02S21[NE]", player),
        lambda state: state.has_any({"Purified Hand of the Nun", "Wall Climb Ability"}, player))


    # D04Z02S22 (Mother of Mothers)
    # Items
    set_rule(world.get_location("MoM: Melquiades, The Exhumed Archbishop", player),
        lambda state: state._blasphemous_can_beat_boss("Mothers", difficulty, player))
    # Doors
    set_rule(world.get_entrance("D04Z02S22[W]", player),
        lambda state: state._blasphemous_can_beat_boss("Mothers", difficulty, player))
    set_rule(world.get_entrance("D04Z02S22[E]", player),
        lambda state: state._blasphemous_can_beat_boss("Mothers", difficulty, player))


    # D04BZ02S01 (Mother of Mothers - Redento)
    # Items
    set_rule(world.get_location("MoM: Final meeting with Redento", player),
        lambda state: state._blasphemous_redento(blasphemousworld, player, 5))
    # No doors


    # D04Z03S02 (Knot of the Three Words)
    # Items
    set_rule(world.get_location("KotTW: Gift from the Traitor", player),
        lambda state: state.has_all({"Severed Right Eye of the Traitor", "Broken Left Eye of the Traitor"}, player))
    # No doors


    # D04Z04S01 (All the Tears of the Sea)
    # Items
    set_rule(world.get_location("AtTotS: Miriam's gift", player),
        lambda state: state._blasphemous_miriam(player) and \
            state.has("Dash Ability", player) and \
                state.has("Wall Climb Ability", player))
    # No doors


    # D05Z01S03 (Library of the Negated Words)
    # No items
    # Doors
    set_rule(world.get_entrance("D05Z01S03[Frontal]", player),
        lambda state: state.has("Key Grown from Twisted Wood", player) and \
            state.has("D05Z01S23[E]", player) and \
                (state.has("D05Z01S11[NW]", player) or \
                    state.has("D05Z01S11[NE]", player)))


    # D05Z01S05 (Library of the Negated Words)
    # Items
    set_rule(world.get_location("LotNW: Hidden floor", player),
        lambda state: state._blasphemous_can_break_holes(player))
    set_rule(world.get_location("LotNW: Root ceiling platform", player),
        lambda state: (state._blasphemous_can_climb_on_root(player) or \
            state.has("Purified Hand of the Nun", player)) and \
                (state.has("D05Z01S05[NE]", player) or \
                    state.has("Blood Perpetuated in Sand", player)))
    # Doors
    set_rule(world.get_entrance("D05Z01S05[NE]", player),
        lambda state: state.has("Blood Perpetuated in Sand", player))


    # D05Z01S06 (Library of the Negated Words)
    # Items
    set_rule(world.get_location("LotNW: Miasma hallway chest", player),
        lambda state: state.has("D05Z01S06[W]", player) or \
            state._blasphemous_can_survive_poison(difficulty, player, 3))
    # Doors
    set_rule(world.get_entrance("D05Z01S06[W]", player),
        lambda state: state._blasphemous_can_survive_poison(difficulty, player, 3))
    set_rule(world.get_entrance("D05Z01S06[E]", player),
        lambda state: state._blasphemous_can_survive_poison(difficulty, player, 3))


    # D05Z01S07 (Library of the Negated Words)
    # No items
    # Doors
    set_rule(world.get_entrance("D05Z01S07[NW]", player),
        lambda state: state.has("Blood Perpetuated in Sand", player) and \
            (state._blasphemous_can_climb_on_root(player) or \
                state.has("Purified Hand of the Nun", player)) or \
                    (state._blasphemous_can_climb_on_root(player) and \
                        state._blasphemous_can_cross_gap(difficulty, player, 3)) or \
                            state._blasphemous_can_cross_gap(difficulty, player, 7))


    # D05Z01S10 (Library of the Negated Words)
    # Items
    set_rule(world.get_location("LotNW: Platform puzzle chest", player),
        lambda state: state.has_any({"Blood Perpetuated in Sand", "Purified Hand of the Nun"}, player) or \
            state._blasphemous_can_enemy_bounce(difficulty, enemy) and \
                state._blasphemous_can_cross_gap(difficulty, player, 2))
    # No doors


    # D05Z01S11 (Library of the Negated Words)
    # Items
    set_rule(world.get_location("LotNW: Silence for Diosdado", player),
        lambda state: (state.has("D05Z01S11[NW]", player) or \
            state.has("D05Z01S11[NE]", player)) and \
                state.has("D05Z01S23[E]", player))
    set_rule(world.get_location("LotNW: Lowest west upper ledge", player),
        lambda state: state.has("D05Z01S11[NW]", player) or \
            state.has("D05Z01S11[NE]", player))
    # Doors
    set_rule(world.get_entrance("D05Z01S11[SW]", player),
        lambda state: state._blasphemous_can_break_tirana(difficulty, player))
    set_rule(world.get_entrance("D05Z01S11[NW]", player),
        lambda state: state.has("D05Z01S11[NE]", player))
    set_rule(world.get_entrance("D05Z01S11[NE]", player),
        lambda state: state.has("D05Z01S11[NW]", player))


    # D05Z01S21 (Library of the Negated Words)
    # Items
    set_rule(world.get_location("LotNW: Elevator Child of Moonlight", player),
        lambda state: state.has("Zarabanda of the Safe Haven", player) or \
            state.has("Blood Perpetuated in Sand", player) and \
                (state._blasphemous_can_walk_on_root(player) or \
                    state.has("Purified Hand of the Nun", player) or \
                        state._blasphemous_can_cross_gap(difficulty, player, 5) and \
                            state._blasphemous_pillar(player)))
    # Doors
    set_rule(world.get_entrance("D05Z01S21[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D05Z02S06 (The Sleeping Canvases)
    # No items
    # Doors
    set_rule(world.get_entrance("D05Z02S06[SE]", player),
        lambda state: state.has("OpenedTSCGate", player))


    # D05Z02S09 (The Sleeping Canvases)
    # No items
    # Doors
    set_rule(world.get_entrance("D05Z02S09[E]", player),
        lambda state: state.has("Bead of Red Wax", player, 3) and \
            state.has("Bead of Blue Wax", player, 3))


    # D05Z02S10 (The Sleeping Canvases)
    # Items
    set_rule(world.get_location("TSC: Jocinero's 1st reward", player),
        lambda state: state.has("Child of Moonlight", player, 20))
    set_rule(world.get_location("TSC: Jocinero's final reward", player),
        lambda state: state.has("Child of Moonlight", player, 38))
    # Doors
    set_rule(world.get_entrance("D05Z02S10[W]", player),
        lambda state: state.has("Dash Ability", player))
    

    # D05Z02S11 (The Sleeping Canvases)
    # Event
    set_rule(world.get_location("OpenedTSCGate", player),
        lambda state: state._blasphemous_opened_tsc_gate(player))


    # D05Z02S13 (The Sleeping Canvases)
    # No items
    # Doors
    set_rule(world.get_entrance("D05Z02S13[E]", player),
        lambda state: state.has("Dash Ability", player))


    # D05Z02S14 (The Sleeping Canvases)
    # Items
    set_rule(world.get_location("TSC: Exposito, Scion of Abjuration", player),
        lambda state: state._blasphemous_can_beat_boss("Canvases", difficulty, player))
    # Doors
    set_rule(world.get_entrance("D05Z02S14[W]", player),
        lambda state: state._blasphemous_can_beat_boss("Canvases", difficulty, player))
    set_rule(world.get_entrance("D05Z02S14[E]", player),
        lambda state: state._blasphemous_can_beat_boss("Canvases", difficulty, player))


    # D05Z02S15 (The Sleeping Canvases)
    # Items
    set_rule(world.get_location("TSC: Swinging blade tunnel", player),
        lambda state: state.has("Dash Ability", player))
    # No doors


    # D06Z01S01 (Archcathedral Rooftops)
    # No items
    # Doors
    set_rule(world.get_entrance("D06Z01S01[SW]", player),
        lambda state: (state.has("D06Z01S01[SE]", player) or \
            state.has("D06Z01S01[W]", player) or \
                state.has("D06Z01S01[E]", player) or \
                    state.has("D06Z01S01[NNW]", player) or \
                        state.has("D06Z01S01[NNE]", player) or \
                            state.has("D06Z01S01[N]", player)) or \
                                state.has("Linen of Golden Thread", player) and \
                                    (state.has("D06Z01S01[NW]", player) or \
                                        state.has("D06Z01S01[NE]", player)))
    set_rule(world.get_entrance("D06Z01S01[SE]", player),
        lambda state: (state.has("D06Z01S01[SW]", player) or \
            state.has("D06Z01S01[W]", player) or \
                state.has("D06Z01S01[E]", player) or \
                    state.has("D06Z01S01[NNW]", player) or \
                        state.has("D06Z01S01[NNE]", player) or \
                            state.has("D06Z01S01[N]", player)) or \
                                state.has("Linen of Golden Thread", player) and \
                                    (state.has("D06Z01S01[NW]", player) or \
                                        state.has("D06Z01S01[NE]", player)))
    set_rule(world.get_entrance("D06Z01S01[W]", player),
        lambda state: (state.has("D06Z01S01[E]", player) or \
            state.has("D06Z01S01[NNW]", player) or \
                state.has("D06Z01S01[NNE]", player) or \
                    state.has("D06Z01S01[N]", player)) or \
                        state.has_group("masks", player, 1) and \
                            (state.has("D06Z01S01[SW]", player) or \
                                state.has("D06Z01S01[SE]", player)) or \
                                    state.has("Linen of Golden Thread", player) and \
                                        (state.has("D06Z01S01[NW]", player) or \
                                            state.has("D06Z01S01[NE]", player) and \
                                                (state._blasphemous_can_walk_on_root(player) or \
                                                    state._blasphemous_can_cross_gap(difficulty, player, 1))))
    set_rule(world.get_entrance("D06Z01S01[E]", player),
        lambda state: (state.has("D06Z01S01[W]", player) or \
            state.has("D06Z01S01[NNW]", player) or \
                state.has("D06Z01S01[NNE]", player) or \
                    state.has("D06Z01S01[N]", player)) or \
                        state.has_group("masks", player, 1) and \
                            (state.has("D06Z01S01[SW]", player) or \
                                state.has("D06Z01S01[SE]", player)) or \
                                    state.has("Linen of Golden Thread", player) and \
                                        (state.has("D06Z01S01[NW]", player) or \
                                            state.has("D06Z01S01[NE]", player) and \
                                                (state._blasphemous_can_walk_on_root(player) or \
                                                    state._blasphemous_can_cross_gap(difficulty, player, 1))))
    set_rule(world.get_entrance("D06Z01S01[NW]", player),
        lambda state: state.has("D06Z01S01[NE]", player) and \
            (state._blasphemous_can_walk_on_root(player) or \
                state._blasphemous_can_cross_gap(difficulty, player, 8)) or \
                    state.has("Linen of Golden Thread", player) and \
                        (state.has("D06Z01S01[NNW]", player) or \
                            state.has("D06Z01S01[NNE]", player) and \
                                (state._blasphemous_can_walk_on_root(player) or \
                                    state._blasphemous_can_cross_gap(difficulty, player, 3))))
    set_rule(world.get_entrance("D06Z01S01[NE]", player),
        lambda state: state.has("D06Z01S01[NW]", player) or \
            (state._blasphemous_can_walk_on_root(player) or \
                state._blasphemous_can_cross_gap(difficulty, player, 8)) or \
                    state.has("Linen of Golden Thread", player) and \
                        (state.has("D06Z01S01[NNW]", player) or \
                            state.has("D06Z01S01[NNE]", player) and \
                                (state._blasphemous_can_walk_on_root(player) or \
                                    state._blasphemous_can_cross_gap(difficulty, player, 3))))
    set_rule(world.get_entrance("D06Z01S01[NNW]", player),
        lambda state: (state.has("D06Z01S01[NNE]", player) or \
            state.has("D06Z01S01[N]", player)) or \
                state.has_group("masks", player, 2) and \
                    (state.has("D06Z01S01[SW]", player) or \
                        state.has("D06Z01S01[SE]", player) or \
                            state.has("D06Z01S01[W]", player) or \
                                state.has("D06Z01S01[E]", player) or \
                                    state.has("Linen of Golden Thread", player) and \
                                        (state.has("D06Z01S01[NW]", player) or \
                                            state.has("D06Z01S01[NE]", player))))
    set_rule(world.get_entrance("D06Z01S01[NNE]", player),
        lambda state: (state.has("D06Z01S01[NNW]", player) or \
            state.has("D06Z01S01[N]", player)) or \
                state.has_group("masks", player, 2) and \
                    (state.has("D06Z01S01[SW]", player) or \
                        state.has("D06Z01S01[SE]", player) or \
                            state.has("D06Z01S01[W]", player) or \
                                state.has("D06Z01S01[E]", player) or \
                                    state.has("Linen of Golden Thread", player) and \
                                        (state.has("D06Z01S01[NW]", player) or \
                                            state.has("D06Z01S01[NE]", player))))
    set_rule(world.get_entrance("D06Z01S01[N]", player),
        lambda state: state.has_group("masks", player, 3) and \
            (state.has("D06Z01S01[SW]", player) or \
                state.has("D06Z01S01[SE]", player) or \
                    state.has("D06Z01S01[W]", player) or \
                        state.has("D06Z01S01[E]", player) or \
                            state.has("D06Z01S01[NNW]", player) or \
                                state.has("D06Z01S01[NNE]", player) or \
                                    state.has("Linen of Golden Thread", player) and \
                                        (state.has("D06Z01S01[NW]", player) or \
                                            state.has("D06Z01S01[NE]", player))))
    set_rule(world.get_entrance("D06Z01S01[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player) and \
            (state.has("D06Z01S01[SW]", player) or \
                state.has("D06Z01S01[SE]", player) or \
                    state.has("D06Z01S01[W]", player) or \
                        state.has("D06Z01S01[E]", player) or \
                            state.has("D06Z01S01[NW]", player) or \
                                state.has("D06Z01S01[NE]", player) or \
                                    state.has("D06Z01S01[NNW]", player) or \
                                        state.has("D06Z01S01[NNE]", player)))


    # D06Z01S03 (Archcathedral Rooftops)
    # Items
    set_rule(world.get_location("AR: First soldier fight", player),
        lambda state: state._blasphemous_can_beat_boss("Legionary", difficulty, player))
    # Doors
    set_rule(world.get_entrance("D06Z01S03[W]", player),
        lambda state: state._blasphemous_can_beat_boss("Legionary", difficulty, player))
    set_rule(world.get_entrance("D06Z01S03[E]", player),
        lambda state: state._blasphemous_can_beat_boss("Legionary", difficulty, player))


    # D06Z01S04 (Archcathedral Rooftops)
    # No items
    # Doors
    set_rule(world.get_entrance("D06Z01S04[SW]", player),
        lambda state: state.has("D06Z01S04[W]", player) or \
            state.has("D06Z01S04[Health]", player))
    set_rule(world.get_entrance("D06Z01S04[W]", player),
        lambda state: state.has("D06Z01S04[SW]", player) or \
            state.has("D06Z01S04[Health]", player))
    set_rule(world.get_entrance("D06Z01S04[Health]", player),
        lambda state: state.has("D06Z01S04[SW]", player) or \
            state.has("D06Z01S04[W]", player))
    add_rule(world.get_entrance("D06Z01S04[Health]", player),
        lambda state: (state.has("Wall Climb Ability", player) and \
            state._blasphemous_can_survive_poison(difficulty, player, 2) and \
                (state.has("Purified Hand of the Nun", player) or \
                    (state.has("Blood Perpetuated in Sand", player) and \
                        state._blasphemous_can_climb_on_root(player)))))
    set_rule(world.get_entrance("D06Z01S04[NW]", player),
        lambda state: state.has("D06Z01S04[NE]", player) or \
            state.has("D06Z01S04[Cherubs]", player))
    add_rule(world.get_entrance("D06Z01S04[NW]", player),
        lambda state: state.has("D06Z01S04[Cherubs]", player) or \
            (state.has("D06Z01S04[SW]", player) or \
                state.has("D06Z01S04[W]", player) or \
                    state.has("D06Z01S04[Health]", player)) and \
                        state.has("Wall Climb Ability", player) and \
                            state._blasphemous_can_survive_poison(difficulty, player, 2) and \
                                (state.has_any({"Dash Ability", "Purified Hand of the Nun"}, player) and \
                                    (state._blasphemous_can_dawn_jump(difficulty, player) or \
                                        state._blasphemous_can_climb_on_root(player))))
    set_rule(world.get_entrance("D06Z01S04[NE]", player),
        lambda state: state.has("D06Z01S04[NW]", player) or \
            state.has("D06Z01S04[Cherubs]", player))
    add_rule(world.get_entrance("D06Z01S04[NE]", player),
        lambda state: (state.has("D06Z01S04[SW]", player) or \
            state.has("D06Z01S04[W]", player) or \
                state.has("D06Z01S04[Health]", player)) and \
                    state.has("Wall Climb Ability", player) and \
                        state._blasphemous_can_survive_poison(difficulty, player, 2) and \
                            (state.has_any({"Dash Ability", "Purified Hand of the Nun"}, player) and \
                                (state._blasphemous_can_dawn_jump(difficulty, player) or \
                                    state._blasphemous_can_climb_on_root(player))))


    # D06Z01S06 (Archcathedral Rooftops)
    # Items
    set_rule(world.get_location("AR: Second soldier fight", player),
        lambda state: state._blasphemous_can_beat_boss("Legionary", difficulty, player) and \
            (state.has("D06Z01S06[WW]", player) or \
                state.has("D06Z01S06[E]", player)))
    # Doors
    set_rule(world.get_entrance("D06Z01S06[WW]", player),
        lambda state: state.has("D06Z01S06[E]", player))
    add_rule(world.get_entrance("D06Z01S06[WW]", player),
        lambda state: state._blasphemous_can_beat_boss("Legionary", difficulty, player))
    set_rule(world.get_entrance("D06Z01S06[E]", player),
        lambda state: state.has("D06Z01S06[WW]", player))
    add_rule(world.get_entrance("D06Z01S06[E]", player),
        lambda state: state._blasphemous_can_beat_boss("Legionary", difficulty, player))
    set_rule(world.get_entrance("D06Z01S06[W]", player),
        lambda state: state.has("D06Z01S06[EE]", player))
    set_rule(world.get_entrance("D06Z01S06[EE]", player),
        lambda state: state.has("D06Z01S06[W]", player))


    # D06Z01S08 (Archcathedral Rooftops)
    # No items
    # Doors
    set_rule(world.get_entrance("D06Z01S08[E]", player),
        lambda state: state.has("D06Z01S08[N]", player) or \
            state.has("Wall Climb Ability", player))


    # D06Z01S09 (Archcathedral Rooftops)
    # No items
    # Doors
    set_rule(world.get_entrance("D06Z01S09[-CherubsL]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D06Z01S09[-CherubsR]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D06Z01S10 (Archcathedral Rooftops)
    # No items
    # Doors
    set_rule(world.get_entrance("D06Z01S10[-CherubsL]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D06Z01S10[-CherubsR]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D06Z01S12 (Archcathedral Rooftops)
    # Items
    set_rule(world.get_location("AR: Upper west shaft ledge", player),
        lambda state: state.has("D06Z01S12[NW]", player) or \
            state.has("D06Z01S12[NE]", player) or \
                state.has("D06Z01S12[NE2]", player) or \
                    state.has("D06Z01S12[W]", player) or \
                        state.has("D06Z01S12[E]", player) or \
                            state.has("Wall Climb Ability", player))
    set_rule(world.get_location("AR: Upper west shaft chest", player),
        lambda state: state.has("D06Z01S12[NE2]", player) or \
            (state.has("D06Z01S12[NW]", player) or \
                state.has("D06Z01S12[NE]", player)) and \
                    state.has("Purified Hand of the Nun", player))
    set_rule(world.get_location("AR: Upper west shaft Child of Moonlight", player),
        lambda state: state.has("D06Z01S12[W]", player) or \
            state.has("D06Z01S12[E]", player) or \
                state.has("D06Z01S12[NW]", player) or \
                    state.has("D06Z01S12[NE]", player) or \
                        state.has("D06Z01S12[NE2]", player) or \
                            state.has("Wall Climb Ability", player) and \
                                state.has_any({"Purified Hand of the Nun", "Taranto to my Sister"}, player))
    # Doors
    set_rule(world.get_entrance("D06Z01S12[W]", player),
        lambda state: state.has("D06Z01S12[NW]", player) or \
            state.has("D06Z01S12[NE]", player) or \
                state.has("D06Z01S12[NE2]", player) or \
                    state.has("D06Z01S12[E]", player) or \
                        state.has_all({"Wall Climb Ability", "Purified Hand of the Nun"}, player))
    set_rule(world.get_entrance("D06Z01S12[E]", player),
        lambda state: state.has("D06Z01S12[NW]", player) or \
            state.has("D06Z01S12[NE]", player) or \
                state.has("D06Z01S12[NE2]", player) or \
                    state.has("D06Z01S12[W]", player) or \
                        state.has_all({"Wall Climb Ability", "Purified Hand of the Nun"}, player))
    set_rule(world.get_entrance("D06Z01S12[NW]", player),
        lambda state: state.has("D06Z01S12[NE]", player) or \
            state.has("D06Z01S12[NE2]", player))
    add_rule(world.get_entrance("D06Z01S12[NW]", player),
        lambda state: state.has("D06Z01S12[NE]", player) or \
            state.has_any({"Wall Climb Ability", "Purified Hand of the Nun"}, player))
    set_rule(world.get_entrance("D06Z01S12[NE]", player),
        lambda state: state.has("D06Z01S12[NW]", player) or \
            state.has("D06Z01S12[NE2]", player))
    add_rule(world.get_entrance("D06Z01S12[NE]", player),
        lambda state: state.has("D06Z01S12[NW]", player) or \
            state.has_any({"Wall Climb Ability", "Purified Hand of the Nun"}, player))


    # D06Z01S15 (Archcathedral Rooftops)
    # Items
    set_rule(world.get_location("AR: Upper east shaft ledge", player),
        lambda state: state.has("D06Z01S15[SW]", player) and \
            state.has("Wall Climb Ability", player) and \
                (state._blasphemous_can_cross_gap(difficulty, player, 10) or \
                    state._blasphemous_can_climb_on_root(player) and \
                        (state.has("Blood Perpetuated in Sand", player) or \
                            state.has("Purified Hand of the Nun", player) and \
                                state._blasphemous_can_air_stall(difficulty, player))))
    # Doors
    set_rule(world.get_entrance("D06Z01S15[NW]", player),
        lambda state: state.has("D06Z01S15[NE]", player))
    add_rule(world.get_entrance("D06Z01S15[NW]", player),
        lambda state: state.has("D06Z01S15[SW]", player) or \
            state.has("Wall Climb Ability", player))
    set_rule(world.get_entrance("D06Z01S15[NE]", player),
        lambda state: state.has("D06Z01S15[NW]", player))
    add_rule(world.get_entrance("D06Z01S15[NE]", player),
        lambda state: state.has("D06Z01S15[SW]", player) or \
            state.has("Wall Climb Ability", player))


    # D06Z01S16 (Archcathedral Rooftops)
    # No items
    # Doors
    set_rule(world.get_entrance("D06Z01S16[W]", player),
        lambda state: (state.has("D06Z01S16[CherubsL]", player) and \
            (state.has("Purified Hand of the Nun", player) or \
                state.has("Wall Climb Ability", player) and \
                    (state._blasphemous_can_walk_on_root(player) or \
                        state._blasphemous_can_air_stall(difficulty, player)))) or \
                            (state.has("D06Z01S16[CherubsR]", player) and \
                                (state.has("Purified Hand of the Nun", player) or \
                                    state._blasphemous_can_air_stall(difficulty, player) and \
                                        (state._blasphemous_can_walk_on_root(player) or \
                                            state.has("The Young Mason's Wheel", player)) and \
                                                (state.has("Wall Climb Ability", player) or \
                                                    state._blasphemous_can_dawn_jump(difficulty, player)))) or \
                                                        (state.has("D06Z01S16[E]", player) and \
                                                            (state._blasphemous_can_walk_on_root(player) or \
                                                                state._blasphemous_can_cross_gap(difficulty, player, 7)) and \
                                                                    (state.has("Wall Climb Ability", player) or \
                                                                        state._blasphemous_can_cross_gap(difficulty, player, 5))))
    set_rule(world.get_entrance("D06Z01S16[E]", player),
        lambda state: ((state.has("D06Z01S16[W]", player) or \
            state.has("D06Z01S16[CherubsL]", player)) and \
                (state._blasphemous_can_walk_on_root(player) or \
                    state._blasphemous_can_cross_gap(difficulty, player, 5))) or \
                        (state.has("D06Z01S16[CherubsR]", player) and \
                            (state.has("Purified Hand of the Nun", player) or \
                                state._blasphemous_can_air_stall(difficulty, player) and \
                                    (state._blasphemous_can_walk_on_root(player) and \
                                        state.has("The Young Mason's Wheel", player)))))
    set_rule(world.get_entrance("D06Z01S16[-CherubsL]", player),
        lambda state: state.has("Linen of Golden Thread", player) and \
            (state.has("D06Z01S16[W]", player) or \
                (state.has("D06Z01S16[CherubsR]", player) and \
                    (state.has("Purified Hand of the Nun", player) or \
                        state._blasphemous_can_air_stall(difficulty, player) and \
                            (state._blasphemous_can_walk_on_root(player) or \
                                state.has("The Young Mason's Wheel", player)))) or \
                                    (state.has("D06Z01S16[E]", player) and \
                                        (state._blasphemous_can_walk_on_root(player) or \
                                            state._blasphemous_can_cross_gap(difficulty, player, 7)))))
    set_rule(world.get_entrance("D06Z01S16[-CherubsR]", player),
        lambda state: state.has("Linen of Golden Thread", player) and \
            (state.has("D06Z01S16[E]", player) or \
                (state.has("D06Z01S16[CherubsL]", player) and \
                    (state._blasphemous_can_air_stall(difficulty, player) or \
                        state._blasphemous_can_walk_on_root(player) or \
                            state.has("Purified Hand of the Nun", player))) or \
                                (state.has("D06Z01S16[W]", player) and \
                                    (state._blasphemous_can_walk_on_root(player) or \
                                        state._blasphemous_can_cross_gap(difficulty, player, 1)))))


    # D06Z01S17 (Archcathedral Rooftops)
    # No items
    # Doors
    set_rule(world.get_entrance("D06Z01S17[W]", player),
        lambda state: (state.has("D06Z01S17[E]", player) or \
            state.has("D06Z01S17[CherubsR]", player)) and \
                state.has("Blood Perpetuated in Sand", player) or \
                    state.has("D06Z01S17[CherubsL]", player) and \
                        state.has("Purified Hand of the Nun", player))
    set_rule(world.get_entrance("D06Z01S17[E]", player),
        lambda state: state.has("D06Z01S17[CherubsR]", player) or \
            state.has("Blood Perpetuated in Sand", player) and \
                (state.has("D06Z01S17[W]", player) or \
                    state.has("D06Z01S17[CherubsL]", player) and \
                        state.has("Purified Hand of the Nun", player)))
    set_rule(world.get_entrance("D06Z01S17[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))


    # D06Z01S18 (Archcathedral Rooftops)
    # No items
    # Doors
    set_rule(world.get_entrance("D06Z01S18[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))

    # D06Z01S21 (Archcathedral Rooftops)
    # Items
    set_rule(world.get_location("AR: Third soldier fight", player),
        lambda state: state._blasphemous_can_beat_boss("Legionary", difficulty, player))
    # Doors
    set_rule(world.get_entrance("D06Z01S21[W]", player),
        lambda state: state._blasphemous_can_beat_boss("Legionary", difficulty, player))
    set_rule(world.get_entrance("D06Z01S21[E]", player),
        lambda state: state._blasphemous_can_beat_boss("Legionary", difficulty, player))
    

    # D06Z01S23 (Archcathedral Rooftops)
    # Event
    set_rule(world.get_location("OpenedARLadder", player),
        lambda state: state._blasphemous_opened_ar_ladder(player))


    # D06Z01S25 (Archcathedral Rooftops)
    # Items
    set_rule(world.get_location("AR: Crisanta of the Wrapped Agony", player),
        lambda state: state._blasphemous_can_beat_boss("Rooftops", difficulty, player))
    # Doors
    set_rule(world.get_entrance("D06Z01S25[W]", player),
        lambda state: state._blasphemous_can_beat_boss("Rooftops", difficulty, player))
    set_rule(world.get_entrance("D06Z01S25[E]", player),
        lambda state: state._blasphemous_can_beat_boss("Rooftops", difficulty, player))


    # D08Z01S01 (Bridge of the Three Cavalries)
    # Items
    set_rule(world.get_location("BotTC: Esdras, of the Anointed Legion", player),
        lambda state: state.has_group("wounds", player, 3) and \
            state._blasphemous_can_beat_boss("Bridge", difficulty, player))
    set_rule(world.get_location("BotTC: Esdras' gift", player),
        lambda state: state.has_group("wounds", player, 3) and \
            state._blasphemous_can_beat_boss("Bridge", difficulty, player))
    # Doors
    set_rule(world.get_entrance("D08Z01S01[W]", player),
        lambda state: state._blasphemous_can_beat_boss("Bridge", difficulty, player))
    set_rule(world.get_entrance("D08Z01S01[E]", player),
        lambda state: state.has_group("wounds", player, 3) and \
            (state.has("D08Z01S01[Cherubs]", player) or \
                state._blasphemous_can_beat_boss("Bridge", difficulty, player)))


    # D08Z01S02 (Bridge of the Three Cavalries)
    # No items
    # Items
    set_rule(world.get_entrance("D08Z01S02[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    # Event
    set_rule(world.get_location("BrokeBOTTCStatue", player),
        lambda state: state._blasphemous_broke_bottc_statue(player))


    # D08Z02S03 (Ferrous Tree)
    # No items
    # Doors
    set_rule(world.get_entrance("D08Z02S03[W]", player),
        lambda state: state.has("OpenedBOTTCStatue", player))


    # D08Z03S01 (Hall of the Dawning)
    # No items
    # Doors
    set_rule(world.get_entrance("D08Z03S01[E]", player),
        lambda state: state.has("Verses Spun from Gold", player, 4))


    # D08Z03S02 (Hall of the Dawning)
    # No items
    # Doors
    set_rule(world.get_entrance("D08Z03S02[NW]", player),
        lambda state: state.has("Wall Climb Ability", player))


    # D08Z03S03 (Hall of the Dawning)
    # Items
    set_rule(world.get_location("HotD: Laudes, the First of the Amanecidas", player),
        lambda state: state._blasphemous_can_beat_boss("Hall", difficulty, player))
    # Doors
    set_rule(world.get_entrance("D08Z03S03[W]", player),
        lambda state: state._blasphemous_can_beat_boss("Hall", difficulty, player))
    set_rule(world.get_entrance("D08Z03S03[E]", player),
        lambda state: state._blasphemous_can_beat_boss("Hall", difficulty, player))


    # D09Z01S01 (Wall of the Holy Prohibitions)
    # Items
    set_rule(world.get_location("WotHP: Amanecida of the Molten Thorn", player),
        lambda state: state._blasphemous_can_beat_boss("Wall", difficulty, player))
    # No doors


    # D09Z01S02 (Wall of the Holy Prohibitions)
    # Items
    set_rule(world.get_location("WotHP: Upper east room, center gold cell", player),
        lambda state: state.has("D09Z01S02[Cell5]", player))
    set_rule(world.get_location("WotHP: Upper east room, lift puzzle", player),
        lambda state: state.has("D09Z01S02[NW]", player) or \
            state.has("D09Z01S02[N]", player) or \
                state.has("D09Z01S02[Cell1]", player) or \
                    state.has("D09Z01S02[Cell6]", player) or \
                        state.has("D09Z01S02[Cell4]", player) or \
                            state.has("D09Z01S02[Cell3]", player) or \
                                state.has("D09Z01S02[Cell22]", player) or \
                                    state.has("D09Z01S02[Cell23]", player))
    # Doors
    set_rule(world.get_entrance("D09Z01S02[SW]", player),
        lambda state: state.has("D09Z01S02[Cell2]", player))
    set_rule(world.get_entrance("D09Z01S02[NW]", player),
        lambda state: state.has("D09Z01S02[N]", player) or \
            state.has("D09Z01S02[Cell1]", player) or \
                state.has("D09Z01S02[Cell6]", player) or \
                    state.has("D09Z01S02[Cell4]", player) or \
                        state.has("D09Z01S02[Cell3]", player) or \
                            state.has("D09Z01S02[Cell22]", player) or \
                                state.has("D09Z01S02[Cell23]", player))
    set_rule(world.get_entrance("D09Z01S02[N]", player),
        lambda state: state.has("D09Z01S02[NW]", player) or \
            state.has("D09Z01S02[Cell1]", player) or \
                state.has("D09Z01S02[Cell6]", player) or \
                    state.has("D09Z01S02[Cell4]", player) or \
                        state.has("D09Z01S02[Cell3]", player) or \
                            state.has("D09Z01S02[Cell22]", player) or \
                                state.has("D09Z01S02[Cell23]", player))
    set_rule(world.get_entrance("D09Z01S02[Cell1]", player),
        lambda state: state.has("D09Z01S02[NW]", player) or \
            state.has("D09Z01S02[N]", player) or \
                state.has("D09Z01S02[Cell6]", player) or \
                    state.has("D09Z01S02[Cell4]", player) or \
                        state.has("D09Z01S02[Cell3]", player) or \
                            state.has("D09Z01S02[Cell22]", player) or \
                                state.has("D09Z01S02[Cell23]", player))
    add_rule(world.get_entrance("D09Z01S02[Cell1]", player),
        lambda state: state.has("Key of the Secular", player))
    set_rule(world.get_entrance("D09Z01S02[Cell6]", player),
        lambda state: state.has("D09Z01S02[NW]", player) or \
            state.has("D09Z01S02[N]", player) or \
                state.has("D09Z01S02[Cell1]", player) or \
                    state.has("D09Z01S02[Cell4]", player) or \
                        state.has("D09Z01S02[Cell3]", player) or \
                            state.has("D09Z01S02[Cell22]", player) or \
                                state.has("D09Z01S02[Cell23]", player))
    add_rule(world.get_entrance("D09Z01S02[Cell6]", player),
        lambda state: state.has("Key of the Scribe", player))
    set_rule(world.get_entrance("D09Z01S02[Cell4]", player),
        lambda state: state.has("D09Z01S02[NW]", player) or \
            state.has("D09Z01S02[N]", player) or \
                state.has("D09Z01S02[Cell1]", player) or \
                    state.has("D09Z01S02[Cell6]", player) or \
                        state.has("D09Z01S02[Cell3]", player) or \
                            state.has("D09Z01S02[Cell22]", player) or \
                                state.has("D09Z01S02[Cell23]", player))
    add_rule(world.get_entrance("D09Z01S02[Cell4]", player),
        lambda state: state.has("Key of the Inquisitor", player))
    set_rule(world.get_entrance("D09Z01S02[Cell2]", player),
        lambda state: state.has("D09Z01S02[SW]", player))
    set_rule(world.get_entrance("D09Z01S02[Cell3]", player),
        lambda state: state.has("D09Z01S02[NW]", player) or \
            state.has("D09Z01S02[N]", player) or \
                state.has("D09Z01S02[Cell1]", player) or \
                    state.has("D09Z01S02[Cell6]", player) or \
                        state.has("D09Z01S02[Cell4]", player) or \
                            state.has("D09Z01S02[Cell22]", player) or \
                                state.has("D09Z01S02[Cell23]", player))
    add_rule(world.get_entrance("D09Z01S02[Cell3]", player),
        lambda state: state.has("Key of the Secular", player))
    set_rule(world.get_entrance("D09Z01S02[Cell22]", player),
        lambda state: state.has("D09Z01S02[NW]", player) or \
            state.has("D09Z01S02[N]", player) or \
                state.has("D09Z01S02[Cell1]", player) or \
                    state.has("D09Z01S02[Cell6]", player) or \
                        state.has("D09Z01S02[Cell4]", player) or \
                            state.has("D09Z01S02[Cell3]", player) or \
                                state.has("D09Z01S02[Cell23]", player))
    set_rule(world.get_entrance("D09Z01S02[Cell23]", player),
        lambda state: state.has("D09Z01S02[NW]", player) or \
            state.has("D09Z01S02[N]", player) or \
                state.has("D09Z01S02[Cell1]", player) or \
                    state.has("D09Z01S02[Cell6]", player) or \
                        state.has("D09Z01S02[Cell4]", player) or \
                            state.has("D09Z01S02[Cell3]", player) or \
                                state.has("D09Z01S02[Cell22]", player))
    add_rule(world.get_entrance("D09Z01S02[Cell23]", player),
        lambda state: state.has("Key of the Secular", player))


    # D09Z01S03 (Wall of the Holy Prohibitions)
    # Items
    set_rule(world.get_location("WotHP: Quirce, Returned By The Flames", player),
        lambda state: state._blasphemous_can_beat_boss("Prison", difficulty, player))
    # Doors
    set_rule(world.get_entrance("D09Z01S03[W]", player),
        lambda state: state.has("D09Z01S03[N]", player) and \
            state._blasphemous_can_beat_boss("Prison", difficulty, player))
    

    # D09Z01S05 (Wall of the Holy Prohibitions)
    # Event
    set_rule(world.get_location("OpenedWOTHPGate", player),
        lambda state: state._blasphemous_opened_wothp_gate(player))


    # D09Z01S06 (Wall of the Holy Prohibitions)
    # No items
    # Doors
    set_rule(world.get_entrance("D09Z01S06[-E]", player),
        lambda state: state.has("Key of the High Peaks", player))


    # D09Z01S07 (Wall of the Holy Prohibitions)
    # No items
    # Doors
    set_rule(world.get_entrance("D09Z01S07[SW]", player),
        lambda state: state.has("D09Z01S07[SE]", player) or \
            state.has("D09Z01S07[W]", player) or \
                state.has("D09Z01S07[E]", player))
    set_rule(world.get_entrance("D09Z01S07[SE]", player),
        lambda state: state.has("D09Z01S07[SW]", player) or \
            state.has("D09Z01S07[W]", player) or \
                state.has("D09Z01S07[E]", player))
    set_rule(world.get_entrance("D09Z01S07[W]", player),
        lambda state: state.has("D09Z01S07[SW]", player) or \
            state.has("D09Z01S07[SE]", player) or \
                state.has("D09Z01S07[E]", player))
    set_rule(world.get_entrance("D09Z01S07[E]", player),
        lambda state: state.has("D09Z01S07[SW]", player) or \
            state.has("D09Z01S07[SE]", player) or \
                state.has("D09Z01S07[W]", player))
    set_rule(world.get_entrance("D09Z01S07[NW]", player),
        lambda state: state.has("D09Z01S07[N]", player))
    set_rule(world.get_entrance("D09Z01S07[N]", player),
        lambda state: state.has("D09Z01S07[NW]", player))
    set_rule(world.get_entrance("D09Z01S07[NE]", player),
        lambda state: state.has("D09Z01S07[SW]", player) or \
            state.has("D09Z01S07[SE]", player) or \
                state.has("D09Z01S07[W]", player) or \
                    state.has("D09Z01S07[E]", player))
    add_rule(world.get_entrance("D09Z01S07[NE]", player),
        lambda state: state.has("Blood Perpetuated in Sand", player))


    # D09Z01S08 (Wall of the Holy Prohibitions)
    # Items
    set_rule(world.get_location("WotHP: Collapsing floor ledge", player),
        lambda state: (state.has("D09Z01S08[W]", player) or \
            state.has("D09Z01S08[Cell18]", player)) and \
                state.has("OpenedWOTHPGate", player))
    # Doors
    set_rule(world.get_entrance("D09Z01S08[W]", player),
        lambda state: state.has("D09Z01S08[Cell14]", player))
    add_rule(world.get_entrance("D09Z01S08[W]", player),
        lambda state: state.has("OpenedWOTHPGate", player))
    set_rule(world.get_entrance("D09Z01S08[S]", player),
        lambda state: state.has("D09Z01S08[W]", player) or \
            state.has("D09Z01S08[Cell14]", player))
    set_rule(world.get_entrance("D09Z01S08[SE]", player),
        lambda state: state.has("D09Z01S08[Cell15]", player) or \
            state.has("D09Z01S08[Cell16]", player) or \
                state.has("D09Z01S08[Cell18]", player) or \
                    state.has("D09Z01S08[Cell17]", player) and \
                        state.has("Dash Ability", player))
    set_rule(world.get_entrance("D09Z01S08[NE]", player),
        lambda state: state.has("D09Z01S08[Cell7]", player) or \
            state.has("D09Z01S08[Cell17]", player) and \
                state.has("Dash Ability", player))
    set_rule(world.get_entrance("D09Z01S08[Cell14]", player),
        lambda state: state.has("D09Z01S08[W]", player))
    set_rule(world.get_entrance("D09Z01S08[Cell15]", player),
        lambda state: state.has("Key of the Scribe", player) and \
            (state.has("D09Z01S08[SE]", player) or \
                state.has("D09Z01S08[Cell16]", player) or \
                    state.has("D09Z01S08[Cell18]", player) or \
                        state.has("D09Z01S08[Cell17]", player) and \
                            state.has("Dash Ability", player)))
    set_rule(world.get_entrance("D09Z01S08[Cell7]", player),
        lambda state: state.has("Key of the Inquisitor", player) and \
            (state.has("D09Z01S08[NE]", player) or \
                state.has("D09Z01S08[Cell17]", player) and \
                    state.has("Dash Ability", player)))
    set_rule(world.get_entrance("D09Z01S08[Cell16]", player),
        lambda state: state.has("Key of the Inquisitor", player) and \
            (state.has("D09Z01S08[SE]", player) or \
                state.has("D09Z01S08[Cell15]", player) or \
                    state.has("D09Z01S08[Cell18]", player) or \
                        state.has("D09Z01S08[Cell17]", player) and \
                            state.has("Dash Ability", player)))
    set_rule(world.get_entrance("D09Z01S08[Cell18]", player),
        lambda state: state.has("Key of the Scribe", player) and \
            (state.has("D09Z01S08[SE]", player) or \
                state.has("D09Z01S08[Cell15]", player) or \
                    state.has("D09Z01S08[Cell16]", player) or \
                        state.has("D09Z01S08[Cell17]", player) and \
                            state.has("Dash Ability", player)))


    # D09Z01S09 (Wall of the Holy Prohibitions)
    # Items
    set_rule(world.get_location("WotHP: Lower west room, top ledge", player),
        lambda state: state.has("D09Z01S09[Cell24]", player) or \
            state.has("Dash Ability", player) and \
                (state.has("D09Z01S09[NW]", player) or \
                    state.has("D09Z01S09[Cell19]", player)))
    # Doors
    set_rule(world.get_entrance("D09Z01S09[SW]", player),
        lambda state: state.has("D09Z01S09[Cell21]", player) or \
            state.has("D09Z01S09[Cell20]", player) or \
                state.has("D09Z01S09[E]", player) or \
                    state.has("Dash Ability", player))
    set_rule(world.get_entrance("D09Z01S09[NW]", player),
        lambda state: state.has("D09Z01S09[Cell19]", player) or \
            state.has("D09Z01S09[Cell24]", player))
    add_rule(world.get_entrance("D09Z01S09[NW]", player),
        lambda state: state.has("D09Z01S09[Cell19]", player) or \
            state.has("Dash Ability", player))
    set_rule(world.get_entrance("D09Z01S09[E]", player),
        lambda state: state.has("D09Z01S09[Cell21]", player) or \
            state.has("D09Z01S09[Cell20]", player) or \
                state.has("D09Z01S09[SW]", player) or \
                    state.has("Dash Ability", player))
    set_rule(world.get_entrance("D09Z01S09[Cell24]", player),
        lambda state: state.has("D09Z01S09[NW]", player) or \
            state.has("D09Z01S09[Cell19]", player))
    add_rule(world.get_entrance("D09Z01S09[Cell24]", player),
        lambda state: state.has("Dash Ability", player))
    set_rule(world.get_entrance("D09Z01S09[Cell24]", player),
        lambda state: state.has("D09Z01S09[NW]", player) or \
            state.has("D09Z01S09[Cell24]", player))
    add_rule(world.get_entrance("D09Z01S09[Cell19]", player),
        lambda state: state.has("D09Z01S09[NW]", player) or \
            state.has("Dash Ability", player))
    set_rule(world.get_entrance("D09Z01S09[Cell20]", player),
        lambda state: state.has("Key of the Scribe", player) and \
            (state.has("D09Z01S09[Cell21]", player) or \
                state.has("D09Z01S09[SW]", player) or \
                    state.has("D09Z01S09[E]", player) or \
                        state.has("Dash Ability", player)))
    set_rule(world.get_entrance("D09Z01S09[Cell21]", player),
        lambda state: state.has("Key of the Inquisitor", player) and \
            (state.has("D09Z01S09[Cell20]", player) or \
                state.has("D09Z01S09[SW]", player) or \
                    state.has("D09Z01S09[E]", player) or \
                        state.has("Dash Ability", player)))


    # D09Z01S10 (Wall of the Holy Prohibitions)
    # Items
    set_rule(world.get_location("WotHP: Lower east room, top bronze cell", player),
        lambda state: state.has("D09Z01S10[Cell13]", player))
    set_rule(world.get_location("WotHP: Lower east room, hidden ledge", player),
        lambda state: state.has("D09Z01S10[W]", player) or \
            state.has("D09Z01S10[Cell12]", player) or \
                state.has("D09Z01S10[Cell10]", player) or \
                    state.has("D09Z01S10[Cell11]", player))
    # Doors
    set_rule(world.get_entrance("D09Z01S10[W]", player),
        lambda state: state.has("D09Z01S10[Cell12]", player) or \
            state.has("D09Z01S10[Cell10]", player) or \
                state.has("D09Z01S10[Cell11]", player))
    set_rule(world.get_entrance("D09Z01S10[Cell12]", player),
        lambda state: state.has("D09Z01S10[W]", player) or \
            state.has("D09Z01S10[Cell10]", player) or \
                state.has("D09Z01S10[Cell11]", player))
    add_rule(world.get_entrance("D09Z01S10[Cell12]", player),
        lambda state: state.has("Key of the Secular", player))
    set_rule(world.get_entrance("D09Z01S10[Cell10]", player),
        lambda state: state.has("D09Z01S10[W]", player) or \
            state.has("D09Z01S10[Cell12]", player) or \
                state.has("D09Z01S10[Cell11]", player))
    add_rule(world.get_entrance("D09Z01S10[Cell10]", player),
        lambda state: state.has("Key of the Scribe", player))
    set_rule(world.get_entrance("D09Z01S10[Cell11]", player),
        lambda state: state.has("D09Z01S10[W]", player) or \
            state.has("D09Z01S10[Cell12]", player) or \
                state.has("D09Z01S10[Cell10]", player))
    add_rule(world.get_entrance("D09Z01S10[Cell11]", player),
        lambda state: state.has("Key of the Scribe", player))
    
    # D09BZ01S01 (Wall of the Holy Prohibitions - Inside cells)
    # Items
    set_rule(world.get_location("WotHP: Upper east room, center cell ledge", player),
        lambda state: state.has("D09BZ01S01[Cell22]", player))
    set_rule(world.get_location("WotHP: Upper east room, center cell floor", player),
        lambda state: state.has("D09BZ01S01[Cell22]", player) or \
            state.has("D09BZ01S01[Cell23]", player))
    set_rule(world.get_location("WotHP: Upper east room, top bronze cell", player),
        lambda state: state.has("D09BZ01S01[Cell1]", player))
    set_rule(world.get_location("WotHP: Upper east room, top silver cell", player),
        lambda state: state.has("D09BZ01S01[Cell6]", player))
    set_rule(world.get_location("WotHP: Upper west room, top silver cell", player),
        lambda state: state.has("D09BZ01S01[Cell14]", player) or \
            state.has("D09BZ01S01[Cell15]", player))
    set_rule(world.get_location("WotHP: Upper west room, center gold cell", player),
        lambda state: state.has("D09BZ01S01[Cell16]", player))
    set_rule(world.get_location("WotHP: Lower west room, bottom gold cell", player),
        lambda state: state.has("D09BZ01S01[Cell21]", player) and \
            state.has("Blood Perpetuated in Sand", player) and \
                state._blasphemous_can_climb_on_root(player) and \
                    state._blasphemous_can_survive_poison(difficulty, player, 2) and \
                        state.has("Dash Ability", player))
    set_rule(world.get_location("WotHP: Lower east room, top silver cell", player),
        lambda state: state.has("D09BZ01S01[Cell10]", player))
    set_rule(world.get_location("WotHP: Lower east room, bottom silver cell", player),
        lambda state: state.has("D09BZ01S01[Cell11]", player) and \
            (state._blasphemous_can_survive_poison(difficulty, player, 1) and \
                state.has("Dash Ability", player) or \
                    state.has_any({"Debla of the Lights", "Taranto to my Sister", "Cante Jondo of the Three Sisters", "Verdiales of the Forsaken Hamlet", "Cantina of the Blue Rose"}, player) or \
                        state._blasphemous_aubade(player)))
    # Doors
    set_rule(world.get_entrance("D09BZ01S01[Cell2]", player),
        lambda state: state.has("D09BZ01S01[Cell3]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell3]", player),
        lambda state: state.has("D09BZ01S01[Cell2]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell4]", player),
        lambda state: state.has("D09BZ01S01[Cell5]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell5]", player),
        lambda state: state.has("D09BZ01S01[Cell5]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell12]", player),
        lambda state: state.has("D09BZ01S01[Cell13]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell13]", player),
        lambda state: state.has("D09BZ01S01[Cell12]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell14]", player),
        lambda state: state.has("D09BZ01S01[Cell15]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell15]", player),
        lambda state: state.has("D09BZ01S01[Cell14]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell17]", player),
        lambda state: state.has("D09BZ01S01[Cell18]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell19]", player),
        lambda state: state.has("D09BZ01S01[Cell20]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell20]", player),
        lambda state: state.has("D09BZ01S01[Cell19]", player))
    set_rule(world.get_entrance("D09BZ01S01[Cell23]", player),
        lambda state: state.has("D09BZ01S01[Cell22]", player))
    add_rule(world.get_entrance("D09BZ01S01[Cell23]", player),
        lambda state: state.has("Key of the Secular", player))


    # D17Z01S01 (Brotherhood of the Silent Sorrow)
    set_rule(world.get_location("BotSS: Starting room ledge", player),
        lambda state: state.has("D17Z01S01[Cherubs3]", player))
    set_rule(world.get_location("BotSS: Starting room Child of Moonlight", player),
        lambda state: state.has("D17Z01S01[Cherubs1]", player) or \
            state.has("Taranto to my Sister", player) or \
                (state._blasphemous_can_climb_on_root(player) or \
                    state._blasphemous_can_cross_gap(difficulty, player, 9)) and \
                        (state.has_any({"Blood Perpetuated in Sand", "Purified Hand of the Nun", "Debla of the Lights", "Verdiales of the Forsaken Hamlet", "Cloistered Ruby"}, player) or \
                            state._blasphemous_tirana(player)))


    # D17Z01S02 (Brotherhood of the Silent Sorrow)
    # No items
    # Doors
    set_rule(world.get_entrance("D17Z01S02[W]", player),
        lambda state: state.has("Dash Ability", player))
    set_rule(world.get_entrance("D17Z01S02[E]", player),
        lambda state: state.has("D17Z01S02[N]", player) or \
            state.has("Dash Ability", player))
    set_rule(world.get_entrance("D17Z01S02[N]", player),
        lambda state: state.has("Blood Perpetuated in Sand", player) and \
            (state.has("D17Z01S02[E]", player) or \
                state.has("D17Z01S02[W]", player) and \
                    state.has("Dash Ability", player)))


    # D17Z01S03 (Brotherhood of the Silent Sorrow)
    # No items
    # Doors
    set_rule(world.get_entrance("D17Z01S03[relic]", player),
        lambda state: state.has("Key to the Chamber of the Eldest Brother", player))


    # D17Z01S04 (Brotherhood of the Silent Sorrow)
    # Items
    if world.boots_of_pleading[player]:
        set_rule(world.get_location("BotSS: 2nd meeting with Redento", player),
            lambda state: state._blasphemous_redento(blasphemousworld, player, 2))
    # Doors
    set_rule(world.get_entrance("D17Z01S04[N]", player),
        lambda state: state.has("D17Z01S04[FrontR]", player))
    set_rule(world.get_entrance("D17Z01S04[FrontR]", player),
        lambda state: state.has("D17Z01S04[N]", player))
    # Event
    set_rule(world.get_location("OpenedBOTSSLadder", player),
        lambda state: state._blasphemous_opened_botss_ladder(player))


    # D17Z01S05 (Brotherhood of the Silent Sorrow)
    # No items
    # Doors
    set_rule(world.get_entrance("D17Z01S05[S]", player),
        lambda state: state.has("OpenedBOTSSLadder", player))


    # D17Z01S10 (Brotherhood of the Silent Sorrow)
    # No items
    # Doors
    set_rule(world.get_entrance("D17Z01S10[W]", player),
        lambda state: state.has_any({"Blood Perpetuated in Sand", "Purified Hand of the Nun"}, player))


    # D17Z01S11 (Brotherhood of the Silent Sorrow)
    # Items
    set_rule(world.get_location("BotSS: Warden of the Silent Sorrow", player),
        lambda state: state._blasphemous_can_beat_boss("Brotherhood", difficulty, player))
    # Doors
    set_rule(world.get_entrance("D17Z01S11[W]", player),
        lambda state: state._blasphemous_can_beat_boss("Brotherhood", difficulty, player))
    set_rule(world.get_entrance("D17Z01S11[E]", player),
        lambda state: state._blasphemous_can_beat_boss("Brotherhood", difficulty, player))


    # D17Z01S14 (Brotherhood of the Silent Sorrow)
    # Items
    set_rule(world.get_location("BotSS: Outside church", player),
        lambda state: state.has("D17Z01S14[W]", player) or \
            state.has("Blood Perpetuated in Sand", player))
    # Doors
    set_rule(world.get_entrance("D17Z01S14[W]", player),
        lambda state: state.has("Incomplete Scapular", player) and \
            (state.has("Blood Perpetuated in Sand", player)))
    set_rule(world.get_entrance("D17Z01S14[E]", player),
        lambda state: state.has("Blood Perpetuated in Sand", player))
    set_rule(world.get_entrance("D17Z01S14[-Cherubs1]", player),
        lambda state: state.has("Linen of Golden Thread", player) and \
            (state.has("D17Z01S14[W]", player) or \
                state.has("Blood Perpetuated in Sand", player) or \
                    state._blasphemous_can_cross_gap(difficulty, player, 11)))
    set_rule(world.get_entrance("D17Z01S14[-Cherubs2]", player),
        lambda state: state.has("Linen of Golden Thread", player) and \
            (state.has("D17Z01S14[E]", player) and \
                state._blasphemous_can_cross_gap(difficulty, player, 8) or \
                    state.has("D17Z01S14[W]", player) and \
                        state._blasphemous_can_cross_gap(difficulty, player, 10) or \
                            state.has("Blood Perpetuated in Sand", player)))
    set_rule(world.get_entrance("D17Z01S14[-Cherubs3]", player),
        lambda state: state.has("Linen of Golden Thread", player) and \
            (state.has("D17Z01S14[E]", player) or \
                state.has("Blood Perpetuated in Sand", player)))


    # D17Z01S15 (Brotherhood of the Silent Sorrow)
    # Items
    set_rule(world.get_location("BotSS: Esdras' final gift", player),
        lambda state: state._blasphemous_can_beat_boss("Bridge", difficulty, player) and \
            state.has_group("wounds", player, 3))
    set_rule(world.get_location("BotSS: Crisanta's gift", player),
        lambda state: state._blasphemous_can_beat_boss("Rooftops", difficulty, player) and \
            state.has("Apodictic Heart of Mea Culpa", player))
    # No doors


    # D17BZ02S01 (Brotherhood of the Silent Sorrow - Platforming challenge)
    # Items
    set_rule(world.get_location("BotSS: Platforming gauntlet", player),
        lambda state: state.has("D17BZ02S01[FrontR]", player) or \
            state.has_all({"Dash Ability", "Wall Climb Ability"}, player))
    # Doors
    set_rule(world.get_entrance("D17BZ02S01[FrontR]", player),
        lambda state: state.has_all({"Dash Ability", "Wall Climb Ability"}, player))


    # D20Z01S04 (Echoes of Salt)
    # No items
    # Doors
    set_rule(world.get_entrance("D20Z01S04[E]", player),
        lambda state: state.has("OpenedDCGateW", player))


    # D20Z01S09 (Echoes of Salt)
    # Items
    set_rule(world.get_location("EoS: Lantern jump near elevator", player),
        lambda state: state.has("D20Z01S09[W]", player) or \
            state.has("Dash Ability", player))
    # Doors
    set_rule(world.get_entrance("D20Z01S09[W]", player),
        lambda state: state.has("Dash Ability", player))
    set_rule(world.get_entrance("D20Z01S09[E]", player),
        lambda state: state.has_all({"Blood Perpetuated in Sand", "Dash Ability"}, player))


    # D20Z01S10 (Echoes of Salt)
    # No items
    # Doors
    set_rule(world.get_entrance("D20Z01S10[W]", player),
        lambda state: state.has_all({"Blood Perpetuated in Sand", "Dash Ability"}, player))
    set_rule(world.get_entrance("D20Z01S10[E]", player),
        lambda state: state.has_all({"Blood Perpetuated in Sand", "Dash Ability"}, player))


    # D20Z02S03 (Mourning and Havoc)
    # No items
    # Doors
    set_rule(world.get_entrance("D20Z02S03[NE]", player),
        lambda state: state._blasphemous_can_walk_on_root(player) or \
            state._blasphemous_can_cross_gap(difficulty, player, 5))


    # D20Z02S04 (Mourning and Havoc)
    # No items
    # Doors
    set_rule(world.get_entrance("D20Z02S04[W]", player),
        lambda state: state.has("Dash Ability", player))
    set_rule(world.get_entrance("D20Z02S04[E]", player),
        lambda state: state.has("Dash Ability", player))


    # D20Z02S05 (Mourning and Havoc)
    # No items
    # Doors
    set_rule(world.get_entrance("D20Z02S05[NW]", player),
        lambda state: state.has("Nail Uprooted from Dirt", player) or \
            state._blasphemous_can_cross_gap(difficulty, player, 3))


    # D20Z02S06 (Mourning and Havoc)
    # No items
    # Doors
    set_rule(world.get_entrance("D20Z02S06[NW]", player),
        lambda state: state.has("D20Z02S06[NE]", player) or \
            state.has("Purified Hand of the Nun", player) or \
                state._blasphemous_can_climb_on_root(player) or \
                    state._blasphemous_can_dive_laser(difficulty, player))
    set_rule(world.get_entrance("D20Z02S06[NE]", player),
        lambda state: state.has("D20Z02S06[NW]", player) or \
            state.has("Purified Hand of the Nun", player) or \
                state._blasphemous_can_climb_on_root(player) or \
                    state._blasphemous_can_dive_laser(difficulty, player))


    # D20Z02S08 (Mourning and Havoc)
    # Items
    set_rule(world.get_location("MaH: Sierpes", player),
        lambda state: state._blasphemous_can_beat_boss("Mourning", difficulty, player))
    set_rule(world.get_location("MaH: Sierpes' eye", player),
        lambda state: state._blasphemous_can_beat_boss("Mourning", difficulty, player))
    # No doors


    # D20Z02S11 (Mourning and Havoc)
    # No items
    # Doors
    set_rule(world.get_entrance("D20Z02S11[NW]", player),
        lambda state: state.has("D20Z02S11[E]", player))
    set_rule(world.get_entrance("D20Z02S11[NW]", player),
        lambda state: state._blasphemous_mourning_skips_allowed(difficulty) and \
            (state.has("Purified Hand of the Nun", player) or \
                state._blasphemous_can_break_tirana(difficulty, player) or \
                    state.has("D20Z02S11[E]", player)))
    set_rule(world.get_entrance("D20Z02S11[E]", player),
        lambda state: state._blasphemous_mourning_skips_allowed(difficulty) and \
            (state.has("Purified Hand of the Nun", player) or \
                state._blasphemous_can_break_tirana(difficulty, player) or \
                    state.has("D20Z02S11[NW]", player) and \
                        state._blasphemous_can_cross_gap(difficulty, player, 5)))
    

    # Misc Items
    set_rule(world.get_location("Second red candle", player),
        lambda state: state.has("Bead of Red Wax", player) and \
            (state.can_reach(world.get_region("D02Z03S06", player), player) or \
                    state.has("D05Z01S02[W]", player)))
    set_rule(world.get_location("Third red candle", player),
        lambda state: state.has("Bead of Red Wax", player) and \
            state.has("D05Z01S02[W]", player) and \
                state.can_reach(world.get_region("D02Z03S06", player), player))
    set_rule(world.get_location("Second blue candle", player),
        lambda state: state.has("Bead of Blue Wax", player) and \
            (state.has("OpenedBOTSSLadder", player) or \
                state.can_reach(world.get_region("D01Z04S16", player), player)))
    set_rule(world.get_location("Third blue candle", player),
        lambda state: state.has("Bead of Blue Wax", player) and \
            state.has("OpenedBOTSSLadder", player) and \
                state.can_reach(world.get_region("D01Z04S16", player), player))
    set_rule(world.get_location("Defeat 1 Amanecida", player),
        lambda state: state._blasphemous_amanecida_rooms(blasphemousworld, difficulty, player, 1))
    set_rule(world.get_location("Defeat 2 Amanecidas", player),
        lambda state: state._blasphemous_amanecida_rooms(blasphemousworld, difficulty, player, 2))
    set_rule(world.get_location("Defeat 3 Amanecidas", player),
        lambda state: state._blasphemous_amanecida_rooms(blasphemousworld, difficulty, player, 3))
    set_rule(world.get_location("Defeat 4 Amanecidas", player),
        lambda state: state._blasphemous_amanecida_rooms(blasphemousworld, difficulty, player, 4))
    set_rule(world.get_location("Defeat all Amanecidas", player),
        lambda state: state._blasphemous_amanecida_rooms(blasphemousworld, difficulty, player, 4))
    set_rule(world.get_location("Confessor Dungeon 1 main", player),
        lambda state: state.has("Weight of True Guilt", player) and \
            state._blasphemous_guilt_rooms(player, 1))
    set_rule(world.get_location("Confessor Dungeon 2 main", player),
        lambda state: state.has("Weight of True Guilt", player) and \
            state._blasphemous_guilt_rooms(player, 2))
    set_rule(world.get_location("Confessor Dungeon 3 main", player),
        lambda state: state.has("Weight of True Guilt", player) and \
            state._blasphemous_guilt_rooms(player, 3))
    set_rule(world.get_location("Confessor Dungeon 4 main", player),
        lambda state: state.has("Weight of True Guilt", player) and \
            state._blasphemous_guilt_rooms(player, 4))
    set_rule(world.get_location("Confessor Dungeon 5 main", player),
        lambda state: state.has("Weight of True Guilt", player) and \
            state._blasphemous_guilt_rooms(player, 5))
    set_rule(world.get_location("Confessor Dungeon 6 main", player),
        lambda state: state.has("Weight of True Guilt", player) and \
            state._blasphemous_guilt_rooms(player, 6))
    set_rule(world.get_location("Confessor Dungeon 7 main", player),
        lambda state: state.has("Weight of True Guilt", player) and \
            state._blasphemous_guilt_rooms(player, 7))
    set_rule(world.get_location("Confessor Dungeon 1 extra", player),
        lambda state: state.has("Weight of True Guilt", player) and \
            state._blasphemous_guilt_rooms(player, 1))
    set_rule(world.get_location("Confessor Dungeon 2 extra", player),
        lambda state: state.has("Weight of True Guilt", player) and \
            state._blasphemous_guilt_rooms(player, 2))
    set_rule(world.get_location("Confessor Dungeon 3 extra", player),
        lambda state: state.has("Weight of True Guilt", player) and \
            state._blasphemous_guilt_rooms(player, 3))
    set_rule(world.get_location("Confessor Dungeon 4 extra", player),
        lambda state: state.has("Weight of True Guilt", player) and \
            state._blasphemous_guilt_rooms(player, 4))
    set_rule(world.get_location("Confessor Dungeon 5 extra", player),
        lambda state: state.has("Weight of True Guilt", player) and \
            state._blasphemous_guilt_rooms(player, 5))
    set_rule(world.get_location("Confessor Dungeon 6 extra", player),
        lambda state: state.has("Weight of True Guilt", player) and \
            state._blasphemous_guilt_rooms(player, 6))
    set_rule(world.get_location("Confessor Dungeon 7 extra", player),
        lambda state: state.has("Weight of True Guilt", player) and \
            state._blasphemous_guilt_rooms(player, 7))
    set_rule(world.get_location("Skill 1, Tier 1", player),
        lambda state: state._blasphemous_sword_rooms(player, 1))
    set_rule(world.get_location("Skill 1, Tier 2", player),
        lambda state: state._blasphemous_sword_rooms(player, 2))
    set_rule(world.get_location("Skill 1, Tier 3", player),
        lambda state: state._blasphemous_sword_rooms(player, 4))
    set_rule(world.get_location("Skill 2, Tier 1", player),
        lambda state: state._blasphemous_sword_rooms(player, 1))
    set_rule(world.get_location("Skill 2, Tier 2", player),
        lambda state: state._blasphemous_sword_rooms(player, 3))
    set_rule(world.get_location("Skill 2, Tier 3", player),
        lambda state: state._blasphemous_sword_rooms(player, 6))
    set_rule(world.get_location("Skill 3, Tier 1", player),
        lambda state: state._blasphemous_sword_rooms(player, 2))
    set_rule(world.get_location("Skill 3, Tier 2", player),
        lambda state: state._blasphemous_sword_rooms(player, 5))
    set_rule(world.get_location("Skill 3, Tier 3", player),
        lambda state: state._blasphemous_sword_rooms(player, 7))
    set_rule(world.get_location("Skill 4, Tier 1", player),
        lambda state: state._blasphemous_sword_rooms(player, 1))
    set_rule(world.get_location("Skill 4, Tier 2", player),
        lambda state: state._blasphemous_sword_rooms(player, 3))
    set_rule(world.get_location("Skill 4, Tier 3", player),
        lambda state: state._blasphemous_sword_rooms(player, 6))
    set_rule(world.get_location("Skill 5, Tier 1", player),
        lambda state: state._blasphemous_sword_rooms(player, 1))
    set_rule(world.get_location("Skill 5, Tier 2", player),
        lambda state: state._blasphemous_sword_rooms(player, 2))
    set_rule(world.get_location("Skill 5, Tier 3", player),
        lambda state: state._blasphemous_sword_rooms(player, 4))