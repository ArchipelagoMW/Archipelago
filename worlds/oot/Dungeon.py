class Dungeon(object):

    def __init__(self, world, name, hint, font_color, boss_key, small_keys, dungeon_items):
        def to_array(obj):
            if obj == None:
                return []
            if isinstance(obj, list):
                return obj
            else:
                return [obj]

        self.multiworld = world
        self.name = name
        self.hint_text = hint
        self.font_color = font_color
        self.regions = []
        self.boss_key = to_array(boss_key)
        self.small_keys = to_array(small_keys)
        self.dungeon_items = to_array(dungeon_items)

        for region in world.multiworld.regions:
            if region.player == world.player and region.dungeon == self.name:
                region.dungeon = self
                self.regions.append(region)                


    def copy(self, new_world):
        new_boss_key = [item.copy(new_world) for item in self.boss_key]
        new_small_keys = [item.copy(new_world) for item in self.small_keys]
        new_dungeon_items = [item.copy(new_world) for item in self.dungeon_items]

        new_dungeon = Dungeon(new_world, self.name, self.hint_text, self.font_color, new_boss_key, new_small_keys, new_dungeon_items)

        return new_dungeon


    @property
    def keys(self):
        return self.small_keys + self.boss_key


    @property
    def all_items(self):
        return self.dungeon_items + self.keys


    def is_dungeon_item(self, item):
        return item.name in [dungeon_item.name for dungeon_item in self.all_items]


    def __str__(self):
        return str(self.__unicode__())


    def __unicode__(self):
        return '%s' % self.name

