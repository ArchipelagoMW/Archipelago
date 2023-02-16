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

    def _blasphemous_redento(self, player):
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
        return self.has("Tirana of the Celestial Bastion", player)

    def _blasphemous_aubade(self, player):
        return self.has("Aubade of the Nameless Guardian", player)

    def _blasphemous_cherub_6(self, player):
        return self.has_any({"Debla of the Lights", "Taranto to my Sister", "Verdiales of the Forsaken Hamlet", \
            "Tirana of the Celestial Bastion", "Cloistered Ruby"}, player)

    def _blasphemous_cherub_13(self, player):
        return self.has_any({"Ranged Skill", "Debla of the Lights", "Taranto to my Sister", \
            "Cante Jondo of the Three Sisters", "Aubade of the Nameless Guardian", "Tirana of the Celestial Bastion", \
                "Cloistered Ruby"}, player)
    
    def _blasphemous_cherub_20(self, player):
        return self.has_any({"Debla of the Lights", "Lorqiana", "Zarabanda of the Safe Haven", "Taranto to my Sister", \
            "Cante Jondo of the Three Sisters", "Aubade of the Nameless Guardian", "Tirana of the Celestial Bastion", \
                "Cloistered Ruby"}, player)

    def _blasphemous_cherub_21(self, player):
        return self.has_any({"Debla of the Lights", "Taranto to my Sister", "Cante Jondo of the Three Sisters", \
            "Verdiales of the Forsaken Hamlet", "Tirana of the Celestial Bastion", "Cloistered Ruby"}, player)
    
    def _blasphemous_cherub_22_23_31_32(self, player):
        return self.has_any({"Debla of the Lights", "Taranto to my Sister", "Cloistered Ruby"}, player)

    def _blasphemous_cherub_24_33(self, player):
        return self.has_any({"Debla of the Lights", "Taranto to my Sister", "Cante Jondo of the Three Sisters", \
            "Tirana of the Celestial Bastion", "Cloistered Ruby"}, player)

    def _blasphemous_cherub_25(self, player):
        return self.has_any({"Debla of the Lights", "Lorquiana", "Taranto to my Sister", \
            "Cante Jondo of the Three Sisters", "Verdiales of the Forsaken Hamlet", "Aubade of the Nameless Guardian", \
                "Cantina of the Blue Rose", "Cloistered Ruby"}, player)

    def _blasphemous_cherub_27(self, player):
        return self.has_any({"Ranged Skill", "Debla of the Lights", "Lorquiana", "Taranto to my Sister", \
            "Cante Jondo of the Three Sisters", "Aubade of the Nameless Guardian", "Cantina of the Blue Rose", \
                "Cloistered Ruby"}, player)

    def _blasphemous_cherub_38(self, player):
        return self.has_any({"Ranged Skill", "Lorquiana", "Cante Jondo of the Three Sisters", \
            "Aubade of the Nameless Guardian", "Cantina of the Blue Rose", "Cloistered Ruby"}, player) or \
                (self.has("The Young Mason's Wheel", player) and \
                    self.has("Brilliant Heart of Dawn", player))

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
        return self.has_all({"Petrified Bell", "Blood Perpetuated in Sand", "Three Gnarled Tongues", "Key of the Secular", "Key of the Scribe", "Verses Spun from Gold"}, player)

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


def rules(blasphemousworld):
    world = blasphemousworld.multiworld
    player = blasphemousworld.player

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
            state._blasphemous_laudes_gate(player) and \
                state._blasphemous_1_mask(player))
    
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
    set_rule(world.get_location("BotSS: Blue candle", player),
        lambda state: state._blasphemous_blue_wax(player))
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
    set_rule(world.get_location("CoOLotCV: Red candle", player),
        lambda state: state._blasphemous_red_wax(player))
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
                state._blasphemous_1_mask(player) and \
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
    set_rule(world.get_location("LotNW: Red candle", player),
        lambda state: state._blasphemous_red_wax(player))
    set_rule(world.get_location("LotNW: Twisted wood hidden wall", player),
        lambda state: state._blasphemous_wood_key(player))

    # Mercy Dreams
    set_rule(world.get_location("MD: Blue candle", player),
        lambda state: state._blasphemous_bridge_access(player) and \
            state._blasphemous_blue_wax(player))
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
        lambda state: state._blasphemous_redento(player))
    set_rule(world.get_location("MoM: Final meeting with Redento", player),
        lambda state: state._blasphemous_redento(player))
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
    set_rule(world.get_location("WotHP: Lower west room, bottom gold cell", player),
        lambda state: state._blasphemous_gold_key(player) and \
            state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Upper west room, top silver cell", player),
        lambda state: state._blasphemous_silver_key(player) and \
            state._blasphemous_bronze_key(player))
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
        lambda state: state._blasphemous_silver_key(player))
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
                state._blasphemous_laudes_gate(player) and \
                    state._blasphemous_1_mask(player))
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
                    state._blasphemous_1_mask(player) and \
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
        add_rule(world.get_location("MD: Blue candle", player),
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
        add_rule(world.get_location("MD: Blue candle", player),
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
        add_rule(world.get_location("MD: Blue candle", player),
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