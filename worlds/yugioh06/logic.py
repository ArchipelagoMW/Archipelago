from worlds.AutoWorld import LogicMixin


class YuGiOh06Logic(LogicMixin):
    def yugioh06_difficulty(self, player, amount: int):
        return self.has_group("Core Booster", player, amount)

    def yugioh06_has_ojama_delta_hurricane(self, player):
        return self.has_all(["Ojama Delta Hurricane", "Ojama Green", "Ojama Yellow", "Ojama Black"], player)

    def yugioh06_has_huge_revolution(self, player):
        return self.has_all(["Huge Revolution", "Oppressed People", "United Resistance",
                             "People Running About"], player)

    def yugioh06_has_perfectly_ultimate_great_moth(self, player):
        return self.has_all(["Perfectly Ultimate Great Moth", "Petit Moth", "Cocoon of Evolution"], player)

    def yugioh06_has_valkyrion_the_magna_warrior(self, player):
        return self.has_all(["Valkyrion the Magna Warrior", "Alpha the Magnet Warrior",
                            "Beta the Magnet Warrior", "Gamma the Magnet Warrior"], player)

    def yugioh06_has_dark_sage(self, player):
        return self.has_all(["Dark Sage", "Dark Magician", "Time Wizard"], player)

    def yugioh06_has_destiny_board(self, player):
        return self.has_all(["Destiny Board", "Spirit Message 'I'", "Spirit Message 'N'",
                            "Spirit Message 'A'", "Spirit Message 'L'"], player)

    def yugioh06_has_all_xyz_dragon_cannon_fusions(self, player):
        return self.has_all(["X-Head Cannon", "Y-Dragon Head", "Z-Metal Tank",
                            "XY-Dragon Cannon", "XZ-Tank Cannon", "YZ-Tank Dragon", "XYZ-Dragon Cannon"], player)#

    def yugioh06_has_vwxyz_dragon_catapult_cannon(self, player):
        return self.has_all(["X-Head Cannon", "Y-Dragon Head", "Z-Metal Tank", "XYZ-Dragon Cannon",
                             "V-Tiger Jet", "W-Wing Catapult", "VW-Tiger Catapult", "VWXYZ-Dragon Catapult Cannon"],
                            player)

    def yugioh06_has_gate_guardian(self, player):
        return self.has_all(["Gate Guardian", "Kazejin", "Suijin", "Sanga of the Thunder"], player)

    def yugioh06_has_dark_scorpion_combination(self, player):
        return self.has_all(["Dark Scorpion Combination", "Don Zaloog", "Dark Scorpion - Chick the Yellow",
                             "Dark Scorpion - Meanae the Thorn", "Dark Scorpion - Cliff the Trap Remover"], player)

    def yugioh06_can_exodia_win(self, player):
        # TODO: more ways to win with Exodia
        return self.has_all(["Exodia", "Heart of the Underdog"], player)

    def yugioh06_can_last_turn_win(self, player):
        # TODO: add more ways to set it up
        return self.has_all(["Last Turn", "Wall of Revealing Light", "Jowgen the Spiritualist"], player)

    def yugioh06_can_yata_lock(self, player):
        return self.has_all(["Yata-Garasu", "Chaos Emperor Dragon - Envoy of the End", "Sangan"], player)\
                and self.has_any(["No Banlist", "Banlist September 2003"], player)

    def yugioh06_can_get_konami_bonus(self, player):
        return (self.has_all(["Messenger of Peace", "Castle of Dark Illusions", "Mystik Wok"], player) or
                self.has_all(["Mystik Wok", "Barox", "Cyber-Stein", "Poison of the Old Man"], player)) and\
                self.yugioh06_difficulty(player, 8)

