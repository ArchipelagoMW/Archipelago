class StatusEffects:
    GROUP_A = ["dark", "zombie", "poison", "magitek", "clear", "imp", "petrify", "death"]
    GROUP_B = ["condemn", "near_fatal", "image", "mute", "berserk", "muddle", "seizure", "sleep"]
    GROUP_C = ["dance", "regen", "slow", "haste", "stop", "shell", "safe", "reflect"]
    GROUP_D = ["rage", "frozen", "reraise", "morph", "chant", "hide", "interceptor", "float"]


    def __init__(self, groups, data):
        assert(len(groups) == len(data))
        self.groups = groups

        for group, byte in zip(self.groups, data):
            for index, name in enumerate(group):
                value = (byte >> index) & 0x01
                setattr(self, name, value)

    def data(self):
        data = [0x00] * len(self.groups)

        for index, group in enumerate(self.groups):
            for effect_index, effect_name in enumerate(group):
                data[index] |= getattr(self, effect_name) << effect_index

        return data
