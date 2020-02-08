class OWGSets(self):
    '''
    Helper class to deliver entrance/exit/region sets to OWG rules.
    '''

    def get_immediately_accessible_entrances(self):
        '''
        Entrances that are available with no items at all.

        At this point, these are fake flipper spots.
        '''
        return [
            'Hobo Bridge',
            'Zoras River',
            'Lake Hylia Island Mirror Spot',
            'Capacity Upgrade',
            ]

    def get_lw_boots_accessible_entrances(self, world, player):
        '''
        Light World entrances that can be accessed with boots clips.
        '''
        entrances = [
            'Bat Cave Drop Ledge',
            'Desert Ledge Return Rocks',
            'Desert Palace Entrance (West)',
            'Desert Palace Entrance (North)',
            'Flute Spot 1',
            'Broken Bridge (East)',
            'Death Mountain Drop',
            'Old Man Cave (East)',
            'Old Man House (Bottom)',
            'Old Man House (Top)',
            'Death Mountain Return Cave (East)',
            'Spectacle Rock Cave',
            'Spectacle Rock Cave Peak',
            'Spectacle Rock Cave (Bottom)',
            'Spectacle Rock Mirror Spot',
            'Broken Bridge (West)',
            'Broken Bridge (East)',
            'East Death Mountain Drop',
            'Spiral Cave Ledge Drop',
            'Fairy Ascension Drop',
            'Fairy Ascension Cave (Bottom)',
            'East Death Mountain (Top)',
            'Death Mountain (Top)',
            'Spectacle Rock Drop',
            'Death Mountain Return Cave (West)',
            'Paradox Cave (Bottom)',
            'Paradox Cave (Middle)',
            'Hookshot Fairy',
            'Spiral Cave (Bottom)',
            'Paradox Cave (Top)',
            'Spiral Cave Ledge Access',
            'Fairy Ascension Ledge',
            'Cave 45 Mirror Spot',
            'Graveyard Ledge Mirror Spot',
            'Bumper Cave Ledge Mirror Spot',
            'Desert Ledge (Northeast) Mirror Spot',
            'Desert Ledge Mirror Spot',
            'Desert Palace Entrance (North) Mirror Spot',
            'East Death Mountain (Top) Mirror Spot',
            'Spiral Cave Mirror Spot',
            'Fairy Ascension Mirror Spot',
            'Floating Island Mirror Spot',
            ]

        if world.mode[player] != 'inverted':
            entrances.append('Cave 45')
            entrances.append('Graveyard Cave')

        return entrances


    def get_lw_boots_accessible_locations(self):
        '''
        Light World locations that can be reached using boots clips.
        '''
        return [
            'Lake Hylia Island',
            'Desert Ledge',
            'Spectacle Rock',
            'Floating Island',
            ]


    def get_dw_boots_accessible_entrances(self):
        '''
        Dark World entrances that can be accessed with boots clips.
        '''
        return [
            'Northeast Dark World Broken Bridge Pass',
            'Peg Area Rocks',
            'Grassy Lawn Pegs',
            'West Dark World Gap',
            'Bumper Cave Ledge Drop',
            'Turtle Rock Drop',
            'Floating Island Drop',
            'Dark Death Mountain Drop (East)',
            'Village of Outcasts Drop',
            'Dark Lake Hylia Ledge',
            'Hype Cave',
            'Dark World Potion Shop',
            'Big Bomb Shop',
            'Archery Game',
            'Brewery',
            'C-Shaped House',
            'Chest Game',
            'Thieves Town',
            'Kings Grave Mirror Spot',
            'Bumper Cave Entrance Rock',
            'Red Shield Shop',
            'Dark Sanctuary Hint',
            'Fortune Teller (Dark)',
            'Dark World Lumberjack Shop',
            'Misery Mire',
            'Mire Shed',
            'Dark Desert Hint',
            'Dark Desert Fairy',
            ]


    def get_dw_boots_accessible_locations(self):
        '''
        Dark World locations accessible using boots clips.
        '''
        return [
            'Catfish',
            'Dark Blacksmith Ruins',
            'Bumper Cave Ledge',
            ]


    def get_dw_bunny_inaccessible_locations(self):
        '''
        Locations that the bunny cannot access.
        '''
        return [
            'Thieves Town',
            'Graveyard Ledge Mirror Spot',
            'Kings Grave Mirror Spot',
            'Bumper Cave Entrance Rock',
            'Brewery',
            'Village of Outcasts Pegs',
            'Village of Outcasts Eastern Rocks',
            'Dark Lake Hylia Drop (South)',
            'Hype Cave',
            'Village of Outcasts Heavy Rock',
            'East Dark World Bridge',
            'Bonk Fairy (Dark)',
            ]


    def get_dmd_and_bunny_regions(self):
        '''
        Dark World regions accessible using Link and Bunny DMD methods.
        '''
        return [
            'West Dark World',
            'South Dark World',
            'Northeast Dark World',
            ]


    def get_dmd_non_bunny_regions(self):
        '''
        Dark World regions accessible using only Link DMD methods.
        '''
        return [
            'Dark Desert',
            'East Dark World',
            ]


    def get_mirror_hookshot_accessible_dw_locations(self, world, player):
        '''
        Locations accessible potentially using weird mirror hookshot boots setups.
        '''
        locations = [
            'Pyramid Fairy',
            'Pyramid Entrance',
            'Pyramid Drop',
            ]
        locations.extend(world.get_region('Dark Death Mountain Ledge', player).locations)
        return locations


    def sword_required_superbunny_mirror_regions(self):
        '''
        Cave regions that superbunny can get through - but only with a sword.
        '''
        return [
            'Mini Moldorm Cave',
            'Spiral Cave (Top)',
            ]