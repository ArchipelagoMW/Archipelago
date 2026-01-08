from ..data.enemy import Enemy
from ..data.structures import DataArray

from ..data.enemy_formations import EnemyFormations
from ..data.enemy_packs import EnemyPacks
from ..data.enemy_zones import EnemyZones
from ..data.enemy_scripts import EnemyScripts
from ..data import bosses as bosses

class Enemies():
    DATA_START = 0xf0000
    DATA_END = 0xf2fff
    DATA_SIZE = 32

    NAMES_START = 0xfc050
    NAMES_END = 0xfd0cf
    NAME_SIZE = 10

    ITEMS_START = 0xf3000
    ITEMS_END = 0xf35ff
    ITEMS_SIZE = 4

    SPECIAL_NAMES_START = 0xfd0d0
    SPECIAL_NAMES_END = 0xfdfdf
    SPECIAL_NAMES_SIZE = 10

    DRAGON_COUNT = 8

    SRBEHEMOTH2_ID = 127
    INVINCIBLE_GUARDIAN_ID = 273

    def __init__(self, rom, args, items=[]):
        self.rom = rom
        self.args = args
        self.items = items

        self.enemy_data = DataArray(self.rom, self.DATA_START, self.DATA_END, self.DATA_SIZE)
        self.enemy_name_data = DataArray(self.rom, self.NAMES_START, self.NAMES_END, self.NAME_SIZE)
        self.enemy_item_data = DataArray(self.rom, self.ITEMS_START, self.ITEMS_END, self.ITEMS_SIZE)
        self.enemy_special_name_data = DataArray(self.rom, self.SPECIAL_NAMES_START, self.SPECIAL_NAMES_END, self.SPECIAL_NAMES_SIZE)

        self.enemies = []
        self.bosses = []
        for enemy_index in range(len(self.enemy_data)):
            enemy = Enemy(enemy_index, self.enemy_data[enemy_index], self.enemy_name_data[enemy_index], self.enemy_item_data[enemy_index], self.enemy_special_name_data[enemy_index])
            self.enemies.append(enemy)

            if enemy_index in bosses.enemy_name and enemy_index not in bosses.removed_enemy_name:
                self.bosses.append(enemy)

        self.formations = EnemyFormations(self.rom, self.args, self)
        self.packs = EnemyPacks(self.rom, self.args, self.formations)
        self.zones = EnemyZones(self.rom, self.args)
        self.scripts = EnemyScripts(self.rom, self.args, self)

        if self.args.doom_gaze_no_escape:
            # if doom gaze cannot escape, do not allow the party to escape from doom gaze
            # this prevents escaping from doom gaze in a shuffled/random place and getting a free check
            doom_gaze_id = self.get_enemy("Doom Gaze")
            self.enemies[doom_gaze_id].no_run = 1

    def __len__(self):
        return len(self.enemies)

    def get_random(self):
        import random
        random_enemy = random.choice(self.enemies[:255])
        return random_enemy.id

    def get_enemy(self, name):
        if name in bosses.name_enemy:
            return bosses.name_enemy[name]
        for enemy in self.enemies:
            if enemy.name == name:
                return enemy.id

    def get_name(self, enemy_id):
        if enemy_id in bosses.enemy_name:
            return bosses.enemy_name[enemy_id]
        return self.enemies[enemy_id].name

    def set_rare_steal(self, enemy_id, item_id):
        self.enemies[enemy_id].steal_rare = item_id

    def set_common_steal(self, enemy_id, item_id):
        self.enemies[enemy_id].steal_common = item_id

    def set_rare_drop(self, enemy_id, item_id):
        self.enemies[enemy_id].drop_rare = item_id

    def set_common_drop(self, enemy_id, item_id):
        self.enemies[enemy_id].drop_common = item_id

    def remove_fenix_downs(self):
        import random
        from ..data.item_names import name_id

        fenix_down = name_id["Fenix Down"]
        possible_replacements = ["Tonic", "Potion", "Tincture", "Antidote", "Echo Screen", "Eyedrop", "Green Cherry",
                                 "Revivify", "Soft", "Ether", "Sleeping Bag", "Tent", "Remedy", "Dried Meat"]
        possible_replacements = [name_id[item_name] for item_name in possible_replacements]

        for enemy in self.enemies:
            if enemy.steal_common == fenix_down:
                replacement = random.choice(possible_replacements)
                self.set_common_steal(enemy.id, replacement)

            if enemy.steal_rare == fenix_down:
                replacement = random.choice(possible_replacements)
                self.set_rare_steal(enemy.id, replacement)

            if enemy.drop_common == fenix_down:
                replacement = random.choice(possible_replacements)
                self.set_common_drop(enemy.id, replacement)

            if enemy.drop_rare == fenix_down:
                replacement = random.choice(possible_replacements)
                self.set_rare_drop(enemy.id, replacement)

    def apply_scaling(self):
        # lower vargas and whelk's hp
        vargas_id = self.get_enemy("Vargas")
        self.enemies[vargas_id].hp = self.enemies[vargas_id].hp // 2

        ultros3_id = self.get_enemy("Ultros 3")
        self.enemies[ultros3_id].hp = self.enemies[ultros3_id].hp // 2

        # increase hp of some early bosses (especially ones which are normally not fought with a full party)
        hp4x = ["Leader", "Marshal"]
        hp3x = ["Rizopas", "Piranha", "TunnelArmr"]
        hp2x = ["Ipooh", "GhostTrain", "Kefka (Narshe)", "Dadaluma", "Ifrit", "Shiva", "Number 024",
                "Number 128", "Left Blade", "Right Blade", "Left Crane", "Right Crane", "Nerapa"]

        if not self.args.boss_normalize_distort_stats:
            # double opera ultros' hp only if not already normalized
            # each form (location) has different hp pools so it is already challenging enough after the normalize
            hp2x.append("Ultros 2")

        for boss_id, boss_name in bosses.enemy_name.items():
            enemy = self.enemies[boss_id]
            if boss_name in hp4x:
                enemy.hp *= 4
            elif boss_name in hp3x:
                enemy.hp *= 3
            elif boss_name in hp2x:
                enemy.hp *= 2

    def boss_experience(self):
        from ..data.bosses_custom_exp import custom_exp
        for enemy_id, exp in custom_exp.items():
            self.enemies[enemy_id].exp = exp * self.enemies[enemy_id].level

    def boss_normalize_distort_stats(self):
        import random

        def stat_min_max(stat_value, min_possible, max_possible):
            distortion_percent = 0.25
            stat_distortion_amount = int(stat_value * distortion_percent)

            # if distortion_percent can potentially set value outside allowed range
            # then set the distortion to the max amount allowable
            if stat_value - stat_distortion_amount < min_possible:
                stat_distortion_amount = stat_value
            elif stat_value + stat_distortion_amount > max_possible:
                stat_distortion_amount = max_possible - stat_value

            stat_min = stat_value - stat_distortion_amount
            stat_max = stat_value + stat_distortion_amount

            return stat_min, stat_max

        stats = ["speed", "vigor", "accuracy", "evasion", "magic_evasion", "defense", "magic_defense", "magic"]
        min_stat_max = [70, 24, 100, 0, 0, 150, 160, 16] # minimum values for maximum random values

        for enemy in self.bosses:
            for stat_index, stat in enumerate(stats):
                stat_value = getattr(enemy, stat)
                stat_min, stat_max = stat_min_max(stat_value, 0, 2**8 - 1)

                if stat_max < min_stat_max[stat_index]:
                    # max rand value is lower than the minimum for this stat, increase it to the minimum
                    stat_max = min_stat_max[stat_index]

                setattr(enemy, stat, random.randint(stat_min, stat_max))

        stats = ["hp", "mp"]
        for enemy in self.bosses:
            hp_min, hp_max = stat_min_max(enemy.hp, 0, 2**16 - 1)
            mp_min, mp_max = stat_min_max(enemy.mp, 0, 2**16 - 1)

            # minimum hp/mp max values based on mean (hp / level) and mean (mp / level) of bosses
            # cap the max at triple the original hp/mp
            min_hp_max = min(enemy.level * 500, enemy.hp * 3)
            min_mp_max = min(enemy.level * 150, enemy.mp * 3)

            if hp_max < min_hp_max:
                hp_max = min_hp_max
            if mp_max < min_mp_max:
                mp_max = min_mp_max

            enemy.hp = random.randint(hp_min, hp_max)
            enemy.mp = random.randint(mp_min, mp_max)

    def skip_shuffling_zone(self, maps, zone):
        if zone.MAP and zone.id >= maps.MAP_COUNT:
            return True # do not shuffle map zones that do not correspond to a map

        if zone.MAP and not maps.properties[zone.id].enable_random_encounters:
            return True # do not shuffle map zones with disabled random encounters

        return False

    def skip_shuffling_pack(self, pack, encounter_rate):
        from ..data.enemy_zone import EnemyZone

        if pack == 0 and encounter_rate == EnemyZone.NORMAL_ENCOUNTER_RATE:
            # 0 is used as a placeholder (leafer x1 and leafer x2, dark wind)
            # luckily the real ones outside narshe have lower encounter rates to differentiate them
            # except for the forest, does this cause problems?
            return True

        if pack == EnemyPacks.VELDT:
            return True

        if pack == EnemyPacks.ZONE_EATER:
            return True

        return False

    def skip_shuffling_formation(self, formation):
        if formation == EnemyFormations.PRESENTER:
            return True

        return False

    def shuffle_encounters(self, maps):
        import collections
        # find all packs that are randomly encountered in zones
        packs = collections.OrderedDict()
        for zone in self.zones.zones:
            if self.skip_shuffling_zone(maps, zone):
                continue

            for x in range(zone.PACK_COUNT):
                if self.skip_shuffling_pack(zone.packs[x], zone.encounter_rates[x]):
                    continue

                packs[self.packs.packs[zone.packs[x]]] = None

        # find all formations that are randomly encountered in packs
        formations = []
        for pack in packs:
            for y in range(pack.FORMATION_COUNT):
                if self.skip_shuffling_formation(pack.formations[y]):
                    continue

                if pack.extra_formations[y]:
                    # pack has extra formations (i.e. each formation is randomized with the subsequent 3 formations)
                    # unfortunately, this means there are more formations than packs to put them in, so some formations are lost
                    for x in range(4):
                        formations.append(pack.formations[y] + x)
                else:
                    formations.append(pack.formations[y])

        # shuffle the randomly encounterable formations
        import random
        random.shuffle(formations)

        for pack in packs:
            for y in range(pack.FORMATION_COUNT):
                if self.skip_shuffling_formation(pack.formations[y]):
                    continue

                pack.formations[y] = formations.pop()

        # NOTE: any remaining formations (due to extra_formations) are lost

    def chupon_encounters(self, maps):
        # find all packs that are randomly encountered in zones
        packs = []
        for zone in self.zones.zones:
            if self.skip_shuffling_zone(maps, zone):
                continue

            for x in range(zone.PACK_COUNT):
                if self.skip_shuffling_pack(zone.packs[x], zone.encounter_rates[x]):
                    continue

                packs.append(zone.packs[x])

        self.packs.chupon_packs(packs)
        
    def randomize_encounters(self, maps):
        # find all packs that are randomly encountered in zones
        packs = []
        boss_percent = self.args.random_encounters_random / 100.0
        for zone in self.zones.zones:
            if self.skip_shuffling_zone(maps, zone):
                continue

            for x in range(zone.PACK_COUNT):
                if self.skip_shuffling_pack(zone.packs[x], zone.encounter_rates[x]):
                    continue

                packs.append(zone.packs[x])

        self.packs.randomize_packs(packs, boss_percent)

    def randomize_loot(self):
        for enemy in self.enemies:
            self.set_common_steal(enemy.id, self.items.get_random())
            self.set_rare_steal(enemy.id, self.items.get_random())
            self.set_common_drop(enemy.id, self.items.get_random())
            self.set_rare_drop(enemy.id, self.items.get_random())

    def shuffle_steals_drops_random(self):
        import random
        from ..data.bosses import final_battle_enemy_name

        # Assemble the list of steals and drops
        steals_drops = []
        for enemy in self.enemies:
            if len(enemy.name) > 0:
                loot_list = [enemy.steal_common, enemy.steal_rare]
                if enemy.id not in final_battle_enemy_name.keys():
                    loot_list += [enemy.drop_common, enemy.drop_rare]
                steals_drops.extend(loot_list)

        # Randomize the requested number
        random_percent = self.args.shuffle_steals_drops_random_percent / 100.0
        number_random = int(random_percent * len(steals_drops))
        which_random = [a for a in range(len(steals_drops))]
        random.shuffle(which_random)
        for id in range(number_random):
            steals_drops[which_random[id]] = self.items.get_random()

        # Shuffle list & reassign to enemies
        random.shuffle(steals_drops)
        for enemy in self.enemies:
            if len(enemy.name) > 0:
                self.set_common_steal(enemy.id, steals_drops.pop(0))
                self.set_rare_steal(enemy.id, steals_drops.pop(0))
                if enemy.id not in final_battle_enemy_name.keys():
                    self.set_common_drop(enemy.id, steals_drops.pop(0))
                    self.set_rare_drop(enemy.id, steals_drops.pop(0))

    def set_escapable(self):
        import random

        escapable_percent = self.args.encounters_escapable_random / 100.0
        for enemy in self.enemies:
            if enemy.id in bosses.enemy_name or enemy.id == self.SRBEHEMOTH2_ID or enemy.id == self.INVINCIBLE_GUARDIAN_ID:
                continue

            enemy.no_run = random.random() >= escapable_percent

    def no_undead_bosses(self):
        boss_ids = list(bosses.enemy_name.keys())
        boss_ids.append(self.SRBEHEMOTH2_ID)

        for boss_id in boss_ids:
            self.enemies[boss_id].undead = False

    def scan_all(self):
        for enemy in self.enemies:
            enemy.no_scan = 0

    def mod(self, maps):
        if self.args.boss_normalize_distort_stats:
            self.boss_normalize_distort_stats()

        if self.args.shuffle_steals_drops:
            self.shuffle_steals_drops_random()

        if self.args.permadeath:
            self.remove_fenix_downs()

        self.apply_scaling()

        if self.args.boss_experience:
            self.boss_experience()

        if not self.args.encounters_escapable_original:
            self.set_escapable()

        if self.args.boss_no_undead:
            self.no_undead_bosses()

        if self.args.random_encounters_shuffle:
            self.shuffle_encounters(maps)
        elif self.args.random_encounters_chupon:
            self.chupon_encounters(maps)
        elif not self.args.random_encounters_original:
            self.randomize_encounters(maps)

        self.formations.mod()
        self.packs.mod()
        self.zones.mod()
        self.scripts.mod()

        if self.args.scan_all:
            self.scan_all()

        if self.args.debug:
            for enemy in self.enemies:
                enemy.debug_mod()

    def get_event_boss(self, original_boss_name):
        return self.packs.get_event_boss_replacement(original_boss_name)

    def print(self):
        for enemy in self.enemies:
            enemy.print()

    def write(self):
        for enemy_index in range(len(self.enemies)):
            self.enemy_data[enemy_index] = self.enemies[enemy_index].data()
            self.enemy_name_data[enemy_index] = self.enemies[enemy_index].name_data()
            self.enemy_item_data[enemy_index] = self.enemies[enemy_index].item_data()
            self.enemy_special_name_data[enemy_index] = self.enemies[enemy_index].special_name_data()

        self.enemy_data.write()
        self.enemy_name_data.write()
        self.enemy_item_data.write()
        self.enemy_special_name_data.write()

        self.formations.write()
        self.packs.write()
        self.zones.write()
        self.scripts.write()
