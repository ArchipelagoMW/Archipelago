import copy
from typing import List, Union

from BaseClasses import Location
from .utils import convert_to_ingame_text


class ScriptLine:
    contents: List[Union[str, int]]

    def __init__(self, contents):
        self.contents = contents

    def get_bytes(self):
        out_bytes = []
        for content in self.contents:
            if type(content) is str:
                out_bytes += convert_to_ingame_text(content)
            else:
                out_bytes.append(content)
        return out_bytes


class PhoneScript:
    caller_id: int
    lines: List[ScriptLine]

    def __init__(self, caller_id, lines):
        self.caller_id = caller_id
        self.lines = lines

    def get_script_bytes(self):
        out_bytes = []
        for line in self.lines:
            out_bytes += line.get_bytes()
        return out_bytes


caller_none = 0x00
caller_mom = 0x01
caller_bikeshop = 0x02
caller_bill = 0x03
caller_elm = 0x04

caller_withheld = 38
caller_bank_of_mom = 39
caller_brock = 40
caller_eusine = 41
caller_out_of_area = 42

text_cmd = 0x00
line_cmd = 0x4f
para_cmd = 0x51
cont_cmd = 0x55
done_cmd = 0x57

play_g_cmd = 0x14
player_cmd = 0x52
rival_cmd = 0x53
poke_cmd = 0x54


def split_location(location_name):
    if len(location_name) < 17:
        return [line_cmd, location_name]
    if len(location_name) < 33:
        return [line_cmd, location_name[:15] + "-", cont_cmd, location_name[15:]]
    return [line_cmd, location_name[:15] + "-", cont_cmd, location_name[15:33] + "…"]


def template_call_remote(location: Location, world):
    player = location.item.player
    # split into lines with cont
    location_cmd = split_location(location.name.upper())

    game_name = location.game.upper()
    game_name = (game_name[:15] + "…") if len(game_name) > 16 else game_name

    player_name = world.multiworld.player_name[player].upper()

    item_name = location.item.name.upper()
    item_name = (item_name[:15] + "…") if len(item_name) > 16 else item_name

    return PhoneScript(caller_out_of_area, [
        ScriptLine([text_cmd, "Hi, ", play_g_cmd, "! It's"]),
        ScriptLine([line_cmd, player_name]),
        ScriptLine([para_cmd, "I'm calling from"]),
        ScriptLine([line_cmd, game_name]),
        ScriptLine([para_cmd, "I'm looking for my"]),
        ScriptLine([line_cmd, item_name]),
        ScriptLine([para_cmd, "that's at your"]),
        ScriptLine(location_cmd),
        ScriptLine([para_cmd, "Have you found it"]),
        ScriptLine([line_cmd, "yet?"]),
        ScriptLine([done_cmd])
    ])


def template_call_bike_shop(location):
    item_name = location.item.name.upper()
    item_name = (item_name[:15] + "…") if len(item_name) > 16 else item_name
    return PhoneScript(caller_mom, [
        ScriptLine([text_cmd, "Hello?"]),
        ScriptLine([para_cmd, "Hi ", play_g_cmd, "!"]),
        ScriptLine([para_cmd, "I got a call from"]),
        ScriptLine([line_cmd, "A man in GOLDENROD"]),
        ScriptLine([para_cmd, "He said he has a"]),
        ScriptLine([line_cmd, item_name]),
        ScriptLine([cont_cmd, "for you."]),
        ScriptLine([para_cmd, "Make sure you head"]),
        ScriptLine([line_cmd, "to the BIKE SHOP"]),
        ScriptLine([para_cmd, "to pick that up,"]),
        ScriptLine([line_cmd, "okay?"]),
        ScriptLine([done_cmd])
    ])


def template_call_psychic():
    return PhoneScript(caller_withheld, [
        ScriptLine([text_cmd, "…"]),
        ScriptLine([para_cmd, "…"]),
        ScriptLine([para_cmd, "…"]),
        ScriptLine([para_cmd, "…I got it!"]),
        ScriptLine([para_cmd, "You're looking"]),
        ScriptLine([line_cmd, "for this!"]),
        ScriptLine([done_cmd])
    ])


def get_shuffled_basic_calls(random):
    basic_calls = copy.deepcopy(phone_scripts)
    random.shuffle(basic_calls)
    return basic_calls


ffxiv = PhoneScript(caller_withheld, [
    ScriptLine([text_cmd, "Hi, ", play_g_cmd, "!"]),
    ScriptLine([para_cmd, "Have you heard of"]),
    ScriptLine([line_cmd, "the critically"]),
    ScriptLine([para_cmd, "acclaimed MMORPG"]),
    ScriptLine([line_cmd, "Final Fantasy XIV?"]),
    ScriptLine([para_cmd, "With an expanded"]),
    ScriptLine([line_cmd, "free trial which"]),
    ScriptLine([para_cmd, "you can play"]),
    ScriptLine([line_cmd, "through the"]),
    ScriptLine([para_cmd, "entirety of A"]),
    ScriptLine([line_cmd, "Realm Reborn and"]),
    ScriptLine([para_cmd, "the award-winning"]),
    ScriptLine([line_cmd, "Heavensward"]),
    ScriptLine([cont_cmd, "expansion"]),
    ScriptLine([para_cmd, "up to Lv.60 for"]),
    ScriptLine([line_cmd, "free with no"]),
    ScriptLine([para_cmd, "restrictions on"]),
    ScriptLine([line_cmd, "playtime?"]),
    ScriptLine([done_cmd])
])

brock_oven = PhoneScript(caller_brock, [
    ScriptLine([text_cmd, "Why do they"]),
    ScriptLine([line_cmd, "call it OVEN…"]),
    ScriptLine([para_cmd, "when you OF IN"]),
    ScriptLine([line_cmd, "the COLD FOOD…"]),
    ScriptLine([para_cmd, "OF OUT hot eat"]),
    ScriptLine([line_cmd, "the FOOD?"]),
    ScriptLine([para_cmd, "Really makes you"]),
    ScriptLine([line_cmd, "think…"]),
    ScriptLine([done_cmd])
])

gura_call = PhoneScript(caller_withheld, [
    ScriptLine([text_cmd, "H-Hello ma'am…"]),
    ScriptLine([para_cmd, "Do you have a"]),
    ScriptLine([line_cmd, "moment to talk"]),
    ScriptLine([para_cmd, "about our lord and"]),
    ScriptLine([line_cmd, "savior LIGHTNING"]),
    ScriptLine([cont_cmd, "MCQUEEN?"]),
    ScriptLine([para_cmd, "He's he star of"]),
    ScriptLine([line_cmd, "several feature"]),
    ScriptLine([cont_cmd, "films, such as"]),
    ScriptLine([para_cmd, "CARS, CARS 2,"]),
    ScriptLine([line_cmd, "CARS 3, PLANES:"]),
    ScriptLine([cont_cmd, "FIRE & RESCUE,"]),
    ScriptLine([para_cmd, "FINDING DORY, TOY"]),
    ScriptLine([line_cmd, "STORY 3, COCO,"]),
    ScriptLine([para_cmd, "and RALPH BREAKS"]),
    ScriptLine([line_cmd, "THE INTERNET,"]),
    ScriptLine([para_cmd, "as well as other"]),
    ScriptLine([line_cmd, "short films such"]),
    ScriptLine([cont_cmd, "as-"]),
    ScriptLine([para_cmd, "K-KINGDOM HEARTS?"]),
    ScriptLine([done_cmd])
])

regi_call = PhoneScript(caller_withheld, [
    ScriptLine([text_cmd, "REGIROCK: ÜN ÜN ÜN"]),
    ScriptLine([line_cmd, "$Ae▶&!→ ,♀é▷Ö"]),
    ScriptLine([para_cmd, "ÜN ÜN ÜN ÜN ÜN ÜN"]),
    ScriptLine([line_cmd, "AAAAAAOOOOOOOORT"]),
    ScriptLine([para_cmd, "REGISTEEL: 1001000"]),
    ScriptLine([line_cmd, "1000101 1001100"]),
    ScriptLine([cont_cmd, "1001100 1001111"]),
    ScriptLine([done_cmd])
])

eusine_call = PhoneScript(caller_eusine, [
    ScriptLine([text_cmd, "Hiya, ", play_g_cmd, "!"]),
    ScriptLine([line_cmd, "It's EUSINE!"]),
    ScriptLine([para_cmd, "I just wanted to"]),
    ScriptLine([line_cmd, "call you about"]),
    ScriptLine([para_cmd, "a discovery I"]),
    ScriptLine([line_cmd, "made. A baby"]),
    ScriptLine([cont_cmd, "SUICUNE!"]),
    ScriptLine([para_cmd, "That's right, it's"]),
    ScriptLine([line_cmd, "small and blue,"]),
    ScriptLine([para_cmd, "large head with"]),
    ScriptLine([line_cmd, "antennae of some"]),
    ScriptLine([cont_cmd, "kind."]),
    ScriptLine([para_cmd, "It has no arms,"]),
    ScriptLine([line_cmd, "but somehow it"]),
    ScriptLine([cont_cmd, "learned ICE PUNCH!"]),
    ScriptLine([done_cmd])
])

slowpoke_call = PhoneScript(caller_withheld, [
    ScriptLine([text_cmd, "Hi, hello?"]),
    ScriptLine([para_cmd, "I'm calling about"]),
    ScriptLine([line_cmd, "an amazing invest-"]),
    ScriptLine([cont_cmd, "ment opportunity:"]),
    ScriptLine([para_cmd, "Just for you, a"]),
    ScriptLine([line_cmd, "delicious, mouth-"]),
    ScriptLine([para_cmd, "watering, tender"]),
    ScriptLine([line_cmd, "SLOWPOKETAIL for"]),
    ScriptLine([para_cmd, "the low low price"]),
    ScriptLine([line_cmd, "of ¥1000000!"]),
    ScriptLine([para_cmd, "Hello? Are you"]),
    ScriptLine([line_cmd, "still there?"]),
    ScriptLine([done_cmd])
])

elm_hacked_call = PhoneScript(caller_elm, [
    ScriptLine([text_cmd, play_g_cmd, "?"]),
    ScriptLine([line_cmd, "Oh it's terrible."]),
    ScriptLine([para_cmd, "I got a call from"]),
    ScriptLine([line_cmd, poke_cmd, "GEAR tech-"]),
    ScriptLine([cont_cmd, "nical support,"]),
    ScriptLine([para_cmd, "or so they said!"]),
    ScriptLine([para_cmd, "They took my"]),
    ScriptLine([line_cmd, "number, my"]),
    ScriptLine([cont_cmd, poke_cmd, "PAY account,"]),
    ScriptLine([para_cmd, "Gosh, even all my"]),
    ScriptLine([line_cmd, "PRIMEAPES are gone"]),
    ScriptLine([para_cmd, player_cmd, " got ELM's"]),
    ScriptLine([line_cmd, "new phone number."]),
    ScriptLine([para_cmd, "Whatever will I"]),
    ScriptLine([line_cmd, "do…"]),
    ScriptLine([done_cmd])
])

mom_password_call = PhoneScript(caller_mom, [
    ScriptLine([text_cmd, "Hello?"]),
    ScriptLine([para_cmd, "Hi ", play_g_cmd, "…"]),
    ScriptLine([line_cmd, "I was going to"]),
    ScriptLine([para_cmd, "buy something"]),
    ScriptLine([line_cmd, "nice for you,"]),
    ScriptLine([para_cmd, "but I accident-"]),
    ScriptLine([line_cmd, "ally spent the"]),
    ScriptLine([para_cmd, "money on BLUE"]),
    ScriptLine([line_cmd, "CARD points."]),
    ScriptLine([para_cmd, "I promise I'll"]),
    ScriptLine([line_cmd, "make it up to you,"]),
    ScriptLine([para_cmd, "but later,"]),
    ScriptLine([line_cmd, "PASSWORD is"]),
    ScriptLine([cont_cmd, "starting now!"]),
    ScriptLine([done_cmd])
])

warranty_call = PhoneScript(caller_withheld, [
    ScriptLine([text_cmd, "Hello, we're"]),
    ScriptLine([line_cmd, "trying to reach"]),
    ScriptLine([para_cmd, "you about your"]),
    ScriptLine([line_cmd, "BICYCLE's ex-"]),
    ScriptLine([cont_cmd, "tended warranty-"]),
    ScriptLine([done_cmd])
])

bill_id_call = PhoneScript(caller_bill, [
    ScriptLine([text_cmd, "Gugyoo…"]),
    ScriptLine([line_cmd, "Guooh! Pijji!"]),
    ScriptLine([para_cmd, "Ha! Fooled you!"]),
    ScriptLine([line_cmd, "Those aren't "]),
    ScriptLine([cont_cmd, poke_cmd, "MON"]),
    ScriptLine([para_cmd, "It's actually me,"]),
    ScriptLine([line_cmd, "BILL!"]),
    ScriptLine([para_cmd, "Wh-You knew?"]),
    ScriptLine([line_cmd, "Caller ID?"]),
    ScriptLine([para_cmd, "Rats, foiled by my"]),
    ScriptLine([line_cmd, "own invention"]),
    ScriptLine([cont_cmd, "again"]),
    ScriptLine([done_cmd])
])

elm_jsr_call = PhoneScript(caller_elm, [
    ScriptLine([text_cmd, play_g_cmd, ", how are"]),
    ScriptLine([line_cmd, "things going?"]),
    ScriptLine([para_cmd, "I called because"]),
    ScriptLine([line_cmd, "something weird is"]),
    ScriptLine([para_cmd, "happening with the"]),
    ScriptLine([line_cmd, "radio broadcasts."]),
    ScriptLine([para_cmd, "They were talking"]),
    ScriptLine([line_cmd, "about FUNKY FRESH"]),
    ScriptLine([cont_cmd, "BEATS."]),
    ScriptLine([para_cmd, "TEAM ROCKET must"]),
    ScriptLine([line_cmd, "be running some"]),
    ScriptLine([para_cmd, "kind of pirate"]),
    ScriptLine([line_cmd, "radio station…"]),
    ScriptLine([done_cmd])
])

bike_loyalty_call = PhoneScript(caller_bikeshop, [
    ScriptLine([text_cmd, "Hiya ", play_g_cmd, "!"]),
    ScriptLine([line_cmd, "We're calling"]),
    ScriptLine([cont_cmd, "around"]),
    ScriptLine([para_cmd, "to spread the word"]),
    ScriptLine([line_cmd, "about our new"]),
    ScriptLine([cont_cmd, "loyalty program!"]),
    ScriptLine([para_cmd, "On your 10th"]),
    ScriptLine([line_cmd, "purchase of any"]),
    ScriptLine([cont_cmd, "BICYCLE, you get"]),
    ScriptLine([para_cmd, "a BIKE VOUCHER,"]),
    ScriptLine([line_cmd, "free of charge!"]),
    ScriptLine([para_cmd, "We're also"]),
    ScriptLine([line_cmd, "offering a "]),
    ScriptLine([cont_cmd, "discount!"]),
    ScriptLine([para_cmd, "A brand new"]),
    ScriptLine([line_cmd, "BICYCLE for"]),
    ScriptLine([cont_cmd, "¥999999.99!"]),
    ScriptLine([done_cmd])
])

ppip_call = PhoneScript(caller_withheld, [
    ScriptLine([text_cmd, "THIS IS AN AUTO-"]),
    ScriptLine([line_cmd, "MATED MESSAGE"]),
    ScriptLine([para_cmd, "FROM THE PORYGON"]),
    ScriptLine([line_cmd, "POLITICAL"]),
    ScriptLine([cont_cmd, "INTERESTS PARTY,"]),
    ScriptLine([para_cmd, "OR P P I P FOR"]),
    ScriptLine([line_cmd, "SHORT."]),
    ScriptLine([para_cmd, "WE CAMPAIGN FOR"]),
    ScriptLine([line_cmd, "PORYGON ISSUES,"]),
    ScriptLine([cont_cmd, "PORYGON2 ISSUES"]),
    ScriptLine([para_cmd, "AND ISSUES OF"]),
    ScriptLine([line_cmd, "ANY OTHER POT-"]),
    ScriptLine([cont_cmd, "ENTIAL PORYGON"]),
    ScriptLine([para_cmd, "ISSUES SUCH AS:"]),
    ScriptLine([para_cmd, "PENSIONS FOR"]),
    ScriptLine([line_cmd, "VETERAN ELECTRIC"]),
    ScriptLine([cont_cmd, "SOLDIERS,"]),
    ScriptLine([para_cmd, "AND UNFAIR"]),
    ScriptLine([line_cmd, "MALIGNMENT FOR THE"]),
    ScriptLine([para_cmd, "UNFORTUNATE"]),
    ScriptLine([line_cmd, "EVENTS OF 16. DEC"]),
    ScriptLine([cont_cmd, "1997."]),
    ScriptLine([para_cmd, "PLEASE VOTE FOR"]),
    ScriptLine([line_cmd, "US IN THE UPCOMING"]),
    ScriptLine([para_cmd, "JOHTO LOCAL"]),
    ScriptLine([line_cmd, "ELECTIONS."]),
    ScriptLine([done_cmd])
])

bill_eevee_call = PhoneScript(caller_bill, [
    ScriptLine([text_cmd, "Hey ", play_g_cmd, "!"]),
    ScriptLine([para_cmd, "I have just"]),
    ScriptLine([line_cmd, "completed some"]),
    ScriptLine([para_cmd, "research into"]),
    ScriptLine([line_cmd, "EEVEE and its"]),
    ScriptLine([cont_cmd, "evolutions!"]),
    ScriptLine([para_cmd, "I have been able"]),
    ScriptLine([line_cmd, "to scientif-"]),
    ScriptLine([done_cmd])
])

elm_kyogre_call = PhoneScript(caller_elm, [
    ScriptLine([text_cmd, "Hi, Mr. ", poke_cmd, "MON?"]),
    ScriptLine([line_cmd, "Just following up"]),
    ScriptLine([cont_cmd, "on your email."]),
    ScriptLine([para_cmd, "The way I see it,"]),
    ScriptLine([line_cmd, "KYOGRE is the one"]),
    ScriptLine([cont_cmd, "surrounded!"]),
    ScriptLine([para_cmd, "What's under the"]),
    ScriptLine([line_cmd, "ocean? More"]),
    ScriptLine([cont_cmd, "earth!"]),
    ScriptLine([para_cmd, "Oh, ", play_g_cmd, "?!"]),
    ScriptLine([line_cmd, "I must have called"]),
    ScriptLine([cont_cmd, "the wrong number…"]),
    ScriptLine([done_cmd])
])

elm_mew_call = PhoneScript(caller_elm, [
    ScriptLine([text_cmd, "Oh… ", player_cmd, "…"]),
    ScriptLine([para_cmd, "That red-headed"]),
    ScriptLine([line_cmd, "kid came back"]),
    ScriptLine([cont_cmd, "to the lab."]),
    ScriptLine([para_cmd, "He said he would"]),
    ScriptLine([line_cmd, "tell me where to"]),
    ScriptLine([para_cmd, "find a rare ", poke_cmd, "-"]),
    ScriptLine([line_cmd, "MON if I didn't"]),
    ScriptLine([cont_cmd, "call the police."]),
    ScriptLine([para_cmd, "Long story short,"]),
    ScriptLine([line_cmd, "I've been pushing"]),
    ScriptLine([para_cmd, "on this truck"]),
    ScriptLine([line_cmd, "for hours now,"]),
    ScriptLine([para_cmd, "and still no"]),
    ScriptLine([line_cmd, "sight of the"]),
    ScriptLine([cont_cmd, "thing…"]),
    ScriptLine([done_cmd])
])

bank_of_mom_1 = PhoneScript(caller_bank_of_mom, [
    ScriptLine([text_cmd, "Hello, ", play_g_cmd, "."]),
    ScriptLine([line_cmd, "We're calling to"]),
    ScriptLine([para_cmd, "let you know that"]),
    ScriptLine([line_cmd, "your latest bank"]),
    ScriptLine([para_cmd, "statement is now"]),
    ScriptLine([line_cmd, "available online."]),
    ScriptLine([para_cmd, "Thank you for"]),
    ScriptLine([line_cmd, "managing your"]),
    ScriptLine([cont_cmd, "finances with"]),
    ScriptLine([para_cmd, "BANK of MOM."]),
    ScriptLine([done_cmd])
])

bank_of_mom_2 = PhoneScript(caller_bank_of_mom, [
    ScriptLine([text_cmd, "Hello, ", play_g_cmd, "."]),
    ScriptLine([line_cmd, "We're calling to"]),
    ScriptLine([para_cmd, "ask you about"]),
    ScriptLine([line_cmd, "some suspicious"]),
    ScriptLine([para_cmd, "transactions"]),
    ScriptLine([line_cmd, "made with your"]),
    ScriptLine([cont_cmd, "bank account."]),
    ScriptLine([para_cmd, "Today there were"]),
    ScriptLine([line_cmd, "3 purchases of"]),
    ScriptLine([cont_cmd, "SUPER POTIONs"]),
    ScriptLine([para_cmd, "from an unknown"]),
    ScriptLine([line_cmd, "location."]),
    ScriptLine([para_cmd, "Okay, we can"]),
    ScriptLine([line_cmd, "unfreeze your"]),
    ScriptLine([cont_cmd, "account."]),
    ScriptLine([para_cmd, "Thank you for"]),
    ScriptLine([line_cmd, "managing your"]),
    ScriptLine([cont_cmd, "finances with"]),
    ScriptLine([para_cmd, "BANK of MOM."]),
    ScriptLine([done_cmd])
])

phone_scripts = [
    ffxiv,
    brock_oven,
    gura_call,
    regi_call,
    eusine_call,
    slowpoke_call,
    elm_hacked_call,
    mom_password_call,
    warranty_call,
    bill_id_call,
    elm_jsr_call,
    bike_loyalty_call,
    ppip_call,
    bill_eevee_call,
    elm_kyogre_call,
    elm_mew_call,
    bank_of_mom_1,
    bank_of_mom_2
]
