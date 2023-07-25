from typing import List, TypedDict


room_table: List[str] = [
    "D01Z01S01", # THL
    "D01Z01S02", # THL
    "D01Z01S03", # THL
    "D01Z01S07", # THL
    "D01Z02S01", # Albero
    "D01Z02S02", # Albero
    "D01Z02S03", # Albero
    "D01Z02S04", # Albero
    "D01Z02S05", # Albero
    "D01Z02S06", # Albero
    "D01Z02S07", # Albero
    "D01BZ04S01", # Albero Church
    "D01BZ06S01", # Ossuary
    "D01BZ08S01", # Ossuary - isidora's room?
    "D01Z03S01", # WotBC
    "D01Z03S02", # WotBC
    "D01Z03S03", # WotBC
    "D01Z03S04", # WotBC
    "D01Z03S05", # WotBC
    "D01Z03S06", # WotBC
    "D01Z03S07", # WotBC
    "D01Z04S01", # MD
    "D01Z04S02", # MD
    "D01Z04S03", # MD
    "D01Z04S05", # MD
    "D01Z04S06", # MD
    "D01Z04S07", # MD
    "D01Z04S08", # MD
    "D01Z04S09", # MD
    "D01Z04S10", # MD
    "D01Z04S11", # MD
    "D01Z04S12", # MD
    "D01Z04S13", # MD
    "D01Z04S14", # MD
    "D01Z04S15", # MD
    "D01Z04S16", # MD
    "D01Z04S17", # MD
    "D01Z04S18", # MD
    "D01Z04S19", # MD
    "D01BZ02S01", # MD - shop
    "D01Z05S01", # DC
    "D01Z05S02", # DC
    "D01Z05S03", # DC
    "D01Z05S04", # DC
    "D01Z05S05", # DC
    "D01Z05S06", # DC
    "D01Z05S07", # DC
    "D01Z05S08", # DC
    "D01Z05S09", # DC
    "D01Z05S10", # DC
    "D01Z05S11", # DC
    "D01Z05S12", # DC
    "D01Z05S13", # DC
    "D01Z05S14", # DC
    "D01Z05S15", # DC
    "D01Z05S16", # DC
    "D01Z05S17", # DC
    "D01Z05S18", # DC
    "D01Z05S19", # DC
    "D01Z05S20", # DC
    "D01Z05S21", # DC
    "D01Z05S22", # DC
    "D01Z05S23", # DC
    "D01Z05S24", # DC
    "D01Z05S25", # DC
    "D01Z05S26", # DC
    "D01Z05S27", # DC
    "D01BZ05S01", # DC - shroud of dreamt sins room?
    "D01BZ09S01", # DC - arcade room
    "D01Z06S01", # Petrous
    "D01BZ07S01", # Petrous - Jibrael
    "D02Z01S01", # WOTW
    "D02Z01S02", # WOTW
    "D02Z01S03", # WOTW
    "D02Z01S04", # WOTW
    "D02Z01S05", # WOTW
    "D02Z01S06", # WOTW
    "D02Z01S08", # WOTW
    "D02Z01S09", # WOTW
    "D02Z02S01", # GOTP
    "D02Z02S02", # GOTP
    "D02Z02S03", # GOTP
    "D02Z02S04", # GOTP
    "D02Z02S05", # GOTP
    "D02Z02S06", # GOTP
    "D02Z02S07", # GOTP
    "D02Z02S08", # GOTP
    "D02Z02S09", # GOTP
    "D02Z02S10", # GOTP
    "D02Z02S11", # GOTP
    "D02Z02S12", # GOTP
    "D02Z02S13", # GOTP
    "D02Z02S14", # GOTP
    "D02BZ02S01", # GOTP - shop
    "D02Z03S01", # COOLOTCV
    "D02Z03S02", # COOLOTCV
    "D02Z03S03", # COOLOTCV
    "D02Z03S05", # COOLOTCV
    "D02Z03S06", # COOLOTCV
    "D02Z03S07", # COOLOTCV
    "D02Z03S08", # COOLOTCV
    "D02Z03S09", # COOLOTCV
    "D02Z03S10", # COOLOTCV
    "D02Z03S11", # COOLOTCV
    "D02Z03S12", # COOLOTCV
    "D02Z03S13", # COOLOTCV
    "D02Z03S14", # COOLOTCV
    "D02Z03S15", # COOLOTCV
    "D02Z03S16", # COOLOTCV
    "D02Z03S17", # COOLOTCV
    "D02Z03S18", # COOLOTCV
    "D02Z03S19", # COOLOTCV
    "D02Z03S20", # COOLOTCV
    "D02Z03S21", # COOLOTCV
    "D02Z03S22", # COOLOTCV
    "D02Z03S23", # COOLOTCV
    "D02Z03S24", # COOLOTCV
    "D03Z01S01", # MOTED
    "D03Z01S02", # MOTED
    "D03Z01S03", # MOTED
    "D03Z01S04", # MOTED
    "D03Z01S05", # MOTED
    "D03Z01S06", # MOTED
    "D03Z02S01", # Jondo
    "D03Z02S02", # Jondo
    "D03Z02S03", # Jondo
    "D03Z02S04", # Jondo
    "D03Z02S05", # Jondo
    "D03Z02S06", # Jondo
    "D03Z02S07", # Jondo
    "D03Z02S08", # Jondo
    "D03Z02S09", # Jondo
    "D03Z02S10", # Jondo
    "D03Z02S11", # Jondo
    "D03Z02S12", # Jondo
    "D03Z02S13", # Jondo
    "D03Z02S14", # Jondo
    "D03Z02S15", # Jondo
    "D03Z03S01", # GA
    "D03Z03S02", # GA
    "D03Z03S03", # GA
    "D03Z03S04", # GA
    "D03Z03S05", # GA
    "D03Z03S06", # GA
    "D03Z03S07", # GA
    "D03Z03S08", # GA
    "D03Z03S09", # GA
    "D03Z03S10", # GA
    "D03Z03S11", # GA
    "D03Z03S12", # GA
    "D03Z03S13", # GA
    "D03Z03S14", # GA
    "D03Z03S15", # GA
    "D03Z03S16", # GA
    "D03Z03S17", # GA
    "D03Z03S18", # GA
    "D03Z03S19", # GA
    "D04Z01S01", # POTSS
    "D04Z01S02", # POTSS
    "D04Z01S03", # POTSS
    "D04Z01S04", # POTSS
    "D04Z01S05", # POTSS
    "D04Z01S06", # POTSS
    "D04Z02S01", # MOM
    "D04Z02S02", # MOM
    "D04Z02S03", # MOM
    "D04Z02S04", # MOM
    "D04Z02S05", # MOM
    "D04Z02S06", # MOM
    "D04Z02S07", # MOM
    "D04Z02S08", # MOM
    "D04Z02S09", # MOM
    "D04Z02S10", # MOM
    "D04Z02S11", # MOM
    "D04Z02S12", # MOM
    "D04Z02S13", # MOM
    "D04Z02S14", # MOM
    "D04Z02S15", # MOM
    "D04Z02S16", # MOM
    "D04Z02S17", # MOM
    "D04Z02S19", # MOM
    "D04Z02S20", # MOM
    "D04Z02S21", # MOM
    "D04Z02S22", # MOM
    "D04Z02S23", # MOM
    "D04Z02S24", # MOM
    "D04Z02S25", # MOM
    "D04BZ02S01", # MOM - Redento
    "D04Z03S01", # KOTTW
    "D04Z03S02", # KOTTW
    "D04Z04S01", # ATTOTS
    "D04Z04S02", # ATTOTS
    "D05Z01S01", # LOTNW
    "D05Z01S02", # LOTNW
    "D05Z01S03", # LOTNW
    "D05Z01S04", # LOTNW
    "D05Z01S05", # LOTNW
    "D05Z01S06", # LOTNW
    "D05Z01S07", # LOTNW
    "D05Z01S08", # LOTNW
    "D05Z01S09", # LOTNW
    "D05Z01S10", # LOTNW
    "D05Z01S11", # LOTNW
    "D05Z01S12", # LOTNW
    "D05Z01S13", # LOTNW
    "D05Z01S14", # LOTNW
    "D05Z01S15", # LOTNW
    "D05Z01S16", # LOTNW
    "D05Z01S17", # LOTNW
    "D05Z01S18", # LOTNW
    "D05Z01S19", # LOTNW
    "D05Z01S20", # LOTNW
    "D05Z01S21", # LOTNW
    "D05Z01S22", # LOTNW
    "D05Z01S23", # LOTNW
    "D05Z01S24", # LOTNW
    "D05BZ01S01", # LOTNW - secret entrance to KOTTW?
    "D05Z02S01", # TSC
    "D05Z02S02", # TSC
    "D05Z02S03", # TSC
    "D05Z02S04", # TSC
    "D05Z02S05", # TSC
    "D05Z02S06", # TSC
    "D05Z02S07", # TSC
    "D05Z02S08", # TSC
    "D05Z02S09", # TSC
    "D05Z02S10", # TSC
    "D05Z02S11", # TSC
    "D05Z02S12", # TSC
    "D05Z02S13", # TSC
    "D05Z02S14", # TSC
    "D05Z02S15", # TSC
    "D05BZ02S01", # TSC - shop
    "D06Z01S01", # AR
    "D06Z01S02", # AR
    "D06Z01S03", # AR
    "D06Z01S04", # AR
    "D06Z01S05", # AR
    "D06Z01S06", # AR
    "D06Z01S07", # AR
    "D06Z01S08", # AR
    "D06Z01S09", # AR
    "D06Z01S10", # AR
    "D06Z01S11", # AR
    "D06Z01S12", # AR
    "D06Z01S13", # AR
    "D06Z01S14", # AR
    "D06Z01S15", # AR
    "D06Z01S16", # AR
    "D06Z01S17", # AR
    "D06Z01S18", # AR
    "D06Z01S19", # AR
    "D06Z01S20", # AR
    "D06Z01S21", # AR
    "D06Z01S22", # AR
    "D06Z01S23", # AR
    "D06Z01S24", # AR
    "D06Z01S25", # AR
    "D06Z01S26", # AR
    "D07Z01S01", # DOHH?
    "D07Z01S02", # DOHH?
    "D07Z01S03", # DOHH?
    "D08Z01S01", # BOTTC
    "D08Z01S02", # BOTTC
    "D08Z02S01", # FT
    "D08Z02S02", # FT
    "D08Z02S03", # FT
    "D08Z03S01", # HOTD
    "D08Z03S02", # HOTD
    "D08Z03S03", # HOTD
    "D09Z01S01", # WOTHP
    "D09Z01S02", # WOTHP
    "D09Z01S03", # WOTHP
    "D09Z01S04", # WOTHP
    "D09Z01S05", # WOTHP
    "D09Z01S06", # WOTHP
    "D09Z01S07", # WOTHP
    "D09Z01S08", # WOTHP
    "D09Z01S09", # WOTHP
    "D09Z01S10", # WOTHP
    "D09Z01S11", # WOTHP
    "D09Z01S12", # WOTHP
    "D09Z01S13", # WOTHP
    "D09BZ01S01", # WOTHP - all cells
    "D17Z01S01", # BOTSS
    "D17Z01S02", # BOTSS
    "D17Z01S03", # BOTSS
    "D17Z01S04", # BOTSS
    "D17Z01S05", # BOTSS
    "D17Z01S06", # BOTSS
    "D17Z01S07", # BOTSS
    "D17Z01S08", # BOTSS
    "D17Z01S09", # BOTSS
    "D17Z01S10", # BOTSS
    "D17Z01S11", # BOTSS
    "D17Z01S12", # BOTSS
    "D17Z01S13", # BOTSS
    "D17Z01S14", # BOTSS
    "D17Z01S15", # BOTSS
    "D17BZ01S01", # BOTSS - chamber of the eldest brother
    "D17BZ02S01", # BOTSS - platforming challenge
    "D20Z01S01", # EOS
    "D20Z01S02", # EOS
    "D20Z01S03", # EOS
    "D20Z01S04", # EOS
    "D20Z01S05", # EOS
    "D20Z01S06", # EOS
    "D20Z01S07", # EOS
    "D20Z01S08", # EOS
    "D20Z01S09", # EOS
    "D20Z01S10", # EOS
    "D20Z01S11", # EOS
    "D20Z01S12", # EOS
    "D20Z01S13", # EOS
    "D20Z01S14", # EOS
    "D20Z02S01", # MAH
    "D20Z02S02", # MAH
    "D20Z02S03", # MAH
    "D20Z02S04", # MAH
    "D20Z02S05", # MAH
    "D20Z02S06", # MAH
    "D20Z02S07", # MAH
    "D20Z02S08", # MAH
    "D20Z02S09", # MAH
    "D20Z02S10", # MAH
    "D20Z02S11", # MAH
    "D20Z02S12", # MAH
    "D20Z03S01", # TRPOTS
]


class DoorDict(TypedDict, total=False):
    Id: str
    Direction: int
    OriginalDoor: str
    Type: int
    Logic: str
    VisibilityFlags: int
    RequiredDoors: List[str]


door_table: List[DoorDict] = [
	{
		"Id": "D01Z01S01[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z01S07[E]"
	},
	{
		"Id": "D01Z01S01[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z01S02[W]"
	},
	{
		"Id": "D01Z01S01[S]",
		"Direction": 2,
		"OriginalDoor": "D01Z06S01[N]",
		"Type": 1,
		"Logic": "D01Z01S01[S] || canBreakHoles || doubleJump"
	},
	{
		"Id": "D01Z01S02[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z01S01[E]"
	},
	{
		"Id": "D01Z01S02[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z01S03[W]"
	},
	{
		"Id": "D01Z01S03[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z01S02[E]"
	},
	{
		"Id": "D01Z01S03[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z02S01[W]",
		"Type": 1
	},
	{
		"Id": "D01Z01S07[W]",
		"Direction": 1,
		"OriginalDoor": "D17Z01S03[E]",
		"Type": 1
	},
	{
		"Id": "D01Z01S07[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z01S01[W]"
	},

	{
		"Id": "D01Z02S01[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z01S03[E]",
		"Type": 1
	},
	{
		"Id": "D01Z02S01[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z02S02[W]"
	},
	{
		"Id": "D01Z02S02[SW]",
		"Direction": 1,
		"OriginalDoor": "D01Z02S06[E]"
	},
	{
		"Id": "D01Z02S02[SE]",
		"Direction": 2,
		"OriginalDoor": "D01Z02S04[W]"
	},
	{
		"Id": "D01Z02S02[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z02S01[E]"
	},
	{
		"Id": "D01Z02S02[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z02S03[W]"
	},
	{
		"Id": "D01Z02S02[NE]",
		"Direction": 2,
		"OriginalDoor": "D01Z02S03[NW]"
	},
	{
		"Id": "D01Z02S03[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z02S02[E]"
	},
	{
		"Id": "D01Z02S03[NW]",
		"Direction": 1,
		"OriginalDoor": "D01Z02S02[NE]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D02Z02S11[NW]", "D02Z02S11[NE]", "D02Z02S11[W]", "D02Z02S11[E]", "D02Z02S11[SE]" ]
	},
	{
		"Id": "D01Z02S03[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z02S05[W]"
	},
	{
		"Id": "D01Z02S03[church]",
		"Direction": 4,
		"OriginalDoor": "D01BZ04S01[church]",
		"Logic": "canBeatMercyBoss || canBeatConventBoss || canBeatGrievanceBoss"
	},
	{
		"Id": "D01Z02S03[Cherubs]",
		"Direction": 5
	},
	{
		"Id": "D01Z02S04[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z02S02[SE]"
	},
	{
		"Id": "D01Z02S04[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S01[N]",
		"Type": 1
	},
	{
		"Id": "D01Z02S04[Ossary]",
		"Direction": 4,
		"OriginalDoor": "D01BZ06S01[Ossary]"
	},
	{
		"Id": "D01Z02S05[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z02S03[E]"
	},
	{
		"Id": "D01Z02S05[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z03S01[W]",
		"Type": 1
	},
	{
		"Id": "D01Z02S06[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z02S07[E]"
	},
	{
		"Id": "D01Z02S06[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z02S02[SW]"
	},
	{
		"Id": "D01Z02S07[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z02S06[W]"
	},
	{
		"Id": "D01BZ04S01[church]",
		"Direction": 7,
		"OriginalDoor": "D01Z02S03[church]"
	},
	{
		"Id": "D01BZ06S01[Ossary]",
		"Direction": 7,
		"OriginalDoor": "D01Z02S04[Ossary]"
	},
	{
		"Id": "D01BZ06S01[E]",
		"Direction": 2,
		"OriginalDoor": "D01BZ08S01[W]",
		"Logic": "bones >= 30"
	},
	{
		"Id": "D01BZ08S01[W]",
		"Direction": 1,
		"OriginalDoor": "D01BZ06S01[E]"
	},
	
	{
		"Id": "D01Z03S01[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z02S05[E]",
		"Type": 1
	},
	{
		"Id": "D01Z03S01[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z03S02[W]"
	},
	{
		"Id": "D01Z03S01[SE]",
		"Direction": 2,
		"OriginalDoor": "D01Z03S02[SW]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D01Z03S02[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z03S01[E]"
	},
	{
		"Id": "D01Z03S02[SW]",
		"Direction": 1,
		"OriginalDoor": "D01Z03S01[SE]"
	},
	{
		"Id": "D01Z03S02[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z03S03[W]"
	},
	{
		"Id": "D01Z03S02[S]",
		"Direction": 3,
		"OriginalDoor": "D01Z05S05[N]",
		"Type": 1,
		"VisibilityFlags": 1
	},
	{
		"Id": "D01Z03S03[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z03S02[E]"
	},
	{
		"Id": "D01Z03S03[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z03S04[SW]"
	},
	{
		"Id": "D01Z03S03[Cherubs]",
		"Direction": 5
	},
	{
		"Id": "D01Z03S03[-Cherubs]",
		"Direction": 6,
		"OriginalDoor": "D01Z05S06[Cherubs]",
		"Type": 1,
		"Logic": "linen"
	},
	{
		"Id": "D01Z03S04[SW]",
		"Direction": 1,
		"OriginalDoor": "D01Z03S03[E]"
	},
	{
		"Id": "D01Z03S04[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z03S07[E]"
	},
	{
		"Id": "D01Z03S04[NW]",
		"Direction": 1,
		"OriginalDoor": "D02Z01S01[SE]",
		"Type": 1
	},
	{
		"Id": "D01Z03S04[SE]",
		"Direction": 2,
		"OriginalDoor": "D01Z03S05[W]"
	},
	{
		"Id": "D01Z03S04[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z03S06[W]"
	},
	{
		"Id": "D01Z03S05[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z03S04[SE]"
	},
	{
		"Id": "D01Z03S05[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z04S01[NW]",
		"Type": 1
	},
	{
		"Id": "D01Z03S05[Cherubs]",
		"Direction": 6,
		"OriginalDoor": "D01Z05S11[Cherubs]",
		"Type": 1,
		"Logic": "linen"
	},
	{
		"Id": "D01Z03S06[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z03S04[E]"
	},
	{
		"Id": "D01Z03S06[E]",
		"Direction": 2,
		"OriginalDoor": "D08Z01S01[W]",
		"Type": 1
	},
	{
		"Id": "D01Z03S07[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z03S04[W]"
	},
	{
		"Id": "D01Z03S07[-Cherubs]",
		"Direction": 6,
		"OriginalDoor": "D01Z03S03[Cherubs]",
		"Logic": "linen"
	},
	
	{
		"Id": "D01Z04S01[NW]",
		"Direction": 1,
		"OriginalDoor": "D01Z03S05[E]",
		"Type": 1
	},
	{
		"Id": "D01Z04S01[NE]",
		"Direction": 2,
		"OriginalDoor": "D01Z04S17[W]"
	},
	{
		"Id": "D01Z04S01[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z04S03[E]"
	},
	{
		"Id": "D01Z04S01[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z04S05[NW]"
	},
	{
		"Id": "D01Z04S01[SE]",
		"Direction": 2,
		"OriginalDoor": "D01Z04S05[SW]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D01Z04S01[S]" ]
	},
	{
		"Id": "D01Z04S01[S]",
		"Direction": 3,
		"OriginalDoor": "D01Z04S15[N]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D01Z04S01[SE]" ]
	},
	{
		"Id": "D01Z04S02[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z04S13[NE]"
	},
	{
		"Id": "D01Z04S03[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z04S01[W]"
	},
	{
		"Id": "D01Z04S05[NW]",
		"Direction": 1,
		"OriginalDoor": "D01Z04S01[E]"
	},
	{
		"Id": "D01Z04S05[SW]",
		"Direction": 1,
		"OriginalDoor": "D01Z04S01[SE]"
	},
	{
		"Id": "D01Z04S06[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z04S07[W]"
	},
	{
		"Id": "D01Z04S06[NW]",
		"Direction": 1,
		"OriginalDoor": "D01Z04S15[NE]"
	},
	{
		"Id": "D01Z04S06[SW]",
		"Direction": 1,
		"OriginalDoor": "D01Z04S15[E]"
	},
	{
		"Id": "D01Z04S07[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z04S06[E]"
	},
	{
		"Id": "D01Z04S08[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z04S15[W]"
	},
	{
		"Id": "D01Z04S09[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S12[E]",
		"Type": 1,
		"Logic": "openedDCGateE"
	},
	{
		"Id": "D01Z04S09[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z04S15[SW]"
	},
	{
		"Id": "D01Z04S09[C]",
		"Direction": 4,
		"OriginalDoor": "D01BZ02S01[C]"
	},
	{
		"Id": "D01Z04S10[NW]",
		"Direction": 1,
		"OriginalDoor": "D01Z04S15[SE]"
	},
	{
		"Id": "D01Z04S10[SW]",
		"Direction": 3,
		"OriginalDoor": "D01Z04S11[NE]"
	},
	{
		"Id": "D01Z04S10[SE]",
		"Direction": 3,
		"OriginalDoor": "D01Z04S12[NW]"
	},
	{
		"Id": "D01Z04S11[NE]",
		"Direction": 0,
		"OriginalDoor": "D01Z04S10[SW]"
	},
	{
		"Id": "D01Z04S12[NW]",
		"Direction": 0,
		"OriginalDoor": "D01Z04S10[SE]"
	},
	{
		"Id": "D01Z04S12[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z04S18[E]"
	},
	{
		"Id": "D01Z04S12[SE]",
		"Direction": 2,
		"OriginalDoor": "D01Z04S13[NW]"
	},
	{
		"Id": "D01Z04S13[NW]",
		"Direction": 1,
		"OriginalDoor": "D01Z04S12[SE]"
	},
	{
		"Id": "D01Z04S13[NE]",
		"Direction": 2,
		"OriginalDoor": "D01Z04S02[W]"
	},
	{
		"Id": "D01Z04S13[SW]",
		"Direction": 1,
		"OriginalDoor": "D01Z04S14[E]"
	},
	{
		"Id": "D01Z04S13[SE]",
		"Direction": 2,
		"OriginalDoor": "D01Z04S16[W]",
		"VisibilityFlags": 5,
		"Logic": "D01Z04S13[SE] || canDiveLaser && (canAirStall || wheel || doubleJump || canEnemyBounce)"
	},
	{
		"Id": "D01Z04S14[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z04S13[SW]"
	},
	{
		"Id": "D01Z04S15[N]",
		"Direction": 0,
		"OriginalDoor": "D01Z04S01[S]"
	},
	{
		"Id": "D01Z04S15[NE]",
		"Direction": 2,
		"OriginalDoor": "D01Z04S06[NW]"
	},
	{
		"Id": "D01Z04S15[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z04S08[E]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D01Z04S15[E]", "D01Z04S15[SW]", "D01Z04S15[SE]" ]
	},
	{
		"Id": "D01Z04S15[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z04S06[SW]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D01Z04S15[W]", "D01Z04S15[SW]", "D01Z04S15[SE]" ]
	},
	{
		"Id": "D01Z04S15[SW]",
		"Direction": 1,
		"OriginalDoor": "D01Z04S09[E]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D01Z04S15[W]", "D01Z04S15[E]", "D01Z04S15[SE]" ]
	},
	{
		"Id": "D01Z04S15[SE]",
		"Direction": 2,
		"OriginalDoor": "D01Z04S10[NW]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D01Z04S15[W]", "D01Z04S15[E]", "D01Z04S15[SW]" ]
	},
	{
		"Id": "D01Z04S16[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z04S13[SE]"
	},
	{
		"Id": "D01Z04S16[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z02S12[W]",
		"Type": 1
	},
	{
		"Id": "D01Z04S17[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z04S01[NE]"
	},
	{
		"Id": "D01Z04S18[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z04S19[E]",
		"Logic": "D01Z04S18[W] || canBeatMercyBoss"
	},
	{
		"Id": "D01Z04S18[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z04S12[W]",
		"Logic": "D01Z04S18[E] || canBeatMercyBoss"
	},
	{
		"Id": "D01Z04S19[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S19[E]",
		"Type": 1
	},
	{
		"Id": "D01Z04S19[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z04S18[W]"
	},
	{
		"Id": "D01BZ02S01[C]",
		"Direction": 7,
		"OriginalDoor": "D01Z04S09[C]"
	},
	
	{
		"Id": "D01Z05S01[N]",
		"Direction": 1,
		"OriginalDoor": "D01Z02S04[E]",
		"Type": 1
	},
	{
		"Id": "D01Z05S01[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S27[E]"
	},
	{
		"Id": "D01Z05S01[S]",
		"Direction": 3,
		"OriginalDoor": "D01Z05S02[N]"
	},
	{
		"Id": "D01Z05S02[N]",
		"Direction": 0,
		"OriginalDoor": "D01Z05S01[S]"
	},
	{
		"Id": "D01Z05S02[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z01S01[NE]",
		"Type": 1
	},
	{
		"Id": "D01Z05S02[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S03[NW]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D01Z05S02[S]",
		"Direction": 3,
		"OriginalDoor": "D01Z05S20[N]",
		"Logic": "openedDCLadder"
	},
	{
		"Id": "D01Z05S03[NW]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S02[E]"
	},
	{
		"Id": "D01Z05S03[NE]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S04[W]"
	},
	{
		"Id": "D01Z05S03[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S07[E]"
	},
	{
		"Id": "D01Z05S03[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S08[W]"
	},
	{
		"Id": "D01Z05S03[S]",
		"Direction": 3,
		"OriginalDoor": "D01Z05S13[N]"
	},
	{
		"Id": "D01Z05S04[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S03[NE]"
	},
	{
		"Id": "D01Z05S04[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S05[NW]"
	},
	{
		"Id": "D01Z05S05[N]",
		"Direction": 0,
		"OriginalDoor": "D01Z03S02[S]",
		"Type": 1
	},
	{
		"Id": "D01Z05S05[NW]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S04[E]"
	},
	{
		"Id": "D01Z05S05[NE]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S06[W]"
	},
	{
		"Id": "D01Z05S05[SW]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S18[E]"
	},
	{
		"Id": "D01Z05S05[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S09[NW]"
	},
	{
		"Id": "D01Z05S06[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S05[NE]"
	},
	{
		"Id": "D01Z05S06[Cherubs]",
		"Direction": 5,
		"Type": 1
	},
	{
		"Id": "D01Z05S07[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S03[W]"
	},
	{
		"Id": "D01Z05S08[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S03[E]"
	},
	{
		"Id": "D01Z05S09[NW]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S05[E]"
	},
	{
		"Id": "D01Z05S09[SE]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S10[W]"
	},
	{
		"Id": "D01Z05S10[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S09[SE]"
	},
	{
		"Id": "D01Z05S10[NE]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S11[W]"
	},
	{
		"Id": "D01Z05S10[SE]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S12[W]"
	},
	{
		"Id": "D01Z05S10[S]",
		"Direction": 3,
		"OriginalDoor": "D01Z05S14[N]"
	},
	{
		"Id": "D01Z05S11[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S10[NE]"
	},
	{
		"Id": "D01Z05S11[Cherubs]",
		"Direction": 5,
		"Type": 1
	},
	{
		"Id": "D01Z05S12[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S10[SE]"
	},
	{
		"Id": "D01Z05S12[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z04S09[W]",
		"Type": 1
	},
	{
		"Id": "D01Z05S13[SW]",
		"Direction": 3,
		"OriginalDoor": "D01Z05S16[N]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D01Z05S13[E]" ],
		"Logic": "D01Z05S13[SW] || canSurvivePoison3 && canWaterJump"
	},
	{
		"Id": "D01Z05S13[N]",
		"Direction": 0,
		"OriginalDoor": "D01Z05S03[S]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D01Z05S13[E]" ],
		"Logic": "D01Z05S13[N] || canSurvivePoison3 && canWaterJump"
	},
	{
		"Id": "D01Z05S13[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S14[W]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D01Z05S14[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S13[E]"
	},
	{
		"Id": "D01Z05S14[N]",
		"Direction": 0,
		"OriginalDoor": "D01Z05S10[S]"
	},
	{
		"Id": "D01Z05S14[SE]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S15[W]"
	},
	{
		"Id": "D01Z05S15[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S14[SE]"
	},
	{
		"Id": "D01Z05S15[SW]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S22[E]"
	},
	{
		"Id": "D01Z05S15[SE]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S19[W]"
	},
	{
		"Id": "D01Z05S16[N]",
		"Direction": 0,
		"OriginalDoor": "D01Z05S13[SW]"
	},
	{
		"Id": "D01Z05S16[SW]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S21[E]"
	},
	{
		"Id": "D01Z05S16[SE]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S17[W]"
	},
	{
		"Id": "D01Z05S17[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S16[SE]"
	},
	{
		"Id": "D01Z05S17[E]",
		"Direction": 2,
		"OriginalDoor": "D01BZ09S01[W]",
		"Logic": "dash && (D01Z05S17[E] || canWaterJump || canCrossGap5)"
	},
	{
		"Id": "D01Z05S18[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S05[SW]"
	},
	{
		"Id": "D01Z05S19[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S15[SE]"
	},
	{
		"Id": "D01Z05S19[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z04S19[W]",
		"Type": 1
	},
	{
		"Id": "D01Z05S20[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S25[NE]"
	},
	{
		"Id": "D01Z05S20[N]",
		"Direction": 0,
		"OriginalDoor": "D01Z05S02[S]"
	},
	{
		"Id": "D01Z05S21[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S25[E]"
	},
	{
		"Id": "D01Z05S21[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S16[SW]"
	},
	{
		"Id": "D01Z05S21[Reward]",
		"Direction": 4,
		"OriginalDoor": "D01BZ05S01[Reward]",
		"Logic": "shroud"
	},
	{
		"Id": "D01Z05S22[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S15[SW]"
	},
	{
		"Id": "D01Z05S23[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S24[E]",
		"Logic": "chalice && chaliceRooms >= 3"
	},
	{
		"Id": "D01Z05S23[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S25[W]"
	},
	{
		"Id": "D01Z05S24[W]",
		"Direction": 1,
		"OriginalDoor": "D20Z01S04[E]",
		"Type": 1
	},
	{
		"Id": "D01Z05S24[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S23[W]"
	},
	{
		"Id": "D01Z05S25[NE]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S20[W]",
		"Logic": "D01Z05S25[SW] || D01Z05S25[SE] || D01Z05S25[NE] || linen"
	},
	{
		"Id": "D01Z05S25[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S23[E]",
		"Logic": "D01Z05S25[W] || (linen && (canWalkOnRoot || doubleJump || canAirStall)) || (D01Z05S25[E] && (canWalkOnRoot || canCrossGap3))"
	},
	{
		"Id": "D01Z05S25[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S21[W]",
		"VisibiliyFlags": 5,
		"Logic": "D01Z05S25[E] || canBreakTirana && (linen || D01Z05S25[W] && (canWalkOnRoot || canCrossGap3))"
	},
	{
		"Id": "D01Z05S25[SW]",
		"Direction": 1,
		"OriginalDoor": "D03Z03S17[E]",
		"Type": 1,
		"Logic": "D01Z05S25[SW] || D01Z05S25[SE] || D01Z05S25[NE] || linen"
	},
	{
		"Id": "D01Z05S25[SE]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S26[W]",
		"Logic": "D01Z05S25[SW] || D01Z05S25[SE] || D01Z05S25[NE] || linen"
	},
	{
		"Id": "D01Z05S25[EchoesW]",
		"Direction": 1,
		"OriginalDoor": "D20Z01S09[E]",
		"Type": 1,
		"VisibilityFlags": 11,
		"RequiredDoors": [ "D01Z05S25[EchoesE]" ],
		"Logic": "D01Z05S25[EchoesW] || (D01Z05S25[EchoesE] && (blood || canCrossGap8)) || (linen && doubleJump)"
	},
	{
		"Id": "D01Z05S25[EchoesE]",
		"Direction": 2,
		"OriginalDoor": "D20Z01S10[W]",
		"Type": 1,
		"VisibilityFlags": 11,
		"RequiredDoors": [ "D01Z05S25[EchoesW]" ],
		"Logic": "D01Z05S25[EchoesE] || (D01Z05S25[EchoesW] && (blood || canCrossGap8)) || (linen && doubleJump)"
	},
	{
		"Id": "D01Z05S26[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S25[SE]"
	},
	{
		"Id": "D01Z05S27[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S01[W]"
	},
	{
		"Id": "D01BZ05S01[Reward]",
		"Direction": 7,
		"OriginalDoor": "D01Z05S21[Reward]"
	},
	{
		"Id": "D01BZ09S01[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S17[E]"
	},
	
	{
		"Id": "D01Z06S01[N]",
		"Direction": 1,
		"OriginalDoor": "D01Z01S01[S]",
		"Type": 1
	},
	{
		"Id": "D01Z06S01[Santos]",
		"Direction": 4,
		"OriginalDoor": "D01BZ07S01[Santos]",
		"Logic": "bell"
	},
	{
		"Id": "D01BZ07S01[Santos]",
		"Direction": 7,
		"OriginalDoor": "D01Z06S01[Santos]"
	},
	
	{
		"Id": "D02Z01S01[SW]",
		"Direction": 1,
		"OriginalDoor": "D02Z01S06[E]",
		"Logic": "openedWOTWCave && (D02Z01S01[W] || D02Z01S01[CherubsL] || D02Z01S01[SW] || D02Z01S01[CherubsR] || doubleJump || wallClimb)"
	},
	{
		"Id": "D02Z01S01[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z01S02[E]",
		"Logic": "D02Z01S01[W] || D02Z01S01[CherubsL] || wallClimb || doubleJump || ((D02Z01S01[SW] || D02Z01S01[CherubsR]) && canDawnJump)"
	},
	{
		"Id": "D02Z01S01[SE]",
		"Direction": 2,
		"OriginalDoor": "D01Z03S04[NW]",
		"Type": 1
	},
	{
		"Id": "D02Z01S01[CherubsL]",
		"Direction": 5
	},
	{
		"Id": "D02Z01S01[CherubsR]",
		"Direction": 5
	},
	{
		"Id": "D02Z01S02[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z01S04[E]"
	},
	{
		"Id": "D02Z01S02[NW]",
		"Direction": 1,
		"OriginalDoor": "D02Z01S03[SE]",
		"Logic": "D02Z01S02[NW] || wallClimb || doubleJump || (D02Z01S02[NE] && canWalkOnRoot && canCrossGap5)"
	},
	{
		"Id": "D02Z01S02[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z01S01[W]"
	},
	{
		"Id": "D02Z01S02[NE]",
		"Direction": 2,
		"OriginalDoor": "D02Z01S09[W]",
		"Logic": "D02Z01S02[NE] || (doubleJump && canEnemyBounce) || (D02Z01S02[NW] || wallClimb || doubleJump) && (canWalkOnRoot || canCrossGap10)"
	},
	{
		"Id": "D02Z01S02[]",
		"Direction": 6,
		"OriginalDoor": "D02Z01S06[Cherubs]",
		"Logic": "linen"
	},
	{
		"Id": "D02Z01S03[SW]",
		"Direction": 1,
		"OriginalDoor": "D02Z01S05[E]"
	},
	{
		"Id": "D02Z01S03[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z02S01[E]",
		"Type": 1,
		"Logic": "D02Z01S03[W] || D02Z01S03[SE] || D02Z01S03[Cherubs] || wallClimb"
	},
	{
		"Id": "D02Z01S03[SE]",
		"Direction": 2,
		"OriginalDoor": "D02Z01S02[NW]",
		"Logic": "D02Z01S03[W] || D02Z01S03[SE] || D02Z01S03[Cherubs] || wallClimb"
	},
	{
		"Id": "D02Z01S03[Cherubs]",
		"Direction": 5
	},
	{
		"Id": "D02Z01S04[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z01S02[W]"
	},
	{
		"Id": "D02Z01S04[-N]",
		"Direction": 6,
		"OriginalDoor": "D02Z01S08[N]",
		"Logic": "fullThimble && (D02Z01S01[W] || D02Z01S01[CherubsL] || wallClimb || doubleJump || ((D02Z01S01[SW] || D02Z01S01[CherubsR]) && canDawnJump))"
	},
	{
		"Id": "D02Z01S05[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z01S03[SW]"
	},
	{
		"Id": "D02Z01S06[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z01S08[E]",
		"Logic": "D02Z01S06[W] || dash || wallClimb && doubleJump"
	},
	{
		"Id": "D02Z01S06[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z01S01[SW]",
		"Logic": "D02Z01S06[E] || wallClimb"
	},
	{
		"Id": "D02Z01S06[Cherubs]",
		"Direction": 5
	},
	{
		"Id": "D02Z01S08[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z01S06[W]"
	},
	{
		"Id": "D02Z01S08[N]",
		"Direction": 5
	},
	{
		"Id": "D02Z01S09[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z01S02[NE]"
	},
	{
		"Id": "D02Z01S09[-CherubsL]",
		"Direction": 6,
		"OriginalDoor": "D02Z01S01[CherubsL]",
		"Logic": "linen"
	},
	{
		"Id": "D02Z01S09[-CherubsR]",
		"Direction": 6,
		"OriginalDoor": "D02Z01S01[CherubsR]",
		"Logic": "linen && (canWalkOnRoot || canCrossGap2 || canEnemyBounce && canAirStall)"
	},
	
	{
		"Id": "D02Z02S01[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z02S08[E]",
		"Logic": "D02Z02S01[W] || D02Z02S01[NW] || D02Z02S01[Cherubs] || dash"
	},
	{
		"Id": "D02Z02S01[NW]",
		"Direction": 1,
		"OriginalDoor": "D02Z02S02[SE]",
		"Logic": "D02Z02S01[NW] || D02Z02S01[Cherubs] || wallClimb && (D02Z02S01[W] || dash)"
	},
	{
		"Id": "D02Z02S01[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z01S03[W]",
		"Type": 1,
		"Logic": "D02Z02S01[E] || D02Z02S01[NW] || D02Z02S01[Cherubs] || wallClimb || dash"
	},
	{
		"Id": "D02Z02S01[Cherubs]",
		"Direction": 5
	},
	{
		"Id": "D02Z02S02[SE]",
		"Direction": 2,
		"OriginalDoor": "D02Z02S01[NW]"
	},
	{
		"Id": "D02Z02S02[NW]",
		"Direction": 1,
		"OriginalDoor": "D02Z02S04[SE]",
		"Logic": "D02Z02S02[NW] || D02Z02S02[NE] || D02Z02S02[CherubsL] || D02Z02S02[CherubsR] || wallClimb"
	},
	{
		"Id": "D02Z02S02[NE]",
		"Direction": 2,
		"OriginalDoor": "D02Z02S03[SW]",
		"Logic": "D02Z02S02[NW] || D02Z02S02[NE] || D02Z02S02[CherubsL] || D02Z02S02[CherubsR] || wallClimb"
	},
	{
		"Id": "D02Z02S02[-CherubsR]",
		"Direction": 6,
		"OriginalDoor": "D02Z02S08[CherubsR]",
		"Logic": "linen"
	},
	{
		"Id": "D02Z02S02[CherubsL]",
		"Direction": 5
	},
	{
		"Id": "D02Z02S02[CherubsR]",
		"Direction": 5
	},
	{
		"Id": "D02Z02S03[SW]",
		"Direction": 1,
		"OriginalDoor": "D02Z02S02[NE]"
	},
	{
		"Id": "D02Z02S03[NW]",
		"Direction": 1,
		"OriginalDoor": "D02Z02S05[SE]",
		"Logic": "D02Z02S03[NW] || doubleJump || wallClimb || D02Z02S03[NE] && canWalkOnRoot"
	},
	{
		"Id": "D02Z02S03[NE]",
		"Direction": 2,
		"OriginalDoor": "D02Z02S14[W]",
		"Logic": "D02Z02S03[NE] || wallClimb && (canCrossGap11 || (blood && (canWalkOnRoot || canCrossGap7)) || (canWalkOnRoot && (doubleJump || canAirStall)))"
	},
	{
		"Id": "D02Z02S03[-Cherubs]",
		"Direction": 6,
		"OriginalDoor": "D02Z02S01[Cherubs]",
		"Logic": "linen"
	},
	{
		"Id": "D02Z02S04[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z02S09[E]",
		"Logic": "D02Z02S04[NE] || D02Z02S04[W] || D02Z02S04[E] && dash || D02Z02S04[SE] && (wallClimb || doubleJump && canEnemyUpslash)"
	},
	{
		"Id": "D02Z02S04[SE]",
		"Direction": 2,
		"OriginalDoor": "D02Z02S02[NW]",
		"Logic": "D02Z02S04[NE] || D02Z02S04[W] || D02Z02S04[SE] || dash"
	},
	{
		"Id": "D02Z02S04[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z02S05[SW]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D02Z02S04[NE]",
		"Direction": 2,
		"OriginalDoor": "D02Z02S05[W]",
		"Logic": "D02Z02S04[NE] || ((D02Z02S04[W] || D02Z02S04[E] && dash) && (doubleJump || wallClimb)) || (D02Z02S04[SE] && (wallClimb || doubleJump && canEnemyUpslash))"
	},
	{
		"Id": "D02Z02S04[-CherubsL]",
		"Direction": 6,
		"OriginalDoor": "D02Z02S08[CherubsL]",
		"Logic": "linen && (D02Z02S04[NE] || D02Z02S04[W] || D02Z02S04[SE] || dash)"
	},
	{
		"Id": "D02Z02S05[SW]",
		"Direction": 1,
		"OriginalDoor": "D02Z02S04[E]"
	},
	{
		"Id": "D02Z02S05[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z02S04[NE]",
		"VisibilityFlags": 65,
		"Logic": "D02Z02S05[W] || doubleJump && canEnemyBounce"
	},
	{
		"Id": "D02Z02S05[SE]",
		"Direction": 2,
		"OriginalDoor": "D02Z02S03[NW]"
	},
	{
		"Id": "D02Z02S05[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z02S10[W]",
		"Logic": "D02Z02S05[NW] || D02Z02S05[E] || wallClimb"
	},
	{
		"Id": "D02Z02S05[NW]",
		"Direction": 1,
		"OriginalDoor": "D02Z02S07[E]",
		"Logic": "D02Z02S05[NW] || wallClimb"
	},
	{
		"Id": "D02Z02S05[-CherubsL]",
		"Direction": 6,
		"OriginalDoor": "D02Z02S02[CherubsL]",
		"Logic": "linen"
	},
	{
		"Id": "D02Z02S05[-CherubsR]",
		"Direction": 6,
		"OriginalDoor": "D02Z02S02[CherubsR]",
		"Logic": "linen"
	},
	{
		"Id": "D02Z02S06[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z02S11[W]"
	},
	{
		"Id": "D02Z02S07[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S01[E]",
		"Type": 1
	},
	{
		"Id": "D02Z02S07[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z02S05[NW]"
	},
	{
		"Id": "D02Z02S07[Cherubs]",
		"Direction": 5
	},
	{
		"Id": "D02Z02S08[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z02S11[SE]"
	},
	{
		"Id": "D02Z02S08[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z02S01[W]"
	},
	{
		"Id": "D02Z02S08[C]",
		"Direction": 4,
		"OriginalDoor": "D02BZ02S01[C]"
	},
	{
		"Id": "D02Z02S08[CherubsL]",
		"Direction": 5
	},
	{
		"Id": "D02Z02S08[CherubsR]",
		"Direction": 5
	},
	{
		"Id": "D02Z02S09[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z02S04[W]"
	},
	{
		"Id": "D02Z02S10[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z02S05[E]"
	},
	{
		"Id": "D02Z02S11[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z02S06[E]"
	},
	{
		"Id": "D02Z02S11[SE]",
		"Direction": 2,
		"OriginalDoor": "D02Z02S08[W]"
	},
	{
		"Id": "D02Z02S11[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z02S12[W]",
		"Logic": "D02Z02S11[E] || D02Z02S11[NW] || D02Z02S11[NE] || canCrossGap6"
	},
	{
		"Id": "D02Z02S11[NW]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S14[E]",
		"Type": 1,
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D02Z02S11[NE]" ]
	},
	{
		"Id": "D02Z02S11[NE]",
		"Direction": 2,
		"OriginalDoor": "D02Z02S13[W]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D02Z02S11[NW]" ]
	},
	{
		"Id": "D02Z02S11[-Cherubs]",
		"Direction": 6,
		"OriginalDoor": "D01Z02S03[Cherubs]",
		"Logic": "linen"
	},
	{
		"Id": "D02Z02S12[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z02S11[E]"
	},
	{
		"Id": "D02Z02S13[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z02S11[NE]"
	},
	{
		"Id": "D02Z02S14[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z02S03[NE]"
	},
	{
		"Id": "D02Z02S14[-Cherubs]",
		"Direction": 6,
		"OriginalDoor": "D02Z01S03[Cherubs]",
		"Logic": "linen"
	},
	{
		"Id": "D02BZ02S01[C]",
		"Direction": 7,
		"OriginalDoor": "D02Z02S08[C]"
	},
	
	{
		"Id": "D02Z03S01[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S08[E]"
	},
	{
		"Id": "D02Z03S01[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z02S07[W]",
		"Type": 1
	},
	{
		"Id": "D02Z03S02[S]",
		"Direction": 3,
		"OriginalDoor": "D02Z03S16[N]"
	},
	{
		"Id": "D02Z03S02[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S03[E]",
		"Logic": "D02Z03S02[NW] || D02Z03S02[NE] || D02Z03S02[N] || D02Z03S02[W] || doubleJump || wallClimb"
	},
	{
		"Id": "D02Z03S02[NW]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S21[E]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D02Z03S02[NE]", "D02Z03S02[N]" ]
	},
	{
		"Id": "D02Z03S02[NE]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S13[W]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D02Z03S02[NW]", "D02Z03S02[N]" ]
	},
	{
		"Id": "D02Z03S02[N]",
		"Direction": 0,
		"OriginalDoor": "D02Z03S11[S]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D02Z03S02[NW]", "D02Z03S02[NE]" ],
		"Logic": "openedConventLadder"
	},
	{
		"Id": "D02Z03S03[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S05[E]"
	},
	{
		"Id": "D02Z03S03[NW]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S05[NE]",
		"Logic": "D02Z03S03[NW] || blood || canCrossGap3"
	},
	{
		"Id": "D02Z03S03[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S02[W]"
	},
	{
		"Id": "D02Z03S05[S]",
		"Direction": 3,
		"OriginalDoor": "D02Z03S07[N]",
		"Logic": "D02Z03S05[S] || D02Z03S05[NE] || wallClimb"
	},
	{
		"Id": "D02Z03S05[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S03[W]"
	},
	{
		"Id": "D02Z03S05[NE]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S03[NW]",
		"Logic": "D02Z03S05[S] || D02Z03S05[NE] || wallClimb || doubleJump"
	},
	{
		"Id": "D02Z03S06[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S18[SE]"
	},
	{
		"Id": "D02Z03S06[S]",
		"Direction": 3,
		"OriginalDoor": "D02Z03S07[NW]"
	},
	{
		"Id": "D02Z03S07[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S17[E]"
	},
	{
		"Id": "D02Z03S07[NWW]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S24[E]"
	},
	{
		"Id": "D02Z03S07[NW]",
		"Direction": 0,
		"OriginalDoor": "D02Z03S06[S]"
	},
	{
		"Id": "D02Z03S07[N]",
		"Direction": 0,
		"OriginalDoor": "D02Z03S05[S]"
	},
	{
		"Id": "D02Z03S07[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S08[W]"
	},
	{
		"Id": "D02Z03S08[SW]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S12[E]"
	},
	{
		"Id": "D02Z03S08[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S07[E]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D02Z03S08[SE]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S14[W]"
	},
	{
		"Id": "D02Z03S08[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S01[W]"
	},
	{
		"Id": "D02Z03S08[NE]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S16[W]"
	},
	{
		"Id": "D02Z03S09[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S18[NE]"
	},
	{
		"Id": "D02Z03S09[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S20[W]"
	},
	{
		"Id": "D02Z03S10[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S11[E]"
	},
	{
		"Id": "D02Z03S10[-W]",
		"Direction": 2,
		"OriginalDoor": "D09Z01S06[-E]",
		"Type": 1
	},
	{
		"Id": "D02Z03S10[-Cherubs]",
		"Direction": 6,
		"OriginalDoor": "D02Z02S07[Cherubs]",
		"Logic": "linen"
	},
	{
		"Id": "D02Z03S11[S]",
		"Direction": 3,
		"OriginalDoor": "D02Z03S02[N]"
	},
	{
		"Id": "D02Z03S11[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S15[E]"
	},
	{
		"Id": "D02Z03S11[NW]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S19[E]"
	},
	{
		"Id": "D02Z03S11[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S10[W]"
	},
	{
		"Id": "D02Z03S11[NE]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S22[W]"
	},
	{
		"Id": "D02Z03S12[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S08[SW]"
	},
	{
		"Id": "D02Z03S13[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S02[NE]"
	},
	{
		"Id": "D02Z03S14[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S08[SE]"
	},
	{
		"Id": "D02Z03S14[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z02S11[NW]",
		"Type": 1
	},
	{
		"Id": "D02Z03S15[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S11[W]"
	},
	{
		"Id": "D02Z03S16[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S08[NE]"
	},
	{
		"Id": "D02Z03S16[N]",
		"Direction": 0,
		"OriginalDoor": "D02Z03S02[S]"
	},
	{
		"Id": "D02Z03S17[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S07[W]"
	},
	{
		"Id": "D02Z03S18[NW]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S23[E]",
		"Logic": "D02Z03S18[NW] || D02Z03S18[NE] || wallClimb"
	},
	{
		"Id": "D02Z03S18[SE]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S06[W]"
	},
	{
		"Id": "D02Z03S18[NE]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S09[W]",
		"Logic": "D02Z03S18[NW] || D02Z03S18[NE] || wallClimb"
	},
	{
		"Id": "D02Z03S19[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S11[NW]"
	},
	{
		"Id": "D02Z03S20[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S09[E]",
		"Logic": "D02Z03S20[W] || canBeatConventBoss"
	},
	{
		"Id": "D02Z03S20[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S21[W]",
		"Logic": "D02Z03S20[E] || canBeatConventBoss"
	},
	{
		"Id": "D02Z03S21[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S20[E]"
	},
	{
		"Id": "D02Z03S21[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S02[NW]"
	},
	{
		"Id": "D02Z03S22[W]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S11[NE]"
	},
	{
		"Id": "D02Z03S23[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S18[NW]"
	},
	{
		"Id": "D02Z03S24[E]",
		"Direction": 2,
		"OriginalDoor": "D02Z03S07[NWW]"
	},
	
	{
		"Id": "D03Z01S01[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z01S02[E]"
	},
	{
		"Id": "D03Z01S01[NE]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S02[W]",
		"Type": 1
	},
	{
		"Id": "D03Z01S01[S]",
		"Direction": 3,
		"OriginalDoor": "D20Z01S03[N]",
		"Type": 1,
		"VisibilityFlags": 1
	},
	{
		"Id": "D03Z01S01[-Cherubs]",
		"Direction": 6,
		"OriginalDoor": "D20Z01S01[Cherubs]",
		"Logic": "linen"
	},
	{
		"Id": "D03Z01S02[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z01S06[E]",
		"Logic": "D03Z01S02[W] || wallClimb || canCrossGap3"
	},
	{
		"Id": "D03Z01S02[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z01S01[W]",
		"Logic": "D03Z01S02[E] || wallClimb || canCrossGap7"
	},
	{
		"Id": "D03Z01S03[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z01S04[E]",
		"Logic": "D03Z01S03[W] || wallClimb && (D03Z01S03[SW] || canCrossGap9)"
	},
	{
		"Id": "D03Z01S03[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z01S06[W]",
		"Logic": "D03Z01S03[E] || wallClimb"
	},
	{
		"Id": "D03Z01S03[SW]",
		"Direction": 3,
		"OriginalDoor": "D03Z02S10[N]",
		"Type": 1,
		"Logic": "D03Z01S03[W] || D03Z01S03[SW] || canCrossGap9"
	},
	{
		"Id": "D03Z01S03[SE]",
		"Direction": 3,
		"OriginalDoor": "D03Z02S01[N]",
		"Type": 1
	},
	{
		"Id": "D03Z01S03[-WestL]",
		"Direction": 6,
		"OriginalDoor": "D03Z02S10[Cherubs]",
		"Type": 1,
		"Logic": "linen && (D03Z01S03[W] || D03Z01S03[SW] || canCrossGap9)"
	},
	{
		"Id": "D03Z01S03[-WestR]",
		"Direction": 6,
		"OriginalDoor": "D03Z02S02[CherubsL]",
		"Type": 1,
		"Logic": "linen && (D03Z01S03[W] || D03Z01S03[SW] || canCrossGap9)"
	},
	{
		"Id": "D03Z01S03[-EastL]",
		"Direction": 6,
		"OriginalDoor": "D03Z02S02[CherubsR]",
		"Type": 1,
		"Logic": "linen && (D03Z01S03[W] || D03Z01S03[SW] || canCrossGap5)"
	},
	{
		"Id": "D03Z01S03[-EastR]",
		"Direction": 6,
		"OriginalDoor": "D03Z02S01[Cherubs]",
		"Type": 1,
		"Logic": "linen"
	},
	{
		"Id": "D03Z01S04[NW]",
		"Direction": 1,
		"OriginalDoor": "D03Z01S05[E]"
	},
	{
		"Id": "D03Z01S04[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z01S03[W]"
	},
	{
		"Id": "D03Z01S05[W]",
		"Direction": 1,
		"OriginalDoor": "D17Z01S07[SE]",
		"Type": 1
	},
	{
		"Id": "D03Z01S05[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z01S04[NW]"
	},
	{
		"Id": "D03Z01S06[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z01S03[E]",
		"Logic": "D03Z01S06[W] || canBeatPerpetua"
	},
	{
		"Id": "D03Z01S06[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z01S02[W]",
		"Logic": "D03Z01S06[E] || canBeatPerpetua"
	},
	
	{
		"Id": "D03Z02S01[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z02S02[E]",
		"Logic": "D03Z02S01[W] || wallClimb || doubleJump && canEnemyBounce"
	},
	{
		"Id": "D03Z02S01[N]",
		"Direction": 0,
		"OriginalDoor": "D03Z01S03[SE]",
		"Type": 1,
		"Logic": "D03Z02S01[N] || wallClimb || doubleJump"
	},
	{
		"Id": "D03Z02S01[Cherubs]",
		"Direction": 5,
		"Type": 1
	},
	{
		"Id": "D03Z02S02[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z02S10[E]",
		"Logic": "D03Z02S02[W] || D03Z02S02[CherubsL] || doubleJump && (D03Z02S02[E] || D03Z02S02[CherubsR] || wallClimb || canEnemyBounce)"
	},
	{
		"Id": "D03Z02S02[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z02S01[W]",
		"Logic": "D03Z02S02[E] || wallClimb || doubleJump && canEnemyBounce"
	},
	{
		"Id": "D03Z02S02[S]",
		"Direction": 3,
		"OriginalDoor": "D03Z02S03[N]"
	},
	{
		"Id": "D03Z02S02[CherubsL]",
		"Direction": 5,
		"Type": 1
	},
	{
		"Id": "D03Z02S02[CherubsR]",
		"Direction": 5,
		"Type": 1
	},
	{
		"Id": "D03Z02S03[W]",
		"Direction": 3,
		"OriginalDoor": "D03Z02S07[N]",
		"Logic": "D03Z02S03[W] || dash && (D03Z02S03[E] || D03Z02S03[N] || D03Z02S03[SE2])"
	},
	{
		"Id": "D03Z02S03[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z02S05[W]",
		"Logic": "D03Z02S03[E] || (canAirStall || doubleJump || boots) && (D03Z02S03[E] && dash || D03Z02S03[N] || D03Z02S03[SE2])"
	},
	{
		"Id": "D03Z02S03[N]",
		"Direction": 0,
		"OriginalDoor": "D03Z02S02[S]",
		"Logic": "D03Z02S03[W] && dash || D03Z02S03[E] || D03Z02S03[N] || D03Z02S03[SE2]"
	},
	{
		"Id": "D03Z02S03[SE2]",
		"Direction": 3,
		"OriginalDoor": "D03Z02S04[NW]",
		"Logic": "D03Z02S03[W] && dash || D03Z02S03[E] || D03Z02S03[N] || D03Z02S03[SE2]"
	},
	{
		"Id": "D03Z02S03[SW]",
		"Direction": 1,
		"OriginalDoor": "D03Z02S07[E]",
		"Logic": "D03Z02S03[SW] || D03Z02S03[SE] || D03Z02S03[SSL] || D03Z02S03[SSR] || brokeJondoBellW && brokeJondoBellE && (D03Z02S03[W] && dash || D03Z02S03[E] || D03Z02S03[N] || D03Z02S03[SE2])"
	},
	{
		"Id": "D03Z02S03[SE]",
		"Direction": 2,
		"OriginalDoor": "D03Z02S06[W]",
		"Logic": "D03Z02S03[SW] || D03Z02S03[SE] || D03Z02S03[SSL] || D03Z02S03[SSR] || brokeJondoBellW && brokeJondoBellE && (D03Z02S03[W] && dash || D03Z02S03[E] || D03Z02S03[N] || D03Z02S03[SE2])"
	},
	{
		"Id": "D03Z02S03[SSL]",
		"Direction": 3,
		"OriginalDoor": "D03Z03S01[NL]",
		"Type": 1,
		"Logic": "D03Z02S03[SW] || D03Z02S03[SE] || D03Z02S03[SSL] || D03Z02S03[SSR] || brokeJondoBellW && brokeJondoBellE && (D03Z02S03[W] && dash || D03Z02S03[E] || D03Z02S03[N] || D03Z02S03[SE2])"
	},
	{
		"Id": "D03Z02S03[SSC]",
		"Direction": 6,
		"OriginalDoor": "D03Z03S01[NC]",
		"Type": 1,
		"Logic": "D03Z02S03[SW] || D03Z02S03[SE] || D03Z02S03[SSL] || D03Z02S03[SSR] || brokeJondoBellW && brokeJondoBellE && (D03Z02S03[W] && dash || D03Z02S03[E] || D03Z02S03[N] || D03Z02S03[SE2])"
	},
	{
		"Id": "D03Z02S03[SSR]",
		"Direction": 3,
		"OriginalDoor": "D03Z03S01[NR]",
		"Type": 1,
		"Logic": "D03Z02S03[SW] || D03Z02S03[SE] || D03Z02S03[SSL] || D03Z02S03[SSR] || brokeJondoBellW && brokeJondoBellE && (D03Z02S03[W] && dash || D03Z02S03[E] || D03Z02S03[N] || D03Z02S03[SE2])"
	},
	{
		"Id": "D03Z02S04[NW]",
		"Direction": 0,
		"OriginalDoor": "D03Z02S03[SE2]",
		"Logic": "D03Z02S04[NW] || wallClimb || doubleJump"
	},
	{
		"Id": "D03Z02S04[NE]",
		"Direction": 0,
		"OriginalDoor": "D03Z02S05[S]",
		"Logic": "D03Z02S04[NE] || wallClimb || (D03Z02S04[S] && doubleJump)"
	},
	{
		"Id": "D03Z02S04[S]",
		"Direction": 3,
		"OriginalDoor": "D03Z02S06[N]",
		"Logic": "D03Z02S04[NE] || D03Z02S04[S] || wallClimb"
	},
	{
		"Id": "D03Z02S05[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z02S03[E]"
	},
	{
		"Id": "D03Z02S05[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z02S11[W]",
		"Logic": "D03Z02S05[E] || D03Z02S05[S] || canCrossGap5 || (canEnemyBounce && canCrossGap3)"
	},
	{
		"Id": "D03Z02S05[S]",
		"Direction": 3,
		"OriginalDoor": "D03Z02S04[NE]",
		"Logic": "D03Z02S05[E] || D03Z02S05[S] || canCrossGap5 || (canEnemyBounce && canCrossGap3)"
	},
	{
		"Id": "D03Z02S06[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z02S03[SE]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D03Z02S06[N]",
		"Direction": 0,
		"OriginalDoor": "D03Z02S04[S]"
	},
	{
		"Id": "D03Z02S07[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z02S08[E]"
	},
	{
		"Id": "D03Z02S07[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z02S03[SW]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D03Z02S07[N]",
		"Direction": 0,
		"OriginalDoor": "D03Z02S03[W]"
	},
	{
		"Id": "D03Z02S08[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z02S14[E]",
		"Logic": "D03Z02S08[N] || D03Z02S08[W] || wallClimb || doubleJump"
	},
	{
		"Id": "D03Z02S08[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z02S07[W]"
	},
	{
		"Id": "D03Z02S08[N]",
		"Direction": 0,
		"OriginalDoor": "D03Z02S09[S]",
		"Logic": "D03Z02S08[N] || D03Z02S08[W] || wallClimb || doubleJump"
	},
	{
		"Id": "D03Z02S09[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z02S12[E]",
		"Logic": "D03Z02S09[W] || dash"
	},
	{
		"Id": "D03Z02S09[N]",
		"Direction": 0,
		"OriginalDoor": "D03Z02S10[S]",
		"Logic": "D03Z02S09[N] || D03Z02S09[S] || D03Z02S09[Cherubs] || dash"
	},
	{
		"Id": "D03Z02S09[S]",
		"Direction": 3,
		"OriginalDoor": "D03Z02S08[N]",
		"Logic": "D03Z02S09[N] || D03Z02S09[S] || D03Z02S09[Cherubs] || dash"
	},
	{
		"Id": "D03Z02S09[Cherubs]",
		"Direction": 5
	},
	{
		"Id": "D03Z02S10[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z02S13[E]"
	},
	{
		"Id": "D03Z02S10[N]",
		"Direction": 0,
		"OriginalDoor": "D03Z01S03[SW]",
		"Type": 1
	},
	{
		"Id": "D03Z02S10[S]",
		"Direction": 3,
		"OriginalDoor": "D03Z02S09[N]"
	},
	{
		"Id": "D03Z02S10[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z02S02[W]"
	},
	{
		"Id": "D03Z02S10[-Cherubs]",
		"Direction": 6,
		"OriginalDoor": "D03Z02S09[Cherubs]",
		"Logic": "linen"
	},
	{
		"Id": "D03Z02S10[Cherubs]",
		"Direction": 5,
		"Type": 1
	},
	{
		"Id": "D03Z02S11[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z02S05[E]",
		"Logic": "D03Z02S11[W] || dash && (doubleJump || wallClimb || canCrossGap2)"
	},
	{
		"Id": "D03Z02S11[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z02S15[W]",
		"Logic": "D03Z02S11[E] || dash && (wallClimb || doubleJump)"
	},
	{
		"Id": "D03Z02S12[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z02S09[W]"
	},
	{
		"Id": "D03Z02S12[Cherubs]",
		"Direction": 5
	},
	{
		"Id": "D03Z02S13[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z02S10[W]"
	},
	{
		"Id": "D03Z02S13[-Cherubs]",
		"Direction": 6,
		"OriginalDoor": "D03Z02S12[Cherubs]",
		"Logic": "linen"
	},
	{
		"Id": "D03Z02S14[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z02S08[W]"
	},
	{
		"Id": "D03Z02S15[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z02S11[E]"
	},
	{
		"Id": "D03Z02S15[E]",
		"Direction": 2,
		"OriginalDoor": "D20Z01S01[W]",
		"Type": 1
	},
	
	{
		"Id": "D03Z03S01[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z03S18[E]"
	},
	{
		"Id": "D03Z03S01[S]",
		"Direction": 2,
		"OriginalDoor": "D03Z03S12[W]"
	},
	{
		"Id": "D03Z03S01[NL]",
		"Direction": 0,
		"OriginalDoor": "D03Z02S03[SSL]",
		"Type": 1,
		"Logic": "D03Z03S01[NL] || D03Z03S01[NR] || D03Z03S01[NC] || wallClimb || doubleJump"
	},
	{
		"Id": "D03Z03S01[NC]",
		"Direction": 5,
		"Type": 1
	},
	{
		"Id": "D03Z03S01[NR]",
		"Direction": 0,
		"OriginalDoor": "D03Z02S03[SSR]",
		"Type": 1,
		"Logic": "D03Z03S01[NL] || D03Z03S01[NR] || D03Z03S01[NC] || wallClimb || doubleJump"
	},
	{
		"Id": "D03Z03S02[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z03S12[E]",
		"Logic": "D03Z03S02[NE] || D03Z03S02[W] || wallClimb || doubleJump"
	},
	{
		"Id": "D03Z03S02[NE]",
		"Direction": 2,
		"OriginalDoor": "D03Z03S14[W]",
		"Logic": "D03Z03S02[NE] || wallClimb || doubleJump"
	},
	{
		"Id": "D03Z03S02[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z03S03[W]"
	},
	{
		"Id": "D03Z03S03[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z03S02[E]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D03Z03S03[NE]" ]
	},
	{
		"Id": "D03Z03S03[NE]",
		"Direction": 2,
		"OriginalDoor": "D03Z03S04[NW]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D03Z03S03[W]" ]
	},
	{
		"Id": "D03Z03S03[SE]",
		"Direction": 2,
		"OriginalDoor": "D03Z03S04[SW]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D03Z03S04[NW]",
		"Direction": 1,
		"OriginalDoor": "D03Z03S03[NE]",
		"Logic": "D03Z03S04[NW] || D03Z03S04[NE] || (wallClimb || doubleJump) && (D03Z03S04[E] || D03Z03S04[SW] || blood || canCrossGap10)"
	},
	{
		"Id": "D03Z03S04[NE]",
		"Direction": 2,
		"OriginalDoor": "D03Z03S05[NW]",
		"Logic": "D03Z03S04[NE] || wallClimb && (D03Z03S04[NW] || D03Z03S04[E] || D03Z03S04[SW] || blood || canCrossGap10)"
	},
	{
		"Id": "D03Z03S04[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z03S05[SW]",
		"Logic": "D03Z03S04[NW] || D03Z03S04[NE] || D03Z03S04[E] || (wallClimb || doubleJump) && (D03Z03S04[SW] || blood || canCrossGap10)"
	},
	{
		"Id": "D03Z03S04[SW]",
		"Direction": 1,
		"OriginalDoor": "D03Z03S03[SE]",
		"Logic": "D03Z03S04[NW] || D03Z03S04[NE] || D03Z03S04[E] || D03Z03S04[SW] || blood || canCrossGap10"
	},
	{
		"Id": "D03Z03S04[SE]",
		"Direction": 2,
		"OriginalDoor": "D03Z03S13[W]",
		"Logic": "D03Z03S04[SE] || blood"
	},
	{
		"Id": "D03Z03S04[-Cherubs]",
		"Direction": 6,
		"OriginalDoor": "D03Z03S10[Cherubs]",
		"Logic": "linen"
	},
	{
		"Id": "D03Z03S05[NW]",
		"Direction": 1,
		"OriginalDoor": "D03Z03S04[NE]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D03Z03S05[NE]" ]
	},
	{
		"Id": "D03Z03S05[NE]",
		"Direction": 2,
		"OriginalDoor": "D03Z03S06[W]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D03Z03S05[NW]" ]
	},
	{
		"Id": "D03Z03S05[SW]",
		"Direction": 1,
		"OriginalDoor": "D03Z03S04[E]",
		"Logic": "D03Z03S05[SW] || D03Z03S05[SE] || linen"
	},
	{
		"Id": "D03Z03S05[SE]",
		"Direction": 2,
		"OriginalDoor": "D03Z03S07[SW]",
		"Logic": "D03Z03S05[SW] || D03Z03S05[SE] || linen"
	},
	{
		"Id": "D03Z03S06[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z03S05[NE]"
	},
	{
		"Id": "D03Z03S07[NW]",
		"Direction": 1,
		"OriginalDoor": "D03Z03S19[E]",
		"Logic": "D03Z03S07[NW] || D03Z03S07[NE] || wallClimb || doubleJump"
	},
	{
		"Id": "D03Z03S07[NE]",
		"Direction": 2,
		"OriginalDoor": "D03Z03S08[W]",
		"Logic": "D03Z03S07[NW] || D03Z03S07[NE] || wallClimb || doubleJump"
	},
	{
		"Id": "D03Z03S07[SW]",
		"Direction": 1,
		"OriginalDoor": "D03Z03S05[SE]"
	},
	{
		"Id": "D03Z03S07[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z03S11[W]"
	},
	{
		"Id": "D03Z03S07[S]",
		"Direction": 3,
		"OriginalDoor": "D03Z03S09[N]"
	},
	{
		"Id": "D03Z03S08[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z03S07[NE]"
	},
	{
		"Id": "D03Z03S08[-CherubsL]",
		"Direction": 6,
		"OriginalDoor": "D03Z03S11[CherubsL]",
		"Logic": "linen"
	},
	{
		"Id": "D03Z03S08[-CherubsR]",
		"Direction": 6,
		"OriginalDoor": "D03Z03S11[CherubsR]",
		"Logic": "linen"
	},
	{
		"Id": "D03Z03S09[SW]",
		"Direction": 1,
		"OriginalDoor": "D03Z03S10[E]"
	},
	{
		"Id": "D03Z03S09[N]",
		"Direction": 0,
		"OriginalDoor": "D03Z03S07[S]"
	},
	{
		"Id": "D03Z03S10[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z03S09[SW]"
	},
	{
		"Id": "D03Z03S10[Cherubs]",
		"Direction": 5
	},
	{
		"Id": "D03Z03S11[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z03S07[E]"
	},
	{
		"Id": "D03Z03S11[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z03S15[W]"
	},
	{
		"Id": "D03Z03S11[CherubsL]",
		"Direction": 5
	},
	{
		"Id": "D03Z03S11[CherubsR]",
		"Direction": 5
	},
	{
		"Id": "D03Z03S12[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z03S01[S]"
	},
	{
		"Id": "D03Z03S12[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z03S02[W]"
	},
	{
		"Id": "D03Z03S13[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z03S04[SE]"
	},
	{
		"Id": "D03Z03S14[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z03S02[NE]"
	},
	{
		"Id": "D03Z03S15[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z03S11[E]",
		"Logic": "canBeatGrievanceBoss"
	},
	{
		"Id": "D03Z03S15[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z03S16[W]",
		"Logic": "canBeatGrievanceBoss"
	},
	{
		"Id": "D03Z03S16[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z03S15[E]"
	},
	{
		"Id": "D03Z03S16[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z03S17[W]"
	},
	{
		"Id": "D03Z03S17[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z03S16[E]"
	},
	{
		"Id": "D03Z03S17[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S25[SW]",
		"Type": 1
	},
	{
		"Id": "D03Z03S18[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z03S01[W]"
	},
	{
		"Id": "D03Z03S19[E]",
		"Direction": 2,
		"OriginalDoor": "D03Z03S07[NW]"
	},
	
	{
		"Id": "D04Z01S01[W]",
		"Direction": 1,
		"OriginalDoor": "D08Z02S01[E]",
		"Type": 1
	},
	{
		"Id": "D04Z01S01[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z01S02[W]"
	},
	{
		"Id": "D04Z01S01[NE]",
		"Direction": 2,
		"OriginalDoor": "D04Z01S02[NW]",
		"Logic": "D04Z01S01[NE] || D04Z01S01[N] || canCrossGap3"
	},
	{
		"Id": "D04Z01S01[N]",
		"Direction": 0,
		"OriginalDoor": "D04Z01S05[S]",
		"Logic": "D04Z01S01[NE] || D04Z01S01[N] || canCrossGap3"
	},
	{
		"Id": "D04Z01S01[Cherubs]",
		"Direction": 5
	},
	{
		"Id": "D04Z01S02[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z01S01[E]"
	},
	{
		"Id": "D04Z01S02[NW]",
		"Direction": 1,
		"OriginalDoor": "D04Z01S01[NE]"
	},
	{
		"Id": "D04Z01S02[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z01S03[W]"
	},
	{
		"Id": "D04Z01S03[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z01S02[E]"
	},
	{
		"Id": "D04Z01S03[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z01S04[W]"
	},
	{
		"Id": "D04Z01S03[S]",
		"Direction": 3,
		"OriginalDoor": "D05Z01S20[N]",
		"Type": 1,
		"VisibilityFlags": 1
	},
	{
		"Id": "D04Z01S04[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z01S03[E]"
	},
	{
		"Id": "D04Z01S04[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S01[W]",
		"Type": 1
	},
	{
		"Id": "D04Z01S04[Cherubs]",
		"Direction": 5,
		"Type": 1
	},
	{
		"Id": "D04Z01S05[S]",
		"Direction": 3,
		"OriginalDoor": "D04Z01S01[N]"
	},
	{
		"Id": "D04Z01S05[N]",
		"Direction": 0,
		"OriginalDoor": "D04Z01S06[S]",
		"Logic": "D04Z01S05[N] || (blood && canClimbOnRoot) || doubleJump && (blood || canClimbOnRoot)"
	},
	{
		"Id": "D04Z01S05[-Cherubs]",
		"Direction": 6,
		"OriginalDoor": "D04Z01S01[Cherubs]",
		"Logic": "linen"
	},
	{
		"Id": "D04Z01S05[CherubsN]",
		"Direction": 5
	},
	{
		"Id": "D04Z01S06[S]",
		"Direction": 3,
		"OriginalDoor": "D04Z01S05[N]"
	},
	{
		"Id": "D04Z01S06[E]",
		"Direction": 2,
		"OriginalDoor": "D09Z01S09[SW]",
		"Type": 1,
		"VisibilityFlags": 9,
		"Logic": "D04Z01S06[E] || doubleJump"
	},
	{
		"Id": "D04Z01S06[Cherubs]",
		"Direction": 6,
		"OriginalDoor": "D04Z01S05[CherubsN]",
		"Logic": "linen"
	},

	{
		"Id": "D04Z02S01[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z01S04[E]",
		"Type": 1
	},
	{
		"Id": "D04Z02S01[N]",
		"Direction": 0,
		"OriginalDoor": "D04Z02S02[S]",
		"Logic": "D04Z02S01[N] || D04Z02S01[NE] && dash && (doubleJump || wallClimb)"
	},
	{
		"Id": "D04Z02S01[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z03S01[W]",
		"Type": 1
	},
	{
		"Id": "D04Z02S01[NE]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S03[W]",
		"Logic": "D04Z02S01[NE] || D04Z02S01[N] && dash && canCrossGap1"
	},
	{
		"Id": "D04Z02S02[S]",
		"Direction": 3,
		"OriginalDoor": "D04Z02S01[N]"
	},
	{
		"Id": "D04Z02S02[SE]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S17[W]"
	},
	{
		"Id": "D04Z02S02[NE]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S15[W]",
		"VisibilityFlags": 49,
		"Logic": "D04Z02S02[NE] || (doubleJump && upwarpSkipsAllowed) || (doubleJump && canEnemyUpslash) || (canEnemyUpslash && upwarpSkipsAllowed && (wallClimb || D04Z02S02[N]))"
	},
	{
		"Id": "D04Z02S02[N]",
		"Direction": 0,
		"OriginalDoor": "D06Z01S02[S]",
		"Type": 1,
		"Logic": "D04Z02S02[N] || D04Z02S02[NE] || wallClimb || doubleJump"
	},
	{
		"Id": "D04Z02S03[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S01[NE]"
	},
	{
		"Id": "D04Z02S03[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S04[NW]"
	},
	{
		"Id": "D04Z02S04[SW]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S14[E]"
	},
	{
		"Id": "D04Z02S04[SE]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S01[NW]",
		"Type": 1
	},
	{
		"Id": "D04Z02S04[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z03S01[E]",
		"Type": 1
	},
	{
		"Id": "D04Z02S04[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S05[W]"
	},
	{
		"Id": "D04Z02S04[NW]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S03[E]",
		"Logic": "D04Z02S04[NW] || D04Z02S04[NE] || D04Z02S04[N] || D04Z02S04[Cherubs] || wallClimb && doubleJump"
	},
	{
		"Id": "D04Z02S04[NE]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S19[W]",
		"Logic": "D04Z02S04[NW] || D04Z02S04[NE] || D04Z02S04[N] || D04Z02S04[Cherubs] || wallClimb && doubleJump"
	},
	{
		"Id": "D04Z02S04[N]",
		"Direction": 0,
		"OriginalDoor": "D04Z02S06[S]",
		"Logic": "(D04Z02S04[NW] || D04Z02S04[NE] || D04Z02S04[N] || D04Z02S04[Cherubs] || wallClimb && doubleJump) && openedMoMLadder"
	},
	{
		"Id": "D04Z02S04[Cherubs]",
		"Direction": 5
	},
	{
		"Id": "D04Z02S05[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S04[E]"
	},
	{
		"Id": "D04Z02S05[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S07[SW]"
	},
	{
		"Id": "D04Z02S06[S]",
		"Direction": 3,
		"OriginalDoor": "D04Z02S04[N]"
	},
	{
		"Id": "D04Z02S06[NW]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S11[E]",
		"Logic": "D04Z02S06[NW] || D04Z02S06[N] || D04Z02S06[NE] || wallClimb"
	},
	{
		"Id": "D04Z02S06[N]",
		"Direction": 0,
		"OriginalDoor": "D06Z01S23[S]",
		"Type": 1,
		"Logic": "(D04Z02S06[NW] || D04Z02S06[N] || D04Z02S06[NE] || wallClimb) && openedARLadder"
	},
	{
		"Id": "D04Z02S06[NE]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S09[W]",
		"Logic": "D04Z02S06[NW] || D04Z02S06[N] || D04Z02S06[NE] || wallClimb"
	},
	{
		"Id": "D04Z02S06[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S10[W]"
	},
	{
		"Id": "D04Z02S06[-Cherubs]",
		"Direction": 6,
		"OriginalDoor": "D04Z02S04[Cherubs]",
		"Logic": "linen"
	},
	{
		"Id": "D04Z02S07[SW]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S05[E]"
	},
	{
		"Id": "D04Z02S07[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S19[E]"
	},
	{
		"Id": "D04Z02S07[N]",
		"Direction": 0,
		"OriginalDoor": "D04Z02S08[S]"
	},
	{
		"Id": "D04Z02S07[NE]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S13[W]"
	},
	{
		"Id": "D04Z02S07[SE]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S23[W]"
	},
	{
		"Id": "D04Z02S08[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S09[E]"
	},
	{
		"Id": "D04Z02S08[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S20[W]"
	},
	{
		"Id": "D04Z02S08[S]",
		"Direction": 3,
		"OriginalDoor": "D04Z02S07[N]"
	},
	{
		"Id": "D04Z02S08[Cherubs]",
		"Direction": 5
	},
	{
		"Id": "D04Z02S09[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S06[NE]"
	},
	{
		"Id": "D04Z02S09[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S08[W]"
	},
	{
		"Id": "D04Z02S09[NE]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S16[W]",
		"Logic": "D04Z02S09[NE] || blood"
	},
	{
		"Id": "D04Z02S10[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S06[E]"
	},
	{
		"Id": "D04Z02S11[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S21[SE]"
	},
	{
		"Id": "D04Z02S11[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S06[NW]"
	},
	{
		"Id": "D04Z02S12[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S21[NE]"
	},
	{
		"Id": "D04Z02S13[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S07[NE]"
	},
	{
		"Id": "D04Z02S14[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S04[SW]"
	},
	{
		"Id": "D04Z02S15[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S02[NE]"
	},
	{
		"Id": "D04Z02S15[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S22[W]"
	},
	{
		"Id": "D04Z02S16[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S09[NE]"
	},
	{
		"Id": "D04Z02S16[-Cherubs]",
		"Direction": 6,
		"OriginalDoor": "D04Z02S08[Cherubs]",
		"Logic": "linen"
	},
	{
		"Id": "D04Z02S17[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S02[SE]"
	},
	{
		"Id": "D04Z02S19[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S04[NE]"
	},
	{
		"Id": "D04Z02S19[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S07[W]"
	},
	{
		"Id": "D04Z02S20[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S08[E]"
	},
	{
		"Id": "D04Z02S20[Redento]",
		"Direction": 4,
		"OriginalDoor": "D04BZ02S01[Redento]",
		"Logic": "redentoRooms >= 5"
	},
	{
		"Id": "D04Z02S21[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S22[E]",
		"Logic": "D04Z02S21[NE] || D04Z02S21[W] || wallClimb || doubleJump"
	},
	{
		"Id": "D04Z02S21[SE]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S11[W]"
	},
	{
		"Id": "D04Z02S21[NE]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S12[W]",
		"Logic": "D04Z02S21[NE] || wallClimb || doubleJump"
	},
	{
		"Id": "D04Z02S22[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S15[E]",
		"Logic": "D04Z02S22[W] || canBeatMothersBoss"
	},
	{
		"Id": "D04Z02S22[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S21[W]",
		"Logic": "D04Z02S22[E] || canBeatMothersBoss"
	},
	{
		"Id": "D04Z02S23[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S07[SE]"
	},
	{
		"Id": "D04Z02S23[SE]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S24[NW]"
	},
	{
		"Id": "D04Z02S23[NE]",
		"Direction": 2,
		"OriginalDoor": "D04Z04S01[W]",
		"Type": 1
	},
	{
		"Id": "D04Z02S24[NW]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S23[SE]"
	},
	{
		"Id": "D04Z02S24[SW]",
		"Direction": 1,
		"OriginalDoor": "D20Z02S01[E]",
		"Type": 1
	},
	{
		"Id": "D04Z02S24[SE]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S25[W]"
	},
	{
		"Id": "D04Z02S25[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S24[SE]"
	},
	{
		"Id": "D04BZ02S01[Redento]",
		"Direction": 7,
		"OriginalDoor": "D04Z02S20[Redento]"
	},
	
	{
		"Id": "D04Z03S01[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S01[E]",
		"Type": 1
	},
	{
		"Id": "D04Z03S01[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S04[W]",
		"Type": 1
	},
	{
		"Id": "D04Z03S02[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S22[E]",
		"Type": 1
	},
	
	{
		"Id": "D04Z04S01[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S23[NE]",
		"Type": 1
	},
	{
		"Id": "D04Z04S01[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z04S02[W]",
		"Type": 9
	},
	{
		"Id": "D04Z04S02[W]",
		"Direction": 1,
		"OriginalDoor": "D04Z04S01[E]",
		"Type": 9
	},
	
	{
		"Id": "D05Z01S01[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S02[E]"
	},
	{
		"Id": "D05Z01S01[NW]",
		"Direction": 1,
		"OriginalDoor": "D04Z02S04[SE]",
		"Type": 1
	},
	{
		"Id": "D05Z01S01[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S16[W]"
	},
	{
		"Id": "D05Z01S02[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S15[E]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D05Z01S02[NW]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S03[E]"
	},
	{
		"Id": "D05Z01S02[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S01[W]"
	},
	{
		"Id": "D05Z01S03[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S04[E]"
	},
	{
		"Id": "D05Z01S03[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S02[NW]"
	},
	{
		"Id": "D05Z01S03[Frontal]",
		"Direction": 4,
		"OriginalDoor": "D05BZ01S01[FrontalS]",
		"Logic": "woodKey && D05Z01S23[E] && (D05Z01S11[NW] || D05Z01S11[NE])"
	},
	{
		"Id": "D05Z01S04[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S05[E]"
	},
	{
		"Id": "D05Z01S04[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S03[W]"
	},
	{
		"Id": "D05Z01S05[SW]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S07[E]"
	},
	{
		"Id": "D05Z01S05[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S04[W]"
	},
	{
		"Id": "D05Z01S05[NE]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S17[W]",
		"Logic": "D05Z01S05[NE] || blood"
	},
	{
		"Id": "D05Z01S06[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S24[E]",
		"Logic": "D05Z01S06[W] || canSurvivePoison3"
	},
	{
		"Id": "D05Z01S06[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S20[W]",
		"Logic": "D05Z01S06[E] || canSurvivePoison3"
	},
	{
		"Id": "D05Z01S07[SW]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S08[NE]"
	},
	{
		"Id": "D05Z01S07[NW]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S20[E]",
		"Logic": "D05Z01S07[NW] || blood && (canClimbOnRoot || doubleJump) || (canClimbOnRoot && canCrossGap3) || canCrossGap7"
	},
	{
		"Id": "D05Z01S07[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S05[SW]"
	},
	{
		"Id": "D05Z01S08[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S10[E]"
	},
	{
		"Id": "D05Z01S08[NW]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S12[E]"
	},
	{
		"Id": "D05Z01S08[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S09[W]"
	},
	{
		"Id": "D05Z01S08[Health]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S14[W]"
	},
	{
		"Id": "D05Z01S08[NE]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S07[SW]"
	},
	{
		"Id": "D05Z01S09[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S08[E]"
	},
	{
		"Id": "D05Z01S09[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S18[W]"
	},
	{
		"Id": "D05Z01S10[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S11[E]"
	},
	{
		"Id": "D05Z01S10[NW]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S11[NE]"
	},
	{
		"Id": "D05Z01S10[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S08[W]"
	},
	{
		"Id": "D05Z01S11[SW]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S19[E]",
		"VisibilityFlags": 5,
		"Logic": "canBreakTirana"
	},
	{
		"Id": "D05Z01S11[NW]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S23[E]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D05Z01S11[NE]" ]
	},
	{
		"Id": "D05Z01S11[NE]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S10[NW]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D05Z01S11[NW]" ]
	},
	{
		"Id": "D05Z01S11[SE]",
		"Direction": 2,
		"OriginalDoor": "D05Z02S01[W]",
		"Type": 1
	},
	{
		"Id": "D05Z01S11[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S10[W]"
	},
	{
		"Id": "D05Z01S12[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S08[NW]"
	},
	{
		"Id": "D05Z01S13[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S21[NW]"
	},
	{
		"Id": "D05Z01S14[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S08[Health]"
	},
	{
		"Id": "D05Z01S15[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S21[NE]"
	},
	{
		"Id": "D05Z01S15[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S02[W]"
	},
	{
		"Id": "D05Z01S16[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S01[E]"
	},
	{
		"Id": "D05Z01S17[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S05[NE]"
	},
	{
		"Id": "D05Z01S18[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S09[E]"
	},
	{
		"Id": "D05Z01S19[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z02S15[E]",
		"Type": 1
	},
	{
		"Id": "D05Z01S19[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S11[SW]"
	},
	{
		"Id": "D05Z01S20[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S06[E]"
	},
	{
		"Id": "D05Z01S20[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S07[NW]"
	},
	{
		"Id": "D05Z01S20[N]",
		"Direction": 0,
		"OriginalDoor": "D04Z01S03[S]",
		"Type": 1
	},
	{
		"Id": "D05Z01S21[SW]",
		"Direction": 1,
		"OriginalDoor": "D05Z02S14[E]",
		"Type": 1
	},
	{
		"Id": "D05Z01S21[NW]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S13[E]"
	},
	{
		"Id": "D05Z01S21[NE]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S15[W]"
	},
	{
		"Id": "D05Z01S21[-Cherubs]",
		"Direction": 6,
		"OriginalDoor": "D05Z02S11[Cherubs]",
		"Type": 1,
		"Logic": "linen"
	},
	{
		"Id": "D05Z01S22[FrontalN]",
		"Direction": 4,
		"OriginalDoor": "D05BZ01S01[FrontalN]"
	},
	{
		"Id": "D05Z01S22[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z03S02[W]",
		"Type": 1
	},
	{
		"Id": "D05Z01S23[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S11[NW]"
	},
	{
		"Id": "D05Z01S24[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S06[W]"
	},
	{
		"Id": "D05BZ01S01[FrontalS]",
		"Direction": 7,
		"OriginalDoor": "D05Z01S03[Frontal]"
	},
	{
		"Id": "D05BZ01S01[FrontalN]",
		"Direction": 7,
		"OriginalDoor": "D05Z01S22[FrontalN]"
	},

	{
		"Id": "D05Z02S01[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z01S11[SE]",
		"Type": 1
	},
	{
		"Id": "D05Z02S01[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z02S02[NW]"
	},
	{
		"Id": "D05Z02S02[SW]",
		"Direction": 1,
		"OriginalDoor": "D05Z02S03[E]"
	},
	{
		"Id": "D05Z02S02[NW]",
		"Direction": 1,
		"OriginalDoor": "D05Z02S01[E]"
	},
	{
		"Id": "D05Z02S02[SE]",
		"Direction": 2,
		"OriginalDoor": "D05Z02S09[W]"
	},
	{
		"Id": "D05Z02S02[NE]",
		"Direction": 2,
		"OriginalDoor": "D05Z02S05[W]"
	},
	{
		"Id": "D05Z02S03[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z02S04[E]"
	},
	{
		"Id": "D05Z02S03[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z02S02[SW]"
	},
	{
		"Id": "D05Z02S04[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z02S12[E]"
	},
	{
		"Id": "D05Z02S04[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z02S03[W]"
	},
	{
		"Id": "D05Z02S04[C]",
		"Direction": 4,
		"OriginalDoor": "D05BZ02S01[C]"
	},
	{
		"Id": "D05Z02S05[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z02S02[NE]"
	},
	{
		"Id": "D05Z02S05[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z02S06[SW]"
	},
	{
		"Id": "D05Z02S06[SW]",
		"Direction": 1,
		"OriginalDoor": "D05Z02S05[E]"
	},
	{
		"Id": "D05Z02S06[NW]",
		"Direction": 1,
		"OriginalDoor": "D05Z02S07[E]"
	},
	{
		"Id": "D05Z02S06[SE]",
		"Direction": 2,
		"OriginalDoor": "D05Z02S11[W]",
		"Logic": "openedTSCGate"
	},
	{
		"Id": "D05Z02S06[NE]",
		"Direction": 2,
		"OriginalDoor": "D05Z02S14[W]"
	},
	{
		"Id": "D05Z02S07[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z02S10[E]"
	},
	{
		"Id": "D05Z02S07[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z02S06[NW]"
	},
	{
		"Id": "D05Z02S08[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z02S09[E]"
	},
	{
		"Id": "D05Z02S09[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z02S02[SE]"
	},
	{
		"Id": "D05Z02S09[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z02S08[W]",
		"Logic": "redWax >= 3 && blueWax >= 3"
	},
	{
		"Id": "D05Z02S10[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z02S13[E]",
		"Logic": "dash"
	},
	{
		"Id": "D05Z02S10[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z02S07[W]"
	},
	{
		"Id": "D05Z02S11[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z02S06[SE]"
	},
	{
		"Id": "D05Z02S11[Cherubs]",
		"Direction": 5,
		"Type": 1
	},
	{
		"Id": "D05Z02S12[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z04S16[E]",
		"Type": 1
	},
	{
		"Id": "D05Z02S12[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z02S04[W]"
	},
	{
		"Id": "D05Z02S12[N]",
		"Direction": 0,
		"OriginalDoor": "D05Z02S15[S]"
	},
	{
		"Id": "D05Z02S13[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z02S10[W]",
		"Logic": "dash"
	},
	{
		"Id": "D05Z02S14[W]",
		"Direction": 1,
		"OriginalDoor": "D05Z02S06[NE]",
		"Logic": "D05Z02S14[W] || canBeatCanvasesBoss"
	},
	{
		"Id": "D05Z02S14[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S21[SW]",
		"Type": 1,
		"Logic": "D05Z02S14[E] || canBeatCanvasesBoss"
	},
	{
		"Id": "D05Z02S15[S]",
		"Direction": 3,
		"OriginalDoor": "D05Z02S12[N]"
	},
	{
		"Id": "D05Z02S15[E]",
		"Direction": 2,
		"OriginalDoor": "D05Z01S19[W]",
		"Type": 1
	},
	{
		"Id": "D05BZ02S01[C]",
		"Direction": 7,
		"OriginalDoor": "D05Z02S04[C]"
	},

	{
		"Id": "D06Z01S01[SW]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S14[E]",
		"Logic": "(D06Z01S01[SW] || D06Z01S01[SE] || D06Z01S01[W] || D06Z01S01[E] || D06Z01S01[NNW] || D06Z01S01[NNE] || D06Z01S01[N]) || linen && (D06Z01S01[NW] || D06Z01S01[NE])"
	},
	{
		"Id": "D06Z01S01[SE]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S03[W]",
		"Logic": "(D06Z01S01[SW] || D06Z01S01[SE] || D06Z01S01[W] || D06Z01S01[E] || D06Z01S01[NNW] || D06Z01S01[NNE] || D06Z01S01[N]) || linen && (D06Z01S01[NW] || D06Z01S01[NE])"
	},
	{
		"Id": "D06Z01S01[W]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S07[E]",
		"Logic": "(D06Z01S01[W] || D06Z01S01[E] || D06Z01S01[NNW] || D06Z01S01[NNE] || D06Z01S01[N]) || masks >= 1 && (D06Z01S01[SW] || D06Z01S01[SE]) || linen && (D06Z01S01[NW] || D06Z01S01[NE] && (canWalkOnRoot || canCrossGap1))"
	},
	{
		"Id": "D06Z01S01[E]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S06[WW]",
		"Logic": "(D06Z01S01[W] || D06Z01S01[E] || D06Z01S01[NNW] || D06Z01S01[NNE] || D06Z01S01[N]) || masks >= 1 && (D06Z01S01[SW] || D06Z01S01[SE]) || linen && (D06Z01S01[NE] || D06Z01S01[NW] && (canWalkOnRoot || canCrossGap1))"
	},
	{
		"Id": "D06Z01S01[NW]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S16[E]",
		"Logic": "D06Z01S01[NW] || D06Z01S01[NE] && (canWalkOnRoot || canCrossGap8) || linen && (D06Z01S01[NNW] || D06Z01S01[NNE] && (canWalkOnRoot || canCrossGap3))"
	},
	{
		"Id": "D06Z01S01[NE]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S17[W]",
		"Logic": "D06Z01S01[NE] || D06Z01S01[NW] && (canWalkOnRoot || canCrossGap8) || linen && (D06Z01S01[NNE] || D06Z01S01[NNW] && (canWalkOnRoot || canCrossGap3))"
	},
	{
		"Id": "D06Z01S01[NNW]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S09[E]",
		"Logic": "(D06Z01S01[NNW] || D06Z01S01[NNE] || D06Z01S01[N]) || masks >= 2 && (D06Z01S01[SW] || D06Z01S01[SE] || D06Z01S01[W] || D06Z01S01[E] || linen && (D06Z01S01[NW] || D06Z01S01[NE]))"
	},
	{
		"Id": "D06Z01S01[NNE]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S10[W]",
		"Logic": "(D06Z01S01[NNW] || D06Z01S01[NNE] || D06Z01S01[N]) || masks >= 2 && (D06Z01S01[SW] || D06Z01S01[SE] || D06Z01S01[W] || D06Z01S01[E] || linen && (D06Z01S01[NW] || D06Z01S01[NE]))"
	},
	{
		"Id": "D06Z01S01[N]",
		"Direction": 0,
		"OriginalDoor": "D06Z01S19[S]",
		"Logic": "masks >= 3 && (D06Z01S01[SW] || D06Z01S01[SE] || D06Z01S01[W] || D06Z01S01[E] || D06Z01S01[NNW] || D06Z01S01[NNE] || D06Z01S01[N] || linen && (D06Z01S01[NW] || D06Z01S01[NE]))",
		"Type": 9
	},
	{
		"Id": "D06Z01S01[-Cherubs]",
		"Direction": 6,
		"OriginalDoor": "D06Z01S23[Cherubs]",
		"Logic": "linen && (D06Z01S01[SW] || D06Z01S01[SE] || D06Z01S01[W] || D06Z01S01[E] || D06Z01S01[NW] || D06Z01S01[NE] || D06Z01S01[NNW] || D06Z01S01[NNE])"
	},
	{
		"Id": "D06Z01S02[W]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S18[E]"
	},
	{
		"Id": "D06Z01S02[E]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S08[W]"
	},
	{
		"Id": "D06Z01S02[S]",
		"Direction": 3,
		"OriginalDoor": "D04Z02S02[N]",
		"Type": 1
	},
	{
		"Id": "D06Z01S03[W]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S01[SE]",
		"Logic": "D06Z01S03[W] || canBeatLegionary"
	},
	{
		"Id": "D06Z01S03[E]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S04[W]",
		"Logic": "D06Z01S03[E] || canBeatLegionary"
	},
	{
		"Id": "D06Z01S04[SW]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S20[E]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D06Z01S04[W]", "D06Z01S04[Health]" ]
	},
	{
		"Id": "D06Z01S04[W]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S03[E]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D06Z01S04[SW]", "D06Z01S04[Health]" ]
	},
	{
		"Id": "D06Z01S04[Health]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S24[W]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D06Z01S04[SW]", "D06Z01S04[W]" ],
		"Logic": "D06Z01S04[Health] || (wallClimb && canSurvivePoison2 && (doubleJump || blood && canClimbOnRoot))"
	},
	{
		"Id": "D06Z01S04[NW]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S06[E]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D06Z01S04[NE]", "D06Z01S04[Cherubs]" ],
		"Logic": "D06Z01S04[NW] || D06Z01S04[Cherubs] || (D06Z01S04[SW] || D06Z01S04[W] || D06Z01S04[Health]) && wallClimb && canSurvivePoison2 && (dash || doubleJump && (canDawnJump || canClimbOnRoot))"
	},
	{
		"Id": "D06Z01S04[NE]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S06[W]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D06Z01S04[NW]", "D06Z01S04[Cherubs]" ],
		"Logic": "D06Z01S04[NE] || (D06Z01S04[SW] || D06Z01S04[W] || D06Z01S04[Health]) && wallClimb && canSurvivePoison2 && (dash || doubleJump && (canDawnJump || canClimbOnRoot))"
	},
	{
		"Id": "D06Z01S04[Cherubs]",
		"Direction": 5
	},
	{
		"Id": "D06Z01S05[E]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S12[NW]"
	},
	{
		"Id": "D06Z01S06[WW]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S01[E]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D06Z01S06[E]" ],
		"Logic": "D06Z01S06[WW] || canBeatLegionary"
	},
	{
		"Id": "D06Z01S06[E]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S04[NW]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D06Z01S06[WW]" ],
		"Logic": "D06Z01S06[E] || canBeatLegionary"
	},
	{
		"Id": "D06Z01S06[W]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S04[NE]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D06Z01S06[EE]" ]
	},
	{
		"Id": "D06Z01S06[EE]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S15[SW]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D06Z01S06[W]" ]
	},
	{
		"Id": "D06Z01S07[W]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S12[E]"
	},
	{
		"Id": "D06Z01S07[E]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S01[W]"
	},
	{
		"Id": "D06Z01S07[CherubsL]",
		"Direction": 5
	},
	{
		"Id": "D06Z01S07[CherubsR]",
		"Direction": 5
	},
	{
		"Id": "D06Z01S08[W]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S02[E]"
	},
	{
		"Id": "D06Z01S08[E]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S14[W]",
		"Logic": "D06Z01S08[N] || D06Z01S08[E] || wallClimb"
	},
	{
		"Id": "D06Z01S08[N]",
		"Direction": 0,
		"OriginalDoor": "D06Z01S13[S]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D06Z01S09[W]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S12[NE]"
	},
	{
		"Id": "D06Z01S09[E]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S01[NNW]"
	},
	{
		"Id": "D06Z01S09[-CherubsL]",
		"Direction": 6,
		"OriginalDoor": "D06Z01S16[CherubsL]",
		"Logic": "linen"
	},
	{
		"Id": "D06Z01S09[-CherubsR]",
		"Direction": 6,
		"OriginalDoor": "D06Z01S16[CherubsR]",
		"Logic": "linen"
	},
	{
		"Id": "D06Z01S10[W]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S01[NNE]"
	},
	{
		"Id": "D06Z01S10[E]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S21[W]"
	},
	{
		"Id": "D06Z01S10[-CherubsL]",
		"Direction": 6,
		"OriginalDoor": "D06Z01S17[CherubsL]",
		"Logic": "linen"
	},
	{
		"Id": "D06Z01S10[-CherubsR]",
		"Direction": 6,
		"OriginalDoor": "D06Z01S17[CherubsR]",
		"Logic": "linen"
	},
	{
		"Id": "D06Z01S11[W]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S15[NE]"
	},
	{
		"Id": "D06Z01S12[S]",
		"Direction": 3,
		"OriginalDoor": "D06Z01S14[N]"
	},
	{
		"Id": "D06Z01S12[W]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S13[E]",
		"Logic": "D06Z01S12[NW] || D06Z01S12[NE] || D06Z01S12[NE2] || D06Z01S12[W] || D06Z01S12[E] || wallClimb && doubleJump"
	},
	{
		"Id": "D06Z01S12[E]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S07[W]",
		"Logic": "D06Z01S12[NW] || D06Z01S12[NE] || D06Z01S12[NE2] || D06Z01S12[W] || D06Z01S12[E] || wallClimb && doubleJump"
	},
	{
		"Id": "D06Z01S12[NW]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S05[E]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D06Z01S12[NE]", "D06Z01S12[NE2]" ],
		"Logic": "D06Z01S12[NW] || D06Z01S12[NE] || wallClimb || doubleJump"
	},
	{
		"Id": "D06Z01S12[NE]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S09[W]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D06Z01S12[NW]", "D06Z01S12[NE2]" ],
		"Logic": "D06Z01S12[NW] || D06Z01S12[NE] || wallClimb || doubleJump"
	},
	{
		"Id": "D06Z01S12[NE2]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S16[W]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D06Z01S13[W]",
		"Direction": 1,
		"OriginalDoor": "D09Z01S01[E]",
		"Type": 1
	},
	{
		"Id": "D06Z01S13[E]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S12[W]"
	},
	{
		"Id": "D06Z01S13[S]",
		"Direction": 3,
		"OriginalDoor": "D06Z01S08[N]"
	},
	{
		"Id": "D06Z01S14[W]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S08[E]"
	},
	{
		"Id": "D06Z01S14[E]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S01[SW]"
	},
	{
		"Id": "D06Z01S14[N]",
		"Direction": 0,
		"OriginalDoor": "D06Z01S12[S]"
	},
	{
		"Id": "D06Z01S15[SW]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S06[EE]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D06Z01S15[NW]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S21[E]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D06Z01S15[NE]" ],
		"Logic": "D06Z01S15[NW] || D06Z01S15[SW] && wallClimb"
	},
	{
		"Id": "D06Z01S15[NE]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S11[W]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D06Z01S15[NW]" ],
		"Logic": "D06Z01S15[NE] || D06Z01S15[SW] && wallClimb"
	},
	{
		"Id": "D06Z01S16[W]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S12[NE2]",
		"Logic": "D06Z01S16[W] || (D06Z01S16[CherubsL] && (doubleJump || wallClimb && (canWalkOnRoot || canAirStall))) || (D06Z01S16[CherubsR] && (doubleJump || canAirStall && (canWalkOnRoot || wheel) && (wallClimb || canDawnJump))) || (D06Z01S16[E] && (canWalkOnRoot || canCrossGap7) && (wallClimb || canCrossGap5))"
	},
	{
		"Id": "D06Z01S16[E]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S01[NW]",
		"Logic": "D06Z01S16[E] || ((D06Z01S16[W] || D06Z01S16[CherubsL]) && (canWalkOnRoot || canCrossGap5)) || (D06Z01S16[CherubsR] && (doubleJump || canAirStall && (canWalkOnRoot || wheel)))"
	},
	{
		"Id": "D06Z01S16[-CherubsL]",
		"Direction": 6,
		"OriginalDoor": "D06Z01S07[CherubsL]",
		"Logic": "linen && (D06Z01S16[W] || D06Z01S16[CherubsL] || (D06Z01S16[CherubsR] && (doubleJump || canAirStall && (canWalkOnRoot || wheel))) || (D06Z01S16[E] && (canWalkOnRoot || canCrossGap7)))"
	},
	{
		"Id": "D06Z01S16[-CherubsR]",
		"Direction": 6,
		"OriginalDoor": "D06Z01S07[CherubsR]",
		"Logic": "linen && (D06Z01S16[E] || D06Z01S16[CherubsR] || (D06Z01S16[CherubsL] && (canAirStall || canWalkOnRoot || doubleJump)) || (D06Z01S16[W] && (canWalkOnRoot || canCrossGap1)))"
	},
	{
		"Id": "D06Z01S16[CherubsL]",
		"Direction": 5
	},
	{
		"Id": "D06Z01S16[CherubsR]",
		"Direction": 5
	},
	{
		"Id": "D06Z01S17[W]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S01[NE]",
		"Logic": "D06Z01S17[W] || (D06Z01S17[E] || D06Z01S17[CherubsR]) && blood || D06Z01S17[CherubsL] && doubleJump"
	},
	{
		"Id": "D06Z01S17[E]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S26[W]",
		"Logic": "D06Z01S17[E] || D06Z01S17[CherubsR] || blood && (D06Z01S17[W] || D06Z01S17[CherubsL] && doubleJump)"
	},
	{
		"Id": "D06Z01S17[-Cherubs]",
		"Direction": 6,
		"OriginalDoor": "D06Z01S04[Cherubs]",
		"Logic": "linen"
	},
	{
		"Id": "D06Z01S17[CherubsL]",
		"Direction": 5
	},
	{
		"Id": "D06Z01S17[CherubsR]",
		"Direction": 5
	},
	{
		"Id": "D06Z01S18[E]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S02[W]"
	},
	{
		"Id": "D06Z01S18[-Cherubs]",
		"Direction": 6,
		"OriginalDoor": "D04Z01S04[Cherubs]",
		"Type": 1,
		"Logic": "linen"
	},
	{
		"Id": "D06Z01S19[S]",
		"Direction": 3,
		"OriginalDoor": "D06Z01S01[N]",
		"Type": 9
	},
	{
		"Id": "D06Z01S19[E]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S25[W]",
		"Type": 9
	},
	{
		"Id": "D06Z01S20[W]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S23[E]"
	},
	{
		"Id": "D06Z01S20[E]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S04[SW]"
	},
	{
		"Id": "D06Z01S21[W]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S10[E]",
		"Logic": "D06Z01S21[W] || canBeatLegionary"
	},
	{
		"Id": "D06Z01S21[E]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S15[NW]",
		"Logic": "D06Z01S21[E] || canBeatLegionary"
	},
	{
		"Id": "D06Z01S22[Sword]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S23[Sword]"
	},
	{
		"Id": "D06Z01S23[Sword]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S22[Sword]"
	},
	{
		"Id": "D06Z01S23[E]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S20[W]"
	},
	{
		"Id": "D06Z01S23[S]",
		"Direction": 3,
		"OriginalDoor": "D04Z02S06[N]",
		"Type": 1
	},
	{
		"Id": "D06Z01S23[Cherubs]",
		"Direction": 5
	},
	{
		"Id": "D06Z01S24[W]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S04[Health]"
	},
	{
		"Id": "D06Z01S25[W]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S19[E]",
		"Logic": "D06Z01S25[W] || canBeatRooftopsBoss",
		"Type": 9
	},
	{
		"Id": "D06Z01S25[E]",
		"Direction": 2,
		"OriginalDoor": "D07Z01S01[W]",
		"Logic": "D06Z01S25[E] || canBeatRooftopsBoss",
		"Type": 9
	},
	{
		"Id": "D06Z01S26[W]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S17[E]"
	},

	{
		"Id": "D07Z01S01[W]",
		"Direction": 1,
		"OriginalDoor": "D06Z01S25[E]",
		"Type": 9
	},
	{
		"Id": "D07Z01S01[E]",
		"Direction": 2,
		"OriginalDoor": "D07Z01S02[W]",
		"Type": 9
	},
	{
		"Id": "D07Z01S02[W]",
		"Direction": 1,
		"OriginalDoor": "D07Z01S01[E]",
		"Type": 9
	},
	{
		"Id": "D07Z01S02[E]",
		"Direction": 2,
		"OriginalDoor": "D07Z01S03[W]",
		"Type": 9
	},
	{
		"Id": "D07Z01S03[W]",
		"Direction": 1,
		"OriginalDoor": "D07Z01S02[E]",
		"Type": 9
	},

	{
		"Id": "D08Z01S01[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z03S06[E]",
		"Type": 1,
		"Logic": "D08Z01S01[W] || canBeatBridgeBoss"
	},
	{
		"Id": "D08Z01S01[E]",
		"Direction": 2,
		"OriginalDoor": "D08Z02S01[W]",
		"Type": 1,
		"Logic": "holyWounds >= 3 && (D08Z01S01[E] || D08Z01S01[Cherubs] || canBeatBridgeBoss)"
	},
	{
		"Id": "D08Z01S01[Cherubs]",
		"Direction": 5
	},
	{
		"Id": "D08Z01S02[NE]",
		"Direction": 2,
		"OriginalDoor": "D08Z03S03[W]",
		"Type": 1,
		"VisibilityFlags": 1
	},
	{
		"Id": "D08Z01S02[SE]",
		"Direction": 2,
		"OriginalDoor": "D08Z02S03[W]",
		"Type": 1
	},
	{
		"Id": "D08Z01S02[-Cherubs]",
		"Direction": 6,
		"OriginalDoor": "D08Z01S01[Cherubs]",
		"Logic": "linen"
	},
	
	{
		"Id": "D08Z02S01[W]",
		"Direction": 1,
		"OriginalDoor": "D08Z01S01[E]",
		"Type": 1
	},
	{
		"Id": "D08Z02S01[SE]",
		"Direction": 2,
		"OriginalDoor": "D08Z02S02[W]"
	},
	{
		"Id": "D08Z02S01[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z01S01[W]",
		"Type": 1
	},
	{
		"Id": "D08Z02S01[N]",
		"Direction": 0,
		"OriginalDoor": "D08Z02S03[S]"
	},
	{
		"Id": "D08Z02S02[W]",
		"Direction": 1,
		"OriginalDoor": "D08Z02S01[SE]"
	},
	{
		"Id": "D08Z02S03[W]",
		"Direction": 1,
		"OriginalDoor": "D08Z01S02[SE]",
		"Type": 1,
		"Logic": "brokeBotTCStatue"
	},
	{
		"Id": "D08Z02S03[E]",
		"Direction": 2,
		"OriginalDoor": "D08Z03S01[W]",
		"Type": 1
	},
	{
		"Id": "D08Z02S03[S]",
		"Direction": 3,
		"OriginalDoor": "D08Z02S01[N]"
	},
	
	{
		"Id": "D08Z03S01[W]",
		"Direction": 1,
		"OriginalDoor": "D08Z02S03[E]",
		"Type": 1
	},
	{
		"Id": "D08Z03S01[E]",
		"Direction": 2,
		"OriginalDoor": "D08Z03S02[SW]",
		"Logic": "verses >= 4"
	},
	{
		"Id": "D08Z03S02[SW]",
		"Direction": 1,
		"OriginalDoor": "D08Z03S01[E]"
	},
	{
		"Id": "D08Z03S02[NW]",
		"Direction": 1,
		"OriginalDoor": "D08Z03S03[E]",
		"Logic": "D08Z03S02[NW] || wallClimb"
	},
	{
		"Id": "D08Z03S03[W]",
		"Direction": 1,
		"OriginalDoor": "D08Z01S02[NE]",
		"Type": 1,
		"Logic": "D08Z03S03[W] || canBeatHallBoss"
	},
	{
		"Id": "D08Z03S03[E]",
		"Direction": 2,
		"OriginalDoor": "D08Z03S02[NW]",
		"Logic": "D08Z03S03[E] || canBeatHallBoss"
	},
	
	{
		"Id": "D09Z01S01[W]",
		"Direction": 1,
		"OriginalDoor": "D09Z01S11[E]"
	},
	{
		"Id": "D09Z01S01[E]",
		"Direction": 2,
		"OriginalDoor": "D06Z01S13[W]",
		"Type": 1
	},
	{
		"Id": "D09Z01S02[SW]",
		"Direction": 1,
		"OriginalDoor": "D09Z01S07[E]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S02[Cell2]" ]
	},
	{
		"Id": "D09Z01S02[NW]",
		"Direction": 1,
		"OriginalDoor": "D09Z01S07[NE]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S02[NW]", "D09Z01S02[N]", "D09Z01S02[Cell1]", "D09Z01S02[Cell6]", "D09Z01S02[Cell4]", "D09Z01S02[Cell3]", "D09Z01S02[Cell22]", "D09Z01S02[Cell23]" ]
	},
	{
		"Id": "D09Z01S02[N]",
		"Direction": 0,
		"OriginalDoor": "D09Z01S11[S]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S02[NW]", "D09Z01S02[N]", "D09Z01S02[Cell1]", "D09Z01S02[Cell6]", "D09Z01S02[Cell4]", "D09Z01S02[Cell3]", "D09Z01S02[Cell22]", "D09Z01S02[Cell23]" ]
	},
	{
		"Id": "D09Z01S02[Cell1]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell1]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S02[NW]", "D09Z01S02[N]", "D09Z01S02[Cell1]", "D09Z01S02[Cell6]", "D09Z01S02[Cell4]", "D09Z01S02[Cell3]", "D09Z01S02[Cell22]", "D09Z01S02[Cell23]" ],
		"Logic": "bronzeKey"
	},
	{
		"Id": "D09Z01S02[Cell6]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell6]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S02[NW]", "D09Z01S02[N]", "D09Z01S02[Cell1]", "D09Z01S02[Cell6]", "D09Z01S02[Cell4]", "D09Z01S02[Cell3]", "D09Z01S02[Cell22]", "D09Z01S02[Cell23]" ],
		"Logic": "silverKey"
	},
	{
		"Id": "D09Z01S02[Cell5]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell5]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D09Z01S02[Cell4]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell4]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S02[NW]", "D09Z01S02[N]", "D09Z01S02[Cell1]", "D09Z01S02[Cell6]", "D09Z01S02[Cell4]", "D09Z01S02[Cell3]", "D09Z01S02[Cell22]", "D09Z01S02[Cell23]" ],
		"Logic": "goldKey"
	},
	{
		"Id": "D09Z01S02[Cell2]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell2]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S02[SW]" ]
	},
	{
		"Id": "D09Z01S02[Cell3]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell3]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S02[NW]", "D09Z01S02[N]", "D09Z01S02[Cell1]", "D09Z01S02[Cell6]", "D09Z01S02[Cell4]", "D09Z01S02[Cell3]", "D09Z01S02[Cell22]", "D09Z01S02[Cell23]" ],
		"Logic": "bronzeKey"
	},
	{
		"Id": "D09Z01S02[Cell22]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell22]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S02[NW]", "D09Z01S02[N]", "D09Z01S02[Cell1]", "D09Z01S02[Cell6]", "D09Z01S02[Cell4]", "D09Z01S02[Cell3]", "D09Z01S02[Cell22]", "D09Z01S02[Cell23]" ]
	},
	{
		"Id": "D09Z01S02[Cell23]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell23]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S02[NW]", "D09Z01S02[N]", "D09Z01S02[Cell1]", "D09Z01S02[Cell6]", "D09Z01S02[Cell4]", "D09Z01S02[Cell3]", "D09Z01S02[Cell22]", "D09Z01S02[Cell23]" ],
		"Logic": "bronzeKey"
	},
	{
		"Id": "D09Z01S03[W]",
		"Direction": 1,
		"OriginalDoor": "D09Z01S05[SE]",
		"Logic": "D09Z01S03[N] && canBeatPrisonBoss"
	},
	{
		"Id": "D09Z01S03[N]",
		"Direction": 5
	},
	{
		"Id": "D09Z01S04[W]",
		"Direction": 1,
		"OriginalDoor": "D09Z01S06[E]"
	},
	{
		"Id": "D09Z01S04[E]",
		"Direction": 2,
		"OriginalDoor": "D09Z01S11[W]"
	},
	{
		"Id": "D09Z01S04[S]",
		"Direction": 3,
		"OriginalDoor": "D09Z01S07[N]"
	},
	{
		"Id": "D09Z01S05[W]",
		"Direction": 1,
		"OriginalDoor": "D09Z01S13[E]"
	},
	{
		"Id": "D09Z01S05[SE]",
		"Direction": 2,
		"OriginalDoor": "D09Z01S03[W]"
	},
	{
		"Id": "D09Z01S05[NE]",
		"Direction": 2,
		"OriginalDoor": "D09Z01S08[W]"
	},
	{
		"Id": "D09Z01S06[-E]",
		"Direction": 1,
		"OriginalDoor": "D02Z03S10[-W]",
		"Type": 1,
		"Logic": "peaksKey"
	},
	{
		"Id": "D09Z01S06[E]",
		"Direction": 2,
		"OriginalDoor": "D09Z01S04[W]"
	},
	{
		"Id": "D09Z01S07[SW]",
		"Direction": 1,
		"OriginalDoor": "D09Z01S09[E]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S07[SW]", "D09Z01S07[SE]", "D09Z01S07[W]", "D09Z01S07[E]" ]
	},
	{
		"Id": "D09Z01S07[SE]",
		"Direction": 2,
		"OriginalDoor": "D09Z01S10[W]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S07[SW]", "D09Z01S07[SE]", "D09Z01S07[W]", "D09Z01S07[E]" ]
	},
	{
		"Id": "D09Z01S07[W]",
		"Direction": 1,
		"OriginalDoor": "D09Z01S08[SE]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S07[SW]", "D09Z01S07[SE]", "D09Z01S07[W]", "D09Z01S07[E]" ]
	},
	{
		"Id": "D09Z01S07[E]",
		"Direction": 2,
		"OriginalDoor": "D09Z01S02[SW]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S07[SW]", "D09Z01S07[SE]", "D09Z01S07[W]", "D09Z01S07[E]" ]
	},
	{
		"Id": "D09Z01S07[NW]",
		"Direction": 1,
		"OriginalDoor": "D09Z01S08[NE]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S07[N]" ]
	},
	{
		"Id": "D09Z01S07[N]",
		"Direction": 0,
		"OriginalDoor": "D09Z01S04[S]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S07[NW]" ]
	},
	{
		"Id": "D09Z01S07[NE]",
		"Direction": 2,
		"OriginalDoor": "D09Z01S02[NW]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S07[SW]", "D09Z01S07[SE]", "D09Z01S07[W]", "D09Z01S07[E]" ],
		"Logic": "D09Z01S07[NE] || blood"
	},
	{
		"Id": "D09Z01S08[W]",
		"Direction": 1,
		"OriginalDoor": "D09Z01S05[NE]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S08[Cell14]" ],
		"Logic": "openedWotHPGate"
	},
	{
		"Id": "D09Z01S08[S]",
		"Direction": 6,
		"OriginalDoor": "D09Z01S03[N]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S08[W]", "D09Z01S08[Cell14]" ]
	},
	{
		"Id": "D09Z01S08[SE]",
		"Direction": 2,
		"OriginalDoor": "D09Z01S07[W]",
		"Logic": "D09Z01S08[SE] || D09Z01S08[Cell15] || D09Z01S08[Cell16] || D09Z01S08[Cell18] || D09Z01S08[Cell17] && dash"
	},
	{
		"Id": "D09Z01S08[NE]",
		"Direction": 2,
		"OriginalDoor": "D09Z01S07[NW]",
		"Logic": "D09Z01S08[NE] || D09Z01S08[Cell7] || D09Z01S08[Cell17] && dash"
	},
	{
		"Id": "D09Z01S08[Cell14]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell14]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S08[W]" ]
	},
	{
		"Id": "D09Z01S08[Cell15]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell15]",
		"Logic": "silverKey && (D09Z01S08[SE] || D09Z01S08[Cell15] || D09Z01S08[Cell16] || D09Z01S08[Cell18] || D09Z01S08[Cell17] && dash)"
	},
	{
		"Id": "D09Z01S08[Cell7]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell7]",
		"Logic": "goldKey && (D09Z01S08[NE] || D09Z01S08[Cell7] || D09Z01S08[Cell17] && dash)"
	},
	{
		"Id": "D09Z01S08[Cell16]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell16]",
		"Logic": "goldKey && (D09Z01S08[SE] || D09Z01S08[Cell15] || D09Z01S08[Cell16] || D09Z01S08[Cell18] || D09Z01S08[Cell17] && dash)"
	},
	{
		"Id": "D09Z01S08[Cell18]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell18]",
		"Logic": "silverKey && (D09Z01S08[SE] || D09Z01S08[Cell15] || D09Z01S08[Cell16] || D09Z01S08[Cell18] || D09Z01S08[Cell17] && dash)"
	},
	{
		"Id": "D09Z01S08[Cell17]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell17]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D09Z01S09[SW]",
		"Direction": 1,
		"OriginalDoor": "D04Z01S06[E]",
		"Type": 1,
		"Logic": "D09Z01S09[Cell21] || D09Z01S09[Cell20] || D09Z01S09[SW] || D09Z01S09[E] || dash"
	},
	{
		"Id": "D09Z01S09[NW]",
		"Direction": 1,
		"OriginalDoor": "D09Z01S12[E]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S09[Cell19]", "D09Z01S09[Cell24]" ],
		"Logic": "D09Z01S09[NW] || D09Z01S09[Cell19] || dash"
	},
	{
		"Id": "D09Z01S09[E]",
		"Direction": 2,
		"OriginalDoor": "D09Z01S07[SW]",
		"Logic": "D09Z01S09[Cell21] || D09Z01S09[Cell20] || D09Z01S09[SW] || D09Z01S09[E] || dash"
	},
	{
		"Id": "D09Z01S09[Cell24]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell24]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S09[NW]", "D09Z01S09[Cell19]" ],
		"Logic": "D09Z01S09[Cell24] || dash"
	},
	{
		"Id": "D09Z01S09[Cell19]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell19]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S09[NW]", "D09Z01S09[Cell24]" ],
		"Logic": "D09Z01S09[NW] || D09Z01S09[Cell19] || dash"
	},
	{
		"Id": "D09Z01S09[Cell20]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell20]",
		"Logic": "silverKey && (D09Z01S09[Cell21] || D09Z01S09[Cell20] || D09Z01S09[SW] || D09Z01S09[E] || dash)"
	},
	{
		"Id": "D09Z01S09[Cell21]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell21]",
		"Logic": "goldKey && (D09Z01S09[Cell21] || D09Z01S09[Cell20] || D09Z01S09[SW] || D09Z01S09[E] || dash)"
	},
	{
		"Id": "D09Z01S10[W]",
		"Direction": 1,
		"OriginalDoor": "D09Z01S07[SE]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S10[Cell12]", "D09Z01S10[Cell10]", "D09Z01S10[Cell11]" ]
	},
	{
		"Id": "D09Z01S10[Cell13]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell13]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D09Z01S10[Cell12]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell12]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S10[W]", "D09Z01S10[Cell10]", "D09Z01S10[Cell11]" ],
		"Logic": "bronzeKey"
	},
	{
		"Id": "D09Z01S10[Cell10]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell10]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S10[W]", "D09Z01S10[Cell12]", "D09Z01S10[Cell11]" ],
		"Logic": "silverKey"
	},
	{
		"Id": "D09Z01S10[Cell11]",
		"Direction": 4,
		"OriginalDoor": "D09BZ01S01[Cell11]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09Z01S10[W]", "D09Z01S10[Cell12]", "D09Z01S10[Cell10]" ],
		"Logic": "silverKey"
	},
	{
		"Id": "D09Z01S11[W]",
		"Direction": 1,
		"OriginalDoor": "D09Z01S04[E]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D09Z01S11[E]",
		"Direction": 2,
		"OriginalDoor": "D09Z01S01[W]"
	},
	{
		"Id": "D09Z01S11[S]",
		"Direction": 3,
		"OriginalDoor": "D09Z01S02[N]"
	},
	{
		"Id": "D09Z01S12[E]",
		"Direction": 2,
		"OriginalDoor": "D09Z01S09[NW]"
	},
	{
		"Id": "D09Z01S13[E]",
		"Direction": 2,
		"OriginalDoor": "D09Z01S05[W]"
	},
	{
		"Id": "D09BZ01S01[Cell1]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S02[Cell1]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D09BZ01S01[Cell2]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S02[Cell2]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09BZ01S01[Cell3]" ]
	},
	{
		"Id": "D09BZ01S01[Cell3]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S02[Cell3]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09BZ01S01[Cell2]" ]
	},
	{
		"Id": "D09BZ01S01[Cell4]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S02[Cell4]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09BZ01S01[Cell5]" ]
	},
	{
		"Id": "D09BZ01S01[Cell5]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S02[Cell5]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09BZ01S01[Cell4]" ]
	},
	{
		"Id": "D09BZ01S01[Cell6]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S02[Cell6]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D09BZ01S01[Cell7]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S08[Cell7]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D09BZ01S01[Cell10]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S10[Cell10]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D09BZ01S01[Cell11]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S10[Cell11]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D09BZ01S01[Cell12]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S10[Cell12]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09BZ01S01[Cell13]" ]
	},
	{
		"Id": "D09BZ01S01[Cell13]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S10[Cell13]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09BZ01S01[Cell12]" ]
	},
	{
		"Id": "D09BZ01S01[Cell14]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S08[Cell14]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09BZ01S01[Cell15]" ]
	},
	{
		"Id": "D09BZ01S01[Cell15]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S08[Cell15]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09BZ01S01[Cell14]" ]
	},
	{
		"Id": "D09BZ01S01[Cell16]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S08[Cell16]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D09BZ01S01[Cell17]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S08[Cell17]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09BZ01S01[Cell18]" ]
	},
	{
		"Id": "D09BZ01S01[Cell18]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S08[Cell18]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D09BZ01S01[Cell19]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S09[Cell19]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09BZ01S01[Cell20]" ]
	},
	{
		"Id": "D09BZ01S01[Cell20]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S09[Cell20]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09BZ01S01[Cell19]" ]
	},
	{
		"Id": "D09BZ01S01[Cell21]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S09[Cell21]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D09BZ01S01[Cell22]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S02[Cell22]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D09BZ01S01[Cell23]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S02[Cell23]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D09BZ01S01[Cell22]" ],
		"Logic": "bronzeKey"
	},
	{
		"Id": "D09BZ01S01[Cell24]",
		"Direction": 7,
		"OriginalDoor": "D09Z01S09[Cell24]",
		"VisibilityFlags": 1
	},
	
	{
		"Id": "D17Z01S01[E]",
		"Direction": 2,
		"OriginalDoor": "D17Z01S02[W]"
	},
	{
		"Id": "D17Z01S01[Cherubs1]",
		"Direction": 5
	},
	{
		"Id": "D17Z01S01[Cherubs2]",
		"Direction": 5
	},
	{
		"Id": "D17Z01S01[Cherubs3]",
		"Direction": 5
	},
	{
		"Id": "D17Z01S02[W]",
		"Direction": 1,
		"OriginalDoor": "D17Z01S01[E]",
		"Logic": "D17Z01S02[W] || dash"
	},
	{
		"Id": "D17Z01S02[E]",
		"Direction": 2,
		"OriginalDoor": "D17Z01S05[W]",
		"Logic": "D17Z01S02[N] || D17Z01S02[E] || dash"
	},
	{
		"Id": "D17Z01S02[N]",
		"Direction": 0,
		"OriginalDoor": "D17Z01S10[S]",
		"Logic": "D17Z01S02[N] || blood && (D17Z01S02[E] || D17Z01S02[W] && dash)"
	},
	{
		"Id": "D17Z01S03[W]",
		"Direction": 1,
		"OriginalDoor": "D17Z01S11[E]"
	},
	{
		"Id": "D17Z01S03[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z01S07[W]",
		"Type": 1
	},
	{
		"Id": "D17Z01S03[relic]",
		"Direction": 4,
		"OriginalDoor": "D17BZ01S01[relic]",
		"Logic": "elderKey"
	},
	{
		"Id": "D17Z01S04[W]",
		"Direction": 1,
		"OriginalDoor": "D17Z01S12[E]"
	},
	{
		"Id": "D17Z01S04[S]",
		"Direction": 3,
		"OriginalDoor": "D17Z01S07[N]"
	},
	{
		"Id": "D17Z01S04[FrontL]",
		"Direction": 4,
		"OriginalDoor": "D17BZ02S01[FrontL]"
	},
	{
		"Id": "D17Z01S04[N]",
		"Direction": 0,
		"OriginalDoor": "D17Z01S05[S]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D17Z01S04[FrontR]" ]
	},
	{
		"Id": "D17Z01S04[FrontR]",
		"Direction": 4,
		"OriginalDoor": "D17BZ02S01[FrontR]",
		"VisibilityFlags": 3,
		"RequiredDoors": [ "D17Z01S04[N]" ]
	},
	{
		"Id": "D17Z01S05[W]",
		"Direction": 1,
		"OriginalDoor": "D17Z01S02[E]"
	},
	{
		"Id": "D17Z01S05[E]",
		"Direction": 2,
		"OriginalDoor": "D17Z01S11[W]"
	},
	{
		"Id": "D17Z01S05[S]",
		"Direction": 3,
		"OriginalDoor": "D17Z01S04[N]",
		"Logic": "openedBotSSLadder"
	},
	{
		"Id": "D17Z01S06[E]",
		"Direction": 2,
		"OriginalDoor": "D17Z01S07[W]"
	},
	{
		"Id": "D17Z01S07[SW]",
		"Direction": 1,
		"OriginalDoor": "D17Z01S08[E]"
	},
	{
		"Id": "D17Z01S07[SE]",
		"Direction": 2,
		"OriginalDoor": "D03Z01S05[W]",
		"Type": 1
	},
	{
		"Id": "D17Z01S07[W]",
		"Direction": 1,
		"OriginalDoor": "D17Z01S06[E]"
	},
	{
		"Id": "D17Z01S07[NW]",
		"Direction": 1,
		"OriginalDoor": "D17Z01S09[E]"
	},
	{
		"Id": "D17Z01S07[N]",
		"Direction": 0,
		"OriginalDoor": "D17Z01S04[S]"
	},
	{
		"Id": "D17Z01S08[E]",
		"Direction": 2,
		"OriginalDoor": "D17Z01S07[SW]"
	},
	{
		"Id": "D17Z01S09[E]",
		"Direction": 2,
		"OriginalDoor": "D17Z01S07[NW]"
	},
	{
		"Id": "D17Z01S10[W]",
		"Direction": 1,
		"OriginalDoor": "D17Z01S13[E]",
		"Logic": "D17Z01S10[W] || blood || doubleJump"
	},
	{
		"Id": "D17Z01S10[S]",
		"Direction": 3,
		"OriginalDoor": "D17Z01S02[N]"
	},
	{
		"Id": "D17Z01S11[W]",
		"Direction": 1,
		"OriginalDoor": "D17Z01S05[E]",
		"Logic": "D17Z01S11[W] || canBeatBrotherhoodBoss"
	},
	{
		"Id": "D17Z01S11[E]",
		"Direction": 2,
		"OriginalDoor": "D17Z01S03[W]",
		"Logic": "D17Z01S11[E] || canBeatBrotherhoodBoss"
	},
	{
		"Id": "D17Z01S12[E]",
		"Direction": 2,
		"OriginalDoor": "D17Z01S04[W]"
	},
	{
		"Id": "D17Z01S13[W]",
		"Direction": 1,
		"OriginalDoor": "D17Z01S14[E]"
	},
	{
		"Id": "D17Z01S13[E]",
		"Direction": 2,
		"OriginalDoor": "D17Z01S10[W]"
	},
	{
		"Id": "D17Z01S14[W]",
		"Direction": 1,
		"OriginalDoor": "D17Z01S15[E]",
		"Logic": "scapular && (D17Z01S14[W] || blood)"
	},
	{
		"Id": "D17Z01S14[E]",
		"Direction": 2,
		"OriginalDoor": "D17Z01S13[W]",
		"Logic": "D17Z01S14[E] || blood"
	},
	{
		"Id": "D17Z01S14[-Cherubs1]",
		"Direction": 6,
		"OriginalDoor": "D17Z01S01[Cherubs1]",
		"Logic": "linen && (D17Z01S14[W] || blood || canCrossGap11)"
	},
	{
		"Id": "D17Z01S14[-Cherubs2]",
		"Direction": 6,
		"OriginalDoor": "D17Z01S01[Cherubs2]",
		"Logic": "linen && (D17Z01S14[E] && canCrossGap8 || D17Z01S14[W] && canCrossGap10 || blood)"
	},
	{
		"Id": "D17Z01S14[-Cherubs3]",
		"Direction": 6,
		"OriginalDoor": "D17Z01S01[Cherubs3]",
		"Logic": "linen && (D17Z01S14[E] || blood)"
	},
	{
		"Id": "D17Z01S15[E]",
		"Direction": 2,
		"OriginalDoor": "D17Z01S14[W]"
	},
	{
		"Id": "D17BZ01S01[relic]",
		"Direction": 7,
		"OriginalDoor": "D17Z01S03[relic]"
	},
	{
		"Id": "D17BZ02S01[FrontL]",
		"Direction": 7,
		"OriginalDoor": "D17Z01S04[FrontL]",
		"VisibilityFlags": 1
	},
	{
		"Id": "D17BZ02S01[FrontR]",
		"Direction": 7,
		"OriginalDoor": "D17Z01S04[FrontR]",
		"Logic": "D17BZ02S01[FrontR] || dash && wallClimb"
	},
	
	{
		"Id": "D20Z01S01[W]",
		"Direction": 1,
		"OriginalDoor": "D03Z02S15[E]",
		"Type": 1
	},
	{
		"Id": "D20Z01S01[E]",
		"Direction": 2,
		"OriginalDoor": "D20Z01S02[W]"
	},
	{
		"Id": "D20Z01S01[S]",
		"Direction": 3,
		"OriginalDoor": "D20Z01S04[N]"
	},
	{
		"Id": "D20Z01S01[Cherubs]",
		"Direction": 5
	},
	{
		"Id": "D20Z01S02[W]",
		"Direction": 1,
		"OriginalDoor": "D20Z01S01[E]"
	},
	{
		"Id": "D20Z01S02[E]",
		"Direction": 2,
		"OriginalDoor": "D20Z01S03[W]"
	},
	{
		"Id": "D20Z01S03[W]",
		"Direction": 1,
		"OriginalDoor": "D20Z01S02[E]"
	},
	{
		"Id": "D20Z01S03[N]",
		"Direction": 0,
		"OriginalDoor": "D03Z01S01[S]",
		"Type": 1
	},
	{
		"Id": "D20Z01S04[W]",
		"Direction": 1,
		"OriginalDoor": "D20Z01S05[E]"
	},
	{
		"Id": "D20Z01S04[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S24[W]",
		"Type": 1,
		"Logic": "openedDCGateW"
	},
	{
		"Id": "D20Z01S04[N]",
		"Direction": 0,
		"OriginalDoor": "D20Z01S01[S]"
	},
	{
		"Id": "D20Z01S05[W]",
		"Direction": 1,
		"OriginalDoor": "D20Z01S06[NE]"
	},
	{
		"Id": "D20Z01S05[E]",
		"Direction": 2,
		"OriginalDoor": "D20Z01S04[W]"
	},
	{
		"Id": "D20Z01S06[NE]",
		"Direction": 2,
		"OriginalDoor": "D20Z01S05[W]"
	},
	{
		"Id": "D20Z01S06[SE]",
		"Direction": 2,
		"OriginalDoor": "D20Z01S07[NW]"
	},
	{
		"Id": "D20Z01S07[NW]",
		"Direction": 1,
		"OriginalDoor": "D20Z01S06[SE]"
	},
	{
		"Id": "D20Z01S07[NE]",
		"Direction": 2,
		"OriginalDoor": "D20Z01S08[W]"
	},
	{
		"Id": "D20Z01S07[SE]",
		"Direction": 2,
		"OriginalDoor": "D20Z01S09[W]"
	},
	{
		"Id": "D20Z01S08[W]",
		"Direction": 1,
		"OriginalDoor": "D20Z01S07[NE]"
	},
	{
		"Id": "D20Z01S09[W]",
		"Direction": 1,
		"OriginalDoor": "D20Z01S07[SE]",
		"Logic": "D20Z01S09[W] || dash"
	},
	{
		"Id": "D20Z01S09[E]",
		"Direction": 2,
		"OriginalDoor": "D01Z05S25[EchoesW]",
		"Type": 1,
		"Logic": "D20Z01S09[E] || blood && dash"
	},
	{
		"Id": "D20Z01S10[W]",
		"Direction": 1,
		"OriginalDoor": "D01Z05S25[EchoesE]",
		"Type": 1,
		"Logic": "D20Z01S10[W] || blood && dash"
	},
	{
		"Id": "D20Z01S10[E]",
		"Direction": 2,
		"OriginalDoor": "D20Z01S11[W]",
		"Logic": "D20Z01S10[E] || blood && dash"
	},
	{
		"Id": "D20Z01S11[W]",
		"Direction": 1,
		"OriginalDoor": "D20Z01S10[E]"
	},
	{
		"Id": "D20Z01S11[NW]",
		"Direction": 1,
		"OriginalDoor": "D20Z01S12[E]"
	},
	{
		"Id": "D20Z01S11[NE]",
		"Direction": 2,
		"OriginalDoor": "D20Z01S13[W]"
	},
	{
		"Id": "D20Z01S11[SE]",
		"Direction": 2,
		"OriginalDoor": "D20Z02S12[W]",
		"Type": 1
	},
	{
		"Id": "D20Z01S12[E]",
		"Direction": 2,
		"OriginalDoor": "D20Z01S11[NW]"
	},
	{
		"Id": "D20Z01S13[W]",
		"Direction": 1,
		"OriginalDoor": "D20Z01S11[NE]"
	},
	{
		"Id": "D20Z01S13[E]",
		"Direction": 2,
		"OriginalDoor": "D20Z02S11[NW]",
		"Type": 1
	},
	{
		"Id": "D20Z01S13[N]",
		"Direction": 0,
		"OriginalDoor": "D20Z01S14[S]"
	},
	{
		"Id": "D20Z01S14[S]",
		"Direction": 3,
		"OriginalDoor": "D20Z01S13[N]"
	},
	{
		"Id": "D20Z01S14[E]",
		"Direction": 2,
		"OriginalDoor": "D20Z03S01[W]",
		"Type": 1
	},
	
	{
		"Id": "D20Z02S01[W]",
		"Direction": 1,
		"OriginalDoor": "D20Z02S03[SE]"
	},
	{
		"Id": "D20Z02S01[E]",
		"Direction": 2,
		"OriginalDoor": "D04Z02S24[SW]",
		"Type": 1
	},
	{
		"Id": "D20Z02S02[W]",
		"Direction": 1,
		"OriginalDoor": "D20Z02S03[NE]"
	},
	{
		"Id": "D20Z02S03[W]",
		"Direction": 1,
		"OriginalDoor": "D20Z02S04[E]"
	},
	{
		"Id": "D20Z02S03[NE]",
		"Direction": 2,
		"OriginalDoor": "D20Z02S02[W]",
		"Logic": "D20Z02S03[NE] || canWalkOnRoot || canCrossGap5"
	},
	{
		"Id": "D20Z02S03[SE]",
		"Direction": 2,
		"OriginalDoor": "D20Z02S01[W]"
	},
	{
		"Id": "D20Z02S04[W]",
		"Direction": 1,
		"OriginalDoor": "D20Z02S05[E]",
		"Logic": "D20Z02S04[W] || dash"
	},
	{
		"Id": "D20Z02S04[E]",
		"Direction": 2,
		"OriginalDoor": "D20Z02S03[W]",
		"Logic": "D20Z02S04[E] || dash"
	},
	{
		"Id": "D20Z02S05[SW]",
		"Direction": 1,
		"OriginalDoor": "D20Z02S06[SE]"
	},
	{
		"Id": "D20Z02S05[NW]",
		"Direction": 1,
		"OriginalDoor": "D20Z02S06[NE]",
		"Logic": "D20Z02S05[NW] || nail || canCrossGap3"
	},
	{
		"Id": "D20Z02S05[E]",
		"Direction": 2,
		"OriginalDoor": "D20Z02S04[W]"
	},
	{
		"Id": "D20Z02S06[SW]",
		"Direction": 1,
		"OriginalDoor": "D20Z02S09[E]"
	},
	{
		"Id": "D20Z02S06[SE]",
		"Direction": 2,
		"OriginalDoor": "D20Z02S05[SW]"
	},
	{
		"Id": "D20Z02S06[NW]",
		"Direction": 1,
		"OriginalDoor": "D20Z02S07[E]",
		"Logic": "D20Z02S06[NW] || D20Z02S06[NE] || doubleJump || canClimbOnRoot || canDiveLaser"
	},
	{
		"Id": "D20Z02S06[NE]",
		"Direction": 2,
		"OriginalDoor": "D20Z02S05[NW]",
		"Logic": "D20Z02S06[NW] || D20Z02S06[NE] || doubleJump || canClimbOnRoot || canDiveLaser"
	},
	{
		"Id": "D20Z02S07[W]",
		"Direction": 1,
		"OriginalDoor": "D20Z02S08[E]"
	},
	{
		"Id": "D20Z02S07[E]",
		"Direction": 2,
		"OriginalDoor": "D20Z02S06[NW]"
	},
	{
		"Id": "D20Z02S08[E]",
		"Direction": 2,
		"OriginalDoor": "D20Z02S07[W]"
	},
	{
		"Id": "D20Z02S09[W]",
		"Direction": 1,
		"OriginalDoor": "D20Z02S10[E]"
	},
	{
		"Id": "D20Z02S09[E]",
		"Direction": 2,
		"OriginalDoor": "D20Z02S06[SW]"
	},
	{
		"Id": "D20Z02S10[W]",
		"Direction": 1,
		"OriginalDoor": "D20Z02S11[E]"
	},
	{
		"Id": "D20Z02S10[E]",
		"Direction": 2,
		"OriginalDoor": "D20Z02S09[W]"
	},
	{
		"Id": "D20Z02S11[SW]",
		"Direction": 1,
		"OriginalDoor": "D20Z02S12[E]"
	},
	{
		"Id": "D20Z02S11[NW]",
		"Direction": 1,
		"OriginalDoor": "D20Z01S13[E]",
		"Type": 1,
		"VisibilityFlags": 5,
		"RequiredDoors": [ "D20Z02S11[E]" ],
		"Logic": "D20Z02S11[NW] || mourningSkipAllowed && (doubleJump || canBreakTirana || D20Z02S11[E])"
	},
	{
		"Id": "D20Z02S11[E]",
		"Direction": 2,
		"OriginalDoor": "D20Z02S10[W]",
		"VisibilityFlags": 5,
		"Logic": "D20Z02S11[E] || mourningSkipAllowed && (doubleJump || canBreakTirana || D20Z02S11[NW] && canCrossGap5)"
	},
	{
		"Id": "D20Z02S12[W]",
		"Direction": 1,
		"OriginalDoor": "D20Z01S11[SE]",
		"Type": 1
	},
	{
		"Id": "D20Z02S12[E]",
		"Direction": 2,
		"OriginalDoor": "D20Z02S11[SW]"
	},
	
	{
		"Id": "D20Z03S01[W]",
		"Direction": 1,
		"OriginalDoor": "D20Z01S14[E]",
		"Type": 1
	},
]