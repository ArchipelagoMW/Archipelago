from typing import List, TypedDict


class DoorDict(TypedDict):
    id: str
    direction: int
    parent: str | None


door_table: List[DoorDict] = [
	{
		"id": "D01Z01S01[W]",
		"direction": 1,
		"parent": "D01Z01S07[E]"
	},
	{
		"id": "D01Z01S01[E]",
		"direction": 2,
		"parent": "D01Z01S02[W]"
	},
	{
		"id": "D01Z01S01[S]",
		"direction": 2,
		"parent": "D01Z06S01[N]",
	},
	{
		"id": "D01Z01S02[W]",
		"direction": 1,
		"parent": "D01Z01S01[E]"
	},
	{
		"id": "D01Z01S02[E]",
		"direction": 2,
		"parent": "D01Z01S03[W]"
	},
	{
		"id": "D01Z01S03[W]",
		"direction": 1,
		"parent": "D01Z01S02[E]"
	},
	{
		"id": "D01Z01S03[E]",
		"direction": 2,
		"parent": "D01Z02S01[W]"
	},
	{
		"id": "D01Z01S07[W]",
		"direction": 1,
		"parent": "D17Z01S03[E]"
	},
	{
		"id": "D01Z01S07[E]",
		"direction": 2,
		"parent": "D01Z01S01[W]"
	},

	{
		"id": "D01Z02S01[W]",
		"direction": 1,
		"parent": "D01Z01S03[E]"
	},
	{
		"id": "D01Z02S01[E]",
		"direction": 2,
		"parent": "D01Z02S02[W]"
	},
	{
		"id": "D01Z02S02[SW]",
		"direction": 1,
		"parent": "D01Z02S06[E]"
	},
	{
		"id": "D01Z02S02[SE]",
		"direction": 2,
		"parent": "D01Z02S04[W]"
	},
	{
		"id": "D01Z02S02[W]",
		"direction": 1,
		"parent": "D01Z02S01[E]"
	},
	{
		"id": "D01Z02S02[E]",
		"direction": 2,
		"parent": "D01Z02S03[W]"
	},
	{
		"id": "D01Z02S02[NE]",
		"direction": 2,
		"parent": "D01Z02S03[NW]"
	},
	{
		"id": "D01Z02S03[W]",
		"direction": 1,
		"parent": "D01Z02S02[E]"
	},
	{
		"id": "D01Z02S03[NW]",
		"direction": 1,
		"parent": "D01Z02S02[NE]",
	},
	{
		"id": "D01Z02S03[E]",
		"direction": 2,
		"parent": "D01Z02S05[W]"
	},
	{
		"id": "D01Z02S03[church]",
		"direction": 4,
		"parent": "D01BZ04S01[church]",
	},
	{
		"id": "D01Z02S03[Cherubs]",
		"direction": 5
	},
	{
		"id": "D01Z02S04[W]",
		"direction": 1,
		"parent": "D01Z02S02[SE]"
	},
	{
		"id": "D01Z02S04[E]",
		"direction": 2,
		"parent": "D01Z05S01[N]"
	},
	{
		"id": "D01Z02S04[Ossary]",
		"direction": 4,
		"parent": "D01BZ06S01[Ossary]"
	},
	{
		"id": "D01Z02S05[W]",
		"direction": 1,
		"parent": "D01Z02S03[E]"
	},
	{
		"id": "D01Z02S05[E]",
		"direction": 2,
		"parent": "D01Z03S01[W]"
	},
	{
		"id": "D01Z02S06[W]",
		"direction": 1,
		"parent": "D01Z02S07[E]",
	},
	{
		"id": "D01Z02S06[E]",
		"direction": 2,
		"parent": "D01Z02S02[SW]"
	},
	{
		"id": "D01Z02S07[E]",
		"direction": 2,
		"parent": "D01Z02S06[W]",
	},
	{
		"id": "D01BZ04S01[church]",
		"direction": 4,
		"parent": "D01Z02S03[church]"
	},
	{
		"id": "D01BZ06S01[Ossary]",
		"direction": 4,
		"parent": "D01Z02S04[Ossary]"
	},
	{
		"id": "D01BZ06S01[E]",
		"direction": 2,
		"parent": "D01BZ08S01[W]",
	},
	{
		"id": "D01BZ08S01[W]",
		"direction": 1,
		"parent": "D01BZ06S01[E]"
	},
	
	{
		"id": "D01Z03S01[W]",
		"direction": 1,
		"parent": "D01Z02S05[E]"
	},
	{
		"id": "D01Z03S01[E]",
		"direction": 2,
		"parent": "D01Z03S02[W]"
	},
	{
		"id": "D01Z03S01[SE]",
		"direction": 2,
		"parent": "D01Z03S02[SW]",
	},
	{
		"id": "D01Z03S02[W]",
		"direction": 1,
		"parent": "D01Z03S01[E]"
	},
	{
		"id": "D01Z03S02[SW]",
		"direction": 1,
		"parent": "D01Z03S01[SE]"
	},
	{
		"id": "D01Z03S02[E]",
		"direction": 2,
		"parent": "D01Z03S03[W]"
	},
	{
		"id": "D01Z03S02[S]",
		"direction": 3,
		"parent": "D01Z05S05[N]",
	},
	{
		"id": "D01Z03S03[W]",
		"direction": 1,
		"parent": "D01Z03S02[E]"
	},
	{
		"id": "D01Z03S03[E]",
		"direction": 2,
		"parent": "D01Z03S04[SW]"
	},
	{
		"id": "D01Z03S03[Cherubs]",
		"direction": 5
	},
	{
		"id": "D01Z03S03[-Cherubs]",
		"direction": 6,
		"parent": "D01Z05S06[Cherubs]",
	},
	{
		"id": "D01Z03S04[SW]",
		"direction": 1,
		"parent": "D01Z03S03[E]"
	},
	{
		"id": "D01Z03S04[W]",
		"direction": 1,
		"parent": "D01Z03S07[E]"
	},
	{
		"id": "D01Z03S04[NW]",
		"direction": 1,
		"parent": "D02Z01S01[SE]"
	},
	{
		"id": "D01Z03S04[SE]",
		"direction": 2,
		"parent": "D01Z03S05[W]"
	},
	{
		"id": "D01Z03S04[E]",
		"direction": 2,
		"parent": "D01Z03S06[W]"
	},
	{
		"id": "D01Z03S05[W]",
		"direction": 1,
		"parent": "D01Z03S04[SE]"
	},
	{
		"id": "D01Z03S05[E]",
		"direction": 2,
		"parent": "D01Z04S01[NW]"
	},
	{
		"id": "D01Z03S05[Cherubs]",
		"direction": 6,
		"parent": "D01Z05S11[Cherubs]",
	},
	{
		"id": "D01Z03S06[W]",
		"direction": 1,
		"parent": "D01Z03S04[E]"
	},
	{
		"id": "D01Z03S06[E]",
		"direction": 2,
		"parent": "D08Z01S01[W]"
	},
	{
		"id": "D01Z03S07[E]",
		"direction": 2,
		"parent": "D01Z03S04[W]"
	},
	{
		"id": "D01Z03S07[-Cherubs]",
		"direction": 6,
		"parent": "D01Z03S03[Cherubs]",
	},
	
	{
		"id": "D01Z04S01[NW]",
		"direction": 1,
		"parent": "D01Z03S05[E]"
	},
	{
		"id": "D01Z04S01[NE]",
		"direction": 2,
		"parent": "D01Z04S17[W]"
	},
	{
		"id": "D01Z04S01[W]",
		"direction": 1,
		"parent": "D01Z04S03[E]"
	},
	{
		"id": "D01Z04S01[E]",
		"direction": 2,
		"parent": "D01Z04S05[NW]"
	},
	{
		"id": "D01Z04S01[SE]",
		"direction": 2,
		"parent": "D01Z04S05[SW]",
	},
	{
		"id": "D01Z04S01[S]",
		"direction": 3,
		"parent": "D01Z04S15[N]",
	},
	{
		"id": "D01Z04S02[W]",
		"direction": 1,
		"parent": "D01Z04S13[NE]"
	},
	{
		"id": "D01Z04S03[E]",
		"direction": 2,
		"parent": "D01Z04S01[W]"
	},
	{
		"id": "D01Z04S05[NW]",
		"direction": 1,
		"parent": "D01Z04S01[E]"
	},
	{
		"id": "D01Z04S05[SW]",
		"direction": 1,
		"parent": "D01Z04S01[SE]"
	},
	{
		"id": "D01Z04S06[E]",
		"direction": 2,
		"parent": "D01Z04S07[W]"
	},
	{
		"id": "D01Z04S06[NW]",
		"direction": 1,
		"parent": "D01Z04S15[NE]"
	},
	{
		"id": "D01Z04S06[SW]",
		"direction": 1,
		"parent": "D01Z04S15[E]"
	},
	{
		"id": "D01Z04S07[W]",
		"direction": 1,
		"parent": "D01Z04S06[E]"
	},
	{
		"id": "D01Z04S08[E]",
		"direction": 2,
		"parent": "D01Z04S15[W]"
	},
	{
		"id": "D01Z04S09[W]",
		"direction": 1,
		"parent": "D01Z05S12[E]",
	},
	{
		"id": "D01Z04S09[E]",
		"direction": 2,
		"parent": "D01Z04S15[SW]"
	},
	{
		"id": "D01Z04S09[C]",
		"direction": 4,
		"parent": "D01BZ02S01[C]"
	},
	{
		"id": "D01Z04S10[NW]",
		"direction": 1,
		"parent": "D01Z04S15[SE]"
	},
	{
		"id": "D01Z04S10[SW]",
		"direction": 3,
		"parent": "D01Z04S11[NE]"
	},
	{
		"id": "D01Z04S10[SE]",
		"direction": 3,
		"parent": "D01Z04S12[NW]"
	},
	{
		"id": "D01Z04S11[NE]",
		"direction": 0,
		"parent": "D01Z04S10[SW]"
	},
	{
		"id": "D01Z04S12[NW]",
		"direction": 0,
		"parent": "D01Z04S10[SE]"
	},
	{
		"id": "D01Z04S12[W]",
		"direction": 1,
		"parent": "D01Z04S18[E]"
	},
	{
		"id": "D01Z04S12[SE]",
		"direction": 2,
		"parent": "D01Z04S13[NW]"
	},
	{
		"id": "D01Z04S13[NW]",
		"direction": 1,
		"parent": "D01Z04S12[SE]"
	},
	{
		"id": "D01Z04S13[NE]",
		"direction": 2,
		"parent": "D01Z04S02[W]"
	},
	{
		"id": "D01Z04S13[SW]",
		"direction": 1,
		"parent": "D01Z04S14[E]"
	},
	{
		"id": "D01Z04S13[SE]",
		"direction": 2,
		"parent": "D01Z04S16[W]",
	},
	{
		"id": "D01Z04S14[E]",
		"direction": 2,
		"parent": "D01Z04S13[SW]"
	},
	{
		"id": "D01Z04S15[N]",
		"direction": 0,
		"parent": "D01Z04S01[S]"
	},
	{
		"id": "D01Z04S15[NE]",
		"direction": 2,
		"parent": "D01Z04S06[NW]"
	},
	{
		"id": "D01Z04S15[W]",
		"direction": 1,
		"parent": "D01Z04S08[E]",
	},
	{
		"id": "D01Z04S15[E]",
		"direction": 2,
		"parent": "D01Z04S06[SW]",
	},
	{
		"id": "D01Z04S15[SW]",
		"direction": 1,
		"parent": "D01Z04S09[E]",
	},
	{
		"id": "D01Z04S15[SE]",
		"direction": 2,
		"parent": "D01Z04S10[NW]",
	},
	{
		"id": "D01Z04S16[W]",
		"direction": 1,
		"parent": "D01Z04S13[SE]"
	},
	{
		"id": "D01Z04S16[E]",
		"direction": 2,
		"parent": "D05Z02S12[W]"
	},
	{
		"id": "D01Z04S17[W]",
		"direction": 1,
		"parent": "D01Z04S01[NE]"
	},
	{
		"id": "D01Z04S18[W]",
		"direction": 1,
		"parent": "D01Z04S19[E]",
	},
	{
		"id": "D01Z04S18[E]",
		"direction": 2,
		"parent": "D01Z04S12[W]",
	},
	{
		"id": "D01Z04S19[W]",
		"direction": 1,
		"parent": "D01Z05S19[E]"
	},
	{
		"id": "D01Z04S19[E]",
		"direction": 2,
		"parent": "D01Z04S18[W]"
	},
	{
		"id": "D01BZ02S01[C]",
		"direction": 4,
		"parent": "D01Z04S09[C]"
	},
	
	{
		"id": "D01Z05S01[N]",
		"direction": 1,
		"parent": "D01Z02S04[E]"
	},
	{
		"id": "D01Z05S01[W]",
		"direction": 1,
		"parent": "D01Z05S27[E]"
	},
	{
		"id": "D01Z05S01[S]",
		"direction": 3,
		"parent": "D01Z05S02[N]"
	},
	{
		"id": "D01Z05S02[N]",
		"direction": 0,
		"parent": "D01Z05S01[S]"
	},
	{
		"id": "D01Z05S02[W]",
		"direction": 1,
		"parent": "D03Z01S01[NE]"
	},
	{
		"id": "D01Z05S02[E]",
		"direction": 2,
		"parent": "D01Z05S03[NW]",
	},
	{
		"id": "D01Z05S02[S]",
		"direction": 3,
		"parent": "D01Z05S20[N]",
	},
	{
		"id": "D01Z05S03[NW]",
		"direction": 1,
		"parent": "D01Z05S02[E]"
	},
	{
		"id": "D01Z05S03[NE]",
		"direction": 2,
		"parent": "D01Z05S04[W]"
	},
	{
		"id": "D01Z05S03[W]",
		"direction": 1,
		"parent": "D01Z05S07[E]"
	},
	{
		"id": "D01Z05S03[E]",
		"direction": 2,
		"parent": "D01Z05S08[W]"
	},
	{
		"id": "D01Z05S03[S]",
		"direction": 3,
		"parent": "D01Z05S13[N]"
	},
	{
		"id": "D01Z05S04[W]",
		"direction": 1,
		"parent": "D01Z05S03[NE]"
	},
	{
		"id": "D01Z05S04[E]",
		"direction": 2,
		"parent": "D01Z05S05[NW]"
	},
	{
		"id": "D01Z05S05[N]",
		"direction": 0,
		"parent": "D01Z03S02[S]"
	},
	{
		"id": "D01Z05S05[NW]",
		"direction": 1,
		"parent": "D01Z05S04[E]"
	},
	{
		"id": "D01Z05S05[NE]",
		"direction": 2,
		"parent": "D01Z05S06[W]"
	},
	{
		"id": "D01Z05S05[SW]",
		"direction": 1,
		"parent": "D01Z05S18[E]"
	},
	{
		"id": "D01Z05S05[E]",
		"direction": 2,
		"parent": "D01Z05S09[NW]"
	},
	{
		"id": "D01Z05S06[W]",
		"direction": 1,
		"parent": "D01Z05S05[NE]"
	},
	{
		"id": "D01Z05S06[Cherubs]",
		"direction": 5
	},
	{
		"id": "D01Z05S07[E]",
		"direction": 2,
		"parent": "D01Z05S03[W]"
	},
	{
		"id": "D01Z05S08[W]",
		"direction": 1,
		"parent": "D01Z05S03[E]"
	},
	{
		"id": "D01Z05S09[NW]",
		"direction": 1,
		"parent": "D01Z05S05[E]"
	},
	{
		"id": "D01Z05S09[SE]",
		"direction": 2,
		"parent": "D01Z05S10[W]"
	},
	{
		"id": "D01Z05S10[W]",
		"direction": 1,
		"parent": "D01Z05S09[SE]"
	},
	{
		"id": "D01Z05S10[NE]",
		"direction": 2,
		"parent": "D01Z05S11[W]"
	},
	{
		"id": "D01Z05S10[SE]",
		"direction": 2,
		"parent": "D01Z05S12[W]"
	},
	{
		"id": "D01Z05S10[S]",
		"direction": 3,
		"parent": "D01Z05S14[N]"
	},
	{
		"id": "D01Z05S11[W]",
		"direction": 1,
		"parent": "D01Z05S10[NE]"
	},
	{
		"id": "D01Z05S11[Cherubs]",
		"direction": 5
	},
	{
		"id": "D01Z05S12[W]",
		"direction": 1,
		"parent": "D01Z05S10[SE]"
	},
	{
		"id": "D01Z05S12[E]",
		"direction": 2,
		"parent": "D01Z04S09[W]"
	},
	{
		"id": "D01Z05S13[SW]",
		"direction": 3,
		"parent": "D01Z05S16[N]",
	},
	{
		"id": "D01Z05S13[N]",
		"direction": 0,
		"parent": "D01Z05S03[S]",
	},
	{
		"id": "D01Z05S13[E]",
		"direction": 2,
		"parent": "D01Z05S14[W]",
	},
	{
		"id": "D01Z05S14[W]",
		"direction": 1,
		"parent": "D01Z05S13[E]"
	},
	{
		"id": "D01Z05S14[N]",
		"direction": 0,
		"parent": "D01Z05S10[S]"
	},
	{
		"id": "D01Z05S14[SE]",
		"direction": 2,
		"parent": "D01Z05S15[W]"
	},
	{
		"id": "D01Z05S15[W]",
		"direction": 1,
		"parent": "D01Z05S14[SE]"
	},
	{
		"id": "D01Z05S15[SW]",
		"direction": 1,
		"parent": "D01Z05S22[E]"
	},
	{
		"id": "D01Z05S15[SE]",
		"direction": 2,
		"parent": "D01Z05S19[W]"
	},
	{
		"id": "D01Z05S16[N]",
		"direction": 0,
		"parent": "D01Z05S13[SW]"
	},
	{
		"id": "D01Z05S16[SW]",
		"direction": 1,
		"parent": "D01Z05S21[E]"
	},
	{
		"id": "D01Z05S16[SE]",
		"direction": 2,
		"parent": "D01Z05S17[W]"
	},
	{
		"id": "D01Z05S17[W]",
		"direction": 1,
		"parent": "D01Z05S16[SE]"
	},
	{
		"id": "D01Z05S18[E]",
		"direction": 2,
		"parent": "D01Z05S05[SW]"
	},
	{
		"id": "D01Z05S19[W]",
		"direction": 1,
		"parent": "D01Z05S15[SE]"
	},
	{
		"id": "D01Z05S19[E]",
		"direction": 2,
		"parent": "D01Z04S19[W]"
	},
	{
		"id": "D01Z05S20[W]",
		"direction": 1,
		"parent": "D01Z05S25[NE]"
	},
	{
		"id": "D01Z05S20[N]",
		"direction": 0,
		"parent": "D01Z05S02[S]"
	},
	{
		"id": "D01Z05S21[W]",
		"direction": 1,
		"parent": "D01Z05S25[E]"
	},
	{
		"id": "D01Z05S21[E]",
		"direction": 2,
		"parent": "D01Z05S16[SW]"
	},
	{
		"id": "D01Z05S21[Reward]",
		"direction": 4,
		"parent": "D01BZ05S01[Reward]",
	},
	{
		"id": "D01Z05S22[E]",
		"direction": 2,
		"parent": "D01Z05S15[SW]"
	},
	{
		"id": "D01Z05S23[W]",
		"direction": 1,
		"parent": "D01Z05S24[E]",
	},
	{
		"id": "D01Z05S23[E]",
		"direction": 2,
		"parent": "D01Z05S25[W]"
	},
	{
		"id": "D01Z05S24[W]",
		"direction": 1,
		"parent": "D20Z01S04[E]"
	},
	{
		"id": "D01Z05S24[E]",
		"direction": 2,
		"parent": "D01Z05S23[W]"
	},
	{
		"id": "D01Z05S25[NE]",
		"direction": 2,
		"parent": "D01Z05S20[W]",
	},
	{
		"id": "D01Z05S25[W]",
		"direction": 1,
		"parent": "D01Z05S23[E]",
	},
	{
		"id": "D01Z05S25[E]",
		"direction": 2,
		"parent": "D01Z05S21[W]",
	},
	{
		"id": "D01Z05S25[SW]",
		"direction": 1,
		"parent": "D03Z03S17[E]",
	},
	{
		"id": "D01Z05S25[SE]",
		"direction": 2,
		"parent": "D01Z05S26[W]",
	},
	{
		"id": "D01Z05S25[EchoesW]",
		"direction": 1,
		"parent": "D20Z01S09[E]",
	},
	{
		"id": "D01Z05S25[EchoesE]",
		"direction": 2,
		"parent": "D20Z01S10[W]",
	},
	{
		"id": "D01Z05S26[W]",
		"direction": 1,
		"parent": "D01Z05S25[SE]"
	},
	{
		"id": "D01Z05S27[E]",
		"direction": 2,
		"parent": "D01Z05S01[W]"
	},
	{
		"id": "D01BZ05S01[Reward]",
		"direction": 4,
		"parent": "D01Z05S21[Reward]"
	},
	
	{
		"id": "D01Z06S01[N]",
		"direction": 1,
		"parent": "D01Z01S01[S]"
	},
	{
		"id": "D01Z06S01[Santos]",
		"direction": 4,
		"parent": "D01BZ07S01[Santos]",
	},
	{
		"id": "D01BZ07S01[Santos]",
		"direction": 4,
		"parent": "D01Z06S01[Santos]"
	},
	
	{
		"id": "D02Z01S01[SW]",
		"direction": 1,
		"parent": "D02Z01S06[E]",
	},
	{
		"id": "D02Z01S01[W]",
		"direction": 1,
		"parent": "D02Z01S02[E]"
	},
	{
		"id": "D02Z01S01[SE]",
		"direction": 2,
		"parent": "D01Z03S04[NW]"
	},
	{
		"id": "D02Z01S01[CherubsL]",
		"direction": 5
	},
	{
		"id": "D02Z01S01[CherubsR]",
		"direction": 5
	},
	{
		"id": "D02Z01S02[W]",
		"direction": 1,
		"parent": "D02Z01S04[E]"
	},
	{
		"id": "D02Z01S02[NW]",
		"direction": 1,
		"parent": "D02Z01S03[SE]"
	},
	{
		"id": "D02Z01S02[E]",
		"direction": 2,
		"parent": "D02Z01S01[W]"
	},
	{
		"id": "D02Z01S02[NE]",
		"direction": 2,
		"parent": "D02Z01S09[W]",
	},
	{
		"id": "D02Z01S02[]",
		"direction": 6,
		"parent": "D02Z01S06[Cherubs]",
	},
	{
		"id": "D02Z01S03[SW]",
		"direction": 1,
		"parent": "D02Z01S05[E]"
	},
	{
		"id": "D02Z01S03[W]",
		"direction": 1,
		"parent": "D02Z02S01[E]"
	},
	{
		"id": "D02Z01S03[SE]",
		"direction": 2,
		"parent": "D02Z01S02[NW]"
	},
	{
		"id": "D02Z01S03[Cherubs]",
		"direction": 5
	},
	{
		"id": "D02Z01S04[E]",
		"direction": 2,
		"parent": "D02Z01S02[W]"
	},
	{
		"id": "D02Z01S04[-N]",
		"direction": 6,
		"parent": "D02Z01S08[N]",
	},
	{
		"id": "D02Z01S05[E]",
		"direction": 2,
		"parent": "D02Z01S03[SW]"
	},
	{
		"id": "D02Z01S06[W]",
		"direction": 1,
		"parent": "D02Z01S08[E]"
	},
	{
		"id": "D02Z01S06[E]",
		"direction": 2,
		"parent": "D02Z01S01[SW]"
	},
	{
		"id": "D02Z01S06[Cherubs]",
		"direction": 5
	},
	{
		"id": "D02Z01S08[E]",
		"direction": 2,
		"parent": "D02Z01S06[W]"
	},
	{
		"id": "D02Z01S08[N]",
		"direction": 5
	},
	{
		"id": "D02Z01S09[W]",
		"direction": 1,
		"parent": "D02Z01S02[NE]"
	},
	{
		"id": "D02Z01S09[-CherubsL]",
		"direction": 6,
		"parent": "D02Z01S01[CherubsL]",
	},
	{
		"id": "D02Z01S09[-CherubsR]",
		"direction": 6,
		"parent": "D02Z01S01[CherubsR]",
	},
	
	
	{
		"id": "D02Z02S01[W]",
		"direction": 1,
		"parent": "D02Z02S08[E]"
	},
	{
		"id": "D02Z02S01[NW]",
		"direction": 1,
		"parent": "D02Z02S02[SE]"
	},
	{
		"id": "D02Z02S01[E]",
		"direction": 2,
		"parent": "D02Z01S03[W]"
	},
	{
		"id": "D02Z02S01[Cherubs]",
		"direction": 5
	},
	{
		"id": "D02Z02S02[SE]",
		"direction": 2,
		"parent": "D02Z02S01[NW]"
	},
	{
		"id": "D02Z02S02[NW]",
		"direction": 1,
		"parent": "D02Z02S04[SE]"
	},
	{
		"id": "D02Z02S02[NE]",
		"direction": 2,
		"parent": "D02Z02S03[SW]"
	},
	{
		"id": "D02Z02S02[-CherubsR]",
		"direction": 6,
		"parent": "D02Z02S08[CherubsR]",
	},
	{
		"id": "D02Z02S02[CherubsL]",
		"direction": 5
	},
	{
		"id": "D02Z02S02[CherubsR]",
		"direction": 5
	},
	{
		"id": "D02Z02S03[SW]",
		"direction": 1,
		"parent": "D02Z02S02[NE]"
	},
	{
		"id": "D02Z02S03[NW]",
		"direction": 1,
		"parent": "D02Z02S05[SE]"
	},
	{
		"id": "D02Z02S03[NE]",
		"direction": 2,
		"parent": "D02Z02S14[W]",
	},
	{
		"id": "D02Z02S03[-Cherubs]",
		"direction": 6,
		"parent": "D02Z02S01[Cherubs]",
	},
	{
		"id": "D02Z02S04[W]",
		"direction": 1,
		"parent": "D02Z02S09[E]"
	},
	{
		"id": "D02Z02S04[SE]",
		"direction": 2,
		"parent": "D02Z02S02[NW]"
	},
	{
		"id": "D02Z02S04[E]",
		"direction": 2,
		"parent": "D02Z02S05[SW]",
	},
	{
		"id": "D02Z02S04[NE]",
		"direction": 2,
		"parent": "D02Z02S05[W]"
	},
	{
		"id": "D02Z02S04[-CherubsL]",
		"direction": 6,
		"parent": "D02Z02S08[CherubsL]",
	},
	{
		"id": "D02Z02S05[SW]",
		"direction": 1,
		"parent": "D02Z02S04[E]"
	},
	{
		"id": "D02Z02S05[W]",
		"direction": 1,
		"parent": "D02Z02S04[NE]",
	},
	{
		"id": "D02Z02S05[SE]",
		"direction": 2,
		"parent": "D02Z02S03[NW]"
	},
	{
		"id": "D02Z02S05[E]",
		"direction": 2,
		"parent": "D02Z02S10[W]"
	},
	{
		"id": "D02Z02S05[NW]",
		"direction": 1,
		"parent": "D02Z02S07[E]"
	},
	{
		"id": "D02Z02S05[-CherubsL]",
		"direction": 6,
		"parent": "D02Z02S02[CherubsL]",
	},
	{
		"id": "D02Z02S05[-CherubsR]",
		"direction": 6,
		"parent": "D02Z02S02[CherubsR]",
	},
	{
		"id": "D02Z02S06[E]",
		"direction": 2,
		"parent": "D02Z02S11[W]"
	},
	{
		"id": "D02Z02S07[W]",
		"direction": 1,
		"parent": "D02Z03S01[E]"
	},
	{
		"id": "D02Z02S07[E]",
		"direction": 2,
		"parent": "D02Z02S05[NW]"
	},
	{
		"id": "D02Z02S07[Cherubs]",
		"direction": 5
	},
	{
		"id": "D02Z02S08[W]",
		"direction": 1,
		"parent": "D02Z02S11[SE]"
	},
	{
		"id": "D02Z02S08[E]",
		"direction": 2,
		"parent": "D02Z02S01[W]"
	},
	{
		"id": "D02Z02S08[C]",
		"direction": 4,
		"parent": "D02BZ02S01[C]"
	},
	{
		"id": "D02Z02S08[CherubsL]",
		"direction": 5
	},
	{
		"id": "D02Z02S08[CherubsR]",
		"direction": 5
	},
	{
		"id": "D02Z02S09[E]",
		"direction": 2,
		"parent": "D02Z02S04[W]"
	},
	{
		"id": "D02Z02S10[W]",
		"direction": 1,
		"parent": "D02Z02S05[E]"
	},
	{
		"id": "D02Z02S11[W]",
		"direction": 1,
		"parent": "D02Z02S06[E]"
	},
	{
		"id": "D02Z02S11[SE]",
		"direction": 2,
		"parent": "D02Z02S08[W]"
	},
	{
		"id": "D02Z02S11[E]",
		"direction": 2,
		"parent": "D02Z02S12[W]",
	},
	{
		"id": "D02Z02S11[NW]",
		"direction": 1,
		"parent": "D02Z03S14[E]",
	},
	{
		"id": "D02Z02S11[NE]",
		"direction": 2,
		"parent": "D02Z02S13[W]",
	},
	{
		"id": "D02Z02S11[-Cherubs]",
		"direction": 6,
		"parent": "D01Z02S03[Cherubs]",
	},
	{
		"id": "D02Z02S12[W]",
		"direction": 1,
		"parent": "D02Z02S11[E]"
	},
	{
		"id": "D02Z02S13[W]",
		"direction": 1,
		"parent": "D02Z02S11[NE]"
	},
	{
		"id": "D02Z02S14[W]",
		"direction": 1,
		"parent": "D02Z02S03[NE]"
	},
	{
		"id": "D02Z02S14[-Cherubs]",
		"direction": 6,
		"parent": "D02Z01S03[Cherubs]",
	},
	{
		"id": "D02BZ02S01[C]",
		"direction": 4,
		"parent": "D02Z02S08[C]"
	},
	
	{
		"id": "D02Z03S01[W]",
		"direction": 1,
		"parent": "D02Z03S08[E]"
	},
	{
		"id": "D02Z03S01[E]",
		"direction": 2,
		"parent": "D02Z02S07[W]"
	},
	{
		"id": "D02Z03S02[S]",
		"direction": 3,
		"parent": "D02Z03S16[N]"
	},
	{
		"id": "D02Z03S02[W]",
		"direction": 1,
		"parent": "D02Z03S03[E]"
	},
	{
		"id": "D02Z03S02[NW]",
		"direction": 1,
		"parent": "D02Z03S21[E]",
	},
	{
		"id": "D02Z03S02[NE]",
		"direction": 2,
		"parent": "D02Z03S13[W]",
	},
	{
		"id": "D02Z03S02[N]",
		"direction": 0,
		"parent": "D02Z03S11[S]",
	},
	{
		"id": "D02Z03S03[W]",
		"direction": 1,
		"parent": "D02Z03S05[E]"
	},
	{
		"id": "D02Z03S03[NW]",
		"direction": 1,
		"parent": "D02Z03S05[NE]",
	},
	{
		"id": "D02Z03S03[E]",
		"direction": 2,
		"parent": "D02Z03S02[W]"
	},
	{
		"id": "D02Z03S05[S]",
		"direction": 3,
		"parent": "D02Z03S07[N]"
	},
	{
		"id": "D02Z03S05[E]",
		"direction": 2,
		"parent": "D02Z03S03[W]"
	},
	{
		"id": "D02Z03S05[NE]",
		"direction": 2,
		"parent": "D02Z03S03[NW]"
	},
	{
		"id": "D02Z03S06[W]",
		"direction": 1,
		"parent": "D02Z03S18[SE]"
	},
	{
		"id": "D02Z03S06[S]",
		"direction": 3,
		"parent": "D02Z03S07[NW]"
	},
	{
		"id": "D02Z03S07[W]",
		"direction": 1,
		"parent": "D02Z03S17[E]"
	},
	{
		"id": "D02Z03S07[NWW]",
		"direction": 1,
		"parent": "D02Z03S24[E]"
	},
	{
		"id": "D02Z03S07[NW]",
		"direction": 0,
		"parent": "D02Z03S06[S]"
	},
	{
		"id": "D02Z03S07[N]",
		"direction": 0,
		"parent": "D02Z03S05[S]"
	},
	{
		"id": "D02Z03S07[E]",
		"direction": 2,
		"parent": "D02Z03S08[W]"
	},
	{
		"id": "D02Z03S08[SW]",
		"direction": 1,
		"parent": "D02Z03S12[E]"
	},
	{
		"id": "D02Z03S08[W]",
		"direction": 1,
		"parent": "D02Z03S07[E]",
	},
	{
		"id": "D02Z03S08[SE]",
		"direction": 2,
		"parent": "D02Z03S14[W]"
	},
	{
		"id": "D02Z03S08[E]",
		"direction": 2,
		"parent": "D02Z03S01[W]"
	},
	{
		"id": "D02Z03S08[NE]",
		"direction": 2,
		"parent": "D02Z03S16[W]"
	},
	{
		"id": "D02Z03S09[W]",
		"direction": 1,
		"parent": "D02Z03S18[NE]"
	},
	{
		"id": "D02Z03S09[E]",
		"direction": 2,
		"parent": "D02Z03S20[W]"
	},
	{
		"id": "D02Z03S10[W]",
		"direction": 1,
		"parent": "D02Z03S11[E]"
	},
	{
		"id": "D02Z03S10[-W]",
		"direction": 2,
		"parent": "D09Z01S06[W]"
	},
	{
		"id": "D02Z03S10[-Cherubs]",
		"direction": 6,
		"parent": "D02Z02S07[Cherubs]",
	},
	{
		"id": "D02Z03S11[S]",
		"direction": 3,
		"parent": "D02Z03S02[N]"
	},
	{
		"id": "D02Z03S11[W]",
		"direction": 1,
		"parent": "D02Z03S15[E]"
	},
	{
		"id": "D02Z03S11[NW]",
		"direction": 1,
		"parent": "D02Z03S19[E]"
	},
	{
		"id": "D02Z03S11[E]",
		"direction": 2,
		"parent": "D02Z03S10[W]"
	},
	{
		"id": "D02Z03S11[NE]",
		"direction": 2,
		"parent": "D02Z03S22[W]"
	},
	{
		"id": "D02Z03S12[E]",
		"direction": 2,
		"parent": "D02Z03S08[SW]"
	},
	{
		"id": "D02Z03S13[W]",
		"direction": 1,
		"parent": "D02Z03S02[NE]"
	},
	{
		"id": "D02Z03S14[W]",
		"direction": 1,
		"parent": "D02Z03S08[SE]"
	},
	{
		"id": "D02Z03S14[E]",
		"direction": 2,
		"parent": "D02Z02S11[NW]"
	},
	{
		"id": "D02Z03S15[E]",
		"direction": 2,
		"parent": "D02Z03S11[W]"
	},
	{
		"id": "D02Z03S16[W]",
		"direction": 1,
		"parent": "D02Z03S08[NE]"
	},
	{
		"id": "D02Z03S16[N]",
		"direction": 0,
		"parent": "D02Z03S02[S]"
	},
	{
		"id": "D02Z03S17[E]",
		"direction": 2,
		"parent": "D02Z03S07[W]"
	},
	{
		"id": "D02Z03S18[NW]",
		"direction": 1,
		"parent": "D02Z03S23[E]"
	},
	{
		"id": "D02Z03S18[SE]",
		"direction": 2,
		"parent": "D02Z03S06[W]"
	},
	{
		"id": "D02Z03S18[NE]",
		"direction": 2,
		"parent": "D02Z03S09[W]"
	},
	{
		"id": "D02Z03S19[E]",
		"direction": 2,
		"parent": "D02Z03S11[NW]"
	},
	{
		"id": "D02Z03S20[W]",
		"direction": 1,
		"parent": "D02Z03S09[E]",
	},
	{
		"id": "D02Z03S20[E]",
		"direction": 2,
		"parent": "D02Z03S21[W]",
	},
	{
		"id": "D02Z03S21[W]",
		"direction": 1,
		"parent": "D02Z03S20[E]"
	},
	{
		"id": "D02Z03S21[E]",
		"direction": 2,
		"parent": "D02Z03S02[NW]"
	},
	{
		"id": "D02Z03S22[W]",
		"direction": 1,
		"parent": "D02Z03S11[NE]"
	},
	{
		"id": "D02Z03S23[E]",
		"direction": 2,
		"parent": "D02Z03S18[NW]"
	},
	{
		"id": "D02Z03S24[E]",
		"direction": 2,
		"parent": "D02Z03S07[NWW]"
	},
	
	{
		"id": "D03Z01S01[W]",
		"direction": 1,
		"parent": "D03Z01S02[E]"
	},
	{
		"id": "D03Z01S01[NE]",
		"direction": 2,
		"parent": "D01Z05S02[W]"
	},
	{
		"id": "D03Z01S01[S]",
		"direction": 3,
		"parent": "D20Z01S03[N]",
	},
	{
		"id": "D03Z01S01[-Cherubs]",
		"direction": 6,
		"parent": "D20Z01S01[Cherubs]",
	},
	{
		"id": "D03Z01S02[W]",
		"direction": 1,
		"parent": "D03Z01S06[E]"
	},
	{
		"id": "D03Z01S02[E]",
		"direction": 2,
		"parent": "D03Z01S01[W]"
	},
	{
		"id": "D03Z01S03[W]",
		"direction": 1,
		"parent": "D03Z01S04[E]",
	},
	{
		"id": "D03Z01S03[E]",
		"direction": 2,
		"parent": "D03Z01S06[W]"
	},
	{
		"id": "D03Z01S03[SW]",
		"direction": 3,
		"parent": "D03Z02S10[N]",
	},
	{
		"id": "D03Z01S03[SE]",
		"direction": 3,
		"parent": "D03Z02S01[N]"
	},
	{
		"id": "D03Z01S03[-WestL]",
		"direction": 6,
		"parent": "D03Z02S10[Cherubs]",
	},
	{
		"id": "D03Z01S03[-WestR]",
		"direction": 6,
		"parent": "D03Z02S02[CherubsL]",
	},
	{
		"id": "D03Z01S03[-EastL]",
		"direction": 6,
		"parent": "D03Z02S02[CherubsR]",
	},
	{
		"id": "D03Z01S03[-EastR]",
		"direction": 6,
		"parent": "D03Z02S01[Cherubs]",
	},
	{
		"id": "D03Z01S04[NW]",
		"direction": 1,
		"parent": "D03Z01S05[E]"
	},
	{
		"id": "D03Z01S04[E]",
		"direction": 2,
		"parent": "D03Z01S03[W]"
	},
	{
		"id": "D03Z01S05[W]",
		"direction": 1,
		"parent": "D17Z01S07[SE]"
	},
	{
		"id": "D03Z01S05[E]",
		"direction": 2,
		"parent": "D03Z01S04[NW]"
	},
	{
		"id": "D03Z01S06[W]",
		"direction": 1,
		"parent": "D03Z01S03[E]"
	},
	{
		"id": "D03Z01S06[E]",
		"direction": 2,
		"parent": "D03Z01S02[W]"
	},
	
	{
		"id": "D03Z02S01[W]",
		"direction": 1,
		"parent": "D03Z02S02[E]"
	},
	{
		"id": "D03Z02S01[N]",
		"direction": 0,
		"parent": "D03Z01S03[SE]"
	},
	{
		"id": "D03Z02S01[Cherubs]",
		"direction": 5
	},
	{
		"id": "D03Z02S02[W]",
		"direction": 1,
		"parent": "D03Z02S10[E]",
	},
	{
		"id": "D03Z02S02[E]",
		"direction": 2,
		"parent": "D03Z02S01[W]"
	},
	{
		"id": "D03Z02S02[S]",
		"direction": 3,
		"parent": "D03Z02S03[N]"
	},
	{
		"id": "D03Z02S02[CherubsL]",
		"direction": 5
	},
	{
		"id": "D03Z02S02[CherubsR]",
		"direction": 5
	},
	{
		"id": "D03Z02S03[W]",
		"direction": 3,
		"parent": "D03Z02S07[N]",
	},
	{
		"id": "D03Z02S03[E]",
		"direction": 2,
		"parent": "D03Z02S05[W]",
	},
	{
		"id": "D03Z02S03[N]",
		"direction": 0,
		"parent": "D03Z02S02[S]",
	},
	{
		"id": "D03Z02S03[SE2]",
		"direction": 3,
		"parent": "D03Z02S04[NW]",
	},
	{
		"id": "D03Z02S03[SW]",
		"direction": 1,
		"parent": "D03Z02S07[E]",
	},
	{
		"id": "D03Z02S03[SE]",
		"direction": 2,
		"parent": "D03Z02S06[W]",
	},
	{
		"id": "D03Z02S03[SSL]",
		"direction": 3,
		"parent": "D03Z03S01[NL]",
	},
	{
		"id": "D03Z02S03[SSC]",
		"direction": 6,
		"parent": "D03Z03S01[NC]",
	},
	{
		"id": "D03Z02S03[SSR]",
		"direction": 3,
		"parent": "D03Z03S01[NR]",
	},
	{
		"id": "D03Z02S04[NW]",
		"direction": 0,
		"parent": "D03Z02S03[SE2]"
	},
	{
		"id": "D03Z02S04[NE]",
		"direction": 0,
		"parent": "D03Z02S05[S]"
	},
	{
		"id": "D03Z02S04[S]",
		"direction": 3,
		"parent": "D03Z02S06[N]"
	},
	{
		"id": "D03Z02S05[W]",
		"direction": 1,
		"parent": "D03Z02S03[E]"
	},
	{
		"id": "D03Z02S05[E]",
		"direction": 2,
		"parent": "D03Z02S11[W]",
	},
	{
		"id": "D03Z02S05[S]",
		"direction": 3,
		"parent": "D03Z02S04[NE]",
	},
	{
		"id": "D03Z02S06[W]",
		"direction": 1,
		"parent": "D03Z02S03[SE]",
	},
	{
		"id": "D03Z02S06[N]",
		"direction": 0,
		"parent": "D03Z02S04[S]"
	},
	{
		"id": "D03Z02S07[W]",
		"direction": 1,
		"parent": "D03Z02S08[E]"
	},
	{
		"id": "D03Z02S07[E]",
		"direction": 2,
		"parent": "D03Z02S03[SW]",
	},
	{
		"id": "D03Z02S07[N]",
		"direction": 0,
		"parent": "D03Z02S03[W]"
	},
	{
		"id": "D03Z02S08[W]",
		"direction": 1,
		"parent": "D03Z02S14[E]"
	},
	{
		"id": "D03Z02S08[E]",
		"direction": 2,
		"parent": "D03Z02S07[W]"
	},
	{
		"id": "D03Z02S08[N]",
		"direction": 0,
		"parent": "D03Z02S09[S]"
	},
	{
		"id": "D03Z02S09[W]",
		"direction": 1,
		"parent": "D03Z02S12[E]"
	},
	{
		"id": "D03Z02S09[N]",
		"direction": 0,
		"parent": "D03Z02S10[S]"
	},
	{
		"id": "D03Z02S09[S]",
		"direction": 3,
		"parent": "D03Z02S08[N]"
	},
	{
		"id": "D03Z02S09[Cherubs]",
		"direction": 5
	},
	{
		"id": "D03Z02S10[W]",
		"direction": 1,
		"parent": "D03Z02S13[E]"
	},
	{
		"id": "D03Z02S10[N]",
		"direction": 0,
		"parent": "D03Z01S03[SW]"
	},
	{
		"id": "D03Z02S10[S]",
		"direction": 3,
		"parent": "D03Z02S09[N]"
	},
	{
		"id": "D03Z02S10[E]",
		"direction": 2,
		"parent": "D03Z02S02[W]"
	},
	{
		"id": "D03Z02S10[-Cherubs]",
		"direction": 6,
		"parent": "D03Z02S09[Cherubs]",
	},
	{
		"id": "D03Z02S10[Cherubs]",
		"direction": 5
	},
	{
		"id": "D03Z02S11[W]",
		"direction": 1,
		"parent": "D03Z02S05[E]"
	},
	{
		"id": "D03Z02S11[E]",
		"direction": 2,
		"parent": "D03Z02S15[W]"
	},
	{
		"id": "D03Z02S12[E]",
		"direction": 2,
		"parent": "D03Z02S09[W]"
	},
	{
		"id": "D03Z02S12[Cherubs]",
		"direction": 5
	},
	{
		"id": "D03Z02S13[E]",
		"direction": 2,
		"parent": "D03Z02S10[W]"
	},
	{
		"id": "D03Z02S13[-Cherubs]",
		"direction": 6,
		"parent": "D03Z02S12[Cherubs]",
	},
	{
		"id": "D03Z02S14[E]",
		"direction": 2,
		"parent": "D03Z02S08[W]"
	},
	{
		"id": "D03Z02S15[W]",
		"direction": 1,
		"parent": "D03Z02S11[E]"
	},
	{
		"id": "D03Z02S15[E]",
		"direction": 2,
		"parent": "D20Z01S01[W]"
	},
	
	{
		"id": "D03Z03S01[W]",
		"direction": 1,
		"parent": "D03Z03S18[E]"
	},
	{
		"id": "D03Z03S01[S]",
		"direction": 2,
		"parent": "D03Z03S12[W]"
	},
	{
		"id": "D03Z03S01[NL]",
		"direction": 0,
		"parent": "D03Z02S03[SSL]"
	},
	{
		"id": "D03Z03S01[NC]",
		"direction": 5
	},
	{
		"id": "D03Z03S01[NR]",
		"direction": 0,
		"parent": "D03Z02S03[SSR]"
	},
	{
		"id": "D03Z03S02[W]",
		"direction": 1,
		"parent": "D03Z03S12[E]"
	},
	{
		"id": "D03Z03S02[NE]",
		"direction": 2,
		"parent": "D03Z03S14[W]"
	},
	{
		"id": "D03Z03S02[E]",
		"direction": 2,
		"parent": "D03Z03S03[W]"
	},
	{
		"id": "D03Z03S03[W]",
		"direction": 1,
		"parent": "D03Z03S02[E]",
	},
	{
		"id": "D03Z03S03[NE]",
		"direction": 2,
		"parent": "D03Z03S04[NW]",
	},
	{
		"id": "D03Z03S03[SE]",
		"direction": 2,
		"parent": "D03Z03S04[SW]",
	},
	{
		"id": "D03Z03S04[NW]",
		"direction": 1,
		"parent": "D03Z03S03[NE]",
	},
	{
		"id": "D03Z03S04[NE]",
		"direction": 2,
		"parent": "D03Z03S05[NW]",
	},
	{
		"id": "D03Z03S04[E]",
		"direction": 2,
		"parent": "D03Z03S05[SW]",
	},
	{
		"id": "D03Z03S04[SW]",
		"direction": 1,
		"parent": "D03Z03S03[SE]",
	},
	{
		"id": "D03Z03S04[SE]",
		"direction": 2,
		"parent": "D03Z03S13[W]",
	},
	{
		"id": "D03Z03S04[-Cherubs]",
		"direction": 6,
		"parent": "D03Z03S10[Cherubs]"
	},
	{
		"id": "D03Z03S05[NW]",
		"direction": 1,
		"parent": "D03Z03S04[NE]",
	},
	{
		"id": "D03Z03S05[NE]",
		"direction": 2,
		"parent": "D03Z03S06[W]",
	},
	{
		"id": "D03Z03S05[SW]",
		"direction": 1,
		"parent": "D03Z03S04[E]",
	},
	{
		"id": "D03Z03S05[SE]",
		"direction": 2,
		"parent": "D03Z03S07[SW]",
	},
	{
		"id": "D03Z03S06[W]",
		"direction": 1,
		"parent": "D03Z03S05[NE]"
	},
	{
		"id": "D03Z03S07[NW]",
		"direction": 1,
		"parent": "D03Z03S19[E]"
	},
	{
		"id": "D03Z03S07[NE]",
		"direction": 2,
		"parent": "D03Z03S08[W]"
	},
	{
		"id": "D03Z03S07[SW]",
		"direction": 1,
		"parent": "D03Z03S05[SE]"
	},
	{
		"id": "D03Z03S07[E]",
		"direction": 2,
		"parent": "D03Z03S11[W]"
	},
	{
		"id": "D03Z03S07[S]",
		"direction": 3,
		"parent": "D03Z03S09[N]"
	},
	{
		"id": "D03Z03S08[W]",
		"direction": 1,
		"parent": "D03Z03S07[NE]"
	},
	{
		"id": "D03Z03S08[-CherubsL]",
		"direction": 6,
		"parent": "D03Z03S11[CherubsL]",
	},
	{
		"id": "D03Z03S08[-CherubsR]",
		"direction": 6,
		"parent": "D03Z03S11[CherubsR]",
	},
	{
		"id": "D03Z03S09[SW]",
		"direction": 1,
		"parent": "D03Z03S10[E]"
	},
	{
		"id": "D03Z03S09[N]",
		"direction": 0,
		"parent": "D03Z03S07[S]"
	},
	{
		"id": "D03Z03S10[E]",
		"direction": 2,
		"parent": "D03Z03S09[SW]"
	},
	{
		"id": "D03Z03S10[Cherubs]",
		"direction": 5
	},
	{
		"id": "D03Z03S11[W]",
		"direction": 1,
		"parent": "D03Z03S07[E]"
	},
	{
		"id": "D03Z03S11[E]",
		"direction": 2,
		"parent": "D03Z03S15[W]"
	},
	{
		"id": "D03Z03S11[CherubsL]",
		"direction": 5
	},
	{
		"id": "D03Z03S11[CherubsR]",
		"direction": 5
	},
	{
		"id": "D03Z03S12[W]",
		"direction": 1,
		"parent": "D03Z03S01[S]"
	},
	{
		"id": "D03Z03S12[E]",
		"direction": 2,
		"parent": "D03Z03S02[W]"
	},
	{
		"id": "D03Z03S13[W]",
		"direction": 1,
		"parent": "D03Z03S04[SE]"
	},
	{
		"id": "D03Z03S14[W]",
		"direction": 1,
		"parent": "D03Z03S02[NE]"
	},
	{
		"id": "D03Z03S15[W]",
		"direction": 1,
		"parent": "D03Z03S11[E]"
	},
	{
		"id": "D03Z03S15[E]",
		"direction": 2,
		"parent": "D03Z03S16[W]",
	},
	{
		"id": "D03Z03S16[W]",
		"direction": 1,
		"parent": "D03Z03S15[E]"
	},
	{
		"id": "D03Z03S16[E]",
		"direction": 2,
		"parent": "D03Z03S17[W]"
	},
	{
		"id": "D03Z03S17[W]",
		"direction": 1,
		"parent": "D03Z03S16[E]"
	},
	{
		"id": "D03Z03S17[E]",
		"direction": 2,
		"parent": "D01Z05S25[SW]"
	},
	{
		"id": "D03Z03S18[E]",
		"direction": 2,
		"parent": "D03Z03S01[W]"
	},
	{
		"id": "D03Z03S19[E]",
		"direction": 2,
		"parent": "D03Z03S07[NW]"
	},
	
	{
		"id": "D04Z01S01[W]",
		"direction": 1,
		"parent": "D08Z02S01[E]"
	},
	{
		"id": "D04Z01S01[E]",
		"direction": 2,
		"parent": "D04Z01S02[W]"
	},
	{
		"id": "D04Z01S01[NE]",
		"direction": 2,
		"parent": "D04Z01S02[NW]",
	},
	{
		"id": "D04Z01S01[N]",
		"direction": 0,
		"parent": "D04Z01S05[S]",
	},
	{
		"id": "D04Z01S01[Cherubs]",
		"direction": 5
	},
	{
		"id": "D04Z01S02[W]",
		"direction": 1,
		"parent": "D04Z01S01[E]"
	},
	{
		"id": "D04Z01S02[NW]",
		"direction": 1,
		"parent": "D04Z01S01[NE]"
	},
	{
		"id": "D04Z01S02[E]",
		"direction": 2,
		"parent": "D04Z01S03[W]"
	},
	{
		"id": "D04Z01S03[W]",
		"direction": 1,
		"parent": "D04Z01S02[E]"
	},
	{
		"id": "D04Z01S03[E]",
		"direction": 2,
		"parent": "D04Z01S04[W]"
	},
	{
		"id": "D04Z01S03[S]",
		"direction": 3,
		"parent": "D05Z01S20[N]",
	},
	{
		"id": "D04Z01S04[W]",
		"direction": 1,
		"parent": "D04Z01S03[E]"
	},
	{
		"id": "D04Z01S04[E]",
		"direction": 2,
		"parent": "D04Z02S01[W]"
	},
	{
		"id": "D04Z01S04[Cherubs]",
		"direction": 5
	},
	{
		"id": "D04Z01S05[S]",
		"direction": 3,
		"parent": "D04Z01S01[N]"
	},
	{
		"id": "D04Z01S05[N]",
		"direction": 0,
		"parent": "D04Z01S06[S]",
	},
	{
		"id": "D04Z01S05[-Cherubs]",
		"direction": 6,
		"parent": "D04Z01S01[Cherubs]",
	},
	{
		"id": "D04Z01S05[CherubsN]",
		"direction": 5
	},
	{
		"id": "D04Z01S06[S]",
		"direction": 3,
		"parent": "D04Z01S05[N]"
	},
	{
		"id": "D04Z01S06[E]",
		"direction": 2,
		"parent": "D09Z01S09[SW]",
	},
	{
		"id": "D04Z01S06[Cherubs]",
		"direction": 6,
		"parent": "D04Z01S05[CherubsN]",
	},

	{
		"id": "D04Z02S01[W]",
		"direction": 1,
		"parent": "D04Z01S04[E]"
	},
	{
		"id": "D04Z02S01[N]",
		"direction": 0,
		"parent": "D04Z02S02[S]",
	},
	{
		"id": "D04Z02S01[E]",
		"direction": 2,
		"parent": "D04Z03S01[W]"
	},
	{
		"id": "D04Z02S01[NE]",
		"direction": 2,
		"parent": "D04Z02S03[W]",
	},
	{
		"id": "D04Z02S02[S]",
		"direction": 3,
		"parent": "D04Z02S01[N]"
	},
	{
		"id": "D04Z02S02[SE]",
		"direction": 2,
		"parent": "D04Z02S17[W]"
	},
	{
		"id": "D04Z02S02[NE]",
		"direction": 2,
		"parent": "D04Z02S15[W]",
	},
	{
		"id": "D04Z02S02[N]",
		"direction": 0,
		"parent": "D06Z01S02[S]"
	},
	{
		"id": "D04Z02S03[W]",
		"direction": 1,
		"parent": "D04Z02S01[NE]"
	},
	{
		"id": "D04Z02S03[E]",
		"direction": 2,
		"parent": "D04Z02S04[NW]"
	},
	{
		"id": "D04Z02S04[SW]",
		"direction": 1,
		"parent": "D04Z02S14[E]"
	},
	{
		"id": "D04Z02S04[SE]",
		"direction": 2,
		"parent": "D05Z01S01[NW]"
	},
	{
		"id": "D04Z02S04[W]",
		"direction": 1,
		"parent": "D04Z03S01[E]"
	},
	{
		"id": "D04Z02S04[E]",
		"direction": 2,
		"parent": "D04Z02S05[W]"
	},
	{
		"id": "D04Z02S04[NW]",
		"direction": 1,
		"parent": "D04Z02S03[E]",
	},
	{
		"id": "D04Z02S04[NE]",
		"direction": 2,
		"parent": "D04Z02S19[W]",
	},
	{
		"id": "D04Z02S04[N]",
		"direction": 0,
		"parent": "D04Z02S06[S]",
	},
	{
		"id": "D04Z02S04[Cherubs]",
		"direction": 5
	},
	{
		"id": "D04Z02S05[W]",
		"direction": 1,
		"parent": "D04Z02S04[E]"
	},
	{
		"id": "D04Z02S05[E]",
		"direction": 2,
		"parent": "D04Z02S07[SW]"
	},
	{
		"id": "D04Z02S06[S]",
		"direction": 3,
		"parent": "D04Z02S04[N]"
	},
	{
		"id": "D04Z02S06[NW]",
		"direction": 1,
		"parent": "D04Z02S11[E]"
	},
	{
		"id": "D04Z02S06[N]",
		"direction": 0,
		"parent": "D06Z01S23[S]",
	},
	{
		"id": "D04Z02S06[NE]",
		"direction": 2,
		"parent": "D04Z02S09[W]"
	},
	{
		"id": "D04Z02S06[E]",
		"direction": 2,
		"parent": "D04Z02S10[W]"
	},
	{
		"id": "D04Z02S06[-Cherubs]",
		"direction": 6,
		"parent": "D04Z02S04[Cherubs]",
	},
	{
		"id": "D04Z02S07[SW]",
		"direction": 1,
		"parent": "D04Z02S05[E]"
	},
	{
		"id": "D04Z02S07[W]",
		"direction": 1,
		"parent": "D04Z02S19[E]"
	},
	{
		"id": "D04Z02S07[N]",
		"direction": 0,
		"parent": "D04Z02S08[S]"
	},
	{
		"id": "D04Z02S07[NE]",
		"direction": 2,
		"parent": "D04Z02S13[W]"
	},
	{
		"id": "D04Z02S07[SE]",
		"direction": 2,
		"parent": "D04Z02S23[W]"
	},
	{
		"id": "D04Z02S08[W]",
		"direction": 1,
		"parent": "D04Z02S09[E]"
	},
	{
		"id": "D04Z02S08[E]",
		"direction": 2,
		"parent": "D04Z02S20[W]"
	},
	{
		"id": "D04Z02S08[S]",
		"direction": 3,
		"parent": "D04Z02S07[N]"
	},
	{
		"id": "D04Z02S08[Cherubs]",
		"direction": 5
	},
	{
		"id": "D04Z02S09[W]",
		"direction": 1,
		"parent": "D04Z02S06[NE]"
	},
	{
		"id": "D04Z02S09[E]",
		"direction": 2,
		"parent": "D04Z02S08[W]"
	},
	{
		"id": "D04Z02S09[NE]",
		"direction": 2,
		"parent": "D04Z02S16[W]",
	},
	{
		"id": "D04Z02S10[W]",
		"direction": 1,
		"parent": "D04Z02S06[E]"
	},
	{
		"id": "D04Z02S11[W]",
		"direction": 1,
		"parent": "D04Z02S21[SE]"
	},
	{
		"id": "D04Z02S11[E]",
		"direction": 2,
		"parent": "D04Z02S06[NW]"
	},
	{
		"id": "D04Z02S12[W]",
		"direction": 1,
		"parent": "D04Z02S21[NE]"
	},
	{
		"id": "D04Z02S13[W]",
		"direction": 1,
		"parent": "D04Z02S07[NE]"
	},
	{
		"id": "D04Z02S14[E]",
		"direction": 2,
		"parent": "D04Z02S04[SW]"
	},
	{
		"id": "D04Z02S15[W]",
		"direction": 1,
		"parent": "D04Z02S02[NE]"
	},
	{
		"id": "D04Z02S15[E]",
		"direction": 2,
		"parent": "D04Z02S22[W]"
	},
	{
		"id": "D04Z02S16[W]",
		"direction": 1,
		"parent": "D04Z02S09[NE]"
	},
	{
		"id": "D04Z02S16[-Cherubs]",
		"direction": 6,
		"parent": "D04Z02S08[Cherubs]",
	},
	{
		"id": "D04Z02S17[W]",
		"direction": 1,
		"parent": "D04Z02S02[SE]"
	},
	{
		"id": "D04Z02S19[W]",
		"direction": 1,
		"parent": "D04Z02S04[NE]"
	},
	{
		"id": "D04Z02S19[E]",
		"direction": 2,
		"parent": "D04Z02S07[W]"
	},
	{
		"id": "D04Z02S20[W]",
		"direction": 1,
		"parent": "D04Z02S08[E]"
	},
	{
		"id": "D04Z02S20[Redento]",
		"direction": 4,
		"parent": "D04BZ02S01[Redento]",
	},
	{
		"id": "D04Z02S21[W]",
		"direction": 1,
		"parent": "D04Z02S22[E]"
	},
	{
		"id": "D04Z02S21[SE]",
		"direction": 2,
		"parent": "D04Z02S11[W]"
	},
	{
		"id": "D04Z02S21[NE]",
		"direction": 2,
		"parent": "D04Z02S12[W]"
	},
	{
		"id": "D04Z02S22[W]",
		"direction": 1,
		"parent": "D04Z02S15[E]",
	},
	{
		"id": "D04Z02S22[E]",
		"direction": 2,
		"parent": "D04Z02S21[W]",
	},
	{
		"id": "D04Z02S23[W]",
		"direction": 1,
		"parent": "D04Z02S07[SE]"
	},
	{
		"id": "D04Z02S23[SE]",
		"direction": 2,
		"parent": "D04Z02S24[NW]"
	},
	{
		"id": "D04Z02S23[NE]",
		"direction": 2,
		"parent": "D04Z04S01[W]"
	},
	{
		"id": "D04Z02S24[NW]",
		"direction": 1,
		"parent": "D04Z02S23[SE]"
	},
	{
		"id": "D04Z02S24[SW]",
		"direction": 1,
		"parent": "D20Z02S01[E]"
	},
	{
		"id": "D04Z02S24[SE]",
		"direction": 2,
		"parent": "D04Z02S25[W]"
	},
	{
		"id": "D04Z02S25[W]",
		"direction": 1,
		"parent": "D04Z02S24[SE]"
	},
	{
		"id": "D04BZ02S01[Redento]",
		"direction": 4,
		"parent": "D04Z02S20[Redento]"
	},
	
	{
		"id": "D04Z03S01[W]",
		"direction": 1,
		"parent": "D04Z02S01[E]"
	},
	{
		"id": "D04Z03S01[E]",
		"direction": 2,
		"parent": "D04Z02S04[W]"
	},
	{
		"id": "D04Z03S02[W]",
		"direction": 1,
		"parent": "D05Z01S22[E]"
	},
	
	{
		"id": "D04Z04S01[W]",
		"direction": 1,
		"parent": "D04Z02S23[NE]"
	},
	{
		"id": "D04Z04S01[E]",
		"direction": 2,
		"parent": "D04Z04S02[W]"
	},
	{
		"id": "D04Z04S02[W]",
		"direction": 1,
		"parent": "D04Z04S01[E]"
	},
	
	{
		"id": "D05Z01S01[W]",
		"direction": 1,
		"parent": "D05Z01S02[E]"
	},
	{
		"id": "D05Z01S01[NW]",
		"direction": 1,
		"parent": "D04Z02S04[SE]"
	},
	{
		"id": "D05Z01S01[E]",
		"direction": 2,
		"parent": "D05Z01S16[W]"
	},
	{
		"id": "D05Z01S02[W]",
		"direction": 1,
		"parent": "D05Z01S15[E]",
	},
	{
		"id": "D05Z01S02[NW]",
		"direction": 1,
		"parent": "D05Z01S03[E]"
	},
	{
		"id": "D05Z01S02[E]",
		"direction": 2,
		"parent": "D05Z01S01[W]"
	},
	{
		"id": "D05Z01S03[W]",
		"direction": 1,
		"parent": "D05Z01S04[E]"
	},
	{
		"id": "D05Z01S03[E]",
		"direction": 2,
		"parent": "D05Z01S02[NW]"
	},
	{
		"id": "D05Z01S03[Frontal]",
		"direction": 4,
		"parent": "D05BZ01S01[FrontalS]",
	},
	{
		"id": "D05Z01S04[W]",
		"direction": 1,
		"parent": "D05Z01S05[E]"
	},
	{
		"id": "D05Z01S04[E]",
		"direction": 2,
		"parent": "D05Z01S03[W]"
	},
	{
		"id": "D05Z01S05[SW]",
		"direction": 1,
		"parent": "D05Z01S07[E]"
	},
	{
		"id": "D05Z01S05[E]",
		"direction": 2,
		"parent": "D05Z01S04[W]"
	},
	{
		"id": "D05Z01S05[NE]",
		"direction": 2,
		"parent": "D05Z01S17[W]",
	},
	{
		"id": "D05Z01S06[W]",
		"direction": 1,
		"parent": "D05Z01S24[E]",
	},
	{
		"id": "D05Z01S06[E]",
		"direction": 2,
		"parent": "D05Z01S20[W]",
	},
	{
		"id": "D05Z01S07[SW]",
		"direction": 1,
		"parent": "D05Z01S08[NE]"
	},
	{
		"id": "D05Z01S07[NW]",
		"direction": 1,
		"parent": "D05Z01S20[E]",
	},
	{
		"id": "D05Z01S07[E]",
		"direction": 2,
		"parent": "D05Z01S05[SW]"
	},
	{
		"id": "D05Z01S08[W]",
		"direction": 1,
		"parent": "D05Z01S10[E]"
	},
	{
		"id": "D05Z01S08[NW]",
		"direction": 1,
		"parent": "D05Z01S12[E]"
	},
	{
		"id": "D05Z01S08[E]",
		"direction": 2,
		"parent": "D05Z01S09[W]"
	},
	{
		"id": "D05Z01S08[Health]",
		"direction": 2,
		"parent": "D05Z01S14[W]"
	},
	{
		"id": "D05Z01S08[NE]",
		"direction": 2,
		"parent": "D05Z01S07[SW]"
	},
	{
		"id": "D05Z01S09[W]",
		"direction": 1,
		"parent": "D05Z01S08[E]"
	},
	{
		"id": "D05Z01S09[E]",
		"direction": 2,
		"parent": "D05Z01S18[W]"
	},
	{
		"id": "D05Z01S10[W]",
		"direction": 1,
		"parent": "D05Z01S11[E]"
	},
	{
		"id": "D05Z01S10[NW]",
		"direction": 1,
		"parent": "D05Z01S11[NE]"
	},
	{
		"id": "D05Z01S10[E]",
		"direction": 2,
		"parent": "D05Z01S08[W]"
	},
	{
		"id": "D05Z01S11[SW]",
		"direction": 1,
		"parent": "D05Z01S19[E]",
	},
	{
		"id": "D05Z01S11[NW]",
		"direction": 1,
		"parent": "D05Z01S23[E]",
	},
	{
		"id": "D05Z01S11[SE]",
		"direction": 2,
		"parent": "D05Z02S01[W]"
	},
	{
		"id": "D05Z01S11[E]",
		"direction": 2,
		"parent": "D05Z01S10[W]"
	},
	{
		"id": "D05Z01S11[NE]",
		"direction": 2,
		"parent": "D05Z01S10[NW]",
	},
	{
		"id": "D05Z01S12[E]",
		"direction": 2,
		"parent": "D05Z01S08[NW]"
	},
	{
		"id": "D05Z01S13[E]",
		"direction": 2,
		"parent": "D05Z01S21[NW]"
	},
	{
		"id": "D05Z01S14[W]",
		"direction": 1,
		"parent": "D05Z01S08[Health]"
	},
	{
		"id": "D05Z01S15[W]",
		"direction": 1,
		"parent": "D05Z01S21[NE]"
	},
	{
		"id": "D05Z01S15[E]",
		"direction": 2,
		"parent": "D05Z01S02[W]"
	},
	{
		"id": "D05Z01S16[W]",
		"direction": 1,
		"parent": "D05Z01S01[E]"
	},
	{
		"id": "D05Z01S17[W]",
		"direction": 1,
		"parent": "D05Z01S05[NE]"
	},
	{
		"id": "D05Z01S18[W]",
		"direction": 1,
		"parent": "D05Z01S09[E]"
	},
	{
		"id": "D05Z01S19[W]",
		"direction": 1,
		"parent": "D05Z02S15[E]"
	},
	{
		"id": "D05Z01S19[E]",
		"direction": 2,
		"parent": "D05Z01S11[SW]"
	},
	{
		"id": "D05Z01S20[W]",
		"direction": 1,
		"parent": "D05Z01S06[E]"
	},
	{
		"id": "D05Z01S20[E]",
		"direction": 2,
		"parent": "D05Z01S07[NW]"
	},
	{
		"id": "D05Z01S20[N]",
		"direction": 0,
		"parent": "D04Z01S03[S]"
	},
	{
		"id": "D05Z01S21[SW]",
		"direction": 1,
		"parent": "D05Z02S14[E]",
	},
	{
		"id": "D05Z01S21[NW]",
		"direction": 1,
		"parent": "D05Z01S13[E]"
	},
	{
		"id": "D05Z01S21[NE]",
		"direction": 2,
		"parent": "D05Z01S15[W]",
	},
	{
		"id": "D05Z01S21[-Cherubs]",
		"direction": 6,
		"parent": "D05Z02S11[Cherubs]",
	},
	{
		"id": "D05Z01S22[FrontalN]",
		"direction": 4,
		"parent": "D05BZ01S01[FrontalN]"
	},
	{
		"id": "D05Z01S22[E]",
		"direction": 2,
		"parent": "D04Z03S02[W]"
	},
	{
		"id": "D05Z01S23[E]",
		"direction": 2,
		"parent": "D05Z01S11[NW]"
	},
	{
		"id": "D05Z01S24[E]",
		"direction": 2,
		"parent": "D05Z01S06[W]"
	},
	{
		"id": "D05BZ01S01[FrontalS]",
		"direction": 4,
		"parent": "D05Z01S03[Frontal]"
	},
	{
		"id": "D05BZ01S01[FrontalN]",
		"direction": 4,
		"parent": "D05Z01S22[FrontalN]"
	},

	{
		"id": "D05Z02S01[W]",
		"direction": 1,
		"parent": "D05Z01S11[SE]"
	},
	{
		"id": "D05Z02S01[E]",
		"direction": 2,
		"parent": "D05Z02S02[NW]"
	},
	{
		"id": "D05Z02S02[SW]",
		"direction": 1,
		"parent": "D05Z02S03[E]"
	},
	{
		"id": "D05Z02S02[NW]",
		"direction": 1,
		"parent": "D05Z02S01[E]"
	},
	{
		"id": "D05Z02S02[SE]",
		"direction": 2,
		"parent": "D05Z02S09[W]"
	},
	{
		"id": "D05Z02S02[NE]",
		"direction": 2,
		"parent": "D05Z02S05[W]"
	},
	{
		"id": "D05Z02S03[W]",
		"direction": 1,
		"parent": "D05Z02S04[E]"
	},
	{
		"id": "D05Z02S03[E]",
		"direction": 2,
		"parent": "D05Z02S02[SW]"
	},
	{
		"id": "D05Z02S04[W]",
		"direction": 1,
		"parent": "D05Z02S12[E]"
	},
	{
		"id": "D05Z02S04[E]",
		"direction": 2,
		"parent": "D05Z02S03[W]"
	},
	{
		"id": "D05Z02S04[C]",
		"direction": 4,
		"parent": "D05BZ02S01[C]"
	},
	{
		"id": "D05Z02S05[W]",
		"direction": 1,
		"parent": "D05Z02S02[NE]"
	},
	{
		"id": "D05Z02S05[E]",
		"direction": 2,
		"parent": "D05Z02S06[SW]"
	},
	{
		"id": "D05Z02S06[SW]",
		"direction": 1,
		"parent": "D05Z02S05[E]"
	},
	{
		"id": "D05Z02S06[NW]",
		"direction": 1,
		"parent": "D05Z02S07[E]"
	},
	{
		"id": "D05Z02S06[SE]",
		"direction": 2,
		"parent": "D05Z02S11[W]",
	},
	{
		"id": "D05Z02S06[NE]",
		"direction": 2,
		"parent": "D05Z02S14[W]"
	},
	{
		"id": "D05Z02S07[W]",
		"direction": 1,
		"parent": "D05Z02S10[E]"
	},
	{
		"id": "D05Z02S07[E]",
		"direction": 2,
		"parent": "D05Z02S06[NW]"
	},
	{
		"id": "D05Z02S08[W]",
		"direction": 1,
		"parent": "D05Z02S09[E]"
	},
	{
		"id": "D05Z02S09[W]",
		"direction": 1,
		"parent": "D05Z02S02[SE]"
	},
	{
		"id": "D05Z02S09[E]",
		"direction": 2,
		"parent": "D05Z02S08[W]",
	},
	{
		"id": "D05Z02S10[W]",
		"direction": 1,
		"parent": "D05Z02S13[E]"
	},
	{
		"id": "D05Z02S10[E]",
		"direction": 2,
		"parent": "D05Z02S07[W]"
	},
	{
		"id": "D05Z02S11[W]",
		"direction": 1,
		"parent": "D05Z02S06[SE]"
	},
	{
		"id": "D05Z02S11[Cherubs]",
		"direction": 5
	},
	{
		"id": "D05Z02S12[W]",
		"direction": 1,
		"parent": "D01Z04S16[E]"
	},
	{
		"id": "D05Z02S12[E]",
		"direction": 2,
		"parent": "D05Z02S04[W]"
	},
	{
		"id": "D05Z02S12[N]",
		"direction": 0,
		"parent": "D05Z02S15[S]"
	},
	{
		"id": "D05Z02S13[E]",
		"direction": 2,
		"parent": "D05Z02S10[W]"
	},
	{
		"id": "D05Z02S14[W]",
		"direction": 1,
		"parent": "D05Z02S06[NE]",
	},
	{
		"id": "D05Z02S14[E]",
		"direction": 2,
		"parent": "D05Z01S21[SW]",
	},
	{
		"id": "D05Z02S15[S]",
		"direction": 3,
		"parent": "D05Z02S12[N]"
	},
	{
		"id": "D05Z02S15[E]",
		"direction": 2,
		"parent": "D05Z01S19[W]"
	},
	{
		"id": "D05BZ02S01[C]",
		"direction": 4,
		"parent": "D05Z02S04[C]"
	},

	{
		"id": "D06Z01S01[SW]",
		"direction": 1,
		"parent": "D06Z01S14[E]",
	},
	{
		"id": "D06Z01S01[SE]",
		"direction": 2,
		"parent": "D06Z01S03[W]",
	},
	{
		"id": "D06Z01S01[W]",
		"direction": 1,
		"parent": "D06Z01S07[E]",
	},
	{
		"id": "D06Z01S01[E]",
		"direction": 2,
		"parent": "D06Z01S06[WW]",
	},
	{
		"id": "D06Z01S01[NNW]",
		"direction": 1,
		"parent": "D06Z01S16[E]",
	},
	{
		"id": "D06Z01S01[NNE]",
		"direction": 2,
		"parent": "D06Z01S17[W]",
	},
	{
		"id": "D06Z01S01[NW]",
		"direction": 1,
		"parent": "D06Z01S09[E]",
	},
	{
		"id": "D06Z01S01[NE]",
		"direction": 2,
		"parent": "D06Z01S10[W]",
	},
	{
		"id": "D06Z01S01[N]",
		"direction": 0,
		"parent": "D06Z01S19[S]",
	},
	{
		"id": "D06Z01S01[-Cherubs]",
		"direction": 6,
		"parent": "D06Z01S23[Cherubs]",
	},
	{
		"id": "D06Z01S02[W]",
		"direction": 1,
		"parent": "D06Z01S18[E]"
	},
	{
		"id": "D06Z01S02[E]",
		"direction": 2,
		"parent": "D06Z01S08[W]"
	},
	{
		"id": "D06Z01S02[S]",
		"direction": 3,
		"parent": "D04Z02S02[N]"
	},
	{
		"id": "D06Z01S03[W]",
		"direction": 1,
		"parent": "D06Z01S01[SE]"
	},
	{
		"id": "D06Z01S03[E]",
		"direction": 2,
		"parent": "D06Z01S04[W]"
	},
	{
		"id": "D06Z01S04[SW]",
		"direction": 1,
		"parent": "D06Z01S20[E]",
	},
	{
		"id": "D06Z01S04[W]",
		"direction": 1,
		"parent": "D06Z01S03[E]",
	},
	{
		"id": "D06Z01S04[NW]",
		"direction": 1,
		"parent": "D06Z01S06[E]",
	},
	{
		"id": "D06Z01S04[Health]",
		"direction": 2,
		"parent": "D06Z01S24[W]",
	},
	{
		"id": "D06Z01S04[NE]",
		"direction": 2,
		"parent": "D06Z01S06[W]",
	},
	{
		"id": "D06Z01S04[Cherubs]",
		"direction": 5
	},
	{
		"id": "D06Z01S05[E]",
		"direction": 2,
		"parent": "D06Z01S12[NW]"
	},
	{
		"id": "D06Z01S06[WW]",
		"direction": 1,
		"parent": "D06Z01S01[E]",
	},
	{
		"id": "D06Z01S06[E]",
		"direction": 2,
		"parent": "D06Z01S04[NW]",
	},
	{
		"id": "D06Z01S06[W]",
		"direction": 1,
		"parent": "D06Z01S04[NE]",
	},
	{
		"id": "D06Z01S06[EE]",
		"direction": 2,
		"parent": "D06Z01S15[SW]",
	},
	{
		"id": "D06Z01S07[W]",
		"direction": 1,
		"parent": "D06Z01S12[E]"
	},
	{
		"id": "D06Z01S07[E]",
		"direction": 2,
		"parent": "D06Z01S01[W]"
	},
	{
		"id": "D06Z01S07[CherubsL]",
		"direction": 5
	},
	{
		"id": "D06Z01S07[CherubsR]",
		"direction": 5
	},
	{
		"id": "D06Z01S08[W]",
		"direction": 1,
		"parent": "D06Z01S02[E]"
	},
	{
		"id": "D06Z01S08[E]",
		"direction": 2,
		"parent": "D06Z01S14[W]"
	},
	{
		"id": "D06Z01S08[N]",
		"direction": 0,
		"parent": "D06Z01S13[S]",
	},
	{
		"id": "D06Z01S09[W]",
		"direction": 1,
		"parent": "D06Z01S12[NE]"
	},
	{
		"id": "D06Z01S09[E]",
		"direction": 2,
		"parent": "D06Z01S01[NW]"
	},
	{
		"id": "D06Z01S09[-CherubsL]",
		"direction": 6,
		"parent": "D06Z01S16[CherubsL]",
	},
	{
		"id": "D06Z01S09[-CherubsR]",
		"direction": 6,
		"parent": "D06Z01S16[CherubsR]",
	},
	{
		"id": "D06Z01S10[W]",
		"direction": 1,
		"parent": "D06Z01S01[NE]"
	},
	{
		"id": "D06Z01S10[E]",
		"direction": 2,
		"parent": "D06Z01S21[W]"
	},
	{
		"id": "D06Z01S10[-CherubsL]",
		"direction": 6,
		"parent": "D06Z01S17[CherubsL]",
	},
	{
		"id": "D06Z01S10[-CherubsR]",
		"direction": 6,
		"parent": "D06Z01S17[CherubsR]",
	},
	{
		"id": "D06Z01S11[W]",
		"direction": 1,
		"parent": "D06Z01S15[NE]"
	},
	{
		"id": "D06Z01S12[S]",
		"direction": 3,
		"parent": "D06Z01S14[N]"
	},
	{
		"id": "D06Z01S12[W]",
		"direction": 1,
		"parent": "D06Z01S13[E]",
	},
	{
		"id": "D06Z01S12[E]",
		"direction": 2,
		"parent": "D06Z01S07[W]",
	},
	{
		"id": "D06Z01S12[NW]",
		"direction": 1,
		"parent": "D06Z01S05[E]",
	},
	{
		"id": "D06Z01S12[NE]",
		"direction": 2,
		"parent": "D06Z01S09[W]",
	},
	{
		"id": "D06Z01S12[NE2]",
		"direction": 2,
		"parent": "D06Z01S16[W]",
	},
	{
		"id": "D06Z01S13[W]",
		"direction": 1,
		"parent": "D09Z01S01[E]"
	},
	{
		"id": "D06Z01S13[E]",
		"direction": 2,
		"parent": "D06Z01S12[W]"
	},
	{
		"id": "D06Z01S13[S]",
		"direction": 3,
		"parent": "D06Z01S08[N]"
	},
	{
		"id": "D06Z01S14[W]",
		"direction": 1,
		"parent": "D06Z01S08[E]"
	},
	{
		"id": "D06Z01S14[E]",
		"direction": 2,
		"parent": "D06Z01S01[SW]"
	},
	{
		"id": "D06Z01S14[N]",
		"direction": 0,
		"parent": "D06Z01S12[S]"
	},
	{
		"id": "D06Z01S15[SW]",
		"direction": 1,
		"parent": "D06Z01S06[EE]",
	},
	{
		"id": "D06Z01S15[NW]",
		"direction": 1,
		"parent": "D06Z01S21[E]",
	},
	{
		"id": "D06Z01S15[NE]",
		"direction": 2,
		"parent": "D06Z01S11[W]",
	},
	{
		"id": "D06Z01S16[W]",
		"direction": 1,
		"parent": "D06Z01S12[NE2]",
	},
	{
		"id": "D06Z01S16[E]",
		"direction": 2,
		"parent": "D06Z01S01[NNW]",
	},
	{
		"id": "D06Z01S16[-CherubsL]",
		"direction": 6,
		"parent": "D06Z01S07[CherubsL]",
	},
	{
		"id": "D06Z01S16[-CherubsR]",
		"direction": 6,
		"parent": "D06Z01S07[CherubsR]",
	},
	{
		"id": "D06Z01S16[CherubsL]",
		"direction": 5
	},
	{
		"id": "D06Z01S16[CherubsR]",
		"direction": 5
	},
	{
		"id": "D06Z01S17[W]",
		"direction": 1,
		"parent": "D06Z01S01[NNE]",
	},
	{
		"id": "D06Z01S17[E]",
		"direction": 2,
		"parent": "D06Z01S26[W]",
	},
	{
		"id": "D06Z01S17[-Cherubs]",
		"direction": 6,
		"parent": "D06Z01S04[Cherubs]"
	},
	{
		"id": "D06Z01S17[CherubsL]",
		"direction": 5
	},
	{
		"id": "D06Z01S17[CherubsR]",
		"direction": 5
	},
	{
		"id": "D06Z01S18[E]",
		"direction": 2,
		"parent": "D06Z01S02[W]"
	},
	{
		"id": "D06Z01S18[-Cherubs]",
		"direction": 6,
		"parent": "D04Z01S04[Cherubs]",
	},
	{
		"id": "D06Z01S19[S]",
		"direction": 3,
		"parent": "D06Z01S01[N]"
	},
	{
		"id": "D06Z01S19[E]",
		"direction": 2,
		"parent": "D06Z01S25[W]"
	},
	{
		"id": "D06Z01S20[W]",
		"direction": 1,
		"parent": "D06Z01S23[E]"
	},
	{
		"id": "D06Z01S20[E]",
		"direction": 2,
		"parent": "D06Z01S04[SW]"
	},
	{
		"id": "D06Z01S21[W]",
		"direction": 1,
		"parent": "D06Z01S10[E]"
	},
	{
		"id": "D06Z01S21[E]",
		"direction": 2,
		"parent": "D06Z01S15[NW]"
	},
	{
		"id": "D06Z01S22[Sword]",
		"direction": 2,
		"parent": "D06Z01S23[Sword]"
	},
	{
		"id": "D06Z01S23[Sword]",
		"direction": 1,
		"parent": "D06Z01S22[Sword]"
	},
	{
		"id": "D06Z01S23[E]",
		"direction": 2,
		"parent": "D06Z01S20[W]"
	},
	{
		"id": "D06Z01S23[S]",
		"direction": 3,
		"parent": "D04Z02S06[N]"
	},
	{
		"id": "D06Z01S23[Cherubs]",
		"direction": 5
	},
	{
		"id": "D06Z01S24[W]",
		"direction": 1,
		"parent": "D06Z01S04[Health]"
	},
	{
		"id": "D06Z01S25[W]",
		"direction": 1,
		"parent": "D06Z01S19[E]",
	},
	{
		"id": "D06Z01S25[E]",
		"direction": 2,
		"parent": "D07Z01S01[W]",
	},
	{
		"id": "D06Z01S26[W]",
		"direction": 1,
		"parent": "D06Z01S17[E]"
	},

	{
		"id": "D07Z01S01[W]",
		"direction": 1,
		"parent": "D06Z01S25[E]"
	},
	{
		"id": "D07Z01S01[E]",
		"direction": 2,
		"parent": "D07Z01S02[W]"
	},
	{
		"id": "D07Z01S02[W]",
		"direction": 1,
		"parent": "D07Z01S01[E]"
	},
	{
		"id": "D07Z01S02[E]",
		"direction": 2,
		"parent": "D07Z01S03[W]"
	},
	{
		"id": "D07Z01S03[W]",
		"direction": 1,
		"parent": "D07Z01S02[E]"
	},

	{
		"id": "D08Z01S01[W]",
		"direction": 1,
		"parent": "D01Z03S06[E]",
	},
	{
		"id": "D08Z01S01[E]",
		"direction": 2,
		"parent": "D08Z02S01[W]",
	},
	{
		"id": "D08Z01S01[Cherubs]",
		"direction": 5
	},
	{
		"id": "D08Z01S02[NE]",
		"direction": 2,
		"parent": "D08Z03S03[W]",
	},
	{
		"id": "D08Z01S02[SE]",
		"direction": 2,
		"parent": "D08Z02S03[W]",
	},
	{
		"id": "D08Z01S02[-Cherubs]",
		"direction": 6,
		"parent": "D08Z01S01[Cherubs]",
	},
	
	{
		"id": "D08Z02S01[W]",
		"direction": 1,
		"parent": "D08Z01S01[E]"
	},
	{
		"id": "D08Z02S01[SE]",
		"direction": 2,
		"parent": "D08Z02S02[W]"
	},
	{
		"id": "D08Z02S01[E]",
		"direction": 2,
		"parent": "D04Z01S01[W]"
	},
	{
		"id": "D08Z02S01[N]",
		"direction": 0,
		"parent": "D08Z02S03[S]"
	},
	{
		"id": "D08Z02S02[W]",
		"direction": 1,
		"parent": "D08Z02S01[SE]"
	},
	{
		"id": "D08Z02S03[W]",
		"direction": 1,
		"parent": "D08Z01S02[SE]",
	},
	{
		"id": "D08Z02S03[E]",
		"direction": 2,
		"parent": "D08Z03S01[W]"
	},
	{
		"id": "D08Z02S03[S]",
		"direction": 3,
		"parent": "D08Z02S01[N]"
	},
	
	{
		"id": "D08Z03S01[W]",
		"direction": 1,
		"parent": "D08Z02S03[E]"
	},
	{
		"id": "D08Z03S01[E]",
		"direction": 2,
		"parent": "D08Z03S02[SW]",
	},
	{
		"id": "D08Z03S02[SW]",
		"direction": 1,
		"parent": "D08Z03S01[E]"
	},
	{
		"id": "D08Z03S02[NW]",
		"direction": 1,
		"parent": "D08Z03S03[E]"
	},
	{
		"id": "D08Z03S03[W]",
		"direction": 1,
		"parent": "D08Z01S02[NE]",
	},
	{
		"id": "D08Z03S03[E]",
		"direction": 2,
		"parent": "D08Z03S02[NW]",
	},
	
	{
		"id": "D09Z01S01[W]",
		"direction": 1,
		"parent": "D09Z01S11[E]"
	},
	{
		"id": "D09Z01S01[E]",
		"direction": 2,
		"parent": "D06Z01S13[W]"
	},
	{
		"id": "D09Z01S02[SW]",
		"direction": 1,
		"parent": "D09Z01S07[E]",
	},
	{
		"id": "D09Z01S02[NW]",
		"direction": 1,
		"parent": "D09Z01S07[NE]",
	},
	{
		"id": "D09Z01S02[N]",
		"direction": 0,
		"parent": "D09Z01S11[S]",
	},
	{
		"id": "D09Z01S02[Cell1]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell1]",
	},
	{
		"id": "D09Z01S02[Cell6]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell6]",
	},
	{
		"id": "D09Z01S02[Cell5]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell5]",
	},
	{
		"id": "D09Z01S02[Cell4]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell4]",
	},
	{
		"id": "D09Z01S02[Cell2]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell2]",
	},
	{
		"id": "D09Z01S02[Cell3]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell3]",
	},
	{
		"id": "D09Z01S02[Cell22]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell22]",
	},
	{
		"id": "D09Z01S02[Cell23]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell23]",
	},
	{
		"id": "D09Z01S03[W]",
		"direction": 1,
		"parent": "D09Z01S05[SE]",
	},
	{
		"id": "D09Z01S03[N]",
		"direction": 5
	},
	{
		"id": "D09Z01S04[W]",
		"direction": 1,
		"parent": "D09Z01S06[E]"
	},
	{
		"id": "D09Z01S04[E]",
		"direction": 2,
		"parent": "D09Z01S11[W]"
	},
	{
		"id": "D09Z01S04[S]",
		"direction": 3,
		"parent": "D09Z01S07[N]"
	},
	{
		"id": "D09Z01S05[W]",
		"direction": 1,
		"parent": "D09Z01S13[E]"
	},
	{
		"id": "D09Z01S05[SE]",
		"direction": 2,
		"parent": "D09Z01S03[W]"
	},
	{
		"id": "D09Z01S05[NE]",
		"direction": 2,
		"parent": "D09Z01S08[W]"
	},
	{
		"id": "D09Z01S06[W]",
		"direction": 1,
		"parent": "D02Z03S10[-W]",
	},
	{
		"id": "D09Z01S06[E]",
		"direction": 2,
		"parent": "D09Z01S04[W]"
	},
	{
		"id": "D09Z01S07[SW]",
		"direction": 1,
		"parent": "D09Z01S09[E]",
	},
	{
		"id": "D09Z01S07[SE]",
		"direction": 2,
		"parent": "D09Z01S10[W]",
	},
	{
		"id": "D09Z01S07[W]",
		"direction": 1,
		"parent": "D09Z01S08[SE]",
	},
	{
		"id": "D09Z01S07[E]",
		"direction": 2,
		"parent": "D09Z01S02[SW]",
	},
	{
		"id": "D09Z01S07[NW]",
		"direction": 1,
		"parent": "D09Z01S08[NE]",
	},
	{
		"id": "D09Z01S07[NE]",
		"direction": 2,
		"parent": "D09Z01S02[NW]",
	},
	{
		"id": "D09Z01S07[N]",
		"direction": 0,
		"parent": "D09Z01S04[S]",
	},
	{
		"id": "D09Z01S08[W]",
		"direction": 1,
		"parent": "D09Z01S05[NE]",
	},
	{
		"id": "D09Z01S08[S]",
		"direction": 6,
		"parent": "D09Z01S03[N]",
	},
	{
		"id": "D09Z01S08[SE]",
		"direction": 2,
		"parent": "D09Z01S07[W]",
	},
	{
		"id": "D09Z01S08[NE]",
		"direction": 2,
		"parent": "D09Z01S07[NW]",
	},
	{
		"id": "D09Z01S08[Cell14]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell14]",
	},
	{
		"id": "D09Z01S08[Cell15]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell15]",
	},
	{
		"id": "D09Z01S08[Cell7]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell7]",
	},
	{
		"id": "D09Z01S08[Cell16]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell16]",
	},
	{
		"id": "D09Z01S08[Cell18]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell18]",
	},
	{
		"id": "D09Z01S08[Cell17]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell17]",
	},
	{
		"id": "D09Z01S09[SW]",
		"direction": 1,
		"parent": "D04Z01S06[E]"
	},
	{
		"id": "D09Z01S09[NW]",
		"direction": 1,
		"parent": "D09Z01S12[E]",
	},
	{
		"id": "D09Z01S09[E]",
		"direction": 2,
		"parent": "D09Z01S07[SW]"
	},
	{
		"id": "D09Z01S09[Cell24]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell24]",
	},
	{
		"id": "D09Z01S09[Cell19]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell19]",
	},
	{
		"id": "D09Z01S09[Cell20]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell20]",
	},
	{
		"id": "D09Z01S09[Cell21]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell21]",
	},
	{
		"id": "D09Z01S10[W]",
		"direction": 1,
		"parent": "D09Z01S07[SE]",
	},
	{
		"id": "D09Z01S10[Cell13]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell13]",
	},
	{
		"id": "D09Z01S10[Cell12]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell12]",
	},
	{
		"id": "D09Z01S10[Cell10]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell10]",
	},
	{
		"id": "D09Z01S10[Cell11]",
		"direction": 4,
		"parent": "D09BZ01S01[Cell11]",
	},
	{
		"id": "D09Z01S11[W]",
		"direction": 1,
		"parent": "D09Z01S04[E]",
	},
	{
		"id": "D09Z01S11[E]",
		"direction": 2,
		"parent": "D09Z01S01[W]"
	},
	{
		"id": "D09Z01S11[S]",
		"direction": 3,
		"parent": "D09Z01S02[N]"
	},
	{
		"id": "D09Z01S12[E]",
		"direction": 2,
		"parent": "D09Z01S09[NW]"
	},
	{
		"id": "D09Z01S13[E]",
		"direction": 2,
		"parent": "D09Z01S05[W]"
	},
	{
		"id": "D09BZ01S01[Cell1]",
		"direction": 4,
		"parent": "D09Z01S02[Cell1]",
	},
	{
		"id": "D09BZ01S01[Cell2]",
		"direction": 4,
		"parent": "D09Z01S02[Cell2]",
	},
	{
		"id": "D09BZ01S01[Cell3]",
		"direction": 4,
		"parent": "D09Z01S02[Cell3]",
	},
	{
		"id": "D09BZ01S01[Cell4]",
		"direction": 4,
		"parent": "D09Z01S02[Cell4]",
	},
	{
		"id": "D09BZ01S01[Cell5]",
		"direction": 4,
		"parent": "D09Z01S02[Cell5]",
	},
	{
		"id": "D09BZ01S01[Cell6]",
		"direction": 4,
		"parent": "D09Z01S02[Cell6]",
	},
	{
		"id": "D09BZ01S01[Cell7]",
		"direction": 4,
		"parent": "D09Z01S08[Cell7]",
	},
	{
		"id": "D09BZ01S01[Cell10]",
		"direction": 4,
		"parent": "D09Z01S10[Cell10]",
	},
	{
		"id": "D09BZ01S01[Cell11]",
		"direction": 4,
		"parent": "D09Z01S10[Cell11]",
	},
	{
		"id": "D09BZ01S01[Cell12]",
		"direction": 4,
		"parent": "D09Z01S10[Cell12]",
	},
	{
		"id": "D09BZ01S01[Cell13]",
		"direction": 4,
		"parent": "D09Z01S10[Cell13]",
	},
	{
		"id": "D09BZ01S01[Cell14]",
		"direction": 4,
		"parent": "D09Z01S08[Cell14]",
	},
	{
		"id": "D09BZ01S01[Cell15]",
		"direction": 4,
		"parent": "D09Z01S08[Cell15]",
	},
	{
		"id": "D09BZ01S01[Cell16]",
		"direction": 4,
		"parent": "D09Z01S08[Cell16]",
	},
	{
		"id": "D09BZ01S01[Cell17]",
		"direction": 4,
		"parent": "D09Z01S08[Cell17]",
	},
	{
		"id": "D09BZ01S01[Cell18]",
		"direction": 4,
		"parent": "D09Z01S08[Cell18]",
	},
	{
		"id": "D09BZ01S01[Cell19]",
		"direction": 4,
		"parent": "D09Z01S09[Cell19]",
	},
	{
		"id": "D09BZ01S01[Cell20]",
		"direction": 4,
		"parent": "D09Z01S09[Cell19]",
	},
	{
		"id": "D09BZ01S01[Cell21]",
		"direction": 4,
		"parent": "D09Z01S09[Cell21]",
	},
	{
		"id": "D09BZ01S01[Cell22]",
		"direction": 4,
		"parent": "D09Z01S02[Cell22]",
	},
	{
		"id": "D09BZ01S01[Cell23]",
		"direction": 4,
		"parent": "D09Z01S02[Cell23]",
	},
	{
		"id": "D09BZ01S01[Cell24]",
		"direction": 4,
		"parent": "D09Z01S09[Cell24]",
	},
	
	{
		"id": "D17Z01S01[E]",
		"direction": 2,
		"parent": "D17Z01S02[W]"
	},
	{
		"id": "D17Z01S01[Cherubs1]",
		"direction": 5
	},
	{
		"id": "D17Z01S01[Cherubs2]",
		"direction": 5
	},
	{
		"id": "D17Z01S01[Cherubs3]",
		"direction": 5
	},
	{
		"id": "D17Z01S02[W]",
		"direction": 1,
		"parent": "D17Z01S01[E]"
	},
	{
		"id": "D17Z01S02[E]",
		"direction": 2,
		"parent": "D17Z01S05[W]"
	},
	{
		"id": "D17Z01S02[N]",
		"direction": 0,
		"parent": "D17Z01S10[S]",
	},
	{
		"id": "D17Z01S03[W]",
		"direction": 1,
		"parent": "D17Z01S11[E]"
	},
	{
		"id": "D17Z01S03[E]",
		"direction": 2,
		"parent": "D01Z01S07[W]"
	},
	{
		"id": "D17Z01S03[relic]",
		"direction": 4,
		"parent": "D17BZ01S01[relic]",
	},
	{
		"id": "D17Z01S04[W]",
		"direction": 1,
		"parent": "D17Z01S12[E]"
	},
	{
		"id": "D17Z01S04[S]",
		"direction": 3,
		"parent": "D17Z01S07[N]"
	},
	{
		"id": "D17Z01S04[FrontL]",
		"direction": 4,
		"parent": "D17BZ02S01[FrontL]"
	},
	{
		"id": "D17Z01S04[N]",
		"direction": 0,
		"parent": "D17Z01S05[S]",
	},
	{
		"id": "D17Z01S04[FrontR]",
		"direction": 4,
		"parent": "D17BZ02S01[FrontR]",
	},
	{
		"id": "D17Z01S05[W]",
		"direction": 1,
		"parent": "D17Z01S02[E]"
	},
	{
		"id": "D17Z01S05[E]",
		"direction": 2,
		"parent": "D17Z01S11[W]"
	},
	{
		"id": "D17Z01S05[S]",
		"direction": 3,
		"parent": "D17Z01S04[N]",
	},
	{
		"id": "D17Z01S06[E]",
		"direction": 2,
		"parent": "D17Z01S07[W]"
	},
	{
		"id": "D17Z01S07[SW]",
		"direction": 1,
		"parent": "D17Z01S08[E]"
	},
	{
		"id": "D17Z01S07[SE]",
		"direction": 2,
		"parent": "D03Z01S05[W]"
	},
	{
		"id": "D17Z01S07[W]",
		"direction": 1,
		"parent": "D17Z01S06[E]"
	},
	{
		"id": "D17Z01S07[NW]",
		"direction": 1,
		"parent": "D17Z01S09[E]"
	},
	{
		"id": "D17Z01S07[N]",
		"direction": 0,
		"parent": "D17Z01S04[S]"
	},
	{
		"id": "D17Z01S08[E]",
		"direction": 2,
		"parent": "D17Z01S07[SW]"
	},
	{
		"id": "D17Z01S09[E]",
		"direction": 2,
		"parent": "D17Z01S07[NW]"
	},
	{
		"id": "D17Z01S10[W]",
		"direction": 1,
		"parent": "D17Z01S13[E]",
	},
	{
		"id": "D17Z01S10[S]",
		"direction": 3,
		"parent": "D17Z01S02[N]"
	},
	{
		"id": "D17Z01S11[W]",
		"direction": 1,
		"parent": "D17Z01S05[E]"
	},
	{
		"id": "D17Z01S11[E]",
		"direction": 2,
		"parent": "D17Z01S03[W]"
	},
	{
		"id": "D17Z01S12[E]",
		"direction": 2,
		"parent": "D17Z01S04[W]"
	},
	{
		"id": "D17Z01S13[W]",
		"direction": 1,
		"parent": "D17Z01S14[E]"
	},
	{
		"id": "D17Z01S13[E]",
		"direction": 2,
		"parent": "D17Z01S10[W]"
	},
	{
		"id": "D17Z01S14[W]",
		"direction": 1,
		"parent": "D17Z01S15[E]",
	},
	{
		"id": "D17Z01S14[E]",
		"direction": 2,
		"parent": "D17Z01S13[W]",
	},
	{
		"id": "D17Z01S14[-Cherubs1]",
		"direction": 6,
		"parent": "D17Z01S01[Cherubs1]",
	},
	{
		"id": "D17Z01S14[-Cherubs2]",
		"direction": 6,
		"parent": "D17Z01S01[Cherubs2]",
	},
	{
		"id": "D17Z01S14[-Cherubs3]",
		"direction": 6,
		"parent": "D17Z01S01[Cherubs3]",
	},
	{
		"id": "D17Z01S15[E]",
		"direction": 2,
		"parent": "D17Z01S14[W]"
	},
	{
		"id": "D17BZ01S01[relic]",
		"direction": 4,
		"parent": "D17Z01S03[relic]"
	},
	{
		"id": "D17BZ02S01[FrontL]",
		"direction": 4,
		"parent": "D17Z01S04[FrontL]",
	},
	{
		"id": "D17BZ02S01[FrontR]",
		"direction": 4,
		"parent": "D17Z01S04[FrontR]"
	},
	
	{
		"id": "D20Z01S01[W]",
		"direction": 1,
		"parent": "D03Z02S15[E]"
	},
	{
		"id": "D20Z01S01[E]",
		"direction": 2,
		"parent": "D20Z01S02[W]"
	},
	{
		"id": "D20Z01S01[S]",
		"direction": 3,
		"parent": "D20Z01S04[N]"
	},
	{
		"id": "D20Z01S01[Cherubs]",
		"direction": 5
	},
	{
		"id": "D20Z01S02[W]",
		"direction": 1,
		"parent": "D20Z01S01[E]"
	},
	{
		"id": "D20Z01S02[E]",
		"direction": 2,
		"parent": "D20Z01S03[W]"
	},
	{
		"id": "D20Z01S03[W]",
		"direction": 1,
		"parent": "D20Z01S02[E]"
	},
	{
		"id": "D20Z01S03[N]",
		"direction": 0,
		"parent": "D03Z01S01[S]"
	},
	{
		"id": "D20Z01S04[W]",
		"direction": 1,
		"parent": "D20Z01S05[E]"
	},
	{
		"id": "D20Z01S04[E]",
		"direction": 2,
		"parent": "D01Z05S24[W]",
	},
	{
		"id": "D20Z01S04[N]",
		"direction": 0,
		"parent": "D20Z01S01[S]"
	},
	{
		"id": "D20Z01S05[W]",
		"direction": 1,
		"parent": "D20Z01S06[NE]"
	},
	{
		"id": "D20Z01S05[E]",
		"direction": 2,
		"parent": "D20Z01S04[W]"
	},
	{
		"id": "D20Z01S06[NE]",
		"direction": 2,
		"parent": "D20Z01S05[W]"
	},
	{
		"id": "D20Z01S06[SE]",
		"direction": 2,
		"parent": "D20Z01S07[NW]"
	},
	{
		"id": "D20Z01S07[NW]",
		"direction": 1,
		"parent": "D20Z01S06[SE]"
	},
	{
		"id": "D20Z01S07[NE]",
		"direction": 2,
		"parent": "D20Z01S08[W]"
	},
	{
		"id": "D20Z01S07[SE]",
		"direction": 2,
		"parent": "D20Z01S09[W]"
	},
	{
		"id": "D20Z01S08[W]",
		"direction": 1,
		"parent": "D20Z01S07[NE]"
	},
	{
		"id": "D20Z01S09[W]",
		"direction": 1,
		"parent": "D20Z01S07[SE]"
	},
	{
		"id": "D20Z01S09[E]",
		"direction": 2,
		"parent": "D01Z05S25[EchoesW]",
	},
	{
		"id": "D20Z01S10[W]",
		"direction": 1,
		"parent": "D01Z05S25[EchoesE]",
	},
	{
		"id": "D20Z01S10[E]",
		"direction": 2,
		"parent": "D20Z01S11[W]",
	},
	{
		"id": "D20Z01S11[W]",
		"direction": 1,
		"parent": "D20Z01S10[E]"
	},
	{
		"id": "D20Z01S11[NW]",
		"direction": 1,
		"parent": "D20Z01S12[E]"
	},
	{
		"id": "D20Z01S11[NE]",
		"direction": 2,
		"parent": "D20Z01S13[W]"
	},
	{
		"id": "D20Z01S11[SE]",
		"direction": 2,
		"parent": "D20Z02S12[W]"
	},
	{
		"id": "D20Z01S12[E]",
		"direction": 2,
		"parent": "D20Z01S11[NW]"
	},
	{
		"id": "D20Z01S13[W]",
		"direction": 1,
		"parent": "D20Z01S11[NE]"
	},
	{
		"id": "D20Z01S13[E]",
		"direction": 2,
		"parent": "D20Z02S11[NW]"
	},
	{
		"id": "D20Z01S13[N]",
		"direction": 0,
		"parent": "D20Z01S14[S]"
	},
	{
		"id": "D20Z01S14[S]",
		"direction": 3,
		"parent": "D20Z01S13[N]"
	},
	{
		"id": "D20Z01S14[E]",
		"direction": 2,
		"parent": "D20Z03S01[W]"
	},
	
	{
		"id": "D20Z02S01[W]",
		"direction": 1,
		"parent": "D20Z02S03[SE]"
	},
	{
		"id": "D20Z02S01[E]",
		"direction": 2,
		"parent": "D04Z02S24[SW]"
	},
	{
		"id": "D20Z02S02[W]",
		"direction": 1,
		"parent": "D20Z02S03[NE]"
	},
	{
		"id": "D20Z02S03[W]",
		"direction": 1,
		"parent": "D20Z02S04[E]"
	},
	{
		"id": "D20Z02S03[NE]",
		"direction": 2,
		"parent": "D20Z02S02[W]",
	},
	{
		"id": "D20Z02S03[SE]",
		"direction": 2,
		"parent": "D20Z02S01[W]"
	},
	{
		"id": "D20Z02S04[W]",
		"direction": 1,
		"parent": "D20Z02S05[E]"
	},
	{
		"id": "D20Z02S04[E]",
		"direction": 2,
		"parent": "D20Z02S03[W]"
	},
	{
		"id": "D20Z02S05[SW]",
		"direction": 1,
		"parent": "D20Z02S06[SE]"
	},
	{
		"id": "D20Z02S05[NW]",
		"direction": 1,
		"parent": "D20Z02S06[NE]",
	},
	{
		"id": "D20Z02S05[E]",
		"direction": 2,
		"parent": "D20Z02S04[W]"
	},
	{
		"id": "D20Z02S06[SW]",
		"direction": 1,
		"parent": "D20Z02S09[E]"
	},
	{
		"id": "D20Z02S06[SE]",
		"direction": 2,
		"parent": "D20Z02S05[SW]"
	},
	{
		"id": "D20Z02S06[NW]",
		"direction": 1,
		"parent": "D20Z02S07[E]",
	},
	{
		"id": "D20Z02S06[NE]",
		"direction": 2,
		"parent": "D20Z02S05[NW]",
	},
	{
		"id": "D20Z02S07[W]",
		"direction": 1,
		"parent": "D20Z02S08[E]"
	},
	{
		"id": "D20Z02S07[E]",
		"direction": 2,
		"parent": "D20Z02S06[NW]"
	},
	{
		"id": "D20Z02S08[E]",
		"direction": 2,
		"parent": "D20Z02S07[W]"
	},
	{
		"id": "D20Z02S09[W]",
		"direction": 1,
		"parent": "D20Z02S10[E]"
	},
	{
		"id": "D20Z02S09[E]",
		"direction": 2,
		"parent": "D20Z02S06[SW]"
	},
	{
		"id": "D20Z02S10[W]",
		"direction": 1,
		"parent": "D20Z02S11[E]"
	},
	{
		"id": "D20Z02S10[E]",
		"direction": 2,
		"parent": "D20Z02S09[W]"
	},
	{
		"id": "D20Z02S11[SW]",
		"direction": 1,
		"parent": "D20Z02S12[E]"
	},
	{
		"id": "D20Z02S11[NW]",
		"direction": 1,
		"parent": "D20Z01S13[E]",
	},
	{
		"id": "D20Z02S11[E]",
		"direction": 2,
		"parent": "D20Z02S10[W]",
	},
	{
		"id": "D20Z02S12[W]",
		"direction": 1,
		"parent": "D20Z01S11[SE]"
	},
	{
		"id": "D20Z02S12[E]",
		"direction": 2,
		"parent": "D20Z02S11[SW]"
	},
	
	{
		"id": "D20Z03S01[W]",
		"direction": 1,
		"parent": "D20Z01S14[E]"
	},
]
