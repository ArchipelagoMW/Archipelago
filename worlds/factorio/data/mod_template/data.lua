{% from "macros.lua" import dict_to_lua %}
data.raw["map-gen-presets"].default["archipelago"] = {{ dict_to_lua({"default": False, "order": "a", "basic_settings": world_gen["basic"], "advanced_settings": world_gen["advanced"]}) }}
if mods["science-not-invited"] then
    local weights = {
        ["automation-science-pack"] =   0, -- Red science
        ["logistic-science-pack"]   =   0, -- Green science
        ["military-science-pack"]   =   0, -- Black science
        ["chemical-science-pack"]   =   0, -- Blue science
        ["production-science-pack"] =   0, -- Purple science
        ["utility-science-pack"]    =   0, -- Yellow science
        ["space-science-pack"]      =   0  -- Space science
    }
{% if max_science_pack == 6 -%}
    weights["space-science-pack"] = 1
{%- endif %}
{% for key in allowed_science_packs -%}
    weights["{{key}}"] = 1
{% endfor %}
    SNI.setWeights(weights)
end
