from ..data.enemy_script import EnemyScript
from ..data.enemy_script_custom_commands import EnemyScriptCommands
from ..data.enemy_script_dialogs import EnemyScriptDialogs
from ..data.enemy_script_abilities import EnemyScriptAbilities
from ..data.structures import DataMap

from ..data import enemy_script_commands as ai_instr

class EnemyScripts():
    SCRIPT_PTRS_START = 0xf8400
    SCRIPT_PTRS_END   = 0xf86ff
    SCRIPTS_START = 0xf8700
    SCRIPTS_END   = 0xfc04f

    def __init__(self, rom, args, enemies):
        self.rom = rom
        self.args = args
        self.enemies = enemies

        self.script_data = DataMap(self.rom, self.SCRIPT_PTRS_START, self.SCRIPT_PTRS_END,
                                   self.rom.SHORT_PTR_SIZE, self.SCRIPTS_START,
                                   self.SCRIPTS_START, self.SCRIPTS_END)

        self.scripts = []
        for script_index in range(len(self.script_data)):
            script = EnemyScript(script_index, self.script_data[script_index])
            self.scripts.append(script)

        self.enemy_script_custom_commands = EnemyScriptCommands(self.rom, self.args, self, self.enemies)
        self.enemy_script_dialogs = EnemyScriptDialogs(self.args, self)
        self.enemy_script_abilities = EnemyScriptAbilities(self.args, self, self.enemies)

    def __len__(self):
        return len(self.scripts)

    def get_script(self, enemy_name):
        enemy_id = self.enemies.get_enemy(enemy_name)
        return self.scripts[enemy_id]

    def cleanup_mod(self):
        terra_kefka_burn_soldiers_script = self.scripts[366]
        terra_kefka_burn_soldiers_script.delete()

        # this script is used for sealed gate bridge battles and kefka vs gestahl fc battle
        sealed_gate_and_floating_continent_script = self.scripts[379]
        sealed_gate_and_floating_continent_script.delete()

    def mag_roader_wild_cat_fix(self):
        # fix small brown mag roader missing end script byte
        mag_roader_id = 243
        mag_roader_script = self.scripts[mag_roader_id]
        mag_roader_script.append(ai_instr.EndScript())

    def rizopas_timer_mod(self):
        # randomize time until rizopas appears to prevent doing nothing until 60 seconds passes
        piranha_script = self.get_script("Piranha")

        import random
        random_time = random.randint(5, 55) # average of 30

        original_time = 60
        if random_time == original_time:
            return

        rizopas_timer_check = ai_instr.If(0x16, 0x3c, 0x00) # if timer is larger than 0x3c (60)
        rizopas_timer_check_new = ai_instr.If(0x16, random_time, 0x00) # if timer is larger than random_time

        piranha_script.replace(rizopas_timer_check, rizopas_timer_check_new)

    def ifrit_shiva_death_mod(self):
        ifrit_script = self.get_script("Ifrit")
        shiva_script = self.get_script("Shiva")

        # there are 2 versions of ifrit/shiva, do not show the event one for whichever was killed or no exp received
        show_both = ai_instr.ChangeEnemies(0x00, 0x00, 0x03)    # show shiva/ifrit, restore their hp
        show_ifrit = ai_instr.ChangeEnemies(0x00, 0x00, 0x01)   # show ifrit, restore hp
        show_shiva = ai_instr.ChangeEnemies(0x00, 0x00, 0x02)   # show shiva, restore hp

        ifrit_script.replace(show_both, show_shiva)
        shiva_script.replace(show_both, show_ifrit)

        end_battle = ai_instr.Misc(0x02, 0x00)                  # end battle
        boss_death = ai_instr.ChangeEnemies(0x0c, 0x01, 0xff)   # kill all enemies with boss death animation

        ifrit_script.replace(end_battle, boss_death)
        shiva_script.replace(end_battle, boss_death)

    def doom_gaze_no_escape_mod(self):
        from ..data.spell_names import name_id

        doom_gaze_script = self.get_script("Doom Gaze")
        escape_turn = [
            ai_instr.EndTurn(),         # wait until next turn
            ai_instr.SetTarget(0x36),   # set target: self
            ai_instr.RandomAttack(name_id["Nothing"], name_id["Escape"], name_id["Escape"]),
        ]
        doom_gaze_script.remove(escape_turn)

    def doom_gaze_event_bit_mod(self):
        doom_gaze_script = self.get_script("Doom Gaze")

        # instructions which set doom gaze defeated event bit
        set_defeated_bit = ai_instr.Bits(0x01, 0x0d, 0x00) # set bit 0x00 in byte 13 (1dd2, bit 0)
        doom_gaze_script.remove(set_defeated_bit)

    def wrexsoul_no_zinger_mod(self):
        from ..data.spell_names import name_id

        wrexsoul_script = self.get_script("Wrexsoul")

        # first turn, executes dialog and zinger
        dialog_zinger = [
            ai_instr.If(0x15, 0x00, 0x01),      # if byte 0 bit 0x01 clear
            ai_instr.Bits(0x01, 0x00, 0x01),    # set bit 0x01 in byte 0
            ai_instr.Event(0x1f),               # trigger event 0x1f (dialog)
            ai_instr.Spell(name_id["Zinger"]),
            ai_instr.EndIf(),
        ]
        wrexsoul_script.remove(dialog_zinger)

        # zinger's after the first
        zinger_turn = [
            ai_instr.EndTurn(),                 # wait until next turn
            ai_instr.SetTarget(0x44),           # set target: random ally
            ai_instr.RandomAttack(name_id["Nothing"], name_id["Zinger"], name_id["Zinger"])
        ]
        wrexsoul_script.remove(zinger_turn)

    def srbehemoth_no_back_attack_mod(self):
        srbehemoth_id = 281 # first battle
        srbehemoth_script = self.scripts[srbehemoth_id]

        # move allies from right side to left side for second srbehemoth
        party_move = ai_instr.Animate(0x06, 0x00, 0x00)
        srbehemoth_script.remove(party_move)

    def chadarnook_flashing_mod(self):
        chadarnook_painting_script = self.get_script("Chadarnook")

        switch_animation = 0x0d # enemies flash in and out rapidly

        switch_to_demon = [
            ai_instr.ChangeEnemies(0x0e, 0x02, 0x02),   # lightning flash, add enemy 2 at current hp
            ai_instr.ChangeEnemies(0x0e, 0x01, 0x01),   # lightning flash, remove enemy 1
        ]
        switch_to_demon_new = [
            ai_instr.ChangeEnemies(switch_animation, 0x02, 0x02), # change animation
            ai_instr.ChangeEnemies(switch_animation, 0x01, 0x01), # change animation
        ]
        chadarnook_painting_script.replace(switch_to_demon, switch_to_demon_new, count = 2)

        chadarnook_demon_id = 328
        chadarnook_demon_script = self.scripts[chadarnook_demon_id]

        switch_to_painting = [
            ai_instr.ChangeEnemies(0x0e, 0x02, 0x01),   # lightning flash, add enemy 1 at current hp
            ai_instr.ChangeEnemies(0x0e, 0x01, 0x02),   # lightning flash, remove enemy 2
        ]
        switch_to_painting_new = [
            ai_instr.ChangeEnemies(switch_animation, 0x02, 0x01), # change animation
            ai_instr.ChangeEnemies(switch_animation, 0x01, 0x02), # change animation
        ]
        chadarnook_demon_script.replace(switch_to_painting, switch_to_painting_new, count = 2)

    def chadarnook_more_demon_mod(self):
        chadarnook_demon_id = 328
        chadarnook_demon_script = self.scripts[chadarnook_demon_id]

        # NOTE: if the painting returns and only takes one action, the switch was triggered by number of attacks
        #       if the painting returns and takes 2 or 3 actions, the switch was triggered by the timer

        # timer until demon turns back to painting (default is 40)
        time_until_switch = 48
        timer_check = ai_instr.If(0x0b, 0x28, 0x00)
        timer_check_new = ai_instr.If(0x0b, time_until_switch, 0x00)

        # number of times demon attacked before turning back to painting (default is 5 times)
        # NOTE, the threshold is (value + 1), e,g, if set to 4 demon will switch after the 5th attack
        attacks_until_switch = 6 # switch after being targeted 6 times
        attacks_check = ai_instr.If(0x0d, 0x00, 0x04)
        attacks_check_new = ai_instr.If(0x0d, 0x00, attacks_until_switch - 1)

        # when chadarnook demon timer runs out the number of times attacked counter is not reset
        # also, when the number of attacks threshold is reached, the timer is not reset to zero
        # this can cause demon to appear and immediately switch back to the painting
        # change it so both the timer and attack counter are reset before switching
        reset_timer = ai_instr.Misc(0x00, 0x00)                 # reset timer for current enemy
        timer_switch_flag = ai_instr.Arithmetic(0x03, 0x01)     # set a flag telling painting enemy that time ran out
        reset_attacked_count = ai_instr.Arithmetic(0x00, 0x00)  # reset attack counter (var 0000)
        attacked_switch_flag = ai_instr.Arithmetic(0x03, 0x00)  # clear flag telling painting enemy that attack threshold reached (not timer)

        time_up_switch = [
            timer_check,
            reset_timer,
            timer_switch_flag,
        ]
        time_up_switch_new = [
            timer_check_new,
            reset_attacked_count,
            reset_timer,
            timer_switch_flag,
        ]
        chadarnook_demon_script.replace(time_up_switch, time_up_switch_new)

        attacked_enough_switch = [
            attacks_check,
            reset_attacked_count,
            attacked_switch_flag,
        ]
        attacked_enough_switch_new = [
            attacks_check_new,
            reset_attacked_count,
            reset_timer,
            attacked_switch_flag,
        ]
        chadarnook_demon_script.replace(attacked_enough_switch, attacked_enough_switch_new)

    def magimaster_no_ultima_mod(self):
        from ..data.spell_names import name_id

        magimaster_script = self.get_script("MagiMaster")

        # removing the if/end if causes him to use wallchange before dying so leave them in
        ultima = [
            ai_instr.SetTarget(0x47), # set target: default
            ai_instr.Spell(name_id["Ultima"]),
        ]
        magimaster_script.remove(ultima)

    def hidon_no_chokesmoke(self):
        from ..data.spell_names import name_id

        hidon_script = self.get_script("Hidon")

        chokesmoke = []
        for character in range(4):
            chokesmoke.extend([
                ai_instr.If(8, 72 + character, 7),
                ai_instr.If(9, 72 + character, 1),
                ai_instr.SetTarget(72 + character),
                ai_instr.Spell(name_id["ChokeSmoke"]),
                ai_instr.EndIf(),
            ])
        hidon_script.remove(chokesmoke)

    def magic_urn_no_life(self):
        from ..data.spell_names import name_id

        magic_urn_script = self.get_script("Magic Urn")

        life = [
            ai_instr.If(8, 67, 7),
            ai_instr.RandomAttack(name_id["Life"], name_id["Life"], name_id["Life 2"]),
            ai_instr.SetTarget(54),
            ai_instr.RandomAttack(name_id["Escape"], name_id["Nothing"], name_id["Nothing"]),
            ai_instr.EndIf(),
        ]
        magic_urn_script.remove(life)

    def chupon_sneeze_all(self):
        # Make Chupon 64 (Coliseum) target all allies with initial sneeze
        chupon_id = 64
        chupon_script = self.scripts[chupon_id]
        chupon_script.insert(0, ai_instr.SetTarget(0x43)) # Target: Allies

    def mod(self):
        # first free up some space for other mods
        self.cleanup_mod()

        # remove dialogs
        self.enemy_script_dialogs.cleanup_mod()

        self.enemy_script_custom_commands.mod()

        self.mag_roader_wild_cat_fix()
        self.rizopas_timer_mod()

        if self.args.boss_experience:
            self.ifrit_shiva_death_mod()

        if self.args.doom_gaze_no_escape:
            self.doom_gaze_no_escape_mod()

            if self.args.boss_battles_shuffle or self.args.boss_battles_random:
                self.doom_gaze_event_bit_mod()

        if self.args.wrexsoul_no_zinger:
            self.wrexsoul_no_zinger_mod()

        if self.args.boss_battles_shuffle or self.args.boss_battles_random:
            # the animation chadarnook uses to switch between demon and painting
            # breaks with other battle backgrounds, they turn weird colors and look very glitchy
            self.chadarnook_flashing_mod()

            self.srbehemoth_no_back_attack_mod()

        if self.args.chadarnook_more_demon:
            self.chadarnook_more_demon_mod()

        if self.args.magimaster_no_ultima:
            self.magimaster_no_ultima_mod()

        if self.args.permadeath:
            self.hidon_no_chokesmoke()
            self.magic_urn_no_life()

        if self.args.random_encounters_chupon:
            self.chupon_sneeze_all()

        if self.args.ability_scaling:
            self.enemy_script_abilities.scale_abilities_mod()

    def write(self):
        self.script_data.assign([script.data() for script in self.scripts])
        self.script_data.write()
