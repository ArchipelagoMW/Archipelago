import json

def item_list(data):
    items = []

    for name, floor in data['floors'].items():
        if not floor["unlocked"]:
            items.append(f'Unlock {name}')

    items.append('Angel Deal Item')
    items.append('Boss Item')
    items.append('Curse Room Item')
    items.append('Devil Deal Item')
    items.append('Golden Chest Item')
    items.append('Library Item')
    items.append('Planetarium Item')
    items.append('Red Chest Item')
    items.append('Secret Room Item')
    items.append('Shop Item')
    items.append('Treasure Room Item')
    items.append('1-UP')
    items.append('Random Bomb')
    items.append('Random Card')
    items.append('Random Chest')
    items.append('Random Coin')
    items.append('Random Heart')
    items.append('Random Key')
    items.append('Random Pill')
    items.append('Random Trinket')
    
    items.append('Curse Trap')
    items.append('Paralysis Trap')
    items.append('Retro Vision Trap')
    items.append('Teleport Trap')
    items.append('Troll Bomb Trap')
    items.append('Wavy Cap Trap')

    items.append('Victory Condition')

    return items