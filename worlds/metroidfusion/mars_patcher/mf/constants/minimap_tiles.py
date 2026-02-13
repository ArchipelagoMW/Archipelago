from __future__ import annotations

from enum import Enum
from typing import NamedTuple

from typing_extensions import Self

# String Format
# <top><left><right><bottom>_<top-left><top-right><bottom-left><bottom-right>_<content>

# Chunk 1 (tile edges)
# - see Edge and ColoredDoor for values

# Chunk 2 (tile corners)
# - C: corner pixel
# - x: none

# Chunk 3 (tile content)
# - see Content for values


# Edges
class Edge(Enum):
    EMPTY = "x"
    WALL = "W"
    SHORTCUT = "S"
    DOOR = "D"

    @property
    def is_door(self) -> bool:
        return self == Edge.DOOR


class ColoredDoor(Enum):
    BLUE = "B"
    GREEN = "G"
    YELLOW = "Y"
    RED = "R"

    @property
    def is_door(self) -> bool:
        return True

    # Aliases
    L1 = BLUE
    L2 = GREEN
    L3 = YELLOW
    L4 = RED


class TileEdges(NamedTuple):
    top: Edge = Edge.WALL
    left: Edge | ColoredDoor = Edge.WALL
    right: Edge | ColoredDoor = Edge.WALL
    bottom: Edge = Edge.WALL

    @property
    def as_str(self) -> str:
        return f"{self.top.value}{self.left.value}{self.right.value}{self.bottom.value}"

    @classmethod
    def from_str(cls, value: str) -> Self:
        if len(value) != 4:
            raise ValueError(f"'{value}' is not a valid TileEdges string")
        top, left, right, bottom = tuple(value)

        def any_edge_from_value(v: str) -> Edge | ColoredDoor:
            try:
                return Edge(v)
            except ValueError:
                pass

            try:
                return ColoredDoor(v)
            except ValueError:
                raise ValueError(f"{repr(v)} is not a valid Edge or ColoredDoor")

        return cls(
            top=Edge(top),
            left=any_edge_from_value(left),
            right=any_edge_from_value(right),
            bottom=Edge(bottom),
        )

    def h_flip(self) -> TileEdges:
        return TileEdges(
            top=self.top,
            left=self.right,
            right=self.left,
            bottom=self.bottom,
        )

    def v_flip(self) -> TileEdges:
        return TileEdges(
            top=self.bottom,
            left=self.left,
            right=self.right,
            bottom=self.top,
        )


# Corners
class TileCorners(NamedTuple):
    top_left: bool = False
    top_right: bool = False
    bottom_left: bool = False
    bottom_right: bool = False

    @property
    def as_str(self) -> str:
        def s(corner: bool) -> str:
            return "C" if corner else "x"

        return f"{s(self.top_left)}{s(self.top_right)}{s(self.bottom_left)}{s(self.bottom_right)}"

    @classmethod
    def from_str(cls, value: str) -> Self:
        if len(value) != 4:
            raise ValueError(f"'{value}' is not a valid TileCorners string")
        tl, tr, bl, br = tuple(value)
        return cls(
            top_left=(tl == "C"),
            top_right=(tr == "C"),
            bottom_left=(bl == "C"),
            bottom_right=(br == "C"),
        )

    def h_flip(self) -> TileCorners:
        return TileCorners(
            top_left=self.top_right,
            top_right=self.top_left,
            bottom_left=self.bottom_right,
            bottom_right=self.bottom_left,
        )

    def v_flip(self) -> TileCorners:
        return TileCorners(
            top_left=self.bottom_left,
            top_right=self.bottom_right,
            bottom_left=self.top_left,
            bottom_right=self.top_right,
        )


# Contents
class Content(Enum):
    EMPTY = "x"
    NAVIGATION = "N"
    SAVE = "S"
    RECHARGE = "R"
    HIDDEN_RECHARGE = "H"
    DATA = "D"
    ITEM = "I"
    OBTAINED_ITEM = "O"
    BOSS = "B"
    GUNSHIP = "G"
    GUNSHIP_EDGE = "P"
    SECURITY = "K"
    AUXILLARY_POWER = "X"
    ANIMALS = "A"
    BOILER_PAD = "b"
    TUNNEL = "T"

    @property
    def can_h_flip(self) -> bool:
        exclude = {
            Content.NAVIGATION,
            Content.SAVE,
            Content.RECHARGE,
            Content.HIDDEN_RECHARGE,
            Content.DATA,
            Content.GUNSHIP,
            Content.GUNSHIP_EDGE,
        }
        return self not in exclude

    @property
    def can_v_flip(self) -> bool:
        exclude = {
            Content.NAVIGATION,
            Content.SAVE,
            Content.RECHARGE,
            Content.HIDDEN_RECHARGE,
            Content.GUNSHIP,
            Content.GUNSHIP_EDGE,
            Content.BOSS,
        }
        return self not in exclude


# Tile
class MapTile(NamedTuple):
    edges: TileEdges = TileEdges()
    corners: TileCorners = TileCorners()
    content: Content = Content.EMPTY

    @property
    def as_str(self) -> str:
        return f"{self.edges.as_str}_{self.corners.as_str}_{self.content.value}"

    @classmethod
    def from_str(cls, value: str) -> Self:
        if len(value) != 11:
            raise ValueError(f"'{value}' is not a valid MapTile string")
        edges, corners, content = value.split("_")
        return cls(
            edges=TileEdges.from_str(edges),
            corners=TileCorners.from_str(corners),
            content=Content(content),
        )

    def h_flip(self) -> MapTile:
        if not self.content.can_h_flip:
            raise ValueError(f"Cannot h_flip tile with contents {self.content}")

        return MapTile(
            edges=self.edges.h_flip(),
            corners=self.corners.h_flip(),
            content=self.content,
        )

    def v_flip(self) -> MapTile:
        if not self.content.can_v_flip:
            raise ValueError(f"Cannot v_flip tile with contents {self.content}")

        return MapTile(
            edges=self.edges.v_flip(),
            corners=self.corners.v_flip(),
            content=self.content,
        )


# Constants
COLORED_DOOR_TILES = {
    0x005: MapTile.from_str("WBxx_xxxx_x"),
    0x006: MapTile.from_str("DBxx_xxxx_x"),
    0x007: MapTile.from_str("DBxx_xxxC_x"),
    0x008: MapTile.from_str("DBBD_xxxx_x"),
    0x009: MapTile.from_str("DBBx_xxxx_x"),
    0x025: MapTile.from_str("xBxx_xxxx_x"),
    0x026: MapTile.from_str("xBxx_xCxC_x"),
    0x027: MapTile.from_str("DBWD_xxxx_x"),
    0x028: MapTile.from_str("DBDx_xxxx_x"),
    0x029: MapTile.from_str("DBBW_xxxx_x"),
    0x045: MapTile.from_str("WBxW_xxxx_x"),
    0x046: MapTile.from_str("DBxD_xxxx_x"),
    0x047: MapTile.from_str("DBxW_xxxx_x"),
    0x048: MapTile.from_str("WBWW_xxxx_x"),
    0x049: MapTile.from_str("WBBW_xxxx_x"),
    0x065: MapTile.from_str("DBWx_xxxx_x"),
    0x066: MapTile.from_str("WBDx_xxxx_x"),
    0x068: MapTile.from_str("WBWx_xxxx_x"),
    0x069: MapTile.from_str("WBBx_xxxx_x"),
    0x085: MapTile.from_str("DBWW_xxxx_x"),
    0x086: MapTile.from_str("xBDx_xxxx_x"),
    0x088: MapTile.from_str("xBWx_xxxx_x"),
    0x089: MapTile.from_str("xBBx_xxxx_x"),
    0x00A: MapTile.from_str("WGxx_xxxx_x"),
    0x00B: MapTile.from_str("DGxx_xxxx_x"),
    0x00C: MapTile.from_str("DGxx_xxxC_x"),
    0x00D: MapTile.from_str("DGGD_xxxx_x"),
    0x00E: MapTile.from_str("DGGx_xxxx_x"),
    0x02A: MapTile.from_str("xGxx_xxxx_x"),
    0x02B: MapTile.from_str("xGxx_xCxC_x"),
    0x02C: MapTile.from_str("DGWD_xxxx_x"),
    0x02D: MapTile.from_str("DGDx_xxxx_x"),
    0x02E: MapTile.from_str("DGGW_xxxx_x"),
    0x04A: MapTile.from_str("WGxW_xxxx_x"),
    0x04B: MapTile.from_str("DGxD_xxxx_x"),
    0x04C: MapTile.from_str("DGxW_xxxx_x"),
    0x04D: MapTile.from_str("WGWW_xxxx_x"),
    0x04E: MapTile.from_str("WGGW_xxxx_x"),
    0x06A: MapTile.from_str("DGWx_xxxx_x"),
    0x06B: MapTile.from_str("WGDx_xxxx_x"),
    0x06D: MapTile.from_str("WGWx_xxxx_x"),
    0x06E: MapTile.from_str("WGGx_xxxx_x"),
    0x08A: MapTile.from_str("DGWW_xxxx_x"),
    0x08B: MapTile.from_str("xGDx_xxxx_x"),
    0x08D: MapTile.from_str("xGWx_xxxx_x"),
    0x08E: MapTile.from_str("xGGx_xxxx_x"),
    0x00F: MapTile.from_str("WRxx_xxxx_x"),
    0x010: MapTile.from_str("DRxx_xxxx_x"),
    0x011: MapTile.from_str("DRxx_xxxC_x"),
    0x012: MapTile.from_str("DRRD_xxxx_x"),
    0x013: MapTile.from_str("DRRx_xxxx_x"),
    0x02F: MapTile.from_str("xRxx_xxxx_x"),
    0x030: MapTile.from_str("xRxx_xCxC_x"),
    0x031: MapTile.from_str("DRWD_xxxx_x"),
    0x032: MapTile.from_str("DRDx_xxxx_x"),
    0x033: MapTile.from_str("DRRW_xxxx_x"),
    0x04F: MapTile.from_str("WRxW_xxxx_x"),
    0x050: MapTile.from_str("DRxD_xxxx_x"),
    0x051: MapTile.from_str("DRxW_xxxx_x"),
    0x052: MapTile.from_str("WRWW_xxxx_x"),
    0x053: MapTile.from_str("WRRW_xxxx_x"),
    0x06F: MapTile.from_str("DRWx_xxxx_x"),
    0x070: MapTile.from_str("WRDx_xxxx_x"),
    0x072: MapTile.from_str("WRWx_xxxx_x"),
    0x073: MapTile.from_str("WRRx_xxxx_x"),
    0x08F: MapTile.from_str("DRWW_xxxx_x"),
    0x090: MapTile.from_str("xRDx_xxxx_x"),
    0x092: MapTile.from_str("xRWx_xxxx_x"),
    0x093: MapTile.from_str("xRRx_xxxx_x"),
    0x014: MapTile.from_str("WYxx_xxxx_x"),
    0x015: MapTile.from_str("DYxx_xxxx_x"),
    0x016: MapTile.from_str("DYxx_xxxC_x"),
    0x017: MapTile.from_str("DYYD_xxxx_x"),
    0x018: MapTile.from_str("DYYx_xxxx_x"),
    0x034: MapTile.from_str("xYxx_xxxx_x"),
    0x035: MapTile.from_str("xYxx_xCxC_x"),
    0x036: MapTile.from_str("DYWD_xxxx_x"),
    0x037: MapTile.from_str("DYDx_xxxx_x"),
    0x038: MapTile.from_str("DYYW_xxxx_x"),
    0x054: MapTile.from_str("WYxW_xxxx_x"),
    0x055: MapTile.from_str("DYxD_xxxx_x"),
    0x056: MapTile.from_str("DYxW_xxxx_x"),
    0x057: MapTile.from_str("WYWW_xxxx_x"),
    0x058: MapTile.from_str("WYYW_xxxx_x"),
    0x074: MapTile.from_str("DYWx_xxxx_x"),
    0x075: MapTile.from_str("WYDx_xxxx_x"),
    0x077: MapTile.from_str("WYWx_xxxx_x"),
    0x078: MapTile.from_str("WYYx_xxxx_x"),
    0x094: MapTile.from_str("DYWW_xxxx_x"),
    0x095: MapTile.from_str("xYDx_xxxx_x"),
    0x097: MapTile.from_str("xYWx_xxxx_x"),
    0x098: MapTile.from_str("xYYx_xxxx_x"),
    0x019: MapTile.from_str("DBGx_xxxx_x"),
    0x01A: MapTile.from_str("DBRx_xxxx_x"),
    0x01B: MapTile.from_str("DBYx_xxxx_x"),
    0x01C: MapTile.from_str("DGRx_xxxx_x"),
    0x01D: MapTile.from_str("DGYx_xxxx_x"),
    0x01E: MapTile.from_str("DRYx_xxxx_x"),
    0x039: MapTile.from_str("DBGW_xxxx_x"),
    0x03A: MapTile.from_str("DBRW_xxxx_x"),
    0x03B: MapTile.from_str("DBYW_xxxx_x"),
    0x03C: MapTile.from_str("DGRW_xxxx_x"),
    0x03D: MapTile.from_str("DGYW_xxxx_x"),
    0x03E: MapTile.from_str("DRYW_xxxx_x"),
    0x059: MapTile.from_str("WBGW_xxxx_x"),
    0x05A: MapTile.from_str("WBRW_xxxx_x"),
    0x05B: MapTile.from_str("WBYW_xxxx_x"),
    0x05C: MapTile.from_str("WGRW_xxxx_x"),
    0x05D: MapTile.from_str("WGYW_xxxx_x"),
    0x05E: MapTile.from_str("WRYW_xxxx_x"),
    0x079: MapTile.from_str("WBGx_xxxx_x"),
    0x07A: MapTile.from_str("WBRx_xxxx_x"),
    0x07B: MapTile.from_str("WBYx_xxxx_x"),
    0x07C: MapTile.from_str("WGRx_xxxx_x"),
    0x07D: MapTile.from_str("WGYx_xxxx_x"),
    0x07E: MapTile.from_str("WRYx_xxxx_x"),
    0x099: MapTile.from_str("xBGx_xxxx_x"),
    0x09A: MapTile.from_str("xBRx_xxxx_x"),
    0x09B: MapTile.from_str("xBYx_xxxx_x"),
    0x09C: MapTile.from_str("xGRx_xxxx_x"),
    0x09D: MapTile.from_str("xGYx_xxxx_x"),
    0x09E: MapTile.from_str("xRYx_xxxx_x"),
    0x01F: MapTile.from_str("DBGD_xxxx_x"),
    0x03F: MapTile.from_str("DBRD_xxxx_x"),
    0x05F: MapTile.from_str("DBYD_xxxx_x"),
    0x07F: MapTile.from_str("DGRD_xxxx_x"),
    0x09F: MapTile.from_str("DGYD_xxxx_x"),
    0x096: MapTile.from_str("DRYD_xxxx_x"),
    0x0E6: MapTile.from_str("WDBW_xxxx_x"),
    0x0E7: MapTile.from_str("DDBW_xxxx_x"),
    0x0E8: MapTile.from_str("DDBD_xxxx_x"),
    0x0EA: MapTile.from_str("DGxx_xxxC_x"),
    0x0EB: MapTile.from_str("WDGW_xxxx_x"),
    0x0EC: MapTile.from_str("DDGW_xxxx_x"),
    0x0ED: MapTile.from_str("DDGD_xxxx_x"),
    0x0EF: MapTile.from_str("DRxx_xxxC_x"),
    0x0F0: MapTile.from_str("WDRW_xxxx_x"),
    0x0F1: MapTile.from_str("DDRW_xxxx_x"),
    0x0F2: MapTile.from_str("DDRD_xxxx_x"),
    0x0F4: MapTile.from_str("DYxx_xxxC_x"),
    0x0F5: MapTile.from_str("WDYW_xxxx_x"),
    0x0F6: MapTile.from_str("DDYW_xxxx_x"),
    0x0F7: MapTile.from_str("DDYD_xxxx_x"),
    0x0F8: MapTile.from_str("WYxx_xxxC_x"),
    0x06C: MapTile.from_str("WGxx_xxxC_x"),
    0x140: MapTile.from_str("WBWW_xxxx_R"),
    0x141: MapTile.from_str("WWBW_xxxx_R"),
    0x142: MapTile.from_str("WBBW_xxxx_R"),
    0x14C: MapTile.from_str("WBWW_xxxx_N"),
    0x14D: MapTile.from_str("WWBW_xxxx_N"),
    0x14E: MapTile.from_str("WBBW_xxxx_N"),
    0x160: MapTile.from_str("WBWW_xxxx_D"),
    0x161: MapTile.from_str("WWBW_xxxx_D"),
    0x162: MapTile.from_str("WBBW_xxxx_D"),
    0x143: MapTile.from_str("WGWW_xxxx_R"),
    0x144: MapTile.from_str("WWGW_xxxx_R"),
    0x145: MapTile.from_str("WGGW_xxxx_R"),
    0x14F: MapTile.from_str("WGWW_xxxx_N"),
    0x150: MapTile.from_str("WWGW_xxxx_N"),
    0x151: MapTile.from_str("WGGW_xxxx_N"),
    0x163: MapTile.from_str("WGWW_xxxx_D"),
    0x164: MapTile.from_str("WWGW_xxxx_D"),
    0x165: MapTile.from_str("WGGW_xxxx_D"),
    0x146: MapTile.from_str("WRWW_xxxx_R"),
    0x147: MapTile.from_str("WWRW_xxxx_R"),
    0x148: MapTile.from_str("WRRW_xxxx_R"),
    0x152: MapTile.from_str("WRWW_xxxx_N"),
    0x153: MapTile.from_str("WWRW_xxxx_N"),
    0x154: MapTile.from_str("WRRW_xxxx_N"),
    0x166: MapTile.from_str("WRWW_xxxx_D"),
    0x167: MapTile.from_str("WWRW_xxxx_D"),
    0x168: MapTile.from_str("WRRW_xxxx_D"),
    0x149: MapTile.from_str("WYWW_xxxx_R"),
    0x14A: MapTile.from_str("WWYW_xxxx_R"),
    0x14B: MapTile.from_str("WYYW_xxxx_R"),
    0x155: MapTile.from_str("WYWW_xxxx_N"),
    0x156: MapTile.from_str("WWYW_xxxx_N"),
    0x157: MapTile.from_str("WYYW_xxxx_N"),
    0x169: MapTile.from_str("WYWW_xxxx_D"),
    0x16A: MapTile.from_str("WWYW_xxxx_D"),
    0x16B: MapTile.from_str("WYYW_xxxx_D"),
    0x128: MapTile.from_str("WRDW_xxxx_R"),
    0x15E: MapTile.from_str("WDYW_xxxx_R"),
    0x17E: MapTile.from_str("WRRW_xxxx_S"),
    0x17F: MapTile.from_str("WYDW_xxxx_S"),
    0x198: MapTile.from_str("WBWW_xxxx_I"),
    0x199: MapTile.from_str("WBWW_xxxx_O"),
    0x19E: MapTile.from_str("WGWW_xxxx_I"),
    0x19F: MapTile.from_str("WGWW_xxxx_O"),
    0x1AC: MapTile.from_str("WYYW_xxxx_I"),
    0x1AD: MapTile.from_str("WYYW_xxxx_O"),
    # New Tiles
    0x10B: MapTile.from_str("xxGW_Cxxx_B"),
    0x16C: MapTile.from_str("xWBW_xxxx_K"),
    0x16D: MapTile.from_str("WWGW_xxxx_K"),
    0x16E: MapTile.from_str("WWRW_xxxx_K"),
    0x16F: MapTile.from_str("WYDW_xxxx_K"),
    0x1AE: MapTile.from_str("WYWW_xxxx_I"),
    0x1AF: MapTile.from_str("WYWW_xxxx_O"),
}


NORMAL_DOOR_TILES = {
    0x000: MapTile.from_str("WWxx_xxxx_x"),
    0x001: MapTile.from_str("Wxxx_xxxx_x"),
    0x002: MapTile.from_str("DWxx_xxxx_x"),
    0x003: MapTile.from_str("Dxxx_xxxx_x"),
    0x004: MapTile.from_str("DWxx_xxxC_x"),
    0x020: MapTile.from_str("xWxx_xxxx_x"),
    0x021: MapTile.from_str("xDxx_xxxx_x"),
    0x022: MapTile.from_str("Wxxx_xxCC_x"),
    0x023: MapTile.from_str("xWxx_xCxC_x"),
    0x024: MapTile.from_str("DWWD_xxxx_x"),
    0x040: MapTile.from_str("WWxW_xxxx_x"),
    0x041: MapTile.from_str("WxxW_xxxx_x"),
    0x042: MapTile.from_str("DWxD_xxxx_x"),
    0x043: MapTile.from_str("DWxW_xxxx_x"),
    0x044: MapTile.from_str("DxxD_xxxx_x"),
    0x060: MapTile.from_str("DWWx_xxxx_x"),
    0x061: MapTile.from_str("WDWx_xxxx_x"),
    0x062: MapTile.from_str("WDDx_xxxx_x"),
    0x063: MapTile.from_str("WWWx_xxxx_x"),
    0x064: MapTile.from_str("DxxW_xxxx_x"),
    0x080: MapTile.from_str("DWWW_xxxx_x"),
    0x081: MapTile.from_str("xDWx_xxxx_x"),
    0x082: MapTile.from_str("xDDx_xxxx_x"),
    0x083: MapTile.from_str("xWWx_xxxx_x"),
    0x084: MapTile.from_str("WDDW_xxxx_x"),
    0x087: MapTile.from_str("WWWW_xxxx_x"),
    0x0B4: MapTile.from_str("WSDW_xxxx_I"),
    0x0B6: MapTile.from_str("WSDW_xxxx_x"),
    0x0E0: MapTile.from_str("DDxW_xxxx_x"),
    0x0E1: MapTile.from_str("DDxD_xxxx_x"),
    0x0E2: MapTile.from_str("DDWx_xxxx_x"),
    0x0E3: MapTile.from_str("DDDx_xxxx_x"),
    0x0E4: MapTile.from_str("WWxx_xxxC_x"),
    0x0E5: MapTile.from_str("xWxx_xxxC_x"),
    0x100: MapTile.from_str("Dxxx_xxCC_x"),
    0x101: MapTile.from_str("xDxx_xCxC_x"),
    0x102: MapTile.from_str("DDxx_xxxC_x"),
    0x104: MapTile.from_str("WDxx_xxxC_x"),
    0x105: MapTile.from_str("xDxx_xCxx_x"),
    0x108: MapTile.from_str("xxDW_xxxx_B"),
    0x109: MapTile.from_str("WDxW_xxxx_B"),
    0x10D: MapTile.from_str("xxDx_xxxx_B"),
    0x10F: MapTile.from_str("xDxW_xxxx_B"),
    0x120: MapTile.from_str("DDWW_xxxx_x"),
    0x121: MapTile.from_str("DDDW_xxxx_x"),
    0x122: MapTile.from_str("DDWD_xxxx_x"),
    0x123: MapTile.from_str("DDDD_xxxx_x"),
    0x124: MapTile.from_str("WDWW_xxxx_x"),
    0x125: MapTile.from_str("WDxx_xxxx_x"),
    0x126: MapTile.from_str("xxxx_xxxx_x"),
    0x127: MapTile.from_str("Wxxx_xxxC_x"),
    0x129: MapTile.from_str("WDxW_xxxx_P"),
    0x12A: MapTile.from_str("WxWW_xxxx_G"),
    0x12B: MapTile.from_str("WDxW_xxxx_x"),
    0x12C: MapTile.from_str("DDxx_xxxx_x"),
    0x138: MapTile.from_str("WDWW_xxxx_H"),
    0x139: MapTile.from_str("WWDW_xxxx_H"),
    0x13A: MapTile.from_str("WDDW_xxxx_H"),
    0x158: MapTile.from_str("WDWW_xxxx_R"),
    0x159: MapTile.from_str("WWDW_xxxx_R"),
    0x15A: MapTile.from_str("WDDW_xxxx_R"),
    0x15B: MapTile.from_str("WDWW_xxxx_D"),
    0x15C: MapTile.from_str("WWDW_xxxx_D"),
    0x15D: MapTile.from_str("WDDW_xxxx_D"),
    0x178: MapTile.from_str("WDWW_xxxx_N"),
    0x179: MapTile.from_str("WWDW_xxxx_N"),
    0x17A: MapTile.from_str("WDDW_xxxx_N"),
    0x17B: MapTile.from_str("WDWW_xxxx_S"),
    0x17C: MapTile.from_str("WWDW_xxxx_S"),
    0x17D: MapTile.from_str("WDDW_xxxx_S"),
    0x180: MapTile.from_str("WDWW_xxxx_I"),
    0x181: MapTile.from_str("WDWW_xxxx_O"),
    0x182: MapTile.from_str("WWxW_xxxx_I"),
    0x183: MapTile.from_str("WWxW_xxxx_O"),
    0x184: MapTile.from_str("WDDW_xxxx_I"),
    0x185: MapTile.from_str("WDDW_xxxx_O"),
    0x186: MapTile.from_str("WWxx_xxxx_I"),
    0x187: MapTile.from_str("WWxx_xxxx_O"),
    0x188: MapTile.from_str("WDxW_xxxx_I"),
    0x189: MapTile.from_str("WDxW_xxxx_O"),
    0x18A: MapTile.from_str("xWxx_xxxx_I"),
    0x18B: MapTile.from_str("xWxx_xxxx_O"),
    0x18C: MapTile.from_str("xDxx_xxxx_I"),
    0x18D: MapTile.from_str("xDxx_xxxx_O"),
    0x18E: MapTile.from_str("WDxx_xxxx_I"),
    0x18F: MapTile.from_str("WDxx_xxxx_O"),
    0x190: MapTile.from_str("Wxxx_xxxx_I"),
    0x191: MapTile.from_str("Wxxx_xxxx_O"),
    0x192: MapTile.from_str("WxxW_xxxx_I"),
    0x193: MapTile.from_str("WxxW_xxxx_O"),
    0x194: MapTile.from_str("WWWx_xxxx_I"),
    0x195: MapTile.from_str("WWWx_xxxx_O"),
    0x196: MapTile.from_str("DDDW_xxxx_I"),
    0x197: MapTile.from_str("DDDW_xxxx_O"),
    0x19A: MapTile.from_str("xDDW_xxxx_I"),
    0x19B: MapTile.from_str("xDDW_xxxx_O"),
    0x19C: MapTile.from_str("WWDx_xxxx_I"),
    0x19D: MapTile.from_str("WWDx_xxxx_O"),
    0x1A0: MapTile.from_str("xWWD_xxxx_I"),
    0x1A1: MapTile.from_str("xWWD_xxxx_O"),
    0x1A2: MapTile.from_str("WWWD_xxxx_I"),
    0x1A3: MapTile.from_str("WWWD_xxxx_O"),
    0x1A4: MapTile.from_str("xxxx_xxxx_I"),
    0x1A5: MapTile.from_str("xxxx_xxxx_O"),
    0x1A6: MapTile.from_str("WWxD_xxxx_I"),
    0x1A7: MapTile.from_str("WWxD_xxxx_O"),
    0x1A8: MapTile.from_str("xWWx_xxxx_I"),
    0x1A9: MapTile.from_str("xWWx_xxxx_O"),
    0x1AA: MapTile.from_str("DDWW_xxxx_I"),
    0x1AB: MapTile.from_str("DDWW_xxxx_O"),
    0x0B5: MapTile.from_str("WSDW_xxxx_O"),
    # New Tiles
    0x0A4: MapTile.from_str("WDxW_xxxx_T"),
    0x0D4: MapTile.from_str("WSDW_xxxx_I"),
    0x0D5: MapTile.from_str("WSDW_xxxx_O"),
    0x10A: MapTile.from_str("WxDx_xxxx_B"),
    0x10C: MapTile.from_str("xDxW_xCxx_B"),
    0x170: MapTile.from_str("WWDx_xxxx_x"),
    0x172: MapTile.from_str("WDDW_xxxx_X"),
}

COLORED_DOOR_TILE_IDS = {tile: id for id, tile in COLORED_DOOR_TILES.items()}
NORMAL_DOOR_TILE_IDS = {tile: id for id, tile in NORMAL_DOOR_TILES.items()}

ALL_DOOR_TILES = COLORED_DOOR_TILES | NORMAL_DOOR_TILES
ALL_DOOR_TILE_IDS = COLORED_DOOR_TILE_IDS | NORMAL_DOOR_TILE_IDS
