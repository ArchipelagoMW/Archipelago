from . import databases

items_dbview = databases.get_items_dbview()

for item in items_dbview:
    name = databases.get_item_spoiler_name(item)
    if not name.strip():
        continue
    if 'K' in item.flag or 'D' in item.flag:
        continue

    if item.tier == 99:
        tier = '*'
    elif item.tier > 0:
        tier = str(item.tier)
    else:
        tier = '-'

    price = (item.price if item.price > 0 else '-')
    j_exclusive = ('Yes' if item.j else 'No')
    
    notes = []
    if item.shopoverride == 'wild':
        notes.append("not in shops, except in ''Swild''")
    if item.tier == 99:
        notes.append("not in treasure chests, except in ''Twild''")
    note = '; '.join(notes)

    #print(f"| {name} | {tier} | {price} | {j_exclusive} | {note} |")

print()
curves_dbview = databases.get_curves_dbview()

curves = sorted(curves_dbview.find_all(), key=lambda c: c.wikiindex)
for curve in curves:
    parts = [ curve.wikiname ]
    parts.extend([str(getattr(curve, f'tier{i}')) for i in range(1,9)])
    #print('| ' + ' | '.join(parts) + ' |')
