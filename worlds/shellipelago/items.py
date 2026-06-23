from BaseClasses import ItemClassification

classification_table = {
    "progression": ItemClassification.progression,
    "useful": ItemClassification.useful,
    "filler": ItemClassification.filler,
    "trap": ItemClassification.trap,
}


raw_item_table = [
  {
    "key": "graphics",
    "id": 100000,
    "name": "Graphics",
    "classification": "progression",
    "trap": False,
    "count": 3
  },
  {
    "key": "progressiveRoom",
    "id": 100001,
    "name": "Progressive Room",
    "classification": "progression",
    "trap": False,
    "count": 5
  },
  {
    "key": "bomb",
    "id": 100002,
    "name": "Bombs",
    "classification": "progression",
    "trap": False,
    "count": 3
  },
  {
    "key": "gun",
    "id": 100003,
    "name": "Gun",
    "classification": "progression",
    "trap": False,
    "count": 2
  },
  {
    "key": "sword",
    "id": 100004,
    "name": "Sword",
    "classification": "progression",
    "trap": False,
    "count": 3
  },
  {
    "key": "energy",
    "id": 100005,
    "name": "Energy",
    "classification": "filler",
    "trap": False,
    "count": 9
  },
  {
    "key": "hp",
    "id": 100006,
    "name": "Max HP",
    "classification": "filler",
    "trap": False,
    "count": 30
  },
  {
    "key": "rounds",
    "id": 100007,
    "name": "Max Rounds",
    "classification": "progression",
    "trap": False,
    "count": 40
  },
  {
    "key": "fire",
    "id": 100008,
    "name": "Fire",
    "classification": "progression",
    "trap": False,
    "count": 1
  },
  {
    "key": "sfx",
    "id": 100009,
    "name": "SFX",
    "classification": "progression",
    "trap": False,
    "count": 1
  },
  {
    "key": "bgm",
    "id": 100010,
    "name": "BGM",
    "classification": "progression",
    "trap": False,
    "count": 1
  },
  {
    "key": "pickaxe",
    "id": 100011,
    "name": "Pickaxe",
    "classification": "progression",
    "trap": False,
    "count": 1
  },
  {
    "key": "waterWalkers",
    "id": 100012,
    "name": "Water Walkers",
    "classification": "progression",
    "trap": False,
    "count": 1
  },
  {
    "key": "tankTreads",
    "id": 100013,
    "name": "Tank Treads",
    "classification": "progression",
    "trap": False,
    "count": 1
  },
  {
    "key": "tankChassis",
    "id": 100014,
    "name": "Tank Chassis",
    "classification": "progression",
    "trap": False,
    "count": 1
  },
  {
    "key": "tankCannon",
    "id": 100015,
    "name": "Tank Cannon",
    "classification": "progression",
    "trap": False,
    "count": 1
  },
  {
    "key": "healthPotion",
    "id": 100016,
    "name": "Health Potion",
    "classification": "filler",
    "trap": False,
    "count": 1
  },
  {
    "key": "energyGem",
    "id": 100017,
    "name": "Energy Gem",
    "classification": "filler",
    "trap": False,
    "count": 1
  },
  {
    "key": "roundPouch",
    "id": 100018,
    "name": "Round Pouch",
    "classification": "filler",
    "trap": False,
    "count": 1
  },
  {
    "key": "itemPool",
    "id": 100019,
    "name": "Item Pool",
    "classification": "filler",
    "trap": False,
    "count": 1
  },
  {
    "key": "trapStun",
    "id": 100020,
    "name": "Stun Trap",
    "classification": "trap",
    "trap": True,
    "count": 1
  },
  {
    "key": "trapInvisible",
    "id": 100021,
    "name": "Invisible Trap",
    "classification": "trap",
    "trap": True,
    "count": 1
  },
  {
    "key": "trapFast",
    "id": 100022,
    "name": "Fast Trap",
    "classification": "trap",
    "trap": True,
    "count": 1
  },
  {
    "key": "trapSlow",
    "id": 100023,
    "name": "Slow Trap",
    "classification": "trap",
    "trap": True,
    "count": 1
  },
  {
    "key": "trapReverse",
    "id": 100024,
    "name": "Reverse Trap",
    "classification": "trap",
    "trap": True,
    "count": 1
  },
  {
    "key": "trapScreenFlip",
    "id": 100025,
    "name": "Screen Flip Trap",
    "classification": "trap",
    "trap": True,
    "count": 1
  },
  {
    "key": "trapZoom",
    "id": 100026,
    "name": "Zoom Trap",
    "classification": "trap",
    "trap": True,
    "count": 1
  },
  {
    "key": "trapDeath",
    "id": 100027,
    "name": "Death Trap",
    "classification": "trap",
    "trap": True,
    "count": 1
  },
  {
    "key": "suddenlySnake",
    "id": 100028,
    "name": "Suddenly Snake",
    "classification": "trap",
    "trap": True,
    "count": 1
  }
]
item_table = {
    item['name']: {
        'id': item['id'],
        'key': item['key'],
        'classification': classification_table[item['classification']],
        'classification_name': item['classification'],
        'count': item.get('count', 1),
    } for item in raw_item_table
}

filler_item_names = [item['name'] for item in raw_item_table if item['classification'] == 'filler' and item['key'] != 'itemPool' and not item.get('trap')]
trap_item_names = [item['name'] for item in raw_item_table if item.get('trap')]
progression_item_names = [item['name'] for item in raw_item_table if item['classification'] == 'progression']
