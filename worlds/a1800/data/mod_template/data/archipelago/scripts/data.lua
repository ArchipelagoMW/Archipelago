g_location_guid_data = {
{% for location_guid, (_, unlocked) in location_guid_data.items() %}
    { {{ location_guid }}, {{ unlocked }} },
{% endfor %}
    { {{ victory_condition[3] }}, False },
}