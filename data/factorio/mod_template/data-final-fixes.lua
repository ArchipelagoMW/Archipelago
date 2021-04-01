-- this file gets written automatically by the Archipelago Randomizer and is in its raw form a Jinja2 Template
local technologies = data.raw["technology"]
local original_tech
local new_tree_copy
local template_tech = table.deepcopy(technologies["automation"])
{#-  ensure the copy unlocks nothing #}
template_tech.unlocks = {}
template_tech.upgrade = false
template_tech.effects = {}
{# each randomized tech gets set to be invisible, with new nodes added that trigger those #}
{%- for original_tech_name, item_name, receiving_player in locations %}
original_tech = technologies["{{original_tech_name}}"]
{#- the tech researched by the local player #}
new_tree_copy = table.deepcopy(template_tech)
new_tree_copy.name = "ap-{{ tech_table[original_tech_name] }}-"{# use AP ID #}
{#- hide and disable original tech; which will be shown, unlocked and enabled by AP Client #}
original_tech.enabled = false
{#- copy original tech costs #}
new_tree_copy.unit = table.deepcopy(original_tech.unit)
{% if item_name in tech_table %}
{#- copy Factorio Technology Icon #}
new_tree_copy.icon = table.deepcopy(technologies["{{ item_name }}"].icon)
new_tree_copy.icons = table.deepcopy(technologies["{{ item_name }}"].icons)
new_tree_copy.icon_size = table.deepcopy(technologies["{{ item_name }}"].icon_size)
{% else %}
{#- use default AP icon if no Factorio graphics exist #}
new_tree_copy.icon = "__{{ mod_name }}__/graphics/icons/ap.png"
new_tree_copy.icons = nil
new_tree_copy.icon_size = 512
{% endif %}
{#- add new technology to game #}
data:extend{new_tree_copy}

{% endfor %}