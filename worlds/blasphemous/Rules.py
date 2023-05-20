from worlds.generic.Rules import set_rule, add_rule
from ..AutoWorld import LogicMixin


class BlasphemousLogic(LogicMixin):
    def _blasphemous_blood_relic(self, player):
        return self.has("Blood Perpetuated in Sand", player)

    def _blasphemous_water_relic(self, player):
        return self.has("Nail Uprooted from Dirt", player)

    def _blasphemous_corpse_relic(self, player):
        return self.has("Shroud of Dreamt Sins", player)

    def _blasphemous_fall_relic(self, player):
        return self.has("Linen of Golden Thread", player)

    def _blasphemous_miasma_relic(self, player):
        return self.has("Silvered Lung of Dolphos", player)
    
    def _blasphemous_root_relic(self, player):
        return self.has("Three Gnarled Tongues", player)

    def _blasphemous_open_holes(self, player):
        return self.has_any({"Dive Skill", "Charged Skill"}, player) or \
            self.has_group("prayer", player, 1) or \
                (self.has_any({"Tirana of the Celestial Bastion", "Aubade of the Nameless Guardian"}, player) and \
                    self.has("Fervour Upgrade", player, 2))

    def _blasphemous_bell(self, player):
        return self.has("Petrified Bell", player)

    def _blasphemous_bead(self, player):
        return self.has("Weight of True Guilt", player)

    def _blasphemous_cloth(self, player):
        return self.has("Linen Cloth", player)

    def _blasphemous_pre_egg(self, player):
        return self.has("Egg of Deformity", player)

    def _blasphemous_egg(self, player):
        return self.has("Hatched Egg of Deformity", player)

    def _blasphemous_hand(self, player):
        return self.has("Severed Hand", player)

    def _blasphemous_chalice(self, player):
        return self.has("Chalice of Inverted Verses", player)

    def _blasphemous_thimble(self, player):
        return self.has("Empty Golden Thimble", player)

    def _blasphemous_full_thimble(self, player):
        return self.has("Golden Thimble Filled with Burning Oil", player)

    def _blasphemous_flowers(self, player):
        return self.has("Dried Flowers bathed in Tears", player)

    def _blasphemous_redento_old(self, player):
        return self.has_all({"Little Toe made of Limestone", "Big Toe made of Limestone", \
            "Fourth Toe made of Limestone"}, player) and \
                self.has("Knot of Rosary Rope", player)

    def _blasphemous_cord(self, player):
        return self.has("Cord of the True Burying", player)

    def _blasphemous_marks(self, player):
        return self.has_all({"Mark of the First Refuge", "Mark of the Second Refuge", \
            "Mark of the Third Refuge"}, player)

    def _blasphemous_red_wax(self, player):
        return self.has("Bead of Red Wax", player)
    
    def _blasphemous_blue_wax(self, player):
        return self.has("Bead of Blue Wax", player)

    def _blasphemous_both_wax(self, player):
        return self.has("Bead of Red Wax", player, 3) and \
            self.has("Bead of Blue Wax", player, 3)

    def _blasphemous_elder_key(self, player):
        return self.has("Key to the Chamber of the Eldest Brother", player)

    def _blasphemous_bronze_key(self, player):
        return self.has("Key of the Secular", player)

    def _blasphemous_silver_key(self, player):
        return self.has("Key of the Scribe", player)

    def _blasphemous_gold_key(self, player):
        return self.has("Key of the Inquisitor", player)

    def _blasphemous_high_key(self, player):
        return self.has("Key of the High Peaks", player)

    def _blasphemous_wood_key(self, player):
        return self.has("Key Grown from Twisted Wood", player)

    def _blasphemous_scapular(self, player):
        return self.has("Incomplete Scapular", player)

    def _blasphemous_heart_c(self, player):
        return self.has("Apodictic Heart of Mea Culpa", player)

    def _blasphemous_eyes(self, player):
        return self.has("Severed Right Eye of the Traitor", player) and \
            self.has("Broken Left Eye of the Traitor", player)

    def _blasphemous_debla(self, player):
        return self.has("Debla of the Lights", player)

    def _blasphemous_taranto(self, player):
        return self.has("Taranto to my Sister", player)

    def _blasphemous_tirana(self, player):
        return self.has("Tirana of the Celestial Bastion", player) and \
            self.has("Fervour Upgrade", player, 2)

    def _blasphemous_aubade(self, player):
        return self.has("Aubade of the Nameless Guardian", player) and \
            self.has("Fervour Upgrade", player, 2)

    def _blasphemous_cherub_6(self, player):
        return self.has_any({"Debla of the Lights", "Taranto to my Sister", "Verdiales of the Forsaken Hamlet", \
            "Cloistered Ruby"}, player) or \
                (self.has("Tirana of the Celestial Bastion", player) and \
                    self.has("Fervour Upgrade", player, 2))

    def _blasphemous_cherub_13(self, player):
        return self.has_any({"Ranged Skill", "Debla of the Lights", "Taranto to my Sister", \
            "Cante Jondo of the Three Sisters", "Cloistered Ruby"}, player) or \
                    (self.has_any({"Aubade of the Nameless Guardian", "Tirana of the Celestial Bastion"}, player) and \
                        self.has("Fervour Upgrade", player, 2))
    
    def _blasphemous_cherub_20(self, player):
        return self.has_any({"Debla of the Lights", "Lorqiana", "Zarabanda of the Safe Haven", "Taranto to my Sister", \
            "Cante Jondo of the Three Sisters", "Cloistered Ruby"}, player) or \
                    (self.has_any({"Aubade of the Nameless Guardian", "Tirana of the Celestial Bastion"}, player) and \
                        self.has("Fervour Upgrade", player, 2))

    def _blasphemous_cherub_21(self, player):
        return self.has_any({"Debla of the Lights", "Taranto to my Sister", "Cante Jondo of the Three Sisters", \
            "Verdiales of the Forsaken Hamlet", "Cloistered Ruby"}, player) or \
                (self.has("Tirana of the Celestial Bastion", player) and \
                    self.has("Fervour Upgrade", player, 2))
    
    def _blasphemous_cherub_22_23_31_32(self, player):
        return self.has_any({"Debla of the Lights", "Taranto to my Sister", "Cloistered Ruby"}, player)

    def _blasphemous_cherub_24_33(self, player):
        return self.has_any({"Debla of the Lights", "Taranto to my Sister", "Cante Jondo of the Three Sisters", \
            "Cloistered Ruby"}, player) or \
                (self.has("Tirana of the Celestial Bastion", player) and \
                    self.has("Fervour Upgrade", player, 2))

    def _blasphemous_cherub_25(self, player):
        return self.has_any({"Debla of the Lights", "Lorquiana", "Taranto to my Sister", \
            "Cante Jondo of the Three Sisters", "Verdiales of the Forsaken Hamlet", "Cantina of the Blue Rose", \
                "Cloistered Ruby"}, player) or \
                    (self.has("Aubade of the Nameless Guardian", player) and \
                        self.has("Fervour Upgrade", player, 2))

    def _blasphemous_cherub_27(self, player):
        return self.has_any({"Ranged Skill", "Debla of the Lights", "Lorquiana", "Taranto to my Sister", \
            "Cante Jondo of the Three Sisters", "Cantina of the Blue Rose", "Cloistered Ruby"}, player) or \
                    (self.has("Aubade of the Nameless Guardian", player) and \
                        self.has("Fervour Upgrade", player, 2))

    def _blasphemous_cherub_38(self, player):
        return self.has_any({"Ranged Skill", "Lorquiana", "Cante Jondo of the Three Sisters", \
            "Cantina of the Blue Rose", "Cloistered Ruby"}, player) or \
                (self.has("The Young Mason's Wheel", player) and \
                    self.has("Brilliant Heart of Dawn", player)) or \
                        (self.has("Aubade of the Nameless Guardian", player) and \
                            self.has("Fervour Upgrade", player, 2))

    def _blasphemous_wheel(self, player):
        return self.has("The Young Mason's Wheel", player)

    def _blasphemous_dawn_heart(self, player):
        return self.has("Brilliant Heart of Dawn", player)

    def _blasphemous_tirso_1(self, player):
        return self.has_group("tirso", player, 1)
    
    def _blasphemous_tirso_2(self, player):
        return self.has_group("tirso", player, 2)

    def _blasphemous_tirso_3(self, player):
        return self.has_group("tirso", player, 3)

    def _blasphemous_tirso_4(self, player):
        return self.has_group("tirso", player, 4)

    def _blasphemous_tirso_5(self, player):
        return self.has_group("tirso", player, 5)

    def _blasphemous_tirso_6(self, player):
        return self.has_group("tirso", player, 6)

    def _blasphemous_tentudia_1(self, player):
        return self.has_group("tentudia", player, 1)

    def _blasphemous_tentudia_2(self, player):
        return self.has_group("tentudia", player, 2)

    def _blasphemous_tentudia_3(self, player):
        return self.has_group("tentudia", player, 3)

    def _blasphemous_altasgracias_3(self, player):
        return self.has_group("egg", player, 3)

    def _blasphemous_cherubs_20(self, player):
        return self.has("Child of Moonlight", player, 20)

    def _blasphemous_cherubs_all(self, player):
        return self.has("Child of Moonlight", player, 38)

    def _blasphemous_bones_4(self, player):
        return self.has_group("bones", player, 4)

    def _blasphemous_bones_8(self, player):
        return self.has_group("bones", player, 8)

    def _blasphemous_bones_12(self, player):
        return self.has_group("bones", player, 12)
    
    def _blasphemous_bones_16(self, player):
        return self.has_group("bones", player, 16)

    def _blasphemous_bones_20(self, player):
        return self.has_group("bones", player, 20)

    def _blasphemous_bones_24(self, player):
        return self.has_group("bones", player, 24)

    def _blasphemous_bones_28(self, player):
        return self.has_group("bones", player, 28)

    def _blasphemous_bones_30(self, player):
        return self.has_group("bones", player, 30)

    def _blasphemous_bones_32(self, player):
        return self.has_group("bones", player, 32)

    def _blasphemous_bones_36(self, player):
        return self.has_group("bones", player, 36)

    def _blasphemous_bones_40(self, player):
        return self.has_group("bones", player, 40)

    def _blasphemous_bones_44(self, player):
        return self.has_group("bones", player, 44)

    def _blasphemous_sword_1(self, player):
        return self.has("Mea Culpa Upgrade", player)

    def _blasphemous_sword_2(self, player):
        return self.has("Mea Culpa Upgrade", player, 2)
    
    def _blasphemous_sword_3(self, player):
        return self.has("Mea Culpa Upgrade", player, 3)

    def _blasphemous_sword_4(self, player):
        return self.has("Mea Culpa Upgrade", player, 4)

    def _blasphemous_sword_5(self, player):
        return self.has("Mea Culpa Upgrade", player, 5)

    def _blasphemous_sword_6(self, player):
        return self.has("Mea Culpa Upgrade", player, 6)

    def _blasphemous_sword_7(self, player):
        return self.has("Mea Culpa Upgrade", player, 7)

    def _blasphemous_ranged(self, player):
        return self.has("Ranged Skill", player)

    def _blasphemous_bridge_access(self, player):
        return self.has_group("wounds", player, 3)

    def _blasphemous_ex_bridge_access(self, player):
        return self.has_group("wounds", player, 3) or \
            (self.has("Brilliant Heart of Dawn", player) and \
                self.has("Ranged Skill", player) and \
                    self.has("Blood Perpetuated in Sand", player)) or \
                        (self.has("Blood Perpetuated in Sand", player) and \
                            self.has("Tirana of the Celestial Bastion", player) and \
                                self.has("Fervour Upgrade", player, 2))

    def _blasphemous_1_mask(self, player):
        return self.has_group("masks", player, 1)

    def _blasphemous_2_masks(self, player):
        return self.has_group("masks", player, 2)

    def _blasphemous_3_masks(self, player):
        return self.has_group("masks", player, 3)

    def _blasphemous_laudes_gate(self, player): 
        return self.has("Verses Spun from Gold", player, 4)

    # Ten Piedad, Tres Angustias, Our Lady of the Charred Visage
    def _blasphemous_wound_boss_easy(self, player):
        return self.has("Mea Culpa Upgrade", player, 2) and \
            self.has_group("power", player, 3)

    def _blasphemous_wound_boss_normal(self, player):
        return self.has("Mea Culpa Upgrade", player, 1)

    def _blasphemous_wound_boss_hard(self, player):
        return True

    # Esdras
    def _blasphemous_esdras_boss_easy(self, player):
        return self.has("Mea Culpa Upgrade", player, 3) and \
            self.has_group("power", player, 5)

    def _blasphemous_esdras_boss_normal(self, player):
        return self.has("Mea Culpa Upgrade", player, 2) and \
            self.has_group("power", player, 2)

    def _blasphemous_esdras_boss_hard(self, player):
        return self.has("Mea Culpa Upgrade", player, 1) and \
            self.has_group("power", player, 1)

    # Melquiades, Exposito, Quirce
    def _blasphemous_mask_boss_easy(self, player):
        return self.has("Mea Culpa Upgrade", player, 4) and \
            self.has_group("power", player, 8)

    def _blasphemous_mask_boss_normal(self, player):
        return self.has("Mea Culpa Upgrade", player, 3) and \
            self.has_group("power", player, 4)

    def _blasphemous_mask_boss_hard(self, player):
        return self.has("Mea Culpa Upgrade", player, 2) and \
            self.has_group("power", player, 2)

    # Crisanta, Isidora, Sierpes, Amanecidas, Laudes
    def _blasphemous_endgame_boss_easy(self, player):
        return self.has("Mea Culpa Upgrade", player, 6) and \
            self.has_group("power", player, 16)

    def _blasphemous_endgame_boss_normal(self, player):
        return self.has("Mea Culpa Upgrade", player, 5) and \
            self.has_group("power", player, 8)

    def _blasphemous_endgame_boss_hard(self, player):
        return self.has("Mea Culpa Upgrade", player, 4) and \
            self.has_group("power", player, 5)
    
    def _blasphemous_tirso_final(self, world, player):
        return self.can_reach(world.get_region("D01Z04S18", player)) and \
            self.can_reach(world.get_region("D02Z03S20", player)) and \
                self.can_reach(world.get_region("D03Z03S15", player)) and \
                    self.can_reach(world.get_region("D04Z02S22", player)) and \
                        self.can_reach(world.get_region("D05Z02S14", player)) and \
                            self.can_reach(world.get_region("D09Z01S03", player)) and \
                                self.has_group("tirso", 6)

    def _blasphemous_cross_gap(self, player, number: int):
        if number == 1:
            return self.has_any({"Purified Hand of the Nun", "The Young Mason's Wheel", "Ranged Skill"}, player) or \
                self.has_all({"Brilliant Heart of Dawn", "Dash"}, player)
        elif number == 2:
            return self.has_any({"Purified Hand of the Nun", "The Young Mason's Wheel"}, player) or \
                self.has_all({"Brilliant Heart of Dawn", "Dash"}, player)
        elif number == 3:
            return self.has("Purified Hand of the Nun", player) or \
                self.has_all({"Brilliant Heart of Dawn", "Dash"}, player) or \
                    self.has_all({"The Young Mason's Wheel", "Ranged Skill"}, player)
        elif number == 4:
            return self.has("Purified Hand of the Nun", player) or \
                self.has_all({"Brilliant Heart of Dawn", "Dash"}, player)
        elif number == 5:
            return self.has("Purified Hand of the Nun", player) or \
                self.has_all({"Brilliant Heart of Dawn", "Dash", "Ranged Skill"}, player)
        elif number == 6:
            return self.has("Purified Hand of the Nun", player)
        elif number == 7:
            return self.has("Purified Hand of the Nun", player) and \
                (self.has_any({"The Young Mason's Wheel", "Ranged Skill"}, player) or \
                    self.has_all({"Brilliant Heart of Dawn", "Dash"}, player))
        elif number == 8:
            return self.has("Purified Hand of the Nun", player) and \
                (self.has("The Young Mason's Wheel", player) or \
                    self.has_all({"Brilliant Heart of Dawn", "Dash"}, player))
        elif number == 9:
            return self.has("Purified Hand of the Nun", player) and \
                (self.has_all({"The Young Mason's Wheel", "Ranged Skill"}, player) or \
                    self.has_all({"Brilliant Heart of Dawn", "Dash"}, player))
        elif number == 10:
            return self.has("Purified Hand of the Nun", player) and \
                self.has_all({"Brilliant Heart of Dawn", "Dash"}, player)
        elif number == 11:
            return self.has_all({"Purified Hand of the Nun", "Ranged Skill"}, player) and \
                self.has_all({"Brilliant Heart of Dawn", "Dash"}, player)
    
    def _blasphemous_redento(self, world, player, number: int):
        if number == 1:
            return self.can_reach(world.get_connected_door("D03Z01S03[W]"), player) or \
                self.can_reach(world.get_connected_door("D03Z01S03[SW]"), player)
        elif number == 2:
            return (self.can_reach(world.get_connected_door("D03Z01S03[W]"), player) or \
                self.can_reach(world.get_connected_door("D03Z01S03[SW]"), player)) and \
                    (self.can_reach(world.get_connected_door("D17Z01S04[N]"), player) or \
                        self.can_reach(world.get_connected_door("D17Z01S04[FrontR]"), player))
        elif number == 3:
            return (self.can_reach(world.get_connected_door("D03Z01S03[W]"), player) or \
                self.can_reach(world.get_connected_door("D03Z01S03[SW]"), player)) and \
                    (self.can_reach(world.get_connected_door("D17Z01S04[N]"), player) or \
                        self.can_reach(world.get_connected_door("D17Z01S04[FrontR]"), player)) and \
                            self.can_reach(world.multiworld.get_region("D01Z03S06", player))
        elif number == 4:
            return (self.can_reach(world.get_connected_door("D03Z01S03[W]"), player) or \
                self.can_reach(world.get_connected_door("D03Z01S03[SW]"), player)) and \
                    (self.can_reach(world.get_connected_door("D17Z01S04[N]"), player) or \
                        self.can_reach(world.get_connected_door("D17Z01S04[FrontR]"), player)) and \
                            self.can_reach(world.multiworld.get_region("D01Z03S06", player)) and \
                                self.can_reach(world.multiworld.get_region("D04Z01S04", player))
        elif number == 5:
            return (self.can_reach(world.get_connected_door("D03Z01S03[W]"), player) or \
                self.can_reach(world.get_connected_door("D03Z01S03[SW]"), player)) and \
                    (self.can_reach(world.get_connected_door("D17Z01S04[N]"), player) or \
                        self.can_reach(world.get_connected_door("D17Z01S04[FrontR]"), player)) and \
                            self.can_reach(world.multiworld.get_region("D01Z03S06", player)) and \
                                self.can_reach(world.multiworld.get_region("D04Z01S04", player)) and \
                                    self.can_reach(world.multiworld.get_region("D04Z02S20", player)) and \
                                        self.has_all({"Little Toe made of Limestone", "Big Toe made of Limestone", "Fourth Toe made of Limestone"}, player) and \
                                            self.has("Knot of Rosary Rope", player)

    def _blasphemous_dawn_jump(self, player):
        return self.has_all({"Brilliant Heart of Dawn", "Dash"}, player)

    def _blasphemous_jondo_bell(self, world, player):
        return (self.can_reach(world.get_connected_door("D03Z02S05[W]"), player) and \
            (self.has("Purified Hand of the Nun", player) or \
                self.has_all({"Brilliant Heart of Dawn", "Dash", "Ranged Skill"}, player)) or \
                    self.can_reach(world.get_connected_door("D03Z02S05[S]"), player) or \
                        self.can_reach(world.get_connected_door("D03Z02S05[E]"), player)) and \
                            (self.can_reach(world.get_connected_door("D03Z02S09[S]"), player) and \
                                self.has("Dash", player) or \
                                    self.can_reach(world.get_connected_door("D03Z02S09[N]"), player) or \
                                        self.can_reach(world.get_connected_door("D03Z02S09[Cherubs]"), player))
        


def rules(blasphemousworld):
    world = blasphemousworld.multiworld
    player = blasphemousworld.player
    door = world.door_randomizer[player]
    doublejump = world.doublejump[player]
    dash = world.dash[player]
    enemy = world.enemy_randomizer[player]

    # D01Z01S01 (The Holy Line)
    if door:
        set_rule(world.get_entrance("D01Z01S01[S]", player),
            lambda state: state.can_reach("") or \
                state._blasphemous_open_holes(player))
        
    # D01Z01S02 (The Holy Line)
    if doublejump:
        set_rule(world.get_location("THL: Hanging skeleton", player),
            lambda state: state.has("Purified Hand of the Nun", player) or \
                state.has("Blood Perpetuated in Sand", player))
    else:
        set_rule(world.get_location("THL: Hanging skeleton", player),
            lambda state: state.has("Blood Perpetuated in Sand", player))
        
    # D01Z01S03 (The Holy Line)
    set_rule(world.get_location("THL: Underground chest", player),
        lambda state: state.has("Blood Perpetuated in Sand", player))
    if dash:
        add_rule(world.get_location("THL: Underground chest", player),
            lambda state: state.has("Dash", player))
    if doublejump:
        add_rule(world.get_location("THL: Underground chest", player),
            lambda state: state.has("Nail Uprooted from Dirt", player) or \
                state.has("Purified Hand of the Nun", player))
    else:
        add_rule(world.get_location("THL: Underground chest", player),
            lambda state: state.has("Nail Uprooted from Dirt", player))
        
    # D01Z02S01 (Albero)
    set_rule(world.get_location("Albero: Bless Linen Cloth", player),
        lambda state: state.has("Linen Cloth", player))
    set_rule(world.get_location("Albero: Bless Hatched Egg", player),
        lambda state: state.has("Hatched Egg of Deformity", player))
    set_rule(world.get_location("Albero: Bless Severed Hand", player),
        lambda state: state.has("Severed Hand", player))
    
    # D01Z02S02 (Albero)
    set_rule(world.get_location("Albero: Tirso's 1st reward", player),
        lambda state: state._blasphemous_tirso_1(player))
    set_rule(world.get_location("Albero: Tirso's 2nd reward", player),
        lambda state: state._blasphemous_tirso_2(player))
    set_rule(world.get_location("Albero: Tirso's 3rd reward", player),
        lambda state: state._blasphemous_tirso_3(player))
    set_rule(world.get_location("Albero: Tirso's 4th reward", player),
        lambda state: state._blasphemous_tirso_4(player))
    set_rule(world.get_location("Albero: Tirso's 5th reward", player),
        lambda state: state._blasphemous_tirso_5(player))
    set_rule(world.get_location("Albero: Tirso's 6th reward", player),
        lambda state: state._blasphemous_tirso_6(player))
    set_rule(world.get_location("Albero: Tirso's final reward", player),
        lambda state: state._blasphemous_tirso_final(blasphemousworld, player))
    
    # D01Z02S03 (Albero)
    set_rule(world.get_entrance("D01Z02S03[church]", player),
        lambda state: state.can_reach("D01Z04S18", player) or \
            state.can_reach("D02Z03S20", player) or \
                state.can_reach("D03Z03S15", player))
    
    set_rule(world.get_location("Albero: Lvdovico's 1st reward", player),
        lambda state: state._blasphemous_tentudia_1(player))
    set_rule(world.get_location("Albero: Lvdovico's 2nd reward", player),
        lambda state: state._blasphemous_tentudia_2(player))
    set_rule(world.get_location("Albero: Lvdovico's 3rd reward", player),
        lambda state: state._blasphemous_tentudia_3(player))
    
    set_rule(world.get_location("Albero: First gift for Cleofas", player),
        lambda state: state.can_reach(world.get_region("D04Z02S10", player)))
    
    set_rule(world.get_location("Albero: Child of Moonlight", player),
        lambda state: (state.can_reach(world.get_region("D02Z02S11", player)) or 
            state.has_any({"Debla of the Lights", "Taranto to my Sister", "Cante Jondo of the Three Sisters", "Cloistered Ruby"}, player)) or 
                (state.can_reach("", player) and #to do: get connected door
                    state.has_any({"Ranged Skill", "Lorquiana", "Cantina of the Blue Rose"}, player) or 
                        (state.has("Aubade of the Nameless Guardian", player) and 
                            state.has("Fervour Upgrade", player, 2))))

    # D01BZ04S01 (Albero: Inside church)
    set_rule(world.get_location("Albero: Final gift for Cleofas", player),
        lambda state: state.can_reach(world.get_region("D04Z02S10", player)) and \
            state.can_reach(world.get_region("D06Z01S18", player)) and \
                state._blasphemous_marks(player) and \
                    state._blasphemous_cord(player))
    
    # D01BZ06S01 (Ossuary)
    set_rule(world.get_location("Ossuary: 1st reward", player),
        lambda state: state._blasphemous_bones_4(player))
    set_rule(world.get_location("Ossuary: 2nd reward", player),
        lambda state: state._blasphemous_bones_8(player))
    set_rule(world.get_location("Ossuary: 3rd reward", player),
        lambda state: state._blasphemous_bones_12(player))
    set_rule(world.get_location("Ossuary: 4th reward", player),
        lambda state: state._blasphemous_bones_16(player))
    set_rule(world.get_location("Ossuary: 5th reward", player),
        lambda state: state._blasphemous_bones_20(player))
    set_rule(world.get_location("Ossuary: 6th reward", player),
        lambda state: state._blasphemous_bones_24(player))
    set_rule(world.get_location("Ossuary: 7th reward", player),
        lambda state: state._blasphemous_bones_28(player))
    set_rule(world.get_location("Ossuary: 8th reward", player),
        lambda state: state._blasphemous_bones_32(player))
    set_rule(world.get_location("Ossuary: 9th reward", player),
        lambda state: state._blasphemous_bones_36(player))
    set_rule(world.get_location("Ossuary: 10th reward", player),
        lambda state: state._blasphemous_bones_40(player))
    set_rule(world.get_location("Ossuary: 11th reward", player),
        lambda state: state._blasphemous_bones_44(player))
    
    set_rule(world.get_entrance("D01BZ06S01[E]", player),
        lambda state: state._blasphemous_bones_30(player))
    
    # D01BZ08S01 (Isidora)
    # to do: boss difficulty

    # D01Z03S01 (Wasteland of the Buried Churches)
    set_rule(world.get_location("WotBC: Lower log path", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D01Z03S01[SW]"), player))
    
    # D01Z03S02 (Wasteland of the Buried Churches)
    set_rule(world.get_location("WotBC: Lower log path", player),
        lambda state: state.has("Dash", player))
    
    # D01Z03S03 (Wasteland of the Buried Churches)
    set_rule(world.get_entrance("D01Z03S03[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D01Z03S05 (Wasteland of the Buried Churches)
    set_rule(world.get_entrance("WotBC: Under broken bridge", player),
        lambda state: state._blasphemous_cross_gap(player, 3) or \
            state.has("Blood Perpetuated in Sand", player) or \
                state.has("Boots of Pleading", player))

    set_rule(world.get_entrance("D01Z03S05[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D01Z03S06 (Wasteland of the Buried Churches)
    set_rule(world.get_location("WotBC: 3rd meeting with Redento", player),
        lambda state: state._blasphemous_redento(blasphemousworld, player, 3))

    # D01Z03S07 (Wasteland of the Buried Churches)
    set_rule(world.get_entrance("WotBC: Cliffside Child of Moonlight", player),
        lambda state: state._blasphemous_cross_gap(player, 2) or \
            state.has_any({"Lorquiana", "Cante Jondo of the Three Sisters", "Cantina of the Blue Rose", "Ranged Skill", "Cloistered Ruby"}, player) or \
                (state.has("Aubade of the Nameless Guardian", player) and \
                    state.has("Fervour Upgrade", player, 2)))

    set_rule(world.get_entrance("D01Z03S07[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))

    # D01Z04S09 (Mercy Dreams)
    set_rule(world.get_entrance("D01Z04S09[W]", player),
        lambda state: state.can_reach("D01Z05S12", player))
    
    # D01Z04S13 (Mercy Dreams)
    if enemy != 0:
        set_rule(world.get_entrance("D01Z04S13[SE]", player),
            lambda state: state.can_reach("", player) or #to do: get connected door
                state.has("Dive Skill", player, 3))
        set_rule(world.get_location("MD: Behind gate to TSC", player),
            lambda state: state.can_reach("", player) or #to do: get connected door
                state.has("Dive Skill", player, 3))
    else:
        set_rule(world.get_entrance("D01Z04S13[SE]", player),
            lambda state: state.can_reach("", player) or #to do: get connected door
                (state.has("Dive Skill", player, 3) and \
                    state.has_any({"Purified Hand of the Nun", "The Young Mason's Wheel"}, player)))
        set_rule(world.get_location("MD: Behind gate to TSC", player),
            lambda state: state.can_reach("", player) or #to do: get connected door
                (state.has("Dive Skill", player, 3) and \
                    state.has_any({"Purified Hand of the Nun", "The Young Mason's Wheel"}, player)))

    # D01Z04S14 (Mercy Dreams)
    set_rule(world.get_location("MD: Sliding challenge", player),
        lambda state: state.has("Dash", player))

    # D01Z04S16 (Mercy Dreams)
    set_rule(world.get_location("MD: Cave Child of Moonlight", player),
        lambda state: state.has_any({"Debla of the Lights", "Taranto to my Sister", "Cloistered Ruby", "Cante Jondo of the Three Sisters", "Purified Hand of the Nun"}, player) or \
            (state.has("Tirana of the Celestial Bastion", player) and \
                state.has("Fervour Upgrade", player, 2)))
    
    # D01Z04S18 (Ten Piedad)
    # to do: boss difficulty

    # D01Z05S02 (Desecrated Cistern)
    # to do: E door can only be reached by entering from E
    set_rule(world.get_entrance("D01Z05S02[S]", player),
        lambda state: state.can_reach("D01Z05S20", player))
    
    # D01Z05S05 (Desecrated Cistern)
    set_rule(world.get_location("DC: Hidden alcove near fountain", player),
        lambda state: state.has_any({"Purified Hand of the Nun", "Nail Uprooted from Dirt"}, player) and \
            state.has("Dash", player))
    
    # D01Z05S06 (Desecrated Cistern)
    set_rule(world.get_location("DC: Upper east Child of Moonlight", player),
        lambda state: (state.has_any({"Debla of the Lights", "Taranto to my Sister", "Cante Jondo of the Three Sisters", "Ranged Skill", "Cloistered Ruby"}, player) or \
            (state.has_any({"Aubade of the Nameless Guardian", "Tirana of the Celestial Bastion"}, player) and \
                state.has("Fervour Upgrade", player, 2))))
    set_rule(world.get_location("DC: Upper east tunnel chest", player),
        lambda state: (state.has_any({"Debla of the Lights", "Taranto to my Sister", "Cante Jondo of the Three Sisters", "Ranged Skill", "Cloistered Ruby"}, player) or \
            (state.has_any({"Aubade of the Nameless Guardian", "Tirana of the Celestial Bastion"}, player) and \
                state.has("Fervour Upgrade", player, 2))))
        
    # D01Z05S17 (Desecrated Cistern)
    set_rule(world.get_location("DC: Hidden alcove near fountain", player),
        lambda state: state.has_any({"Purified Hand of the Nun", "Nail Uprooted from Dirt"}, player) or \
            state._blasphemous_cross_gap(player, 5))

    # D01Z05S21 (Desecrated Cistern)
    set_rule(world.get_entrance("D01Z05S21[Reward]", player),
        lambda state: state.has("Shroud of Dreamt Sins", player))
    
    # D01Z05S23 (Desecrated Cistern)
    set_rule(world.get_entrance("D01Z05S21[Reward]", player),
        lambda state: state.can_reach("D03Z01S01", player) and \
            state.can_reach("D05Z02S01", player) and \
                state.can_reach("D09Z01S07", player) and \
                    state.has("Chalice of Inverted Verses", player))
    
    # D01Z05S25 (help me)
    set_rule(world.get_entrance("D01Z05S25[NE]", player),
        lambda state: state.has("Linen of Golden Thread", player) or \
            state.can_reach(blasphemousworld.get_connected_door("D01Z05S25[NE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D01Z05S25[SW]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D01Z05S25[SE]"), player))
    set_rule(world.get_entrance("D01Z05S25[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D01Z05S25[W]"), player) or \
            (state.has("Linen of Golden Thread", player) and \
                state.has_any({"Three Gnarled Tongues", "Purified Hand of the Nun", "Ranged Skill"}, player)) or \
                    (state.can_reach(blasphemousworld.get_connected_door("D01Z05S25[E]"), player) and \
                        (state.has("Three Gnarled Tongues", player) or \
                            state._blasphemous_cross_gap(player, 3))))
    set_rule(world.get_entrance("D01Z05S25[E]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D01Z05S25[E]"), player) or \
            (state.has("Tirana of the Celestial Bastion", player) and \
                state.has("Fervour Upgrade", player, 2) and \
                    (state.has("Linen of Golden Thread", player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D01Z05S25[W]"), player) and \
                            (state.has("Three Gnarled Tongues", player) or \
                                state._blasphemous_cross_gap(player, 3)))))
    set_rule(world.get_entrance("D01Z05S25[SW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D01Z05S25[SW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D01Z05S25[SE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D01Z05S25[NE]"), player) or \
                    state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D01Z05S25[SE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D01Z05S25[SW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D01Z05S25[SE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D01Z05S25[NE]"), player) or \
                    state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D01Z05S25[EchoesW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D01Z05S25[EchoesW]"), player) or \
            (state.can_reach(blasphemousworld.get_connected_door("D01Z05S25[EchoesE]"), player) and \
                (state.has("Blood Perpetuated in Sand", player) or \
                    state._blasphemous_cross_gap(player, 8))) or \
                        state.has_all({"Linen of Golden Thread", "Purified Hand of the Nun"}, player))
    set_rule(world.get_entrance("D01Z05S25[EchoesE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D01Z05S25[EchoesE]"), player) or \
            (state.can_reach(blasphemousworld.get_connected_door("D01Z05S25[EchoesW]"), player) and \
                (state.has("Blood Perpetuated in Sand", player) or \
                    state._blasphemous_cross_gap(player, 8))) or \
                        state.has_all({"Linen of Golden Thread", "Purified Hand of the Nun"}, player))

    # D01Z06S01 (Petrous)
    set_rule(world.get_entrance("D01Z06S01[Santos]", player),
        lambda state: state.has("Petrified Bell", player))
    
    # D02Z01S01 (Where Olive Trees Wither)
    set_rule(world.get_entrance("D02Z01S01[SW]", player),
        lambda state: (state.can_reach(blasphemousworld.get_connected_door("D02Z01S06[E]"), player) or \
            (state.can_reach(blasphemousworld.get_connected_door("D02Z01S06[W]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D02Z01S06[Cherubs]"), player)) and \
                    state.has("Wall Climb", player)) and \
                        (state.can_reach(blasphemousworld.get_connected_door("D02Z01S01[W]"), player) or \
                            state.can_reach(blasphemousworld.get_connected_door("D02Z01S01[CherubsL]"), player) or \
                                state.can_reach(blasphemousworld.get_connected_door("D02Z01S01[SW]"), player) or \
                                    state.can_reach(blasphemousworld.get_connected_door("D02Z01S01[CherubsR]"), player) or \
                                        state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player)))
    set_rule(world.get_entrance("D02Z01S01[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z01S01[W]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D02Z01S01[CherubsL]"), player) or \
                state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player) or \
                    ((state.can_reach(blasphemousworld.get_connected_door("D02Z01S01[SW]"), player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D02Z01S01[CherubsR]"), player)) and \
                            state._blasphemous_dawn_jump(player)))
    
    # D02Z01S02 (Where Olive Trees Wither)
    set_rule(world.get_entrance("D02Z01S02[NW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z01S02[NW]"), player) or \
            state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player) or \
                (state.can_reach(blasphemousworld.get_connected_door("D02Z01S02[NE]"), player) and \
                    state.has("Three Gnarled Tongues", player) and \
                        state._blasphemous_cross_gap(player, 5)))
    set_rule(world.get_entrance("D02Z01S02[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z01S02[NE]"), player) or \
            (state.can_reach(blasphemousworld.get_connected_door("D02Z01S02[NW]"), player) or \
                state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player)) and \
                    (state.has("Three Gnarled Tongues", player) or \
                        state._blasphemous_cross_gap(player, 10)))
    set_rule(world.get_entrance("D02Z01S02[]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D02Z01S03 (Where Olive Trees Wither)
    set_rule(world.get_entrance("D02Z01S03[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z01S03[W]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D02Z01S03[SE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D02Z01S03[Cherubs]"), player) or \
                    state.has("Wall Climb", player))
    set_rule(world.get_entrance("D02Z01S03[SE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z01S03[W]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D02Z01S03[SE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D02Z01S03[Cherubs]"), player) or \
                    state.has("Wall Climb", player))
    
    # D02Z01S04 (Where Olive Trees Wither)
    set_rule(world.get_entrance("D02Z01S04[-N]", player),
        lambda state: state.has("Golden Thimble Filled with Burning Oil", player) and \
            (state.can_reach(blasphemousworld.get_connected_door("D02Z01S01[W]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D02Z01S01[CherubsL]"), player) or \
                    state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player) or \
                        ((state.can_reach(blasphemousworld.get_connected_door("D02Z01S01[SW]"), player) or \
                            state.can_reach(blasphemousworld.get_connected_door("D02Z01S01[CherubsR]"), player)) and \
                                state._blasphemous_dawn_jump(player))))
    
    # D02Z01S06 (Where Olive Trees Wither)
    set_rule(world.get_entrance("D02Z01S06[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z01S06[W]"), player) or \
            state.has("Dash", player) or \
                state.has_all({"Purified Hand of the Nun", "Wall Climb"}, player))
    set_rule(world.get_entrance("D02Z01S06[E]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z01S06[E]"), player) or \
            state.has("Wall Climb", player))
    
    # D02Z01S09 (Where Olive Trees Wither)
    set_rule(world.get_entrance("D02Z01S09[-CherubsL]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D02Z01S09[-CherubsR]", player),
        lambda state: state.has("Linen of Golden Thread", player) and \
            (state.has("Three Gnarled Tongues", player) or \
                state._blasphemous_cross_gap(player, 10)))
    
    # D02Z02S01 (Graveyard of the Peaks)
    set_rule(world.get_entrance("D02Z02S01[NW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z02S01[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D02Z02S01[Cherubs]"), player) or \
                state.has("Wall Climb", player))
    
    # D02Z02S02 (Graveyard of the Peaks)
    set_rule(world.get_entrance("D02Z02S02[NW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z02S02[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D02Z02S02[NE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D02Z02S02[CherubsL]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D02Z02S02[CherubsR]"), player) or \
                        state.has("Wall Climb", player))
    set_rule(world.get_entrance("D02Z02S02[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z02S02[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D02Z02S02[NE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D02Z02S02[CherubsL]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D02Z02S02[CherubsR]"), player) or \
                        state.has("Wall Climb", player))
    set_rule(world.get_entrance("D02Z02S02[-CherubsR]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D02Z02S03 (Graveyard of the Peaks)
    set_rule(world.get_entrance("D02Z02S03[NW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z02S03[NW]"), player) or \
            state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player) or \
                state.can_reach(blasphemousworld.get_connected_door("D02Z02S03[NE]"), player) and \
                    state.has("Three Gnarled Tongues", player))
    set_rule(world.get_entrance("D02Z02S03[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z02S03[NE]"), player) or \
            state.has("Wall Climb", player) and \
                (state._blasphemous_cross_gap(player, 11) or \
                    (state.has("Blood Perpetuated in Sand", player) and \
                        (state.has("Three Gnarled Tongues", player) or \
                            state._blasphemous_cross_gap(player, 7))) or \
                                (state.has("Three Gnarled Tongues", player) and \
                                    (state.has("Purified Hand of the Nun", player) or \
                                        state.blasphemous_air_stall(player)))))
    set_rule(world.get_entrance("D02Z02S03[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D02Z02S04 (Graveyard of the Peaks)
    set_rule(world.get_entrance("D02Z02S04[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z02S04[NE]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D02Z02S04[W]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D02Z02S03[E]"), player) and \
                    state.has("Dash", player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D02Z02S04[SE]"), player) and \
                            state.has("Wall Climb", player))
    set_rule(world.get_entrance("D02Z02S04[SE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z02S04[NE]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D02Z02S04[W]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D02Z02S04[SE]"), player) or \
                    state.has("Dash", player))
    set_rule(world.get_entrance("D02Z02S04[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z02S04[NE]"), player) or \
            ((state.can_reach(blasphemousworld.get_connected_door("D02Z02S04[W]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D02Z02S04[E]"), player) and \
                    state.has("Dash", player)) and \
                        state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player)) or \
                            (state.can_reach(blasphemousworld.get_connected_door("D02Z02S04[SE]"), player) and \
                                state.has("Wall Climb", player)))
    set_rule(world.get_entrance("D02Z02S04[-CherubsL]", player),
        lambda state: state.has("Linen of Golden Thread", player) and \
            (state.can_reach(blasphemousworld.get_connected_door("D02Z02S04[NE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D02Z02S04[W]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D02Z02S03[SE]"), player) or \
                        state.has("Dash", player)))
    
    # D02Z02S05 (Graveyard of the Peaks)
    set_rule(world.get_entrance("D02Z02S05[E]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z02S05[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D02Z02S05[E]"), player) or \
                state.has("Wall Climb", player))
    set_rule(world.get_entrance("D02Z02S05[NW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z02S05[NW]"), player) or \
            state.has("Wall Climb", player))
    set_rule(world.get_entrance("D02Z02S05[-CherubsL]", player),
        lambda state: state.has("Linen of Golden Thread"))
    set_rule(world.get_entrance("D02Z02S05[-CherubsR]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D02Z02S11 (Graveyard of the Peaks)
    set_rule(world.get_entrance("D02Z02S11[E]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z02S11[E]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D02Z02S11[NW]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D02Z02S11[NE]"), player) or \
                    state._blasphemous_cross_gap(player, 6))
    set_rule(world.get_entrance("D02Z02S11[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread"))
    
    # D02Z02S14 (Graveyard of the Peaks)
    set_rule(world.get_entrance("D02Z02S14[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D02Z03S02 (Convent of Our Lady of the Charred Visage)
    set_rule(world.get_entrance("D02Z03S02[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z03S02[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D02Z03S02[NE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D02Z03S02[N]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D02Z03S02[W]"), player) or \
                        state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player))
    set_rule(world.get_entrance("D02Z03S02[N]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z03S11[S]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D02Z03S11[W]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D02Z03S11[NW]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D02Z03S11[E]"), player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D02Z03S11[NE]"), player))
    
    # D02Z03S03 (Convent of Our Lady of the Charred Visage)
    set_rule(world.get_entrance("D02Z03S03[NW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z03S03[NW]"), player) or \
            state.has("Blood Perpetuated in Sand", player) or \
                state.blasphemous_cross_gap(player, 3))
    
    # D02Z03S05 (Convent of Our Lady of the Charred Visage)
    set_rule(world.get_entrance("D02Z03S05[S]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z03S05[S]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D02Z03S05[NE]"), player) or \
                state.has("Wall Climb", player))
    set_rule(world.get_entrance("D02Z03S05[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z03S05[S]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D02Z03S05[NE]"), player) or \
                state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player))
    
    # D02Z02S10 (Convent of Our Lady of the Charred Visage)
    set_rule(world.get_entrance("D02Z03S10[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D02Z02S18 (Convent of Our Lady of the Charred Visage)
    set_rule(world.get_entrance("D02Z03S18[NW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z03S18[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D02Z03S18[NE]"), player) or \
                state.has("Wall Climb", player))
    set_rule(world.get_entrance("D02Z03S18[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D02Z03S18[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D02Z03S18[NE]"), player) or \
                state.has("Wall Climb", player))
    
    # D02Z02S20 (Convent of Our Lady of the Charred Visage)
    # to do: boss logic

    # D03Z01S01 (Mountains of the Endless Dusk)
    set_rule(world.get_entrance("D03Z01S01[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D03Z01S02 (Mountains of the Endless Dusk)
    set_rule(world.get_entrance("D03Z01S02[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z01S02[W]"), player) or \
            state.has("Wall Climb", player) or \
                state._blasphemous_cross_gap(player, 3))
    set_rule(world.get_entrance("D03Z01S02[E]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z01S02[E]"), player) or \
            state.has("Wall Climb", player) or \
                state._blasphemous_cross_gap(player, 7))
    
    # D03Z01S03 (Mountains of the Endless Dusk)
    set_rule(world.get_entrance("D03Z01S03[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z01S03[W]"), player) or \
            state.has("Wall Climb", player) and \
                (state.can_reach(blasphemousworld.get_connected_door("D03Z01S03[SW]"), player) or \
                    state._blasphemous_cross_gap(player, 9)))
    set_rule(world.get_entrance("D03Z01S03[E]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z01S03[E]"), player) or \
            state.has("Wall Climb", player))
    set_rule(world.get_entrance("D03Z01S03[SW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z01S03[W]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z01S03[SW]"), player) or \
                state._blasphemous_cross_gap(player, 9))
    set_rule(world.get_entrance("D03Z01S03[-WestL]", player),
        lambda state: state.has("Linen of Golden Thread", player) and \
            (state.can_reach(blasphemousworld.get_connected_door("D03Z01S03[W]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D03Z01S03[SW]"), player) or \
                    state._blasphemous_cross_gap(player, 9)))
    set_rule(world.get_entrance("D03Z01S03[-WestR]", player),
        lambda state: state.has("Linen of Golden Thread", player) and \
            (state.can_reach(blasphemousworld.get_connected_door("D03Z01S03[W]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D03Z01S03[SW]"), player) or \
                    state._blasphemous_cross_gap(player, 9)))
    set_rule(world.get_entrance("D03Z01S03[-EastL]", player),
        lambda state: state.has("Linen of Golden Thread", player) and \
            (state.can_reach(blasphemousworld.get_connected_door("D03Z01S03[W]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D03Z01S03[SW]"), player) or \
                    state._blasphemous_cross_gap(player, 9)))
    set_rule(world.get_entrance("D03Z01S03[-EastR]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D03Z02S01 (Jondo)
    set_rule(world.get_entrance("D03Z02S01[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S01[W]"), player) or \
            state.has("Wall Climb", player))
    set_rule(world.get_entrance("D03Z02S01[N]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S01[N]"), player) or \
            state.has("Wall Climb", player) or \
                state._blasphemous_cross_gap(player, 8))
    
    # D03Z02S02 (Jondo)
    set_rule(world.get_entrance("D03Z02S02[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S02[W]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z02S02[CherubsL]"), player) or \
                state.has("Purified Hand of the Nun", player) and \
                    (state.can_reach(blasphemousworld.get_connected_door("D03Z02S02[E]"), player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D03Z02S02[CherubsR]"), player) or \
                            state.has("Wall Climb", player)))
    set_rule(world.get_entrance("D03Z02S02[E]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S02[E]"), player) or \
            state.has("Wall Climb", player))
    
    # D03Z02S03 (Jondo)
    set_rule(world.get_entrance("D03Z02S03[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[W]"), player) or \
            state.has("Dash", player) and \
                (state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[E]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[N]"), player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SE2]"), player)))
    set_rule(world.get_entrance("D03Z02S03[E]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[E]"), player) or \
            (state._blasphemous_air_stall(player) or \
                state.has_any({"Purified Hand of the Nun", "Boots of Pleading"}, player)) and \
                    (state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[E]"), player) and \
                        state.has("Dash", player) or \
                            state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[N]"), player) or \
                                state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SE2]"), player)))
    set_rule(world.get_entrance("D03Z02S03[N]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[W]"), player) or \
            state.has("Dash", player) and \
                (state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[E]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[N]"), player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SE2]"), player)))
    set_rule(world.get_entrance("D03Z02S03[SE2]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[W]"), player) or \
            state.has("Dash", player) and \
                (state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[E]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[N]"), player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SE2]"), player)))
    set_rule(world.get_entrance("D03Z02S03[SW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SSL]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SSR]"), player) or \
                        state._blasphemous_jondo_bell(blasphemousworld, player) and \
                            (state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[W]"), player) and \
                                state.has("Dash", player) or \
                                    state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[E]"), player) or \
                                        state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[N]"), player) or \
                                            state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SE2]"), player)))
    set_rule(world.get_entrance("D03Z02S03[SE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SSL]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SSR]"), player) or \
                        state._blasphemous_jondo_bell(blasphemousworld, player) and \
                            (state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[W]"), player) and \
                                state.has("Dash", player) or \
                                    state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[E]"), player) or \
                                        state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[N]"), player) or \
                                            state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SE2]"), player)))
    set_rule(world.get_entrance("D03Z02S03[SSL]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SSL]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SSR]"), player) or \
                        state._blasphemous_jondo_bell(blasphemousworld, player) and \
                            (state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[W]"), player) and \
                                state.has("Dash", player) or \
                                    state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[E]"), player) or \
                                        state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[N]"), player) or \
                                            state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SE2]"), player)))
    set_rule(world.get_entrance("D03Z02S03[SSC]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SSL]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SSR]"), player) or \
                        state._blasphemous_jondo_bell(blasphemousworld, player) and \
                            (state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[W]"), player) and \
                                state.has("Dash", player) or \
                                    state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[E]"), player) or \
                                        state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[N]"), player) or \
                                            state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SE2]"), player)))
    set_rule(world.get_entrance("D03Z02S03[SSR]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SSL]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SSR]"), player) or \
                        state._blasphemous_jondo_bell(blasphemousworld, player) and \
                            (state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[W]"), player) and \
                                state.has("Dash", player) or \
                                    state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[E]"), player) or \
                                        state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[N]"), player) or \
                                            state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[SE2]"), player)))
    
    # D03Z02S04 (Jondo)
    set_rule(world.get_entrance("D03Z02S04[NW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S04[NW]"), player) or \
            state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player))
    set_rule(world.get_entrance("D03Z02S04[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S04[NE]"), player) or \
            state.has("Wall Climb", player) or \
                (state.can_reach(blasphemousworld.get_connected_door("D03Z02S04[S]"), player) and \
                    state.has("Purified Hand of the Nun", player)))
    set_rule(world.get_entrance("D03Z02S04[S]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S04[NE]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z02S03[S]"), player) or \
                state.has("Wall Climb", player))
    
    # D03Z02S05 (Jondo)
    set_rule(world.get_entrance("D03Z02S05[E]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S05[E]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z02S05[S]"), player) or \
                state._blasphemous_cross_gap(player, 5))
    set_rule(world.get_entrance("D03Z02S05[S]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S05[E]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z02S05[S]"), player) or \
                state._blasphemous_cross_gap(player, 5))
    
    # D03Z02S08 (Jondo)
    set_rule(world.get_entrance("D03Z02S08[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S08[N]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z02S08[W]"), player) or \
                state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player))
    set_rule(world.get_entrance("D03Z02S08[N]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S08[N]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z02S08[W]"), player) or \
                state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player))
    
    # D03Z02S09 (Jondo)
    set_rule(world.get_entrance("D03Z02S09[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S09[W]"), player) or \
            state.has("Dash", player))
    set_rule(world.get_entrance("D03Z02S09[N]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S09[N]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z02S09[S]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D03Z02S09[Cherubs]"), player) or \
                    state.has("Dash", player))
    set_rule(world.get_entrance("D03Z02S09[S]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S09[N]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z02S09[S]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D03Z02S09[Cherubs]"), player) or \
                    state.has("Dash", player))
    
    # D03Z02S10 (Jondo)
    set_rule(world.get_entrance("D03Z02S10[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D03Z02S11 (Jondo)
    set_rule(world.get_entrance("D03Z02S11[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S11[W]"), player) or \
            state.has("Dash", player) and \
                state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player))
    set_rule(world.get_entrance("D03Z02S11[E]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z02S11[E]"), player) or \
            state.has("Dash", player) and \
                state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player))
    
    # D03Z02S13 (Jondo)
    set_rule(world.get_entrance("D03Z02S13[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D03Z03S01 (Grievance Ascends)
    set_rule(world.get_entrance("D03Z03S01[NL]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z03S01[NL]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z03S01[NR]"), player) or \
                state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player))
    set_rule(world.get_entrance("D03Z03S01[NR]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z03S01[NL]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z03S01[NR]"), player) or \
                state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player))
    
    # D03Z03S02 (Grievance Ascends)
    set_rule(world.get_entrance("D03Z03S02[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z03S02[NE]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z03S02[W]"), player) or \
                state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player))
    set_rule(world.get_entrance("D03Z03S02[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z03S02[NE]"), player) or \
            state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player))
    
    # D03Z03S04 (Grievance Ascends)
    set_rule(world.get_entrance("D03Z03S04[NW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z03S04[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z03S04[NE]"), player) or \
                state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player) and \
                    (state.can_reach(blasphemousworld.get_connected_door("D03Z03S04[E]"), player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D03Z03S04[SW]"), player) or \
                            state.has("Blood Perpetuated in Sand", player) or \
                                state._blasphemous_cross_gap(player, 10)))
    set_rule(world.get_entrance("D03Z03S04[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z03S04[NE]"), player) or \
            state.has("Wall Climb", player) and \
                (state.can_reach(blasphemousworld.get_connected_door("D03Z03S04[NW]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D03Z03S04[E]"), player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D03Z03S04[SW]"), player) or \
                            state.has("Blood Perpetuated in Sand", player) or \
                                state._blasphemous_cross_gap(player, 10)))
    set_rule(world.get_entrance("D03Z03S04[E]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z03S04[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z03S04[NE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D03Z03S04[E]"), player) or \
                    state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player) and \
                        (state.can_reach(blasphemousworld.get_connected_door("D03Z03S04[SW]"), player) or \
                            state.has("Blood Perpetuated in Sand", player) or \
                                state._blasphemous_cross_gap(player, 10)))
    set_rule(world.get_entrance("D03Z03S04[SW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z03S04[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z03S04[NE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D03Z03S04[E]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D03Z03S04[SW]"), player) or \
                        state.has("Blood Perpetuated in Sand", player) or \
                            state._blasphemous_cross_gap(player, 10))
    set_rule(world.get_entrance("D03Z03S04[SE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z03S04[SE]"), player) or \
            state.has("Blood Perpetuated in Sand", player))
    set_rule(world.get_entrance("D03Z03D04[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D03Z03S05 (Grievance Ascends)
    set_rule(world.get_entrance("D03Z03S05[SW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z03S05[SW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z03S05[SE]"), player) or \
                state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D03Z03S05[SE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z03S05[SW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z03S05[SE]"), player) or \
                state.has("Linen of Golden Thread", player))
    
    # D03Z03S07 (Grievance Ascends)
    set_rule(world.get_entrance("D03Z03S07[NW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z03S07[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z03S07[NE]"), player) or \
                state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player))
    set_rule(world.get_entrance("D03Z03S07[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D03Z03S07[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D03Z03S07[NE]"), player) or \
                state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player))
    
    # D03Z03S08 (Grievance Ascends)
    set_rule(world.get_entrance("D03Z03S08[-CherubsL]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D03Z03S08[-CherubsR]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D03Z03S15 (Grievance Ascends)
    # to do: boss logic

    # D04Z01S01 (Patio of the Silent Steps)
    set_rule(world.get_entrance("D04Z01S01[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D04Z01S01[NE]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D04Z01S01[N]"), player) or \
                state._blasphemous_cross_gap(player, 3))
    set_rule(world.get_entrance("D04Z01S01[N]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D04Z01S01[NE]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D04Z01S01[N]"), player) or \
                state._blasphemous_cross_gap(player, 3))
    
    # D04Z01S05 (Patio of the Silent Steps)
    set_rule(world.get_entrance("D04Z01S05[N]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D04Z01S05[N]"), player) or \
            state.has_all({"Blood Perpetuated in Sand", "Three Gnarled Tongues", "Wall Climb"}, player) or \
                state.has("Purified Hand of the Nun", player) and \
                    (state.has("Blood Perpetuated in Sand", player) or \
                        state.has_all({"Three Gnarled Tongues", "Wall Climb"}, player)))
    set_rule(world.get_entrance("D04Z01S05[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D04Z01S06 (Patio of the Silent Steps)
    set_rule(world.get_entrance("D04Z01S06[E]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D04Z01S06[E]"), player) or \
            state.has("Purified Hand of the Nun", player))
    set_rule(world.get_entrance("D04Z01S06[Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D04Z02S01 (Mother of Mothers)
    set_rule(world.get_entrance("D04Z02S01[N]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D04Z02S04[N]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D04Z02S04[NE]"), player) and \
                state.has("Dash", player) and \
                    state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player))
    set_rule(world.get_entrance("D04Z02S01[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D04Z02S04[N]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D04Z02S04[NE]"), player) and \
                state.has("Dash", player) and \
                    state._blasphemous_cross_gap(player, 1))
    # to do: is this a mistake? should the doors be for this room?

    # D04Z02S02 (Mother of Mothers)
    set_rule(world.get_entrance("D04Z02S02[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D04Z02S02[NE]"), player))
    # to do: upwarp skips??
    set_rule(world.get_entrance("D04Z02S02[N]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D04Z02S02[N]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D04Z02S02[NE]"), player) or \
                state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player))
    
    # D04Z02S04 (Mother of Mothers)
    set_rule(world.get_entrance("D04Z02S04[NW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D04Z02S04[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D04Z02S04[NE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D04Z02S04[N]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D04Z02S04[Cherubs]"), player) or \
                        state.has_all({"Purified Hand of the Nun", "Wall Climb"}, player))
    set_rule(world.get_entrance("D04Z02S04[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D04Z02S04[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D04Z02S04[NE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D04Z02S04[N]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D04Z02S04[Cherubs]"), player) or \
                        state.has_all({"Purified Hand of the Nun", "Wall Climb"}, player))
    set_rule(world.get_entrance("D04Z02S04[N]", player),
        lambda state: (state.can_reach(blasphemousworld.get_connected_door("D04Z02S04[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D04Z02S04[NE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D04Z02S04[N]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D04Z02S04[Cherubs]"), player) or \
                        state.has_all({"Purified Hand of the Nun", "Wall Climb"}, player)) and \
                            (state.can_reach(blasphemousworld.get_connected_door("D04Z02S06[NW]"), player) or \
                                state.can_reach(blasphemousworld.get_connected_door("D04Z02S06[N]"), player) or \
                                    state.can_reach(blasphemousworld.get_connected_door("D04Z02S06[NE]"), player) or \
                                        state.can_reach(blasphemousworld.get_connected_door("D04Z02S06[S]"), player) or \
                                            state.can_reach(blasphemousworld.get_connected_door("D04Z02S06[SE]"), player)))
    
    # D04Z02S06 (Mother of Mothers)
    set_rule(world.get_entrance("D04Z02S06[NW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D04Z02S06[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D04Z02S06[N]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D04Z02S06[NE]"), player) or \
                    state.has("Wall Climb", player))
    set_rule(world.get_entrance("D04Z02S06[N]", player),
        lambda state: (state.can_reach(blasphemousworld.get_connected_door("D04Z02S06[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D04Z02S06[N]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D04Z02S06[NE]"), player) or \
                    state.has("Wall Climb", player)) and \
                        (state.can_reach(blasphemousworld.get_connected_door("D06Z01S23[Sword]"), player) or \
                            state.can_reach(blasphemousworld.get_connected_door("D06Z01S23[E]"), player) or \
                                state.can_reach(blasphemousworld.get_connected_door("D06Z01S23[S]"), player) or \
                                    state.can_reach(blasphemousworld.get_connected_door("D06Z01S23[Cherubs]"), player)))
    set_rule(world.get_entrance("D04Z02S06[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D04Z02S06[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D04Z02S06[N]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D04Z02S06[NE]"), player) or \
                    state.has("Wall Climb", player))
    set_rule(world.get_entrance("D04Z02S06[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D04Z02S09 (Mother of Mothers)
    set_rule(world.get_entrance("D04Z02S09[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D04Z02S09[NE]"), player) or \
            state.has("Blood Perpetuated in Sand", player))
    
    # D04Z02S16 (Mother of Mothers)
    set_rule(world.get_entrance("D04Z02S16[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D04Z02S20 (Mother of Mothers)
    set_rule(world.get_entrance("D04Z02S20[Redento]", player),
        lambda state: state._blasphemous_redento(blasphemousworld, player, 5))
    
    # D04Z02S21 (Mother of Mothers)
    set_rule(world.get_entrance("D04Z02S21[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D04Z02S21[NE]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D04Z02S21[W]"), player) or \
                state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player))
    set_rule(world.get_entrance("D04Z02S21[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D04Z02S21[NE]"), player) or \
            state.has_any({"Purified Hand of the Nun", "Wall Climb"}, player))
    
    # D04Z02S22 (Mother of Mothers)
    # to do: boss logic

    # D05Z01S03 (Library of the Negated Words)
    set_rule(world.get_entrance("D05Z01S03[Frontal]", player),
        lambda state: state.has("Key Grown from Twisted Wood", player) and \
            state.can_reach(blasphemousworld.get_connected_door("D05Z01S23[E]"), player) and \
                (state.can_reach(blasphemousworld.get_connected_door("D05Z01S11[NW]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D05Z01S11[NE]"), player)))
    
    # D05Z01S05 (Library of the Negated Words)
    set_rule(world.get_entrance("D05Z01S05[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D05Z01S05[NE]"), player) or \
            state.has("Blood Perpetuated in Sand", player))
    
    # D05Z01S06 (Library of the Negated Words)
    set_rule(world.get_entrance("D05Z01S06[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D05Z01S06[W]"), player) or \
            state.has("Silvered Lung of Dolphos", player))
    set_rule(world.get_entrance("D05Z01S06[E]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D05Z01S06[E]"), player) or \
            state.has("Silvered Lung of Dolphos", player))
    # to do: detailed miasma logic

    # D05Z01S07 (Library of the Negated Words)
    set_rule(world.get_entrance("D05Z01S07[NW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D05Z01S07[NW]"), player) or \
            state.has("Blood Perpetuated in Sand", player) and \
                (state.has_all({"Three Gnarled Tongues", "Wall Climb"}, player) or \
                    state.has("Purified Hand of the Nun", player)) or \
                        (state.has_all({"Three Gnarled Tongues", "Wall Climb"}, player) or \
                            state._blasphemous_cross_gap(player, 3)) or \
                                state._blasphemous_cross_gap(player, 7))
    
    # D05Z01S21 (Library of the Negated Words)
    set_rule(world.get_entrance("D05Z01S21[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D05Z02S06 (The Sleeping Canvases)
    set_rule(world.get_entrance("D05Z02S06[SE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D05Z02S11[W]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D05Z01S11[Cherubs]"), player))
    
    # D05Z02S09 (The Sleeping Canvases)
    set_rule(world.get_entrance("D05Z02S09[E]", player),
        lambda state: state.has("Bead of Red Wax", player, 3) and \
            state.has("Bead of Blue Wax", player, 3))
    
    # D05Z02S10 (The Sleeping Canvases)
    set_rule(world.get_entrance("D05Z02S10[W]", player),
        lambda state: state.has("Dash", player))
    
    # D05Z02S13 (The Sleeping Canvases)
    set_rule(world.get_entrance("D05Z02S13[E]", player),
        lambda state: state.has("Dash", player))
    
    # D05Z02S14 (The Sleeping Canvases)
    set_rule(world.get_entrance("D05Z02S14[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D05Z02S14[W]"), player))
    set_rule(world.get_entrance("D05Z02S14[E]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D05Z02S14[E]"), player))
    # to do: boss logic

    # D06Z01S01 (Archcathedral Rooftops)
    set_rule(world.get_entrance("D06Z01S01[SW]", player),
        lambda state: (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[SW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[SE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[W]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[E]"), player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NNW]"), player) or \
                            state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NNE]"), player) or \
                                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[N]"), player)) or \
                                    state.has("Linen of Golden Thread", player) and \
                                        (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NW]"), player) or \
                                            state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NE]"), player)))
    set_rule(world.get_entrance("D06Z01S01[SE]", player),
        lambda state: (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[SW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[SE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[W]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[E]"), player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NNW]"), player) or \
                            state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NNE]"), player) or \
                                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[N]"), player)) or \
                                    state.has("Linen of Golden Thread", player) and \
                                        (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NW]"), player) or \
                                            state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NE]"), player)))
    set_rule(world.get_entrance("D06Z01S01[W]", player),
        lambda state: (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[W]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[E]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NNW]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NNE]"), player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[N]"), player)) or \
                            state.has_group("masks", player, 1) and \
                                (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[SW]"), player) or \
                                    state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[SE]"), player)) or \
                                        state.has("Linen of Golden Thread", player) and \
                                            (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NW]"), player) or \
                                                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NE]"), player) and \
                                                    (state.has("Three Gnarled Tongues", player) or \
                                                        state._blasphemous_cross_gap(player, 1))))
    set_rule(world.get_entrance("D06Z01S01[E]", player),
        lambda state: (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[W]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[E]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NNW]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NNE]"), player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[N]"), player)) or \
                            state.has_group("masks", player, 1) and \
                                (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[SW]"), player) or \
                                    state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[SE]"), player)) or \
                                        state.has("Linen of Golden Thread", player) and \
                                            (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NW]"), player) or \
                                                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NE]"), player) and \
                                                    (state.has("Three Gnarled Tongues", player) or \
                                                        state._blasphemous_cross_gap(player, 1))))
    set_rule(world.get_entrance("D06Z01S01[NW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NE]"), player) and \
                (state.has("Three Gnarled Tongues", player) or \
                    state._blasphemous_cross_gap(player, 8)) or \
                        state.has("Linen of Golden Thread", player) and \
                            (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NNW]"), player) or \
                                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NNE]"), player) and \
                                    (state.has("Three Gnarled Tongues", player) or \
                                        state._blasphemous_cross_gap(player, 3))))
    set_rule(world.get_entrance("D06Z01S01[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NE]"), player) and \
                (state.has("Three Gnarled Tongues", player) or \
                    state._blasphemous_cross_gap(player, 8)) or \
                        state.has("Linen of Golden Thread", player) and \
                            (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NNW]"), player) or \
                                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NNE]"), player) and \
                                    (state.has("Three Gnarled Tongues", player) or \
                                        state._blasphemous_cross_gap(player, 3))))
    set_rule(world.get_entrance("D06Z01S01[NNW]", player),
        lambda state: (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NNW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NNE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[N]"), player)) or \
                    state.has_group("masks", player, 2) and \
                        (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[SW]"), player) or \
                            state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[SE]"), player) or \
                                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[W]"), player) or \
                                    state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[E]"), player) or \
                                        state.has("Linen of Golden Thread", player) and \
                                            (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NW]"), player) or \
                                                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NE]"), player))))
    set_rule(world.get_entrance("D06Z01S01[NNE]", player),
        lambda state: (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NNW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NNE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[N]"), player)) or \
                    state.has_group("masks", player, 2) and \
                        (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[SW]"), player) or \
                            state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[SE]"), player) or \
                                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[W]"), player) or \
                                    state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[E]"), player) or \
                                        state.has("Linen of Golden Thread", player) and \
                                            (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NW]"), player) or \
                                                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NE]"), player))))
    set_rule(world.get_entrance("D06Z01S01[N]", player),
        lambda state: state.has_group("masks", player, 3) and \
            (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[SW]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[SE]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[W]"), player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[E]"), player) or \
                            state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NNW]"), player) or \
                                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NNE]"), player) or \
                                    state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[N]"), player) or \
                                        state.has("Linen of Golden Thread", player) and \
                                            (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NW]"), player) or \
                                                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NE]"), player))))
    set_rule(world.get_entrance("D06Z01S01[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player) and \
            (state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[SW]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[SE]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[W]"), player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[E]"), player) or \
                            state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NW]"), player) or \
                                state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NE]"), player) or \
                                    state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NNW]"), player) or \
                                        state.can_reach(blasphemousworld.get_connected_door("D06Z01S01[NNE]"), player)))
    
    # D06Z01S04 (Archcathedral Rooftops)
    set_rule(world.get_entrance("D06Z01S04[Health]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D06Z01S04[Health]"), player) or \
            (state.has("Wall Climb", player) and \
                state.has("Silvered Lung of Dolphos", player) and \
                    (state.has("Purified Hand of the Nun", player) or \
                        state.has_all({"Blood Perpetuated in Sand", "Three Gnarled Tongues"}, player))))
    set_rule(world.get_entrance("D06Z01S04[NW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D06Z01S04[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D06Z01S04[Cherubs]"), player) or \
                (state.can_reach(blasphemousworld.get_connected_door("D06Z01S04[SW]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D06Z01S04[W]"), player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D06Z01S04[Health]"), player)) and \
                            state.has("Wall Climb", player) and \
                                state.has("Silvered Lung of Dolphos", player) and \
                                    (state.has_any({"Dash", "Purified Hand of the Nun"}, player) and \
                                        (state._blasphemous_dawn_jump(player) or \
                                            state.has("Three Gnarled Tongues", player))))
    set_rule(world.get_entrance("D06Z01S04[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D06Z01S04[NE]"), player) or \
            (state.can_reach(blasphemousworld.get_connected_door("D06Z01S04[SW]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D06Z01S04[W]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D06Z01S04[Health]"), player)) and \
                        state.has("Wall Climb", player) and \
                            state.has("Silvered Lung of Dolphos", player) and \
                                (state.has_any({"Dash", "Purified Hand of the Nun"}, player) and \
                                    (state._blasphemous_dawn_jump(player) or \
                                        state.has("Three Gnarled Tongues", player))))
    # to do: detailed miasma logic

    # D06Z01S08 (Archcathedral Rooftops)
    set_rule(world.get_entrance("D06Z01S08[E]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D06Z01S08[N]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D06Z01S08[E]"), player) or \
                state.has("Wall Climb", player))
    
    # D06Z01S09 (Archcathedral Rooftops)
    set_rule(world.get_entrance("D06Z01S09[-CherubsL]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D06Z01S09[-CherubsR]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D06Z01S10 (Archcathedral Rooftops)
    set_rule(world.get_entrance("D06Z01S10[-CherubsL]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    set_rule(world.get_entrance("D06Z01S10[-CherubsR]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D06Z01S12 (Archcathedral Rooftops)
    set_rule(world.get_entrance("D06Z01S12[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D06Z01S12[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D06Z01S12[NE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D06Z01S12[NE2]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D06Z01S12[W]"), player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D06Z01S12[E]"), player) or \
                            state.has_all({"Wall Climb", "Purified Hand of the Nun"}, player))
    set_rule(world.get_entrance("D06Z01S12[E]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D06Z01S12[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D06Z01S12[NE]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D06Z01S12[NE2]"), player) or \
                    state.can_reach(blasphemousworld.get_connected_door("D06Z01S12[W]"), player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D06Z01S12[E]"), player) or \
                            state.has_all({"Wall Climb", "Purified Hand of the Nun"}, player))
    set_rule(world.get_entrance("D06Z01S12[NW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D06Z01S12[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D06Z01S12[NE]"), player) or \
                state.has_any({"Wall Climb", "Purified Hand of the Nun"}, player))
    set_rule(world.get_entrance("D06Z01S12[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D06Z01S12[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D06Z01S12[NE]"), player) or \
                state.has_any({"Wall Climb", "Purified Hand of the Nun"}, player))
    
    # D06Z01S15 (Archcathedral Rooftops)
    set_rule(world.get_entrance("D06Z01S15[NW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D06Z01S15[NW]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D06Z01S12[SW]"), player) or \
                state.has("Wall Climb", player))
    set_rule(world.get_entrance("D06Z01S15[NE]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D06Z01S15[NE]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D06Z01S12[SW]"), player) or \
                state.has("Wall Climb", player))
    
    # D06Z01S16 (Archcathedral Rooftops)
    set_rule(world.get_entrance("D06Z01S16[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D06Z01S16[W]"), player) or \
            (state.can_reach(blasphemousworld.get_connected_door("D06Z01S16[CherubsL]"), player) and \
                (state.has("Purified Hand of the Nun", player) or \
                    state.has("Wall Climb", player) and \
                        (state.has("Three Gnarled Tongues", player) or \
                            state._blasphemous_air_stall(player)))) or \
                                (state.can_reach(blasphemousworld.get_connected_door("D06Z01S16[CherubsR]"), player) and \
                                    (state.has("Purified Hand of the Nun", player) or \
                                        state._blasphemous_air_stall(player) and \
                                            (state.has_any({"Three Gnarled Tongues", "The Young Mason's Wheel"}, player) and \
                                                (state.has("Wall Climb", player) or \
                                                    state._blasphemous_dawn_jump(player))))) or \
                                                        state.can_reach(blasphemousworld.get_connected_door("D06Z01S16[E]"), player) and \
                                                            (state.has("Three Gnarled Tongues", player) or \
                                                                state._blasphemous_cross_gap(player, 7)) and \
                                                                    (state.has("Wall Climb", player) or \
                                                                        state._blasphemous_cross_gap(player, 5)))
    set_rule(world.get_entrance("D06Z01S16[E]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D06Z01S16[E]"), player) or \
            ((state.can_reach(blasphemousworld.get_connected_door("D06Z01S16[W]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D06Z01S16[CherubsL]"), player)) and \
                    (state.has("Three Gnarled Tongues", player) or \
                        state._blasphemous_cross_gap(player, 5))) or \
                            (state.can_reach(blasphemousworld.get_connected_door("D06Z01S16[CherubsR]"), player) and \
                                (state.has("Purified Hand of the Nun", player) or \
                                    state._blasphemous_air_stall(player) and \
                                        state.has_any({"Three Gnarled Tongues", "The Young Mason's Wheel"}, player))))
    set_rule(world.get_entrance("D06Z01S16[-CherubsL]", player),
        lambda state: state.has("Linen of Golden Thread", player) and \
            (state.can_reach(blasphemousworld.get_connected_door("D06Z01S16[W]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D06Z01S16[CherubsL]"), player) or \
                    (state.can_reach(blasphemousworld.get_connected_door("D06Z01S16[CherubsR]"), player) and \
                        (state.has("Purified Hand of the Nun", player) or \
                            state._blasphemous_air_stall(player) and \
                                state.has_any({"Three Gnarled Tongues", "The Young Mason's Wheel"}, player))) or \
                                    (state.can_reach(blasphemousworld.get_connected_door("D06Z01S16[E]"), player) and \
                                        (state.has("Three Gnarled Tongues", player) or \
                                            state._blasphemous_cross_gap(player, 7)))))
    set_rule(world.get_entrance("D06Z01S16[-CherubsR]", player),
        lambda state: state.has("Linen of Golden Thread", player) and \
            (state.can_reach(blasphemousworld.get_connected_door("D06Z01S16[E]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D06Z01S16[CherubsR]"), player) or \
                    (state.can_reach(blasphemousworld.get_connected_door("D06Z01S16[CherubsL]"), player) and \
                        (state._blasphemous_air_stall(player) or \
                            state.has_any({"Three Gnarled Tongues", "Purified Hand of the Nun"}, player))) or \
                                (state.can_reach(blasphemousworld.get_connected_door("D06Z01S16[W]"), player) and \
                                    (state.has("Three Gnarled Tongues", player) or \
                                        state._blasphemous_cross_gap(player, 1)))))
    
    # D06Z01S17 (Archcathedral Rooftops)
    set_rule(world.get_entrance("D06Z01S17[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D06Z01S17[W]"), player) or \
            (state.can_reach(blasphemousworld.get_connected_door("D06Z01S17[E]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D06Z01S17[CherubsR]"), player)) and \
                    state.has("Blood Perpetuated in Sand", player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D06Z01S17[CherubsL]"), player) and \
                            state.has("Purified Hand of the Nun", player))
    set_rule(world.get_entrance("D06Z01S17[E]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D06Z01S17[E]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D06Z01S17[CherubsR]"), player) or \
                state.has("Blood Perpetuated in Sand", player) and \
                    (state.can_reach(blasphemousworld.get_connected_door("D06Z01S17[W]"), player) or \
                        state.can_reach(blasphemousworld.get_connected_door("D06Z01S17[CherubsL]"), player) and \
                            state.has("Purified Hand of the Nun", player)))
    set_rule(world.get_entrance("D06Z01S17[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D06Z01S18 (Archcathedral Rooftops)
    set_rule(world.get_entrance("D06Z01S18[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D06Z01S25 (Archcathedral Rooftops)
    set_rule(world.get_entrance("D06Z01S25[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D06Z01S25[W]"), player))
    set_rule(world.get_entrance("D06Z01S25[E]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D06Z01S25[E]"), player))
    # to do: boss logic

    # D08Z01S01 (Bridge of the Three Cavalries)
    set_rule(world.get_entrance("D08Z01S01[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D08Z01S01[W]"), player))
    set_rule(world.get_entrance("D08Z01S01[E]", player),
        lambda state: state.has_group("wounds", player, 3) and \
            (state.can_reach(blasphemousworld.get_connected_door("D08Z01S01[E]"), player) or \
                state.can_reach(blasphemousworld.get_connected_door("D08Z01S01[Cherubs]"), player)))
    # to do: boss logic

    # D08Z01S02 (Bridge of the Three Cavalries)
    set_rule(world.get_entrance("D08Z01S02[-Cherubs]", player),
        lambda state: state.has("Linen of Golden Thread", player))
    
    # D08Z02S03 (Ferrous Tree)
    set_rule(world.get_entrance("D08Z02S03[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D08Z01S02[NE]"), player) or \
            state.can_reach(blasphemousworld.get_connected_door("D08Z01S02[SE]"), player))
    
    # D08Z03S01 (Hall of the Dawning)
    set_rule(world.get_entrance("D08Z03S01[E]", player),
        lambda state: state.has("Verses Spun from Gold", player, 4))
    
    # D08Z03S02 (Hall of the Dawning)
    set_rule(world.get_entrance("D08Z03S02[NW]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D08Z03S02[NW]"), player) or \
            state.has("Wall Climb", player))
    
    # D08Z03S03 (Hall of the Dawning)
    set_rule(world.get_entrance("D08Z03S03[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D08Z03S03[W]"), player))
    set_rule(world.get_entrance("D08Z03S03[E]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D08Z03S03[E]"), player))
    # to do: boss logic

    # D09Z01S02 (Wall of the Holy Prohibitions)
    set_rule(world.get_entrance("D09Z01S02[Cell1]", player),
        lambda state: state.has("Key of the Secular", player))
    set_rule(world.get_entrance("D09Z01S02[Cell6]", player),
        lambda state: state.has("Key of the Scribe", player))
    set_rule(world.get_entrance("D09Z01S02[Cell4]", player),
        lambda state: state.has("Key of the Inquisitor", player))
    set_rule(world.get_entrance("D09Z01S02[Cell3]", player),
        lambda state: state.has("Key of the Secular"))
    set_rule(world.get_entrance("D09Z01S02[Cell23]", player),
        lambda state: state.has("Key of the Secular", player))
    
    # D09Z01S03 (Wall of the Holy Prohibitions)
    set_rule(world.get_entrance("D09Z01S03[W]", player),
        lambda state: state.can_reach(blasphemousworld.get_connected_door("D09Z01S03[N]"), player))
    # to do: boss logic

    # D09Z01S06 (Wall of the Holy Prohibitions)
    set_rule(world.get_entrance("D09Z01S06[W]", player),
        lambda state: state.has("Key of the High Peaks", player))
    
    


    # old logic
    # entrances
    for i in world.get_region("Deambulatory of His Holiness", player).entrances:
        set_rule(i, lambda state: state._blasphemous_3_masks(player))
    for i in world.get_region("Ferrous Tree", player).entrances:
        set_rule(i, lambda state: state._blasphemous_bridge_access(player))
    for i in world.get_region("Mother of Mothers", player).entrances:
        set_rule(i, lambda state: state._blasphemous_bridge_access(player))
    for i in world.get_region("Mourning and Havoc", player).entrances:
        set_rule(i, lambda state: state._blasphemous_blood_relic(player) or \
            state.can_reach(world.get_region("Mother of Mothers", player), player))
    for i in world.get_region("Patio of the Silent Steps", player).entrances:
        set_rule(i, lambda state: state._blasphemous_bridge_access(player))
    for i in world.get_region("The Resting Place of the Sister", player).entrances:
        set_rule(i, lambda state: state._blasphemous_blood_relic(player))
    for i in world.get_region("The Sleeping Canvases", player).entrances:
        set_rule(i, lambda state: state._blasphemous_bridge_access(player))
    for i in world.get_region("Wall of the Holy Prohibitions", player).entrances:
        set_rule(i, lambda state: state._blasphemous_1_mask(player) and \
            state._blasphemous_bridge_access(player))

    # Albero
    set_rule(world.get_location("Albero: Bless Linen Cloth", player), 
        lambda state: state._blasphemous_cloth(player))
    set_rule(world.get_location("Albero: Bless Hatched Egg", player),
        lambda state: state._blasphemous_egg(player))
    set_rule(world.get_location("Albero: Bless Severed Hand", player),
        lambda state: state._blasphemous_hand(player))
    set_rule(world.get_location("Albero: First gift for Cleofas", player),
        lambda state: state.can_reach(world.get_region("Mother of Mothers", player)))
    set_rule(world.get_location("Albero: Final gift for Cleofas", player),
        lambda state: state.can_reach(world.get_region("Mother of Mothers", player)) and \
            state._blasphemous_marks(player) and \
                state._blasphemous_cord(player))
    set_rule(world.get_location("Albero: Tirso's 1st reward", player),
        lambda state: state._blasphemous_tirso_1(player))
    set_rule(world.get_location("Albero: Tirso's 2nd reward", player),
        lambda state: state._blasphemous_tirso_2(player))
    set_rule(world.get_location("Albero: Tirso's 3rd reward", player),
        lambda state: state._blasphemous_tirso_3(player))
    set_rule(world.get_location("Albero: Tirso's 4th reward", player),
        lambda state: state._blasphemous_tirso_4(player))
    set_rule(world.get_location("Albero: Tirso's 5th reward", player),
        lambda state: state._blasphemous_tirso_5(player))
    set_rule(world.get_location("Albero: Tirso's 6th reward", player),
        lambda state: state._blasphemous_tirso_6(player))
    set_rule(world.get_location("Albero: Tirso's final reward", player),
        lambda state: state._blasphemous_tirso_6(player) and \
            state.can_reach(world.get_region("Wall of the Holy Prohibitions", player)) and \
                state._blasphemous_silver_key(player) and \
                    state._blasphemous_bronze_key(player))
    set_rule(world.get_location("Albero: Lvdovico's 1st reward", player),
        lambda state: state._blasphemous_tentudia_1(player))
    set_rule(world.get_location("Albero: Lvdovico's 2nd reward", player),
        lambda state: state._blasphemous_tentudia_2(player))
    set_rule(world.get_location("Albero: Lvdovico's 3rd reward", player),
        lambda state: state._blasphemous_tentudia_3(player))
    set_rule(world.get_location("Ossuary: Isidora, Voice of the Dead", player),
        lambda state: state._blasphemous_bones_30(player))
    set_rule(world.get_location("Ossuary: 1st reward", player),
        lambda state: state._blasphemous_bones_4(player))
    set_rule(world.get_location("Ossuary: 2nd reward", player),
        lambda state: state._blasphemous_bones_8(player))
    set_rule(world.get_location("Ossuary: 3rd reward", player),
        lambda state: state._blasphemous_bones_12(player))
    set_rule(world.get_location("Ossuary: 4th reward", player),
        lambda state: state._blasphemous_bones_16(player))
    set_rule(world.get_location("Ossuary: 5th reward", player),
        lambda state: state._blasphemous_bones_20(player))
    set_rule(world.get_location("Ossuary: 6th reward", player),
        lambda state: state._blasphemous_bones_24(player))
    set_rule(world.get_location("Ossuary: 7th reward", player),
        lambda state: state._blasphemous_bones_28(player))
    set_rule(world.get_location("Ossuary: 8th reward", player),
        lambda state: state._blasphemous_bones_32(player))
    set_rule(world.get_location("Ossuary: 9th reward", player),
        lambda state: state._blasphemous_bones_36(player))
    set_rule(world.get_location("Ossuary: 10th reward", player),
        lambda state: state._blasphemous_bones_40(player))
    set_rule(world.get_location("Ossuary: 11th reward", player),
        lambda state: state._blasphemous_bones_44(player))

    # All the Tears of the Sea
    set_rule(world.get_location("AtTotS: Miriam's gift", player),
        lambda state: state._blasphemous_2_masks(player) and \
            state._blasphemous_fall_relic(player) and \
                state._blasphemous_blood_relic(player) and \
                    state._blasphemous_root_relic(player) and \
                        state._blasphemous_miasma_relic(player))

    # Archcathedral Rooftops
    set_rule(world.get_location("AR: Second soldier fight", player),
        lambda state: state._blasphemous_1_mask(player))
    set_rule(world.get_location("AR: Third soldier fight", player),
        lambda state: state._blasphemous_2_masks(player))
    set_rule(world.get_location("AR: Upper west shaft Child of Moonlight", player),
        lambda state: state._blasphemous_1_mask(player))
    set_rule(world.get_location("AR: Upper west shaft chest", player),
        lambda state: state._blasphemous_2_masks(player) and \
            state._blasphemous_fall_relic(player) and \
                state._blasphemous_root_relic(player))
    set_rule(world.get_location("AR: Lady of the Six Sorrows", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_miasma_relic(player) and \
                state._blasphemous_root_relic(player))
    set_rule(world.get_location("AR: Upper east shaft ledge", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_miasma_relic(player) and \
                state._blasphemous_root_relic(player) and \
                    state._blasphemous_1_mask(player))
    set_rule(world.get_location("AR: Mea Culpa altar", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_miasma_relic(player) and \
                    state._blasphemous_2_masks(player))
    set_rule(world.get_location("AR: Crisanta of the Wrapped Agony", player),
        lambda state: state._blasphemous_3_masks(player))
    
    # Bridge of the Three Cavalries
    set_rule(world.get_location("BotTC: Esdras, of the Anointed Legion", player),
        lambda state: state._blasphemous_bridge_access(player))
    set_rule(world.get_location("BotTC: Esdras' gift", player),
        lambda state: state._blasphemous_bridge_access(player))
    set_rule(world.get_location("BotTC: Inside giant statue", player),
        lambda state: state._blasphemous_bridge_access(player) and \
            state._blasphemous_laudes_gate(player))
    
    # Brotherhood of the Silent Sorrow
    set_rule(world.get_location("BotSS: Starting room Child of Moonlight", player),
        lambda state: (state._blasphemous_blood_relic(player) and \
            (state._blasphemous_root_relic(player)) or \
                (state._blasphemous_fall_relic(player))) or \
                    (state._blasphemous_blood_relic(player) and \
                        state._blasphemous_cherub_6(player)) or \
                            (state._blasphemous_debla(player) or \
                                state._blasphemous_taranto(player)))
    set_rule(world.get_location("BotSS: Starting room ledge", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_fall_relic(player))
    set_rule(world.get_location("BotSS: Chamber of the Eldest Brother", player),
        lambda state: state._blasphemous_elder_key(player))
    set_rule(world.get_location("BotSS: Outside church", player),
        lambda state: state._blasphemous_blood_relic(player))
    set_rule(world.get_location("BotSS: Esdras' final gift", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_scapular(player) and \
                state._blasphemous_bridge_access(player))
    set_rule(world.get_location("BotSS: Crisanta's gift", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_scapular(player) and \
                state._blasphemous_heart_c(player) and \
                    state._blasphemous_3_masks(player) and \
                        state._blasphemous_bridge_access(player))
    
    # Convent of our Lady of the Charred Visage
    set_rule(world.get_location("CoOLotCV: Lower west statue", player),
        lambda state: state._blasphemous_miasma_relic(player))
    set_rule(world.get_location("CoOLotCV: Lady of the Six Sorrows", player),
        lambda state: state._blasphemous_bridge_access(player) and \
            state._blasphemous_1_mask(player) and \
                state._blasphemous_bronze_key(player) and \
                    state._blasphemous_silver_key(player) and \
                        state._blasphemous_high_key(player))
    set_rule(world.get_location("CoOLotCV: Fountain of burning oil", player),
        lambda state: state._blasphemous_thimble(player))
    set_rule(world.get_location("CoOLotCV: Mask room", player),
        lambda state: state._blasphemous_bridge_access(player) and \
            state._blasphemous_1_mask(player) and \
                state._blasphemous_bronze_key(player) and \
                    state._blasphemous_silver_key(player) and \
                        state._blasphemous_high_key(player))

    # Desecrated Cistern
    set_rule(world.get_location("DC: Upper east tunnel chest", player),
        lambda state: state._blasphemous_water_relic(player) or \
            state._blasphemous_fall_relic(player))
    set_rule(world.get_location("DC: Upper east Child of Moonlight", player),
        lambda state: state._blasphemous_water_relic(player) or \
            state._blasphemous_fall_relic(player) or \
                state._blasphemous_cherub_13(player))
    set_rule(world.get_location("DC: Hidden alcove near fountain", player),
        lambda state: state._blasphemous_water_relic(player))
    set_rule(world.get_location("DC: Shroud puzzle", player),
        lambda state: state._blasphemous_corpse_relic(player) and \
            state._blasphemous_miasma_relic(player) and \
                state._blasphemous_water_relic(player))
    set_rule(world.get_location("DC: Chalice room", player),
        lambda state: (state._blasphemous_miasma_relic(player) and \
            state._blasphemous_water_relic(player) and \
                state._blasphemous_root_relic(player)) or \
                    (state._blasphemous_fall_relic(player) and \
                        state._blasphemous_root_relic(player)))
    set_rule(world.get_location("DC: Mea Culpa altar", player),
        lambda state: state._blasphemous_chalice(player) and \
            state._blasphemous_bridge_access(player) and \
                state._blasphemous_1_mask(player) and \
                    state._blasphemous_bronze_key(player) and \
                        state._blasphemous_miasma_relic(player) and \
                            state._blasphemous_water_relic(player) and \
                                state._blasphemous_root_relic(player))
    set_rule(world.get_location("DC: Child of Moonlight, behind pillar", player),
        lambda state: state._blasphemous_miasma_relic(player) and \
            state._blasphemous_water_relic(player))
    set_rule(world.get_location("DC: High ledge near elevator shaft", player),
        lambda state: state._blasphemous_miasma_relic(player) and \
            state._blasphemous_water_relic(player))
    set_rule(world.get_location("DC: Elevator shaft Child of Moonlight", player),
        lambda state: state._blasphemous_fall_relic(player) or \
            (state._blasphemous_miasma_relic(player) and \
                state._blasphemous_water_relic(player) and \
                    state._blasphemous_cherub_22_23_31_32(player)))
    set_rule(world.get_location("DC: Elevator shaft ledge", player),
        lambda state: state._blasphemous_fall_relic(player))

    # Graveyard of the Peaks
    set_rule(world.get_location("GotP: Shop cave Child of Moonlight", player),
        lambda state: state._blasphemous_blood_relic(player) or \
            state._blasphemous_fall_relic(player) or \
                state._blasphemous_cherub_22_23_31_32(player))
    # to do: or dive
    set_rule(world.get_location("GotP: Shop cave hidden hole", player),
        lambda state: state._blasphemous_blood_relic(player) or \
            state._blasphemous_open_holes(player))
    set_rule(world.get_location("GotP: Upper east shaft", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_root_relic(player))
    set_rule(world.get_location("GotP: East cliffside", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_root_relic(player))
    set_rule(world.get_location("GotP: West shaft Child of Moonlight", player),
        lambda state: state._blasphemous_blood_relic(player) or \
            state._blasphemous_cherub_25(player))
    set_rule(world.get_location("GotP: Center shaft Child of Moonlight", player),
        lambda state: state._blasphemous_fall_relic(player) or \
            state._blasphemous_cherub_24_33(player))
    # to do: requires dive
    set_rule(world.get_location("GotP: Amanecida of the Bejeweled Arrow", player),
        lambda state: state._blasphemous_bell(player) and \
            state._blasphemous_blood_relic(player) and \
                state._blasphemous_root_relic(player) and \
                    state._blasphemous_open_holes(player))

    # Grievance Ascends
    set_rule(world.get_location("GA: Lower west ledge", player),
        lambda state: state._blasphemous_miasma_relic(player))
    set_rule(world.get_location("GA: Miasma room floor", player),
        lambda state: state._blasphemous_miasma_relic(player))
    set_rule(world.get_location("GA: Oil of the Pilgrims", player),
        lambda state: state._blasphemous_blood_relic(player))
    set_rule(world.get_location("GA: End of blood bridge", player),
        lambda state: state._blasphemous_blood_relic(player))
    set_rule(world.get_location("GA: Blood bridge Child of Moonlight", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            ((state._blasphemous_aubade(player) and \
                state._blasphemous_ranged(player)) or \
                    state._blasphemous_cherub_21(player)))
    set_rule(world.get_location("GA: Lower east Child of Moonlight", player),
        lambda state: state._blasphemous_root_relic(player) or \
            state._blasphemous_cherub_20(player))
    set_rule(world.get_location("GA: Altasgracias' gift", player),
        lambda state: state._blasphemous_altasgracias_3(player))
    set_rule(world.get_location("GA: Empty giant egg", player),
        lambda state: state._blasphemous_altasgracias_3(player) and \
            state._blasphemous_egg(player))

    # Hall of the Dawning
    set_rule(world.get_location("HotD: Laudes, the First of the Amanecidas", player),
        lambda state: state._blasphemous_bridge_access(player) and \
            state._blasphemous_laudes_gate(player))

    # Jondo
    set_rule(world.get_location("Jondo: Upper east chest", player),
        lambda state: state._blasphemous_fall_relic(player) or \
            state._blasphemous_root_relic(player))
    set_rule(world.get_location("Jondo: Upper west tree root", player),
        lambda state: state._blasphemous_root_relic(player) or \
            state._blasphemous_dawn_heart(player))

    # Knot of the Three Words
    set_rule(world.get_location("KotTW: Gift from the Traitor", player),
        lambda state: state._blasphemous_wood_key(player) and \
            state._blasphemous_eyes(player))
    
    # Library of the Negated Words
    set_rule(world.get_location("LotNW: Root ceiling platform", player),
        lambda state: state._blasphemous_root_relic(player))
    # to do: requires dive (sometimes opens with other skills?)
    set_rule(world.get_location("LotNW: Hidden floor", player),
        lambda state: state._blasphemous_open_holes(player))
    set_rule(world.get_location("LotNW: Miasma hallway chest", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_root_relic(player) and \
                state._blasphemous_miasma_relic(player))
    set_rule(world.get_location("LotNW: Platform puzzle chest", player),
        lambda state: state._blasphemous_blood_relic(player))
    set_rule(world.get_location("LotNW: Elevator Child of Moonlight", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_root_relic(player))
    set_rule(world.get_location("LotNW: Twisted wood hidden wall", player),
        lambda state: state._blasphemous_wood_key(player))

    # Mercy Dreams
    set_rule(world.get_location("MD: Cave Child of Moonlight", player),
        lambda state: state._blasphemous_bridge_access(player) and \
            state._blasphemous_cherub_24_33(player))
    set_rule(world.get_location("MD: Behind gate to TSC", player),
        lambda state: state._blasphemous_bridge_access(player))
    
    # Mother of Mothers
    set_rule(world.get_location("MoM: East chandelier platform", player),
        lambda state: state._blasphemous_blood_relic(player) or \
            state._blasphemous_dawn_heart(player))
    set_rule(world.get_location("MoM: Redento's treasure", player),
        lambda state: state._blasphemous_redento_old(player))
    set_rule(world.get_location("MoM: Final meeting with Redento", player),
        lambda state: state._blasphemous_redento_old(player))
    set_rule(world.get_location("MoM: Giant chandelier statue", player),
        lambda state: state._blasphemous_blood_relic(player))

    # Mountains of the Endless Dusk
    set_rule(world.get_location("MotED: Platform above chasm", player),
        lambda state: state._blasphemous_blood_relic(player))
    set_rule(world.get_location("MotED: Blood platform alcove", player),
        lambda state: state._blasphemous_blood_relic(player))
    set_rule(world.get_location("MotED: Egg hatching", player),
        lambda state: state._blasphemous_pre_egg(player))
    # to do: requires dive
    set_rule(world.get_location("MotED: Amanecida of the Golden Blades", player),
        lambda state: state._blasphemous_bell(player) and \
            state._blasphemous_open_holes(player))
    
    # Mourning and Havoc
    set_rule(world.get_location("MaH: Upper east chest", player),
        lambda state: state._blasphemous_bridge_access(player) and \
            state._blasphemous_root_relic(player))
    set_rule(world.get_location("MaH: Sierpes' eye", player),
        lambda state: state._blasphemous_bridge_access(player) and \
            (state._blasphemous_root_relic(player)) or \
                state._blasphemous_water_relic(player) or \
                    state._blasphemous_dawn_heart(player))
    set_rule(world.get_location("MaH: Sierpes", player),
        lambda state: state._blasphemous_bridge_access(player) and \
            (state._blasphemous_root_relic(player)) or \
                state._blasphemous_water_relic(player) or \
                    state._blasphemous_dawn_heart(player))

    # Patio of the Silent Steps
    set_rule(world.get_location("PotSS: Second area ledge", player),
        lambda state: state._blasphemous_root_relic(player) or \
            state._blasphemous_dawn_heart(player) or \
                (state._blasphemous_wheel(player) and \
                    state._blasphemous_ranged(player)))
    set_rule(world.get_location("PotSS: Third area upper ledge", player),
        lambda state: state._blasphemous_root_relic(player) or \
            state._blasphemous_dawn_heart(player))
    set_rule(world.get_location("PotSS: Climb to WotHP", player),
        lambda state: (state._blasphemous_blood_relic(player) and \
            state._blasphemous_root_relic(player)) or \
                (state.can_reach(world.get_region("Wall of the Holy Prohibitions", player)) and \
                    state._blasphemous_bronze_key(player)))
    # to do: requires dive
    set_rule(world.get_location("PotSS: Amanecida of the Chiselled Steel", player),
        lambda state: state._blasphemous_bell(player) and \
            state._blasphemous_open_holes(player))
    
    # Petrous
    # to do: requires dive
    set_rule(world.get_location("Petrous: Temple entrance", player),
        lambda state: state._blasphemous_open_holes(player))

    # The Sleeping Canvases
    set_rule(world.get_location("TSC: Candle wax puzzle", player),
        lambda state: state._blasphemous_both_wax(player))
    set_rule(world.get_location("TSC: Under elevator shaft", player),
        lambda state: state._blasphemous_fall_relic(player))
    set_rule(world.get_location("TSC: Jocinero's 1st reward", player),
        lambda state: state._blasphemous_cherubs_20(player))
    set_rule(world.get_location("TSC: Jocinero's final reward", player),
        lambda state: state._blasphemous_cherubs_all(player))
    
    # The Holy Line
    set_rule(world.get_location("THL: Across blood platforms", player),
        lambda state: state._blasphemous_blood_relic(player))
    set_rule(world.get_location("THL: Underground chest", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_water_relic(player))
    
    # Wall of the Holy Prohibitions
    set_rule(world.get_location("WotHP: Upper east room, top bronze cell", player),
        lambda state: state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Upper east room, top silver cell", player),
        lambda state: state._blasphemous_silver_key(player))
    set_rule(world.get_location("WotHP: Upper east room, center gold cell", player),
        lambda state: state._blasphemous_gold_key(player))
    set_rule(world.get_location("WotHP: Upper west room, center gold cell", player),
        lambda state: state._blasphemous_gold_key(player) and \
            state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Upper west room, top silver cell", player),
        lambda state: state._blasphemous_silver_key(player) and \
            state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Lower west room, bottom gold cell", player),
        lambda state: state._blasphemous_gold_key(player) and \
            state._blasphemous_bronze_key(player) and \
                state._blasphemous_root_relic(player) and \
                    state._blasphemous_blood_relic(player) and \
                        state._blasphemous_miasma_relic(player))
    set_rule(world.get_location("WotHP: Lower west room, top ledge", player),
        lambda state: state._blasphemous_silver_key(player) and \
            state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Lower east room, hidden ledge", player),
        lambda state: state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Lower east room, bottom silver cell", player),
        lambda state: state._blasphemous_silver_key(player) and \
            state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Lower east room, top bronze cell", player),
        lambda state: state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Lower east room, top silver cell", player),
        lambda state: state._blasphemous_silver_key(player) and \
            state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Outside Child of Moonlight", player),
        lambda state: state._blasphemous_silver_key(player) and \
            state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Oil of the Pilgrims", player),
        lambda state: state._blasphemous_silver_key(player) and \
            state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Quirce, Returned By The Flames", player),
        lambda state: state._blasphemous_silver_key(player) and \
            state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Collapsing floor ledge", player),
        lambda state: state._blasphemous_silver_key(player) and \
            state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Amanecida of the Molten Thorn", player),
        lambda state: state._blasphemous_bell(player) and \
            state._blasphemous_silver_key(player) and \
                state._blasphemous_bronze_key(player))

    # Wasteland of the Buried Churches
    set_rule(world.get_location("WotBC: Under broken bridge", player),
        lambda state: state._blasphemous_blood_relic(player) or \
            state._blasphemous_dawn_heart(player))
    set_rule(world.get_location("WotBC: Cliffside Child of Moonlight", player),
        lambda state: state._blasphemous_cherub_38(player))

    # Where Olive Trees Wither
    set_rule(world.get_location("WOTW: Gift for the tomb", player),
        lambda state: state._blasphemous_full_thimble(player))
    set_rule(world.get_location("WOTW: Underground tomb", player),
        lambda state: state._blasphemous_flowers(player) and \
            (state._blasphemous_full_thimble(player) or \
                state._blasphemous_fall_relic(player)))
    set_rule(world.get_location("WOTW: Underground Child of Moonlight", player),
        lambda state: (state._blasphemous_full_thimble(player) or \
            state._blasphemous_fall_relic(player)) and \
                state._blasphemous_cherub_27(player))
    set_rule(world.get_location("WOTW: Underground ledge", player),
        lambda state: (state._blasphemous_full_thimble(player) or \
            state._blasphemous_fall_relic(player)) and \
                state._blasphemous_blood_relic(player))
    set_rule(world.get_location("WOTW: Upper east Child of Moonlight", player),
        lambda state: state._blasphemous_root_relic(player) or \
            state._blasphemous_cherub_22_23_31_32(player))
    set_rule(world.get_location("WOTW: Upper east statue", player),
        lambda state: state._blasphemous_root_relic(player))
    set_rule(world.get_location("WOTW: Gemino's reward", player),
        lambda state: state._blasphemous_full_thimble(player))

    # Various
    set_rule(world.get_location("Second red candle", player),
        lambda state: state._blasphemous_red_wax(player))
    set_rule(world.get_location("Third red candle", player),
        lambda state: state._blasphemous_red_wax(player))
    set_rule(world.get_location("Second blue candle", player),
        lambda state: state._blasphemous_blue_wax(player))
    set_rule(world.get_location("Third blue candle", player),
        lambda state: state._blasphemous_blue_wax(player))
    set_rule(world.get_location("Confessor Dungeon 1 extra", player),
        lambda state: state._blasphemous_bead(player))
    set_rule(world.get_location("Confessor Dungeon 1 main", player),
        lambda state: state._blasphemous_bead(player))
    set_rule(world.get_location("Confessor Dungeon 2 extra", player),
        lambda state: state._blasphemous_bead(player))
    set_rule(world.get_location("Confessor Dungeon 2 main", player),
        lambda state: state._blasphemous_bead(player))
    set_rule(world.get_location("Confessor Dungeon 3 extra", player),
        lambda state: state._blasphemous_bead(player))
    set_rule(world.get_location("Confessor Dungeon 3 main", player),
        lambda state: state._blasphemous_bead(player))
    set_rule(world.get_location("Confessor Dungeon 4 extra", player),
        lambda state: state._blasphemous_bead(player))
    set_rule(world.get_location("Confessor Dungeon 4 main", player),
        lambda state: state._blasphemous_bead(player))
    set_rule(world.get_location("Confessor Dungeon 5 extra", player),
        lambda state: state._blasphemous_bead(player) and \
            state._blasphemous_bridge_access(player))
    set_rule(world.get_location("Confessor Dungeon 5 main", player),
        lambda state: state._blasphemous_bead(player) and \
            state._blasphemous_bridge_access(player))
    set_rule(world.get_location("Confessor Dungeon 6 extra", player),
        lambda state: state._blasphemous_bead(player) and \
            state._blasphemous_bridge_access(player) and \
                (state._blasphemous_1_mask(player) or \
                    state._blasphemous_blood_relic(player) and \
                        state._blasphemous_silver_key(player) and \
                            state._blasphemous_bronze_key(player)))
    set_rule(world.get_location("Confessor Dungeon 6 main", player),
        lambda state: state._blasphemous_bead(player) and \
            state._blasphemous_bridge_access(player) and \
                (state._blasphemous_1_mask(player) or \
                    state._blasphemous_blood_relic(player) and \
                        state._blasphemous_silver_key(player) and \
                            state._blasphemous_bronze_key(player)))
    set_rule(world.get_location("Confessor Dungeon 7 extra", player),
        lambda state: state._blasphemous_bead(player) and \
            state._blasphemous_bridge_access(player) and \
                state._blasphemous_1_mask(player) and \
                    state._blasphemous_bronze_key(player) and \
                        state._blasphemous_silver_key(player) and \
                            state._blasphemous_blood_relic(player))
    set_rule(world.get_location("Confessor Dungeon 7 main", player),
        lambda state: state._blasphemous_bead(player) and \
            state._blasphemous_bridge_access(player) and \
                state._blasphemous_1_mask(player) and \
                    state._blasphemous_bronze_key(player) and \
                        state._blasphemous_silver_key(player) and \
                            state._blasphemous_blood_relic(player))
    # to do: requires dive
    set_rule(world.get_location("Defeat 1 Amanecida", player),
        lambda state: state._blasphemous_bell(player) and \
            state._blasphemous_open_holes(player))
    set_rule(world.get_location("Defeat 2 Amanecidas", player),
        lambda state: state._blasphemous_bell(player) and \
            state._blasphemous_open_holes(player) and \
                state._blasphemous_blood_relic(player) and \
                    (state._blasphemous_root_relic(player) or \
                        state._blasphemous_bridge_access(player)))
    set_rule(world.get_location("Defeat 3 Amanecidas", player),
        lambda state: state._blasphemous_bell(player) and \
            state._blasphemous_open_holes(player) and \
                state._blasphemous_bridge_access(player) and \
                    state._blasphemous_blood_relic(player) and \
                        (state._blasphemous_root_relic(player) or \
                            (state._blasphemous_1_mask(player) and \
                                state._blasphemous_bronze_key(player) and \
                                    state._blasphemous_silver_key(player))))
    set_rule(world.get_location("Defeat 4 Amanecidas", player),
        lambda state: state._blasphemous_bell(player) and \
            state._blasphemous_open_holes(player) and \
                state._blasphemous_bridge_access(player) and \
                    state._blasphemous_1_mask(player) and \
                        state._blasphemous_blood_relic(player) and \
                            state._blasphemous_root_relic(player) and \
                                state._blasphemous_bronze_key(player) and \
                                    state._blasphemous_silver_key(player))
    set_rule(world.get_location("Defeat all Amanecidas", player),
        lambda state: state._blasphemous_bell(player) and \
            state._blasphemous_open_holes(player) and \
                state._blasphemous_bridge_access(player) and \
                    state._blasphemous_1_mask(player) and \
                        state._blasphemous_blood_relic(player) and \
                            state._blasphemous_root_relic(player) and \
                                state._blasphemous_bronze_key(player) and \
                                    state._blasphemous_silver_key(player))

    # expert logic
    if world.expert_logic[player]:
        # entrances
        for i in world.get_region("Ferrous Tree", player).entrances:
            set_rule(i, lambda state: state._blasphemous_ex_bridge_access(player))
        for i in world.get_region("Mother of Mothers", player).entrances:
            set_rule(i, lambda state: state._blasphemous_ex_bridge_access(player))
        for i in world.get_region("Patio of the Silent Steps", player).entrances:
            set_rule(i, lambda state: state._blasphemous_ex_bridge_access(player))
        for i in world.get_region("The Sleeping Canvases", player).entrances:
            set_rule(i, lambda state: state._blasphemous_ex_bridge_access(player))
        for i in world.get_region("Wall of the Holy Prohibitions", player).entrances:
            set_rule(i, lambda state: state._blasphemous_1_mask(player) and \
                state._blasphemous_ex_bridge_access(player))

        # locations
        set_rule(world.get_location("AR: Upper west shaft chest", player),
            lambda state: state._blasphemous_2_masks(player) and \
                state._blasphemous_fall_relic(player) and \
                    (state._blasphemous_root_relic(player) or \
                        state._blasphemous_ranged(player)))
        set_rule(world.get_location("BotTC: Esdras, of the Anointed Legion", player),
            lambda state: state._blasphemous_ex_bridge_access(player))
        set_rule(world.get_location("BotTC: Esdras' gift", player),
            lambda state: state._blasphemous_ex_bridge_access(player))
        set_rule(world.get_location("BotTC: Inside giant statue", player),
            lambda state: state._blasphemous_ex_bridge_access(player) and \
                state._blasphemous_laudes_gate(player))
        set_rule(world.get_location("BotSS: Esdras' final gift", player),
            lambda state: state._blasphemous_blood_relic(player) and \
                state._blasphemous_scapular(player) and \
                    state._blasphemous_ex_bridge_access(player))
        set_rule(world.get_location("BotSS: Crisanta's gift", player),
            lambda state: state._blasphemous_blood_relic(player) and \
                state._blasphemous_scapular(player) and \
                    state._blasphemous_heart_c(player) and \
                        state._blasphemous_3_masks(player) and \
                            state._blasphemous_ex_bridge_access(player))
        set_rule(world.get_location("CoOLotCV: Lady of the Six Sorrows", player),
            lambda state: state._blasphemous_ex_bridge_access(player) and \
                state._blasphemous_1_mask(player) and \
                    state._blasphemous_bronze_key(player) and \
                        state._blasphemous_silver_key(player) and \
                            state._blasphemous_high_key(player))
        set_rule(world.get_location("CoOLotCV: Mask room", player),
            lambda state: state._blasphemous_ex_bridge_access(player) and \
                state._blasphemous_1_mask(player) and \
                    state._blasphemous_bronze_key(player) and \
                        state._blasphemous_silver_key(player) and \
                            state._blasphemous_high_key(player))
        set_rule(world.get_location("DC: Chalice room", player),
            lambda state: (state._blasphemous_miasma_relic(player) and \
                state._blasphemous_water_relic(player) and \
                    (state._blasphemous_root_relic(player) or \
                        state._blasphemous_dawn_heart(player) or \
                            (state._blasphemous_wheel(player) and \
                                state._blasphemous_ranged(player)))) or \
                                    (state._blasphemous_fall_relic(player) and \
                                        (state._blasphemous_root_relic(player) or \
                                            state._blasphemous_ranged(player))))
        set_rule(world.get_location("DC: Mea Culpa altar", player),
            lambda state: state._blasphemous_chalice(player) and \
                state._blasphemous_ex_bridge_access(player) and \
                    state._blasphemous_1_mask(player) and \
                        state._blasphemous_bronze_key(player) and \
                            (state._blasphemous_fall_relic(player) and \
                                (state._blasphemous_ranged(player) or \
                                    state._blasphemous_root_relic(player))) or \
                                        (state._blasphemous_miasma_relic(player) and \
                                            state._blasphemous_water_relic(player) and \
                                                (state._blasphemous_root_relic(player) or \
                                                    state._blasphemous_dawn_heart(player) or \
                                                        (state._blasphemous_wheel(player) and \
                                                            state._blasphemous_ranged(player)))))
        set_rule(world.get_location("HotD: Laudes, the First of the Amanecidas", player),
            lambda state: state._blasphemous_ex_bridge_access(player) and \
                state._blasphemous_laudes_gate(player))
        set_rule(world.get_location("LotNW: Elevator Child of Moonlight", player),
            lambda state: state._blasphemous_blood_relic(player) and \
                (state._blasphemous_cherub_22_23_31_32(player) and \
                    state._blasphemous_dawn_heart(player) and \
                        state._blasphemous_ranged(player)) or \
                            state._blasphemous_root_relic(player))
        set_rule(world.get_location("MD: Cave Child of Moonlight", player),
            lambda state: state._blasphemous_ex_bridge_access(player) and \
                state._blasphemous_cherub_24_33(player))
        set_rule(world.get_location("MD: Behind gate to TSC", player),
            lambda state: state._blasphemous_ex_bridge_access(player))
        set_rule(world.get_location("MoM: East chandelier platform", player),
            lambda state: state._blasphemous_blood_relic(player) or \
                state._blasphemous_dawn_heart(player) or \
                    (state._blasphemous_wheel(player) and \
                        state._blasphemous_ranged(player)))
        set_rule(world.get_location("MaH: Upper east chest", player),
            lambda state: state._blasphemous_ex_bridge_access(player) and \
                (state._blasphemous_root_relic(player)) or \
                    (state._blasphemous_dawn_heart(player) and \
                        state._blasphemous_ranged(player)))
        set_rule(world.get_location("MaH: Sierpes' eye", player),
            lambda state: state._blasphemous_ex_bridge_access(player) and \
                (state._blasphemous_root_relic(player)) or \
                    state._blasphemous_dawn_heart(player) or \
                        state._blasphemous_water_relic(player) or \
                            (state._blasphemous_wheel(player) and \
                                state._blasphemous_ranged(player)))
        set_rule(world.get_location("MaH: Sierpes", player),
            lambda state: state._blasphemous_ex_bridge_access(player) and \
                (state._blasphemous_root_relic(player)) or \
                    state._blasphemous_dawn_heart(player) or \
                        state._blasphemous_water_relic(player) or \
                            (state._blasphemous_wheel(player) and \
                                state._blasphemous_ranged(player)))
        set_rule(world.get_location("PotSS: Third area upper ledge", player),
            lambda state: state._blasphemous_root_relic(player) or \
                state._blasphemous_dawn_heart(player) or \
                    (state._blasphemous_wheel(player) and \
                        state._blasphemous_ranged(player)))
        set_rule(world.get_location("WotBC: Under broken bridge", player),
            lambda state: state._blasphemous_blood_relic(player) or \
                state._blasphemous_dawn_heart(player) or \
                    (state._blasphemous_wheel(player) and \
                        state._blasphemous_ranged(player)))
        set_rule(world.get_location("Third blue candle", player),
            lambda state: state._blasphemous_blue_wax(player) and \
                state._blasphemous_ex_bridge_access(player))
        set_rule(world.get_location("Confessor Dungeon 5 extra", player),
            lambda state: state._blasphemous_bead(player) and \
                state._blasphemous_ex_bridge_access(player))
        set_rule(world.get_location("Confessor Dungeon 5 main", player),
            lambda state: state._blasphemous_bead(player) and \
                state._blasphemous_ex_bridge_access(player))
        set_rule(world.get_location("Confessor Dungeon 6 extra", player),
            lambda state: state._blasphemous_bead(player) and \
                state._blasphemous_ex_bridge_access(player) and \
                    (state._blasphemous_1_mask(player) or \
                        state._blasphemous_blood_relic(player) and \
                            state._blasphemous_silver_key(player) and \
                                state._blasphemous_bronze_key(player)))
        set_rule(world.get_location("Confessor Dungeon 6 main", player),
            lambda state: state._blasphemous_bead(player) and \
                state._blasphemous_ex_bridge_access(player) and \
                    (state._blasphemous_1_mask(player) or \
                        state._blasphemous_blood_relic(player) and \
                            state._blasphemous_silver_key(player) and \
                                state._blasphemous_bronze_key(player)))
        set_rule(world.get_location("Confessor Dungeon 7 extra", player),
            lambda state: state._blasphemous_bead(player) and \
                state._blasphemous_ex_bridge_access(player) and \
                    state._blasphemous_1_mask(player) and \
                        state._blasphemous_bronze_key(player) and \
                            state._blasphemous_silver_key(player) and \
                                state._blasphemous_blood_relic(player))
        set_rule(world.get_location("Confessor Dungeon 7 main", player),
            lambda state: state._blasphemous_bead(player) and \
                state._blasphemous_ex_bridge_access(player) and \
                    state._blasphemous_1_mask(player) and \
                        state._blasphemous_bronze_key(player) and \
                            state._blasphemous_silver_key(player) and \
                                state._blasphemous_blood_relic(player))
        set_rule(world.get_location("Defeat 2 Amanecidas", player),
            lambda state: state._blasphemous_bell(player) and \
                state._blasphemous_open_holes(player) and \
                    state._blasphemous_blood_relic(player) and \
                        (state._blasphemous_root_relic(player) or \
                            state._blasphemous_ex_bridge_access(player)))
        set_rule(world.get_location("Defeat 3 Amanecidas", player),
            lambda state: state._blasphemous_bell(player) and \
                state._blasphemous_open_holes(player) and \
                    state._blasphemous_ex_bridge_access(player) and \
                        state._blasphemous_blood_relic(player) and \
                            (state._blasphemous_root_relic(player) or \
                                (state._blasphemous_1_mask(player) and \
                                    state._blasphemous_bronze_key(player) and \
                                        state._blasphemous_silver_key(player))))
        set_rule(world.get_location("Defeat 4 Amanecidas", player),
            lambda state: state._blasphemous_bell(player) and \
                state._blasphemous_open_holes(player) and \
                    state._blasphemous_ex_bridge_access(player) and \
                        state._blasphemous_1_mask(player) and \
                            state._blasphemous_blood_relic(player) and \
                                state._blasphemous_root_relic(player) and \
                                    state._blasphemous_bronze_key(player) and \
                                        state._blasphemous_silver_key(player))
        set_rule(world.get_location("Defeat all Amanecidas", player),
            lambda state: state._blasphemous_bell(player) and \
                state._blasphemous_open_holes(player) and \
                    state._blasphemous_ex_bridge_access(player) and \
                        state._blasphemous_1_mask(player) and \
                            state._blasphemous_blood_relic(player) and \
                                state._blasphemous_root_relic(player) and \
                                    state._blasphemous_bronze_key(player) and \
                                        state._blasphemous_silver_key(player))

    # skill rando
    if world.skill_randomizer[player] and not world.expert_logic[player]:
        set_rule(world.get_location("Skill 1, Tier 3", player),
            lambda state: state._blasphemous_bridge_access(player))
        set_rule(world.get_location("Skill 5, Tier 3", player),
            lambda state: state._blasphemous_bridge_access(player))
        set_rule(world.get_location("Skill 3, Tier 2", player),
            lambda state: state._blasphemous_bridge_access(player))
        set_rule(world.get_location("Skill 2, Tier 3", player),
            lambda state: state._blasphemous_blood_relic(player) and \
                state._blasphemous_miasma_relic(player) and \
                        state._blasphemous_2_masks(player) and \
                            state._blasphemous_bridge_access(player))
        set_rule(world.get_location("Skill 4, Tier 3", player),
            lambda state: state._blasphemous_blood_relic(player) and \
                state._blasphemous_miasma_relic(player) and \
                        state._blasphemous_2_masks(player) and \
                            state._blasphemous_bridge_access(player))
        set_rule(world.get_location("Skill 3, Tier 3", player),
            lambda state: state._blasphemous_chalice(player) and \
                state._blasphemous_bridge_access(player) and \
                    state._blasphemous_1_mask(player) and \
                        state._blasphemous_bronze_key(player) and \
                            state._blasphemous_miasma_relic(player) and \
                                state._blasphemous_water_relic(player) and \
                                    state._blasphemous_root_relic(player))
    elif world.skill_randomizer[player] and world.expert_logic[player]:
        set_rule(world.get_location("Skill 1, Tier 3", player),
            lambda state: state._blasphemous_ex_bridge_access(player))
        set_rule(world.get_location("Skill 5, Tier 3", player),
            lambda state: state._blasphemous_ex_bridge_access(player))
        set_rule(world.get_location("Skill 3, Tier 2", player),
            lambda state: state._blasphemous_ex_bridge_access(player))
        set_rule(world.get_location("Skill 2, Tier 3", player),
            lambda state: state._blasphemous_blood_relic(player) and \
                state._blasphemous_miasma_relic(player) and \
                        state._blasphemous_2_masks(player) and \
                            state._blasphemous_ex_bridge_access(player))
        set_rule(world.get_location("Skill 4, Tier 3", player),
            lambda state: state._blasphemous_blood_relic(player) and \
                state._blasphemous_miasma_relic(player) and \
                        state._blasphemous_2_masks(player) and \
                            state._blasphemous_ex_bridge_access(player))
        set_rule(world.get_location("Skill 3, Tier 3", player),
            lambda state: state._blasphemous_chalice(player) and \
                state._blasphemous_ex_bridge_access(player) and \
                    state._blasphemous_1_mask(player) and \
                        state._blasphemous_bronze_key(player) and \
                            (state._blasphemous_fall_relic(player) and \
                                (state._blasphemous_ranged(player) or \
                                    state._blasphemous_root_relic(player))) or \
                                        (state._blasphemous_miasma_relic(player) and \
                                            state._blasphemous_water_relic(player) and \
                                                (state._blasphemous_root_relic(player) or \
                                                    state._blasphemous_dawn_heart(player) or \
                                                        (state._blasphemous_wheel(player) and \
                                                            state._blasphemous_ranged(player)))))

    # difficulty (easy)
    if world.difficulty[player].value == 0:
        for i in world.get_region("Desecrated Cistern", player).entrances:
            add_rule(i, lambda state: state._blasphemous_wound_boss_easy(player))
        for i in world.get_region("Ferrous Tree", player).entrances:
            add_rule(i, lambda state: state._blasphemous_esdras_boss_easy(player))
        for i in world.get_region("Patio of the Silent Steps", player).entrances:
            add_rule(i, lambda state: state._blasphemous_esdras_boss_easy(player))
        for i in world.get_region("The Sleeping Canvases", player).entrances:
            add_rule(i, lambda state: state._blasphemous_esdras_boss_easy(player))
        for i in world.get_region("Deambulatory of His Holiness", player).entrances:
            add_rule(i, lambda state: state._blasphemous_endgame_boss_easy(player))
        add_rule(world.get_location("Albero: Donate 5000 Tears", player),
            lambda state: state._blasphemous_wound_boss_easy(player))
        add_rule(world.get_location("Albero: Donate 50000 Tears", player),
            lambda state: state._blasphemous_wound_boss_easy(player))
        add_rule(world.get_location("Albero: Tirso's final reward", player),
            lambda state: state._blasphemous_mask_boss_easy(player))
        add_rule(world.get_location("Ossuary: Isidora, Voice of the Dead", player),
            lambda state: state._blasphemous_endgame_boss_easy(player))
        add_rule(world.get_location("AR: Crisanta of the Wrapped Agony", player),
            lambda state: state._blasphemous_endgame_boss_easy(player))
        add_rule(world.get_location("BotTC: Esdras, of the Anointed Legion", player),
            lambda state: state._blasphemous_esdras_boss_easy(player))
        add_rule(world.get_location("BotTC: Esdras' gift", player),
            lambda state: state._blasphemous_esdras_boss_easy(player))
        add_rule(world.get_location("BotTC: Inside giant statue", player),
            lambda state: state._blasphemous_endgame_boss_easy(player))
        add_rule(world.get_location("BotSS: Crisanta's gift", player),
            lambda state: state._blasphemous_endgame_boss_easy(player))
        add_rule(world.get_location("CoOLotCV: Lady of the Six Sorrows", player),
            lambda state: state._blasphemous_mask_boss_easy(player))
        add_rule(world.get_location("CoOLotCV: Mask room", player),
            lambda state: state._blasphemous_mask_boss_easy(player))
        add_rule(world.get_location("GotP: Amanecida of the Bejeweled Arrow", player),
            lambda state: state._blasphemous_endgame_boss_easy(player))
        add_rule(world.get_location("HotD: Laudes, the First of the Amanecidas", player),
            lambda state: state._blasphemous_endgame_boss_easy(player))
        add_rule(world.get_location("LotNW: Elevator Child of Moonlight", player),
            lambda state: state._blasphemous_mask_boss_easy(player))
        add_rule(world.get_location("LotNW: Mask room", player),
            lambda state: state._blasphemous_mask_boss_easy(player))
        add_rule(world.get_location("LotNW: Mea Culpa altar", player),
            lambda state: state._blasphemous_mask_boss_easy(player))
        add_rule(world.get_location("LotNW: Red candle", player),
            lambda state: state._blasphemous_mask_boss_easy(player))
        add_rule(world.get_location("Third blue candle", player),
            lambda state: state._blasphemous_wound_boss_easy(player))
        add_rule(world.get_location("MD: Cave Child of Moonlight", player),
            lambda state: state._blasphemous_wound_boss_easy(player))
        add_rule(world.get_location("MD: Behind gate to TSC", player),
            lambda state: state._blasphemous_wound_boss_easy(player))
        add_rule(world.get_location("MoM: Melquiades, The Exhumed Archbishop", player),
            lambda state: state._blasphemous_mask_boss_easy(player))
        add_rule(world.get_location("MoM: Mask room", player),
            lambda state: state._blasphemous_mask_boss_easy(player))
        add_rule(world.get_location("MotED: Amanecida of the Golden Blades", player),
            lambda state: state._blasphemous_endgame_boss_easy(player))
        add_rule(world.get_location("MaH: Sierpes' eye", player),
            lambda state: state._blasphemous_endgame_boss_easy(player))
        add_rule(world.get_location("MaH: Sierpes", player),
            lambda state: state._blasphemous_endgame_boss_easy(player))
        add_rule(world.get_location("PotSS: Amanecida of the Chiselled Steel", player),
            lambda state: state._blasphemous_endgame_boss_easy(player))
        add_rule(world.get_location("TSC: Under elevator shaft", player),
            lambda state: state._blasphemous_mask_boss_easy(player))
        add_rule(world.get_location("TSC: Exposito, Scion of Abjuration", player),
            lambda state: state._blasphemous_mask_boss_easy(player))
        add_rule(world.get_location("WotHP: Quirce, Returned By The Flames", player),
            lambda state: state._blasphemous_mask_boss_easy(player))
        add_rule(world.get_location("WotHP: Collapsing floor ledge", player),
            lambda state: state._blasphemous_mask_boss_easy(player))
        add_rule(world.get_location("WotHP: Amanecida of the Molten Thorn", player),
            lambda state: state._blasphemous_endgame_boss_easy(player))
        add_rule(world.get_location("Confessor Dungeon 4 extra", player),
            lambda state: state._blasphemous_wound_boss_easy(player))
        add_rule(world.get_location("Confessor Dungeon 4 main", player),
            lambda state: state._blasphemous_wound_boss_easy(player))
        add_rule(world.get_location("Confessor Dungeon 5 extra", player),
            lambda state: state._blasphemous_wound_boss_easy(player))
        add_rule(world.get_location("Confessor Dungeon 5 main", player),
            lambda state: state._blasphemous_wound_boss_easy(player))
        add_rule(world.get_location("Confessor Dungeon 6 extra", player),
            lambda state: state._blasphemous_wound_boss_easy(player))
        add_rule(world.get_location("Confessor Dungeon 6 main", player),
            lambda state: state._blasphemous_wound_boss_easy(player))
        add_rule(world.get_location("Confessor Dungeon 7 extra", player),
            lambda state: state._blasphemous_wound_boss_easy(player))
        add_rule(world.get_location("Confessor Dungeon 7 main", player),
            lambda state: state._blasphemous_wound_boss_easy(player))
        add_rule(world.get_location("Defeat 1 Amanecida", player),
            lambda state: state._blasphemous_endgame_boss_easy(player))
        add_rule(world.get_location("Defeat 2 Amanecidas", player),
            lambda state: state._blasphemous_endgame_boss_easy(player))
        add_rule(world.get_location("Defeat 3 Amanecidas", player),
            lambda state: state._blasphemous_endgame_boss_easy(player))
        add_rule(world.get_location("Defeat 4 Amanecidas", player),
            lambda state: state._blasphemous_endgame_boss_easy(player))
        add_rule(world.get_location("Defeat all Amanecidas", player),
            lambda state: state._blasphemous_endgame_boss_easy(player))

    # difficulty (normal)
    elif world.difficulty[player].value == 1:
        for i in world.get_region("Desecrated Cistern", player).entrances:
            add_rule(i, lambda state: state._blasphemous_wound_boss_normal(player))
        for i in world.get_region("Ferrous Tree", player).entrances:
            add_rule(i, lambda state: state._blasphemous_esdras_boss_normal(player))
        for i in world.get_region("Patio of the Silent Steps", player).entrances:
            add_rule(i, lambda state: state._blasphemous_esdras_boss_normal(player))
        for i in world.get_region("The Sleeping Canvases", player).entrances:
            add_rule(i, lambda state: state._blasphemous_esdras_boss_normal(player))
        for i in world.get_region("Deambulatory of His Holiness", player).entrances:
            add_rule(i, lambda state: state._blasphemous_endgame_boss_normal(player))
        add_rule(world.get_location("Albero: Donate 5000 Tears", player),
            lambda state: state._blasphemous_wound_boss_normal(player))
        add_rule(world.get_location("Albero: Donate 50000 Tears", player),
            lambda state: state._blasphemous_wound_boss_normal(player))
        add_rule(world.get_location("Albero: Tirso's final reward", player),
            lambda state: state._blasphemous_mask_boss_normal(player))
        add_rule(world.get_location("Ossuary: Isidora, Voice of the Dead", player),
            lambda state: state._blasphemous_endgame_boss_normal(player))
        add_rule(world.get_location("AR: Crisanta of the Wrapped Agony", player),
            lambda state: state._blasphemous_endgame_boss_normal(player))
        add_rule(world.get_location("BotTC: Esdras, of the Anointed Legion", player),
            lambda state: state._blasphemous_esdras_boss_normal(player))
        add_rule(world.get_location("BotTC: Esdras' gift", player),
            lambda state: state._blasphemous_esdras_boss_normal(player))
        add_rule(world.get_location("BotTC: Inside giant statue", player),
            lambda state: state._blasphemous_endgame_boss_normal(player))
        add_rule(world.get_location("BotSS: Crisanta's gift", player),
            lambda state: state._blasphemous_endgame_boss_normal(player))
        add_rule(world.get_location("CoOLotCV: Lady of the Six Sorrows", player),
            lambda state: state._blasphemous_mask_boss_normal(player))
        add_rule(world.get_location("CoOLotCV: Mask room", player),
            lambda state: state._blasphemous_mask_boss_normal(player))
        add_rule(world.get_location("GotP: Amanecida of the Bejeweled Arrow", player),
            lambda state: state._blasphemous_endgame_boss_normal(player))
        add_rule(world.get_location("HotD: Laudes, the First of the Amanecidas", player),
            lambda state: state._blasphemous_endgame_boss_normal(player))
        add_rule(world.get_location("LotNW: Elevator Child of Moonlight", player),
            lambda state: state._blasphemous_mask_boss_normal(player))
        add_rule(world.get_location("LotNW: Mask room", player),
            lambda state: state._blasphemous_mask_boss_normal(player))
        add_rule(world.get_location("LotNW: Mea Culpa altar", player),
            lambda state: state._blasphemous_mask_boss_normal(player))
        add_rule(world.get_location("LotNW: Red candle", player),
            lambda state: state._blasphemous_mask_boss_normal(player))
        add_rule(world.get_location("Third blue candle", player),
            lambda state: state._blasphemous_wound_boss_normal(player))
        add_rule(world.get_location("MD: Cave Child of Moonlight", player),
            lambda state: state._blasphemous_wound_boss_normal(player))
        add_rule(world.get_location("MD: Behind gate to TSC", player),
            lambda state: state._blasphemous_wound_boss_normal(player))
        add_rule(world.get_location("MoM: Melquiades, The Exhumed Archbishop", player),
            lambda state: state._blasphemous_mask_boss_normal(player))
        add_rule(world.get_location("MoM: Mask room", player),
            lambda state: state._blasphemous_mask_boss_normal(player))
        add_rule(world.get_location("MotED: Amanecida of the Golden Blades", player),
            lambda state: state._blasphemous_endgame_boss_normal(player))
        add_rule(world.get_location("MaH: Sierpes' eye", player),
            lambda state: state._blasphemous_endgame_boss_normal(player))
        add_rule(world.get_location("MaH: Sierpes", player),
            lambda state: state._blasphemous_endgame_boss_normal(player))
        add_rule(world.get_location("PotSS: Amanecida of the Chiselled Steel", player),
            lambda state: state._blasphemous_endgame_boss_normal(player))
        add_rule(world.get_location("TSC: Under elevator shaft", player),
            lambda state: state._blasphemous_mask_boss_normal(player))
        add_rule(world.get_location("TSC: Exposito, Scion of Abjuration", player),
            lambda state: state._blasphemous_mask_boss_normal(player))
        add_rule(world.get_location("WotHP: Quirce, Returned By The Flames", player),
            lambda state: state._blasphemous_mask_boss_normal(player))
        add_rule(world.get_location("WotHP: Collapsing floor ledge", player),
            lambda state: state._blasphemous_mask_boss_normal(player))
        add_rule(world.get_location("WotHP: Amanecida of the Molten Thorn", player),
            lambda state: state._blasphemous_endgame_boss_normal(player))
        add_rule(world.get_location("Confessor Dungeon 4 extra", player),
            lambda state: state._blasphemous_wound_boss_normal(player))
        add_rule(world.get_location("Confessor Dungeon 4 main", player),
            lambda state: state._blasphemous_wound_boss_normal(player))
        add_rule(world.get_location("Confessor Dungeon 5 extra", player),
            lambda state: state._blasphemous_wound_boss_normal(player))
        add_rule(world.get_location("Confessor Dungeon 5 main", player),
            lambda state: state._blasphemous_wound_boss_normal(player))
        add_rule(world.get_location("Confessor Dungeon 6 extra", player),
            lambda state: state._blasphemous_wound_boss_normal(player))
        add_rule(world.get_location("Confessor Dungeon 6 main", player),
            lambda state: state._blasphemous_wound_boss_normal(player))
        add_rule(world.get_location("Confessor Dungeon 7 extra", player),
            lambda state: state._blasphemous_wound_boss_normal(player))
        add_rule(world.get_location("Confessor Dungeon 7 main", player),
            lambda state: state._blasphemous_wound_boss_normal(player))
        add_rule(world.get_location("Defeat 1 Amanecida", player),
            lambda state: state._blasphemous_endgame_boss_normal(player))
        add_rule(world.get_location("Defeat 2 Amanecidas", player),
            lambda state: state._blasphemous_endgame_boss_normal(player))
        add_rule(world.get_location("Defeat 3 Amanecidas", player),
            lambda state: state._blasphemous_endgame_boss_normal(player))
        add_rule(world.get_location("Defeat 4 Amanecidas", player),
            lambda state: state._blasphemous_endgame_boss_normal(player))
        add_rule(world.get_location("Defeat all Amanecidas", player),
            lambda state: state._blasphemous_endgame_boss_normal(player))

    # difficulty (hard)
    elif world.difficulty[player].value == 2:
        for i in world.get_region("Desecrated Cistern", player).entrances:
            add_rule(i, lambda state: state._blasphemous_wound_boss_hard(player))
        for i in world.get_region("Ferrous Tree", player).entrances:
            add_rule(i, lambda state: state._blasphemous_esdras_boss_hard(player))
        for i in world.get_region("Patio of the Silent Steps", player).entrances:
            add_rule(i, lambda state: state._blasphemous_esdras_boss_hard(player))
        for i in world.get_region("The Sleeping Canvases", player).entrances:
            add_rule(i, lambda state: state._blasphemous_esdras_boss_hard(player))
        for i in world.get_region("Deambulatory of His Holiness", player).entrances:
            add_rule(i, lambda state: state._blasphemous_endgame_boss_hard(player))
        add_rule(world.get_location("Albero: Donate 5000 Tears", player),
            lambda state: state._blasphemous_wound_boss_hard(player))
        add_rule(world.get_location("Albero: Donate 50000 Tears", player),
            lambda state: state._blasphemous_wound_boss_hard(player))
        add_rule(world.get_location("Albero: Tirso's final reward", player),
            lambda state: state._blasphemous_mask_boss_hard(player))
        add_rule(world.get_location("Ossuary: Isidora, Voice of the Dead", player),
            lambda state: state._blasphemous_endgame_boss_hard(player))
        add_rule(world.get_location("AR: Crisanta of the Wrapped Agony", player),
            lambda state: state._blasphemous_endgame_boss_hard(player))
        add_rule(world.get_location("BotTC: Esdras, of the Anointed Legion", player),
            lambda state: state._blasphemous_esdras_boss_hard(player))
        add_rule(world.get_location("BotTC: Esdras' gift", player),
            lambda state: state._blasphemous_esdras_boss_hard(player))
        add_rule(world.get_location("BotTC: Inside giant statue", player),
            lambda state: state._blasphemous_endgame_boss_hard(player))
        add_rule(world.get_location("BotSS: Crisanta's gift", player),
            lambda state: state._blasphemous_endgame_boss_hard(player))
        add_rule(world.get_location("CoOLotCV: Lady of the Six Sorrows", player),
            lambda state: state._blasphemous_mask_boss_hard(player))
        add_rule(world.get_location("CoOLotCV: Mask room", player),
            lambda state: state._blasphemous_mask_boss_hard(player))
        add_rule(world.get_location("GotP: Amanecida of the Bejeweled Arrow", player),
            lambda state: state._blasphemous_endgame_boss_hard(player))
        add_rule(world.get_location("HotD: Laudes, the First of the Amanecidas", player),
            lambda state: state._blasphemous_endgame_boss_hard(player))
        add_rule(world.get_location("LotNW: Elevator Child of Moonlight", player),
            lambda state: state._blasphemous_mask_boss_hard(player))
        add_rule(world.get_location("LotNW: Mask room", player),
            lambda state: state._blasphemous_mask_boss_hard(player))
        add_rule(world.get_location("LotNW: Mea Culpa altar", player),
            lambda state: state._blasphemous_mask_boss_hard(player))
        add_rule(world.get_location("LotNW: Red candle", player),
            lambda state: state._blasphemous_mask_boss_hard(player))
        add_rule(world.get_location("Third blue candle", player),
            lambda state: state._blasphemous_wound_boss_hard(player))
        add_rule(world.get_location("MD: Cave Child of Moonlight", player),
            lambda state: state._blasphemous_wound_boss_hard(player))
        add_rule(world.get_location("MD: Behind gate to TSC", player),
            lambda state: state._blasphemous_wound_boss_hard(player))
        add_rule(world.get_location("MoM: Melquiades, The Exhumed Archbishop", player),
            lambda state: state._blasphemous_mask_boss_hard(player))
        add_rule(world.get_location("MoM: Mask room", player),
            lambda state: state._blasphemous_mask_boss_hard(player))
        add_rule(world.get_location("MotED: Amanecida of the Golden Blades", player),
            lambda state: state._blasphemous_endgame_boss_hard(player))
        add_rule(world.get_location("MaH: Sierpes' eye", player),
            lambda state: state._blasphemous_endgame_boss_hard(player))
        add_rule(world.get_location("MaH: Sierpes", player),
            lambda state: state._blasphemous_endgame_boss_hard(player))
        add_rule(world.get_location("PotSS: Amanecida of the Chiselled Steel", player),
            lambda state: state._blasphemous_endgame_boss_hard(player))
        add_rule(world.get_location("TSC: Under elevator shaft", player),
            lambda state: state._blasphemous_mask_boss_hard(player))
        add_rule(world.get_location("TSC: Exposito, Scion of Abjuration", player),
            lambda state: state._blasphemous_mask_boss_hard(player))
        add_rule(world.get_location("WotHP: Quirce, Returned By The Flames", player),
            lambda state: state._blasphemous_mask_boss_hard(player))
        add_rule(world.get_location("WotHP: Collapsing floor ledge", player),
            lambda state: state._blasphemous_mask_boss_hard(player))
        add_rule(world.get_location("WotHP: Amanecida of the Molten Thorn", player),
            lambda state: state._blasphemous_endgame_boss_hard(player))
        add_rule(world.get_location("Confessor Dungeon 4 extra", player),
            lambda state: state._blasphemous_wound_boss_hard(player))
        add_rule(world.get_location("Confessor Dungeon 4 main", player),
            lambda state: state._blasphemous_wound_boss_hard(player))
        add_rule(world.get_location("Confessor Dungeon 5 extra", player),
            lambda state: state._blasphemous_wound_boss_hard(player))
        add_rule(world.get_location("Confessor Dungeon 5 main", player),
            lambda state: state._blasphemous_wound_boss_hard(player))
        add_rule(world.get_location("Confessor Dungeon 6 extra", player),
            lambda state: state._blasphemous_wound_boss_hard(player))
        add_rule(world.get_location("Confessor Dungeon 6 main", player),
            lambda state: state._blasphemous_wound_boss_hard(player))
        add_rule(world.get_location("Confessor Dungeon 7 extra", player),
            lambda state: state._blasphemous_wound_boss_hard(player))
        add_rule(world.get_location("Confessor Dungeon 7 main", player),
            lambda state: state._blasphemous_wound_boss_hard(player))
        add_rule(world.get_location("Defeat 1 Amanecida", player),
            lambda state: state._blasphemous_endgame_boss_hard(player))
        add_rule(world.get_location("Defeat 2 Amanecidas", player),
            lambda state: state._blasphemous_endgame_boss_hard(player))
        add_rule(world.get_location("Defeat 3 Amanecidas", player),
            lambda state: state._blasphemous_endgame_boss_hard(player))
        add_rule(world.get_location("Defeat 4 Amanecidas", player),
            lambda state: state._blasphemous_endgame_boss_hard(player))
        add_rule(world.get_location("Defeat all Amanecidas", player),
            lambda state: state._blasphemous_endgame_boss_hard(player))
