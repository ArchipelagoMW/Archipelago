from ..data.enemy_formation import EnemyFormation
from ..data.structures import DataArray
from ..data import bosses as bosses

class EnemyFormations():
    FLAGS_START = 0xf5900
    FLAGS_END = 0xf61ff
    FLAGS_SIZE = 4

    ENEMIES_START = 0xf6200
    ENEMIES_END = 0xf83bf
    ENEMIES_SIZE = 15

    PHUNBABA3 = bosses.name_formation["Phunbaba 3"]
    DOOM_GAZE = bosses.name_formation["Doom Gaze"]
    ALL_STATUES = list(bosses.statue_formation_name)
    ALL_DRAGONS = list(bosses.dragon_formation_name)
    PRESENTER = 433
    COLISEUM = 575
    CHUPON = 563 # Otherwise unused formation -- we'll use it for the random_encounters_chupon flag.

    def __init__(self, rom, args, enemies):
        self.rom = rom
        self.args = args
        self.enemies = enemies

        self.flags_data = DataArray(self.rom, self.FLAGS_START, self.FLAGS_END, self.FLAGS_SIZE)
        self.enemies_data = DataArray(self.rom, self.ENEMIES_START, self.ENEMIES_END, self.ENEMIES_SIZE)

        self.dragons = list(bosses.dragon_formation_name)
        self.bosses = list(bosses.normal_formation_name)

        # formations not to include in "normal" (i.e. non-boss/dragon) pool
        self.non_normal = [*self.dragons, *self.bosses, 4, 40, 42, 43, 59, 60, 63, 252, 335,
                           *range(384, 387), *range(388, 394), 420, 421, 424, *range(434, 465),
                           *range(467, 472), *range(473, 476), 477, 481, 482, 484, 485, *range(487, 576)]
        non_normal_set = set(self.non_normal)

        self.normal = []
        self.formations = []
        self.formation_names = []
        for formation_index in range(len(self.flags_data)):
            formation = EnemyFormation(formation_index, self.flags_data[formation_index], self.enemies_data[formation_index])
            self.formations.append(formation)

            if formation_index not in non_normal_set:
                self.normal.append(formation_index)

            # name the formation based on enemies and their counts
            enemy_count = {}
            enemies = formation.enemies()
            for enemy_id in enemies:
                if enemy_id in enemy_count:
                    enemy_count[enemy_id] += 1
                else:
                    enemy_count[enemy_id] = 1

            name = ""
            for enemy_id, count in enemy_count.items():
                if count == 1:
                    name += f"{self.enemies.get_name(enemy_id)}, "
                else:
                    name += f"{self.enemies.get_name(enemy_id)} x{count}, "
            self.formation_names.append(name[:-2])

    def __len__(self):
        return len(self.formations)

    def get_id(self, name):
        if name in bosses.name_formation:
            return bosses.name_formation[name]
        for formation_index, formation_name in self.formation_names:
            if formation_name == name:
                return formation_index

    def get_name(self, formation_id):
        if formation_id in bosses.formation_name:
            return bosses.formation_name[formation_id]
        return self.formation_names[formation_id]

    def get_enemies(self, formation_id):
        return self.formations[formation_id].enemies()

    def has_enemy(self, formation_id, enemy_id):
        enemies = self.get_enemies(formation_id)
        for cur_enemy_id in enemies:
            if cur_enemy_id == enemy_id:
                return True
        return False

    def get_random_normal(self):
        import random
        return random.choice(self.normal)

    def get_random_boss(self, exclude = None):
        import random
        if exclude is None:
            return random.choice(self.bosses)

        possible_bosses = [boss_id for boss_id in self.bosses if boss_id not in exclude]
        return random.choice(possible_bosses)

    def get_random_dragon(self):
        import random
        return random.choice(self.dragons)

    def set_chadarnook_position_left_screen(self):
        self.formations[456].enemy_x_positions[0] = 1 # painting
        self.formations[456].enemy_x_positions[1] = 1 # demon

    def randomize_marshal_minion(self):
        # adjust lobo positions to allow larger randomized enemy sprites to fit
        self.formations[bosses.name_formation["Marshal"]].enemy_y_positions[0] -= 2
        self.formations[bosses.name_formation["Marshal"]].enemy_y_positions[1] -= 2

        # Enemy id's are the same as rage IDs.
        from ..constants.rages import rage_id
        import random
        possible_minions = [
            rage_id["Red Wolf"],
            rage_id["Covert"],
            rage_id["Ogor"],
            rage_id["Tap Dancer"],
            rage_id["Sky Cap"],
            rage_id["Dueller"],
            rage_id["Fortis"],
            rage_id["Tyranosaur"],
            rage_id["PlutoArmor"],
            rage_id["Barb-e"],
            rage_id["Retainer"]
        ]
        random_minion = random.choice(possible_minions)
        self.formations[bosses.name_formation["Marshal"]].enemy_ids[0] = random_minion
        self.formations[bosses.name_formation["Marshal"]].enemy_ids[1] = random_minion


    def add_chupon(self):
        # Add Chupon (Coliseum) to an unused formation for use with random_encounters_chupon
        self.formations[self.CHUPON].enemy_ids[0] = 64 # Chupon (Coliseum)
        self.formations[self.CHUPON].enemy_slots = 1
        self.formations[self.CHUPON].not_on_veldt = 1
        self.formations[self.CHUPON].disable_back_attack = 1
        self.formations[self.CHUPON].disable_pincer_attack = 1
        self.formations[self.CHUPON].disable_side_attack = 1
        self.formations[self.CHUPON].enemy_y_positions[0] = 5
        self.formations[self.CHUPON].enemy_x_positions[0] = 6
        self.formations[self.CHUPON].mold = 6 << 4

    def write(self):
        for formation_index in range(len(self.formations)):
            self.flags_data[formation_index] = self.formations[formation_index].flags_data()
            self.enemies_data[formation_index] = self.formations[formation_index].enemies_data()

        self.flags_data.write()
        self.enemies_data.write()

    def mod(self):
        # disable sabin/vargas mt kolts battle script
        self.formations[435].event_script = 0
        self.formations[435].enable_event_script = 0

        # disable relm/ultros esper mountain battle script
        self.formations[387].event_script = 0
        self.formations[387].enable_event_script = 0

        if self.args.boss_battles_shuffle or self.args.boss_battles_random:
            # second srbehemoth only appears as a front attack with shuffled/random boss battles
            self.formations[424].disable_front_attack = 0
            self.formations[424].disable_back_attack = 1

            # move chadarnook to left edge of screen, somewhat misaligns on the original owzer's mansion battle background
            # but it looks better than having chadarnook's left edge showing on all the other battle backgrounds
            self.set_chadarnook_position_left_screen()

        # Randomize the minions that appear with Marshal
        if not self.args.boss_marshal_keep_lobos:
            self.randomize_marshal_minion()

        if self.args.random_encounters_chupon:
            self.add_chupon()

    def print_scripts(self):
        for formation_index, formation in enumerate(self.formations):
            if formation.enable_event_script:
                print("{}: script {}".format(formation_index, hex(formation.event_script)))
