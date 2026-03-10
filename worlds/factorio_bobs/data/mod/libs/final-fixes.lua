
local general = require("Archipelago/general")
local util = require("util")

local library = {}

local technology = data.raw.technology


local progressives
local get_progressives = function()
    if progressives == nil then
        progressives = general.technologies.progressive() or {}
        for name, list in pairs(progressives) do
            for _, entry in pairs(list) do
                if technology[entry] == nil then
                    error(entry .." could not be found. This should be a technology that is present at this point in the loading stage. This was found in the progressive list near "..name)
                end
            end
        end
    end
    return progressives
end

--more icons need to be placed here.
local function get_ap_icon()
    return {
        icon = "__"..general.mod_name.."__/graphics/icons/ap.png",
        icon_size = 128,
        scale = 1
    }
end

local function get_ap_unimportant_icon()
    return {
        icon = "__"..general.mod_name.."__/graphics/icons/ap_unimportant.png",
        icon_size = 128,
        scale = 1
    }
end

--more icons need to be added to this if statement
local function get_icon_from_type(type)
    if type == "advancement" or type == "unkown" then
        return get_ap_icon()
    else
        return get_ap_unimportant_icon()
    end
end

local function set_top_layer(icons, type)
    --if type == "advancement" then
    --    table.insert(icons, get_advancement_arrow()) --this is the up arrow. I placed this code already here to not need to really think about it anymore.
    --end
end

local function get_background(icons, type, this_world)
    if this_world then return end --no background for your own items.
    local pre_icons = get_icon_from_type(type)
    pre_icons.tint = {r=0.7,g=0.7,b=0.7,a=0.7}
    table.insert(icons, pre_icons)
end

local get_icons = function (tech_name)
    --ensure that we are working with a properly made 'icons' of a technology.
    local tech = technology[tech_name]
    local icons = table.deepcopy(tech.icons)
    if icons == nil then
        icons = {{icon = tech.icon, icon_size = tech.icon_size or 64}}
    end
    if icons[1].draw_background == nil then
        icons[1].draw_background = true --ensure that the shadows will be drawn as they would normally be done my default.
    end
    for item, _ in pairs(icons) do
        if icons[item].scale == nil then
            icons[item].scale = (128) / icons[item].icon_size --once again making the default value. because I am doing abnormal things. And the merging does not do this propperly.
        end
    end
    return icons
end

local function get_factorio_icons(icons, item_name, this_world)
    --add factorio icons.
    local tech_sources
    if get_progressives()[item_name] then
        tech_sources = get_progressives()[item_name]
    else
        tech_sources = {item_name}
    end
    local total_amount = table_size(tech_sources)
    if total_amount == 1 then -- or settings.startup["archipelago-progressive-technology-icons"].value == "never" or (this_world == false and settings.startup["archipelago-progressive-technology-icons"].value == "only-own") then
        --only display the first of the list.
        icons = util.combine_icons(icons, get_icons(tech_sources[1]), {}, nil)
        return icons
    end
    local line_size = 1
    while total_amount / line_size > line_size do
        -- this is basically a square root function. I do not need more than this info. So I kept it at this.
        line_size = line_size + 1
    end
    local top_layer = total_amount % line_size --find out how many icons need to be placed on the top layer.
    local full_layers = math.floor(total_amount / line_size) -- find out how many row of icons I have of line_size.
    local all_layers_shift_pre_calc = -0.5 * (full_layers - 1) - 1 --how much higher the start of the full layers needs to be to fit everything. (only full layers. top layer gets take care of later.)
    local icon_pixel_size = 96/line_size --128 is to get the icons to just touch on the sides. 64 is twice as big. 96 is recommended and 1.5 times the size.
    local inputs = {} -- need this to tell the merger of icons how things need to be merged. Only affects the second icons in the function.
    inputs.scale = 1/line_size
    local icon_processing = 0 --the position in the full tech_sources list I am currently processing.
    if top_layer > 0 then
        all_layers_shift_pre_calc = -0.5 * full_layers --change the full layers shift because of this extra layer.
        local vertical_shift = (-0.5 * full_layers) * icon_pixel_size --figure out the current layer.
        for icon_location = 1, top_layer, 1 do
            icon_processing = icon_processing + 1
            local temp_icons = get_icons(tech_sources[icon_processing])
            inputs.shift = {(-0.5 * (top_layer - 1) + icon_location - 1) * icon_pixel_size, vertical_shift}
            icons = util.combine_icons(icons, temp_icons, inputs, nil)
        end
    end
    for line = 1, full_layers, 1 do
        local vertical_shift = (all_layers_shift_pre_calc + line) * icon_pixel_size
        for icon_location = 1, line_size, 1 do
            icon_processing = icon_processing + 1
            local temp_icons = get_icons(tech_sources[icon_processing])
            inputs.shift = {(-0.5 * (line_size - 1) + icon_location - 1) * icon_pixel_size, vertical_shift}
            icons = util.combine_icons(icons, temp_icons, inputs, nil)
        end
    end
    return icons
end

library.get_icons = function(location_information)
    local icons = {}
    if location_information.revealed then
        if technology[location_information.item_name] or get_progressives()[location_information.item_name] then
            --this is an item that will get the factorio treatment.
            get_background(icons, location_information.type, location_information.player_slot == general.slot_id)
            icons = get_factorio_icons(icons, location_information.item_name, location_information.player_slot == general.slot_id)
        else
            icons = {get_icon_from_type(location_information.type)}
        end
    else
        icons = {get_icon_from_type(location_information.type)}
    end
    set_top_layer(icons, location_information.type) --for the advancement arrow and other icons that work from the same category.
    return icons
end

library.template_tech =  { --making one from scratch, ensuring that absolutely nothing can go wrong by other mods doing funky things.
    type = "technology",
    --name = "this-is-required" --this should be getting overwritten at every AP location. if it does not this is a good as any error to notify us.
    unit = {time = 10}, --10 second per research pack.
    --all other values either are default or are overwritten.
}

return library