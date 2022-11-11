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

    def _blasphemous_bead(self, player):
        return self.has("Immaculate Bead", player)

    def _blasphemous_cloth(self, player):
        return self.has("Linen Cloth", player)

    def _blasphemous_pre_egg(self, player):
        return self.has("Egg of Deformity", player)

    def _blasphemous_egg(self, player):
        return self.has("Hatched Egg of Deformity", player)

    def _blasphemous_hand(self, player):
        return self.has("Severed Hand", player)

    def _blasphemous_thimble(self, player):
        return self.has("Empty Golden Thimble", player)

    def _blasphemous_flowers(self, player):
        return self.has("Dried Flowers bathed in Tears", player)

    def _blasphemous_toes(self, player):
        return self.has("Little Toe made of Limestone", player) and \
            self.has("Big Toe made of Limestone", player) and \
                self.has("Fourth Toe made of Limestone", player)

    def _blasphemous_wax(self, player):
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

    def _blasphemous_prayers_vertical(self, player):
        return self.has("Debla of the Lights", player) or \
            self.has("Taranto to my Sister", player)

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

    def _blasphemous_egg_3(self, player):
        return self.has_group("egg", player, 3)

    def _blasphemous_cherubs_20(self, player):
        return self.has("Child of Moonlight", player, 20)

    def _blasphemous_cherubs_all(self, player):
        return self.has("Child of Moonlight", player, 38)

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
        set_rule(i, lambda state: state._blasphemous_3_wounds(player))
    for i in world.get_region("Hall of the Dawning", player).entrances:
        set_rule(i, lambda state: state._blasphemous_3_wounds(player))
    for i in world.get_region("Mourning and Havoc", player).entrances:
        set_rule(i, lambda state: state._blasphemous_blood_relic(player) or \
            state.can_reach(world.get_region("Mother of Mothers", player)))
    for i in world.get_region("Patio of the Silent Steps", player).entrances:
        set_rule(i, lambda state: state._blasphemous_3_wounds(player))
    for i in world.get_region("The Resting Place of the Sister", player).entrances:
        set_rule(i, lambda state: state._blasphemous_blood_relic(player))
    for i in world.get_region("The Sleeping Canvases", player).entrances:
        set_rule(i, lambda state: state._blasphemous_3_wounds(player))
    for i in world.get_region("Wall of the Holy Prohibitions", player).entrances:
        set_rule(i, lambda state: state._blasphemous_1_mask(player))

    # Albero
    set_rule(world.get_location("Lake of Silent Pilgrims: Bless cloth", player), 
        lambda state: state._blasphemous_cloth(player))
    set_rule(world.get_location("Lake of Silent Pilgrims: Bless egg", player),
        lambda state: state._blasphemous_egg(player))
    set_rule(world.get_location("Lake of Silent Pilgrims: Bless hand", player),
        lambda state: state._blasphemous_hand(player))
    set_rule(world.get_location("Albero: Cleofas gift initial", player),
        lambda state: state.can_reach(world.get_region("Mother of Mothers", player)))
    set_rule(world.get_location("Albero: Cleofas gift final", player),
        lambda state: state.can_reach(world.get_region("Mother of Mothers", player)))
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
            state.can_reach(world.get_region("Wall of the Holy Prohibitions", player)))
    set_rule(world.get_location("Albero: Tentudia reward 1", player),
        lambda state: state._blasphemous_tentudia_1(player))
    set_rule(world.get_location("Albero: Tentudia reward 2", player),
        lambda state: state._blasphemous_tentudia_2(player))
    set_rule(world.get_location("Albero: Tentudia reward 3", player),
        lambda state: state._blasphemous_tentudia_3(player))
    # to do: ossuary

    # All the Tears of the Sea
    set_rule(world.get_location("AtTotS: Miriam gift", player),
        lambda state: state.can_reach(world.get_region("Archcathedral Rooftops", player)) and \
            state._blasphemous_blood_relic(player) and \
                state._blasphemous_fall_relic(player))

    # Archcathedral Rooftops
    set_rule(world.get_location("AR: Bridge fight 2", player),
        lambda state: state._blasphemous_1_mask(player))
    set_rule(world.get_location("AR: Bridge fight 3", player),
        lambda state: state._blasphemous_2_masks(player))
    set_rule(world.get_location("AR: Western shaft ledge", player),
        lambda state: state._blasphemous_1_mask(player))
    set_rule(world.get_location("AR: Western shaft cherub", player),
        lambda state: state._blasphemous_1_mask(player))
    set_rule(world.get_location("AR: Western shaft chest", player),
        lambda state: state._blasphemous_2_masks(player) and \
            state._blasphemous_fall_relic(player))
    set_rule(world.get_location("AR: Lady room", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_miasma_relic(player) and \
                state._blasphemous_fall_relic(player))
    set_rule(world.get_location("AR: Second checkpoint ledge", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_miasma_relic(player) and \
                state._blasphemous_fall_relic(player) and \
                    state._blasphemous_1_mask(player))
    set_rule(world.get_location("AR: Sword room", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_miasma_relic(player) and \
                state._blasphemous_fall_relic(player) and \
                    state._blasphemous_2_masks(player))
    set_rule(world.get_location("AR: Crisanta", player),
        lambda state: state._blasphemous_3_masks(player))
    
    # Bridge of the Three Cavalries
    set_rule(world.get_location("BotTC: Esdras", player),
        lambda state: state._blasphemous_3_wounds(player))
    set_rule(world.get_location("BotTC: Esdras gift initial", player),
        lambda state: state._blasphemous_3_wounds(player))
    set_rule(world.get_location("BotTC: Amanecida core", player),
        lambda state: state._blasphemous_bell(player) and \
            state.can_reach(world.get_region("Patio of the Silent Steps", player)) and \
                state.can_reach(world.get_region("Wall of the Holy Prohibitions", player)))
    
    # Brotherhood of the Silent Sorrow
    set_rule(world.get_location("BotSS: Initial room cherub", player),
        lambda state: (state._blasphemous_blood_relic(player) and \
            state._blasphemous_root_relic(player)) or \
                (state._blasphemous_blood_relic(player) and \
                    state._blasphemous_fall_relic(player)))
    set_rule(world.get_location("BotSS: Initial room ledge", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_fall_relic(player))
    set_rule(world.get_location("BotSS: Elder Brother's room", player),
        lambda state: state._blasphemous_elder_key(player))
    set_rule(world.get_location("BotSS: Church entrance", player),
        lambda state: state._blasphemous_blood_relic(player))
    set_rule(world.get_location("BotSS: Esdras gift final", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_scapular(player))
    set_rule(world.get_location("BotSS: Crisanta gift", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_scapular(player) and \
                state._blasphemous_heart_c(player) and \
                    state._blasphemous_3_masks(player))
    
    # Convent of our Lady of the Charred Visage
    if world.strict_miasma[player]:
        set_rule(world.get_location("CoOLotCV: Southwest lung room", player),
            lambda state: state._blasphemous_miasma_relic(player))
    set_rule(world.get_location("CoOLotCV: Lady room", player),
        lambda state: state._blasphemous_high_key(player))
    set_rule(world.get_location("CoOLotCV: Mask room", player),
        lambda state: state._blasphemous_high_key(player))

    # Desecrated Cistern
    set_rule(world.get_location("DC: Eastern upper tunnel chest", player),
        lambda state: state._blasphemous_water_relic(player) or \
            state._blasphemous_fall_relic(player))
    set_rule(world.get_location("DC: Eastern upper tunnel cherub", player),
        lambda state: state._blasphemous_water_relic(player) or \
            state._blasphemous_prayers_vertical(player) or \
                state._blasphemous_fall_relic(player))
    set_rule(world.get_location("DC: Hidden hand room", player),
        lambda state: state._blasphemous_water_relic(player))
    set_rule(world.get_location("DC: Shroud puzzle", player),
        lambda state: state._blasphemous_corpse_relic(player))
    set_rule(world.get_location("DC: Chalice room", player),
        lambda state: state._blasphemous_root_relic(player))
    set_rule(world.get_location("DC: Sword room", player),
        lambda state: state._blasphemous_root_relic(player))
    if world.strict_miasma[player]:
        set_rule(world.get_location("DC: Lung tunnel cherub", player),
            lambda state: state._blasphemous_miasma_relic(player))
        set_rule(world.get_location("DC: Lung tunnel ledge", player),
            lambda state: state._blasphemous_miasma_relic(player))
        add_rule(world.get_location("DC: Chalice room", player),
            lambda state: state._blasphemous_miasma_relic(player))
        add_rule(world.get_location("DC: Sword room", player),
            lambda state: state._blasphemous_miasma_relic(player))
    set_rule(world.get_location("DC: Elevator shaft cherub", player),
        lambda state: state._blasphemous_fall_relic(player))
    set_rule(world.get_location("DC: Elevator shaft ledge", player),
        lambda state: state._blasphemous_fall_relic(player))

    # Graveyard of the Peaks
    set_rule(world.get_location("GotP: Shop cave cherub", player),
        lambda state: state._blasphemous_blood_relic(player) or \
            state._blasphemous_fall_relic(player))
    # to do: requires dive
    #set_rule(world.get_location("GotP: Shop cave hole", player),
    #    lambda state: state._blasphemous_(player))
    set_rule(world.get_location("GotP: Eastern shaft upper", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_root_relic(player))
    set_rule(world.get_location("GotP: Amanecida ledge", player),
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_root_relic(player))
    set_rule(world.get_location("GotP: Western shaft cherub", player),
        lambda state: state._blasphemous_blood_relic(player))
    set_rule(world.get_location("GotP: Center shaft cherub", player),
        lambda state: state._blasphemous_fall_relic(player) or \
            state._blasphemous_prayers_vertical(player))
    set_rule(world.get_location("GotP: Bow Amanecida", player),
        lambda state: state._blasphemous_bell(player))

    # Grievance Ascends
    if world.strict_miasma[player]:
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
            state._blasphemous_prayers_vertical(player))
    set_rule(world.get_location("GA: Altasgracias cherub", player),
        lambda state: state._blasphemous_root_relic(player) or \
            state._blasphemous_prayers_vertical(player))
    set_rule(world.get_location("GA: Altasgracias gift", player),
        lambda state: state._blasphemous_egg_3(player))
    set_rule(world.get_location("GA: Altasgracias cocoon", player),
        lambda state: state._blasphemous_egg_3(player))

    # Hall of the Dawning
    set_rule(world.get_location("HotD: Laudes", player),
        lambda state: state._blasphemous_bell(player) and \
            state._blasphemous_1_mask(player))

    # Jondo
    set_rule(world.get_location("Jondo: Eastern entrance chest", player),
        lambda state: state._blasphemous_fall_relic(player) or \
            state._blasphemous_root_relic(player))
    set_rule(world.get_location("Jondo: Western shaft root puzzle", player),
        lambda state: state._blasphemous_root_relic(player))

    # Knot of the Three Words
    # to do: do you actually need the scapular for this??
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
        lambda state: state._blasphemous_blood_relic(player) and \
            state._blasphemous_root_relic(player) and \
                state._blasphemous_prayers_vertical(player))
    set_rule(world.get_location("LotNW: Diosdado gift", player),
        lambda state: state._blasphemous_corpse_relic(player))
    set_rule(world.get_location("LotNW: Fourth Visage hidden wall", player),
        lambda state: state._blasphemous_wood_key(player))

    # Mercy Dreams
    set_rule(world.get_location("MD: Blue candle", player),
        lambda state: state._blasphemous_3_wounds(player))
    set_rule(world.get_location("MD: SlC entrance cherub", player),
        lambda state: state._blasphemous_3_wounds(player))
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
    set_rule(world.get_location("MotED: Axe Amanecida", player),
        lambda state: state._blasphemous_bell(player))
    
    # Mourning and Havoc
    set_rule(world.get_location("MaH: Eastern chest", player),
        lambda state: state._blasphemous_root_relic(player) and \
            state.can_reach(world.get_region("Mother of Mothers", player)))
    set_rule(world.get_location("MaH: Sierpes reward", player),
        lambda state: state.can_reach(world.get_region("Mother of Mothers", player)))
    set_rule(world.get_location("MaH: Sierpes", player),
        lambda state: state.can_reach(world.get_region("Mother of Mothers", player)))

    # Patio of the Silent Steps
    set_rule(world.get_location("PotSS: Garden 2 ledge", player),
        lambda state: state._blasphemous_root_relic(player))
    set_rule(world.get_location("PotSS: Garden 3 upper ledge", player),
        lambda state: state._blasphemous_root_relic(player))
    set_rule(world.get_location("PotSS: Northern shaft", player),
        lambda state: (state._blasphemous_blood_relic(player) and \
            state._blasphemous_root_relic(player)) or \
                state.can_reach(world.get_region("Wall of the Holy Prohibitions", player)))
    set_rule(world.get_location("PotSS: Falcata Amanecida", player),
        lambda state: state._blasphemous_bell(player))
    
    # Petrous
    # to do: requires dive
    #set_rule(world.get_location("Petrous: Entrance room", player),
    #    lambda state: state._blasphemous_(player))

    # The Sleeping Canvases
    set_rule(world.get_location("TSC: Wax bleed puzzle", player),
        lambda state: state._blasphemous_wax(player))
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
        lambda state: state._blasphemous_gold_key(player))
    set_rule(world.get_location("WotHP: Q3 lower gold door", player),
        lambda state: state._blasphemous_gold_key(player))
    set_rule(world.get_location("WotHP: Q3 upper silver door", player),
        lambda state: state._blasphemous_silver_key(player))
    set_rule(world.get_location("WotHP: Q3 upper ledge", player),
        lambda state: state._blasphemous_silver_key(player))
    set_rule(world.get_location("WotHP: Q4 lower silver door", player),
        lambda state: state._blasphemous_silver_key(player))
    set_rule(world.get_location("WotHP: Q4 upper bronze door", player),
        lambda state: state._blasphemous_bronze_key(player))
    set_rule(world.get_location("WotHP: Q4 upper silver door", player),
        lambda state: state._blasphemous_silver_key(player))
    set_rule(world.get_location("WotHP: CoLCV entrance", player),
        lambda state: state._blasphemous_silver_key(player))
    set_rule(world.get_location("WotHP: Oil room", player),
        lambda state: state._blasphemous_silver_key(player))
    set_rule(world.get_location("WotHP: Quirce", player),
        lambda state: state._blasphemous_silver_key(player))
    set_rule(world.get_location("WotHP: Quirce room", player),
        lambda state: state._blasphemous_silver_key(player))
    # to do: does the amanecida need any keys?

    # Wasteland of the Buried Churches
    set_rule(world.get_location("WotBC: Underneath MeD bridge", player),
        lambda state: state._blasphemous_blood_relic(player))
    # to do: requires either a prayer that can hit horizontally or throwing blood
    #set_rule(world.get_location("WotBC: Cliffside cherub", player),
    #    lambda state: state._blasphemous_(player))

    # Where Olive Trees Wither
    set_rule(world.get_location("WOTW: White lady flower", player),
        lambda state: state._blasphemous_thimble(player))
    set_rule(world.get_location("WOTW: White lady tomb", player),
        lambda state: state._blasphemous_flowers(player) and \
            (state._blasphemous_thimble(player) or \
                state._blasphemous_fall_relic(player)))
    set_rule(world.get_location("WOTW: White lady cave cherub", player),
        lambda state: (state._blasphemous_thimble(player) or \
            state._blasphemous_fall_relic(player)) and \
                state._blasphemous_prayers_vertical(player))
    set_rule(world.get_location("WOTW: White lady cave ledge", player),
        lambda state: (state._blasphemous_thimble(player) or \
            state._blasphemous_fall_relic(player)) and \
                state._blasphemous_blood_relic(player))
    set_rule(world.get_location("WOTW: Eastern root cherub", player),
        lambda state: state._blasphemous_root_relic(player) or \
            state._blasphemous_prayers_vertical(player))
    set_rule(world.get_location("WOTW: Eastern root ledge", player),
        lambda state: state._blasphemous_root_relic(player))
    set_rule(world.get_location("WOTW: Gemino gift final", player),
        lambda state: state._blasphemous_thimble(player))

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
            state._blasphemous_3_wounds(player))
    set_rule(world.get_location("Guilt arena 6 main", player),
        lambda state: state._blasphemous_bead(player) and \
            state._blasphemous_3_wounds(player))
    set_rule(world.get_location("Guilt arena 7 extra", player),
        lambda state: state._blasphemous_bead(player) and \
            state._blasphemous_3_wounds(player) and \
                state._blasphemous_1_mask(player))
    set_rule(world.get_location("Guilt arena 7 main", player),
        lambda state: state._blasphemous_bead(player) and \
            state._blasphemous_3_wounds(player) and \
                state._blasphemous_1_mask(player))
    set_rule(world.get_location("Amanecida 1", player),
        lambda state: state._blasphemous_bell(player))
    set_rule(world.get_location("Amanecida 2", player),
        lambda state: state._blasphemous_bell(player))
    set_rule(world.get_location("Amanecida 3", player),
        lambda state: state._blasphemous_bell(player) and \
            state._blasphemous_3_wounds(player))
    set_rule(world.get_location("Amanecida 4", player),
        lambda state: state._blasphemous_bell(player) and \
            state._blasphemous_3_wounds(player) and \
                state._blasphemous_1_mask(player))
    set_rule(world.get_location("All amanecidas reward", player),
        lambda state: state._blasphemous_bell(player) and \
            state._blasphemous_3_wounds(player) and \
                state._blasphemous_1_mask(player))