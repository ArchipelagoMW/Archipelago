
local goldTotal = 0
local item_timer = 0

--Enemy Shuffleing
local e_model_mode = 0
local e_ai_mode = 0
local shuffled_enemy = {}
local e_shuffled = false
local frame_count = 0


local function shuffle(tbl)
	for i = #tbl, 2, -1 do
	  local j = math.random(i)
	  tbl[i], tbl[j] = tbl[j], tbl[i]
	end
	return tbl
end

local function shuffle_model_list()
	local VALID_MODELS = {0xDE, 0xDF, 0xE0, 0xE1, 0xE2, 0xE4, 0xE5, 0xE6, 0xE7, 0xE8, 0xE9, 0xEA, 0xEB, 0xEC, 0xED, 0xEE, 0xEF, 0xF0, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE, }
	local temp_mdl_list = shuffle(VALID_MODELS)
	local i = 1
	local ai = 0xFF
	local mod = 0x00
	for id= 0xDE, 0xFF, 1 do
		if id == 0xE3 then goto continue end
		if e_ai_mode == 1 then
			ai = math.random(0x00, 0x26)
		end
		if e_model_mode == 1 then
			mod = temp_mdl_list[i]
		end
		shuffled_enemy[id] = {mod,ai}
		::continue::
		i = i + 1
	end
end

local function randomize_model(off)
	local val = math.random(0xDE,0xFE)
	while val == 0xE3 do
		val = math.random(0xDE,0xFE)
	end
	memory.write_u8(0xBA8EB + off, val)
end

local function randomize_ai(off)
	local val = math.random(0x00,0x26)
	memory.write_u8(0xBA8E9 + off, val)
end

local function randomize_enemies(addr, val, flags)
	local e_model = memory.read_u8(0xBA8EB)
	local e_ai = memory.read_u8(0xBA8E9)
	local i = 0
	while e_model > 0xDC and e_model < 0xFF do
		if e_model_mode == 2 then
			randomize_model(i)
		elseif e_model_mode == 1 then
			memory.write_u8(0xBA8EB+ i, shuffled_enemy[e_model][1])
		end
		if e_ai_mode == 2 then
			randomize_ai(i)
		elseif e_ai_mode == 1 then
			memory.write_u8(0xBA8E9+ i, shuffled_enemy[e_model][2])
		end

		i = i + 4
		e_model = memory.read_u8(0xBA8EB + i)
		e_ai = memory.read_u8(0xBA8E9 + i)
	end
	e_shuffled = true
end

local function print_powers()
	local powerups =  memory.read_bytes_as_array(0xAEE00,0x20)
	--local abilities =  memory.read_bytes_as_array(0x2ADFF0,0x10)
	local bombcount = powerups[0xF+1]
	local firecount = powerups[0x13+1]
	local bombstate = powerups[0x0B+1]
	local remote = bombstate & 0x2
	local power = bombstate & 0x1
	local glove = memory.read_u8(0x2ADFF3) & 0xA0
	local kick = ((memory.read_u8(0x2ADFF6)<<8) + memory.read_u8(0x2ADFF7)) & 0x120
	--local kick = ((abilities[0x6 + 1] << 8) + abilities[0x7 + 1]) & 0x120
	local kills = memory.read_u8(0xBD003)
	local golds = memory.read_u8(0xBD007)
	local color = "#303030"
	
	local goldstr = "Gold Cards "..tostring(golds).."/"..goldTotal
	local bomblvlstr = "Bombs: "..tostring(bombcount).." Fires: "..tostring(firecount)
	local killstr = "Kills Needed: "..tostring(kills)
	gui.drawText(180,0,goldstr,"#FFFFFF","#000000")
	gui.drawText(180,10,bomblvlstr,"#FFFFFF","#000000")
	gui.drawText(180,20,killstr,"#FFFFFF","#000000")
	local xpow = 250
	if remote == 2 then
		color = "#FFFFFF"
	else
		color = "#303030"
	end
	gui.drawText(xpow,70,"Remote",color,"#000000")

	if power == 1 then
		color = "#FFFFFF"
	else
		color = "#303030"
	end
	gui.drawText(xpow,80,"Power",color,"#000000")

	if glove == 0xA0 then
		color = "#FFFFFF"
	else
		color = "#303030"
	end
	gui.drawText(xpow,90,"Glove",color,"#000000")

	if kick == 0x120 then
		color = "#FFFFFF"
	else
		color = "#303030"
	end
	gui.drawText(xpow,100,"Kick",color,"#000000")

end

local function print_item(item_in)
	ITEM_TEXT = {
		[0x01] = "I can carry more bombs!",
		[0x02] = "Bombs have been Powered up!",
		[0x03] = "I can now kick bombs!",
		[0x04] = "I can now carry my bombs!",
		[0x05] = "I can now detonate my bombs!",
		[0x06] = "My bombs are super powerful!",
	
		[0x07] = "I feel healthier!",
		[0x08] = "I found a Gold Card!",
		[0x09] = "Kills needed has been reduced.",
		[0x0A] = "I found 5 gems.",
		[0x0B] = "I have an extra life!",
		[0x0C] = "That's one boss down!",
		[0x0D] = "The world is saved!",
	
		[0x0E] = "I can advance into Green Garden!",
		[0x0F] = "I can advance into Blue Resort!",
		[0x10] = "I can advance into Red Mountain!",
		[0x11] = "I can advance into White Glacier!",
		[0x12] = "I can advance into Black Fortress!",
		[0x13] = "I can advance into Rainbow Palace!",
	
		[0x14] = "I feel light!",
		[0x15] = "I can't move!",
		[0x16] = "I feel heavy",
		[0x17] = "I can't use my bombs!",
		[0x18] = "I feel restless!",
		[0x19] = "I'm going to die!",
	}	
	gui.drawText(10,220,ITEM_TEXT[item_in],"#FFFFFF","#000000")
	item_timer = item_timer - 1
	if item_timer == 1 then
		memory.write_u8(0xBD006, 0x00)
	end
end

local function print_customs()
	local checks = memory.read_bytes_as_array(0x8E570,0x6)
	local xbase = 112
	--local checkoffset = 0
	local y = 0
	local fontsize = 8
	local fontfam = 0
	local bgcolor = nil
	local customclr = {
		["red"] = {"#FF0000","#600000"},
		["blue"] = {"#0000FF","#000060"},
		["green"] = {"#00FF00","#006000"},
		["yellow"] ={"#FFFF00","#606000"}}
	local customballs = { -- [World, Level, Byte, Bit, color, number]
		{1,1,1,2,"red",0}, -- GF1 Red
		{3,1,1,3,"red", 0}, -- RM1 Red
		{2,1,1,4,"red",0}, -- BR1 Red
		{6,3,1,5,"red",0}, -- RP3 Red
		{5,3,1,6,"red",0}, -- BF 3 Red
		{4,1,1,7,"red",0}, -- WG1 Red

		{1,3,2,5,"blue",0}, -- GF3 Blue
		{4,1,2,6,"blue",1}, -- WG1 Blue
		{2,3,2,7,"blue",0}, -- BR3 Blue
		{5,3,3,0,"blue",1}, -- BF3 Blue
		{6,1,3,1,"blue",0}, -- RP1 Blue
		{3,3,3,2,"blue",0}, -- RM3 Blue

		{1,1,4,0,"green",1}, --GF 1
		{2,1,4,1,"green",1}, -- BR 1
		{6,1,4,2,"green",1}, -- RP1
		{3,1,4,3,"green",1}, -- RM1
		{5,1,4,4,"green",0}, -- BF1
		{4,3,4,5,"green",0}, -- WG3

		{1,3,5,3,"yellow",1}, -- GF3
		{4,3,5,4,"yellow",1}, -- WG3
		{3,3,5,5,"yellow",1}, -- RM3
		{2,3,5,6,"yellow",1}, -- BR3
		{6,3,5,7,"yellow",1}, -- RP3
		{5,3,6,0,"yellow",2}, --BF3
	}
	for idx, ball in ipairs(customballs) do
		local x = xbase + (ball[6]*8)
		y = ((ball[1] * (fontsize * 5))-(fontsize * 5)) + (ball[2]*fontsize)
		local color = customclr[ball[5]][2]
		local checkbyte = checks[ball[3]]
		local mask = 1 << ball[4]
		local flag = checkbyte & mask
		if flag > 0 then
			bgcolor = "#000000"
			color = customclr[ball[5]][1]
		else
			bgcolor = nil
		end
		gui.pixelText(x,y,"C",color,bgcolor,fontfam)
	end
end


local function print_remotepower()
	local checks = memory.read_bytes_as_array(0x8EF61,0x60)
	local xbase = 94
	local checkoffset = 0
	local y = 0
	local fontsize = 8
	local remotecolor = "#FFC0CB"
	local powercolor = "#FF5349"
	local offcolor = "#303030"
	local fontfam = 0
	local bgcolor = nil
	local remotepower_lookup = {-- [World, Level, Maps, mask, color]
	{1,1,{0x03},0,powercolor}, -- GF1 Power 
	{1,1,{0x01},1,remotecolor}, -- GF1 Remote
	{1,3,{0x08},0,powercolor}, -- GF3 Power 
	{1,3,{0x08},1,remotecolor}, -- GF3 Remote 

	{2,1,{0x12},0,powercolor}, -- BR1 Power 
	{2,1,{0x11},1,remotecolor}, -- BR1 Remote 
	{2,3,{0x15,0x14},0,powercolor}, -- BR3 Power 
	--{2,3,{0x01},1,remotecolor}, -- BR3 Remote 

	{3,1,{0x22},0,powercolor}, -- RM1 Power 
	{3,1,{0x21},1,remotecolor}, -- RM1 Remote 
	{3,3,{0x2B},0,powercolor}, -- RM2 Power 
	{3,3,{0x28,0x2C},1,remotecolor}, -- RM3 Remote 

	{4,1,{0x33},0,powercolor}, -- WG1 Power 
	{4,1,{0x31},1,remotecolor}, -- WG1 Remote 
	--{4,3,{0x03},0,powercolor}, -- WG3 Power 
	{4,3,{0x38},1,remotecolor}, -- WG3 Remote 

	{5,1,{0x45},0,powercolor}, -- BF1 Power 
	{5,1,{0x45},1,remotecolor}, -- BF1 Remote 
	{5,3,{0x4B},0,powercolor}, -- BF3 Power 
	{5,3,{0x46},1,remotecolor}, -- BF3 Remote 

	--{6,1,{0x51},0,powercolor}, -- RP1 Power 
	{6,1,{0x51},1,remotecolor}, -- RP1 Remote 
	{6,3,{0x53},0,powercolor}, -- RP3 Power 
	{6,3,{0x53},1,remotecolor}, -- RP3 Remote 
	}

	for idx, powerup in ipairs(remotepower_lookup) do
		local x = xbase + (powerup[4]*8)
		y = ((powerup[1] * (fontsize * 5))-(fontsize * 5)) + (powerup[2]*fontsize)
		local color = offcolor
		local checkbyte = checks[powerup[3][1]]

		local mask = 1 << powerup[4]

		local flag = checkbyte & mask
		--console.log(checkbyte.." "..powerup[3][1].." "..mask.." "..flag)
		local text = "-"
		if flag > 0 then
			bgcolor = "#000000"
			color = powerup[5]
		else
			bgcolor = nil
		end
		if powerup[4] == 0 then
			text = "P"
		else
			text = "R"
		end
		gui.pixelText(x,y,text,color,bgcolor,fontfam)
	end

	--for w=1, 6, 1  do
	--	for l=1, 4, 1 do
	--		if l == 2 or l == 4 then goto continue end
	--		remotecolor = "#303030"
	--		powercolor = 
	--		checkoffset = ((w-1) * 0x10) + ((l-1) * 0x4) + 4
	--		local byte = checks[checkoffset]
	--		y = ((w * (fontsize*5))-(fontsize*5)) + (l*fontsize)
	--		if byte & 0x02 == 2 then
	--			remotecolor = 
	--		end
	--		if byte & 0x01 == 1 then
	--			powercolor = 
	--		end
	--		gui.pixelText(xbase,y,"P",powercolor,bgcolor,fontfam)
	--		gui.pixelText(xbase + 8,y,"R",remotecolor,bgcolor,fontfam)
	--		::continue::
	--	end
	--end
end

local function print_stages()
	local worldabv = {
		"GG","BR","RM","WG","BF","RP"
	}
	local worldclr = {
		"#00FF00","#5DACEB","#FF0000","#FFFFFF","#909090","#A020F0"
	}
	
	local fontsize = 8
	local fontfam = 0
	local bgcolor = nil
	local worldbgcolor = nil
	local stage_clears = memory.read_bytes_as_array(0x8E5DC,0x64)
	local stage_unlocks = memory.read_bytes_as_array(0x8EF00,0x60)
	local gold_cards =  memory.read_bytes_as_array(0x8E575,0x10)
	gui.pixelText(10,0,"Green Garden",worldclr[1],worldbgcolor,fontfam)
	gui.pixelText(10,(fontsize * 5),"Blue Resort",worldclr[2],worldbgcolor,fontfam)
	gui.pixelText(10,(fontsize * 10),"Red Mountain",worldclr[3],worldbgcolor,fontfam)
	gui.pixelText(10,(fontsize * 15),"White Glacier",worldclr[4],worldbgcolor,fontfam)
	gui.pixelText(10,(fontsize * 20),"Black Fortress",worldclr[5],worldbgcolor,fontfam)
	local ranbowtext = "Rainbow Palace"
	local i = 0
	local rainbowhex = {
		"#F89696", -- R 
		"#F8C396", -- a
		"#F8F196", -- i
		"#D2F896", -- n 
		"#A5F896", -- b
		"#96F8B4", -- o
		"#96F8E1", -- w 
		"#79c314", --
		"#96E1F8", -- P
		"#96B4F8", -- a
		"#A596F8", -- l 
		"#D296F8", -- a
		"#F896F1", -- c
		"#F896C3", -- e 
	}
	for c in ranbowtext:gmatch"." do
		i = i+1
		gui.pixelText(((i-1)*(fontsize-2)) + 10 ,(fontsize * 25),c,rainbowhex[i],worldbgcolor,fontfam)
	end
	--gui.pixelText(10,(fontsize * 25),"Rainbow Palace",worldclr[6],bgcolor,fontfam)
	--local adokHave = memory.read_u8(0x57499)
	--local adokstr = tostring("Adok Bomb: "..adokHave.."/"..adokTotal)
	--gui.drawText(180,0,adokstr,"#FFFFFF","#000000")
	
	for w=1, 6, 1  do
		for l=1, 4, 1 do
			local stagetext = worldabv[w].."-"..tostring(l).." "
			local y = ((w * (fontsize * 5))-(fontsize * 5)) + (l*fontsize)
			local x = 10
			local color = "#303030"
			local stage_offset = (((w-1)*0x10)+ ((l-1)*0x4)+1)
			local bgclr = "#000000"
			local goldoffset = 0
			local goldbit = 0
			local goldbase = 0

			if l == 1 then
				color = "#B0B0B0"
			end
			if l > 1 then
				if (stage_unlocks[(stage_offset+3)-4]  ~= 0x00) then
					color = "#B0B0B0"
				end
			end

			if  (stage_clears[(stage_offset+3)] > 0x00) then
					color = worldclr[w]
			end


			--if w == 5 then
			--	bgclr = "#FFFFFF"
			--end

			gui.pixelText(x,y,stagetext,color,bgcolor,fontfam)
			for g=1,5,1 do
				color = "#FFFFFF"
				goldbase = (((w-1)*20) + ((l-1)*5) + (g-1)+4)
				goldoffset = math.floor(goldbase/8)
				goldbit = 1 << (goldbase % 8)
				--console.log(goldoffset)
				--console.log(goldbit)
				if (gold_cards[goldoffset+1] & goldbit) ~= 0x00 then
					color = "#FFD700"
				end
				x = ((g-1) *8) + 50
				gui.pixelText(x,y,"G",color,"#000000",fontfam)
			end
		end
	end
end

local function startup()
	memory.usememorydomain("ROM")
	goldTotal = memory.read_u8(0xDFFB0)
	e_model_mode = memory.read_u8(0xDFFB4)
	e_ai_mode = memory.read_u8(0xDFFB5)
	memory.usememorydomain("RDRAM")

	if e_model_mode == 1 or e_ai_mode == 1 then
		shuffle_model_list()
	end
end

startup()

while true do
	gui.cleartext()
	gui.clearGraphics()
	frame_count = frame_count + 1

	local in_item = memory.read_u8(0xBD006)
	--Print recieved item
	if in_item ~= 0 and item_timer == 0 then
		item_timer = 180
	end
	if item_timer > 0 then
		print_item(in_item)
	end
	-- Randomize Enemies
	local enemy_state = memory.read_u8(0xBA8E8)
	if enemy_state == 0xFF then
		e_shuffled = false
	end
	if (e_model_mode > 0 or e_ai_mode > 0) and (e_shuffled == false) and (enemy_state == 0x00) then
		randomize_enemies()
	end

	--print tracker
	if joypad.get(1)["DPad D"] == true then
		print_stages()
		print_remotepower()
		print_customs()
		print_powers()
	end
	emu.frameadvance();
end
