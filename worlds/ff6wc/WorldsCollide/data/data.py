from ..data import dialogs as dialogs
from ..data import spells as spells
from ..data import characters as characters
from ..data import items as items
from ..data import metamorph_groups as metamorph_groups
from ..data import maps as maps
from ..data import enemies as enemies
from ..data import swdtechs as swdtechs
from ..data import blitzes as blitzes
from ..data import lores as lores
from ..data import rages as rages
from ..data import dances as dances
from ..data import steal as steal
from ..data import sketches as sketches
from ..data import controls as controls
from ..data import magiteks as magiteks
from ..data import espers as espers
from ..data import shops as shops
from ..data import coliseum as coliseum
from ..data import title_graphics as title_graphics

class Data:
    def __init__(self, rom, args):
        self.dialogs = dialogs

        self.spells = spells.Spells(rom, args)
        self.spells.mod()

        self.characters = characters.Characters(rom, args, self.spells)
        self.characters.mod()

        self.items = items.Items(rom, args, self.dialogs, self.characters)
        self.items.mod()

        self.metamorph_groups = metamorph_groups.MetamorphGroups(rom)
        self.metamorph_groups.mod()

        self.maps = maps.Maps(rom, args, self.items)
        self.maps.mod(self.characters)

        self.enemies = enemies.Enemies(rom, args, self.items)
        self.enemies.mod(self.maps)

        self.swdtechs = swdtechs.SwdTechs(rom, args, self.characters)
        self.swdtechs.mod()

        self.blitzes = blitzes.Blitzes(rom, args, self.characters)
        self.blitzes.mod()

        self.lores = lores.Lores(rom, args, self.characters)
        self.lores.mod(self.dialogs)

        self.rages = rages.Rages(rom, args, self.enemies)
        self.rages.mod()

        self.dances = dances.Dances(rom, args, self.characters)
        self.dances.mod()

        self.steal = steal.Steal(rom, args)
        self.steal.mod()

        self.sketches = sketches.Sketches(rom, args, self.enemies, self.rages)
        self.sketches.mod()

        self.controls = controls.Controls(rom, args, self.enemies, self.rages)
        self.controls.mod()

        self.magiteks = magiteks.Magiteks(rom, args)
        self.magiteks.mod()

        self.espers = espers.Espers(rom, args, self.spells, self.characters)
        self.espers.mod(self.dialogs)

        self.shops = shops.Shops(rom, args, self.items)
        self.shops.mod()

        self.coliseum = coliseum.Coliseum(rom, args, self.enemies, self.items)
        self.coliseum.mod()

        self.title_graphics = title_graphics.TitleGraphics(rom, args)
        self.title_graphics.mod()

    def write(self):
        self.dialogs.write()
        self.characters.write()
        self.items.write()
        self.metamorph_groups.write()
        self.maps.write()
        self.enemies.write()
        self.spells.write()
        self.swdtechs.write()
        self.blitzes.write()
        self.lores.write()
        self.rages.write()
        self.dances.write()
        self.steal.write()
        self.sketches.write()
        self.controls.write()
        self.magiteks.write()
        self.espers.write()
        self.shops.write()
        self.coliseum.write()
        self.title_graphics.write()
