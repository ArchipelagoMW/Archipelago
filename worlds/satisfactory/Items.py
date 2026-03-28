from random import Random
from typing import ClassVar, Optional
from collections.abc import Sequence
from BaseClasses import Item, ItemClassification as C
from .GameLogic import GameLogic
from .Options import SatisfactoryOptions
from .ItemData import ItemData, ItemGroups as G
from .CriticalPathCalculator import CriticalPathCalculator


class Items:
    item_data: ClassVar[dict[str, ItemData]] = {
        # Resource Bundles
        "Bundle: Adaptive Control Unit": ItemData(G.Parts, 1338000, count=0),
        "Bundle: AI Limiter": ItemData(G.Parts, 1338001),
        "Bundle: Alclad Aluminum Sheet": ItemData(G.Parts, 1338002),
        "Bundle: Blue Power Slug": ItemData(G.Parts, 1338003),
        "Bundle: Yellow Power Slug": ItemData(G.Parts, 1338004),
        "Bundle: Alien Protein": ItemData(G.Parts, 1338005),
        "Bundle: Purple Power Slug": ItemData(G.Parts, 1338006),
        "Bundle: Aluminum Casing": ItemData(G.Parts, 1338007),
        "Bundle: Aluminum Ingot": ItemData(G.Parts, 1338008),
        "Bundle: Aluminum Scrap": ItemData(G.Parts, 1338009),
        "Bundle: Assembly Director System": ItemData(G.Parts, 1338010, count=0),
        "Bundle: Automated Wiring": ItemData(G.Parts, 1338011, count=0),
        "Bundle: Battery": ItemData(G.Parts, 1338012),
        "Bundle: Bauxite": ItemData(G.Parts, 1338013),
        "Bundle: Neural-Quantum Processor": ItemData(G.Parts, 1338014),  # 1.0
        "Bundle: Biomass": ItemData(G.Parts, 1338015),
        "Bundle: Black Powder": ItemData(G.Parts, 1338016),
        "Bundle: Cable": ItemData(G.Parts, 1338017),
        "Bundle: Caterium Ingot": ItemData(G.Parts, 1338018),
        "Bundle: Caterium Ore": ItemData(G.Parts, 1338019),
        "Bundle: Circuit Board": ItemData(G.Parts, 1338020),
        "Bundle: Coal": ItemData(G.Parts, 1338021),
        "Bundle: Singularity Cell": ItemData(G.Parts, 1338022),  # 1.0
        "Bundle: Compacted Coal": ItemData(G.Parts, 1338023),
        "Bundle: Computer": ItemData(G.Parts, 1338024),
        "Bundle: Concrete": ItemData(G.Parts, 1338025),
        "Bundle: Cooling System": ItemData(G.Parts, 1338026),
        "Bundle: Copper Ingot": ItemData(G.Parts, 1338027),
        "Bundle: Copper Ore": ItemData(G.Parts, 1338028),
        "Bundle: Copper Powder": ItemData(G.Parts, 1338029),
        "Bundle: Copper Sheet": ItemData(G.Parts, 1338030),
        "Bundle: Adequate Pioneering Statue": ItemData(G.Parts, 1338031),
        "Bundle: Crystal Oscillator": ItemData(G.Parts, 1338032),
        "Bundle: Electromagnetic Control Rod": ItemData(G.Parts, 1338033),
        "Bundle: Empty Canister": ItemData(G.Parts, 1338034),
        "Bundle: Empty Fluid Tank": ItemData(G.Parts, 1338035),
        "Bundle: Encased Industrial Beam": ItemData(G.Parts, 1338036),
        "Bundle: Encased Plutonium Cell": ItemData(G.Trap, 1338037, C.trap),
        "Bundle: Encased Uranium Cell": ItemData(G.Trap, 1338038, C.trap),
        "Bundle: Fabric": ItemData(G.Parts, 1338039),
        "Bundle: FICSIT Coupon": ItemData(G.Parts, 1338040, count=0),
        "Bundle: AI Expansion Server": ItemData(G.Parts, 1338041, count=0),  # 1.0
        "Bundle: Fused Modular Frame": ItemData(G.Parts, 1338042),
        "Bundle: Hard Drive": ItemData(G.Parts, 1338043, count=0),
        "Bundle: Heat Sink": ItemData(G.Parts, 1338044),
        "Bundle: Heavy Modular Frame": ItemData(G.Parts, 1338045),
        "Bundle: High-Speed Connector": ItemData(G.Parts, 1338046),
        "Bundle: Satisfactory Pioneering Statue": ItemData(G.Parts, 1338047),
        "Bundle: Pretty Good Pioneering Statue": ItemData(G.Parts, 1338048),
        "Bundle: Iron Ingot": ItemData(G.Parts, 1338049),
        "Bundle: Iron Ore": ItemData(G.Parts, 1338050),
        "Bundle: Iron Plate": ItemData(G.Parts, 1338051),
        "Bundle: Iron Rod": ItemData(G.Parts, 1338052),
        "Bundle: Golden Nut Statue": ItemData(G.Parts, 1338053),
        "Bundle: Leaves": ItemData(G.Parts, 1338054),
        "Bundle: Limestone": ItemData(G.Parts, 1338055),
        "Bundle: Magnetic Field Generator": ItemData(G.Parts, 1338056, count=0),
        "Bundle: Mercer Sphere": ItemData(G.Parts, 1338057, count=0),
        "Bundle: Modular Engine": ItemData(G.Parts, 1338058, count=0),
        "Bundle: Modular Frame": ItemData(G.Parts, 1338059),
        "Bundle: Motor": ItemData(G.Parts, 1338060),
        "Bundle: Mycelia": ItemData(G.Parts, 1338061),
        "Bundle: Non-fissile Uranium": ItemData(G.Trap, 1338062, C.trap),
        "Bundle: Nuclear Pasta": ItemData(G.Parts, 1338063, count=0),
        "Bundle: Lizard Doggo Statue": ItemData(G.Parts, 1338064),
        "Bundle: Organic Data Capsule": ItemData(G.Parts, 1338065),
        "Bundle: Packaged Alumina Solution": ItemData(G.Parts, 1338066),
        "Bundle: Packaged Fuel": ItemData(G.Parts, 1338067),
        "Bundle: Packaged Heavy Oil Residue": ItemData(G.Parts, 1338068),
        "Bundle: Packaged Liquid Biofuel": ItemData(G.Parts, 1338069),
        "Bundle: Packaged Nitric Acid": ItemData(G.Parts, 1338070),
        "Bundle: Packaged Nitrogen Gas": ItemData(G.Parts, 1338071),
        "Bundle: Packaged Oil": ItemData(G.Parts, 1338072),
        "Bundle: Packaged Sulfuric Acid": ItemData(G.Parts, 1338073),
        "Bundle: Packaged Turbofuel": ItemData(G.Parts, 1338074),
        "Bundle: Packaged Water": ItemData(G.Parts, 1338075),
        "Bundle: Petroleum Coke": ItemData(G.Parts, 1338076),
        "Bundle: Plastic": ItemData(G.Parts, 1338077),
        "Bundle: Plutonium Fuel Rod": ItemData(G.Trap, 1338078, C.trap),
        "Bundle: Plutonium Pellet": ItemData(G.Trap, 1338079, C.trap),
        "Bundle: Plutonium Waste": ItemData(G.Trap, 1338080, C.trap),
        "Bundle: Polymer Resin": ItemData(G.Parts, 1338081),
        "Bundle: Power Shard": ItemData(G.Parts, 1338082, count=0),
        "Bundle: Confusing Creature Statue": ItemData(G.Parts, 1338083),
        "Bundle: Pressure Conversion Cube": ItemData(G.Parts, 1338084),
        "Bundle: Alien Power Matrix": ItemData(G.Parts, 1338085),  # 1.0
        "Bundle: Quartz Crystal": ItemData(G.Parts, 1338086),
        "Bundle: Quickwire": ItemData(G.Parts, 1338087),
        "Bundle: Radio Control Unit": ItemData(G.Parts, 1338088),
        "Bundle: Raw Quartz": ItemData(G.Parts, 1338089),
        "Bundle: Reinforced Iron Plate": ItemData(G.Parts, 1338090),
        "Bundle: Rotor": ItemData(G.Parts, 1338091),
        "Bundle: Rubber": ItemData(G.Parts, 1338092),
        "Bundle: SAM": ItemData(G.Parts, 1338093),  # 1.0
        "Bundle: Screw": ItemData(G.Parts, 1338094),
        "Bundle: Silica": ItemData(G.Parts, 1338095),
        "Bundle: Smart Plating": ItemData(G.Parts, 1338096, count=0),
        "Bundle: Smokeless Powder": ItemData(G.Parts, 1338097),
        "Bundle: Solid Biofuel": ItemData(G.Parts, 1338098, C.useful),
        "Bundle: Somersloop": ItemData(G.Parts, 1338099, count=0),
        "Bundle: Stator": ItemData(G.Parts, 1338100),
        "Bundle: Silver Hog Statue": ItemData(G.Parts, 1338101),
        "Bundle: Steel Beam": ItemData(G.Parts, 1338102),
        "Bundle: Steel Ingot": ItemData(G.Parts, 1338103),
        "Bundle: Steel Pipe": ItemData(G.Parts, 1338104),
        "Bundle: Sulfur": ItemData(G.Parts, 1338105),
        "Bundle: Supercomputer": ItemData(G.Parts, 1338106),
        "Bundle: Superposition Oscillator": ItemData(G.Parts, 1338107),
        "Bundle: Thermal Propulsion Rocket": ItemData(G.Parts, 1338108, count=0),
        "Bundle: Turbo Motor": ItemData(G.Parts, 1338109),
        "Bundle: Hog Remains": ItemData(G.Parts, 1338110),
        "Bundle: Uranium": ItemData(G.Trap, 1338111, C.trap),
        "Bundle: Uranium Fuel Rod": ItemData(G.Trap, 1338112, C.trap),
        "Bundle: Uranium Waste": ItemData(G.Trap, 1338113, C.trap),
        "Bundle: Versatile Framework": ItemData(G.Parts, 1338114, count=0),
        "Bundle: Wire": ItemData(G.Parts, 1338115),
        "Bundle: Wood": ItemData(G.Parts, 1338116),
        "Bundle: Plasma Spitter Remains": ItemData(G.Parts, 1338117),
        "Bundle: Stinger Remains": ItemData(G.Parts, 1338118),
        "Bundle: Hatcher Remains": ItemData(G.Parts, 1338119),
        "Bundle: Alien DNA Capsule": ItemData(G.Parts, 1338120),
        "Bundle: Diamonds": ItemData(G.Parts, 1338121),
        "Bundle: Time Crystal": ItemData(G.Parts, 1338122),
        "Bundle: Ficsite Ingot": ItemData(G.Parts, 1338123),
        "Bundle: Ficsite Trigon": ItemData(G.Parts, 1338124),
        "Bundle: Reanimated SAM": ItemData(G.Parts, 1338125),
        "Bundle: SAM Fluctuator": ItemData(G.Parts, 1338126),
        "Bundle: Biochemical Sculptor": ItemData(G.Parts, 1338127, count=0),
        "Bundle: Ballistic Warp Drive": ItemData(G.Parts, 1338128, count=0),
        "Bundle: Ficsonium": ItemData(G.Trap, 1338129, C.trap),
        "Bundle: Ficsonium Fuel Rod": ItemData(G.Trap, 1338130, C.trap),
        "Bundle: Packaged Rocket Fuel": ItemData(G.Parts, 1338131),
        "Bundle: Packaged Ionized Fuel": ItemData(G.Parts, 1338132),
        "Bundle: Dark Matter Crystal": ItemData(G.Parts, 1338133),
        # 1338134 - 1338149 Reserved for future parts
        # 1338150 - 1338199 Equipment / Ammo
        "Bundle: Bacon Agaric": ItemData(G.Ammo, 1338150, count=0),
        "Bundle: Beryl Nut": ItemData(G.Ammo, 1338151, count=0),
        "Bundle: Blade Runners": ItemData(G.Equipment, 1338152, count=0),
        "Bundle: Boom Box": ItemData(G.Equipment, 1338153, count=0),
        "Bundle: Chainsaw": ItemData(G.Equipment, 1338154, count=0),
        "Bundle: Cluster Nobelisk": ItemData(G.Ammo, 1338155),
        "Bundle: Iodine-Infused Filter": ItemData(G.Equipment, 1338156, count=3),  # 1.1
        "Bundle: Cup": ItemData(G.Equipment, 1338157, count=0),
        "Bundle: Cup (gold)": ItemData(G.Equipment, 1338158, count=0),
        "Bundle: Explosive Rebar": ItemData(G.Ammo, 1338159),
        "Bundle: Factory Cart": ItemData(G.Equipment, 1338160, count=0),
        "Bundle: Factory Cart (golden)": ItemData(G.Equipment, 1338161, count=0),
        "Bundle: Gas Mask": ItemData(G.Equipment, 1338162, count=0),
        "Bundle: Gas Nobelisk": ItemData(G.Ammo, 1338163),
        "Bundle: Hazmat Suit": ItemData(G.Equipment, 1338164, count=0),
        "Bundle: Homing Rifle Ammo": ItemData(G.Ammo, 1338165),
        "Bundle: Hoverpack": ItemData(G.Equipment, 1338166, count=0),
        "Bundle: Iron Rebar": ItemData(G.Ammo, 1338167),
        "Bundle: Jetpack": ItemData(G.Equipment, 1338168, count=0),
        "Bundle: Medicinal Inhaler": ItemData(G.Ammo, 1338169),
        "Bundle: Nobelisk": ItemData(G.Ammo, 1338170),
        "Bundle: Nobelisk Detonator": ItemData(G.Equipment, 1338171, count=0),
        "Bundle: Nuke Nobelisk": ItemData(G.Ammo, 1338172),
        "Bundle: Object Scanner": ItemData(G.Equipment, 1338173, count=0),
        "Bundle: Paleberry": ItemData(G.Ammo, 1338174, count=0),
        "Bundle: Parachute": ItemData(G.Equipment, 1338175, count=0),
        "Bundle: Pulse Nobelisk": ItemData(G.Ammo, 1338176),
        "Bundle: Rebar Gun": ItemData(G.Equipment, 1338177, count=0),
        "Bundle: Rifle": ItemData(G.Equipment, 1338178, count=0),
        "Bundle: Rifle Ammo": ItemData(G.Ammo, 1338179),
        "Bundle: Shatter Rebar": ItemData(G.Ammo, 1338180),
        "Bundle: Stun Rebar": ItemData(G.Ammo, 1338181),
        "Bundle: Turbo Rifle Ammo": ItemData(G.Ammo, 1338182),
        "Bundle: Xeno-Basher": ItemData(G.Equipment, 1338183, count=0),
        "Bundle: Xeno-Zapper": ItemData(G.Equipment, 1338184, count=0),
        "Bundle: Zipline": ItemData(G.Equipment, 1338185, count=0),
        "Bundle: Portable Miner": ItemData(G.Equipment, 1338186, count=0),
        "Bundle: Gas Filter": ItemData(G.Equipment, 1338187, count=3),
        # Special cases
        "Small Inflated Pocket Dimension": ItemData(G.Upgrades, 1338188, C.useful, 11),
        "Inflated Pocket Dimension": ItemData(G.Upgrades, 1338189, C.useful, 5),
        "Expanded Toolbelt": ItemData(G.Upgrades, 1338190, C.useful, 5),
        "Dimensional Depot upload from inventory": ItemData(G.Upgrades, 1338191, C.useful),
# added in 1.1
        "Bundle of Three: Power Shards": ItemData(G.Parts, 1338192),
        "Bundle of Three: Mercer Spheres": ItemData(G.Parts, 1338193),
        "Bundle of Four: Somersloops": ItemData(G.Parts, 1338194),
        "Bundle of Three: Hard Drives": ItemData(G.Parts, 1338195),
#
# Ficsmas
        "FICSMAS Data Cartridge Day 1": ItemData(G.Ammo | G.Ficsmas, 1338196, C.progression, 0), # removed
        "FICSMAS Data Cartridge Day 4": ItemData(G.Ammo | G.Ficsmas, 1338197, C.progression),
        "FICSMAS Data Cartridge Day 8": ItemData(G.Ammo | G.Ficsmas, 1338198, C.progression),
        "FICSMAS Data Cartridge Day 14": ItemData(G.Ammo | G.Ficsmas, 1338199, C.progression),
#
        # 1338200+ Recipes / buildings / schematics
        "Recipe: Reinforced Iron Plate": ItemData(G.Recipe, 1338200, C.progression),
        "Recipe: Adhered Iron Plate": ItemData(G.Recipe, 1338201, C.progression),
        "Recipe: Bolted Iron Plate": ItemData(G.Recipe, 1338202, C.progression),
        "Recipe: Stitched Iron Plate": ItemData(G.Recipe, 1338203, C.progression),
        "Recipe: Rotor": ItemData(G.Recipe, 1338204, C.progression),
        "Recipe: Copper Rotor": ItemData(G.Recipe, 1338205, C.progression),
        "Recipe: Steel Rotor": ItemData(G.Recipe, 1338206, C.progression),
        "Recipe: Stator": ItemData(G.Recipe, 1338207, C.progression),
        "Recipe: Quickwire Stator": ItemData(G.Recipe, 1338208, C.progression),
        "Recipe: Plastic": ItemData(G.Recipe, 1338209, C.progression),
        "Recipe: Residual Plastic": ItemData(G.Recipe, 1338210, C.progression),
        "Recipe: Recycled Plastic": ItemData(G.Recipe, 1338211, C.progression),
        "Recipe: Rubber": ItemData(G.Recipe, 1338212, C.progression),
        "Recipe: Residual Rubber": ItemData(G.Recipe, 1338213, C.progression),
        "Recipe: Recycled Rubber": ItemData(G.Recipe, 1338214, C.progression),
        "Recipe: Iron Plate": ItemData(G.Recipe, 1338215, C.progression),
        "Recipe: Coated Iron Plate": ItemData(G.Recipe, 1338216, C.progression),
        "Recipe: Steel Cast Plate": ItemData(G.Recipe, 1338217, C.progression),  # 1.0
        "Recipe: Iron Rod": ItemData(G.Recipe, 1338218, C.progression),
        "Recipe: Steel Rod": ItemData(G.Recipe, 1338219, C.progression),
        "Recipe: Screw": ItemData(G.Recipe, 1338220, C.progression),
        "Recipe: Cast Screw": ItemData(G.Recipe, 1338221, C.progression),
        "Recipe: Steel Screw": ItemData(G.Recipe, 1338222, C.progression),
        "Recipe: Wire": ItemData(G.Recipe, 1338223, C.progression),
        "Recipe: Fused Wire": ItemData(G.Recipe, 1338224, C.progression),
        "Recipe: Iron Wire": ItemData(G.Recipe, 1338225, C.progression),
        "Recipe: Caterium Wire": ItemData(G.Recipe, 1338226, C.progression),
        "Recipe: Cable": ItemData(G.Recipe, 1338227, C.progression),
        "Recipe: Coated Cable": ItemData(G.Recipe, 1338228, C.progression),
        "Recipe: Insulated Cable": ItemData(G.Recipe, 1338229, C.progression),
        "Recipe: Quickwire Cable": ItemData(G.Recipe, 1338230, C.progression),
        "Recipe: Quickwire": ItemData(G.Recipe, 1338231, C.progression),
        "Recipe: Fused Quickwire": ItemData(G.Recipe, 1338232, C.progression),
        "Recipe: Copper Sheet": ItemData(G.Recipe, 1338233, C.progression),
        "Recipe: Steamed Copper Sheet": ItemData(G.Recipe, 1338234, C.progression),
        "Recipe: Steel Pipe": ItemData(G.Recipe, 1338235, C.progression),
        "Recipe: Steel Beam": ItemData(G.Recipe, 1338236, C.progression),
        "Recipe: Neural-Quantum Processor": ItemData(G.Recipe, 1338237, C.progression),  # 1.0
        "Recipe: Heavy Oil Residue": ItemData(G.Recipe, 1338238, C.progression),
        "Recipe: Polymer Resin": ItemData(G.Recipe, 1338239, C.progression),
        "Recipe: Fuel": ItemData(G.Recipe, 1338240, C.progression),
        "Recipe: Residual Fuel": ItemData(G.Recipe, 1338241, C.progression),
        "Recipe: Diluted Packaged Fuel": ItemData(G.Recipe, 1338242, C.progression),
        "Recipe: AI Expansion Server": ItemData(G.Recipe, 1338243, C.progression),  # 1.0
        "Recipe: Concrete": ItemData(G.Recipe, 1338244, C.progression),
        "Recipe: Rubber Concrete": ItemData(G.Recipe, 1338245, C.progression),
        "Recipe: Wet Concrete": ItemData(G.Recipe, 1338246, C.progression),
        "Recipe: Fine Concrete": ItemData(G.Recipe, 1338247, C.progression),
        "Recipe: Silica": ItemData(G.Recipe, 1338248, C.progression),
        "Recipe: Cheap Silica": ItemData(G.Recipe, 1338249, C.progression),
        "Recipe: Quartz Crystal": ItemData(G.Recipe, 1338250, C.progression),
        "Recipe: Pure Quartz Crystal": ItemData(G.Recipe, 1338251, C.progression),
        "Recipe: Iron Ingot": ItemData(G.Recipe, 1338252, C.progression),
        "Recipe: Pure Iron Ingot": ItemData(G.Recipe, 1338253, C.progression),
        "Recipe: Iron Alloy Ingot": ItemData(G.Recipe, 1338254, C.progression),
        "Recipe: Steel Ingot": ItemData(G.Recipe, 1338255, C.progression),
        "Recipe: Coke Steel Ingot": ItemData(G.Recipe, 1338256, C.progression),
        "Recipe: Compacted Steel Ingot": ItemData(G.Recipe, 1338257, C.progression),
        "Recipe: Solid Steel Ingot": ItemData(G.Recipe, 1338258, C.progression),
        "Recipe: Copper Ingot": ItemData(G.Recipe, 1338259, C.progression),
        "Recipe: Copper Alloy Ingot": ItemData(G.Recipe, 1338260, C.progression),
        "Recipe: Pure Copper Ingot": ItemData(G.Recipe, 1338261, C.progression),
        "Recipe: Caterium Ingot": ItemData(G.Recipe, 1338262, C.progression),
        "Recipe: Pure Caterium Ingot": ItemData(G.Recipe, 1338263, C.progression),
        "Recipe: Alien Power Matrix": ItemData(G.Recipe, 1338264),  # 1.0
        "Recipe: Ficsite Ingot (Aluminum)": ItemData(G.Recipe, 1338265, C.progression),  # 1.0
        "Recipe: Ficsite Ingot (Caterium)": ItemData(G.Recipe, 1338266, C.progression),  # 1.0
        "Recipe: Ficsite Ingot (Iron)": ItemData(G.Recipe, 1338267, C.progression),  # 1.0
        "Recipe: Ficsite Trigon": ItemData(G.Recipe, 1338268, C.progression),  # 1.0
        "Recipe: Reanimated SAM": ItemData(G.Recipe, 1338269, C.progression),  # 1.0
        "Recipe: SAM Fluctuator": ItemData(G.Recipe, 1338270, C.progression),  # 1.0
        "Recipe: Petroleum Coke": ItemData(G.Recipe, 1338271, C.progression),
        "Recipe: Compacted Coal": ItemData(G.Recipe, 1338272, C.progression),
        "Recipe: Motor": ItemData(G.Recipe, 1338273, C.progression),
        "Recipe: Rigor Motor": ItemData(G.Recipe, 1338274, C.progression),
        "Recipe: Electric Motor": ItemData(G.Recipe, 1338275, C.progression),
        "Recipe: Modular Frame": ItemData(G.Recipe, 1338276, C.progression),
        "Recipe: Bolted Frame": ItemData(G.Recipe, 1338277, C.progression),
        "Recipe: Steeled Frame": ItemData(G.Recipe, 1338278, C.progression),
        "Recipe: Heavy Modular Frame": ItemData(G.Recipe, 1338279, C.progression),
        "Recipe: Heavy Flexible Frame": ItemData(G.Recipe, 1338280, C.progression),
        "Recipe: Heavy Encased Frame": ItemData(G.Recipe, 1338281, C.progression),
        "Recipe: Encased Industrial Beam": ItemData(G.Recipe, 1338282, C.progression),
        "Recipe: Encased Industrial Pipe": ItemData(G.Recipe, 1338283, C.progression),
        "Recipe: Computer": ItemData(G.Recipe, 1338284, C.progression),
        "Recipe: Crystal Computer": ItemData(G.Recipe, 1338285, C.progression),
        "Recipe: Caterium Computer": ItemData(G.Recipe, 1338286, C.progression),
        "Recipe: Circuit Board": ItemData(G.Recipe, 1338287, C.progression),
        "Recipe: Electrode Circuit Board": ItemData(G.Recipe, 1338288, C.progression),
        "Recipe: Silicon Circuit Board": ItemData(G.Recipe, 1338289, C.progression),
        "Recipe: Caterium Circuit Board": ItemData(G.Recipe, 1338290, C.progression),
        "Recipe: Crystal Oscillator": ItemData(G.Recipe, 1338291, C.progression),
        "Recipe: Insulated Crystal Oscillator": ItemData(G.Recipe, 1338292, C.progression),
        "Recipe: AI Limiter": ItemData(G.Recipe, 1338293, C.progression),
        "Recipe: Electromagnetic Control Rod": ItemData(G.Recipe, 1338294, C.progression),
        "Recipe: Electromagnetic Connection Rod": ItemData(G.Recipe, 1338295, C.progression),
        "Recipe: High-Speed Connector": ItemData(G.Recipe, 1338296, C.progression),
        "Recipe: Silicon High-Speed Connector": ItemData(G.Recipe, 1338297, C.progression),
        "Recipe: Smart Plating": ItemData(G.Recipe, 1338298, C.progression),
        "Recipe: Plastic Smart Plating": ItemData(G.Recipe, 1338299, C.progression),
        "Recipe: Versatile Framework": ItemData(G.Recipe, 1338300, C.progression),
        "Recipe: Flexible Framework": ItemData(G.Recipe, 1338301, C.progression),
        "Recipe: Automated Wiring": ItemData(G.Recipe, 1338302, C.progression),
        "Recipe: Automated Speed Wiring": ItemData(G.Recipe, 1338303, C.progression),
        "Recipe: Modular Engine": ItemData(G.Recipe, 1338304, C.progression),
        "Recipe: Adaptive Control Unit": ItemData(G.Recipe, 1338305, C.progression),
        "Recipe: Diluted Fuel": ItemData(G.Recipe, 1338306, C.progression),
        "Recipe: Alumina Solution": ItemData(G.Recipe, 1338307, C.progression),
        "Recipe: Automated Miner": ItemData(G.Recipe, 1338308, C.progression),
        "Recipe: Singularity Cell": ItemData(G.Recipe, 1338309, C.progression),  # 1.0
        "Recipe: Aluminum Scrap": ItemData(G.Recipe, 1338310, C.progression),
        "Recipe: Electrode Aluminum Scrap": ItemData(G.Recipe, 1338311, C.progression),
        "Recipe: Instant Scrap": ItemData(G.Recipe, 1338312, C.progression),
        "Recipe: Aluminum Ingot": ItemData(G.Recipe, 1338313, C.progression),
        "Recipe: Pure Aluminum Ingot": ItemData(G.Recipe, 1338314, C.progression),
        "Recipe: Alclad Aluminum Sheet": ItemData(G.Recipe, 1338315, C.progression),
        "Recipe: Aluminum Casing": ItemData(G.Recipe, 1338316, C.progression),
        "Recipe: Alclad Casing": ItemData(G.Recipe, 1338317, C.progression),
        "Recipe: Heat Sink": ItemData(G.Recipe, 1338318, C.progression),
        "Recipe: Heat Exchanger": ItemData(G.Recipe, 1338319, C.progression),
        "Recipe: Synthetic Power Shard": ItemData(G.Recipe, 1338320, C.progression),
        "Recipe: Nitric Acid": ItemData(G.Recipe, 1338321, C.progression),
        "Recipe: Fused Modular Frame": ItemData(G.Recipe, 1338322, C.progression),
        "Recipe: Heat-Fused Frame": ItemData(G.Recipe, 1338323, C.progression),
        "Recipe: Radio Control Unit": ItemData(G.Recipe, 1338324, C.progression),
        "Recipe: Radio Connection Unit": ItemData(G.Recipe, 1338325, C.progression),
        "Recipe: Radio Control System": ItemData(G.Recipe, 1338326, C.progression),
        "Recipe: Pressure Conversion Cube": ItemData(G.Recipe, 1338327, C.progression),
        "Recipe: Cooling System": ItemData(G.Recipe, 1338328, C.progression),
        "Recipe: Cooling Device": ItemData(G.Recipe, 1338329, C.progression),
        "Recipe: Turbo Motor": ItemData(G.Recipe, 1338330, C.progression),
        "Recipe: Turbo Electric Motor": ItemData(G.Recipe, 1338331, C.progression),
        "Recipe: Turbo Pressure Motor": ItemData(G.Recipe, 1338332, C.progression),
        "Recipe: Battery": ItemData(G.Recipe, 1338333, C.progression),
        "Recipe: Classic Battery": ItemData(G.Recipe, 1338334, C.progression),
        "Recipe: Supercomputer": ItemData(G.Recipe, 1338335, C.progression),
        "Recipe: OC Supercomputer": ItemData(G.Recipe, 1338336, C.progression),
        "Recipe: Super-State Computer": ItemData(G.Recipe, 1338337, C.progression),
        "Recipe: Biochemical Sculptor": ItemData(G.Recipe, 1338338, C.progression),  # 1.0
        "Recipe: Sulfuric Acid": ItemData(G.Recipe, 1338339, C.progression),
        "Recipe: Ballistic Warp Drive": ItemData(G.Recipe, 1338340, C.progression),  # 1.0
        "Recipe: Encased Uranium Cell": ItemData(G.Recipe, 1338341, C.progression),
        "Recipe: Infused Uranium Cell": ItemData(G.Recipe, 1338342, C.progression),
        "Recipe: Uranium Fuel Rod": ItemData(G.Recipe, 1338343, C.progression),
        "Recipe: Uranium Fuel Unit": ItemData(G.Recipe, 1338344, C.progression),
        "Recipe: Aluminum Beam": ItemData(G.Recipe, 1338345, C.progression),  # 1.0
        "Recipe: Aluminum Rod": ItemData(G.Recipe, 1338346, C.progression),  # 1.0
        "Recipe: Basic Iron Ingot": ItemData(G.Recipe, 1338347, C.progression),  # 1.0
        "Recipe: Non-fissile Uranium": ItemData(G.Recipe, 1338348, C.progression),
        "Recipe: Fertile Uranium": ItemData(G.Recipe, 1338349, C.progression),
        "Recipe: Plutonium Pellet": ItemData(G.Recipe, 1338350),
        "Recipe: Encased Plutonium Cell": ItemData(G.Recipe, 1338351),
        "Recipe: Instant Plutonium Cell": ItemData(G.Recipe, 1338352),
        "Recipe: Plutonium Fuel Rod": ItemData(G.Recipe, 1338353),
        "Recipe: Plutonium Fuel Unit": ItemData(G.Recipe, 1338354),
        "Recipe: Gas Filter": ItemData(G.Recipe, 1338355, C.progression),
        "Recipe: Iodine-Infused Filter": ItemData(G.Recipe, 1338356, C.progression),
        "Recipe: Assembly Director System": ItemData(G.Recipe, 1338357, C.progression),
        "Recipe: Magnetic Field Generator": ItemData(G.Recipe, 1338358, C.progression),
        "Recipe: Copper Powder": ItemData(G.Recipe, 1338359, C.progression),
        "Recipe: Nuclear Pasta": ItemData(G.Recipe, 1338360, C.progression),
        "Recipe: Thermal Propulsion Rocket": ItemData(G.Recipe, 1338361, C.progression),
        "Recipe: Ficsonium": ItemData(G.Recipe, 1338362),  # 1.0
        "Recipe: Ficsonium Fuel Rod": ItemData(G.Recipe, 1338363),  # 1.0
        "Recipe: Dark Matter Crystal": ItemData(G.Recipe, 1338364, C.progression),  # 1.0
        "Recipe: Dark Matter Crystallization": ItemData(G.Recipe, 1338365, C.progression),  # 1.0
        "Recipe: Dark Matter Trap": ItemData(G.Recipe, 1338366, C.progression),  # 1.0
        "Recipe: Pulse Nobelisk":  ItemData(G.Recipe, 1338367, C.useful),
        "Recipe: Hatcher Protein": ItemData(G.Recipe, 1338368, C.progression),
        "Recipe: Hog Protein": ItemData(G.Recipe, 1338369, C.progression),
        "Recipe: Spitter Protein": ItemData(G.Recipe, 1338370, C.progression),
        "Recipe: Stinger Protein": ItemData(G.Recipe, 1338371, C.progression),
        "Recipe: Biomass (Leaves)": ItemData(G.Recipe, 1338372, C.progression),
        "Recipe: Biomass (Wood)": ItemData(G.Recipe, 1338373, C.progression),
        "Recipe: Biomass (Mycelia)": ItemData(G.Recipe, 1338374, C.progression),
        "Recipe: Biomass (Alien Protein)": ItemData(G.Recipe, 1338375, C.progression),
        "Recipe: Turbo Rifle Ammo (Packaged)": ItemData(G.Recipe, 1338376, C.useful),
        "Recipe: Fabric": ItemData(G.Recipe, 1338377, C.progression),
        "Recipe: Polyester Fabric": ItemData(G.Recipe, 1338378, C.progression),
        "Recipe: Solid Biofuel": ItemData(G.Recipe, 1338379, C.progression),
        "Recipe: Liquid Biofuel": ItemData(G.Recipe, 1338380, C.progression),
        "Recipe: Empty Canister": ItemData(G.Recipe, 1338381, C.progression),
        "Recipe: Coated Iron Canister": ItemData(G.Recipe, 1338382, C.progression),
        "Recipe: Steel Canister": ItemData(G.Recipe, 1338383, C.progression),
        "Recipe: Empty Fluid Tank": ItemData(G.Recipe, 1338384, C.progression),
        "Recipe: Packaged Alumina Solution": ItemData(G.Recipe, 1338385, C.progression),
        "Recipe: Packaged Fuel": ItemData(G.Recipe, 1338386, C.progression),
        "Recipe: Candy Cane Basher": ItemData(G.Recipe | G.Ficsmas, 1338387),  # ficsmas filling the gap
        "Recipe: Packaged Heavy Oil Residue": ItemData(G.Recipe, 1338388, C.progression),
        "Recipe: Packaged Liquid Biofuel": ItemData(G.Recipe, 1338389, C.progression),
        "Recipe: Packaged Nitric Acid": ItemData(G.Recipe, 1338390, C.progression),
        "Recipe: Packaged Nitrogen Gas": ItemData(G.Recipe, 1338391, C.progression),
        "Recipe: Packaged Oil": ItemData(G.Recipe, 1338392, C.progression),
        "Recipe: Packaged Sulfuric Acid": ItemData(G.Recipe, 1338393, C.progression),
        "Recipe: Packaged Turbofuel": ItemData(G.Recipe, 1338394, C.progression),
        "Recipe: Packaged Water": ItemData(G.Recipe, 1338395, C.progression),
        "Recipe: Turbofuel": ItemData(G.Recipe, 1338396, C.progression),
        "Recipe: Turbo Heavy Fuel": ItemData(G.Recipe, 1338397, C.progression),
        "Recipe: Turbo Blend Fuel": ItemData(G.Recipe, 1338398, C.progression),
        "Recipe: Hazmat Suit": ItemData(G.Recipe, 1338399, C.progression),
        "Recipe: Gas Mask": ItemData(G.Recipe, 1338400, C.progression),
        "Recipe: Black Powder": ItemData(G.Recipe, 1338401, C.progression),
        "Recipe: Blade Runners": ItemData(G.Recipe, 1338402, C.useful),
        "Recipe: Chainsaw": ItemData(G.Recipe, 1338403, C.useful),
        "Recipe: Cluster Nobelisk":  ItemData(G.Recipe, 1338404, C.useful),
        "Recipe: Explosive Rebar":  ItemData(G.Recipe, 1338405, C.useful),
        "Recipe: Factory Cart": ItemData(G.Recipe, 1338406, C.useful),
        "Recipe: Gas Nobelisk":  ItemData(G.Recipe, 1338407, C.useful),
        "Recipe: Golden Factory Cart":  ItemData(G.Recipe, 1338408),
        "Recipe: Homing Rifle Ammo": ItemData(G.Recipe, 1338409, C.useful),
        "Recipe: Iron Rebar":  ItemData(G.Recipe, 1338410, C.progression),
        "Recipe: Nobelisk":  ItemData(G.Recipe, 1338411, C.progression),
        "Recipe: Nuke Nobelisk": ItemData(G.Recipe, 1338412, C.useful),
        "Recipe: Nutritional Inhaler":  ItemData(G.Recipe, 1338413, C.useful),
        "Recipe: Object Scanner":  ItemData(G.Recipe, 1338414, C.progression),
        "Recipe: Parachute":  ItemData(G.Recipe, 1338415, C.useful),
        "Recipe: Protein Inhaler": ItemData(G.Recipe, 1338416, C.useful),
        "Recipe: Rebar Gun":  ItemData(G.Recipe, 1338417, C.useful),
        "Recipe: Rifle": ItemData(G.Recipe, 1338418, C.useful),
        "Recipe: Rifle Ammo":  ItemData(G.Recipe, 1338419, C.progression),
        "Recipe: Shatter Rebar":  ItemData(G.Recipe, 1338420, C.useful),
        "Recipe: Stun Rebar":  ItemData(G.Recipe, 1338421, C.useful),
        "Recipe: Therapeutic Inhaler": ItemData(G.Recipe, 1338422, C.useful),
        "Recipe: Turbo Rifle Ammo":  ItemData(G.Recipe, 1338423, C.useful),
        "Recipe: Vitamin Inhaler":  ItemData(G.Recipe, 1338424, C.useful),
        "Recipe: Xeno-Basher": ItemData(G.Recipe, 1338425, C.useful),
        "Recipe: Xeno-Zapper":  ItemData(G.Recipe, 1338426, C.useful),
        "Recipe: Zipline":  ItemData(G.Recipe, 1338427, C.useful),
        "Recipe: Fine Black Powder": ItemData(G.Recipe, 1338428, C.progression),
        "Recipe: Smokeless Powder": ItemData(G.Recipe, 1338429, C.progression),
        "Recipe: Alien DNA Capsule": ItemData(G.Recipe, 1338430, C.progression),
        "Recipe: Power Shard (1)": ItemData(G.Recipe, 1338431, C.progression),
        "Recipe: Power Shard (2)": ItemData(G.Recipe, 1338432, C.useful),
        "Recipe: Power Shard (5)": ItemData(G.Recipe, 1338433, C.useful),

# 1.0
        "Recipe: Diamonds": ItemData(G.Recipe, 1338434, C.progression),
        "Recipe: Cloudy Diamonds": ItemData(G.Recipe, 1338435, C.progression),
        "Recipe: Oil-Based Diamonds": ItemData(G.Recipe, 1338436, C.progression),
        "Recipe: Petroleum Diamonds": ItemData(G.Recipe, 1338437, C.progression),
        "Recipe: Pink Diamonds": ItemData(G.Recipe, 1338438, C.progression),
        "Recipe: Turbo Diamonds": ItemData(G.Recipe, 1338439, C.progression),
        "Recipe: Time Crystal": ItemData(G.Recipe, 1338440, C.progression),
        "Recipe: Superposition Oscillator": ItemData(G.Recipe, 1338441, C.progression),
        # "Recipe: Excited Photonic Matter": ItemData(G.Recipe, 1338442, C.progression), unlocked with converter
        "Recipe: Rocket Fuel": ItemData(G.Recipe, 1338443, C.progression),
        "Recipe: Nitro Rocket Fuel": ItemData(G.Recipe, 1338444, C.progression),
        "Recipe: Ionized Fuel": ItemData(G.Recipe, 1338445, C.useful),
        "Recipe: Packaged Rocket Fuel": ItemData(G.Recipe, 1338446, C.progression),
        "Recipe: Packaged Ionized Fuel": ItemData(G.Recipe, 1338447, C.useful),
        "Recipe: Dark-Ion Fuel": ItemData(G.Recipe, 1338448, C.useful),
        "Recipe: Quartz Purification": ItemData(G.Recipe, 1338449, C.progression),
        "Recipe: Fused Quartz Crystal": ItemData(G.Recipe, 1338450, C.progression),
        "Recipe: Leached Caterium Ingot": ItemData(G.Recipe, 1338451, C.progression),
        "Recipe: Leached Copper Ingot": ItemData(G.Recipe, 1338452, C.progression),
        "Recipe: Leached Iron ingot": ItemData(G.Recipe, 1338453, C.progression),
        "Recipe: Molded Beam": ItemData(G.Recipe, 1338454, C.progression),
        "Recipe: Molded Steel Pipe": ItemData(G.Recipe, 1338455, C.progression),
        "Recipe: Plastic AI Limiter": ItemData(G.Recipe, 1338456, C.progression),
        "Recipe: Tempered Caterium Ingot": ItemData(G.Recipe, 1338457, C.progression),
        "Recipe: Tempered Copper Ingot": ItemData(G.Recipe, 1338458, C.progression),
# 1.0

# added in 1.1 or missed
        "Recipe: Iron Pipe": ItemData(G.Recipe, 1338459, C.progression),
        "Recipe: Biocoal": ItemData(G.Recipe, 1338460, C.useful),
        "Recipe: Charcoal": ItemData(G.Recipe, 1338461, C.useful),
        "Recipe: Sloppy Alumina": ItemData(G.Recipe, 1338462, C.progression),
        "Recipe: Hoverpack": ItemData(G.Recipe, 1338463, C.useful),
        "Recipe: Jetpack": ItemData(G.Recipe | G.NeverExclude, 1338464, C.useful),
        "Recipe: Nobelisk Detonator": ItemData(G.Recipe, 1338465, C.progression),
        "Recipe: Portable Miner": ItemData(G.Recipe, 1338466, C.progression),
# 
        "Recipe: Dark Matter Residue": ItemData(G.Recipe, 1338467, C.progression),

        # Ficsmas
        "Recipe: FICSMAS Tree Branch": ItemData(G.Recipe | G.Ficsmas, 1338468, C.progression),
        "Recipe: Blue FICSMAS Ornament": ItemData(G.Recipe | G.Ficsmas, 1338469, C.progression),
        "Recipe: Red FICSMAS Ornament": ItemData(G.Recipe | G.Ficsmas, 1338470, C.progression),
        "Recipe: Iron FICSMAS Ornament": ItemData(G.Recipe | G.Ficsmas, 1338471, C.progression),
        "Recipe: Copper FICSMAS Ornament": ItemData(G.Recipe | G.Ficsmas, 1338472, C.progression),
        "Recipe: Candy Cane": ItemData(G.Recipe | G.Ficsmas, 1338473, C.progression),
        "Recipe: FICSMAS Actual Snow": ItemData(G.Recipe | G.Ficsmas, 1338474, C.progression),
        "Recipe: FICSMAS Bow": ItemData(G.Recipe | G.Ficsmas, 1338475, C.progression),
        "Recipe: FICSMAS Ornament Bundle": ItemData(G.Recipe | G.Ficsmas, 1338476, C.progression),
        "Recipe: FICSMAS Wreath": ItemData(G.Recipe | G.Ficsmas, 1338477, C.progression),
        "Recipe: FICSMAS Wonder Star": ItemData(G.Recipe | G.Ficsmas, 1338478, C.progression),
        "Recipe: Sweet Fireworks": ItemData(G.Recipe | G.Ficsmas, 1338479, C.useful),
        "Recipe: Fancy Fireworks": ItemData(G.Recipe | G.Ficsmas, 1338480, C.useful),
        "Recipe: Sparkly Fireworks": ItemData(G.Recipe | G.Ficsmas, 1338481, C.useful),
#

        # 1338479 - 1338599 Reserved for future recipes
        # 1338600 - 1338799 buildings / others
        "Building: Constructor": ItemData(G.Building, 1338600, C.progression),  # unlocked by default
        "Building: Assembler": ItemData(G.Building, 1338601, C.progression),
        "Building: Manufacturer": ItemData(G.Building, 1338602, C.progression),
        "Building: Packager": ItemData(G.Building, 1338603, C.progression),
        "Building: Refinery": ItemData(G.Building, 1338604, C.progression),
        "Building: Blender": ItemData(G.Building, 1338605, C.progression),
        "Building: Particle Accelerator": ItemData(G.Building, 1338606, C.progression),
        "Building: Biomass Burner": ItemData(G.Building, 1338607, C.progression),  # unlocked by default
        "Building: Coal Generator": ItemData(G.Building, 1338608, C.progression),
        "Building: Geothermal Generator": ItemData(G.Building, 1338609, C.progression),
        "Building: Nuclear Power Plant": ItemData(G.Building, 1338610, C.progression),
        "Building: Miner Mk.1": ItemData(G.Building, 1338611, C.progression),  # unlocked by default
        "Building: Miner Mk.2": ItemData(G.Building, 1338612, C.progression),
        "Building: Miner Mk.3": ItemData(G.Building, 1338613, C.progression),
        "Building: Oil Extractor": ItemData(G.Building, 1338614, C.progression),
        "Building: Water Extractor": ItemData(G.Building, 1338615, C.progression),
        "Building: Smelter": ItemData(G.Building, 1338616, C.progression),  # unlocked by default
        "Building: Foundry": ItemData(G.Building, 1338617, C.progression),
        "Building: Fuel Generator": ItemData(G.Building, 1338618, C.progression),
        "Building: Resource Well Pressurizer": ItemData(G.Building, 1338619, C.progression),
        "Building: Equipment Workshop": ItemData(G.Building, 1338620, C.progression),
        "Building: AWESOME Sink": ItemData(G.Building | G.NeverExclude, 1338621, C.progression),
        "Building: AWESOME Shop": ItemData(G.Building | G.NeverExclude, 1338622, C.progression),
        "Building: Structural Beam Pack": ItemData(G.Beams, 1338623, C.filler),
        "Building: Blueprint Designer": ItemData(G.Building, 1338624, C.filler, 0),  # unlocked by default
        "Building: Fluid Buffer": ItemData(G.Building | G.NeverExclude, 1338625, C.useful),
        "Building: Industrial Fluid Buffer": ItemData(G.Building | G.NeverExclude, 1338626, C.useful),
        "Building: Jump Pad": ItemData(G.Building, 1338627, C.filler),
        "Building: Ladder": ItemData(G.Building, 1338628, C.filler),
        "Building: MAM": ItemData(G.Building | G.NeverExclude, 1338629, C.progression),
        "Building: Personal Storage Box": ItemData(G.Building, 1338630, C.filler),
        "Building: Power Storage": ItemData(G.Building | G.NeverExclude, 1338631, C.progression),
        "Building: U-Jelly Landing Pad": ItemData(G.Building, 1338632, C.useful),
        "Building: Power Switch": ItemData(G.Building | G.NeverExclude, 1338633, C.useful),
        "Building: Priority Power Switch": ItemData(G.Building | G.NeverExclude, 1338634, C.useful),
        "Building: Storage Container": ItemData(G.Building, 1338635, C.useful, 0),
        "Building: Lookout Tower": ItemData(G.Building, 1338636, C.filler),
        # "Building: Power Pole Mk.1": ItemData(G.Building, 1338637, C.progression), # unlocked by default
        "Building: Power Pole Mk.2": ItemData(G.Building | G.NeverExclude, 1338638, C.useful),
        "Building: Power Pole Mk.3": ItemData(G.Building | G.NeverExclude, 1338639, C.useful),
        "Building: Industrial Storage Container": ItemData(G.Building | G.NeverExclude, 1338640, C.useful),
        "Building: Conveyor Merger": ItemData(G.Building | G.NeverExclude, 1338641, C.progression),
        "Building: Conveyor Splitter": ItemData(G.Building | G.NeverExclude, 1338642, C.progression),
        "Building: Conveyor Mk.1": ItemData(G.Building | G.ConveyorMk1, 1338643, C.progression),  # unlocked by default
        "Building: Conveyor Mk.2": ItemData(G.Building | G.ConveyorMk2, 1338644, C.progression),
        "Building: Conveyor Mk.3": ItemData(G.Building | G.ConveyorMk3, 1338645, C.progression),
        "Building: Conveyor Mk.4": ItemData(G.Building | G.ConveyorMk4, 1338646, C.progression),
        "Building: Conveyor Mk.5": ItemData(G.Building | G.ConveyorMk5, 1338647, C.progression),
        "Building: Conveyor Lift Mk.1": ItemData(G.Building | G.ConveyorMk1, 1338648, C.useful),
        "Building: Conveyor Lift Mk.2": ItemData(G.Building | G.ConveyorMk2, 1338649, C.useful),
        "Building: Conveyor Lift Mk.3": ItemData(G.Building | G.ConveyorMk3, 1338650, C.useful),
        "Building: Conveyor Lift Mk.4": ItemData(G.Building | G.ConveyorMk4, 1338651, C.useful),
        "Building: Conveyor Lift Mk.5": ItemData(G.Building | G.ConveyorMk5, 1338652, C.useful),
        "Building: Cable Beam Pack": ItemData(G.Beams, 1338653, C.filler, 0),
        "Building: Stackable Conveyor Pole": ItemData(G.Building | G.ConveyorSupports, 1338654, C.useful),
        "Building: Conveyor Wall Mount": ItemData(G.Building | G.ConveyorSupports, 1338655, C.useful, 0),
        "Building: Conveyor Lift Floor Hole": ItemData(G.Building | G.ConveyorSupports, 1338656, C.useful, 0),
        "Building: Conveyor Ceiling Mount": ItemData(G.Building | G.ConveyorSupports, 1338657, C.useful, 0),
        "Building: Pipes Mk.1": ItemData(G.Building | G.PipesMk1, 1338658, C.progression),
        "Building: Pipes Mk.2": ItemData(G.Building | G.PipesMk2, 1338659, C.progression),
        "Building: Pipeline Pump Mk.1": ItemData(G.Building | G.PipesMk1, 1338660, C.progression),
        "Building: Pipeline Pump Mk.2": ItemData(G.Building | G.PipesMk2, 1338661, C.progression),
        "Building: Pipeline Junction Cross": ItemData(G.Building | G.PipesMk1 | G.PipesMk2, 1338662, C.progression),
        "Building: Valve": ItemData(G.Building | G.PipesMk1 | G.PipesMk2, 1338663, C.useful),
        "Building: Stackable Pipeline Support": ItemData(G.Building | G.PipelineSupports, 1338664, C.useful, 0),
        "Building: Wall Pipeline Support": ItemData(G.Building | G.PipelineSupports, 1338665, C.useful, 0),
        "Building: Pipeline Wall Hole": ItemData(G.Building | G.PipelineSupports, 1338666, C.useful, 0),
        "Building: Pipeline Floor Hole": ItemData(G.Building | G.PipelineSupports, 1338667, C.useful, 0),
        "Building: Lights Control Panel": ItemData(G.Building | G.Lights, 1338668, C.filler, 0),
        "Building: Wall Mounted Flood Light": ItemData(G.Building | G.Lights, 1338669, C.filler, 0),
        "Building: Street Light": ItemData(G.Building | G.Lights, 1338670, C.filler, 0),
        "Building: Flood Light Tower": ItemData(G.Building | G.Lights, 1338671, C.filler, 0),
        "Building: Ceiling Light": ItemData(G.Building | G.Lights, 1338672, C.filler, 0),
        "Building: Power Tower": ItemData(G.Building | G.NeverExclude, 1338673, C.useful),
        "Building: Walls Orange": ItemData(G.Building | G.Walls, 1338674, C.progression),
        "Building: Radar Tower": ItemData(G.Building, 1338675, C.useful),
        "Building: Smart Splitter": ItemData(G.Building | G.NeverExclude, 1338676, C.useful),
        "Building: Programmable Splitter": ItemData(G.Building | G.NeverExclude, 1338677, C.useful),
        "Building: Label Sign Bundle": ItemData(G.Building | G.Signs, 1338678, C.filler, 0),
        "Building: Display Sign Bundle": ItemData(G.Building | G.Signs, 1338679, C.filler, 0),
        "Building: Billboard Set": ItemData(G.Building | G.Signs, 1338680, C.filler, 0),
        # 1338681 Moved to cosmetics - 1.1
        "Building: Metal Pillar": ItemData(G.Pilars, 1338682, C.filler, 0),
        "Building: Concrete Pillar": ItemData(G.Pilars, 1338683, C.filler, 0),
        "Building: Frame Pillar": ItemData(G.Pilars, 1338684, C.filler, 0),
        # 1338685 - 1338691 Moved to cosmetics - 1.1
        "Building: Foundation": ItemData(G.Building | G.Foundations | G.NeverExclude, 1338692, C.progression),
        "Building: Half Foundation": ItemData(G.Foundations, 1338693, C.filler, 0),
        "Building: Corner Ramp Pack": ItemData(G.Foundations, 1338694, C.filler, 0),
        "Building: Inverted Ramp Pack": ItemData(G.Foundations, 1338695, C.filler, 0),
        "Building: Inverted Corner Ramp Pack": ItemData(G.Foundations, 1338696, C.filler, 0),
        "Building: Quarter Pipes Pack": ItemData(G.Foundations, 1338697, C.filler, 0),
        "Building: Quarter Pipe Extensions Pack": ItemData(G.Foundations, 1338698, C.filler, 0),
        "Building: Frame Foundation": ItemData(G.Foundations, 1338699, C.filler, 0),
        "Building: Wall Outlet Mk.1": ItemData(G.Building, 1338700, C.useful),
        "Building: Wall Outlet Mk.2": ItemData(G.Building, 1338701, C.useful),
        "Building: Wall Outlet Mk.3": ItemData(G.Building, 1338702, C.useful),
        "Building: Modern Catwalks": ItemData(G.Building, 1338703, C.filler, 0),
        "Building: Industrial Walkways": ItemData(G.Building, 1338704, C.filler, 0),
        "Building: Stairs": ItemData(G.Building, 1338705, C.filler, 0),
        "Building: Clean Pipeline Mk.1": ItemData(G.Building, 1338706, C.filler, 0),
        "Building: Clean Pipeline Mk.2": ItemData(G.Building, 1338707, C.filler, 0),
        "Building: Road Barrier": ItemData(G.Building, 1338708, C.filler, 0),
        "Building: Modern Railing": ItemData(G.Building, 1338709, C.filler, 0),
        "Building: Industrial Railing": ItemData(G.Building, 1338710, C.filler, 0),
        "Building: Double Ramp Pack": ItemData(G.Foundations, 1338711, C.filler, 0),
        "Building: Conveyor Walls": ItemData(G.Walls, 1338712, C.filler, 0),
        "Building: Inverted Ramp Wall Bundle": ItemData(G.Walls, 1338713, C.filler, 0),
        "Building: Ramp Wall Bundle": ItemData(G.Walls, 1338714, C.filler, 0),
        "Building: Door Walls": ItemData(G.Walls, 1338715, C.filler, 0),
        "Building: Tilted Walls": ItemData(G.Walls, 1338716, C.filler, 0),
        "Building: Windowed Walls": ItemData(G.Walls, 1338717, C.filler, 0),
        "Building: Steel-framed Windows": ItemData(G.Walls, 1338718, C.filler, 0),
        "Building: Gates": ItemData(G.Walls, 1338719, C.filler, 0),
        "Building: Roofs": ItemData(G.Walls, 1338720, C.filler, 0),
        "Building: Roof Corners": ItemData(G.Walls, 1338721, C.filler, 0),
        "Building: Converter": ItemData(G.Building, 1338722, C.progression),
        "Building: Quantum Encoder": ItemData(G.Building, 1338723, C.progression),
        "Building: Portal": ItemData(G.Building, 1338724, C.useful),
        "Building: Conveyor Mk.6": ItemData(G.Building | G.ConveyorMk6, 1338725, C.progression),
        "Building: Conveyor Lift Mk.6": ItemData(G.Building | G.ConveyorMk6, 1338726, C.useful),
        "Building: Alien Power Augmenter": ItemData(G.Building, 1338727, C.progression),
        "Building: Dimensional Depot Uploader": ItemData(G.Building, 1338728, C.useful),
# Added in 1.1
        "Building: Priority Merger": ItemData(G.Building | G.NeverExclude, 1338729, C.useful),
        "Building: Conveyor Wall Hole": ItemData(G.Building, 1338730, C.useful, 0),
        "Building: Conveyor Throughput Monitor": ItemData(G.Building, 1338731, C.useful, 0),
        "Building: Basic Shelf Unit": ItemData(G.Building, 1338732, C.useful, 0),
        "Building: Beam Expansion Pack": ItemData(G.Beams, 1338733, C.filler, 0),
        "Building: Ventilation Bundle": ItemData(G.Building, 1338734, C.filler, 0),

### Ficsmas
        "Building: FICSMAS Candy Cane": ItemData(G.Building | G.Ficsmas, 1338735, count=0),
        "Building: FICSMAS Decoration": ItemData(G.Building | G.Ficsmas, 1338736, count=0),
        "Building: FICSMAS Gift Tree": ItemData(G.Building | G.Ficsmas, 1338737, count=0),
        "Building: FICSMAS Power Light": ItemData(G.Building | G.Ficsmas, 1338738, count=0),
        "Building: FICSMAS Snow Cannon": ItemData(G.Building | G.Ficsmas, 1338739, count=0),
        "Building: FICSMAS Snow Dispenser": ItemData(G.Building | G.Ficsmas, 1338740, count=0),
        "Building: FICSMAS Snowman": ItemData(G.Building | G.Ficsmas, 1338741, count=0),
        "Building: Giant FICSMAS Tree": ItemData(G.Building | G.Ficsmas, 1338742, count=0),
###
###
        # 1338735 - 1338749 Reserved for buildings
        "Customizer: Asphalt Foundation Material": ItemData(G.Customizer | G.Foundations, 1338750, C.filler, 0),
        "Customizer: Concrete Foundation Material": ItemData(G.Customizer | G.Foundations, 1338751, C.filler, 0),
        "Customizer: Concrete Wall Material": ItemData(G.Customizer | G.Walls, 1338752, C.filler, 0),
        "Customizer: Glass Roof Material": ItemData(G.Customizer | G.Walls, 1338753, C.filler, 0),
        "Customizer: Grip Metal Foundation Material": ItemData(G.Customizer | G.Foundations, 1338754, C.filler, 0),
        "Customizer: Coated Concrete Foundation Material": ItemData(G.Customizer | G.Foundations, 1338755, C.filler, 0),
        "Customizer: Metal Roof Material": ItemData(G.Customizer | G.Walls, 1338756, C.filler, 0),
        "Customizer: Steel Wall Material": ItemData(G.Customizer | G.Walls, 1338757, C.filler, 0),
        "Customizer: Tar Roof Material": ItemData(G.Customizer | G.Walls, 1338758, C.filler, 0),
        "Customizer: Arrow Patterns": ItemData(G.Customizer | G.Foundations, 1338759, C.filler, 0),
        "Customizer: Dotted Line Patterns": ItemData(G.Customizer | G.Foundations, 1338760, C.filler, 0),
        "Customizer: Solid Line Patterns": ItemData(G.Customizer | G.Foundations, 1338761, C.filler, 0),
        "Customizer: Factory Icon Patterns": ItemData(G.Customizer | G.Foundations, 1338762, C.filler, 0),
        "Customizer: Transportation Icon Patterns": ItemData(G.Customizer | G.Foundations, 1338763, C.filler, 0),
        "Customizer: Number Patterns": ItemData(G.Customizer | G.Foundations, 1338764, C.filler, 0),
        "Customizer: Pathway Patterns": ItemData(G.Customizer | G.Foundations, 1338765, C.filler, 0),
        "Customizer: Factory Zone Patterns": ItemData(G.Customizer | G.Foundations, 1338766, C.filler, 0),
        "Customizer: Steel-Framed Windows": ItemData(G.Customizer | G.Walls, 1338767, C.filler, 0), 
        "Customizer: Construction Fences": ItemData(G.Customizer, 1338768, C.filler, 0), 
        "Customizer: Unpainted Finish": ItemData(G.Customizer, 1338769, C.filler, 0), 
        "Customizer: Copper Paint Finish": ItemData(G.Customizer, 1338770, C.filler, 0), 
        "Customizer: Chrome Paint Finish": ItemData(G.Customizer, 1338771, C.filler, 0), 
        "Customizer: Carbon Steel Finish": ItemData(G.Customizer, 1338772, C.filler, 0), 
        "Customizer: Caterium Paint Finish": ItemData(G.Customizer, 1338773, C.filler, 0), 
        ### ficsmas
        "Customizer: Basic FICSMAS Skins": ItemData(G.Customizer | G.Ficsmas, 1338774, C.filler, 0), 
        "Customizer: Premium FICSMAS Skins": ItemData(G.Customizer | G.Ficsmas, 1338775, C.filler, 0), 
        ###


        # 1338776 - 1338799 Reserved for Cosmetics

        # Transports 1338800 - 1338819
        # Drones (including Drone)
        "Transport: Drones": ItemData(G.Transport, 1338800, C.useful),
        # Trains (including Empty Platform, rails, station, locomotive, train stop)  # 1.1
        "Transport: Trains": ItemData(G.Transport | G.Trains, 1338801, C.useful),
        "Transport: Fluid Trains": ItemData(G.Transport | G.Trains, 1338802, C.useful),
        # Tracker / Truck (including truck station)
        "Transport: Tractor": ItemData(G.Transport | G.Vehicles, 1338803, C.useful),
        "Transport: Truck": ItemData(G.Transport | G.Vehicles, 1338804, C.useful),
        "Transport: Explorer": ItemData(G.Transport | G.Vehicles, 1338805, C.useful),
        "Transport: Factory Cart": ItemData(G.Transport | G.Vehicles, 1338806, C.useful),
        "Transport: Factory Cart (golden)": ItemData(G.Transport | G.Vehicles, 1338807, C.filler),
        "Transport: Cyber Wagon": ItemData(G.Transport | G.Vehicles | G.Trap, 1338808, C.filler),
        # Hypertubes (including supports / pipes / entrance / holes)
        "Transport: Hypertube": ItemData(G.Transport | G.HyperTubes, 1338809, C.useful),
        "Transport: Hypertube Floor Hole": ItemData(G.Transport | G.HyperTubes, 1338810, C.filler),
        "Transport: Hypertube Wall Support": ItemData(G.Transport | G.HyperTubes, 1338811, C.filler),
        "Transport: Hypertube Wall Hole": ItemData(G.Transport | G.HyperTubes, 1338812, C.filler),
        # Personal Elevator (including additional floors)
        "Transport: Personal Elevator": ItemData(G.Transport, 1338813, C.useful),  # 1.1
        
        # 1338820 - 1338899 more parts / equipment / ammo
        "Bundle: FICSMAS Tree Branch": ItemData(G.Parts | G.Ficsmas, 1338820),
        "Bundle: Blue FICSMAS Ornament": ItemData(G.Parts | G.Ficsmas, 1338821),
        "Bundle: Red FICSMAS Ornament": ItemData(G.Parts | G.Ficsmas, 1338822),
        "Bundle: Iron FICSMAS Ornament": ItemData(G.Parts | G.Ficsmas, 1338823),
        "Bundle: Copper FICSMAS Ornament": ItemData(G.Parts | G.Ficsmas, 1338824),
        "Bundle: Candy Cane": ItemData(G.Parts | G.Ficsmas, 1338825),
        "Bundle: FICSMAS Actual Snow": ItemData(G.Parts | G.Ficsmas, 1338826),
        "Bundle: FICSMAS Bow": ItemData(G.Parts | G.Ficsmas, 1338827),
        "Bundle: FICSMAS Ornament Bundle": ItemData(G.Parts | G.Ficsmas, 1338828),
        "Bundle: FICSMAS Wreath": ItemData(G.Parts | G.Ficsmas, 1338829),
        "Bundle: FICSMAS Wonder Star": ItemData(G.Parts | G.Ficsmas, 1338830),
        "Bundle: Candy Cane Basher": ItemData(G.Equipment | G.Ficsmas, 1338831, count=0),
        "Bundle: Fancy Fireworks": ItemData(G.Ammo | G.Ficsmas, 1338832, count=0),
        "Bundle: Sparkly Fireworks": ItemData(G.Ammo | G.Ficsmas, 133883, count=0),
        "Bundle: Sweet Fireworks": ItemData(G.Ammo | G.Ficsmas, 1338834, count=0),

        # 1338900 - 1338998 Handled by trap system (includes a few non-trap things)
        # Regenerate via /Script/Blutility.EditorUtilityWidgetBlueprint'/Archipelago/Debug/EU_GenerateTrapIds.EU_GenerateTrapIds'
        "Trap: Hog": ItemData(G.Trap, 1338900, C.trap),
        "Trap: Alpha Hog": ItemData(G.Trap, 1338901, C.trap),
        "Trap: Johnny": ItemData(G.Trap, 1338902, C.trap),
        "Trap: Cliff Hog": ItemData(G.Trap, 1338903, C.trap),
        "Trap: Nuclear Hog": ItemData(G.Trap, 1338904, C.trap),
        "Trap: Not the Bees": ItemData(G.Trap, 1338905, C.trap),
        "Trap: Hatcher": ItemData(G.Trap, 1338906, C.trap),
        "Trap: Doggo with Pulse Nobelisk": ItemData(G.Trap, 1338907, C.trap),
        "Trap: Doggo with Nuke Nobelisk": ItemData(G.Trap, 1338908, C.trap),
        "Doggo with Power Slug": ItemData(G.Parts, 1338909, C.filler),
        "Trap: Doggo with Gas Nobelisk": ItemData(G.Trap, 1338910, C.trap),
        "Trap: Spore Flower": ItemData(G.Trap, 1338911, C.trap),
        "Trap: Stinger": ItemData(G.Trap, 1338912, C.trap),
        "Trap: Gas Stinger": ItemData(G.Trap, 1338913, C.trap),
        "Trap: Small Stinger": ItemData(G.Trap, 1338914, C.trap),
        "Trap: Spitter": ItemData(G.Trap, 1338915, C.trap),
        "Trap: Alpha Spitter": ItemData(G.Trap, 1338916, C.trap),
        "Trap: Nuclear Waste Drop": ItemData(G.Trap, 1338917, C.trap),
        "Trap: Plutonium Waste Drop": ItemData(G.Trap, 1338918, C.trap),
        "Trap: Elite Hatcher": ItemData(G.Trap, 1338919, C.trap),
        "Trap: Can of Beans": ItemData(G.Trap, 1338920, C.trap),
        "Trap: Fart Cloud": ItemData(G.Trap, 1338921, C.trap),

        "Building: Space Elevator": ItemData(G.Building, 1338999, C.progression),

        # Resource singles
        "Single: Adaptive Control Unit": ItemData(G.Parts, 1339000, count=0),
        "Single: AI Limiter": ItemData(G.Parts, 1339001, count=0),
        "Single: Alclad Aluminum Sheet": ItemData(G.Parts, 1339002, count=0),
        "Single: Blue Power Slug": ItemData(G.Parts, 1339003, count=0),
        "Single: Yellow Power Slug": ItemData(G.Parts, 1339004, count=0),
        "Single: Alien Protein": ItemData(G.Parts, 1339005, count=0),
        "Single: Purple Power Slug": ItemData(G.Parts, 1339006, count=0),
        "Single: Aluminum Casing": ItemData(G.Parts, 1339007, count=0),
        "Single: Aluminum Ingot": ItemData(G.Parts, 1339008, count=0),
        "Single: Aluminum Scrap": ItemData(G.Parts, 1339009, count=0),
        "Single: Assembly Director System": ItemData(G.Parts, 1339010, count=0),
        "Single: Automated Wiring": ItemData(G.Parts, 1339011, count=0),
        "Single: Battery": ItemData(G.Parts, 1339012, count=0),
        "Single: Bauxite": ItemData(G.Parts, 1339013, count=0),
        "Single: Neural-Quantum Processor": ItemData(G.Parts, 1339014, count=0),
        "Single: Biomass": ItemData(G.Parts, 1339015, count=0),
        "Single: Black Powder": ItemData(G.Parts, 1339016, count=0),
        "Single: Cable": ItemData(G.Parts, 1339017, count=0),
        "Single: Caterium Ingot": ItemData(G.Parts, 1339018, count=0),
        "Single: Caterium Ore": ItemData(G.Parts, 1339019, count=0),
        "Single: Circuit Board": ItemData(G.Parts, 1339020, count=0),
        "Single: Coal": ItemData(G.Parts, 1339021, count=0),
        "Single: Singularity Cell": ItemData(G.Parts, 1339022, count=0),
        "Single: Compacted Coal": ItemData(G.Parts, 1339023, count=0),
        "Single: Computer": ItemData(G.Parts, 1339024, count=0),
        "Single: Concrete": ItemData(G.Parts, 1339025, count=0),
        "Single: Cooling System": ItemData(G.Parts, 1339026, count=0),
        "Single: Copper Ingot": ItemData(G.Parts, 1339027, count=0),
        "Single: Copper Ore": ItemData(G.Parts, 1339028, count=0),
        "Single: Copper Powder": ItemData(G.Parts, 1339029, count=0),
        "Single: Copper Sheet": ItemData(G.Parts, 1339030, count=0),
        "Single: Adequate Pioneering Statue": ItemData(G.Parts, 1339031, count=0),
        "Single: Crystal Oscillator": ItemData(G.Parts, 1339032, count=0),
        "Single: Electromagnetic Control Rod": ItemData(G.Parts, 1339033, count=0),
        "Single: Empty Canister": ItemData(G.Parts, 1339034, count=0),
        "Single: Empty Fluid Tank": ItemData(G.Parts, 1339035, count=0),
        "Single: Encased Industrial Beam": ItemData(G.Parts, 1339036, count=0),
        "Single: Encased Plutonium Cell": ItemData(G.Trap, 1339037, C.trap, count=0),
        "Single: Encased Uranium Cell": ItemData(G.Trap, 1339038, C.trap, count=0),
        "Single: Fabric": ItemData(G.Parts, 1339039, count=0),
        "Single: FICSIT Coupon": ItemData(G.Parts, 1339040, count=0),
        "Single: AI Expansion Server": ItemData(G.Parts, 1339041, count=0),
        "Single: Fused Modular Frame": ItemData(G.Parts, 1339042, count=0),
        "Single: Hard Drive": ItemData(G.Parts, 1339043, count=0),
        "Single: Heat Sink": ItemData(G.Parts, 1339044, count=0),
        "Single: Heavy Modular Frame": ItemData(G.Parts, 1339045, count=0),
        "Single: High-Speed Connector": ItemData(G.Parts, 1339046, count=0),
        "Single: Satisfactory Pioneering Statue": ItemData(G.Parts, 1339047, count=0),
        "Single: Pretty Good Pioneering Statue": ItemData(G.Parts, 1339048, count=0),
        "Single: Iron Ingot": ItemData(G.Parts, 1339049, count=0),
        "Single: Iron Ore": ItemData(G.Parts, 1339050, count=0),
        "Single: Iron Plate": ItemData(G.Parts, 1339051, count=0),
        "Single: Iron Rod": ItemData(G.Parts, 1339052, count=0),
        "Single: Golden Nut Statue": ItemData(G.Parts, 1339053, count=0),
        "Single: Leaves": ItemData(G.Parts, 1339054, count=0),
        "Single: Limestone": ItemData(G.Parts, 1339055, count=0),
        "Single: Magnetic Field Generator": ItemData(G.Parts, 1339056, count=0),
        "Single: Mercer Sphere": ItemData(G.Parts, 1339057, count=0),
        "Single: Modular Engine": ItemData(G.Parts, 1339058, count=0),
        "Single: Modular Frame": ItemData(G.Parts, 1339059, count=0),
        "Single: Motor": ItemData(G.Parts, 1339060, count=0),
        "Single: Mycelia": ItemData(G.Parts, 1339061, count=0),
        "Single: Non-fissile Uranium": ItemData(G.Trap, 1339062, C.trap, count=0),
        "Single: Nuclear Pasta": ItemData(G.Parts, 1339063, count=0),
        "Single: Lizard Doggo Statue": ItemData(G.Parts, 1339064, count=0),
        "Single: Organic Data Capsule": ItemData(G.Parts, 1339065, count=0),
        "Single: Packaged Alumina Solution": ItemData(G.Parts, 1339066, count=0),
        "Single: Packaged Fuel": ItemData(G.Parts, 1339067, count=0),
        "Single: Packaged Heavy Oil Residue": ItemData(G.Parts, 1339068, count=0),
        "Single: Packaged Liquid Biofuel": ItemData(G.Parts, 1339069, count=0),
        "Single: Packaged Nitric Acid": ItemData(G.Parts, 1339070, count=0),
        "Single: Packaged Nitrogen Gas": ItemData(G.Parts, 1339071, count=0),
        "Single: Packaged Oil": ItemData(G.Parts, 1339072, count=0),
        "Single: Packaged Sulfuric Acid": ItemData(G.Parts, 1339073, count=0),
        "Single: Packaged Turbofuel": ItemData(G.Parts, 1339074, count=0),
        "Single: Packaged Water": ItemData(G.Parts, 1339075, count=0),
        "Single: Petroleum Coke": ItemData(G.Parts, 1339076, count=0),
        "Single: Plastic": ItemData(G.Parts, 1339077, count=0),
        "Single: Plutonium Fuel Rod": ItemData(G.Trap, 1339078, C.trap, count=0),
        "Single: Plutonium Pellet": ItemData(G.Trap, 1339079, C.trap, count=0),
        "Single: Plutonium Waste": ItemData(G.Trap, 1339080, C.trap, count=0),
        "Single: Polymer Resin": ItemData(G.Parts, 1339081, count=0),
        "Single: Power Shard": ItemData(G.Parts, 1339082, count=0),
        "Single: Confusing Creature Statue": ItemData(G.Parts, 1339083, count=0),
        "Single: Pressure Conversion Cube": ItemData(G.Parts, 1339084, count=0),
        "Single: Alien Power Matrix": ItemData(G.Parts, 1339085, count=0),
        "Single: Quartz Crystal": ItemData(G.Parts, 1339086, count=0),
        "Single: Quickwire": ItemData(G.Parts, 1339087, count=0),
        "Single: Radio Control Unit": ItemData(G.Parts, 1339088, count=0),
        "Single: Raw Quartz": ItemData(G.Parts, 1339089, count=0),
        "Single: Reinforced Iron Plate": ItemData(G.Parts, 1339090, count=0),
        "Single: Rotor": ItemData(G.Parts, 1339091, count=0),
        "Single: Rubber": ItemData(G.Parts, 1339092, count=0),
        "Single: SAM": ItemData(G.Parts, 1339093, count=0),
        "Single: Screw": ItemData(G.Parts, 1339094, count=0),
        "Single: Silica": ItemData(G.Parts, 1339095, count=0),
        "Single: Smart Plating": ItemData(G.Parts, 1339096, count=0),
        "Single: Smokeless Powder": ItemData(G.Parts, 1339097, count=0),
        "Single: Solid Biofuel": ItemData(G.Parts, 1339098, count=0),
        "Single: Somersloop": ItemData(G.Parts, 1339099, count=0),
        "Single: Stator": ItemData(G.Parts, 1339100, count=0),
        "Single: Silver Hog Statue": ItemData(G.Parts, 1339101, count=0),
        "Single: Steel Beam": ItemData(G.Parts, 1339102, count=0),
        "Single: Steel Ingot": ItemData(G.Parts, 1339103, count=0),
        "Single: Steel Pipe": ItemData(G.Parts, 1339104, count=0),
        "Single: Sulfur": ItemData(G.Parts, 1339105, count=0),
        "Single: Supercomputer": ItemData(G.Parts, 1339106, count=0),
        "Single: Superposition Oscillator": ItemData(G.Parts, 1339107, count=0),
        "Single: Thermal Propulsion Rocket": ItemData(G.Parts, 1339108, count=0),
        "Single: Turbo Motor": ItemData(G.Parts, 1339109, count=0),
        "Single: Hog Remains": ItemData(G.Parts, 1339110, count=0),
        "Single: Uranium": ItemData(G.Trap, 1339111, C.trap, count=0),
        "Single: Uranium Fuel Rod": ItemData(G.Trap, 1339112, C.trap, count=0),
        "Single: Uranium Waste": ItemData(G.Trap, 1339113, C.trap, count=0),
        "Single: Versatile Framework": ItemData(G.Parts, 1339114, count=0),
        "Single: Wire": ItemData(G.Parts, 1339115, count=0),
        "Single: Wood": ItemData(G.Parts, 1339116, count=0),
        "Single: Plasma Spitter Remains": ItemData(G.Parts, 1339117, count=0),
        "Single: Stinger Remains": ItemData(G.Parts, 1339118, count=0),
        "Single: Hatcher Remains": ItemData(G.Parts, 1339119, count=0),
        "Single: Alien DNA Capsule": ItemData(G.Parts, 1339120, count=0),
        "Single: Diamonds": ItemData(G.Parts, 1339121, count=0),
        "Single: Time Crystal": ItemData(G.Parts, 1339122, count=0),
        "Single: Ficsite Ingot": ItemData(G.Parts, 1339123, count=0),
        "Single: Ficsite Trigon": ItemData(G.Parts, 1339124, count=0),
        "Single: Reanimated SAM": ItemData(G.Parts, 1339125, count=0),
        "Single: SAM Fluctuator": ItemData(G.Parts, 1339126, count=0),
        "Single: Biochemical Sculptor": ItemData(G.Parts, 1339127, count=0),
        "Single: Ballistic Warp Drive": ItemData(G.Parts, 1339128, count=0),
        "Single: Ficsonium": ItemData(G.Trap, 1339129, C.trap, count=0),
        "Single: Ficsonium Fuel Rod": ItemData(G.Trap, 1339130, C.trap, count=0),
        "Single: Packaged Rocket Fuel": ItemData(G.Parts, 1339131, count=0),
        "Single: Packaged Ionized Fuel": ItemData(G.Parts, 1339132, count=0),
        "Single: Dark Matter Crystal": ItemData(G.Parts, 1339133, count=0),
        # 1339134 - 1339149 Reserved for future parts
        # 1339150 - 1339199 Equipment / Ammo
        "Single: Bacon Agaric": ItemData(G.Ammo, 1339150, count=0),
        "Single: Beryl Nut": ItemData(G.Ammo, 1339151, count=0),
        "Single: Blade Runners": ItemData(G.Equipment, 1339152),
        "Single: Boom Box": ItemData(G.Equipment, 1339153),
        "Single: Chainsaw": ItemData(G.Equipment, 1339154, C.useful),
        "Single: Cluster Nobelisk": ItemData(G.Ammo, 1339155, count=0),
        "Single: Iodine-Infused Filter": ItemData(G.Equipment, 1339156, count=0),  # 1.1
        "Single: Cup": ItemData(G.Equipment, 1339157),
        "Single: Cup (gold)": ItemData(G.Equipment, 1339158, count=0),
        "Single: Explosive Rebar": ItemData(G.Ammo, 1339159, count=0),
        "Single: Factory Cart": ItemData(G.Equipment, 1339160, C.useful),
        "Single: Factory Cart (golden)": ItemData(G.Equipment, 1339161, count=0),
        "Single: Gas Mask": ItemData(G.Equipment, 1339162, C.useful),
        "Single: Gas Nobelisk": ItemData(G.Ammo, 1339163, count=0),
        "Single: Hazmat Suit": ItemData(G.Equipment, 1339164, C.useful),
        "Single: Homing Rifle Ammo": ItemData(G.Ammo, 1339165, count=0),
        "Single: Hoverpack": ItemData(G.Equipment, 1339166, C.useful),
        "Single: Iron Rebar": ItemData(G.Ammo, 1339167, count=0),
        "Single: Jetpack": ItemData(G.Equipment, 1339168, C.useful),
        "Single: Medicinal Inhaler": ItemData(G.Ammo, 1339169, count=0),
        "Single: Nobelisk": ItemData(G.Ammo, 1339170, count=0),
        "Single: Nobelisk Detonator": ItemData(G.Equipment, 1339171, C.useful),
        "Single: Nuke Nobelisk": ItemData(G.Ammo, 1339172, count=0),
        "Single: Object Scanner": ItemData(G.Equipment, 1339173),
        "Single: Paleberry": ItemData(G.Ammo, 1339174, count=0),
        "Single: Parachute": ItemData(G.Equipment, 1339175, C.useful),
        "Single: Pulse Nobelisk": ItemData(G.Ammo, 1339176, count=0),
        "Single: Rebar Gun": ItemData(G.Equipment, 1339177, C.useful),
        "Single: Rifle": ItemData(G.Equipment, 1339178, C.useful),
        "Single: Rifle Ammo": ItemData(G.Ammo, 1339179, count=0),
        "Single: Shatter Rebar": ItemData(G.Ammo, 1339180, count=0),
        "Single: Stun Rebar": ItemData(G.Ammo, 1339181, count=0),
        "Single: Turbo Rifle Ammo": ItemData(G.Ammo, 1339182, count=0),
        "Single: Xeno-Basher": ItemData(G.Equipment, 1339183, C.useful),
        "Single: Xeno-Zapper": ItemData(G.Equipment, 1339184, C.useful),
        "Single: Zipline": ItemData(G.Equipment, 1339185, C.useful),
        "Single: Portable Miner": ItemData(G.Equipment, 1339186),
        "Single: Gas Filter": ItemData(G.Equipment, 1339187, count=0),

        # 1339820 - 1339899 more parts
        "Single: FICSMAS Tree Branch": ItemData(G.Parts | G.Ficsmas, 1339820),
        "Single: Blue FICSMAS Ornament": ItemData(G.Parts | G.Ficsmas, 1339821),
        "Single: Red FICSMAS Ornament": ItemData(G.Parts | G.Ficsmas, 1339822),
        "Single: Iron FICSMAS Ornament": ItemData(G.Parts | G.Ficsmas, 1339823),
        "Single: Copper FICSMAS Ornament": ItemData(G.Parts | G.Ficsmas, 1339824),
        "Single: Candy Cane": ItemData(G.Parts | G.Ficsmas, 1339825),
        "Single: FICSMAS Actual Snow": ItemData(G.Parts | G.Ficsmas, 1339826),
        "Single: FICSMAS Bow": ItemData(G.Parts | G.Ficsmas, 1339827),
        "Single: FICSMAS Ornament Bundle": ItemData(G.Parts | G.Ficsmas, 1339828),
        "Single: FICSMAS Wreath": ItemData(G.Parts | G.Ficsmas, 1339829),
        "Single: FICSMAS Wonder Star": ItemData(G.Parts | G.Ficsmas, 1339830),
        "Single: Candy Cane Basher": ItemData(G.Equipment | G.Ficsmas, 1339831, count=0),
        "Single: Fancy Fireworks": ItemData(G.Ammo | G.Ficsmas, 1339832, count=0),
        "Single: Sparkly Fireworks": ItemData(G.Ammo | G.Ficsmas, 1339833, count=0),
        "Single: Sweet Fireworks": ItemData(G.Ammo | G.Ficsmas, 1339834, count=0)
    }

    item_names_and_ids: ClassVar[dict[str, int]] = {name: data.code for name, data in item_data.items()}
    filler_items: ClassVar[tuple[str, ...]] = tuple(item for item, details in item_data.items() 
                                                    if details.count > 0 and details.category & (G.Parts | G.Ammo))

    @classmethod
    def get_item_names_per_category(cls, game_logic: GameLogic) -> dict[str, set[str]]:
        groups: dict[str, set[str]] = {}

        # To allow hinting for first part recipe in logic
        for part, recipes in game_logic.recipes.items():
            recipes_for_part: set[str] = {recipe.name for recipe in recipes if not recipe.implicitly_unlocked}
            if recipes_for_part:

                for original, indirect in game_logic.indirect_recipes.items():
                    if indirect in recipes_for_part:
                        recipes_for_part.remove(indirect)
                        recipes_for_part.add(original)

                groups[part] = recipes_for_part

        for name, data in cls.item_data.items():
            for category in data.category:
                if category != G.NeverExclude:
                    groups.setdefault(category.name, set()).add(name)
                
        return groups

    player: int
    logic: GameLogic
    random: Random
    critical_path: CriticalPathCalculator

    trap_chance: int 
    enabled_traps: tuple[str, ...]

    def __init__(self, player: Optional[int], logic: GameLogic, random: Random,
                 options: SatisfactoryOptions, critical_path: CriticalPathCalculator):
        self.player = player
        self.logic = logic
        self.random = random
        self.critical_path = critical_path
        self.options = options

        self.trap_chance = self.options.trap_chance.value
        self.enabled_traps = tuple(sorted(self.options.trap_selection_override.value))

    @classmethod
    def create_item_uninitialized(cls, name: str, player: int) -> Item:
        data: ItemData = cls.item_data[name]
        return Item(name, data.type, data.code, player)

    def create_item(self, name: str, player: int) -> Item:
        data: ItemData = self.item_data[name]
        item_type = data.type

        if item_type == C.progression \
            and (data.category & (G.Recipe | G.Building | G.Ficsmas)) and not (data.category & G.NeverExclude) \
                and self.critical_path.required_item_names and name not in self.critical_path.required_item_names:
            item_type = C.useful

        return Item(name, item_type, data.code, player)

    @classmethod
    def get_filler_item_name_uninitialized(cls, random: Random) -> str:
        return random.choice(cls.filler_items)

    def get_filler_item_name(self, random: Random, filler_items: Sequence[str] | None) -> str:
        if self.enabled_traps and random.random() < (self.trap_chance / 100):
            return random.choice(self.enabled_traps)
        else:
            if filler_items:
                return random.choice(filler_items)
            else:
                return Items.get_filler_item_name_uninitialized(random)

    def get_excluded_items(self, precollected_items: list[Item]) -> set[str]:
        excluded_items: set[str] = { 
            item.name 
            for item in precollected_items
            if item.name in self.item_data and item.name not in self.options.start_inventory_from_pool.value
        }

        excluded_items.update({"Building: " + building for building in self.critical_path.buildings_to_exclude})
        excluded_items.update({"Bundle: " + part for part in self.critical_path.parts_to_exclude})
        excluded_items.update({"Single: " + part for part in self.critical_path.parts_to_exclude})

        excluded_items.update({recipe for recipe in self.critical_path.recipes_to_exclude})
        excluded_items.update(self.critical_path.implicitly_unlocked)

        # since we dont have part logic setup for Transports
        if self.options.final_elevator_phase == 1:
            excluded_items.add("Transport: Drones")

        # Remove excluded items that arent unique
        excluded_items = excluded_items - {
            item_name
            for item_name, data in self.item_data.items()
            if data.category & (G.Parts | G.Equipment | G.Ammo | G.Trap | G.Upgrades)
        }

        if not "Erect a FICSMAS Tree" in self.options.goal_selection:
            excluded_items.update({
                item_name
                for item_name, data in self.item_data.items()
                if data.category & G.Ficsmas
            })

        return excluded_items

    def build_item_pool(self, random: Random, precollected_items: list[Item], number_of_locations: int) -> list[Item]:
        excluded_from_pool: set[str] = self.get_excluded_items(precollected_items)

        pool: list[Item] = [
            self.create_item(name, self.player)
            for name, data in self.item_data.items()
            for _ in range(data.count)
            if data.category & (G.Recipe | G.Building | G.Equipment | G.Ammo | G.Transport | G.Upgrades)
                and (data.type != C.filler or data.category & (G.Equipment | G.Ammo))
                and name not in excluded_from_pool
        ]

        free_space: int = number_of_locations - len(pool)
        if free_space < 0:
            raise Exception(f"Location pool starved, trying to add {len(pool)} items to {number_of_locations} locations")

        non_excluded_filler_items: list[str] = [item for item in self.filler_items if item not in excluded_from_pool]
        pool += [
            self.create_item(self.get_filler_item_name(random, non_excluded_filler_items), self.player)
            for _ in range(free_space)
        ]

        return pool
