from ..data import text as text

class Character():
    # every 2 seconds while running in battle the character's run value is incremented by a
    # random number from 1 to run_success. Once it reaches battle's threshold (and atb full) the character runs
    # run_success value is between 2 and 5, but 0b11 = 2, 0b10 = 3, 0b01 = 4, 0b00 = 5 (run_val = 5 - bit_val)
    MIN_RUN_SUCCESS = 2
    MAX_RUN_SUCCESS = 5

    def __init__(self, id, init_data, name_data):
        self.id = id
        self.name = text.get_string(name_data, text.TEXT2).rstrip('\0')

        self.init_extra_hp      = init_data[0]
        self.init_extra_mp      = init_data[1]
        self.commands           = init_data[2 : 6]
        self.init_vigor         = init_data[6]
        self.init_speed         = init_data[7]
        self.init_stamina       = init_data[8]
        self.init_magic         = init_data[9]
        self.init_attack        = init_data[10]
        self.init_defense       = init_data[11]
        self.init_magic_defense = init_data[12]
        self.init_evasion       = init_data[13]
        self.init_magic_evasion = init_data[14]
        self.init_right_hand    = init_data[15]
        self.init_left_hand     = init_data[16]
        self.init_body          = init_data[18] # https://discord.com/channels/666661907628949504/931737764205047858/1069220818300698675
        self.init_head          = init_data[17]
        self.init_relic1        = init_data[19]
        self.init_relic2        = init_data[20]
        self._init_run_success  = init_data[21] & 0x03
        self._init_level_factor = (init_data[21] & 0x0c) >> 2
        self._cant_reequip      = (init_data[21] & 0x10) >> 4

    def init_data(self):
        from ..data.characters import Characters
        init_data = [0x00] * Characters.INIT_DATA_SIZE

        init_data[0]     = self.init_extra_hp
        init_data[1]     = self.init_extra_mp
        init_data[2 : 6] = self.commands
        init_data[6]     = self.init_vigor
        init_data[7]     = self.init_speed
        init_data[8]     = self.init_stamina
        init_data[9]     = self.init_magic
        init_data[10]    = self.init_attack
        init_data[11]    = self.init_defense
        init_data[12]    = self.init_magic_defense
        init_data[13]    = self.init_evasion
        init_data[14]    = self.init_magic_evasion
        init_data[15]    = self.init_right_hand
        init_data[16]    = self.init_left_hand
        init_data[18]    = self.init_body
        init_data[17]    = self.init_head
        init_data[19]    = self.init_relic1
        init_data[20]    = self.init_relic2
        init_data[21]    = self._init_run_success
        init_data[21]   |= self._init_level_factor   << 2
        init_data[21]   |= self._cant_reequip        << 4

        return init_data

    def name_data(self):
        from ..data.characters import Characters
        data = text.get_bytes(self.name, text.TEXT2)
        data.extend([0xff] * (Characters.NAME_SIZE - len(data)))
        return data

    def clear_init_equip(self):
        from ..data.items import Items
        self.init_right_hand = Items.EMPTY
        self.init_left_hand = Items.EMPTY
        self.init_body = Items.EMPTY
        self.init_head = Items.EMPTY
        self.init_relic1 = Items.EMPTY
        self.init_relic2 = Items.EMPTY

    @property
    def init_run_success(self):
        return self.MAX_RUN_SUCCESS - self._init_run_success

    @init_run_success.setter
    def init_run_success(self, value):
        if value < self.MIN_RUN_SUCCESS or value > self.MAX_RUN_SUCCESS:
            raise ValueError(f"Character.init_run_success setter: invalid value {value}")

        self._init_run_success = value - self.MAX_RUN_SUCCESS

    # initial level of characters is 3
    # when new character is recruited, their level is set to the average of all other recruited characters + init_level_factor
    @property
    def init_level_factor(self):
        VALUE_ADJUSTMENT = [0, 2, 5, -3]
        return VALUE_ADJUSTMENT[self._init_level_factor]

    @init_level_factor.setter
    def init_level_factor(self, adjustment):
        ADJUSTMENT_VALUE = {0 : 0, 2 : 1, 5 : 2, -3 : 3} # level adjustment -> data value
        self._init_level_factor = ADJUSTMENT_VALUE[adjustment]


    def print(self):
        print(f"{self.id}: {self.name}\n"
              f"{self.init_extra_hp}, {self.init_extra_mp}, {self.commands}"
              f"{self.init_vigor}, {self.init_speed}, {self.init_stamina}, {self.init_magic}, {self.init_attack}, "
              f"{self.init_defense}, {self.init_magic_defense}, {self.init_evasion}, {self.init_magic_evasion}, "
              f"{self.init_right_hand}, {self.init_left_hand}, {self.init_body}, {self.init_head}, "
              f"{self.init_relic1}, {self.init_relic2}, {self._init_run_success}, {self._init_level_factor}, {self._cant_reequip}")
