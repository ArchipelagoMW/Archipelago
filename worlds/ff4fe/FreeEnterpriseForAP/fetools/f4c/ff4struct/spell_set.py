class SpellSet:
    def __init__(self):
        self.initial_spells = []
        self.learned_spells = {}

    def encode_initial(self):
        return (self.initial_spells + [0xFF])[:24]

    def encode_learned(self):
        keys = sorted(self.learned_spells)
        byte_list = []
        for k in keys:
            if type(self.learned_spells[k]) in (list, tuple):
                for s in self.learned_spells[k]:
                    byte_list.append(k)
                    byte_list.append(s)
            else:
                byte_list.append(k)
                byte_list.append(self.learned_spells[k])
        byte_list.append(0xFF)
        return byte_list

def decode(initial_byte_list, learned_byte_list):
    if initial_byte_list[-1] == 0xFF:
        initial_byte_list = initial_byte_list[:-1]
    if learned_byte_list[-1] == 0xFF:
        learned_byte_list = learned_byte_list[:-1]

    ss = SpellSet()
    ss.initial_spells = list(initial_byte_list)
    ss.learned_spells = {}
    for i in range(0, len(learned_byte_list), 2):
        lv, s = learned_byte_list[i:i+2]
        if lv in ss.learned_spells:
            if type(ss.learned_spells) in (list, tuple):
                ss.learned_spells[lv].append(s)
            else:
                ss.learned_spells[lv] = [ss.learned_spells[lv], s]
        else:
            ss.learned_spells[lv] = s
    return ss
