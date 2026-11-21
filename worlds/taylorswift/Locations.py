# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2026 Benny Dreamly.

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import Location

if TYPE_CHECKING:
    from . import TaylorSwiftWorld


class TaylorSwiftLocation(Location):
    game = "Taylor Swift Discography"


# (region, [vault_track_song?])
class LocationData(NamedTuple):
    region: str
    vault: bool = False
    deluxe: bool = False
    extra: bool = False


LOCATION_TABLE: dict[str, LocationData] = {
    # Freebie locations (accessible from start, no item required)
    "First Listen":                    LocationData("Menu"),
    "Encore":                          LocationData("Menu"),

    # Taylor Swift (Debut)
    "Tim McGraw":                          LocationData("Taylor Swift"),
    "Picture to Burn":                     LocationData("Taylor Swift"),
    "Teardrops on My Guitar":              LocationData("Taylor Swift"),
    "A Place in This World":               LocationData("Taylor Swift"),
    "Cold as You":                         LocationData("Taylor Swift"),
    "The Outside":                         LocationData("Taylor Swift"),
    "Tied Together with a Smile":          LocationData("Taylor Swift"),
    "Stay Beautiful":                      LocationData("Taylor Swift"),
    "Should've Said No":                   LocationData("Taylor Swift"),
    "Mary's Song (Oh My My My)":           LocationData("Taylor Swift"),
    "Our Song":                            LocationData("Taylor Swift"),
    "I'm Only Me When I'm With You":      LocationData("Taylor Swift"),
    "Invisible":                           LocationData("Taylor Swift"),
    "A Perfectly Good Heart":              LocationData("Taylor Swift"),
    "Teardrops on My Guitar - Pop Version": LocationData("Taylor Swift"),

    # Fearless
    "Fearless":                            LocationData("Fearless"),
    "Fifteen":                             LocationData("Fearless"),
    "Love Story":                          LocationData("Fearless"),
    "Hey Stephen":                         LocationData("Fearless"),
    "White Horse":                         LocationData("Fearless"),
    "You Belong With Me":                  LocationData("Fearless"),
    "Breathe (feat. Colbie Caillat)":      LocationData("Fearless"),
    "Tell Me Why":                         LocationData("Fearless"),
    "You're Not Sorry":                    LocationData("Fearless"),
    "The Way I Loved You":                 LocationData("Fearless"),
    "Forever & Always":                    LocationData("Fearless"),
    "The Best Day":                        LocationData("Fearless"),
    "Change":                              LocationData("Fearless"),
    "Jump Then Fall":                      LocationData("Fearless", False, True),
    "Untouchable":                         LocationData("Fearless", False, True),
    "Forever & Always (Piano Version)":    LocationData("Fearless", False, True),
    "Come In With The Rain":               LocationData("Fearless", False, True),
    "Superstar":                           LocationData("Fearless", False, True),
    "The Other Side of the Door":          LocationData("Fearless", False, True),

    # Fearless (Taylor's Version)
    "Fearless (Taylor's Version)":                          LocationData("Fearless (Taylor's Version)"),
    "Fifteen (Taylor's Version)":                           LocationData("Fearless (Taylor's Version)"),
    "Love Story (Taylor's Version)":                        LocationData("Fearless (Taylor's Version)"),
    "Hey Stephen (Taylor's Version)":                       LocationData("Fearless (Taylor's Version)"),
    "White Horse (Taylor's Version)":                       LocationData("Fearless (Taylor's Version)"),
    "You Belong With Me (Taylor's Version)":                LocationData("Fearless (Taylor's Version)"),
    "Breathe (feat. Colbie Caillat) (Taylor's Version)":    LocationData("Fearless (Taylor's Version)"),
    "Tell Me Why (Taylor's Version)":                       LocationData("Fearless (Taylor's Version)"),
    "You're Not Sorry (Taylor's Version)":                  LocationData("Fearless (Taylor's Version)"),
    "The Way I Loved You (Taylor's Version)":               LocationData("Fearless (Taylor's Version)"),
    "Forever & Always (Taylor's Version)":                  LocationData("Fearless (Taylor's Version)"),
    "The Best Day (Taylor's Version)":                      LocationData("Fearless (Taylor's Version)"),
    "Change (Taylor's Version)":                            LocationData("Fearless (Taylor's Version)"),
    "Jump Then Fall (Taylor's Version)":                    LocationData("Fearless (Taylor's Version)"),
    "Untouchable (Taylor's Version)":                       LocationData("Fearless (Taylor's Version)"),
    "Forever & Always (Piano Version) (Taylor's Version)":  LocationData("Fearless (Taylor's Version)"),
    "Come In With The Rain (Taylor's Version)":             LocationData("Fearless (Taylor's Version)"),
    "Superstar (Taylor's Version)":                         LocationData("Fearless (Taylor's Version)"),
    "The Other Side of the Door (Taylor's Version)":        LocationData("Fearless (Taylor's Version)"),
    "Today Was a Fairytale (Taylor's Version)":             LocationData("Fearless (Taylor's Version)"),
    "You All Over Me (feat. Maren Morris) (Taylor's Version) (From The Vault)":       LocationData("Fearless (Taylor's Version)", True),
    "Mr. Perfectly Fine (Taylor's Version) (From The Vault)":                          LocationData("Fearless (Taylor's Version)", True),
    "We Were Happy (Taylor's Version) (From The Vault)":                               LocationData("Fearless (Taylor's Version)", True),
    "That's When (Taylor's Version) (From The Vault) (Featuring Keith Urban)":         LocationData("Fearless (Taylor's Version)", True),
    "Don't You (Taylor's Version) (From The Vault)":                                   LocationData("Fearless (Taylor's Version)", True),
    "Bye Bye Baby (Taylor's Version) (From The Vault)":                                LocationData("Fearless (Taylor's Version)", True),

    # Speak Now
    "Mine":                               LocationData("Speak Now"),
    "Sparks Fly":                         LocationData("Speak Now"),
    "Back to December":                   LocationData("Speak Now"),
    "Speak Now":                          LocationData("Speak Now"),
    "Dear John":                          LocationData("Speak Now"),
    "Mean":                               LocationData("Speak Now"),
    "The Story of Us":                    LocationData("Speak Now"),
    "Never Grow Up":                      LocationData("Speak Now"),
    "Enchanted":                          LocationData("Speak Now"),
    "Better Than Revenge":                LocationData("Speak Now"),
    "Innocent":                           LocationData("Speak Now"),
    "Haunted":                            LocationData("Speak Now"),
    "Last Kiss":                          LocationData("Speak Now"),
    "Long Live":                          LocationData("Speak Now"),
    "Ours":                               LocationData("Speak Now", False, True),
    "If This Was A Movie":                LocationData("Speak Now", False, True),
    "Superman":                           LocationData("Speak Now", False, True),
    "Back To December - Acoustic":        LocationData("Speak Now", False, True),
    "Haunted - Acoustic Version":         LocationData("Speak Now", False, True),
    "Mine - POP Mix":                     LocationData("Speak Now", False, True),

    # Speak Now (Taylor's Version)
    "Mine (Taylor's Version)":                                              LocationData("Speak Now (Taylor's Version)"),
    "Sparks Fly (Taylor's Version)":                                        LocationData("Speak Now (Taylor's Version)"),
    "Back to December (Taylor's Version)":                                  LocationData("Speak Now (Taylor's Version)"),
    "Speak Now (Taylor's Version)":                                         LocationData("Speak Now (Taylor's Version)"),
    "Dear John (Taylor's Version)":                                         LocationData("Speak Now (Taylor's Version)"),
    "Mean (Taylor's Version)":                                              LocationData("Speak Now (Taylor's Version)"),
    "The Story of Us (Taylor's Version)":                                   LocationData("Speak Now (Taylor's Version)"),
    "Never Grow Up (Taylor's Version)":                                     LocationData("Speak Now (Taylor's Version)"),
    "Enchanted (Taylor's Version)":                                         LocationData("Speak Now (Taylor's Version)"),
    "Better Than Revenge (Taylor's Version)":                               LocationData("Speak Now (Taylor's Version)"),
    "Innocent (Taylor's Version)":                                          LocationData("Speak Now (Taylor's Version)"),
    "Haunted (Taylor's Version)":                                           LocationData("Speak Now (Taylor's Version)"),
    "Last Kiss (Taylor's Version)":                                         LocationData("Speak Now (Taylor's Version)"),
    "Ours (Taylor's Version)":                                              LocationData("Speak Now (Taylor's Version)"),
    "Superman (Taylor's Version)":                                          LocationData("Speak Now (Taylor's Version)"),
    "Long Live (Taylor's Version)":                                         LocationData("Speak Now (Taylor's Version)"),
    "Electric Touch (feat. Fall Out Boy) (Taylor's Version) (From The Vault)":                LocationData("Speak Now (Taylor's Version)", True),
    "When Emma Falls in Love (Taylor's Version) (From The Vault)":                             LocationData("Speak Now (Taylor's Version)", True),
    "I Can See You (Taylor's Version) (From The Vault)":                                       LocationData("Speak Now (Taylor's Version)", True),
    "Castles Crumbling (feat. Hayley Williams) (Taylor's Version) (From The Vault)":           LocationData("Speak Now (Taylor's Version)", True),
    "Foolish One (Taylor's Version) (From The Vault)":                                         LocationData("Speak Now (Taylor's Version)", True),
    "Timeless (Taylor's Version) (From The Vault)":                                            LocationData("Speak Now (Taylor's Version)", True),

    # Red
    "State of Grace":                     LocationData("Red"),
    "Red":                                LocationData("Red"),
    "Treacherous":                        LocationData("Red"),
    "I Knew You Were Trouble.":           LocationData("Red"),
    "All Too Well":                       LocationData("Red"),
    "Red - 22":                                 LocationData("Red"),
    "I Almost Do":                        LocationData("Red"),
    "We Are Never Ever Getting Back Together": LocationData("Red"),
    "Stay Stay Stay":                     LocationData("Red"),
    "The Last Time (feat. Gary Lightbody)": LocationData("Red"),
    "Holy Ground":                        LocationData("Red"),
    "Sad Beautiful Tragic":               LocationData("Red"),
    "The Lucky One":                      LocationData("Red"),
    "Everything Has Changed (feat. Ed Sheeran)": LocationData("Red"),
    "Starlight":                          LocationData("Red"),
    "Begin Again":                        LocationData("Red"),
    "The Moment I Knew":                  LocationData("Red", False, True),
    "Come Back... Be Here":               LocationData("Red", False, True),
    "Girl at Home":                       LocationData("Red", False, True),
    "Treacherous (original demo recording)": LocationData("Red", False, True, True),
    "Red (original demo recording)":      LocationData("Red", False, True, True),
    "State of Grace (acoustic version)":  LocationData("Red", False, True, False),

    # Red (Taylor's Version)
    "State of Grace (Taylor's Version)":                                         LocationData("Red (Taylor's Version)"),
    "Red (Taylor's Version)":                                                    LocationData("Red (Taylor's Version)"),
    "Treacherous (Taylor's Version)":                                            LocationData("Red (Taylor's Version)"),
    "I Knew You Were Trouble (Taylor's Version)":                                LocationData("Red (Taylor's Version)"),
    "All Too Well (Taylor's Version)":                                           LocationData("Red (Taylor's Version)"),
    "22 (Taylor's Version)":                                                     LocationData("Red (Taylor's Version)"),
    "I Almost Do (Taylor's Version)":                                            LocationData("Red (Taylor's Version)"),
    "We Are Never Ever Getting Back Together (Taylor's Version)":                LocationData("Red (Taylor's Version)"),
    "Stay Stay Stay (Taylor's Version)":                                         LocationData("Red (Taylor's Version)"),
    "The Last Time (feat. Gary Lightbody) (Taylor's Version)":                   LocationData("Red (Taylor's Version)"),
    "Holy Ground (Taylor's Version)":                                            LocationData("Red (Taylor's Version)"),
    "Sad Beautiful Tragic (Taylor's Version)":                                   LocationData("Red (Taylor's Version)"),
    "The Lucky One (Taylor's Version)":                                          LocationData("Red (Taylor's Version)"),
    "Everything Has Changed (feat. Ed Sheeran) (Taylor's Version)":              LocationData("Red (Taylor's Version)"),
    "Starlight (Taylor's Version)":                                              LocationData("Red (Taylor's Version)"),
    "Begin Again (Taylor's Version)":                                            LocationData("Red (Taylor's Version)"),
    "The Moment I Knew (Taylor's Version)":                                      LocationData("Red (Taylor's Version)"),
    "Come Back... Be Here (Taylor's Version)":                                   LocationData("Red (Taylor's Version)"),
    "Girl at Home (Taylor's Version)":                                           LocationData("Red (Taylor's Version)"),
    "State of Grace (Acoustic Version) (Taylor's Version)":                      LocationData("Red (Taylor's Version)"),
    "Ronan (Taylor's Version)":                                                  LocationData("Red (Taylor's Version)"),
    "Better Man (Taylor's Version) (From The Vault)":                            LocationData("Red (Taylor's Version)", True),
    "Nothing New (feat. Phoebe Bridgers) (Taylor's Version) (From The Vault)":   LocationData("Red (Taylor's Version)", True),
    "Babe (Taylor's Version) (From The Vault)":                                  LocationData("Red (Taylor's Version)", True),
    "Message In A Bottle (Taylor's Version) (From The Vault)":                   LocationData("Red (Taylor's Version)", True),
    "I Bet You Think About Me (feat. Chris Stapleton) (Taylor's Version) (From The Vault)": LocationData("Red (Taylor's Version)", True),
    "Forever Winter (Taylor's Version) (From The Vault)":                        LocationData("Red (Taylor's Version)", True),
    "Run (feat. Ed Sheeran) (Taylor's Version) (From The Vault)":                LocationData("Red (Taylor's Version)", True),
    "The Very First Night (Taylor's Version) (From The Vault)":                  LocationData("Red (Taylor's Version)", True),
    "All Too Well (10 Minute Version) (Taylor's Version) (From The Vault)":      LocationData("Red (Taylor's Version)", True),

    # 1989
    "Welcome to New York":              LocationData("1989"),
    "Blank Space":                      LocationData("1989"),
    "Style":                            LocationData("1989"),
    "Out of the Woods":                 LocationData("1989"),
    "All You Had to Do Was Stay":       LocationData("1989"),
    "Shake It Off":                     LocationData("1989"),
    "I Wish You Would":                 LocationData("1989"),
    "Bad Blood":                        LocationData("1989"),
    "Wildest Dreams":                   LocationData("1989"),
    "How You Get the Girl":             LocationData("1989"),
    "This Love":                        LocationData("1989"),
    "I Know Places":                    LocationData("1989"),
    "Clean":                            LocationData("1989"),
    "Wonderland":                       LocationData("1989", False, True),
    "You Are in Love":                  LocationData("1989", False, True),
    "New Romantics":                    LocationData("1989", False, True),
    "I Know Places - Voice Memo":       LocationData("1989", False, True, True),
    "I Wish You Would - Voice Memo":    LocationData("1989", False, True, True),
    "Blank Space - Voice Memo":         LocationData("1989", False, True, True),

    # 1989 (Taylor's Version)
    "Welcome to New York (Taylor's Version)":                                   LocationData("1989 (Taylor's Version)"),
    "Blank Space (Taylor's Version)":                                           LocationData("1989 (Taylor's Version)"),
    "Style (Taylor's Version)":                                                 LocationData("1989 (Taylor's Version)"),
    "Out of the Woods (Taylor's Version)":                                      LocationData("1989 (Taylor's Version)"),
    "All You Had to Do Was Stay (Taylor's Version)":                            LocationData("1989 (Taylor's Version)"),
    "Shake It Off (Taylor's Version)":                                          LocationData("1989 (Taylor's Version)"),
    "I Wish You Would (Taylor's Version)":                                      LocationData("1989 (Taylor's Version)"),
    "Bad Blood (Taylor's Version)":                                             LocationData("1989 (Taylor's Version)"),
    "Wildest Dreams (Taylor's Version)":                                        LocationData("1989 (Taylor's Version)"),
    "How You Get the Girl (Taylor's Version)":                                  LocationData("1989 (Taylor's Version)"),
    "This Love (Taylor's Version)":                                             LocationData("1989 (Taylor's Version)"),
    "I Know Places (Taylor's Version)":                                         LocationData("1989 (Taylor's Version)"),
    "Clean (Taylor's Version)":                                                 LocationData("1989 (Taylor's Version)"),
    "Wonderland (Taylor's Version)":                                            LocationData("1989 (Taylor's Version)"),
    "You Are in Love (Taylor's Version)":                                       LocationData("1989 (Taylor's Version)"),
    "New Romantics (Taylor's Version)":                                         LocationData("1989 (Taylor's Version)"),
    "\"Slut!\" (Taylor's Version) (From The Vault)":                            LocationData("1989 (Taylor's Version)", True),
    "Say Don't Go (Taylor's Version) (From The Vault)":                         LocationData("1989 (Taylor's Version)", True),
    "Now That We Don't Talk (Taylor's Version) (From The Vault)":               LocationData("1989 (Taylor's Version)", True),
    "Suburban Legends (Taylor's Version) (From The Vault)":                     LocationData("1989 (Taylor's Version)", True),
    "Is It Over Now? (Taylor's Version) (From The Vault)":                      LocationData("1989 (Taylor's Version)", True),
    "Bad Blood (feat. Kendrick Lamar) (Taylor's Version)":                      LocationData("1989 (Taylor's Version)", False, True),

    # Reputation
    "...Ready for It?":                LocationData("Reputation"),
    "End Game (feat. Ed Sheeran & Future)": LocationData("Reputation"),
    "I Did Something Bad":             LocationData("Reputation"),
    "Don't Blame Me":                  LocationData("Reputation"),
    "Delicate":                        LocationData("Reputation"),
    "Look What You Made Me Do":        LocationData("Reputation"),
    "So It Goes...":                   LocationData("Reputation"),
    "Gorgeous":                        LocationData("Reputation"),
    "Getaway Car":                     LocationData("Reputation"),
    "King of My Heart":                LocationData("Reputation"),
    "Dancing with Our Hands Tied":     LocationData("Reputation"),
    "Dress":                           LocationData("Reputation"),
    "This Is Why We Can't Have Nice Things": LocationData("Reputation"),
    "Call It What You Want":           LocationData("Reputation"),
    "New Year's Day":                  LocationData("Reputation"),

    # Lover
    "I Forgot That You Existed":       LocationData("Lover"),
    "Cruel Summer":                    LocationData("Lover"),
    "Lover":                           LocationData("Lover"),
    "The Man":                         LocationData("Lover"),
    "The Archer":                      LocationData("Lover"),
    "I Think He Knows":                LocationData("Lover"),
    "Miss Americana & The Heartbreak Prince": LocationData("Lover"),
    "Paper Rings":                     LocationData("Lover"),
    "Cornelia Street":                 LocationData("Lover"),
    "Death By A Thousand Cuts":        LocationData("Lover"),
    "London Boy":                      LocationData("Lover"),
    "Soon You'll Get Better (feat. Dixie Chicks)": LocationData("Lover"),
    "False God":                       LocationData("Lover"),
    "You Need to Calm Down":           LocationData("Lover"),
    "Afterglow":                       LocationData("Lover"),
    "ME! (feat. Brendon Urie)":        LocationData("Lover"),
    "It's Nice to Have a Friend":      LocationData("Lover"),
    "Daylight":                        LocationData("Lover"),

    # Folklore
    "the 1":                           LocationData("Folklore"),
    "cardigan":                        LocationData("Folklore"),
    "the last great american dynasty": LocationData("Folklore"),
    "exile (feat. Bon Iver)":          LocationData("Folklore"),
    "my tears ricochet":               LocationData("Folklore"),
    "mirrorball":                      LocationData("Folklore"),
    "seven":                           LocationData("Folklore"),
    "august":                          LocationData("Folklore"),
    "this is me trying":               LocationData("Folklore"),
    "illicit affairs":                 LocationData("Folklore"),
    "invisible string":                LocationData("Folklore"),
    "mad woman":                       LocationData("Folklore"),
    "epiphany":                        LocationData("Folklore"),
    "betty":                           LocationData("Folklore"),
    "peace":                           LocationData("Folklore"),
    "hoax":                            LocationData("Folklore"),
    "the lakes (bonus track)":         LocationData("Folklore", False, True),

    # Evermore
    "willow":                          LocationData("Evermore"),
    "champagne problems":              LocationData("Evermore"),
    "gold rush":                       LocationData("Evermore"),
    "'tis the damn season":            LocationData("Evermore"),
    "tolerate it":                     LocationData("Evermore"),
    "no body, no crime (feat. HAIM)":  LocationData("Evermore"),
    "happiness":                       LocationData("Evermore"),
    "dorothea":                        LocationData("Evermore"),
    "coney island (feat. The National)": LocationData("Evermore"),
    "ivy":                             LocationData("Evermore"),
    "cowboy like me":                  LocationData("Evermore"),
    "long story short":                LocationData("Evermore"),
    "marjorie":                        LocationData("Evermore"),
    "closure":                         LocationData("Evermore"),
    "evermore (feat. Bon Iver)":       LocationData("Evermore"),
    "right where you left me (bonus track)": LocationData("Evermore", False, True),
    "it's time to go (bonus track)":   LocationData("Evermore", False, True),

    # Midnights
    "Lavender Haze":                   LocationData("Midnights"),
    "Maroon":                          LocationData("Midnights"),
    "Anti-Hero":                       LocationData("Midnights"),
    "Snow On The Beach (feat. Lana Del Rey)": LocationData("Midnights"),
    "You're On Your Own, Kid":         LocationData("Midnights"),
    "Midnight Rain":                   LocationData("Midnights"),
    "Question...?":                    LocationData("Midnights"),
    "Vigilante Shit":                  LocationData("Midnights"),
    "Bejeweled":                       LocationData("Midnights"),
    "Labyrinth":                       LocationData("Midnights"),
    "Karma":                           LocationData("Midnights"),
    "Sweet Nothing":                   LocationData("Midnights"),
    "Mastermind":                      LocationData("Midnights"),
    "The Great War":                   LocationData("Midnights", False, True),
    "Bigger Than The Whole Sky":       LocationData("Midnights", False, True),
    "Paris":                           LocationData("Midnights", False, True),
    "High Infidelity":                 LocationData("Midnights", False, True),
    "Glitch":                          LocationData("Midnights", False, True),
    "Would've, Could've, Should've":   LocationData("Midnights", False, True),
    "Dear Reader":                     LocationData("Midnights", False, True),
    "Hits Different":                  LocationData("Midnights", False, True),
    "Snow On The Beach (feat. More Lana Del Rey)": LocationData("Midnights", False, True),
    "Karma (feat. Ice Spice)":         LocationData("Midnights", False, True),

    # The Tortured Poets Department
    "Fortnight (feat. Post Malone)":   LocationData("The Tortured Poets Department"),
    "The Tortured Poets Department":   LocationData("The Tortured Poets Department"),
    "My Boy Only Breaks His Favorite Toys": LocationData("The Tortured Poets Department"),
    "Down Bad":                        LocationData("The Tortured Poets Department"),
    "So Long, London":                 LocationData("The Tortured Poets Department"),
    "But Daddy I Love Him":            LocationData("The Tortured Poets Department"),
    "Fresh Out the Slammer":           LocationData("The Tortured Poets Department"),
    "Florida!!! (feat. Florence + The Machine)": LocationData("The Tortured Poets Department"),
    "Guilty as Sin?":                  LocationData("The Tortured Poets Department"),
    "Who's Afraid of Little Old Me?":  LocationData("The Tortured Poets Department"),
    "I Can Fix Him (No Really I Can)": LocationData("The Tortured Poets Department"),
    "loml":                            LocationData("The Tortured Poets Department"),
    "I Can Do It With a Broken Heart": LocationData("The Tortured Poets Department"),
    "The Smallest Man Who Ever Lived": LocationData("The Tortured Poets Department"),
    "The Alchemy":                     LocationData("The Tortured Poets Department"),
    "Clara Bow":                       LocationData("The Tortured Poets Department"),
    "The Black Dog":                   LocationData("The Tortured Poets Department", False, True),
    "imgonnagetyouback":               LocationData("The Tortured Poets Department", False, True),
    "The Albatross":                   LocationData("The Tortured Poets Department", False, True),
    "Chloe or Sam or Sophia or Marcus": LocationData("The Tortured Poets Department", False, True),
    "How Did It End?":                 LocationData("The Tortured Poets Department", False, True),
    "So High School":                  LocationData("The Tortured Poets Department", False, True),
    "I Hate It Here":                  LocationData("The Tortured Poets Department", False, True),
    "thanK you aIMee":                 LocationData("The Tortured Poets Department", False, True),
    "I Look in People's Windows":      LocationData("The Tortured Poets Department", False, True),
    "The Prophecy":                    LocationData("The Tortured Poets Department", False, True),
    "Cassandra":                       LocationData("The Tortured Poets Department", False, True),
    "Peter":                           LocationData("The Tortured Poets Department", False, True),
    "The Bolter":                      LocationData("The Tortured Poets Department", False, True),
    "Robin":                           LocationData("The Tortured Poets Department", False, True),
    "The Manuscript":                  LocationData("The Tortured Poets Department", False, True),

    # The Life of a Showgirl
    "The Fate of Ophelia":             LocationData("The Life of a Showgirl"),
    "Elizabeth Taylor":                LocationData("The Life of a Showgirl"),
    "Opalite":                         LocationData("The Life of a Showgirl"),
    "Father Figure":                   LocationData("The Life of a Showgirl"),
    "Eldest Daughter":                 LocationData("The Life of a Showgirl"),
    "Ruin The Friendship":             LocationData("The Life of a Showgirl"),
    "Actually Romantic":               LocationData("The Life of a Showgirl"),
    "Wi$h Li$t":                       LocationData("The Life of a Showgirl"),
    "Wood":                            LocationData("The Life of a Showgirl"),
    "CANCELLED!":                      LocationData("The Life of a Showgirl"),
    "Honey":                           LocationData("The Life of a Showgirl"),
    "The Life of a Showgirl (feat. Sabrina Carpenter)": LocationData("The Life of a Showgirl"),
    "Patient Zero": LocationData("The Life of a Showgirl", False, True, False),
    "Cleveland!": LocationData("The Life of a Showgirl", False, True, False),
    "Pink Clouding": LocationData("The Life of a Showgirl", False, True, False),
    "Babylon": LocationData("The Life of a Showgirl", False, True, False)
}

LOCATION_NAME_TO_ID = {
    name: 1989 + i for i, name in enumerate(LOCATION_TABLE)
}

REGIONS: dict[str, list[str]] = {}
for name, data in LOCATION_TABLE.items():
    REGIONS.setdefault(data.region, []).append(name)


def create_all_locations(world: TaylorSwiftWorld) -> None:
    for region_name, location_names in REGIONS.items():
        try:
            region = world.get_region(region_name)
        except KeyError:
            continue
        for loc_name in location_names:
            if LOCATION_TABLE[loc_name].vault and not world.options.include_vault_tracks.value:
                continue
            if LOCATION_TABLE[loc_name].deluxe and not world.options.include_deluxe.value:
                continue
            if LOCATION_TABLE[loc_name].extra and not world.options.include_extra.value:
                continue
            loc = TaylorSwiftLocation(
                world.player,
                loc_name,
                LOCATION_NAME_TO_ID[loc_name],
                region,
            )
            region.locations.append(loc)
