from data_manager import *
from enemy import *

NUM_FORMATIONS = 512

class Formation(object):
    def __init__(self,index,data_manager,enemy_manager,original_flag = False):
        self.idx = index
        self.generate_from_data(data_manager.files['formations'])
        '''
        self.offset
        self.randomized_boss
        self.rank
        self.boss_rank
        self.event_id
        self.event_lookup_loc1
        self.event_lookup_loc2
        self.event_formation_reference
        self.formationid_1
        self.escape_%
        self.abp
        self.visible_enemy
        self.enemy_1
        self.enemy_2
        self.enemy_3
        self.enemy_4
        self.enemy_5
        self.enemy_6
        self.enemy_7
        self.enemy_8
        self.formationid_13
        self.formationid_14
        self.formationid_15
        self.formationid_16
        self.enemy_list
        '''
        self.assign_enemies(enemy_manager, data_manager, original_flag)
        self.original_enemy_list = self.enemy_list
        self.enemy_change = ''
        self.mib_arch_flag = False

    @property
    def asar_output(self):
        return '; ' + str(self.enemy_change) + ' \norg $'+ str(self.event_lookup_loc1) + \
           '\ndb $' + str(self.event_formation_reference[0:2]) + ", $" + str(self.event_formation_reference[2:4]) + \
           ' \norg $' + str(self.event_lookup_loc2) + '\ndb $' + str(self.event_formation_reference[0:2]) + \
           ', $' + str(self.event_formation_reference[2:4])

    @property
    def short_output(self):
        try:
            split1, split2 = self.enemy_change.split(" > ",1)
            
            if self.offset == 'D04C90':
                split1 = split1.replace("Gilgamesh","Gilgamesh I")    
            elif self.offset == 'D04D00':
                split1 = split1.replace("Gilgamesh","Gilgamesh II")
            elif self.offset == 'D04D40':
                split1 = split1.replace("Gilgamesh","Gilgamesh III")
            elif self.offset == 'D04D80':
                split1 = split1.replace("Gilgamesh","Gilgamesh IV")


            if "Gilgamesh (Rank 4)" in split2:
                split2 = split2.replace("Gilgamesh","Gilgamesh I")
            elif "Gilgamesh (Rank 5)" in split2:
                split2 = split2.replace("Gilgamesh","Gilgamesh II")
            elif "Gilgamesh (Rank 6)" in split2:
                split2 = split2.replace("Gilgamesh","Gilgamesh III")
            elif "Gilgamesh (Rank 7)" in split2:
                split2 = split2.replace("Gilgamesh","Gilgamesh IV")
            split1 = split1.replace("Hole","Sandworm").replace("Forza","Magisa")
            split2 = split2.replace("Hole","Sandworm").replace("Forza","Magisa")
            
            split1_boss = split1.split(" (")[0].strip()
            split1_rank = split1.split(" (")[1].replace(")","").strip()
            split2_boss = split2.split(" (")[0].strip()
            split2_rank = split2.split(" (")[1].replace(")","").strip()
            
            
            return '{:10}'.format("%s" % (split1_rank)) + '{:25}'.format("%s" % (split1_boss)) + '{:5}'.format(">")  + '{:10}'.format("%s" % (split2_rank)) + '{:25}'.format("%s" % (split2_boss)) 
        except Exception as e:
            print("Exception %s" % e)
            return ""

    def generate_from_data(self, data):
        if str(self.idx) in data.keys():
            s = data[str(self.idx)]
            for k, v in s.items():
                setattr(self,k,v)
            pass
        else:
            print("No match on index found for Formation %s" % self.idx)
            
    def assign_enemies(self,enemy_manager, data_manager, original_flag):
        enemy_list = []
        for enemy in ['enemy_1','enemy_2','enemy_3','enemy_4','enemy_5','enemy_6','enemy_7','enemy_8']:
            # print(self.enemy_list,original_flag)
            # Find enemy ID
            enemy_id = getattr(self,enemy)

            # If it's $FF, then ignore entirely
            if enemy_id == 'FF':
                continue
            
            # ORIGINAL FLAG
            # if the original flag is called, a NEW enemy object is created per enemy
            # Otherwise, the shared pool of enemies for the output will be used
            
            # What happens is that we need to preserve the enemies that are being randomized elsewhere
            # primarly for loot and stats. But we need to make sure those same enemies are the same objects
            # All the way through the end for our randomized output. 
            
            # But when we use the original flag, it's for comparison to the vanilla enemy
            # which is VERY important for preserving boss swap
            
            # This avoids a situation such as:
            # Swap LiquidFlame with TwinTania, giving 55000 hp to LiquidFlame
            # Then, swap WingRaptor with LiquidFlame, giving 55000 hp to WingRaptor
            # That's NOT what we want. We want 3000hp to WingRaptor (LiquidFlame's vanilla hp), 
            # which is why this original clause exists
            
            elif original_flag:
                # Create new Enemy classes to grab from original, unaltered/randomized data
                # If it's Byblos or Ifrit, the only exceptions, grab from enemies, else grab from bosses
                if self.rank == 'boss':
                    new_enemy = Enemy(enemy_id,data_manager,'hex', True)
                else:
                    new_enemy = Enemy(enemy_id,data_manager,'hex', False)
            else:
                # If it's not original, iterate through the list of all enemies 
                
                if self.rank == 'standard':
                    for enemy_loop in [x for x in enemy_manager.enemies if x.enemy_rank == 'enemy']:  # Search through first set of enemies before bosses
                        if enemy_loop.idx_hex == enemy_id:
                            new_enemy = enemy_loop
                else:
                    for enemy_loop in [x for x in enemy_manager.enemies if x.enemy_rank == 'boss']:  # Search through last set of enemies, bosses only
                        if enemy_loop.idx_hex == enemy_id:
                            new_enemy = enemy_loop
            enemy_list.append(new_enemy)
            
            
            
        # Assign list of enemy class objects to self for all enemies
        self.enemy_classes = enemy_list

class FormationManager(object):
    def __init__(self, data_manager, enemy_manager):
        self.formations = [Formation(x, data_manager, enemy_manager) for x in data_manager.files['formations'].keys()]
        self.mib_arch_patch = ''
    def get_patch(self,remove_ned_flag):
        output = ";=========="
        output = output + "\n;formations"
        output = output + "\n;==========\n"
        if remove_ned_flag:
            formation_list = [i for i in self.formations if i.randomized_boss == 'y' or i.randomized_boss == 'ned']
        else:
            formation_list = [i for i in self.formations if i.randomized_boss == 'y']
        for i in formation_list:
            output = output + i.asar_output + "\n"
            
        if self.mib_arch_patch:
            output += self.mib_arch_patch + "\n"
        output = output + "\n"

        return output

    def get_spoiler_mib_patch(self):
        mib_formations = [i for i in self.formations if i.mib_arch_flag]
        output = "-----TRAPPED CHEST/MIB FORMATIONS-----\n"
        mib_formations = sorted(mib_formations, key = lambda x: x.region_rank)
        for f in mib_formations:
            output += "Rank %s > %s\n" % (f.region_rank, f.enemy_list)
        output = output + '\n'
        return output
    def get_spoiler(self,remove_ned_flag):
        output = "-----FORMATIONS-----\n"
        output = output+ "-- List in order of bosses where they appear in power ranking--\n  (WingRaptor appears at X location)\n"

        if remove_ned_flag:
            boss_list = [x for x in self.formations if x.randomized_boss == 'y' or x.randomized_boss == 'ned']

        else:
            boss_list = [x for x in self.formations if x.randomized_boss == 'y']
        boss_list.sort(key=lambda x: int(x.boss_rank), reverse=False)

        for i in boss_list:
            output = output + i.short_output + "\n"
            
        output = output+ "\n-- List in order of bosses where they appear in location ranking --\n  (At WingRaptor location, X boss appears)\n"
        boss_list.sort(key=lambda x: int(x.random_boss_rank), reverse=False)

        for i in boss_list:
            output = output + i.short_output + "\n"
        
        if remove_ned_flag:
            output = output.replace("Goblin              ","NeoExdeath (Goblins)")
            
        output = output + "\n -- Boss HP/EXP Details --\n"
            
        if remove_ned_flag:
            formation_list = [i for i in self.formations if i.randomized_boss == 'y' or i.randomized_boss == 'ned']
        else:
            formation_list = [i for i in self.formations if i.randomized_boss == 'y']
        for i in formation_list:
            output = output +  i.enemy_change + '\n'
            for e in i.enemy_classes:
                output = output + "{:20}".format("    %s" % e.enemy_name) + "{:10}".format(" HP: %s" % e.num_hp) + "{:10}".format(" EXP: %s" % e.num_exp) + '\n'

        output = output + "\n-----**********-----\n"

        
        return output