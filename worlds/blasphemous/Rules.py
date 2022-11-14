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

    def _blasphemous_bell(self, player):
        return self.has("Petrified Bell", player)

    def _blasphemous_verses(self, player):
        return self.has("Verses Spun from Gold", player, 4)

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

    def _blasphemous_toes(self, player):
        return self.has("Little Toe made of Limestone", player) and \
            self.has("Big Toe made of Limestone", player) and \
                self.has("Fourth Toe made of Limestone", player)

    def _blasphemous_cord(self, player):
        return self.has("Cord of the True Burying", player)

    def _blasphemous_marks(self, player):
        return self.has("Mark of the First Refuge", player) and \
            self.has("Mark of the Second Refuge", player) and \
                self.has("Mark of the Third Refuge", player)

    def _blasphemous_red_wax(self, player):
        return self.has("Bead of Red Wax", player)
    
    def _blasphemous_blue_wax(self, player):
        return self.has("Bead of Blue Wax", player)

    def _blasphemous_both_wax(self, player):
        return self.has("Bead of Red Wax", player) and \
            self.has("Bead of Blue Wax", player)

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

    def _blasphemous_aubade(self, player):
        return self.has("Aubade of the Nameless Guardian", player)

    def _blasphemous_cherub_6(self, player):
        return self.has("Debla of the Lights", player) or \
            self.has("Taranto to my Sister", player) or \
                self.has("Verdiales of the Forsaken Hamlet", player) or \
                    self.has("Tirana of the Celestial Bastion", player) or \
                        self.has("Cloistered Ruby", player)

    # assumed true until random skills are added. needs throwing blood
    def _blasphemous_cherub_13(self, player):
        return True
        #return self.has("Debla of the Lights", player) or \
        #    self.has("Taranto to my Sister", player) or \
        #        self.has("Cante Jondo of the Three Sisters", player) or \
        #            self.has("Aubade of the Nameless Guardian", player) or \
        #                self.has("Tirana of the Celestial Bastion", player) or \
        #                    self.has("Cloistered Ruby", player)
    
    def _blasphemous_cherub_20(self, player):
        return self.has("Debla of the Lights", player) or \
            self.has("Lorquiana", player) or \
                self.has("Zarabanda of the Safe Haven", player) or \
                    self.has("Taranto to my Sister", player) or \
                        self.has("Cante Jondo of the Three Sisters", player) or \
                            self.has("Aubade of the Nameless Guardian", player) or \
                                self.has("Tirana of the Celestial Bastion", player) or \
                                    self.has("Cloistered Ruby", player)

    def _blasphemous_cherub_21(self, player):
        return self.has("Debla of the Lights", player) or \
            self.has("Taranto to my Sister", player) or \
                self.has("Cante Jondo of the Three Sisters", player) or \
                    self.has("Verdiales of the Forsaken Hamlet", player) or \
                        self.has("Tirana of the Celestial Bastion", player) or \
                            self.has("Cloistered Ruby", player)
    
    def _blasphemous_cherub_22_23_31_32(self, player):
        return self.has("Debla of the Lights", player) or \
            self.has("Taranto to my Sister", player) or \
                self.has("Cloistered Ruby", player)

    def _blasphemous_cherub_24_33(self, player):
        return self.has("Debla of the Lights", player) or \
            self.has("Taranto to my Sister", player) or \
                self.has("Cante Jondo of the Three Sisters", player) or \
                    self.has("Tirana of the Celestial Bastion", player) or \
                        self.has("Cloistered Ruby", player)

    def _blasphemous_cherub_25(self, player):
        return self.has("Debla of the Lights", player) or \
            self.has("Lorquiana", player) or \
                self.has("Taranto to my Sister", player) or \
                    self.has("Cante Jondo of the Three Sisters", player) or \
                        self.has("Verdiales of the Forsaken Hamlet", player) or \
                            self.has("Aubade of the Nameless Guardian", player) or \
                                self.has("Cantina of the Blue Rose", player) or \
                                    self.has("Cloistered Ruby", player)

    # assumed true until random skills are added. needs throwing blood
    def _blasphemous_cherub_27(self, player):
        return True
        #return self.has("Debla of the Lights", player) or \
        #    self.has("Lorquiana", player) or \
        #        self.has("Taranto to my Sister", player) or \
        #            self.has("Cante Jondo of the Three Sisters", player) or \
        #                self.has("Aubade of the Nameless Guardian", player) or \
        #                    self.has("Cantina of the Blue Rose", player) or \
        #                        self.has("Cloistered Ruby", player)

    # assumed true until random skills are added. needs throwing blood
    def _blasphemous_cherub_38(self, player):
        return True
        #return self.has("Lorquiana", player) or \
        #    self.has("Cante Jondo of the Three Sisters", player) or \
        #        self.has("Aubade of the Nameless Guardian", player) or \
        #            self.has("Cantina of the Blue Rose", player) or \
        #                self.has("Cloistered Ruby", player) or \
        #                    (self.has("The Young Mason's Wheel", player) and \
        #                        self.has("Brilliant Heart of Dawn", player))

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

    def _blasphemous_3_wounds(self, player):
        return self.has_group("wounds", player, 3)

    def _blasphemous_1_mask(self, player):
        return self.has_group("masks", player, 1)

    def _blasphemous_2_masks(self, player):
        return self.has_group("masks", player, 2)

    def _blasphemous_3_masks(self, player):
        return self.has_group("masks", player, 3)


def rules(blasphemousworld):
    world = blasphemousworld.multiworld
    player = blasphemousworld.player

    # entrances
    for i in world.get_region("Deambulatory of His Holiness", player).entrances:
        set_rule(i, lambda state: state._blasphemous_3_masks(player))
    for i in world.get_region("Ferrous Tree", player).entrances:
        set_rule(i, lambda state: state._blasphemous_3_wounds(player) and \
            state._blasphemous_blood_relic(player))
    for i in world.get_region("Mother of Mothers", player).entrances:
        set_rule(i, lambda state: state._blasphemous_3_wounds(player) and \
            state._blasphemous_blood_relic(player))
    for i in world.get_region("Mourning and Havoc", player).entrances:
        set_rule(i, lambda state: state._blasphemous_blood_relic(player))
    for i in world.get_region("Patio of the Silent Steps", player).entrances:
        set_rule(i, lambda state: state._blasphemous_3_wounds(player) and \
            state._blasphemous_blood_relic(player))
    for i in world.get_region("The Resting Place of the Sister", player).entrances:
        set_rule(i, lambda state: state._blasphemous_blood_relic(player))
    for i in world.get_region("The Sleeping Canvases", player).entrances:
        set_rule(i, lambda state: state._blasphemous_3_wounds(player) and \
            state._blasphemous_blood_relic(player))
    for i in world.get_region("Wall of the Holy Prohibitions", player).entrances:
        set_rule(i, lambda state: state._blasphemous_1_mask(player) and \
            state._blasphemous_3_wounds(player) and \
                state._blasphemous_blood_relic(player))

    # Albero
    set_rule(world.get_location("Albero: Bless cloth", player), 
        lambda state: state._blasphemous_cloth(player))
    set_rule(world.get_location("Albero: Bless egg", player),
        lambda state: state._blasphemous_egg(player))
    set_rule(world.get_location("Albero: Bless hand", player),
        lambda state: state._blasphemous_hand(player))
    set_rule(world.get_location("Albero: Cleofas gift initial", player),
        lambda state: state.can_reach(world.get_region("Mother of Mothers", player)) and \
            state._blasphemous_marks(player))
    set_rule(world.get_location("Albero: Cleofas gift final", player),
        lambda state: state.can_reach(world.get_region("Mother of Mothers", player)) and \
            state._blasphemous_marks(player) and \
                state._blasphemous_cord(player))
    set_rule(world.get_location("Albero: Tirso reward 1", player),
        lambda state: state._blasphemous_tirso_1(player))
    set_rule(world.get_location("Albero: Tirso reward 2", player),
        lambda state: state._blasphemous_tirso_2(player))
    set_rule(world.get_location("Albero: Tirso reward 3", player),
        lambda state: state._blasphemous_tirso_3(player))
    set_rule(world.get_location("Albero: Tirso reward 4", player),
        lambda state: state._blasphemous_tirso_4(player))
    set_rule(world.get_location("Albero: Tirso reward 5", player),
        lambda state: state._blasphemous_tirso_5(player))
    set_rule(world.get_location("Albero: Tirso reward 6", player),
        lambda state: state._blasphemous_tirso_6(player))
    set_rule(world.get_location("Albero: Tirso reward final", player),
        lambda state: state._blasphemous_tirso_6(player) and \
            state.can_reach(world.get_region("Wall of the Holy Prohibitions", player)) and \
                state._blasphemous_silver_key(player) and \
                    state._blasphemous_bronze_key(player))
    set_rule(world.get_location("Albero: Tentudia reward 1", player),
        lambda state: state._blasphemous_tentudia_1(player))
    set_rule(world.get_location("Albero: Tentudia reward 2", player),
        lambda state: state._blasphemous_tentudia_2(player))
    set_rule(world.get_location("Albero: Tentudia reward 3", player),
        lambda state: state._blasphemous_tentudia_3(player))
    set_rule(world.get_location("Ossuary: Isidora reward main", player),
        lambda state: state._blasphemous_bones_30(player))
    set_rule(world.get_location("Ossuary: Reward 1", player),
        lambda state: state._blasphemous_bones_4(player))
    set_rule(world.get_location("Ossuary: Reward 2", player),
        lambda state: state._blasphemous_bones_8(player))
    set_rule(world.get_location("Ossuary: Reward 3", player),
        lambda state: state._blasphemous_bones_12(player))
    set_rule(world.get_location("Ossuary: Reward 4", player),
        lambda state: state._blasphemous_bones_16(player))
    set_rule(world.get_location("Ossuary: Reward 5", player),
        lambda state: state._blasphemous_bones_20(player))
    set_rule(world.get_location("Ossuary: Reward 6", player),
        lambda state: state._blasphemous_bones_24(player))
    set_rule(world.get_location("Ossuary: Reward 7", player),
        lambda state: state._blasphemous_bones_28(player))
    set_rule(world.get_location("Ossuary: Reward 8", player),
        lambda state: state._blasphemous_bones_32(player))
    set_rule(world.get_location("Ossuary: Reward 9", player),
        lambda state: state._blasphemous_bones_36(player))
    set_rule(world.get_location("Ossuary: Reward 10", player),
        lambda state: state._blasphemous_bones_40(player))
    set_rule(world.get_location("Ossuary: Reward 11", player),
        lambda state: state._blasphemous_bones_44(player))

    # All the Tears of the Sea
    set_rule(world.get_location("AtTotS: Miriam gift", player),
        lambda state: state._blasphemous_2_masks(player) and \
            state._blasphemous_fall_relic(player) and \
                state._blasphemous_blood_relic(player) and \
                    state._blasphemous_root_relic(player) and \
                        state._blasphemous_miasma_relic(player))

    # Archcathedral Rooftops
    set_rule(world.get_location("AR: Bridge fight 2", player),
        lambda state: state._blasphemous_1_mask(player))
    set_rule(world.get_location("AR: Bridge fight 3", player),
        lambda state: state._blasphemous_2_masks(player))
    set_rule(world.get_location("AR: Western shaft cherub", player),
        lambda state: state._blasphemous_1_mask(player))
    set_rule(world.get_location("AR: Western shaft chest", player),
        lambda state: state._blasphemous_2_masks(player) and \
            state._blasphemous_fall_relic(player) and \
                state._blasphemous_root_relic(player))
    set_rule(world.get_location("AR: Lady room", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_miasma_relic(player) and \
                state._blasphemous_root_relic(player))
    set_rule(world.get_location("AR: Second checkpoint ledge", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_miasma_relic(player) and \
                state._blasphemous_root_relic(player) and \
                    state._blasphemous_1_mask(player))
    set_rule(world.get_location("AR: Sword room", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_miasma_relic(player) and \
                    state._blasphemous_2_masks(player))
    set_rule(world.get_location("AR: Crisanta", player),
        lambda state: state._blasphemous_3_masks(player) and \
            state._blasphemous_heart_c(player))
    
    # Bridge of the Three Cavalries
    set_rule(world.get_location("BotTC: Esdras", player),
        lambda state: state._blasphemous_3_wounds(player) and \
            state._blasphemous_blood_relic(player))
    set_rule(world.get_location("BotTC: Esdras gift initial", player),
        lambda state: state._blasphemous_3_wounds(player) and \
            state._blasphemous_blood_relic(player))
    set_rule(world.get_location("BotTC: Amanecida core", player),
        lambda state: state._blasphemous_3_wounds(player) and \
            state._blasphemous_verses(player))
    
    # Brotherhood of the Silent Sorrow
    set_rule(world.get_location("BotSS: Initial room cherub", player),
        lambda state: (state._blasphemous_blood_relic(player) and \
            (state._blasphemous_root_relic(player)) or \
                (state._blasphemous_fall_relic(player))) or \
                    (state._blasphemous_blood_relic(player) and \
                        state._blasphemous_cherub_6(player)))
    set_rule(world.get_location("BotSS: Initial room ledge", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_fall_relic(player))
    set_rule(world.get_location("BotSS: Elder Brother's room", player),
        lambda state: state._blasphemous_elder_key(player))
    set_rule(world.get_location("BotSS: Blue candle", player),
        lambda state: state._blasphemous_blue_wax(player))
    set_rule(world.get_location("BotSS: Church entrance", player),
        lambda state: state._blasphemous_blood_relic(player))
    set_rule(world.get_location("BotSS: Esdras gift final", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_scapular(player) and \
                state._blasphemous_3_wounds(player))
    set_rule(world.get_location("BotSS: Crisanta gift", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_scapular(player) and \
                state._blasphemous_heart_c(player) and \
                    state._blasphemous_3_masks(player) and \
                        state._blasphemous_3_wounds(player))
    
    # Convent of our Lady of the Charred Visage
    set_rule(world.get_location("CoOLotCV: Southwest lung room", player),
        lambda state: state._blasphemous_miasma_relic(player))
    set_rule(world.get_location("CoOLotCV: Lady room", player),
        lambda state: state._blasphemous_3_wounds(player) and \
            state._blasphemous_1_mask(player) and \
                state._blasphemous_bronze_key(player) and \
                    state._blasphemous_silver_key(player) and \
                        state._blasphemous_high_key(player))
    set_rule(world.get_location("CoOLotCV: Red candle", player),
        lambda state: state._blasphemous_red_wax(player))
    set_rule(world.get_location("CoOLotCV: Burning oil fountain", player),
        lambda state: state._blasphemous_thimble(player))
    set_rule(world.get_location("CoOLotCV: Mask room", player),
        lambda state: state._blasphemous_3_wounds(player) and \
            state._blasphemous_1_mask(player) and \
                state._blasphemous_bronze_key(player) and \
                    state._blasphemous_silver_key(player) and \
                        state._blasphemous_high_key(player))

    # Desecrated Cistern
    set_rule(world.get_location("DC: Eastern upper tunnel chest", player),
        lambda state: state._blasphemous_water_relic(player) or \
            state._blasphemous_fall_relic(player))
    set_rule(world.get_location("DC: Eastern upper tunnel cherub", player),
        lambda state: state._blasphemous_water_relic(player) or \
            state._blasphemous_fall_relic(player) or \
                state._blasphemous_cherub_13(player))
    set_rule(world.get_location("DC: Hidden hand room", player),
        lambda state: state._blasphemous_water_relic(player))
    set_rule(world.get_location("DC: Shroud puzzle", player),
        lambda state: state._blasphemous_corpse_relic(player))
    set_rule(world.get_location("DC: Chalice room", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            (state._blasphemous_root_relic(player) or \
                state._blasphemous_fall_relic(player)))
    set_rule(world.get_location("DC: Sword room", player),
        lambda state: state._blasphemous_chalice(player) and \
            state._blasphemous_3_wounds(player) and \
                state._blasphemous_1_mask(player) and \
                    state._blasphemous_bronze_key(player) and \
                        ((state._blasphemous_miasma_relic(player) and \
                            state._blasphemous_water_relic(player) and \
                                state._blasphemous_root_relic(player)) or \
                                    state._blasphemous_fall_relic(player)))
    set_rule(world.get_location("DC: Lung tunnel cherub", player),
        lambda state: state._blasphemous_miasma_relic(player) and \
            state._blasphemous_water_relic(player))
    set_rule(world.get_location("DC: Lung tunnel ledge", player),
        lambda state: state._blasphemous_miasma_relic(player) and \
            state._blasphemous_water_relic(player))
    set_rule(world.get_location("DC: Elevator shaft cherub", player),
        lambda state: state._blasphemous_fall_relic(player) or \
            (state._blasphemous_miasma_relic(player) and \
                state._blasphemous_water_relic(player) and \
                    state._blasphemous_cherub_22_23_31_32(player)))
    set_rule(world.get_location("DC: Elevator shaft ledge", player),
        lambda state: state._blasphemous_fall_relic(player))

    # Graveyard of the Peaks
    set_rule(world.get_location("GotP: Shop cave cherub", player),
        lambda state: state._blasphemous_blood_relic(player) or \
            state._blasphemous_fall_relic(player) or \
                state._blasphemous_cherub_22_23_31_32(player))
    # to do: or dive
    set_rule(world.get_location("GotP: Shop cave hole", player),
        lambda state: state._blasphemous_blood_relic(player))
    set_rule(world.get_location("GotP: Eastern shaft upper", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_root_relic(player))
    set_rule(world.get_location("GotP: Amanecida ledge", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_root_relic(player))
    set_rule(world.get_location("GotP: Western shaft cherub", player),
        lambda state: state._blasphemous_blood_relic(player) or \
            state._blasphemous_cherub_25(player))
    set_rule(world.get_location("GotP: Center shaft cherub", player),
        lambda state: state._blasphemous_fall_relic(player) or \
            state._blasphemous_cherub_24_33(player))
    # to do: requires dive
    set_rule(world.get_location("GotP: Bow Amanecida", player),
        lambda state: state._blasphemous_bell(player) and \
            state._blasphemous_blood_relic(player) and \
                state._blasphemous_root_relic(player))

    # Grievance Ascends
    set_rule(world.get_location("GA: Western lung ledge", player),
        lambda state: state._blasphemous_miasma_relic(player))
    set_rule(world.get_location("GA: Lung room lower", player),
        lambda state: state._blasphemous_miasma_relic(player))
    set_rule(world.get_location("GA: Oil room", player),
        lambda state: state._blasphemous_blood_relic(player))
    set_rule(world.get_location("GA: Blood tunnel ledge", player),
        lambda state: state._blasphemous_blood_relic(player))
    set_rule(world.get_location("GA: Blood tunnel cherub", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            (state._blasphemous_aubade(player) or \
                state._blasphemous_cherub_21(player)))
    set_rule(world.get_location("GA: Altasgracias cherub", player),
        lambda state: state._blasphemous_root_relic(player) or \
            state._blasphemous_cherub_20(player))
    set_rule(world.get_location("GA: Altasgracias gift", player),
        lambda state: state._blasphemous_altasgracias_3(player))
    set_rule(world.get_location("GA: Altasgracias cacoon", player),
        lambda state: state._blasphemous_altasgracias_3(player) and \
            state._blasphemous_egg(player))

    # Hall of the Dawning
    set_rule(world.get_location("HotD: Laudes", player),
        lambda state: state._blasphemous_bell(player) and \
            state._blasphemous_1_mask(player) and \
                state._blasphemous_blood_relic(player) and \
                    state._blasphemous_root_relic(player) and \
                        state._blasphemous_silver_key(player) and \
                            state._blasphemous_bronze_key(player) and \
                                state._blasphemous_verses(player))

    # Jondo
    set_rule(world.get_location("Jondo: Eastern entrance chest", player),
        lambda state: state._blasphemous_fall_relic(player) or \
            state._blasphemous_root_relic(player))
    set_rule(world.get_location("Jondo: Western shaft root puzzle", player),
        lambda state: state._blasphemous_root_relic(player))

    # Knot of the Three Words
    set_rule(world.get_location("KotTW: Fourth Visage gift", player),
        lambda state: state._blasphemous_wood_key(player) and \
            state._blasphemous_eyes(player))
    
    # Library of the Negated Words
    set_rule(world.get_location("LotNW: Upper cathedral ledge", player),
        lambda state: state._blasphemous_root_relic(player))
    # to do: requires dive (sometimes opens with other skills?)
    #set_rule(world.get_location("LotNW: Hidden floor", player),
    #    lambda state: state._blasphemous_(player))
    set_rule(world.get_location("LotNW: Lung ambush chest", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_root_relic(player) and \
                state._blasphemous_miasma_relic(player))
    set_rule(world.get_location("LotNW: Platform puzzle chest", player),
        lambda state: state._blasphemous_blood_relic(player))
    set_rule(world.get_location("LotNW: Elevator cherub", player),
        lambda state: (state._blasphemous_cherub_22_23_31_32(player) and \
                state._blasphemous_dawn_heart(player)) or \
                    state._blasphemous_root_relic(player))
    set_rule(world.get_location("LotNW: Red candle", player),
        lambda state: state._blasphemous_red_wax(player))
    set_rule(world.get_location("LotNW: Diosdado gift", player),
        lambda state: state._blasphemous_corpse_relic(player))
    set_rule(world.get_location("LotNW: Fourth Visage hidden wall", player),
        lambda state: state._blasphemous_wood_key(player))

    # Mercy Dreams
    set_rule(world.get_location("MD: Blue candle", player),
        lambda state: state._blasphemous_3_wounds(player) and \
            state._blasphemous_blue_wax(player))
    set_rule(world.get_location("MD: SlC entrance cherub", player),
        lambda state: state._blasphemous_3_wounds(player) and \
            state._blasphemous_cherub_24_33(player))
    set_rule(world.get_location("MD: SlC entrance ledge", player),
        lambda state: state._blasphemous_3_wounds(player))
    
    # Mother of Mothers
    set_rule(world.get_location("MoM: Eastern room lower", player),
        lambda state: state._blasphemous_blood_relic(player))
    set_rule(world.get_location("MoM: Redento prayer room", player),
        lambda state: state._blasphemous_toes(player))
    set_rule(world.get_location("MoM: Redento corpse", player),
        lambda state: state._blasphemous_toes(player))
    set_rule(world.get_location("MoM: Blood incense shaft", player),
        lambda state: state._blasphemous_blood_relic(player))

    # Mountains of the Endless Dusk
    set_rule(world.get_location("MotED: Bell gap ledge", player),
        lambda state: state._blasphemous_blood_relic(player))
    set_rule(world.get_location("MotED: Blood platform", player),
        lambda state: state._blasphemous_blood_relic(player))
    set_rule(world.get_location("MotED: Egg hatching", player),
        lambda state: state._blasphemous_pre_egg(player))
    # to do: requires dive
    set_rule(world.get_location("MotED: Axe Amanecida", player),
        lambda state: state._blasphemous_bell(player))
    
    # Mourning and Havoc
    set_rule(world.get_location("MaH: Eastern chest", player),
        lambda state: state._blasphemous_root_relic(player) and \
            state.can_reach(world.get_region("Mother of Mothers", player)))
    set_rule(world.get_location("MaH: Sierpes reward", player),
        lambda state: state.can_reach(world.get_region("Mother of Mothers", player)) and \
            state._blasphemous_root_relic(player))
    set_rule(world.get_location("MaH: Sierpes", player),
        lambda state: state.can_reach(world.get_region("Mother of Mothers", player)) and \
            state._blasphemous_root_relic(player))

    # Patio of the Silent Steps
    set_rule(world.get_location("PotSS: Garden 2 ledge", player),
        lambda state: state._blasphemous_root_relic(player))
    set_rule(world.get_location("PotSS: Garden 3 upper ledge", player),
        lambda state: state._blasphemous_root_relic(player) or \
            (state._blasphemous_wheel(player) and \
                state._blasphemous_dawn_heart(player)))
    set_rule(world.get_location("PotSS: Northern shaft", player),
        lambda state: (state._blasphemous_blood_relic(player) and \
            state._blasphemous_root_relic(player)) or \
                (state.can_reach(world.get_region("Wall of the Holy Prohibitions", player)) and \
                    state._blasphemous_bronze_key(player)))
    # to do: requires dive
    set_rule(world.get_location("PotSS: Falcata Amanecida", player),
        lambda state: state._blasphemous_bell(player))
    
    # Petrous
    # to do: requires dive
    #set_rule(world.get_location("Petrous: Entrance room", player),
    #    lambda state: state._blasphemous_(player))

    # The Sleeping Canvases
    set_rule(world.get_location("TSC: Wax bleed puzzle", player),
        lambda state: state._blasphemous_both_wax(player))
    set_rule(world.get_location("TSC: Linen drop room", player),
        lambda state: state._blasphemous_fall_relic(player))
    set_rule(world.get_location("TSC: Jocinero gift initial", player),
        lambda state: state._blasphemous_cherubs_20(player))
    set_rule(world.get_location("TSC: Jocinero gift final", player),
        lambda state: state._blasphemous_cherubs_all(player))
    
    # The Holy Line
    set_rule(world.get_location("THL: Mud ledge upper", player),
        lambda state: state._blasphemous_blood_relic(player))
    # to do: requires dive
    #set_rule(world.get_location("THL: Cave ledge", player),
    #    lambda state: state._blasphemous_(player))
    set_rule(world.get_location("THL: Cave chest", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_water_relic(player))
    
    # Wall of the Holy Prohibitions
    set_rule(world.get_location("WotHP: Q1 upper bronze door", player),
        lambda state: state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Q1 upper silver door", player),
        lambda state: state._blasphemous_silver_key(player))
    set_rule(world.get_location("WotHP: Q1 middle gold door", player),
        lambda state: state._blasphemous_gold_key(player))
    set_rule(world.get_location("WotHP: Q2 middle gold door", player),
        lambda state: state._blasphemous_gold_key(player) and \
            state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Q3 lower gold door", player),
        lambda state: state._blasphemous_gold_key(player) and \
            state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Q3 upper silver door", player),
        lambda state: state._blasphemous_silver_key(player) and \
            state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Q3 upper ledge", player),
        lambda state: state._blasphemous_silver_key(player) and \
            state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Q4 hidden ledge", player),
        lambda state: state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Q4 lower silver door", player),
        lambda state: state._blasphemous_silver_key(player) and \
            state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Q4 upper bronze door", player),
        lambda state: state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Q4 upper silver door", player),
        lambda state: state._blasphemous_silver_key(player))
    set_rule(world.get_location("WotHP: CoLCV entrance", player),
        lambda state: state._blasphemous_silver_key(player) and \
            state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Oil room", player),
        lambda state: state._blasphemous_silver_key(player) and \
            state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Quirce", player),
        lambda state: state._blasphemous_silver_key(player) and \
            state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Quirce room", player),
        lambda state: state._blasphemous_silver_key(player) and \
            state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Quirce room", player),
        lambda state: state._blasphemous_silver_key(player) and \
            state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Lance Amanecida", player),
        lambda state: state._blasphemous_bell(player) and \
            state._blasphemous_silver_key(player) and \
                state._blasphemous_bronze_key(player))

    # Wasteland of the Buried Churches
    set_rule(world.get_location("WotBC: Underneath MeD bridge", player),
        lambda state: state._blasphemous_blood_relic(player))
    set_rule(world.get_location("WotBC: Cliffside cherub", player),
        lambda state: state._blasphemous_cherub_38(player))

    # Where Olive Trees Wither
    set_rule(world.get_location("WOTW: White lady flower", player),
        lambda state: state._blasphemous_full_thimble(player))
    set_rule(world.get_location("WOTW: White lady tomb", player),
        lambda state: state._blasphemous_flowers(player) and \
            (state._blasphemous_full_thimble(player) or \
                state._blasphemous_fall_relic(player)))
    set_rule(world.get_location("WOTW: White lady cave cherub", player),
        lambda state: (state._blasphemous_full_thimble(player) or \
            state._blasphemous_fall_relic(player)) and \
                state._blasphemous_cherub_27(player))
    set_rule(world.get_location("WOTW: White lady cave ledge", player),
        lambda state: (state._blasphemous_full_thimble(player) or \
            state._blasphemous_fall_relic(player)) and \
                state._blasphemous_blood_relic(player))
    set_rule(world.get_location("WOTW: Eastern root cherub", player),
        lambda state: state._blasphemous_root_relic(player) or \
            state._blasphemous_cherub_22_23_31_32(player))
    set_rule(world.get_location("WOTW: Eastern root ledge", player),
        lambda state: state._blasphemous_root_relic(player))
    set_rule(world.get_location("WOTW: Gemino gift final", player),
        lambda state: state._blasphemous_full_thimble(player))

    # Various
    set_rule(world.get_location("Guilt arena 1 extra", player),
        lambda state: state._blasphemous_bead(player))
    set_rule(world.get_location("Guilt arena 1 main", player),
        lambda state: state._blasphemous_bead(player))
    set_rule(world.get_location("Guilt arena 2 extra", player),
        lambda state: state._blasphemous_bead(player))
    set_rule(world.get_location("Guilt arena 2 main", player),
        lambda state: state._blasphemous_bead(player))
    set_rule(world.get_location("Guilt arena 3 extra", player),
        lambda state: state._blasphemous_bead(player))
    set_rule(world.get_location("Guilt arena 3 main", player),
        lambda state: state._blasphemous_bead(player))
    set_rule(world.get_location("Guilt arena 4 extra", player),
        lambda state: state._blasphemous_bead(player))
    set_rule(world.get_location("Guilt arena 4 main", player),
        lambda state: state._blasphemous_bead(player))
    set_rule(world.get_location("Guilt arena 5 extra", player),
        lambda state: state._blasphemous_bead(player) and \
            state._blasphemous_3_wounds(player))
    set_rule(world.get_location("Guilt arena 5 main", player),
        lambda state: state._blasphemous_bead(player) and \
            state._blasphemous_3_wounds(player))
    set_rule(world.get_location("Guilt arena 6 extra", player),
        lambda state: state._blasphemous_bead(player) and \
            state._blasphemous_3_wounds(player) and \
                (state._blasphemous_1_mask(player) or \
                    state._blasphemous_blood_relic(player) and \
                        state._blasphemous_silver_key(player) and \
                            state._blasphemous_bronze_key(player)))
    set_rule(world.get_location("Guilt arena 6 main", player),
        lambda state: state._blasphemous_bead(player) and \
            state._blasphemous_3_wounds(player) and \
                (state._blasphemous_1_mask(player) or \
                    state._blasphemous_blood_relic(player) and \
                        state._blasphemous_silver_key(player) and \
                            state._blasphemous_bronze_key(player)))
    set_rule(world.get_location("Guilt arena 7 extra", player),
        lambda state: state._blasphemous_bead(player) and \
            state._blasphemous_3_wounds(player) and \
                state._blasphemous_1_mask(player) and \
                    state._blasphemous_bronze_key(player) and \
                        state._blasphemous_silver_key(player) and \
                            state._blasphemous_blood_relic(player))
    set_rule(world.get_location("Guilt arena 7 main", player),
        lambda state: state._blasphemous_bead(player) and \
            state._blasphemous_3_wounds(player) and \
                state._blasphemous_1_mask(player) and \
                    state._blasphemous_bronze_key(player) and \
                        state._blasphemous_silver_key(player) and \
                            state._blasphemous_blood_relic(player))
    # to do: requires dive
    set_rule(world.get_location("Amanecida 1", player),
        lambda state: state._blasphemous_bell(player))
    set_rule(world.get_location("Amanecida 2", player),
        lambda state: state._blasphemous_bell(player) and \
            state._blasphemous_blood_relic(player) and \
                (state._blasphemous_root_relic(player) or \
                    state._blasphemous_3_wounds(player)))
    set_rule(world.get_location("Amanecida 3", player),
        lambda state: state._blasphemous_bell(player) and \
            state._blasphemous_3_wounds(player) and \
                state._blasphemous_blood_relic(player) and \
                    (state._blasphemous_root_relic(player) or \
                        (state._blasphemous_1_mask(player) and \
                            state._blasphemous_bronze_key(player) and \
                                state._blasphemous_silver_key(player))))
    set_rule(world.get_location("Amanecida 4", player),
        lambda state: state._blasphemous_bell(player) and \
            state._blasphemous_3_wounds(player) and \
                state._blasphemous_1_mask(player) and \
                    state._blasphemous_blood_relic(player) and \
                        state._blasphemous_root_relic(player) and \
                            state._blasphemous_bronze_key(player) and \
                                state._blasphemous_silver_key(player))
    set_rule(world.get_location("All amanecidas reward", player),
        lambda state: state._blasphemous_bell(player) and \
            state._blasphemous_3_wounds(player) and \
                state._blasphemous_1_mask(player) and \
                    state._blasphemous_blood_relic(player) and \
                        state._blasphemous_root_relic(player) and \
                            state._blasphemous_bronze_key(player) and \
                                state._blasphemous_silver_key(player))