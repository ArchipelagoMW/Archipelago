from BaseClasses import CollectionState
from worlds._sc2common.bot import player


#region Victory rules
def has_serpulo_victory(state: CollectionState, player: int) -> bool:
    """If the player has archived victory on Serpulo"""
    return state.has("Victory archived on Serpulo", player)

def has_erekir_victory(state: CollectionState, player: int) -> bool:
    """If the player has archived victory on Erekir"""
    return state.has("Victory archived on Erekir", player)

#endregion

#region Serpulo rules
def has_frozen_forest(state: CollectionState, player: int) -> bool:
    """If the player has captured Frozen Forest"""
    return state.has("Frozen Forest captured", player)

def has_the_craters(state: CollectionState, player: int) -> bool:
    """If the player has captured The Craters"""
    return state.has("The Craters captured", player) and has_frozen_forest(state, player)

def has_ruinous_shores(state: CollectionState, player: int) -> bool:
    """If the player has captured Ruinous Shores"""
    return state.has("Ruinous Shores captured", player) and has_the_craters(state, player)

def has_windswept_islands(state: CollectionState, player: int) -> bool:
    """If the player has captured Windswept Islands"""
    return state.has("Windswept Islands captured", player) and has_ruinous_shores(state, player)

def has_tar_fields(state: CollectionState, player: int) -> bool:
    """If the player has captured Tar Fields"""
    return state.has("Tar Fields captured", player) and has_windswept_islands(state, player)

def has_impact_0078(state: CollectionState, player: int) -> bool:
    """If the player has captured Impact 0078"""
    return state.has("Impact 0078 captured", player) and has_tar_fields(state, player)

def has_desolate_rift(state: CollectionState, player: int) -> bool:
    """If the player has captured Desolate Rift"""
    return state.has("Desolate Rift captured", player) and has_impact_0078(state, player)

def has_planetary_launch_terminal(state: CollectionState, player: int) -> bool:
    """If the player has captured Planetary Launch Terminal"""
    return state.has("Planetary Launch Terminal captured", player) and has_desolate_rift(state, player)

def has_extraction_outpost(state: CollectionState, player: int) -> bool:
    """If the player has captured Extraction Outpost"""
    return state.has("Extraction Outpost captured", player) and has_windswept_islands(state, player)

def has_salt_flats(state: CollectionState, player: int) -> bool:
    """If the player has captured Salt Flats"""
    return state.has("Salt Flats captured", player) and has_windswept_islands(state, player)

def has_coastline(state: CollectionState, player: int) -> bool:
    """If the player has captured Coastline"""
    return state.has("Coastline captured", player) and has_salt_flats(state, player)

def has_naval_fortress(state: CollectionState, player: int) -> bool:
    """If the player has captured Naval Fortress"""
    return state.has("Naval Fortress captured", player) and has_coastline(state, player)

def has_overgrowth(state: CollectionState, player: int) -> bool:
    """If the player has captured Overgrowth"""
    return state.has("Overgrowth captured", player) and has_the_craters(state, player)

def has_biomass_synthesis_facility(state: CollectionState, player: int) -> bool:
    """If the player has captured Biomass Synthesis Facility"""
    return state.has("Biomass Synthesis Facility captured", player) and has_frozen_forest(state, player)

def has_stained_mountains(state: CollectionState, player: int) -> bool:
    """If the player has captured Stained Mountains"""
    return state.has("Stained Mountains captured", player) and has_biomass_synthesis_facility(state, player)

def has_fungal_pass(state: CollectionState, player: int) -> bool:
    """If the player has captured Fungal Pass"""
    return state.has("Fungal Pass captured", player) and has_stained_mountains(state, player)

def has_nuclear_production_complex(state: CollectionState, player: int) -> bool:
    """If the player has captured Nuclear Production Complex"""
    return state.has("Nuclear Production Complex captured", player) and has_fungal_pass(state, player)

def has_titanium(state: CollectionState, player: int) -> bool:
    """If the player has produced Titanium on Serpulo"""
    return state.has("Titanium produced on Serpulo", player) and has_pneumatic_drill(state, player)

def has_cryofluid(state: CollectionState, player: int) -> bool:
    """If the player has produced Cryofluid on Serpulo"""
    available: bool = False
    if state.has("Cryofluid produced on Serpulo", player) and has_power_serpulo(state, player) and has_cryofluid_mixer(state, player):
        available = True
    return available

def has_thorium_serpulo(state: CollectionState, player: int) -> bool:
    """If the player has produced Thorium on Serpulo"""
    available: bool = False
    if (state.has("Thorium produced on Serpulo", player) and has_power_serpulo(state, player) and
            has_laser_drill(state, player) and has_windswept_islands(state, player)):
        available = True
    return available

def has_surge_alloy_serpulo(state: CollectionState, player: int) -> bool:
    """If the player has produced Surge Alloy on Serpulo"""
    available: bool = False
    if state.has("Surge Alloy produced on Serpulo", player) and has_power_serpulo(state, player) and has_surge_smelter(state, player):
        available = True
    return available

def has_phase_fabric_serpulo(state: CollectionState, player: int) -> bool:
    """If the player has produced Phase Fabric on Serpulo"""
    available: bool = False
    if state.has("Phase Fabric produced on Serpulo", player) and has_power_serpulo(state, player) and has_phase_weaver(state, player):
        available = True
    return available

def has_metaglass(state: CollectionState, player: int) -> bool:
    """If the player has produced Metaglass on Serpulo"""
    available: bool = False
    if state.has("Metaglass produced on Serpulo", player) and has_power_serpulo(state, player) and has_kiln(state, player):
        available = True
    return available

def has_melter(state: CollectionState, player: int) -> bool:
    """If the player has and can use the melter"""
    return state.has("Melter", player) and has_power_serpulo(state, player) and has_graphite_serpulo(state, player)

def has_graphite_serpulo(state: CollectionState, player: int) -> bool:
    """If the player has produced Graphite on Serpulo"""
    available: bool = False
    if state.has("Graphite produced on Serpulo", player) and has_graphite_press(state, player):
        available = True
    return available

def has_silicon_serpulo(state: CollectionState, player: int) -> bool:
    """If the player has produced Silicon on Serpulo"""
    available: bool = False
    if state.has("Silicon produced on Serpulo", player) and has_power_serpulo(state, player) and has_silicon_smelter(state, player):
        available = True
    return available

def has_pyratite(state: CollectionState, player: int) -> bool:
    """If the player has produced Pyratite on Serpulo"""
    available: bool = False
    if state.has("Pyratite produced on Serpulo", player) and has_power_serpulo(state, player) and has_pyratite_mixer(state, player):
        available = True
    return available

def has_blast_compound(state: CollectionState, player: int) -> bool:
    """If the player has produced Blast Compound on Serpulo"""
    available: bool = False
    if state.has("Blast Compound produced on Serpulo", player) and has_power_serpulo(state, player) and has_blast_mixer(state, player) and has_pyratite(state, player) and has_spore_pod(state, player):
        available = True
    return available

def has_spore_pod(state: CollectionState, player: int) -> bool:
    """If the player has produced Spore Pod on Serpulo"""
    available: bool = False
    if state.has("Spore Pod produced on Serpulo", player) and has_power_serpulo(state, player) and has_cultivator(state, player):
        available = True
    return available

def has_oil(state: CollectionState, player: int) -> bool:
    """If the player has produced Oil on Serpulo"""
    available: bool = False
    if state.has("Oil produced on Serpulo", player) and has_mechanical_pump(state, player):
        available = True
    return available

def has_slag_serpulo(state: CollectionState, player: int) -> bool:
    """If the player has produced Slag on Serpulo"""
    return state.has("Slag produced on Serpulo", player) and has_melter(state, player) and has_mechanical_pump(state, player)

def has_plastanium(state: CollectionState, player: int) -> bool:
    """If the player has produced Plastanium on Serpulo"""
    available: bool = False
    if state.has("Plastanium produced on Serpulo", player) and has_power_serpulo(state, player) and has_plastanium_compressor(state, player) and has_oil(state, player):
        available = True
    return available

def has_power_serpulo(state: CollectionState, player: int) -> bool:
    """If the player has acces to electricity on Serpulo"""
    return state.has("Combustion Generator", player) or state.has("Progressive Generators Serpulo", player, 1)

def has_mechanical_pump(state: CollectionState, player: int) -> bool:
    """If the player has received Mechanical Pump"""
    available: bool = False
    if state.has_all(["Mechanical Pump", "Conduit"], player) and has_metaglass(state, player):
        available = True
    return available

def has_graphite_press(state: CollectionState, player: int) -> bool:
    """If the player has received Graphite Press"""
    return state.has("Graphite Press", player)

def has_pneumatic_drill(state: CollectionState, player: int) -> bool:
    """If the player has received Pneumatic Drill"""
    available: bool = False
    if ((state.has("Pneumatic Drill", player) or state.has("Progressive Drills Serpulo", player, 1)) and
            has_graphite_serpulo(state, player)):
        available = True
    return available

def has_cultivator(state: CollectionState, player: int) -> bool:
    """If the player has received Cultivator"""
    available: bool = False
    if state.has("Cultivator", player) and has_silicon_serpulo(state, player) and has_mechanical_pump(state, player):
        available = True
    return available

def has_laser_drill(state: CollectionState, player: int) -> bool:
    """If the player received Laser Drill"""
    available: bool = False
    if (state.has("Laser Drill", player) or state.has("Progressive Drills Serpulo", player, 2)) and has_graphite_serpulo(state, player) and has_silicon_serpulo(state, player) and has_titanium(state, player):
        available = True
    return available

def has_pyratite_mixer(state: CollectionState, player: int) -> bool:
    """If the player received Pyratite Mixer"""
    return state.has("Pyratite Mixer", player)

def has_blast_mixer(state: CollectionState, player: int) -> bool:
    """If the player received Blast Mixer"""
    available: bool = False
    if state.has("Blast Mixer", player) and has_titanium(state, player):
        available = True
    return available

def has_silicon_smelter(state: CollectionState, player: int) -> bool:
    """If the player received Silicon Smelter"""
    return state.has("Silicon Smelter", player) and has_power_serpulo(state, player)

def has_plastanium_compressor(state: CollectionState, player: int) -> bool:
    """If the player received Plastanium Compressor"""
    available: bool = False
    if state.has("Plastanium Compressor", player) and has_silicon_serpulo(state, player) and has_graphite_serpulo(state, player) and has_titanium(state, player):
        available = True
    return available

def has_phase_weaver(state: CollectionState, player: int) -> bool:
    """If the player received Phase Weaver"""
    available: bool = False
    if state.has("Phase Weaver", player) and has_silicon_serpulo(state, player) and has_thorium_serpulo(state, player):
        available = True
    return available

def has_kiln(state: CollectionState, player: int) -> bool:
    """If the player received Kiln"""
    available: bool = False
    if state.has("Kiln", player) and has_graphite_serpulo(state, player):
        available = True
    return available

def has_surge_smelter(state: CollectionState, player: int) -> bool:
    """If the player received Surge Smelter"""
    available: bool = False
    if state.has("Surge Smelter", player) and has_silicon_serpulo(state, player) and has_thorium_serpulo(state, player):
        available = True
    return available

def has_cryofluid_mixer(state: CollectionState, player: int) -> bool:
    """If the player received Cryofluid Mixer"""
    available: bool = False
    if state.has("Cryofluid Mixer", player) and has_titanium(state, player) and has_silicon_serpulo(state, player):
        available = True
    return available

def has_ground_factory(state: CollectionState, player:int) -> bool:
    """If the player received Ground Factory"""
    available: bool = False
    if state.has("Ground Factory", player) and has_silicon_serpulo(state, player):
        available = True
    return available

def has_air_factory(state: CollectionState, player:int) -> bool:
    """If the player received Air Factory"""
    return state.has("Air Factory", player)

def has_naval_factory(state: CollectionState, player:int) -> bool:
    """If the player received Naval Factory"""
    available: bool = False
    if state.has("Naval Factory", player) and has_metaglass(state, player):
        available = True
    return available

@DeprecationWarning
def has_early_logistics_serpulo(state: CollectionState, player:int) -> bool:
    """Rules for early logistics options on Serpulo"""
    return state.has_all({"Conduit", "Liquid Junction", "Liquid Router", "Bridge Conduit", "Junction", "Router", "Bridge Conveyor", "Power Node"}, player)

def can_produce_naval_unit(state: CollectionState, player:int) -> bool:
    """If the player can produce naval units"""
    return state.has_any({"Progressive Offensive Naval Unit","Progressive Support Naval Unit"}, player)

def can_produce_ground_unit(state: CollectionState, player:int) -> bool:
    """If the player can produce ground units"""
    return state.has_any({"Progressive Offensive Ground Unit","Progressive Support Ground Unit", "Progressive Insectoid Ground Unit"}, player)

def get_military_score_serpulo(state: CollectionState, player:int) -> int:
    """Return the military score of the player based on their available research"""
    score = 0
    if state.has("Hail", player) and has_hail_requirements(state, player):
        score += 1
    if state.has("Arc", player) and has_arc_requirements(state, player):
        score += 1
    if state.has("Scorch", player) and has_scorch_requirements(state, player):
        score += 1
    if state.has("Parallax", player) and has_parallax_requirements(state, player):
        score += 1 #Parallax is bad so the score is 1 :^)
    if state.has("Wave", player) and has_wave_requirements(state, player):
        score += 1
    if state.has("Lancer", player) and has_lancer_requirements(state, player):
        score += 3
    if state.has("Salvo", player) and has_salvo_requirements(state, player):
        score += 3
    if state.has("Swarmer", player) and has_swarmer_requirements(state, player):
        score += 5
    if state.has("Ripple", player) and has_ripple_requirements(state, player):
        score += 4
    if state.has("Tsunami", player) and has_tsunami_requirements(state, player):
        score += 4
    if state.has("Fuse", player) and has_fuse_requirements(state, player):
        score += 4
    if state.has("Meltdown", player) and has_meltdown_requirements(state, player):
        score += 10
    if state.has("Foreshadow", player) and has_foreshadow_requirements(state, player):
        score += 10
    if state.has("Cyclone", player) and has_cyclone_requirements(state, player):
        score += 4
    if state.has("Spectre", player) and has_spectre_requirements(state, player):
        score += 10
    if state.has("Segment", player) and has_segment_requirements(state, player):
        score += 10

    if state.has("Mender", player) and has_power_serpulo(state, player):
        score += 2
    if state.has("Mend Projector", player) and has_mend_projector_requirements(state, player):
        score += 3
    if state.has("Shock Mine", player) and has_silicon_serpulo(state, player):
        score += 2
    return score

def has_segment_requirements(state: CollectionState, player:int) -> bool:
    """If the player has requirement to place and fire the Segment turret."""
    can_place = has_titanium(state, player) and has_thorium_serpulo(state, player) and has_silicon_serpulo(state, player) and has_phase_fabric_serpulo(state, player)
    can_fire = has_power_serpulo(state, player)
    return can_place and can_fire

def has_cyclone_requirements(state: CollectionState, player:int) -> bool:
    """If the player has requirement to place and fire the Cyclone turret."""
    can_place = has_titanium(state, player) and has_plastanium(state, player)
    can_fire = has_metaglass(state, player) or has_plastanium(state, player) or has_surge_alloy_serpulo(state, player) or has_blast_compound(state, player)
    return can_place and can_fire

def has_spectre_requirements(state: CollectionState, player:int) -> bool:
    """If the player has requirement to place and fire the Spectre turret."""
    can_place = has_graphite_serpulo(state, player) and has_thorium_serpulo(state, player) and has_plastanium(state, player) and has_surge_alloy_serpulo(state, player)
    can_fire = has_thorium_serpulo(state, player) or has_pyratite(state, player)
    return can_place and can_fire

def has_foreshadow_requirements(state: CollectionState, player:int) -> bool:
    """If the player has requirement to place and fire the Foreshadow turret."""
    can_place = has_metaglass(state, player) and has_silicon_serpulo(state, player) and has_plastanium(state, player) and has_surge_alloy_serpulo(state, player)
    can_fire = has_surge_alloy_serpulo(state, player)
    return can_place and can_fire

def has_meltdown_requirements(state: CollectionState, player:int) -> bool:
    """If the player has requirement to place and fire the Meltdown turret."""
    can_place = has_graphite_serpulo(state, player) and has_silicon_serpulo(state, player) and has_surge_alloy_serpulo(state, player)
    can_fire = has_mechanical_pump(state, player) # Req fluids
    return can_place and can_fire

def has_scorch_requirements(state: CollectionState, player:int) -> bool:
    """If the player has requirement to place and fire the Scorch turret."""
    can_place = has_graphite_serpulo(state, player)
    can_fire = True # Req coal = no requirement for logic
    return can_place and can_fire

def has_wave_requirements(state: CollectionState, player:int) -> bool:
    """If the player has requirement to place and fire the Wave turret."""
    can_place = has_metaglass(state, player)
    can_fire = has_mechanical_pump(state, player)
    return can_place and can_fire

def has_parallax_requirements(state: CollectionState, player:int) -> bool:
    """If the player has requirement to place and fire the Parallax turret."""
    can_place = has_titanium(state, player) and has_silicon_serpulo(state, player)
    can_fire = has_power_serpulo(state, player)
    return can_place and can_fire

def has_hail_requirements(state: CollectionState, player:int) -> bool:
    """If the player has requirement to place and fire the Hail turret."""
    can_place = has_graphite_serpulo(state, player)
    can_fire = has_graphite_serpulo(state, player) or has_silicon_serpulo(state, player) or has_pyratite(state, player)
    return can_place and can_fire

def has_arc_requirements(state: CollectionState, player:int) -> bool:
    """If the player has requirement to place and fire the Arc turret."""
    can_place = True #No special requirements
    can_fire = has_power_serpulo(state, player)
    return can_place and can_fire

def has_lancer_requirements(state: CollectionState, player:int) -> bool:
    """If the player has requirement to place and fire the Lancer turret."""
    can_place = has_titanium(state, player) and has_silicon_serpulo(state, player)
    can_fire = has_power_serpulo(state, player)
    return can_place and can_fire

def has_salvo_requirements(state: CollectionState, player:int) -> bool:
    """If the player has requirement to place and fire the Salvo turret."""
    can_place = has_titanium(state, player) and has_graphite_serpulo(state, player)
    can_fire = has_graphite_serpulo(state, player) or has_pyratite(state, player) or has_silicon_serpulo(state, player) or has_thorium_serpulo(state, player)
    return can_place and can_fire

def has_swarmer_requirements(state: CollectionState, player:int) -> bool:
    """If the player has requirement to place and fire the Swarmer turret."""
    can_place = has_graphite_serpulo(state, player) and has_titanium(state, player) and has_silicon_serpulo(state, player) and has_plastanium(state, player)
    can_fire = has_pyratite(state, player) or has_blast_compound(state, player) or has_surge_alloy_serpulo(state, player)
    return can_place and can_fire

def has_ripple_requirements(state: CollectionState, player:int) -> bool:
    """If the player has requirement to place and fire the Ripple turret."""
    can_place = has_graphite_serpulo(state, player) and has_titanium(state, player)
    can_fire = has_graphite_serpulo(state, player) or has_silicon_serpulo(state, player) or has_plastanium(state, player) or has_blast_compound(state, player or has_pyratite(state, player))
    return can_place and can_fire

def has_tsunami_requirements(state: CollectionState, player:int) -> bool:
    """If the player has requirement to place and fire the Tsunami turret."""
    can_place = has_metaglass(state, player) and has_titanium(state, player) and has_thorium_serpulo(state, player)
    can_fire = has_mechanical_pump(state, player)
    return can_place and can_fire

def has_fuse_requirements(state: CollectionState, player:int) -> bool:
    """If the player has requirement to place and fire the Fuse turret."""
    can_place = has_graphite_serpulo(state, player) and has_thorium_serpulo(state, player)
    can_fire = has_thorium_serpulo(state, player) or has_thorium_serpulo(state, player)
    return can_place and can_fire

def has_mend_projector_requirements(state: CollectionState, player:int) -> bool:
    """If the player has requirement to place and use the Mender."""
    can_place = has_titanium(state, player) and has_silicon_serpulo(state, player)
    can_use = has_power_serpulo(state, player)
    return can_place and can_use

#endregion

#region Erekir rules
def has_aegis_requirements(state: CollectionState, player:int) -> bool:
    """If the player has received the research required to clear Aegis"""
    return has_impact_drill(state, player)

def has_aegis(state: CollectionState, player:int) -> bool:
    """If the player has captured Aegis"""
    return state.has("Aegis captured", player)

def has_lake_requirements(state: CollectionState, player:int) -> bool:
    """If the player has received the research required to clear Lake"""
    return state.has("Ship Fabricator", player) and state.has_any_count({"Progressive Ships": 1}, player)

def has_lake(state: CollectionState, player:int) -> bool:
    """If the player captured Lake"""
    return state.has("Lake captured", player) and has_aegis(state, player) and has_lake_requirements(state, player)

def has_intersect_requirements(state: CollectionState, player:int) -> bool:
    """If the player has received the research required to clear Intersect"""
    return state.has("Mech Fabricator", player) and state.has_any_count({"Progressive Mechs": 1}, player)

def has_intersect(state: CollectionState, player:int) -> bool:
    """If the player captured Intersect"""
    return state.has("Intersect captured", player) and has_lake(state, player) and has_intersect_requirements(state, player)

def has_atlas(state: CollectionState, player:int) -> bool:
    """If the player captured Atlas"""
    return state.has("Atlas captured", player) and has_intersect(state, player)

def has_split_requirements(state: CollectionState, player:int) -> bool:
    """If the player has received the research required to clear Split"""
    return state.has("Payload Mass Driver", player)

def has_split(state: CollectionState, player:int) -> bool:
    """If the player captured Split"""
    return state.has("Split captured", player) and has_atlas(state, player) and has_split_requirements(state, player)

def has_basin(state: CollectionState, player:int) -> bool:
    """If the player captured Basin"""
    return state.has("Basin captured", player) and has_atlas(state, player)

def has_marsh_requirement(state: CollectionState, player:int) -> bool:
    """If the player has received the research required to clear Marsh"""
    return (state.has_all({"Oxidation Chamber", "Reinforced Pump"}, player) and
            (state.has("Chemical Combustion Chamber", player) or state.has("Progressive Generators Erekir", player, 1)))

def has_marsh(state: CollectionState, player:int) -> bool:
    """If the player captured Marsh"""
    return state.has("Marsh captured", player) and has_basin(state, player) and has_marsh_requirement(state, player)

def has_ravine(state: CollectionState, player:int) -> bool:
    """If the player captured Ravine"""
    return state.has("Ravine captured", player) and has_marsh(state, player)

def has_caldera_launch(state: CollectionState, player:int) -> bool:
    """If the player is able to launch to caldera"""
    return has_ravine(state, player) and has_peaks(state, player)

def has_caldera_requirement(state: CollectionState, player:int) -> bool:
    """If the player has received the research required to clear Caldera"""
    return has_surge_alloy_erekir(state, player)

def has_caldera(state: CollectionState, player:int) -> bool:
    """If the player captured Caldera"""
    return state.has("Caldera captured", player) and has_ravine(state, player) and has_peaks(state, player) and has_caldera_requirement(state, player)

def has_stronghold(state: CollectionState, player:int) -> bool:
    """If the player captured Stronghold"""
    return state.has("Stronghold captured", player) and has_caldera(state, player)

def has_crevice(state: CollectionState, player:int) -> bool:
    """If the player captured Crevice"""
    return state.has("Crevice captured", player) and has_stronghold(state, player)

def has_siege(state: CollectionState, player:int) -> bool:
    """If the player captured Siege"""
    return state.has("Siege captured", player) and has_crevice(state, player)

def has_crossroads(state: CollectionState, player:int) -> bool:
    """If the player captured Crossroads"""
    return state.has("Crossroads captured", player) and has_siege(state, player)

def has_karst(state: CollectionState, player:int) -> bool:
    """If the player captured Karst"""
    return state.has("Karst captured", player) and has_crossroads(state, player)

def has_origin(state: CollectionState, player:int) -> bool:
    """If the player captured Origin"""
    return state.has("Origin captured", player) and has_karst(state, player)

def has_peaks_launch(state: CollectionState, player:int) -> bool:
    """If the player is able to launch to Peaks"""
    return has_marsh(state, player) and has_split(state, player)

def has_peaks_requirement(state: CollectionState, player:int) -> bool:
    """If the player has received the research required to clear Peaks"""
    return (state.has_all({"Beam Tower", "Ship Refabricator", "Reinforced Container",
                           "Payload Loader", "Payload Unloader"}, player) and
            state.has_any_count({"Progressive Ships": 2}, player) and
            (state.has("Chemical Combustion Chamber", player) or state.has("Progressive Generators Erekir", player, 1)))

def has_peaks(state: CollectionState, player:int) -> bool:
    """If the player captured Peaks"""
    return state.has("Peaks captured", player) and has_marsh(state, player) and has_split(state, player) and has_peaks_requirement(state, player)

def has_oxide(state: CollectionState, player:int) -> bool:
    """If the player has produced Oxide on Erekir"""
    return state.has("Oxide produced on Erekir", player) and has_oxidation_chamber(state, player) and has_ozone(state, player)

def has_ozone(state: CollectionState, player:int) -> bool:
    """If the player has produced Ozone on Erekir"""
    return state.has("Ozone produced on Erekir", player) and has_electrolyzer(state, player)

def has_hydrogen(state: CollectionState, player:int) -> bool:
    """If the player has produced Hydrogen on Erekir"""
    return state.has("Hydrogen produced on Erekir", player) and has_electrolyzer(state, player)

def has_nitrogen(state: CollectionState, player:int) -> bool:
    """If the player has produced Nitrogen on Erekir"""
    return state.has("Nitrogen produced on Erekir", player) and has_atmospheric_concentrator(state, player) and has_heat(state, player)

def has_cyanogen(state: CollectionState, player:int) -> bool:
    """If the player has produced Cyanogen on Erekir"""
    return state.has("Cyanogen produced on Erekir", player) and has_cyanogen_synthesizer(state, player) and has_arkycite(state, player) and has_heat(state, player)

def has_neoplasm(state: CollectionState, player:int) -> bool:
    """If the player has produced Neoplasm"""
    return state.has("Neoplasm produced", player) and has_neoplasia_reactor(state, player) and has_arkycite(state, player)

def has_tungsten(state: CollectionState, player:int) -> bool:
    """If the player has produced Tungsten on Erekir"""
    return state.has("Tungsten produced on Erekir", player) and has_impact_drill(state, player)

def has_arkycite(state: CollectionState, player:int) -> bool:
    """If the player has produced Arkycite on Erekir"""
    return state.has("Arkycite produced on Erekir", player) and has_reinforced_pump(state, player)

def has_thorium_erekir(state: CollectionState, player:int) -> bool:
    """If the player has produced Thorium on Erekir"""
    return state.has("Thorium produced on Erekir", player) and has_large_plasma_bore(state, player)
def has_carbide(state: CollectionState, player:int) -> bool:
    """If the player has produced Carbide on Erekir"""
    return state.has("Carbide produced on Erekir", player) and has_carbide_crucible(state, player) and has_heat(state, player)

def has_surge_alloy_erekir(state: CollectionState, player:int) -> bool:
    """If the player has produced Surge Alloy on Erekir"""
    return (state.has("Surge Alloy produced on Erekir", player) and has_surge_crucible(state, player) and has_heat(state, player) and
            has_reinforced_pump(state, player) and has_intersect_requirements(state, player))

def has_phase_fabric_erekir(state: CollectionState, player:int) -> bool:
    """If the player has produced Phase Fabric on Erekir"""
    return state.has("Phase Fabric produced on Erekir", player) and has_phase_synthesizer(state, player) and has_heat(state, player)

def has_slag_erekir(state: CollectionState, player:int) -> bool:
    """If the player has produced Slag on Erekir"""
    return state.has("Slag produced on Erekir", player) and has_reinforced_pump(state, player)

def has_heat(state: CollectionState, player:int) -> bool:
    """If the player has access to heat"""
    return has_oxidation_chamber(state, player)

def has_high_heat(state: CollectionState, player:int) -> bool:
    """If the player has acces to higher heat"""
    return ((state.has_all({"Electric Heater", "Slag Heater", "Phase Heater", "Heat Redirector", "Heat Router"}, player) and has_tungsten(state, player) and has_oxide(state, player) and has_carbide(state, player) and has_phase_fabric_erekir(state, player)) or (
            state.has_all({"Neoplasia Reactor", "Heat Redirector", "Heat Router"}, player) and has_tungsten(state, player) and has_oxide(state, player) and has_carbide(state, player) and has_surge_alloy_erekir(state, player) and has_phase_fabric_erekir(state, player) and has_arkycite(state, player)))

def has_electrolyzer(state: CollectionState, player:int) -> bool:
    """If the player received Electrolyzer"""
    return state.has("Electrolyzer", player) and has_tungsten(state, player)

def has_oxidation_chamber(state: CollectionState, player:int) -> bool:
    """If the player received Oxidation Chamber"""
    return state.has("Oxidation Chamber", player) and has_tungsten(state, player)

def has_surge_crucible(state: CollectionState, player:int) -> bool:
    """If the player received Surge Crucible"""
    return state.has("Surge Crucible", player) and has_tungsten(state, player) and has_oxide(state, player)

def has_reinforced_pump(state: CollectionState, player:int) -> bool:
    """If the player received Reinforced Pump"""
    return state.has_all({"Reinforced Pump", "Reinforced Conduit"}, player) and has_tungsten(state, player) and has_hydrogen(state, player)

def has_atmospheric_concentrator(state: CollectionState, player:int) -> bool:
    """If the player received Atmospheric Concentrator"""
    return state.has("Atmospheric Concentrator", player) and has_carbide(state, player)

def has_cyanogen_synthesizer(state: CollectionState, player:int) -> bool:
    """If the player received Cyanogen Synthesizer"""
    return state.has("Cyanogen Synthesizer", player) and has_carbide(state, player)

def has_carbide_crucible(state: CollectionState, player:int) -> bool:
    """If the player received Carbide Crucible"""
    return (state.has("Carbide Crucible", player) and has_thorium_erekir(state, player) and
            has_tungsten(state, player) and has_oxide(state, player))

def has_phase_synthesizer(state: CollectionState, player:int) -> bool:
    """If the player received Phase Synthesizer"""
    return (state.has("Phase Synthesizer", player) and has_thorium_erekir(state, player)
            and has_tungsten(state, player) and has_carbide(state, player))

def has_neoplasia_reactor(state: CollectionState, player:int) -> bool:
    """If the player received Neoplasia Reactor"""
    return (state.has("Neoplasia Reactor", player) and has_tungsten(state, player)
            and has_phase_fabric_erekir(state, player) and has_surge_alloy_erekir(state, player) and
            has_oxide(state, player) and has_carbide(state, player))

def has_impact_drill(state: CollectionState, player:int) -> bool:
    """If the player received Impact Drill"""
    return (state.has("Impact Drill", player) or state.has("Progressive Drills Erekir", player, 1)) and state.has("Reinforced Conduit", player)

def has_large_plasma_bore(state: CollectionState, player:int) -> bool:
    """If the player received Large Plasma Bore"""
    return (state.has("Large Plasma Bore", player) or state.has("Progressive Drills Erekir", player, 2)) and has_oxide(state, player) and has_tungsten(state, player)

@DeprecationWarning
def has_early_logistics_erekir(state: CollectionState, player:int) -> bool:
    """Rules for early logistics options on Erekir"""
    return state.has_all({"Duct Router", "Duct Bridge", "Reinforced Conduit", "Reinforced Liquid Junction", "Reinforced Bridge Conduit", "Reinforced Liquid Router"}, player)

def _has_erekir_t3_unit_requirements(state: CollectionState, player:int) -> bool:
    has_base_t3_requirements = False
    if state.has("Prime Refabricator", player) and has_tungsten(state, player) and has_oxide(
            state, player) and has_thorium_erekir(state, player) and has_nitrogen(state, player):
        has_base_t3_requirements = True
    return has_base_t3_requirements

def _has_mech_assembler_requirements(state: CollectionState, player:int) -> bool:
    has_mech_assembler_requirements = False
    if state.has("Mech Assembler", player) and has_tungsten(state, player) and has_oxide(state, player) and has_carbide(state, player) and has_thorium_erekir(state, player) and has_cyanogen(state, player):
        has_mech_assembler_requirements = True
    return has_mech_assembler_requirements

def _has_ship_assembler_requirements(state: CollectionState, player:int) -> bool:
    has_ship_assembler_requirements = False
    if state.has("Ship Assembler", player) and has_tungsten(state, player) and has_oxide(state, player) and has_carbide(state, player) and has_thorium_erekir(state, player) and has_cyanogen(state, player):
        has_ship_assembler_requirements = True
    return has_ship_assembler_requirements

def _has_tank_assembler_requirements(state: CollectionState, player:int) -> bool:
    has_tank_assembler_requirements = False
    if state.has("Tank Assembler", player) and has_oxide(state, player) and has_thorium_erekir(state, player) and has_carbide(state, player) and has_cyanogen(state, player):
        has_tank_assembler_requirements = True
    return has_tank_assembler_requirements

def _has_basic_assembler_module_requirements(state: CollectionState, player:int) -> bool:
    has_basic_assembler_module_requirements = False
    if state.has("Basic Assembler Module", player) and has_oxide(state, player) and has_thorium_erekir(state, player) and has_carbide(state, player) and has_phase_fabric_erekir(state, player):
        has_basic_assembler_module_requirements = True
    return has_basic_assembler_module_requirements

def _has_elude_requirements(state: CollectionState, player:int) -> bool:
    can_use_elude = False
    if state.has("Ship Fabricator", player) and state.has_any_count({"Progressive Ships": 1}, player):
        can_use_elude = True
    return can_use_elude


def _has_avert_requirements(state, player) -> bool:
    can_use_avert = False
    if state.has("Ship Refabricator", player) and state.has_all_counts({"Progressive Ships": 2}, player) and _has_elude_requirements(
            state, player) and has_tungsten(state, player) and has_hydrogen(state, player) and has_oxide(state, player):
        can_use_avert = True
    return can_use_avert


def _has_obviate_requirements(state, player) -> bool:
    can_use_obviate = False
    if _has_erekir_t3_unit_requirements(state, player) and state.has_all_counts({"Progressive Ships": 3}, player) and _has_avert_requirements(state, player):
        can_use_obviate = True
    return can_use_obviate


def _has_quell_requirements(state, player) -> bool:
    can_use_quell = False
    if _has_ship_assembler_requirements(state, player) and state.has_all({"Large Beryllium Wall", "Constructor"}, player) and state.has_all_counts(
            {"Progressive Ships": 4}, player) and _has_elude_requirements(state, player):
        can_use_quell = True
    return can_use_quell


def _has_disrupt_requiremts(state, player):
    can_use_disrupt = False
    if _has_basic_assembler_module_requirements(state, player) and _has_ship_assembler_requirements(state, player) and state.has_all(
            {"Large Carbide Wall", "Constructor"}, player) and _has_avert_requirements(state, player) and state.has_all_counts({"Progressive Ships": 5}, player):
        can_use_disrupt = True
    return can_use_disrupt


def _has_merui_requirements(state, player) -> bool:
    can_use_merui = False
    if state.has("Mech Fabricator", player) and state.has_any_count({"Progressive Mechs": 1}, player) and has_tungsten(state, player):
        can_use_merui = True
    return can_use_merui


def _has_cleroi_requirements(state, player):
    can_use_cleroi = False
    if state.has("Mech Refrabricator", player) and _has_merui_requirements(state, player) and state.has_all_counts(
            {"Progressive Mechs": 2}, player) and has_tungsten(state, player) and has_hydrogen(state, player):
        can_use_cleroi = True
    return can_use_cleroi


def _has_anthicus_requirements(state, player):
    can_use_anthicus = False
    if _has_erekir_t3_unit_requirements(state, player) and state.has_all_counts({"Progressive Mechs": 3}, player) and _has_cleroi_requirements(state, player):
        can_use_anthicus = True
    return can_use_anthicus


def _has_tecta_requirements(state, player):
    can_use_tecta = False
    if _has_mech_assembler_requirements(state, player) and state.has_all_counts({"Progressive Mechs": 4}, player) and state.has_all(
            {"Large Tungsten Wall", "Constructor"}, player) and _has_merui_requirements(state, player):
        can_use_tecta = True
    return can_use_tecta


def _has_collaris_requirements(state, player):
    can_use_collaris = False
    if _has_mech_assembler_requirements(state, player) and _has_basic_assembler_module_requirements(state, player) and state.has_all_counts(
            {"Progressive Mechs": 5}, player) and state.has_all({"Large Carbide Wall", "Constructor"}, player) and _has_cleroi_requirements(state, player):
        can_use_collaris = True
    return can_use_collaris


def _has_locus_requirements(state, player):
    can_use_locus = False
    if state.has("Tank Refabricator", player) and state.has_all_counts({"Progressive Tanks": 1}, player) and has_tungsten(state, player) and has_hydrogen(state, player):
        can_use_locus = True
    return can_use_locus


def _has_precept_requirements(state, player):
    can_use_precept = False
    if _has_erekir_t3_unit_requirements(state, player) and _has_locus_requirements(state, player) and state.has_all_counts({"Progressive Tanks": 2}, player):
        can_use_precept = True
    return can_use_precept


def _has_vanquish_requirements(state, player):
    can_use_vanquish = False
    if _has_tank_assembler_requirements(state, player) and state.has_all_counts({"Progressive Tanks": 3}, player) and state.has_all(
            {"Large Tungsten Wall", "Constructor"}, player):
        can_use_vanquish = True
    return can_use_vanquish


def _has_conquer_requirements(state, player):
    can_use_conquer = False
    if _has_tank_assembler_requirements(state, player) and _has_basic_assembler_module_requirements(state, player) and state.has_all_counts(
            {"Progressive Tanks": 4}, player) and _has_locus_requirements(state, player) and state.has_all({"Large Carbide Wall", "Constructor"}, player):
        can_use_conquer = True
    return can_use_conquer


def _has_diffuse_requirements(state, player):
    can_use_diffuse = False
    if state.has("Diffuse", player) and has_tungsten(state, player):
        can_use_diffuse = True
    return can_use_diffuse


def _has_sublimate_requirements(state, player):
    can_use_sublimate = False
    if state.has_all({"Sublimate", "Reinforced Conduit"}, player) and has_tungsten(state, player) and has_oxide(state, player) and (has_ozone(state, player) or has_cyanogen(state, player)):
        can_use_sublimate = True
    return can_use_sublimate


def has_disperse_requirements(state, player):
    can_use_disperse = False
    if state.has("Disperse", player) and has_thorium_erekir(state, player) and has_oxide(state, player) and has_tungsten(state, player):
        can_use_disperse = True
    return can_use_disperse


def has_afflict_requirements(state, player):
    can_use_afflict = False
    if state.has("Afflict", player) and has_surge_alloy_erekir(state, player) and has_oxide(state, player) and has_heat(state, player):
        can_use_afflict = True
    return can_use_afflict


def has_scathe_requirements(state, player):
    can_use_scathe = False
    if state.has("Scathe", player) and has_tungsten(state, player) and has_oxide(state, player) and has_carbide(state, player):
        can_use_scathe = True
    return can_use_scathe


def has_titan_requirements(state, player):
    can_use_titan = False
    if state.has("Titan", player) and has_thorium_erekir(state, player) and has_tungsten(state, player) and has_hydrogen(state, player):
        can_use_titan = True
    return can_use_titan

def has_malign_requirements(state, player):
    can_use_malign = False
    if state.has("Malign", player) and has_phase_fabric_erekir(state, player) and has_carbide(state, player) and has_high_heat(state, player):
        can_use_malign = True
    return can_use_malign


def has_lustre_requirements(state, player):
    can_use_lustre = False
    if state.has_all({"Lustre", "Reinforced Conduit"}, player) and has_oxide(state, player) and has_carbide(state, player) and has_nitrogen(state, player):
        can_use_lustre = True
    return can_use_lustre


def has_smite_requirements(state, player):
    can_use_smite = False
    if state.has("Smite", player) and has_phase_fabric_erekir(state, player) and has_surge_alloy_erekir(state, player) and has_oxide(state, player) and has_carbide(state, player):
        can_use_smite = True
    return can_use_smite


def has_tungsten_wall_requirements(state, player):
    can_use_wall = False
    if state.has_any({"Tungsten Wall", "Large Tungsten Wall"}, player) and has_tungsten(state, player):
        can_use_wall = True
    return can_use_wall

def has_surge_wall_requirements(state, player):
    can_use_wall = False
    if state.has_any({"Reinforced Surge Wall", "Large Reinforced Surge Wall"}, player) and has_tungsten(state, player) and has_surge_alloy_erekir(state, player):
        can_use_wall = True
    return can_use_wall

def has_carbide_wall_requirements(state, player):
    can_use_wall = False
    if state.has_any({"Carbide Wall", "Large Carbide Wall"}, player) and has_carbide(state, player) and has_thorium_erekir(state, player):
        can_use_wall = True
    return can_use_wall

def has_shielded_wall_requirements(state, player):
    can_use_wall = False
    if state.has("Shielded Wall", player) and has_surge_alloy_erekir(state, player) and has_phase_fabric_erekir(state, player):
        can_use_wall = True
    return can_use_wall


def has_regen_projector_requirements(state, player):
    can_use_projector = False
    if state.has_all({"Regen Projector", "Reinforced Conduit"}, player) and has_tungsten(state, player) and has_oxide(state, player) and has_hydrogen(state, player):
        can_use_projector = True
    return can_use_projector

def has_build_tower_requirements(state, player):
    can_use_tower = False
    if state.has_all({"Build Tower", "Reinforced Conduit"}, player) and has_thorium_erekir(state, player) and has_oxide(state, player) and has_nitrogen(state, player):
        can_use_tower = True
    return can_use_tower

def has_shockwave_tower_requirements(state, player):
    can_use_tower = False
    if state.has_all({"Shockwave Tower", "Reinforced Conduit"}, player) and has_tungsten(state, player) and has_oxide(state, player) and has_surge_alloy_erekir(state, player) and has_cyanogen(state, player):
        can_use_tower = True
    return can_use_tower


def get_defense_military_score_erekir(state: CollectionState, player:int) ->int:
    """Return the military score of the player defense based on their research"""
    score = 0

    if _has_diffuse_requirements(state, player):
        score += 1
    if _has_sublimate_requirements(state, player):
        score += 2
    if has_disperse_requirements(state, player):
        score += 3
    if has_afflict_requirements(state, player):
        score += 4
    if has_scathe_requirements(state, player):
        score += 4
    if has_titan_requirements(state, player):
        score += 4
    if has_malign_requirements(state, player):
        score += 8
    if has_lustre_requirements(state, player):
        score += 8
    if has_smite_requirements(state, player):
        score += 10

    if has_tungsten_wall_requirements(state, player):
        score += 1
    if has_surge_wall_requirements(state, player):
        score += 3
    if has_carbide_wall_requirements(state, player):
        score += 5
    if has_shielded_wall_requirements(state, player):
        score += 10

    if has_regen_projector_requirements(state, player):
        score += 3
    if has_build_tower_requirements(state, player):
        score += 4
    if has_shockwave_tower_requirements(state, player):
        score += 8
    # Total = 78
    return score

def get_unit_military_score_erekir(state: CollectionState, player:int) -> int:
    """Return the military score of the player unit based on their research"""
    score = 0

    if _has_elude_requirements(state, player):
        score += 1
    if _has_avert_requirements(state, player):
        score += 2
    if _has_obviate_requirements(state, player):
        score += 3
    if _has_quell_requirements(state, player):
        score += 4
    if _has_disrupt_requiremts(state, player):
        score += 5

    if _has_merui_requirements(state, player):
        score += 1
    if _has_cleroi_requirements(state, player):
        score += 2
    if _has_anthicus_requirements(state, player):
        score += 3
    if _has_tecta_requirements(state, player):
        score += 4
    if _has_collaris_requirements(state, player):
        score += 5

    if _has_locus_requirements(state, player):
        score += 2
    if _has_precept_requirements(state, player):
        score += 3
    if _has_vanquish_requirements(state, player):
        score += 4
    if _has_conquer_requirements(state, player):
        score += 5
    #Total = 44
    return score

#endregion