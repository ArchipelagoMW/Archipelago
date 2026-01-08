from ..event.event import *
from ..data.npc import NPC
from ..music.song_utils import get_character_theme

class DebugRoom(Event):
    # Using the 3 Scenarios room as our debug map
    DEBUG_ROOM = 0x9

    def name(self):
        return "Debug Room"
    
    def init_event_bits(self, space):
        pass

    def remove_npcs_mod(self):
        # Remove all existing NPCs
        while(self.maps.get_npc_count(self.DEBUG_ROOM) > 0):
            self.maps.remove_npc(self.DEBUG_ROOM, 0)

    def _add_recruit_npc(self, character, x, y, direction):
        # Add an NPC to recruit each character
        src = [
            field.RecruitCharacter(character),
            field.PlaySoundEffect(150),
            field.StartSong(get_character_theme(character)),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "Recruit NPC")

        recruit_npc = NPC()
        recruit_npc.x = x
        recruit_npc.y = y
        recruit_npc.direction = direction
        recruit_npc.sprite = self.characters.get_sprite(character)
        recruit_npc.palette = self.characters.get_palette(character)
        recruit_npc.set_event_address(space.start_address)
        self.maps.append_npc(self.DEBUG_ROOM, recruit_npc)

    def add_recruit_npcs_mod(self):
        self._add_recruit_npc(self.characters.TERRA,  1, 8, direction.DOWN)
        self._add_recruit_npc(self.characters.LOCKE,  2, 8, direction.DOWN)
        self._add_recruit_npc(self.characters.CYAN,   3, 8, direction.DOWN)
        self._add_recruit_npc(self.characters.SHADOW, 4, 8, direction.DOWN)
        self._add_recruit_npc(self.characters.EDGAR,  5, 8, direction.DOWN)
        self._add_recruit_npc(self.characters.SABIN,  6, 8, direction.DOWN)
        self._add_recruit_npc(self.characters.CELES,  7, 8, direction.DOWN)
        self._add_recruit_npc(self.characters.STRAGO, 8, 8, direction.DOWN)
        self._add_recruit_npc(self.characters.RELM,   9, 8, direction.DOWN)
        self._add_recruit_npc(self.characters.SETZER, 10, 8, direction.DOWN)
        self._add_recruit_npc(self.characters.MOG,    11, 8, direction.DOWN)
        self._add_recruit_npc(self.characters.GAU,    12, 8, direction.DOWN)
        self._add_recruit_npc(self.characters.GOGO,   13, 8, direction.DOWN)
        self._add_recruit_npc(self.characters.UMARO,  14, 8, direction.DOWN)

    def _add_teleport_npc(self, source_map, source_x, source_y, direction, dest_map, dest_x, dest_y):
        # Test code to add a Marshal battle NPC to Blackjack
        from ..data.bosses import name_pack
        src = [
            field.LoadMap(dest_map, direction, True, dest_x, dest_y, fade_in = True),
            field.Return(),
        ]
        space = Write(Bank.CC, src, "Teleport NPC")

        teleport_npc = NPC()
        teleport_npc.x = source_x
        teleport_npc.y = source_y
        teleport_npc.sprite = 22
        teleport_npc.palette = 3
        teleport_npc.direction = direction
        teleport_npc.set_event_address(space.start_address)
        self.maps.append_npc(source_map, teleport_npc)

    def add_teleport_npcs_mod(self):
        # get to and from the debug room via WoB Airship
        BLACKJACK_EXTERIOR_MAP = 0x06
        self._add_teleport_npc(BLACKJACK_EXTERIOR_MAP, 15, 4, direction.DOWN, self.DEBUG_ROOM, 8, 9)
        self._add_teleport_npc(self.DEBUG_ROOM, 8, 10, direction.UP, BLACKJACK_EXTERIOR_MAP, 15, 5)

    def mod(self):
        if self.args.debug:
            self.remove_npcs_mod()
            self.add_recruit_npcs_mod()
            self.add_teleport_npcs_mod()
