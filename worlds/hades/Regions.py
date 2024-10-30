def create_main_weapon_regions(ctx, weaponSubfix, subfixCounter, location_database):
    from . import create_region
    
    hades_base_location_id = 5093427000
    
    tartarus = {}
    asphodel = {}
    elysium = {}
    styx = {}
    styx_late = {}
    
    for i in range(13):
        stringInt = i + 1
        if stringInt < 10:
            stringInt = "0" + str(stringInt)
        tartarus["Clear Room " + str(stringInt) + " " +  weaponSubfix] = hades_base_location_id + 1073 + i \
            + 73 * subfixCounter
    tartarus["Beat Meg " + weaponSubfix] = None

    for i in range(13, 23):
        asphodel["Clear Room " + str(i + 1) + " " + weaponSubfix] = hades_base_location_id + 1073 + i \
            + 73 * subfixCounter
    
    asphodel["Beat Lernie " + weaponSubfix] = None

    for i in range(23, 35):
        elysium["Clear Room " + str(i + 1) + " " + weaponSubfix] = hades_base_location_id + 1073 + i \
            + 73 * subfixCounter
    elysium["Beat Bros " + weaponSubfix] = None

    for i in range(35, 60):
        styx["Clear Room " + str(i + 1) + " " + weaponSubfix] = hades_base_location_id + 1073 + i + 73 * subfixCounter
        
    styx["Beat Hades " + weaponSubfix] = None

    for i in range(60, 72):
        styx_late["Clear Room " + str(i + 1) + " " + weaponSubfix] = hades_base_location_id + 1073 + i \
            + 73 * subfixCounter
    
    ctx.multiworld.regions += [
                create_region(ctx.multiworld, ctx.player, location_database, "Tartarus " + weaponSubfix,
                              [location for location in tartarus], 
                              ["Exit Tartarus " + weaponSubfix, "Die Tartarus " + weaponSubfix]),
                create_region(ctx.multiworld, ctx.player, location_database, "Asphodel " + weaponSubfix,
                              [location for location in asphodel], 
                              ["Exit Asphodel " + weaponSubfix, "Die Asphodel " + weaponSubfix]),
                create_region(ctx.multiworld, ctx.player, location_database, "Elysium " + weaponSubfix, 
                              [location for location in elysium], 
                              ["Exit Elysium " + weaponSubfix, "Die Elysium " + weaponSubfix]),
                create_region(ctx.multiworld, ctx.player, location_database, "Styx " + weaponSubfix,
                              [location for location in styx], 
                              ["Die Styx " + weaponSubfix, "Late Chambers " + weaponSubfix]),
                create_region(ctx.multiworld, ctx.player, location_database, "Styx Late " + weaponSubfix, 
                              [location for location in styx_late],
                              ["Die Styx Late " + weaponSubfix]),
            ]
    
    tartarus = {}
    asphodel = {}
    elysium = {}
    styx = {}
    styx_late = {}


def create_regions(ctx, location_database):
    from . import create_region
    from .Locations import location_table_tartarus, location_table_asphodel, location_table_elysium, \
        location_table_styx, location_table_styx_late, location_keepsakes, location_weapons, \
        should_ignore_weapon_location, location_store_gemstones, location_store_diamonds, \
        location_table_fates, location_table_fates_events, location_weapons_subfixes

    # create correct underworld exit
    underworldExits = []
    if ctx.options.keepsakesanity:
        underworldExits += ["NPCS"]
        
    if ctx.options.weaponsanity:
        underworldExits += ["Weapon Cache"]
        
    if ctx.options.storesanity:
        underworldExits += ["Store Gemstones Entrance"]
        underworldExits += ["Store Diamonds Entrance"]
    
    # Add fates list for achievement logic and fatesanity if needed
    underworldExits += ["Fated Lists"]

    ctx.multiworld.regions += [create_region(ctx.multiworld, ctx.player, location_database, "Menu", None, ["Menu"])]    

    if ctx.options.location_system == "room_weapon_based":
        # do as below but per weapons
        subfixCounter = 0
        for weaponSubfix in location_weapons_subfixes:
            underworldExits += ["Zags room "+weaponSubfix]
            create_main_weapon_regions(ctx, weaponSubfix, subfixCounter, location_database)
            subfixCounter += 1
    else:
        underworldExits += ["Zags room"]
        ctx.multiworld.regions += [
            create_region(ctx.multiworld, ctx.player, location_database, "Tartarus", 
                          [location for location in location_table_tartarus], ["Exit Tartarus", "Die Tartarus"]),
            create_region(ctx.multiworld, ctx.player, location_database, "Asphodel", 
                          [location for location in location_table_asphodel], ["Exit Asphodel", "Die Asphodel"]),
            create_region(ctx.multiworld, ctx.player, location_database, "Elysium", 
                          [location for location in location_table_elysium], ["Exit Elysium", "Die Elysium"]),
            create_region(ctx.multiworld, ctx.player, location_database, "Styx", 
                          [location for location in location_table_styx], ["Die Styx", "Late Chambers"]),
            create_region(ctx.multiworld, ctx.player, location_database, "Styx Late",
                          [location for location in location_table_styx_late], ["Die Styx Late"]),
        ]

    ctx.multiworld.regions += [create_region(ctx.multiworld, ctx.player, location_database,
                                             "Underworld", None, underworldExits)]

    # here we set locations that depend on options
    if ctx.options.keepsakesanity:
        ctx.multiworld.regions += [create_region(ctx.multiworld, ctx.player, location_database, "Keepsakes Locations", 
                                                 [location for location in location_keepsakes], ["Exit NPCS"])] 
    
    if ctx.options.weaponsanity:
        weaponChecks = {}
        for weaponLocation, weaponData in location_weapons.items():
            if not should_ignore_weapon_location(weaponLocation, ctx.options):
                weaponChecks.update({weaponLocation: weaponData})
        ctx.multiworld.regions += [create_region(ctx.multiworld, ctx.player, location_database, "Weapons Locations", 
                                                 [location for location in weaponChecks], ["Exit Weapon Cache"])]
        
    if ctx.options.storesanity:
        ctx.multiworld.regions += [create_region(ctx.multiworld, ctx.player, location_database, "Store Gemstones", 
                                                 [location for location in location_store_gemstones], ["Exit Gem Store"])] 
        ctx.multiworld.regions += [create_region(ctx.multiworld, ctx.player, location_database, 
                                                 "Store Diamonds", 
                                                 [location for location in location_store_diamonds], 
                                                 ["Exit Diamond Store"])] 
    
    fates_location = location_table_fates_events.copy()
    if ctx.options.fatesanity:
        fates_location.update(location_table_fates)
    ctx.multiworld.regions += [create_region(ctx.multiworld, ctx.player, location_database, "Fated List", 
                                             [location for location in fates_location], ["Exit Fated List"])] 

    # link up regions
    ctx.multiworld.get_entrance("Menu", ctx.player).connect(ctx.multiworld.get_region("Underworld", ctx.player))
    if ctx.options.location_system == "room_weapon_based":
        for weaponSubfix in location_weapons_subfixes:
            ctx.multiworld.get_entrance("Zags room "+weaponSubfix, ctx.player).connect(
                ctx.multiworld.get_region("Tartarus "+weaponSubfix, ctx.player))
            ctx.multiworld.get_entrance("Exit Tartarus "+weaponSubfix, ctx.player).connect(
                ctx.multiworld.get_region("Asphodel "+weaponSubfix, ctx.player))
            ctx.multiworld.get_entrance("Exit Asphodel "+weaponSubfix, ctx.player).connect(
                ctx.multiworld.get_region("Elysium "+weaponSubfix, ctx.player))
            ctx.multiworld.get_entrance("Exit Elysium "+weaponSubfix, ctx.player).connect(
                ctx.multiworld.get_region("Styx "+weaponSubfix, ctx.player))
            ctx.multiworld.get_entrance("Late Chambers "+weaponSubfix, ctx.player).connect(
                ctx.multiworld.get_region("Styx Late "+weaponSubfix, ctx.player))
            ctx.multiworld.get_entrance("Die Tartarus "+weaponSubfix, ctx.player).connect(
                ctx.multiworld.get_region("Underworld", ctx.player))
            ctx.multiworld.get_entrance("Die Asphodel "+weaponSubfix, ctx.player).connect(
                ctx.multiworld.get_region("Underworld", ctx.player))    
            ctx.multiworld.get_entrance("Die Elysium "+weaponSubfix, ctx.player).connect(
                ctx.multiworld.get_region("Underworld", ctx.player))
            ctx.multiworld.get_entrance("Die Styx "+weaponSubfix, ctx.player).connect(
                ctx.multiworld.get_region("Underworld", ctx.player))
            ctx.multiworld.get_entrance("Die Styx Late "+weaponSubfix, ctx.player).connect(
                ctx.multiworld.get_region("Underworld", ctx.player))
    else:
        ctx.multiworld.get_entrance("Zags room", ctx.player).connect(ctx.multiworld.get_region("Tartarus", ctx.player))
        ctx.multiworld.get_entrance("Exit Tartarus", ctx.player).connect(
            ctx.multiworld.get_region("Asphodel", ctx.player))
        ctx.multiworld.get_entrance("Exit Asphodel", ctx.player).connect(
            ctx.multiworld.get_region("Elysium", ctx.player))
        ctx.multiworld.get_entrance("Exit Elysium", ctx.player).connect(
            ctx.multiworld.get_region("Styx", ctx.player))
        ctx.multiworld.get_entrance("Late Chambers", ctx.player).connect(
            ctx.multiworld.get_region("Styx Late", ctx.player))
        ctx.multiworld.get_entrance("Die Tartarus", ctx.player).connect(
            ctx.multiworld.get_region("Underworld", ctx.player))
        ctx.multiworld.get_entrance("Die Asphodel", ctx.player).connect(
            ctx.multiworld.get_region("Underworld", ctx.player))    
        ctx.multiworld.get_entrance("Die Elysium", ctx.player).connect(
            ctx.multiworld.get_region("Underworld", ctx.player))
        ctx.multiworld.get_entrance("Die Styx", ctx.player).connect(
            ctx.multiworld.get_region("Underworld", ctx.player))
        ctx.multiworld.get_entrance("Die Styx Late", ctx.player).connect(
            ctx.multiworld.get_region("Underworld", ctx.player))

    # here we connect locations that depend on options
    if ctx.options.keepsakesanity:
        ctx.multiworld.get_entrance("NPCS", ctx.player).connect(
            ctx.multiworld.get_region("Keepsakes Locations", ctx.player))
        ctx.multiworld.get_entrance("Exit NPCS", ctx.player).connect(ctx.multiworld.get_region("Underworld", ctx.player))
        
    if ctx.options.weaponsanity:
        ctx.multiworld.get_entrance("Weapon Cache", ctx.player).connect(
            ctx.multiworld.get_region("Weapons Locations", ctx.player))
        ctx.multiworld.get_entrance("Exit Weapon Cache", ctx.player).connect(
            ctx.multiworld.get_region("Underworld", ctx.player))
        
    if ctx.options.storesanity:
        ctx.multiworld.get_entrance("Store Gemstones Entrance", ctx.player).connect(
            ctx.multiworld.get_region("Store Gemstones", ctx.player))
        ctx.multiworld.get_entrance("Exit Gem Store", ctx.player).connect(
            ctx.multiworld.get_region("Underworld", ctx.player))
        
        ctx.multiworld.get_entrance("Store Diamonds Entrance", ctx.player).connect(
            ctx.multiworld.get_region("Store Diamonds", ctx.player))
        ctx.multiworld.get_entrance("Exit Diamond Store", ctx.player).connect(
            ctx.multiworld.get_region("Underworld", ctx.player))
        
    ctx.multiworld.get_entrance("Fated Lists", ctx.player).connect(
        ctx.multiworld.get_region("Fated List", ctx.player))
    ctx.multiworld.get_entrance("Exit Fated List", ctx.player).connect(
        ctx.multiworld.get_region("Underworld", ctx.player))