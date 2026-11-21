from typing import List, Optional


class LocationType():
    world = 1  # Just standing there in the world
    hidden = 2  # Kill all monsters in the room to reveal, each "item room" counter tick.
    boss_reward = 3  # Kill a boss to reveal the item
    shop = 4  # Buy at a shop
    give = 5  # Given by an NPC
    spring = 6  # Activatable spring
    boss = 7  # Entity to kill to trigger the check


class ItemType():
    unknown = 0  # Or don't care
    red_potion = 1


class LocationDef:
    def __init__(self, id: Optional[int], name: str, region: str, type: int, original_item: int):
        self.id = id
        self.name = name
        self.region = region
        self.type = type
        self.original_item = original_item


locations: List[LocationDef] = [
    # Eolis
    LocationDef(400100, 'Eolis Guru', 'Eolis', LocationType.give, ItemType.unknown),
    LocationDef(400101, 'Eolis Key Jack', 'Eolis', LocationType.shop, ItemType.unknown),
    LocationDef(400102, 'Eolis Hand Dagger', 'Eolis', LocationType.shop, ItemType.unknown),
    LocationDef(400103, 'Eolis Red Potion', 'Eolis', LocationType.shop, ItemType.red_potion),
    LocationDef(400104, 'Eolis Elixir', 'Eolis', LocationType.shop, ItemType.unknown),
    LocationDef(400105, 'Eolis Deluge', 'Eolis', LocationType.shop, ItemType.unknown),

    # Path to Apolune
    LocationDef(400106, 'Path to Apolune Magic Shield', 'Path to Apolune', LocationType.shop, ItemType.unknown),
    LocationDef(400107, 'Path to Apolune Death', 'Path to Apolune', LocationType.shop, ItemType.unknown),

    # Apolune
    LocationDef(400108, 'Apolune Small Shield', 'Apolune', LocationType.shop, ItemType.unknown),
    LocationDef(400109, 'Apolune Hand Dagger', 'Apolune', LocationType.shop, ItemType.unknown),
    LocationDef(400110, 'Apolune Deluge', 'Apolune', LocationType.shop, ItemType.unknown),
    LocationDef(400111, 'Apolune Red Potion', 'Apolune', LocationType.shop, ItemType.red_potion),
    LocationDef(400112, 'Apolune Key Jack', 'Apolune', LocationType.shop, ItemType.unknown),

    # Tower of Trunk
    LocationDef(400113, 'Tower of Trunk Hidden Mattock', 'Tower of Trunk', LocationType.hidden, ItemType.unknown),
    LocationDef(400114, 'Tower of Trunk Hidden Hourglass', 'Tower of Trunk', LocationType.hidden, ItemType.unknown),
    LocationDef(400115, 'Tower of Trunk Boss Mattock', 'Tower of Trunk', LocationType.boss_reward, ItemType.unknown),

    # Path to Forepaw
    LocationDef(400116, 'Path to Forepaw Hidden Red Potion', 'Path to Forepaw', LocationType.hidden, ItemType.red_potion),
    LocationDef(400117, 'Path to Forepaw Glove', 'Path to Forepaw', LocationType.world, ItemType.unknown),

    # Forepaw
    LocationDef(400118, 'Forepaw Long Sword', 'Forepaw', LocationType.shop, ItemType.unknown),
    LocationDef(400119, 'Forepaw Studded Mail', 'Forepaw', LocationType.shop, ItemType.unknown),
    LocationDef(400120, 'Forepaw Small Shield', 'Forepaw', LocationType.shop, ItemType.unknown),
    LocationDef(400121, 'Forepaw Red Potion', 'Forepaw', LocationType.shop, ItemType.red_potion),
    LocationDef(400122, 'Forepaw Wingboots', 'Forepaw', LocationType.shop, ItemType.unknown),
    LocationDef(400123, 'Forepaw Key Jack', 'Forepaw', LocationType.shop, ItemType.unknown),
    LocationDef(400124, 'Forepaw Key Queen', 'Forepaw', LocationType.shop, ItemType.unknown),

    # Trunk
    LocationDef(400125, 'Trunk Hidden Ointment', 'Trunk', LocationType.hidden, ItemType.unknown),
    LocationDef(400126, 'Trunk Hidden Red Potion', 'Trunk', LocationType.hidden, ItemType.red_potion),
    LocationDef(400127, 'Trunk Red Potion', 'Trunk', LocationType.world, ItemType.red_potion),
    LocationDef(None, 'Sky Spring', 'Trunk', LocationType.spring, ItemType.unknown),

    # Joker Spring
    LocationDef(400128, 'Joker Spring Ruby Ring', 'Joker Spring', LocationType.give, ItemType.unknown),
    LocationDef(None, 'Joker Spring', 'Joker Spring', LocationType.spring, ItemType.unknown),

    # Tower of Fortress
    LocationDef(400129, 'Tower of Fortress Poison 1', 'Tower of Fortress', LocationType.world, ItemType.unknown),
    LocationDef(400130, 'Tower of Fortress Poison 2', 'Tower of Fortress', LocationType.world, ItemType.unknown),
    LocationDef(400131, 'Tower of Fortress Hidden Wingboots', 'Tower of Fortress', LocationType.world, ItemType.unknown),
    LocationDef(400132, 'Tower of Fortress Ointment', 'Tower of Fortress', LocationType.world, ItemType.unknown),
    LocationDef(400133, 'Tower of Fortress Boss Wingboots', 'Tower of Fortress', LocationType.boss_reward, ItemType.unknown),
    LocationDef(400134, 'Tower of Fortress Elixir', 'Tower of Fortress', LocationType.world, ItemType.unknown),
    LocationDef(400135, 'Tower of Fortress Guru', 'Tower of Fortress', LocationType.give, ItemType.unknown),
    LocationDef(None, 'Tower of Fortress Spring', 'Tower of Fortress', LocationType.spring, ItemType.unknown),

    # Path to Mascon
    LocationDef(400136, 'Path to Mascon Hidden Wingboots', 'Path to Mascon', LocationType.hidden, ItemType.unknown),

    # Tower of Red Potion
    LocationDef(400137, 'Tower of Red Potion', 'Tower of Red Potion', LocationType.world, ItemType.red_potion),

    # Mascon
    LocationDef(400138, 'Mascon Large Shield', 'Mascon', LocationType.shop, ItemType.unknown),
    LocationDef(400139, 'Mascon Thunder', 'Mascon', LocationType.shop, ItemType.unknown),
    LocationDef(400140, 'Mascon Mattock', 'Mascon', LocationType.shop, ItemType.unknown),
    LocationDef(400141, 'Mascon Red Potion', 'Mascon', LocationType.shop, ItemType.red_potion),
    LocationDef(400142, 'Mascon Key Jack', 'Mascon', LocationType.shop, ItemType.unknown),
    LocationDef(400143, 'Mascon Key Queen', 'Mascon', LocationType.shop, ItemType.unknown),

    # Path to Victim
    LocationDef(400144, 'Misty Shop Death', 'Path to Victim', LocationType.shop, ItemType.unknown),
    LocationDef(400145, 'Misty Shop Hourglass', 'Path to Victim', LocationType.shop, ItemType.unknown),
    LocationDef(400146, 'Misty Shop Elixir', 'Path to Victim', LocationType.shop, ItemType.unknown),
    LocationDef(400147, 'Misty Shop Red Potion', 'Path to Victim', LocationType.shop, ItemType.red_potion),
    LocationDef(400148, 'Misty Doctor Office', 'Path to Victim', LocationType.hidden, ItemType.unknown),

    # Tower of Suffer
    LocationDef(400149, 'Tower of Suffer Hidden Wingboots', 'Tower of Suffer', LocationType.hidden, ItemType.unknown),
    LocationDef(400150, 'Tower of Suffer Hidden Hourglass', 'Tower of Suffer', LocationType.hidden, ItemType.unknown),
    LocationDef(400151, 'Tower of Suffer Pendant', 'Tower of Suffer', LocationType.boss_reward, ItemType.unknown),

    # Victim
    LocationDef(400152, 'Victim Full Plate', 'Victim', LocationType.shop, ItemType.unknown),
    LocationDef(400153, 'Victim Mattock', 'Victim', LocationType.shop, ItemType.unknown),
    LocationDef(400154, 'Victim Red Potion', 'Victim', LocationType.shop, ItemType.red_potion),
    LocationDef(400155, 'Victim Key King', 'Victim', LocationType.shop, ItemType.unknown),
    LocationDef(400156, 'Victim Key Queen', 'Victim', LocationType.shop, ItemType.unknown),
    LocationDef(400157, 'Victim Tavern', 'Mist', LocationType.give, ItemType.unknown),

    # Mist
    LocationDef(400158, 'Mist Hidden Poison 1', 'Mist', LocationType.hidden, ItemType.unknown),
    LocationDef(400159, 'Mist Hidden Poison 2', 'Mist', LocationType.hidden, ItemType.unknown),
    LocationDef(400160, 'Mist Hidden Wingboots', 'Mist', LocationType.hidden, ItemType.unknown),
    LocationDef(400161, 'Misty Magic Hall', 'Mist', LocationType.give, ItemType.unknown),
    LocationDef(400162, 'Misty House', 'Mist', LocationType.give, ItemType.unknown),

    # Useless Tower
    LocationDef(400163, 'Useless Tower', 'Useless Tower', LocationType.hidden, ItemType.unknown),

    # Tower of Mist
    LocationDef(400164, 'Tower of Mist Hidden Ointment', 'Tower of Mist', LocationType.hidden, ItemType.unknown),
    LocationDef(400165, 'Tower of Mist Elixir', 'Tower of Mist', LocationType.world, ItemType.unknown),
    LocationDef(400166, 'Tower of Mist Black Onyx', 'Tower of Mist', LocationType.boss_reward, ItemType.unknown),

    # Path to Conflate
    LocationDef(400167, 'Path to Conflate Hidden Ointment', 'Path to Conflate', LocationType.hidden, ItemType.unknown),
    LocationDef(400168, 'Path to Conflate Poison', 'Path to Conflate', LocationType.hidden, ItemType.unknown),

    # Helm Branch
    LocationDef(400169, 'Helm Branch Hidden Glove', 'Helm Branch', LocationType.hidden, ItemType.unknown),
    LocationDef(400170, 'Helm Branch Battle Helmet', 'Helm Branch', LocationType.boss_reward, ItemType.unknown),

    # Conflate
    LocationDef(400171, 'Conflate Giant Blade', 'Conflate', LocationType.shop, ItemType.unknown),
    LocationDef(400172, 'Conflate Magic Shield', 'Conflate', LocationType.shop, ItemType.unknown),
    LocationDef(400173, 'Conflate Wingboots', 'Conflate', LocationType.shop, ItemType.unknown),
    LocationDef(400174, 'Conflate Red Potion', 'Conflate', LocationType.shop, ItemType.red_potion),
    LocationDef(400175, 'Conflate Guru', 'Conflate', LocationType.give, ItemType.unknown),

    # Branches
    LocationDef(400176, 'Branches Hidden Ointment', 'Branches', LocationType.hidden, ItemType.unknown),
    LocationDef(400177, 'Branches Poison', 'Branches', LocationType.world, ItemType.unknown),
    LocationDef(400178, 'Branches Hidden Mattock', 'Branches', LocationType.hidden, ItemType.unknown),
    LocationDef(400179, 'Branches Hidden Hourglass', 'Branches', LocationType.hidden, ItemType.unknown),

    # Path to Daybreak
    LocationDef(400180, 'Path to Daybreak Hidden Wingboots 1', 'Path to Daybreak', LocationType.hidden, ItemType.unknown),
    LocationDef(400181, 'Path to Daybreak Magical Rod', 'Path to Daybreak', LocationType.world, ItemType.unknown),
    LocationDef(400182, 'Path to Daybreak Hidden Wingboots 2', 'Path to Daybreak', LocationType.hidden, ItemType.unknown),
    LocationDef(400183, 'Path to Daybreak Poison', 'Path to Daybreak', LocationType.world, ItemType.unknown),
    LocationDef(400184, 'Path to Daybreak Glove', 'Path to Daybreak', LocationType.world, ItemType.unknown),
    LocationDef(400185, 'Path to Daybreak Battle Suit', 'Path to Daybreak', LocationType.boss_reward, ItemType.unknown),

    # Daybreak
    LocationDef(400186, 'Daybreak Tilte', 'Daybreak', LocationType.shop, ItemType.unknown),
    LocationDef(400187, 'Daybreak Giant Blade', 'Daybreak', LocationType.shop, ItemType.unknown),
    LocationDef(400188, 'Daybreak Red Potion', 'Daybreak', LocationType.shop, ItemType.red_potion),
    LocationDef(400189, 'Daybreak Key King', 'Daybreak', LocationType.shop, ItemType.unknown),
    LocationDef(400190, 'Daybreak Key Queen', 'Daybreak', LocationType.shop, ItemType.unknown),

    # Dartmoor Castle
    LocationDef(400191, 'Dartmoor Castle Hidden Hourglass', 'Dartmoor Castle', LocationType.hidden, ItemType.unknown),
    LocationDef(400192, 'Dartmoor Castle Hidden Red Potion', 'Dartmoor Castle', LocationType.hidden, ItemType.red_potion),

    # Dartmoor
    LocationDef(400193, 'Dartmoor Giant Blade', 'Dartmoor', LocationType.shop, ItemType.unknown),
    LocationDef(400194, 'Dartmoor Red Potion', 'Dartmoor', LocationType.shop, ItemType.red_potion),
    LocationDef(400195, 'Dartmoor Key King', 'Dartmoor', LocationType.shop, ItemType.unknown),

    # Fraternal Castle
    LocationDef(400196, 'Fraternal Castle Hidden Ointment', 'Fraternal Castle', LocationType.hidden, ItemType.unknown),
    LocationDef(400197, 'Fraternal Castle Shop Hidden Ointment', 'Fraternal Castle', LocationType.hidden, ItemType.unknown),
    LocationDef(400198, 'Fraternal Castle Poison 1', 'Fraternal Castle', LocationType.world, ItemType.unknown),
    LocationDef(400199, 'Fraternal Castle Poison 2', 'Fraternal Castle', LocationType.world, ItemType.unknown),
    LocationDef(400200, 'Fraternal Castle Poison 3', 'Fraternal Castle', LocationType.world, ItemType.unknown),
    # LocationDef(400201, 'Fraternal Castle Red Potion', 'Fraternal Castle', LocationType.world, ItemType.red_potion),  # This location is inaccessible. Keeping commented for context.
    LocationDef(400202, 'Fraternal Castle Hidden Hourglass', 'Fraternal Castle', LocationType.hidden, ItemType.unknown),
    LocationDef(400203, 'Fraternal Castle Dragon Slayer', 'Fraternal Castle', LocationType.boss_reward, ItemType.unknown),
    LocationDef(400204, 'Fraternal Castle Guru', 'Fraternal Castle', LocationType.give, ItemType.unknown),

    # Evil Fortress
    LocationDef(400205, 'Evil Fortress Ointment', 'Evil Fortress', LocationType.world, ItemType.unknown),
    LocationDef(400206, 'Evil Fortress Poison 1', 'Evil Fortress', LocationType.world, ItemType.unknown),
    LocationDef(400207, 'Evil Fortress Glove', 'Evil Fortress', LocationType.world, ItemType.unknown),
    LocationDef(400208, 'Evil Fortress Poison 2', 'Evil Fortress', LocationType.world, ItemType.unknown),
    LocationDef(400209, 'Evil Fortress Poison 3', 'Evil Fortress', LocationType.world, ItemType.unknown),
    LocationDef(400210, 'Evil Fortress Hidden Glove', 'Evil Fortress', LocationType.hidden, ItemType.unknown),
    LocationDef(None, 'Evil One', 'Evil Fortress', LocationType.boss, ItemType.unknown),
]
