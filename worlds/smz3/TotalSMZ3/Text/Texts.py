import io
from pathlib import Path
import sys
from typing import Any, List
import zipfile
from ..Region import Region
from ..Regions.Zelda.GanonsTower import GanonsTower
from ..Item import Item, ItemType
from Utils import unsafe_parse_yaml
import random
import os

text_folder = Path(__file__).parents[3]

def openFile(resource: str, mode: str = "r", encoding: str = None):
    filename = sys.modules[__name__].__file__
    apworldExt = ".apworld"
    game = "smz3/"
    if apworldExt in filename:
        zip_path = Path(filename[:filename.index(apworldExt) + len(apworldExt)])
        with zipfile.ZipFile(zip_path) as zf:
            zipFilePath = resource[resource.index(game):]
            if mode == 'rb':
                return zf.open(zipFilePath, 'r')
            else:
                return io.TextIOWrapper(zf.open(zipFilePath, 'r'), encoding)
    else:
        return open(os.path.join(text_folder, resource), mode, encoding=encoding)

class Texts:
    @staticmethod
    def ParseYamlScripts(resource: str):
        with openFile(resource, 'rb') as f:
            yaml = str(f.read(), "utf-8")
        return unsafe_parse_yaml(yaml)

    @staticmethod        
    def ParseTextScript(resource: str):
        with openFile(resource, 'r', encoding="utf-8-sig") as file:
            return [text.rstrip('\n') for text in file.read().replace("\r", "").split("---\n") if text]

    scripts: Any = ParseYamlScripts.__func__("smz3/TotalSMZ3/Text/Scripts/General.yaml")
    blind: List[str] = ParseTextScript.__func__("smz3/TotalSMZ3/Text/Scripts/Blind.txt")
    ganon: List[str] = ParseTextScript.__func__("smz3/TotalSMZ3/Text/Scripts/Ganon.txt")
    tavernMan: List[str] = ParseTextScript.__func__("smz3/TotalSMZ3/Text/Scripts/TavernMan.txt")
    triforceRoom: List[str] = ParseTextScript.__func__("smz3/TotalSMZ3/Text/Scripts/TriforceRoom.txt")

    @staticmethod
    def SahasrahlaReveal(dungeon: Region):
        text = Texts.scripts["SahasrahlaReveal"]
        return text.replace("<dungeon>", dungeon.Area)

    @staticmethod
    def BombShopReveal(dungeons: List[Region]):
        text = Texts.scripts["BombShopReveal"]
        return text.replace("<first>", dungeons[0].Area).replace("<second>", dungeons[1].Area)

    @staticmethod
    def GanonThirdPhaseSingle(silvers: Region):
        node = Texts.scripts["GanonSilversReveal"]["single"]
        text = node["local" if isinstance(silvers, GanonsTower) else "remote"]
        return text.replace("<region>", silvers.Area)

    @staticmethod
    def GanonThirdPhaseMulti(silvers: Region, myWorld: int, silversWorld: int = None, silversPlayer: str = None):
        node = Texts.scripts["GanonSilversReveal"]["multi"]
        if silvers is None:
            if (silversWorld == myWorld.Id):
                return node["local"]
            player = silversPlayer
        else:
            if (silvers.world == myWorld):
                return node["local"]
            player = silvers.world.Player
        player = player.rjust(7 + len(player) // 2)
        text = node["remote"]
        return text.replace("<player>", player)

    @staticmethod
    def ItemTextbox(item: Item):
        nameMap = {
                    ItemType.BottleWithGoldBee : ItemType.BottleWithBee.name,
                    ItemType.HeartContainerRefill : ItemType.HeartContainer.name,
                    ItemType.OneRupee : "PocketRupees",
                    ItemType.FiveRupees : "PocketRupees",
                    ItemType.TwentyRupees : "CouchRupees",
                    ItemType.TwentyRupees2 : "CouchRupees",
                    ItemType.FiftyRupees : "CouchRupees",
                    ItemType.BombUpgrade5 : "BombUpgrade",
                    ItemType.BombUpgrade10 : "BombUpgrade",
                    ItemType.ArrowUpgrade5 : "ArrowUpgrade",
                    ItemType.ArrowUpgrade10 : "ArrowUpgrade",
                    item.Type : item.Type.name,
                }
        if item.IsMap(): name = "Map"
        elif item.IsCompass(): name = "Compass"
        elif item.IsSmMap(): name = "SmMap"
        else: name = nameMap[item.Type]

        items = Texts.scripts["Items"]
        return items.get(name, None) or items["default"]

    @staticmethod
    def Blind(rnd: random): return Texts.RandomLine(rnd, Texts.blind)

    @staticmethod
    def TavernMan(rnd: random): return Texts.RandomLine(rnd, Texts.tavernMan)

    @staticmethod
    def GanonFirstPhase(rnd: random): return Texts.RandomLine(rnd, Texts.ganon)

    @staticmethod
    def TriforceRoom(rnd: random): return Texts.RandomLine(rnd, Texts.triforceRoom)

    @staticmethod
    def RandomLine(rnd: random, lines: List[str]): return lines[rnd.randrange(0, len(lines))]
