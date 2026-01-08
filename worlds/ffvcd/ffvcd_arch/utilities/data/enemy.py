from ai_parser import *

NUM_ENEMIES = 368
STAT_HEX_MAP = {
        'gauge_time' : '00',
        'phys_power' : '01',
        'phys_mult' : '02',
        'evade' : '03',
        'phys_def' : '04',
        'mag_power' : '05',
        'mag_def' : '06',
        'mag_evade' : '07',
        'hp_lo' : '08',
        'hp_hi' : '09',
        'mp_lo' : '0A',
        'mp_hi' : '0B',
        'exp_lo' : '0C',
        'exp_hi' : '0D',
        'gil_lo' : '0E',
        'gil_hi' : '0F',
        'atk_index' : '10',
        'elemental_immune' : '11',
        'status0_immune' : '12',
        'status1_immune' : '13',
        'status2_immune' : '14',
        'elemental_absorb' : '15',
        'unavoidable_atk' : '16',
        'elemental_weakness' : '17',
        'enemy_type' : '18',
        'special_immune' : '19',
        'initial_status0' : '1A',
        'initial_status1' : '1B',
        'initial_status2' : '1C',
        'initial_status3' : '1D',
        'name_index' : '1E',
        'level' : '1F'
        }

class Enemy(object):
    def __init__(self,index, data_manager, pass_type, use_boss_table = True):
        self.idx = index
        self.generate_from_data(data_manager, pass_type, use_boss_table)
        '''
        self.idx_hex
        self.enemy_name
        self.enemy_rank (enemy, boss)
        self.stats_address
        self.drops_address
        self.name_address
        self.enemy_name_python
        self.unique_name
        self.num_gauge_time
        self.num_phys_power
        self.num_phys_mult
        self.num_evade
        self.num_phys_def
        self.num_mag_power
        self.num_mag_def
        self.num_mag_evade
        self.num_hp
        self.num_mp
        self.num_exp
        self.num_gil
        self.num_level
        self.gauge_time
        self.phys_power
        self.phys_mult
        self.evade
        self.phys_def
        self.mag_power
        self.mag_def
        self.mag_evade
        self.hp_lo
        self.hp_hi
        self.mp_lo
        self.mp_hi
        self.exp_lo
        self.exp_hi
        self.gil_lo
        self.gil_hi
        self.atk_index
        self.elemental_immune
        self.status0_immune
        self.status1_immune
        self.sattus2_immune
        self.elemental_absorb
        self.unavoidable_atk
        self.elemental_weakness
        self.enemy_type
        self.special_immune
        self.initial_status0
        self.initial_status1
        self.initial_status2
        self.initial_status3
        self.name_index
        self.level
        self.steal_common
        self.steal_rare
        self.drop_common
        self.drop_rare
        self.steal_common_name
        self.steal_rare_name
        self.drop_common_name
        self.drop_rare_name
        self.name_string
        '''
        self.original_num_hp = self.num_hp
        self.original_hp_hi = self.hp_hi
        self.original_hp_lo = self.hp_lo
        self.ai_patch_text = None

    @property
    def asar_output(self):
        # This outputs asar code for a enemy's stats
        final_output = ''
        
        final_output = final_output + "; Enemy: "+str(self.enemy_name)
        
        stat_data = '; Stats: \norg $'+self.stats_address+"\ndb "
        for stat in STAT_HEX_MAP:
            hex_val = str(getattr(self, stat))
            stat_data = stat_data + "$" + hex_val + ", "
        final_output = final_output + "\n" + stat_data[:-2] + "\n"

        final_output = final_output +  '; Loot: \norg $'+self.drops_address+"\ndb $"+self.steal_common+", $"+self.steal_rare+", $"+self.drop_common+", $"+self.drop_rare+"\n"
        
        if self.ai_patch_text is not None:
            final_output = final_output + self.ai_patch_text

        return final_output

    @property
    def short_output(self, length='full'):
        # This prints the stat values that are in HEX therefore what will specifically be coded to the game
        # NOT the "num_" values, which are used for updating THESE values 
        
        # Arguments
        # length : 
        # 'short' is name & loot
        # 'full' is stats
        # 'loot_only' returns loot
        
        if length == 'loot_only':
            return '{0: <15}'.format(self.enemy_name)+'{0: <40}'.format("Steal: "+self.steal_common_name+" / "+self.steal_rare_name)+'{0: <40}'.format("Drop: "+self.drop_common_name+" / "+self.drop_rare_name)
        
        final_output = ''
        # Name
        final_output  = final_output  + '{0: <15}'.format("Enemy:")+self.enemy_name+"\n"

        # Loot
        final_output  = final_output  + '{0: <15}'.format("Steal: ")+self.steal_common_name+" / "+self.steal_rare_name+"\n"+'{0: <15}'.format("Drop: ")+self.drop_common_name+" / "+self.drop_rare_name+"\n"

    
        # Stats 
        if length == 'full':
            for stat in ['hp','mp','exp','gil']:
                new_val = int(getattr(self,stat+"_hi"),base=16) * 256  + int(getattr(self,stat+"_lo"),base=16)
                final_output  = final_output  + '{0: <15}'.format(stat +": ") +str(new_val)+"\n"
            for stat in ['gauge_time','phys_power','phys_mult','evade','phys_def','mag_power','mag_def','mag_evade','level']:
                new_val = int(getattr(self,stat),base=16)
                final_output  = final_output  + '{0: <15}'.format(stat +": ") +str(new_val)+"\n"

        # AI
        #TODO
        
        return final_output

    def generate_from_data(self,data_manager, pass_type, use_boss_table):
        # if pass_type == 'id': #if we're passing in ids, we can look anywhere
        
        # if pass_type == 'hex': #if we're passing in hexes, we have to star
        #     if use_boss_table:
        #         s = data_manager.files['enemies_bosses'][data_manager.files['enemies_bosses']['idx_hex'].str.match(str(self.idx))].iloc[0]
        #     else:
        #         s = data_manager.files['enemies_nonbosses'][data_manager.files['enemies_nonbosses']['idx_hex'].str.match(str(self.idx))].iloc[0]
        
        
        if pass_type == 'id':
    
            if str(self.idx) in data_manager.files['enemies'].keys():
                data = data_manager.files['enemies'][str(self.idx)]
                for k, v in data.items():
                    setattr(self,k,v)
            else:
                print("No match on index found for Enemy data %s" % self.idx)
                
        elif pass_type == 'hex':
            try:
                if use_boss_table:
                    data = data_manager.files['enemies_bosses'][[i for i in data_manager.files['enemies_bosses'] if data_manager.files['enemies_bosses'][i]['idx_hex'] == self.idx][0]]
                else:
                    data = data_manager.files['enemies_nonbosses'][[i for i in data_manager.files['enemies_nonbosses'] if data_manager.files['enemies_nonbosses'][i]['idx_hex'] == self.idx][0]]
                for k, v in data.items():
                    setattr(self,k,v)
            except:
                print("No match on index found for Enemy data via passing in hex as pass_type %s" % self.idx)
                

    def update_val(self, attr, val):
        val = int(val)
        if val > 65535:
            val = 65535
        val_bytes = val.to_bytes(2, 'little') or b'\0' #format our data as little endian bytes
        val_lo = format(val_bytes[0], '02x').upper() #pass through format with 'x' to get just
        val_hi = format(val_bytes[1], '02x').upper() #hex value (no '0x')

        if attr == 'exp':
            self.num_exp = val
            self.exp_lo = val_lo
            self.exp_hi = val_hi
        elif attr == 'gil':
            self.num_gil = val
            self.gil_lo = val_lo
            self.gil_hi = val_hi
        elif attr == 'hp':
            self.num_hp = val
            self.hp_lo = val_lo
            self.hp_hi = val_hi
        elif attr == 'mp':
            self.num_mp = val
            self.mp_lo = val_lo
            self.mp_hi = val_hi
        else:
            # For now, have to cap
            if val >= 255:
                val = 255
            val_byte = val.to_bytes(1, 'little') or b'\0'
            setattr(self,attr,format(val_byte[0], '02x'))

    def apply_rank_mult(self):
        rank_mult = self.rank_mult
        for stat in ['num_phys_power','num_phys_def','num_mag_power','num_mag_def','num_gil','num_level']:

            setattr(self,stat,str(round(int(getattr(self,stat)) * rank_mult)))

        self.update_all()

    def update_all(self):
        self.update_val('exp',self.num_exp)
        self.update_val('gil',self.num_gil)
        self.update_val('hp',self.num_hp)
        self.update_val('mp',self.num_mp)
        self.update_val('gauge_time',self.num_gauge_time)
        self.update_val('phys_power',self.num_phys_power)
        self.update_val('phys_mult',self.num_phys_mult)
        self.update_val('evade',self.num_evade)
        self.update_val('phys_def',self.num_phys_def)
        self.update_val('mag_power',self.num_mag_power)
        self.update_val('mag_def',self.num_mag_def)
        self.update_val('mag_evade',self.num_mag_evade)
        self.update_val('level',self.num_level)  
        


class EnemyManager(object):
    def __init__(self, data_manager):
        self.enemies = [Enemy(x, data_manager, 'id') for x in range(0, NUM_ENEMIES)]
        self.relevant_enemies = []

    def get_patch(self, relevant=False):
        output = ";======="
        output = output + "\n;enemies"
        output = output + "\n;=======\n"
        if relevant == True:
            l = self.relevant_enemies
        else:
            l = self.enemies
        for i in l:
            output = output + i.asar_output + "\n"
        output = output + "\n"

        return output

    def get_loot_patch(self):
        output = "\n;Enemy Loot\n"
        for enemy in self.enemies:
#            steal_rare      = hex(int(y.stats_address,base=16) + 29)
#            drop_common     = hex(int(y.stats_address,base=16) + 30)
#            drop_rare       = hex(int(y.stats_address,base=16) + 31)
            output = output +   "; %s" % (enemy.enemy_name) + "\n" +\
                                "org $%s" % (enemy.drops_address) + "\n" +\
                                "db $%s, $%s, $%s, $%s" % (enemy.steal_common, enemy.steal_rare, enemy.drop_common, enemy.drop_rare) + "\n"
        return output
             
                
    def get_loot_spoiler(self):
        output = "\n-----ENEMY LOOT-----\n"
        output = output +   '{:16}'.format("Enemy Name") +\
                            '{:16}'.format("Steal (Common)") +\
                            '{:16}'.format("Steal (Rare)") +\
                            '{:16}'.format("Drop (Common)") +\
                            '{:16}'.format("Drop (Rare)")+"\n"
        for enemy in self.enemies:
             output = output +   '{:16}'.format(enemy.enemy_name) +\
                                 '{:16}'.format(enemy.steal_common_name) +\
                                 '{:16}'.format(enemy.steal_rare_name) +\
                                 '{:16}'.format(enemy.drop_common_name) +\
                                 '{:16}'.format(enemy.drop_rare_name)+"\n"
             
                     
        return output 

    def get_spoiler(self):
        output = "-----ENEMIES-----\n"
        for i in self.enemies:
            output = output + i.short_output + "\n"
        output = output + "-----*******-----\n"

        return output
    
    def set_portal_boss(self, portal_data, portal_boss_str, output_str):
        
        # This all currently supports 3 enemies, which replace LiquiFlame/Kuzar/SolCannon from Phoenix Tower
        # with entirely new enemies
        # It's ASSUMING there's three enemies as part of the process
        
        
        # STEPS TO MAKE NEW BOSSES
        # You can ignore the section below if you have 3 enemies in the formation 
        # Look for "UPDATE STEP" in notes below
        
        
        portal_indexes = [i for i in portal_data if portal_data[i]['enemy_name']==portal_boss_str]
        
        enemies = [[x for x in self.enemies if x.idx == 357][0],
                   [x for x in self.enemies if x.idx == 358][0],
                   [x for x in self.enemies if x.idx == 359][0]
                  ]
        
        self.relevant_enemies = self.relevant_enemies + enemies
        
        for _, enemy in enumerate(enemies):
            data = portal_data[portal_indexes[_]]
            for i in data.keys():
                if i == 'enemy_name':
                    setattr(enemy,i,str(data[i]))
                if "num_" in i:
                    setattr(enemy,i,str(data[i]).zfill(2))
                if i in [  'atk_index',
                            'elemental_immune',
                            'status0_immune',
                            'status1_immune',
                            'status2_immune',
                            'elemental_absorb',
                            'unavoidable_atk',
                            'elemental_weakness',
                            'enemy_type',
                            'special_immune',
                            'initial_status0',
                            'initial_status1',
                            'initial_status2',
                            'initial_status3',
                            'steal_common',
                            'steal_rare',
                            'drop_common',
                            'drop_rare']: 
                    setattr(enemy,i,str(data[i]).zfill(2))
            enemy.update_all()
            output_str = output_str + "\n" + (enemy.asar_output)

        # Change AI 
        if portal_boss_str == 'SomberMage':

            output_str = ''
            output_str = '\n\n; PORTAL BOSS\n'
            
            # Change liquiflame formation to not have opening hide and no ABP. Last byte shows who's unhidden
            output_str = output_str + "\n" + "; Formation changes"
            output_str = output_str + "\n" + ("org $D04EB0")
            output_str = output_str + "\n" + ("db $00, $80, $00, $80")
            
            # Add 3 bosses for liquiflame, kuzar, solcannon
            output_str = output_str + "\n" + ("org $D04EB4")
            output_str = output_str + "\n" + ("db $65, $66, $67")
            # Change to Exdeath W2 music and Strong Boss fade
            output_str = output_str + "\n" + ("org $D04EBE")
            output_str = output_str + "\n" + ("db $28, $21")
            
            
            # set liquidflame spot to AI
            output_str = output_str + "\n" + ";AI table changes"
            output_str = output_str + "\n" + ("org $D09ECA")
            output_str = output_str + "\n" + ("db $E0, $F1")
            # set kuzar ai
            output_str = output_str + "\n" + ("db $E0, $F2")
            # set solcannon ai
            output_str = output_str + "\n" + ("db $E0, $F3")
            
            output_str = output_str + "\n" + ";Formation table changes"
            # Formation table, which will correspond to battle code $BD, $55, $FF found in the custom event
            output_str = output_str + "\n" + ("org $D07954")
            output_str = output_str + "\n" + ("db $EB, $01") # ; use liquiflame formation in free space on lookup table
            output_str = output_str + "\n" + ("db $EB, $01") # ; duplicate for table sometimes pulling next address
            # Now pivot on which type of portal boss 

            ########## 
            # UPDATE STEP
            # Custom write AI for each of the forms
            ##########
            output_str = output_str + "\n" + ";AI Changes"
            #LiquiFlame AI
            
            data = parse_ai_data('somber_mage.txt')
            output_str = output_str + "\n" + data


            # End of battle dialogue
            output_str = output_str + "\n" + "org $D0F1D4"
            output_str = output_str + "\n" + "db $B0, $4F"
            
            output_str = output_str + "\n" + "org $E74FB0"
            output_str = output_str + "\n" + "db $A3, $A3, $A3, $00"
            ########## 
            # UPDATE STEP
            # Change formation x/y coords if necessary. Default is middle
            ##########
            output_str = output_str + "\n" + ";Enemy X/Y Coords"
            # ; Formation coords. Low byte x, High byte y coord
            output_str = output_str + "\n" + ("org $d09858")
            output_str = output_str + "\n" + ("db $78, $78, $78, $78, $78, $78, $78, $78") # ; default

            ########## 
            # UPDATE STEP
            # Change sprites. The addresses are always the same, but you can grab from enemy_data.csv, the rightmost columns
            # Then change the 4th byte (and also the $00 or $01 on the 3rd byte) for palette swaps
            ##########
            
            # Change sprites 
            # ; Cherie sprite
            output_str = output_str + "\n" + "; Battle sprite changes"
            output_str = output_str + "\n" + ("org $D4B879")
            output_str = output_str + "\n" + ("db $31, $27, $01, $68, $51")
            output_str = output_str + "\n" + ("db $31, $27, $01, $69, $51")
            output_str = output_str + "\n" + ("db $31, $27, $01, $5f, $51")
            

            ########## 
            # UPDATE STEP
            # Change name of enemy with text_parser2.py, limit of 10 characters
            ##########            
            # ; Change LiquiFlame, Kuzar and Sol Cannon name to SOMBERMAGE
            output_str = output_str + "\n" + ("org $E00E42")
            output_str = output_str + "\n" + ("db $72, $88, $86, $7B, $7E, $8B, $6C, $7A, $80, $7E")
            output_str = output_str + "\n" + ("db $72, $88, $86, $7B, $7E, $8B, $6C, $7A, $80, $7E")
            output_str = output_str + "\n" + ("db $72, $88, $86, $7B, $7E, $8B, $6C, $7A, $80, $7E")
            
            ########## 
            # UPDATE STEP
            # Change dialogue of enemy before battle
            ##########            

            output_str = output_str + "\n" + "; Pre-battle dialogue"
            output_str = output_str + "\n" + "org $E14BF1"
            output_str = output_str + "\n" + "db $73, $81, $7E, $96, $90, $82, $87, $7D, $96, $82, $8C, $96, $7C, $7A, $85, $85, $82, $87, $80, $A3, $A3, $A3, $96, $82, $8D, $99, $8C, $01, $8D, $82, $86, $7E, $96, $7F, $88, $8B, $96, $8E, $8C, $96, $8D, $88, $96, $7F, $82, $80, $81, $8D, $A3, $00"


        if portal_boss_str == 'RainSenshi':
            output_str = ''
            output_str = '\n\n; PORTAL BOSS\n'
            
            # Change liquiflame formation to not have opening hide and no ABP. Last byte shows who's unhidden
            output_str = output_str + "\n" + "; Formation changes"
            output_str = output_str + "\n" + ("org $D04EB0")
            output_str = output_str + "\n" + ("db $00, $80, $00, $80")
            
            # Add 3 bosses for liquiflame, kuzar, solcannon
            output_str = output_str + "\n" + ("org $D04EB4")
            output_str = output_str + "\n" + ("db $65, $66, $67")
            # Change to Exdeath W2 music and Strong Boss fade
            output_str = output_str + "\n" + ("org $D04EBE")
            output_str = output_str + "\n" + ("db $28, $21")
            
            
            # set liquidflame spot to AI
            output_str = output_str + "\n" + ";AI table changes"
            output_str = output_str + "\n" + ("org $D09ECA")
            output_str = output_str + "\n" + ("db $E0, $F1")
            # set kuzar ai
            output_str = output_str + "\n" + ("db $E0, $F2")
            # set solcannon ai
            output_str = output_str + "\n" + ("db $E0, $F3")
            
            output_str = output_str + "\n" + ";Formation table changes"
            # Formation table, which will correspond to battle code $BD, $55, $FF found in the custom event
            output_str = output_str + "\n" + ("org $D07954")
            output_str = output_str + "\n" + ("db $EB, $01") # ; use liquiflame formation in free space on lookup table
            output_str = output_str + "\n" + ("db $EB, $01") # ; duplicate for table sometimes pulling next address
            # Now pivot on which type of portal boss 
            ########## 
            # UPDATE STEP
            # Custom write AI for each of the forms
            ##########
            output_str = output_str + "\n" + ";AI Changes"
            #LiquiFlame AI

            data = parse_ai_data('rain_senshi.txt')
            output_str = output_str + "\n" + data


            # End of battle dialogue
            output_str = output_str + "\n" + "org $D0F1D4"
            output_str = output_str + "\n" + "db $B0, $4F"

            output_str = output_str + "\n" + "org $E74FB0"
            output_str = output_str + "\n" + "db $A3, $A3, $A3, $00"
            ########## 
            # UPDATE STEP
            # Change formation x/y coords if necessary. Default is middle
            ##########
            output_str = output_str + "\n" + ";Enemy X/Y Coords"
            # ; Formation coords. Low byte x, High byte y coord
            output_str = output_str + "\n" + ("org $d09858")
            output_str = output_str + "\n" + ("db $78, $78, $78, $78, $78, $78, $78, $78") # ; default

            ########## 
            # UPDATE STEP
            # Change sprites. The addresses are always the same, but you can grab from enemy_data.csv, the rightmost columns
            # Then change the 4th byte (and also the $00 or $01 on the 3rd byte) for palette swaps
            ##########


            # Change sprites 
            output_str = output_str + "\n" + "; Battle sprite changes"
            output_str = output_str + "\n" + ("org $D4B879")
            output_str = output_str + "\n" + ("db $2C, $FF, $01, $5D, $4B")
            output_str = output_str + "\n" + ("db $2C, $FF, $01, $4F, $4B")
            output_str = output_str + "\n" + ("db $86, $D3, $01, $3B, $12")


            ########## 
            # UPDATE STEP
            # Change name of enemy with text_parser2.py, limit of 10 characters
            ##########            
            # ; Change LiquiFlame, Kuzar and Sol Cannon name to name of enemy
            output_str = output_str + "\n" + ("org $E00E42")
            output_str = output_str + "\n" + ("db $71, $7A, $82, $87, $72, $7E, $87, $8C, $81, $82")
            output_str = output_str + "\n" + ("db $71, $7A, $82, $87, $72, $7E, $87, $8C, $81, $82")
            output_str = output_str + "\n" + ("db $71, $7A, $82, $87, $72, $7E, $87, $8C, $81, $82")

            ########## 
            # UPDATE STEP
            # Change dialogue of enemy before battle
            ##########            

            output_str = output_str + "\n" + "; Pre-battle dialogue"
            output_str = output_str + "\n" + "org $E14BF1"
            output_str = output_str + "\n" + "db $63, $8B, $7A, $90, $96, $92, $88, $8E, $8B, $96, $85, $7A, $8C, $8D, $96, $7B, $8B, $7E, $7A, $8D, $81, $01, $7A, $8C, $96, $8D, $81, $7E, $96, $8D, $82, $7D, $7A, $85, $96, $90, $7A, $8F, $7E, $96, $7A, $89, $89, $8B, $88, $7A, $7C, $81, $7E, $8C, $A3, $00"
        if portal_boss_str == 'DragonClan':
            
            
            output_str = ''
            output_str = '\n\n; PORTAL BOSS\n'
            
            # Change liquiflame formation to not have opening hide and no ABP. Last byte shows who's unhidden
            output_str = output_str + "\n" + "; Formation changes"
            output_str = output_str + "\n" + ("org $D04EB0")
            output_str = output_str + "\n" + ("db $00, $80, $00, $E0")
            
            # Add 3 bosses for liquiflame, kuzar, solcannon
            output_str = output_str + "\n" + ("org $D04EB4")
            output_str = output_str + "\n" + ("db $65, $66, $67")
            # Change to Exdeath W2 music and Strong Boss fade
            output_str = output_str + "\n" + ("org $D04EBC")
            output_str = output_str + "\n" + ("db $1B, $00, $28, $21")
            
            
            # set liquidflame spot to AI
            output_str = output_str + "\n" + ";AI table changes"
            output_str = output_str + "\n" + ("org $D09ECA")
            output_str = output_str + "\n" + ("db $E0, $F1")
            # set kuzar ai
            output_str = output_str + "\n" + ("db $E0, $F2")
            # set solcannon ai
            output_str = output_str + "\n" + ("db $E0, $F3")
            
            output_str = output_str + "\n" + ";Formation table changes"
            # Formation table, which will correspond to battle code $BD, $55, $FF found in the custom event
            output_str = output_str + "\n" + ("org $D07954")
            output_str = output_str + "\n" + ("db $EB, $01") # ; use liquiflame formation in free space on lookup table
            output_str = output_str + "\n" + ("db $EB, $01") # ; duplicate for table sometimes pulling next address
            # Now pivot on which type of portal boss 
            ########## 
            # UPDATE STEP
            # Custom write AI for each of the forms
            ##########
            output_str = output_str + "\n" + ";AI Changes"
            #LiquiFlame AI
            
            data = parse_ai_data('dragon_clan.txt')
            output_str = output_str + "\n" + data


            # End of battle dialogue
            output_str = output_str + "\n" + "org $D0F1D4"
            output_str = output_str + "\n" + "db $B0, $4F"
            
            output_str = output_str + "\n" + "org $E74FB0"
            output_str = output_str + "\n" + "db $A3, $A3, $A3, $00"
            ########## 
            # UPDATE STEP
            # Change formation x/y coords if necessary. Default is middle
            ##########
            output_str = output_str + "\n" + ";Enemy X/Y Coords"
            # ; Formation coords. Low byte x, High byte y coord
            output_str = output_str + "\n" + ("org $d09858")
            output_str = output_str + "\n" + ("db $70, $2B, $CB, $78, $78, $78, $78, $78") # ; default

            ########## 
            # UPDATE STEP
            # Change sprites. The addresses are always the same, but you can grab from enemy_data.csv, the rightmost columns
            # Then change the 4th byte (and also the $00 or $01 on the 3rd byte) for palette swaps
            ##########
            

            # Change sprites 
            output_str = output_str + "\n" + "; Battle sprite changes"
            output_str = output_str + "\n" + ("org $D4B879")
            output_str = output_str + "\n" + ("db $26, $6F, $C0, $BA, $12")
            output_str = output_str + "\n" + ("db $1A, $45, $80, $04, $0A") # 16, 06
            output_str = output_str + "\n" + ("db $27, $4F, $80, $48, $13")



            ########## 
            # UPDATE STEP
            # Change name of enemy with text_parser2.py, limit of 10 characters
            ##########            
            # ; Change LiquiFlame, Kuzar and Sol Cannon name to name of enemy
            output_str = output_str + "\n" + ("org $E00E42")
            output_str = output_str + "\n" + ("db $75, $7E, $85, $88, $7C, $82, $8D, $92, $00, $00")
            output_str = output_str + "\n" + ("db $73, $88, $8B, $8A, $8E, $7E, $00, $00, $00, $00")
            output_str = output_str + "\n" + ("db $65, $88, $8B, $7C, $7E, $00, $00, $00, $00, $00")
            
            ########## 
            # UPDATE STEP
            # Change dialogue of enemy before battle
            ##########            

            output_str = output_str + "\n" + "; Pre-battle dialogue"
            output_str = output_str + "\n" + "org $E14BF1"
            output_str = output_str + "\n" + "db $76, $81, $7A, $8D, $96, $81, $7A, $8F, $7E, $96, $92, $88, $8E, $96, $85, $7E, $7A, $8B, $87, $7E, $7D, $96, $7A, $7B, $88, $8E, $8D, $96, $8D, $81, $7E, $01, $85, $7A, $90, $8C, $96, $88, $7F, $96, $89, $81, $92, $8C, $82, $7C, $8C, $96, $8D, $88, $96, $89, $8B, $7E, $89, $7A, $8B, $7E, $96, $92, $88, $8E, $01, $7F, $88, $8B, $96, $8D, $81, $82, $8C, $96, $7B, $7A, $8D, $8D, $85, $7E, $A2, $96, $62, $88, $86, $7E, $A1, $00"



        if portal_boss_str == 'Tetsudono':
            
            
            output_str = ''
            output_str = '\n\n; PORTAL BOSS\n'
            
            # Change liquiflame formation to not have opening hide and no ABP. Last byte shows who's unhidden
            output_str = output_str + "\n" + "; Formation changes"
            output_str = output_str + "\n" + ("org $D04EB0")
            output_str = output_str + "\n" + ("db $00, $80, $00, $80")
            
            # Add 3 bosses for liquiflame, kuzar, solcannon
            output_str = output_str + "\n" + ("org $D04EB4")
            output_str = output_str + "\n" + ("db $65, $66, $67")
            # Change to Exdeath W2 music and Strong Boss fade
            output_str = output_str + "\n" + ("org $D04EBE")
            output_str = output_str + "\n" + ("db $28, $21")
            
            
            # set liquidflame spot to AI
            output_str = output_str + "\n" + ";AI table changes"
            output_str = output_str + "\n" + ("org $D09ECA")
            output_str = output_str + "\n" + ("db $E0, $F1")
            # set kuzar ai
            output_str = output_str + "\n" + ("db $E0, $F2")
            # set solcannon ai
            output_str = output_str + "\n" + ("db $E0, $F3")
            
            output_str = output_str + "\n" + ";Formation table changes"
            # Formation table, which will correspond to battle code $BD, $55, $FF found in the custom event
            output_str = output_str + "\n" + ("org $D07954")
            output_str = output_str + "\n" + ("db $EB, $01") # ; use liquiflame formation in free space on lookup table
            output_str = output_str + "\n" + ("db $EB, $01") # ; duplicate for table sometimes pulling next address
            # Now pivot on which type of portal boss 

            ########## 
            # UPDATE STEP
            # Custom write AI for each of the forms
            ##########
            output_str = output_str + "\n" + ";AI Changes"
            #LiquiFlame AI
            
            data = parse_ai_data('tetsudono.txt')
            output_str = output_str + "\n" + data


            # End of battle dialogue
            output_str = output_str + "\n" + "org $D0F1D4"
            output_str = output_str + "\n" + "db $B0, $4F"
            
            output_str = output_str + "\n" + "org $E74FB0"
            output_str = output_str + "\n" + "db $A3, $A3, $A3, $00"
            ########## 
            # UPDATE STEP
            # Change formation x/y coords if necessary. Default is middle
            ##########
            output_str = output_str + "\n" + ";Enemy X/Y Coords"
            # ; Formation coords. Low byte x, High byte y coord
            output_str = output_str + "\n" + ("org $d09858")
            output_str = output_str + "\n" + ("db $78, $78, $78, $78, $78, $78, $78, $78") # ; default

            ########## 
            # UPDATE STEP
            # Change sprites. The addresses are always the same, but you can grab from enemy_data.csv, the rightmost columns
            # Then change the 4th byte (and also the $00 or $01 on the 3rd byte) for palette swaps
            ##########
            
            # Change sprites 
            # ; Cherie sprite
            output_str = output_str + "\n" + "; Battle sprite changes"
            output_str = output_str + "\n" + ("org $D4B879")
            

            output_str = output_str + "\n" + ("db $32, $6A, $81, $51, $19")
            output_str = output_str + "\n" + ("db $32, $6A, $81, $53, $19")
            output_str = output_str + "\n" + ("db $32, $6A, $81, $4C, $19")
            

            ########## 
            # UPDATE STEP
            # Change name of enemy with text_parser2.py, limit of 10 characters
            ##########            
            # ; Change LiquiFlame, Kuzar and Sol Cannon name to TETSUDONO
            output_str = output_str + "\n" + ("org $E00E42")
            output_str = output_str + "\n" + ("db $73, $7E, $8D, $8C, $8E, $7D, $88, $87, $88, $FF")
            output_str = output_str + "\n" + ("db $73, $7E, $8D, $8C, $8E, $7D, $88, $87, $88, $FF")
            output_str = output_str + "\n" + ("db $73, $7E, $8D, $8C, $8E, $7D, $88, $87, $88, $FF")
            
            ########## 
            # UPDATE STEP
            # Change dialogue of enemy before battle
            ##########            

            output_str = output_str + "\n" + "; Pre-battle dialogue"
            output_str = output_str + "\n" + "org $E14BF1"
            output_str = output_str + "\n" + "db $65, $8B, $88, $86, $96, $8D, $81, $7E, $96, $7F, $88, $8B, $80, $7E, $A3, $A3, $A3, $01, $68, $96, $81, $7A, $8F, $7E, $96, $7A, $8B, $82, $8C, $7E, $87, $96, $8D, $88, $96, $7E, $91, $8D, $7E, $8B, $86, $82, $87, $7A, $8D, $7E, $96, $92, $88, $8E, $A3, $A3, $A3, $01, $61, $7E, $96, $80, $88, $87, $7E, $A1, $00"




        return output_str