{% from "macros.lua" import dict_to_recipe, dict_to_lua, variable_to_lua %}
-- this file gets written automatically by the Archipelago Randomizer and is in its raw form a Jinja2 Template

local library = require('libs/final-fixes')


local function create_technology(location_data)
    local new_location = table.deepcopy(library.template_tech)
    new_location.name = location_data.name
    new_location.unit.count = location_data.unit.count
    new_location.unit.ingredients = location_data.unit.ingredients
    if location_data.information.revealed then
        new_location.localised_name = {"technology-name.ap-technology-full", location_data.information.player_name, location_data.information.item_name, location_data.location_name}
        if location_data.information.type == "filler" or location_data.information.type == "unknown" then
            new_location.localised_description  = {"technology-description.ap-technology-full",  location_data.information.item_name, location_data.information.player_name, ""}
        else
            new_location.localised_description  = {"technology-description.ap-technology-full",  location_data.information.item_name, location_data.information.player_name, {"technology-description.ap-technology-item-" .. location_data.information.type}}
        end
    else
        new_location.localised_name = {"technology-name.ap-technology-hidden", location_data.location_name}
        if location_data.information.type == "filler" or location_data.information.type == "unknown" then
            new_location.localised_description  = {"technology-description.ap-technology-hidden", ""}
        else
            new_location.localised_description  = {"technology-description.ap-technology-hidden", {"technology-description.ap-technology-item-" .. location_data.information.type}}
        end
    end
    new_location.icons = library.get_icons(location_data.information)
    new_location.prerequisites = location_data.prerequisites
    data:extend({new_location})
end

{%- for location, item in locations %}
{#- the tech researched by the local player #}
create_technology({
    location = {{ location.address }}, --ap location
    name = "ap-{{ location.address }}-", --factorio name
    location_name = "{{location.name}}", --ap name for the location.
    unit = {
        count = {{ location.count }},
        ingredients = {{ variable_to_lua(location.factorio_ingredients) }},
    },
    information = {
        {%- if (location.revealed) -%}
        revealed = true, --if the tech is known.
        --type is 1 of the five types. might be used for making the icons and/or description. "advancement", "useful", "trap", "filler", "unknown"
        type = {% if item.advancement %}"advancement"{% elif item.useful %}"useful"{% elif item.trap %}"trap"{% else %}"filler"{% endif %},
        item_name = "{{ item.name }}", --ap name for the item.
        player_name = "{{ player_names[item.player] }}", --ap name for player who owns the item.
        player_slot = {{ item.player }}, --ap name for player who owns the item.
        {%- else  %}
        revealed = false,
        type = {% if item.advancement and tech_tree_information == 1 %}"advancement"{% elif tech_tree_information == 1 %}"filler"{% else %}"unknown"{% endif %},
        {% endif %}
    },
    prerequisites = {
        {%- if location in tech_tree_layout_prerequisites %}
        {{ variable_to_lua(tech_tree_layout_prerequisites[location]) }}
        {% endif -%}
    },
})
{% endfor %}

