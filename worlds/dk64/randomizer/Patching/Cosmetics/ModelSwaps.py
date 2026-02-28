"""All code associated with model swaps."""

import random
import js
from randomizer.Enums.Models import Model, Sprite
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Settings import KongModels, RandomModels
from randomizer.Settings import Settings, ColorOptions
from randomizer.Patching.Patcher import ROM
from randomizer.Patching.Library.Generic import applyCharacterSpawnerChanges, SpawnerChange, IsColorOptionSelected

turtle_models = [
    Model.Diddy,  # Diddy
    Model.DK,  # DK
    Model.Lanky,  # Lanky
    Model.Tiny,  # Tiny
    Model.Chunky,  # Regular Chunky
    Model.ChunkyDisco,  # Disco Chunky
    Model.Cranky,  # Cranky
    Model.Funky,  # Funky
    Model.Candy,  # Candy
    Model.Seal,  # Seal
    Model.Enguarde,  # Enguarde
    Model.BeaverBlue_LowPoly,  # Beaver
    Model.Squawks_28,  # Squawks
    Model.KlaptrapGreen,  # Klaptrap Green
    Model.KlaptrapPurple,  # Klaptrap Purple
    Model.KlaptrapRed,  # Klaptrap Red
    Model.KlaptrapTeeth,  # Klaptrap Teeth
    Model.SirDomino,  # Sir Domino
    Model.MrDice_41,  # Mr Dice
    Model.Beetle,  # Beetle
    Model.NintendoLogo,  # N64 Logo
    Model.MechanicalFish,  # Mech Fish
    Model.ToyCar,  # Toy Car
    Model.BananaFairy,  # Fairy
    Model.Shuri,  # Starfish
    Model.Gimpfish,  # Gimpfish
    Model.Spider,  # Spider
    Model.Rabbit,  # Rabbit
    Model.KRoolCutscene,  # K Rool
    Model.SkeletonHead,  # Skeleton Head
    Model.Vulture_76,  # Vulture
    Model.Vulture_77,  # Racing Vulture
    Model.Tomato,  # Tomato
    Model.Fly,  # Fly
    Model.SpotlightFish,  # Spotlight Fish
    Model.Puftup,  # Pufftup
    Model.CuckooBird,  # Cuckoo Bird
    Model.IceTomato,  # Ice Tomato
    Model.Boombox,  # Boombox
    Model.KRoolFight,  # K Rool (Boxing)
    Model.Microphone,  # Microbuffer
    Model.DeskKRool,  # K Rool's Desk
    Model.Bell,  # Bell
    Model.BonusBarrel,  # Bonus Barrel
    Model.HunkyChunkyBarrel,  # HC Barrel
    Model.MiniMonkeyBarrel,  # MM Barrel
    Model.TNTBarrel,  # TNT Barrel
    Model.Rocketbarrel,  # RB Barrel
    Model.StrongKongBarrel,  # SK Barrel
    Model.OrangstandSprintBarrel,  # OSS Barrel
    Model.BBBSlot_143,  # BBB Slot
    Model.PlayerCar,  # Tiny Car
    Model.Boulder,  # Boulder
    Model.Boat_158,  # Boat
    Model.Potion,  # Potion
    Model.ArmyDilloMissle,  # AD Missile
    Model.TagBarrel,  # Tag Barrel
    Model.QuestionMark,  # Question Mark
    Model.Krusha,  # Krusha
    Model.BananaPeel,  # Banana Peel
    Model.Butterfly,  # Butterfly
    Model.FunkyGun,  # Funky's Gun
]

panic_models = [
    Model.Diddy,  # Diddy
    Model.DK,  # DK
    Model.Lanky,  # Lanky
    Model.Tiny,  # Tiny
    Model.Chunky,  # Regular Chunky
    Model.ChunkyDisco,  # Disco Chunky
    Model.Cranky,  # Cranky
    Model.Funky,  # Funky
    Model.Candy,  # Candy
    Model.Seal,  # Seal
    Model.Enguarde,  # Enguarde
    Model.BeaverBlue_LowPoly,  # Beaver
    Model.Squawks_28,  # Squawks
    Model.KlaptrapGreen,  # Klaptrap Green
    Model.KlaptrapPurple,  # Klaptrap Purple
    Model.KlaptrapRed,  # Klaptrap Red
    Model.MadJack,  # Mad Jack
    Model.Troff,  # Troff
    Model.SirDomino,  # Sir Domino
    Model.MrDice_41,  # Mr Dice
    Model.RoboKremling,  # Robo Kremling
    Model.Scoff,  # Scoff
    Model.Beetle,  # Beetle
    Model.NintendoLogo,  # N64 Logo
    Model.MechanicalFish,  # Mech Fish
    Model.ToyCar,  # Toy Car
    Model.Klump,  # Klump
    Model.Dogadon,  # Dogadon
    Model.BananaFairy,  # Fairy
    Model.Guard,  # Guard
    Model.Shuri,  # Starfish
    Model.Gimpfish,  # Gimpfish
    Model.KLumsy,  # K Lumsy
    Model.Spider,  # Spider
    Model.Rabbit,  # Rabbit
    # Model.Beanstalk,  # Beanstalk
    Model.KRoolCutscene,  # K Rool
    Model.SkeletonHead,  # Skeleton Head
    Model.Vulture_76,  # Vulture
    Model.Vulture_77,  # Racing Vulture
    Model.Ghost,  # Ghost
    Model.Fly,  # Fly
    Model.FlySwatter_83,  # Fly Swatter
    Model.Owl,  # Owl
    Model.Book,  # Book
    Model.SpotlightFish,  # Spotlight Fish
    Model.Puftup,  # Pufftup
    Model.Mermaid,  # Mermaid
    Model.Mushroom,  # Mushroom Man
    Model.Worm,  # Worm
    Model.EscapeShip,  # Escape Ship
    Model.KRoolFight,  # K Rool (Boxing)
    Model.Microphone,  # Microbuffer
    Model.BonusBarrel,  # Bonus Barrel
    Model.HunkyChunkyBarrel,  # HC Barrel
    Model.MiniMonkeyBarrel,  # MM Barrel
    Model.TNTBarrel,  # TNT Barrel
    Model.Rocketbarrel,  # RB Barrel
    Model.StrongKongBarrel,  # SK Barrel
    Model.OrangstandSprintBarrel,  # OSS Barrel
    Model.PlayerCar,  # Tiny Car
    Model.Boulder,  # Boulder
    Model.VaseCircle,  # Vase
    Model.VaseColon,  # Vase
    Model.VaseTriangle,  # Vase
    Model.VasePlus,  # Vase
    Model.ArmyDilloMissle,  # AD Missile
    Model.TagBarrel,  # Tag Barrel
    Model.QuestionMark,  # Question Mark
    Model.Krusha,  # Krusha
    Model.Light,  # Light
    Model.BananaPeel,  # Banana Peel
    Model.FunkyGun,  # Funky's Gun
]

bother_models = [
    Model.BeaverBlue_LowPoly,  # Beaver
    Model.Klobber,  # Klobber
    Model.Kaboom,  # Kaboom
    Model.KlaptrapGreen,  # Green Klap
    Model.KlaptrapPurple,  # Purple Klap
    Model.KlaptrapRed,  # Red Klap
    Model.KlaptrapTeeth,  # Klap Teeth
    Model.Krash,  # Krash
    Model.Troff,  # Troff
    Model.NintendoLogo,  # N64 Logo
    Model.MechanicalFish,  # Mech Fish
    Model.Krossbones,  # Krossbones
    Model.Rabbit,  # Rabbit
    Model.SkeletonHead,  # Minecart Skeleton Head
    Model.Tomato,  # Tomato
    Model.IceTomato,  # Ice Tomato
    Model.GoldenBanana_104,  # Golden Banana
    Model.Microphone,  # Microbuffer
    Model.Bell,  # Bell
    Model.Missile,  # Missile (Car Race)
    Model.Buoy,  # Red Buoy
    Model.BuoyGreen,  # Green Buoy
    Model.RarewareLogo,  # Rareware Logo
]

piano_models = [
    Model.Krash,
    Model.RoboKremling,
    Model.KoshKremling,
    Model.KoshKremlingRed,
    Model.Kasplat,
    Model.Guard,
    Model.Krossbones,
    Model.Mermaid,
    Model.Mushroom,
    Model.GoldenBanana_104,
    Model.FlySwatter_83,
    Model.Ruler,
]
piano_extreme_model = [
    Model.SkeletonHead,
    Model.Owl,
    Model.Kosha,
    # Model.Beanstalk,
]

spotlight_fish_models = [
    # Model.Turtle,  # Lighting Bug
    Model.Seal,
    Model.BeaverBlue,
    Model.BeaverGold,
    Model.Zinger,
    Model.Squawks_28,
    Model.Klobber,
    Model.Kaboom,
    Model.KlaptrapGreen,
    Model.KlaptrapPurple,
    Model.KlaptrapRed,
    Model.Krash,
    # Model.SirDomino,  # Lighting issue
    # Model.MrDice_41,  # Lighting issue
    # Model.Ruler, # Lighting issue
    # Model.RoboKremling, # Lighting issue
    Model.NintendoLogo,
    Model.MechanicalFish,
    Model.ToyCar,
    Model.Kasplat,
    Model.BananaFairy,
    Model.Guard,
    Model.Gimpfish,
    # Model.Shuri,  # Lighting issue
    Model.Spider,
    Model.Rabbit,
    Model.KRoolCutscene,
    Model.KRoolFight,
    # Model.SkeletonHead, # Lighting bug
    # Model.Vulture_76, # Lighting bug
    # Model.Vulture_77, # Lighting bug
    # Model.Bat, # Lighting bug
    # Model.Tomato, # Lighting bug
    # Model.IceTomato, # Lighting bug
    # Model.FlySwatter_83, # Lighting bug
    Model.SpotlightFish,
    Model.Microphone,
    # Model.Rocketbarrel,  # Model too big, obstructs view
    # Model.StrongKongBarrel,  # Model too big, obstructs view
    # Model.OrangstandSprintBarrel,  # Model too big, obstructs view
    # Model.MiniMonkeyBarrel,  # Model too big, obstructs view
    # Model.HunkyChunkyBarrel,  # Model too big, obstructs view
]
candy_cutscene_models = [
    Model.Cranky,
    # Model.Funky, # Disappears with collision
    Model.Candy,
    Model.Snide,
    Model.Seal,
    Model.BeaverBlue,
    Model.BeaverGold,
    Model.Klobber,
    Model.Kaboom,
    Model.Krash,
    Model.Troff,
    Model.Scoff,
    Model.RoboKremling,
    Model.Beetle,
    Model.MrDice_41,
    Model.MrDice_56,
    Model.BananaFairy,
    Model.Rabbit,
    Model.KRoolCutscene,
    Model.KRoolFight,
    Model.Vulture_76,
    Model.Vulture_77,
    Model.Tomato,
    Model.IceTomato,
    Model.FlySwatter_83,
    Model.Microphone,
    Model.StrongKongBarrel,
    Model.Rocketbarrel,
    Model.OrangstandSprintBarrel,
    Model.MiniMonkeyBarrel,
    Model.HunkyChunkyBarrel,
    Model.RambiCrate,
    Model.EnguardeCrate,
    Model.Boulder,
    Model.SteelKeg,
    Model.GoldenBanana_104,
]

funky_cutscene_models = [
    Model.Cranky,
    Model.Candy,
    Model.Funky,
    Model.Troff,
    Model.Scoff,
    Model.Ruler,
    Model.RoboKremling,
    Model.KRoolCutscene,
    Model.KRoolFight,
    Model.Microphone,
]

# Not holding gun
funky_cutscene_models_extreme = [
    Model.BeaverBlue,
    Model.BeaverGold,
    Model.Klobber,
    Model.Kaboom,
    Model.SirDomino,
    Model.MechanicalFish,
    Model.BananaFairy,
    Model.SkeletonHand,
    Model.IceTomato,
    Model.Tomato,
]

boot_cutscene_models = [
    Model.Turtle,
    Model.Enguarde,
    Model.BeaverBlue,
    Model.BeaverGold,
    Model.Zinger,
    Model.Squawks_28,
    Model.KlaptrapGreen,
    Model.KlaptrapPurple,
    Model.KlaptrapRed,
    Model.BananaFairy,
    Model.Spider,
    Model.Bat,
    Model.KRoolGlove,
]

melon_random_sprites = [
    Sprite.BouncingMelon,
    Sprite.BouncingOrange,
    Sprite.Coconut,
    Sprite.Peanut,
    Sprite.Grape,
    Sprite.Feather,
    Sprite.Pineapple,
    Sprite.CrystalCoconut0,
    Sprite.DKCoin,
    Sprite.DiddyCoin,
    Sprite.LankyCoin,
    Sprite.TinyCoin,
    Sprite.ChunkyCoin,
    Sprite.Fairy,
    Sprite.RaceCoin,
]

model_mapping = {
    KongModels.default: 0,
    KongModels.disco_chunky: 6,
    KongModels.krusha: 7,
    KongModels.krool_cutscene: 9,
    KongModels.krool_fight: 8,
    KongModels.cranky: 10,
    KongModels.candy: 11,
    KongModels.funky: 12,
    KongModels.disco_donkey: 13,
}

model_texture_sections = {
    KongModels.krusha: {
        "skin": [0x4738, 0x2E96, 0x3A5E],
        "kong": [0x3126, 0x354E, 0x37FE, 0x41E6],
    },
    KongModels.krool_fight: {
        "skin": [
            0x61D6,
            0x63FE,
            0x6786,
            0x7DD6,
            0x7E8E,
            0x7F3E,
            0x7FEE,
            0x5626,
            0x56E6,
            0x5A86,
            0x5BAE,
            0x5D46,
            0x5E2E,
            0x5FAE,
            0x69BE,
            0x735E,
            0x7C5E,
            0x7E4E,
            0x7EF6,
            0x7FA6,
            0x8056,
        ],
        "kong": [0x607E, 0x7446, 0x7D46, 0x80FE],
    },
    # KongModels.krool_cutscene: {
    #     "skin": [0x4A6E, 0x4CBE, 0x52AE, 0x55BE, 0x567E, 0x57E6, 0x5946, 0x5AA6, 0x5E06, 0x5EC6, 0x6020, 0x618E, 0x62F6, 0x6946, 0x6A6E, 0x6C5E, 0x6D86, 0x6F76, 0x702E, 0x70DE, 0x718E, 0x72FE, 0x4FBE, 0x51FE, 0x5C26, 0x6476, 0x6826, 0x6B26, 0x6E3E, 0x6FE6, 0x7096, 0x7146, 0x71F6, 0x733E, 0x743E],
    #     "kong": [],
    # }
}

KLAPTRAPS = [Model.KlaptrapGreen, Model.KlaptrapPurple, Model.KlaptrapRed]


def getRandomKlaptrapModel() -> Model:
    """Get random klaptrap model."""
    return random.choice(KLAPTRAPS)


def applyCosmeticModelSwaps(settings: Settings, ROM_COPY: ROM):
    """Apply model swaps to the settings dict."""
    sav = settings.rom_data

    bother_model_index = Model.KlaptrapGreen
    panic_fairy_model_index = Model.BananaFairy
    panic_klap_model_index = Model.KlaptrapGreen
    turtle_model_index = Model.Turtle
    sseek_klap_model_index = Model.KlaptrapGreen
    fungi_tomato_model_index = Model.Tomato
    caves_tomato_model_index = Model.IceTomato
    racer_beetle = Model.Beetle
    racer_rabbit = Model.Rabbit
    piano_burper = Model.KoshKremlingRed
    spotlight_fish_model_index = Model.SpotlightFish
    candy_model_index = Model.Candy
    funky_model_index = Model.Funky
    boot_model_index = Model.Boot
    melon_sprite = Sprite.BouncingMelon
    swap_bitfield = 0

    model_inverse_mapping = {}
    for model in model_mapping:
        val = model_mapping[model]
        model_inverse_mapping[val] = model

    ROM_COPY.seek(settings.rom_data + 0x1B8)
    settings.kong_model_dk = model_inverse_mapping[int.from_bytes(ROM_COPY.readBytes(1), "big")]
    settings.kong_model_diddy = model_inverse_mapping[int.from_bytes(ROM_COPY.readBytes(1), "big")]
    settings.kong_model_lanky = model_inverse_mapping[int.from_bytes(ROM_COPY.readBytes(1), "big")]
    settings.kong_model_tiny = model_inverse_mapping[int.from_bytes(ROM_COPY.readBytes(1), "big")]
    settings.kong_model_chunky = model_inverse_mapping[int.from_bytes(ROM_COPY.readBytes(1), "big")]

    if settings.override_cosmetics:
        model_setting = RandomModels[js.document.getElementById("random_models").value]
    else:
        model_setting = settings.random_models
    if model_setting == RandomModels.random:
        bother_model_index = getRandomKlaptrapModel()
    elif model_setting == RandomModels.extreme:
        bother_model_index = getRandomKlaptrapModel()
        racer_beetle = random.choice([Model.Beetle, Model.Rabbit])
        racer_rabbit = random.choice([Model.Beetle, Model.Rabbit])
        if racer_rabbit == Model.Beetle:
            spawner_changes = []
            # Fungi
            rabbit_race_fungi_change = SpawnerChange(Maps.FungiForest, 2)
            rabbit_race_fungi_change.new_scale = 50
            rabbit_race_fungi_change.new_speed_0 = 95
            rabbit_race_fungi_change.new_speed_1 = 184
            spawner_changes.append(rabbit_race_fungi_change)
            # Caves
            rabbit_caves_change = SpawnerChange(Maps.CavesChunkyIgloo, 1)
            rabbit_caves_change.new_scale = 40
            spawner_changes.append(rabbit_caves_change)
            applyCharacterSpawnerChanges(ROM_COPY, spawner_changes)
    if model_setting != RandomModels.off:
        panic_fairy_model_index = random.choice(panic_models)
        turtle_model_index = random.choice(turtle_models)
        panic_klap_model_index = getRandomKlaptrapModel()
        sseek_klap_model_index = getRandomKlaptrapModel()
        fungi_tomato_model_index = random.choice([Model.Tomato, Model.IceTomato])
        caves_tomato_model_index = random.choice([Model.Tomato, Model.IceTomato])
        referenced_piano_models = piano_models.copy()
        referenced_funky_models = funky_cutscene_models.copy()
        if model_setting == RandomModels.extreme:
            referenced_piano_models.extend(piano_extreme_model)
            spotlight_fish_model_index = random.choice(spotlight_fish_models)
            referenced_funky_models.extend(funky_cutscene_models_extreme)
            boot_model_index = random.choice(boot_cutscene_models)
        piano_burper = random.choice(referenced_piano_models)
        candy_model_index = random.choice(candy_cutscene_models)
        funky_model_index = random.choice(funky_cutscene_models)
    settings.bother_klaptrap_model = bother_model_index
    settings.beetle_model = racer_beetle
    settings.rabbit_model = racer_rabbit
    settings.panic_fairy_model = panic_fairy_model_index
    settings.turtle_model = turtle_model_index
    settings.panic_klaptrap_model = panic_klap_model_index
    settings.seek_klaptrap_model = sseek_klap_model_index
    settings.fungi_tomato_model = fungi_tomato_model_index
    settings.caves_tomato_model = caves_tomato_model_index
    settings.piano_burp_model = piano_burper
    settings.spotlight_fish_model = spotlight_fish_model_index
    settings.candy_cutscene_model = candy_model_index
    settings.funky_cutscene_model = funky_model_index
    settings.boot_cutscene_model = boot_model_index
    settings.wrinkly_rgb = [255, 255, 255]
    # Compute swap bitfield
    swap_bitfield |= 0x10 if settings.rabbit_model == Model.Beetle else 0
    swap_bitfield |= 0x20 if settings.beetle_model == Model.Rabbit else 0
    swap_bitfield |= 0x40 if settings.fungi_tomato_model == Model.IceTomato else 0
    swap_bitfield |= 0x80 if settings.caves_tomato_model == Model.Tomato else 0
    if settings.override_cosmetics:
        if IsColorOptionSelected(settings, ColorOptions.items):
            melon_sprite = random.choice(melon_random_sprites)
        if IsColorOptionSelected(settings, ColorOptions.friendly_npcs):
            settings.wrinkly_rgb = [random.randint(0, 255) for _ in range(3)]
    settings.minigame_melon_sprite = melon_sprite
    # Write Models
    ROM_COPY.seek(sav + 0x1B5)
    ROM_COPY.writeMultipleBytes(settings.panic_fairy_model + 1, 1)  # Still needed for end seq fairy swap
    ROM_COPY.seek(sav + 0x1E2)
    ROM_COPY.write(swap_bitfield)
