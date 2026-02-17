from __future__ import annotations

from typing import TYPE_CHECKING

from . import logic_handling

if TYPE_CHECKING:
    from .world import TVRUHHWorld




def get_location_names_with_ids(location_names: list[str], chosen_list) -> dict[str, int | None]:
    return {location_name: chosen_list[location_name][0] for location_name in location_names}

def create_all_locations(world: TVRUHHWorld) -> None:
    create_regular_locations(world)
    create_events(world)
    # world.location_name_to_id.update(big_bad_list_of_all_locations_with_IDs)




big_bad_list_of_all_locations_with_IDs = {
    "Dream: Love at First Shot": 1000000
}

locations_to_tags = {

}

extra_location_list = {

}

def create_regular_locations(world: TVRUHHWorld) -> None:
    #get regions
    start_dreams = world.get_region("Start")
    quickplay_dreams = world.get_region("Unlocked Quickplay")
    
    #locations in start region
    logic_handling.logic_placer(world,load_location_list(world,dream_list),"dreams")
    logic_handling.logic_placer(world,load_location_list(world,qp_copper),"qp_medal")


def create_extra_locations(world: TVRUHHWorld, amount: int) -> None:
    bonus_locations = world.get_region("Start")
    bonus_locations.add_locations(get_location_names_with_ids(load_extra_locations(amount),extra_location_list))

def load_location_list(world,parentlist: dict,min_id = -1, max_id = -1) -> dict[str, int | None]:
    names = []
    for x in parentlist:
        if not min_id == -1:
            if parentlist[x][0] >= min_id and parentlist[x][0] <= max_id:
                if not world.options.disabled_dreams.__contains__(x.replace("Dream: ","")):
                    names.append(x)
        else:
            if not world.options.disabled_dreams.__contains__(x.replace("Dream: ","")):
                names.append(x)
    names = logic_handling.logic_remover(world, names)
    locations = get_location_names_with_ids(names,parentlist)
    return locations

def load_extra_locations(amount: int) -> dict[str, int | None]:
    a: int = 1
    l = []
    while a <= amount: 
        x = "Bonus Gift " + ((a).__str__())
        l.append(x)
        a += 1
    return l

def create_events(world: TVRUHHWorld) -> None:
    pass

def requestbbl() -> dict[str:int]: 
    # normal locations
    updatebbl(dream_list)
    updatebbl(qp_copper)
    
    # bonus locations
    a: int = 1
    while a <= 1000: 
        x = "Bonus Gift " + ((a).__str__())
        big_bad_list_of_all_locations_with_IDs.update({str(x): int(1450000 + (a-1))})
        extra_location_list.update({str(x): [int(1450000 + (a-1))]})
        a += 1
    
    return big_bad_list_of_all_locations_with_IDs

def updatebbl(whichlist) -> None:
    for x in whichlist:
        big_bad_list_of_all_locations_with_IDs.update({x: whichlist[x][0]})
        locations_to_tags.update({x: whichlist[x][1]})




# First three numbers indicate what type location it is
# Last four numbers is the count
# 100 = dreams (status: currently being worked on)
# 101 = story medals (status: WIP)
# 102 = quickplay copper medals (status: WIP)
# 103 = quickplay bronze medals (status: WIP)
# 104 = quickplay silver medals (status: WIP)
# 105 = quickplay gold medals (status: WIP)
# 106 = quickplay radiant medals (status: WIP)
# 107 = uqp radiant 1 (status: WIP)
# 108 = uqp radiant 2 (status: WIP)
# 109 = uqp radiant 3 (status: WIP)
# 110 = altstory copper medals (status: WIP)
# 111 = altstory bronze medals (status: WIP)
# 112 = altstory silver medals (status: WIP)
# 113 = altstory gold medals (status: WIP)
# 114 = altstory radiant medals (status: WIP)
# 115 = altstory rose medals (status: WIP)
# 116 = altstory crimson medals (status: WIP)
# 117 = towers copper medals (status: WIP)
# 118 = towers bronze medals (status: WIP)
# 119 = towers silver medals (status: WIP)
# 120 = towers gold medals (status: WIP)
# 121 = towers radiant medals (status: WIP)
# 122 = endless stress copper medals (status: WIP)
# 123 = endless stress bronze medals (status: WIP)
# 124 = endless stress silver medals (status: WIP)
# 125 = endless stress gold medals (status: WIP)
# 126 = endless stress radiant medals (status: WIP)
# 127 = endless terror copper medals (status: WIP)
# 128 = endless terror bronze medals (status: WIP)
# 129 = endless terror silver medals (status: WIP)
# 130 = endless terror gold medals (status: WIP)
# 131 = endless terror radiant medals (status: WIP)
# 132 = sublime medals uqp (status: WIP)
# 133 = sublime medals alt story (status: WIP)
# 134 = sublime medals towers (status: WIP)
# 135 = sublime medals endless (status: WIP)
# 136 = qp upgrades (status: WIP)
# 137 = altstory upgrades (status: WIP)
# 138 = endless upgrades (status: WIP)
# 139 = event upgrades (status: WIP)
# 140 = other locations (status: unknown, has any misc. location)

# every list is ordered in sublists that corrospont to the regions
# many regions do not exist in some lists, because they are just tied to a specific gamemode (or something else)
# anything that is not contained in a sublist will have location-based rules in rules.py

dream_list = {
    "Dream: Love at First Shot" : [1000000, []],
    "Dream: Monster Admirer" : [1000001, []],
    "Dream: Monster Hugger" : [1000002, []],
    "Dream: Monster Lover" : [1000003, []],
    "Dream: Nightmarephile" : [1000004, ["grind"]],
    "Dream: Teramonstrophile" : [1000005, ["grind"]],
    "Dream: Weapon of Mass Affection" : [1000006, ["very_grind"]],
    "Dream: Lovepocalypse" : [1000007, ["very_grind"]],
    "Dream: Let Me Love You!" : [1000008, []],
    "Dream: Let Yourself Be Loved!" : [1000009, []],
    "Dream: Violence in the Name of Love!" : [1000010, ["grind"]],
    "Dream: To Shreds, You Say?" : [1000011, ["grind"]],
    "Dream: Love You to Pieces!" : [1000012, ["very_grind"]],
    "Dream: Monster Fear Genophiler" : [1000013, ["very_grind"]],
    "Dream: Ten Thousand Shots in the Air" : [1000014, []],
    "Dream: The Rain Will Love Us All" : [1000015, []],   
    "Dream: Love Is a Battlefield" : [1000016, ["grind"]],
    "Dream: Pour Your Misery Down on Me" : [1000017, ["very_grind"]],
    "Dream: Clearing Out the Fear" : [1000018, []],
    "Dream: Sweating Bullets" : [1000019, ["grind"]],
    "Dream: Shambled Paradox" : [1000020, []],
    "Dream: Trypophobia" : [1000021, ["grind"]],
    "Dream: Her Adamant Will" : [1000022, []],
    "Dream: Guardian Angel" : [1000023, ["grind"]],
    "Dream: Mutual Exclusion" : [1000024, []],
    "Dream: Theoretically Beautiful" : [1000025, ["grind"]],
    "Dream: Defense Mechanism" : [1000026, []],
    "Dream: Towering Anxiety" : [1000027, ["grind"]],
    "Dream: My Heart Is See Through" : [1000028, []],
    "Dream: Stained Glass Battle Dance" : [1000029, ["grind"]],
    "Dream: The Void Rains Down Upon You" : [1000030, []],
    "Dream: Alone in the Dark" : [1000031, ["grind"]],
    "Dream: Fever Dream" : [1000032, []],
    "Dream: Gathering Hearts" : [1000033, []],
    "Dream: Making Friends" : [1000034, []],
    "Dream: Monster Party" : [1000035, []],
    "Dream: Monster Ball" : [1000036, []],
    "Dream: Monster Festival" : [1000037, []],
    "Dream: Friendship Army" : [1000038, []],
    "Dream: Legion of Love" : [1000039, []],
    "Dream: Star Allies in the Void" : [1000040, []],
    "Dream: The Friends We Made Along the Way" : [1000041, []],
    "Dream: Gotta Love Em All!" : [1000042, []],
    "Dream: Full Combo!" : [1000043, []],
    "Dream: Affection Sevenfold" : [1000044, []],
    "Dream: The Ace of Hearts" : [1000045, []],
    "Dream: Love Is The Answer" : [1000046, []],
    "Dream: Heart Shaped Box" : [1000047, ["tedious"]],
    "Dream: The Mighty Ninety-Nine" : [1000048, ["tedious"]],
    "Dream: Expert Level Affection" : [1000049, []],
    "Dream: Good Score" : [1000050, []],
    "Dream: Great Score" : [1000051, []],
    "Dream: Lovely Score" : [1000052, []],
    "Dream: Wonderful Score" : [1000053, ["tedious"]],
    "Dream: Radiant Score" : [1000054, ["tedious"]],
    "Dream: BFF" : [1000055, []], #Easy if quickplay is available, overwise very_grind
    "Dream: Panic Attack!" : [1000056, []],
    "Dream: No Need to Panic" : [1000057, ["tedious"]],
    "Dream: Indestructible Master of Love" : [1000058, ["very_tedious"]], #Items like Self-Portrait and Denial are absolutely needed to survive this
    "Dream: Tsundere" : [1000059, ["tedious"]],
    "Dream: Tetrahedron of Shame" : [1000060, ["grind"]],
    "Dream: Tetrahedron of Frustration" : [1000061, ["grind"]],
    "Dream: Tetrahedron of Denial" : [1000062, ["grind"]],
    "Dream: Tetrahedron of Anxiety" : [1000063, ["grind"]],
    "Dream: Tetrahedron of Insecurity" : [1000064, ["grind"]],
    "Dream: Tetrahedron of Loneliness" : [1000065, ["grind"]],
    "Dream: Tetrahedron of Power" : [1000066, ["grind"]],
    "Dream: Collection of Triangles" : [1000067, []],
    "Dream: 200 Tetrahedrons!" : [1000068, ["grind"]],
    "Dream: 400 Tetrahedrons!" : [1000069, ["grind"]],
    "Dream: 600 Tetrahedrons!" : [1000070, ["grind"]],
    "Dream: 900 Tetrahedrons!" : [1000071, ["very_grind"]],
    "Dream: 1,200 Tetrahedrons!" : [1000072, ["very_grind"]],
    "Dream: Crystallized Dyophobia" : [1000073, ["very_grind"]],
    "Dream: Crystallized Triskaphobia" : [1000074, ["very_grind"]],
    "Dream: Crystallized Tetraphobia" : [1000075, ["very_grind"]],
    "Dream: Shiny Monster Cards" : [1000076, []],
    "Dream: Glowing Starter Pack" : [1000077, []],
    "Dream: Lovely Deck of Monsters" : [1000078, []],
    "Dream: Wonderful Deck of Monsters" : [1000079, []],
    "Dream: Radiant Deck of Monsters" : [1000080, []],
    "Dream: Radiant Legion of Love" : [1000081, []],
    "Dream: 99 Shiny Hearts Floating in the Rainy Sky" : [1000082, []],
    "Dream: Eleven Level Elevens" : [1000083, []],
    "Dream: Waking The Fallen Hearts" : [1000084, []],
    "Dream: Rare Monster Cards" : [1000085, []],
    "Dream: Seven Super Monster Cards" : [1000086, []],
    "Dream: A Handful of Shiny Gifts" : [1000087, []],
    "Dream: A Pile of Sparkling Gifts" : [1000088, []],
    "Dream: A Glistening Heap of Gifts" : [1000089, []],
    "Dream: A Glowing Mass of Gifts" : [1000090, []],
    "Dream: A Luminous Pile of Gifts" : [1000091, []],
    "Dream: A Rare Holographic Card!" : [1000092, []],
    "Dream: Sparkling Bonus Pack" : [1000093, []],
    "Dream: Brilliant Bonus Deck" : [1000094, []],
    "Dream: Shimmering Quick Gifts" : [1000095, []],
    "Dream: Twinkling Quick Gifts" : [1000096, []],
    "Dream: Brighter Bounties" : [1000097, []],
    "Dream: Beautiful Bounties" : [1000098, []],
    "Dream: And for This Gift, I Feel Blessed" : [1000099, []],
    "Dream: A Little Help From My Friends" : [1000100, []],
    "Dream: Let This Burden Drift Away" : [1000101, []],
    "Dream: This Is My Curse!" : [1000102, []],
    "Dream: Mental Pictures" : [1000103, []],
    "Dream: Dream Journal" : [1000104, []],
    "Dream: Known Occurences" : [1000105, []],
    "Dream: Discovered Miracles" : [1000106, []],
    "Dream: A Series of Fortunate Events" : [1000107, []],
    "Dream: Her Heart: Story Lover" : [1000108, []],
    "Dream: Her Heart: Karma Collector" : [1000109, ["grind"]],
    "Dream: Her Heart: Heavy Combo Keeper" : [1000110, ["heavy_rain"]],
    "Dream: Her Heart: Quick Void" : [1000111, ["tedious"]],
    "Dream: Her Heart: Light Gifts" : [1000112, ["tedious"]],
    "Dream: Her Heart: Quickplay Lover" : [1000113, ["quickplay"]],
    "Dream: Her Heart: Heart of Gold" : [1000114, ["quickplay"]],
    "Dream: Her Heart: Nightmare Lover" : [1000115, ["endl_nightmare"]],
    "Dream: Her Heart: Nightmare Gifts" : [1000116, ["endl_nightmare"]],
    "Dream: Her Heart: Quick Nightmares" : [1000117, ["tedious","endl_nightmare"]],
    "Dream: Alter Heart: Three Days" : [1000118, ["alt_her","alt_story","grind"]],
    "Dream: Alter Heart: Bouquet" : [1000119, ["alt_her","alt_story"]],
    "Dream: Alter Heart: Mote Extractor" : [1000120, ["alt_her","alt_story"]],
    "Dream: Alter Heart: Radiance" : [1000121, ["alt_her","quickplay"]],
    "Dream: Alter Heart: Nightmare Lover" : [1000122, ["alt_her","endl_nightmare"]],
    "Dream: Alter Heart: Combo Nightmare" : [1000123, ["alt_her","endl_nightmare","tedious"]],
    "Dream: Defect: Flawless Five" : [1000124, ["defect"]],
    "Dream: Defect: Mote Extractor" : [1000125, ["defect"]],
    "Dream: Defect: Light Combo Keeper" : [1000126, ["defect"]],
    "Dream: Defect: Torrent of Motes" : [1000127, ["defect","torr_rain"]],
    "Dream: Defect: Heavy Gifts" : [1000128, ["defect","heavy_rain"]],
    "Dream: Defect: Silver Heart" : [1000129, ["defect","quickplay"]],
    "Dream: Defect: Super Quick" : [1000130, ["defect","quickplay"]], #will need a lot of dps items
    "Dream: Defect: Karma Collector" : [1000131, ["defect","endl_nightmare","grind"]],
    "Dream: Defect: Overlover" : [1000132, ["defect","endl_nightmare","tedious"]],
    "Dream: Defect: Terror Triplet" : [1000133, ["defect","endl_nightmare"]],
    "Dream: Alter Defect: Three Days" : [1000134, ["alt_defect","alt_story"]],
    "Dream: Alter Defect: Bloodstones" : [1000135, ["alt_defect","alt_story","very_grind"]],
    "Dream: Alter Defect: Perfect Helper" : [1000136, ["alt_defect","alt_story"]],
    "Dream: Alter Defect: Double Radiance" : [1000137, ["alt_defect","ult_quick"]],
    "Dream: Alter Defect: Nightmare Challenger" : [1000138, ["alt_defect","endl_nightmare"]],
    "Dream: Alter Defect: Perfect Nightmare" : [1000139, ["alt_defect","endl_nightmare"]],
    "Dream: Twin Heart: Story Lover" : [1000140, ["twin"]],
    "Dream: Twin Heart: Light Karma" : [1000141, ["twin"]],
    "Dream: Twin Heart: Full Combos" : [1000142, ["twin"]],
    "Dream: Twin Heart: Heavy Void" : [1000143, ["twin","heavy_rain","tedious"]],
    "Dream: Twin Heart: Torrent of Gifts" : [1000144, ["twin","torr_rain"]],
    "Dream: Twin Heart: High Score" : [1000145, ["twin","quickplay"]],
    "Dream: Twin Heart: Radiant Focus" : [1000146, ["twin","quickplay"]],
    "Dream: Twin Heart: Mote Extractor" : [1000147, ["twin","endl_nightmare","grind"]],
    "Dream: Twin Heart: Combo Nightmare" : [1000148, ["twin","endl_nightmare"]],
    "Dream: Twin Heart: Escalating Terror" : [1000149, ["twin","endl_terror"]],
    "Dream: Alter Twin: Three Days" : [1000150, ["alt_twin","alt_story"]],
    "Dream: Alter Twin: Heavy Rain" : [1000151, ["alt_twin","alt_story","heavy_rain"]],
    "Dream: Alter Twin: Friend Chain" : [1000152, ["alt_twin","alt_story","tedious"]], #luck-based
    "Dream: Alter Twin: Quickplay Lover" : [1000153, ["alt_twin","quickplay"]],
    "Dream: Alter Twin: Karma Collector" : [1000154, ["alt_twin","endl_nightmare"]],
    "Dream: Alter Twin: Quad Combo" : [1000155, ["alt_twin","endl_nightmare"]],
    "Dream: The Devil: Mote Extractor" : [1000156, ["devil"]],
    "Dream: The Devil: Karma Collector" : [1000157, ["devil","grind"]],
    "Dream: The Devil: Heavy Challenger" : [1000158, ["devil","heavy_rain"]],
    "Dream: The Devil: Negative Ten" : [1000159, ["devil"]],
    "Dream: The Devil: Light Gifts" : [1000160, ["devil"]],
    "Dream: The Devil: Quickplay Lover" : [1000161, ["devil","quickplay"]],
    "Dream: The Devil: Heart of Gold" : [1000162, ["devil","quickplay"]],
    "Dream: The Devil: Nightmare Lover" : [1000163, ["devil","endl_nightmare","grind"]],
    "Dream: The Devil: Overlover" : [1000164, ["devil","endl_nightmare"]],
    "Dream: The Devil: Nightmare Combo" : [1000165, ["devil","endl_nightmare"]],
    "Dream: Alter Devil: Three Days" : [1000166, ["alt_devil","alter_story"]],
    "Dream: Alter Devil: Bouquet" : [1000167, ["alt_devil","alter_story"]],
    "Dream: Alter Devil: Overlover" : [1000168, ["alt_devil","alter_story"]],
    "Dream: Alter Devil: High Score" : [1000169, ["alt_devil","quickplay"]],
    "Dream: Alter Devil: Escalating Stress" : [1000170, ["alt_devil","endl_nightmare"]],
    "Dream: Alter Devil: Nightmare Combo" : [1000171, ["alt_devil","endl_nightmare","tedious"]],
    "Dream: She Will Repair It" : [1000172, []],
    "Dream: Defective Heart" : [1000173, []],
    "Dream: One Chapter Clear" : [1000174, []],
    "Dream: Two Chapters Clear" : [1000175, []],
    "Dream: Three Chapters Clear" : [1000176, []],
    "Dream: Four Chapters Clear" : [1000177, []], #I think the final boss is a chapter?
    "Dream: Five Chapters Clear" : [1000178, ["alter_story"]], #Possible in story mode with Polyps battle (or shiny but I forgot it it's possible in base story)
    "Dream: Six Chapters Clear" : [1000179, ["alter_story"]],
    "Dream: Seven Chapters Clear" : [1000180, ["alter_story"]], #Possible in alter if you buy extra battles
    "Dream: Eight Chapters Clear" : [1000181, ["alter_story"]], #Need a shiny or a polyp fight
    "Dream: Nine Chapters Clear" : [1000182, ["alter_story", "tedious"]], #Need both
    "Dream: Level 4 Drizzle" : [1000183, []],
    "Dream: Level 8 Rainstorm" : [1000184, ["heavy_rain"]],
    "Dream: Level 12 Monsoon" : [1000185, ["heavy_rain"]],
    "Dream: Even Further Beyond" : [1000186, ["torr_rain"]], #I don't think (or it's hard) to have overlevels in heavy
    "Dream: 20,000 Specks" : [1000187, []],
    "Dream: 40,000 Flakes" : [1000188, []],
    "Dream: 60,000 Bits" : [1000189, []],
    "Dream: 80,000 Dots" : [1000190, []],
    "Dream: Mountain of Motes" : [1000191, ["heavy_rain"]],
    "Dream: Ocean of Motes" : [1000192, ["heavy_rain"]],
    "Dream: Planet of Motes" : [1000193, ["heavy_rain","grind"]],
    "Dream: Star of Motes" : [1000194, ["torr_rain","grind"]],
    "Dream: Galaxy of Motes" : [1000195, ["torr_rain",'very_grind']],
    "Dream: RNG Persuader" : [1000196, []],
    "Dream: RNG Dominator?" : [1000197, []],
    "Dream: Hacked Dice" : [1000198, ["heavy_rain"]], #At this point I wonder if alter story is just the better way for this
    "Dream: Excessively Superfluous Luck" : [1000199, ["heavy_rain","grind"]],
    "Dream: Lucky 13" : [1000200, []],
    "Dream: A Wonderful Gift" : [1000201, []],
    "Dream: They Really Love Me!" : [1000202, []],
    "Dream: All the Right Moves" : [1000203, []],
    "Dream: Playing Hard to Love" : [1000204, ["very_grind"]],
    "Dream: Bottle It Up" : [1000205, []],
    "Dream: Calm Under Pressure" : [1000206, ["grind","tedious"]],
    "Dream: It's Almost Easy" : [1000207, []],
    "Dream: She Will Not Give Up" : [1000208, []],
    "Dream: Friend Train" : [1000209, []],
    "Dream: Chain of Misfits" : [1000210, ["tedious"]], #needs lot of helpers
    "Dream: Sunglasses" : [1000211, []],
    "Dream: Void Nullifier" : [1000212, []],
    "Dream: Fire Wall" : [1000213, []],
    "Dream: Lightning Rod" : [1000214, []],
    "Dream: The Antidote" : [1000215, []],
    "Dream: Heart Trick" : [1000216, []],
    "Dream: Perfect Ten" : [1000217, ["tedious"]],
    "Dream: God Run" : [1000218, ["very_tedious", "heavy_rain"]],
    "Dream: Triple Deluxe" : [1000219, []],
    "Dream: Super Septuplet" : [1000220, ["tedious"]],
    "Dream: Torrential Triplet" : [1000221, ["tedious","torr_rain"]],
    "Dream: Random Encounters" : [1000222, []],
    "Dream: All The Pretty Faces" : [1000223, []],
    "Dream: Scary Monsters and Lovely Creeps" : [1000224, ["grind"]],
    "Dream: Lonely Gift" : [1000225, []],
    "Dream: The Key to Love" : [1000226, []],
    "Dream: Rest Assured" : [1000227, []],
    "Dream: Sparkling Soil" : [1000228, []],
    "Dream: Phobiasynthesis" : [1000229, ["grind"]],
    "Dream: What Plants Crave!" : [1000230, ["grind"]],
    "Dream: The Call of the Garden" : [1000231, []],
    "Dream: Secret Admirer" : [1000232, []],
    "Dream: Don't Forget to Breathe" : [1000233, []],
    "Dream: Boss Rush in My Boss Rush" : [1000234, []],
    "Dream: To My Future Self" : [1000235, []],
    "Dream: Tomorrow is Already Loved" : [1000236, []],
    "Dream: Fully Scrambled" : [1000237, []],
    "Dream: Maximum Spicy!" : [1000238, []],
    "Dream: Mild Paradox" : [1000239, ["grind"]],
    "Dream: Self Confidence" : [1000240, []],
    "Dream: She's Got a Ticket to Ride" : [1000241, ["grind"]],
    "Dream: Weathered the Storm" : [1000242, ["grind"]],
    "Dream: The Cutest Art Collector" : [1000243, ["very_grind"]],
    "Dream: Blot's Patron" : [1000244, ["grind"]],
    "Dream: Wonderfully Generous" : [1000245, []],
    "Dream: I Feel It, I Feel the Cosmos!" : [1000246, ["very_grind"]],
    "Dream: Did You Know?" : [1000247, ["grind"]],
    "Dream: Vitrea's Secret" : [1000248, []],
    "Dream: You Passed!" : [1000249, []],
    "Dream: Extra Credit!" : [1000250, []],
    "Dream: A++" : [1000251, []],
    "Dream: Void Smart" : [1000252, ["grind"]],
    "Dream: Forbidden Knowledge" : [1000253, ["very_grind"]],
    "Dream: 8 Free Gifts!" : [1000254, ["grind"]],
    "Dream: 16 Free Gifts!" : [1000255, ["very_grind"]],
    "Dream: 32 Free Gifts!" : [1000256, ["very_grind"]],
    "Dream: Coming Undone" : [1000257, []],
    "Dream: Free Hug With Every Sawblade" : [1000258, []],
    "Dream: Worth a Thousand Words" : [1000259, []],
    "Dream: Under My Umbrella" : [1000260, []],
    "Dream: Thunderstruck" : [1000261, []],
    "Dream: Saving It for a Rainy Day" : [1000262, []],
    "Dream: Pure Affection" : [1000263, []],
    "Dream: Polished Affect" : [1000264, []],
    "Dream: Extra Crispy" : [1000265, []],
    "Dream: Pour Some Venom on Me" : [1000266, []],
    "Dream: 12 Trades!" : [1000267, ["grind"]],
    "Dream: 24 Trades!" : [1000268, ["very_grind"]],
    "Dream: 48 Trades!" : [1000269, ['very_grind']],
    "Dream: Cool Side of the Pillow" : [1000270, []],
    "Dream: Feed the Eyeball" : [1000271, []],
    "Dream: I Bleed It Out" : [1000272, []],
    "Dream: A Chemical Romance" : [1000273, []],
    "Dream: Pathetic, Wasted, Soulless, Compromised" : [1000274, []],
    "Dream: Screaming for Vengeance" : [1000275, []],
    "Dream: Double Take" : [1000276, []],
    "Dream: The Gift of Giving" : [1000277, []],
    "Dream: Just Warming Up" : [1000278, []],
    "Dream: Vibrant Trade" : [1000279, []],
    "Dream: Time's Up Already?" : [1000280, []],
    "Dream: 5 Bonding Time Gifts" : [1000281, []],
    "Dream: 15 Bonding Time Gifts" : [1000282, ["grind"]],
    "Dream: 40 Bonding Time Gifts" : [1000283, ["very_grind"]],
    "Dream: 90 Bonding Time Gifts" : [1000284, ["very_grind"]],
    "Dream: Demonlord's Souls" : [1000285, ["grind"]],
    "Dream: Absolute Destiny Apocalypse" : [1000286, []],
    "Dream: I Would Walk Five Hundred Tiles" : [1000287, ["grind"]],
    "Dream: I Know the Pieces Fit" : [1000288, ["tedious"]],
    "Dream: A Critical Roll!" : [1000289, ["grind"]],
    "Dream: Veyeral Games" : [1000290, []],
    "Dream: Can't Resist the Current" : [1000291, ["grind"]],
    "Dream: I'm At Soup!" : [1000292, ["grind"]],
    "Dream: Bring an Umbrella" : [1000293, []],
    "Dream: How Do You Love Disorder?" : [1000294, ["defect"]],
    "Dream: Alone Together" : [1000295, ["twin"]],
    "Dream: Wrong Side of Heaven" : [1000296, ["devil"]],
    "Dream: Nothing Times Two" : [1000297, []],
    "Dream: Nothing Times Three" : [1000298, []],
    "Dream: Nothing Times Five" : [1000299, ["grind"]],
    "Dream: The Void: Heavy" : [1000300, ["heavy_rain"]],
    "Dream: The Void: Torrent" : [1000301, ["torr_rain"]],
    "Dream: Fallen Angel" : [1000302, []],
    "Dream: The Infection Must Die!" : [1000303, ["defect"]],
    "Dream: Can't Pull Us Apart" : [1000304, ["twin"]],
    "Dream: Righteous Side of Hell" : [1000305, ["devil"]],
    "Dream: Negative Two" : [1000306, []],
    "Dream: Negative Three" : [1000307, []],
    "Dream: Totaria: Heavy" : [1000308, ["heavy_rain"]],
    "Dream: Totaria: Torrent" : [1000309, ["torr_rain"]],
    "Dream: The Perfect Veyeral" : [1000310, []],
    "Dream: My Best Veyeral" : [1000311, ["defect"]],
    "Dream: Group Hug" : [1000312, ["twin"]],
    "Dream: Wrathful Pride" : [1000313, ["devil"]],
    "Dream: Two Perfect" : [1000314, []],
    "Dream: Blue Veyeral: Heavy" : [1000315, ["heavy_rain"]],
    "Dream: Blue Veyeral: Torrent" : [1000316, ["torr_rain"]],
    "Dream: Unusual Drizzle" : [1000317, ["alter_story"]],
    "Dream: Peculiar Rainstorm" : [1000318, ["alter_story","heavy_rain"]],
    "Dream: Extraordinary Monsoon" : [1000319, ["alter_story","torr_rain"]],
    "Dream: Day After Tomorrow" : [1000320, ["alter_story"]],
    "Dream: Eight Days a Week" : [1000321, ["alter_story","grind"]],
    "Dream: Altered Fortnight" : [1000322, ["alter_story","very_grind"]],
    "Dream: 28 Altered Days Later" : [1000323, ["alter_story","very_grind"]],
    "Dream: Strange Flood" : [1000324, ["alter_story"]],
    "Dream: Abnormal Deluge" : [1000325, ["alter_story","tedious"]],
    "Dream: Unimaginable Tsunami" : [1000326, ["alter_story","torr_rain","very_tedious"]],
    "Dream: The Heart of a Zaraden" : [1000327, ["alter_story"]],
    "Dream: Her Heart of Gold" : [1000328, ["alter_story"]],
    "Dream: The Flawed Heart" : [1000329, ["alter_story","defect"]],
    "Dream: Fool's Gold" : [1000330, ["alter_story","defect"]],
    "Dream: The Heart of a Twin" : [1000331, ["alter_story","twin"]],
    "Dream: Golden Twins" : [1000332, ["alter_story","twin"]],
    "Dream: The Heart of a Devil" : [1000333, ["alter_story","devil"]],
    "Dream: Devil's Gold" : [1000334, ["alter_story","devil"]],
    "Dream: The Painted Heart" : [1000335, ["alter_story","alt_her"]],
    "Dream: She's Painted Gold" : [1000336, ["alter_story","alt_her"]],
    "Dream: The Perfect Heart" : [1000337, ["alter_story","alt_defect"]],
    "Dream: Flawless Gold" : [1000338, ["alter_story","alt_defect"]],
    "Dream: The Beaming Heart" : [1000339, ["alter_story","alt_twin"]],
    "Dream: Reflected in Gold" : [1000340, ["alter_story","alt_twin"]],
    "Dream: The Condemned Heart" : [1000341, ["alter_story","alt_devil"]],
    "Dream: Scorched Gold" : [1000342, ["alter_story","alt_devil"]],
    "Dream: 3 Altered Silvers" : [1000343, ["alter_story"]], #For the following 6, tag won't be enough, to make the logic elegant, we should make stuff depending on the number of difficulties unlocked with the number of characters
    "Dream: 12 Altered Silvers" : [1000344, ["alter_story"]],
    "Dream: 24 Altered Silvers" : [1000345, ["alter_story"]],
    "Dream: Altered Radiance" : [1000346, ["alter_story"]],
    "Dream: 5 Altered Radiants" : [1000347, ["alter_story"]],
    "Dream: 15 Altered Radiants" : [1000348, ["alter_story","tedious"]],
    "Dream: 50 Altered Roses" : [1000349, ["alter_story"]],
    "Dream: 100 Altered Roses" : [1000350, ["alter_story","grind"]],
    "Dream: 250 Altered Roses" : [1000351, ["alter_story","very_grind"]],
    "Dream: 500 Altered Roses" : [1000352, ["alter_story","very_grind"]],
    "Dream: Altered Bloodstone" : [1000353, ["alter_story"]],
    "Dream: 5 Altered Bloodstones" : [1000354, ["alter_story"]],
    "Dream: 20 Altered Bloodstones" : [1000355, ["alter_story","grind"]],
    "Dream: 50 Altered Bloodstones" : [1000356, ["alter_story","very_grind"]],
    "Dream: Love Them All Over Again" : [1000357, ["quickplay"]],
    "Dream: Love Is Overpowered!" : [1000358, ["quickplay"]],
    "Dream: Giant Lover" : [1000359, ["quickplay"]],
    "Dream: Titan Lover" : [1000360, ["quickplay"]],
    "Dream: Lovely Level 5" : [1000361, ["quickplay"]],
    "Dream: Lovely Level 10" : [1000362, ["quickplay"]],
    "Dream: Lovely Level 15" : [1000363, ["quickplay"]],
    "Dream: Lovely Level 20" : [1000364, ["quickplay","grind"]],
    "Dream: Lovely Level 25" : [1000365, ["quickplay","grind"]],
    "Dream: Lovely Level 30" : [1000366, ["quickplay","very_grind"]],
    "Dream: Lovely Level 35" : [1000367, ["quickplay","very_grind"]],
    "Dream: Lovely Level 40" : [1000368, ["quickplay","very_grind"]],
    "Dream: Lovely Level 45" : [1000369, ["quickplay","very_grind"]],
    "Dream: Lovely Level 50" : [1000370, ["quickplay","very_grind"]],
    "Dream: A Radiant Medal!" : [1000371, ["quickplay"]],
    "Dream: Glowing Radiance" : [1000372, ["quickplay"]],
    "Dream: Burning Radiance" : [1000373, ["quickplay"]],
    "Dream: Blinding Radiance" : [1000374, ["quickplay"]],
    "Dream: 10 Medals" : [1000375, ["quickplay"]],
    "Dream: 40 Medals" : [1000376, ["quickplay"]],
    "Dream: 90 Medals" : [1000377, ["quickplay"]],
    "Dream: 160 Medals" : [1000378, ["quickplay","grind"]],
    "Dream: 250 Medals" : [1000379, ["quickplay",'very_grind']],
    "Dream: 360 Medals" : [1000380, ["quickplay","very_grind"]],
    "Dream: 10 Gold Medals" : [1000381, ["quickplay"]],
    "Dream: 40 Gold Medals" : [1000382, ["quickplay"]],
    "Dream: 90 Gold Medals" : [1000383, ["quickplay"]],
    "Dream: 160 Gold Medals" : [1000384, ["quickplay","grind"]],
    "Dream: 250 Gold Medals" : [1000385, ["quickplay","very_grind"]],
    "Dream: 360 Gold Medals" : [1000386, ["quickplay","very_grind"]],
    "Dream: 10 Radiant Medals!" : [1000387, ["quickplay"]],
    "Dream: 40 Radiant Medals!" : [1000388, ["quickplay"]],
    "Dream: 90 Radiant Medals!" : [1000389, ["quickplay","grind"]],
    "Dream: 160 Radiant Medals!" : [1000390, ["quickplay","very_grind"]],
    "Dream: 250 Radiant Medals!" : [1000391, ["quickplay","very_grind"]],
    "Dream: 360 Radiant Medals!" : [1000392, ["quickplay","very_grind"]],
    "Dream: Colossus Lover" : [1000393, ["ult_quick"]],
    "Dream: Leviathan Lover" : [1000394, ["ult_quick","tedious"]],
    "Dream: Ultimate Goddess Lover" : [1000395, ["ult_quick","tedious"]],
    "Dream: Ultra Level 10" : [1000396, ["ult_quick"]],
    "Dream: Ultra Level 20" : [1000397, ["ult_quick","grind"]],
    "Dream: Ultra Level 30" : [1000398, ["ult_quick","grind","tedious"]],
    "Dream: Ultra Level 40" : [1000399, ["ult_quick","very_grind","tedious"]],
    "Dream: Ultra Level 50" : [1000400, ["ult_quick","very_grind","very_tedious"]],
    "Dream: Ultra Radiance" : [1000401, ["ult_quick"]],
    "Dream: 30 Ultra Radiant Medals" : [1000402, ["ult_quick","grind"]],
    "Dream: 80 Ultra Radiant Medals" : [1000403, ["ult_quick","grind","tedious"]],
    "Dream: 150 Ultra Radiant Medals" : [1000404, ["ult_quick","very_grind","very_tedious"]],
    "Dream: A Sublime Medal!" : [1000405, ["ult_quick"]],
    "Dream: Plus Ultra!" : [1000406, ["ult_quick","tedious"]],
    "Dream: 10 Sublime Medals!" : [1000407, ["ult_quick","grind"]],
    "Dream: 25 Sublime Medals!" : [1000408, ["ult_quick","grind","tedious"]],
    "Dream: 50 Sublime Medals!" : [1000409, ["ult_quick","grind","very_tedious"]],
    "Dream: 100 Sublime Medals!" : [1000410, ["ult_quick","very_grind","very_tedious"]],
    "Dream: Burdens and All" : [1000411, ["towers"]],
    "Dream: Level 4 Pillar" : [1000412, ["towers"]],
    "Dream: Level 8 Pylon" : [1000413, ["towers"]],
    "Dream: Level 12 Monolith" : [1000414, ["towers"]],
    "Dream: Level 16 Obelisk" : [1000415, ["towers","tedious"]],
    "Dream: Shameful Spire" : [1000416, ["towers"]],
    "Dream: Frustration Fortress" : [1000417, ["towers"]],
    "Dream: Symbolic Skyscraper" : [1000418, ["towers"]],
    "Dream: Anxious Ascent" : [1000419, ["towers"]],
    "Dream: Blossoming Belfry" : [1000420, ["towers"]],
    "Dream: Looming Loneliness" : [1000421, ["towers"]],
    "Dream: Citadel of Spiders" : [1000422, ["towers","tedious"]],
    "Dream: Dream Den" : [1000423, ["towers"]],
    "Dream: We Are Programmed to Receive" : [1000424, ["towers"]],
    "Dream: One Zaraden's Trash" : [1000425, ["towers"]],
    "Dream: The Emptiness Machine" : [1000426, ["towers"]],
    "Dream: 10 Vault Gifts!" : [1000427, ["towers","grind"]],
    "Dream: 20 Vault Gifts!" : [1000428, ["towers","very_grind"]],
    "Dream: Insecure Passwords" : [1000429, ["towers"]],
    "Dream: Smooth Operator" : [1000430, ["towers"]],
    "Dream: Prideful Shame" : [1000431, ["towers"]],
    "Dream: Content in Frustration" : [1000432, ["towers"]],
    "Dream: Accepting Denial" : [1000433, ["towers"]],
    "Dream: Calming Anxiety" : [1000434, ["towers"]],
    "Dream: Confident Insecurity" : [1000435, ["towers"]],
    "Dream: Belonging With Loneliness" : [1000436, ["towers"]],
    "Dream: Build Tall, Build Higher" : [1000437, ["towers"]],
    "Dream: Build Far, Build Wider" : [1000438, ["towers"]],
    "Dream: Build, Build, Build, Build..." : [1000439, ["towers"]],
    "Dream: Scattered Across Time and Space" : [1000440, ["towers"]],
    "Dream: Rapture My Heart" : [1000441, ["towers"]],
    "Dream: Sticks and Stones" : [1000442, ["towers"]],
    "Dream: Marked For Deletion" : [1000443, ["towers"]],
    "Dream: Unbreakable Starlight Bloom" : [1000444, ["towers"]],
    "Dream: Together As None" : [1000445, ["towers"]],
    "Dream: Tower of Her Love" : [1000446, ["towers"]],
    "Dream: Looking to the Sky to Save Me" : [1000447, ["towers"]],
    "Dream: Flawless Tower Climber" : [1000448, ["towers","defect"]],
    "Dream: Looking Cause I'm Tired of Trying" : [1000449, ["towers","defect"]],
    "Dream: Siblings Climb Together" : [1000450, ["towers","twin"]],
    "Dream: Looking for Something to Help Me" : [1000451, ["towers","twin"]],
    "Dream: Tenacious Tower Climber" : [1000452, ["towers","devil"]],
    "Dream: Looking for a Complication" : [1000453, ["towers","devil"]],
    "Dream: Painted Tower Climber" : [1000454, ["towers","alt_her"]],
    "Dream: When I Learn to Fly" : [1000455, ["towers","alt_her"]],
    "Dream: Perfect Tower Climber" : [1000456, ["towers","alt_defect"]],
    "Dream: I Can't Quite Make It Alone" : [1000457, ["towers","alt_defect"]],
    "Dream: Sunshine at the Top" : [1000458, ["towers","alt_twin"]],
    "Dream: Fly Along With Me" : [1000459, ["towers","alt_twin"]],
    "Dream: Demonic Tower Climber" : [1000460, ["towers","alt_devil"]],
    "Dream: Run and Tell All of the Angels" : [1000461, ["towers","alt_devil"]],
    "Dream: Top of Tiny Tower" : [1000462, ["towers"]],
    "Dream: Top of Taller Tower" : [1000463, ["towers"]],
    "Dream: Top of Torrential Tower" : [1000464, ["towers"]],
    "Dream: Top of Shameful Spire" : [1000465, ["towers"]],
    "Dream: Top of Frustration Fortress" : [1000466, ["towers"]],
    "Dream: Top of Symbolic Skyscraper" : [1000467, ["towers"]],
    "Dream: Top of Anxious Ascent" : [1000468, ["towers"]],
    "Dream: Top of Blossoming Belfry" : [1000469, ["towers"]],
    "Dream: Top of Looming Loneliness" : [1000470, ["towers"]],
    "Dream: 5 Silver Towers" : [1000471, ["towers"]],
    "Dream: 15 Silver Towers" : [1000472, ["towers","grind"]],
    "Dream: 30 Silver Towers" : [1000473, ["towers","very_grind"]],
    "Dream: A Radiant Tower" : [1000474, ["towers"]],
    "Dream: 6 Radiant Towers" : [1000475, ["towers"]],
    "Dream: 18 Radiant Towers" : [1000476, ["towers","grind"]],
    "Dream: One out of Infinity" : [1000477, ["endless"]],
    "Dream: A Nightmare Cycle" : [1000478, ["endless"]],
    "Dream: Two Nightmare Cycles" : [1000479, ["endless"]],
    "Dream: Three Nightmare Cycles" : [1000480, ["endless"]],
    "Dream: Four Nightmare Cycles" : [1000481, ["endless","tedious"]],
    "Dream: All Nightmare Long" : [1000482, ["endless","tedious"]],
    "Dream: 30K Nightmare" : [1000483, ["endless"]],
    "Dream: 60K Nightmare" : [1000484, ["endless"]],
    "Dream: 90K Nightmare" : [1000485, ["endless"]],
    "Dream: 120K Nightmare" : [1000486, ["endless"]],
    "Dream: 150K Nightmare" : [1000487, ["endless","tedious"]],
    "Dream: Mountain of Nightmares" : [1000488, ["endless","tedious"]],
    "Dream: A Dim Glow in the Dark" : [1000489, ["endless"]],
    "Dream: A Bright Light in the Dark" : [1000490, ["endless"]],
    "Dream: A Rainbow in the Dark" : [1000491, ["endless","tedious"]],
    "Dream: Level 5 Scare" : [1000492, ["endless"]],
    "Dream: Level 10 Fright" : [1000493, ["endless"]],
    "Dream: Level 15 Terror" : [1000494, ["endless"]],
    "Dream: Level 20 Abomination" : [1000495, ["endless","tedious"]], #does it deserve tedious?
    "Dream: Infinite Dreams" : [1000496, ["endless","grind"]],
    "Dream: Karmic Hoarding" : [1000497, ["endless"]],
    "Dream: Karmic Bounty" : [1000498, ["endless","grind"]],
    "Dream: Karmic Fortune" : [1000499, ["endless","very_grind"]],
    #for testing:
    "Dream: Something Something Quick" : [1004242, ["quickplay"]]
}

story_medals = {

}

qp_copper = {
    #"QP Copper: Scrambla" : [1020000, []]
}

qp_bronze = {

}

qp_silver = {

}

qp_gold = {

}

qp_radiant = {

}

uqp_rad1 = {

}

uqp_rad2 = {

}

uqp_rad3 = {

}

altstory_copper = {

}

altstory_bronze = {

}

altstory_silver = {

}

altstory_gold = {

}

altstory_radiant = {

}

altstory_rose = {

}

altstory_crimson = {

}

towers_copper = {

}

towers_bronze = {

}

towers_silver = {

}

towers_gold = {

}

towers_radiant = {

}

endl_str_copper = {

}

endl_str_bronze = {

}

endl_str_silver = {

}

endl_str_gold = {

}

endl_str_radiant = {

}

endl_ter_copper = {

}

endl_ter_bronze = {

}

endl_ter_silver = {

}

endl_ter_gold = {

}

endl_ter_radiant = {

}

sublime_uqp = {

}

sublime_altstory = {

}

sublime_tower = {

}

sublime_endless = {

}

qp_upgrades = {

}

altstory_upgr = {

}

endless_upgr = {

}

event_upgrades = {

}

other_locations_list = {
    "Bonus Gift" : [1400000,[]] 
    # unique: 1000 bonus gifts are always loaded in the BBL whereas the needed amount of locations gets added to the regions later. 
    #DO NOT GIVE A LOCATION AN ID OF 1450000 THROUGH 1451000 AS THAT IS WHERE THEY ARE IN TERMS OF ID!!
}