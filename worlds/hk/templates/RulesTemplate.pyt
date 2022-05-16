from ..generic.Rules import set_rule, add_rule

units = {
    "Egg": "RANCIDEGGS",
    "Grub": "GRUBS",
    "Essence": "ESSENCE",
    "Charm": "CHARMS",
}


def hk_set_rule(hk_world, location: str, rule):
    count = hk_world.created_multi_locations[location]
    if count:
        locations = [f"{location}_{x}" for x in range(1, count+1)]
    elif (location, hk_world.player) in hk_world.world._location_cache:
        locations = [location]
    else:
        return
    for location in locations:
        set_rule(hk_world.world.get_location(location, hk_world.player), rule)


def set_shop_prices(hk_world):
    player = hk_world.player
    for shop, unit in hk_world.shops.items():
        for i in range(1, 1 + hk_world.created_multi_locations[shop]):
            loc = hk_world.world.get_location(f"{shop}_{i}", hk_world.player)
            add_rule(loc, lambda state, unit=units[unit], cost=loc.cost: state.count(unit, player) > cost)


def set_rules(hk_world):
    player = hk_world.player
    world = hk_world.world

    # Events
    {% for location, rule_text in event_rules.items() %}
    hk_set_rule(hk_world, "{{location}}", lambda state: {{rule_text}})
    {%- endfor %}

    # Locations
    {% for location, rule_text in location_rules.items() %}
    hk_set_rule(hk_world, "{{location}}", lambda state: {{rule_text}})
    {%- endfor %}

    # Shop prices
    set_shop_prices(hk_world)

    # Connectors
    {% for entrance, rule_text in connectors_rules.items() %}
    rule = lambda state: {{rule_text}}
    entrance = world.get_entrance("{{entrance}}", player)
    entrance.access_rule = rule
    {%- if entrance not in one_ways %}
    world.get_entrance("{{entrance}}_R", player).access_rule = lambda state, entrance= entrance: \
        rule(state) and entrance.can_reach(state)
    {%- endif %}
    {% endfor %}