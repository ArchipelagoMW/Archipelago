from worlds.ff4fe.FreeEnterpriseForAP.FreeEnt.generate_wiki_tables import items_dbview
from . import core_rando
from .crosspolinate import crosspolinate
from . import databases
from .address import *
from . import rewards
from . import util
from . import spoilers

FIGHT_SPOILER_DESCRIPTIONS = {
    0x1C0 : "Staleman/Skulls",
    0x1C1 : "BlackCats/Lamia",
    0x1C2 : "Mad Ogre x3",
    0x1C3 : "FlameDog",
    0x1C4 : "Mad Ogre x4",
    0x1C5 : "Green D.",
    0x1C6 : "Staleman x2",
    0x1C7 : "Last Arm",
    0x1E0 : "Alert (Chimera)",
    0x1E1 : "Alert (Stoneman)",
    0x1E2 : "Alert (Naga)",
    0x1E3 : "Alert (FlameDog)",
    0x1E4 : "Warrior x5",
    0x1E5 : "ToadLady/TinyToads",
    0x1E6 : "Ghost x6",
    0x1E7 : "DarkTrees/Molbols",
    0x1E8 : "Molbol x2",
    0x1E9 : "Centpede x2",
    0x1EA : "Procyotes/Juclyotes",
    0x1EB : "RedGiant x2",
    0x1EC : "Warlock x2/Kary x2",
    0x1ED : "Warlock/Kary x3",
    0x1EE : "Red D./Blue D.",
    0x1EF : "Blue D. x2",
    0x1F0 : "Behemoth",
    0x1F1 : "Red D. x2",
    0x1F2 : "D.Fossil/Warlock",
    0x1F3 : "Behemoth",
    0x1F4 : "Behemoth"
}

def _round_gp(amount):
    if amount < 1280:
        return int(amount / 10) * 10
    else:
        return int(min(127000, amount) / 1000) * 1000

def _slug(treasure):
    if type(treasure) is str:
        return treasure
    else:
        return f"{treasure.map} {treasure.index}"

class TreasureAssignment:
    def __init__(self, autosells):
        self._autosells = autosells
        self._assignments = {}
        self._remaps = {}

    def remap(self, old, new):
        self._remaps[_slug(old)] = _slug(new)

    def assign(self, t, contents, fight=None, remap=True):
        slug = _slug(t)
        if remap and slug in self._remaps:
            slug = self._remaps[slug]

        if contents in self._autosells and fight is None:
            contents = '{} gp'.format(self._autosells[contents])
        self._assignments[slug] = (contents, fight)

    def get(self, t, remap=True):
        slug = _slug(t)
        if remap and slug in self._remaps:
            slug = self._remaps[slug]

        return self._assignments.get(slug, (None, None))

    def get_script(self):
        lines = []
        for slug in self._assignments:
            contents,fight = self._assignments[slug]
            if contents is None:
                contents = '$00'
            line = f"trigger({slug}) {{ treasure {contents} "
            if fight is not None:
                if fight >= 0x1E0:
                    fight -= 0x1E0
                else:
                    fight -= 0x1C0
                line += f"fight ${fight:02X} "
            line += "}"
            lines.append(line)
        return '\n'.join(lines)

def apply(env):
    treasure_dbview = databases.get_treasure_dbview()
    treasure_dbview.refine(lambda t: not t.exclude)
    plain_chests_dbview = treasure_dbview.get_refined_view(lambda t: t.fight is None)

    items_dbview = databases.get_items_dbview()
    #items_dbview.refine(lambda it: it.tier > 0)
    #if env.options.flags.has('treasure_no_j_items'):
    #    items_dbview.refine(lambda it: not it.j)
    #if env.options.flags.has('no_adamants'):
    #    items_dbview.refine(lambda it: it.const != '#item.AdamantArmor')
    #if env.options.flags.has('no_cursed_rings'):
    #    items_dbview.refine(lambda it: it.const != '#item.Cursed')

    maxtier = env.options.flags.get_suffix('Tmaxtier:')
    if maxtier:
        maxtier = int(maxtier)
        items_dbview.refine(lambda it: it.tier <= maxtier)

    if env.meta.get('wacky_challenge') == 'kleptomania':
        items_dbview.refine(lambda it: (it.category not in ['weapon', 'armor']))

    autosells = {}
    if env.options.flags.has('treasure_money'):
        autosell_items = items_dbview.find_all()
    elif not env.options.flags.has_any('treasure_vanilla', 'treasure_shuffle', 'treasure_junk'):
        autosell_items = items_dbview.find_all(lambda it: it.tier == 1)
    else:
        autosell_items = []

    for item in autosell_items:
        if env.options.flags.has('shops_sell_zero'):
            autosells[item.const] = 0
        else:
            multiplier = (10 if item.subtype == 'arrow' else 1)
            divisor = (4 if env.options.flags.has('shops_sell_quarter') else 2)
            autosells[item.const] = max(10, _round_gp(int(item.price * multiplier / divisor)))

    treasure_assignment = TreasureAssignment(autosells)

    if env.options.ap_data is not None:
        treasure_table_start = 0x1A0000
        for t in treasure_dbview:
            id = t.flag
            ap_item = env.options.ap_data[str(id)]
            placement = items_dbview.find_one(lambda i: i.code == ap_item["item_data"]["fe_id"])
            if placement is None:
                treasure_assignment.assign(t, "#item.Cure1")
            elif placement.tier <= env.options.ap_data["junk_tier"] and placement.flag != "K":
                multiplier = (10 if placement.subtype == 'arrow' else 1)
                divisor = (4 if env.options.flags.has('shops_sell_quarter') else 2)
                price = max(10, _round_gp(int(placement.price * multiplier / divisor)))
                treasure_assignment.assign(t, '{} gp'.format(price))
            else:
                treasure_assignment.assign(t, placement.const)
            script_text = env.meta["text_pointers"].pop()
            bank = int(script_text[10], 16)
            pointer = script_text[20:24]
            pointer = pointer[1:] if pointer[3] != ")" else pointer[1:3]
            pointer = int(pointer, 16)
            entry_location = treasure_table_start + (id * 3)
            entry_location = f"${hex(entry_location)[2:]}"
            high_byte = pointer % 256
            low_byte = pointer // 256
            env.add_script(f"patch({entry_location}) {{ {bank:X} {high_byte:02X} {low_byte:02X} }}")
            env.add_script(f'{script_text} {{Found {ap_item["player_name"]}\'s \n{ap_item["item_name"]}. }}')

    fight_chest_locations = ['{} {}'.format(*env.meta['miab_locations'][slot]) for slot in env.meta['miab_locations']]
    fight_treasure_areas = list(set([t.area for t in treasure_dbview.find_all(lambda t: t.fight is not None)]))
    for area in fight_treasure_areas:
        # find the differences between the lists of:
        #  - chest locations that were originally not MIABs
        #  - chest locations that are now not MIABs
        # 
        treasures = treasure_dbview.find_all(lambda t: t.area == area)
        original_chests = [_slug(t) for t in treasures if t.fight is None]
        new_chests = [_slug(t) for t in treasures if _slug(t) not in fight_chest_locations]
        remapped_original_chests = sorted(set(original_chests) - set(new_chests))
        remapped_new_chests = sorted(set(new_chests) - set(original_chests))
        if len(remapped_original_chests) != len(remapped_new_chests):
            print('---')
            print('\n'.join(original_chests))
            print('---')
            print('\n'.join(new_chests))
            print('---')
            print('\n'.join(remapped_original_chests))
            print('---')
            print('\n'.join(remapped_new_chests))
            print('---')
            raise Exception("Ok things are fuckered")
        for old,new in zip(remapped_original_chests, remapped_new_chests):
            treasure_assignment.remap(old, new)

    if env.options.ap_data is not None:
        pass
    elif env.options.flags.has('treasure_vanilla'):
        # for various reasons we really do need to assign every treasure chest still
        for t in treasure_dbview:
            if t.fight is None:
                contents = (t.jcontents if (t.jcontents and not env.options.flags.has('treasure_no_j_items')) else t.contents)
                treasure_assignment.assign(t, contents)
    elif env.options.flags.has('treasure_empty'):
        # all treasures contain nothing
        for t in treasure_dbview:
            treasure_assignment.assign(t, None)
    elif env.options.flags.has('treasure_shuffle'):
        tiers = []

        # split into two tiers
        src_tiers = [
            plain_chests_dbview.find_all(lambda t: t.world == 'Overworld'),
            plain_chests_dbview.find_all(lambda t: t.world != 'Overworld')
            ]

        for src_tier in src_tiers:
            tier = {'chests' : [], 'pool' : []}
            for t in src_tier:
                tier['chests'].append(t)
                tier['pool'].append(t.jcontents if (t.jcontents and not env.options.flags.has('treasure_no_j_items')) else t.contents)
            tiers.append(tier)

        if len(tiers) > 1:
            # crosspolinate the two pools
            crosspolinated_pools = crosspolinate(tiers[0]['pool'], tiers[1]['pool'], 0.5, 0.5, env.rnd)
            tiers[0]['pool'] = crosspolinated_pools[0]
            tiers[1]['pool'] = crosspolinated_pools[1]

        for tier in tiers:
            env.rnd.shuffle(tier['pool'])
            for i,t in enumerate(tier['chests']):
                treasure_assignment.assign(t, tier['pool'][i])
    elif env.options.flags.has('treasure_wild') or env.options.flags.has('treasure_standard'):
        max_item_tier = (99 if env.options.flags.has('treasure_wild') else 5)
        item_pool = items_dbview.get_refined_view(lambda it: it.tier <= max_item_tier).find_all()
        for t in plain_chests_dbview.find_all():
            treasure_assignment.assign(t, env.rnd.choice(item_pool).const)
    else:
        # revised rivers rando
        items_by_tier = {}
        for item in items_dbview:
            items_by_tier.setdefault(item.tier, []).append(item.const)

        distributions = {}
        for row in databases.get_curves_dbview():
            weights = {i : getattr(row, f"tier{i}") for i in range(1,9)}
            if env.options.flags.has('treasure_wild_weighted'):
                weights = util.get_boosted_weights(weights)

            # null out distributions for empty item tiers
            for i in range(1,9):
                if not items_by_tier.get(i, None):
                    weights[i] = 0

            distributions[row.area] = util.Distribution(weights)

        for t in plain_chests_dbview.find_all():
            tier = min(8, distributions[t.area].choose(env.rnd))
            treasure_assignment.assign(t, env.rnd.choice(items_by_tier[tier]))

    # apply sparsity
    sparse_level = env.options.flags.get_suffix('Tsparse:')
    if sparse_level:
        sparse_level = int(sparse_level)
        plain_chests = plain_chests_dbview.find_all()
        empty_count = (len(plain_chests) * (100 - sparse_level)) // 100
        for t in env.rnd.sample(plain_chests, empty_count):
            treasure_assignment.assign(t, None)

    # apply passes if Pt flag
    if env.options.flags.has('pass_in_chests'):
        remaining_chests = plain_chests_dbview.get_refined_view(lambda t: t.world != 'Moon')

        pass_chest = env.rnd.choice(remaining_chests.find_all())
        treasure_assignment.assign(pass_chest, '#item.Pass')
        remaining_chests.refine(lambda t: t.world != 'Overworld' and t.area != pass_chest.area)
        pass_chest = env.rnd.choice(remaining_chests.find_all())
        treasure_assignment.assign(pass_chest, '#item.Pass')
        remaining_chests.refine(lambda t: t.area != pass_chest.area)
        pass_chest = env.rnd.choice(remaining_chests.find_all())
        treasure_assignment.assign(pass_chest, '#item.Pass')

    # apply required objective treasures
    if env.meta['required_treasures']:
        area_use_count = {}
        remaining_chests = []
        for t in plain_chests_dbview.find_all():
            contents,fight = treasure_assignment.get(t)
            if contents != '#item.Pass':
                remaining_chests.append(t)
                area_use_count[t.area] = 0


    # map the fight treasures to the rewards table
    for chest_slot in core_rando.CHEST_ITEM_SLOTS:
        chest_number = env.meta['miab_locations'][chest_slot]
        orig_chest_number = core_rando.CHEST_NUMBERS[chest_slot]
        reward_slot_name =  f'#reward_slot.{chest_slot.name}'
        orig_chest = treasure_dbview.find_one(lambda t: t.map == orig_chest_number[0] and t.index == orig_chest_number[1])
        new_chest = treasure_dbview.find_one(lambda t: t.map == chest_number[0] and t.index == chest_number[1])
        id = new_chest.flag
        ap_item = env.options.ap_data[str(id)]
        placement = items_dbview.find_one(lambda i: i.code == ap_item["item_data"]["fe_id"])
        if placement is None:
            env.assignments[reward_slot_name] = "#item.Cure1"
        else:
            env.assignments[reward_slot_name] = placement.const
        treasure_assignment.assign(
            '{} {}'.format(chest_number[0], chest_number[1]),
            reward_slot_name,
            orig_chest.fight,
            remap=False)

    env.add_script(treasure_assignment.get_script())

    # write the pre-opened chest values
    chest_init_flags = [0x00] * 0x40
    empty_count = 0
    for t in treasure_dbview.find_all():
        contents,fight = treasure_assignment.get(t, remap=False)
        if contents is None:
            byte_index = t.flag >> 3
            bit_index = t.flag & 0x7
            chest_init_flags[byte_index] |= (1 << bit_index)
            empty_count += 1
    env.add_binary(BusAddress(0x21d9a0), chest_init_flags, as_script=True)

    nonempty_count = 399 - empty_count
    env.add_binary(BusAddress(0x21f0fa), [nonempty_count & 0xFF, (nonempty_count >> 8)], as_script=True)

    # generate spoilers
    treasure_spoilers = []
    treasure_spoiler_order = sorted(treasure_dbview.find_all(), key=lambda t: (t.spoilerarea, t.spoilersubarea))
    all_treasure_public = env.options.flags.has_any('-spoil:all', '-spoil:treasure')
    miabs_public = all_treasure_public or env.options.flags.has('-spoil:miabs')
    for t in treasure_spoiler_order:
        contents,fight = treasure_assignment.get(t, remap=False)
        if contents is None:
            contents = "  (nothing)"
        elif contents.startswith('#reward_slot.'):
            slot = rewards.RewardSlot[contents[len('#reward_slot.'):]]
            try:
                item = env.meta['rewards_assignment'][slot].item
                contents = databases.get_item_spoiler_name(item)
            except KeyError:
                contents = 'DEBUG'
        elif not contents.endswith(' gp'):
            contents = databases.get_item_spoiler_name(contents)

        if fight is not None:
            miab = f" (MIAB: {FIGHT_SPOILER_DESCRIPTIONS[fight]})"
            treasure_spoilers.append( spoilers.SpoilerRow(
                t.spoilerarea, contents, f"{t.spoilersubarea} - {t.spoilerdetail}", miab, 
                public = miabs_public,
                obscurable=True,
                obscure_mask=("NYN!" if all_treasure_public else "NYNY")
                ) )
        else:
            treasure_spoilers.append( spoilers.SpoilerRow(
                t.spoilerarea, contents, f"{t.spoilersubarea} - {t.spoilerdetail}", 
                public = all_treasure_public,
                obscurable=True,
                obscure_mask="NYN"
                ) )

    env.spoilers.add_table("TREASURE", treasure_spoilers, public=(all_treasure_public or miabs_public), ditto_depth=1)


if __name__ == '__main__':
    import FreeEnt
    import random
    import argparse

    parser = argparse.ArgumentParser();
    parser.add_argument('flags', nargs='?')
    args = parser.parse_args();

    options = FreeEnt.FreeEntOptions()
    options.flags.load(args.flags if args.flags else 'Tpro')

    env = FreeEnt.Environment(options)
    env.meta['miab_locations'] = {}
    env.meta['required_treasures'] = {}
    env.meta['rewards_assignment'] = rewards.RewardsAssignment()
    if options.flags.has('objective_mode_dkmatter'):
        env.meta['required_treasures']['#item.DkMatter'] = 12

    for slot in core_rando.CHEST_NUMBERS:
        env.meta['miab_locations'][slot] = core_rando.CHEST_NUMBERS[slot]
        env.assignments[slot] = ''

    apply(env)
    print(env.scripts[0])

