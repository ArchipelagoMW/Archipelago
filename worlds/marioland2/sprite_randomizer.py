# Based on SML2R enemy and platform randomizer
# # https://github.com/slashinfty/sml2r-node/blob/862128c73d336d6cbfbf6290c09f3eff103688e8/src/index.ts#L284

def randomize_enemies(sprite_data, random):
    for level, level_sprite_data in sprite_data.items():
        shuffle = ()
        if level in ("Mushroom Zone", "Macro Zone 4"):
            shuffle = ("Koopa Troopa", "Goomba", "Paragoomba (Vertical)", "Paragoomba (Diagonal)")
        elif level in ("Scenic Course", "Pumpkin Zone Secret Course 1"):
            shuffle = ("Goomba", "Paragoomba (Vertical)", "Paragoomba (Diagonal)")
        elif level == "Tree Zone 1":
            shuffle = ("Money Bag/Bopping Toady", "Ragumo/Aqua Kuribo", "Pencil/Spikey", "Kyotonbo")
        elif level == "Tree Zone 2":
            shuffle = ("Noko Bombette/Bear", "No 48/Mogyo")
        elif level == "Tree Zone 3":
            shuffle = ("Battle Beetle", "Be", "Ant")
        elif level == "Tree Zone 5":
            shuffle = ("Paragoomba (Diagonal)", "Dondon", "Paragoomba (Vertical)")
        elif level == "Pumpkin Zone 2":
            shuffle = ("Boo/Bomubomu", "Kyororo", "Honebon/F Boy", "Karakara", "Star (Vertical)/Blurp (Horizontal)",
                       "Star (Horizontal)/Blurp (Vertical)")
        elif level == "Pumpkin Zone 3":
            shuffle = ("Boo/Bomubomu", "Unibo/Terekuribo")
        elif level == "Mario Zone 1":
            shuffle = ("Koopa Troopa", "Neiji/Buichi", "Tatenoko")
        elif level == "Mario Zone 2":
            shuffle = ("Paragoomba (Diagonal)", "Goomba", "Paragoomba (Vertical)", "Noko Bombette/Bear",
                       "Boo/Bomubomu")
        elif level == "Turtle Zone 1":
            shuffle = ("Horizontal Blurp", "Shark", "Cheep Cheep (Vertical)", "Paragoomba (Diagonal)", "Goomba",
                       "Spiny Cheep Cheep", "Paragoomba (Vertical)",
                       "Owl Platform (Horizontal)/Cheep Cheep (Horizontal)")
        elif level == "Hippo Zone":
            shuffle = ("Horizontal Blurp", "Dondon", "Unibo/Terekuribo", "Toriuo")
        elif level == "Space Zone 2":
            shuffle = ("Tosenbo/Pikku", "Star (Vertical)/Blurp (Horizontal)", "Star (Horizontal)/Blurp (Vertical)")
        elif level == "Macro Zone 1":
            shuffle = ("Kyotonbo", "Goronto", "Dokanto", "Chikunto")
        elif level == "Macro Zone 2":
            shuffle = ("Cheep Cheep (Vertical)", "Battle Beetle", "Be",
                       "Owl Platform (Horizontal)/Cheep Cheep (Horizontal)", "Ant")
        elif level == "Macro Zone 3":
            shuffle = ("Koopa Troopa", "Paragoomba (Diagonal)", "Goomba", "Be", "Paragoomba (Vertical)",
                       "Honebon/F Boy")
        elif level == "Pumpkin Zone Secret Course 2":
            shuffle = ("Koopa Troopa", "Goomba")
        for sprite in level_sprite_data:
            if level == "Pumpkin Zone 1":
                if sprite["sprite"] == "Falling Spike":
                    shuffle = ("Boo/Bomubomu", "Falling Spike", "Kurokyura/Jack-in-the-Box", "Masked Ghoul/Bullet Bill")
                elif sprite["sprite"] == "Falling Spike on Chain":
                    shuffle = ("Boo/Bomubomu", "Falling Spike on Chain", "Kurokyura/Jack-in-the-Box",
                               "Masked Ghoul/Bullet Bill")
                else:
                    shuffle = ("Boo/Bomubomu", "Kurokyura/Jack-in-the-Box", "Masked Ghoul/Bullet Bill")
            elif level == "Pumpkin Zone 4":
                if sprite["sprite"] == "Falling Spike on Chain":
                    shuffle = ("Boo/Bomubomu", "Falling Spike on Chain", "Masked Ghoul/Bullet Bill", "Rerere/Poro",
                               "Tosenbo/Pikku")
                else:
                    shuffle = ("Boo/Bomubomu", "Masked Ghoul/Bullet Bill", "Rerere/Poro", "Tosenbo/Pikku")
            elif level == "Mario Zone 3":
                if sprite["sprite"] == "Claw Grabber":
                    shuffle = ("Koopa Troopa", "Diagonal Ball on Chain", "Kiddokatto", "Claw Grabber",
                               "Masked Ghoul/Bullet Bill")
                elif sprite["sprite"] in ("Koopa Troopa", "Diagonal Ball on Chain", "Kiddokatto"):
                    shuffle = ("Koopa Troopa", "Diagonal Ball on Chain", "Kiddokatto", "Masked Ghoul/Bullet Bill")
                else:
                    shuffle = ()
            elif level == "Mario Zone 4":
                if sprite["sprite"] == "Spinning Spike/Tamara":
                    shuffle = ("Goomba", "Spinning Spike/Tamara", "Boo/Bomubomu", "Masked Ghoul/Bullet Bill")
                elif sprite["sprite"] == "Moving Saw (Floor)":
                    shuffle = ("Goomba", "Moving Saw (Floor)", "Boo/Bomubomu", "Masked Ghoul/Bullet Bill")
                else:
                    shuffle = ("Goomba", "Boo/Bomubomu", "Masked Ghoul/Bullet Bill")
            elif level == "Turtle Zone 3":
                if sprite["sprite"] == "Pencil/Spikey":
                    shuffle = ("Koopa Troopa", "Paragoomba (Diagonal)", "Ragumo/Aqua Kuribo", "Pencil/Spikey",
                               "Paragoomba (Vertical)", "Honebon/F Boy")
                else:
                    shuffle = ("Koopa Troopa", "Paragoomba (Diagonal)", "Ragumo/Aqua Kuribo",
                               "Paragoomba (Vertical)", "Honebon/F Boy")
            elif level == "Space Zone 1":
                if sprite["sprite"] == "Boo/Bomubomu":
                    shuffle = ("Boo/Bomubomu", "No 48/Mogyo")
                else:
                    shuffle = ("Boo/Bomubomu", "No 48/Mogyo", "Rerere/Poro")
            elif level == "Mario's Castle":
                if sprite["sprite"] in ("Fire Pakkun Zo (Large)", "Fire Pakkun Zo (Left)"):
                    shuffle = ("Fire Pakkun Zo (Large)", "Fire Pakkun Zo (Left)")
                else:
                    shuffle = ("Spike Ball (Large)", "Spike Ball (Small)")
            elif level == "Tree Zone 4":
                # Deviation from SML2R: No Buichis placed into non-Buichi locations, as they can place under the
                # underground question mark blocks. Potentially could make a list of which ones are allowed to become
                # Buichis?
                if sprite["sprite"] in ("Runaway Heart Block/Bibi", "Piranha Plant (Downward)/Grubby",
                                        "Spinning Platform (Horizontal)/Skeleton Bee",
                                        "Spinning Spike (Horizontal)/Unera"):
                    shuffle = ("Runaway Heart Block/Bibi", "Piranha Plant (Downward)/Grubby",
                               "Spinning Platform (Horizontal)/Skeleton Bee", "Spinning Spike (Horizontal)/Unera")
                elif sprite["sprite"] == "Neiji/Buichi":
                    shuffle = ("Runaway Heart Block/Bibi", "Neiji/Buichi", "Piranha Plant (Downward)/Grubby",
                               "Spinning Platform (Horizontal)/Skeleton Bee", "Spinning Spike (Horizontal)/Unera")
                else:
                    shuffle = ()
            if sprite["sprite"] in ("Piranha Plant", "Fire Piranha Plant"):
                if level not in ("Pumpkin Zone 2", "Pumpkin Zone 4", "Macro Zone 3"):
                    shuffle = ("Piranha Plant", "Fire Piranha Plant")
            if sprite["sprite"] in shuffle:
                sprite["sprite"] = random.choice(shuffle)
            elif level == "Mario's Castle" and sprite["sprite"] == "Karamenbo" and not random.randint(0, 9):
                sprite["y"] += 1


def randomize_platforms(sprite_data, random):
    shuffle = ("Moving Platform (Small, Vertical)", "Moving Platform (Large, Vertical)",
               "Moving Platform (Small, Horizontal)", "Moving Platform (Large, Horizontal)",
               "Moving Platform (Large, Diagonal)", "Falling Platform")
    for sprite in sprite_data["Tree Zone 3"]:
        if sprite["sprite"] in shuffle:
            sprite["sprite"] = random.choice(shuffle)
    shuffle = ("Cloud Platform (Horizontal)", "Owl Platform (Horizontal)/Cheep Cheep (Horizontal)")
    for sprite in sprite_data["Tree Zone 5"]:
        if sprite["sprite"] in shuffle:
            sprite["sprite"] = random.choice(shuffle)
    shuffle = ("Falling Bone Platform", "Rising Bone Platform", "Skull Platform")
    for sprite in sprite_data["Mario's Castle"]:
        if sprite["sprite"] in shuffle:
            sprite["sprite"] = random.choice(shuffle)
