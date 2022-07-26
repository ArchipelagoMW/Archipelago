# This module is written by Extractor.py, do not edit manually!.
from functools import partial

def set_generated_rules(hk_world, hk_set_rule):
    player = hk_world.player
    fn = partial(hk_set_rule, hk_world)

    # Events
    {% for location, rule_text in event_rules.items() %}
    fn("{{location}}", lambda state: {{rule_text}})
    {%- endfor %}

    # Locations
    {% for location, rule_text in location_rules.items() %}
    fn("{{location}}", lambda state: {{rule_text}})
    {%- endfor %}

    # Connectors
    {% for entrance, rule_text in connectors_rules.items() %}
    rule = lambda state: {{rule_text}}
    entrance = world.get_entrance("{{entrance}}", player)
    entrance.access_rule = rule
    {%- if entrance not in one_ways %}
    world.get_entrance("{{entrance}}_R", player).access_rule = lambda state, entrance= entrance: \
        rule(state) and entrance.can_reach(state)
    {%- endif %}
    {%- endfor %}