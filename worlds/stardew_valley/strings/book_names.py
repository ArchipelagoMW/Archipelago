class Book:
    animal_catalogue = "Animal Catalogue"
    book_of_mysteries = "Book of Mysteries"
    book_of_stars = "Book Of Stars"
    stardew_valley_almanac = "Stardew Valley Almanac"
    bait_and_bobber = "Bait And Bobber"
    mining_monthly = "Mining Monthly"
    combat_quarterly = "Combat Quarterly"
    woodcutters_weekly = "Woodcutter's Weekly"
    the_alleyway_buffet = "The Alleyway Buffet"
    the_art_o_crabbing = "The Art O' Crabbing"
    dwarvish_safety_manual = "Dwarvish Safety Manual"
    jewels_of_the_sea = "Jewels Of The Sea"
    raccoon_journal = "Raccoon Journal"
    woodys_secret = "Woody's Secret"
    jack_be_nimble_jack_be_thick = "Jack Be Nimble, Jack Be Thick"
    friendship_101 = "Friendship 101"
    monster_compendium = "Monster Compendium"
    mapping_cave_systems = "Mapping Cave Systems"
    treasure_appraisal_guide = "Treasure Appraisal Guide"
    way_of_the_wind_pt_1 = "Way Of The Wind pt. 1"
    way_of_the_wind_pt_2 = "Way Of The Wind pt. 2"
    horse_the_book = "Horse: The Book"
    ol_slitherlegs = "Ol' Slitherlegs"
    queen_of_sauce_cookbook = "Queen Of Sauce Cookbook"
    price_catalogue = "Price Catalogue"
    the_diamond_hunter = "The Diamond Hunter"


ordered_lost_books = []
all_lost_books = set()


def lost_book(book_name: str):
    ordered_lost_books.append(book_name)
    all_lost_books.add(book_name)
    return book_name


class LostBook:
    tips_on_farming = lost_book("Tips on Farming")
    this_is_a_book_by_marnie = lost_book("This is a book by Marnie")
    on_foraging = lost_book("On Foraging")
    the_fisherman_act_1 = lost_book("The Fisherman, Act 1")
    how_deep_do_the_mines_go = lost_book("How Deep do the mines go?")
    an_old_farmers_journal = lost_book("An Old Farmer's Journal")
    scarecrows = lost_book("Scarecrows")
    the_secret_of_the_stardrop = lost_book("The Secret of the Stardrop")
    journey_of_the_prairie_king_the_smash_hit_video_game = lost_book("Journey of the Prairie King -- The Smash Hit Video Game!")
    a_study_on_diamond_yields = lost_book("A Study on Diamond Yields")
    brewmasters_guide = lost_book("Brewmaster's Guide")
    mysteries_of_the_dwarves = lost_book("Mysteries of the Dwarves")
    highlights_from_the_book_of_yoba = lost_book("Highlights From The Book of Yoba")
    marriage_guide_for_farmers = lost_book("Marriage Guide for Farmers")
    the_fisherman_act_ii = lost_book("The Fisherman, Act II")
    technology_report = lost_book("Technology Report!")
    secrets_of_the_legendary_fish = lost_book("Secrets of the Legendary Fish")
    gunther_tunnel_notice = lost_book("Gunther Tunnel Notice")
    note_from_gunther = lost_book("Note From Gunther")
    goblins_by_m_jasper = lost_book("Goblins by M. Jasper")
    secret_statues_acrostics = lost_book("Secret Statues Acrostics")
