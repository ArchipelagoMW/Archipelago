from ..bases import SVTestBase
from ... import options
from ...locations import locations_by_tag, LocationTags, location_table
from ...strings.entrance_names import Entrance
from ...strings.region_names import Region


class TestDonationLogicAll(SVTestBase):
    options = {
        options.Museumsanity.internal_name: options.Museumsanity.option_all
    }

    def test_cannot_make_any_donation_without_museum_access(self):
        railroad_item = "Railroad Boulder Removed"
        swap_museum_and_bathhouse(self.multiworld, self.player)
        self.collect_all_except(railroad_item)

        for donation in locations_by_tag[LocationTags.MUSEUM_DONATIONS]:
            self.assert_cannot_reach_location(donation.name)

        self.multiworld.state.collect(self.create_item(railroad_item))

        for donation in locations_by_tag[LocationTags.MUSEUM_DONATIONS]:
            self.assert_can_reach_location(donation.name)


class TestDonationLogicRandomized(SVTestBase):
    options = {
        options.Museumsanity.internal_name: options.Museumsanity.option_randomized
    }

    def test_cannot_make_any_donation_without_museum_access(self):
        railroad_item = "Railroad Boulder Removed"
        swap_museum_and_bathhouse(self.multiworld, self.player)
        self.collect_all_except(railroad_item)
        donation_locations = [location for location in self.get_real_locations() if
                              LocationTags.MUSEUM_DONATIONS in location_table[location.name].tags]

        for donation in donation_locations:
            self.assert_cannot_reach_location(donation.name)

        self.multiworld.state.collect(self.create_item(railroad_item))

        for donation in donation_locations:
            self.assert_can_reach_location(donation.name)


class TestDonationLogicMilestones(SVTestBase):
    options = {
        options.Museumsanity.internal_name: options.Museumsanity.option_milestones
    }

    def test_cannot_make_any_donation_without_museum_access(self):
        railroad_item = "Railroad Boulder Removed"
        swap_museum_and_bathhouse(self.multiworld, self.player)
        self.collect_all_except(railroad_item)

        for donation in locations_by_tag[LocationTags.MUSEUM_MILESTONES]:
            self.assert_cannot_reach_location(donation.name)

        self.multiworld.state.collect(self.create_item(railroad_item))

        for donation in locations_by_tag[LocationTags.MUSEUM_MILESTONES]:
            self.assert_can_reach_location(donation.name)


def swap_museum_and_bathhouse(multiworld, player):
    museum_region = multiworld.get_region(Region.museum, player)
    bathhouse_region = multiworld.get_region(Region.bathhouse_entrance, player)
    museum_entrance = multiworld.get_entrance(Entrance.town_to_museum, player)
    bathhouse_entrance = multiworld.get_entrance(Entrance.enter_bathhouse_entrance, player)
    museum_entrance.connect(bathhouse_region)
    bathhouse_entrance.connect(museum_region)
