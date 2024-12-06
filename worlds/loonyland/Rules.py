class LoonylandRules:

    access_rules = {
        "Halloween Hill - Swamp Mud Path": lambda state: state.has("Boots", player),
        "Halloween Hill - Bog Beast Home": lambda state: true,
        "Halloween Hill - Rocky Cliffs below Upper Caverns": lambda state: CanEnterRockyCliffs(state, player)),
        "Halloween Hill - Sapling Shrine": lambda state: state.has("Boots", player),
        "Halloween Hill - Terror Glade": lambda state: true),
        "Halloween Hill - Rocky Cliffs Vine": lambda state: state.has("Fertilizer", player),
        "Halloween Hill - Rocky Cliffs Grand Pharoh": lambda state: CanEnterRockyCliffs(state, player),
        "Halloween Hill - Rocky Cliffs Rock Corner": lambda state: CanEnterRockyCliffs(state, player) and HaveBombs(state, player),
        "Halloween Hill - Mushroom outside town": lambda state: true,
        "Halloween Hill - North of UG Passage": lambda state: true,
        "Halloween Hill - Top left mushroom spot": lambda state: true,
        "Halloween Hill - NE of UG Passage": lambda state: true,
        "Halloween Hill - East Woods": lambda state: true,
        "Halloween Hill - Rocky Cliffs Ledge": lambda state: CanEnterRockyCliffs(state, player),
        "Halloween Hill - Rocky Cliffs Peak": lambda state: CanEnterRockyCliffs(state, player),
        "Halloween Hill - Cat Tree": lambda state: true,
        "The Witch's Cabin - Bedroom": lambda state: HaveLightSource(state, player),
        "The Witch's Cabin - Backroom": lambda state: true,
        "Bonita's Cabin - Barrel Maze": lambda state: true,
        "The Bog Pit - Top Door": lambda state: state.has("Skull Key", player),
        "The Bog Pit - Post Room": lambda state: true,
        "The Bog Pit - Window Drip": lambda state: true,
        "The Bog Pit - Green room": lambda state: true,
        "The Bog Pit - Arena": lambda state: true,
        "The Bog Pit - Kill Wall": lambda state: true,
        "Underground Tunnel - Swampdog Door": lambda state: state.has("Pumpkin Key", player),
        "Underground Tunnel - Scribble Wall": lambda state: HaveSpecialWeaponBullet(state, player),
        "Underground Tunnel - Tiny Passage": lambda state: true,
        "Underground Tunnel - fire frogs": lambda state: true,
        "Underground Tunnel - Torch Island": lambda state: state.has("Boots", player),
        "Underground Tunnel - Small Room": lambda state: true,
        "Swamp Gas Cavern - Scratch Wall": lambda state: state.has("Boots", player) and HaveSpecialWeaponBullet)state, player),
        "Swamp Gas Cavern - Bat Mound": lambda state: state.has("Boots", player) and state.has("Bat Key", player),
        "Swamp Gas Cavern - Stair room": lambda state: state.has("Boots", player),
        "Swamp Gas Cavern - Rock Prison": lambda state: state.has("Boots", player) and HaveBombs(state, player),
        "A Tiny Cabin - Tiny Cabin": lambda state: state.has("Skull Key", player),
        "A Cabin - Bedside ": lambda state: CanEnterZombiton(state, player),
        "Dusty Crypt - Pumpkin Door": lambda state: HaveLightSource(state, player) and state.has("Pumpkin Key", player),
        "Dusty Crypt - Maze": lambda state: HaveLightSource(state, player),
        "Musty Crypt - Big Closed Room": lambda state: HaveLightSource(state, player) and  CanEnterZombiton(state, player) and HaveSpecialWeaponBullet(state, player)
        "Rusty Crypt - Spike Vine": lambda state: HaveLightSource(state, player) and state.has("Fertilizer", player),
        "Rusty Crypt - Boulders": lambda state: HaveLightSource(state, player),
        "A Messy Cabin - Barrel Mess": lambda state: CanEnterZombiton(state, player),
        "Under the Lake - Lightning Rod Secret": lambda state: HaveLightSource(state, player) and HaveAllOrbs(state, player),
        "Under the Lake - Bat Door": lambda state: HaveLightSource(state, player) and HaveAllOrbs(state, player) and state.has("Bat Key", player),
        "Deeper Under the Lake - SE corner": lambda state: HaveLightSource(state, player) and HaveAllOrbs(state, player),
        "Deeper Under the Lake - Rhombus": lambda state: HaveLightSource(state, player) and HaveAllOrbs(state, player),
        "Frankenjulie's Laboratory - Boss Reward": lambda state: HaveLightSource(state, player) and HaveAllOrbs(state, player),
        "Haunted Tower - Barracks": lambda state: state.has("Ghost Potion", player) and state.has("Bat Key", player),
        "Haunted Tower, Floor 2 - Top Left": lambda state: state.has("Ghost Potion", player),
        "Haunted Tower Roof - Boss Reward": lambda state: state.has("Ghost Potion", player),
        "Haunted Basement - DoorDoorDoorDoorDoorDoor": lambda state: state.has("Ghost Potion", player) and HaveLightSource(state, player) and state.has("Bat Key", player) and state.has("Skull Key", player) and state.has("Pumpkin Key", player),
        "Abandoned Mines - Shaft": lambda state: HaveLightSource(state, player) and CanEnterRockyCliffs(state, player),
        "The Shrine of Bombulus - Bombulus": lambda state: CanEnterRockyCliffs(state, player),
        "A Gloomy Cavern - Lockpick": lambda state: HaveLightSource(state, player) and CanEnterRockyCliffs(state, player),
        "Happy Stick Woods - Happy Stick Hidden": lambda state: state.has("Talisman", player),
        "Happy Stick Woods - Happy Stick Reward": lambda state: state.has("Talisman", player),
        "The Wolf Den - Wolf Top Left": lambda state: HaveLightSource(state, player) and state.has("Silver Sling", player),
        "The Wolf Den - Pumpkin Door": lambda state: HaveLightSource(state, player) and state.has("Silver Sling", player) and state.has("Pumpkin Key", player),
        "The Wolf Den - Grow Room": lambda state: HaveLightSource(state, player) and state.has("Silver Sling", player) and state.has("Fertilizer", player),
        "Upper Creepy Cavern - The Three ombres": lambda state: HaveLightSource(state, player) and CanEnterRockyCliffs(state, player),
        "Under the Ravine - Left Vine": lambda state: HaveLightSource(state, player) and CanEnterRockyCliffs(state, player) and state.has("Fertilizer", player),
        "Under the Ravine - Right Vine": lambda state: HaveLightSource(state, player) and CanEnterRockyCliffs(state, player) and state.has("Fertilizer", player),
        "Creepy Caverns - M Pharoh bat Room": lambda state: HaveLightSource(state, player) and CanEnterRockyCliffs(state, player) and state.has("Bat Key", player),
        "Creepy Caverns - E 2 blue Pharos": lambda state: HaveLightSource(state, player) and CanEnterRockyCliffs(state, player),
        "Creepy Caverns - M GARGOYLE ROOM": lambda state: HaveLightSource(state, player) and CanEnterRockyCliffs(state, player),
        "Castle Vampy - Vampire Guard": lambda state: CanEnterVampy(state, player),
        "Castle Vampy - maze top left": lambda state: CanEnterVampy(state, player),
        "Castle Vampy - Top Right Gauntlet": lambda state: CanEnterVampy(state, player),
        "Castle Vampy - Bat Closet": lambda state: CanEnterVampy(state, player),
        "Castle Vampy II - Candle Room": lambda state: CanEnterVampyII(state, player),
        "Castle Vampy II - Top Right Top": lambda state: CanEnterVampyII(state, player),
        "Castle Vampy II - Bottom Right Middle": lambda state: CanEnterVampyII(state, player),
        "Castle Vampy II - Bat room": lambda state: CanEnterVampyII(state, player) and HaveSpecialWeaponBullet(state, player),
        "Cabin in the woods - Gold Skull": lambda state: true,
        "Castle Vampy III - Middle": lambda state: CanEnterVampyIII(state, player),
        "Castle Vampy III - Behind the Pews": lambda state: CanEnterVampyIII(state, player),
        "Castle Vampy III - AMBUSH!": lambda state: CanEnterVampyIII(state, player),
        "Castle Vampy III - Halloween": lambda state: CanEnterVampyIII(state, player),
        "Castle Vampy III - So many bats": lambda state: CanEnterVampyIII(state, player),
        "Castle Vampy IV - Right Path": lambda state: CanEnterVampyIV(state, player),
        "Castle Vampy IV - Left Path": lambda state: CanEnterVampyIV(state, player),
        "Castle Vampy IV - Ballroom Right": lambda state: CanEnterVampyIV(state, player) and state.has("Ghost Potion", player) and state.has("Silver Sling", player),
        "Castle Vampy IV - Right Secret Wall": lambda state: CanEnterVampyIV(state, player),
        "Castle Vampy IV - Ballroom Left": lambda state: CanEnterVampyIV(state, player) and state.has("Ghost Potion", player) and state.has("Silver Sling", player),
        "Castle Vampy Roof - Gutsy the Elder": lambda state: CanEnterVampy(state, player) and HaveAllBats(state, player) and HaveSpecialWeaponDamage(state, player),
        "Castle Vampy Roof - Stoney the Elder": lambda state: CanEnterVampy(state, player) and HaveAllBats(state, player),
        "Castle Vampy Roof - Drippy the Elder": lambda state: CanEnterVampy(state, player) and HaveAllBats(state, player)),
        "Castle Vampy Roof - Toasty the Elder": lambda state: CanEnterVampy(state, player) and HaveAllBats(state, player),
        "Heart of Terror - Bonkula": lambda state: CanEnterVampyIV(state, player) and HaveAllVamps(state, player),
        "A Hidey Hole - Bat Door": lambda state: state.has("Bat Key", player),
        "A Hidey Hole - Pebbles": lambda state: true,
        "Swampdog Lair - Entrance": lambda state: state.has("Boots", player),
        "Swampdog Lair - End": lambda state: state.has("Boots", player) and HaveLightSource(state, player) and state.has("Fertilizer", player),
        "The Witch's Cabin - Ghostbusting": lambda state: state.has("Big Gem", player) and state.has("Daisy", player) and HaveAllMushrooms(state, player),
        "A Cabin3 - Hairy Larry": lambda state: HaveLightSource(state, player) and state.has("Silver Sling", player) and state.has("Boots", player) ,
        "Halloween Hill - Scaredy Cat": lambda state: state.has("Cat", player),
        "Halloween Hill - Silver Bullet": lambda state: state.has("Silver", player) and CanCleanseCrypts(state, player),
        "Halloween Hill - Smashing Pumpkins": lambda state: CanCleanseCrypts(state, player),
        "Halloween Hill - Sticky Shoes": lambda state: true
        "A Cabin4 - The Collection": lambda state: state.has("Silver Sling", player) and state.has("Ghost Potion", player) and CanEnterVampy(state, player),
        "A Gloomy Cavern - The Rescue": lambda state: HaveLightSource(state, player) and CanEnterRockyCliffs(state, player),
        "A Cabin - Tree Trimming": lambda state: true,
        "The Witch's Cabin - Witch Mushrooms": lambda state: HaveAllMushrooms(state, player),
        "Halloween Hill - Zombie Stomp": lambda state: CanCleanseCrypts(state, player)
        }
        
        
def  HaveLightSource(state: CollectionState, player: int)
{
	return (state.has("Lantern", player) or (state.has("Stick", player) and state.has("Boots", player)))
}

def HaveBombs(state: CollectionState, player: int)
{
	return state.has("Bombs", player)
    #or werewolf badge when badges are added
}

def HaveAnyBigGem(state: CollectionState, player: int)
{
	return state.has("Big Gem", player)
}

def HaveAllOrbs(state: CollectionState, player: int)
{
	return (state.count("Orb", player) >= 4)
}

def HaveAllBats(state: CollectionState, player: int)
{
	return (state.count("Bat Statue", player) >= 4)
}

def HaveAllVamps(state: CollectionState, player: int)
{
	return (state.count("Vampire Statue", player) >= 8)
}

def HaveSpecialWeaponDamage(state: CollectionState, player: int)
{
	return (
            state.has("Bombs", player) or
            state.has("Shock Wand", player) or
            #state.has("Ice Spear")  ice doesn't hurt elder
            state.has("Cactus", player) or
            state.has("Boomerang", player) or
            state.has("Whoopee", player) or
            state.has("Hot Pants", player)
    )
}

def HaveSpecialWeaponBullet(state: CollectionState, player: int)
{
    return (
            state.has("Bombs", player) or
            #state.has("Shock Wand") or shock wand isn't bullet
            state.has("Ice Spear", player) or
            state.has("Cactus", player) or
            state.has("Boomerang", player) or
            state.has("Whoopee", player) or
            state.has("Hot Pants", player)
    )
	#return true slingshot counts
	
}

def HaveSpecialWeaponRangeDamage(state: CollectionState, player: int)
{
    return (
            state.has("Bombs", player) or
            state.has("Shock Wand", player) or 
            #state.has("Ice Spear") or Ice spear no damage
            state.has("Cactus", player) or
            state.has("Boomerang", player) or
            #state.has("Whoopee") or whopee not ranged
            #state.has("Hot Pants") hot pants not ranged
    )
    #return true slingshot counts
}

def HaveSpecialWeaponThroughWalls(state: CollectionState, player: int)
{
    return (
            state.has("Bombs", player) or
            state.has("Shock Wand", player) or 
            #state.has("Ice Spear") or Ice spear no damage
            #state.has("Cactus") or
            #state.has("Boomerang") or
            state.has("Whoopee", player)
            #state.has("Hot Pants") 
            )
    )
}

def HaveAllMushrooms(state: CollectionState, player: int)
{
	return state.count("Mushroom", player) >= 10
}

def CanCleanseCrypts(state: CollectionState, player: int)
{
	return (HaveLightSource(state, player) and CanEnterZombiton(state, player) and HaveSpecialWeaponRangeDamage(state, player))
}

#these will get removed in favor of region access reqs eventually
def CanEnterZombiton(state: CollectionState, player: int)
{
	return state.has("Boots", player)
}

def CanEnterRockyCliffs(state: CollectionState, player: int)
{
	return HaveAnyBigGem(state, player)
}

def CanEnterVampy(state: CollectionState, player: int)
{
	return CanEnterRockyCliffs(state, player) and HaveLightSource(state, player)
}

def CanEnterVampyII(state: CollectionState, player: int)
{
	return CanEnterVampy(state, player) && state.has("Skull Key", player)
}

def CanEnterVampyIII(state: CollectionState, player: int)
{
	return CanEnterVampyII(state, player) && state.has("Bat Key", player)
}

def CanEnterVampyIV(state: CollectionState, player: int)
{
	return CanEnterVampyIII(inv) && state.has("Pumpkin Key", player)
}
        
def CanEnterRockyCliffs(state: CollectionState, player: int)
{
    return state.has("Big Gem", player)
}