class EnemyFormation():
    ENEMY_CAPACITY = 6 # up to 6 enemies in a formation

    def __init__(self, id, flags_data, enemies_data):
        self.id = id

        # flags data
        self.appearance_animation       = (flags_data[0] & 0x0f) >> 0
        self.disable_front_attack       = (flags_data[0] & 0x10) >> 4
        self.disable_back_attack        = (flags_data[0] & 0x20) >> 5
        self.disable_pincer_attack      = (flags_data[0] & 0x40) >> 6
        self.disable_side_attack        = (flags_data[0] & 0x80) >> 7

        self.unknown1                   = (flags_data[1] & 0x01) >> 0
        self.disable_victory_dance      = (flags_data[1] & 0x02) >> 1
        self.enable_joker_doom          = (flags_data[1] & 0x04) >> 2
        self.leapable                   = (flags_data[1] & 0x08) >> 3
        self.unknown2                   = (flags_data[1] & 0x10) >> 4
        self.unknown3                   = (flags_data[1] & 0x20) >> 5
        self.unknown4                   = (flags_data[1] & 0x40) >> 6
        self.enable_event_script        = (flags_data[1] & 0x80) >> 7

        self.event_script               = flags_data[2]

        self.disable_escape             = (flags_data[3] & 0x01) >> 0 # no running animation and no "Can't run away!!" dialog
        self.not_on_veldt               = (flags_data[3] & 0x02) >> 1
        self.show_attack_type_windows   = (flags_data[3] & 0x04) >> 2
        self.disable_start_messages     = (flags_data[3] & 0x08) >> 3
        self.battle_music               = (flags_data[3] & 0x70) >> 4
        self.disable_battle_music       = (flags_data[3] & 0x80) >> 7

        # enemies data
        self.mold                       = enemies_data[0]

        self.enemy_slots                = (enemies_data[1] & 0x3f) >> 0
        self.unknown5                   = (enemies_data[1] & 0xc0) >> 6

        cur_byte = 2
        self.enemy_ids = []
        for enemy_index in range(self.ENEMY_CAPACITY):
            self.enemy_ids.append(enemies_data[cur_byte])
            cur_byte += 1

        self.enemy_y_positions = []
        self.enemy_x_positions = []
        for enemy_index in range(self.ENEMY_CAPACITY):
            y_pos                       = (enemies_data[cur_byte] & 0x0f) >> 0
            x_pos                       = (enemies_data[cur_byte] & 0xf0) >> 4

            self.enemy_y_positions.append(y_pos)
            self.enemy_x_positions.append(x_pos)
            cur_byte += 1

        enemy_id_msbs                   = (enemies_data[14] & 0x3f) >> 0
        self.unknown6                   = (enemies_data[14] & 0xc0) >> 6

        # apply most significant bits to enemy ids
        for enemy_index in range(len(self.enemy_ids)):
            if enemy_id_msbs & (1 << enemy_index):
                self.enemy_ids[enemy_index] += 256

    def flags_data(self):
        from ..data.enemy_formations import EnemyFormations
        flags_data = [0x00] * EnemyFormations.FLAGS_SIZE

        flags_data[0]       = self.appearance_animation     << 0
        flags_data[0]      |= self.disable_front_attack     << 4
        flags_data[0]      |= self.disable_back_attack      << 5
        flags_data[0]      |= self.disable_pincer_attack    << 6
        flags_data[0]      |= self.disable_side_attack      << 7

        flags_data[1]       = self.unknown1                 << 0
        flags_data[1]      |= self.disable_victory_dance    << 1
        flags_data[1]      |= self.enable_joker_doom        << 2
        flags_data[1]      |= self.leapable                 << 3
        flags_data[1]      |= self.unknown2                 << 4
        flags_data[1]      |= self.unknown3                 << 5
        flags_data[1]      |= self.unknown4                 << 6
        flags_data[1]      |= self.enable_event_script      << 7

        flags_data[2]       = self.event_script

        flags_data[3]       = self.disable_escape           << 0
        flags_data[3]      |= self.not_on_veldt             << 1
        flags_data[3]      |= self.show_attack_type_windows << 2
        flags_data[3]      |= self.disable_start_messages   << 3
        flags_data[3]      |= self.battle_music             << 4
        flags_data[3]      |= self.disable_battle_music     << 7

        return flags_data

    def enemies_data(self):
        from ..data.enemy_formations import EnemyFormations
        enemies_data = [0x00] * EnemyFormations.ENEMIES_SIZE

        enemies_data[0]     = self.mold

        enemies_data[1]     = self.enemy_slots              << 0
        enemies_data[1]    |= self.unknown5                 << 6

        cur_byte = 2
        enemy_id_msbs = 0
        for enemy_index in range(self.ENEMY_CAPACITY):
            enemy_id = self.enemy_ids[enemy_index]
            if enemy_id >= 256:
                enemy_id -= 256                     # remove msb
                enemy_id_msbs |= 1 << enemy_index   # record msb
            enemies_data[cur_byte] = enemy_id
            cur_byte += 1

        for enemy_index in range(self.ENEMY_CAPACITY):
            y_pos = self.enemy_y_positions[enemy_index]
            x_pos = self.enemy_x_positions[enemy_index]

            enemies_data[cur_byte]  = y_pos                 << 0
            enemies_data[cur_byte] |= x_pos                 << 4
            cur_byte += 1

        enemies_data[14]    = enemy_id_msbs                 << 0
        enemies_data[14]   |= self.unknown6                 << 6

        return enemies_data

    def enemies(self):
        result = []
        for enemy_index in range(len(self.enemy_ids)):
            if self.enemy_slots & (1 << enemy_index):
                result.append(self.enemy_ids[enemy_index])
        return result
