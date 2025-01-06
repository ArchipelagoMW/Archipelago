from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule

WORLDS = [
    "World Card Wonderland",
    "World Card Olympus Coliseum",
    "World Card Agrabah",
    "World Card Monstro",
    "World Card Atlantica",
    "World Card Halloween Town",
    "World Card Neverland",
    "World Card Hollow Bastion",
    "World Card 100 Acre Wood",
    "World Card Twilight Town",
    "World Card Destiny Islands"]

def has_castle_oblivion(state: CollectionState, player: int) -> bool:
    return (
        state.has_all({
            "Friend Card Donald",
            "Friend Card Goofy",
            "Friend Card Aladdin",
            "Friend Card Ariel",
            "Friend Card Beast",
            "Friend Card Jack",
            "Friend Card Peter Pan",
            "Friend Card Pluto"}, player)
        and has_x_worlds(state, player, 8))

def has_x_worlds(state: CollectionState, player: int, num_of_worlds: int) -> bool:
    return state.has_from_list_unique(WORLDS, player, num_of_worlds)

def set_rules(khrecomworld):
    multiworld = khrecomworld.multiworld
    options    = khrecomworld.options
    player     = khrecomworld.player
    
    #Location rules.
    add_rule(khrecomworld.get_location("Traverse Town Room of Rewards (Attack Cards Lionheart)"),
        lambda state: state.has("Key to Rewards Traverse Town", player))
    add_rule(khrecomworld.get_location("Olympus Coliseum Room of Rewards (Attack Cards Metal Chocobo)"),
        lambda state: state.has("Key to Rewards Olympus Coliseum", player))
    add_rule(khrecomworld.get_location("Hollow Bastion Room of Rewards (Summon Cards Mushu)"),
        lambda state: state.has("Key to Rewards Hollow Bastion", player))
    add_rule(khrecomworld.get_location("Destiny Islands Room of Rewards (Item Cards Megalixir)"),
        lambda state: state.has("Key to Rewards Destiny Islands", player))
    add_rule(khrecomworld.get_location("06F Exit Hall Larxene I (Magic Cards Thunder)"),
        lambda state: has_x_worlds(state, player, 4))
    add_rule(khrecomworld.get_location("07F Exit Hall Riku I (Magic Cards Aero)"),
        lambda state: has_x_worlds(state, player, 5))
    add_rule(khrecomworld.get_location("11F Exit Hall Riku III (Item Cards Mega-Potion)"),
        lambda state: has_x_worlds(state, player, 6))
    add_rule(khrecomworld.get_location("12F Exit Hall Larxene II (Attack Cards Oblivion)"),
        lambda state: has_x_worlds(state, player, 7))
    add_rule(khrecomworld.get_location("12F Exit Hall Larxene II (Enemy Cards Larxene)"),
        lambda state: has_x_worlds(state, player, 7))
    add_rule(khrecomworld.get_location("12F Exit Hall Riku IV (Enemy Cards Riku)"),
        lambda state: has_x_worlds(state, player, 7))
    add_rule(khrecomworld.get_location("100 Acre Wood Tigger's Playground (Attack Cards Spellbinder)"),
        lambda state: state.has("World Card Neverland", player) and state.has("World Card Monstro", player))
    
    # Days Rules
    if options.days_locations:
        add_rule(khrecomworld.get_location("Traverse Town Room of Rewards (Enemy Cards Saix)"),
            lambda state: state.has("Key to Rewards Traverse Town", player))
        add_rule(khrecomworld.get_location("Wonderland Room of Rewards (Enemy Cards Xemnas)"),
            lambda state: state.has("Key to Rewards Wonderland", player))
        add_rule(khrecomworld.get_location("Olympus Coliseum Room of Rewards (Attack Cards Total Eclipse)"),
            lambda state: state.has("Key to Rewards Olympus Coliseum", player))
        add_rule(khrecomworld.get_location("Monstro Room of Rewards (Enemy Cards Xaldin)"),
            lambda state: state.has("Key to Rewards Monstro", player))
        add_rule(khrecomworld.get_location("Agrabah Room of Rewards (Enemy Cards Luxord)"),
            lambda state: state.has("Key to Rewards Agrabah", player))
        add_rule(khrecomworld.get_location("Halloween Town Room of Rewards (Attack Cards Bond of Flame)"),
            lambda state: state.has("Key to Rewards Halloween Town", player))
        add_rule(khrecomworld.get_location("Atlantica Room of Rewards (Enemy Cards Demyx)"),
            lambda state: state.has("Key to Rewards Atlantica", player))
        add_rule(khrecomworld.get_location("Neverland Room of Rewards (Attack Cards Midnight Roar)"),
            lambda state: state.has("Key to Rewards Neverland", player))
        add_rule(khrecomworld.get_location("Hollow Bastion Room of Rewards (Enemy Cards Xigbar)"),
            lambda state: state.has("Key to Rewards Hollow Bastion", player))
        add_rule(khrecomworld.get_location("Twilight Town Room of Rewards (Enemy Cards Roxas)"),
            lambda state: state.has("Key to Rewards Twilight Town", player))
        add_rule(khrecomworld.get_location("Destiny Islands Room of Rewards (Attack Cards Two Become One)"),
            lambda state: state.has("Key to Rewards Destiny Islands", player))
        add_rule(khrecomworld.get_location("Castle Oblivion Room of Rewards (Attack Cards Star Seeker)"),
            lambda state: state.has("Key to Rewards Castle Oblivion", player))

    
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Air Pirate"),
        lambda state: state.has("World Card Neverland", player))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Air Pirate"),
        lambda state: state.has("World Card Neverland", player))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Air Pirate"),
        lambda state: state.has("World Card Neverland", player))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Air Soldier"),
        lambda state: (
            state.has_any({
                "World Card Monstro",
                "World Card Agrabah",
                "World Card Twilight Town"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Air Soldier"),
        lambda state: (
            state.has_any({
                "World Card Monstro",
                "World Card Agrabah",
                "World Card Twilight Town"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Air Soldier"),
        lambda state: (
            state.has_any({
                "World Card Monstro",
                "World Card Agrabah",
                "World Card Twilight Town"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Aquatank"),
        lambda state: state.has("World Card Atlantica", player))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Aquatank"),
        lambda state: state.has("World Card Atlantica", player))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Aquatank"),
        lambda state: state.has("World Card Atlantica", player))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Bandit"),
        lambda state: state.has("World Card Agrabah", player))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Bandit"),
        lambda state: state.has("World Card Agrabah", player))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Bandit"),
        lambda state: state.has("World Card Agrabah", player))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Barrel Spider"),
        lambda state: (
            state.has_any({
                "World Card Monstro",
                "World Card Agrabah",
                "World Card Neverland"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Barrel Spider"),
        lambda state: (
            state.has_any({
                "World Card Monstro",
                "World Card Agrabah",
                "World Card Neverland"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Barrel Spider"),
        lambda state: (
            state.has_any({
                "World Card Monstro",
                "World Card Agrabah",
                "World Card Neverland"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Bouncywild"),
        lambda state: state.has("World Card Olympus Coliseum", player))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Bouncywild"),
        lambda state: state.has("World Card Olympus Coliseum", player))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Bouncywild"),
        lambda state: state.has("World Card Olympus Coliseum", player))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Creeper Plant"),
        lambda state: (
            state.has_any({
                "World Card Wonderland",
                "World Card Halloween Town",
                "World Card Destiny Islands"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Creeper Plant"),
        lambda state: (
            state.has_any({
                "World Card Wonderland",
                "World Card Halloween Town",
                "World Card Destiny Islands"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Creeper Plant"),
        lambda state: (
            state.has_any({
                "World Card Wonderland",
                "World Card Halloween Town",
                "World Card Destiny Islands"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Crescendo"),
        lambda state: (
            state.has_any({
                "World Card Wonderland",
                "World Card Neverland",
                "World Card Destiny Islands"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Crescendo"),
        lambda state: (
            state.has_any({
                "World Card Wonderland",
                "World Card Neverland",
                "World Card Destiny Islands"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Crescendo"),
        lambda state: (
            state.has_any({
                "World Card Wonderland",
                "World Card Neverland",
                "World Card Destiny Islands"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Darkball"),
        lambda state: (
            state.has_any({
                "World Card Atlantica",
                "World Card Neverland",
                "World Card Destiny Islands"}, player)
            or has_castle_oblivion(state, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Darkball"),
        lambda state: (
            state.has_any({
                "World Card Atlantica",
                "World Card Neverland",
                "World Card Destiny Islands"}, player)
            or has_castle_oblivion(state, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Darkball"),
        lambda state: (
            state.has_any({
                "World Card Atlantica",
                "World Card Neverland",
                "World Card Destiny Islands"}, player)
            or has_castle_oblivion(state, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Defender"),
        lambda state: state.has("World Card Hollow Bastion", player) 
        or has_castle_oblivion(state, player))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Defender"),
        lambda state: state.has("World Card Hollow Bastion", player) 
        or has_castle_oblivion(state, player))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Defender"),
        lambda state: state.has("World Card Hollow Bastion", player) 
        or has_castle_oblivion(state, player))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Fat Bandit"),
        lambda state: state.has("World Card Agrabah", player))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Fat Bandit"),
        lambda state: state.has("World Card Agrabah", player))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Fat Bandit"),
        lambda state: state.has("World Card Agrabah", player))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Gargoyle"),
        lambda state: state.has("World Card Halloween Town", player))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Gargoyle"),
        lambda state: state.has("World Card Halloween Town", player))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Gargoyle"),
        lambda state: state.has("World Card Halloween Town", player))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Green Requiem"),
        lambda state: (
            state.has_any({
                "World Card Monstro",
                "World Card Agrabah"}, player)
            or has_castle_oblivion(state, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Green Requiem"),
        lambda state: (
            state.has_any({
                "World Card Monstro",
                "World Card Agrabah"}, player)
            or has_castle_oblivion(state, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Green Requiem"),
        lambda state: (
            state.has_any({
                "World Card Monstro",
                "World Card Agrabah"}, player) 
            or has_castle_oblivion(state, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Large Body"),
        lambda state: (
            state.has_any({
                "World Card Wonderland",
                "World Card Olympus Coliseum",
                "World Card Monstro"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Large Body"),
        lambda state: (
            state.has_any({
                "World Card Wonderland",
                "World Card Olympus Coliseum",
                "World Card Monstro"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Large Body"),
        lambda state: (
            state.has_any({
                "World Card Wonderland",
                "World Card Olympus Coliseum",
                "World Card Monstro"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Neoshadow"),
        lambda state: has_castle_oblivion(state, player))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Neoshadow"),
        lambda state: has_castle_oblivion(state, player))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Neoshadow"),
        lambda state: has_castle_oblivion(state, player))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Pirate"),
        lambda state: state.has("World Card Neverland", player))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Pirate"),
        lambda state: state.has("World Card Neverland", player))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Pirate"),
        lambda state: state.has("World Card Neverland", player))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Powerwild"),
        lambda state: state.has("World Card Olympus Coliseum", player))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Powerwild"),
        lambda state: state.has("World Card Olympus Coliseum", player))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Powerwild"),
        lambda state: state.has("World Card Olympus Coliseum", player))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Screwdiver"),
        lambda state: state.has("World Card Atlantica", player))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Screwdiver"),
        lambda state: state.has("World Card Atlantica", player))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Screwdiver"),
        lambda state: state.has("World Card Atlantica", player))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Sea Neon"),
        lambda state: state.has("World Card Atlantica", player))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Sea Neon"),
        lambda state: state.has("World Card Atlantica", player))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Sea Neon"),
        lambda state: state.has("World Card Atlantica", player))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Search Ghost"),
        lambda state: (
            state.has_any({
                "World Card Monstro",
                "World Card Atlantica", 
                "World Card Halloween Town"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Search Ghost"),
        lambda state: (
            state.has_any({
                "World Card Monstro",
                "World Card Atlantica", 
                "World Card Halloween Town"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Search Ghost"),
        lambda state: (
            state.has_any({
                "World Card Monstro",
                "World Card Atlantica", 
                "World Card Halloween Town"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Tornado Step"),
        lambda state: (
            state.has_any({
                "World Card Monstro",
                "World Card Hollow Bastion",
                "World Card Destiny Islands"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Tornado Step"),
        lambda state: (
            state.has_any({
                "World Card Monstro",
                "World Card Hollow Bastion",
                "World Card Destiny Islands"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Tornado Step"),
        lambda state: (
            state.has_any({
                "World Card Monstro",
                "World Card Hollow Bastion",
                "World Card Destiny Islands"}, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Wight Knight"),
        lambda state: state.has("World Card Halloween Town", player))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Wight Knight"),
        lambda state: state.has("World Card Halloween Town", player))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Wight Knight"),
        lambda state: state.has("World Card Halloween Town", player))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Wizard"),
        lambda state: (
            state.has("World Card Hollow Bastion", player) 
            or has_castle_oblivion(state, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Wizard"),
        lambda state: (
            state.has("World Card Hollow Bastion", player) 
            or has_castle_oblivion(state, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Wizard"),
        lambda state: (
            state.has("World Card Hollow Bastion", player) 
            or has_castle_oblivion(state, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Wyvern"),
        lambda state: (
            state.has("World Card Hollow Bastion", player) 
            or has_castle_oblivion(state, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Wyvern"),
        lambda state: (
            state.has("World Card Hollow Bastion", player) 
            or has_castle_oblivion(state, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Wyvern"),
        lambda state: (
            state.has("World Card Hollow Bastion", player) 
            or has_castle_oblivion(state, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 1 Heartless Yellow Opera"),
        lambda state: (
            state.has_any({
                "World Card Monstro",
                "World Card Agrabah",
                "World Card Neverland"}, player)
            or has_castle_oblivion(state, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 2 Heartless Yellow Opera"),
        lambda state: (
            state.has_any({
                "World Card Monstro",
                "World Card Agrabah",
                "World Card Neverland"}, player)
            or has_castle_oblivion(state, player)
        ))
    add_rule(khrecomworld.get_location("Defeat 3 Heartless Yellow Opera"),
        lambda state: (
            state.has_any({
                "World Card Monstro",
                "World Card Agrabah",
                "World Card Neverland"}, player)
            or has_castle_oblivion(state, player)
        ))
    
    if options.levels:
        add_rule(khrecomworld.get_location("Level 12 (Sleight Strike Raid)"),
            lambda state: has_x_worlds(state, player, 2))
        add_rule(khrecomworld.get_location("Level 17 (Sleight Blitz)"),
            lambda state: has_x_worlds(state, player, 2))
        add_rule(khrecomworld.get_location("Level 22 (Sleight Zantetsuken)"),
            lambda state: has_x_worlds(state, player, 3))
        add_rule(khrecomworld.get_location("Level 27 (Sleight Sonic Blade)"),
            lambda state: has_x_worlds(state, player, 3))
        add_rule(khrecomworld.get_location("Level 32 (Sleight Lethal Frame)"),
            lambda state: has_x_worlds(state, player, 4))
        add_rule(khrecomworld.get_location("Level 37 (Sleight Tornado)"),
            lambda state: has_x_worlds(state, player, 4))
        add_rule(khrecomworld.get_location("Level 42 (Sleight Ars Arcanum)"),
            lambda state: has_x_worlds(state, player, 5))
        add_rule(khrecomworld.get_location("Level 47 (Sleight Holy)"),
            lambda state: has_x_worlds(state, player, 5))
        add_rule(khrecomworld.get_location("Level 52 (Sleight Ragnarok)"),
            lambda state: has_x_worlds(state, player, 6))
        add_rule(khrecomworld.get_location("Level 57 (Sleight Mega Flare)"),
            lambda state: has_x_worlds(state, player, 6))
    add_rule(khrecomworld.get_location("Agrabah Room of Rewards (Sleight Warp)"),
        lambda state: state.has( "Key to Rewards Agrabah", player))
    add_rule(khrecomworld.get_location("Atlantica Room of Rewards (Sleight Quake)"),
        lambda state: state.has( "Key to Rewards Atlantica", player))
    add_rule(khrecomworld.get_location("Halloween Town Room of Rewards (Sleight Bind)"),
        lambda state: state.has( "Key to Rewards Halloween Town", player))
    add_rule(khrecomworld.get_location("Hollow Bastion Room of Rewards (Sleight Flare Breath LV2)"),
        lambda state: state.has( "Key to Rewards Hollow Bastion", player))
    add_rule(khrecomworld.get_location("Hollow Bastion Room of Rewards (Sleight Flare Breath LV3)"),
        lambda state: state.has( "Key to Rewards Hollow Bastion", player))
    add_rule(khrecomworld.get_location("Monstro Room of Rewards (Sleight Aqua Splash)"),
        lambda state: state.has( "Key to Rewards Monstro", player))
    add_rule(khrecomworld.get_location("Neverland Room of Rewards (Sleight Thunder Raid)"),
        lambda state: state.has( "Key to Rewards Neverland", player))
    add_rule(khrecomworld.get_location("Twilight Town Room of Rewards (Sleight Stardust Blitz)"),
        lambda state: state.has( "Key to Rewards Twilight Town", player))
    add_rule(khrecomworld.get_location("Wonderland Room of Rewards (Sleight Synchro)"),
        lambda state: state.has( "Key to Rewards Wonderland", player))
    add_rule(khrecomworld.get_location("08F Exit Hall Riku II (Sleight Magnet Spiral)"),
        lambda state: has_x_worlds(state, player, 5))
    add_rule(khrecomworld.get_location("10F Exit Hall Vexen I (Sleight Freeze)"),
        lambda state: has_x_worlds(state, player, 6))
    add_rule(khrecomworld.get_location("06F Exit Hall Larxene I (Sleight Thundara)"),
        lambda state: has_x_worlds(state, player, 4))
    add_rule(khrecomworld.get_location("06F Exit Hall Larxene I (Sleight Thundaga)"),
        lambda state: has_x_worlds(state, player, 4))
    add_rule(khrecomworld.get_location("07F Exit Hall Riku I (Sleight Aerora)"),
        lambda state: has_x_worlds(state, player, 5))
    add_rule(khrecomworld.get_location("07F Exit Hall Riku I (Sleight Aeroga)"),
        lambda state: has_x_worlds(state, player, 5))
    
    # Region rules.
    add_rule(khrecomworld.get_entrance("Wonderland"),
        lambda state: state.has("World Card Wonderland", player))
    add_rule(khrecomworld.get_entrance("Olympus Coliseum"),
        lambda state: state.has("World Card Olympus Coliseum", player))
    add_rule(khrecomworld.get_entrance("Monstro"),
        lambda state: state.has("World Card Monstro", player))
    add_rule(khrecomworld.get_entrance("Agrabah"),
        lambda state: state.has("World Card Agrabah", player))
    add_rule(khrecomworld.get_entrance("Halloween Town"),
        lambda state: state.has("World Card Halloween Town", player))
    add_rule(khrecomworld.get_entrance("Atlantica"),
        lambda state: state.has("World Card Atlantica", player))
    add_rule(khrecomworld.get_entrance("Neverland"),
        lambda state: state.has("World Card Neverland", player))
    add_rule(khrecomworld.get_entrance("Hollow Bastion"),
        lambda state: state.has("World Card Hollow Bastion", player))
    add_rule(khrecomworld.get_entrance("100 Acre Wood"),
        lambda state: state.has("World Card 100 Acre Wood", player))
    add_rule(khrecomworld.get_entrance("Twilight Town"),
        lambda state: state.has("World Card Twilight Town", player) and has_x_worlds(state, player, 4))
    add_rule(khrecomworld.get_entrance("Destiny Islands"),
        lambda state: state.has("World Card Destiny Islands", player) and has_x_worlds(state, player, 6))
    add_rule(khrecomworld.get_entrance("Castle Oblivion"),
        lambda state: has_castle_oblivion(state, player))
    
    # Win condition.
    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
