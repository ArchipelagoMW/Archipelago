{% if victory %}
g_victory = True
{% else %}
g_location_guid_data[{{ unlocked_guid }}] = (g_location_guid_data[{{ unlocked_guid }}][0], True)
{% endif %}
