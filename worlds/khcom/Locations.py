from BaseClasses import Location
import typing


class AchieveData(typing.NamedTuple):
    id: typing.Optional[int]
    region: str


class KHCOMAchievement(Location):
    game: str = "Kingdom Hearts Chain of Memories"

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.event = not address
        
achievement_table = {
    ,"Kingdom Key 0": AchieveData(5001, "Floor 1")
    ,"Kingdom Key 1": AchieveData(5002, "Floor 1")
    ,"Kingdom Key 2": AchieveData(5003, "Floor 1")
    ,"Kingdom Key 3": AchieveData(5004, "Floor 1")
    ,"Kingdom Key 4": AchieveData(5005, "Floor 1")
    ,"Kingdom Key 5": AchieveData(5006, "Floor 1")
    ,"Kingdom Key 6": AchieveData(5007, "Floor 1")
    ,"Kingdom Key 7": AchieveData(5008, "Floor 1")
    ,"Kingdom Key 8": AchieveData(5009, "Floor 1")
    ,"Kingdom Key 9": AchieveData(5010, "Floor 1")
    
    ,"Three Wishes 0": AchieveData(5011, "Floor 5")
    ,"Three Wishes 1": AchieveData(5012, "Floor 5")
    ,"Three Wishes 2": AchieveData(5013, "Floor 5")
    ,"Three Wishes 3": AchieveData(5014, "Floor 5")
    ,"Three Wishes 4": AchieveData(5015, "Floor 5")
    ,"Three Wishes 5": AchieveData(5016, "Floor 5")
    ,"Three Wishes 6": AchieveData(5017, "Floor 5")
    ,"Three Wishes 7": AchieveData(5018, "Floor 5")
    ,"Three Wishes 8": AchieveData(5019, "Floor 5")
    ,"Three Wishes 9": AchieveData(5020, "Floor 5")
    
    ,"Crabclaw 0": AchieveData(5021, "Floor 7")
    ,"Crabclaw 1": AchieveData(5022, "Floor 7")
    ,"Crabclaw 2": AchieveData(5023, "Floor 7")
    ,"Crabclaw 3": AchieveData(5024, "Floor 7")
    ,"Crabclaw 4": AchieveData(5025, "Floor 7")
    ,"Crabclaw 5": AchieveData(5026, "Floor 7")
    ,"Crabclaw 6": AchieveData(5027, "Floor 7")
    ,"Crabclaw 7": AchieveData(5028, "Floor 7")
    ,"Crabclaw 8": AchieveData(5029, "Floor 7")
    ,"Crabclaw 9": AchieveData(5030, "Floor 7")
    
    ,"Pumpkinhead 0": AchieveData(5031, "Floor 6")
    ,"Pumpkinhead 1": AchieveData(5032, "Floor 6")
    ,"Pumpkinhead 2": AchieveData(5033, "Floor 6")
    ,"Pumpkinhead 3": AchieveData(5034, "Floor 6")
    ,"Pumpkinhead 4": AchieveData(5035, "Floor 6")
    ,"Pumpkinhead 5": AchieveData(5036, "Floor 6")
    ,"Pumpkinhead 6": AchieveData(5037, "Floor 6")
    ,"Pumpkinhead 7": AchieveData(5038, "Floor 6")
    ,"Pumpkinhead 8": AchieveData(5039, "Floor 6")
    ,"Pumpkinhead 9": AchieveData(5040, "Floor 6")
    
    ,"Fairy Harp 0": AchieveData(5041, "Floor 8")
    ,"Fairy Harp 1": AchieveData(5042, "Floor 8")
    ,"Fairy Harp 2": AchieveData(5043, "Floor 8")
    ,"Fairy Harp 3": AchieveData(5044, "Floor 8")
    ,"Fairy Harp 4": AchieveData(5045, "Floor 8")
    ,"Fairy Harp 5": AchieveData(5046, "Floor 8")
    ,"Fairy Harp 6": AchieveData(5047, "Floor 8")
    ,"Fairy Harp 7": AchieveData(5048, "Floor 8")
    ,"Fairy Harp 8": AchieveData(5049, "Floor 8")
    ,"Fairy Harp 9": AchieveData(5050, "Floor 8")
    
    ,"Wishing Star 0": AchieveData(5051, "Floor 4")
    ,"Wishing Star 1": AchieveData(5052, "Floor 4")
    ,"Wishing Star 2": AchieveData(5053, "Floor 4")
    ,"Wishing Star 3": AchieveData(5054, "Floor 4")
    ,"Wishing Star 4": AchieveData(5055, "Floor 4")
    ,"Wishing Star 5": AchieveData(5056, "Floor 4")
    ,"Wishing Star 6": AchieveData(5057, "Floor 4")
    ,"Wishing Star 7": AchieveData(5058, "Floor 4")
    ,"Wishing Star 8": AchieveData(5059, "Floor 4")
    ,"Wishing Star 9": AchieveData(5060, "Floor 4")
    
    ,"Spellbinder 0": AchieveData(5061, "Floor 10")
    ,"Spellbinder 1": AchieveData(5062, "Floor 10")
    ,"Spellbinder 2": AchieveData(5063, "Floor 10")
    ,"Spellbinder 3": AchieveData(5064, "Floor 10")
    ,"Spellbinder 4": AchieveData(5065, "Floor 10")
    ,"Spellbinder 5": AchieveData(5066, "Floor 10")
    ,"Spellbinder 6": AchieveData(5067, "Floor 10")
    ,"Spellbinder 7": AchieveData(5068, "Floor 10")
    ,"Spellbinder 8": AchieveData(5069, "Floor 10")
    ,"Spellbinder 9": AchieveData(5070, "Floor 10")
    
    ,"Metal Chocobo 0": AchieveData(5071, "Floor 3 Room of Rewards")
    ,"Metal Chocobo 1": AchieveData(5072, "Floor 3 Room of Rewards")
    ,"Metal Chocobo 2": AchieveData(5073, "Floor 3 Room of Rewards")
    ,"Metal Chocobo 3": AchieveData(5074, "Floor 3 Room of Rewards")
    ,"Metal Chocobo 4": AchieveData(5075, "Floor 3 Room of Rewards")
    ,"Metal Chocobo 5": AchieveData(5076, "Floor 3 Room of Rewards")
    ,"Metal Chocobo 6": AchieveData(5077, "Floor 3 Room of Rewards")
    ,"Metal Chocobo 7": AchieveData(5078, "Floor 3 Room of Rewards")
    ,"Metal Chocobo 8": AchieveData(5079, "Floor 3 Room of Rewards")
    ,"Metal Chocobo 9": AchieveData(5080, "Floor 3 Room of Rewards")
    
    ,"Olympia 0": AchieveData(5081, "Floor 3")
    ,"Olympia 1": AchieveData(5082, "Floor 3")
    ,"Olympia 2": AchieveData(5083, "Floor 3")
    ,"Olympia 3": AchieveData(5084, "Floor 3")
    ,"Olympia 4": AchieveData(5085, "Floor 3")
    ,"Olympia 5": AchieveData(5086, "Floor 3")
    ,"Olympia 6": AchieveData(5087, "Floor 3")
    ,"Olympia 7": AchieveData(5088, "Floor 3")
    ,"Olympia 8": AchieveData(5089, "Floor 3")
    ,"Olympia 9": AchieveData(5090, "Floor 3")
    
    ,"Lionheart 0": AchieveData(5091, "Floor 1 Room of Rewards")
    ,"Lionheart 1": AchieveData(5092, "Floor 1 Room of Rewards")
    ,"Lionheart 2": AchieveData(5093, "Floor 1 Room of Rewards")
    ,"Lionheart 3": AchieveData(5094, "Floor 1 Room of Rewards")
    ,"Lionheart 4": AchieveData(5095, "Floor 1 Room of Rewards")
    ,"Lionheart 5": AchieveData(5096, "Floor 1 Room of Rewards")
    ,"Lionheart 6": AchieveData(5097, "Floor 1 Room of Rewards")
    ,"Lionheart 7": AchieveData(5098, "Floor 1 Room of Rewards")
    ,"Lionheart 8": AchieveData(5099, "Floor 1 Room of Rewards")
    ,"Lionheart 9": AchieveData(5100, "Floor 1 Room of Rewards")
    
    ,"Lady Luck 0": AchieveData(5101, "Floor 2")
    ,"Lady Luck 1": AchieveData(5102, "Floor 2")
    ,"Lady Luck 2": AchieveData(5103, "Floor 2")
    ,"Lady Luck 3": AchieveData(5104, "Floor 2")
    ,"Lady Luck 4": AchieveData(5105, "Floor 2")
    ,"Lady Luck 5": AchieveData(5106, "Floor 2")
    ,"Lady Luck 6": AchieveData(5107, "Floor 2")
    ,"Lady Luck 7": AchieveData(5108, "Floor 2")
    ,"Lady Luck 8": AchieveData(5109, "Floor 2")
    ,"Lady Luck 9": AchieveData(5110, "Floor 2")
    
    ,"Divine Rose 0": AchieveData(5111, "Floor 9")
    ,"Divine Rose 1": AchieveData(5112, "Floor 9")
    ,"Divine Rose 2": AchieveData(5113, "Floor 9")
    ,"Divine Rose 3": AchieveData(5114, "Floor 9")
    ,"Divine Rose 4": AchieveData(5115, "Floor 9")
    ,"Divine Rose 5": AchieveData(5116, "Floor 9")
    ,"Divine Rose 6": AchieveData(5117, "Floor 9")
    ,"Divine Rose 7": AchieveData(5118, "Floor 9")
    ,"Divine Rose 8": AchieveData(5119, "Floor 9")
    ,"Divine Rose 9": AchieveData(5120, "Floor 9")
    
    ,"Oathkeeper 0": AchieveData(5121, "Floor 13")
    ,"Oathkeeper 1": AchieveData(5122, "Floor 13")
    ,"Oathkeeper 2": AchieveData(5123, "Floor 13")
    ,"Oathkeeper 3": AchieveData(5124, "Floor 13")
    ,"Oathkeeper 4": AchieveData(5125, "Floor 13")
    ,"Oathkeeper 5": AchieveData(5126, "Floor 13")
    ,"Oathkeeper 6": AchieveData(5127, "Floor 13")
    ,"Oathkeeper 7": AchieveData(5128, "Floor 13")
    ,"Oathkeeper 8": AchieveData(5129, "Floor 13")
    ,"Oathkeeper 9": AchieveData(5130, "Floor 13")
    
    ,"Oblivion 0": AchieveData(5131, "Floor 13")
    ,"Oblivion 1": AchieveData(5132, "Floor 13")
    ,"Oblivion 2": AchieveData(5133, "Floor 13")
    ,"Oblivion 3": AchieveData(5134, "Floor 13")
    ,"Oblivion 4": AchieveData(5135, "Floor 13")
    ,"Oblivion 5": AchieveData(5136, "Floor 13")
    ,"Oblivion 6": AchieveData(5137, "Floor 13")
    ,"Oblivion 7": AchieveData(5138, "Floor 13")
    ,"Oblivion 8": AchieveData(5139, "Floor 13")
    ,"Oblivion 9": AchieveData(5140, "Floor 13")
    
    ,"Diamond Dust 0": AchieveData(5141, "Floor 13 Room of Guidance")
    ,"Diamond Dust 1": AchieveData(5142, "Floor 13 Room of Guidance")
    ,"Diamond Dust 2": AchieveData(5143, "Floor 13 Room of Guidance")
    ,"Diamond Dust 3": AchieveData(5144, "Floor 13 Room of Guidance")
    ,"Diamond Dust 4": AchieveData(5145, "Floor 13 Room of Guidance")
    ,"Diamond Dust 5": AchieveData(5146, "Floor 13 Room of Guidance")
    ,"Diamond Dust 6": AchieveData(5147, "Floor 13 Room of Guidance")
    ,"Diamond Dust 7": AchieveData(5148, "Floor 13 Room of Guidance")
    ,"Diamond Dust 8": AchieveData(5149, "Floor 13 Room of Guidance")
    ,"Diamond Dust 9": AchieveData(5150, "Floor 13 Room of Guidance")
    
    ,"One Winged Angel 0": AchieveData(5151, "Floor 13 Room of Guidance")
    ,"One Winged Angel 1": AchieveData(5152, "Floor 13 Room of Guidance")
    ,"One Winged Angel 2": AchieveData(5153, "Floor 13 Room of Guidance")
    ,"One Winged Angel 3": AchieveData(5154, "Floor 13 Room of Guidance")
    ,"One Winged Angel 4": AchieveData(5155, "Floor 13 Room of Guidance")
    ,"One Winged Angel 5": AchieveData(5156, "Floor 13 Room of Guidance")
    ,"One Winged Angel 6": AchieveData(5157, "Floor 13 Room of Guidance")
    ,"One Winged Angel 7": AchieveData(5158, "Floor 13 Room of Guidance")
    ,"One Winged Angel 8": AchieveData(5159, "Floor 13 Room of Guidance")
    ,"One Winged Angel 9": AchieveData(5160, "Floor 13 Room of Guidance")
    
    ,"Ultima Weapon 0": AchieveData(5161, "Floor 13")
    ,"Ultima Weapon 1": AchieveData(5162, "Floor 13")
    ,"Ultima Weapon 2": AchieveData(5163, "Floor 13")
    ,"Ultima Weapon 3": AchieveData(5164, "Floor 13")
    ,"Ultima Weapon 4": AchieveData(5165, "Floor 13")
    ,"Ultima Weapon 5": AchieveData(5166, "Floor 13")
    ,"Ultima Weapon 6": AchieveData(5167, "Floor 13")
    ,"Ultima Weapon 7": AchieveData(5168, "Floor 13")
    ,"Ultima Weapon 8": AchieveData(5169, "Floor 13")
    ,"Ultima Weapon 9": AchieveData(5170, "Floor 13")
    
    ,"Fire 0": AchieveData(5171, "Floor 1 Room of Truth")
    ,"Fire 1": AchieveData(5172, "Floor 1 Room of Truth")
    ,"Fire 2": AchieveData(5173, "Floor 1 Room of Truth")
    ,"Fire 3": AchieveData(5174, "Floor 1 Room of Truth")
    ,"Fire 4": AchieveData(5175, "Floor 1 Room of Truth")
    ,"Fire 5": AchieveData(5176, "Floor 1 Room of Truth") #Dropped by Axel
    ,"Fire 6": AchieveData(5177, "Floor 1 Room of Truth")
    ,"Fire 7": AchieveData(5178, "Floor 1 Room of Truth")
    ,"Fire 8": AchieveData(5179, "Floor 1 Room of Truth")
    ,"Fire 9": AchieveData(5180, "Floor 1 Room of Truth")
    
    ,"Blizzard 0": AchieveData(5181, "Floor 1")
    ,"Blizzard 1": AchieveData(5182, "Floor 1")
    ,"Blizzard 2": AchieveData(5183, "Floor 1")
    ,"Blizzard 3": AchieveData(5184, "Floor 1")
    ,"Blizzard 4": AchieveData(5185, "Floor 1")
    ,"Blizzard 5": AchieveData(5186, "Floor 1")
    ,"Blizzard 6": AchieveData(5187, "Floor 1")
    ,"Blizzard 7": AchieveData(5188, "Floor 1")
    ,"Blizzard 8": AchieveData(5189, "Floor 1")
    ,"Blizzard 9": AchieveData(5190, "Floor 1")
    
    ,"Thunder 0": AchieveData(5191, "Floor 6 Room of Truth")
    ,"Thunder 1": AchieveData(5192, "Floor 6 Room of Truth")
    ,"Thunder 2": AchieveData(5193, "Floor 6 Room of Truth")
    ,"Thunder 3": AchieveData(5194, "Floor 6 Room of Truth")
    ,"Thunder 4": AchieveData(5195, "Floor 6 Room of Truth")
    ,"Thunder 5": AchieveData(5196, "Floor 6 Room of Truth")
    ,"Thunder 6": AchieveData(5197, "Floor 6 Room of Truth")
    ,"Thunder 7": AchieveData(5198, "Floor 6 Room of Truth") #Dropped by Larxene
    ,"Thunder 8": AchieveData(5199, "Floor 6 Room of Truth")
    ,"Thunder 9": AchieveData(5200, "Floor 6 Room of Truth")
    
    ,"Cure 0": AchieveData(5201, "Floor 1")
    ,"Cure 1": AchieveData(5202, "Floor 1")
    ,"Cure 2": AchieveData(5203, "Floor 1")
    ,"Cure 3": AchieveData(5204, "Floor 1")
    ,"Cure 4": AchieveData(5205, "Floor 1")
    ,"Cure 5": AchieveData(5206, "Floor 1")
    ,"Cure 6": AchieveData(5207, "Floor 1")
    ,"Cure 7": AchieveData(5208, "Floor 1")
    ,"Cure 8": AchieveData(5209, "Floor 1")
    ,"Cure 9": AchieveData(5210, "Floor 1")
    
    ,"Gravity 0": AchieveData(5211, "Floor 5")
    ,"Gravity 1": AchieveData(5212, "Floor 5")
    ,"Gravity 2": AchieveData(5213, "Floor 5")
    ,"Gravity 3": AchieveData(5214, "Floor 5")
    ,"Gravity 4": AchieveData(5215, "Floor 5")
    ,"Gravity 5": AchieveData(5216, "Floor 5")
    ,"Gravity 6": AchieveData(5217, "Floor 5")
    ,"Gravity 7": AchieveData(5218, "Floor 5")
    ,"Gravity 8": AchieveData(5219, "Floor 5")
    ,"Gravity 9": AchieveData(5220, "Floor 5")
    
    ,"Stop 0": AchieveData(5221, "Floor 2")
    ,"Stop 1": AchieveData(5222, "Floor 2")
    ,"Stop 2": AchieveData(5223, "Floor 2")
    ,"Stop 3": AchieveData(5224, "Floor 2")
    ,"Stop 4": AchieveData(5225, "Floor 2")
    ,"Stop 5": AchieveData(5226, "Floor 2")
    ,"Stop 6": AchieveData(5227, "Floor 2")
    ,"Stop 7": AchieveData(5228, "Floor 2")
    ,"Stop 8": AchieveData(5229, "Floor 2")
    ,"Stop 9": AchieveData(5230, "Floor 2")
    
    ,"Aero 0": AchieveData(5231, "Floor 7 Room of Truth")
    ,"Aero 1": AchieveData(5232, "Floor 7 Room of Truth")
    ,"Aero 2": AchieveData(5233, "Floor 7 Room of Truth")
    ,"Aero 3": AchieveData(5234, "Floor 7 Room of Truth")
    ,"Aero 4": AchieveData(5235, "Floor 7 Room of Truth")
    ,"Aero 5": AchieveData(5236, "Floor 7 Room of Truth")
    ,"Aero 6": AchieveData(5237, "Floor 7 Room of Truth") #Dropped by Riku
    ,"Aero 7": AchieveData(5238, "Floor 7 Room of Truth")
    ,"Aero 8": AchieveData(5239, "Floor 7 Room of Truth")
    ,"Aero 9": AchieveData(5240, "Floor 7 Room of Truth")
    
    ,"Simba 0": AchieveData(5241, "Floor 1 Room of Beginnings")
    ,"Simba 1": AchieveData(5242, "Floor 1 Room of Beginnings")
    ,"Simba 2": AchieveData(5243, "Floor 1 Room of Beginnings")
    ,"Simba 3": AchieveData(5244, "Floor 1 Room of Beginnings")
    ,"Simba 4": AchieveData(5245, "Floor 1 Room of Beginnings")
    ,"Simba 5": AchieveData(5246, "Floor 1 Room of Beginnings")
    ,"Simba 6": AchieveData(5247, "Floor 1 Room of Beginnings") #Given by Leon
    ,"Simba 7": AchieveData(5248, "Floor 1 Room of Beginnings")
    ,"Simba 8": AchieveData(5249, "Floor 1 Room of Beginnings")
    ,"Simba 9": AchieveData(5250, "Floor 1 Room of Beginnings")
    
    ,"Genie 0": AchieveData(5251, "Floor 5 Room of Truth")
    ,"Genie 1": AchieveData(5252, "Floor 5 Room of Truth")
    ,"Genie 2": AchieveData(5253, "Floor 5 Room of Truth")
    ,"Genie 3": AchieveData(5254, "Floor 5 Room of Truth")
    ,"Genie 4": AchieveData(5255, "Floor 5 Room of Truth")
    ,"Genie 5": AchieveData(5256, "Floor 5 Room of Truth")
    ,"Genie 6": AchieveData(5257, "Floor 5 Room of Truth") #Given by Aladdin
    ,"Genie 7": AchieveData(5258, "Floor 5 Room of Truth")
    ,"Genie 8": AchieveData(5259, "Floor 5 Room of Truth")
    ,"Genie 9": AchieveData(5260, "Floor 5 Room of Truth")
    
    ,"Bambi 0": AchieveData(5271, "Floor 10")
    ,"Bambi 1": AchieveData(5272, "Floor 10")
    ,"Bambi 2": AchieveData(5273, "Floor 10")
    ,"Bambi 3": AchieveData(5274, "Floor 10")
    ,"Bambi 4": AchieveData(5275, "Floor 10")
    ,"Bambi 5": AchieveData(5276, "Floor 10")
    ,"Bambi 6": AchieveData(5277, "Floor 10")
    ,"Bambi 7": AchieveData(5278, "Floor 10")
    ,"Bambi 8": AchieveData(5279, "Floor 10")
    ,"Bambi 9": AchieveData(5280, "Floor 10")
    
    ,"Dumbo 0": AchieveData(5281, "Floor 4 Room of Truth")
    ,"Dumbo 1": AchieveData(5282, "Floor 4 Room of Truth")
    ,"Dumbo 2": AchieveData(5283, "Floor 4 Room of Truth")
    ,"Dumbo 3": AchieveData(5284, "Floor 4 Room of Truth")
    ,"Dumbo 4": AchieveData(5285, "Floor 4 Room of Truth")
    ,"Dumbo 5": AchieveData(5286, "Floor 4 Room of Truth")
    ,"Dumbo 6": AchieveData(5287, "Floor 4 Room of Truth")
    ,"Dumbo 7": AchieveData(5288, "Floor 4 Room of Truth")
    ,"Dumbo 8": AchieveData(5289, "Floor 4 Room of Truth")
    ,"Dumbo 9": AchieveData(5290, "Floor 4 Room of Truth")
    
    ,"Tinker Bell 0": AchieveData(5291, "Floor 8 Room of Truth")
    ,"Tinker Bell 1": AchieveData(5292, "Floor 8 Room of Truth")
    ,"Tinker Bell 2": AchieveData(5293, "Floor 8 Room of Truth")
    ,"Tinker Bell 3": AchieveData(5294, "Floor 8 Room of Truth")
    ,"Tinker Bell 4": AchieveData(5295, "Floor 8 Room of Truth") #Given by Peter Pan
    ,"Tinker Bell 5": AchieveData(5296, "Floor 8 Room of Truth")
    ,"Tinker Bell 6": AchieveData(5297, "Floor 8 Room of Truth")
    ,"Tinker Bell 7": AchieveData(5298, "Floor 8 Room of Truth")
    ,"Tinker Bell 8": AchieveData(5299, "Floor 8 Room of Truth")
    ,"Tinker Bell 9": AchieveData(5300, "Floor 8 Room of Truth")
    
    ,"Mushu 0": AchieveData(5301, "Floor 9 Room of Rewards")
    ,"Mushu 1": AchieveData(5302, "Floor 9 Room of Rewards")
    ,"Mushu 2": AchieveData(5303, "Floor 9 Room of Rewards")
    ,"Mushu 3": AchieveData(5304, "Floor 9 Room of Rewards")
    ,"Mushu 4": AchieveData(5305, "Floor 9 Room of Rewards")
    ,"Mushu 5": AchieveData(5306, "Floor 9 Room of Rewards")
    ,"Mushu 6": AchieveData(5307, "Floor 9 Room of Rewards")
    ,"Mushu 7": AchieveData(5308, "Floor 9 Room of Rewards")
    ,"Mushu 8": AchieveData(5309, "Floor 9 Room of Rewards")
    ,"Mushu 9": AchieveData(5310, "Floor 9 Room of Rewards")
    
    ,"Cloud 0": AchieveData(5311, "Floor 3 Room of Truth")
    ,"Cloud 1": AchieveData(5312, "Floor 3 Room of Truth")
    ,"Cloud 2": AchieveData(5313, "Floor 3 Room of Truth")
    ,"Cloud 3": AchieveData(5314, "Floor 3 Room of Truth")
    ,"Cloud 4": AchieveData(5315, "Floor 3 Room of Truth") #Given by Cloud
    ,"Cloud 5": AchieveData(5316, "Floor 3 Room of Truth")
    ,"Cloud 6": AchieveData(5317, "Floor 3 Room of Truth")
    ,"Cloud 7": AchieveData(5318, "Floor 3 Room of Truth")
    ,"Cloud 8": AchieveData(5319, "Floor 3 Room of Truth")
    ,"Cloud 9": AchieveData(5320, "Floor 3 Room of Truth")
    
    ,"Potion 0": AchieveData(5321, "Floor 1")
    ,"Potion 1": AchieveData(5322, "Floor 1")
    ,"Potion 2": AchieveData(5323, "Floor 1")
    ,"Potion 3": AchieveData(5324, "Floor 1")
    ,"Potion 4": AchieveData(5325, "Floor 1")
    ,"Potion 5": AchieveData(5326, "Floor 1")
    ,"Potion 6": AchieveData(5327, "Floor 1")
    ,"Potion 7": AchieveData(5328, "Floor 1")
    ,"Potion 8": AchieveData(5329, "Floor 1")
    ,"Potion 9": AchieveData(5330, "Floor 1")
    
    ,"Hi-Potion 0": AchieveData(5331, "Floor 3 Room of Guidance")
    ,"Hi-Potion 1": AchieveData(5332, "Floor 3 Room of Guidance")
    ,"Hi-Potion 2": AchieveData(5333, "Floor 3 Room of Guidance")
    ,"Hi-Potion 3": AchieveData(5334, "Floor 3 Room of Guidance") #Given by Cloud
    ,"Hi-Potion 4": AchieveData(5335, "Floor 3 Room of Guidance")
    ,"Hi-Potion 5": AchieveData(5336, "Floor 3 Room of Guidance")
    ,"Hi-Potion 6": AchieveData(5337, "Floor 3 Room of Guidance")
    ,"Hi-Potion 7": AchieveData(5338, "Floor 3 Room of Guidance")
    ,"Hi-Potion 8": AchieveData(5339, "Floor 3 Room of Guidance")
    ,"Hi-Potion 9": AchieveData(5340, "Floor 3 Room of Guidance")
    
    ,"Mega-Potion 0": AchieveData(5341, "Floor 11 Room of Guidance")
    ,"Mega-Potion 1": AchieveData(5342, "Floor 11 Room of Guidance")
    ,"Mega-Potion 2": AchieveData(5343, "Floor 11 Room of Guidance") #Obtained from Riku III
    ,"Mega-Potion 3": AchieveData(5344, "Floor 11 Room of Guidance")
    ,"Mega-Potion 4": AchieveData(5345, "Floor 11 Room of Guidance")
    ,"Mega-Potion 5": AchieveData(5346, "Floor 11 Room of Guidance")
    ,"Mega-Potion 6": AchieveData(5347, "Floor 11 Room of Guidance")
    ,"Mega-Potion 7": AchieveData(5348, "Floor 11 Room of Guidance")
    ,"Mega-Potion 8": AchieveData(5349, "Floor 11 Room of Guidance")
    ,"Mega-Potion 9": AchieveData(5350, "Floor 11 Room of Guidance")
    
    ,"Ether 0": AchieveData(5351, "Floor 5 Room of Guidance")
    ,"Ether 1": AchieveData(5352, "Floor 5 Room of Guidance")
    ,"Ether 2": AchieveData(5353, "Floor 5 Room of Guidance")
    ,"Ether 3": AchieveData(5354, "Floor 5 Room of Guidance") #Dropped in Agrabah Room of Guidance
    ,"Ether 4": AchieveData(5355, "Floor 5 Room of Guidance")
    ,"Ether 5": AchieveData(5356, "Floor 5 Room of Guidance")
    ,"Ether 6": AchieveData(5357, "Floor 5 Room of Guidance")
    ,"Ether 7": AchieveData(5358, "Floor 5 Room of Guidance")
    ,"Ether 8": AchieveData(5359, "Floor 5 Room of Guidance")
    ,"Ether 9": AchieveData(5360, "Floor 5 Room of Guidance")
    
    ,"Mega-Ether 0": AchieveData(5361, "Floor 10")
    ,"Mega-Ether 1": AchieveData(5362, "Floor 10")
    ,"Mega-Ether 2": AchieveData(5363, "Floor 10")
    ,"Mega-Ether 3": AchieveData(5364, "Floor 10")
    ,"Mega-Ether 4": AchieveData(5365, "Floor 10") #Dropped by Vexen I
    ,"Mega-Ether 5": AchieveData(5366, "Floor 10")
    ,"Mega-Ether 6": AchieveData(5367, "Floor 10")
    ,"Mega-Ether 7": AchieveData(5368, "Floor 10")
    ,"Mega-Ether 8": AchieveData(5369, "Floor 10")
    ,"Mega-Ether 9": AchieveData(5370, "Floor 10")
    
    ,"Elxir 0": AchieveData(5371, "Floor 10")
    ,"Elxir 1": AchieveData(5372, "Floor 10") #Given by Roo
    ,"Elxir 2": AchieveData(5373, "Floor 10")
    ,"Elxir 3": AchieveData(5374, "Floor 10")
    ,"Elxir 4": AchieveData(5375, "Floor 10")
    ,"Elxir 5": AchieveData(5376, "Floor 10")
    ,"Elxir 6": AchieveData(5377, "Floor 10")
    ,"Elxir 7": AchieveData(5378, "Floor 10")
    ,"Elxir 8": AchieveData(5379, "Floor 10")
    ,"Elxir 9": AchieveData(5380, "Floor 10")
    
    ,"Megalixir 0": AchieveData(5381, "Floor 12 Room of Rewards")
    ,"Megalixir 1": AchieveData(5382, "Floor 12 Room of Rewards")
    ,"Megalixir 2": AchieveData(5383, "Floor 12 Room of Rewards")
    ,"Megalixir 3": AchieveData(5384, "Floor 12 Room of Rewards")
    ,"Megalixir 4": AchieveData(5385, "Floor 12 Room of Rewards")
    ,"Megalixir 5": AchieveData(5386, "Floor 12 Room of Rewards")
    ,"Megalixir 6": AchieveData(5387, "Floor 12 Room of Rewards")
    ,"Megalixir 7": AchieveData(5388, "Floor 12 Room of Rewards")
    ,"Megalixir 8": AchieveData(5389, "Floor 12 Room of Rewards")
    ,"Megalixir 9": AchieveData(5390, "Floor 12 Room of Rewards")
    
    #Premium Battle Cards
    ,"Premium Kingdom Key 0": AchieveData(6001, "Floor 1")
    ,"Premium Kingdom Key 1": AchieveData(6002, "Floor 1")
    ,"Premium Kingdom Key 2": AchieveData(6003, "Floor 1")
    ,"Premium Kingdom Key 3": AchieveData(6004, "Floor 1")
    ,"Premium Kingdom Key 4": AchieveData(6005, "Floor 1")
    ,"Premium Kingdom Key 5": AchieveData(6006, "Floor 1")
    ,"Premium Kingdom Key 6": AchieveData(6007, "Floor 1")
    ,"Premium Kingdom Key 7": AchieveData(6008, "Floor 1")
    ,"Premium Kingdom Key 8": AchieveData(6009, "Floor 1")
    ,"Premium Kingdom Key 9": AchieveData(6010, "Floor 1")
    
    ,"Premium Three Wishes 0": AchieveData(6011, "Floor 5")
    ,"Premium Three Wishes 1": AchieveData(6012, "Floor 5")
    ,"Premium Three Wishes 2": AchieveData(6013, "Floor 5")
    ,"Premium Three Wishes 3": AchieveData(6014, "Floor 5")
    ,"Premium Three Wishes 4": AchieveData(6015, "Floor 5")
    ,"Premium Three Wishes 5": AchieveData(6016, "Floor 5")
    ,"Premium Three Wishes 6": AchieveData(6017, "Floor 5")
    ,"Premium Three Wishes 7": AchieveData(6018, "Floor 5")
    ,"Premium Three Wishes 8": AchieveData(6019, "Floor 5")
    ,"Premium Three Wishes 9": AchieveData(6020, "Floor 5")
    
    ,"Premium Crabclaw 0": AchieveData(6021, "Floor 7")
    ,"Premium Crabclaw 1": AchieveData(6022, "Floor 7")
    ,"Premium Crabclaw 2": AchieveData(6023, "Floor 7")
    ,"Premium Crabclaw 3": AchieveData(6024, "Floor 7")
    ,"Premium Crabclaw 4": AchieveData(6025, "Floor 7")
    ,"Premium Crabclaw 5": AchieveData(6026, "Floor 7")
    ,"Premium Crabclaw 6": AchieveData(6027, "Floor 7")
    ,"Premium Crabclaw 7": AchieveData(6028, "Floor 7")
    ,"Premium Crabclaw 8": AchieveData(6029, "Floor 7")
    ,"Premium Crabclaw 9": AchieveData(6030, "Floor 7")
    
    ,"Premium Pumpkinhead 0": AchieveData(6031, "Floor 6")
    ,"Premium Pumpkinhead 1": AchieveData(6032, "Floor 6")
    ,"Premium Pumpkinhead 2": AchieveData(6033, "Floor 6")
    ,"Premium Pumpkinhead 3": AchieveData(6034, "Floor 6")
    ,"Premium Pumpkinhead 4": AchieveData(6035, "Floor 6")
    ,"Premium Pumpkinhead 5": AchieveData(6036, "Floor 6")
    ,"Premium Pumpkinhead 6": AchieveData(6037, "Floor 6")
    ,"Premium Pumpkinhead 7": AchieveData(6038, "Floor 6")
    ,"Premium Pumpkinhead 8": AchieveData(6039, "Floor 6")
    ,"Premium Pumpkinhead 9": AchieveData(6040, "Floor 6")
    
    ,"Premium Fairy Harp 0": AchieveData(6041, "Floor 8")
    ,"Premium Fairy Harp 1": AchieveData(6042, "Floor 8")
    ,"Premium Fairy Harp 2": AchieveData(6043, "Floor 8")
    ,"Premium Fairy Harp 3": AchieveData(6044, "Floor 8")
    ,"Premium Fairy Harp 4": AchieveData(6045, "Floor 8")
    ,"Premium Fairy Harp 5": AchieveData(6046, "Floor 8")
    ,"Premium Fairy Harp 6": AchieveData(6047, "Floor 8")
    ,"Premium Fairy Harp 7": AchieveData(6048, "Floor 8")
    ,"Premium Fairy Harp 8": AchieveData(6049, "Floor 8")
    ,"Premium Fairy Harp 9": AchieveData(6050, "Floor 8")
    
    ,"Premium Wishing Star 0": AchieveData(6051, "Floor 4")
    ,"Premium Wishing Star 1": AchieveData(6052, "Floor 4")
    ,"Premium Wishing Star 2": AchieveData(6053, "Floor 4")
    ,"Premium Wishing Star 3": AchieveData(6054, "Floor 4")
    ,"Premium Wishing Star 4": AchieveData(6055, "Floor 4")
    ,"Premium Wishing Star 5": AchieveData(6056, "Floor 4")
    ,"Premium Wishing Star 6": AchieveData(6057, "Floor 4")
    ,"Premium Wishing Star 7": AchieveData(6058, "Floor 4")
    ,"Premium Wishing Star 8": AchieveData(6059, "Floor 4")
    ,"Premium Wishing Star 9": AchieveData(6060, "Floor 4")
    
    ,"Premium Spellbinder 0": AchieveData(6061, "Floor 10")
    ,"Premium Spellbinder 1": AchieveData(6062, "Floor 10")
    ,"Premium Spellbinder 2": AchieveData(6063, "Floor 10")
    ,"Premium Spellbinder 3": AchieveData(6064, "Floor 10")
    ,"Premium Spellbinder 4": AchieveData(6065, "Floor 10")
    ,"Premium Spellbinder 5": AchieveData(6066, "Floor 10")
    ,"Premium Spellbinder 6": AchieveData(6067, "Floor 10")
    ,"Premium Spellbinder 7": AchieveData(6068, "Floor 10")
    ,"Premium Spellbinder 8": AchieveData(6069, "Floor 10")
    ,"Premium Spellbinder 9": AchieveData(6070, "Floor 10")
    
    ,"Premium Metal Chocobo 0": AchieveData(6071, "Floor 3 Room of Rewards")
    ,"Premium Metal Chocobo 1": AchieveData(6072, "Floor 3 Room of Rewards")
    ,"Premium Metal Chocobo 2": AchieveData(6073, "Floor 3 Room of Rewards")
    ,"Premium Metal Chocobo 3": AchieveData(6074, "Floor 3 Room of Rewards")
    ,"Premium Metal Chocobo 4": AchieveData(6075, "Floor 3 Room of Rewards")
    ,"Premium Metal Chocobo 5": AchieveData(6076, "Floor 3 Room of Rewards")
    ,"Premium Metal Chocobo 6": AchieveData(6077, "Floor 3 Room of Rewards")
    ,"Premium Metal Chocobo 7": AchieveData(6078, "Floor 3 Room of Rewards")
    ,"Premium Metal Chocobo 8": AchieveData(6079, "Floor 3 Room of Rewards")
    ,"Premium Metal Chocobo 9": AchieveData(6080, "Floor 3 Room of Rewards")
    
    ,"Premium Olympia 0": AchieveData(6081, "Floor 3")
    ,"Premium Olympia 1": AchieveData(6082, "Floor 3")
    ,"Premium Olympia 2": AchieveData(6083, "Floor 3")
    ,"Premium Olympia 3": AchieveData(6084, "Floor 3")
    ,"Premium Olympia 4": AchieveData(6085, "Floor 3")
    ,"Premium Olympia 5": AchieveData(6086, "Floor 3")
    ,"Premium Olympia 6": AchieveData(6087, "Floor 3")
    ,"Premium Olympia 7": AchieveData(6088, "Floor 3")
    ,"Premium Olympia 8": AchieveData(6089, "Floor 3")
    ,"Premium Olympia 9": AchieveData(6090, "Floor 3")
    
    ,"Premium Lionheart 0": AchieveData(6091, "Floor 1 Room of Rewards")
    ,"Premium Lionheart 1": AchieveData(6092, "Floor 1 Room of Rewards")
    ,"Premium Lionheart 2": AchieveData(6093, "Floor 1 Room of Rewards")
    ,"Premium Lionheart 3": AchieveData(6094, "Floor 1 Room of Rewards")
    ,"Premium Lionheart 4": AchieveData(6095, "Floor 1 Room of Rewards")
    ,"Premium Lionheart 5": AchieveData(6096, "Floor 1 Room of Rewards")
    ,"Premium Lionheart 6": AchieveData(6097, "Floor 1 Room of Rewards")
    ,"Premium Lionheart 7": AchieveData(6098, "Floor 1 Room of Rewards")
    ,"Premium Lionheart 8": AchieveData(6099, "Floor 1 Room of Rewards")
    ,"Premium Lionheart 9": AchieveData(6100, "Floor 1 Room of Rewards")
    
    ,"Premium Lady Luck 0": AchieveData(6101, "Floor 2")
    ,"Premium Lady Luck 1": AchieveData(6102, "Floor 2")
    ,"Premium Lady Luck 2": AchieveData(6103, "Floor 2")
    ,"Premium Lady Luck 3": AchieveData(6104, "Floor 2")
    ,"Premium Lady Luck 4": AchieveData(6105, "Floor 2")
    ,"Premium Lady Luck 5": AchieveData(6106, "Floor 2")
    ,"Premium Lady Luck 6": AchieveData(6107, "Floor 2")
    ,"Premium Lady Luck 7": AchieveData(6108, "Floor 2")
    ,"Premium Lady Luck 8": AchieveData(6109, "Floor 2")
    ,"Premium Lady Luck 9": AchieveData(6110, "Floor 2")
    
    ,"Premium Divine Rose 0": AchieveData(6111, "Floor 9")
    ,"Premium Divine Rose 1": AchieveData(6112, "Floor 9")
    ,"Premium Divine Rose 2": AchieveData(6113, "Floor 9")
    ,"Premium Divine Rose 3": AchieveData(6114, "Floor 9")
    ,"Premium Divine Rose 4": AchieveData(6115, "Floor 9")
    ,"Premium Divine Rose 5": AchieveData(6116, "Floor 9")
    ,"Premium Divine Rose 6": AchieveData(6117, "Floor 9")
    ,"Premium Divine Rose 7": AchieveData(6118, "Floor 9")
    ,"Premium Divine Rose 8": AchieveData(6119, "Floor 9")
    ,"Premium Divine Rose 9": AchieveData(6120, "Floor 9")
    
    ,"Premium Oathkeeper 0": AchieveData(6121, "Floor 13")
    ,"Premium Oathkeeper 1": AchieveData(6122, "Floor 13")
    ,"Premium Oathkeeper 2": AchieveData(6123, "Floor 13")
    ,"Premium Oathkeeper 3": AchieveData(6124, "Floor 13")
    ,"Premium Oathkeeper 4": AchieveData(6125, "Floor 13")
    ,"Premium Oathkeeper 5": AchieveData(6126, "Floor 13")
    ,"Premium Oathkeeper 6": AchieveData(6127, "Floor 13")
    ,"Premium Oathkeeper 7": AchieveData(6128, "Floor 13")
    ,"Premium Oathkeeper 8": AchieveData(6129, "Floor 13")
    ,"Premium Oathkeeper 9": AchieveData(6130, "Floor 13")
    
    ,"Premium Oblivion 0": AchieveData(6131, "Floor 13")
    ,"Premium Oblivion 1": AchieveData(6132, "Floor 13")
    ,"Premium Oblivion 2": AchieveData(6133, "Floor 13")
    ,"Premium Oblivion 3": AchieveData(6134, "Floor 13")
    ,"Premium Oblivion 4": AchieveData(6135, "Floor 13")
    ,"Premium Oblivion 5": AchieveData(6136, "Floor 13")
    ,"Premium Oblivion 6": AchieveData(6137, "Floor 13")
    ,"Premium Oblivion 7": AchieveData(6138, "Floor 13")
    ,"Premium Oblivion 8": AchieveData(6139, "Floor 13")
    ,"Premium Oblivion 9": AchieveData(6140, "Floor 13")
    
    ,"Premium Diamond Dust 0": AchieveData(6141, "Floor 13 Room of Guidance")
    ,"Premium Diamond Dust 1": AchieveData(6142, "Floor 13 Room of Guidance")
    ,"Premium Diamond Dust 2": AchieveData(6143, "Floor 13 Room of Guidance")
    ,"Premium Diamond Dust 3": AchieveData(6144, "Floor 13 Room of Guidance")
    ,"Premium Diamond Dust 4": AchieveData(6145, "Floor 13 Room of Guidance")
    ,"Premium Diamond Dust 5": AchieveData(6146, "Floor 13 Room of Guidance")
    ,"Premium Diamond Dust 6": AchieveData(6147, "Floor 13 Room of Guidance")
    ,"Premium Diamond Dust 7": AchieveData(6148, "Floor 13 Room of Guidance")
    ,"Premium Diamond Dust 8": AchieveData(6149, "Floor 13 Room of Guidance")
    ,"Premium Diamond Dust 9": AchieveData(6150, "Floor 13 Room of Guidance")
    
    ,"Premium One Winged Angel 0": AchieveData(6151, "Floor 13 Room of Guidance")
    ,"Premium One Winged Angel 1": AchieveData(6152, "Floor 13 Room of Guidance")
    ,"Premium One Winged Angel 2": AchieveData(6153, "Floor 13 Room of Guidance")
    ,"Premium One Winged Angel 3": AchieveData(6154, "Floor 13 Room of Guidance")
    ,"Premium One Winged Angel 4": AchieveData(6155, "Floor 13 Room of Guidance")
    ,"Premium One Winged Angel 5": AchieveData(6156, "Floor 13 Room of Guidance")
    ,"Premium One Winged Angel 6": AchieveData(6157, "Floor 13 Room of Guidance")
    ,"Premium One Winged Angel 7": AchieveData(6158, "Floor 13 Room of Guidance")
    ,"Premium One Winged Angel 8": AchieveData(6159, "Floor 13 Room of Guidance")
    ,"Premium One Winged Angel 9": AchieveData(6160, "Floor 13 Room of Guidance")
    
    ,"Premium Ultima Weapon 0": AchieveData(6161, "Floor 13")
    ,"Premium Ultima Weapon 1": AchieveData(6162, "Floor 13")
    ,"Premium Ultima Weapon 2": AchieveData(6163, "Floor 13")
    ,"Premium Ultima Weapon 3": AchieveData(6164, "Floor 13")
    ,"Premium Ultima Weapon 4": AchieveData(6165, "Floor 13")
    ,"Premium Ultima Weapon 5": AchieveData(6166, "Floor 13")
    ,"Premium Ultima Weapon 6": AchieveData(6167, "Floor 13")
    ,"Premium Ultima Weapon 7": AchieveData(6168, "Floor 13")
    ,"Premium Ultima Weapon 8": AchieveData(6169, "Floor 13")
    ,"Premium Ultima Weapon 9": AchieveData(6170, "Floor 13")
    
    ,"Premium Fire 0": AchieveData(6171, "Floor 1 Room of Truth")
    ,"Premium Fire 1": AchieveData(6172, "Floor 1 Room of Truth")
    ,"Premium Fire 2": AchieveData(6173, "Floor 1 Room of Truth")
    ,"Premium Fire 3": AchieveData(6174, "Floor 1 Room of Truth")
    ,"Premium Fire 4": AchieveData(6175, "Floor 1 Room of Truth")
    ,"Premium Fire 5": AchieveData(6176, "Floor 1 Room of Truth")
    ,"Premium Fire 6": AchieveData(6177, "Floor 1 Room of Truth")
    ,"Premium Fire 7": AchieveData(6178, "Floor 1 Room of Truth")
    ,"Premium Fire 8": AchieveData(6179, "Floor 1 Room of Truth")
    ,"Premium Fire 9": AchieveData(6180, "Floor 1 Room of Truth")
    
    ,"Premium Blizzard 0": AchieveData(6181, "Floor 1")
    ,"Premium Blizzard 1": AchieveData(6182, "Floor 1")
    ,"Premium Blizzard 2": AchieveData(6183, "Floor 1")
    ,"Premium Blizzard 3": AchieveData(6184, "Floor 1")
    ,"Premium Blizzard 4": AchieveData(6185, "Floor 1")
    ,"Premium Blizzard 5": AchieveData(6186, "Floor 1")
    ,"Premium Blizzard 6": AchieveData(6187, "Floor 1")
    ,"Premium Blizzard 7": AchieveData(6188, "Floor 1")
    ,"Premium Blizzard 8": AchieveData(6189, "Floor 1")
    ,"Premium Blizzard 9": AchieveData(6190, "Floor 1")
    
    ,"Premium Thunder 0": AchieveData(6191, "Floor 6 Room of Truth")
    ,"Premium Thunder 1": AchieveData(6192, "Floor 6 Room of Truth")
    ,"Premium Thunder 2": AchieveData(6193, "Floor 6 Room of Truth")
    ,"Premium Thunder 3": AchieveData(6194, "Floor 6 Room of Truth")
    ,"Premium Thunder 4": AchieveData(6195, "Floor 6 Room of Truth")
    ,"Premium Thunder 5": AchieveData(6196, "Floor 6 Room of Truth")
    ,"Premium Thunder 6": AchieveData(6197, "Floor 6 Room of Truth")
    ,"Premium Thunder 7": AchieveData(6198, "Floor 6 Room of Truth")
    ,"Premium Thunder 8": AchieveData(6199, "Floor 6 Room of Truth")
    ,"Premium Thunder 9": AchieveData(6200, "Floor 6 Room of Truth")
    
    ,"Premium Cure 0": AchieveData(6201, "Floor 1")
    ,"Premium Cure 1": AchieveData(6202, "Floor 1")
    ,"Premium Cure 2": AchieveData(6203, "Floor 1")
    ,"Premium Cure 3": AchieveData(6204, "Floor 1")
    ,"Premium Cure 4": AchieveData(6205, "Floor 1")
    ,"Premium Cure 5": AchieveData(6206, "Floor 1")
    ,"Premium Cure 6": AchieveData(6207, "Floor 1")
    ,"Premium Cure 7": AchieveData(6208, "Floor 1")
    ,"Premium Cure 8": AchieveData(6209, "Floor 1")
    ,"Premium Cure 9": AchieveData(6210, "Floor 1")
    
    ,"Premium Gravity 0": AchieveData(6211, "Floor 5")
    ,"Premium Gravity 1": AchieveData(6212, "Floor 5")
    ,"Premium Gravity 2": AchieveData(6213, "Floor 5")
    ,"Premium Gravity 3": AchieveData(6214, "Floor 5")
    ,"Premium Gravity 4": AchieveData(6215, "Floor 5")
    ,"Premium Gravity 5": AchieveData(6216, "Floor 5")
    ,"Premium Gravity 6": AchieveData(6217, "Floor 5")
    ,"Premium Gravity 7": AchieveData(6218, "Floor 5")
    ,"Premium Gravity 8": AchieveData(6219, "Floor 5")
    ,"Premium Gravity 9": AchieveData(6220, "Floor 5")
    
    ,"Premium Stop 0": AchieveData(6221, "Floor 2")
    ,"Premium Stop 1": AchieveData(6222, "Floor 2")
    ,"Premium Stop 2": AchieveData(6223, "Floor 2")
    ,"Premium Stop 3": AchieveData(6224, "Floor 2")
    ,"Premium Stop 4": AchieveData(6225, "Floor 2")
    ,"Premium Stop 5": AchieveData(6226, "Floor 2")
    ,"Premium Stop 6": AchieveData(6227, "Floor 2")
    ,"Premium Stop 7": AchieveData(6228, "Floor 2")
    ,"Premium Stop 8": AchieveData(6229, "Floor 2")
    ,"Premium Stop 9": AchieveData(6230, "Floor 2")
    
    ,"Premium Aero 0": AchieveData(6231, "Floor 7 Room of Truth")
    ,"Premium Aero 1": AchieveData(6232, "Floor 7 Room of Truth")
    ,"Premium Aero 2": AchieveData(6233, "Floor 7 Room of Truth")
    ,"Premium Aero 3": AchieveData(6234, "Floor 7 Room of Truth")
    ,"Premium Aero 4": AchieveData(6235, "Floor 7 Room of Truth")
    ,"Premium Aero 5": AchieveData(6236, "Floor 7 Room of Truth")
    ,"Premium Aero 6": AchieveData(6237, "Floor 7 Room of Truth")
    ,"Premium Aero 7": AchieveData(6238, "Floor 7 Room of Truth")
    ,"Premium Aero 8": AchieveData(6239, "Floor 7 Room of Truth")
    ,"Premium Aero 9": AchieveData(6240, "Floor 7 Room of Truth")
    
    ,"Premium Simba 0": AchieveData(6241, "Floor 1 Room of Beginnings")
    ,"Premium Simba 1": AchieveData(6242, "Floor 1 Room of Beginnings")
    ,"Premium Simba 2": AchieveData(6243, "Floor 1 Room of Beginnings")
    ,"Premium Simba 3": AchieveData(6244, "Floor 1 Room of Beginnings")
    ,"Premium Simba 4": AchieveData(6245, "Floor 1 Room of Beginnings")
    ,"Premium Simba 5": AchieveData(6246, "Floor 1 Room of Beginnings")
    ,"Premium Simba 6": AchieveData(6247, "Floor 1 Room of Beginnings")
    ,"Premium Simba 7": AchieveData(6248, "Floor 1 Room of Beginnings")
    ,"Premium Simba 8": AchieveData(6249, "Floor 1 Room of Beginnings")
    ,"Premium Simba 9": AchieveData(6250, "Floor 1 Room of Beginnings")
    
    ,"Premium Genie 0": AchieveData(6251, "Floor 5 Room of Truth")
    ,"Premium Genie 1": AchieveData(6252, "Floor 5 Room of Truth")
    ,"Premium Genie 2": AchieveData(6253, "Floor 5 Room of Truth")
    ,"Premium Genie 3": AchieveData(6254, "Floor 5 Room of Truth")
    ,"Premium Genie 4": AchieveData(6255, "Floor 5 Room of Truth")
    ,"Premium Genie 5": AchieveData(6256, "Floor 5 Room of Truth")
    ,"Premium Genie 6": AchieveData(6257, "Floor 5 Room of Truth")
    ,"Premium Genie 7": AchieveData(6258, "Floor 5 Room of Truth")
    ,"Premium Genie 8": AchieveData(6259, "Floor 5 Room of Truth")
    ,"Premium Genie 9": AchieveData(6260, "Floor 5 Room of Truth")
    
    ,"Premium Genie 0": AchieveData(6261, "Floor 10")
    ,"Premium Genie 1": AchieveData(6262, "Floor 10")
    ,"Premium Genie 2": AchieveData(6263, "Floor 10")
    ,"Premium Genie 3": AchieveData(6264, "Floor 10")
    ,"Premium Genie 4": AchieveData(6265, "Floor 10")
    ,"Premium Genie 5": AchieveData(6266, "Floor 10")
    ,"Premium Genie 6": AchieveData(6267, "Floor 10")
    ,"Premium Genie 7": AchieveData(6268, "Floor 10")
    ,"Premium Genie 8": AchieveData(6269, "Floor 10")
    ,"Premium Genie 9": AchieveData(6270, "Floor 10")
    
    ,"Premium Bambi 0": AchieveData(6271, "Floor 8 Room of Truth")
    ,"Premium Bambi 1": AchieveData(6272, "Floor 8 Room of Truth")
    ,"Premium Bambi 2": AchieveData(6273, "Floor 8 Room of Truth")
    ,"Premium Bambi 3": AchieveData(6274, "Floor 8 Room of Truth")
    ,"Premium Bambi 4": AchieveData(6275, "Floor 8 Room of Truth")
    ,"Premium Bambi 5": AchieveData(6276, "Floor 8 Room of Truth")
    ,"Premium Bambi 6": AchieveData(6277, "Floor 8 Room of Truth")
    ,"Premium Bambi 7": AchieveData(6278, "Floor 8 Room of Truth")
    ,"Premium Bambi 8": AchieveData(6279, "Floor 8 Room of Truth")
    ,"Premium Bambi 9": AchieveData(6280, "Floor 8 Room of Truth")
    
    ,"Premium Dumbo 0": AchieveData(6281, "Floor 4 Room of Truth")
    ,"Premium Dumbo 1": AchieveData(6282, "Floor 4 Room of Truth")
    ,"Premium Dumbo 2": AchieveData(6283, "Floor 4 Room of Truth")
    ,"Premium Dumbo 3": AchieveData(6284, "Floor 4 Room of Truth")
    ,"Premium Dumbo 4": AchieveData(6285, "Floor 4 Room of Truth")
    ,"Premium Dumbo 5": AchieveData(6286, "Floor 4 Room of Truth")
    ,"Premium Dumbo 6": AchieveData(6287, "Floor 4 Room of Truth")
    ,"Premium Dumbo 7": AchieveData(6288, "Floor 4 Room of Truth")
    ,"Premium Dumbo 8": AchieveData(6289, "Floor 4 Room of Truth")
    ,"Premium Dumbo 9": AchieveData(6290, "Floor 4 Room of Truth")
    
    ,"Premium Tinker Bell 0": AchieveData(6291, "Floor 8 Room of Truth")
    ,"Premium Tinker Bell 1": AchieveData(6292, "Floor 8 Room of Truth")
    ,"Premium Tinker Bell 2": AchieveData(6293, "Floor 8 Room of Truth")
    ,"Premium Tinker Bell 3": AchieveData(6294, "Floor 8 Room of Truth")
    ,"Premium Tinker Bell 4": AchieveData(6295, "Floor 8 Room of Truth")
    ,"Premium Tinker Bell 5": AchieveData(6296, "Floor 8 Room of Truth")
    ,"Premium Tinker Bell 6": AchieveData(6297, "Floor 8 Room of Truth")
    ,"Premium Tinker Bell 7": AchieveData(6298, "Floor 8 Room of Truth")
    ,"Premium Tinker Bell 8": AchieveData(6299, "Floor 8 Room of Truth")
    ,"Premium Tinker Bell 9": AchieveData(6300, "Floor 8 Room of Truth")
    
    ,"Premium Mushu 0": AchieveData(6301, "Floor 9 Room of Rewards")
    ,"Premium Mushu 1": AchieveData(6302, "Floor 9 Room of Rewards")
    ,"Premium Mushu 2": AchieveData(6303, "Floor 9 Room of Rewards")
    ,"Premium Mushu 3": AchieveData(6304, "Floor 9 Room of Rewards")
    ,"Premium Mushu 4": AchieveData(6305, "Floor 9 Room of Rewards")
    ,"Premium Mushu 5": AchieveData(6306, "Floor 9 Room of Rewards")
    ,"Premium Mushu 6": AchieveData(6307, "Floor 9 Room of Rewards")
    ,"Premium Mushu 7": AchieveData(6308, "Floor 9 Room of Rewards")
    ,"Premium Mushu 8": AchieveData(6309, "Floor 9 Room of Rewards")
    ,"Premium Mushu 9": AchieveData(6310, "Floor 9 Room of Rewards")
    
    ,"Premium Cloud 0": AchieveData(6311, "Floor 3 Room of Truth")
    ,"Premium Cloud 1": AchieveData(6312, "Floor 3 Room of Truth")
    ,"Premium Cloud 2": AchieveData(6313, "Floor 3 Room of Truth")
    ,"Premium Cloud 3": AchieveData(6314, "Floor 3 Room of Truth")
    ,"Premium Cloud 4": AchieveData(6315, "Floor 3 Room of Truth")
    ,"Premium Cloud 5": AchieveData(6316, "Floor 3 Room of Truth")
    ,"Premium Cloud 6": AchieveData(6317, "Floor 3 Room of Truth")
    ,"Premium Cloud 7": AchieveData(6318, "Floor 3 Room of Truth")
    ,"Premium Cloud 8": AchieveData(6319, "Floor 3 Room of Truth")
    ,"Premium Cloud 9": AchieveData(6320, "Floor 3 Room of Truth")
    
    #Enemy Battle Cards
    ,"Shadow": AchieveData(7001, "Floor 1")
    ,"Soldier": AchieveData(7002, "Floor 1")
    ,"Large Body": AchieveData(7003, "Floor 2")
    ,"Red Nocturne": AchieveData(7004, "Floor 2")
    ,"Blue Rhapsody": AchieveData(7005, "Floor 3")
    ,"Yellow Opera": AchieveData(7006, "Floor 3")
    ,"Green Requiem": AchieveData(7007, "Floor 3")
    ,"Powerwild": AchieveData(7008, "Floor 3")
    ,"Bouncywild": AchieveData(7009, "Floor 3")
    ,"Air Soldier": AchieveData(7010, "Floor 4")
    ,"Bandit": AchieveData(7011, "Floor 5")
    ,"Fat Bandit": AchieveData(7012, "Floor 5")
    ,"Barrel Spider": AchieveData(7013, "Floor 3")
    ,"Search Ghost": AchieveData(7014, "Floor 4")
    ,"Sea Neon": AchieveData(7015, "Floor 7")
    ,"Screwdriver": AchieveData(7016, "Floor 7")
    ,"Aquatank": AchieveData(7017, "Floor 7")
    ,"Wight Knight": AchieveData(7018, "Floor 6")
    ,"Gargoyle": AchieveData(7019, "Floor 6")
    ,"Pirate": AchieveData(7020, "Floor 8")
    ,"Air Pirate": AchieveData(7021, "Floor 8")
    ,"Darkball": AchieveData(7022, "Floor 9")
    ,"Defender": AchieveData(7023, "Floor 9")
    ,"Wyvern": AchieveData(7024, "Floor 9")
    ,"Wizard": AchieveData(7050, "Floor 9")
    ,"Neoshadow": AchieveData(7025, "Floor 13")
    ,"White Mushroom": AchieveData(7026, "Floor 7")
    ,"Black Fungus": AchieveData(7027, "Floor 1")
    ,"Creeper Plant": AchieveData(7028, "Floor 2")
    ,"Tornado Step": AchieveData(7029, "Floor 4")
    ,"Crescendo": AchieveData(7030, "Floor 2")
    ,"Guard Armor": AchieveData(7031, "Floor 1 Room of Truth")
    ,"Parasite Cage": AchieveData(7032, "Floor 4 Room of Guidance")
    ,"Trickmaster": AchieveData(7033, "Floor 2 Room of Truth")
    ,"Darkside": AchieveData(7034, "Floor 11 Room of Guidance")
    ,"Card Soldier (Red)": AchieveData(7035, "Floor 2 Room of Beginnings")
    ,"Card Soldier (Black)": AchieveData(7036, "Floor 2 Room of Beginnings")
    ,"Hades": AchieveData(7037, "Floor 3 Room of Truth")
    ,"Jafar": AchieveData(7039, "Floor 5 Room of Truth")
    ,"Oogie Boogie": AchieveData(7040, "Floor 6 Room of Truth")
    ,"Ursula": AchieveData(7041, "Floor 7 Room of Truth")
    ,"Hook": AchieveData(7042, "Floor 8 Room of Truth")
    ,"Dragon Maleficent": AchieveData(7043, "Floor 9 Room of Truth")
    ,"Riku" AchieveData(7051, "Floor 12 Room of Guidance")
    ,"Axel": AchieveData(7044, "Floor 13 Room of Beginnings")
    ,"Larxene": AchieveData(7045, "Floor 12 Room of Guidance")
    ,"Vexen": AchieveData(7046, "Floor 11 Room of Beginnings")
    ,"Marluxia": AchieveData(7047, "Floor 13 Room of Beginnings")
    
    #Gold Map Cards
    ,"Key of Beginnings F01": AchieveData(8001, "Floor 1 Start Room")
    ,"Key of Beginnings F02": AchieveData(8002, "Floor 2 Start Room")
    ,"Key of Beginnings F03": AchieveData(8003, "Floor 3 Start Room")
    ,"Key of Beginnings F04": AchieveData(8004, "Floor 4 Start Room")
    ,"Key of Beginnings F05": AchieveData(8005, "Floor 5 Start Room")
    ,"Key of Beginnings F06": AchieveData(8006, "Floor 6 Start Room")
    ,"Key of Beginnings F07": AchieveData(8007, "Floor 7 Start Room")
    ,"Key of Beginnings F08": AchieveData(8008, "Floor 8 Start Room")
    ,"Key of Beginnings F09": AchieveData(8009, "Floor 9 Start Room")
    ,"Key of Beginnings F11": AchieveData(8011, "Floor 11 Start Room")
    ,"Key of Beginnings F12": AchieveData(8012, "Floor 12 Start Room")
    ,"Key of Beginnings F13": AchieveData(8013, "Floor 13 Start Room")
    
    ,"Key of Guidance F01": AchieveData(8101, "Floor 1 Room of Beginnings")
    ,"Key of Guidance F02": AchieveData(8102, "Floor 2 Room of Beginnings")
    ,"Key of Guidance F03": AchieveData(8103, "Floor 3 Room of Beginnings")
    ,"Key of Guidance F04": AchieveData(8104, "Floor 4 Room of Beginnings")
    ,"Key of Guidance F05": AchieveData(8105, "Floor 5 Room of Beginnings")
    ,"Key of Guidance F06": AchieveData(8106, "Floor 6 Room of Beginnings")
    ,"Key of Guidance F07": AchieveData(8107, "Floor 7 Room of Beginnings")
    ,"Key of Guidance F08": AchieveData(8108, "Floor 8 Room of Beginnings")
    ,"Key of Guidance F09": AchieveData(8109, "Floor 9 Room of Beginnings")
    ,"Key of Guidance F12": AchieveData(8112, "Floor 12 Room of Beginnings")
    ,"Key of Guidance F13": AchieveData(8113, "Floor 13 Room of Beginnings")
    
    ,"Key to Truth F01": AchieveData(8201, "Floor 1 Room of Guidance")
    ,"Key to Truth F02": AchieveData(8202, "Floor 2 Room of Guidance")
    ,"Key to Truth F03": AchieveData(8203, "Floor 3 Room of Guidance")
    ,"Key to Truth F04": AchieveData(8204, "Floor 4 Room of Guidance")
    ,"Key to Truth F05": AchieveData(8205, "Floor 5 Room of Guidance")
    ,"Key to Truth F06": AchieveData(8206, "Floor 6 Room of Guidance")
    ,"Key to Truth F07": AchieveData(8207, "Floor 7 Room of Guidance")
    ,"Key to Truth F08": AchieveData(8208, "Floor 8 Room of Guidance")
    ,"Key to Truth F09": AchieveData(8209, "Floor 9 Room of Guidance")
    ,"Key to Truth F13": AchieveData(8213, "Floor 13 Room of Guidance")
}

exclusion_table = {
    ,"battle cards": {
        "Kingdom Key 0"
        ,"Kingdom Key 1"
        ,"Kingdom Key 2"
        ,"Kingdom Key 3"
        ,"Kingdom Key 4"
        ,"Kingdom Key 5"
        ,"Kingdom Key 6"
        ,"Kingdom Key 7"
        ,"Kingdom Key 8"
        ,"Kingdom Key 9"
        ,"Three Wishes 0"
        ,"Three Wishes 1"
        ,"Three Wishes 2"
        ,"Three Wishes 3"
        ,"Three Wishes 4"
        ,"Three Wishes 5"
        ,"Three Wishes 6"
        ,"Three Wishes 7"
        ,"Three Wishes 8"
        ,"Three Wishes 9"
        ,"Crabclaw 0"
        ,"Crabclaw 1"
        ,"Crabclaw 2"
        ,"Crabclaw 3"
        ,"Crabclaw 4"
        ,"Crabclaw 5"
        ,"Crabclaw 6"
        ,"Crabclaw 7"
        ,"Crabclaw 8"
        ,"Crabclaw 9"
        ,"Pumpkinhead 0"
        ,"Pumpkinhead 1"
        ,"Pumpkinhead 2"
        ,"Pumpkinhead 3"
        ,"Pumpkinhead 4"
        ,"Pumpkinhead 5"
        ,"Pumpkinhead 6"
        ,"Pumpkinhead 7"
        ,"Pumpkinhead 8"
        ,"Pumpkinhead 9"
        ,"Fairy Harp 0"
        ,"Fairy Harp 1"
        ,"Fairy Harp 2"
        ,"Fairy Harp 3"
        ,"Fairy Harp 4"
        ,"Fairy Harp 5"
        ,"Fairy Harp 6"
        ,"Fairy Harp 7"
        ,"Fairy Harp 8"
        ,"Fairy Harp 9"
        ,"Wishing Star 0"
        ,"Wishing Star 1"
        ,"Wishing Star 2"
        ,"Wishing Star 3"
        ,"Wishing Star 4"
        ,"Wishing Star 5"
        ,"Wishing Star 6"
        ,"Wishing Star 7"
        ,"Wishing Star 8"
        ,"Wishing Star 9"
        ,"Spellbinder 0"
        ,"Spellbinder 1"
        ,"Spellbinder 2"
        ,"Spellbinder 3"
        ,"Spellbinder 4"
        ,"Spellbinder 5"
        ,"Spellbinder 6"
        ,"Spellbinder 7"
        ,"Spellbinder 8"
        ,"Spellbinder 9"
        ,"Metal Chocobo 0"
        ,"Metal Chocobo 1"
        ,"Metal Chocobo 2"
        ,"Metal Chocobo 3"
        ,"Metal Chocobo 4"
        ,"Metal Chocobo 5"
        ,"Metal Chocobo 6"
        ,"Metal Chocobo 7"
        ,"Metal Chocobo 8"
        ,"Metal Chocobo 9"
        ,"Olympia 0"
        ,"Olympia 1"
        ,"Olympia 2"
        ,"Olympia 3"
        ,"Olympia 4"
        ,"Olympia 5"
        ,"Olympia 6"
        ,"Olympia 7"
        ,"Olympia 8"
        ,"Olympia 9"
        ,"Lionheart 0"
        ,"Lionheart 1"
        ,"Lionheart 2"
        ,"Lionheart 3"
        ,"Lionheart 4"
        ,"Lionheart 5"
        ,"Lionheart 6"
        ,"Lionheart 7"
        ,"Lionheart 8"
        ,"Lionheart 9"
        ,"Lady Luck 0"
        ,"Lady Luck 1"
        ,"Lady Luck 2"
        ,"Lady Luck 3"
        ,"Lady Luck 4"
        ,"Lady Luck 5"
        ,"Lady Luck 6"
        ,"Lady Luck 7"
        ,"Lady Luck 8"
        ,"Lady Luck 9"
        ,"Divine Rose 0"
        ,"Divine Rose 1"
        ,"Divine Rose 2"
        ,"Divine Rose 3"
        ,"Divine Rose 4"
        ,"Divine Rose 5"
        ,"Divine Rose 6"
        ,"Divine Rose 7"
        ,"Divine Rose 8"
        ,"Divine Rose 9"
        ,"Oathkeeper 0"
        ,"Oathkeeper 1"
        ,"Oathkeeper 2"
        ,"Oathkeeper 3"
        ,"Oathkeeper 4"
        ,"Oathkeeper 5"
        ,"Oathkeeper 6"
        ,"Oathkeeper 7"
        ,"Oathkeeper 8"
        ,"Oathkeeper 9"
        ,"Oblivion 0"
        ,"Oblivion 1"
        ,"Oblivion 2"
        ,"Oblivion 3"
        ,"Oblivion 4"
        ,"Oblivion 5"
        ,"Oblivion 6"
        ,"Oblivion 7"
        ,"Oblivion 8"
        ,"Oblivion 9"
        ,"Diamond Dust 0"
        ,"Diamond Dust 1"
        ,"Diamond Dust 2"
        ,"Diamond Dust 3"
        ,"Diamond Dust 4"
        ,"Diamond Dust 5"
        ,"Diamond Dust 6"
        ,"Diamond Dust 7"
        ,"Diamond Dust 8"
        ,"Diamond Dust 9"
        ,"One Winged Angel 0"
        ,"One Winged Angel 1"
        ,"One Winged Angel 2"
        ,"One Winged Angel 3"
        ,"One Winged Angel 4"
        ,"One Winged Angel 5"
        ,"One Winged Angel 6"
        ,"One Winged Angel 7"
        ,"One Winged Angel 8"
        ,"One Winged Angel 9"
        ,"Ultima Weapon 0"
        ,"Ultima Weapon 1"
        ,"Ultima Weapon 2"
        ,"Ultima Weapon 3"
        ,"Ultima Weapon 4"
        ,"Ultima Weapon 5"
        ,"Ultima Weapon 6"
        ,"Ultima Weapon 7"
        ,"Ultima Weapon 8"
        ,"Ultima Weapon 9"
        ,"Fire 0"
        ,"Fire 1"
        ,"Fire 2"
        ,"Fire 3"
        ,"Fire 4"
        #,"Fire 5" Axel I
        ,"Fire 6"
        ,"Fire 7"
        ,"Fire 8"
        ,"Fire 9"
        ,"Blizzard 0"
        ,"Blizzard 1"
        ,"Blizzard 2"
        ,"Blizzard 3"
        ,"Blizzard 4"
        ,"Blizzard 5"
        ,"Blizzard 6"
        ,"Blizzard 7"
        ,"Blizzard 8"
        ,"Blizzard 9"
        ,"Thunder 0"
        ,"Thunder 1"
        ,"Thunder 2"
        ,"Thunder 3"
        ,"Thunder 4"
        ,"Thunder 5"
        ,"Thunder 6"
        #,"Thunder 7" Larxene I
        ,"Thunder 8"
        ,"Thunder 9"
        ,"Cure 0"
        ,"Cure 1"
        ,"Cure 2"
        ,"Cure 3"
        ,"Cure 4"
        ,"Cure 5"
        ,"Cure 6"
        ,"Cure 7"
        ,"Cure 8"
        ,"Cure 9"
        ,"Gravity 0"
        ,"Gravity 1"
        ,"Gravity 2"
        ,"Gravity 3"
        ,"Gravity 4"
        ,"Gravity 5"
        ,"Gravity 6"
        ,"Gravity 7"
        ,"Gravity 8"
        ,"Gravity 9"
        ,"Stop 0"
        ,"Stop 1"
        ,"Stop 2"
        ,"Stop 3"
        ,"Stop 4"
        ,"Stop 5"
        ,"Stop 6"
        ,"Stop 7"
        ,"Stop 8"
        ,"Stop 9"
        ,"Aero 0"
        ,"Aero 1"
        ,"Aero 2"
        ,"Aero 3"
        ,"Aero 4"
        ,"Aero 5"
        #,"Aero 6" Riku
        ,"Aero 7"
        ,"Aero 8"
        ,"Aero 9"
        ,"Simba 0"
        ,"Simba 1"
        ,"Simba 2"
        ,"Simba 3"
        ,"Simba 4"
        ,"Simba 5"
        #,"Simba 6" Leon
        ,"Simba 7"
        ,"Simba 8"
        ,"Simba 9"
        ,"Genie 0"
        ,"Genie 1"
        ,"Genie 2"
        ,"Genie 3"
        ,"Genie 4"
        ,"Genie 5"
        #,"Genie 6" Aladdin
        ,"Genie 7"
        ,"Genie 8"
        ,"Genie 9"
        ,"Bambi 0"
        ,"Bambi 1"
        ,"Bambi 2"
        ,"Bambi 3"
        ,"Bambi 4"
        ,"Bambi 5"
        ,"Bambi 6"
        ,"Bambi 7"
        ,"Bambi 8"
        ,"Bambi 9"
        ,"Dumbo 0"
        ,"Dumbo 1"
        ,"Dumbo 2"
        ,"Dumbo 3"
        ,"Dumbo 4"
        ,"Dumbo 5"
        ,"Dumbo 6"
        ,"Dumbo 7"
        ,"Dumbo 8"
        ,"Dumbo 9"
        ,"Tinker Bell 0"
        ,"Tinker Bell 1"
        ,"Tinker Bell 2"
        ,"Tinker Bell 3"
        #,"Tinker Bell 4" Peter Pan
        ,"Tinker Bell 5"
        ,"Tinker Bell 6"
        ,"Tinker Bell 7"
        ,"Tinker Bell 8"
        ,"Tinker Bell 9"
        ,"Mushu 0"
        ,"Mushu 1"
        ,"Mushu 2"
        ,"Mushu 3"
        ,"Mushu 4"
        ,"Mushu 5"
        ,"Mushu 6"
        ,"Mushu 7"
        ,"Mushu 8"
        ,"Mushu 9"
        ,"Cloud 0"
        ,"Cloud 1"
        ,"Cloud 2"
        ,"Cloud 3"
        #,"Cloud 4" Cloud
        ,"Cloud 5"
        ,"Cloud 6"
        ,"Cloud 7"
        ,"Cloud 8"
        ,"Cloud 9"
        ,"Potion 0"
        ,"Potion 1"
        ,"Potion 2"
        ,"Potion 3"
        ,"Potion 4"
        ,"Potion 5"
        ,"Potion 6"
        ,"Potion 7"
        ,"Potion 8"
        ,"Potion 9"
        ,"Hi-Potion 0"
        ,"Hi-Potion 1"
        ,"Hi-Potion 2"
        #,"Hi-Potion 3" Cloud
        ,"Hi-Potion 4"
        ,"Hi-Potion 5"
        ,"Hi-Potion 6"
        ,"Hi-Potion 7"
        ,"Hi-Potion 8"
        ,"Hi-Potion 9"
        ,"Mega-Potion 0"
        ,"Mega-Potion 1"
        #,"Mega-Potion 2" Riku III
        ,"Mega-Potion 3"
        ,"Mega-Potion 4"
        ,"Mega-Potion 5"
        ,"Mega-Potion 6"
        ,"Mega-Potion 7"
        ,"Mega-Potion 8"
        ,"Mega-Potion 9"
        ,"Ether 0"
        ,"Ether 1"
        ,"Ether 2"
        #,"Ether 3" Agrabah
        ,"Ether 4"
        ,"Ether 5"
        ,"Ether 6"
        ,"Ether 7"
        ,"Ether 8"
        ,"Ether 9"
        ,"Mega-Ether 0"
        ,"Mega-Ether 1"
        ,"Mega-Ether 2"
        ,"Mega-Ether 3"
        #,"Mega-Ether 4" Vexen I
        ,"Mega-Ether 5"
        ,"Mega-Ether 6"
        ,"Mega-Ether 7"
        ,"Mega-Ether 8"
        ,"Mega-Ether 9"
        ,"Elxir 0"
        #,"Elxir 1" Roo
        ,"Elxir 2"
        ,"Elxir 3"
        ,"Elxir 4"
        ,"Elxir 5"
        ,"Elxir 6"
        ,"Elxir 7"
        ,"Elxir 8"
        ,"Elxir 9"
        ,"Megalixir 0"
        ,"Megalixir 1"
        ,"Megalixir 2"
        ,"Megalixir 3"
        ,"Megalixir 4"
        ,"Megalixir 5"
        ,"Megalixir 6"
        ,"Megalixir 7"
        ,"Megalixir 8"
        ,"Megalixir 9"
        ,    #Premium Battle Cards"
        ,"Premium Kingdom Key 0"
        ,"Premium Kingdom Key 1"
        ,"Premium Kingdom Key 2"
        ,"Premium Kingdom Key 3"
        ,"Premium Kingdom Key 4"
        ,"Premium Kingdom Key 5"
        ,"Premium Kingdom Key 6"
        ,"Premium Kingdom Key 7"
        ,"Premium Kingdom Key 8"
        ,"Premium Kingdom Key 9"
        ,"Premium Three Wishes 0"
        ,"Premium Three Wishes 1"
        ,"Premium Three Wishes 2"
        ,"Premium Three Wishes 3"
        ,"Premium Three Wishes 4"
        ,"Premium Three Wishes 5"
        ,"Premium Three Wishes 6"
        ,"Premium Three Wishes 7"
        ,"Premium Three Wishes 8"
        ,"Premium Three Wishes 9"
        ,"Premium Crabclaw 0"
        ,"Premium Crabclaw 1"
        ,"Premium Crabclaw 2"
        ,"Premium Crabclaw 3"
        ,"Premium Crabclaw 4"
        ,"Premium Crabclaw 5"
        ,"Premium Crabclaw 6"
        ,"Premium Crabclaw 7"
        ,"Premium Crabclaw 8"
        ,"Premium Crabclaw 9"
        ,"Premium Pumpkinhead 0"
        ,"Premium Pumpkinhead 1"
        ,"Premium Pumpkinhead 2"
        ,"Premium Pumpkinhead 3"
        ,"Premium Pumpkinhead 4"
        ,"Premium Pumpkinhead 5"
        ,"Premium Pumpkinhead 6"
        ,"Premium Pumpkinhead 7"
        ,"Premium Pumpkinhead 8"
        ,"Premium Pumpkinhead 9"
        ,"Premium Fairy Harp 0"
        ,"Premium Fairy Harp 1"
        ,"Premium Fairy Harp 2"
        ,"Premium Fairy Harp 3"
        ,"Premium Fairy Harp 4"
        ,"Premium Fairy Harp 5"
        ,"Premium Fairy Harp 6"
        ,"Premium Fairy Harp 7"
        ,"Premium Fairy Harp 8"
        ,"Premium Fairy Harp 9"
        ,"Premium Wishing Star 0"
        ,"Premium Wishing Star 1"
        ,"Premium Wishing Star 2"
        ,"Premium Wishing Star 3"
        ,"Premium Wishing Star 4"
        ,"Premium Wishing Star 5"
        ,"Premium Wishing Star 6"
        ,"Premium Wishing Star 7"
        ,"Premium Wishing Star 8"
        ,"Premium Wishing Star 9"
        ,"Premium Spellbinder 0"
        ,"Premium Spellbinder 1"
        ,"Premium Spellbinder 2"
        ,"Premium Spellbinder 3"
        ,"Premium Spellbinder 4"
        ,"Premium Spellbinder 5"
        ,"Premium Spellbinder 6"
        ,"Premium Spellbinder 7"
        ,"Premium Spellbinder 8"
        ,"Premium Spellbinder 9"
        ,"Premium Metal Chocobo 0"
        ,"Premium Metal Chocobo 1"
        ,"Premium Metal Chocobo 2"
        ,"Premium Metal Chocobo 3"
        ,"Premium Metal Chocobo 4"
        ,"Premium Metal Chocobo 5"
        ,"Premium Metal Chocobo 6"
        ,"Premium Metal Chocobo 7"
        ,"Premium Metal Chocobo 8"
        ,"Premium Metal Chocobo 9"
        ,"Premium Olympia 0"
        ,"Premium Olympia 1"
        ,"Premium Olympia 2"
        ,"Premium Olympia 3"
        ,"Premium Olympia 4"
        ,"Premium Olympia 5"
        ,"Premium Olympia 6"
        ,"Premium Olympia 7"
        ,"Premium Olympia 8"
        ,"Premium Olympia 9"
        ,"Premium Lionheart 0"
        ,"Premium Lionheart 1"
        ,"Premium Lionheart 2"
        ,"Premium Lionheart 3"
        ,"Premium Lionheart 4"
        ,"Premium Lionheart 5"
        ,"Premium Lionheart 6"
        ,"Premium Lionheart 7"
        ,"Premium Lionheart 8"
        ,"Premium Lionheart 9"
        ,"Premium Lady Luck 0"
        ,"Premium Lady Luck 1"
        ,"Premium Lady Luck 2"
        ,"Premium Lady Luck 3"
        ,"Premium Lady Luck 4"
        ,"Premium Lady Luck 5"
        ,"Premium Lady Luck 6"
        ,"Premium Lady Luck 7"
        ,"Premium Lady Luck 8"
        ,"Premium Lady Luck 9"
        ,"Premium Divine Rose 0"
        ,"Premium Divine Rose 1"
        ,"Premium Divine Rose 2"
        ,"Premium Divine Rose 3"
        ,"Premium Divine Rose 4"
        ,"Premium Divine Rose 5"
        ,"Premium Divine Rose 6"
        ,"Premium Divine Rose 7"
        ,"Premium Divine Rose 8"
        ,"Premium Divine Rose 9"
        ,"Premium Oathkeeper 0"
        ,"Premium Oathkeeper 1"
        ,"Premium Oathkeeper 2"
        ,"Premium Oathkeeper 3"
        ,"Premium Oathkeeper 4"
        ,"Premium Oathkeeper 5"
        ,"Premium Oathkeeper 6"
        ,"Premium Oathkeeper 7"
        ,"Premium Oathkeeper 8"
        ,"Premium Oathkeeper 9"
        ,"Premium Oblivion 0"
        ,"Premium Oblivion 1"
        ,"Premium Oblivion 2"
        ,"Premium Oblivion 3"
        ,"Premium Oblivion 4"
        ,"Premium Oblivion 5"
        ,"Premium Oblivion 6"
        ,"Premium Oblivion 7"
        ,"Premium Oblivion 8"
        ,"Premium Oblivion 9"
        ,"Premium Diamond Dust 0"
        ,"Premium Diamond Dust 1"
        ,"Premium Diamond Dust 2"
        ,"Premium Diamond Dust 3"
        ,"Premium Diamond Dust 4"
        ,"Premium Diamond Dust 5"
        ,"Premium Diamond Dust 6"
        ,"Premium Diamond Dust 7"
        ,"Premium Diamond Dust 8"
        ,"Premium Diamond Dust 9"
        ,"Premium One Winged Angel 0"
        ,"Premium One Winged Angel 1"
        ,"Premium One Winged Angel 2"
        ,"Premium One Winged Angel 3"
        ,"Premium One Winged Angel 4"
        ,"Premium One Winged Angel 5"
        ,"Premium One Winged Angel 6"
        ,"Premium One Winged Angel 7"
        ,"Premium One Winged Angel 8"
        ,"Premium One Winged Angel 9"
        ,"Premium Ultima Weapon 0"
        ,"Premium Ultima Weapon 1"
        ,"Premium Ultima Weapon 2"
        ,"Premium Ultima Weapon 3"
        ,"Premium Ultima Weapon 4"
        ,"Premium Ultima Weapon 5"
        ,"Premium Ultima Weapon 6"
        ,"Premium Ultima Weapon 7"
        ,"Premium Ultima Weapon 8"
        ,"Premium Ultima Weapon 9"
        ,"Premium Fire 0"
        ,"Premium Fire 1"
        ,"Premium Fire 2"
        ,"Premium Fire 3"
        ,"Premium Fire 4"
        ,"Premium Fire 5"
        ,"Premium Fire 6"
        ,"Premium Fire 7"
        ,"Premium Fire 8"
        ,"Premium Fire 9"
        ,"Premium Blizzard 0"
        ,"Premium Blizzard 1"
        ,"Premium Blizzard 2"
        ,"Premium Blizzard 3"
        ,"Premium Blizzard 4"
        ,"Premium Blizzard 5"
        ,"Premium Blizzard 6"
        ,"Premium Blizzard 7"
        ,"Premium Blizzard 8"
        ,"Premium Blizzard 9"
        ,"Premium Thunder 0"
        ,"Premium Thunder 1"
        ,"Premium Thunder 2"
        ,"Premium Thunder 3"
        ,"Premium Thunder 4"
        ,"Premium Thunder 5"
        ,"Premium Thunder 6"
        ,"Premium Thunder 7"
        ,"Premium Thunder 8"
        ,"Premium Thunder 9"
        ,"Premium Cure 0"
        ,"Premium Cure 1"
        ,"Premium Cure 2"
        ,"Premium Cure 3"
        ,"Premium Cure 4"
        ,"Premium Cure 5"
        ,"Premium Cure 6"
        ,"Premium Cure 7"
        ,"Premium Cure 8"
        ,"Premium Cure 9"
        ,"Premium Gravity 0"
        ,"Premium Gravity 1"
        ,"Premium Gravity 2"
        ,"Premium Gravity 3"
        ,"Premium Gravity 4"
        ,"Premium Gravity 5"
        ,"Premium Gravity 6"
        ,"Premium Gravity 7"
        ,"Premium Gravity 8"
        ,"Premium Gravity 9"
        ,"Premium Stop 0"
        ,"Premium Stop 1"
        ,"Premium Stop 2"
        ,"Premium Stop 3"
        ,"Premium Stop 4"
        ,"Premium Stop 5"
        ,"Premium Stop 6"
        ,"Premium Stop 7"
        ,"Premium Stop 8"
        ,"Premium Stop 9"
        ,"Premium Aero 0"
        ,"Premium Aero 1"
        ,"Premium Aero 2"
        ,"Premium Aero 3"
        ,"Premium Aero 4"
        ,"Premium Aero 5"
        ,"Premium Aero 6"
        ,"Premium Aero 7"
        ,"Premium Aero 8"
        ,"Premium Aero 9"
        ,"Premium Simba 0"
        ,"Premium Simba 1"
        ,"Premium Simba 2"
        ,"Premium Simba 3"
        ,"Premium Simba 4"
        ,"Premium Simba 5"
        ,"Premium Simba 6"
        ,"Premium Simba 7"
        ,"Premium Simba 8"
        ,"Premium Simba 9"
        ,"Premium Genie 0"
        ,"Premium Genie 1"
        ,"Premium Genie 2"
        ,"Premium Genie 3"
        ,"Premium Genie 4"
        ,"Premium Genie 5"
        ,"Premium Genie 6"
        ,"Premium Genie 7"
        ,"Premium Genie 8"
        ,"Premium Genie 9"
        ,"Premium Genie 0"
        ,"Premium Genie 1"
        ,"Premium Genie 2"
        ,"Premium Genie 3"
        ,"Premium Genie 4"
        ,"Premium Genie 5"
        ,"Premium Genie 6"
        ,"Premium Genie 7"
        ,"Premium Genie 8"
        ,"Premium Genie 9"
        ,"Premium Bambi 0"
        ,"Premium Bambi 1"
        ,"Premium Bambi 2"
        ,"Premium Bambi 3"
        ,"Premium Bambi 4"
        ,"Premium Bambi 5"
        ,"Premium Bambi 6"
        ,"Premium Bambi 7"
        ,"Premium Bambi 8"
        ,"Premium Bambi 9"
        ,"Premium Dumbo 0"
        ,"Premium Dumbo 1"
        ,"Premium Dumbo 2"
        ,"Premium Dumbo 3"
        ,"Premium Dumbo 4"
        ,"Premium Dumbo 5"
        ,"Premium Dumbo 6"
        ,"Premium Dumbo 7"
        ,"Premium Dumbo 8"
        ,"Premium Dumbo 9"
        ,"Premium Tinker Bell 0"
        ,"Premium Tinker Bell 1"
        ,"Premium Tinker Bell 2"
        ,"Premium Tinker Bell 3"
        ,"Premium Tinker Bell 4"
        ,"Premium Tinker Bell 5"
        ,"Premium Tinker Bell 6"
        ,"Premium Tinker Bell 7"
        ,"Premium Tinker Bell 8"
        ,"Premium Tinker Bell 9"
        ,"Premium Mushu 0"
        ,"Premium Mushu 1"
        ,"Premium Mushu 2"
        ,"Premium Mushu 3"
        ,"Premium Mushu 4"
        ,"Premium Mushu 5"
        ,"Premium Mushu 6"
        ,"Premium Mushu 7"
        ,"Premium Mushu 8"
        ,"Premium Mushu 9"
        ,"Premium Cloud 0"
        ,"Premium Cloud 1"
        ,"Premium Cloud 2"
        ,"Premium Cloud 3"
        ,"Premium Cloud 4"
        ,"Premium Cloud 5"
        ,"Premium Cloud 6"
        ,"Premium Cloud 7"
        ,"Premium Cloud 8"
        ,"Premium Cloud 9"
        ,"Shadow"
        ,"Soldier"
        ,"Large Body"
        ,"Red Nocturne"
        ,"Blue Rhapsody"
        ,"Yellow Opera"
        ,"Green Requiem"
        ,"Powerwild"
        ,"Bouncywild"
        ,"Air Soldier"
        ,"Bandit"
        ,"Fat Bandit"
        ,"Barrel Spider"
        ,"Search Ghost"
        ,"Sea Neon"
        ,"Screwdriver"
        ,"Aquatank"
        ,"Wight Knight"
        ,"Gargoyle"
        ,"Pirate"
        ,"Air Pirate"
        ,"Darkball"
        ,"Defender"
        ,"Wyvern"
        ,"Wizard"
        ,"Neoshadow"
        ,"White Mushroom"
        ,"Black Fungus"
        ,"Creeper Plant"
        ,"Tornado Step"
        ,"Crescendo"
        #,"Guard Armor"
        #,"Parasite Cage"
        #,"Trickmaster"
        #,"Darkside"
        #,"Card Soldier (Red)"
        ,"Card Soldier (Black)"
        #,"Hades"
        #,"Jafar"
        #,"Oogie Boogie"
        #,"Ursula"
        #,"Hook"
        #,"Dragon Maleficent"
        #,"Riku"
        #,"Axel"
        #,"Larxene"
        #,"Vexen"
        #,"Marluxia"
    }
}

events_table = {
    "Marluxia": "Victory"
}

lookup_id_to_name: typing.Dict[int, str] = {data.id: item_name for item_name, data in achievement_table.items() if data.id}