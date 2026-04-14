checks = {}
didAPLoad = false
ignoreSaveSeed = false
manualChecks = false
local level_mapping = {}
local thisWorld = generaldata.strings[WORLD] -- name of this world
if #thisWorld == 0 then thisWorld = "babapelago" end

local noun_checks = {"text_baba", "text_flag", "text_wall", "text_rock", "text_skull", "text_lava", "text_star", "text_crab", "text_keke", "text_love", "text_pillar", "text_jelly", "text_key", "text_door", "text_rose", "text_violet", "text_water", "text_robot", "text_bolt", "text_cog", "text_box", "text_ghost", "text_ice", "text_leaf", "text_fence", "text_me", "text_belt", "text_tree", "text_bug", "text_fungus", "text_cloud", "text_rocket", "text_ufo", "text_moon", "text_dust", "text_grass", "text_hand", "text_fruit", "text_bat", "text_fire", "text_bird", "text_sun", "text_tile", "text_orb", "text_hedge", "text_cliff", "text_cake"}
local special_noun_checks = {"text_text", "text_empty", "text_all", "text_level", "text_group", "text_cursor", "text_image"}
local verb_checks = {"text_is", "text_has", "text_make", "text_write"}
local prop_checks = {"text_you", "text_win", "text_stop", "text_push", "text_sink", "text_defeat", "text_hot", "text_melt", "text_move", "text_open", "text_shut", "text_red", "text_blue", "text_float", "text_weak", "text_tele", "text_pull", "text_shift", "text_up", "text_down", "text_left", "text_right", "text_swap", "text_best", "text_fall", "text_more", "text_word", "text_sleep", "text_end", "text_hide", "text_bonus", "text_done"}
local condition_checks = {"text_on", "text_facing", "text_lonely", "text_near"}
local letter_checks = {"text_a", "text_ab", "text_b", "text_ba", "text_c", "text_e", "text_f", "text_g", "text_h", "text_i", "text_l", "text_m", "text_n", "text_o", "text_r", "text_s", "text_t", "text_u", "text_v", "text_w", "text_x"}
local other_checks = {"text_and", "text_not"}
local world_key_list = {"Lake Key", "Island Key", "Ruins Key", "Fall Key", "Forest Key", "Space Key", "Garden Key", "Chasm Key", "Cavern Key", "Mountain Key", "ABC Key"}
local non_word_items = {
    ["Speck"] = 0,
    ["Blossom"] = 0,
    ["Blossom Petal"] = 0,
    ["Bonus Orb"] = 0,
    ["Lake Key"] = 1,
    ["Island Key"] = 1,
    ["Ruins Key"] = 1,
    ["Fall Key"] = 1,
    ["Forest Key"] = 1,
    ["Space Key"] = 1,
    ["Garden Key"] = 1,
    ["Chasm Key"] = 1,
    ["Cavern Key"] = 1,
    ["Mountain Key"] = 1,
    ["ABC Key"] = 1,
}

local all_checks_list = {noun_checks, verb_checks, prop_checks, condition_checks, special_noun_checks, other_checks, letter_checks, world_key_list}
local all_checks_list_name = {"Nouns", "Verbs", "Properties", "Conditions", "Special Nouns", "Misc.", "Letters", "World Keys"}

local level_name_to_id = {}

local need_key = {
    ["177level"] = "Lake Key",
    ["207level"] = "Island Key",
    ["206level"] = "Ruins Key",
    ["16level"] = "Fall Key",
    ["169level"] = "Forest Key",
    ["87level"] = "Space Key",
    ["180level"] = "Garden Key",
    ["182level"] = "Chasm Key",
    ["179level"] = "Cavern Key",
    ["232level"] = "Mountain Key",
    ["282level"] = "ABC Key",
}
local have_clears_or_completes = {
    ["177level"] = 3,
    ["207level"] = 3,
    ["206level"] = 3,
    ["16level"] = 3,
    ["169level"] = 3,
    ["87level"] = 3,
    ["180level"] = 3,
    ["182level"] = 3,
    ["179level"] = 3,
    ["232level"] = 3,
    ["282level"] = 3,
}

local message_list = {}
local error_message = ""
function add_to_messages(text)
    table.insert(message_list, {text, 300})
end

-- Set up options
local options = {
    goal=0,
    goal_levels=80,
    goal_blossoms=7,
    start_with_default_words=1,
    open_map=1,
    world_keys=1,
    area_access=0,
    exclude_whoa=1,
    exclude_gallery=1,
    exclude_write=1,
    blossom_petals=0,
    blossoms=12,
    first_gate_blossoms=3,
    second_gate_blossoms=5,
    third_gate_blossoms=7,
    complete_checks=1,
    level_shuffle=0,
    seed="",
}
MF_setfile("level","AP/"..thisWorld.."/AP_OPTIONS.data")
for option, default in pairs(options) do
    local value = MF_read("level", "options", option) or "0"
    if value == "True" then
        value = "1"
    elseif value == "False" then
        value = "0"
    end
    if option ~= "seed" then
        options[option] = tonumber(value) or default
    else
        options[option] = value
    end
end
MF_setfile("level","Data/Worlds/" .. generaldata.strings[WORLD] .. "/" .. generaldata.strings[CURRLEVEL] .. ".ld")

function deep_copy(thisTable)
    local result = {}
    for i,v in pairs(thisTable) do
        if type(v) == "table" then
            result[i] = deep_copy(v)
        else
            result[i] = v
        end
    end
    return result
end

table.insert(mod_hook_functions.rule_baserules, function()
    addbaserule("text", "is", "still", { { "unchecked", {} } })
    addbaserule("text", "is", "grey", { { "unchecked", {} } })
    addbaserule("text", "is", "phantom", { { "unchecked", {} } })
    addbaserule("text", "is", "missing", { { "unchecked", {} } })
end)

-- Handle win checks
timer = 0
table.insert(mod_hook_functions.effect_always, function()
    timer = (timer % 100) + 1
    doeffect(timer,nil,"missing","wonder",1,10,5,{2,2})
end)

-- Handle win checks
table.insert(mod_hook_functions.level_win_after, function()
    MF_setfile("level", "AP/"..thisWorld.."/AP_CHECKS.data")
    local levelname = generaldata.strings[LEVELNAME]
    levelname = capitalize(levelname)
    MF_store("level","checks",levelname..": Win", "1")
    MF_setfile("level","Data/Worlds/" .. generaldata.strings[WORLD] .. "/" .. generaldata.strings[CURRLEVEL] .. ".ld")
end)

condlist["unchecked"] = function(params, checkedconds, checkedconds_, cdata)
    local name = "empty"
    if cdata.unitid == 1 then
        name = "level"
    elseif cdata.unitid ~= 2 then
        local unit = mmf.newObject(cdata.unitid)
        name = unit.strings[UNITNAME]
    end
    return (checks[name] == nil), checkedconds
end

-- Handles custom blossom settings
local orig_addpath = addpath
function addpath(id)
    orig_addpath(id)
    local unitid = paths[#paths]
    local unit = mmf.newObject(unitid)
    if (unit.values[PATH_GATE] == 2) then
        if manualChecks then
            unit.values[PATH_REQUIREMENT] = 0
        elseif unit.values[PATH_REQUIREMENT] == 3 then -- First gate
            unit.values[PATH_REQUIREMENT] = options.first_gate_blossoms
        elseif unit.values[PATH_REQUIREMENT] == 5 then -- Second gate
            unit.values[PATH_REQUIREMENT] = options.second_gate_blossoms
        elseif unit.values[PATH_REQUIREMENT] == 7 then -- Third gate
            if options.area_access ~= 0 then
                unit.values[PATH_REQUIREMENT] = options.third_gate_blossoms
            else
                unit.values[PATH_REQUIREMENT] = 999 -- block access when area access is early
            end
        end
    end
end

-- set all levels to open on map if enabled (except depths, meta, and center)
orig_loadlevelcompletion = orig_loadlevelcompletion or loadlevelcompletion
function loadlevelcompletion()
    --MF_store("save","babapelago_clears","total", 3)

    local levels = {}
    for i,unit in ipairs(units) do
        local levelfile = unit.strings[U_LEVELFILE]
        if string.len(levelfile) > 1 then
            table.insert(levels, unit)
        end
    end

    local result = orig_loadlevelcompletion()
    if generaldata.strings[CURRLEVEL] == "106level" and options.open_map ~= 0 then
        local unlockPos = {}
        for i, unit in ipairs(levels) do
            local levelfile = unit.strings[U_LEVELFILE]
            if unit.values[COMPLETED] < 2 and
            levelfile ~= "264level" and levelfile ~= "283level" and levelfile ~= "304level" then
                unit.values[COMPLETED] = 2
                local x,y = unit.values[XPOS],unit.values[YPOS]
                table.insert(unlockPos, {x, y})
            end
        end

        for i,pos in ipairs(unlockPos) do
            local x, y = pos[1], pos[2]
            unlocklevels(x,y,nil,true)
            hiddendata(x,y,true)
        end
    end

    return result
end

-- handles level randomization
orig_addunit = addunit
function addunit(id,undoing_,levelstart_)
    local result = orig_addunit(id,undoing_,levelstart_)

    local unit = mmf.newObject(id)
    local levelfile = unit.strings[U_LEVELFILE]
    if string.len(levelfile) > 1 then
        -- randomization
        local newFile = level_mapping[levelfile] or levelfile
        if levelfile ~= newFile then
            levelfile = newFile
            unit.strings[U_LEVELFILE] = levelfile
            MF_setfile("level","Data/Worlds/" .. generaldata.strings[WORLD] .. "/" .. levelfile .. ".ld")
            local levelname = MF_read("level","general","name")
            MF_setfile("level","Data/Worlds/" .. generaldata.strings[WORLD] .. "/" .. generaldata.strings[CURRLEVEL] .. ".ld")
            unit.strings[U_LEVELNAME] = levelname
        end
    end

    return result
end

-- prevent entering worlds we don't have the key for, or that are outside of our area access
function mapcursor_enter(varsunitid)
	local cursors = getunitswitheffect("select",true)
	local varsunit = mmf.newObject(varsunitid)
	local entering = {}
	
	for i,unit in ipairs(cursors) do
		local targetfound = MF_findunit_fixed(unit.values[CURSOR_ONLEVEL])
		
		if targetfound then
			local allhere = findallhere(unit.values[XPOS],unit.values[YPOS],unit.fixed)
			
			for a,b in ipairs(allhere) do
				local lunit = mmf.newObject(b)
				
				if (string.len(lunit.strings[U_LEVELFILE]) > 0) and (string.len(lunit.strings[U_LEVELNAME]) > 0) and (generaldata.values[IGNORE] == 0) and (lunit.values[COMPLETED] > 1) then
					local valid = true
					
					for c,d in ipairs(cursors) do
						if (d.fixed == b) then
							valid = false
							break
						end
					end

                    -- KEY CHECK
                    local needed_key = need_key[lunit.strings[U_LEVELFILE]]
                    if options.world_keys ~= 0 and needed_key and not checks[needed_key] then
                        MF_playsound("tune_blop")
                        particles("wonder",unit.values[XPOS],unit.values[YPOS],5,{2,2})
                        add_to_messages("Need \""..needed_key.."\"")
                        valid = false
                    end
                    -- END KEY CHECK
					
					if valid then
						table.insert(entering, {b, lunit.strings[U_LEVELNAME], lunit.strings[U_LEVELFILE]})
					end
				end
			end
		end
	end
	
	if (#entering > 0) then
		dolog("end","event")
	end
	
	if (#entering == 1) then
		generaldata2.values[UNLOCK] = 0
		generaldata2.values[UNLOCKTIMER] = 0
		varsunit.values[1] = entering[1][1]
		MF_loop("enterlevel", 1)
	elseif (#entering > 0) then
		MF_menuselector_hack(1)
		submenu("enterlevel_multiple",entering)
		print("Trying to enter multiple levels!")
	end
end

orig_findletterwords = findletterwords
function findletterwords(...)
    -- behave as base world
    local prevBase = generaldata.strings[BASEWORLD]
    generaldata.strings[BASEWORLD] = generaldata.strings[WORLD]
    local results = table.pack(orig_findletterwords(...))
    generaldata.strings[BASEWORLD] = prevBase -- change back after running
    return table.unpack(results)
end

-- Go to different first level when level shuffle is on
orig_firstlevel = orig_firstlevel or firstlevel
function firstlevel()
    orig_firstlevel()
    generaldata.strings[CURRLEVEL] = level_mapping[generaldata.strings[CURRLEVEL]] or generaldata.strings[CURRLEVEL]
end

-- menu for checks
local itempage = 1
local itemtype = 1
local PER_PAGE = 10
local old_pause = menufuncs.pause.enter
menufuncs.pause.enter = function(...)
    old_pause(...)
    createbutton("items", 50, screenh - 20, 2, 4, 1, "Items", "pause", 3, 2, menufuncs.pause.button)
end

buttonclick_list["items"] = function(unitid)
    submenu("item_categories")
end

menufuncs.item_categories = {
    button = "Item_Categories",
    escbutton = "item_close",
    enter = function(parent, name, buttonid)
        local dynamic_structure = {}
        local x = screenw * 0.5
        local y = f_tilesize * 2

        writetext("Select a category:", 0, x, y, name, true, 2)
        y = y + f_tilesize

        for i,data in ipairs(all_checks_list) do
            local category_name = all_checks_list_name[i] or tostring(i)
            local disabled = (category_name == "World Keys" and options.world_keys == 0)
            
            y = y + f_tilesize
            createbutton("item_category_" .. i, x, y, 2, 12, 1, category_name, name, 3, 2, buttonid, disabled, 0)
            table.insert(dynamic_structure, { { "item_category_" .. i } })
            buttonclick_list["item_category_" .. i] = function(unitid)
                itemtype = i
                itempage = 1
                submenu("items")
            end
        end

        y = y + f_tilesize * 2
        createbutton("item_close", x, y, 2, 12, 1, langtext("editor_menu_close"), name, 1, 3, buttonid)

        local goal = ""
        if options.goal == 0 then
            goal = "Reach \"A Way Out?\" and get the normal ending."
        elseif options.goal == 1 then
            goal = "Reach \"???\"."
        elseif options.goal == 2 then
            goal = "Reach \"Depths\"."
        elseif options.goal == 3 then
            goal = "Reach \"Meta\"."
        elseif options.goal == 4 then
            goal = "Reach \"The End\" and form ALL IS DONE."
        elseif options.goal == 5 then
            goal = "Complete " .. options.goal_levels .. " levels"
        elseif options.goal == 6 then
            goal = "Collect " .. options.goal_blossoms .. " blossoms"
        end
        goal = "Goal: " .. goal
        writetext(goal, 0, screenw / 2, screenh - f_tilesize * 2, name, true, 2)

        table.insert(dynamic_structure, { { "item_close" } })
        buildmenustructure(dynamic_structure)
    end,
    leave = function(parent, name, buttonid)
        MF_letterclear(name)
    end,
}

menufuncs.items = {
    button = "Items",
    escbutton = "item_close",
    enter = function(parent, name, buttonid)
        local dynamic_structure = {}
        local x = screenw * 0.5
        local y = f_tilesize * 2

        local curr_checks = all_checks_list[itemtype]
        local totalpages = (#curr_checks-1) // PER_PAGE + 1

        local category_name = all_checks_list_name[itemtype] or tostring(itemtype)
        writetext(category_name, 0, x, y, name, true, 2)
        y = y + f_tilesize

        local item_num = (itempage-1) * PER_PAGE
        for i=1,PER_PAGE do
            item_num = item_num + 1
            local item_name = curr_checks[item_num]
            if not item_name then break end
            local formatted_name = item_name:gsub("text_", "")
            
            local checked = math.min(checks[item_name] or 0, 1)
            y = y + f_tilesize
            createbutton("item_" .. i, x, y, 2, 12, 1, formatted_name, name, 3, 2, buttonid, false, checked)
            table.insert(dynamic_structure, { { "item_" .. i } })
            if manualChecks then
                buttonclick_list["item_" .. i] = function(unitid)
                    local button = mmf.newObject(unitid)
                    if checks[item_name] then
                        checks[item_name] = nil
                    else
                        checks[item_name] = 1
                    end
                    local value = (checks[item_name] and 1) or 0
                    button.values[BUTTON_SELECTED] = value
                    updatebuttoncolour(unitid, value)
                end
            else
                buttonclick_list["item_" .. i] = nil
            end
        end

        y = f_tilesize * (PER_PAGE + 5)
        writetext("Page " .. itempage .. " / " .. totalpages, 0, x, y, name, true, 2)
        y = y + f_tilesize
        createbutton("item_back", x - 100, y, 2, 6, 1, "<", name, 1, 3, buttonid, (itempage <= 1))
        createbutton("item_forward", x + 100, y, 2, 6, 1, ">", name, 1, 3, buttonid, (itempage >= totalpages))
        table.insert(dynamic_structure, { { "item_back" }, { "item_forward" } })
        y = y + f_tilesize

        y = y + f_tilesize
        createbutton("item_close", x, y, 2, 12, 1, langtext("editor_menu_close"), name, 1, 3, buttonid)
        table.insert(dynamic_structure, { { "item_close" } })
        buildmenustructure(dynamic_structure)
    end,
    leave = function(parent, name, buttonid)
        MF_letterclear(name)
    end,
}

buttonclick_list["item_back"] = function(unitid)
    itempage = itempage - 1
    closemenu()
    submenu("items")
end
buttonclick_list["item_forward"] = function(unitid)
    itempage = itempage + 1
    closemenu()
    submenu("items")
end
buttonclick_list["item_close"] = function(unitid)
    closemenu()
end

-- utility function to list all levels
local test_level_list = {}
function listlevels()
    local world = generaldata.strings[WORLD]
    local files = MF_filelist("Data/Worlds/" .. world .. "/", "*.l")

    if #test_level_list ~= 0 then
        MF_setfile("level", "LEVEL_LIST.data")
        for i, level in ipairs(test_level_list) do
            MF_store("level", "general", level, "1")
        end

        if generaldata.strings[CURRLEVEL] == "" then
            MF_setfile("level", "Data/Temp/temp.ld")
        else
            MF_setfile("level",
                "Data/Worlds/" .. generaldata.strings[WORLD] .. "/" .. generaldata.strings[CURRLEVEL] .. ".ld")
        end
        return
    end

    -- to know the parent, we instead look for a map level and check all levels inside of it
    for a, file in ipairs(files) do
        local parent = string.sub(file, 1, -3)
        MF_setfile("level", "Data/Worlds/" .. world .. "/" .. parent .. ".ld")
        local parentName = MF_read("level", "general", "name")

        local levels = {}
        local totalLevels = MF_read("level", "general", "levels")
        if totalLevels ~= 0 then
            for b = 0, totalLevels - 1 do
                local level = MF_read("level", "levels", tostring(b) .. "file")
                table.insert(levels, level)
            end
        end
        local totalSpecials = MF_read("level", "general", "specials")
        if totalSpecials ~= 0 then
            for b = 0, totalSpecials - 1 do
                local data = MF_read("level", "specials", tostring(b) .. "data")
                if data:sub(1, 6) == "level," then
                    local dataTable = split(data, ",")
                    table.insert(levels, dataTable[2])
                end
            end
        end

        -- hardcoded woah
        if world == generaldata.strings[BASEWORLD] and parent == "283level" then
            table.insert(levels, "327level")
        end

        local alreadyDid = {}
        for i, level in ipairs(levels) do
            MF_setfile("level", "Data/Worlds/" .. world .. "/" .. level .. ".ld")
            local customparent = MF_read("level", "general", "customparent") or ""
            if customparent == "" or customparent == parent then
                if not alreadyDid[level] then
                    local map = (MF_read("level", "general", "leveltype") == "1")
                    if not map then
                        print("\""..level.."\",")
                        local name = MF_read("level", "general", "name")
                        table.insert(test_level_list, capitalize(name)..": "..capitalize(parentName))
                        alreadyDid[level] = 1
                    end
                end
            end
        end
    end

    if generaldata.strings[CURRLEVEL] == "" then
        MF_setfile("level", "Data/Temp/temp.ld")
    else
        MF_setfile("level",
            "Data/Worlds/" .. generaldata.strings[WORLD] .. "/" .. generaldata.strings[CURRLEVEL] .. ".ld")
    end
end

table.insert(mod_hook_functions.keyboard_input, function(data)
    if didAPLoad or editor.strings[MENU] ~= "ingame" then return end

    local key = data[1]
    if key == "M" then
        error_message = ""
        manualChecks = not manualChecks
        if manualChecks then
            add_to_messages("Manual check mode enabled (use menu)")
        else
            add_to_messages("Manual check mode disabled")
        end
    elseif key == "I" then
        ignoreSaveSeed = not ignoreSaveSeed
        if ignoreSaveSeed then
            add_to_messages("Ignoring save file's seed")
        else
            add_to_messages("No longer ignoring save file's seed")
        end
    elseif key == "L" then
        --add_to_messages("Level list test")
        --listlevels()
    end
end)

local checkTimer = 0
local clear_goal_locations = {}
function update_checks()
    if generaldata.strings[WORLD] ~= thisWorld or editor.strings[MENU] ~= "ingame" then return end
    if manualChecks then return end

    checkTimer = checkTimer + 1
    if checkTimer < 30 then return end
    checkTimer = 0

    -- Verify seed is correct
    error_message = ""
    local trueSeed = ""
    local ourSeed = options.seed or ""
    local files = MF_filelist("AP/"..thisWorld, "/*.data")
    for i, file in ipairs(files) do
        if file:sub(1, 8) == "AP_SEED_" then
            trueSeed = file:sub(9, -6)
            break
        end
    end

    if #trueSeed == 0 or trueSeed ~= ourSeed then
        if #trueSeed == 0 then
            error_message = ("$2,2Missing seed file. Please connect to the server using the Baba Is You client.")
        else
            error_message = ("$2,2Game seed does not match AP seed. Please relaunch Baba Is You.")
        end
        MF_setfile("level","Data/Worlds/" .. generaldata.strings[WORLD] .. "/" .. generaldata.strings[CURRLEVEL] .. ".ld")
        return
    end

    -- Compare save file seed to AP seed
    if not (didAPLoad or ignoreSaveSeed) then
        local savedSeed = MF_read("save", thisWorld, "apseed")
        if savedSeed == nil or #savedSeed == 0 then
            MF_store("save", thisWorld, "apseed", ourSeed)
        elseif savedSeed ~= ourSeed then
            error_message = ("$2,2Save file is for another seed! Press I to ignore.")
            MF_setfile("level","Data/Worlds/" .. generaldata.strings[WORLD] .. "/" .. generaldata.strings[CURRLEVEL] .. ".ld")
            return
        end
    end
    
    local world = generaldata.strings[WORLD]

    local prev_blossom_count = tonumber(MF_read("save",world .. "_clears","total")) or 0
    local blossom_count = 0
    local blossom_petal_count = 0
    local bonus_count = 0

    files = MF_filelist("AP/"..thisWorld, "/*.item")
    local prevChecks = checks
    checks = {}
    obtained_keys = {}
    for i, file in ipairs(files) do
        MF_setfile("level", "AP/"..thisWorld.."/"..file)
        local item = MF_read("level", "data", "item")
        if item and #item ~= 0 then
            local trueName = item
            if not non_word_items[item] then
                trueName = "text_" .. item:lower()
            end

            if item == "Blossom" then
                blossom_count = blossom_count + 1
            elseif item == "Blossom Petal" then
                blossom_petal_count = blossom_petal_count + 1
            elseif item == "Bonus Orb" then
                bonus_count = bonus_count + 1
            end

            if not checks[trueName] then
                checks[trueName] = 0
            end
            checks[trueName] = checks[trueName] + 1

            if didAPLoad and (prevChecks[trueName] == nil or prevChecks[trueName] < checks[trueName]) then
                local player = MF_read("level", "data", "player") or "Unknown"
                local location = MF_read("level", "data", "location") or "Unknown"
                add_to_messages(string.format("Received \"%s\" from %s (%s)", item, player, location))
            end
        end
    end

    blossom_count = blossom_count + blossom_petal_count // 8
    MF_store("save",world .. "_clears","total",blossom_count)
    MF_store("save",world .. "_bonus","total",bonus_count)
    
    -- Create blossom when received
    if prev_blossom_count < blossom_count then
        local cursors = getunitswitheffect("select",true)
        if #cursors ~= 0 then
            local x, y = cursors[1].values[XPOS], cursors[1].values[YPOS]
            y = y - 1
            local prizeid = MF_specialcreate("Prize")
		    local prize = mmf.newObject(prizeid)
            prize.layer = 2
            prize.values[ONLINE] = 1
            prize.values[XPOS] = Xoffset + x * tilesize + tilesize * 0.5
            prize.values[YPOS] = Yoffset + y * tilesize + tilesize * 0.5
            prize.values[YVEL] = 0
            prize.scaleX = 0.1
            prize.scaleY = 0.1
            prize.direction = 1
        end
    end

    -- send clear and complete locations
    local prev_clear_goal_locations = clear_goal_locations
    clear_goal_locations = {}
    for level, info in pairs(have_clears_or_completes) do
        MF_setfile("level","Data/Worlds/" .. world .. "/" .. level .. ".ld")
        local levelname = MF_read("level", "general", "name") or level
        levelname = capitalize(levelname)
        if info & 1 ~= 0 then -- Clear
            local clear = tonumber(MF_read("save",world .. "_clears", level)) or 0
            if clear ~= 0 then
                clear_goal_locations[levelname..": Clear"] = 1
            end
        end
        if info & 2 ~= 0 then -- Complete
            local clear = tonumber(MF_read("save",world .. "_complete", level)) or 0
            if clear ~= 0 then
                clear_goal_locations[levelname..": Complete"] = 1
            end
        end
    end

    -- Check goal
    local goal = 0
    if options.goal == 0 then
        goal = tonumber(MF_read("save",world .. "_end_single", "total")) or 0
    elseif options.goal == 4 then
        goal = tonumber(MF_read("save",world .. "_done_single", "total")) or 0
    elseif options.goal == 5 then
        local prizes = tonumber(MF_read("save",world .. "_prize", "total")) or 0
        goal = (prizes >= options.goal_levels and 1) or 0
    elseif options.goal == 6 then
        goal = (blossom_count >= options.goal_blossoms and 1) or 0
    end
    if goal ~= 0 then
        clear_goal_locations["Goal"] = 1
    end

    MF_setfile("level", "AP/"..thisWorld.."/AP_CHECKS.data")
    for location, v in pairs(clear_goal_locations) do
        if not prev_clear_goal_locations[location] then
            MF_store("level","checks",location, "1")
        end
    end

    didAPLoad = true
    MF_setfile("level","Data/Worlds/" .. generaldata.strings[WORLD] .. "/" .. generaldata.strings[CURRLEVEL] .. ".ld")
end

table.insert(mod_hook_functions.always, update_checks)

function display_messages()
    local id = "ap_messages"
    MF_letterclear(id)
    
    local y = screenh - math.min(#message_list, 10) * 20
    if #error_message ~= 0 then
        y = y - 20
    end

    local layer = ((generaldata2.values[INMENU] ~= 0) and 1) or 2
    local i = 1
    local displayed = 1
    while i <= #message_list and displayed <= 10 do
        local msgData = message_list[i]
        local msg, time = msgData[1], msgData[2]
        msg = msg:gsub("#", "") -- # has special meaning (also removed on AP's end but it's here for safety)

        writetext(msg, 0, 20, y, id, false, layer, true)
        time = time - 1
        msgData[2] = time
        if time <= 0 then
            table.remove(message_list, i)
        else
            i = i + 1
        end
        displayed = displayed + 1

        y = y + 20
    end
    
    if #error_message ~= 0 then
        writetext(error_message, 0, 20, y, id, false, layer, true)
    end
end
table.insert(mod_hook_functions.always, display_messages)

-- Converts string into a table using a delimiter
function split(s, delimiter)
    local result = {}
    local match = ""
    for i = 1, #s do
        local char = s:sub(i, i)
        if char == delimiter then
            table.insert(result, match)
            match = ""
        else
            match = match .. char
        end
    end
    table.insert(result, match)
    return result
end

function capitalize_word(word)
    return word:sub(1,1):upper()..word:sub(2)
end
function capitalize(str)
    return str:gsub("%a[^%s]*", capitalize_word)
end

function auto_gen_level_name_to_id(level_name_to_id)
    local world = thisWorld
    local files = MF_filelist("Data/Worlds/" .. world .. "/", "*.l")

    -- to know the parent, we instead look for a map level and check all levels inside of it
    for a, file in ipairs(files) do
        local parent = string.sub(file, 1, -3)
        MF_setfile("level", "Data/Worlds/" .. world .. "/" .. parent .. ".ld")

        local mapId = MF_read("level", "general", "mapid") or ""

        local levels = {}
        local levelExtra = {}
        local totalLevels = MF_read("level", "general", "levels")
        if totalLevels ~= 0 then
            for b = 0, totalLevels - 1 do
                local level = MF_read("level", "levels", tostring(b) .. "file")
                local style = tonumber(MF_read("level", "levels", tostring(b) .. "style")) or 0
                local number = tonumber(MF_read("level", "levels", tostring(b) .. "number")) or 0
                local numberStr = ""
                if style == 0 or style > 2 then
                    numberStr = tostring(number)
                elseif style == 2 then
                    numberStr = "Extra "..tostring(number+1)
                elseif style == 1 then
                    numberStr = string.char(number + 65)
                end
                table.insert(levels, level)
                table.insert(levelExtra, numberStr)
            end
        end
        local totalSpecials = MF_read("level", "general", "specials")
        if totalSpecials ~= 0 then
            for b = 0, totalSpecials - 1 do
                local data = MF_read("level", "specials", tostring(b) .. "data")
                if data:sub(1, 6) == "level," then
                    local dataTable = split(data, ",")
                    local style = tonumber(dataTable[3]) or 0
                    local number = tonumber(dataTable[4]) or 0
                    local numberStr = ""
                    if style == 0 or style > 2 then
                        numberStr = tostring(number)
                    elseif style == 1 then -- why is it different from normal levels?
                        numberStr = "Extra "..tostring(number)
                    elseif style == 2 then
                        numberStr = string.char(number + 65)
                    end
                    table.insert(levels, dataTable[2])
                    table.insert(levelExtra, numberStr)
                end
            end
        end

        -- hardcoded whoa
        if parent == "283level" then
            table.insert(levels, "327level")
            table.insert(levelExtra, "Secret 2")
        end

        for i, level in ipairs(levels) do
            MF_setfile("level", "Data/Worlds/" .. world .. "/" .. level .. ".ld")
            local customparent = MF_read("level", "general", "customparent") or ""
            
            if customparent == "" or customparent == parent then
                local numberStr = levelExtra[i]
                local isMap = (tonumber(MF_read("level", "general", "leveltype")) == 1)
                local mapId2 = MF_read("level", "general", "mapid") or ""
                local customLevelName = ""
                if isMap then
                    customLevelName = capitalize(mapId2)
                else
                    if #mapId2 ~= 0 then numberStr = capitalize(mapId2) end
                    customLevelName = capitalize_word(mapId) .. "-" .. numberStr
                end
                --error(customLevelName)
                level_name_to_id[customLevelName] = level
            end
        end
    end

    --[[MF_setfile("level", "AP/TEST_NAMES.data")
    for old,new in pairs(level_name_to_id) do
        MF_store("level", "general", old, new)
    end]]
    
    -- Set up level shuffle (not active in editor)
    level_mapping = {}
    if options.level_shuffle ~= 0 and editor.values[INEDITOR] == 0 then
        MF_setfile("level","AP/"..thisWorld.."/AP_SHUFFLE.data")
        local total = tonumber(MF_read("level", "general", "total")) or 0
        for i=0,total-1 do
            local newPath = MF_read("level", "general", tostring(i))
            if newPath then
                levelData = split(newPath, "@")
                local level1 = level_name_to_id[levelData[1]]
                local level2 = level_name_to_id[levelData[2]]
                if level1 == nil then
                    error("Level Shuffle - Couldn't find level: "..levelData[1])
                end
                level_mapping[level1] = level2
            end
        end
    end

    if generaldata.strings[CURRLEVEL] == "" then
        MF_setfile("level", "Data/Temp/temp.ld")
    else
        MF_setfile("level",
            "Data/Worlds/" .. generaldata.strings[WORLD] .. "/" .. generaldata.strings[CURRLEVEL] .. ".ld")
    end
end
if options.level_shuffle ~= 0 then
    auto_gen_level_name_to_id(level_name_to_id)
end