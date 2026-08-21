class Tool:
    pickaxe = "Pickaxe"
    axe = "Axe"
    hoe = "Hoe"
    watering_can = "Watering Can"
    trash_can = "Trash Can"
    pan = "Pan"
    fishing_rod = "Fishing Rod"
    scythe = "Scythe"


class ToolMaterial:
    basic = "Basic"
    copper = "Copper"
    iron = "Iron"
    gold = "Gold"
    iridium = "Iridium"
    materials = [basic, copper, iron, gold, iridium]
    tiers = {
        1: basic,
        2: copper,
        3: iron,
        4: gold,
        5: iridium
    }


class FishingRod:
    training = "Training"
    bamboo = "Bamboo"
    fiberglass = "Fiberglass"
    iridium = "Iridium"
    advanced_iridium = "Advanced Iridium"
    tiers = {
        1: training,
        2: bamboo,
        3: fiberglass,
        4: iridium,
        5: advanced_iridium
    }
    material_to_tier = {
        training: 1,
        bamboo: 2,
        fiberglass: 3,
        iridium: 4,
        advanced_iridium: 5
    }


class APTool:
    pickaxe = f"Progressive {Tool.pickaxe}"
    axe = f"Progressive {Tool.axe}"
    hoe = f"Progressive {Tool.hoe}"
    watering_can = f"Progressive {Tool.watering_can}"
    trash_can = f"Progressive {Tool.trash_can}"
    fishing_rod = f"Progressive {Tool.fishing_rod}"
