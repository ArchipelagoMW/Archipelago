data:extend({
    {
        type = "bool-setting",
        name = "archipelago-death-link-{{ slot_player }}-{{ seed_name }}",
        setting_type = "runtime-global",
        {% if death_link %}
            default_value = true
        {% else %}
            default_value = false
        {% endif %}
    }
})