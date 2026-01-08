from ...data.dialogs.dialog import Dialog
from ...data.structures import DataList
from ...memory.space import Space
from ...data.fonts import widths
from ...data import text
from ... import data as data

class Dialogs():
    DIALOG_PTRS_START = 0xce602
    DIALOG_PTRS_END = 0xcffff
    DIALOGS_START = 0xd0000
    DIALOGS_END = 0xef0ff

    # the address of the first ptr index which is relative to 0xce0000
    # dialog ptrs < FIRST_CE_PTR_INDEX are relative to 0xcd0000
    # dialog ptrs >= FIRST_CE_PTR_INDEX are relative to 0xce0000
    FIRST_CE_PTR_INDEX_ADDR = 0xce600

    BATTLE_MESSAGE_PTRS_START = 0x11f7a0
    BATTLE_MESSAGE_PTRS_END = 0x11f99f
    BATTLE_MESSAGES_OFFSET = 0x110000
    BATTLE_MESSAGES_START = 0x11f000    # NOTE: battle messages are moved to a different location
    BATTLE_MESSAGES_END = 0x11f79f

    SINGLE_LINE_BATTLE_DIALOG_PTRS_START = 0xfdfe0
    SINGLE_LINE_BATTLE_DIALOG_PTRS_END = 0xfe1df
    SINGLE_LINE_BATTLE_DIALOGS_OFFSET = 0xf0000
    SINGLE_LINE_BATTLE_DIALOGS_START = 0xfe1e0
    SINGLE_LINE_BATTLE_DIALOGS_END = 0xff44f

    MULTI_LINE_BATTLE_DIALOG_PTRS_START = 0x10d000
    MULTI_LINE_BATTLE_DIALOG_PTRS_END = 0x10d1ff
    MULTI_LINE_BATTLE_DIALOGS_OFFSET = 0x100000
    MULTI_LINE_BATTLE_DIALOGS_START = 0x10d200
    MULTI_LINE_BATTLE_DIALOGS_END = 0x10fcff

    from ...constants.objectives import MAX_OBJECTIVES
    OBJECTIVES = list(range(3084, 3084 + MAX_OBJECTIVES))
    BATTLE_OBJECTIVES = list(range(70, 70 + MAX_OBJECTIVES))

    def __init__(self):
        self.read()
        self.free()
        self.mod()

    def read(self):
        self.read_dialogs()
        self.read_battle_messages()
        self.read_single_line_battle_dialogs()
        self.read_multi_line_battle_dialogs()

    def read_dialogs(self):
        self.dialog_data = DataList(Space.rom, self.DIALOG_PTRS_START, self.DIALOG_PTRS_END,
                                    Space.rom.SHORT_PTR_SIZE, self.DIALOGS_START,
                                    self.DIALOGS_START, self.DIALOGS_END)

        self.dialogs = []
        for dialog_index, dialog_data in enumerate(self.dialog_data):
            dialog = Dialog(dialog_index, data.text.TEXT1, dialog_data)
            self.dialogs.append(dialog)

        # the last used dialog ends with garbage data because the last pointer pointed to the end of
        # the available dialog memory instead of the end of the actual displayed text
        # assign only the displayed text to free that garbage memory
        self.set_text(3083, ("<line><RELM>: How about a nice portrait for you, hmm?!"
                             "<wait 120 frames><wait 1 frame><end>"))

    def read_battle_messages(self):
        self.battle_message_data = DataList(Space.rom, self.BATTLE_MESSAGE_PTRS_START, self.BATTLE_MESSAGE_PTRS_END,
                                            Space.rom.SHORT_PTR_SIZE, self.BATTLE_MESSAGES_OFFSET,
                                            self.BATTLE_MESSAGES_START, self.BATTLE_MESSAGES_END)

        self.battle_messages = []
        for message_index, message_data in enumerate(self.battle_message_data):
            dialog = Dialog(message_index, data.text.TEXT3, message_data)
            self.battle_messages.append(dialog)

        # free garbage memory at end of messages space
        self.set_battle_message_text(255, "<end>")

    def read_single_line_battle_dialogs(self):
        self.single_line_battle_dialog_data = DataList(Space.rom,
                                                       self.SINGLE_LINE_BATTLE_DIALOG_PTRS_START,
                                                       self.SINGLE_LINE_BATTLE_DIALOG_PTRS_END,
                                                       Space.rom.SHORT_PTR_SIZE,
                                                       self.SINGLE_LINE_BATTLE_DIALOGS_OFFSET,
                                                       self.SINGLE_LINE_BATTLE_DIALOGS_START,
                                                       self.SINGLE_LINE_BATTLE_DIALOGS_END)

        self.single_line_battle_dialogs = []
        for dialog_index, dialog_data in enumerate(self.single_line_battle_dialog_data):
            dialog = Dialog(dialog_index, data.text.TEXT3, dialog_data)
            self.single_line_battle_dialogs.append(dialog)

    def read_multi_line_battle_dialogs(self):
        self.multi_line_battle_dialog_data = DataList(Space.rom,
                                                      self.MULTI_LINE_BATTLE_DIALOG_PTRS_START,
                                                      self.MULTI_LINE_BATTLE_DIALOG_PTRS_END,
                                                      Space.rom.SHORT_PTR_SIZE,
                                                      self.MULTI_LINE_BATTLE_DIALOGS_OFFSET,
                                                      self.MULTI_LINE_BATTLE_DIALOGS_START,
                                                      self.MULTI_LINE_BATTLE_DIALOGS_END)

        self.multi_line_battle_dialogs = []
        for dialog_index, dialog_data in enumerate(self.multi_line_battle_dialog_data):
            dialog = Dialog(dialog_index, data.text.TEXT3, dialog_data)
            self.multi_line_battle_dialogs.append(dialog)

    def free(self):
        from ...data.dialogs import free as free

        self.free_multi_line_battle_dialogs = []
        for dialog_id in free.multi_line_battle_dialogs:
            self.multi_line_battle_dialogs[dialog_id].text = ""
            self.free_multi_line_battle_dialogs.append(dialog_id)

    def set_text(self, id, text):
        self.dialogs[id].text = text

    def set_battle_message_text(self, id, text):
        self.battle_messages[id].text = text

    def set_single_line_battle_text(self, id, text):
        self.single_line_battle_dialogs[id].text = text

    def set_multi_line_battle_text(self, id, text):
        self.multi_line_battle_dialogs[id].text = text

    def allocate_multi_line_battle(self, text):
        dialog_id = self.free_multi_line_battle_dialogs.pop()
        self.set_multi_line_battle_text(dialog_id, text)
        return dialog_id

    def get_multi_line_battle_objective(self, objective_index):
        return self.multi_line_battle_objectives[objective_index]

    def get_centered(self, string):
        MAX_WIDTH = 219
        space_width = 5

        string_width = widths.width(string)
        center_start = (MAX_WIDTH - string_width) // 2 + 1
        left_spaces = center_start // space_width
        return (" " * left_spaces) + string

    def move_battle_messages(self):
        from ...memory.space import START_ADDRESS_SNES, Bank, Reserve, Allocate, Free
        space = Allocate(Bank.F0, 4000, "battle messages new location")

        # update pointers to messages (leave pointers in d1 bank)
        pointer_shift = (space.start_address & 0xffff) - self.battle_message_data.pointers[0]
        for pointer_index in range(len(self.battle_message_data.pointers)):
            self.battle_message_data.pointers[pointer_index] += pointer_shift
        self.battle_message_data.pointer_offset = space.start_address

        self.battle_message_data.free_space = len(space) - self.battle_message_data.size()
        self.battle_message_data.start_address = space.start_address
        self.battle_message_data.end_address = space.end_address

        # update bank to load battle messages from
        space = Reserve(0x198ff, 0x198ff, "battle messages bank")
        space.write(START_ADDRESS_SNES + self.battle_message_data.pointer_offset >> 16)

        # free previous message data space
        Free(0x11f000, 0x11f79f)

    def objectives_mod(self):
        from ... import objectives as objectives
        self.multi_line_battle_objectives = []
        for index, objective in enumerate(objectives):
            line2 = self.get_centered(str(objective.result))
            line3 = self.get_centered("Objective Complete!")
            self.set_text(self.OBJECTIVES[index], "<line>" + line2 + "<line>" + line3 + "<end>")

            self.set_battle_message_text(self.BATTLE_OBJECTIVES[index],
                                         str(objective.result) + " Complete<wait for key><end>")

            line1 = self.get_centered(str(objective.result))
            line2 = self.get_centered("Objective Complete!")
            mlid = self.allocate_multi_line_battle(line1 + "<line>" + line2 + "<wait for key><end>")
            self.multi_line_battle_objectives.append(mlid)

    def mod(self):
        self.move_battle_messages()
        self.objectives_mod()
        
        from ... import args as args
        if args.npc_dialog_tips:

            # clear out vanilla dialog to make room for tips
            for lines in range(0,49): # Narshe intro, Terra's flashback, Locke's intro
                self.set_text(lines,"")
            for lines in range(113,145): # Figaro Castle 1st Kefka sequence, Locke and Terra dialog
                self.set_text(lines,"")
            for lines in range(248,267): # Vargas and Sabin intro
                self.set_text(lines,"")
            for lines in range(370,407): # South Figaro Locke scenario
                self.set_text(lines,"")
            for lines in range(667,684): # Phantom Train
                self.set_text(lines,"")
            for lines in range(724,736): # Phantom Train end
                self.set_text(lines,"")
            for lines in range(783,803): # Crescent Mountain scene
                self.set_text(lines,"")
            for lines in range(837,874): # Narshe Battle
                self.set_text(lines,"")
            for lines in range(879,917): # After Narshe Battle
                self.set_text(lines,"")
            for lines in range(1073,1133): # Ramuh at Zozo
                self.set_text(lines,"")
            for lines in range(1372,1380): # Ifrit & Shiva
                self.set_text(lines,"")
            for lines in range(1387,1403): # Magitek Room Cid sequence
                self.set_text(lines,"")
            for lines in range(1410,1422): # After Magitek Factory
                self.set_text(lines,"")
            for lines in range(1635,1655): # Sealed Gate
                self.set_text(lines,"")
            for lines in range(1656,1675): # After Sealed Gate
                self.set_text(lines,"")
            for lines in range(1959,2003): # Thamasa Strago intro, Burning House intro
                self.set_text(lines,"")
            for lines in range(2005,2027): # Thamasa after Burning House
                self.set_text(lines,"")
            for lines in range(2136,2162): # Floating Continent statues scene
                self.set_text(lines,"")

            self.set_text(81, "The Figaro Throne reward exists in both worlds!<end>")
            self.set_text(82, "MasterPug doesn't grant any XP or MP. Too bad…<end>")
            self.set_text(83, "Blue Drgn uses Water magic. Use Imp gear to absorb it.<end>")
            self.set_text(85, "Open a hidden stairwell in the Ancient Castle by walking 5 steps south of the queen's throne and pressing “A”.<end>")
            self.set_text(87, "Use a combination of RunningShoes and Wall Ring to be completely safe from Tentacles.<end>")
            self.set_text(89, "Hitting an enemy with Air Anchor means it'll be dead after its next turn.<end>")
            self.set_text(90, "Drill and Chain Saw both ignore enemy defenses.<end>")
            self.set_text(91, "Drill and Chain Saw both ignore enemy defenses.<end>")
            self.set_text(92, "Chests in Figaro Castle are the same in both worlds…<end>")
            self.set_text(93, "But shops sell different items!<end>")
            self.set_text(98, "Hey! Let us outta here!<end>")
            self.set_text(100, "Hey! Let us outta here!<end>")
            self.set_text(101, "Hey! Let us outta here!<end>")
            self.set_text(102, "When given a dialogue option, hold up/down before the options appear to automatically select the top or bottom option. This is useful for Auction House or Ancient Castle.<end>")
            self.set_text(176, "An old clock.<end>")
            self.set_text(177, "An old clock.<end>")
            self.set_text(179, "Towns sell different things between worlds, even if they look the same.<end>")
            self.set_text(180, "South Figaro has more free chests than any other town! The mansion's basement is open right from the start.<end>")
            self.set_text(181, "If you enter Mt. Kolts from the south and exit from the north, the airship will follow you to the northern exit.<end>")
            self.set_text(182, "If you land a Pummel on Vargas, the fight will end immediately. No XP from him if you do that though!<end>")
            self.set_text(183, "There are 2 hidden paths in Mt. Kolts that lead to treasure chests.<end>")
            self.set_text(184, "Equip relics to gain a variety of abilities!<end>")
            self.set_text(185, "Most Blitz moves utilize a character's MagPwr instead of Vigor. The 2 Blitzes that use Vigor are Pummel and Suplex.<end>")
            self.set_text(198, "Thrown weapons ignore enemy defenses - doesn't matter what type of weapon either.<end>")
            self.set_text(199, "Equip/unequip weapons/shields in battle to gain utility from weapons like Drainer or Assassin, take off an elemental shield to break it, or equip a Cursed Shld mid-battle. You can even take your weapon off and then throw it!<end>")
            self.set_text(201, "Shadow's Interceptor helps block attacks and can counter with powerful magic damage.<end>")
            self.set_text(202, "After recruiting a character, set up your party for Zone Eater or Veldt to save an airship trip. You can also do this after certain checks like Phoenix Cave.<end>")
            self.set_text(203, "Thrown elemental weapons will hit elemental weaknesses.<page>For example, Blossom is Wind. Trident is Water.<end>")
            self.set_text(204, "If you're not sure you can survive a fight, running away with just one character will let you survive the battle.<end>")
            self.set_text(205, "Buy more consumables than you think you'll need! Better safe than sorry.<end>")
            self.set_text(206, "I'm blocking the eastern exit now, but in the World of Ruin I won't be here.<end>")
            self.set_text(207, "Hold A in the menus during battle to select commands/spells fast - best done with Memory Cursor.<end>")
            self.set_text(208, "Hold A in the overworld to buffer interactions with NPCs/chests/the environment.<end>")
            self.set_text(210, "If you Jump with a spear, it will do double damage instead of 50% more damage that a normal weapon would do.<end>")
            self.set_text(211, "Jumps land faster if characters are Hasted or have higher Speed.<end>")
            self.set_text(213, "Fixed encounter checks are good after free progression checks to catch up in levels before a boss fight.<end>")
            self.set_text(215, "There's always a nasty draft in this room. Check behind the bookshelf.<end>")
            self.set_text(216, "Depending on the seed, enemies will get stronger based on<line> 1. How many characters, Espers, dragons, and/or checks you've done<page>2. How high your party's levels are<line>3. How much time has passed in the game.<line>Check the flags if you're not sure!<end>")
            self.set_text(221, "Save before certain checks and reset if the reward is something you don't need. We call this a Save Scum.<end>")
            self.set_text(228, "When entering a map on a staircase, hold up or down, then once your character turns, you're able to walk the stairs faster. Saves time and looks cool.<end>")
            self.set_text(229, "Memorize each map to be able to buffer the direction you will need to walk ahead of time.<end>")
            self.set_text(230, "Enter South Figaro Cave from the south entrance to trigger the boss fight near the healing pool.<end>")
            self.set_text(297, "Morph will double the damage of spells and physical damage as long as it doesn't ignore defense.<end>")
            self.set_text(313, "Check this room for a hidden treasure passage!<end>")
            self.set_text(474, "Cherub Downs and Gaia Gear help with Dirt Drgn's Earth attacks.<end>")
            self.set_text(476, "Use Sleep to put Dirt Drgn to bed.<end>")
            self.set_text(599, "Welcome to Worlds Collide! NPCs throughout this world will now give you useful tips instead of vanilla dialog.<page>By the way, default settings allow every character to equip a Moogle Charm.<end>")
            self.set_text(600, "Some monsters will freeze your characters. Use Fire to restore them to back to normal.<end>")
            self.set_text(601, "Phantom Forest and South Figaro Cave have healing springs that work like this pot.<end>")
            self.set_text(602, "This is a Save Point.<page>You may use Sleeping Bags and Tents here. If you can, use Sleeping Bags to save time.<end>")
            self.set_text(603, "Check barrels, clocks, crates, and pots such as this one for hidden items.<end>")
            self.set_text(604, "Staying at an Inn will revive your party in full.<end>")
            self.set_text(605, "Ha!<line>Sometimes monsters lurk inside of treasure chests!<page>Memorize all locations of these kinds of chests! It will help in future runs!<end>")
            self.set_text(606, "Relics?<end>")
            self.set_text(607, "If the battle mode is set to “Wait”, opening a menu during battle/having the cursor up for some commands will pause ATB. We call this a “Wait trick” - use it to plan out actions in menus while letting animations play.<end>")
            self.set_text(608, "When shopping, you'll see some symbols next to your characters:<page>Triangles pointing up indicate increasing battle power.<page>Triangles pointing down indicate decreasing battle power.<page>“=” indicates no change in battle power.<page>“E” means the item is already equipped on that character.<page>A symbol under a character means that person is now in your party.<end>")
            self.set_text(609, "Select the “Wait” Battle Mode from the Config Menu to take all the time you need to select spells or items without being attacked. Easiest settings? Set Battle Speed to 6 and Message Speed to 1.<end>")
            self.set_text(610, "Run from some battles by pressing (and holding) both the L and R Buttons.<page>This can take time, but will be fast in a preemptive strike/side attack.<page>Stock up on Smoke Bombs/Warp Stones and use them to escape.<end>")
            self.set_text(611, "In fights, “X” cycles character turns in order. “Y” cycles to the last character that had their ATB filled.<end>")
            self.set_text(612, "When selecting a spell, press the L or R Button to select multiple targets.<page>Sometimes, this causes the damage to be lower than a single target attack, so be careful!<end>")
            self.set_text(613, "Press left or right in battle to choose 'Row' or 'Defense.' In Short command menus, hold L or R.<page>Defense cuts damage in half until the next turn.<end>")
            self.set_text(614, "Damage is more severe when caught in a pincer attack! Enemies that hit you from behind deal double damage.<end>")
            self.set_text(615, "If you turn the ATB meter off, you'll be able to see a character's max HP value in battle.<end>")
            self.set_text(616, "In the back row, damage and attack power are halved.<page>Change rows using the Main Menu: press left on the Control Pad, then press “A”.<page>Maximize character's Fight damage by placing them in the front row. Keep characters not using Fight in the back.<end><end>")
            self.set_text(619, "Use a curative spell or item on an undead creature for maximum damage.<page>This will not work on some bosses under specific flags.<end>")
            self.set_text(621, "3-way attack indicates a fire, ice and lightning attack.<page>If an enemy nullifies or absorbs ANY ONE of those elements, they will nullify/absorb all the damage.<page>This applies to attacks like Maduin and Tritoch summons.<end>")
            self.set_text(622, "Use Rflect on your party to change enemy scripts - try it against SrBehemoth or Red Dragon.<end>")
            self.set_text(623, "Runic turns many spells, including those used by other party members, into MP. Can be used repeatedly, and expires when the Runic activates or the user performs another action.<page>Morph increases Attack/Magic power. Duration increases after battles awarding Magic Points.<page>Once selected, Dance and Rage make the user uncontrollable until KO or the battle is over.<end>")
            self.set_text(625, "To use an Esper it must be equipped. Choose “Skills” from the menu, then select “Espers.”<page>During battle, select Magic, and press up on the Control Pad. Press the A Button to use the Esper.<page>An Esper can only be used once per battle if the Multi Summon flag is off.<page>Learning Magic<page>Learn new spells by equipping Espers. Switch Espers to learn different sets of spells.<page>The higher the “Learning Speed” the faster a spell is learned.<page>When equipped, some Espers will raise qualities (Strength, HP, MP etc.) to their maximum limits at the next “level up.”<end>")
            self.set_text(626, "When HP is critical, you go into “Near Fatal” status. During this condition, you have a 1 in 16 chance for a super strong desperation move when choosing “Fight”.<end>")
            self.set_text(627, "Want to learn more about Espers?<line><choice> Yes<line><choice> No<end>")
            self.set_text(628, "See the NPC at the very end of this hall by the last door.<end>")
            self.set_text(629, "Each SwdTech has its own unique name.<page>You'll gain more SwdTech skills by leveling up or completing objectives.<end>")
            self.set_text(630, "“Rflect” doesn't block spells that have been “Rflected” off others.<page>Enemy protected by Rflect?<line>Try bouncing an attack off a Rflect-protected individual in your party!<end>")
            self.set_text(744, "Io Rage uses Flare Star, which does damage based on the enemies' levels - it's solid if you're under-leveled.<page>Prussian and Luridan Rage use Land Slide - stronger than Flare!<end>")
            self.set_text(745, "Talk to a shopkeeper to get the next letter to appear when doing the Injured Lad quest.<end>")
            self.set_text(746, "Each item you send for the Injured Lad costs roughly 1 to 3000 GP.<end>")
            self.set_text(747, "The Veldt check can be done in both the World of Balance and World of Ruin.<page>This check is best done early if possible. Only Lobos roam the Veldt at the very start of a seed.<end>")
            self.set_text(748, "Summon Ragnarok to Morph Lobos on the Veldt for Dried Meat. Most beast-like enemies also Morph into Dried Meat.<end>")
            self.set_text(749, "The Veldt check reward will not appear on a back or pincer attack, nor will it appear after several battles against formations with many enemies. Ensure you have Dried Meat and less than 3 characters in the party when doing this check.<end>")
            self.set_text(750, "The Doom Drgn Rage freezes enemies. It works on bosses, but has a chance of failing.<page>The Nightshade Rage charms enemies, but sometimes is nerfed - check the flags!<end>")
            self.set_text(752, "Many Rage specials boost physical damage, like Stray Cat, Gold Bear, and Trooper. Try them with Sniper or Man Eater. Even Fixed Dice damage benefits from these kinds of boosts!<end>")
            self.set_text(753, "Heard about the Serpent Trench?<line><choice> Yes<line><choice> No<end>")
            self.set_text(754, "Jump into the Trench from Crescent Mountain.<end>")
            self.set_text(755, "Jump into the Trench from Crescent Mountain.<end>")
            self.set_text(756, "In the Serpent Trench, go right twice to get both chests.<end>")
            self.set_text(757, "The Injured Lad quest can be started in the house right behind me.<end>")
            self.set_text(758, "By default, Rage users will learn monster skills after defeating them in battle.<page>This eliminates the need to use Leap on the Veldt.<end>")
            self.set_text(759, "Dried Meat is guaranteed to be in at least 1 shop. It can randomly show up in chests too.<page>Don't forget the airship has a shop too!<end>")
            self.set_text(761, "The entrance to the Serpent Trench is south of here, in Crescent Mountain.<end>")
            self.set_text(805, "If you wish, you can fight the enemy soldier NPCs in the Doma Castle siege.<page>Your party will be fully healed after you defeat the boss there.<end>")
            self.set_text(806, "Hit the chest, don't kick it!<end>")
            self.set_text(807, "Items sold will be at most 1/2 their shop value, depending on the seed.<end>")
            self.set_text(809, "You can exit from this town from both the east and west.<end>")
            self.set_text(810, "South Figaro-bound ferry.<line><choice> (No thanks)<line><choice> (Hop aboard)<end>")
            self.set_text(812, "Nikeah-bound ferry.<line><choice> (No thanks.)<line><choice> (Hop aboard)<end>")
            self.set_text(813, "After the Serpent Trench check, you'll end up on the docks of this town.<end>")
            self.set_text(814, "Some towns have all 4 shop types: Item, Weapon, Armor, and Relic. This is one of them!<end>")
            self.set_text(815, "DANCER: Yoo hoo! You handsome thing. How 'bout joining me?<line>Tee hee!<end>")
            self.set_text(825, "Save time shopping by knowing exactly what you want to buy ahead of time.<end>")
            self.set_text(826, "With No Priceless Items on, consider selling items for high GP values early on, like Elixirs or Genji Helmets.<end>")
            self.set_text(917, "The reward you don't pick during the Lone Wolf check can be found in the World of Ruin Moogle Cave.<end>")
            self.set_text(918, "With good timing you can run past the last line of soldiers during the Kefka at Narshe battle!<end>")
            self.set_text(919, "You can't warp out of the Narshe mines in World of Balance, except for the Moogle Cave.<end>")
            self.set_text(920, "In World of Ruin Narshe, some doors might be locked until you recruit Locke.<end>")
            self.set_text(926, "A Peace Ring or Ribbon can help deal with the negative effects of a Cursed Shld in battle.<end>")
            self.set_text(927, "The entrance to Umaro's cave can be found in the World of Ruin, after defeating the boss at Tritoch. If the reward is a character, they will be peeking out of a cave just north of town.<end>")
            self.set_text(928, "Once you spot him, follow Lone Wolf to the Narshe peak!<end>")
            self.set_text(929, "Use caution with Umaro: enemies like Whelk have mechanics where you need to carefully time your attacks.<end>")
            self.set_text(930, "Umaro comes equipped with a Snow Muffler. Consider giving this to another character, or selling even it.<end>")
            self.set_text(931, "Umaro's body slam attack ignores enemy defense.<end>")
            self.set_text(932, "Activate the Security Checkpoint from the checkpoint room's southern door in the World of Balance.<end>")
            self.set_text(981, "Beyond is the Engine Room. Head to Figaro Castle World of Ruin to go below.<end>")
            self.set_text(986, "ValiantKnife's HP differential damage is not subject to Offering's damage penalty - making for an effective pair.<end>")
            self.set_text(987, "Power up ValiantKnife by unequipping and reequipping Muscle Belt/Red Cap before a battle.<page>Try not to heal ValiantKnife wielders in-between fights.<end>")
            self.set_text(988, "The airship faces North when entering from the world map. Buffer the direction you want to go as you enter.<end>")
            self.set_text(989, "If the Falcon allows you to “Search the Skies”, select that to start the Doom Gaze spot's fight immediately.<end>")
            self.set_text(990, "Hold R or L to turn the Airship faster.<end>")
            self.set_text(991, "Hold R or L to turn the Airship faster.<end>")
            self.set_text(992, "Sniper and Hawk Eye both have a 50% chance to deal 150% damage to enemies.<page>They'll deal 300% damage against floating ones. You can cast Float on enemies to make them vulnerable to this.<end>")
            self.set_text(993, "Fixed Dice ignores enemy defense and deals damage based on character level and the dice rolls.<end>")
            self.set_text(994, "Hold Y when flying to strafe. You won't trigger the Search the Skies encounter while doing this.<page>Avoid that encounter entirely by flying to where your destination would be in the World of Balance, then switching to the World of Ruin and landing. Check your minimap to learn where locations are in both worlds.<end>")
            self.set_text(1012, "ValiantKnife deals bonus damage equal to the difference between the wielder's max HP and current HP.<end>")
            self.set_text(1014, "The Kohlingen Inn reward appears in both worlds.<end>")
            self.set_text(1016, "You might not expect it, but Dice and Fixed Dice gain Jump damage bonuses.<end>")
            self.set_text(1018, "Higher levels and equipping Sneak Ring will improve Steal success rate.<end>")
            self.set_text(1019, "Phoenix revives all Wounded characters in battle.<end>")
            self.set_text(1028, "Higher levels and equipping Sneak Ring will improve Steal success rate.<end>")
            self.set_text(1029, "Save time by only attacking with your highest damage character to reduce animation time.<end>")
            self.set_text(1030, "Two items in the Auction House can be bought repeatedly. That's not the case in World of Ruin though!<end>")
            self.set_text(1031, "Strength or MagPwr +2 Espers may guide which character builds you end up using.<page>Consider keeping characters at low levels (e.g. out of the party) to maximize the use of the bonus later, after another character has made good use of it.<end>")
            self.set_text(1032, "Higher Stamina will increase the amount of damage you take from Poison each turn, as well as the amount of HP healed by Regen each turn.<end>")
            self.set_text(1033, "The Opera House is far to the south of here.<end>")
            self.set_text(1034, "Want physical damage? Go for Atlas Armlet or Hero Ring. Magic user? Equip 2 Earrings, 2 Hero Rings, or 1 of each.<end>")
            self.set_text(1036, "Bring Warp Stones if you venture into Zozo - both Mt. Zozo and Zozo Tower are long climbs down.<end>")
            self.set_text(1038, "In Zozo, the thieves will give you clues to solving the clock puzzle. Remember, they're all liars!<end>")
            self.set_text(1039, "Breaking elemental shields cast tier 3 spells that ignore defense and Reflect status.<end>")
            self.set_text(1040, "Breaking Rods cast tier 2 spells that ignore defense and Reflect status.<end>")
            self.set_text(1041, "The Auction House will always have 2 high tier items or Espers at 20000 GP and 10000 GP.<end>")
            self.set_text(1042, "Quick is a great defensive spell. After casting it, enemy ATB is frozen until your caster completes 2 turns.<page>Enemies won't be able to counter your first turn actions. Damage your enemy one turn, then heal up the next.<end>")
            self.set_text(1206, "Oh my hero, so far away now. Will I ever see your smile?<line>Love goes away, like night into day. It's just a fading dream…<page>I'm the darkness, you're the stars. Our love is brighter than the sun. For eternity, for me there can be,<page>only you, my chosen one…<line>Must I forget you? Our solemn promise? Will autumn take the place of spring?<page>What shall I do? I'm lost without you. Speak to me once more!<page>…here you pick up the flowers.<line>Climb the stairs to the balcony high atop the castle. Raise the flowers to the stars.<end>")
            self.set_text(1260, "Talk to Impresario first.<end>")
            self.set_text(1262, "Hit the 3rd switch from the left.<end>")
            self.set_text(1329, "Illumina deals the same amount of damage from the back row as the front.<end>")
            self.set_text(1334, "My child will heal you for 1 HP at a time!<end>")
            self.set_text(1338, "Magus Rod provides +7 MagPwr and 30% MBlock, an ideal choice for spellcasters.<end>")
            self.set_text(1339, "Man Eater will do 2x damage on human targets. SwordBreaker provides 30% Evade.<end>")
            self.set_text(1344, "Illumina's Pearl will critical hit with MP, dealing twice the damage as a normal Pearl.<end>")
            self.set_text(1346, "If you deal a killing blow with Ragnarok or Illumina, there will be no spell proc.<end>")
            self.set_text(1355, "Illumina and Ragnarok provide great Evade and MBlock - they're like great shields.<end>")
            self.set_text(1365, "Danger…<end>")
            self.set_text(1367, "Aura Lance has stronger battle power, but Pearl Lance can proc the Pearl spell.<end>")
            self.set_text(1368, "Tempest has a 50% chance of casting Wind Slash instead of its regular attack. Try it with Offering.<end>")
            self.set_text(1507, "Is your Blitz user Level 42 yet?<end>")
            self.set_text(1521, "The other reward you didn't pick is in the Narshe Mines World of Balance, past the Whelk check.<end>")
            self.set_text(1522, "Gogo and Umaro can't uncurse the Cursed Shld, so don't try it with them!<end>")
            self.set_text(1551, "Offering makes Fight swing 4 untargettable times with a 100% hit rate and 1/2 damage for each attack.<end>")
            self.set_text(1552, "Certain weapons drain MP to guarantee a critical hit. These criticals won't occur with Offering equipped, however.<end>")
            self.set_text(1553, "Desperation attacks have extremely high spell power and defense ignoring capabilities - don't forget about them when you're up against a wall!<end>")
            self.set_text(1554, "Physical damage is largely based off your level. Pair your Exp. Eggs with physical damage dealers.<end>")
            self.set_text(1555, "Atma Weapon damage increases with Level, but is not dependent on max HP.<page>Damage IS lowered the more HP you have lost.<end>")
            self.set_text(1556, "Gauntlet is great with natural command Jump characters. It also works well with Fight at higher levels if you have a strong weapon, but beware of attacks since you can't equip a shield.<end>")
            self.set_text(1558, "Haste isn't great at getting extra turns, but can help for getting the first turn or running quicker.<end>")
            self.set_text(1560, "Memento Ring does the same thing as Safety Bit.<end>")
            self.set_text(1562, "The Remedy spell won't restore Imp status, but the item will.<end>")
            self.set_text(1564, "Seizure deals damage like Poison, but Antidote items won't cure it. Use Remedy.<end>")
            self.set_text(1566, "The Remedy spell will remove Stop status, but the item won't.<end>")
            self.set_text(1568, "Safety Bit protects against Demi, Quartr, W-Wind, Doom, and all other fractional or instant death attacks.<page>It also prevents the Petrify status too! Great against Delta Hit.<end>")
            self.set_text(1573, "Recover from status effects in a pinch by KOing your own character, then reviving them. This can be a lifesaver if you need to unmute/unfreeze somebody!<end>")
            self.set_text(1574, "Berserked characters will be able to use: Fight, Capture, Jump, Rage, Magitek. They also deal more damage!<end>")
            self.set_text(1575, "Equipping a Relic that prevents a status will also heal that status immediately.<end>")
            self.set_text(1576, "Each time you apply Poison to a monster, it will deal 100% more damage during each poison tick (up to 8x).<end>")
            self.set_text(1577, "Muddled characters can be deadly. Hit them with the Fight command.<end>")
            self.set_text(1581, "Use Scan to identify enemy elemental weaknesses. Spells and elemental weapons can take advantage of those.<end>")
            self.set_text(1584, "Merton damage can be stopped with elemental shields, Rage Ring, Blizzard Orb, Red Jacket, Paladin Shld, and Minerva.<end>")
            self.set_text(1587, "Quake heals your whole party if they're all wearing Gaia Gear.<end>")
            self.set_text(1588, "Magic damage is greatly boosted by the MagPwr stat. Even gear like Magus Hat/White Dress can be worthwhile.<end>")
            self.set_text(1589, "Outside of battle, use Cure instead of Cure 2 and 3. It's more MP efficient!<end>")
            self.set_text(1590, "Fire, Ice, and Bolt 3 are incredibly strong spells you can use throughout the entire game.<end>")
            self.set_text(1592, "Pearl is a strong spell, but several bosses surprisingly absorb it: Atma, Goddess, Wrexsoul.<end>")
            self.set_text(1594, "Beating the boss at the Atma Weapon spot in Kefka's Tower will reward a high tier item and a Save Point.<end>")
            self.set_text(1595, "You can't get the treasure box behind me unless the world ends!<end>")
            self.set_text(1596, "Welcome!<end>")
            self.set_text(1597, "Outta here!<end>")
            self.set_text(1598, "Broke? Sell unused items!<end>")
            self.set_text(1599, "Whooopie!<end>")
            self.set_text(1600, "NPCs here have tips related to Magic and elements.<end>")
            self.set_text(1601, "Elemental shields teach tier 2 magic while equipped. Trade shields in your party to teach them to other characters.<end>")
            self.set_text(1602, "Meteor deals full damage even against multiple targets. It's not the strongest option against a single enemy, though.<end>")
            self.set_text(1603, "Cursed Rings teach X-Zone while equipped.<end>")
            self.set_text(1605, "Doom is more accurate at hitting enemies than X-Zone, but is only single target.<end>")
            self.set_text(1607, "Flare ignores enemy defense, although it takes a long time to cast.<end>")
            self.set_text(1608, "Sure!<end>")
            self.set_text(1734, "If you're looking for Lone Wolf, recruit Mog first and come back here (in the World of Balance)!<end>")
            self.set_text(1748, "If you should perish, you'll be able to play from your last save. You can save a game anywhere on the world map.<end>")
            self.set_text(1750, "Use Osmose on enemies if you need to recover MP mid-fight.<end>")
            self.set_text(1751, "Mirage Vests will provide Image status at the start of every tier.<end>")
            self.set_text(1763, "Learning new dances is as simple as winning a battle in new terrain without dancing.<end>")
            self.set_text(1766, "Dance chances, in order of their listing in the Skills menu:<line>7/16, 6/16, 2/16, 1/16<page>Think about those odds when Dancing!<end>")
            self.set_text(2082, "Pearl Wind heals the party for the same amount of HP the caster has.<end>")
            self.set_text(2083, "Try dodging Burning House flames by running past them the same moment they start moving towards you.<end>")
            self.set_text(2084, "Blow Fish is a great early Lore - unblockable 1000 damage!<end>")
            self.set_text(2085, "Characters won't learn Lores if they have the Dark status. Use Eyedrops or Remedy before the battle ends!<end>")
            self.set_text(2117, "General Leo...<line>Play as him with the help of custom graphics!<end>")
            self.set_text(2201, "The Tzen Thief in World of Balance will mention a glowing stone if he is selling an Esper. However, he won't tell you that here in the World of Ruin.<end>")
            self.set_text(2202, "Gigantos is weak to instant death and only uses physical damage. Use Phantom to be safe.<end>")
            self.set_text(2203, "Monster in a box fights CAN be run from. But sometimes it's better to save before opening them if you're looking for Gigantos (EXP) or PM Stalkers (MP).<end>")
            self.set_text(2204, "Don't use instant death on Specter, PM Stalkers, or other undead - they'll be fully healed.<end>")
            self.set_text(2205, "Allo Ver can be taken out with a Revivify or Fenix Down. Sketch works too.<end>")
            self.set_text(2206, "Telstar will start summoning Soldiers if you don't kill it quickly.<end>")
            self.set_text(2207, "Claw weapons dropped by Presenter and Allo Ver often sell for very high GP.<page>You can't Throw them, so why not get some GP instead?<end>")
            self.set_text(2208, "You can steal Minervas from Pugs, and win them from the fight as drops too.<end>")
            self.set_text(2209, "The Tzen Thief price can vary between 1 and 65535 GP, and it is different between worlds.<end>")
            self.set_text(2212, "There are monsters inside!<end>")
            self.set_text(2229, "NPCs here have tips for the game's final battle. There are 4 tiers to it, and each tier has its own challenges.<end>")
            self.set_text(2230, "Beads have a hidden effect to block physical attacks. Use them to dodge dangerous physical attacks like Calmness.<end>")
            self.set_text(2231, "Girl absorbs all elemental attacks. Use non-elemental damage on her.<end>")
            self.set_text(2232, "Heal Sleep out of Meteo phase (less than 10000 HP) if you're overwhelmed. Revivify will heal him for 5000 HP.<end>")
            self.set_text(2233, "Summon Fenrir or Golem in Tier 3 - they'll protect your entire party from Calmness.<end>")
            self.set_text(2234, "Tiger in Tier 2 can freeze your party, or turn them into Zombies. It's weak to Ice magic.<end>")
            self.set_text(2235, "You can retain your Morph infinitely if it runs out during a tier phase transition, or if the character is frozen or stopped.<end>")
            self.set_text(2236, "Kefka can't counterattack while charging Goner. Save big damage for when the screen starts shaking.<end>")
            self.set_text(2237, "Long Arm of Tier 1 and Tools in Tier 2 are weak to instant death. Mute or summon Siren against Magic in Tier 2.<end>")
            self.set_text(2238, "Vanish status or the Phantom summon will prevent all damage from 10 Hits or Tier 1 physicals.<end>")
            self.set_text(2239, "Watch me despawn this entire room…<end>")
            self.set_text(2240, "It'll never be the same again!<end>")
            self.set_text(2246, "You can only use Magic and Item commands in here.<end>")
            self.set_text(2247, "Check the wall to the right of the chest in this tower's first treasure room.<end>")
            self.set_text(2250, "You'll have to defeat the boss at the top to get the reward down here.<end>")
            self.set_text(2278, "We know about Esper summons!<end>")
            self.set_text(2279, "Summon Ragnarok to Morph dragons for a 1/8 instant kill chance.<end>")
            self.set_text(2280, "If affected by party-wide status effects (like Train), Unicorn is a great summon (casts Remedy on everyone).<end>")
            self.set_text(2281, "Odin and Raiden are instant death attacks on all enemies. Summon Sraphim and Starlet for a party-wide heal.<end>")
            self.set_text(2282, "Phunbaba's BabaBreath will send up to 2 of your characters back to the airship.<page>BabaBreath is also prioritized to be used on Wounded characters.<page>You'll have at least 1 character remaining in the party afterwards.<end>")
            self.set_text(2306, "Queue up attacks as you summon Palidor for extra damage.<end>")
            self.set_text(2323, "Set Battle Speed to 1 before fighting Zone Eater. This will save you time if it decides to use Demi instead of Engulf. But don't forget to change it back after!<end>")
            self.set_text(2324, "Use Mimic to re-use items like Super Balls, elemental shields, or strong throws like Excalibur. You can “Mimic” Mimic to keep using the same throw indefinitely.<end>")
            self.set_text(2326, "Flare, Hyper Drive, and Ultima all can be Runic'ed.<end>")
            self.set_text(2327, "Got money? GP Rain deals more damage with higher levels, and ignores all enemy defenses.<end>")
            self.set_text(2328, "Set Gogo's 3 unused command slots to any abilities of your choosing in his Status menu.<end>")
            self.set_text(2329, "If Possess hits, it will immediately kill its target. Works on bosses too!<end>")
            self.set_text(2335, "Once you start the Doma Dream sequence, you won't be able to warp out. Be careful when saving!<end>")
            self.set_text(2340, "Don't forget the reward on the Doma throne after finishing up the dream sequence.<end>")
            self.set_text(2350, "Left Crane absorbs Lightning. Right Crane absorbs Fire. Think: Left for Lightning!<end>")
            self.set_text(2351, "Fight Wrexsoul with physical damage, since his magic defense is so high.<end>")
            self.set_text(2353, "When Piranhas appear, you'll have to wait 5-55 seconds before Rizopas - the true final boss - appears.<end>")
            self.set_text(2354, "Ultros is always weak to Fire and always absorbs Water.<end>")
            self.set_text(2355, "Dragon Horn gives you 2-4 jumps a turn - a must for any Dragoon build. Make sure your character has Jump!<end>")
            self.set_text(2356, "If you defeat Moe and Curly in the stooges fight, Larry will eventually run away. Larry is weak to instant death.<end>")
            self.set_text(2357, "Use Ice on Ifrit, and Fire on Shiva. Non-elemental will work on both.<page>If you time it right, you can even run away from the battle during their transition phases.<end>")
            self.set_text(2358, "Casting Imp on Number 024 and SrBehemoth will force them into using physical attacks only.<end>")
            self.set_text(2364, "Try using Pearl Rods on Doom Gaze, who has high magic defense but is weak to Pearl.<end>")
            self.set_text(2365, "Despite his appearance, Dullahan is weak to Fire.<end>")
            self.set_text(2366, "Chadarnook is weak to Fire and Pearl…<end>")
            self.set_text(2367, "But don't attack while the girl is visible!<end>")
            self.set_text(2368, "Poltrgeist is vulnerable to Stop and weak to Poison.<end>")
            self.set_text(2369, "MagiMaster is vulnerable to Bserk. Also, you can hit him with one elemental attack before the first WallChange. Make it count!<end>")
            self.set_text(2370, "Phunbaba has a lot of HP, but is weak to Poison. Just don't use Bolt on him!<end>")
            self.set_text(2373, "Inferno uses a lot of powerful magic attacks. Focus down the main body with Bolt magic.<end>")
            self.set_text(2397, "Debilitator will create a new elemental weakness for its target.<end>")
            self.set_text(2398, "Flash and BioBlaster both deal magic damage. Flash applies Dark status, while BioBlaster applies Poison.<end>")
            self.set_text(2400, "Sketch, if it hits, has a 25% of killing KatanaSoul.<end>")
            self.set_text(2402, "Muddle KatanaSoul to kill him fast.<end>")
            self.set_text(2403, "The Figaro Throne reward exists in both worlds!<end>")
            self.set_text(2421, "Try fighting here early in a seed. Low level enemies won't have MP to use their abilities.<end>")
            self.set_text(2424, "My Colosseum is built in the World of Ruin!<end>")
            self.set_text(2425, "This is my colosseum.<end>")
            self.set_text(2426, "This is my colosseum.<end>")
            self.set_text(2427, "I'm in 4 different boss fights throughout the game!<end>")
            self.set_text(2429, "Colosseum can turn low GP items into great ones. Buy stacks of cheap items to maximize Colosseum potential.<end>")
            self.set_text(2430, "Umaro is great in the Colosseum since he won't cast random Magic spells in battle.<end>")
            self.set_text(2431, "Betting the Striker here doesn't unlock any character.<end>")
            self.set_text(2432, "This is Dragon's Neck Colosseum.<end>")
            self.set_text(2436, "You can enter the Phoenix Cave as long as you have at least 2 characters.<end>")
            self.set_text(2437, "Those beautiful days…<end>")
            self.set_text(2438, "Pressing Start in battle to pause the game can help with lining up slots in the Slots command.<end>")
            self.set_text(2442, "Red Dragon uses Fire magic, and is weak to Ice. You can also Muddle it!<end>")
            self.set_text(2443, "At low enough HP, Red Dragon will start using Flare too - which isn't Fire elemental!<end>")
            self.set_text(2444, "Slots' triple Bar will summon a random Esper... hope it's not Crusader!<end>")
            self.set_text(2446, "Several Slots results can deal non-elemental, unblockable damage to enemies.<end>")
            self.set_text(2453, "Slots will give leniency after you stop the first reel, allowing you to land 7-Flush and Chocobop if you can line up Diamonds/Chocobo on the first reel.<end>")
            self.set_text(2454, "Spikes in the Phoenix Cave will drop your HP as you step on them!<end>")
            self.set_text(2455, "Slots' Lagomorph can heal Dark, Sleep, and Poison.<end>")
            self.set_text(2457, "Slots RNG starts off the same in each battle. If you can use H-Bomb turn 1 in a battle, it'll work in every battle if nothing has affected the RNG.<end>")
            self.set_text(2532, "SwdTech 2 and 6 deal more damage with higher MagPwr (instead of Vigor).<end>")
            self.set_text(2533, "Buy Rust-Rid in Zozo for 1000 GP to gain access to Mt. Zozo.<end>")
            self.set_text(2536, "If the Retort bug fix flag is disabled, try KO'ing your SwdTech user, reviving them, and then using Retort.<end>")
            self.set_text(2537, "What shall I talk about?<page><choice> (Narshe)<line><choice> (The Veldt)<line><choice> (Doma Castle)<line><choice> (Nothing, thanks!)<end>")
            self.set_text(2538, "Storm Drgn is weak to Bolt attacks, despite its name.<end>")
            self.set_text(2539, "Use SwdTech 5 to restore both HP and MP.<end>")
            self.set_text(2541, "Did you know that SwdTech damage is not increased by equipped weapon battle power?<page>SwdTech 1, 4, and 7 do get stronger with higher Vigor, however.<end>")
            self.set_text(2603, "Characters selected to fight here have HP restored before battle, even Wounded ones.<page>There's no restore after battles - so if they're injured when the fight's done, they'll stay that way!<end>")
            self.set_text(2623, "Hold A at the victory screen to skip text at max speed.<end>")
            self.set_text(2626, "In tough battles, wait to see the outcome of enemy attacks before queuing up your own.<end>")
            #2640 is used in Auction event, keep vanilla (Ho, ho, ho... There's nothing I can't buy!)
            #self.set_text(2640, "Equip the Cursed Shld in the middle of a battle to avoid its negative status effects entirely.<page>If the character survives the battle, this will still count towards uncursing it!<end>")
            self.set_text(2678, "128+ Evade/MBlock will block everything except unblockable abilities like Ultima.<end>")
            self.set_text(2679, "Higher Stamina will increase the amount of damage you take from Poison each turn, as well as the amount of HP healed by Regen each turn.<end>")
            self.set_text(2681, "Save time by arranging your item menu during battle animations. Group up items you want to sell.<end>")
            self.set_text(2682, "Use Economizer with an Esper like Bahamut or Lore like GrandTrain to quickly break open a seed.<end>")
            self.set_text(2684, "Sketch, if done successfully, can do one of two things depending on the enemy.<end>")
            self.set_text(2691, "Super Balls can help win a few fights if under-leveled. Also, seek undead enemies and kill them with Revivify/Fenix Down.<end>")
            self.set_text(2692, "Memorizing good Rages will help break open seeds quicker.<end>")
            self.set_text(2694, "Learn which attacks ignore enemy defense. Some examples are Flare, Bum Rush, and SwdTech 7.<end>")
            self.set_text(2695, "Use X-Magic on the second turn of Quick and you'll still have full ATB after the X-Magic.<end>")
            self.set_text(2696, "Use Tents/Sleeping Bags in multiparty dungeons when not on a save point by moving onto a save point, then immediately switching to a different party and going into the menu.<end>")
            self.set_text(2699, "Avoid counter attacks by not attacking with weak party members. Use X/Y to skip their turn if needed.<end>")
            self.set_text(2702, "Have you heard? The fourth Ultros fight with Chupon doesn't give you anything. Not even XP.<end>")
            self.set_text(2726, "You can save some frames by closing the command menu before a battle ends. I like to use Defend on everyone.<end>")
            self.set_text(2746, "The Auction House is always a bit of a gamble, isn't it?<end>")
            self.set_text(2747, "In the World of Ruin, you can eventually buy out every item in the Auction House for 90000 GP.<page>Watch out for Imp Robots though - they'll just waste your time.<end>")
            self.set_text(2848, "Killing all the Hidonites will cause Hidon to use a strong non-elemental attack. Be careful when using attacks that damage all enemies.<end>")
            self.set_text(2849, "Hidon is weak to Fire and Pearl! If you kill Hidon first, any other Hidonites will die as well.<end>")
            self.set_text(2850, "22 Coral are required to get past the talking chest in Ebot's Rock.<end>")
            self.set_text(2857, "Lores can't be Runic'ed, making them a good pair (e.g. Runic + Pearl Wind).<end>")
            self.set_text(2915, "This is Figaro Castle.<end>")
            self.set_text(2920, "If Edgar leads your party, all the shops in Figaro Castle are 1/2 off.<end>")
            self.set_text(2921, "This discount works in South Figaro World of Ruin too!<end>")

            # conditional flags for character gating
            if args.character_gating:
                self.set_text(749, "The Veldt check reward will not appear on a back or pincer attack, nor will it appear after several battles against formations with many enemies. Ensure you have Dried Meat, less than 3 characters in the party, and recruited <GAU> when doing this check.<end>")
                self.set_text(1051, "Haven't seen any rewards here. Might want to check the top of the building after recruiting <TERRA>!<end>")
                self.set_text(1065, "This place is dangerous! Visit me in the World of Ruin after recruiting <CYAN>!<end>")
                self.set_text(1196, "Have you recruited Maria, I mean, <CELES> yet?<end>")
                self.set_text(1333, "No one gets in without recruiting General <CELES>!<end>")
                #adjusted in event\figaro_castle_wor.py
                #self.set_text(2379, "I won't budge from this spot until you have recruited <EDGAR>!<end>")
                self.set_text(2436, "You can enter the Phoenix Cave as long as you have at least 2 characters.<page><LOCKE> also needs to be recruited to get the reward at the end.<end>")
                self.set_text(2685, "<RELM>'s checks include Esper Mountain near Thamasa in the World of Balance, and right here in Owzer's Mansion in the World of Ruin.<end>")

        #### end of NPC dialog tip mod

    def write(self):
        self.dialog_data.assign([dialog.data() for dialog in self.dialogs])
        for dialog_index, dialog in enumerate(self.dialogs):
            if (dialog_index < len(self.dialogs) - 1 and
                    self.dialog_data.pointers[dialog_index] < self.dialog_data.pointers[dialog_index - 1]):
                Space.rom.set_short(self.FIRST_CE_PTR_INDEX_ADDR, dialog_index)
        self.dialog_data.write()

        self.battle_message_data.assign([dialog.data() for dialog in self.battle_messages])
        self.battle_message_data.write()

        self.single_line_battle_dialog_data.assign([dialog.data() for dialog in self.single_line_battle_dialogs])
        self.single_line_battle_dialog_data.write()

        self.multi_line_battle_dialog_data.assign([dialog.data() for dialog in self.multi_line_battle_dialogs])
        self.multi_line_battle_dialog_data.write()

    def print(self):
        for dialog in self.dialogs:
            dialog.print()
        for dialog in self.battle_messages:
            dialog.print()
        for dialog in self.single_line_battle_dialogs:
            dialog.print()
        for dialog in self.multi_line_battle_dialogs:
            dialog.print()
