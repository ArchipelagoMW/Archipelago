from typing import Dict, Any


def starting_inventory(world, item) -> bool:
    items = world.multiworld.precollected_items.values()
    if item in items:
        return True
    else:
        return False


def starting_ammo(world, item) -> int:
    items = world.multiworld.precollected_items.values()
    count = 0
    if item == "Missile Expansion":
        for i in items:
            if i == "Missile Expansion" or i == "Missile Launcher":
                count += 5
        return count
    if item == "Energy Tank":
        for i in items:
            if i == "Energy Tank":
                count += 1
    if item == "Power Bomb":
        for i in items:
            if i == "Power Bomb" or i == "Power Bomb Expansion":
                count += 1
    return count


def spring_check(spring) -> bool:
    if spring == 1:
        return True
    else:
        return False


def ridley(boss) -> bool:
    if boss == 0 or boss == 1:
        return False
    else:
        return True


def temple_dest(boss) -> str:
    if boss == 0 or boss == 2:
        return "Crater Entry Point"
    else:
        return "Credits"


def item_text(world, location) -> str:
    loc = world.multiworld.get_location(location, world.player)
    player_name = f"{world.multiworld.player_name[location.player]} " if loc.player != world.player else ""
    return f"{player_name}{loc.item.name}"


def item_model(world, location) -> str:
    loc = world.multiworld.get_location(location, world.player)
    if loc.native_item:
        nam = loc.item.name
        if nam == "Missile Expansion" or nam == "Main Missile":
            return "Missile"
        else:
            return nam
    else:
        return "Nothing"


def make_config(world):
    options = world.options
    config = {
        "$schema": "https://randovania.org/randomprime/randomprime.schema.json",
        "inputIso": "prime.iso",
        "outputIso": "prime_out.iso",
        "forceVanillaLayout": False,
        "preferences": {
            "forceFusion": False,
            "cacheDir": "cache",
            "qolGeneral": True,
            "qolGameBreaking": False,
            "qolCosmetic": True,
            "qolCutscenes": "Skippable",
            "qolPickupScans": True,
            "mapDefaultState": "Always",
            "artifactHintBehavior": "All",
        },
        "gameConfig": {
            "startingRoom": "Tallon Overworld:Landing Site",
            "springBall": spring_check(options.spring_ball.value),
            "warpToStart": True,
            "nonvariaHeatDamage": False,
            "staggeredSuitDamage": False,
            "heatDamagePerSec": 10.0,
            "poisonDamagePerSec": 0.11,
            "phazonDamagePerSec": 0.964,
            "phazonDamageModifier": "Default",
            "autoEnabledElevators": True,
            "skipRidley": ridley(options.final_bosses.value),
            "multiworldDolPatches": False,
            "startingItems": {
                "combatVisor":True,  # starting_inventory(world, "Combat Visor"),
                "powerBeam": True, # starting_inventory(world, "Power Beam"), disabling this for now since we don't have this worked into logic
                "scanVisor": True,  # starting_inventory(world, "Scan Visor"),
                "missiles": starting_ammo(world, "Missile Expansion"),
                "energyTanks": starting_ammo(world, "Energy Tank"),
                "powerBombs": starting_ammo(world, "Power Bomb"),
                "wave": starting_inventory(world, "Wave Beam"),
                "ice": starting_inventory(world, "Ice Beam"),
                "plasma": starting_inventory(world, "Plasma Beam"),
                "charge": starting_inventory(world, "Charge Beam"),
                "morphBall": starting_inventory(world, "Morph Ball"),
                "bombs": starting_inventory(world, "Morph Ball Bomb"),
                "spiderBall": starting_inventory(world, "Spider Ball"),
                "boostBall": starting_inventory(world, "Boost Ball"),
                "variaSuit": starting_inventory(world, "Varia Suit"),
                "gravitySuit": starting_inventory(world, "Gravity Suit"),
                "phazonSuit": starting_inventory(world, "Phazon Suit"),
                "thermalVisor": starting_inventory(world, "Thermal Visor"),
                "xray": starting_inventory(world, "X-Ray Visor"),
                "spaceJump": starting_inventory(world, "Space Jump Boots"),
                "grapple": starting_inventory(world, "Grapple Beam"),
                "superMissile": starting_inventory(world, "Super Missile"),
                "wavebuster": starting_inventory(world, "Wavebuster"),
                "iceSpreader": starting_inventory(world, "Ice Spreader"),
                "flamethrower": starting_inventory(world, "Flamethrower")
            },
            "disableItemLoss": True,
            "startingVisor": "Combat",
            "startingBeam": "Power",
            "enableIceTraps": False,
            "missileStationPbRefill": True,
            "doorOpenMode": "Original",
            "etankCapacity": 100,
            "itemMaxCapacity": {
                "Power Beam": 1,
                "Ice Beam": 1,
                "Wave Beam": 1,
                "Plasma Beam": 1,
                "Missile": 999,
                "Scan Visor": 1,
                "Morph Ball Bomb": 1,
                "Power Bomb": 99,
                "Flamethrower": 1,
                "Thermal Visor": 1,
                "Charge Beam": 1,
                "Super Missile": 1,
                "Grapple Beam": 1,
                "X-Ray Visor": 1,
                "Ice Spreader": 1,
                "Space Jump Boots": 1,
                "Morph Ball": 1,
                "Combat Visor": 1,
                "Boost Ball": 1,
                "Spider Ball": 1,
                "Power Suit": 1,
                "Gravity Suit": 1,
                "Varia Suit": 1,
                "Phazon Suit": 1,
                "Energy Tank": 99,
                "Unknown Item 1": 6000,
                "Health Refill": 999,
                "Unknown Item 2": 1,
                "Wavebuster": 1,
                "Artifact Of Truth": 1,
                "Artifact Of Strength": 1,
                "Artifact Of Elder": 1,
                "Artifact Of Wild": 1,
                "Artifact Of Lifegiver": 1,
                "Artifact Of Warrior": 1,
                "Artifact Of Chozo": 1,
                "Artifact Of Nature": 1,
                "Artifact Of Sun": 1,
                "Artifact Of World": 1,
                "Artifact Of Spirit": 1,
                "Artifact Of Newborn": 1
            },
            "phazonEliteWithoutDynamo": True,
            "mainPlazaDoor": True,
            "backwardsLabs": True,
            "backwardsFrigate": True,
            "backwardsUpperMines": True,
            "backwardsLowerMines": True,
            "patchPowerConduits": False,
            "removeMineSecurityStationLocks": False,
            "removeHiveMecha": False,
            "powerBombArboretumSandstone": False,
            "artifactHints": {
                "Artifact of Chozo": "TODO: Add hint here",
                "Artifact of Nature": "TODO: Add hint here",
                "Artifact of Sun": "TODO: Add hint here",
                "Artifact of World": "TODO: Add hint here",
                "Artifact of Spirit": "TODO: Add hint here",
                "Artifact of Newborn": "TODO: Add hint here",
                "Artifact of Truth": "TODO: Add hint here",
                "Artifact of Strength": "TODO: Add hint here",
                "Artifact of Elder": "TODO: Add hint here",
                "Artifact of Wild": "TODO: Add hint here",
                "Artifact of Lifegiver": "TODO: Add hint here",
                "Artifact of Warrior": "TODO: Add hint here"
            },
            "artifactTempleLayerOverrides": {
                "Artifact of Truth": starting_inventory(world, "Artifact of Truth"),
                "Artifact of Strength": starting_inventory(world, "Artifact of Strength"),
                "Artifact of Elder": starting_inventory(world, "Artifact of Elder"),
                "Artifact of Wild": starting_inventory(world, "Artifact of Wild"),
                "Artifact of Lifegiver": starting_inventory(world, "Artifact of Lifegiver"),
                "Artifact of Warrior": starting_inventory(world, "Artifact of Warrior"),
                "Artifact of Chozo": starting_inventory(world, "Artifact of Chozo"),
                "Artifact of Nature": starting_inventory(world, "Artifact of Nature"),
                "Artifact of Sun": starting_inventory(world, "Artifact of Sun"),
                "Artifact of World": starting_inventory(world, "Artifact of World"),
                "Artifact of Spirit": starting_inventory(world, "Artifact of Spirit"),
                "Artifact of Newborn": starting_inventory(world, "Artifact of Newborn")
            },
            "requiredArtifactCount": options.required_artifacts.value
        },
        "levelData": {
            "Frigate Orpheon": {
                  "transports": {
                      "Frigate Escape Cutscene": "Tallon Overworld:Landing Site"
                  },
                  "rooms": {
                        "Exterior Docking Hangar": {},
                        "Air Lock": {},
                        "Deck Alpha Access Hall": {},
                        "Deck Alpha Mech Shaft": {},
                        "Emergency Evacuation Area": {},
                        "Connection Elevator to Deck Alpha": {},
                        "Deck Alpha Umbilical Hall": {},
                        "Biotech Research Area 2": {},
                        "Map Facility": {},
                        "Main Ventilation Shaft Section F": {},
                        "Connection Elevator to Deck Beta": {},
                        "Main Ventilation Shaft Section E": {},
                        "Deck Beta Conduit Hall": {},
                        "Main Ventilation Shaft Section D": {},
                        "Biotech Research Area 1": {},
                        "Main Ventilation Shaft Section C": {},
                        "Deck Beta Security Hall": {},
                        "Connection Elevator to Deck Beta (2)": {},
                        "Subventilation Shaft Section A": {},
                        "Main Ventilation Shaft Section B": {},
                        "Biohazard Containment": {},
                        "Deck Gamma Monitor Hall": {},
                        "Subventilation Shaft Section B": {},
                        "Main Ventilation Shaft Section A": {},
                        "Deck Beta Transit Hall": {},
                        "Reactor Core": {},
                        "Cargo Freight Lift to Deck Gamma": {},
                        "Reactor Core Entrance": {}
                    },
              },
            "Tallon Overworld": {
                    "transports": {
                            "Tallon Overworld North (Tallon Canyon)":  "Chozo Ruins West (Main Plaza)",
                            "Tallon Overworld West (Root Cave)": "Magmoor Caverns East (Twin Fires)",
                            "Tallon Overworld East (Frigate Crash Site)": "Chozo Ruins East (Reflecting Pool, Save Station)",
                            "Tallon Overworld South (Great Tree Hall, Upper)": "Phazon Mines East (Main Quarry)",
                            "Tallon Overworld South (Great Tree Hall, Lower)": "Chozo Ruins South (Reflecting Pool, Far End)",
                            "Artifact Temple": temple_dest(options.final_bosses)
                    },
                    "rooms": {
                        "Landing Site": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Tallon Overworld: Landing Site"),
                                "hudmemoText": item_text(world,
                                                          "Tallon Overworld: Landing Site") + " Acquired!",
                                "currIncrease": 59,
                                "model": item_model(world, "Tallon Overworld: Landing Site"),
                                "showIcon": True
                            }]
                        },
                        "Gully": {},
                        "Canyon Cavern": {},
                        "Temple Hall": {},
                        "Alcove": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Tallon Overworld: Alcove"),
                                "hudmemoText": item_text(world, "Tallon Overworld: Alcove") + " Acquired!",
                                "currIncrease": 60,
                                "model": item_model(world, "Tallon Overworld: Alcove"),
                                "showIcon": True
                            }]
                        },
                        "Waterfall Cavern": {},
                        "Tallon Canyon": {},
                        "Temple Security Station": {},
                        "Frigate Crash Site": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Tallon Overworld: Frigate Crash Site"),
                                "hudmemoText": item_text(world,
                                                          "Tallon Overworld: Frigate Crash Site") + " Acquired!",
                                "currIncrease": 61,
                                "model": item_model(world, "Tallon Overworld: Frigate Crash Site"),
                                "showIcon": True
                            }]
                        },
                        "Transport Tunnel A": {},
                        "Root Tunnel": {},
                        "Temple Lobby": {},
                        "Frigate Access Tunnel": {},
                        "Overgrown Cavern": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Tallon Overworld: Overgrown Cavern"),
                                "hudmemoText": item_text(world,
                                                          "Tallon Overworld: Overgrown Cavern") + " Acquired!",
                                "currIncrease": 62,
                                "model": item_model(world, "Tallon Overworld: Overgrown Cavern"),
                                "showIcon": True
                            }]
                        },
                        "Transport to Chozo Ruins West": {},
                        "Root Cave": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Tallon Overworld: Root Cave"),
                                "hudmemoText": item_text(world,
                                                          "Tallon Overworld: Root Cave") + " Acquired!",
                                "currIncrease": 63,
                                "model": item_model(world, "Tallon Overworld: Root Cave"),
                                "showIcon": True
                            }]
                        },
                        "Artifact Temple": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Tallon Overworld: Artifact Temple"),
                                "hudmemoText": item_text(world,
                                                          "Tallon Overworld: Artifact Temple") + " Acquired!",
                                "currIncrease": 64,
                                "model": item_model(world, "Tallon Overworld: Artifact Temple"),
                                "showIcon": True
                            }]
                        },
                        "Main Ventilation Shaft Section C": {},
                        "Transport Tunnel C": {},
                        "Transport Tunnel B": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Tallon Overworld: Transport Tunnel B"),
                                "hudmemoText": item_text(world,
                                                          "Tallon Overworld: Transport Tunnel B") + " Acquired!",
                                "currIncrease": 65,
                                "model": item_model(world, "Tallon Overworld: Transport Tunnel B"),
                                "showIcon": True
                            }]
                        },
                        "Arbor Chamber": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Tallon Overworld: Arbor Chamber"),
                                "hudmemoText": item_text(world,
                                                          "Tallon Overworld: Arbor Chamber") + " Acquired!",
                                "currIncrease": 66,
                                "model": item_model(world, "Tallon Overworld: Arbor Chamber"),
                                "showIcon": True
                            }]},
                        "Main Ventilation Shaft Section B": {},
                        "Transport to Chozo Ruins East": {},
                        "Transport to Magmoor Caverns East": {},
                        "Main Ventilation Shaft Section A": {},
                        "Reactor Core": {},
                        "Reactor Access": {},
                        "Cargo Freight Lift to Deck Gamma": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world,
                                                      "Tallon Overworld: Cargo Freight Lift to Deck Gamma"),
                                "hudmemoText": item_text(world,
                                                          "Tallon Overworld: Cargo Freight Lift to Deck Gamma") + " Acquired!",
                                "currIncrease": 67,
                                "model": item_model(world, "Tallon Overworld: Cargo Freight Lift to Deck Gamma"),
                                "showIcon": True
                            }]
                        },
                        "Savestation": {},
                        "Deck Beta Transit Hall": {},
                        "Biohazard Containment": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Tallon Overworld: Biohazard Containment"),
                                "hudmemoText": item_text(world,
                                                          "Tallon Overworld: Biohazard Containment") + " Acquired!",
                                "currIncrease": 68,
                                "model": item_model(world, "Tallon Overworld: Biohazard Containment"),
                                "showIcon": True
                            }]
                        },
                        "Deck Beta Security Hall": {},
                        "Biotech Research Area 1": {},
                        "Deck Beta Conduit Hall": {},
                        "Connection Elevator to Deck Beta": {},
                        "Hydro Access Tunnel": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Tallon Overworld: Hydro Access Tunnel"),
                                "hudmemoText": item_text(world,
                                                          "Tallon Overworld: Hydro Access Tunnel") + " Acquired!",
                                "currIncrease": 69,
                                "model": item_model(world, "Tallon Overworld: Hydro Access Tunnel"),
                                "showIcon": True
                            }]
                        },
                        "Great Tree Hall": {},
                        "Great Tree Chamber": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Tallon Overworld: Great Tree Chamber"),
                                "hudmemoText": item_text(world,
                                                          "Tallon Overworld: Great Tree Chamber") + " Acquired!",
                                "currIncrease": 70,
                                "model": item_model(world, "Tallon Overworld: Great Tree Chamber"),
                                "showIcon": True
                            }]
                        },
                        "Transport Tunnel D": {},
                        "Life Grove Tunnel": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Tallon Overworld: Life Grove Tunnel"),
                                "hudmemoText": item_text(world,
                                                          "Tallon Overworld: Life Grove Tunnel") + " Acquired!",
                                "currIncrease": 71,
                                "model": item_model(world, "Tallon Overworld: Life Grove Tunnel"),
                                "showIcon": True
                            }]
                        },
                        "Transport Tunnel E": {},
                        "Transport to Chozo Ruins South": {},
                        "Life Grove": {
                            "pickups": [
                                {
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Tallon Overworld: Life Grove - Start"),
                                    "hudmemoText": item_text(world,
                                                              "Tallon Overworld: Life Grove - Start") + " Acquired!",
                                    "currIncrease": 72,
                                    "model": item_model(world, "Tallon Overworld: Life Grove - Start"),
                                    "showIcon": True
                                },
                                {
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world,
                                                          "Tallon Overworld: Life Grove - Underwater Spinner"),
                                    "hudmemoText": item_text(world,
                                                              "Tallon Overworld: Life Grove - Underwater Spinner") + " Acquired!",
                                    "currIncrease": 73,
                                    "model": item_model(world,
                                                        "Tallon Overworld: Life Grove - Underwater Spinner"),
                                    "showIcon": True
                                }
                            ]
                        },
                        "Transport to Phazon Mines East": {}
                },
              },
            "Chozo Ruins": {
                  "transports": {
                      "Chozo Ruins West (Main Plaza)": "Tallon Overworld North (Tallon Canyon)",
                      "Chozo Ruins North (Sun Tower)": "Magmoor Caverns North (Lava Lake)",
                      "Chozo Ruins East (Reflecting Pool, Save Station)": "Tallon Overworld East (Frigate Crash Site)",
                      "Chozo Ruins South (Reflecting Pool, Far End)": "Tallon Overworld South (Great Tree Hall, Lower)",
                  },
                  "rooms": {
                      "Transport to Tallon Overworld North": {},
                      "Ruins Entrance": {},
                      "Main Plaza": {
                          "pickups": [
                              {
                                  "type": "Unknown Item 1",
                                  "scanText": item_text(world,
                                                        "Chozo Ruins: Main Plaza - Half-Pipe"),
                                  "hudmemoText": item_text(world,
                                                            "Chozo Ruins: Main Plaza - Half-Pipe") + " Acquired!",
                                  "currIncrease": 1,
                                  "model": item_model(world, "Chozo Ruins: Main Plaza - Half-Pipe"),
                                  "showIcon": True
                              },
                              {
                                  "type": "Unknown Item 1",
                                  "scanText": item_text(world,
                                                        "Chozo Ruins: Main Plaza - Grapple Ledge"),
                                  "hudmemoText": item_text(world,
                                                            "Chozo Ruins: Main Plaza - Grapple Ledge") + " Acquired!",
                                  "currIncrease": 2,
                                  "model": item_model(world,
                                                      "Chozo Ruins: Main Plaza - Grapple Ledge"),
                                  "showIcon": True
                              },
                              {
                                  "type": "Unknown Item 1",
                                  "scanText": item_text(world,
                                                        "Chozo Ruins: Main Plaza - Tree"),
                                  "hudmemoText": item_text(world,
                                                            "Chozo Ruins: Main Plaza - Tree") + " Acquired!",
                                  "currIncrease": 3,
                                  "model": item_model(world,
                                                      "Chozo Ruins: Main Plaza - Tree"),
                                  "showIcon": True
                              },
                              {
                                  "type": "Unknown Item 1",
                                  "scanText": item_text(world,
                                                        "Chozo Ruins: Main Plaza - Locked Door"),
                                  "hudmemoText": item_text(world,
                                                            "Chozo Ruins: Main Plaza - Locked Door") + " Acquired!",
                                  "currIncrease": 4,
                                  "model": item_model(world,
                                                      "Chozo Ruins: Main Plaza - Locked Door"),
                                  "showIcon": True
                              }
                          ]
                      },
                      "Ruined Fountain Access": {},
                      "Ruined Shrine Access": {},
                      "Nursery Access": {},
                      "Plaza Access": {},
                      "Piston Tunnel": {},
                      "Ruined Fountain": {
                          "pickups": [{
                              "type": "Unknown Item 1",
                              "scanText": item_text(world, "Chozo Ruins: Ruined Fountain"),
                              "hudmemoText": item_text(world,
                                                        "Chozo Ruins: Ruined Fountain") + " Acquired!",
                              "currIncrease": 5,
                              "model": item_model(world, "Chozo Ruins: Ruined Fountain"),
                              "showIcon": True
                          }]
                      },
                      "Ruined Shrine": {
                          "pickups": [
                              {
                                  "type": "Unknown Item 1",
                                  "scanText": item_text(world,
                                                        "Chozo Ruins: Ruined Shrine - Plated Beetle"),
                                  "hudmemoText": item_text(world,
                                                            "Chozo Ruins: Ruined Shrine - Plated Beetle") + " Acquired!",
                                  "currIncrease": 6,
                                  "model": item_model(world, "Chozo Ruins: Ruined Shrine - Plated Beetle"),
                                  "showIcon": True
                              },
                              {
                                  "type": "Unknown Item 1",
                                  "scanText": item_text(world,
                                                        "Chozo Ruins: Ruined Shrine - Half-Pipe"),
                                  "hudmemoText": item_text(world,
                                                            "Chozo Ruins: Ruined Shrine - Half-Pipe") + " Acquired!",
                                  "currIncrease": 7,
                                  "model": item_model(world,
                                                      "Chozo Ruins: Ruined Shrine - Half-Pipe"),
                                  "showIcon": True
                              },
                              {
                                  "type": "Unknown Item 1",
                                  "scanText": item_text(world,
                                                        "Chozo Ruins: Ruined Shrine - Lower Tunnel"),
                                  "hudmemoText": item_text(world,
                                                            "Chozo Ruins: Ruined Shrine - Lower Tunnel") + " Acquired!",
                                  "currIncrease": 8,
                                  "model": item_model(world,
                                                      "Chozo Ruins: Ruined Shrine - Lower Tunnel"),
                                  "showIcon": True
                              }
                          ]
                      },
                      "Eyon Tunnel": {},
                      "Vault": {
                          "pickups": [{
                              "type": "Unknown Item 1",
                              "scanText": item_text(world, "Chozo Ruins: Vault"),
                              "hudmemoText": item_text(world,
                                                        "Chozo Ruins: Vault") + " Acquired!",
                              "currIncrease": 9,
                              "model": item_model(world, "Chozo Ruins: Vault"),
                              "showIcon": True
                          }]
                      },
                      "Training Chamber": {
                          "pickups": [{
                              "type": "Unknown Item 1",
                              "scanText": item_text(world, "Chozo Ruins: Training Chamber"),
                              "hudmemoText": item_text(world,
                                                        "Chozo Ruins: Training Chamber") + " Acquired!",
                              "currIncrease": 10,
                              "model": item_model(world, "Chozo Ruins: Training Chamber"),
                              "showIcon": True
                          }]
                      },
                      "Arboretum Access": {},
                      "Meditation Fountain": {},
                      "Tower of Light Access": {},
                      "Ruined Nursery": {
                          "pickups": [{
                              "type": "Unknown Item 1",
                              "scanText": item_text(world, "Chozo Ruins: Ruined Nursery"),
                              "hudmemoText": item_text(world,
                                                        "Chozo Ruins: Ruined Nursery") + " Acquired!",
                              "currIncrease": 11,
                              "model": item_model(world, "Chozo Ruins: Ruined Nursery"),
                              "showIcon": True
                          }]
                      },
                      "Vault Access": {},
                      "Training Chamber Access": {
                          "pickups": [{
                              "type": "Unknown Item 1",
                              "scanText": item_text(world, "Chozo Ruins: Training Chamber Access"),
                              "hudmemoText": item_text(world,
                                                        "Chozo Ruins: Training Chamber Access") + " Acquired!",
                              "currIncrease": 12,
                              "model": item_model(world, "Chozo Ruins: Training Chamber Access"),
                              "showIcon": True
                          }]
                      },
                      "Arboretum": {},
                      "Magma Pool": {
                          "pickups": [{
                              "type": "Unknown Item 1",
                              "scanText": item_text(world, "Chozo Ruins: Magma Pool"),
                              "hudmemoText": item_text(world,
                                                        "Chozo Ruins: Magma Pool") + " Acquired!",
                              "currIncrease": 13,
                              "model": item_model(world, "Chozo Ruins: Magma Pool"),
                              "showIcon": True
                          }]
                      },
                      "Tower of Light": {
                          "pickups": [{
                              "type": "Unknown Item 1",
                              "scanText": item_text(world, "Chozo Ruins: Tower of Light"),
                              "hudmemoText": item_text(world,
                                                        "Chozo Ruins: Tower of Light") + " Acquired!",
                              "currIncrease": 14,
                              "model": item_model(world, "Chozo Ruins: Tower of Light"),
                              "showIcon": True
                          }]
                      },
                      "Save Station 1": {},
                      "North Atrium": {},
                      "Transport to Magmoor Caverns North": {},
                      "Sunchamber Lobby": {},
                      "Gathering Hall Access": {},
                      "Tower Chamber": {
                          "pickups": [{
                              "type": "Unknown Item 1",
                              "scanText": item_text(world, "Chozo Ruins: Tower Chamber"),
                              "hudmemoText": item_text(world,
                                                        "Chozo Ruins: Tower Chamber") + " Acquired!",
                              "currIncrease": 15,
                              "model": item_model(world, "Chozo Ruins: Tower Chamber"),
                              "showIcon": True
                          }]
                      },
                      "Ruined Gallery": {
                          "pickups": [
                              {
                                  "type": "Unknown Item 1",
                                  "scanText": item_text(world,
                                                        "Chozo Ruins: Ruined Gallery - Missile Wall"),
                                  "hudmemoText": item_text(world,
                                                            "Chozo Ruins: Ruined Gallery - Missile Wall") + " Acquired!",
                                  "currIncrease": 16,
                                  "model": item_model(world,
                                                      "Chozo Ruins: Ruined Gallery - Missile Wall"),
                                  "showIcon": True
                              },
                              {
                                  "type": "Unknown Item 1",
                                  "scanText": item_text(world,
                                                        "Chozo Ruins: Ruined Gallery - Tunnel"),
                                  "hudmemoText": item_text(world,
                                                            "Chozo Ruins: Ruined Gallery - Tunnel") + " Acquired!",
                                  "currIncrease": 17,
                                  "model": item_model(world,
                                                      "Chozo Ruins: Ruined Gallery - Tunnel"),
                                  "showIcon": True
                              }
                          ],
                      },
                      "Sun Tower": {},
                      "Transport Access North": {
                          "pickups": [{
                              "type": "Unknown Item 1",
                              "scanText": item_text(world, "Chozo Ruins: Transport Access North"),
                              "hudmemoText": item_text(world,
                                                        "Chozo Ruins: Transport Access North") + " Acquired!",
                              "currIncrease": 18,
                              "model": item_model(world, "Chozo Ruins: Transport Access North"),
                              "showIcon": True
                          }]
                      },
                      "Sunchamber Access": {},
                      "Gathering Hall": {
                          "pickups": [{
                              "type": "Unknown Item 1",
                              "scanText": item_text(world, "Chozo Ruins: Gathering Hall"),
                              "hudmemoText": item_text(world,
                                                        "Chozo Ruins: Gathering Hall") + " Acquired!",
                              "currIncrease": 19,
                              "model": item_model(world, "Chozo Ruins: Gathering Hall"),
                              "showIcon": True
                          }]
                      },
                      "Totem Access": {},
                      "Map Station": {},
                      "Sun Tower Access": {},
                      "Hive Totem": {
                          "pickups": [{
                              "type": "Unknown Item 1",
                              "scanText": item_text(world, "Chozo Ruins: Hive Totem"),
                              "hudmemoText": item_text(world,
                                                        "Chozo Ruins: Hive Totem") + " Acquired!",
                              "currIncrease": 20,
                              "model": item_model(world, "Chozo Ruins: Hive Totem"),
                              "showIcon": True
                          }]
                      },
                      "Sunchamber": {
                          "pickups": [
                              {
                                  "type": "Unknown Item 1",
                                  "scanText": item_text(world,
                                                        "Chozo Ruins: Sunchamber - Flaaghra"),
                                  "hudmemoText": item_text(world,
                                                            "Chozo Ruins: Sunchamber - Flaaghra") + " Acquired!",
                                  "currIncrease": 21,
                                  "model": item_model(world,
                                                      "Chozo Ruins: Sunchamber - Flaaghra"),
                                  "showIcon": True
                              },
                              {
                                  "type": "Unknown Item 1",
                                  "scanText": item_text(world,
                                                        "Chozo Ruins: Sunchamber - Ghosts"),
                                  "hudmemoText": item_text(world,
                                                            "Chozo Ruins: Sunchamber - Ghosts") + " Acquired!",
                                  "currIncrease": 22,
                                  "model": item_model(world,
                                                      "Chozo Ruins: Sunchamber - Ghosts"),
                                  "showIcon": True
                              }
                          ]
                      },
                      "Watery Hall Access": {
                          "pickups": [{
                              "type": "Unknown Item 1",
                              "scanText": item_text(world, "Chozo Ruins: Watery Hall Access"),
                              "hudmemoText": item_text(world,
                                                        "Chozo Ruins: Watery Hall Access") + " Acquired!",
                              "currIncrease": 23,
                              "model": item_model(world, "Chozo Ruins: Watery Hall Access"),
                              "showIcon": True
                          }]
                      },
                      "Save Station 2": {},
                      "East Atrium": {},
                      "Watery Hall": {
                          "pickups": [
                              {
                                  "type": "Unknown Item 1",
                                  "scanText": item_text(world,
                                                        "Chozo Ruins: Watery Hall - Scan Puzzle"),
                                  "hudmemoText": item_text(world,
                                                            "Chozo Ruins: Watery Hall - Scan Puzzle") + " Acquired!",
                                  "currIncrease": 24,
                                  "model": item_model(world,
                                                      "Chozo Ruins: Watery Hall - Scan Puzzle"),
                                  "showIcon": True
                              },
                              {
                                  "type": "Unknown Item 1",
                                  "scanText": item_text(world,
                                                        "Chozo Ruins: Watery Hall - Underwater"),
                                  "hudmemoText": item_text(world,
                                                            "Chozo Ruins: Watery Hall - Underwater") + " Acquired!",
                                  "currIncrease": 25,
                                  "model": item_model(world,
                                                      "Chozo Ruins: Watery Hall - Underwater"),
                                  "showIcon": True
                              }
                          ]
                      },
                      "Energy Core Access": {},
                      "Dynamo Access": {},
                      "Energy Core": {},
                      "Dynamo": {
                          "pickups": [
                              {
                                  "type": "Unknown Item 1",
                                  "scanText": item_text(world,
                                                        "Chozo Ruins: Dynamo - Lower"),
                                  "hudmemoText": item_text(world,
                                                            "Chozo Ruins: Dynamo - Lower") + " Acquired!",
                                  "currIncrease": 26,
                                  "model": item_model(world,
                                                      "Chozo Ruins: Dynamo - Lower"),
                                  "showIcon": True
                              },
                              {
                                  "type": "Unknown Item 1",
                                  "scanText": item_text(world,
                                                        "Chozo Ruins: Dynamo - Spider Track"),
                                  "hudmemoText": item_text(world,
                                                            "Chozo Ruins: Dynamo - Spider Track") + " Acquired!",
                                  "currIncrease": 27,
                                  "model": item_model(world,
                                                      "Chozo Ruins: Dynamo - Spider Track"),
                                  "showIcon": True
                              }
                          ]
                      },
                      "Burn Dome Access": {},
                      "West Furnace Access": {},
                      "Burn Dome": {
                          "pickups": [
                              {
                                  "type": "Unknown Item 1",
                                  "scanText": item_text(world,
                                                        "Chozo Ruins: Burn Dome - Missile"),
                                  "hudmemoText": item_text(world,
                                                            "Chozo Ruins: Burn Dome - Missile") + " Acquired!",
                                  "currIncrease": 28,
                                  "model": item_model(world,
                                                      "Chozo Ruins: Burn Dome - Missile"),
                                  "showIcon": True
                              },
                              {
                                  "type": "Unknown Item 1",
                                  "scanText": item_text(world,
                                                        "Chozo Ruins: Burn Dome - Incinerator Drone"),
                                  "hudmemoText": item_text(world,
                                                            "Chozo Ruins: Burn Dome - Incinerator Drone") + " Acquired!",
                                  "currIncrease": 29,
                                  "model": item_model(world,
                                                      "Chozo Ruins: Burn Dome - Incinerator Drone"),
                                  "showIcon": True
                              }
                          ]
                      },
                      "Furnace": {
                          "pickups": [
                              {
                                  "type": "Unknown Item 1",
                                  "scanText": item_text(world,
                                                        "Chozo Ruins: Furnace - Spider Tracks"),
                                  "hudmemoText": item_text(world,
                                                            "Chozo Ruins: Furnace - Spider Tracks") + " Acquired!",
                                  "currIncrease": 30,
                                  "model": item_model(world,
                                                      "Chozo Ruins: Furnace - Spider Tracks"),
                                  "showIcon": True
                              },
                              {
                                  "type": "Unknown Item 1",
                                  "scanText": item_text(world,
                                                        "Chozo Ruins: Furnace - Inside Furnace"),
                                  "hudmemoText": item_text(world,
                                                            "Chozo Ruins: Furnace - Inside Furnace") + " Acquired!",
                                  "currIncrease": 31,
                                  "model": item_model(world,
                                                      "Chozo Ruins: Furnace - Inside Furnace"),
                                  "showIcon": True
                              }
                          ]
                      },
                      "East Furnace Access": {},
                      "Crossway Access West": {},
                      "Hall of the Elders": {
                          "pickups": [{
                              "type": "Unknown Item 1",
                              "scanText": item_text(world, "Chozo Ruins: Hall of the Elders"),
                              "hudmemoText": item_text(world,
                                                        "Chozo Ruins: Hall of the Elders") + " Acquired!",
                              "currIncrease": 32,
                              "model": item_model(world, "Chozo Ruins: Hall of the Elders"),
                              "showIcon": True
                          }]
                      },
                      "Crossway": {
                          "pickups": [{
                              "type": "Unknown Item 1",
                              "scanText": item_text(world, "Chozo Ruins: Crossway"),
                              "hudmemoText": item_text(world,
                                                        "Chozo Ruins: Crossway") + " Acquired!",
                              "currIncrease": 33,
                              "model": item_model(world, "Chozo Ruins: Crossway"),
                              "showIcon": True
                          }]
                      },
                      "Reflecting Pool Access": {},
                      "Elder Hall Access": {},
                      "Crossway Access South": {},
                      "Elder Chamber": {
                          "pickups": [{
                              "type": "Unknown Item 1",
                              "scanText": item_text(world, "Chozo Ruins: Elder Chamber"),
                              "hudmemoText": item_text(world,
                                                        "Chozo Ruins: Elder Chamber") + " Acquired!",
                              "currIncrease": 34,
                              "model": item_model(world, "Chozo Ruins: Elder Chamber"),
                              "showIcon": True
                          }]
                      },
                      "Reflecting Pool": {},
                      "Save Station 3": {},
                      "Transport Access South": {},
                      "Antechamber": {
                          "pickups": [{
                              "type": "Unknown Item 1",
                              "scanText": item_text(world, "Chozo Ruins: Antechamber"),
                              "hudmemoText": item_text(world,
                                                        "Chozo Ruins: Antechamber") + " Acquired!",
                              "currIncrease": 35,
                              "model": item_model(world, "Chozo Ruins: Antechamber"),
                              "showIcon": True
                          }]
                      },
                      "Transport to Tallon Overworld East": {},
                      "Transport to Tallon Overworld South": {}
                      }
                },
                "Magmoor Caverns": {
                        "transports": {
                            "Magmoor Caverns North (Lava Lake)": "Chozo Ruins North (Sun Tower)",
                            "Magmoor Caverns West (Monitor Station)": "Phendrana Drifts North (Phendrana Shorelines)",
                            "Magmoor Caverns East (Twin Fires)": "Tallon Overworld West (Root Cave)",
                            "Magmoor Caverns South (Magmoor Workstation, Save Station)": "Phendrana Drifts South (Quarantine Cave)",
                            "Magmoor Caverns South (Magmoor Workstation, Debris)": "Phazon Mines West (Phazon Processing Center)",
                        },
                        "rooms": {
                            "Transport to Chozo Ruins North": {},
                            "Burning Trail": {},
                            "Lake Tunnel": {},
                            "Save Station Magmoor A": {},
                            "Lava Lake": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Magmoor Caverns: Lava Lake"),
                                    "hudmemoText": item_text(world,
                                                              "Magmoor Caverns: Lava Lake") + " Acquired!",
                                    "currIncrease": 91,
                                    "model": item_model(world, "Magmoor Caverns: Lava Lake"),
                                    "showIcon": True
                                }]
                            },
                            "Pit Tunnel": {},
                            "Triclops Pit": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Magmoor Caverns: Triclops Pit"),
                                    "hudmemoText": item_text(world,
                                                              "Magmoor Caverns: Triclops Pit") + " Acquired!",
                                    "currIncrease": 92,
                                    "model": item_model(world, "Magmoor Caverns: Triclops Pit"),
                                    "showIcon": True
                                }]
                            },
                            "Monitor Tunnel": {},
                            "Storage Cavern": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Magmoor Caverns: Storage Cavern"),
                                    "hudmemoText": item_text(world,
                                                              "Magmoor Caverns: Storage Cavern") + " Acquired!",
                                    "currIncrease": 93,
                                    "model": item_model(world, "Magmoor Caverns: Storage Cavern"),
                                    "showIcon": True
                                }]
                            },
                            "Monitor Station": {},
                            "Transport Tunnel A": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Magmoor Caverns: Transport Tunnel A"),
                                    "hudmemoText": item_text(world,
                                                              "Magmoor Caverns: Transport Tunnel A") + " Acquired!",
                                    "currIncrease": 94,
                                    "model": item_model(world, "Magmoor Caverns: Transport Tunnel A"),
                                    "showIcon": True
                                }]
                            },
                            "Warrior Shrine": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Magmoor Caverns: Warrior Shrine"),
                                    "hudmemoText": item_text(world,
                                                              "Magmoor Caverns: Warrior Shrine") + " Acquired!",
                                    "currIncrease": 95,
                                    "model": item_model(world, "Magmoor Caverns: Warrior Shrine"),
                                    "showIcon": True
                                }]
                            },
                            "Shore Tunnel": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Magmoor Caverns: Shore Tunnel"),
                                    "hudmemoText": item_text(world,
                                                              "Magmoor Caverns: Shore Tunnel") + " Acquired!",
                                    "currIncrease": 96,
                                    "model": item_model(world, "Magmoor Caverns: Shore Tunnel"),
                                    "showIcon": True
                                }]
                            },
                            "Transport to Phendrana Drifts North": {},
                            "Fiery Shores": {
                                "pickups": [
                                    {
                                        "type": "Unknown Item 1",
                                        "scanText": item_text(world,
                                                              "Magmoor Caverns: Fiery Shores - Morph Track"),
                                        "hudmemoText": item_text(world,
                                                                  "Magmoor Caverns: Fiery Shores - Morph Track") + " Acquired!",
                                        "currIncrease": 97,
                                        "model": item_model(world,
                                                            "Magmoor Caverns: Fiery Shores - Morph Track"),
                                        "showIcon": True
                                    },
                                    {
                                        "type": "Unknown Item 1",
                                        "scanText": item_text(world,
                                                              "Magmoor Caverns: Fiery Shores - Warrior Shrine Tunnel"),
                                        "hudmemoText": item_text(world,
                                                                  "Magmoor Caverns: Fiery Shores - Warrior Shrine Tunnel") + " Acquired!",
                                        "currIncrease": 98,
                                        "model": item_model(world,
                                                            "Magmoor Caverns: Fiery Shores - Warrior Shrine Tunnel"),
                                        "showIcon": True
                                    }
                                ]
                            },
                            "Transport Tunnel B": {},
                            "Transport to Tallon Overworld West": {},
                            "Twin Fires Tunnel": {},
                            "Twin Fires": {},
                            "North Core Tunnel": {},
                            "Geothermal Core": {},
                            "Plasma Processing": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Magmoor Caverns: Plasma Processing"),
                                    "hudmemoText": item_text(world,
                                                              "Magmoor Caverns: Plasma Processing") + " Acquired!",
                                    "currIncrease": 99,
                                    "model": item_model(world, "Magmoor Caverns: Plasma Processing"),
                                    "showIcon": True
                                }]
                            },
                            "South Core Tunnel": {},
                            "Magmoor Workstation": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Magmoor Caverns: Magmoor Workstation"),
                                    "hudmemoText": item_text(world,
                                                              "Magmoor Caverns: Magmoor Workstation") + " Acquired!",
                                    "currIncrease": 100,
                                    "model": item_model(world, "Magmoor Caverns: Magmoor Workstation"),
                                    "showIcon": True
                                }]
                            },
                            "Workstation Tunnel": {},
                            "Transport Tunnel C": {},
                            "Transport to Phazon Mines West": {},
                            "Transport to Phendrana Drifts South": {},
                            "Save Station Magmoor B": {}
                        }
                },
                "Phendrana Drifts": {
                        "transports": {
                            "Phendrana Drifts North (Phendrana Shorelines)": "Magmoor Caverns West (Monitor Station)",
                            "Phendrana Drifts South (Quarantine Cave)": "Magmoor Caverns South (Magmoor Workstation, Save Station)",
                        },
                        "rooms": {
                            "Transport to Magmoor Caverns West": {},
                            "Shoreline Entrance": {},
                            "Phendrana Shorelines": {
                                "pickups": [
                                    {
                                        "type": "Unknown Item 1",
                                        "scanText": item_text(world,
                                                              "Phendrana Drifts: Phendrana Shorelines - Behind Ice"),
                                        "hudmemoText": item_text(world,
                                                                  "Phendrana Drifts: Phendrana Shorelines - Behind Ice") + " Acquired!",
                                        "currIncrease": 36,
                                        "model": item_model(world,
                                                            "Phendrana Drifts: Phendrana Shorelines - Behind Ice"),
                                        "showIcon": True
                                    },
                                    {
                                        "type": "Unknown Item 1",
                                        "scanText": item_text(world,
                                                              "Phendrana Drifts: Phendrana Shorelines - Spider Track"),
                                        "hudmemoText": item_text(world,
                                                                  "Phendrana Drifts: Phendrana Shorelines - Spider Track") + " Acquired!",
                                        "currIncrease": 37,
                                        "model": item_model(world,
                                                            "Phendrana Drifts: Phendrana Shorelines - Spider Track"),
                                        "showIcon": True
                                    }
                                ]
                            },
                            "Temple Entryway": {},
                            "Save Station B": {},
                            "Ruins Entryway": {},
                            "Plaza Walkway": {},
                            "Ice Ruins Access": {},
                            "Chozo Ice Temple": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Phendrana Drifts: Chozo Ice Temple"),
                                    "hudmemoText": item_text(world,
                                                              "Phendrana Drifts: Chozo Ice Temple") + " Acquired!",
                                    "currIncrease": 38,
                                    "model": item_model(world, "Phendrana Drifts: Chozo Ice Temple"),
                                    "showIcon": True
                                }]
                            },
                            "Ice Ruins West": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Phendrana Drifts: Ice Ruins West"),
                                    "hudmemoText": item_text(world,
                                                              "Phendrana Drifts: Ice Ruins West") + " Acquired!",
                                    "currIncrease": 39,
                                    "model": item_model(world, "Phendrana Drifts: Ice Ruins West"),
                                    "showIcon": True
                                }]
                            },
                            "Ice Ruins East": {
                                "pickups": [
                                    {
                                        "type": "Unknown Item 1",
                                        "scanText": item_text(world,
                                                              "Phendrana Drifts: Ice Ruins East - Behind Ice"),
                                        "hudmemoText": item_text(world,
                                                                  "Phendrana Drifts: Ice Ruins East - Behind Ice") + " Acquired!",
                                        "currIncrease": 40,
                                        "model": item_model(world,
                                                            "Phendrana Drifts: Ice Ruins East - Behind Ice"),
                                        "showIcon": True
                                    },
                                    {
                                        "type": "Unknown Item 1",
                                        "scanText": item_text(world,
                                                              "Phendrana Drifts: Ice Ruins East - Spider Track"),
                                        "hudmemoText": item_text(world,
                                                                  "Phendrana Drifts: Ice Ruins East - Spider Track") + " Acquired!",
                                        "currIncrease": 41,
                                        "model": item_model(world,
                                                            "Phendrana Drifts: Ice Ruins East - Spider Track"),
                                        "showIcon": True
                                    }
                                ]
                            },
                            "Chapel Tunnel": {},
                            "Courtyard Entryway": {},
                            "Canyon Entryway": {},
                            "Chapel of the Elders": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Phendrana Drifts: Chapel of the Elders"),
                                    "hudmemoText": item_text(world,
                                                              "Phendrana Drifts: Chapel of the Elders") + " Acquired!",
                                    "currIncrease": 42,
                                    "model": item_model(world, "Phendrana Drifts: Chapel of the Elders"),
                                    "showIcon": True
                                }]
                            },
                            "Ruined Courtyard": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Phendrana Drifts: Ruined Courtyard"),
                                    "hudmemoText": item_text(world,
                                                              "Phendrana Drifts: Ruined Courtyard") + " Acquired!",
                                    "currIncrease": 43,
                                    "model": item_model(world, "Phendrana Drifts: Ruined Courtyard"),
                                    "showIcon": True
                                }]
                            },
                            "Phendrana Canyon": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Phendrana Drifts: Phendrana Canyon"),
                                    "hudmemoText": item_text(world,
                                                              "Phendrana Drifts: Phendrana Canyon") + " Acquired!",
                                    "currIncrease": 44,
                                    "model": item_model(world, "Phendrana Drifts: Phendrana Canyon"),
                                    "showIcon": True
                                }]
                            },
                            "Save Station A": {},
                            "Specimen Storage": {},
                            "Quarantine Access": {},
                            "Research Entrance": {},
                            "North Quarantine Tunnel": {},
                            "Map Station": {},
                            "Hydra Lab Entryway": {},
                            "Quarantine Cave": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Phendrana Drifts: Quarantine Cave"),
                                    "hudmemoText": item_text(world,
                                                              "Phendrana Drifts: Quarantine Cave") + " Acquired!",
                                    "currIncrease": 45,
                                    "model": item_model(world, "Phendrana Drifts: Quarantine Cave"),
                                    "showIcon": True
                                }]
                            },
                            "Research Lab Hydra": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Phendrana Drifts: Research Lab Hydra"),
                                    "hudmemoText": item_text(world,
                                                              "Phendrana Drifts: Research Lab Hydra") + " Acquired!",
                                    "currIncrease": 46,
                                    "model": item_model(world, "Phendrana Drifts: Research Lab Hydra"),
                                    "showIcon": True
                                }]
                            },
                            "South Quarantine Tunnel": {},
                            "Quarantine Monitor": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Phendrana Drifts: Quarantine Monitor"),
                                    "hudmemoText": item_text(world,
                                                              "Phendrana Drifts: Quarantine Monitor") + " Acquired!",
                                    "currIncrease": 47,
                                    "model": item_model(world, "Phendrana Drifts: Quarantine Monitor"),
                                    "showIcon": True
                                }]
                            },
                            "Observatory Access": {},
                            "Transport to Magmoor Caverns South": {},
                            "Observatory": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Phendrana Drifts: Observatory"),
                                    "hudmemoText": item_text(world,
                                                              "Phendrana Drifts: Observatory") + " Acquired!",
                                    "currIncrease": 48,
                                    "model": item_model(world, "Phendrana Drifts: Observatory"),
                                    "showIcon": True
                                }]
                            },
                            "Transport Access": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Phendrana Drifts: Transport Access"),
                                    "hudmemoText": item_text(world,
                                                              "Phendrana Drifts: Transport Access") + " Acquired!",
                                    "currIncrease": 49,
                                    "model": item_model(world, "Phendrana Drifts: Transport Access"),
                                    "showIcon": True
                                }]
                            },
                            "West Tower Entrance": {},
                            "Save Station D": {},
                            "Frozen Pike": {},
                            "West Tower": {},
                            "Pike Access": {},
                            "Frost Cave Access": {},
                            "Hunter Cave Access": {},
                            "Control Tower": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Phendrana Drifts: Control Tower"),
                                    "hudmemoText": item_text(world,
                                                              "Phendrana Drifts: Control Tower") + " Acquired!",
                                    "currIncrease": 50,
                                    "model": item_model(world, "Phendrana Drifts: Control Tower"),
                                    "showIcon": True
                                }]
                            },
                            "Research Core": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Phendrana Drifts: Research Core"),
                                    "hudmemoText": item_text(world,
                                                              "Phendrana Drifts: Research Core") + " Acquired!",
                                    "currIncrease": 51,
                                    "model": item_model(world, "Phendrana Drifts: Research Core"),
                                    "showIcon": True
                                }]
                            },
                            "Frost Cave": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Phendrana Drifts: Frost Cave"),
                                    "hudmemoText": item_text(world,
                                                              "Phendrana Drifts: Frost Cave") + " Acquired!",
                                    "currIncrease": 52,
                                    "model": item_model(world, "Phendrana Drifts: Frost Cave"),
                                    "showIcon": True
                                }]
                            },
                            "Hunter Cave": {},
                            "East Tower": {},
                            "Research Core Access": {},
                            "Save Station C": {},
                            "Upper Edge Tunnel": {},
                            "Lower Edge Tunnel": {},
                            "Chamber Access": {},
                            "Lake Tunnel": {},
                            "Aether Lab Entryway": {},
                            "Research Lab Aether": {
                                "pickups": [
                                    {
                                        "type": "Unknown Item 1",
                                        "scanText": item_text(world,
                                                              "Phendrana Drifts: Research Lab Aether - Tank"),
                                        "hudmemoText": item_text(world,
                                                                  "Phendrana Drifts: Research Lab Aether - Tank") + " Acquired!",
                                        "currIncrease": 53,
                                        "model": item_model(world,
                                                            "Phendrana Drifts: Research Lab Aether - Tank"),
                                        "showIcon": True
                                    },
                                    {
                                        "type": "Unknown Item 1",
                                        "scanText": item_text(world,
                                                              "Phendrana Drifts: Research Lab Aether - Morph Track"),
                                        "hudmemoText": item_text(world,
                                                                  "Phendrana Drifts: Research Lab Aether - Morph Track") + " Acquired!",
                                        "currIncrease": 54,
                                        "model": item_model(world,
                                                            "Phendrana Drifts: Research Lab Aether - Morph Track"),
                                        "showIcon": True
                                    }
                                ]
                            },
                            "Phendrana's Edge": {},
                            "Gravity Chamber": {
                                "pickups": [
                                    {
                                        "type": "Unknown Item 1",
                                        "scanText": item_text(world,
                                                              "Phendrana Drifts: Gravity Chamber - Underwater"),
                                        "hudmemoText": item_text(world,
                                                                  "Phendrana Drifts: Gravity Chamber - Underwater") + " Acquired!",
                                        "currIncrease": 55,
                                        "model": item_model(world,
                                                            "Phendrana Drifts: Gravity Chamber - Underwater"),
                                        "showIcon": True
                                    },
                                    {
                                        "type": "Unknown Item 1",
                                        "scanText": item_text(world,
                                                              "Phendrana Drifts: Gravity Chamber - Grapple Ledge"),
                                        "hudmemoText": item_text(world,
                                                                  "Phendrana Drifts: Gravity Chamber - Grapple Ledge") + " Acquired!",
                                        "currIncrease": 56,
                                        "model": item_model(world,
                                                            "Phendrana Drifts: Gravity Chamber - Grapple Ledge"),
                                        "showIcon": True
                                    }
                                ]
                            },
                            "Storage Cave": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Phendrana Drifts: Storage Cave"),
                                    "hudmemoText": item_text(world,
                                                              "Phendrana Drifts: Storage Cave") + " Acquired!",
                                    "currIncrease": 57,
                                    "model": item_model(world, "Phendrana Drifts: Storage Cave"),
                                    "showIcon": True
                                }]
                            },
                            "Security Cave": {
                                "pickups": [{
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world, "Phendrana Drifts: Security Cave"),
                                    "hudmemoText": item_text(world,
                                                              "Phendrana Drifts: Security Cave") + " Acquired!",
                                    "currIncrease": 58,
                                    "model": item_model(world, "Phendrana Drifts: Security Cave"),
                                    "showIcon": True
                                }]
                            }
                        }
                },
                "Phazon Mines": {
                    "transports": {
                        "Phazon Mines East (Main Quarry)": "Tallon Overworld South (Great Tree Hall, Upper)",
                        "Phazon Mines West (Phazon Processing Center)": "Magmoor Caverns South (Magmoor Workstation, Debris)",
                    },
                    "rooms": {
                        "Transport to Tallon Overworld South": {},
                        "Quarry Access": {},
                        "Main Quarry": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Phazon Mines: Main Quarry"),
                                "hudmemoText": item_text(world,
                                                          "Phazon Mines: Main Quarry") + " Acquired!",
                                "currIncrease": 74,
                                "model": item_model(world, "Phazon Mines: Main Quarry"),
                                "showIcon": True
                            }]
                        },
                        "Waste Disposal": {},
                        "Save Station Mines A": {},
                        "Security Access A": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Phazon Mines: Security Access A"),
                                "hudmemoText": item_text(world,
                                                          "Phazon Mines: Security Access A") + " Acquired!",
                                "currIncrease": 75,
                                "model": item_model(world, "Phazon Mines: Security Access A"),
                                "showIcon": True
                            }]
                        },
                        "Ore Processing": {},
                        "Mine Security Station": {},
                        "Research Access": {},
                        "Storage Depot B": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Phazon Mines: Storage Depot B"),
                                "hudmemoText": item_text(world,
                                                          "Phazon Mines: Storage Depot B") + " Acquired!",
                                "currIncrease": 76,
                                "model": item_model(world, "Phazon Mines: Storage Depot B"),
                                "showIcon": True
                            }]
                        },
                        "Elevator Access A": {},
                        "Security Access B": {},
                        "Storage Depot A": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Phazon Mines: Storage Depot A"),
                                "hudmemoText": item_text(world,
                                                          "Phazon Mines: Storage Depot A") + " Acquired!",
                                "currIncrease": 77,
                                "model": item_model(world, "Phazon Mines: Storage Depot A"),
                                "showIcon": True
                            }]
                        },
                        "Elite Research": {
                            "pickups": [
                                {
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world,
                                                          "Phazon Mines: Elite Research - Phazon Elite"),
                                    "hudmemoText": item_text(world,
                                                              "Phazon Mines: Elite Research - Phazon Elite") + " Acquired!",
                                    "currIncrease": 78,
                                    "model": item_model(world,
                                                        "Phazon Mines: Elite Research - Phazon Elite"),
                                    "showIcon": True
                                },
                                {
                                    "type": "Unknown Item 1",
                                    "scanText": item_text(world,
                                                          "Phazon Mines: Elite Research - Laser"),
                                    "hudmemoText": item_text(world,
                                                              "Phazon Mines: Elite Research - Laser") + " Acquired!",
                                    "currIncrease": 79,
                                    "model": item_model(world,
                                                        "Phazon Mines: Elite Research - Laser"),
                                    "showIcon": True
                                }
                            ]
                        },
                        "Elevator A": {},
                        "Elite Control Access": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Phazon Mines: Elite Control Access"),
                                "hudmemoText": item_text(world,
                                                          "Phazon Mines: Elite Control Access") + " Acquired!",
                                "currIncrease": 80,
                                "model": item_model(world, "Phazon Mines: Elite Control Access"),
                                "showIcon": True
                            }]
                        },
                        "Elite Control": {},
                        "Maintenance Tunnel": {},
                        "Ventilation Shaft": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Phazon Mines: Ventilation Shaft"),
                                "hudmemoText": item_text(world,
                                                          "Phazon Mines: Ventilation Shaft") + " Acquired!",
                                "currIncrease": 81,
                                "model": item_model(world, "Phazon Mines: Ventilation Shaft"),
                                "showIcon": True
                            }]
                        },
                        "Phazon Processing Center": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Phazon Mines: Phazon Processing Center"),
                                "hudmemoText": item_text(world,
                                                          "Phazon Mines: Phazon Processing Center") + " Acquired!",
                                "currIncrease": 82,
                                "model": item_model(world, "Phazon Mines: Phazon Processing Center"),
                                "showIcon": True
                            }]
                        },
                        "Omega Research": {},
                        "Transport Access": {},
                        "Processing Center Access": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Phazon Mines: Processing Center Access"),
                                "hudmemoText": item_text(world,
                                                          "Phazon Mines: Processing Center Access") + " Acquired!",
                                "currIncrease": 83,
                                "model": item_model(world, "Phazon Mines: Processing Center Access"),
                                "showIcon": True
                            }]
                        },
                        "Map Station Mines": {},
                        "Dynamo Access": {},
                        "Transport to Magmoor Caverns South": {},
                        "Elite Quarters": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Phazon Mines: Elite Quarters"),
                                "hudmemoText": item_text(world,
                                                          "Phazon Mines: Elite Quarters") + " Acquired!",
                                "currIncrease": 84,
                                "model": item_model(world, "Phazon Mines: Elite Quarters"),
                                "showIcon": True
                            }]
                        },
                        "Central Dynamo": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Phazon Mines: Central Dynamo"),
                                "hudmemoText": item_text(world,
                                                          "Phazon Mines: Central Dynamo") + " Acquired!",
                                "currIncrease": 85,
                                "model": item_model(world, "Phazon Mines: Central Dynamo"),
                                "showIcon": True
                            }]
                        },
                        "Elite Quarters Access": {},
                        "Quarantine Access A": {},
                        "Save Station Mines B": {},
                        "Metroid Quarantine B": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Phazon Mines: Metroid Quarantine B"),
                                "hudmemoText": item_text(world,
                                                          "Phazon Mines: Metroid Quarantine B") + " Acquired!",
                                "currIncrease": 86,
                                "model": item_model(world, "Phazon Mines: Metroid Quarantine B"),
                                "showIcon": True
                            }]
                        },
                        "Metroid Quarantine A": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Phazon Mines: Metroid Quarantine A"),
                                "hudmemoText": item_text(world,
                                                          "Phazon Mines: Metroid Quarantine A") + " Acquired!",
                                "currIncrease": 87,
                                "model": item_model(world, "Phazon Mines: Metroid Quarantine A"),
                                "showIcon": True
                            }]
                        },
                        "Quarantine Access B": {},
                        "Save Station Mines C": {},
                        "Elevator Access B": {},
                        "Fungal Hall B": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Phazon Mines: Fungal Hall B"),
                                "hudmemoText": item_text(world,
                                                          "Phazon Mines: Fungal Hall B") + " Acquired!",
                                "currIncrease": 88,
                                "model": item_model(world, "Phazon Mines: Fungal Hall B"),
                                "showIcon": True
                            }]
                        },
                        "Elevator B": {},
                        "Missile Station Mines": {},
                        "Phazon Mining Tunnel": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Phazon Mines: Phazon Mining Tunnel"),
                                "hudmemoText": item_text(world,
                                                          "Phazon Mines: Phazon Mining Tunnel") + " Acquired!",
                                "currIncrease": 89,
                                "model": item_model(world, "Phazon Mines: Phazon Mining Tunnel"),
                                "showIcon": True
                            }]
                        },
                        "Fungal Hall Access": {
                            "pickups": [{
                                "type": "Unknown Item 1",
                                "scanText": item_text(world, "Phazon Mines: Fungal Hall Access"),
                                "hudmemoText": item_text(world,
                                                          "Phazon Mines: Fungal Hall Access") + " Acquired!",
                                "currIncrease": 90,
                                "model": item_model(world, "Phazon Mines: Fungal Hall Access"),
                                "showIcon": True
                            }]
                        },
                        "Fungal Hall A": {}
                    }
                },
                "Impact Crater": {
                        "transports": {
                            "Crater Entry Point": "Artifact Temple",
                            "Essence Dead Cutscene": "Credits",
                        },
                        "rooms": {
                            "Crater Entry Point": {},
                            "Crater Tunnel A": {},
                            "Phazon Core": {},
                            "Crater Missile Station": {},
                            "Crater Tunnel B": {},
                            "Phazon Infusion Chamber": {},
                            "Subchamber One": {},
                            "Subchamber Two": {},
                            "Subchamber Three": {},
                            "Subchamber Four": {},
                            "Subchamber Five": {},
                            "Metroid Prime Lair": {}
                        }
                },
                "End Cinema": {
                    "transports": {},
                    "rooms": {
                        "End Cinema": {}
                  }
                }
            }
        }
    return config
