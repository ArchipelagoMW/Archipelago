from dataclasses import dataclass
from typing import Tuple, Dict, List

from ..strings.animal_product_names import AnimalProduct
from ..strings.artisan_good_names import ArtisanGood
from ..strings.crop_names import Vegetable, Fruit
from ..strings.flower_names import Flower
from ..strings.food_names import Meal, Beverage
from ..strings.forageable_names import Forageable
from ..strings.metal_names import Mineral, MetalBar
from ..strings.villager_names import NPC


class SecretNote:
    note_1 = "Secret Note #1: A Page From Abigail's Diary"
    note_2 = "Secret Note #2: Sam's Holiday Shopping List"
    note_3 = "Secret Note #3: Leah's Perfect Dinner"
    note_4 = "Secret Note #4: Maru's Greatest Invention Yet"
    note_5 = "Secret Note #5: Penny gets everyone something they love"
    note_6 = "Secret Note #6: Stardrop Saloon Special Orders"
    note_7 = "Secret Note #7: Older Bachelors In Town"
    note_8 = "Secret Note #8: To Haley And Emily"
    note_9 = "Secret Note #9: Alex's Strength Training Diet"
    note_10 = "Secret Note #10: Cryptic Note"
    note_11 = "Secret Note #11: Marnie's Memory"
    note_12 = "Secret Note #12: Good Things In Garbage Cans"
    note_13 = "Secret Note #13: Junimo Plush"
    note_14 = "Secret Note #14: Stone Junimo"
    note_15 = "Secret Note #15: Mermaid Show"
    note_16 = "Secret Note #16: Treasure Chest"
    note_17 = "Secret Note #17: Green Strange Doll"
    note_18 = "Secret Note #18: Yellow Strange Doll"
    note_19_part_1 = "Secret Note #19: Solid Gold Lewis"
    note_19_part_2 = "Secret Note #19: In Town For All To See"
    note_20 = "Secret Note #20: Special Charm"
    note_21 = "Secret Note #21: A Date In Nature"
    note_22 = "Secret Note #22: The Mysterious Qi"
    note_23 = "Secret Note #23: Strange Note"
    note_24 = "Secret Note #24: M. Jasper's Book On Junimos"
    note_25 = "Secret Note #25: Ornate Necklace"
    note_26 = "Secret Note #26: Ancient Farming Secrets"
    note_27 = "Secret Note #27: A Compendium Of My Greatest Discoveries"


@dataclass(frozen=True)
class RequiredGifts:
    npc: str
    gifts: Tuple[str, ...]


gift_requirements: Dict[str, List[RequiredGifts]] = {
    SecretNote.note_1: [RequiredGifts(NPC.abigail, (Vegetable.pumpkin, Mineral.amethyst, Meal.chocolate_cake, Meal.spicy_eel, Meal.blackberry_cobbler,)), ],
    SecretNote.note_2: [RequiredGifts(NPC.sebastian, (Mineral.frozen_tear, Meal.sashimi,)),
                        RequiredGifts(NPC.penny, (Mineral.emerald, Flower.poppy,)),
                        RequiredGifts(NPC.vincent, (Fruit.grape, Meal.cranberry_candy,)),
                        RequiredGifts(NPC.jodi, (Meal.crispy_bass, Meal.pancakes,)),
                        RequiredGifts(NPC.kent, (Meal.fiddlehead_risotto, Meal.roasted_hazelnuts,)),
                        RequiredGifts(NPC.sam, (Forageable.cactus_fruit, Meal.maple_bar, Meal.pizza,)), ],
    SecretNote.note_3: [RequiredGifts(NPC.leah, (Meal.salad, ArtisanGood.goat_cheese, AnimalProduct.truffle, ArtisanGood.wine,)), ],
    SecretNote.note_4: [RequiredGifts(NPC.maru, (MetalBar.gold, MetalBar.iridium, ArtisanGood.battery_pack, Mineral.diamond, Fruit.strawberry,)), ],
    SecretNote.note_5: [RequiredGifts(NPC.pam, (Vegetable.parsnip, Meal.glazed_yams,)),
                        RequiredGifts(NPC.jas, (Flower.fairy_rose, Meal.plum_pudding,)),
                        RequiredGifts(NPC.vincent, (Meal.pink_cake, Fruit.grape,)),
                        RequiredGifts(NPC.george, (Forageable.leek, Meal.fried_mushroom,)),
                        RequiredGifts(NPC.evelyn, (Vegetable.beet, Flower.tulip,)), ],
    SecretNote.note_6: [RequiredGifts(NPC.lewis, (Meal.autumn_bounty,)),
                        RequiredGifts(NPC.marnie, (Meal.pumpkin_pie,)),
                        RequiredGifts(NPC.demetrius, (Meal.bean_hotpot,)),
                        RequiredGifts(NPC.caroline, (Meal.fish_taco,)), ],
    SecretNote.note_7: [RequiredGifts(NPC.harvey, (Beverage.coffee, ArtisanGood.pickles,)),
                        RequiredGifts(NPC.elliott, (Meal.crab_cakes, Fruit.pomegranate,)),
                        RequiredGifts(NPC.shane, (Beverage.beer, Meal.pizza, Meal.pepper_poppers,)), ],
    SecretNote.note_8: [RequiredGifts(NPC.haley, (Meal.pink_cake, Flower.sunflower,)),
                        RequiredGifts(NPC.emily, (Mineral.amethyst, Mineral.aquamarine, Mineral.emerald, Mineral.jade, Mineral.ruby, Mineral.topaz, AnimalProduct.wool,)), ],
    SecretNote.note_9: [RequiredGifts(NPC.alex, (Meal.complete_breakfast, Meal.salmon_dinner,)), ],
}
