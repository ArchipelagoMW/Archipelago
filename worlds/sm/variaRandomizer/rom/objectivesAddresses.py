from .addressTypes import ValueList, ValueSingle, ValueRange
# generated from asar output
# A1 start: A1FA80
objectivesAddr = {
    # --- objectives checker functions: A1FA80 ---
    'objectivesList': ValueSingle(0xA1FA80),
    'objectiveEventsArray': ValueRange(0xA1FB1A, length=2*5),
    'objective[kraid_is_dead]': ValueSingle(0xA1FBCE),
    'objective[phantoon_is_dead]': ValueSingle(0xA1FBD6),
    'objective[draygon_is_dead]': ValueSingle(0xA1FBDE),
    'objective[ridley_is_dead]': ValueSingle(0xA1FBE6),
    'objective[all_g4_dead]': ValueSingle(0xA1FBEE),
    'objective[spore_spawn_is_dead]': ValueSingle(0xA1FC04),
    'objective[botwoon_is_dead]': ValueSingle(0xA1FC0C),
    'objective[crocomire_is_dead]': ValueSingle(0xA1FC14),
    'objective[golden_torizo_is_dead]': ValueSingle(0xA1FC1C),
    'objective[all_mini_bosses_dead]': ValueSingle(0xA1FC24),
    'objective[scavenger_hunt_completed]': ValueSingle(0xA1FC3A),
    'objective[boss_1_killed]': ValueSingle(0xA1FC7A),
    'objective[boss_2_killed]': ValueSingle(0xA1FC83),
    'objective[boss_3_killed]': ValueSingle(0xA1FC8C),
    'objective[miniboss_1_killed]': ValueSingle(0xA1FC95),
    'objective[miniboss_2_killed]': ValueSingle(0xA1FC9E),
    'objective[miniboss_3_killed]': ValueSingle(0xA1FCA7),
    'objective[collect_25_items]': ValueSingle(0xA1FCB0),
    '__pct25': 0xA1FCB5,
    'objective[collect_50_items]': ValueSingle(0xA1FCB8),
    '__pct50': 0xA1FCBD,
    'objective[collect_75_items]': ValueSingle(0xA1FCC0),
    '__pct75': 0xA1FCC5,
    'objective[collect_100_items]': ValueSingle(0xA1FCC8),
    '__pct100': 0xA1FCCD,
    'objective[nothing_objective]': ValueSingle(0xA1FCD0),
    'objective[fish_tickled]': ValueSingle(0xA1FCF8),
    'objective[orange_geemer]': ValueSingle(0xA1FD00),
    'objective[shak_dead]': ValueSingle(0xA1FD08),
    'itemsMask': ValueSingle(0xA1FD10),
    'beamsMask': ValueSingle(0xA1FD12),
    'objective[all_major_items]': ValueSingle(0xA1FD14),
    'objective[crateria_cleared]': ValueSingle(0xA1FD2B),
    'objective[green_brin_cleared]': ValueSingle(0xA1FD33),
    'objective[red_brin_cleared]': ValueSingle(0xA1FD3B),
    'objective[ws_cleared]': ValueSingle(0xA1FD43),
    'objective[kraid_cleared]': ValueSingle(0xA1FD4B),
    'objective[upper_norfair_cleared]': ValueSingle(0xA1FD53),
    'objective[croc_cleared]': ValueSingle(0xA1FD5B),
    'objective[lower_norfair_cleared]': ValueSingle(0xA1FD63),
    'objective[west_maridia_cleared]': ValueSingle(0xA1FD6B),
    'objective[east_maridia_cleared]': ValueSingle(0xA1FD73),
    'objective[all_chozo_robots]': ValueSingle(0xA1FD7B),
    'objective[visited_animals]': ValueSingle(0xA1FD9A),
    'objective[king_cac_dead]': ValueSingle(0xA1FDE6),
    # A1 end: A1FDEE
    # Pause stuff: 82FB6D
    # *** completed spritemaps: 82FE83
    'objectivesSpritesOAM': ValueSingle(0x82FE83),
    # 82 end: 82FEB0
    'objectivesText': ValueSingle(0xB6F200),
}
_pctList = []
for pct in [25,50,75,100]:
    _pctList.append(objectivesAddr['__pct%d' % pct])
    del objectivesAddr['__pct%d' % pct]
objectivesAddr['totalItemsPercent'] = ValueList(_pctList)
