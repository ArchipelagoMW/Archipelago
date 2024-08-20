def create_main_weapon_regions(ctx, weaponSubfix, subfixCounter, location_database):
    from . import create_region
    
    hades_base_location_id = 5093427000
    
    tartarus = {}
    asphodel = {}
    elyseum = {}
    styx = {}
    styx_late = {}
    
    for i in range(13):
        stringInt=i+1;
        if (stringInt<10):
            stringInt = "0"+str(stringInt);
        tartarus["ClearRoom"+str(stringInt)+weaponSubfix] = hades_base_location_id+1073+i+subfixCounter*73
    tartarus["Beat Meg"+weaponSubfix] = None

    for i in range(13,23):
        asphodel["ClearRoom"+str(i+1)+weaponSubfix]=hades_base_location_id+1073+i+subfixCounter*73
    
    asphodel["Beat Lernie"+weaponSubfix] = None

    for i in range(23,35):
        elyseum["ClearRoom"+str(i+1)+weaponSubfix]=hades_base_location_id+1073+i+subfixCounter*73
    elyseum["Beat Bros"+weaponSubfix] = None    

    for i in range(35,60):
        styx["ClearRoom"+str(i+1)+weaponSubfix]=hades_base_location_id+1073+i+subfixCounter*73
        
    styx["Beat Hades"+weaponSubfix] = None

    for i in range(60,72):
        styx_late["ClearRoom"+str(i+1)+weaponSubfix]=hades_base_location_id+1073+i+subfixCounter*73
    
    ctx.multiworld.regions += [
                create_region(ctx.multiworld, ctx.player, location_database, "Tartarus"+weaponSubfix, 
                              [location for location in tartarus], ["Exit Tartarus"+weaponSubfix, "DieT"+weaponSubfix]),
                create_region(ctx.multiworld, ctx.player, location_database, "Asphodel"+weaponSubfix, 
                              [location for location in asphodel], ["Exit Asphodel"+weaponSubfix, "DieA"+weaponSubfix]),
                create_region(ctx.multiworld, ctx.player, location_database, "Elyseum"+weaponSubfix, 
                              [location for location in elyseum], ["Exit Elyseum"+weaponSubfix, "DieE"+weaponSubfix]),
                create_region(ctx.multiworld, ctx.player, location_database, "Styx"+weaponSubfix,
                               [location for location in styx], ["DieS"+weaponSubfix, "Late Chambers"+weaponSubfix]),
                create_region(ctx.multiworld, ctx.player, location_database, "StyxLate"+weaponSubfix, 
                              [location for location in styx_late], ["DieSL"+weaponSubfix]),
            ]
    
    tartarus = {}
    asphodel = {}
    elyseum = {}
    styx = {}
    styx_late = {}


def create_regions(ctx, location_database):
    from . import create_region
    from .Locations import location_table_tartarus, location_table_asphodel, location_table_elyseum, \
        location_table_styx, location_table_styx_late, location_keepsakes, location_weapons, \
        should_ignore_weapon_location, location_store_gemstones, location_store_diamonds, \
        location_table_fates, location_table_fates_events, location_weapons_subfixes

    #create correct underworld exit
    underworldExits = []
    if ctx.options.keepsakesanity:
        underworldExits += ["NPCS"]
        
    if ctx.options.weaponsanity:
        underworldExits += ["Weapon Cache"]
        
    if ctx.options.storesanity:
        underworldExits += ["Store Gemstones Entrance"]
        underworldExits += ["Store Diamonds Entrance"]
    
    #Add fates list for achievement logic and fatesanity if needed
    underworldExits += ["Fated Lists"]

    ctx.multiworld.regions += [create_region(ctx.multiworld, ctx.player, location_database, "Menu", None, ["Menu"])]    

    if ctx.options.location_system == "roomweaponbased":
        #do as below but per weapons
        subfixCounter = 0
        for weaponSubfix in location_weapons_subfixes:
            underworldExits += ["Zags room"+weaponSubfix]
            create_main_weapon_regions(ctx, weaponSubfix, subfixCounter, location_database)
            subfixCounter += 1
    else:
        underworldExits += ["Zags room"]
        ctx.multiworld.regions += [
            create_region(ctx.multiworld, ctx.player, location_database, "Tartarus", 
                        [location for location in location_table_tartarus], ["Exit Tartarus", "DieT"]),
            create_region(ctx.multiworld, ctx.player, location_database, "Asphodel", 
                        [location for location in location_table_asphodel], ["Exit Asphodel", "DieA"]),
            create_region(ctx.multiworld, ctx.player, location_database, "Elyseum", 
                        [location for location in location_table_elyseum], ["Exit Elyseum", "DieE"]),
            create_region(ctx.multiworld, ctx.player, location_database, "Styx", 
                        [location for location in location_table_styx], ["DieS", "Late Chambers"]),
            create_region(ctx.multiworld, ctx.player, location_database, "StyxLate",
                        [location for location in location_table_styx_late], ["DieSL"]),
        ]

    ctx.multiworld.regions += [create_region(ctx.multiworld, ctx.player, location_database, 
                                             "Underworld", None, underworldExits)]

    #here we set locations that depend on options
    if ctx.options.keepsakesanity:
        ctx.multiworld.regions += [create_region(ctx.multiworld,
                                                ctx.player, 
                                                location_database,
                                                "KeepsakesLocations", 
                                                [location for location in location_keepsakes], 
                                                ["ExitNPCS"])] 
    
    if ctx.options.weaponsanity:
        weaponChecks = {}
        for weaponLocation, weaponData in location_weapons.items():
            if (not should_ignore_weapon_location(weaponLocation, ctx.options)):
                weaponChecks.update({weaponLocation : weaponData})
        ctx.multiworld.regions += [create_region(ctx.multiworld, ctx.player, location_database, "WeaponsLocations", 
                                                [location for location in weaponChecks], ["ExitWeaponCache"])]
        
    if ctx.options.storesanity:
        ctx.multiworld.regions += [create_region(ctx.multiworld, ctx.player, location_database, "StoreGemstones", 
                                                [location for location in location_store_gemstones], ["ExitGemStore"])] 
        ctx.multiworld.regions += [create_region(ctx.multiworld, 
                                                ctx.player, location_database, 
                                                "StoreDiamonds", 
                                                [location for location in location_store_diamonds], 
                                                ["ExitDiamondStore"])] 
    
    fates_location = location_table_fates_events.copy()
    if ctx.options.fatesanity:
        fates_location.update(location_table_fates)
    ctx.multiworld.regions += [create_region(ctx.multiworld, ctx.player, location_database, "FatedList", 
                                             [location for location in fates_location], ["ExitFatedList"])] 


    # link up regions
    ctx.multiworld.get_entrance("Menu", ctx.player).connect(ctx.multiworld.get_region("Underworld", ctx.player))
    if ctx.options.location_system == "roomweaponbased":
        for weaponSubfix in location_weapons_subfixes:
            ctx.multiworld.get_entrance("Zags room"+weaponSubfix, ctx.player).connect(
                ctx.multiworld.get_region("Tartarus"+weaponSubfix, ctx.player))
            ctx.multiworld.get_entrance("Exit Tartarus"+weaponSubfix, ctx.player).connect(
                ctx.multiworld.get_region("Asphodel"+weaponSubfix, ctx.player))
            ctx.multiworld.get_entrance("Exit Asphodel"+weaponSubfix, ctx.player).connect(
                ctx.multiworld.get_region("Elyseum"+weaponSubfix, ctx.player))
            ctx.multiworld.get_entrance("Exit Elyseum"+weaponSubfix, ctx.player).connect(
                ctx.multiworld.get_region("Styx"+weaponSubfix, ctx.player))
            ctx.multiworld.get_entrance("Late Chambers"+weaponSubfix, ctx.player).connect(
                ctx.multiworld.get_region("StyxLate"+weaponSubfix, ctx.player))
            ctx.multiworld.get_entrance("DieT"+weaponSubfix, ctx.player).connect(
                ctx.multiworld.get_region("Underworld", ctx.player))
            ctx.multiworld.get_entrance("DieA"+weaponSubfix, ctx.player).connect(
                ctx.multiworld.get_region("Underworld", ctx.player))    
            ctx.multiworld.get_entrance("DieE"+weaponSubfix, ctx.player).connect(
                ctx.multiworld.get_region("Underworld", ctx.player))
            ctx.multiworld.get_entrance("DieS"+weaponSubfix, ctx.player).connect(
                ctx.multiworld.get_region("Underworld", ctx.player))
            ctx.multiworld.get_entrance("DieSL"+weaponSubfix, ctx.player).connect(
                ctx.multiworld.get_region("Underworld", ctx.player))
    else:
        ctx.multiworld.get_entrance("Zags room", ctx.player).connect(ctx.multiworld.get_region("Tartarus", ctx.player))
        ctx.multiworld.get_entrance("Exit Tartarus", ctx.player).connect(
            ctx.multiworld.get_region("Asphodel", ctx.player))
        ctx.multiworld.get_entrance("Exit Asphodel", ctx.player).connect(
            ctx.multiworld.get_region("Elyseum", ctx.player))
        ctx.multiworld.get_entrance("Exit Elyseum", ctx.player).connect(
            ctx.multiworld.get_region("Styx", ctx.player))
        ctx.multiworld.get_entrance("Late Chambers", ctx.player).connect(
            ctx.multiworld.get_region("StyxLate", ctx.player))
        ctx.multiworld.get_entrance("DieT", ctx.player).connect(ctx.multiworld.get_region("Underworld", ctx.player))
        ctx.multiworld.get_entrance("DieA", ctx.player).connect(ctx.multiworld.get_region("Underworld", ctx.player))    
        ctx.multiworld.get_entrance("DieE", ctx.player).connect(ctx.multiworld.get_region("Underworld", ctx.player))
        ctx.multiworld.get_entrance("DieS", ctx.player).connect(ctx.multiworld.get_region("Underworld", ctx.player))
        ctx.multiworld.get_entrance("DieSL", ctx.player).connect(ctx.multiworld.get_region("Underworld", ctx.player))

    #here we connect locations that depend on options
    if ctx.options.keepsakesanity:
        ctx.multiworld.get_entrance("NPCS", ctx.player).connect(
            ctx.multiworld.get_region("KeepsakesLocations", ctx.player))
        ctx.multiworld.get_entrance("ExitNPCS", ctx.player).connect(ctx.multiworld.get_region("Underworld", ctx.player))
        
    if ctx.options.weaponsanity:
        ctx.multiworld.get_entrance("Weapon Cache", ctx.player).connect(
            ctx.multiworld.get_region("WeaponsLocations", ctx.player))
        ctx.multiworld.get_entrance("ExitWeaponCache", ctx.player).connect(
            ctx.multiworld.get_region("Underworld", ctx.player))
        
    if ctx.options.storesanity:
        ctx.multiworld.get_entrance("Store Gemstones Entrance", ctx.player).connect(
            ctx.multiworld.get_region("StoreGemstones", ctx.player))
        ctx.multiworld.get_entrance("ExitGemStore", ctx.player).connect(
            ctx.multiworld.get_region("Underworld", ctx.player))
        
        ctx.multiworld.get_entrance("Store Diamonds Entrance", ctx.player).connect(
            ctx.multiworld.get_region("StoreDiamonds", ctx.player))
        ctx.multiworld.get_entrance("ExitDiamondStore", ctx.player).connect(
            ctx.multiworld.get_region("Underworld", ctx.player))
        
    
    ctx.multiworld.get_entrance("Fated Lists", ctx.player).connect(
        ctx.multiworld.get_region("FatedList", ctx.player))
    ctx.multiworld.get_entrance("ExitFatedList", ctx.player).connect(
        ctx.multiworld.get_region("Underworld", ctx.player))