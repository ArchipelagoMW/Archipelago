def link_psychonauts2_entrances(world, player):

    # Link mandatory connections
    for (exit, region) in mandatory_connections:
        world.get_entrance(exit, player).connect(world.get_region(region, player))

    

# (Region name, list of exits)
psychonauts2_regions = [
    ('Menu', ['Begin Motherlobe']),

    # Overworld
    ('The Motherlobe', ['To CU', 'To Quarry', 'Enter Helmut', 'Enter Ford Mail', 'Enter Ford Bowling', 'Enter Ford Haircut']),
    ('The Quarry', ['To Motherlobe', 'To QA', 'Enter Compton']),
    ('The Questionable Area', ['To Quarry', 'To Gulch']),
    ('Green Needle Gulch', ['To CU', 'To QA', 'Enter Cassie', 'Enter Bob', 'Enter Lucrecia', 'Enter Gristol']),

    # Minds
    ('Collective Unconscious', ['Motherlobe Tumbler', 'Gulch Tumbler', 'Enter Loboto', 'Enter Hollis 1', 'Enter Hollis 2', 'Enter Helmut', 'Enter Compton', 'Enter Ford Mail', 'Enter Ford Bowling', 'Enter Ford Haircut', 'Enter Ford Tomb', 'Enter Cassie', 'Enter Bob', 'Enter Lucrecia', 'Enter Gristol']),

    # Loboto's Labyrinth
    ('Loboto Start', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Loboto Central Office']),
    ('Loboto Central Office', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Loboto Conference Room', 'To Loboto Poster Gallery', 'To Loboto Dental Void']),
    ('Loboto Conference Room', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Loboto Central Office']),
    ('Loboto Poster Gallery', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Loboto Central Office']),
    ('Loboto Dental Void', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Loboto Asylum']),
    ('Loboto Asylum', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'End Loboto']),

    # Hollis' Classroom
    ('Hollis Class Start', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Hollis 1 Parking Lot']),
    ('Hollis Class Parking Lot', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Hollis 1 Morgue']),
    ('Hollis Class Morgue', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Hollis 1 Final']),
    ('Hollis Class Final', ['End Hollis 1']),

    # Hollis' Hot Streak
    ('Hollis Casino Start',  ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Hollis 2 Parking Lot']),
    ('Hollis Casino Parking Lot', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Hollis 2 Morgue']),
    ('Hollis Casino Morgue', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Hollis 2 Maternity', 'To Hollis 2 Pharmacy', 'To Hollis 2 Cardiology', 'To Hollis 2 Records', 'To Hollis 2 Doctors Only', 'To Hollis 2 Boss']),
    ('Hollis Casino Maternity', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Hollis 2 Morgue', 'To Hollis 2 Maternity Back']),
    ('Hollis Casino Maternity Back', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Hollis 2 Morgue']),
    ('Hollis Casino Pharmacy', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Hollis 2 Morgue', 'To Hollis 2 Pharmacy Back']),
    ('Hollis Casino Pharmacy Back', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Hollis 2 Morgue']),
    ('Hollis Casino Cardiology', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Hollis 2 Morgue', 'To Hollis 2 Cardiology Back']),
    ('Hollis Casino Cardiology Back', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Hollis 2 Morgue']),
    ('Hollis Casino Records', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Hollis 2 Morgue']),
    ('Hollis Casino Doctors Only', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Hollis 2 Morgue']),
    ('Hollis Casino Boss', ['End Hollis 2']),

    # PSI King's Sensorium
    ('PSI King Backstage', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Motherlobe', 'To PSI King Eye Shrine', 'To PSI King Concessions', 'To PSI King Campgrounds', 'To PSI King End']),
    ('PSI King Eye Shrine', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Motherlobe', 'To PSI King Backstage']),
    ('PSI King Concessions', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Motherlobe', 'To PSI King Backstage', 'To PSI King Nose Mouth Shrine']),
    ('PSI King Nose Mouth Shrine', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Motherlobe', 'To PSI King Backstage']),
    ('PSI King Campgrounds', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Motherlobe', 'To PSI King Backstage', 'To PSI King Hand Ear Shrine']),
    ('PSI King Hand Ear Shrine', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Motherlobe', 'To PSI King Backstage']),
    ('PSI King End', ['End Helmut']),

    # Compton's Cookoff
    ('Compton Judge', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Quarry', 'To Compton Round 1']),
    ('Compton Round 1', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Quarry', 'To Compton Break 1']),
    ('Compton Break 1', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Quarry', 'To Compton Round 2']),
    ('Compton Round 2', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Quarry', 'To Compton Break 2']),
    ('Compton Break 2', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Quarry', 'To Compton Round 3']),
    ('Compton Round 3', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Quarry', 'To Compton Boss']),
    ('Compton Boss', ['End Compton']),

    # Cruller's Correspondence
    ('Ford Mail Dead Letter Office', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Motherlobe', 'To Ford Mail Typewriter']),
    ('Ford Mail Typewriter', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Motherlobe', 'To Ford Mail Bot Interior']),
    ('Ford Mail Bot Interior', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Motherlobe', 'To Ford Mail International Dead Letter Office']),
    ('Ford Mail International Dead Letter Office', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Motherlobe', 'To Ford Mail Above Typewriter']),
    ('Ford Mail Above Typewriter', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Motherlobe', 'To Ford Mail Typewriter', 'End Ford Mail', 'Enter Ford Tomb']),

    # Strike City
    ('Ford Bowling Alley Interior', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Motherlobe', 'To Ford Bowling Downtown Center']),
    ('Ford Bowling Downtown Center', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Motherlobe', 'To Ford Bowling Kingpin Express']),
    ('Ford Bowling Kingpin Express', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Motherlobe', 'To Ford Bowling Foul Line']),
    ('Ford Bowling Foul Line', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Motherlobe', 'To Ford Bowling Construction']),
    ('Ford Bowling Construction', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Motherlobe', 'End Ford Bowling', 'Enter Ford Tomb']),

    # Ford's Follicles
    ('Ford Haircut Waiting Area', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Motherlobe', 'To Ford Haircut Willmill']),
    ('Ford Haircut Willmill', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Motherlobe', 'To Ford Haircut Town']),
    ('Ford Haircut Town', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Motherlobe', 'To Ford Haircut Lighthouse']),
    ('Ford Haircut Lighthouse', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Motherlobe', 'End Ford Haircut', 'Enter Ford Tomb']),

    # Tomb of the Sharkophagus
    ('Ford Tomb Graveyard', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Ford Tomb Tomb']),
    ('Ford Tomb Tomb', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Ford Tomb Coffin']),
    ('Ford Tomb Coffin', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'End Ford Tomb']),

    # Cassie's Collection
    ('Cassie Librarian Desk', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Gulch', 'To Cassie Teacher Domain', 'To Cassie Waterfront']),
    ('Cassie Teacher Domain', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Gulch', 'To Cassie Deep Teacher Domain']),
    ('Cassie Deep Teacher Domain', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Gulch', 'To Cassie Librarian Desk']),
    ('Cassie Waterfront', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Gulch', 'To Cassie Boss']),
    ('Cassie Boss', ['End Cassie']),

    # Bob's Bottles
    ('Bob Island', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Gulch', 'To Bob Kitchen', 'To Bob Ship In Bottle', 'To Bob Bog']),
    ('Bob Kitchen', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Gulch', 'To Bob Island']),
    ('Bob Ship In Bottle', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Gulch', 'To Bob Sunken Motherlobe']),
    ('Bob Sunken Motherlobe', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Gulch', 'To Bob Island']),
    ('Bob Bog', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Gulch', 'To Bob Reception']),
    ('Bob Reception', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Gulch', 'To Bob Cake']),
    ('Bob Cake', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Gulch', 'To Bob Boss']),
    ('Bob Boss', ['End Bob']),

    # Lucrecia's Lament
    ('Lucrecia Circus', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Lucrecia Quilts 1']),
    ('Lucrecia Quilts 1', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Lucrecia Quilts 2']),
    ('Lucrecia Quilts 2', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Lucrecia Quilts 3']),
    ('Lucrecia Quilts 3', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Lucrecia Dam']),
    ('Lucrecia Dam', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'End Lucrecia']),

    # Fatherland Follies
    ('Gristol Dressing Room', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Gristol Entrance']),
    ('Gristol Entrance', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Gristol Grulovia']),
    ('Gristol Grulovia', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Gristol Exile']),
    ('Gristol Exile', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Gristol Infiltration']),
    ('Gristol Infiltration', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'To Gristol Gift Shop']),
    ('Gristol Gift Shop', ['Motherlobe Tumbler', 'Gulch Tumbler', 'To CU', 'End Gristol']),

    # Maligula
    ('Maligula Ruins', ['To Maligula Boss']),
    ('Maligula Boss', ['End Maligula']),

]


# (Entrance, region pointed to)
mandatory_connections = [
    ('Begin Motherlobe', 'The Motherlobe'),

    # Overworld
    ('To Motherlobe', 'The Motherlobe'),
    ('To Quarry', 'The Quarry'),
    ('To QA', 'The Questionable Area'),
    ('To Gulch', 'Green Needle Gulch'),

    # Minds
    ('To CU', 'Collective Unconscious'),
    ('Motherlobe Tumbler', 'The Motherlobe'),
    ('Gulch Tumbler', 'Green Needle Gulch'),

    # Loboto's Labyrinth
    ('Enter Loboto', 'Loboto Start'),
    ('To Loboto Central Office', 'Loboto Central Office'),
    ('To Loboto Conference Room', 'Loboto Conference Room'),
    ('To Loboto Poster Gallery', 'Loboto Poster Gallery'),
    ('To Loboto Dental Void', 'Loboto Dental Void'),
    ('To Loboto Asylum', 'Loboto Asylum'),
    ('End Loboto', 'The Motherlobe'),

    # Hollis' Classroom
    ('Enter Hollis 1', 'Hollis Class Start'),
    ('To Hollis 1 Parking Lot', 'Hollis Class Parking Lot'),
    ('To Hollis 1 Morgue', 'Hollis Class Morgue'),
    ('To Hollis 1 Final', 'Hollis Class Final'),
    ('End Hollis 1', 'The Motherlobe'),

    # Hollis' Hot Streak
    ('Enter Hollis 2', 'Hollis Casino Start'),
    ('To Hollis 2 Parking Lot', 'Hollis Casino Parking Lot'),
    ('To Hollis 2 Morgue', 'Hollis Casino Morgue'),
    ('To Hollis 2 Maternity', 'Hollis Casino Maternity'),
    ('To Hollis 2 Maternity Back', 'Hollis Casino Maternity Back'),
    ('To Hollis 2 Pharmacy', 'Hollis Casino Pharmacy'),
    ('To Hollis 2 Pharmacy Back', 'Hollis Casino Pharmacy Back'),
    ('To Hollis 2 Cardiology', 'Hollis Casino Cardiology'),
    ('To Hollis 2 Cardiology Back', 'Hollis Casino Cardiology Back'),
    ('To Hollis 2 Records', 'Hollis Casino Records'),
    ('To Hollis 2 Doctors Only', 'Hollis Casino Doctors Only'),
    ('To Hollis 2 Boss', 'Hollis Casino Boss'),
    ('End Hollis 2', 'The Motherlobe'),

    # PSI King's Sensorium
    ('Enter Helmut', 'PSI King Backstage'),
    ('To PSI King Eye Shrine', 'PSI King Eye Shrine'),
    ('To PSI King Backstage', 'PSI King Backstage'),
    ('To PSI King Concessions', 'PSI King Concessions'),
    ('To PSI King Nose Mouth Shrine', 'PSI King Nose Mouth Shrine'),
    ('To PSI King Campgrounds', 'PSI King Campgrounds'),
    ('To PSI King Hand Ear Shrine', 'PSI King Hand Ear Shrine'),
    ('To PSI King End', 'PSI King End'),
    ('End Helmut', 'The Motherlobe'),

    # Compton's Cookoff
    ('Enter Compton', 'Compton Judge'),
    ('To Compton Round 1', 'Compton Round 1'),
    ('To Compton Break 1', 'Compton Break 1'),
    ('To Compton Round 2', 'Compton Round 2'),
    ('To Compton Break 2', 'Compton Break 1'),
    ('To Compton Round 3', 'Compton Round 3'),
    ('To Compton Boss', 'Compton Boss'),
    ('End Compton', 'The Quarry'),

    # Cruller's Correspondence
    ('Enter Ford Mail', 'Ford Mail Dead Letter Office'),
    ('To Ford Mail Typewriter', 'Ford Mail Typewriter'),
    ('To Ford Mail Bot Interior', 'Ford Mail Bot Interior'),
    ('To Ford Mail International Dead Letter Office', 'Ford Mail International Dead Letter Office'),
    ('To Ford Mail Above Typewriter', 'Ford Mail Above Typewriter'),
    ('End Ford Mail', 'The Motherlobe'),

    # Strike City
    ('Enter Ford Bowling', 'Ford Bowling Alley Interior'),
    ('To Ford Bowling Downtown Center', 'Ford Bowling Downtown Center'),
    ('To Ford Bowling Kingpin Express', 'Ford Bowling Kingpin Express'),
    ('To Ford Bowling Foul Line', 'Ford Bowling Foul Line'),
    ('To Ford Bowling Construction', 'Ford Bowling Construction'),
    ('End Ford Bowling', 'The Motherlobe'),

    # Ford's Follicles
    ('Enter Ford Haircut', 'Ford Haircut Waiting Area'),
    ('To Ford Haircut Willmill', 'Ford Haircut Willmill'),
    ('To Ford Haircut Town', 'Ford Haircut Town'),
    ('To Ford Haircut Lighthouse', 'Ford Haircut Lighthouse'),
    ('End Ford Haircut', 'The Motherlobe'),

    # Tomb of the Sharkophagus
    ('Enter Ford Tomb', 'Ford Tomb Graveyard'),
    ('To Ford Tomb Tomb', 'Ford Tomb Tomb'),
    ('To Ford Tomb Coffin', 'Ford Tomb Coffin'),
    ('End Ford Tomb', 'Green Needle Gulch'),

    # Cassie's Collection
    ('Enter Cassie', 'Cassie Librarian Desk'),
    ('To Cassie Teacher Domain', 'Cassie Teacher Domain'),
    ('To Cassie Deep Teacher Domain', 'Cassie Deep Teacher Domain'),
    ('To Cassie Librarian Desk', 'Cassie Librarian Desk'),
    ('To Cassie Waterfront', 'Cassie Waterfront'),
    ('To Cassie Boss', 'Cassie Boss'),
    ('End Cassie', 'Green Needle Gulch'),

    # Bob's Bottles
    ('Enter Bob', 'Bob Island'),
    ('To Bob Island', 'Bob Island'),
    ('To Bob Kitchen', 'Bob Kitchen'),
    ('To Bob Ship In Bottle', 'Bob Ship In Bottle'),
    ('To Bob Sunken Motherlobe', 'Bob Sunken Motherlobe'),
    ('To Bob Bog', 'Bob Bog'),
    ('To Bob Reception', 'Bob Reception'),
    ('To Bob Cake', 'Bob Cake'),
    ('To Bob Boss', 'Bob Boss'),
    ('End Bob', 'Green Needle Gulch'),

    # Lucrecia's Lament
    ('Enter Lucrecia', 'Lucrecia Circus'),
    ('To Lucrecia Quilts 1', 'Lucrecia Quilts 1'),
    ('To Lucrecia Quilts 2', 'Lucrecia Quilts 2'),
    ('To Lucrecia Quilts 3', 'Lucrecia Quilts 3'),
    ('To Lucrecia Dam', 'Lucrecia Dam'),
    ('End Lucrecia', 'Gristol Dressing Room'),

    # Fatherland Follies
    ('Enter Gristol', 'Gristol Dressing Room'),
    ('To Gristol Entrance', 'Gristol Entrance'),
    ('To Gristol Grulovia', 'Gristol Grulovia'),
    ('To Gristol Exile', 'Gristol Exile'),
    ('To Gristol Infiltration', 'Gristol Infiltration'),
    ('To Gristol Gift Shop', 'Gristol Gift Shop'),
    ('End Gristol', 'Maligula Ruins'),

    # Maligula
    ('To Maligula Boss', 'Maligula Boss'),
    ('End Maligula', 'The Quarry'),
]

default_connections = [
    
]