import pkgutil, json
import os
import sys


THIS_FILEPATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append(THIS_FILEPATH)


class DataManager():
    def __init__(self, config):
        self.config = config
        self.data_table_path = self.config['PATHS']['data_table_path']

        self.files = {}
        
        def load_json_data(filepath: str):
            return json.loads(pkgutil.get_data(__name__,filepath).decode('utf-8-sig'))


        self.files['areas'] = load_json_data(os.path.join('tables', 'json','areas.json'))
        self.files['items'] = load_json_data(os.path.join('tables', 'json','item_id.json'))
        self.files['magics'] = load_json_data(os.path.join('tables', 'json','magic_id.json'))
        self.files['crystals'] = load_json_data(os.path.join('tables', 'json','crystal_id.json'))
        self.files['abilities'] = load_json_data(os.path.join('tables', 'json','ability_id.json'))
        self.files['gil'] = load_json_data(os.path.join('tables', 'json','gil_rewards.json'))
        self.files['key_items'] = load_json_data(os.path.join('tables', 'json','key_items.json'))
        self.files['rewards'] = load_json_data(os.path.join('tables', 'json','rewards.json'))
        self.files['mib_arch_rank'] = load_json_data(os.path.join('tables', 'json','mib_arch_rank.json'))



        d = {}
        for k, v in self.files['rewards'].items():
            d[int(k)] = v
        self.files['rewards'] = d

        self.files['shops'] = load_json_data(os.path.join('tables', 'json','shop_id.json'))
        d = {}
        for k, v in self.files['shops'].items():
            d[int(k)] = v
        self.files['shops'] = d

        self.files['shopprices'] = load_json_data(os.path.join('tables', 'json','shop_prices.json'))
        d = {}
        for k, v in self.files['shopprices'].items():
            d[int(k)] = v
        self.files['shopprices'] = d

        self.files['enemies'] = load_json_data(os.path.join('tables', 'json','enemy_data.json'))
        self.files['enemies_bosses'] = {}
        self.files['enemies_nonbosses'] = {} 
        for k, v in self.files['enemies'].items():
            if v['enemy_rank'] == 'boss':
                self.files['enemies_bosses'][k] = v
            elif v['enemy_rank'] == 'enemy':
                self.files['enemies_nonbosses'][k] = v
        self.files['formations'] = load_json_data(os.path.join('tables', 'json','formation_id.json'))
        self.files['monsters_in_boxes'] = load_json_data(os.path.join('tables', 'json','monster_in_a_box.json'))
        d = {}
        for k, v in self.files['monsters_in_boxes'].items():
            if v['useable_flag'] == 'y':
                d[int(k)] = v
        self.files['monsters_in_boxes'] = d
        self.files['boss_scaling'] = load_json_data(os.path.join('tables', 'json','boss_scaling.json'))
        self.files['portal_bosses'] = load_json_data(os.path.join('tables', 'json','portal_bosses.json'))
        self.files['enemy_skills'] = load_json_data(os.path.join('tables', 'json','enemy_skills.json'))
        self.files['job_color_palettes'] = load_json_data(os.path.join('tables', 'json','job_color_palettes.json'))
        self.files['boss_color_palettes'] = load_json_data(os.path.join('tables', 'json','boss_color_palettes.json'))
        self.files['hints'] = load_json_data(os.path.join('tables', 'json','hint_npc.json'))
        self.files['weapon_randomization'] = load_json_data(os.path.join('tables', 'json','weapon_randomization_id.json'))
        d = {}
        for k, v in self.files['weapon_randomization'].items():
            if v['valid'] and v['type'] == 'weapon':
                d[k] = v
        self.files['weapon_randomization'] = d
        self.files['magic_item_randomization'] = load_json_data(os.path.join('tables', 'json','magic_id.json'))
        d = {}
        for k, v in self.files['magic_item_randomization'].items():
            if v['item_randomization_valid']:
                d[k] = v
        self.files['magic_item_randomization'] = d
        self.files['custom_weapons'] = load_json_data(os.path.join('tables', 'json','custom_weapons_v2.json'))
        self.files['arch_id'] = load_json_data(os.path.join('tables', 'json','arch_id.json'))
        
        
        
        