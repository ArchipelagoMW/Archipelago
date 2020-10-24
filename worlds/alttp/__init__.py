from BaseClasses import World


class ALTTPWorld(World):
    def __init__(self, options, slot: int):
        self._region_cache = {}
        self.slot = slot
        self.shuffle = shuffle
        self.logic = logic
        self.mode = mode
        self.swords = swords
        self.difficulty = difficulty
        self.difficulty_adjustments = difficulty_adjustments
        self.timer = timer
        self.progressive = progressive
        self.goal = goal
        self.dungeons = []
        self.regions = []
        self.shops = []
        self.itempool = []
        self.seed = None
        self.precollected_items = []
        self.state = CollectionState(self)
        self._cached_entrances = None
        self._cached_locations = None
        self._entrance_cache = {}
        self._location_cache = {}
        self.required_locations = []
        self.light_world_light_cone = False
        self.dark_world_light_cone = False
        self.rupoor_cost = 10
        self.aga_randomness = True
        self.lock_aga_door_in_escape = False
        self.save_and_quit_from_boss = True
        self.accessibility = accessibility
        self.shuffle_ganon = shuffle_ganon
        self.fix_gtower_exit = self.shuffle_ganon
        self.retro = retro
        self.custom = custom
        self.customitemarray: List[int] = customitemarray
        self.hints = hints
        self.dynamic_regions = []
        self.dynamic_locations = []


        self.remote_items = False
        self.required_medallions = ['Ether', 'Quake']
        self.swamp_patch_required = False
        self.powder_patch_required = False
        self.ganon_at_pyramid = True
        self.ganonstower_vanilla = True


        self.can_access_trock_eyebridge = None
        self.can_access_trock_front = None
        self.can_access_trock_big_chest = None
        self.can_access_trock_middle = None
        self.fix_fake_world = True
        self.mapshuffle = False
        self.compassshuffle = False
        self.keyshuffle = False
        self.bigkeyshuffle = False
        self.difficulty_requirements = None
        self.boss_shuffle = 'none'
        self.enemy_shuffle = False
        self.enemy_health = 'default'
        self.enemy_damage = 'default'
        self.killable_thieves = False
        self.tile_shuffle = False
        self.bush_shuffle = False
        self.beemizer = 0
        self.escape_assist = []
        self.crystals_needed_for_ganon = 7
        self.crystals_needed_for_gt = 7
        self.open_pyramid = False
        self.treasure_hunt_icon = 'Triforce Piece'
        self.treasure_hunt_count = 0
        self.clock_mode = False
        self.can_take_damage = True
        self.glitch_boots = True
        self.progression_balancing = True
        self.local_items = set()
        self.triforce_pieces_available = 30
        self.triforce_pieces_required = 20
        self.shop_shuffle = 'off'
        self.shuffle_prizes = "g"
        self.sprite_pool = []
        self.dark_room_logic = "lamp"
        self.restrict_dungeon_item_on_boss = False

    @property
    def sewer_light_cone(self):
        return self.mode == "standard"

    @property
    def fix_trock_doors(self):
        return self.shuffle != 'vanilla' or self.mode == 'inverted'

    @property
    def fix_skullwoods_exit(self):
        return self.shuffle not in {'vanilla', 'simple', 'restricted', 'dungeonssimple'}

    @property
    def fix_palaceofdarkness_exit(self):
        return self.shuffle not in {'vanilla', 'simple', 'restricted', 'dungeonssimple'}

    @property
    def fix_trock_exit(self):
        return self.shuffle not in {'vanilla', 'simple', 'restricted', 'dungeonssimple'}