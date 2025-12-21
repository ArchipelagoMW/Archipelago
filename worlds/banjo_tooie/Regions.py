import copy
from dataclasses import dataclass
from typing import List, Dict
from BaseClasses import Region
from .Options import VictoryCondition

from .Names import regionName, locationName, itemName
from .Locations import BanjoTooieLocation
from .Rules import BanjoTooieRules

# This dict contains all the regions, as well as all the locations that are always tracked by Archipelago.
BANJO_TOOIE_REGIONS: Dict[str, List[str]] = {
    regionName.MENU:              [],
    regionName.SM:       [
        locationName.CHEATOSM1,
        locationName.JINJOIH5,
        locationName.PMEGG,
        locationName.BMEGG,
        locationName.ROYSTEN1,
        locationName.ROYSTEN2,
    ],
    regionName.SMGL:     [
        locationName.CHEATOR1,
        locationName.CHEATOR2,
        locationName.CHEATOR3,
        locationName.CHEATOR4,
        locationName.CHEATOR5
    ],
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
    ],
    regionName.MT:       [
        locationName.JINJOMT2,
        locationName.JINJOMT4,
        locationName.JINJOMT5,
        locationName.JIGGYMT4,
        locationName.JIGGYMT5,
        locationName.JIGGYMT9,
        locationName.GLOWBOMT1,
        locationName.HONEYCMT1,
        locationName.HONEYCMT2,
        locationName.HONEYCMT3,
        locationName.CHEATOMT1,
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
    regionName.MTTT: [
        locationName.JINJOMT3,
        locationName.JIGGYMT2,
    ],
    regionName.MTBOSS: [
        locationName.JIGGYMT1
    ],
    regionName.MTJSG:    [
        locationName.JINJOMT1,
        locationName.JIGGYMT6,
        locationName.JIGGYMT10,
        locationName.GLOWBOMT2,
        locationName.CHEATOMT3,
        locationName.GGRAB,

    ],
    regionName.MTPC:    [
        locationName.JIGGYGM6,
        locationName.JIGGYMT7,
        locationName.CHEATOMT2,
        locationName.JIGGYMT8,
    ],
    regionName.MTKS:    [
        locationName.JIGGYMT3,
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
    regionName.CHUFFY: [],
    regionName.GMBOSS: [
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
        locationName.JIGGYWW4,
        locationName.JIGGYWW5,
        locationName.JIGGYWW6,
        locationName.JIGGYWW7,
        locationName.JIGGYWW8,

        locationName.JIGGYWW10,
        locationName.GLOWBOWW2,
        locationName.HONEYCWW1,
        locationName.HONEYCWW3,
        locationName.CHEATOWW1,

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
        locationName.NOTEWW16,

        locationName.MOGGY,
        locationName.SOGGY,
        locationName.GROGGY
    ],
    regionName.WWI: [
        locationName.JIGGYWW9,
        locationName.CHEATOWW2,
        locationName.HONEYCWW2,
        locationName.GLOWBOWW1,
    ],
    regionName.WWBOSS: [
        locationName.JIGGYWW3,
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
    regionName.JRAT: [
        locationName.JIGGYJR3,
        locationName.JIGGYJR8,
        locationName.GLOWBOJR2,
        locationName.HONEYCJR2,
        locationName.CHEATOJR3,
        locationName.TTORP,
        locationName.TREBLEJR,
        locationName.NOTEJRL6,
        locationName.NOTEJRL7,
    ],
    regionName.JRSS:    [
        locationName.JINJOJR5,
    ],
    regionName.JRSS2:   [
        locationName.JINJOJR4,
    ],
    regionName.JRLC:    [
        locationName.JIGGYJR1,
    ],
    regionName.JRBOSS: [
        locationName.JIGGYJR7,
    ],
    regionName.JRBFC:   [
        locationName.JINJOJR3,
        locationName.JIGGYJR6,
        locationName.HONEYCJR1,
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
        # locationName.JIGGYTD2, #In CCL
        locationName.JIGGYTD3,
        locationName.JIGGYTD5,
        locationName.JIGGYTD6,
        locationName.JIGGYTD9,
        locationName.JIGGYTD10,
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
    regionName.TLSP:    [
        locationName.JIGGYTD8,
        locationName.JIGGYHP7,
        locationName.JINJOTL5,
    ],
    regionName.TLTOP:   [],
    regionName.TLIMTOP:  [],
    regionName.TLBOSS: [
        locationName.JIGGYTD1,
        locationName.JIGGYTD4,
        locationName.JIGGYTD7,
    ],
    regionName.IOHQM:   [],
    regionName.GIO: [
        locationName.TREBLEGI,
    ],
    regionName.GIOB: [
        locationName.TRAINSWGI,
        locationName.JINJOGI5,
        locationName.SKIVOU
    ],
    regionName.GIES: [],
    regionName.GIBOSS: [
        locationName.CHEATOGI3,
    ],
    regionName.GI1: [
        # locationName.JINJOGI3, Moved to JRL
        locationName.JIGGYGI1,
        locationName.JIGGYGI2,
        locationName.JIGGYGI7,
        locationName.JIGGYGI8,
        locationName.JIGGYGI10,
        locationName.CHEATOGI1,
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
        locationName.SKIVF1,
        locationName.SKIVWQ,
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
        locationName.SKIVF2
    ],
    regionName.GI2EM: [],
    regionName.GI3: [
        locationName.HONEYCGI1,
        locationName.GLOWBOGI2,
        locationName.NOTEGI15,
        locationName.NOTEGI16,
        locationName.SKIVF3,
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
        locationName.SKIVF5
    ],
    regionName.GIF: [
        locationName.HONEYCGI3,
    ],
    regionName.GIR: [],
    regionName.HP: [
        locationName.JINJOHP1,
        locationName.JINJOHP2,
        locationName.JINJOHP3,
        locationName.JINJOHP4,
        locationName.JINJOHP5,
        locationName.JIGGYHP2,
        locationName.JIGGYHP3,
        locationName.JIGGYHP4,
        locationName.JIGGYHP5,
        locationName.JIGGYHP6,

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
        locationName.NOTEHFP16,
        locationName.ALPHETTE,
        locationName.BETETTE,
        locationName.GAMETTE
    ],
    regionName.HPFBOSS: [
        # rule that should have access to both BOSS regions to obtain.
        locationName.JIGGYHP1,
    ],
    regionName.HPIBOSS: [],
    regionName.CC:      [
        locationName.JINJOCC1,
        locationName.JINJOCC2,
        locationName.JINJOCC3,
        locationName.JINJOCC5,
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
        locationName.NOTECCL16,
        locationName.FITHJ,
        locationName.FITSR,
    ],
    regionName.CCBOSS: [
        locationName.JIGGYCC1,
        locationName.JINJOCC4,
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

    regionName.IHSILOS: [],
}

# Regions for nests. Regions that don't contain anything are omitted.
NEST_REGIONS: Dict[str, List[str]] = {
    regionName.MENU:              [],
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

      locationName.NESTMT36,
      locationName.NESTMT37,
      locationName.NESTMT38,
      locationName.NESTMT39,
      locationName.NESTMT40,
      locationName.NESTMT41,
    ],
    regionName.MTTT: [
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
    ],
    regionName.MTJSG:   [
      locationName.NESTMT1,
      locationName.NESTMT2,

      locationName.NESTMT22,
      locationName.NESTMT23,
      locationName.NESTMT24,
    ],
    regionName.MTPC:    [
      locationName.NESTMT15,
      locationName.NESTMT16,
      locationName.NESTMT17,
      locationName.NESTMT18,
      locationName.NESTMT19,
      locationName.NESTMT20,
      locationName.NESTMT21,
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

      locationName.NESTWW22,
      locationName.NESTWW23,
      locationName.NESTWW24,
      locationName.NESTWW25,
      locationName.NESTWW26,
    ],
    regionName.WWBOSS: [
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
    regionName.WWI:     [
      locationName.NESTWW20,
      locationName.NESTWW21,
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
    regionName.JRAT: [
        locationName.NESTJR16,
        locationName.NESTJR17,
        locationName.NESTJR18,
        locationName.NESTJR19,

        locationName.NESTJR24,

        locationName.NESTJR28,
        locationName.NESTJR29,
        locationName.NESTJR30,
        locationName.NESTJR33,
    ],
    regionName.JRSS:    [
        locationName.NESTJR31,
        locationName.NESTJR32,
    ],
    regionName.JRSS2:   [
        locationName.NESTJR10,
        locationName.NESTJR11,
        locationName.NESTJR12,
        locationName.NESTJR13,

        locationName.NESTJR37,
        locationName.NESTJR38,
    ],
    regionName.JRBFC:   [
        locationName.NESTJR14,
        locationName.NESTJR15,

        locationName.NESTJR39,
        locationName.NESTJR40,
    ],
    regionName.JRLC:    [
        locationName.NESTJR34,
        locationName.NESTJR35,
        locationName.NESTJR36,
    ],
    regionName.JRBOSS: [
        locationName.NESTJR20,
        locationName.NESTJR21,
        locationName.NESTJR22,
        locationName.NESTJR23,
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
        locationName.NESTTL7,

        locationName.NESTTL12,
        locationName.NESTTL13,
        locationName.NESTTL14,
        locationName.NESTTL15,
        locationName.NESTTL18,
        locationName.NESTTL19,
        locationName.NESTTL20,
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
    regionName.TLTOP:   [
        locationName.NESTTL6,
        locationName.NESTTL8,
        locationName.NESTTL9,
        locationName.NESTTL10,
        locationName.NESTTL11,

        locationName.NESTTL16,
        locationName.NESTTL17,

        locationName.NESTTL52,
    ],
    regionName.TLBOSS: [
        locationName.NESTTL21,
        locationName.NESTTL22,
    ],
    regionName.TLSP:   [
        locationName.NESTTL45,
        locationName.NESTTL46,
        locationName.NESTTL47,
        locationName.NESTTL48,
        locationName.NESTTL49,
        locationName.NESTTL50,
        locationName.NESTTL51,
        locationName.NESTTL53,
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
    regionName.GIBOSS: [
      locationName.NESTGI61,
      locationName.NESTGI62,
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
      locationName.NESTGI53,
      locationName.NESTGI54,
      locationName.NESTGI55,
    ],
    regionName.GIR: [
      locationName.NESTGI1,
      locationName.NESTGI2,
      locationName.NESTGI3,
    ],
    regionName.GIF: [
      locationName.NESTGI26,
      locationName.NESTGI31,
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
    regionName.HPFBOSS: [
        locationName.NESTHP23,
    ],
    regionName.HPIBOSS: [
      locationName.NESTHP24,
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

SIGNPOST_REGIONS = {
    regionName.IOHJV: [
        locationName.SIGNIH1,
    ],
    regionName.IOHWH: [
        locationName.SIGNIH2,
        locationName.SIGNIH3,
        locationName.SIGNIH4,
        locationName.SIGNIH5,

        locationName.SIGNIH7,
        locationName.SIGNIH8,
        locationName.SIGNIH9,
        locationName.SIGNIH10,
        locationName.SIGNIH11,
        locationName.SIGNIH12,
        locationName.SIGNIH13,
        locationName.SIGNIH14,
    ],

    regionName.IOHPL: [
        locationName.SIGNIH6,
    ],
    regionName.IOHPG: [
        locationName.SIGNIH15,
        locationName.SIGNIH16,
        locationName.SIGNIH17,
    ],
    regionName.IOHCT: [
        locationName.SIGNIH18,
    ],
    regionName.IOHWL: [
        locationName.SIGNIH19,
    ],
    regionName.MT: [
        locationName.SIGNMT1,
        locationName.SIGNMT2,
    ],
    regionName.MTTT: [
        locationName.SIGNMT8,
        locationName.SIGNMT9,
    ],
    regionName.MTJSG: [
        locationName.SIGNMT5,
        locationName.SIGNMT6,
        locationName.SIGNMT7,
    ],
    regionName.MTPC: [
        locationName.SIGNMT3,
        locationName.SIGNMT4,

    ],
    regionName.GM: [
        locationName.SIGNGM1,
        locationName.SIGNGM2,
        locationName.SIGNGM3,
        locationName.SIGNGM4,
    ],
    regionName.WW: [
        locationName.SIGNWW1,
        locationName.SIGNWW2,
        locationName.SIGNWW3,
        locationName.SIGNWW4,
        locationName.SIGNWW5,
        locationName.SIGNWW6,
        locationName.SIGNWW7,
        locationName.SIGNWW8,
    ],
    regionName.JR: [
        locationName.SIGNJR2,
        locationName.SIGNJR3,
        locationName.SIGNJR4,
    ],
    regionName.JRSS2: [
        locationName.SIGNJR1,
    ],
    regionName.TL: [
        locationName.SIGNTL1,
        locationName.SIGNTL2,
        locationName.SIGNTL4,
    ],
    regionName.TLIMTOP:  [
        locationName.SIGNTL3,
    ],
    regionName.GIO: [
        locationName.SIGNGI1,
    ],
    regionName.GI1: [
        locationName.SIGNGI2,
    ],
    regionName.GIES: [
        locationName.SIGNGI3,
        locationName.SIGNGI4,
    ],
    regionName.HP: [
        locationName.SIGNHP1,
        locationName.SIGNHP2,
        locationName.SIGNHP3,
        locationName.SIGNHP4,
        locationName.SIGNHP5,
    ],
    regionName.CC: [
        locationName.SIGNCC1,
        locationName.SIGNCC2,
        locationName.SIGNCC3,
        locationName.SIGNCC4,
    ],
}

SILO_REGIONS: Dict[str, List[str]] = {
    regionName.IOHJV:       [
      locationName.SILOIOHJV,
    ],
    regionName.IOHWH:       [
      locationName.SILOIOHWH,
    ],
    regionName.IOHPL:       [
      locationName.SILOIOHPL,
    ],
    regionName.IOHPG:       [
      locationName.SILOIOHPG,
    ],
    regionName.IOHCT:       [
      locationName.SILOIOHCT,
    ],
    regionName.IOHQM:       [
      locationName.SILOIOHQM,
    ],
    regionName.IOHWL:       [
      locationName.SILOIOHWL,
    ],
}

WARP_PAD_REGIONS: Dict[str, List[str]] = {
    regionName.MT:       [
        locationName.WARPMT1,
        locationName.WARPMT2,
    ],
    regionName.MTJSG:    [
        locationName.WARPMT4,
    ],
    regionName.MTPC:    [
        locationName.WARPMT3,
    ],
    regionName.MTKS:    [
        locationName.WARPMT5,
    ],
    regionName.GM:       [
        locationName.WARPGM1,
        locationName.WARPGM2,
        locationName.WARPGM3,
        locationName.WARPGM4,
        locationName.WARPGM5,
    ],
    regionName.WW:      [
        locationName.WARPWW1,
        locationName.WARPWW2,
        locationName.WARPWW3,
        locationName.WARPWW4,
    ],
    regionName.WWI:     [
        locationName.WARPWW5,
    ],
    regionName.JR:      [
        locationName.WARPJR1,
    ],
    regionName.JRAT:    [
        locationName.WARPJR2,
    ],
    regionName.JRSS:    [
        locationName.WARPJR3,
    ],
    regionName.JRLC:    [
        locationName.WARPJR5,
    ],
    regionName.JRBFC:   [
        locationName.WARPJR4,
    ],
    regionName.TL:      [
        locationName.WARPTL1,
        locationName.WARPTL3,
        locationName.WARPTL4,
    ],
    regionName.TLTOP:   [
        locationName.WARPTL5,
    ],
    regionName.TLSP:    [
        locationName.WARPTL2,
    ],
    regionName.GI1: [
        locationName.WARPGI1,
    ],
    regionName.GI2: [
        locationName.WARPGI2,
    ],
    regionName.GI3: [
        locationName.WARPGI3,
    ],
    regionName.GI4: [
        locationName.WARPGI4,
    ],
    regionName.GIR: [
        locationName.WARPGI5,
    ],
    regionName.HP: [
        locationName.WARPHP1,
        locationName.WARPHP2,
        locationName.WARPHP3,
        locationName.WARPHP4,
        locationName.WARPHP5,
    ],
    regionName.CC: [
        locationName.WARPCC1,
        locationName.WARPCC2,
    ],
    regionName.CK: [
        locationName.WARPCK1,
        locationName.WARPCK2,
    ],
}

BTTICKETS_REGIONS: Dict[str, List[str]] = {
    regionName.WW:      [
        locationName.BTTICK1,
        locationName.BTTICK2,
        locationName.BTTICK3,
        locationName.BTTICK4,
    ]
}

GREEN_RELIC_REGIONS: Dict[str, List[str]] = {
    regionName.MTTT: [
        locationName.GRRELICE1,
        locationName.GRRELICE2,
        locationName.GRRELICB1,
        locationName.GRRELICB2,
        locationName.GRRELICB3,
        locationName.GRRELICC1,
        locationName.GRRELICC2,
        locationName.GRRELICC3,
        locationName.GRRELICC4,
        locationName.GRRELICC5,
        locationName.GRRELICG1,
        locationName.GRRELICG2,
        locationName.GRRELICG3,
        locationName.GRRELICG4,
        locationName.GRRELICG5,
        locationName.GRRELICT1,
        locationName.GRRELICT2,
        locationName.GRRELICP1,
        locationName.GRRELICP2,
        locationName.GRRELICP3,
        locationName.GRRELICS1,
        locationName.GRRELICS2,
        locationName.GRRELICR1,
        locationName.GRRELICR2,
        locationName.GRRELICR3,
    ]
}

BEANS_REGIONS: Dict[str, List[str]] = {
    regionName.CC:      [
        locationName.BEANCC1,
        locationName.BEANCC2
    ]
}


def create_regions(self):
    player = self.player
    active_locations = self.location_name_to_id
    region_map = copy.deepcopy(BANJO_TOOIE_REGIONS)

    if self.options.victory_condition.value == VictoryCondition.option_minigame_hunt\
            or self.options.victory_condition.value == VictoryCondition.option_wonderwing_challenge:
        region_map[regionName.MT].append(locationName.MUMBOTKNGAME1)
        region_map[regionName.GM].append(locationName.MUMBOTKNGAME2)
        region_map[regionName.WW].append(locationName.MUMBOTKNGAME3)
        region_map[regionName.WW].append(locationName.MUMBOTKNGAME4)
        region_map[regionName.WW].append(locationName.MUMBOTKNGAME5)
        region_map[regionName.WW].append(locationName.MUMBOTKNGAME6)
        region_map[regionName.JRLC].append(locationName.MUMBOTKNGAME7)
        region_map[regionName.TL].append(locationName.MUMBOTKNGAME8)
        region_map[regionName.GI4B].append(locationName.MUMBOTKNGAME9)
        region_map[regionName.GI3B].append(locationName.MUMBOTKNGAME10)
        region_map[regionName.HP].append(locationName.MUMBOTKNGAME11)
        region_map[regionName.CC].append(locationName.MUMBOTKNGAME12)
        region_map[regionName.CC].append(locationName.MUMBOTKNGAME13)
        region_map[regionName.CC].append(locationName.MUMBOTKNGAME14)
        region_map[regionName.CC].append(locationName.MUMBOTKNGAME15)

    if self.options.victory_condition.value == VictoryCondition.option_boss_hunt\
            or self.options.victory_condition.value == VictoryCondition.option_wonderwing_challenge\
            or self.options.victory_condition.value == VictoryCondition.option_boss_hunt_and_hag1:
        region_map[regionName.MTBOSS].append(locationName.MUMBOTKNBOSS1)
        region_map[regionName.GMBOSS].append(locationName.MUMBOTKNBOSS2)
        region_map[regionName.WWBOSS].append(locationName.MUMBOTKNBOSS3)
        region_map[regionName.JRBOSS].append(locationName.MUMBOTKNBOSS4)
        region_map[regionName.TLBOSS].append(locationName.MUMBOTKNBOSS5)
        region_map[regionName.GIBOSS].append(locationName.MUMBOTKNBOSS6)
        # rule to access both boss areas
        region_map[regionName.HPFBOSS].append(locationName.MUMBOTKNBOSS7)
        region_map[regionName.CCBOSS].append(locationName.MUMBOTKNBOSS8)

    if self.options.victory_condition.value == VictoryCondition.option_jinjo_family_rescue\
            or self.options.victory_condition.value == VictoryCondition.option_wonderwing_challenge:
        region_map[regionName.IOHJV].append(locationName.MUMBOTKNJINJO1)
        region_map[regionName.IOHJV].append(locationName.MUMBOTKNJINJO2)
        region_map[regionName.IOHJV].append(locationName.MUMBOTKNJINJO3)
        region_map[regionName.IOHJV].append(locationName.MUMBOTKNJINJO4)
        region_map[regionName.IOHJV].append(locationName.MUMBOTKNJINJO5)
        region_map[regionName.IOHJV].append(locationName.MUMBOTKNJINJO6)
        region_map[regionName.IOHJV].append(locationName.MUMBOTKNJINJO7)
        region_map[regionName.IOHJV].append(locationName.MUMBOTKNJINJO8)
        region_map[regionName.IOHJV].append(locationName.MUMBOTKNJINJO9)

    if self.options.honeyb_rewards.value:
        region_map[regionName.IOHPL].append(locationName.HONEYBR1)
        region_map[regionName.IOHPL].append(locationName.HONEYBR2)
        region_map[regionName.IOHPL].append(locationName.HONEYBR3)
        region_map[regionName.IOHPL].append(locationName.HONEYBR4)
        region_map[regionName.IOHPL].append(locationName.HONEYBR5)

    if self.options.skip_puzzles.value:
        region_map[regionName.IOHWH].append(locationName.W1)
        region_map[regionName.IOHWH].append(locationName.W2)
        region_map[regionName.IOHWH].append(locationName.W3)
        region_map[regionName.IOHWH].append(locationName.W4)
        region_map[regionName.IOHWH].append(locationName.W5)
        region_map[regionName.IOHWH].append(locationName.W6)
        region_map[regionName.IOHWH].append(locationName.W7)
        region_map[regionName.IOHWH].append(locationName.W8)
        region_map[regionName.IOHWH].append(locationName.W9)

    if self.options.nestsanity.value:
        nest_map = copy.deepcopy(NEST_REGIONS)
        for region, locations in nest_map.items():
            for location in locations:
                region_map[region].append(location)

    if self.options.randomize_signposts.value:
        signpost_map = copy.deepcopy(SIGNPOST_REGIONS)
        for region, locations in signpost_map.items():
            for location in locations:
                region_map[region].append(location)

    if self.options.randomize_silos.value:
        silo_map = copy.deepcopy(SILO_REGIONS)
        for region, locations in silo_map.items():
            for location in locations:
                region_map[region].append(location)

    if self.options.randomize_warp_pads.value:
        # Add warp hub regions only when warp pads are randomized
        region_map[regionName.MTWARP] = []
        region_map[regionName.JRWARP] = []
        region_map[regionName.TLWARP] = []
        region_map[regionName.GIWARP] = []

        warp_map = copy.deepcopy(WARP_PAD_REGIONS)
        for region, locations in warp_map.items():
            for location in locations:
                region_map[region].append(location)

    if self.options.randomize_tickets.value:
        ticket_map = copy.deepcopy(BTTICKETS_REGIONS)
        for region, locations in ticket_map.items():
            for location in locations:
                region_map[region].append(location)

    if self.options.randomize_green_relics.value:
        relic_map = copy.deepcopy(GREEN_RELIC_REGIONS)
        for region, locations in relic_map.items():
            for location in locations:
                region_map[region].append(location)

    if self.options.randomize_beans.value:
        beans_map = copy.deepcopy(BEANS_REGIONS)
        for region, locations in beans_map.items():
            for location in locations:
                region_map[region].append(location)

    self.multiworld.regions.extend(create_region(
        self,
        active_locations,
        region,
        locations
    ) for region, locations in region_map.items())
    if self.options.victory_condition.value in (
                VictoryCondition.option_hag1,
                VictoryCondition.option_wonderwing_challenge,
                VictoryCondition.option_boss_hunt_and_hag1
            ):
        self.multiworld.get_location(
            locationName.HAG1, player
        ).place_locked_item(
            self.create_event_item(itemName.VICTORY)
        )


def create_region(world, active_locations, name: str, locations=None):
    ret = Region(name, world.player, world.multiworld)
    if locations:
        loc_to_id = {loc: active_locations.get(loc, 0) for loc in locations if active_locations.get(loc, None)}
        if world.options.victory_condition.value == VictoryCondition.option_hag1\
                and locationName.HAG1 in locations:
            ret.add_locations({locationName.HAG1: None})
        elif world.options.victory_condition.value == VictoryCondition.option_wonderwing_challenge\
                and locationName.HAG1 in locations:
            ret.add_locations({locationName.HAG1: None})
        elif world.options.victory_condition.value == VictoryCondition.option_boss_hunt_and_hag1\
                and locationName.HAG1 in locations:
            ret.add_locations({locationName.HAG1: None})
        else:
            ret.add_locations(loc_to_id, BanjoTooieLocation)
    return ret


def connect_regions(self):
    player = self.player
    rules = BanjoTooieRules(self)

    region_menu = self.get_region(regionName.MENU)
    region_menu.add_exits({regionName.SM})

    region_SM = self.get_region(regionName.SM)
    region_SM.add_exits({regionName.IOHJV, regionName.SMGL}, {
                          regionName.IOHJV: lambda state: rules.canGetPassedKlungo(state),
                          regionName.SMGL: lambda state: rules.SM_to_GL(state)
                        })

    region_JV = self.get_region(regionName.IOHJV)
    region_JV.add_exits({regionName.IOHWH, regionName.IHSILOS}, {
                          regionName.IHSILOS: lambda state: state.has(itemName.SILOIOHJV, player)
                        })

    region_WH = self.get_region(regionName.IOHWH)
    region_WH.add_exits({regionName.MTE, regionName.IOHPL, regionName.IHSILOS}, {
                        regionName.MTE: lambda state: rules.mt_jiggy(state),
                        regionName.IOHPL: lambda state: rules.WH_to_PL(state),
                        regionName.IHSILOS: lambda state: state.has(itemName.SILOIOHWH, player)
                        })

    region_MT = self.get_region(regionName.MT)
    region_MT.add_exits({
            regionName.MTJSG,
            regionName.MTPC,
            regionName.MTKS,
            regionName.TL_HATCH,
            regionName.TL,
            regionName.MTTT,
        }, {
            regionName.MTJSG: lambda state: rules.MT_to_JSG(state),
            regionName.MTPC: lambda state: rules.prison_compound_open(state),
            regionName.MTKS: lambda state: rules.MT_to_KS(state),
            regionName.TL_HATCH: lambda state: rules.mt_to_hatch_region(state),
            regionName.TL: lambda state: rules.mt_tdl_backdoor(state),
            regionName.MTTT: lambda state: rules.breegull_blaster(state)
    })

    region_MTJSG = self.get_region(regionName.MTJSG)
    region_MTJSG.add_exits({regionName.MT}, {})

    region_MTPC = self.get_region(regionName.MTPC)
    region_MTPC.add_exits({regionName.MT, regionName.GM}, {
                            regionName.GM: lambda state: rules.prison_compound_as_banjo(state)
                            and rules.bill_drill(state)
                        })

    region_MTKS = self.get_region(regionName.MTKS)
    region_MTKS.add_exits({regionName.MT, regionName.HP}, {
                            regionName.HP: lambda state: rules.mt_hfp_backdoor(state),
                        })

    if self.options.randomize_warp_pads.value:
        region_MT.add_exits({regionName.MTWARP}, {
            regionName.MTWARP: lambda state: state.has(itemName.WARPMT1, player) or state.has(itemName.WARPMT2, player),
        })
        region_MTJSG.add_exits({regionName.MTWARP}, {
            regionName.MTWARP: lambda state: state.has(itemName.WARPMT4, player)
        })
        region_MTPC.add_exits({regionName.MTWARP}, {
            regionName.MTWARP: lambda state: state.has(itemName.WARPMT3, player),
        })
        region_MTKS.add_exits({regionName.MTWARP}, {
            regionName.MTWARP: lambda state: state.has(itemName.WARPMT5, player),
        })
        region_MTWARP = self.get_region(regionName.MTWARP)
        region_MTWARP.add_exits({regionName.MT, regionName.MTJSG, regionName.MTPC, regionName.MTKS}, {
            regionName.MT: lambda state: state.has(itemName.WARPMT1, player)
                or state.has(itemName.WARPMT2, player),
            regionName.MTJSG: lambda state: state.has(itemName.WARPMT4, player),
            regionName.MTPC: lambda state: state.has(itemName.WARPMT3, player),
            regionName.MTKS: lambda state: state.has(itemName.WARPMT5, player)
        })

    region_HATCH = self.get_region(regionName.TL_HATCH)
    region_HATCH.add_exits({regionName.TL}, {
        regionName.TL: lambda state: rules.hatch_to_TDL(state)
    })

    region_PL = self.get_region(regionName.IOHPL)
    region_PL.add_exits({regionName.GGME, regionName.IOHPG, regionName.IOHCT, regionName.IHSILOS},
                        {regionName.GGME: lambda state: rules.PL_to_GGM(state),
                         regionName.IOHPG: lambda state: rules.PL_to_PG(state),
                        regionName.IOHCT: lambda state: rules.split_up(state),
                        regionName.IHSILOS: lambda state: state.has(itemName.SILOIOHPL, player)})

    region_GM = self.get_region(regionName.GM)
    region_GM.add_exits({regionName.GMWSJT, regionName.CHUFFY, regionName.GMFD, regionName.WW}, {
                        regionName.GMWSJT: lambda state: rules.can_access_water_storage_jinjo_from_GGM(state),
                        regionName.CHUFFY: lambda state: rules.ggm_to_chuffy(state),
                        regionName.GMFD: lambda state: rules.humbaGGM(state),
                        regionName.WW: lambda state: rules.ggm_to_ww(state),
                        })

    region_GMWSJT = self.get_region(regionName.GMWSJT)
    region_GMWSJT.add_exits({regionName.GM}, {})

    region_PG = self.get_region(regionName.IOHPG)
    region_PG.add_exits({regionName.WWE, regionName.IOHPGU, regionName.IOHPL, regionName.IHSILOS}, {
                          regionName.WWE: lambda state: rules.ww_jiggy(state),
                          regionName.IOHPGU: lambda state: rules.dive(state),
                          regionName.IOHPL: lambda state: rules.PG_to_PL(state),
                          regionName.IHSILOS: lambda state: state.has(itemName.SILOIOHPG, player)
                        })

    region_PGU = self.get_region(regionName.IOHPGU)
    region_PGU.add_exits({regionName.IOHWL, regionName.IOHPG}, {
                            regionName.IOHPG: lambda state: rules.PGU_to_PG(state),
                            regionName.IOHWL: lambda state: rules.talon_torpedo(state),
                          })

    region_WW = self.get_region(regionName.WW)
    region_WW.add_exits({regionName.CHUFFY, regionName.WWI, regionName.TL, regionName.GMFD, regionName.WWA51NESTS}, {
                        regionName.CHUFFY: lambda state: rules.ww_to_chuffy(state),
                        regionName.WWI: lambda state: rules.ww_to_inferno(state),
                        regionName.TL: lambda state: rules.ww_tdl_backdoor(state),
                        regionName.GMFD: lambda state: rules.ww_to_fuel_depot(state),
                        regionName.WWA51NESTS: lambda state: rules.a51_nests_from_WW(state),
                        })

    region_IOHCT = self.get_region(regionName.IOHCT)
    region_IOHCT.add_exits({
        regionName.IOHCT_HFP_ENTRANCE,
        regionName.HFPE,
        regionName.JRLE,
        regionName.CHUFFY,
        regionName.IOHPL,
        regionName.IHSILOS
        }, {
            regionName.HFPE: lambda state: rules.hfp_jiggy(state),
            regionName.JRLE: lambda state: rules.jrl_jiggy(state),
            regionName.CHUFFY: lambda state: rules.can_beat_king_coal(state) and rules.ioh_to_chuffy(state),
            regionName.IOHPL: lambda state: rules.PG_to_PL(state),
            regionName.IHSILOS: lambda state: state.has(itemName.SILOIOHCT, player)
        })

    region_JR = self.get_region(regionName.JR)
    region_JR.add_exits({regionName.JRU}, {
                            regionName.JRU: lambda state: rules.can_dive_in_JRL(state),
                            })

    region_JRU = self.get_region(regionName.JRU)
    region_JRU.add_exits({regionName.JRAT}, {
        regionName.JRAT: lambda state: rules.can_pass_octopi(state)
    })

    region_JRAT = self.get_region(regionName.JRAT)
    region_JRAT.add_exits({regionName.JRSS, regionName.JRSS2, regionName.JRU}, {
                            regionName.JRSS: lambda state: rules.can_pass_octopi(state),
                            regionName.JRU: lambda state: rules.can_pass_octopi(state),
                        })

    region_JRSS = self.get_region(regionName.JRSS)
    region_JRSS.add_exits({regionName.JRAT, regionName.JRLC, regionName.GMWSJT}, {
                            regionName.JRAT: lambda state: rules.can_escape_sunken_ship(state),
                            regionName.JRLC: lambda state: rules.can_escape_sunken_ship(state),
                            regionName.GMWSJT: lambda state: rules.sunken_ship_to_ggm(state),
                        })

    region_JRSS2 = self.get_region(regionName.JRSS2)
    region_JRSS2.add_exits({regionName.JRAT, regionName.JRBFC}, {
                            regionName.JRAT: lambda state: rules.dive(state),
                            regionName.JRBFC: lambda state: rules.seaweed_to_bfc(state)})

    region_JRLC = self.get_region(regionName.JRLC)
    region_JRLC.add_exits({regionName.JRSS, regionName.JRBFC}, {
                            regionName.JRSS: lambda state: rules.locker_cavern_to_sunken_ship(state),
                            regionName.JRBFC: lambda state: rules.locker_cavern_to_big_fish_cavern(state)})

    region_JRBFC = self.get_region(regionName.JRBFC)
    region_JRBFC.add_exits({regionName.JRLC, regionName.JRSS2}, {
                            regionName.JRLC: lambda state: rules.big_fish_cave_to_locker_cavern(state)})

    if self.options.randomize_warp_pads.value:
        region_JR.add_exits({regionName.JRWARP}, {
            regionName.JRWARP: lambda state: state.has(itemName.WARPJR1, player),
        })
        region_JRAT.add_exits({regionName.JRWARP}, {
            regionName.JRWARP: lambda state: state.has(itemName.WARPJR2, player)
        })
        region_JRSS.add_exits({regionName.JRWARP}, {
            regionName.JRWARP: lambda state: state.has(itemName.WARPJR3, player),
        })
        region_JRLC.add_exits({regionName.JRWARP}, {
            regionName.JRWARP: lambda state: state.has(itemName.WARPJR5, player)
        })
        region_JRBFC.add_exits({regionName.JRWARP}, {
            regionName.JRWARP: lambda state: state.has(itemName.WARPJR4, player)
        })
        region_JRWARP = self.get_region(regionName.JRWARP)
        region_JRWARP.add_exits({
            regionName.JR,
            regionName.JRAT,
            regionName.JRSS,
            regionName.JRLC,
            regionName.JRBFC
        }, {
            regionName.JR: lambda state: state.has(itemName.WARPJR1, player),
            regionName.JRAT: lambda state: state.has(itemName.WARPJR2, player) and rules.air_pit_from_jrl_warp_pads(state),
            regionName.JRSS: lambda state: state.has(itemName.WARPJR3, player) and rules.air_pit_from_jrl_warp_pads(state),
            regionName.JRLC: lambda state: state.has(itemName.WARPJR5, player) and rules.air_pit_from_jrl_warp_pads(state),
            regionName.JRBFC: lambda state: state.has(itemName.WARPJR4, player) and rules.air_pit_from_jrl_warp_pads(state),
        })

    region_HP = self.get_region(regionName.HP)
    region_HP.add_exits({regionName.MTKS, regionName.JR, regionName.CHUFFY}, {
                            regionName.MTKS: lambda state: rules.HFP_to_MT(state),
                            regionName.JR: lambda state: rules.HFP_to_JRL(state),
                            regionName.CHUFFY: lambda state: rules.hfp_to_chuffy(state),
                        })

    region_IOHWL = self.get_region(regionName.IOHWL)
    region_IOHWL.add_exits({
        regionName.IOHPGU,
        regionName.IOHQM,
        regionName.TDLE,
        regionName.CCLE,
        regionName.IHSILOS
    }, {
        regionName.IOHPGU: lambda state: rules.WL_to_PGU(state),
        regionName.IOHQM: lambda state: rules.springy_step_shoes(state),
        regionName.TDLE: lambda state: rules.tdl_jiggy(state),
        regionName.CCLE: lambda state: rules.ccl_jiggy(state),
        regionName.IHSILOS: lambda state: state.has(itemName.SILOIOHWL, player)
    })

    region_TL = self.get_region(regionName.TL)
    region_TL.add_exits({
        regionName.TL_HATCH,
        regionName.TLTOP,
        regionName.WW,
        regionName.CHUFFY,
        regionName.WWA51NESTS,
        regionName.TLIMTOP
    }, {
        regionName.WW: lambda state: rules.TDL_to_WW(state),
        regionName.CHUFFY: lambda state: rules.tdl_to_chuffy(state),
        regionName.TL_HATCH: lambda state: rules.tdl_to_hatch(state),
        regionName.WWA51NESTS: lambda state: rules.a51_nests_from_TDL(state),
        regionName.TLTOP: lambda state: rules.tdl_to_tdl_top(state),
        regionName.TLIMTOP: lambda state: rules.inside_the_mountain_to_top(state),
    })

    region_TLIMTOP = self.get_region(regionName.TLIMTOP)
    region_TLIMTOP.add_exits({regionName.TL, regionName.TLBOSS}, {
                                regionName.TLBOSS: lambda state: rules.inside_the_mountain_to_terry(state),
                            })

    region_TLBOSS = self.get_region(regionName.TLBOSS)
    region_TLBOSS.add_exits({regionName.TLIMTOP}, {})

    region_TLTOP = self.get_region(regionName.TLTOP)
    region_TLTOP.add_exits({regionName.TLSP}, {
                            regionName.TLSP: lambda state: rules.can_cross_bonfire_cavern(state),
                        })

    region_TLSP = self.get_region(regionName.TLSP)
    region_TLSP.add_exits({regionName.TLTOP}, {
                         regionName.TLTOP: lambda state: rules.can_cross_bonfire_cavern(state),
                         })

    if self.options.randomize_warp_pads.value:
        region_TL.add_exits({regionName.TLWARP}, {
            regionName.TLWARP: lambda state: rules.tdl_to_warp_pads(state),
        })
        region_TLTOP.add_exits({regionName.TLWARP}, {
            regionName.TLWARP: lambda state: state.has(itemName.WARPTL5, player),
        })
        region_TLSP.add_exits({regionName.TLWARP}, {
            regionName.TLWARP: lambda state: state.has(itemName.WARPTL2, player),
        })
        region_TLWARP = self.get_region(regionName.TLWARP)
        region_TLWARP.add_exits({regionName.TL, regionName.TLSP, regionName.TLTOP}, {
            regionName.TL: lambda state: state.has(itemName.WARPTL1, player)
                or state.has(itemName.WARPTL3, player)
                or state.has(itemName.WARPTL4, player),
            regionName.TLTOP: lambda state: state.has(itemName.WARPTL5, player),
            regionName.TLSP: lambda state: state.has(itemName.WARPTL2, player),
        })

    region_QM = self.get_region(regionName.IOHQM)
    region_QM.add_exits({regionName.GIE, regionName.IOHWL, regionName.CKE, regionName.IHSILOS}, {
                          regionName.GIE: lambda state: rules.gi_jiggy(state),
                          regionName.IOHWL: lambda state: rules.QM_to_WL(state),
                          regionName.CKE: lambda state: rules.quag_to_CK(state),
                          regionName.IHSILOS: lambda state: state.has(itemName.SILOIOHQM, player)
                        })

    region_GIO = self.get_region(regionName.GIO)
    region_GIO.add_exits({regionName.GI1, regionName.GIOB, regionName.GIF}, {
                        regionName.GI1: lambda state: rules.outside_gi_to_floor1(state),
                         regionName.GIOB: lambda state: rules.outside_gi_to_outside_back(state),
                         regionName.GIF: lambda state: rules.outside_gi_to_flight(state)})

    region_GIOB = self.get_region(regionName.GIOB)
    region_GIOB.add_exits({regionName.GIO, regionName.GI2, regionName.GI3, regionName.GI4, regionName.GIF}, {
                            regionName.GIO: lambda state: rules.climb(state),
                            regionName.GI2: lambda state: rules.outside_gi_back_to_floor2(state),
                            regionName.GI3: lambda state: rules.outside_gi_back_to_floor_3(state),
                            regionName.GI4: lambda state: rules.outside_gi_back_to_floor_4(state),
                            regionName.GIF: lambda state: rules.outside_gi_back_to_flight(state)
                         })

    region_GIES = self.get_region(regionName.GIES)
    region_GIES.add_exits({regionName.GI1, regionName.GI2EM, regionName.GI3B, regionName.GI4B}, {
                            regionName.GI1: lambda state: rules.elevator_shaft_to_floor_1(state),
                            regionName.GI2EM: lambda state: rules.elevator_shaft_to_em(state),
                            regionName.GI3B: lambda state: rules.elevator_shaft_to_boiler_plant(state),
                            regionName.GI4B: lambda state: rules.elevator_shaft_to_floor_4(state)})

    region_GI1 = self.get_region(regionName.GI1)
    region_GI1.add_exits({regionName.GIO, regionName.GIES, regionName.GI2, regionName.CHUFFY}, {
                        regionName.GIO: lambda state: rules.split_up(state) or self.options.open_gi_frontdoor.value,
                        regionName.GI2: lambda state: rules.F1_to_F2(state),
                        regionName.CHUFFY: lambda state: rules.gi_to_chuffy(state),
                        })

    region_GI2 = self.get_region(regionName.GI2)
    region_GI2.add_exits({regionName.GIOB, regionName.GI1, regionName.GI2EM, regionName.GI3}, {
                            regionName.GI1: lambda state: rules.F2_to_F1(state),
                            regionName.GI2EM: lambda state: rules.floor_2_to_em_room(state),
                            regionName.GI3: lambda state: rules.F2_to_F3(state),
                         })

    region_GI2EM = self.get_region(regionName.GI2EM)
    region_GI2EM.add_exits({regionName.GIES}, {
                            regionName.GIES: lambda state: rules.floor_2_em_room_to_elevator_shaft(state)
                        })

    region_GI3 = self.get_region(regionName.GI3)
    region_GI3.add_exits({regionName.GIOB, regionName.GI2, regionName.GI3B, regionName.GI4}, {
                            regionName.GIOB: lambda state: rules.floor_3_to_outside_back(state),
                            regionName.GI2: lambda state: rules.F3_to_F2(state),
                            regionName.GI3B: lambda state: rules.floor_3_to_boiler_plant(state),
                            regionName.GI4: lambda state: rules.F3_to_F4(state),
                            })

    region_GI3B = self.get_region(regionName.GI3B)
    region_GI3B.add_exits({regionName.GI3, regionName.GIES}, {
                            regionName.GIES: lambda state: rules.elevator_door(state),
                          })

    region_GI4 = self.get_region(regionName.GI4)
    region_GI4.add_exits({regionName.GIOB, regionName.GI3, regionName.GI4B}, {
                            regionName.GIOB: lambda state: rules.floor_4_to_outside_back(state),
                            regionName.GI3: lambda state: rules.floor_4_to_floor_3(state),
                            regionName.GI4B: lambda state: rules.floor_4_to_floor_4_back(state),
                            })

    region_GI4B = self.get_region(regionName.GI4B)
    region_GI4B.add_exits({regionName.GIES, regionName.GI4}, {
                            regionName.GIES: lambda state: rules.floor_4_back_to_elevator_shaft(state)
                            })

    region_GIF = self.get_region(regionName.GIF)
    region_GIF.add_exits({
        regionName.GIO,
        regionName.GIOB,
        regionName.GI1,
        regionName.GI3,
        regionName.GI3B,
        regionName.GI4,
        regionName.GI5,
        regionName.GIR
    }, {
        regionName.GI1: lambda state: rules.flight_to_floor_1(state),
        regionName.GI3B: lambda state: rules.flight_to_boiler_plant(state)
    })

    region_GIR = self.get_region(regionName.GIR)
    region_GIR.add_exits({
        regionName.GIO,
        regionName.GIOB,
        regionName.GIF,
        regionName.GI3,
        regionName.GI4,
        regionName.GI5,
    }, {
        regionName.GIO: lambda state: rules.roof_to_ground_level(state),
        regionName.GIOB: lambda state: rules.roof_to_ground_level(state),
        regionName.GIF: lambda state: rules.flight_pad(state),
        regionName.GI3: lambda state: rules.roof_to_upper_floors(state),
        regionName.GI4: lambda state: rules.roof_to_upper_floors(state),
        regionName.GI5: lambda state: rules.roof_to_floor5(state),
    })

    if self.options.randomize_warp_pads.value:
        region_GI1.add_exits({regionName.GIWARP}, {
            regionName.GIWARP: lambda state: (rules.split_up(state) or self.options.open_gi_frontdoor.value) and state.has(itemName.WARPGI1, player),
        })
        region_GI2.add_exits({regionName.GIWARP}, {
            regionName.GIWARP: lambda state: state.has(itemName.WARPGI2, player)
        })
        region_GI3.add_exits({regionName.GIWARP}, {
            regionName.GIWARP: lambda state: rules.small_elevation(state) and state.has(itemName.WARPGI3, player)
        })
        region_GI4.add_exits({regionName.GIWARP}, {
            regionName.GIWARP: lambda state: rules.warp_pad_floor_4(state) and state.has(itemName.WARPGI4, player)
        })
        region_GIR.add_exits({regionName.GIWARP}, {
            regionName.GIWARP: lambda state: state.has(itemName.WARPGI5, player)
        })
        region_GIWARP = self.get_region(regionName.GIWARP)
        # Warping to floor 1 does nothing to the logic, since you're stuck between 2 doors.
        region_GIWARP.add_exits({regionName.GI2, regionName.GI3, regionName.GI4, regionName.GIR}, {
            regionName.GI2: lambda state: state.has(itemName.WARPGI2, player),
            regionName.GI3: lambda state: state.has(itemName.WARPGI3, player),
            regionName.GI4: lambda state: state.has(itemName.WARPGI4, player),
            regionName.GIR: lambda state: state.has(itemName.WARPGI5, player),
        })

    region_CK = self.get_region(regionName.CK)
    region_CK.add_exits({regionName.H1},
                        {regionName.H1: lambda state: rules.check_hag1_options(state)})

    region_chuffy = self.get_region(regionName.CHUFFY)
    region_chuffy.add_exits({
        regionName.GM,
        regionName.WW,
        regionName.IOHCT,
        regionName.TL,
        regionName.GI1,
        regionName.HP
    }, {
        regionName.GM: lambda state: rules.can_beat_king_coal(state),
        regionName.WW: lambda state: state.has(itemName.TRAINSWWW, player) and rules.can_beat_king_coal(state),
        regionName.IOHCT: lambda state: state.has(itemName.TRAINSWIH, player) and rules.can_beat_king_coal(state),
        regionName.TL: lambda state: state.has(itemName.TRAINSWTD, player) and rules.can_beat_king_coal(state),
        regionName.GI1: lambda state: state.has(itemName.TRAINSWGI, player) and rules.can_beat_king_coal(state),
        regionName.HP: lambda state: state.has(itemName.TRAINSWHP1, player) and rules.can_beat_king_coal(state)
    })

    region_mt_entrance = self.get_region(regionName.MTE)
    region_mt_entrance.add_exits({regionName.IOHWH}, {regionName.IOHWH: lambda state: rules.MT_to_WH(state)})

    region_ggm_entrance = self.get_region(regionName.GGME)
    region_ggm_entrance.add_exits({regionName.IOHPL}, {
        regionName.IOHPL: lambda state: rules.escape_ggm_loading_zone(state)
        })

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

    region_ioh_silos = self.get_region(regionName.IHSILOS)
    region_ioh_silos.add_exits({
        regionName.IOHJV,
        regionName.IOHWH,
        regionName.IOHPL,
        regionName.IOHPG,
        regionName.IOHCT,
        regionName.IOHWL,
        regionName.IOHQM
    }, {
        regionName.IOHJV: lambda state: state.has(itemName.SILOIOHJV, player),
        regionName.IOHWH: lambda state: state.has(itemName.SILOIOHWH, player),
        regionName.IOHPL: lambda state: state.has(itemName.SILOIOHPL, player),
        regionName.IOHPG: lambda state: state.has(itemName.SILOIOHPG, player),
        regionName.IOHCT: lambda state: state.has(itemName.SILOIOHCT, player),
        regionName.IOHWL: lambda state: state.has(itemName.SILOIOHWL, player),
        regionName.IOHQM: lambda state: state.has(itemName.SILOIOHQM, player),
    })

    @dataclass
    class IndirectTransitionCondition:
        source: str
        destination: str
        regions_in_rules: List[str]

    # Read this to know what this code does.
    # https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/apworld_dev_faq.md#i-learned-about-indirect-conditions-in-the-world-api-document-but-i-want-to-know-more-what-are-they-and-why-are-they-necessary
    def add_indirect_condition(condition: IndirectTransitionCondition):
        source_region = self.get_region(condition.source)
        entrance = next(e for e in source_region.exits if e.connected_region.name == condition.destination)
        for rule_region_name in condition.regions_in_rules:
            self.multiworld.register_indirect_condition(self.get_region(rule_region_name), entrance)

    # World entrance randomisation (and exits)
    lookup_table = {
            regionName.MT: regionName.MTE,
            regionName.GM: regionName.GGME,
            regionName.WW: regionName.WWE,
            regionName.JR: regionName.JRLE,
            regionName.TL: regionName.TDLE,
            regionName.GIO: regionName.GIE,
            regionName.HP: regionName.HFPE,
            regionName.CC: regionName.CCLE,
            regionName.CK: regionName.CKE,
            regionName.MTBOSS: regionName.MTTT,
            regionName.GMBOSS: regionName.CHUFFY,
            regionName.WWBOSS: regionName.WW,
            regionName.JRBOSS: regionName.JRLC,
            regionName.TLBOSS: regionName.TLTOP,
            regionName.GIBOSS: regionName.GI1,
            regionName.HPFBOSS: regionName.HP,
            regionName.HPIBOSS: regionName.HP,
            regionName.CCBOSS: regionName.CC,
        }

    # World Entrances
    for source, destination in self.loading_zones.items():
        if source in [
            regionName.MT,
            regionName.GM,
            regionName.WW,
            regionName.JR,
            regionName.TL,
            regionName.GIO,
            regionName.HP,
            regionName.CC,
            regionName.CK
        ]:
            overworld_entrance = lookup_table[source]

            source_region = self.get_region(overworld_entrance)
            source_region.add_exits({destination})

            region_actual_world_entrance = self.get_region(destination)

            if destination == regionName.GM:
                region_actual_world_entrance.add_exits({overworld_entrance}, {
                    overworld_entrance: lambda state: rules.GGM_to_PL(state)
                })
            else:
                region_actual_world_entrance.add_exits({overworld_entrance})

    # Boss Entrances
    for source, boss_room in self.loading_zones.items():
        if source in [
            regionName.MTBOSS,
            regionName.GMBOSS,
            regionName.WWBOSS,
            regionName.JRBOSS,
            regionName.TLBOSS,
            regionName.GIBOSS,
            regionName.HPFBOSS,
            regionName.HPIBOSS,
            regionName.CCBOSS
        ]:


            if source == regionName.MTBOSS:
                source_rule = lambda state: rules.has_green_relics(state, 20)
            elif source == regionName.JRBOSS:
                source_rule = lambda state: ((rules.grenade_eggs_item(state) or rules.clockwork_eggs_item(state)) and rules.sub_aqua_egg_aiming(state)) \
                    or rules.humbaJRL(state)\
                    or rules.talon_torpedo(state)
            elif source == regionName.GIBOSS:
                source_rule = lambda state: rules.can_enter_gi_repair_depot(state)
            elif source == regionName.HPFBOSS:
                source_rule = lambda state: rules.flight_pad(state)
            elif source == regionName.HPIBOSS:
                source_rule = lambda state: rules.can_reach_hfp_ice_crater(state)
            else:
                source_rule = lambda state: True

            if boss_room == regionName.MTBOSS:
                boss_room_rule = lambda state: rules.breegull_blaster(state)
            elif boss_room == regionName.WWBOSS:
                boss_room_rule = lambda state: rules.can_enter_big_top(state)
            elif boss_room == regionName.JRBOSS:
                boss_room_rule = lambda state: rules.sub_aqua_egg_aiming(state) and rules.grenade_eggs_item(state)
            elif boss_room == regionName.GIBOSS:
                boss_room_rule = lambda state: rules.grenade_eggs_item(state)
            elif boss_room == regionName.HPFBOSS:
                boss_room_rule = lambda state: rules.ice_eggs_item(state)
            else:
                boss_room_rule = lambda state: True

            boss_entrance = lookup_table[source]
            source_region = self.get_region(boss_entrance)
            transition_rule = lambda state, sr = source_rule, brr = boss_room_rule: sr(state) and brr(state)
            source_region.add_exits({boss_room}, {boss_room: transition_rule})

            # Davie Jones' locker can be opened with the submarine.
            if source == regionName.JRBOSS:
                add_indirect_condition(IndirectTransitionCondition(boss_entrance, boss_room, [regionName.JRAT]))

            # Entering Repair Depot is a very convoluted process.
            if source == regionName.GIBOSS:
                add_indirect_condition(IndirectTransitionCondition(boss_entrance, boss_room, [regionName.GI3]))

            # Terry's nest has 2 loading zones, one of them not randomised, so leaving Terry's nest is logically relevant.
            if boss_room == regionName.TLBOSS:
                terry_nest_region = self.get_region(regionName.TLBOSS)

                if source == regionName.MTBOSS:
                    leave_terry_rule = lambda state: rules.breegull_blaster(state)
                    terry_nest_region.add_exits({boss_entrance}, {boss_entrance: leave_terry_rule})

                elif source ==regionName.GMBOSS:
                    leave_terry_rule = lambda state: rules.train_raised(state)
                    terry_nest_region.add_exits({boss_entrance}, {boss_entrance: leave_terry_rule})
                    add_indirect_condition(IndirectTransitionCondition(boss_room, boss_entrance, [regionName.GM]))
                else:
                    terry_nest_region.add_exits({boss_entrance}, {})

    static_indirect_transition_conditions: List[IndirectTransitionCondition] = [
        IndirectTransitionCondition(regionName.MT, regionName.MTKS, [regionName.MTJSG]),
        IndirectTransitionCondition(regionName.GIO, regionName.GIF, [regionName.GI2, regionName.GI4]),
        IndirectTransitionCondition(regionName.GIOB, regionName.GIF, [regionName.GI2, regionName.GI4]),
        IndirectTransitionCondition(regionName.HP, regionName.JR, [regionName.CC]),
        IndirectTransitionCondition(regionName.JRSS, regionName.JRAT, [regionName.JRAT]),
        IndirectTransitionCondition(regionName.JRSS, regionName.JRLC, [regionName.JRAT]),
        IndirectTransitionCondition(regionName.JRLC, regionName.JRSS, [regionName.JRAT]),
        IndirectTransitionCondition(regionName.JRLC, regionName.JRBFC, [regionName.JRAT]),
        IndirectTransitionCondition(regionName.JRBFC, regionName.JRLC, [regionName.JRAT]),
        IndirectTransitionCondition(regionName.WW, regionName.CHUFFY, [regionName.GM, regionName.GMBOSS]),
        IndirectTransitionCondition(regionName.TL, regionName.CHUFFY, [regionName.GM, regionName.GMBOSS]),
        IndirectTransitionCondition(regionName.GI1, regionName.CHUFFY, [regionName.GM, regionName.GMBOSS]),
        IndirectTransitionCondition(regionName.HP, regionName.CHUFFY, [regionName.GM, regionName.GMBOSS]),
        IndirectTransitionCondition(regionName.IOHCT, regionName.CHUFFY, [regionName.GM, regionName.GMBOSS]),
        IndirectTransitionCondition(regionName.CHUFFY, regionName.GM, [regionName.GMBOSS]),
        IndirectTransitionCondition(regionName.CHUFFY, regionName.WW, [regionName.GMBOSS]),
        IndirectTransitionCondition(regionName.CHUFFY, regionName.TL, [regionName.GMBOSS]),
        IndirectTransitionCondition(regionName.CHUFFY, regionName.GI1, [regionName.GMBOSS]),
        IndirectTransitionCondition(regionName.CHUFFY, regionName.HP, [regionName.GMBOSS]),
        IndirectTransitionCondition(regionName.CHUFFY, regionName.IOHCT, [regionName.GMBOSS]),
        IndirectTransitionCondition(regionName.TLIMTOP, regionName.TLBOSS, [regionName.TL, regionName.TLSP]),
        IndirectTransitionCondition(regionName.TL, regionName.TLTOP, [regionName.TLBOSS]),
        IndirectTransitionCondition(regionName.WW, regionName.TL, [regionName.WWI])
    ]

    for definition in static_indirect_transition_conditions:
        add_indirect_condition(definition)
