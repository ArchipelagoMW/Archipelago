if self.has_mod("Stardew Valley Expanded"):
    self.item_rules.update({
        "Aged Blue Moon Wine": self.can_reach_region(SVERegion.sophias_house) & self.can_spend_money(28000),
        "Big Bark Burger": self.can_cook() & self.has(["Puppyfish", "Bread", "Oil"]) &
                           self.has_relationship("Gus", 5) & self.can_spend_money(5500) &
                           self.can_reach_region(SVRegion.saloon),
        "Blue Moon Wine": self.can_reach_region(SVERegion.sophias_house) & self.can_spend_money(3000),
        "Fungus Seed": self.can_reach_region(SVERegion.highlands_cavern) & self.has_good_weapon(),
        "Glazed Butterfish": self.can_cook() & self.has(["Butterfish", "Wheat", "Oil"]) &
                             self.has_relationship("Gus", 10) & self.can_spend_money(4000),
        "Green Mushroom": self.can_reach_region(SVERegion.highlands) & self.has_tool("Axe", "Iron"),
        "Monster Fruit": self.has_season("Summer") & self.has("Stalk Seed"),
        "Monster Mushroom": self.has_season("Fall") & self.has("Fungus Seed"),
        "Ornate Treasure Chest": self.can_reach_region(SVERegion.highlands) & self.has_galaxy_weapon() &
                                 self.can_cook() & self.has_tool("Axe", "Iron"),
        "Slime Berry": self.has_season("Spring") & self.has("Slime Seed"),
        "Slime Seed": self.can_reach_region(SVERegion.highlands) & self.has_good_weapon(),
        "Stalk Seed": self.can_reach_region(SVERegion.highlands) & self.has_good_weapon(),
        "Swirl Stone": self.can_reach_region(SVERegion.crimson_badlands) & self.has_great_weapon(),
        "Void Delight": self.has("Void Eel") & self.has("Void Essence") & self.has("Solar Essence"),
        "Void Pebble": self.can_reach_region(SVERegion.crimson_badlands) & self.has_galaxy_weapon(),
        "Void Root": self.has_season("Winter") & self.has("Void Seed"),
        "Void Salmon Sushi": self.has("Void Salmon") & self.has("Void Mayonnaise") & self.has("Seaweed"),
        "Void Seed": self.can_reach_region(SVERegion.highlands_cavern) & self.has_good_weapon(),
        "Void Soul": self.can_reach_region(SVERegion.crimson_badlands) & self.has_good_weapon() &
                     self.can_cook(),
    })

self.sve_location_rules.update({
    "Bear: Baked Berry Oatmeal Recipe": self.can_complete_quest("Strange Note") & self.can_spend_money(12500),
    "Bear: Flower Cookie Recipe": self.can_complete_quest("Strange Note") & self.can_spend_money(8750),
    "Purple Junimo: Super Starfruit": self.can_earn_relationship("Apples", 10) &
                                      self.can_reach_region(
                                          SVERegion.purple_junimo_shop) & self.can_spend_money(80000),
    "Alesia: Tempered Galaxy Dagger": self.can_reach_region(SVERegion.alesia_shop) & self.has_galaxy_weapon() &
                                      self.can_spend_money(350000) & self.has_lived_months(3),
    "Issac: Tempered Galaxy Sword": self.can_reach_region(SVERegion.issac_shop) & self.has_galaxy_weapon() &
                                    self.can_spend_money(600000),
    "Issac: Tempered Galaxy Hammer": self.can_reach_region(SVERegion.issac_shop) & self.has_galaxy_weapon() &
                                     self.can_spend_money(400000),
    "Lance's Diamond Wand": self.can_complete_quest("Monster Crops") & self.can_reach_region(
        SVERegion.lances_house),
    "Volcano Caldera Prismatic Shard": self.can_reach_region(SVRegion.ginger_island) & self.has_good_weapon(),
})

if "Stardew Valley Expanded" in self.options[options.Mods]:
    self.quest_rules.update({
        "The Railroad Boulder": self.received("Skull Key") & self.has(["Furnace", "Iridium Ore", "Coal"]) &
                                self.can_reach_region("Clint's Blacksmith"),
        "Grandpa's Shed": self.has(["Hardwood", "Iron Bar", "Battery Pack", "Stone"]) &
                          self.can_reach_region(SVERegion.grandpas_shed_interior),
        "Marlon's Boat": self.has(["Void Essence", "Solar Essence", "Slime", "Bat Wing", "Bug Meat"]) &
                         self.can_meet("Lance") & self.can_reach_region(SVERegion.guild_summit),
        "Aurora Vineyard": self.can_complete_community_center() & self.has("Starfruit") &
                           self.can_reach_region(SVERegion.aurora_vineyard) & self.has_year_two(),
        "Monster Crops": self.has(["Monster Mushroom", "Slime Berry", "Monster Fruit", "Void Root"]),
        "Void Soul": self.can_reach_region(SVRegion.sewers) & self.has("Void Soul"),
    })
