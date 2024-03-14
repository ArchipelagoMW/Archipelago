class Tool:
    pickaxe = "Pickaxe"
    axe = "Axe"
    hoe = "Hoe"
    watering_can = "Watering Can"
    trash_can = "Trash Can"
    fishing_rod = "Fishing Rod"
    scythe = "Scythe"
    golden_scythe = "Golden Scythe"


class ToolMaterial:
    basic = "Basic"
    copper = "Copper"
    iron = "Iron"
    gold = "Gold"
    iridium = "Iridium"
    tiers = {0: basic,
             1: copper,
             2: iron,
             3: gold,
             4: iridium}


class APTool:
    pickaxe = f"Progressive {Tool.pickaxe}"
    axe = f"Progressive {Tool.axe}"
    hoe = f"Progressive {Tool.hoe}"
    watering_can = f"Progressive {Tool.watering_can}"
    trash_can = f"Progressive {Tool.trash_can}"
    fishing_rod = f"Progressive {Tool.fishing_rod}"