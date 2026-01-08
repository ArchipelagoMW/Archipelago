from ..data import enemy_script_commands as ai_instr

class EnemyScriptDialogs:
    def __init__(self, args, enemy_scripts):
        self.args = args
        self.enemy_scripts = enemy_scripts

    def cleanup_mod(self):
        self.vargas_dialog_mod()
        self.kefka_narshe_dialog_mod()
        self.ifrit_shiva_dialog_mod()
        self.atmaweapon_dialog_mod()
        self.nerapa_dialog_mod()
        self.ultros_lete_river_dialog_mod()
        self.ultros_opera_dialog_mod()
        self.ultros_esper_mountain_dialog_mod()
        self.ultros_chupon_dialog_mod()
        self.srbehemoth_dialog_mod()
        self.chadarnook_dialog_mod()
        self.atma_dialog_mod()

    def _remove_dialog(self, script, dialog_id, count = 1):
        dialog_instr = ai_instr.Message(dialog_id)
        script.remove(dialog_instr, count)

    def _remove_dialogs(self, script, dialog_ids):
        for dialog_id in dialog_ids:
            self._remove_dialog(script, dialog_id)

    def vargas_dialog_mod(self):
        vargas_script = self.enemy_scripts.get_script("Vargas")

        dialog_ids = [
            0x0012, # phew... i tire of this
            0x0043, # come on! there's no going back
            0x000a, # come on. what's the matter
            0x0042, # enough!! off with ya now
        ]

        self._remove_dialogs(vargas_script, dialog_ids)

    def kefka_narshe_dialog_mod(self):
        kefka_narshe_id = 330
        kefka_narshe_script = self.enemy_scripts.scripts[kefka_narshe_id]

        self._remove_dialog(kefka_narshe_script, 0x0015) # don't think you've won

    def ifrit_shiva_dialog_mod(self):
        ifrit_script = self.enemy_scripts.get_script("Ifrit")
        shiva_script = self.enemy_scripts.get_script("Shiva")

        # dialogs are the same in ifrit/shiva scripts but the order of them is different
        dialog_ids = [
            0x001b, # who're you
            0x001c, # i sensed a kindred spirit
            0x001d, # wait we're espers
        ]

        self._remove_dialogs(ifrit_script, dialog_ids)
        self._remove_dialogs(shiva_script, dialog_ids)

    def atmaweapon_dialog_mod(self):
        atmaweapon_id = 279
        atmaweapon_script = self.enemy_scripts.scripts[atmaweapon_id]

        self._remove_dialog(atmaweapon_script, 0x0085) # my name is atma...

    def nerapa_dialog_mod(self):
        nerapa_script = self.enemy_scripts.get_script("Nerapa")

        self._remove_dialog(nerapa_script, 0x0066) # mwa ha ha... ... you can't run

    def ultros_lete_river_dialog_mod(self):
        ultros_id = 300
        ultros_script = self.enemy_scripts.scripts[ultros_id]

        dialog_ids = [
            0x000c, # game over! don't tease the octopus kids
            0x000d, # delicious morsel! let me get my bib
            0x000e, # muscle-heads? hate em
            0x004d, # y... you frighten me
            0x0009, # th... that's all friends
            0x000b, # seafood soup
        ]

        self._remove_dialogs(ultros_script, dialog_ids)

    def ultros_opera_dialog_mod(self):
        ultros_id = 301
        ultros_script = self.enemy_scripts.scripts[ultros_id]

        dialog_ids = [
            0x0013, # long time no see
            0x0062, # imp! pal! buddy!
            0x0004, # what an unlucky day
            0x001e, # i ain't ready to go yet
            0x001a, # how sweet it is!
            0x0018, # have ya read it?
            0x0017, # havin fun?
        ]

        self._remove_dialogs(ultros_script, dialog_ids)

        # the last two dialogs occur twice in the script, delete both
        self._remove_dialog(ultros_script, 0x0019, count = 2) # i ain't no garden-variety octopus
        self._remove_dialog(ultros_script, 0x0016, count = 2) # here! over here!

    def ultros_esper_mountain_dialog_mod(self):
        ultros_id = 302
        ultros_script = self.enemy_scripts.scripts[ultros_id]

        dialog_ids = [
            0x004f, # i was just thinking about you
            0x004e, # hope i'm not making a nuiscance of myself
            0x0050, # how can this be? i-i'm nothing more than a stupid octopus
        ]

        self._remove_dialogs(ultros_script, dialog_ids)

    def ultros_chupon_dialog_mod(self):
        ultros_id = 360 # chupon is 303
        ultros_script = self.enemy_scripts.scripts[ultros_id]

        dialog_ids = [
            0x0051, # no, really... this is our last battle
            0x0056, # i was drowsing the other day
            0x0052, # better not irritate him
            0x0054, # mr. chupon's taciturn
            0x0053, # i lose again
            0x0057, # fungahhh!
        ]

        self._remove_dialogs(ultros_script, dialog_ids)

    def srbehemoth_dialog_mod(self):
        srbehemoth_id = 281 # first battle
        srbehemoth_script = self.enemy_scripts.scripts[srbehemoth_id]

        dialog_ids = [
            0x007c, # enemy's coming from behind
            0x007d, # another monster appeared
        ]

        self._remove_dialogs(srbehemoth_script, dialog_ids)

    def chadarnook_dialog_mod(self):
        chadarnook_painting_script = self.enemy_scripts.get_script("Chadarnook")

        self._remove_dialog(chadarnook_painting_script, 0x005f) # the girl in the picture is mine

        chadarnook_demon_id = 328
        chadarnook_demon_script = self.enemy_scripts.scripts[chadarnook_demon_id]

        self._remove_dialog(chadarnook_demon_script, 0x007a) # i... i'm... this can't be

    def atma_dialog_mod(self):
        atma_id = 381
        atma_script = self.enemy_scripts.scripts[atma_id]

        self._remove_dialog(atma_script, 0x008b) # i'm atma...
