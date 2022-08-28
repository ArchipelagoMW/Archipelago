@archive 6F1054
@size 34

script 10 mmbn6 {
	checkItem
		item = 11
		amount = 1
		jumpIfEqual = 27
		jumpIfGreater = 27
		jumpIfLess = 22
}
@archive 6F12E8
@size 34

script 10 mmbn6 {
	checkItem
		item = 11
		amount = 1
		jumpIfEqual = 27
		jumpIfGreater = 27
		jumpIfLess = 22
}
@archive 75CB24
@size 150

script 0 mmbn6 {
	checkNaviAll
		jumpIfMegaMan = 10
		jumpIfHeatMan = 30
		jumpIfElecMan = 40
		jumpIfSlashMan = 50
		jumpIfEraseMan = 60
		jumpIfChargeMan = 70
		jumpIfSpoutMan = 80
		jumpIfTomahawkMan = 90
		jumpIfTenguMan = 100
		jumpIfGroundMan = 110
		jumpIfDustMan = 120
		jumpIfProtoMan = 10
}
script 3 mmbn6 {
	checkNaviAll
		jumpIfMegaMan = 13
		jumpIfHeatMan = 33
		jumpIfElecMan = 43
		jumpIfSlashMan = 53
		jumpIfEraseMan = 63
		jumpIfChargeMan = 73
		jumpIfSpoutMan = 83
		jumpIfTomahawkMan = 93
		jumpIfTenguMan = 103
		jumpIfGroundMan = 113
		jumpIfDustMan = 123
		jumpIfProtoMan = 13
}
@archive 75CD88
@size 81

script 1 mmbn6 {
	checkSubArea
		lower = 0
		upper = 1
		jumpIfInRange = 60
		jumpIfOutOfRange = 10
	end
}
@archive 75E1A0
@size 81

script 1 mmbn6 {
	checkSubArea
		lower = 0
		upper = 1
		jumpIfInRange = 60
		jumpIfOutOfRange = 10
	end
}
@archive 7B3C1C
@size 41

script 2 mmbn6 {
	checkFlag
		flag = 4608
		jumpIfTrue = continue
		jumpIfFalse = 1
	checkFlag
		flag = 4609
		jumpIfTrue = continue
		jumpIfFalse = 1
	checkFlag
		flag = 4610
		jumpIfTrue = continue
		jumpIfFalse = 1
	checkFlag
		flag = 4611
		jumpIfTrue = continue
		jumpIfFalse = 1
	checkFlag
		flag = 4612
		jumpIfTrue = continue
		jumpIfFalse = 1
	jump
		target = 3
}