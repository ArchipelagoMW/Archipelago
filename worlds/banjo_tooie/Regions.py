import copy
import typing
from BaseClasses import Region
from worlds.banjo_tooie.Options import VictoryCondition

from .Names import regionName, locationName, itemName
from .Locations import BanjoTooieLocation
from .Rules import BanjoTooieRules

# This dict contains all the regions, as well as all the locations that are always tracked by Archipelago.
BANJOTOOIEREGIONS: typing.Dict[str, typing.List[str]] = {
    "Menu":              [],
    regionName.SM:       [
        locationName.CHEATOSM1,
        locationName.JINJOIH5,
        locationName.PMEGG,
        locationName.BMEGG,
        locationName.ROYSTEN1,
        locationName.ROYSTEN2
    ],
    regionName.SMGL:     [],
    regionName.IOHJV:    [
        locationName.JIGGYIH1,
        locationName.JIGGYIH2,
        locationName.JIGGYIH3,
        locationName.JIGGYIH4,
        locationName.JIGGYIH5,
        locationName.JIGGYIH6,
        locationName.JIGGYIH7,
        locationName.JIGGYIH8,
        locationName.JIGGYIH9,
        locationName.JIGGYIH10,
        locationName.TREBLEJV,
        locationName.IKEY,
        locationName.GOGGLES
    ],
    regionName.IOHWH:    [
        locationName.JINJOIH1,
        locationName.YMEGGH,
        locationName.PMEGGH,
        locationName.BMEGGH,

        locationName.W1,
        locationName.W2,
        locationName.W3,
        locationName.W4,
        locationName.W5,
        locationName.W6,
        locationName.W7,
        locationName.W8,
        locationName.W9
    ],
    regionName.MT:       [
        locationName.JIGGYGM6,
        locationName.JINJOMT1,
        locationName.JINJOMT2,
        locationName.JINJOMT3,
        locationName.JINJOMT4,
        locationName.JINJOMT5,
        locationName.JIGGYMT1,
        locationName.JIGGYMT2,
        locationName.JIGGYMT3,
        locationName.JIGGYMT4,
        locationName.JIGGYMT5,
        locationName.JIGGYMT6,
        locationName.JIGGYMT7,
        locationName.JIGGYMT8,
        locationName.JIGGYMT9,
        locationName.JIGGYMT10,
        locationName.GLOWBOMT1,
        locationName.GLOWBOMT2,
        locationName.HONEYCMT1,
        locationName.HONEYCMT2,
        locationName.HONEYCMT3,
        locationName.CHEATOMT1,
        locationName.CHEATOMT2,
        locationName.CHEATOMT3,
        locationName.GGRAB,
        locationName.BBLASTER,
        locationName.EGGAIM,
        locationName.TREBLEMT,
        locationName.NOTEMT1,
        locationName.NOTEMT2,
        locationName.NOTEMT3,
        locationName.NOTEMT4,
        locationName.NOTEMT5,
        locationName.NOTEMT6,
        locationName.NOTEMT7,
        locationName.NOTEMT8,
        locationName.NOTEMT9,
        locationName.NOTEMT10,
        locationName.NOTEMT11,
        locationName.NOTEMT12,
        locationName.NOTEMT13,
        locationName.NOTEMT14,
        locationName.NOTEMT15,
        locationName.NOTEMT16
    ],
    regionName.IOHPL:    [
        locationName.JINJOIH4,
        locationName.HONEYCIH1,
        locationName.FEGGS,
        locationName.NOTEIH1,
        locationName.NOTEIH2,
        locationName.NOTEIH3,
        locationName.NOTEIH4,
    ],
    regionName.GM:       [
        # locationName.JINJOGM1, moved to GMWSJT
        locationName.JINJOGM2,
        locationName.JINJOGM3,
        locationName.JINJOGM4,
        locationName.JINJOGM5,
        locationName.JIGGYGM2,
        locationName.JIGGYGM3,
        locationName.JIGGYGM4,
        locationName.JIGGYGM5,
        # locationName.JIGGYGM6, in MT
        locationName.JIGGYGM7,
        locationName.JIGGYGM8,
        locationName.JIGGYGM9,
        locationName.JIGGYGM10,
        locationName.GLOWBOGM1,
        locationName.GLOWBOGM2,
        locationName.GLOWBOMEG,
        locationName.HONEYCGM1,
        locationName.HONEYCGM2,
        locationName.HONEYCGM3,
        locationName.CHEATOGM1,
        locationName.CHEATOGM2,
        locationName.CHEATOGM3,
        locationName.BDRILL,
        locationName.BBAYONET,
        locationName.TREBLEGM,
        locationName.NOTEGGM1,
        locationName.NOTEGGM2,
        locationName.NOTEGGM3,
        locationName.NOTEGGM4,
        locationName.NOTEGGM5,
        locationName.NOTEGGM6,
        locationName.NOTEGGM7,
        locationName.NOTEGGM8,
        locationName.NOTEGGM9,
        locationName.NOTEGGM10,
        locationName.NOTEGGM11,
        locationName.NOTEGGM12,
        locationName.NOTEGGM13,
        locationName.NOTEGGM14,
        locationName.NOTEGGM15,
        locationName.NOTEGGM16,
        locationName.CHUNK1,
        locationName.CHUNK2,
        locationName.CHUNK3,
    ],
    regionName.GMWSJT: [
        locationName.JINJOGM1,
    ],
    regionName.GMFD: [],
    regionName.CHUFFY:
    [
        locationName.JIGGYGM1,
        locationName.CHUFFY

    ],
    regionName.IOHPG:   [
        locationName.GEGGS,
        locationName.NOTEIH5,
        locationName.NOTEIH6,
    ],
    regionName.IOHPGU:   [
        locationName.NOTEIH7,
        locationName.NOTEIH8,
    ],
    regionName.WW:      [
        locationName.JINJOWW1,
        locationName.JINJOWW2,
        locationName.JINJOWW3,
        locationName.JINJOWW4,
        locationName.JINJOWW5,
        locationName.JIGGYWW1,
        locationName.JIGGYWW2,
        locationName.JIGGYWW3,
        locationName.JIGGYWW4,
        locationName.JIGGYWW5,
        locationName.JIGGYWW6,
        locationName.JIGGYWW7,
        locationName.JIGGYWW8,
        locationName.JIGGYWW9,
        locationName.JIGGYWW10,
        locationName.GLOWBOWW1,
        locationName.GLOWBOWW2,
        locationName.HONEYCWW1,
        locationName.HONEYCWW2,
        locationName.HONEYCWW3,
        locationName.CHEATOWW1,
        locationName.CHEATOWW2,
        locationName.CHEATOWW3,
        locationName.AIREAIM,
        locationName.SPLITUP,
        locationName.PACKWH,
        locationName.TREBLEWW,
        locationName.TRAINSWWW,
        locationName.NOTEWW1,
        locationName.NOTEWW2,
        locationName.NOTEWW3,
        locationName.NOTEWW4,
        locationName.NOTEWW5,
        locationName.NOTEWW6,
        locationName.NOTEWW7,
        locationName.NOTEWW8,
        locationName.NOTEWW9,
        locationName.NOTEWW10,
        locationName.NOTEWW11,
        locationName.NOTEWW12,
        locationName.NOTEWW13,
        locationName.NOTEWW14,
        locationName.NOTEWW15,
        locationName.NOTEWW16
    ],
    regionName.WWA51NESTS:   [],
    regionName.IOHCT:   [
        locationName.JINJOIH3,
        locationName.IEGGS,
        locationName.TRAINSWIH,

    ],
    regionName.IOHCT_HFP_ENTRANCE: [
        locationName.GLOWBOIH1,
        locationName.NOTEIH9,
        locationName.NOTEIH10,
        locationName.NOTEIH11,
        locationName.NOTEIH12,
    ],
    regionName.JR:      [
        locationName.JRLDB1,
        locationName.JRLDB2,
        locationName.JRLDB3,
        locationName.JRLDB4,
        locationName.JRLDB5,
        locationName.JRLDB6,
        locationName.JRLDB7,
        locationName.JRLDB8,
        locationName.JRLDB9,
        locationName.JRLDB10,
        locationName.JRLDB11,
        locationName.JRLDB12,
        locationName.JRLDB13,
        locationName.JRLDB14,
        locationName.JRLDB15,
        locationName.JRLDB16,
        locationName.JRLDB17,
        locationName.JRLDB18,
        locationName.JRLDB19,
        locationName.JRLDB20,
        locationName.JRLDB21,
        locationName.JRLDB22,
        locationName.JRLDB23,
        locationName.JRLDB24,
        locationName.JRLDB25,
        locationName.JRLDB26,
        locationName.JRLDB27,
        locationName.JRLDB28,
        locationName.JRLDB29,
        locationName.JRLDB30,
        locationName.JINJOJR1,
        locationName.JINJOJR2,
        locationName.JIGGYJR2,
        locationName.JIGGYJR4,
        locationName.JIGGYJR5,
        locationName.JIGGYJR9,
        locationName.GLOWBOJR1,
        locationName.HONEYCJR3,
        locationName.CHEATOJR1,
        locationName.WWHACK,
        locationName.AUQAIM,
        locationName.NOTEJRL1,
        locationName.NOTEJRL2,
        locationName.NOTEJRL3,
        locationName.NOTEJRL8,
        locationName.NOTEJRL9,
        locationName.NOTEJRL10,
        locationName.NOTEJRL11,
        locationName.NOTEJRL12,
        locationName.NOTEJRL13,
        locationName.NOTEJRL14,
        locationName.NOTEJRL15,
        locationName.NOTEJRL16
    ],
    regionName.JRU: [
        locationName.JINJOGI3,
        locationName.JIGGYJR10,
        locationName.CHEATOJR2,
        locationName.NOTEJRL4,
        locationName.NOTEJRL5,
    ],
    regionName.JRU2: [
        locationName.JINJOJR3,
        locationName.JINJOJR4,
        locationName.JINJOJR5,
        locationName.JIGGYJR1,
        locationName.JIGGYJR3,
        locationName.JIGGYJR6,
        locationName.JIGGYJR7,
        locationName.JIGGYJR8,
        locationName.GLOWBOJR2,
        locationName.HONEYCJR1,
        locationName.HONEYCJR2,
        locationName.CHEATOJR3,
        locationName.TTORP,
        locationName.TREBLEJR,
        locationName.NOTEJRL6,
        locationName.NOTEJRL7,
    ],
    regionName.IOHWL:   [
        locationName.JINJOIH2,
        locationName.CEGGS,
        locationName.NOTEIH13,
        locationName.NOTEIH14,
        locationName.NOTEIH15,
        locationName.NOTEIH16,
    ],
    regionName.TL:      [
        locationName.JINJOTL1,
        locationName.JINJOTL2,
        locationName.JINJOTL3,
        locationName.JINJOTL4,
        locationName.JINJOTL5,
        locationName.JIGGYTD1,
        #locationName.JIGGYTD2, #In CCL
        locationName.JIGGYTD3,
        locationName.JIGGYTD4,
        locationName.JIGGYTD5,
        locationName.JIGGYTD6,
        locationName.JIGGYTD7,
        locationName.JIGGYTD8,
        locationName.JIGGYTD9,
        locationName.JIGGYTD10,
        locationName.JIGGYHP7,
        locationName.GLOWBOTL1,
        locationName.GLOWBOTL2,
        locationName.HONEYCTL1,
        locationName.HONEYCTL2,
        locationName.HONEYCTL3,
        locationName.CHEATOTL1,
        locationName.CHEATOTL2,
        locationName.CHEATOTL3,
        locationName.SPRINGB,
        locationName.TAXPACK,
        locationName.TREBLETL,
        locationName.TRAINSWTD,
        locationName.NOTETDL1,
        locationName.NOTETDL2,
        locationName.NOTETDL3,
        locationName.NOTETDL4,
        locationName.NOTETDL5,
        locationName.NOTETDL6,
        locationName.NOTETDL7,
        locationName.NOTETDL8,
        locationName.NOTETDL9,
        locationName.NOTETDL10,
        locationName.NOTETDL11,
        locationName.NOTETDL12,
        locationName.NOTETDL13,
        locationName.NOTETDL14,
        locationName.NOTETDL15,
        locationName.NOTETDL16,
        locationName.SCRUT,
        locationName.SCRAT,
        locationName.SCRIT,
        locationName.ROARDINO
    ],
    regionName.TL_HATCH: [
        locationName.HATCH,
    ],
    regionName.IOHQM:   [],
    regionName.GIO: [
        locationName.TREBLEGI,
    ],
    regionName.GIOB: [
        locationName.TRAINSWGI,
        locationName.JINJOGI5,
    ],
    regionName.GIES: [],
    regionName.GI1: [
        # locationName.JINJOGI3, Moved to JRL
        locationName.JIGGYGI1,
        locationName.JIGGYGI2,
        locationName.JIGGYGI7,
        locationName.JIGGYGI8,
        locationName.JIGGYGI10,
        locationName.CHEATOGI1,
        locationName.CHEATOGI3,
        locationName.HONEYCGI2,
        locationName.SNPACK,
        locationName.CLAWBTS,
        locationName.NOTEGI4,
        locationName.NOTEGI5,
        locationName.NOTEGI1,
        locationName.NOTEGI2,
        locationName.NOTEGI3,
        locationName.NOTEGI11,
        locationName.NOTEGI12,
        locationName.NOTEGI13,
        locationName.NOTEGI14,
    ],
    regionName.GI2: [
        locationName.CHEATOGI2,
        locationName.GLOWBOGI1,
        locationName.LSPRING,
        locationName.JINJOGI2,
        locationName.JIGGYGI4,
        locationName.NOTEGI6,
        locationName.NOTEGI7,
        locationName.NOTEGI8,
        locationName.NOTEGI9,
        locationName.NOTEGI10,
    ],
    regionName.GI2EM: [],
    regionName.GI3: [
        locationName.HONEYCGI1,
        locationName.GLOWBOGI2,
        locationName.NOTEGI15,
        locationName.NOTEGI16,
    ],
    regionName.GI3B: [
        locationName.JINJOGI4,
        locationName.JIGGYGI9,
    ],
    regionName.GI4: [],
    regionName.GI4B: [
        locationName.JIGGYGI3,
        locationName.JIGGYGI6,
    ],
    regionName.GI5: [
        locationName.JINJOGI1,
        locationName.JIGGYGI5,
        locationName.HONEYCGI3,
    ],
    regionName.HP: [
        locationName.JINJOHP1,
        locationName.JINJOHP2,
        locationName.JINJOHP3,
        locationName.JINJOHP4,
        locationName.JINJOHP5,
        locationName.JIGGYHP1,
        locationName.JIGGYHP2,
        locationName.JIGGYHP3,
        locationName.JIGGYHP4,
        locationName.JIGGYHP5,
        locationName.JIGGYHP6,
        #locationName.JIGGYHP7, # in TDL
        locationName.JIGGYHP8,
        locationName.JIGGYHP9,
        locationName.JIGGYHP10,
        locationName.GLOWBOHP1,
        locationName.GLOWBOHP2,
        locationName.HONEYCHP1,
        locationName.HONEYCHP2,
        locationName.HONEYCHP3,
        locationName.CHEATOHP1,
        locationName.CHEATOHP2,
        locationName.CHEATOHP3,
        locationName.SHPACK,
        locationName.GLIDE,
        locationName.TREBLEHP,
        locationName.TRAINSWHP1,
        locationName.TRAINSWHP2,
        locationName.NOTEHFP1,
        locationName.NOTEHFP2,
        locationName.NOTEHFP3,
        locationName.NOTEHFP4,
        locationName.NOTEHFP5,
        locationName.NOTEHFP6,
        locationName.NOTEHFP7,
        locationName.NOTEHFP8,
        locationName.NOTEHFP9,
        locationName.NOTEHFP10,
        locationName.NOTEHFP11,
        locationName.NOTEHFP12,
        locationName.NOTEHFP13,
        locationName.NOTEHFP14,
        locationName.NOTEHFP15,
        locationName.NOTEHFP16
    ],
    regionName.CC:      [
        locationName.JINJOCC1,
        locationName.JINJOCC2,
        locationName.JINJOCC3,
        locationName.JINJOCC4,
        locationName.JINJOCC5,
        locationName.JIGGYCC1,
        locationName.JIGGYCC2,
        locationName.JIGGYCC3,
        locationName.JIGGYCC4,
        locationName.JIGGYCC5,
        locationName.JIGGYCC6,
        locationName.JIGGYCC7,
        locationName.JIGGYCC8,
        locationName.JIGGYCC9,
        locationName.JIGGYCC10,
        locationName.JIGGYTD2,
        locationName.GLOWBOCC1,
        locationName.GLOWBOCC2,
        locationName.HONEYCCC1,
        locationName.HONEYCCC2,
        locationName.HONEYCCC3,
        locationName.CHEATOCC1,
        locationName.CHEATOCC2,
        locationName.CHEATOCC3,
        locationName.SAPACK,
        locationName.TREBLECC,
        locationName.NOTECCL1,
        locationName.NOTECCL2,
        locationName.NOTECCL3,
        locationName.NOTECCL4,
        locationName.NOTECCL5,
        locationName.NOTECCL6,
        locationName.NOTECCL7,
        locationName.NOTECCL8,
        locationName.NOTECCL9,
        locationName.NOTECCL10,
        locationName.NOTECCL11,
        locationName.NOTECCL12,
        locationName.NOTECCL13,
        locationName.NOTECCL14,
        locationName.NOTECCL15,
        locationName.NOTECCL16
    ],
    regionName.CK: [],
    regionName.H1: [
        locationName.HAG1
    ],
    regionName.MTE: [],
    regionName.GGME: [],
    regionName.WWE: [],
    regionName.JRLE: [],
    regionName.TDLE: [],
    regionName.GIE: [],
    regionName.HFPE: [],
    regionName.CCLE: [],
    regionName.CKE: [],
}

#Regions for nests. Regions that don't contain anything are omitted.
NEST_REGIONS: typing.Dict[str, typing.List[str]] = {
    "Menu":              [],
    regionName.SM:       [
      locationName.NESTSM8,
      locationName.NESTSM9,
      locationName.NESTSM10,
      locationName.NESTSM11,
      locationName.NESTSM12,
      locationName.NESTSM13,
      locationName.NESTSM14,
      locationName.NESTSM15,
      locationName.NESTSM16,
      locationName.NESTSM17,
      locationName.NESTSM18,
      locationName.NESTSM19,
      locationName.NESTSM20,
      locationName.NESTSM21,
      locationName.NESTSM22,
      locationName.NESTSM23,
      locationName.NESTSM24,
      locationName.NESTSM25,
    ],
    regionName.SMGL:     [
      locationName.NESTSM1,
      locationName.NESTSM2,
      locationName.NESTSM3,
      locationName.NESTSM4,
      locationName.NESTSM5,
      locationName.NESTSM6,
      locationName.NESTSM7,
    ],
    regionName.IOHJV:    [
      locationName.NESTIH1,
      locationName.NESTIH2,
      locationName.NESTIH3,
      locationName.NESTIH4,
      locationName.NESTIH5,
      locationName.NESTIH6,
      locationName.NESTIH7,
      locationName.NESTIH8,
      locationName.NESTIH9,
      locationName.NESTIH10,
      locationName.NESTIH11,
      locationName.NESTIH12,
      locationName.NESTIH13,
    ],
    regionName.IOHWH:    [
      locationName.NESTIH14,
      locationName.NESTIH15,
      locationName.NESTIH16,
      locationName.NESTIH17,
      locationName.NESTIH18,
      locationName.NESTIH19,
      locationName.NESTIH20,
      locationName.NESTIH21,
      locationName.NESTIH22,
      locationName.NESTIH23,
      locationName.NESTIH24,
      locationName.NESTIH25,
      locationName.NESTIH26,
    ],
    regionName.MT:       [
      locationName.NESTMT1,
      locationName.NESTMT2,
      locationName.NESTMT3,
      locationName.NESTMT4,
      locationName.NESTMT5,
      locationName.NESTMT6,
      locationName.NESTMT7,
      locationName.NESTMT8,
      locationName.NESTMT9,
      locationName.NESTMT10,
      locationName.NESTMT11,
      locationName.NESTMT12,
      locationName.NESTMT13,
      locationName.NESTMT14,
      locationName.NESTMT15,
      locationName.NESTMT16,
      locationName.NESTMT17,
      locationName.NESTMT18,
      locationName.NESTMT19,
      locationName.NESTMT20,
      locationName.NESTMT21,
      locationName.NESTMT22,
      locationName.NESTMT23,
      locationName.NESTMT24,
      locationName.NESTMT25,
      locationName.NESTMT26,
      locationName.NESTMT27,
      locationName.NESTMT28,
      locationName.NESTMT29,
      locationName.NESTMT30,
      locationName.NESTMT31,
      locationName.NESTMT32,
      locationName.NESTMT33,
      locationName.NESTMT34,
      locationName.NESTMT35,
      locationName.NESTMT36,
      locationName.NESTMT37,
      locationName.NESTMT38,
      locationName.NESTMT39,
      locationName.NESTMT40,
      locationName.NESTMT41,
    ],
    regionName.IOHPL:    [
      locationName.NESTIH27,
      locationName.NESTIH28,
      locationName.NESTIH29,
      locationName.NESTIH30,
      locationName.NESTIH31,
      locationName.NESTIH32,
      locationName.NESTIH33,
    ],
    regionName.GM:       [
      locationName.NESTGM1,
      locationName.NESTGM2,
      locationName.NESTGM3,
      locationName.NESTGM4,

      locationName.NESTGM11,
      locationName.NESTGM12,
      locationName.NESTGM13,
      locationName.NESTGM14,

      locationName.NESTGM16,
      locationName.NESTGM17,
      locationName.NESTGM18,
      locationName.NESTGM19,
      locationName.NESTGM20,
      locationName.NESTGM21,
      locationName.NESTGM22,
      locationName.NESTGM23,
      locationName.NESTGM24,
      locationName.NESTGM25,
      locationName.NESTGM26,
      locationName.NESTGM27,
      locationName.NESTGM28,
      locationName.NESTGM29,
      locationName.NESTGM30,
      locationName.NESTGM31,
      locationName.NESTGM32,
      locationName.NESTGM33,
      locationName.NESTGM34,
      locationName.NESTGM35,
      locationName.NESTGM36,
      locationName.NESTGM37,
      locationName.NESTGM38,
    ],
    regionName.GMFD: [
      locationName.NESTGM5,
      locationName.NESTGM6,
      locationName.NESTGM7,
      locationName.NESTGM8,
      locationName.NESTGM9,
      locationName.NESTGM10,
    ],
    regionName.GMWSJT: [
      locationName.NESTGM15,
    ],
    regionName.IOHPG:   [
      locationName.NESTIH34,
      locationName.NESTIH35,
      locationName.NESTIH36,
      locationName.NESTIH37,
      locationName.NESTIH38,
      locationName.NESTIH39,

      locationName.NESTIH46,
      locationName.NESTIH47,
    ],
    regionName.WW:      [
      locationName.NESTWW1,
      locationName.NESTWW2,
      locationName.NESTWW3,
      locationName.NESTWW4,

      locationName.NESTWW7,
      locationName.NESTWW8,
      locationName.NESTWW9,
      locationName.NESTWW10,
      locationName.NESTWW11,
      locationName.NESTWW12,
      locationName.NESTWW13,
      locationName.NESTWW14,
      locationName.NESTWW15,
      locationName.NESTWW16,
      locationName.NESTWW17,
      locationName.NESTWW18,
      locationName.NESTWW19,
      locationName.NESTWW20,
      locationName.NESTWW21,
      locationName.NESTWW22,
      locationName.NESTWW23,
      locationName.NESTWW24,
      locationName.NESTWW25,
      locationName.NESTWW26,
      locationName.NESTWW27,
      locationName.NESTWW28,
      locationName.NESTWW29,
      locationName.NESTWW30,
      locationName.NESTWW31,
      locationName.NESTWW32,
      locationName.NESTWW33,
      locationName.NESTWW34,
      locationName.NESTWW35,
      locationName.NESTWW36,
      locationName.NESTWW37,
      locationName.NESTWW38,
      locationName.NESTWW39,
      locationName.NESTWW40,
      locationName.NESTWW41,
      locationName.NESTWW42,
    ],
    regionName.WWA51NESTS:   [
      locationName.NESTWW5,
      locationName.NESTWW6,
    ],
    regionName.IOHCT:   [
      locationName.NESTIH40,
      locationName.NESTIH41,
      locationName.NESTIH42,
      locationName.NESTIH43,
      locationName.NESTIH44,
      locationName.NESTIH45,
      locationName.NESTIH64,
    ],
    regionName.JR:      [
      locationName.NESTJR1,
      locationName.NESTJR2,
      locationName.NESTJR3,
      locationName.NESTJR4,
      locationName.NESTJR5,
      locationName.NESTJR6,
      locationName.NESTJR7,
      locationName.NESTJR8,
      locationName.NESTJR9,

      locationName.NESTGI63,
      locationName.NESTGI66,
    ],
    regionName.JRU: [
      locationName.NESTJR25,
      locationName.NESTJR26,
      locationName.NESTJR27,

      locationName.NESTGI64,
      locationName.NESTGI65,
    ],
    regionName.JRU2: [
      locationName.NESTJR10,
      locationName.NESTJR11,
      locationName.NESTJR12,
      locationName.NESTJR13,
      locationName.NESTJR14,
      locationName.NESTJR15,
      locationName.NESTJR16,
      locationName.NESTJR17,
      locationName.NESTJR18,
      locationName.NESTJR19,
      locationName.NESTJR20,
      locationName.NESTJR21,
      locationName.NESTJR22,
      locationName.NESTJR23,
      locationName.NESTJR24,

      locationName.NESTJR28,
      locationName.NESTJR29,
      locationName.NESTJR30,
      locationName.NESTJR31,
      locationName.NESTJR32,
      locationName.NESTJR33,
      locationName.NESTJR34,
      locationName.NESTJR35,
      locationName.NESTJR36,
      locationName.NESTJR37,
      locationName.NESTJR38,
      locationName.NESTJR39,
      locationName.NESTJR40,
    ],
    regionName.IOHWL:   [
      locationName.NESTIH48,
      locationName.NESTIH49,
      locationName.NESTIH50,
      locationName.NESTIH51,
      locationName.NESTIH52,
      locationName.NESTIH53,
      locationName.NESTIH54,
      locationName.NESTIH55,
      locationName.NESTIH56,
      locationName.NESTIH57,
    ],
    regionName.TL:      [
      locationName.NESTTL1,
      locationName.NESTTL2,
      locationName.NESTTL3,
      locationName.NESTTL4,
      locationName.NESTTL5,
      locationName.NESTTL6,
      locationName.NESTTL7,
      locationName.NESTTL8,
      locationName.NESTTL9,
      locationName.NESTTL10,
      locationName.NESTTL11,
      locationName.NESTTL12,
      locationName.NESTTL13,
      locationName.NESTTL14,
      locationName.NESTTL15,
      locationName.NESTTL16,
      locationName.NESTTL17,
      locationName.NESTTL18,
      locationName.NESTTL19,
      locationName.NESTTL20,
      locationName.NESTTL21,
      locationName.NESTTL22,
      locationName.NESTTL23,
      locationName.NESTTL24,
      locationName.NESTTL25,
      locationName.NESTTL26,
      locationName.NESTTL27,
      locationName.NESTTL28,
      locationName.NESTTL29,
      locationName.NESTTL30,
      locationName.NESTTL31,
      locationName.NESTTL32,
      locationName.NESTTL33,
      locationName.NESTTL34,
      locationName.NESTTL35,
      locationName.NESTTL36,
      locationName.NESTTL37,
      locationName.NESTTL38,

      locationName.NESTTL45,
      locationName.NESTTL46,
      locationName.NESTTL47,
      locationName.NESTTL48,
      locationName.NESTTL49,
      locationName.NESTTL50,
      locationName.NESTTL51,
      locationName.NESTTL52,
      locationName.NESTTL53,
      locationName.NESTTL54,
      locationName.NESTTL55,
    ],
    regionName.TL_HATCH: [
      locationName.NESTTL39,
      locationName.NESTTL40,
      locationName.NESTTL41,
      locationName.NESTTL42,
      locationName.NESTTL43,
      locationName.NESTTL44,
    ],
    regionName.IOHQM:   [
      locationName.NESTIH58,
      locationName.NESTIH59,
      locationName.NESTIH60,
      locationName.NESTIH61,
      locationName.NESTIH62,
      locationName.NESTIH63,
    ],
    regionName.GIO: [
      locationName.NESTGI4,
      locationName.NESTGI5,
    ],
    regionName.GIES: [
      locationName.NESTGI19,
      locationName.NESTGI20,
      locationName.NESTGI21,
    ],
    regionName.GI1: [
      locationName.NESTGI6,
      locationName.NESTGI7,
      locationName.NESTGI8,
      locationName.NESTGI9,
      locationName.NESTGI10,
      locationName.NESTGI11,
      locationName.NESTGI12,
      locationName.NESTGI13,
      locationName.NESTGI14,
      locationName.NESTGI15,
      locationName.NESTGI16,
      locationName.NESTGI17,
      locationName.NESTGI18,

      locationName.NESTGI56,
      locationName.NESTGI57,
      locationName.NESTGI58,
      locationName.NESTGI59,
      locationName.NESTGI60,
      locationName.NESTGI61,
      locationName.NESTGI62,
    ],
    regionName.GI2: [
      locationName.NESTGI22,
      locationName.NESTGI23,
      locationName.NESTGI24,
      locationName.NESTGI25,
      locationName.NESTGI27,
      locationName.NESTGI28,
      locationName.NESTGI29,
      locationName.NESTGI30,
    ],
    regionName.GI2EM: [
      locationName.NESTGI32,
      locationName.NESTGI33,
      locationName.NESTGI34,
    ],
    regionName.GI3: [
      locationName.NESTGI35,
      locationName.NESTGI36,
      locationName.NESTGI37,
      locationName.NESTGI38,
      locationName.NESTGI39,
      locationName.NESTGI40,
    ],
    regionName.GI3B: [
      locationName.NESTGI41,
      locationName.NESTGI42,
    ],
    regionName.GI4: [
      locationName.NESTGI43,
      locationName.NESTGI44,
      locationName.NESTGI45,
      locationName.NESTGI46,
      locationName.NESTGI47,
      locationName.NESTGI48,
    ],
    regionName.GI4B: [
      locationName.NESTGI49,
      locationName.NESTGI50,
      locationName.NESTGI51,
      locationName.NESTGI52,

      locationName.NESTGI67,
      locationName.NESTGI68,
      locationName.NESTGI69,
      locationName.NESTGI70,
      locationName.NESTGI71,
      locationName.NESTGI72,
      locationName.NESTGI73,
      locationName.NESTGI74,
      locationName.NESTGI75,
      locationName.NESTGI76,
      locationName.NESTGI77,
      locationName.NESTGI78,
    ],
    regionName.GI5: [
      locationName.NESTGI1,
      locationName.NESTGI2,
      locationName.NESTGI3,

      locationName.NESTGI26,

      locationName.NESTGI31,

      locationName.NESTGI53,
      locationName.NESTGI54,
      locationName.NESTGI55,
    ],
    regionName.HP: [
      locationName.NESTHP1,
      locationName.NESTHP2,
      locationName.NESTHP3,
      locationName.NESTHP4,
      locationName.NESTHP5,
      locationName.NESTHP6,
      locationName.NESTHP7,
      locationName.NESTHP8,
      locationName.NESTHP9,
      locationName.NESTHP10,
      locationName.NESTHP11,
      locationName.NESTHP12,
      locationName.NESTHP13,
      locationName.NESTHP14,
      locationName.NESTHP15,
      locationName.NESTHP16,
      locationName.NESTHP17,
      locationName.NESTHP18,
      locationName.NESTHP19,
      locationName.NESTHP20,
      locationName.NESTHP21,
      locationName.NESTHP22,
      locationName.NESTHP23,
      locationName.NESTHP24,
      locationName.NESTHP25,
      locationName.NESTHP26,
      locationName.NESTHP27,
      locationName.NESTHP28,
      locationName.NESTHP29,
      locationName.NESTHP30,
      locationName.NESTHP31,
      locationName.NESTHP32,
      locationName.NESTHP33,
      locationName.NESTHP34,
      locationName.NESTHP35,
      locationName.NESTHP36,
      locationName.NESTHP37,
      locationName.NESTHP38,
      locationName.NESTHP39,
      locationName.NESTHP40,
    ],
    regionName.CC:      [
      locationName.NESTCC1,
      locationName.NESTCC2,
      locationName.NESTCC3,
      locationName.NESTCC4,
      locationName.NESTCC5,
      locationName.NESTCC6,
      locationName.NESTCC7,
      locationName.NESTCC8,
      locationName.NESTCC9,
      locationName.NESTCC10,
      locationName.NESTCC11,
      locationName.NESTCC12,
      locationName.NESTCC13,
      locationName.NESTCC14,
      locationName.NESTCC15,
      locationName.NESTCC16,
      locationName.NESTCC17,
      locationName.NESTCC18,
      locationName.NESTCC19,
      locationName.NESTCC20,
      locationName.NESTCC21,
      locationName.NESTCC22,
      locationName.NESTCC23,
      locationName.NESTCC24,
      locationName.NESTCC25,
      locationName.NESTCC26,
      locationName.NESTCC27,
      locationName.NESTCC28,
      locationName.NESTCC29,
      locationName.NESTCC30,
      locationName.NESTCC31,
      locationName.NESTCC32,
      locationName.NESTCC33,
      locationName.NESTCC34,
      locationName.NESTCC35,
      locationName.NESTCC36,
      locationName.NESTCC37,
      locationName.NESTCC38,
      locationName.NESTCC39,
      locationName.NESTCC40,
      locationName.NESTCC41,
      locationName.NESTCC42,
      locationName.NESTCC43,
      locationName.NESTCC44,
      locationName.NESTCC45,
      locationName.NESTCC46,
      locationName.NESTCC47,
      locationName.NESTCC48,
      locationName.NESTCC49,
      locationName.NESTCC50,
    ],
}

def create_regions(self):
    player = self.player
    active_locations = self.location_name_to_id
    region_map = copy.deepcopy(BANJOTOOIEREGIONS)
    nest_map = copy.deepcopy(NEST_REGIONS)

    if self.options.victory_condition == VictoryCondition.option_minigame_hunt\
      or self.options.victory_condition == VictoryCondition.option_wonderwing_challenge:
        region_map[regionName.MT].append(locationName.MUMBOTKNGAME1)
        region_map[regionName.GM].append(locationName.MUMBOTKNGAME2)
        region_map[regionName.WW].append(locationName.MUMBOTKNGAME3)
        region_map[regionName.WW].append(locationName.MUMBOTKNGAME4)
        region_map[regionName.WW].append(locationName.MUMBOTKNGAME5)
        region_map[regionName.WW].append(locationName.MUMBOTKNGAME6)
        region_map[regionName.JRU2].append(locationName.MUMBOTKNGAME7)
        region_map[regionName.TL].append(locationName.MUMBOTKNGAME8)
        region_map[regionName.GI4B].append(locationName.MUMBOTKNGAME9)
        region_map[regionName.GI3B].append(locationName.MUMBOTKNGAME10)
        region_map[regionName.HP].append(locationName.MUMBOTKNGAME11)
        region_map[regionName.CC].append(locationName.MUMBOTKNGAME12)
        region_map[regionName.CC].append(locationName.MUMBOTKNGAME13)
        region_map[regionName.CC].append(locationName.MUMBOTKNGAME14)
        region_map[regionName.CC].append(locationName.MUMBOTKNGAME15)

    if self.options.victory_condition == VictoryCondition.option_boss_hunt\
      or self.options.victory_condition == VictoryCondition.option_wonderwing_challenge:
        region_map[regionName.MT].append(locationName.MUMBOTKNBOSS1)
        region_map[regionName.CHUFFY].append(locationName.MUMBOTKNBOSS2)
        region_map[regionName.WW].append(locationName.MUMBOTKNBOSS3)
        region_map[regionName.JRU2].append(locationName.MUMBOTKNBOSS4)
        region_map[regionName.TL].append(locationName.MUMBOTKNBOSS5)
        region_map[regionName.GI1].append(locationName.MUMBOTKNBOSS6)
        region_map[regionName.HP].append(locationName.MUMBOTKNBOSS7)
        region_map[regionName.CC].append(locationName.MUMBOTKNBOSS8)

    if self.options.victory_condition == VictoryCondition.option_jinjo_family_rescue\
      or self.options.victory_condition == VictoryCondition.option_wonderwing_challenge:
        region_map[regionName.IOHJV].append(locationName.MUMBOTKNJINJO1)
        region_map[regionName.IOHJV].append(locationName.MUMBOTKNJINJO2)
        region_map[regionName.IOHJV].append(locationName.MUMBOTKNJINJO3)
        region_map[regionName.IOHJV].append(locationName.MUMBOTKNJINJO4)
        region_map[regionName.IOHJV].append(locationName.MUMBOTKNJINJO5)
        region_map[regionName.IOHJV].append(locationName.MUMBOTKNJINJO6)
        region_map[regionName.IOHJV].append(locationName.MUMBOTKNJINJO7)
        region_map[regionName.IOHJV].append(locationName.MUMBOTKNJINJO8)
        region_map[regionName.IOHJV].append(locationName.MUMBOTKNJINJO9)

    if self.options.cheato_rewards:
        region_map[regionName.SMGL].append(locationName.CHEATOR1)
        region_map[regionName.SMGL].append(locationName.CHEATOR2)
        region_map[regionName.SMGL].append(locationName.CHEATOR3)
        region_map[regionName.SMGL].append(locationName.CHEATOR4)
        region_map[regionName.SMGL].append(locationName.CHEATOR5)

    if self.options.honeyb_rewards:
        region_map[regionName.IOHPL].append(locationName.HONEYBR1)
        region_map[regionName.IOHPL].append(locationName.HONEYBR2)
        region_map[regionName.IOHPL].append(locationName.HONEYBR3)
        region_map[regionName.IOHPL].append(locationName.HONEYBR4)
        region_map[regionName.IOHPL].append(locationName.HONEYBR5)

    if self.options.nestsanity:
        for region, locations in nest_map.items():
            for location in locations:
                region_map[region].append(location)


    self.multiworld.regions.extend(create_region(self.multiworld, self.player,\
          active_locations, region, locations) for region, locations in region_map.items())
    if self.options.victory_condition in (VictoryCondition.option_hag1, VictoryCondition.option_wonderwing_challenge):
        self.multiworld.get_location(locationName.HAG1, player).place_locked_item(self.create_event_item(itemName.VICTORY))


def create_region(multiworld, player: int, active_locations, name: str, locations=None):
    ret = Region(name, player, multiworld)
    if locations:
        loc_to_id = {loc: active_locations.get(loc, 0) for loc in locations if active_locations.get(loc, None)}
        if multiworld.worlds[player].options.victory_condition == VictoryCondition.option_hag1 and locationName.HAG1 in locations:
            ret.add_locations({locationName.HAG1: None})
        elif multiworld.worlds[player].options.victory_condition == VictoryCondition.option_wonderwing_challenge and locationName.HAG1 in locations:
            ret.add_locations({locationName.HAG1: None})
        else:
            ret.add_locations(loc_to_id, BanjoTooieLocation)
    return ret

def connect_regions(self):
    multiworld = self.multiworld
    player = self.player
    rules = BanjoTooieRules(self)

    region_menu = self.get_region("Menu")
    region_menu.add_exits({regionName.SM})

    region_SM = self.get_region(regionName.SM)
    region_SM.add_exits({regionName.IOHJV, regionName.SMGL},{
                          regionName.IOHJV: lambda state: rules.canGetPassedKlungo(state),
                          regionName.SMGL: lambda state: rules.SM_to_GL(state)
                        })

    region_JV = self.get_region(regionName.IOHJV)
    region_JV.add_exits({regionName.IOHWH})

    region_WH = self.get_region(regionName.IOHWH)
    region_WH.add_exits({regionName.MTE, regionName.IOHPL},
                        {regionName.MTE: lambda state: rules.mt_jiggy(state),
                         regionName.IOHPL: lambda state: rules.WH_to_PL(state)})

    region_MT = self.get_region(regionName.MT)
    region_MT.add_exits({regionName.TL_HATCH, regionName.GM, regionName.HP},
                        {regionName.TL_HATCH: lambda state: rules.jiggy_treasure_chamber(state),\
                        regionName.GM: lambda state: rules.dilberta_free(state),
                        regionName.HP: lambda state: rules.mt_hfp_backdoor(state)})

    region_HATCH = self.get_region(regionName.TL_HATCH)
    region_HATCH.add_exits({regionName.TL},
                        {regionName.TL: lambda state: rules.hatch_to_TDL(state)})

    region_PL = self.get_region(regionName.IOHPL)
    region_PL.add_exits({regionName.GGME, regionName.IOHPG, regionName.IOHCT},
                        {regionName.GGME: lambda state: rules.PL_to_GGM(state),
                         regionName.IOHPG: lambda state: rules.PL_to_PG(state),
                        regionName.IOHCT: lambda state: rules.split_up(state)})

    region_GM = self.get_region(regionName.GM)
    region_GM.add_exits({regionName.GMWSJT, regionName.CHUFFY, regionName.GMFD}, {
                        regionName.GMWSJT: lambda state: rules.can_access_water_storage_jinjo_from_GGM(state),
                        regionName.CHUFFY: lambda state: rules.can_beat_king_coal(state) and rules.ggm_to_chuffy(state),
                        regionName.GMFD: lambda state: rules.humbaGGM(state),
                        regionName.WW: lambda state: rules.ggm_to_ww(state)
                        })

    region_GMWSJT = self.get_region(regionName.GMWSJT)
    region_GMWSJT.add_exits({regionName.GM}, {})

    region_PG = self.get_region(regionName.IOHPG)
    region_PG.add_exits({regionName.WWE, regionName.IOHPGU, regionName.IOHPL}, {
                          regionName.WWE: lambda state: rules.ww_jiggy(state),
                          regionName.IOHPGU: lambda state: rules.dive(state),
                          regionName.IOHPL: lambda state: rules.PG_to_PL(state)
                        })

    region_PGU = self.get_region(regionName.IOHPGU)
    region_PGU.add_exits({regionName.IOHWL, regionName.IOHPG}, {
                            regionName.IOHPG: lambda state: rules.PGU_to_PG(state),
                            regionName.IOHWL: lambda state: rules.talon_torpedo(state),
                          })

    region_WW = self.get_region(regionName.WW)
    region_WW.add_exits({regionName.CHUFFY, regionName.TL, regionName.GMFD, regionName.WWA51NESTS},
                        {regionName.CHUFFY: lambda state: rules.can_beat_king_coal(state) and rules.ww_to_chuffy(state),
                        regionName.TL: lambda state: rules.ww_tdl_backdoor(state),
                        regionName.GMFD: lambda state: rules.ww_to_fuel_depot(state),
                        regionName.WWA51NESTS: lambda state: rules.a51_nests_from_WW(state),
                        })

    region_IOHCT = self.get_region(regionName.IOHCT)
    region_IOHCT.add_exits({regionName.IOHCT_HFP_ENTRANCE, regionName.HFPE, regionName.JRLE, regionName.CHUFFY, regionName.IOHPL},
        {regionName.HFPE:lambda state: rules.hfp_jiggy(state),
         regionName.JRLE: lambda state: rules.jrl_jiggy(state),
         regionName.CHUFFY: lambda state: rules.can_beat_king_coal(state) and rules.ioh_to_chuffy(state),
         regionName.IOHPL: lambda state: rules.PG_to_PL(state)})

    region_JR = self.get_region(regionName.JR)
    region_JR.add_exits({regionName.JRU},
                        {regionName.JRU: lambda state: rules.can_dive_in_JRL(state)})

    region_JRU = self.get_region(regionName.JRU)
    region_JRU.add_exits({regionName.JRU2},
                        {regionName.JRU2: lambda state: rules.can_reach_atlantis(state)})

    region_JRU2 = self.get_region(regionName.JRU2)
    region_JRU2.add_exits({regionName.GMWSJT},
                        {regionName.GMWSJT: lambda state: rules.can_access_water_storage_jinjo_from_JRL(state)})

    region_HP = self.get_region(regionName.HP)
    region_HP.add_exits({regionName.MT, regionName.JR, regionName.CHUFFY},
                        {regionName.MT: lambda state: rules.HFP_to_MT(state),
                         regionName.JR: lambda state: rules.HFP_to_JRL(state),
                         regionName.CHUFFY: lambda state: rules.can_beat_king_coal(state) and rules.hfp_to_chuffy(state)})

    region_IOHWL = self.get_region(regionName.IOHWL)
    region_IOHWL.add_exits({regionName.IOHPGU, regionName.IOHQM, regionName.TDLE, regionName.CCLE},
                        {regionName.IOHPGU: lambda state: rules.WL_to_PGU(state),
                         regionName.IOHQM: lambda state: rules.springy_step_shoes(state),
                         regionName.TDLE: lambda state: rules.tdl_jiggy(state),
                         regionName.CCLE: lambda state: rules.ccl_jiggy(state)})

    region_TL = self.get_region(regionName.TL)
    region_TL.add_exits({regionName.TL_HATCH, regionName.WW, regionName.CHUFFY, regionName.WWA51NESTS},
                        {regionName.WW: lambda state: rules.TDL_to_WW(state),
                         regionName.CHUFFY: lambda state: rules.can_beat_king_coal(state) and rules.tdl_to_chuffy(state),
                         regionName.TL_HATCH: lambda state: rules.tdl_to_hatch(state),
                         regionName.WWA51NESTS: lambda state: rules.a51_nests_from_TDL(state),
                         })

    region_QM = self.get_region(regionName.IOHQM)
    region_QM.add_exits({regionName.GIE, regionName.IOHWL, regionName.CKE},
                        {regionName.GIE: lambda state: rules.gi_jiggy(state),
                         regionName.IOHWL: lambda state: rules.QM_to_WL(state),
                         regionName.CKE: lambda state: rules.quag_to_CK(state)})

    region_GIO = self.get_region(regionName.GIO)
    region_GIO.add_exits({regionName.GI1, regionName.GIOB, regionName.GI5},
                        {regionName.GI1: lambda state: rules.outside_gi_to_floor1(state),
                         regionName.GIOB: lambda state: rules.outside_gi_to_outside_back(state),
                         regionName.GI5: lambda state: rules.outside_gi_to_floor_5(state)})

    region_GIOB = self.get_region(regionName.GIOB)
    region_GIOB.add_exits({regionName.GIO, regionName.GI2, regionName.GI3, regionName.GI4, regionName.GI5},
                        {regionName.GIO: lambda state: rules.climb(state),
                         regionName.GI2: lambda state: rules.outside_gi_back_to_floor2(state),
                         regionName.GI3: lambda state: rules.outside_gi_back_to_floor_3(state),
                         regionName.GI4: lambda state: rules.outside_gi_back_to_floor_4(state),
                         regionName.GI5: lambda state: rules.outside_gi_back_to_floor_5(state)
                         })

    region_GIES = self.get_region(regionName.GIES)
    region_GIES.add_exits({regionName.GI1, regionName.GI2, regionName.GI3, regionName.GI4},
                        {regionName.GI1: lambda state: rules.elevator_shaft_to_floor_1(state),
                         regionName.GI2: lambda state: rules.elevator_shaft_to_em(state),
                         regionName.GI3: lambda state: rules.elevator_shaft_to_boiler_plant(state),
                         regionName.GI4: lambda state: rules.elevator_shaft_to_floor_4(state)})

    region_GI1 = self.get_region(regionName.GI1)
    region_GI1.add_exits({regionName.GIO, regionName.GIES, regionName.GI2, regionName.GI5, regionName.CHUFFY},
                        {regionName.GIO: lambda state: rules.split_up(state),
                         regionName.GI2: lambda state: rules.F1_to_F2(state), # TODO: 1 to 3 and 1 to 4, maybe
                         regionName.GI5: lambda state: rules.F1_to_F5(state),
                         regionName.CHUFFY: lambda state: rules.can_beat_king_coal(state) and rules.gi_to_chuffy(state)})

    region_GI2 = self.get_region(regionName.GI2)
    region_GI2.add_exits({regionName.GIOB, regionName.GI1, regionName.GI2EM, regionName.GI3},
                        {regionName.GI1: lambda state: rules.F2_to_F1(state),
                         regionName.GI2EM: lambda state: rules.floor_2_to_em_room(state),
                         regionName.GI3: lambda state: rules.F2_to_F3(state)
                         })

    region_GI2EM = self.get_region(regionName.GI2)
    region_GI2EM.add_exits({regionName.GIES},
                        {regionName.GIES: lambda state: rules.floor_2_em_room_to_elevator_shaft(state)
                         })

    region_GI3 = self.get_region(regionName.GI3)
    region_GI3.add_exits({regionName.GIOB, regionName.GI2, regionName.GI3B, regionName.GI4, regionName.GI5}, {
                            regionName.GIOB: lambda state: rules.floor_3_to_outside_back(state),
                            regionName.GI2: lambda state: rules.F3_to_F2(state),
                            regionName.GI3B: lambda state: rules.floor_3_to_boiler_plant(state),
                            regionName.GI4: lambda state: rules.F3_to_F4(state),
                            regionName.GI5: lambda state: rules.floor_3_to_floor_5(state),
                            })

    region_GI3B = self.get_region(regionName.GI3B)
    region_GI3B.add_exits({regionName.GI3, regionName.GIES}, {
                            regionName.GIES: lambda state: rules.elevator_door(state),
                          })

    region_GI4 = self.get_region(regionName.GI4)
    region_GI4.add_exits({regionName.GIOB, regionName.GI3, regionName.GI4B, regionName.GI5}, {
                            regionName.GIOB: lambda state: rules.floor_4_to_outside_back(state),
                            regionName.GI3: lambda state: rules.floor_4_to_floor_3(state),
                            regionName.GI4B: lambda state: rules.floor_4_to_floor_4_back(state),
                            regionName.GI5: lambda state: rules.floor_4_to_floor_5(state),
                            })

    region_GI4B = self.get_region(regionName.GI4B)
    region_GI4B.add_exits({regionName.GIES, regionName.GI4}, {
                            regionName.GIES: lambda state: rules.floor_4_back_to_elevator_shaft(state)
                            })

    region_GI5 = self.get_region(regionName.GI5)
    region_GI5.add_exits({regionName.GI1, regionName.GI3, regionName.GI3B, regionName.GI4}, { # If you can fly and reach the roof, you have access to floor 3 and 4.
                            regionName.GI1:  lambda state: rules.floor_5_to_floor_1(state),
                            regionName.GI3B: lambda state: rules.floor_5_to_boiler_plant(state)
                            })

    region_CK = self.get_region(regionName.CK)
    region_CK.add_exits({regionName.H1},
                        {regionName.H1: lambda state: rules.check_hag1_options(state)})

    region_chuffy = self.get_region(regionName.CHUFFY)
    region_chuffy.add_exits({regionName.GM, regionName.WW, regionName.IOHCT, regionName.TL,regionName.GI1,regionName.HP},
                        {regionName.GM: lambda state: state.has(itemName.CHUFFY, player),
                         regionName.WW: lambda state: state.has(itemName.CHUFFY, player) and state.has(itemName.TRAINSWWW, player),
                         regionName.IOHCT: lambda state: state.has(itemName.CHUFFY, player) and state.has(itemName.TRAINSWIH, player),
                         regionName.TL: lambda state: state.has(itemName.CHUFFY, player) and state.has(itemName.TRAINSWTD, player),
                         regionName.GI1: lambda state: state.has(itemName.CHUFFY, player) and state.has(itemName.TRAINSWGI, player),
                         regionName.HP: lambda state: state.has(itemName.CHUFFY, player) and state.has(itemName.TRAINSWHP1, player)
                         })

    region_mt_entrance = self.get_region(regionName.MTE)
    region_mt_entrance.add_exits({regionName.IOHWH}, {regionName.IOHWH: lambda state: rules.MT_to_WH(state)})

    region_ggm_entrance = self.get_region(regionName.GGME)
    region_ggm_entrance.add_exits({regionName.IOHPL}, {regionName.IOHPL: lambda state: rules.escape_ggm_loading_zone(state)})

    region_ww_entrance = self.get_region(regionName.WWE)
    region_ww_entrance.add_exits({regionName.IOHPG}, {regionName.IOHPG: lambda state: rules.ww_jiggy(state)})

    region_jrl_entrance = self.get_region(regionName.JRLE)
    region_jrl_entrance.add_exits({regionName.IOHCT}, {regionName.IOHCT: lambda state: rules.JRL_to_CT(state)})

    region_tdl_entrance = self.get_region(regionName.TDLE)
    region_tdl_entrance.add_exits({regionName.IOHWL}, {regionName.IOHWL: lambda state: rules.TDL_to_IOHWL(state)})

    region_gi_entrance = self.get_region(regionName.GIE)
    region_gi_entrance.add_exits({regionName.IOHQM}, {regionName.IOHQM: lambda state: rules.gi_jiggy(state)})

    region_hfp_entrance = self.get_region(regionName.HFPE)
    region_hfp_entrance.add_exits({regionName.IOHCT_HFP_ENTRANCE, regionName.IOHCT},
                                  {regionName.IOHCT_HFP_ENTRANCE: lambda state: rules.HFP_to_CTHFP(state),
                                   regionName.IOHCT: lambda state: rules.backdoors_enabled(state)})

    region_ccl_entrance = self.get_region(regionName.CCLE)
    region_ccl_entrance.add_exits({regionName.IOHWL}, {regionName.IOHWL: lambda state: rules.CCL_to_WL(state)})

    region_ck_entrance = self.get_region(regionName.CKE)
    region_ck_entrance.add_exits({regionName.IOHQM}, {regionName.IOHQM: lambda state: rules.CK_to_Quag(state)})

    # World entrance randomisation (and exits)
    entrance_lookup = {
            regionName.MT: regionName.MTE,
            regionName.GM: regionName.GGME,
            regionName.WW: regionName.WWE,
            regionName.JR: regionName.JRLE,
            regionName.TL: regionName.TDLE,
            regionName.GIO: regionName.GIE,
            regionName.HP: regionName.HFPE,
            regionName.CC: regionName.CCLE,
            regionName.CK: regionName.CKE,
        }
    for starting_zone, actual_world in self.loading_zones.items():
        overworld_entrance = entrance_lookup[starting_zone]

        region_overworld_entrance = self.get_region(overworld_entrance)
        region_overworld_entrance.add_exits({actual_world})

        region_actual_world_entrance = self.get_region(actual_world)

        if actual_world == regionName.GM:
            region_actual_world_entrance.add_exits({overworld_entrance}, {overworld_entrance: lambda state: rules.GGM_to_PL(state)})
        else:
            region_actual_world_entrance.add_exits({overworld_entrance})


    # Silos
    silo = self.single_silo
    if silo == "NONE":
        pass
    elif silo == "ALL":
        region_JV.add_exits({regionName.IOHPL, regionName.IOHCT, regionName.IOHPG, regionName.IOHWL, regionName.IOHQM})
    else: # The value is a region name of the overworld.
        region_JV.add_exits({silo})

