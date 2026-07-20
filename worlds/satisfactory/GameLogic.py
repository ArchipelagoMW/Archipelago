from typing import Optional
from dataclasses import dataclass
from enum import IntEnum


class PowerInfrastructureLevel(IntEnum):
    Basic = 1
    Automated = 2
    Advanced = 3
    Complex = 4

    def to_name(self) -> str:
        return "Power level: " + self.name


liquids: set[str] = {
    "Water",
    "Liquid Biofuel",
    "Crude Oil",
    "Fuel",
    "Heavy Oil Residue",
    "Turbofuel",
    "Alumina Solution",
    "Sulfuric Acid",
    "Nitrogen Gas",
    "Nitric Acid",
    "Dissolved Silica",
    "Rocket Fuel",
    "Ionized Fuel",
    "Excited Photonic Matter",
    "Dark Matter Residue"
}

radio_actives: set[str] = {
    "Uranium",
    "Encased Uranium Cell",
    "Uranium Fuel Rod"
    "Uranium Waste",
    "Non-fissile Uranium",
    "Plutonium Pellet",
    "Encased Plutonium Cell",
    "Plutonium Fuel Rod",
    "Plutonium Waste",
    "Ficsonium",
    "Ficsonium Fuel Rod"
}


class Recipe:
    """
    Relationship between components and what is required to produce them (input ingredients, production building, etc.)
    Not all recipes are Satisfactory FGRecipes - for example, Water has a Recipe, but it's not an FGRecipe
    """
    name: str
    building: Optional[str]
    inputs: Optional[tuple[str, ...]]
    minimal_belt_speed: int
    handcraftable: bool
    implicitly_unlocked: bool
    """No explicit location/item is needed to unlock this recipe, you have access as soon as dependencies are met 
    (ex. Water, Leaves, tutorial starting items)"""
    additional_outputs: Optional[tuple[str, ...]]
    minimal_phase: int

    needs_pipes: bool
    is_radio_active: bool

    def __init__(self, name: str, building: Optional[str] = None, inputs: Optional[tuple[str, ...]] = None,
                minimal_belt_speed: int = 1, handcraftable: bool = False, implicitly_unlocked: bool = False,
                additional_outputs: Optional[tuple[str, ...]] = None, minimal_phase: Optional[int] = 1):
        self.name = "Recipe: " + name
        self.building = building
        self.inputs = inputs
        self.minimal_belt_speed = minimal_belt_speed
        self.handcraftable = handcraftable
        self.implicitly_unlocked = implicitly_unlocked
        self.additional_outputs = additional_outputs
        self.minimal_phase = minimal_phase

        all_parts: list[str] = [name]
        if inputs:
            all_parts += inputs
        if additional_outputs:
            all_parts += additional_outputs

        self.needs_pipes = not liquids.isdisjoint(all_parts)
        self.is_radio_active = not radio_actives.isdisjoint(all_parts)


class Building(Recipe):
    power_requirement: Optional[PowerInfrastructureLevel]
    can_produce: bool

    def __init__(self, name: str, inputs: Optional[tuple[str, ...]] = None,
                 power_requirement: Optional[PowerInfrastructureLevel] = None, can_produce: bool = True,
                 implicitly_unlocked: bool = False):
        super().__init__(name, None, inputs, handcraftable=True, implicitly_unlocked=implicitly_unlocked)
        self.name = "Building: " + name
        self.power_requirement = power_requirement
        self.can_produce = can_produce
        self.implicitly_unlocked = implicitly_unlocked


class MamNode:
    name: str
    unlock_cost: dict[str, int]
    """All game items must be submitted to purchase this MamNode"""
    depends_on: tuple[str, ...]
    """At least one of these prerequisite MamNodes must be unlocked to purchase this MamNode"""
    minimal_phase: Optional[int]

    def __init__(self, name: str, unlock_cost: dict[str, int], depends_on: tuple[str, ...],
                 minimal_phase: Optional[int] = 1):
        self.name = name
        self.unlock_cost = unlock_cost
        self.depends_on = depends_on
        self.minimal_phase = minimal_phase


class MamTree:
    access_items: tuple[str, ...]
    """At least one of these game items must enter the player inventory for this MamTree to be available"""
    nodes: tuple[MamNode, ...]

    def __init__(self, access_items: tuple[str, ...], nodes: tuple[MamNode, ...]):
        self.access_items = access_items
        self.nodes = nodes


@dataclass
class DropPodData:
    x: int
    y: int
    z: int
    item: Optional[str]
    power: int
    gassed: Optional[bool] = None
    radioactive: Optional[bool] = None


class GameLogic:
    indirect_recipes: dict[str, str] = {
        "Recipe: Quartz Purification": "Recipe: Distilled Silica"
    }

    recipes: dict[str, tuple[Recipe, ...]] = {
        # This Dict should only contain items that are used somewhere in a logic chain

        # Exploration Items
        "Leaves": (
            Recipe("Leaves", handcraftable=True, implicitly_unlocked=True), ),
        "Wood": (
            Recipe("Wood", handcraftable=True, implicitly_unlocked=True), ),
        "Hatcher Remains": (
            Recipe("Hatcher Remains", handcraftable=True, implicitly_unlocked=True), ),
        "Hog Remains": (
            Recipe("Hog Remains", handcraftable=True, implicitly_unlocked=True), ),
        "Plasma Spitter Remains": (
            Recipe("Plasma Spitter Remains", handcraftable=True, implicitly_unlocked=True), ),
        "Stinger Remains": (
            Recipe("Stinger Remains", handcraftable=True, implicitly_unlocked=True), ),
        "Mycelia": (
            Recipe("Mycelia", handcraftable=True, implicitly_unlocked=True), ),
        "Beryl Nut": (
            Recipe("Beryl Nut", handcraftable=True, implicitly_unlocked=True), ),
        "Paleberry": (
            Recipe("Paleberry", handcraftable=True, implicitly_unlocked=True), ),
        "Bacon Agaric": (
            Recipe("Bacon Agaric", handcraftable=True, implicitly_unlocked=True), ),
        "Blue Power Slug": (
            Recipe("Blue Power Slug", handcraftable=True, implicitly_unlocked=True), ),
        "Yellow Power Slug": (
            Recipe("Yellow Power Slug", handcraftable=True, implicitly_unlocked=True), ),
        "Purple Power Slug": (
            Recipe("Purple Power Slug", handcraftable=True, implicitly_unlocked=True), ),
        "Hard Drive": (
            Recipe("Hard Drive", handcraftable=True, implicitly_unlocked=True), ),
        "Mercer Sphere": (
            Recipe("Mercer Sphere", handcraftable=True, implicitly_unlocked=True), ),
        "Somersloop": (
            Recipe("Somersloop", handcraftable=True, implicitly_unlocked=True), ),

        # Raw Resources
        "Water": (
            Recipe("Water", "Water Extractor", implicitly_unlocked=True),
            Recipe("Water (Resource Well)", "Resource Well Pressurizer", implicitly_unlocked=True, minimal_phase=2)),
        "Limestone": (
            Recipe("Limestone", "Miner Mk.1", handcraftable=True, implicitly_unlocked=True), ),
        "Raw Quartz": (
            Recipe("Raw Quartz", "Miner Mk.1", handcraftable=True, implicitly_unlocked=True), ),
        "Iron Ore": (
            Recipe("Iron Ore", "Miner Mk.1", handcraftable=True, implicitly_unlocked=True), ),
        "Copper Ore": (
            Recipe("Copper Ore", "Miner Mk.1", handcraftable=True, implicitly_unlocked=True), ),
        "Coal": (
            Recipe("Coal", "Miner Mk.1", handcraftable=True, implicitly_unlocked=True), ),
        "Sulfur": (
            Recipe("Sulfur", "Miner Mk.1", handcraftable=True, implicitly_unlocked=True), ),
        "Caterium Ore": (
            Recipe("Caterium Ore", "Miner Mk.1", handcraftable=True, implicitly_unlocked=True), ),
        "Crude Oil": (
            Recipe("Crude Oil", "Oil Extractor", implicitly_unlocked=True),
            Recipe("Crude Oil (Resource Well)", "Resource Well Pressurizer", implicitly_unlocked=True, minimal_phase=2)),
        "Bauxite": (
            Recipe("Bauxite", "Miner Mk.1", handcraftable=True, implicitly_unlocked=True, minimal_phase=2), ),
        "Nitrogen Gas": (
            Recipe("Nitrogen Gas", "Resource Well Pressurizer", implicitly_unlocked=True, minimal_phase=2), ),
        "Uranium": (
            Recipe("Uranium", "Miner Mk.1", handcraftable=True, implicitly_unlocked=True, minimal_phase=2), ),

        # Special Items
        "Uranium Waste": (
            Recipe("Uranium Waste", "Nuclear Power Plant", ("Uranium Fuel Rod", "Water"), implicitly_unlocked=True, minimal_phase=2), ),
        # "Plutonium Waste": (
        #    Recipe("Plutonium Waste", "Nuclear Power Plant", ("Plutonium Fuel Rod", "Water"), implicitly_unlocked=True), ),

        # Recipes
        "Reinforced Iron Plate": (
            Recipe("Reinforced Iron Plate", "Assembler", ("Iron Plate", "Screw")),
            Recipe("Adhered Iron Plate", "Assembler", ("Iron Plate", "Rubber")),
            Recipe("Bolted Iron Plate", "Assembler", ("Iron Plate", "Screw"), minimal_belt_speed=3),
            Recipe("Stitched Iron Plate", "Assembler", ("Iron Plate", "Wire"))),
        "Rotor": (
            Recipe("Rotor", "Assembler", ("Iron Rod", "Screw"), minimal_belt_speed=2, handcraftable=True),
            Recipe("Copper Rotor", "Assembler", ("Copper Sheet", "Screw"), minimal_belt_speed=3),
            Recipe("Steel Rotor", "Assembler", ("Steel Pipe", "Wire"))),
        "Stator": (
            Recipe("Stator", "Assembler", ("Steel Pipe", "Wire"), handcraftable=True),
            Recipe("Quickwire Stator", "Assembler", ("Steel Pipe", "Quickwire"))),
        "Plastic": (
            Recipe("Plastic", "Refinery", ("Crude Oil", ), additional_outputs=("Heavy Oil Residue", )),
            Recipe("Residual Plastic", "Refinery", ("Polymer Resin", "Water")),
            Recipe("Recycled Plastic", "Refinery", ("Rubber", "Fuel"))),
        "Rubber": (
            Recipe("Rubber", "Refinery", ("Crude Oil", ), additional_outputs=("Heavy Oil Residue", )),
            Recipe("Residual Rubber", "Refinery", ("Polymer Resin", "Water")),
            Recipe("Recycled Rubber", "Refinery", ("Plastic", "Fuel"))),
        "Iron Plate": (
            Recipe("Iron Plate", "Constructor", ("Iron Ingot", )),
            Recipe("Coated Iron Plate", "Assembler", ("Iron Ingot", "Plastic"), minimal_belt_speed=2),
            Recipe("Steel Cast Plate", "Foundry", ("Iron Ingot", "Steel Ingot"))),
        "Iron Rod": (
            Recipe("Iron Rod", "Constructor", ("Iron Ingot", )),
            Recipe("Steel Rod", "Constructor", ("Steel Ingot", )),
            Recipe("Aluminum Rod", "Constructor", ("Aluminum Ingot", ))),
        "Screw": (
            Recipe("Screw", "Constructor", ("Iron Rod", )),
            Recipe("Cast Screw", "Constructor", ("Iron Ingot", )),
            Recipe("Steel Screw", "Constructor", ("Steel Beam", ), minimal_belt_speed=3)),
        "Wire": (
            Recipe("Wire", "Constructor", ("Copper Ingot", )),
            Recipe("Fused Wire", "Assembler", ("Copper Ingot", "Caterium Ingot"), minimal_belt_speed=2),
            Recipe("Iron Wire", "Constructor", ("Iron Ingot", )),
            Recipe("Caterium Wire", "Constructor", ("Caterium Ingot", ), minimal_belt_speed=2)),
        "Cable": (
            Recipe("Cable", "Constructor", ("Wire", ), handcraftable=True, implicitly_unlocked=True),
            Recipe("Coated Cable", "Refinery", ("Wire", "Heavy Oil Residue"), minimal_belt_speed=2),
            Recipe("Insulated Cable", "Assembler", ("Wire", "Rubber"), minimal_belt_speed=2),
            Recipe("Quickwire Cable", "Assembler", ("Quickwire", "Rubber"))),
        "Quickwire": (
            Recipe("Quickwire", "Constructor", ("Caterium Ingot", ), handcraftable=True),
            Recipe("Fused Quickwire", "Assembler", ("Caterium Ingot", "Copper Ingot"), minimal_belt_speed=2)),
        "Copper Sheet": (
            Recipe("Copper Sheet", "Constructor", ("Copper Ingot", ), handcraftable=True),
            Recipe("Steamed Copper Sheet", "Refinery", ("Copper Ingot", "Water"))),
        "Steel Pipe": (
            Recipe("Steel Pipe", "Constructor", ("Steel Ingot", ), handcraftable=True),
            Recipe("Iron Pipe", "Constructor", ("Iron Ingot", ), minimal_belt_speed=2),
            Recipe("Molded Steel Pipe", "Foundry", ("Steel Ingot", "Concrete"))),
        "Steel Beam": (
            Recipe("Steel Beam", "Constructor", ("Steel Ingot", ), handcraftable=True),
            Recipe("Aluminum Beam", "Constructor", ("Aluminum Ingot", ), minimal_phase=2),
            Recipe("Molded Beam", "Foundry", ("Steel Ingot", "Concrete"), minimal_belt_speed=2)),
        "Heavy Oil Residue": (
            Recipe("Heavy Oil Residue", "Refinery", ("Crude Oil", ), additional_outputs=("Polymer Resin", )),
            Recipe("Plastic", "Refinery", ("Crude Oil", ), additional_outputs=("Plastic", )),
            Recipe("Rubber", "Refinery", ("Crude Oil", ), additional_outputs=("Rubber", )),
            Recipe("Polymer Resin", "Refinery", ("Crude Oil", ), additional_outputs=("Polymer Resin", ), minimal_belt_speed=3)),
        "Polymer Resin": (
            Recipe("Polymer Resin", "Refinery", ("Crude Oil", ), additional_outputs=("Heavy Oil Residue", ), minimal_belt_speed=2),
            Recipe("Fuel", "Refinery", ("Crude Oil", ), additional_outputs=("Fuel", )),
            Recipe("Heavy Oil Residue", "Refinery", ("Crude Oil", ), additional_outputs=("Heavy Oil Residue", ), minimal_belt_speed=3)),
        "Fuel": (
            Recipe("Fuel", "Refinery", ("Crude Oil", ), additional_outputs=("Polymer Resin", )),
            Recipe("Diluted Fuel", "Blender", ("Heavy Oil Residue", "Water"), minimal_phase=2),
            Recipe("Residual Fuel", "Refinery", ("Heavy Oil Residue", ))),
        "Concrete": (
            Recipe("Concrete", "Constructor", ("Limestone", )),
            Recipe("Fine Concrete", "Assembler", ("Limestone", "Silica")),
            Recipe("Rubber Concrete", "Assembler", ("Limestone", "Rubber")),
            Recipe("Wet Concrete", "Refinery", ("Limestone", "Water"), minimal_belt_speed=2)),
        "Silica": (
            Recipe("Silica", "Constructor", ("Raw Quartz", ), handcraftable=True),
            Recipe("Alumina Solution", "Refinery", ("Bauxite", "Water"), additional_outputs=("Alumina Solution", ), minimal_belt_speed=2, minimal_phase=2),
            Recipe("Cheap Silica", "Assembler", ("Raw Quartz", "Limestone")),
            Recipe("Distilled Silica", "Blender", ("Dissolved Silica", "Limestone", "Water"), additional_outputs=("Water", ), minimal_phase=2)),
        "Dissolved Silica": (
            Recipe("Quartz Purification", "Refinery", ("Raw Quartz", "Nitric Acid"), additional_outputs=("Quartz Crystal", ), minimal_belt_speed=2, minimal_phase=2), ),
        "Quartz Crystal": (
            Recipe("Quartz Crystal", "Constructor", ("Raw Quartz", ), handcraftable=True),
            Recipe("Pure Quartz Crystal", "Refinery", ("Raw Quartz", "Water"), minimal_belt_speed=2),
            Recipe("Fused Quartz Crystal", "Foundry", ("Raw Quartz", "Coal"), minimal_belt_speed=2),
            Recipe("Quartz Purification", "Refinery", ("Raw Quartz", "Nitric Acid"), additional_outputs=("Dissolved Silica", ), minimal_belt_speed=2, minimal_phase=2)),
        "Iron Ingot": (
            Recipe("Iron Ingot", "Smelter", ("Iron Ore", )),
            Recipe("Pure Iron Ingot", "Refinery", ("Iron Ore", "Water"), minimal_belt_speed=2),
            Recipe("Iron Alloy Ingot", "Foundry", ("Iron Ore", "Copper Ore")),
            Recipe("Basic Iron Ingot", "Foundry", ("Iron Ore", "Limestone")),
            Recipe("Leached Iron ingot", "Refinery", ("Iron Ore", "Sulfuric Acid"), minimal_belt_speed=2)),
        "Steel Ingot": (
            Recipe("Steel Ingot", "Foundry", ("Iron Ore", "Coal"), handcraftable=True),
            Recipe("Coke Steel Ingot", "Foundry", ("Iron Ore", "Petroleum Coke"), minimal_belt_speed=2),
            Recipe("Compacted Steel Ingot", "Foundry", ("Iron Ore", "Compacted Coal")),
            Recipe("Solid Steel Ingot", "Foundry", ("Iron Ingot", "Coal"))),
        "Copper Ingot": (
            Recipe("Copper Ingot", "Smelter", ("Copper Ore", )),
            Recipe("Copper Alloy Ingot", "Foundry", ("Copper Ore", "Iron Ore"), minimal_belt_speed=2),
            Recipe("Pure Copper Ingot", "Refinery", ("Copper Ore", "Water")),
            Recipe("Leached Copper Ingot", "Refinery", ("Copper Ore", "Sulfuric Acid"), minimal_belt_speed=2),
            Recipe("Tempered Copper Ingot", "Foundry", ("Copper Ore", "Petroleum Coke"))),
        "Caterium Ingot": (
            Recipe("Caterium Ingot", "Smelter", ("Caterium Ore", ), handcraftable=True),
            Recipe("Pure Caterium Ingot", "Refinery", ("Caterium Ore", "Water")),
            Recipe("Leached Caterium Ingot", "Refinery", ("Caterium Ore", "Sulfuric Acid")),
            Recipe("Tempered Caterium Ingot", "Foundry", ("Caterium Ore", "Petroleum Coke"))),
        "Petroleum Coke": (
            Recipe("Petroleum Coke", "Refinery", ("Heavy Oil Residue", ), minimal_belt_speed=2), ),
        "Compacted Coal": (
            Recipe("Compacted Coal", "Assembler", ("Coal", "Sulfur")), ),
        "Motor": (
            Recipe("Motor", "Assembler", ("Rotor", "Stator"), handcraftable=True),
            Recipe("Rigor Motor", "Manufacturer", ("Rotor", "Stator", "Crystal Oscillator")),
            Recipe("Electric Motor", "Assembler", ("Electromagnetic Control Rod", "Rotor"))),
        "Modular Frame": (
            Recipe("Modular Frame", "Assembler", ("Reinforced Iron Plate", "Iron Rod"), handcraftable=True),
            Recipe("Bolted Frame", "Assembler", ("Reinforced Iron Plate", "Screw"), minimal_belt_speed=3),
            Recipe("Steeled Frame", "Assembler", ("Reinforced Iron Plate", "Steel Pipe"))),
        "Heavy Modular Frame": (
            Recipe("Heavy Modular Frame", "Manufacturer", ("Modular Frame", "Steel Pipe", "Encased Industrial Beam", "Screw"), minimal_belt_speed=3, handcraftable=True),
            Recipe("Heavy Flexible Frame", "Manufacturer", ("Modular Frame", "Encased Industrial Beam", "Rubber", "Screw"), minimal_belt_speed=4),
            Recipe("Heavy Encased Frame", "Manufacturer", ("Modular Frame", "Encased Industrial Beam", "Steel Pipe", "Concrete"))),
        "Encased Industrial Beam": (
            Recipe("Encased Industrial Beam", "Assembler", ("Steel Beam", "Concrete"), handcraftable=True),
            Recipe("Encased Industrial Pipe", "Assembler", ("Steel Pipe", "Concrete"))),
        "Computer": (
            Recipe("Computer", "Manufacturer", ("Circuit Board", "Cable", "Plastic"), minimal_belt_speed=3, handcraftable=True),
            Recipe("Crystal Computer", "Assembler", ("Circuit Board", "Crystal Oscillator")),
            Recipe("Caterium Computer", "Manufacturer", ("Circuit Board", "Quickwire", "Rubber"), minimal_belt_speed=2)),
        "Circuit Board": (
            Recipe("Circuit Board", "Assembler", ("Copper Sheet", "Plastic"), handcraftable=True),
            Recipe("Electrode Circuit Board", "Assembler", ("Rubber", "Petroleum Coke")),
            Recipe("Silicon Circuit Board", "Assembler", ("Copper Sheet", "Silica")),
            Recipe("Caterium Circuit Board", "Assembler", ("Plastic", "Quickwire"))),
        "Crystal Oscillator": (
            Recipe("Crystal Oscillator", "Manufacturer", ("Quartz Crystal", "Cable", "Reinforced Iron Plate"), handcraftable=True),
            Recipe("Insulated Crystal Oscillator", "Manufacturer", ("Quartz Crystal", "Rubber", "AI Limiter"))),
        "AI Limiter": (
            Recipe("AI Limiter", "Assembler", ("Copper Sheet", "Quickwire"), minimal_belt_speed=2, handcraftable=True),
            Recipe("Plastic AI Limiter", "Assembler", ("Quickwire", "Plastic"), minimal_belt_speed=2)),
        "Electromagnetic Control Rod": (
            Recipe("Electromagnetic Control Rod", "Assembler", ("Stator", "AI Limiter"), handcraftable=True),
            Recipe("Electromagnetic Connection Rod", "Assembler", ("Stator", "High-Speed Connector"))),
        "High-Speed Connector": (
            Recipe("High-Speed Connector", "Manufacturer", ("Quickwire", "Cable", "Circuit Board"), minimal_belt_speed=3, handcraftable=True),
            Recipe("Silicon High-Speed Connector", "Manufacturer", ("Quickwire", "Silica", "Circuit Board"), minimal_belt_speed=2)),
        "Smart Plating": (
            Recipe("Smart Plating", "Assembler", ("Reinforced Iron Plate", "Rotor")),
            Recipe("Plastic Smart Plating", "Manufacturer", ("Reinforced Iron Plate", "Rotor", "Plastic"))),
        "Versatile Framework": (
            Recipe("Versatile Framework", "Assembler", ("Modular Frame", "Steel Beam"), minimal_phase=2),
            Recipe("Flexible Framework", "Manufacturer", ("Modular Frame", "Steel Beam", "Rubber"), minimal_phase=2)),
        "Automated Wiring": (
            Recipe("Automated Wiring", "Assembler", ("Stator", "Cable"), minimal_phase=2),
            Recipe("Automated Speed Wiring", "Manufacturer", ("Stator", "Wire", "High-Speed Connector"), minimal_belt_speed=2, minimal_phase=2)),
        "Modular Engine": (
            Recipe("Modular Engine", "Manufacturer", ("Motor", "Rubber", "Smart Plating"), minimal_phase=3), ),
        "Adaptive Control Unit": (
            Recipe("Adaptive Control Unit", "Manufacturer", ("Automated Wiring", "Circuit Board", "Heavy Modular Frame", "Computer"), minimal_phase=3), ),
        "Portable Miner": (
            Recipe("Portable Miner", "Equipment Workshop", ("Iron Rod", "Iron Plate"), handcraftable=True, minimal_belt_speed=0, implicitly_unlocked=True),
            Recipe("Automated Miner", "Assembler", ("Steel Pipe", "Iron Plate")), ),
        "Alumina Solution": (
            Recipe("Alumina Solution", "Refinery", ("Bauxite", "Water"), additional_outputs=("Silica", ), minimal_belt_speed=2, minimal_phase=2),
            Recipe("Sloppy Alumina", "Refinery", ("Bauxite", "Water"), minimal_belt_speed=3, minimal_phase=2)),
        "Aluminum Scrap": (
            Recipe("Aluminum Scrap", "Refinery", ("Alumina Solution", "Coal"), additional_outputs=("Water", ), minimal_belt_speed=4, minimal_phase=2),
            Recipe("Electrode Aluminum Scrap", "Refinery", ("Alumina Solution", "Petroleum Coke"), additional_outputs=("Water", ), minimal_belt_speed=4, minimal_phase=2),
            Recipe("Instant Scrap", "Blender", ("Bauxite", "Coal", "Sulfuric Acid", "Water"), additional_outputs=("Water", ), minimal_belt_speed=3, minimal_phase=2)),
        "Aluminum Ingot": (
            Recipe("Aluminum Ingot", "Foundry", ("Aluminum Scrap", "Silica"), minimal_belt_speed=2, handcraftable=True, minimal_phase=2),
            Recipe("Pure Aluminum Ingot", "Smelter", ("Aluminum Scrap", ), minimal_phase=2)),
        "Alclad Aluminum Sheet": (
            Recipe("Alclad Aluminum Sheet", "Assembler", ("Aluminum Ingot", "Copper Ingot"), handcraftable=True, minimal_phase=2), ),
        "Aluminum Casing": (
            Recipe("Aluminum Casing", "Constructor", ("Alclad Aluminum Sheet", ), handcraftable=True, minimal_phase=2),
            Recipe("Alclad Casing", "Assembler", ("Aluminum Ingot", "Copper Ingot"), minimal_phase=2)),
        "Heat Sink": (
            Recipe("Heat Sink", "Assembler", ("Alclad Aluminum Sheet", "Silica"), minimal_belt_speed=2, handcraftable=True, minimal_phase=2),
            Recipe("Heat Exchanger", "Assembler", ("Aluminum Casing", "Rubber"), minimal_belt_speed=3, minimal_phase=2)),
        "Nitric Acid": (
            Recipe("Nitric Acid", "Blender", ("Nitrogen Gas", "Water", "Iron Plate"), minimal_phase=2), ),
        "Fused Modular Frame": (
            Recipe("Fused Modular Frame", "Blender", ("Heavy Modular Frame", "Aluminum Casing", "Nitrogen Gas"), minimal_belt_speed=2, minimal_phase=2),
            Recipe("Heat-Fused Frame", "Blender", ("Heavy Modular Frame", "Aluminum Ingot", "Nitric Acid", "Fuel"), minimal_belt_speed=3, minimal_phase=2)),
        "Radio Control Unit": (
            Recipe("Radio Control Unit", "Manufacturer", ("Aluminum Casing", "Crystal Oscillator", "Computer"), handcraftable=True, minimal_phase=2),
            Recipe("Radio Connection Unit", "Manufacturer", ("Heat Sink", "High-Speed Connector", "Quartz Crystal"), minimal_phase=2),
            Recipe("Radio Control System", "Manufacturer", ("Crystal Oscillator", "Circuit Board", "Aluminum Casing", "Rubber"), minimal_belt_speed=2, minimal_phase=2)),
        "Pressure Conversion Cube": (
            Recipe("Pressure Conversion Cube", "Assembler", ("Fused Modular Frame", "Radio Control Unit"), handcraftable=True, minimal_phase=2), ),
        "Cooling System": (
            Recipe("Cooling System", "Blender", ("Heat Sink", "Rubber", "Water", "Nitrogen Gas"), minimal_phase=2),
            Recipe("Cooling Device", "Blender", ("Heat Sink", "Motor", "Nitrogen Gas"), minimal_phase=2)),
        "Turbo Motor": (
            Recipe("Turbo Motor", "Manufacturer", ("Cooling System", "Radio Control Unit", "Motor", "Rubber"), handcraftable=True, minimal_phase=2),
            Recipe("Turbo Electric Motor", "Manufacturer", ("Motor", "Radio Control Unit", "Electromagnetic Control Rod", "Rotor"), minimal_phase=2),
            Recipe("Turbo Pressure Motor", "Manufacturer", ("Motor", "Pressure Conversion Cube", "Packaged Nitrogen Gas", "Stator"), minimal_phase=2)),
        "Battery": (
            Recipe("Battery", "Blender", ("Sulfuric Acid", "Alumina Solution", "Aluminum Casing"), additional_outputs=("Water", ), minimal_phase=2),
            Recipe("Classic Battery", "Manufacturer", ("Sulfur", "Alclad Aluminum Sheet", "Plastic", "Wire"), minimal_belt_speed=2, minimal_phase=2)),
        "Supercomputer": (
            Recipe("Supercomputer", "Manufacturer", ("Computer", "AI Limiter", "High-Speed Connector", "Plastic"), handcraftable=True, minimal_phase=2),
            Recipe("OC Supercomputer", "Assembler", ("Radio Control Unit", "Cooling System"), minimal_phase=2),
            Recipe("Super-State Computer", "Manufacturer", ("Computer", "Electromagnetic Control Rod", "Battery", "Wire"), minimal_phase=2)),
        "Sulfuric Acid": (
            Recipe("Sulfuric Acid", "Refinery", ("Sulfur", "Water")), ),
        "Encased Uranium Cell": (
            Recipe("Encased Uranium Cell", "Blender", ("Uranium", "Concrete", "Sulfuric Acid"), additional_outputs=("Sulfuric Acid", )),
            Recipe("Infused Uranium Cell", "Manufacturer", ("Uranium", "Silica", "Sulfur", "Quickwire"), minimal_belt_speed=2)),
        "Uranium Fuel Rod": (
            Recipe("Uranium Fuel Rod", "Manufacturer", ("Encased Uranium Cell", "Encased Industrial Beam", "Electromagnetic Control Rod")),
            Recipe("Uranium Fuel Unit", "Manufacturer", ("Encased Uranium Cell", "Electromagnetic Control Rod", "Crystal Oscillator", "Rotor"))),
        "Non-fissile Uranium": (
            Recipe("Non-fissile Uranium", "Blender", ("Uranium Waste", "Silica", "Nitric Acid", "Sulfuric Acid"), additional_outputs=("Water", )),
            Recipe("Fertile Uranium", "Blender", ("Uranium", "Uranium Waste", "Nitric Acid", "Sulfuric Acid"), additional_outputs=("Water", ), minimal_belt_speed=2)),
        "Plutonium Pellet": (
            Recipe("Plutonium Pellet", "Particle Accelerator", ("Non-fissile Uranium", "Uranium Waste"), minimal_belt_speed=2), ),
        "Encased Plutonium Cell": (
            Recipe("Encased Plutonium Cell", "Assembler", ("Plutonium Pellet", "Concrete")),
            Recipe("Instant Plutonium Cell", "Particle Accelerator", ("Non-fissile Uranium", "Aluminum Casing"), minimal_belt_speed=2)),
        "Plutonium Fuel Rod": (
            Recipe("Plutonium Fuel Rod", "Manufacturer", ("Encased Plutonium Cell", "Steel Beam", "Electromagnetic Control Rod", "Heat Sink")),
            Recipe("Plutonium Fuel Unit", "Assembler", ("Encased Plutonium Cell", "Pressure Conversion Cube"))),
        "Gas Filter": (
            Recipe("Gas Filter", "Manufacturer", ("Coal", "Rubber", "Fabric"), handcraftable=True), ),
        "Iodine-Infused Filter": (
            Recipe("Iodine-Infused Filter", "Manufacturer", ("Gas Filter", "Quickwire", "Aluminum Casing"), handcraftable=True, minimal_phase=2), ),
        "Hazmat Suit": (
            Recipe("Hazmat Suit", "Equipment Workshop", ("Rubber", "Plastic", "Fabric", "Alclad Aluminum Sheet"), handcraftable=True, minimal_phase=2), ),
        "Assembly Director System": (
            Recipe("Assembly Director System", "Assembler", ("Adaptive Control Unit", "Supercomputer"), minimal_phase=4), ),
        "Magnetic Field Generator": (
            Recipe("Magnetic Field Generator", "Assembler", ("Versatile Framework", "Electromagnetic Control Rod"), minimal_phase=4), ),
        "Copper Powder": (
            Recipe("Copper Powder", "Constructor", ("Copper Ingot", ), handcraftable=True), ),
        "Nuclear Pasta": (
            Recipe("Nuclear Pasta", "Particle Accelerator", ("Copper Powder", "Pressure Conversion Cube"), minimal_phase=2), ),
        "Thermal Propulsion Rocket": (
            Recipe("Thermal Propulsion Rocket", "Manufacturer", ("Modular Engine", "Turbo Motor", "Cooling System", "Fused Modular Frame"), minimal_phase=4), ),
        "Alien Protein": (
            Recipe("Hatcher Protein", "Constructor", ("Hatcher Remains", ), handcraftable=True),
            Recipe("Hog Protein", "Constructor", ("Hog Remains", ), handcraftable=True),
            Recipe("Spitter Protein", "Constructor", ("Plasma Spitter Remains", ), handcraftable=True),
            Recipe("Stinger Protein", "Constructor", ("Stinger Remains", ), handcraftable=True)),
        "Biomass": (
            Recipe("Biomass (Leaves)", "Constructor", ("Leaves", ), minimal_belt_speed=2, handcraftable=True, implicitly_unlocked=True),
            Recipe("Biomass (Wood)", "Constructor", ("Wood", ), minimal_belt_speed=4, handcraftable=True, implicitly_unlocked=True),
            Recipe("Biomass (Mycelia)", "Constructor", ("Mycelia", ), minimal_belt_speed=3, handcraftable=True),
            Recipe("Biomass (Alien Protein)", "Constructor", ("Alien Protein", ), minimal_belt_speed=4, handcraftable=True)),
        "Fabric": (
            Recipe("Fabric", "Assembler", ("Biomass", "Mycelia"), handcraftable=True, minimal_belt_speed=2),
            Recipe("Polyester Fabric", "Refinery", ("Polymer Resin", "Water"))),
        "Solid Biofuel": (
            Recipe("Solid Biofuel", "Constructor", ("Biomass", ), minimal_belt_speed=2, handcraftable=True), ),
        "Liquid Biofuel": (
            Recipe("Liquid Biofuel", "Refinery", ("Solid Biofuel", "Water"), minimal_belt_speed=2), ),
        "Empty Canister": (
            Recipe("Empty Canister", "Constructor", ("Plastic", ), handcraftable=True),
            Recipe("Coated Iron Canister", "Assembler", ("Iron Plate", "Copper Sheet")),
            Recipe("Steel Canister", "Constructor", ("Steel Ingot", ))),
        "Empty Fluid Tank": (
            Recipe("Empty Fluid Tank", "Constructor", ("Aluminum Ingot", ), handcraftable=True, minimal_phase=2), ),
        "Packaged Alumina Solution": (
            Recipe("Packaged Alumina Solution", "Packager", ("Alumina Solution", "Empty Canister"), minimal_belt_speed=2), ),
        "Packaged Fuel": (
            Recipe("Packaged Fuel", "Packager", ("Fuel", "Empty Canister")),
            Recipe("Diluted Packaged Fuel", "Refinery", ("Heavy Oil Residue", "Packaged Water"))),
        "Packaged Heavy Oil Residue": (
            Recipe("Packaged Heavy Oil Residue", "Packager", ("Heavy Oil Residue", "Empty Canister")), ),
        "Packaged Liquid Biofuel": (
            Recipe("Packaged Liquid Biofuel", "Packager", ("Liquid Biofuel", "Empty Canister")), ),
        "Packaged Nitric Acid": (
            Recipe("Packaged Nitric Acid", "Packager", ("Nitric Acid", "Empty Fluid Tank")), ),
        "Packaged Nitrogen Gas": (
            Recipe("Packaged Nitrogen Gas", "Packager", ("Nitrogen Gas", "Empty Fluid Tank")), ),
        "Packaged Oil": (
            Recipe("Packaged Oil", "Packager", ("Crude Oil", "Empty Canister")), ),
        "Packaged Sulfuric Acid": (
            Recipe("Packaged Sulfuric Acid", "Packager", ("Sulfuric Acid", "Empty Canister")), ),
        "Packaged Turbofuel": (
            Recipe("Packaged Turbofuel", "Packager", ("Turbofuel", "Empty Canister")), ),
        "Packaged Water": (
            Recipe("Packaged Water", "Packager", ("Water", "Empty Canister")), ),
        "Turbofuel": (
            Recipe("Turbofuel", "Refinery", ("Fuel", "Compacted Coal")),
            Recipe("Turbo Heavy Fuel", "Refinery", ("Heavy Oil Residue", "Compacted Coal")),
            Recipe("Turbo Blend Fuel", "Blender", ("Fuel", "Heavy Oil Residue", "Sulfur", "Petroleum Coke"), minimal_phase=2)),
        "Gas Mask": (
            Recipe("Gas Mask", "Equipment Workshop", ("Rubber", "Plastic", "Fabric"), handcraftable=True, minimal_belt_speed=0), ),
        "Alien DNA Capsule": (
            Recipe("Alien DNA Capsule", "Constructor", ("Alien Protein", ), handcraftable=True), ),
        "Black Powder": (
            Recipe("Black Powder", "Equipment Workshop", ("Coal", "Sulfur"), handcraftable=True),
            Recipe("Fine Black Powder", "Assembler", ("Sulfur", "Compacted Coal"))),
        "Smokeless Powder": (
            Recipe("Smokeless Powder", "Refinery", ("Black Powder", "Heavy Oil Residue")), ),
        "Rifle Ammo": (
            Recipe("Rifle Ammo", "Assembler", ("Copper Sheet", "Smokeless Powder"), handcraftable=True, minimal_belt_speed=2), ),
        "Iron Rebar": (
            Recipe("Iron Rebar", "Constructor", ("Iron Rod", ), handcraftable=True), ),
        "Nobelisk": (
            Recipe("Nobelisk", "Assembler", ("Black Powder", "Steel Pipe"), handcraftable=True), ),
        "Power Shard": (
            Recipe("Power Shard (1)", "Constructor", ("Blue Power Slug", ), handcraftable=True),
            Recipe("Power Shard (2)", "Constructor", ("Yellow Power Slug", ), handcraftable=True),
            Recipe("Power Shard (5)", "Constructor", ("Purple Power Slug", ), handcraftable=True),
            Recipe("Synthetic Power Shard", "Quantum Encoder", ("Dark Matter Residue", "Excited Photonic Matter", "Time Crystal", "Dark Matter Crystal", "Quartz Crystal"), minimal_phase=4)),  # 1.0
        "Object Scanner": (
            Recipe("Object Scanner", "Equipment Workshop", ("Reinforced Iron Plate", "Wire", "Screw"), handcraftable=True), ),
        "Xeno-Zapper": (
            Recipe("Xeno-Zapper", "Equipment Workshop", ("Iron Rod", "Reinforced Iron Plate", "Cable", "Wire"), handcraftable=True, implicitly_unlocked=True), ),

# 1.0
        "Rocket Fuel": (
            Recipe("Rocket Fuel", "Blender", ("Turbofuel", "Nitric Acid"), additional_outputs=("Compacted Coal", ), minimal_phase=2),
            Recipe("Nitro Rocket Fuel", "Blender", ("Fuel", "Nitrogen Gas", "Sulfur", "Coal"), minimal_belt_speed=2, additional_outputs=("Compacted Coal", ), minimal_phase=2)),
        "Ionized Fuel": (
            Recipe("Ionized Fuel", "Refinery", ("Rocket Fuel", "Power Shard"), additional_outputs=("Compacted Coal", )),
            Recipe("Dark-Ion Fuel", "Blender", ("Packaged Rocket Fuel", "Dark Matter Crystal"), minimal_belt_speed=3, additional_outputs=("Compacted Coal", ), minimal_phase=4)),
        "Packaged Rocket Fuel": (
            Recipe("Packaged Rocket Fuel", "Packager", ("Rocket Fuel", "Empty Fluid Tank")), ),
        "Packaged Ionized Fuel": (
            Recipe("Packaged Ionized Fuel", "Packager", ("Ionized Fuel", "Empty Fluid Tank")), ),
        "Diamonds": (
            Recipe("Diamonds", "Particle Accelerator", ("Coal", ), minimal_belt_speed=5),
            Recipe("Cloudy Diamonds", "Particle Accelerator", ("Coal", "Limestone"), minimal_belt_speed=4),
            Recipe("Oil-Based Diamonds", "Particle Accelerator", ("Crude Oil", )),
            Recipe("Petroleum Diamonds", "Particle Accelerator", ("Petroleum Coke", ), minimal_belt_speed=5),
            Recipe("Pink Diamonds", "Converter", ("Coal", "Quartz Crystal"), minimal_belt_speed=2),
            Recipe("Turbo Diamonds", "Particle Accelerator", ("Coal", "Packaged Turbofuel"), minimal_belt_speed=5)),
        "Time Crystal": (
            Recipe("Time Crystal", "Converter", ("Diamonds", )), ),
        "Ficsite Ingot": (
            Recipe("Ficsite Ingot (Aluminum)", "Converter", ("Reanimated SAM", "Aluminum Ingot"), minimal_belt_speed=2),
            Recipe("Ficsite Ingot (Caterium)", "Converter", ("Reanimated SAM", "Caterium Ingot")),
            Recipe("Ficsite Ingot (Iron)", "Converter", ("Reanimated SAM", "Iron Ingot"), minimal_belt_speed=3)),
        "Ficsite Trigon": (
            Recipe("Ficsite Trigon", "Constructor", ("Ficsite Ingot", ), handcraftable=True), ),
        "SAM": (
            Recipe("SAM", "Miner Mk.1", handcraftable=True, implicitly_unlocked=True), ),
        "Reanimated SAM": (
            Recipe("Reanimated SAM", "Constructor", ("SAM", ), handcraftable=True, minimal_belt_speed=2), ),
        "SAM Fluctuator": (
            Recipe("SAM Fluctuator", "Manufacturer", ("Reanimated SAM", "Steel Pipe", "Wire"), handcraftable=True), ),
        "Excited Photonic Matter": (
            Recipe("Excited Photonic Matter", "Converter", implicitly_unlocked=True), ),
        "Dark Matter Crystal": (
            Recipe("Dark Matter Crystal", "Particle Accelerator", ("Diamonds", ), additional_outputs=("Dark Matter Residue", )),
            Recipe("Dark Matter Crystallization", "Particle Accelerator", additional_outputs=("Dark Matter Residue", )),
            Recipe("Dark Matter Trap", "Particle Accelerator", ("Time Crystal", ), additional_outputs=("Dark Matter Residue", ))),
        "Singularity Cell": (
            Recipe("Singularity Cell", "Manufacturer", ("Nuclear Pasta", "Dark Matter Crystal", "Iron Plate", "Concrete"), minimal_belt_speed=3), ),
        "Biochemical Sculptor": (
            Recipe("Biochemical Sculptor", "Blender", ("Assembly Director System", "Ficsite Trigon", "Water"), minimal_phase=5), ),
        "Ballistic Warp Drive": (
            Recipe("Ballistic Warp Drive", "Manufacturer", ("Thermal Propulsion Rocket", "Singularity Cell", "Superposition Oscillator", "Dark Matter Crystal"), minimal_phase=5), ),

        # All Quantum Encoder recipes have `Dark Matter Residue` set as an input, this hack makes the logic make sure you can get rid of it
        "Dark Matter Residue": (
            # Recipe("Ficsonium", "Particle Accelerator", ("Plutonium Waste", "Singularity Cell"), additional_outputs=("Ficsonium", )),
            Recipe("Dark Matter Crystal", "Particle Accelerator", ("Diamonds", ), additional_outputs=("Dark Matter Crystal", )),
            Recipe("Dark Matter Crystallization", "Particle Accelerator", additional_outputs=("Dark Matter Crystal", )),
            Recipe("Dark Matter Trap", "Particle Accelerator", ("Time Crystal", ), additional_outputs=("Dark Matter Crystal", )),
            Recipe("Dark Matter Residue", "Converter", ("Reanimated SAM", ))),
        "Superposition Oscillator": (
            Recipe("Superposition Oscillator", "Quantum Encoder", ("Dark Matter Residue", "Excited Photonic Matter", "Dark Matter Crystal", "Crystal Oscillator", "Alclad Aluminum Sheet")), ),
        "Neural-Quantum Processor": (
            Recipe("Neural-Quantum Processor", "Quantum Encoder", ("Dark Matter Residue", "Excited Photonic Matter", "Time Crystal", "Supercomputer", "Ficsite Trigon")), ),
        "AI Expansion Server": (
            Recipe("AI Expansion Server", "Quantum Encoder", ("Dark Matter Residue", "Excited Photonic Matter", "Magnetic Field Generator", "Neural-Quantum Processor", "Superposition Oscillator"), minimal_phase=5), ),
        ###
# 1.0
        # For exclusion logic
        "Hoverpack": (
            Recipe("Hoverpack", "Equipment Workshop", ("Motor", "Heavy Modular Frame", "Computer", "Alclad Aluminum Sheet")), ),
        "Turbo Rifle Ammo": (
            Recipe("Turbo Rifle Ammo", "Blender", ("Rifle Ammo", "Aluminum Casing", "Turbofuel"), minimal_belt_speed=3),
            Recipe("Turbo Rifle Ammo (Packaged)", "Manufacturer", ("Rifle Ammo", "Aluminum Casing", "Packaged Turbofuel"), minimal_belt_speed=2, minimal_phase=2)),
        "Homing Rifle Ammo": (
            Recipe("Homing Rifle Ammo", "Assembler", ("Rifle Ammo", "High-Speed Connector")), ),
        ###
    }

    buildings: dict[str, Building] = {
        "Constructor": Building("Constructor", ("Reinforced Iron Plate", "Cable"), PowerInfrastructureLevel.Basic),
        "Assembler": Building("Assembler", ("Reinforced Iron Plate", "Iron Rod", "Cable"), PowerInfrastructureLevel.Basic),  # Simplified , used ("Reinforced Iron Plate", "Rotor", "Cable")
        "Manufacturer": Building("Manufacturer", ("Motor", "Heavy Modular Frame", "Cable", "Plastic"), PowerInfrastructureLevel.Advanced),
        "Packager": Building("Packager", ("Steel Beam", "Rubber", "Plastic"), PowerInfrastructureLevel.Basic),
        "Refinery": Building("Refinery", ("Motor", "Encased Industrial Beam", "Steel Pipe", "Copper Sheet"), PowerInfrastructureLevel.Automated),
        "Blender": Building("Blender", ("Motor", "Heavy Modular Frame", "Aluminum Casing", "Radio Control Unit"), PowerInfrastructureLevel.Advanced),
        "Particle Accelerator": Building("Particle Accelerator", ("Radio Control Unit", "Electromagnetic Control Rod", "Supercomputer", "Cooling System", "Fused Modular Frame", "Turbo Motor"), PowerInfrastructureLevel.Complex),
        "Biomass Burner": Building("Biomass Burner", ("Iron Plate", "Iron Rod", "Wire"), implicitly_unlocked=True),
        "Coal Generator": Building("Coal Generator", ("Reinforced Iron Plate", "Rotor", "Cable")),
        "Fuel Generator": Building("Fuel Generator", ("Computer", "Heavy Modular Frame", "Motor", "Rubber", "Quickwire")),
        "Geothermal Generator": Building("Geothermal Generator", ("Motor", "Modular Frame", "High-Speed Connector", "Copper Sheet", "Wire")),
        "Nuclear Power Plant": Building("Nuclear Power Plant", ("Concrete", "Heavy Modular Frame", "Supercomputer", "Cable", "Alclad Aluminum Sheet")),
        "Miner Mk.1": Building("Miner Mk.1", ("Iron Plate", "Concrete"), PowerInfrastructureLevel.Basic, implicitly_unlocked=True),
        "Miner Mk.2": Building("Miner Mk.2", ("Encased Industrial Beam", "Steel Pipe", "Modular Frame"), PowerInfrastructureLevel.Automated, can_produce=False),
        "Miner Mk.3": Building("Miner Mk.3", ("Steel Pipe", "Supercomputer", "Fused Modular Frame", "Turbo Motor"), PowerInfrastructureLevel.Advanced, can_produce=False),
        "Oil Extractor": Building("Oil Extractor", ("Motor", "Encased Industrial Beam", "Cable")),
        "Water Extractor": Building("Water Extractor", ("Copper Sheet", "Reinforced Iron Plate", "Rotor")),
        "Smelter": Building("Smelter", ("Iron Rod", "Wire"), PowerInfrastructureLevel.Basic),
        "Foundry": Building("Foundry", ("Reinforced Iron Plate", "Iron Rod", "Concrete"), PowerInfrastructureLevel.Basic),  # Simplified, used ("Modular Frame", "Rotor", "Concrete")
        "Resource Well Pressurizer": Building("Resource Well Pressurizer", ("Steel Pipe", "Heavy Modular Frame", "Motor", "Reinforced Iron Plate", "Copper Sheet", "Steel Beam"), PowerInfrastructureLevel.Advanced),  # Simplified, used ("Radio Control Unit", "Heavy Modular Frame", "Motor", "Alclad Aluminum Sheet", "Rubber", "Steel Beam", "Aluminum Casing")
        "Equipment Workshop": Building("Equipment Workshop", ("Iron Plate", "Iron Rod"), implicitly_unlocked=True),
        "AWESOME Sink": Building("AWESOME Sink", ("Reinforced Iron Plate", "Cable", "Concrete"), can_produce=False),
        "AWESOME Shop": Building("AWESOME Shop", ("Screw", "Iron Plate", "Cable"), can_produce=False),
        "MAM": Building("MAM", ("Reinforced Iron Plate", "Wire", "Cable"), can_produce=False),
        "Pipes Mk.1": Building("Pipes Mk.1", ("Copper Sheet", "Iron Plate", "Concrete"), can_produce=False),
        "Pipes Mk.2": Building("Pipes Mk.2", ("Copper Sheet", "Plastic", "Iron Plate", "Concrete"), can_produce=False),
        "Pipeline Pump Mk.1": Building("Pipeline Pump Mk.1", ("Copper Sheet", "Rotor"), can_produce=False),
        "Pipeline Pump Mk.2": Building("Pipeline Pump Mk.2", ("Motor", "Encased Industrial Beam", "Plastic"), can_produce=False),
        "Conveyor Merger": Building("Conveyor Merger", ("Iron Plate", "Iron Rod"), can_produce=False),
        "Conveyor Splitter": Building("Conveyor Splitter", ("Iron Plate", "Cable"), can_produce=False),
        "Conveyor Mk.1": Building("Conveyor Mk.1", ("Iron Plate", "Iron Rod", "Concrete"), can_produce=False, implicitly_unlocked=True),
        "Conveyor Mk.2": Building("Conveyor Mk.2", ("Reinforced Iron Plate", "Iron Plate", "Iron Rod", "Concrete"), can_produce=False),
        "Conveyor Mk.3": Building("Conveyor Mk.3", ("Steel Beam", "Iron Plate", "Iron Rod", "Concrete"), can_produce=False),
        "Conveyor Mk.4": Building("Conveyor Mk.4", ("Encased Industrial Beam", "Iron Plate", "Iron Rod", "Concrete"), can_produce=False),
        "Conveyor Mk.5": Building("Conveyor Mk.5", ("Alclad Aluminum Sheet", "Iron Plate", "Iron Rod", "Concrete"), can_produce=False),
        "Conveyor Mk.6": Building("Conveyor Mk.6", ("Ficsite Trigon", "Time Crystal", "Iron Plate", "Iron Rod", "Concrete"), can_produce=False),
        "Power Pole Mk.1": Building("Power Pole Mk.1", ("Iron Plate", "Iron Rod", "Concrete"), can_produce=False, implicitly_unlocked=True),
        # higher level power poles arent in logic (yet)
        # "Power Pole Mk.2": Building("Power Pole Mk.2", ("Quickwire", "Iron Rod", "Concrete"), False),
        # "Power Pole Mk.3": Building("Power Pole Mk.3", ("High-Speed Connector", "Steel Pipe", "Rubber"), False),
        "Power Storage": Building("Power Storage", ("Wire", "Modular Frame", "Stator"), can_produce=False),
        "Foundation": Building("Foundation", ("Iron Plate", "Concrete"), can_produce=False),
        "Walls Orange": Building("Walls Orange", ("Iron Plate", "Concrete"), can_produce=False),
        "Space Elevator": Building("Space Elevator", ("Concrete", "Iron Plate", "Iron Rod", "Wire"), can_produce=False),

# 1.0
        "Converter": Building("Converter", ("Fused Modular Frame", "Cooling System", "Radio Control Unit", "SAM Fluctuator"), PowerInfrastructureLevel.Complex),
        "Quantum Encoder": Building("Quantum Encoder", ("Turbo Motor", "Supercomputer", "Cooling System", "Time Crystal", "Ficsite Trigon"), PowerInfrastructureLevel.Complex),
        "Alien Power Augmenter": Building("Alien Power Augmenter", ("SAM Fluctuator", "Cable", "Encased Industrial Beam", "Motor", "Computer")),
# 1.0

        # For exclusion logic
        "Portal": Building("Portal", ("Turbo Motor", "Radio Control Unit", "Superposition Oscillator", "SAM Fluctuator", "Ficsite Trigon", "Singularity Cell"), PowerInfrastructureLevel.Advanced),
        ###
    }

    requirement_per_powerlevel: dict[PowerInfrastructureLevel, tuple[Recipe, ...]] = {
        # no need to polute the logic by including higher level recipes based on previus recipes
        PowerInfrastructureLevel.Basic: (
            Recipe("Biomass Power (Biomass)", "Biomass Burner", ("Biomass", ), implicitly_unlocked=True),
        ),
        PowerInfrastructureLevel.Automated: (
            Recipe("Biomass Power (Solid Biofuel)", "Biomass Burner", ("Solid Biofuel", ), implicitly_unlocked=True),
            # Recipe("Coal Generator Power (Petroleum Coke)", "Coal Generator", ("Petroleum Coke", "Water"), implicitly_unlocked=True),
            Recipe("Coal Generator Power (Coal)", "Coal Generator", ("Coal", "Water"), implicitly_unlocked=True),
        ),
        PowerInfrastructureLevel.Advanced: (
            Recipe("Coal Generator Power (Compacted Coal)", "Coal Generator", ("Compacted Coal", "Water"), implicitly_unlocked=True),
            Recipe("Geothermal Generator Power", "Geothermal Generator", implicitly_unlocked=True),
            Recipe("Fuel Generator Power (Liquid Biofuel)", "Fuel Generator", ("Liquid Biofuel", ), implicitly_unlocked=True),
            Recipe("Fuel Generator Power (Fuel)", "Fuel Generator", ("Fuel", ), implicitly_unlocked=True),
            Recipe("Alien Power Augmenter Power", "Alien Power Augmenter", implicitly_unlocked=True),
        ),
        PowerInfrastructureLevel.Complex: (
            Recipe("Fuel Generator Power (Turbofuel)", "Fuel Generator", ("Turbofuel", ), implicitly_unlocked=True),
            # Recipe("Fuel Generator Power (Rocket Fuel)", "Fuel Generator", ("Rocket Fuel", ), implicitly_unlocked=True),
            # Recipe("Fuel Generator Power (Ionized Fuel)", "Fuel Generator", ("Ionized Fuel", ), implicitly_unlocked=True),
            Recipe("Nuclear Power Plant Power (Uranium)", "Nuclear Power Plant", ("Uranium Fuel Rod", "Water"), implicitly_unlocked=True),
            # Recipe("Nuclear Power Plant Power (Plutonium)", "Nuclear Power Plant", ("Plutonium Fuel Rod", "Water"), implicitly_unlocked=True),
            # Recipe("Nuclear Power Plant Power (Ficsonium)", "Nuclear Power Plant", ("Ficsonium Fuel Rod", "Water"), implicitly_unlocked=True),
            # Recipe("Alien Power Augmenter Power (Alien Power Matrix)", "Alien Power Augmenter", ("Alien Power Matrix"), implicitly_unlocked=True),
        )
    }

    slots_per_milestone: int = 8

    hub_layout: tuple[tuple[dict[str, int], ...], ...] = (
        # Regenerate via /Script/Engine.Blueprint'/Archipelago/Debug/CC_BuildHubData.CC_BuildHubData'
        (  # Tier 1
            {"Concrete": 200, "Iron Plate": 100, "Iron Rod": 100, },  # Schematic: Base Building (Schematic_1-1_C)
            {"Iron Plate": 150, "Iron Rod": 150, "Wire": 300, },  # Schematic: Logistics (Schematic_1-2_C)
            {"Wire": 300, "Screw": 300, "Iron Plate": 100, },  # Schematic: Field Research (Schematic_1-3_C)
            {"Wire": 100, "Screw": 200, "Concrete": 200, },  # Schematic: Archipelago Additional Tier1 (Schem_ApExtraTier1_C)
        ),
        (  # Tier 2
            {"Cable": 200, "Iron Rod": 200, "Screw": 500, "Iron Plate": 300, },  # Schematic: Part Assembly (Schematic_2-1_C)
            {"Screw": 500, "Cable": 100, "Concrete": 100, },  # Schematic: Obstacle Clearing (Schematic_2-2_C)
            {"Rotor": 50, "Iron Plate": 300, "Cable": 150, },  # Schematic: Jump Pads (Schematic_2-3_C)
            {"Concrete": 400, "Wire": 500, "Iron Rod": 200, "Iron Plate": 200, },  # Schematic: Resource Sink Bonus Program (Schematic_2-5_C)
            {"Reinforced Iron Plate": 50, "Concrete": 200, "Iron Rod": 300, "Iron Plate": 300, },  # Schematic: Logistics Mk.2 (Schematic_3-2_C)
        ),
        (  # Tier 3
            {"Reinforced Iron Plate": 150, "Rotor": 50, "Cable": 500, },  # Schematic: Coal Power (Schematic_3-1_C)
            {"Modular Frame": 25, "Rotor": 100, "Cable": 100, "Iron Plate": 400, },  # Schematic: Vehicular Transport (Schematic_3-3_C)
            {"Modular Frame": 50, "Rotor": 150, "Concrete": 500, "Wire": 1000, },  # Schematic: Basic Steel Production (Schematic_3-4_C)
            {"Reinforced Iron Plate": 100, "Iron Rod": 600, "Wire": 1500, },  # Schematic: Improved Melee Combat (Schematic_4-2_C)
        ),
        (  # Tier 4
            {"Modular Frame": 100, "Steel Beam": 200, "Cable": 500, "Concrete": 1000, },  # Schematic: FICSIT Blueprints (Schematic_4-5_C)
            {"Steel Beam": 200, "Steel Pipe": 200, "Reinforced Iron Plate": 400, },  # Schematic: Logistics Mk.3 (Schematic_5-3_C)
            {"Steel Pipe": 100, "Modular Frame": 100, "Rotor": 200, "Concrete": 500, },  # Schematic: Advanced Steel Production (Schematic_4-1_C)
            {"Encased Industrial Beam": 50, "Steel Beam": 100, "Modular Frame": 200, "Wire": 2000, },  # Schematic: Expanded Power Infrastructure (Schematic_4-3_C)
            {"Copper Sheet": 500, "Steel Pipe": 300, "Encased Industrial Beam": 50, },  # Schematic: Hypertubes (Schematic_4-4_C)
        ),
        (  # Tier 5
            {"Motor": 50, "Cable": 100, "Iron Plate": 500, },  # Something jetpack
            {"Motor": 50, "Encased Industrial Beam": 100, "Steel Pipe": 500, "Copper Sheet": 500, },  # Schematic: Oil Processing (Schematic_5-1_C)
            {"Rubber": 200, "Encased Industrial Beam": 300, "Modular Frame": 400, },
            {"Plastic": 200, "Steel Beam": 400, "Copper Sheet": 1000, },  # Schematic: Alternative Fluid Transport (Schematic_5-4_C)
            {"Motor": 100, "Encased Industrial Beam": 100, "Plastic": 200, "Rubber": 200, },  # Schematic: Industrial Manufacturing (Schematic_5-2_C)
        ),
        (  # Tier 6
            {"Motor": 200, "Modular Frame": 200, "Plastic": 400, "Cable": 1000, },  # Schematic: Industrial Manufacturing (Schematic_5-2_C)
            {"Motor": 250, "Encased Industrial Beam": 500, "Steel Pipe": 1000, "Steel Beam": 1000, },  # Schematic: Monorail Train Technology (Schematic_6-3_C)
            {"Computer": 50, "Steel Pipe": 4000, "Copper Sheet": 1000, },
            {"Heavy Modular Frame": 50, "Plastic": 1000, "Rubber": 1000, },  # Schematic: Pipeline Engineering Mk.2 (Schematic_6-5_C)
            {"Heavy Modular Frame": 50, "Computer": 100, "Rubber": 400, "Concrete": 1000, },
        ),
        (  # Tier 7
            {"Computer": 100, "Heavy Modular Frame": 100, "Motor": 250, "Rubber": 500, },  # Schematic: Bauxite Refinement (Schematic_7-1_C)
            {"Alclad Aluminum Sheet": 100, "Heavy Modular Frame": 100, "Computer": 100, "Motor": 250, },  # Schematic: Hover Pack (Schematic_8-3_C)
            {"Alclad Aluminum Sheet": 200, "Encased Industrial Beam": 400, "Reinforced Iron Plate": 600, },  # Schematic: Logistics Mk.5 (Schematic_7-2_C)
            {"Gas Filter": 50, "Aluminum Casing": 100, "Quickwire": 500, },  # Schematic: Hazmat Suit (Schematic_7-3_C)
            {"Alclad Aluminum Sheet": 200, "Aluminum Casing": 400, "Computer": 200, "Plastic": 1000, },  # Schematic: Aeronautical Engineering (Schematic_7-4_C)
        ),
        (  # Tier 8
            {"Radio Control Unit": 50, "Alclad Aluminum Sheet": 100, "Aluminum Casing": 200, "Motor": 300, },  # Schematic: Aeronautical Engineering (Schematic_7-4_C)
            {"Supercomputer": 50, "Heavy Modular Frame": 200, "Cable": 1000, "Concrete": 2000, },  # Schematic: Nuclear Power (Schematic_8-1_C)
            {"Radio Control Unit": 50, "Aluminum Casing": 200, "Alclad Aluminum Sheet": 400, "Wire": 3000, },  # Schematic: Advanced Aluminum Production (Schematic_8-2_C)
            {"Fused Modular Frame": 50, "Supercomputer": 100, "Steel Pipe": 1000, },  # Schematic: Leading-edge Production (Schematic_8-4_C)
            {"Turbo Motor": 50, "Fused Modular Frame": 100,  "Cooling System": 200, "Quickwire": 2500, },  # Schematic: Particle Enrichment (Schematic_8-5_C)
        ),
        (  # Tier 9
            {"Fused Modular Frame": 100, "Radio Control Unit": 250, "Cooling System": 500, },
            {"Time Crystal": 50, "Ficsite Trigon": 100, "Turbo Motor": 200, "Supercomputer": 400, },
            {"Neural-Quantum Processor": 100, "Time Crystal": 250, "Ficsite Trigon": 500, "Fused Modular Frame": 500, },
            {"Superposition Oscillator": 100, "Turbo Motor": 250, "Radio Control Unit": 500, "SAM Fluctuator": 1000, },
            {"Time Crystal": 250, "Ficsite Trigon": 250, "Alclad Aluminum Sheet": 500, "Iron Plate": 10000, },
        ),
    )

    # Values from /Game/FactoryGame/Schematics/Progression/BP_GamePhaseManager.BP_GamePhaseManager
    space_elevator_phases: tuple[dict[str, int], ...] = (
        {"Smart Plating": 50},
        {"Smart Plating": 500, "Versatile Framework": 500, "Automated Wiring": 100},
        {"Versatile Framework": 2500, "Modular Engine": 500, "Adaptive Control Unit": 100},
        {"Assembly Director System": 4000, "Magnetic Field Generator": 4000, "Nuclear Pasta": 1000, "Thermal Propulsion Rocket": 1000},
        {"Nuclear Pasta": 1000, "Biochemical Sculptor": 1000, "AI Expansion Server": 256, "Ballistic Warp Drive": 200}
    )

    # Do not regenerate as format got changed
    # Regenerate via /Script/Engine.Blueprint'/Archipelago/Debug/CC_BuildMamData.CC_BuildMamData'
    man_trees: dict[str, MamTree] = {
        "Alien Organisms": MamTree(("Hog Remains", "Plasma Spitter Remains", "Stinger Remains", "Hatcher Remains"), (  # Alien Organisms (BPD_ResearchTree_AlienOrganisms_C)
            MamNode("Inflated Pocket Dimension", {"Alien Protein": 3, "Cable": 1000, }, depends_on=("Bio-Organic Properties", )),  # (Research_AOrgans_3_C)
            MamNode("Hostile Organism Detection", {"Alien DNA Capsule": 10, "Crystal Oscillator": 5, "High-Speed Connector": 5, }, depends_on=("Bio-Organic Properties", )),  # (Research_AOrganisms_2_C)
            MamNode("Expanded Toolbelt", {"Alien DNA Capsule": 5, "Steel Beam": 500, }, depends_on=("Inflated Pocket Dimension", )),  # (Research_ACarapace_3_C)
            MamNode("Bio-Organic Properties", {"Alien Protein": 5, }, depends_on=("Spitter Research", "Hog Research", "Hatcher Research", "Stinger Research")),  # (Research_AO_DNACapsule_C)
            MamNode("Stinger Research", {"Stinger Remains": 1, }, depends_on=tuple()),  # (Research_AO_Stinger_C)
            MamNode("Hatcher Research", {"Hatcher Remains": 1, }, depends_on=tuple()),  # (Research_AO_Hatcher_C)
            MamNode("Hog Research", {"Hog Remains": 1, }, depends_on=tuple()),  # (Research_ACarapace_0_C)
            MamNode("Spitter Research", {"Plasma Spitter Remains": 1, }, depends_on=tuple()),  # (Research_AOrgans_0_C)
            MamNode("Structural Analysis", {"Alien DNA Capsule": 5, "Iron Rod": 100, }, depends_on=("Bio-Organic Properties", )),  # (Research_AO_Pre_Rebar_C)
            MamNode("Protein Inhaler", {"Alien Protein": 2, "Beryl Nut": 20, "Rotor": 50, }, depends_on=("Bio-Organic Properties", )),  # (Research_AOrgans_2_C)
            MamNode("The Rebar Gun", {"Rotor": 25, "Reinforced Iron Plate": 50, "Screw": 500, }, depends_on=("Structural Analysis", )),  # (Research_ACarapace_2_C)
        )),
        # 1.0
        "Alien Technology": MamTree(("SAM", "Mercer Sphere", "Somersloop"), (
            MamNode("SAM Analysis", {"SAM": 10, }, depends_on=tuple()),
            MamNode("SAM Reanimation", {"SAM": 20, }, depends_on=("SAM Analysis",)),
            MamNode("SAM Fluctuator", {"Reanimated SAM": 10, "Steel Pipe": 100, "Wire": 200, }, depends_on=("SAM Reanimation",)),
            MamNode("Mercer Sphere Analysis", {"Mercer Sphere": 1, }, depends_on=tuple()),
            MamNode("Dimensional Depot", {"Mercer Sphere": 1, "SAM Fluctuator": 11, }, depends_on=("Mercer Sphere Analysis", "SAM Fluctuator")),
            MamNode("Manual Depot Uploader", {"Mercer Sphere": 3, "Computer": 17, "SAM Fluctuator": 19, }, depends_on=("Dimensional Depot",)),
            MamNode("Depot Expansion (200%)", {"Mercer Sphere": 3, "SAM Fluctuator": 47, }, depends_on=("Dimensional Depot",)),
            MamNode("Depot Expansion (300%)", {"Mercer Sphere": 7, "SAM Fluctuator": 103, }, depends_on=("Depot Expansion (200%)",)),
            MamNode("Depot Expansion (400%)", {"Mercer Sphere": 13, "SAM Fluctuator": 151, }, depends_on=("Depot Expansion (300%)",)),
            MamNode("Depot Expansion (500%)", {"Mercer Sphere": 23, "SAM Fluctuator": 199, }, depends_on=("Depot Expansion (400%)",)),
            MamNode("Upload Upgrade: 30/min", {"Mercer Sphere": 3, "SAM Fluctuator": 47, }, depends_on=("Dimensional Depot",)),
            MamNode("Upload Upgrade: 60/min", {"Mercer Sphere": 7, "SAM Fluctuator": 103, }, depends_on=("Upload Upgrade: 30/min",)),
            MamNode("Upload Upgrade: 120/min", {"Mercer Sphere": 13, "SAM Fluctuator": 151, }, depends_on=("Upload Upgrade: 60/min",)),
            MamNode("Upload Upgrade: 240/min", {"Mercer Sphere": 23, "SAM Fluctuator": 199, }, depends_on=("Upload Upgrade: 120/min",)),
            MamNode("Somersloop Analysis", {"Somersloop": 1, }, depends_on=tuple()),
            MamNode("Alien Energy Harvesting", {"SAM Fluctuator": 10, }, depends_on=("Somersloop Analysis", "SAM Fluctuator")),
            MamNode("Production Amplifier", {"Somersloop": 1, "SAM Fluctuator": 100, "Circuit Board": 50, }, depends_on=("Alien Energy Harvesting",)),
            MamNode("Power Augmenter", {"Somersloop": 1, "SAM Fluctuator": 100, "Computer": 50, }, depends_on=("Alien Energy Harvesting",)),
            MamNode("Alien Power Matrix", {"Singularity Cell": 50, "Power Shard": 100, "SAM Fluctuator": 500, }, depends_on=("Power Augmenter",), minimal_phase=4),
        )),
        # 1.0
        "Caterium": MamTree(("Caterium Ore", ), (  # Caterium (BPD_ResearchTree_Caterium_C)
            MamNode("Caterium Electronics", {"Quickwire": 100, }, depends_on=("Quickwire", )),  # (Research_Caterium_3_C)
            MamNode("Bullet Guidance System", {"High-Speed Connector": 10, "Rifle Ammo": 500, }, depends_on=("High-Speed Connector", )),  # (Research_Caterium_6_3_C)
            MamNode("High-Speed Connector", {"Quickwire": 500, "Plastic": 50, }, depends_on=("Caterium Electronics", )),  # (Research_Caterium_5_C)
            MamNode("Caterium", {"Caterium Ore": 10, }, depends_on=tuple()),  # (Research_Caterium_0_C)
            MamNode("Caterium Ingots", {"Caterium Ore": 50, }, depends_on=("Caterium", )),  # (Research_Caterium_1_C)
            MamNode("Quickwire", {"Caterium Ingot": 50, }, depends_on=("Caterium Ingots", )),  # (Research_Caterium_2_C)
            MamNode("Power Switch", {"Steel Beam": 100, "AI Limiter": 50, }, depends_on=("AI Limiter", )),  # (Research_Caterium_4_1_2_C)
            MamNode("Priority Power Switch", {"High-Speed Connector": 25, "Quickwire": 500, }, depends_on=("High-Speed Connector", )),  # 1.0
            MamNode("Power Poles Mk.2", {"Quickwire": 300, }, depends_on=("Caterium Electronics", )),  # (Research_Caterium_4_2_C)
            MamNode("AI Limiter", {"Quickwire": 200, "Copper Sheet": 50, }, depends_on=("Caterium Electronics", )),  # (Research_Caterium_4_1_C)
            MamNode("Smart Splitter", {"AI Limiter": 10, "Reinforced Iron Plate": 50, }, depends_on=("AI Limiter", )),  # (Research_Caterium_4_1_1_C)
            MamNode("Programmable Splitter", {"AI Limiter": 100, "Computer": 50, "Heavy Modular Frame": 50, }, depends_on=("AI Limiter", "High-Speed Connector")),  # (Research_Caterium_7_1_C) # 1.0
            MamNode("Zipline", {"Quickwire": 100, "Cable": 50, }, depends_on=("Quickwire", )),  # (Research_Caterium_2_1_C)
            MamNode("Geothermal Generator", {"High-Speed Connector": 100, "Quickwire": 1000, "Motor": 50, }, depends_on=("AI Limiter", "High-Speed Connector")),  # (Research_Caterium_7_2_C) # 1.0
            MamNode("Stun Rebar", {"Quickwire": 50, "Iron Rebar": 10, }, depends_on=("Quickwire", )),  # (Research_Caterium_3_2_C)
            MamNode("Power Poles Mk.3", {"High-Speed Connector": 50, "Steel Pipe": 200, }, depends_on=("Power Poles Mk.2", )),  # (Research_Caterium_6_2_C) # 1.0
        )),
        "Mycelia": MamTree(("Mycelia", ), (  # Mycelia (BPD_ResearchTree_Mycelia_C)
            MamNode("Therapeutic Inhaler", {"Mycelia": 15, "Bacon Agaric": 1, "Alien Protein": 1, }, depends_on=("Medical Properties", )),  # (Research_Mycelia_6_C)
            MamNode("Expanded Toolbelt", {"Fabric": 50, "Rotor": 100, }, depends_on=("Fabric", )),  # (Research_Mycelia_7_C)
            MamNode("Mycelia", {"Mycelia": 5, }, depends_on=tuple()),  # (Research_Mycelia_1_C)
            MamNode("Fabric", {"Mycelia": 25, "Biomass": 100, }, depends_on=("Mycelia", )),  # (Research_Mycelia_2_C)
            MamNode("Medical Properties", {"Mycelia": 25, "Stator": 10, }, depends_on=("Mycelia", )),  # (Research_Mycelia_4_C)
            MamNode("Toxic Cellular Modification", {"Nobelisk": 10, "Mycelia": 100, "Biomass": 200, }, depends_on=("Mycelia", )),  # (Research_Mycelia_8_C)
            MamNode("Vitamin Inhaler", {"Mycelia": 10, "Paleberry": 5, }, depends_on=("Medical Properties", )),  # (Research_Mycelia_5_C)
            MamNode("Parachute", {"Fabric": 10, "Cable": 50, }, depends_on=("Fabric", )),  # (Research_Mycelia_3_C)
            MamNode("Synthethic Polyester Fabric", {"Fabric": 25, "Polymer Resin": 100, }, depends_on=("Fabric", )),  # (Research_Mycelia_2_1_C)
            MamNode("Gas Mask", {"Coal": 10, "Fabric": 50, "Steel Pipe": 50, }, depends_on=("Fabric", )),  # 1.0
        )),
        "Nutrients": MamTree(("Paleberry", "Beryl Nut", "Bacon Agaric"), (  # Nutrients (BPD_ResearchTree_Nutrients_C)
            MamNode("Bacon Agaric", {"Bacon Agaric": 1, }, depends_on=tuple()),  # (Research_Nutrients_2_C)
            MamNode("Beryl Nut", {"Beryl Nut": 5, }, depends_on=tuple()),  # (Research_Nutrients_1_C)
            MamNode("Paleberry", {"Paleberry": 2, }, depends_on=tuple()),  # (Research_Nutrients_0_C)
            MamNode("Nutritional Processor", {"Modular Frame": 25, "Steel Pipe": 50, "Wire": 500, }, depends_on=("Beryl Nut", "Bacon Agaric", "Paleberry")),  # (Research_Nutrients_3_C)
            MamNode("Nutritional Inhaler", {"Bacon Agaric": 2, "Paleberry": 4, "Beryl Nut": 10, }, depends_on=("Nutritional Processor", )),  # (Research_Nutrients_4_C)
        )),
        "Power Slugs": MamTree(("Blue Power Slug", ), (  # Power Slugs (BPD_ResearchTree_PowerSlugs_C)
            MamNode("Slug Scanning", {"Iron Rod": 50, "Wire": 100, "Screw": 200, }, depends_on=("Blue Power Slugs", )),  # (Research_PowerSlugs_3_C)
            MamNode("Blue Power Slugs", {"Blue Power Slug": 1, }, depends_on=tuple()),  # (Research_PowerSlugs_1_C)
            MamNode("Yellow Power Shards", {"Yellow Power Slug": 1, "Rotor": 25, "Cable": 100, }, depends_on=("Blue Power Slugs", )),  # (Research_PowerSlugs_4_C)
            MamNode("Purple Power Shards", {"Purple Power Slug": 1, "Modular Frame": 25, "Copper Sheet": 100, }, depends_on=("Yellow Power Shards", )),  # (Research_PowerSlugs_5_C)
            MamNode("Overclock Production", {"Power Shard": 1, "Iron Plate": 50, "Wire": 50, }, depends_on=("Blue Power Slugs", )),  # (Research_PowerSlugs_2_C)
            MamNode("Synthetic Power Shards", {"Power Shard": 10, "Time Crystal": 100, "Quartz Crystal": 200, }, depends_on=("Purple Power Shards", ), minimal_phase=4),  # 1.0
        )),
        "Quartz": MamTree(("Raw Quartz", ), (  # Quartz (BPD_ResearchTree_Quartz_C)
            MamNode("Crystal Oscillator", {"Quartz Crystal": 100, "Reinforced Iron Plate": 50, }, depends_on=("Quartz Crystals", )),  # (Research_Quartz_2_C)
            MamNode("Quartz Crystals", {"Raw Quartz": 20, }, depends_on=("Quartz", )),  # (Research_Quartz_1_1_C)
            MamNode("Quartz", {"Raw Quartz": 10, }, depends_on=tuple()),  # (Research_Quartz_0_C)
            MamNode("Shatter Rebar", {"Quartz Crystal": 30, "Iron Rebar": 150, }, depends_on=("Quartz Crystals", )),  # (Research_Quartz_2_1_C)
            MamNode("Silica", {"Raw Quartz": 20, }, depends_on=("Quartz", )),  # (Research_Quartz_1_2_C)
            MamNode("Explosive Resonance Application", {"Crystal Oscillator": 5, "Nobelisk": 100, }, depends_on=("Crystal Oscillator", )),  # (Research_Quartz_3_4_C)
            MamNode("Blade Runners", {"Silica": 50, "Modular Frame": 10, }, depends_on=("Silica", )),  # (Research_Caterium_4_3_C)
            MamNode("The Explorer", {"Crystal Oscillator": 10, "Modular Frame": 100, }, depends_on=("Crystal Oscillator", )),  # (Research_Quartz_3_1_C)
            MamNode("Material Resonance Screening", {"Crystal Oscillator": 15, "Reinforced Iron Plate": 100, }, depends_on=("Crystal Oscillator", )),  # (Research_Quartz_PriorityMerger_C)
            MamNode("Radio Signal Scanning", {"Crystal Oscillator": 100, "Motor": 100, "Object Scanner": 1, }, depends_on=("Crystal Oscillator", )),  # (Research_Quartz_4_1_C)
            MamNode("Inflated Pocket Dimension", {"Silica": 200, }, depends_on=("Silica", )),  # (Research_Caterium_3_1_C)
            MamNode("Radar Technology", {"Crystal Oscillator": 50, "Heavy Modular Frame": 50, "Computer": 50, }, depends_on=("Crystal Oscillator", )),  # (Research_Quartz_4_C) # 1.0
        )),
        "Sulfur": MamTree(("Sulfur", ), (  # Sulfur (BPD_ResearchTree_Sulfur_C)
            MamNode("The Nobelisk Detonator", {"Black Powder": 50, "Steel Pipe": 100, "Cable": 200, }, depends_on=("Black Powder", )),  # (Research_Sulfur_3_1_C)
            MamNode("Smokeless Powder", {"Black Powder": 100, "Plastic": 50, }, depends_on=("Black Powder", )),  # (Research_Sulfur_3_C)
            MamNode("Sulfur", {"Sulfur": 10, }, depends_on=tuple()),  # (Research_Sulfur_0_C)
            MamNode("Inflated Pocket Dimension", {"Smokeless Powder": 50, "Computer": 50, }, depends_on=("Nuclear Deterrent Development", "Turbo Rifle Ammo", "Cluster Nobelisk", "The Rifle")),  # (Research_Sulfur_6_C)
            MamNode("The Rifle", {"Smokeless Powder": 50, "Motor": 100, "Rubber": 200, }, depends_on=("Smokeless Powder", )),  # (Research_Sulfur_4_1_C)
            MamNode("Compacted Coal", {"Hard Drive": 1, "Sulfur": 25, "Coal": 25, }, depends_on=("Experimental Power Generation", )),  # (Research_Sulfur_CompactedCoal_C)
            MamNode("Black Powder", {"Sulfur": 50, "Coal": 25, }, depends_on=("Sulfur", )),  # (Research_Sulfur_1_C)
            MamNode("Explosive Rebar", {"Smokeless Powder": 200, "Iron Rebar": 200, "Steel Beam": 200, }, depends_on=("Smokeless Powder", )),  # (Research_Sulfur_4_2_C)
            MamNode("Cluster Nobelisk", {"Smokeless Powder": 100, "Nobelisk": 200, }, depends_on=("Smokeless Powder", )),  # (Research_Sulfur_4_C)
            MamNode("Experimental Power Generation", {"Sulfur": 25, "Modular Frame": 50, "Rotor": 100, }, depends_on=("Sulfur", )),  # (Research_Sulfur_ExperimentalPower_C)
            MamNode("Turbo Rifle Ammo", {"Rifle Ammo": 1000, "Packaged Turbofuel": 50, "Aluminum Casing": 100, }, depends_on=("The Rifle", ), minimal_phase=2),  # (Research_Sulfur_5_2_C) # 1.0
            MamNode("Turbo Fuel", {"Hard Drive": 1, "Compacted Coal": 15, "Packaged Fuel": 50, }, depends_on=("Experimental Power Generation", )),  # (Research_Sulfur_TurboFuel_C)
            MamNode("Expanded Toolbelt", {"Black Powder": 100, "Encased Industrial Beam": 50, }, depends_on=("Black Powder", )),  # (Research_Sulfur_5_C)
            MamNode("Nuclear Deterrent Development", {"Nobelisk": 500, "Encased Uranium Cell": 10, "AI Limiter": 100, }, depends_on=("Cluster Nobelisk", ), minimal_phase=2),  # (Research_Sulfur_5_1_C) # 1.0
            MamNode("Rocket Fuel", {"Hard Drive": 1, "Empty Fluid Tank": 10, "Packaged Turbofuel": 100, }, depends_on=("Turbo Fuel", ), minimal_phase=3),  # 1.0
            MamNode("Ionized Fuel", {"Hard Drive": 1, "Power Shard": 100, "Packaged Rocket Fuel": 200, }, depends_on=("Turbo Fuel", ), minimal_phase=4),  # 1.0
        ))
    }

    drop_pods: list[DropPodData] = [
        # Regenerate via /Script/Engine.Blueprint'/Archipelago/Debug/CC_BuildDropPodLocations.CC_BuildDropPodLocations' 
        DropPodData(-29068, -22640, 17384,  "Encased Industrial Beam", 0),  # Unlocks with: 4 x Desc_SteelPlateReinforced_C
        DropPodData(-33340, 5176,   23519,  "Crystal Oscillator", 0),  # Unlocks with: 5 x Desc_CrystalOscillator_C
        DropPodData(8680,   -41777, 13053,  "Steel Pipe", 0),  # Unlocks with: 7 x Desc_SteelPipe_C
        DropPodData(35082,  16211,  22759,  "Supercomputer", 0),  # Unlocks with: 7 x Desc_ComputerSuper_C
        # DropPodData(-3511, 62314,  22109,  "Quantum Computer", 0),  # Unlocks with: 1 x Desc_ComputerQuantum_C
        DropPodData(66652,  -13642, 13420,  "Encased Industrial Beam", 50),  # Unlocks with: 3 x Desc_SteelPlateReinforced_C
        DropPodData(55247,  -51316, 14363,  None, 25),  # Unlocks with: (No Item)
        DropPodData(-4706,  -76301, 13618,  "Black Powder", 0),  # Unlocks with: 10 x Desc_Gunpowder_C
        DropPodData(-40194, 62956,  26261,  "Superposition Oscillator", 138),  # Unlocks with: 2 x Desc_QuantumOscillator_C
        DropPodData(80980,  -44100, 8303,   "Rotor", 0),  # Unlocks with: 3 x Desc_Rotor_C
        DropPodData(-56144, -72864, 27668,  "Quartz Crystal", 0),  # Unlocks with: 2 x Desc_QuartzCrystal_C
        DropPodData(-95228, 6970,   25142,  "High-Speed Connector", 112),  # Unlocks with: 11 x Desc_HighSpeedConnector_C
        DropPodData(-89284, -50630, 16019,  None, 50),  # Unlocks with: (No Item)
        DropPodData(-94708, 40337,  19832,  "Heat Sink", 138),  # Unlocks with: 2 x Desc_AluminumPlateReinforced_C
        DropPodData(94267,  47237,  9435,   "Motor", 0),  # Unlocks with: 1 x Desc_Motor_C
        DropPodData(87739,  -62975, 13444,  None, 30),  # Unlocks with: (No Item)
        DropPodData(12249,  114177, 26721,  "AI Limiter", 267),  # Unlocks with: 9 x Desc_CircuitBoardHighSpeed_C
        DropPodData(115978, 21424,  15519,  None, 0),  # Unlocks with: (No Item)
        DropPodData(-78236, 90857,  20305,  "Radio Control Unit", 0),  # Unlocks with: 6 x Desc_ModularFrameLightweight_C
        DropPodData(-35359, 116594, 21827,  "Turbo Motor", 0),  # Unlocks with: 6 x Desc_MotorLightweight_C
        DropPodData(111479, -54515, 17081,  "Stator", 20),  # Unlocks with: 1 x Desc_Stator_C
        DropPodData(121061, 45324,  17373,  None, 0),  # Unlocks with: (No Item)
        DropPodData(125497, -34949, 8220,   None, 50),  # Unlocks with: (No Item)
        DropPodData(-26327, -129047, 7780,   "Modular Frame", 0),  # Unlocks with: 1 x Desc_ModularFrame_C
        DropPodData(21373,  132336, 2510,   "Motor", 20),  # Unlocks with: 2 x Desc_Motor_C
        DropPodData(17807,  -136922, 13621,  "Rotor", 0),  # Unlocks with: 1 x Desc_Rotor_C
        DropPodData(-118480, 74929,  16995,  None, 420),  # Unlocks with: (No Item)
        DropPodData(94940,  105482, 9860,   "Heavy Modular Frame", 0),  # Unlocks with: 1 x Desc_ModularFrameHeavy_C
        DropPodData(-129115, 60165,  4800,   None, 53),  # Unlocks with: (No Item)
        DropPodData(-142000, 23970,  32660,  None, 0),  # Unlocks with: (No Item)
        DropPodData(46048,  141933, 13064,  None, 40),  # Unlocks with: (No Item)
        DropPodData(144456, 36294,  17301,  "Circuit Board", 48),  # Unlocks with: 20 x Desc_CircuitBoard_C
        DropPodData(-43144, 145820, 7472,   "Modular Frame", 0),  # Unlocks with: 5 x Desc_ModularFrame_C
        DropPodData(-108774, 107811, 10154,  "Crystal Oscillator", 0),  # Unlocks with: 1 x Desc_CrystalOscillator_C
        DropPodData(-56987, -144603, 2072,   "Rotor", 10),  # Unlocks with: 1 x Desc_Rotor_C
        DropPodData(-152676, 33864,  19283,  None, 256),  # Unlocks with: (No Item)
        DropPodData(90313,  129583, 9112,   "Crystal Oscillator", 20),  # Unlocks with: 2 x Desc_CrystalOscillator_C
        DropPodData(111212, -113040, 12036,  "Screw", 10),  # Unlocks with: 15 x Desc_IronScrew_C
        DropPodData(-157077, -6312,  25128,  "Turbo Motor", 0),  # Unlocks with: 8 x Desc_MotorLightweight_C
        DropPodData(157249, -40206, 13694,  "High-Speed Connector", 0),  # Unlocks with: 2 x Desc_HighSpeedConnector_C
        DropPodData(-151842, 72468,  9945,   "Encased Industrial Beam", 0),  # Unlocks with: 3 x Desc_SteelPlateReinforced_C
        DropPodData(64696,  156038, 14067,  "Modular Frame", 0),  # Unlocks with: 6 x Desc_ModularFrame_C
        DropPodData(-157080, -67028, 11766,  "Rotor", 0),  # Unlocks with: 4 x Desc_Rotor_C
        DropPodData(170057, -10579, 18823,  None, 50),  # Unlocks with: (No Item)
        DropPodData(143671, 92573,  24990,  "Crystal Oscillator", 20),  # Unlocks with: 2 x Desc_CrystalOscillator_C
        DropPodData(127215, -116866, -1397,  "Rubber", 0),  # Unlocks with: 10 x Desc_Rubber_C
        DropPodData(163999, 61333,  21481,  "AI Limiter", 0),  # Unlocks with: 3 x Desc_CircuitBoardHighSpeed_C
        DropPodData(98306,  -149781, 2552,   None, 40),  # Unlocks with: (No Item)
        DropPodData(5302,   -187090, -1608,  None, 0),  # Unlocks with: (No Item)
        DropPodData(188304, 17059,  12949,  None, 0),  # Unlocks with: (No Item)
        DropPodData(84256,  -171122, -290,   None, 0),  # Unlocks with: (No Item)
        DropPodData(191366, 37694,  5676,   "Computer", 0),  # Unlocks with: 4 x Desc_Computer_C
        DropPodData(28695,  193441, 17459,  "Quickwire", 0),  # Unlocks with: 9 x Desc_HighSpeedWire_C
        DropPodData(-146044, -137047, 2357,   "Modular Frame", 0),  # Unlocks with: 9 x Desc_ModularFrame_C
        DropPodData(-200203, -17766, 12193,  "Solid Biofuel", 0),  # Unlocks with: 10 x Desc_Biofuel_C
        DropPodData(47834,  195703, 2943,   "Black Powder", 0),  # Unlocks with: 4 x Desc_Gunpowder_C
        DropPodData(198418, -41186, 13786,  None, 0),  # Unlocks with: (No Item)
        DropPodData(-195756, -59210, -84,    None, 30),  # Unlocks with: (No Item)
        DropPodData(-121994, 166916, -49,    "Steel Beam", 20),  # Unlocks with: 4 x Desc_SteelPlate_C
        DropPodData(88323,  188913, 1420,   None, 30),  # Unlocks with: (No Item)
        DropPodData(-123677, -167107, 29710,  "Motor", 0),  # Unlocks with: 4 x Desc_Motor_C
        DropPodData(150633, 146698, 7727,   "Crystal Oscillator", 20),  # Unlocks with: 2 x Desc_CrystalOscillator_C
        DropPodData(-55111, -204857, 7844,   "Motor", 0),  # Unlocks with: 30 x Desc_Motor_C
        DropPodData(216096, -268,   -1592,  "Heat Sink", 0),  # Unlocks with: 7 x Desc_AluminumPlateReinforced_C
        DropPodData(159088, -145116, 23164,  "Motor", 0),  # Unlocks with: 30 x Desc_Motor_C
        DropPodData(207683, -68352, 3927,   "Encased Industrial Beam", 20),  # Unlocks with: 27 x Desc_SteelPlateReinforced_C
        DropPodData(-189258, 116331, -1764,  None, 0),  # Unlocks with: (No Item)
        DropPodData(46951,  221859, 5917,   None, 20),  # Unlocks with: (No Item)
        DropPodData(-9988,  227625, -1017,  None, 40),  # Unlocks with: (No Item)
        DropPodData(232515, -20519, 8979,   "Crystal Oscillator", 15),  # Unlocks with: 2 x Desc_CrystalOscillator_C
        DropPodData(232138, 27191,  -1629,  "Supercomputer", 0),  # Unlocks with: 5 x Desc_ComputerSuper_C
        DropPodData(-135,   -237257, -1760,  None, 0),  # Unlocks with: (No Item)
        DropPodData(-232498, -51432, -386,   "Rotor", 0),  # Unlocks with: 21 x Desc_Rotor_C
        DropPodData(-238333, 17321,  19741,  "Heat Sink", 0),  # Unlocks with: 3 x Desc_AluminumPlateReinforced_C
        DropPodData(200510, 131912, 6341,   "Motor", 0),  # Unlocks with: 30 x Desc_Motor_C
        DropPodData(-108812, 214051, 3200,   "Quickwire", 0),  # Unlocks with: 1 x Desc_HighSpeedWire_C
        DropPodData(232255, 79925,  -1275,  "Turbo Motor", 67),  # Unlocks with: 2 x Desc_MotorLightweight_C
        DropPodData(226418, 98109,  7339,   None, 200),  # Unlocks with: (No Item)
        DropPodData(156569, 191767, -9312,  "Rubber", 0),  # Unlocks with: 4 x Desc_Rubber_C
        DropPodData(44579,  -244343, -874,   None, 0),  # Unlocks with: (No Item)
        DropPodData(118349, 221905, -7063,  "Encased Industrial Beam", 0),  # Unlocks with: 6 x Desc_SteelPlateReinforced_C
        # DropPodData(249919, 59534,  2430,   "Quantum Computer", 0), # Unlocks with: 1 x Desc_ComputerQuantum_C
        DropPodData(188233, 177201, 9608,   "Quickwire", 0),  # Unlocks with: 12 x Desc_HighSpeedWire_C
        DropPodData(-174494, -197134, -1538,  None, 30),  # Unlocks with: (No Item)
        DropPodData(-50655, -259272, -1667,  None, 0),  # Unlocks with: (No Item)
        DropPodData(30383,  266975, -987,   "Screw", 0),  # Unlocks with: 12 x Desc_IronScrew_C
        DropPodData(272715, 28087,  -1586,  "Supercomputer", 0),  # Unlocks with: 2 x Desc_ComputerSuper_C
        DropPodData(-152279, 229520, 1052,   "Modular Frame", 0),  # Unlocks with: 5 x Desc_ModularFrame_C
        DropPodData(241532, 131343, 17157,  None, 0),  # Unlocks with: (No Item)
        DropPodData(-259577, 105048, -1548,  None, 0),  # Unlocks with: (No Item)
        DropPodData(275070, -52585, 5980,   None, 0),  # Unlocks with: (No Item)
        DropPodData(-247303, -142348, 4524,   "Rotor", 0),  # Unlocks with: 4 x Desc_Rotor_C
        DropPodData(261797, 124616, -2597,  "AI Limiter", 73),  # Unlocks with: 3 x Desc_CircuitBoardHighSpeed_C
        DropPodData(187056, 223656, -3215,  None, 42),  # Unlocks with: (No Item)
        DropPodData(293299, 51,     522,    "Crystal Oscillator", 42),  # Unlocks with: 8 x Desc_CrystalOscillator_C
        DropPodData(219146, -199880, 6503,   "Rotor", 0),  # Unlocks with: 10 x Desc_Rotor_C
        DropPodData(176423, 243273, -9780,  "Motor", 19),  # Unlocks with: 3 x Desc_Motor_C
        DropPodData(291821, 74782, -1574,  "Superposition Oscillator", 0),  # Unlocks with: 5 x Desc_QuantumOscillator_C
        DropPodData(-78884, 292640, -4763,  "Modular Frame", 0),  # Unlocks with: 5 x Desc_ModularFrame_C
        DropPodData(174948, -276436, 21151,  "Motor", 0),  # Unlocks with: 30 x Desc_Motor_C
        DropPodData(295166, -173139, 8083,   None, 0),  # Unlocks with: (No Item)
        DropPodData(349295, -38831, -1485,  "Motor", 0),  # Unlocks with: 10 x Desc_Motor_C
        DropPodData(360114, -106614, 11815,  "Motor", 0),  # Unlocks with: 35 x Desc_Motor_C
        DropPodData(303169, -246169, 5487,   None, 50),  # Unlocks with: (No Item)
        DropPodData(236508, -312236, 9971,   "Motor", 0),  # Unlocks with: 30 x Desc_Motor_C
        DropPodData(360285, -217558, 3900,   None, 70),  # Unlocks with: (No Item)
        DropPodData(366637, -303548, -7288,  None, 0),  # Unlocks with: (No Item)
    ]
