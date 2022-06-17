from ..generic.Rules import set_rule, add_rule
from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin


class Psychonauts2Logic(LogicMixin):
    # PSI Powers
    def _pn2_has_telekinesis(self, player: int):
        return self.has('Telekinesis', player)

    def _pn2_has_psi_blast(self, player: int):
        return self.has('PSI Blast', player)

    def _pn2_has_pyrokinesis(self, player: int):
        return self.has('Pyrokinesis', player)

    def _pn2_has_levitation(self, player: int):
        return self.has('Levitation', player)

    def _pn2_has_clairvoyance(self, player: int):
        return self.has('Clairvoyance', player)

    def _pn2_has_mental_connection(self, player: int):
        return self.has('Mental Connection', player)

    def _pn2_has_time_bubble(self, player: int):
        return self.has('Time Bubble', player)

    def _pn2_has_projection(self, player: int):
        return self.has('Projection', player)

    # Other important items / upgrades
    def _pn2_has_thought_tuner(self, player: int):
        return self.has('Thought Tuner', player)

    def _pn2_has_helmuts_brain(self, player: int):
        return self.has('Brain in a Jar', player)

    def _pn2_has_bee_jar(self, player: int):
        return self.has('Empty Specimen Jar', player)

    def _pn2_has_bowling_card(self, player: int):
        return self.has('Senior League Membership Card', player)

    # Completed levels
    def _pn2_can_complete_loboto(self, player: int):
        return self.can_reach('End Loboto', 'Region', player)

    def _pn2_can_complete_psi_king(self, player: int):
        return self.can_reach('End Helmut', 'Region', player)

    def _pn2_can_complete_compton(self, player: int):
        return self.can_reach('End Compton', 'Region', player)

    def _pn2_can_complete_ford_mail(self, player: int):
        return self.can_reach('End Ford Mail', 'Region', player)

    def _pn2_can_complete_ford_bowling(self, player: int):
        return self.can_reach('End Ford Bowling', 'Region', player)

    def _pn2_can_complete_ford_haircut(self, player: int):
        return self.can_reach('End Ford Haircut', 'Region', player)

    def _pn2_can_complete_ford_tomb(self, player: int):
        return self.can_reach('End Ford Tomb', 'Region', player)

    def _pn2_can_complete_cassie(self, player: int):
        return self.can_reach('End Cassie', 'Region', player)

    def _pn2_can_complete_bob(self, player: int):
        return self.can_reach('End Bob', 'Region', player)

    def _pn2_can_complete_lucrecia(self, player: int):
        return self.can_reach('End Lucrecia', 'Region', player)

    def _pn2_can_complete_gristol(self, player: int):
        return self.can_reach('End Gristol', 'Region', player)


def set_location_rules(world: MultiWorld, player: int):

    # Overworld Entrances
    set_rule(world.get_entrance('To Gulch', player), lambda state: state._pn2_can_complete_ford_tomb(player))
    set_rule(world.get_entrance('Gulch Tumbler', player), lambda state: state._pn2_can_complete_ford_tomb(player))

    # The Motherlobe Collectibles
    set_rule(world.get_location("The Motherlobe: PSI Card - Floating Platform 1", player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_thought_tuner(player))
    set_rule(world.get_location("The Motherlobe: PSI Card - Floating Platform 2", player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_thought_tuner(player))
    set_rule(world.get_location("The Motherlobe: PSI Card - Astral Lanes Behind Counter", player), lambda state: state._pn2_has_bowling_card(player))
    set_rule(world.get_location("The Motherlobe: PSI Card - Astral Lanes Left Lane", player), lambda state: state._pn2_has_bowling_card(player))
    set_rule(world.get_location("The Motherlobe: Supply Chest - Artifact Storage", player), lambda state: state._pn2_has_pyrokinesis(player))
    set_rule(world.get_location("The Motherlobe: Supply Chest - Mailroom Office", player), lambda state: state._pn2_can_complete_psi_king(player))
    set_rule(world.get_location("The Motherlobe: Supply Chest - Nerve Center Above Elevator", player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_thought_tuner(player))
    set_rule(world.get_location("The Motherlobe: Supply Chest - Astral Lanes Right Lane", player), lambda state: state._pn2_has_bowling_card(player))
    set_rule(world.get_location("The Motherlobe: Supply Chest Key - Artifact Storage", player), lambda state: state._pn2_has_pyrokinesis(player))
    set_rule(world.get_location("The Motherlobe: Supply Chest Key - Mailroom Spinning Fan", player), lambda state: state._pn2_has_time_bubble(player))
    set_rule(world.get_location("The Motherlobe: PSI Challenge Marker - Floating Platform", player), lambda state: state._pn2_has_levitation(player))
    set_rule(world.get_location("The Motherlobe: PSI Challenge Marker - Mailroom Behind Narrow Door", player), lambda state: state._pn2_has_projection(player))
    set_rule(world.get_location("The Motherlobe: PSI Challenge Marker - Astral Lanes Spinning Sign", player), lambda state: state._pn2_has_bowling_card(player))

    # The Quarry Collectibles
    set_rule(world.get_location("The Quarry: PSI Card - Root Cave 1", player), lambda state: state._pn2_has_pyrokinesis(player))
    set_rule(world.get_location("The Quarry: PSI Card - Root Cave 2", player), lambda state: state._pn2_has_pyrokinesis(player))
    set_rule(world.get_location("The Quarry: PSI Card - Otto's Lab Spinning Fan", player), lambda state: state._pn2_has_time_bubble(player))
    set_rule(world.get_location("The Quarry: Supply Chest Key - Otto's Lab Spinning Fan", player), lambda state: state._pn2_has_time_bubble(player))
    set_rule(world.get_location("The Quarry: PSI Challenge Marker - Top of Psychoisolation", player), lambda state: state._pn2_has_levitation(player))
    set_rule(world.get_location("The Quarry: PSI Challenge Marker - Top of Otto's Lab", player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_thought_tuner(player))
    set_rule(world.get_location("The Quarry: PSI Challenge Marker - Behind the Motherlobe", player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_thought_tuner(player))
    set_rule(world.get_location("The Quarry: PSI Challenge Marker - Pillar in the Water", player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_thought_tuner(player))
    set_rule(world.get_location("Get Senior League Membership Card", player), lambda state: state._pn2_has_bee_jar(player) and state._pn2_can_complete_compton(player))

    # The Questionable Area? Collectibles
    set_rule(world.get_location("The Questionable Area?: PSI Card - Behind Sassclops Sign", player), lambda state: state._pn2_has_pyrokinesis(player))
    set_rule(world.get_location("The Questionable Area?: PSI Card - Playground Thoughts", player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_thought_tuner(player))
    set_rule(world.get_location("The Questionable Area?: PSI Card - Old Gift Shop", player), lambda state: state._pn2_has_telekinesis(player) or state._pn2_has_time_bubble(player))
    set_rule(world.get_location("The Questionable Area?: PSI Card - Near Old Gift Shop", player), lambda state: state._pn2_has_telekinesis(player) or state._pn2_has_time_bubble(player))
    set_rule(world.get_location("The Questionable Area?: PSI Card - Near Waterfall 1", player), lambda state: state._pn2_has_telekinesis(player) or state._pn2_has_time_bubble(player))
    set_rule(world.get_location("The Questionable Area?: PSI Card - Near Waterfall 2", player), lambda state: (state._pn2_has_telekinesis(player) and state._pn2_has_psi_blast(player)) or state._pn2_has_time_bubble(player))
    set_rule(world.get_location("The Questionable Area?: Supply Chest - Aquato Campfire", player), lambda state: state._pn2_has_pyrokinesis(player) and state._pn2_has_levitation(player))
    set_rule(world.get_location("The Questionable Area?: Supply Chest - Behind the Waterfall", player), lambda state: state._pn2_has_time_bubble(player))
    set_rule(world.get_location("The Questionable Area?: Supply Chest Key - Aquato Campfire", player), lambda state: state._pn2_has_pyrokinesis(player) and state._pn2_has_levitation(player))
    set_rule(world.get_location("The Questionable Area?: Supply Chest Key - Funicular Ride", player), lambda state: state._pn2_has_telekinesis(player) or state._pn2_has_time_bubble(player))
    set_rule(world.get_location("The Questionable Area?: PSI Challenge Marker - Diner Sign", player), lambda state: state._pn2_has_psi_blast(player))
    set_rule(world.get_location("The Questionable Area?: PSI Challenge Marker - On Top of Aquatodome", player), lambda state: state._pn2_has_psi_blast(player))
    set_rule(world.get_location("The Questionable Area?: PSI Challenge Marker - Inside the Aquatodome", player), lambda state: state._pn2_has_psi_blast(player))
    set_rule(world.get_location("The Questionable Area?: PSI Challenge Marker - Behind Sassclops Sign", player), lambda state: state._pn2_has_pyrokinesis(player))
    set_rule(world.get_location("The Questionable Area?: PSI Challenge Marker - Playground Thoughts", player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_thought_tuner(player))
    set_rule(world.get_location("The Questionable Area?: PSI Challenge Marker - On Top of Old Gift Shop", player), lambda state: state._pn2_has_telekinesis(player) or state._pn2_has_time_bubble(player))
    set_rule(world.get_location("The Questionable Area?: PSI Challenge Marker - Complete Queepie's Quest", player), lambda state: state._pn2_has_pyrokinesis(player) and state._pn2_has_levitation(player))

    # Green Needle Gulch Collectibles
    set_rule(world.get_location("Green Needle Gulch: PSI Card - Roof of River House", player), lambda state: state._pn2_has_pyrokinesis(player) and state._pn2_has_levitation(player))
    set_rule(world.get_location("Green Needle Gulch: PSI Card - On Top of Old Treehouse", player), lambda state: state._pn2_has_levitation(player))
    set_rule(world.get_location("Green Needle Gulch: PSI Card - Old Treehouse Thoughts", player), lambda state: state._pn2_has_levitation(player) and state._pn2_has_mental_connection(player) and state._pn2_has_thought_tuner(player))
    set_rule(world.get_location("Green Needle Gulch: PSI Card - Giant Vine 1", player), lambda state: state._pn2_has_psi_blast(player))
    set_rule(world.get_location("Green Needle Gulch: PSI Card - Giant Vine 2", player), lambda state: state._pn2_has_psi_blast(player))
    set_rule(world.get_location("Green Needle Gulch: PSI Card - Near Greenhouse", player), lambda state: state._pn2_has_psi_blast(player))
    set_rule(world.get_location("Green Needle Gulch: PSI Card - Near Otto's Old Workshop", player), lambda state: state._pn2_has_psi_blast(player))
    set_rule(world.get_location("Green Needle Gulch: PSI Card - Inside Cassie's House", player), lambda state: state._pn2_has_levitation(player))
    set_rule(world.get_location("Green Needle Gulch: PSI Card - Pillar Surrounded by Honey", player), lambda state: state._pn2_has_telekinesis(player))
    set_rule(world.get_location("Green Needle Gulch: Supply Chest - Cassie's House Narrow Door", player), lambda state: state._pn2_has_projection(player))
    set_rule(world.get_location("Green Needle Gulch: Supply Chest Key - Beaver's Treasure", player), lambda state: state._pn2_has_clairvoyance(player))
    set_rule(world.get_location("Green Needle Gulch: Supply Chest Key - Otto's Old Workshop", player), lambda state: state._pn2_has_psi_blast(player))
    set_rule(world.get_location("Green Needle Gulch: PSI Challenge Marker - Tree Stump Thoughts", player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_thought_tuner(player))
    set_rule(world.get_location("Green Needle Gulch: PSI Challenge Marker - Outhouse Narrow Door", player), lambda state: state._pn2_has_projection(player))
    set_rule(world.get_location("Green Needle Gulch: PSI Challenge Marker - Old Treehouse Thoughts", player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_thought_tuner(player))

    # Loboto's Labyrinth Entrances
    set_rule(world.get_entrance('Enter Loboto', player), lambda state: state._pn2_has_mental_connection(player))
    set_rule(world.get_entrance('To Loboto Central Office', player), lambda state: state._pn2_has_telekinesis(player))
    set_rule(world.get_entrance('To Loboto Conference Room', player), lambda state: state._pn2_has_telekinesis(player))
    set_rule(world.get_entrance('To Loboto Poster Gallery', player), lambda state: state._pn2_has_psi_blast(player))
    set_rule(world.get_entrance('To Loboto Dental Void', player), lambda state: state._pn2_has_pyrokinesis(player))
    set_rule(world.get_entrance('To Loboto Asylum', player), lambda state: state._pn2_has_levitation(player))
    set_rule(world.get_entrance('End Loboto', player), lambda state: True)

    # Loboto's Labyrinth Collectibles
    set_rule(world.get_location("Learn PSI Blast", player), lambda state: state._pn2_has_telekinesis(player))
    set_rule(world.get_location("Learn Pyrokinesis", player), lambda state: state._pn2_has_telekinesis(player) and state._pn2_has_psi_blast(player))
    set_rule(world.get_location("Learn Levitation", player), lambda state: state._pn2_has_telekinesis(player) and state._pn2_has_psi_blast(player) and state._pn2_has_pyrokinesis(player))
    set_rule(world.get_location("Loboto's Labyrinth: Nugget of Wisdom 1", player), lambda state: state._pn2_can_complete_loboto(player) and state._pn2_has_pyrokinesis(player))
    set_rule(world.get_location("Loboto's Labyrinth: Nugget of Wisdom 2", player), lambda state: state._pn2_can_complete_loboto(player) and state._pn2_has_telekinesis(player))
    set_rule(world.get_location("Loboto's Labyrinth: Steamer Trunk", player), lambda state: state._pn2_has_mental_connection(player) and state.has("Steamer Trunk Tag (Loboto's Labyrinth)", player))
    set_rule(world.get_location("Loboto's Labyrinth: Steamer Trunk Tag", player), lambda state: state._pn2_has_mental_connection(player))
    set_rule(world.get_location("Loboto's Labyrinth: Dufflebag", player), lambda state: state.has("Dufflebag Tag (Loboto's Labyrinth)", player))
    set_rule(world.get_location("Loboto's Labyrinth: Suitcase", player), lambda state: state._pn2_has_pyrokinesis(player) and state.has("Suitcase Tag (Loboto's Labyrinth)", player))
    set_rule(world.get_location("Loboto's Labyrinth: Hatbox", player), lambda state: state._pn2_has_pyrokinesis(player) and state.has("Hatbox Tag (Loboto's Labyrinth)", player))
    set_rule(world.get_location("Loboto's Labyrinth: Purse", player), lambda state: state._pn2_can_complete_loboto(player) and state.has("Purse Tag (Loboto's Labyrinth)", player))
    set_rule(world.get_location("Loboto's Labyrinth: Purse Tag", player), lambda state: state._pn2_has_levitation(player))
    set_rule(world.get_location("Loboto's Labyrinth: Memory Vault 2", player), lambda state: state._pn2_has_mental_connection(player))

    # Hollis' Classroom Entrances
    set_rule(world.get_entrance('Enter Hollis 1', player), lambda state: state._pn2_has_mental_connection(player))
    set_rule(world.get_entrance('To Hollis 1 Parking Lot', player), lambda state: state._pn2_has_mental_connection(player))
    set_rule(world.get_entrance('To Hollis 1 Morgue', player), lambda state: True)
    set_rule(world.get_entrance('To Hollis 1 Final', player), lambda state: state._pn2_has_mental_connection(player))
    set_rule(world.get_entrance('End Hollis 1', player), lambda state: state._pn2_has_mental_connection(player))

    # Hollis' Classroom Collectibles
    set_rule(world.get_location("Hollis' Classroom: Nugget of Wisdom 1", player), lambda state: state._pn2_has_mental_connection(player))
    set_rule(world.get_location("Hollis' Classroom: Half-A-Mind 2", player), lambda state: state._pn2_has_mental_connection(player))
    set_rule(world.get_location("Hollis' Classroom: Steamer Trunk", player), lambda state: state.has("Steamer Trunk Tag (Hollis' Classroom)", player))
    set_rule(world.get_location("Hollis' Classroom: Hatbox", player), lambda state: state.has("Hatbox Tag (Hollis' Classroom)", player))

    # Hollis' Hot Streak Entrances
    set_rule(world.get_entrance('Enter Hollis 2', player), lambda state: state._pn2_has_mental_connection(player))
    set_rule(world.get_entrance('To Hollis 2 Parking Lot', player), lambda state: state._pn2_has_mental_connection(player))
    set_rule(world.get_entrance('To Hollis 2 Morgue', player), lambda state: True)
    set_rule(world.get_entrance('To Hollis 2 Maternity', player), lambda state: True)
    set_rule(world.get_entrance('To Hollis 2 Pharmacy', player), lambda state: True)
    set_rule(world.get_entrance('To Hollis 2 Cardiology', player), lambda state: True)
    set_rule(world.get_entrance('To Hollis 2 Doctors Only', player), lambda state: True)
    set_rule(world.get_entrance('To Hollis 2 Records', player), lambda state: True)
    set_rule(world.get_entrance('To Hollis 2 Maternity Back', player), lambda state: state._pn2_has_mental_connection(player))
    set_rule(world.get_entrance('To Hollis 2 Pharmacy Back', player), lambda state: state._pn2_has_mental_connection(player))
    set_rule(world.get_entrance('To Hollis 2 Cardiology Back', player), lambda state: state._pn2_has_mental_connection(player))
    set_rule(world.get_entrance('To Hollis 2 Boss', player), lambda state: state._pn2_has_mental_connection(player))
    set_rule(world.get_entrance('End Hollis 2', player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_psi_blast(player) and state._pn2_has_telekinesis(player))

    # Hollis' Hot Streak Collectibles
    set_rule(world.get_location("Hollis' Hot Streak: Nugget of Wisdom 2", player), lambda state: state._pn2_has_pyrokinesis(player))
    set_rule(world.get_location("Hollis' Hot Streak: Nugget of Wisdom 3", player), lambda state: state._pn2_has_mental_connection(player)) # tracking & randomization of PSI powers is not yet implemented, though this would require Dark Thoughts
    set_rule(world.get_location("Hollis' Hot Streak: Nugget of Wisdom 4", player), lambda state: state._pn2_has_projection(player))
    set_rule(world.get_location("Hollis' Hot Streak: Half-A-Mind 1", player), lambda state: state._pn2_has_mental_connection(player) or state._pn2_has_levitation(player))
    set_rule(world.get_location("Hollis' Hot Streak: Half-A-Mind 2", player), lambda state: state._pn2_has_mental_connection(player))
    set_rule(world.get_location("Hollis' Hot Streak: Half-A-Mind 3", player), lambda state: state._pn2_has_mental_connection(player))
    set_rule(world.get_location("Hollis' Hot Streak: Half-A-Mind 4", player), lambda state: state._pn2_has_levitation(player))
    set_rule(world.get_location("Hollis' Hot Streak: Dufflebag", player), lambda state: state._pn2_has_mental_connection(player) and state.has("Dufflebag Tag (Hollis' Hot Streak)", player)) # tracking & randomization of PSI powers is not yet implemented, though this would require Dark Thoughts
    set_rule(world.get_location("Hollis' Hot Streak: Dufflebag Tag", player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_levitation(player))
    set_rule(world.get_location("Hollis' Hot Streak: Suitcase", player), lambda state: state.has("Suitcase Tag (Hollis' Hot Streak)", player))
    set_rule(world.get_location("Hollis' Hot Streak: Purse", player), lambda state: state.has("Purse Tag (Hollis' Hot Streak)", player))
    set_rule(world.get_location("Hollis' Hot Streak: Purse Tag", player), lambda state: state._pn2_has_mental_connection(player))

    # PSI King's Sensorium Entrances
    set_rule(world.get_entrance('Enter Helmut', player), lambda state: state._pn2_has_helmuts_brain(player))
    set_rule(world.get_entrance('To PSI King Eye Shrine', player), lambda state: True)
    set_rule(world.get_entrance('To PSI King Backstage', player), lambda state: state._pn2_has_time_bubble(player))
    set_rule(world.get_entrance('To PSI King Concessions', player), lambda state: state._pn2_has_time_bubble(player))
    set_rule(world.get_entrance('To PSI King Nose Mouth Shrine', player), lambda state: True)
    set_rule(world.get_entrance('To PSI King Campgrounds', player), lambda state: state._pn2_has_time_bubble(player))
    set_rule(world.get_entrance('To PSI King Hand Ear Shrine', player), lambda state: state._pn2_has_time_bubble(player))
    set_rule(world.get_entrance('To PSI King End', player), lambda state: state._pn2_has_time_bubble(player) and state._pn2_has_mental_connection(player) and state._pn2_has_telekinesis(player))
    set_rule(world.get_entrance('End Helmut', player), lambda state: state._pn2_has_time_bubble(player))

    # PSI King's Sensorium Collectibles
    set_rule(world.get_location("PSI King's Sensorium: Nugget of Wisdom 1", player), lambda state: state._pn2_has_time_bubble(player))
    set_rule(world.get_location("PSI King's Sensorium: Nugget of Wisdom 2", player), lambda state: state._pn2_has_time_bubble(player))
    set_rule(world.get_location("PSI King's Sensorium: Half-A-Mind 1", player), lambda state: state._pn2_has_pyrokinesis(player))
    set_rule(world.get_location("PSI King's Sensorium: Half-A-Mind 2", player), lambda state: state._pn2_has_time_bubble(player))
    set_rule(world.get_location("PSI King's Sensorium: Half-A-Mind 3", player), lambda state: state._pn2_has_time_bubble(player))
    set_rule(world.get_location("PSI King's Sensorium: Half-A-Mind 4", player), lambda state: state._pn2_has_time_bubble(player))
    set_rule(world.get_location("PSI King's Sensorium: Steamer Trunk", player), lambda state: state._pn2_has_time_bubble(player) and state.has("Steamer Trunk Tag (PSI King's Sensorium)", player))
    set_rule(world.get_location("PSI King's Sensorium: Steamer Trunk Tag", player), lambda state: state._pn2_has_time_bubble(player))
    set_rule(world.get_location("PSI King's Sensorium: Dufflebag", player), lambda state: state.has("Dufflebag Tag (PSI King's Sensorium)", player))
    set_rule(world.get_location("PSI King's Sensorium: Suitcase", player), lambda state: state.has("Suitcase Tag (PSI King's Sensorium)", player))
    set_rule(world.get_location("PSI King's Sensorium: Suitcase Tag", player), lambda state: state._pn2_has_time_bubble(player))
    set_rule(world.get_location("PSI King's Sensorium: Hatbox", player), lambda state: state.has("Hatbox Tag (PSI King's Sensorium)", player))
    set_rule(world.get_location("PSI King's Sensorium: Hatbox Tag", player), lambda state: state._pn2_has_time_bubble(player) and state._pn2_has_pyrokinesis(player))
    set_rule(world.get_location("PSI King's Sensorium: Purse", player), lambda state: state.has("Purse Tag (PSI King's Sensorium)", player))
    set_rule(world.get_location("PSI King's Sensorium: Memory Vault 1", player), lambda state: state._pn2_has_projection(player))
    set_rule(world.get_location("PSI King's Sensorium: Memory Vault 2", player), lambda state: state._pn2_has_projection(player))

    # Compton's Cookoff Entrances
    set_rule(world.get_entrance('Enter Compton', player), lambda state: state._pn2_has_bee_jar(player))
    set_rule(world.get_entrance('To Compton Round 1', player), lambda state: True)
    set_rule(world.get_entrance('To Compton Break 1', player), lambda state: state._pn2_has_telekinesis(player))
    set_rule(world.get_entrance('To Compton Round 2', player), lambda state: True)
    set_rule(world.get_entrance('To Compton Break 2', player), lambda state: state._pn2_has_telekinesis(player))
    set_rule(world.get_entrance('To Compton Round 3', player), lambda state: True)
    set_rule(world.get_entrance('To Compton Boss', player), lambda state: state._pn2_has_telekinesis(player))
    set_rule(world.get_entrance('End Compton', player), lambda state: state._pn2_has_telekinesis(player))

    # Compton's Cookoff Collectibles
    set_rule(world.get_location("Compton's Cookoff: Nugget of Wisdom 1", player), lambda state: state._pn2_has_mental_connection(player)) # tracking & randomization of PSI powers is not yet implemented, though this would require Dark Thoughts
    set_rule(world.get_location("Compton's Cookoff: Steamer Trunk", player), lambda state: state.has("Steamer Trunk Tag (Compton's Cookoff)", player))
    set_rule(world.get_location("Compton's Cookoff: Dufflebag", player), lambda state: state.has("Dufflebag Tag (Compton's Cookoff)", player))
    set_rule(world.get_location("Compton's Cookoff: Dufflebag Tag", player), lambda state: state._pn2_has_mental_connection(player)) 
    set_rule(world.get_location("Compton's Cookoff: Suitcase", player), lambda state: state.has("Suitcase Tag (Compton's Cookoff)", player))
    set_rule(world.get_location("Compton's Cookoff: Hatbox", player), lambda state: state.has("Hatbox Tag (Compton's Cookoff)", player))
    set_rule(world.get_location("Compton's Cookoff: Purse", player), lambda state: state.has("Purse Tag (Compton's Cookoff)", player))

    # Cruller's Correspondence Entrances
    set_rule(world.get_entrance('Enter Ford Mail', player), lambda state: state._pn2_can_complete_psi_king(player))
    set_rule(world.get_entrance('To Ford Mail Typewriter', player), lambda state: True)
    set_rule(world.get_entrance('To Ford Mail Bot Interior', player), lambda state: state._pn2_has_time_bubble(player) and state._pn2_has_mental_connection(player))
    set_rule(world.get_entrance('To Ford Mail International Dead Letter Office', player), lambda state: True)
    set_rule(world.get_entrance('To Ford Mail Above Typewriter', player), lambda state: True)
    set_rule(world.get_entrance('End Ford Mail', player), lambda state: state._pn2_has_telekinesis(player))

    # Cruller's Correspondence Collectibles
    set_rule(world.get_location("Cruller's Correspondence: Nugget of Wisdom", player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_time_bubble(player))
    set_rule(world.get_location("Cruller's Correspondence: Half-A-Mind", player), lambda state: state._pn2_has_time_bubble(player))
    set_rule(world.get_location("Cruller's Correspondence: Hatbox", player), lambda state: state._pn2_has_time_bubble(player) and state.has("Hatbox Tag (Cruller's Correspondence)", player))

    # Strike City Entrances
    set_rule(world.get_entrance('Enter Ford Bowling', player), lambda state: state._pn2_has_bowling_card(player))

    # Strike City Collectibles
    set_rule(world.get_location("Strike City: Dufflebag", player), lambda state: state.has("Dufflebag Tag (Strike City)", player))
    set_rule(world.get_location("Strike City: Suitcase", player), lambda state: state.has("Suitcase Tag (Strike City)", player))

    # Ford's Follicles Entrances
    set_rule(world.get_entrance('Enter Ford Haircut', player), lambda state: True)
    set_rule(world.get_entrance('To Ford Haircut Willmill', player), lambda state: True)
    set_rule(world.get_entrance('To Ford Haircut Town', player), lambda state: state._pn2_has_psi_blast(player) and state._pn2_has_levitation(player) and state._pn2_has_time_bubble(player))
    set_rule(world.get_entrance('To Ford Haircut Lighthouse', player), lambda state: True)
    set_rule(world.get_entrance('End Ford Haircut', player), lambda state: True)

    # Ford's Follicles Collectibles
    set_rule(world.get_location("Ford's Follicles: Nugget of Wisdom", player), lambda state: state._pn2_has_levitation(player))
    set_rule(world.get_location("Ford's Follicles: Steamer Trunk", player), lambda state: state.has("Steamer Trunk Tag (Ford's Follicles", player))

    # Tomb of the Sharkophagus Entrances
    set_rule(world.get_entrance('Enter Ford Tomb', player), lambda state: state._pn2_can_complete_ford_mail(player) and state._pn2_can_complete_ford_bowling(player) and state._pn2_can_complete_ford_haircut(player))

    # Tomb of the Sharkophagus Collectibles
    set_rule(world.get_location("Tomb of the Sharkophagus: Purse", player), lambda state: state.has("Purse Tag (Tomb of the Sharkophagus)", player))
    set_rule(world.get_location("Tomb of the Sharkophagus: Purse Tag", player), lambda state: state._pn2_has_time_bubble(player))
    set_rule(world.get_location("Tomb of the Sharkophagus: Memory Vault", player), lambda state: state._pn2_can_complete_ford_tomb(player))

    # Cassie's Collection Entrances
    set_rule(world.get_entrance('Enter Cassie', player), lambda state: state._pn2_can_complete_ford_tomb(player) and state._pn2_has_telekinesis(player))
    set_rule(world.get_entrance('To Cassie Teacher Domain', player), lambda state: True)
    set_rule(world.get_entrance('To Cassie Deep Teacher Domain', player), lambda state: state._pn2_has_projection(player))
    set_rule(world.get_entrance('To Cassie Librarian Desk', player), lambda state: state._pn2_has_projection(player) and state._pn2_has_levitation(player))
    set_rule(world.get_entrance('To Cassie Waterfront', player), lambda state: state._pn2_has_projection(player))
    set_rule(world.get_entrance('To Cassie Boss', player), lambda state: state._pn2_has_projection(player) and state._pn2_has_levitation(player))
    set_rule(world.get_entrance('End Cassie', player), lambda state: state._pn2_has_projection(player) and (state._pn2_has_psi_blast(player) or state._pn2_has_telekinesis(player)))

    # Cassie's Collection Collectibles
    set_rule(world.get_location("Cassie's Collection: Nugget of Wisdom 1", player), lambda state: state._pn2_has_time_bubble(player) and state._pn2_has_levitation(player))
    set_rule(world.get_location("Cassie's Collection: Nugget of Wisdom 2", player), lambda state: state._pn2_has_mental_connection(player))
    set_rule(world.get_location("Cassie's Collection: Nugget of Wisdom 3", player), lambda state: state._pn2_has_projection(player))
    set_rule(world.get_location("Cassie's Collection: Nugget of Wisdom 4", player), lambda state: state._pn2_has_levitation(player))
    set_rule(world.get_location("Cassie's Collection: Half-A-Mind 1", player), lambda state: state._pn2_has_projection(player))
    set_rule(world.get_location("Cassie's Collection: Half-A-Mind 2", player), lambda state: state._pn2_has_projection(player))
    set_rule(world.get_location("Cassie's Collection: Steamer Trunk", player), lambda state: state._pn2_has_projection(player) and state._pn2_has_time_bubble(player) and state.has("Steamer Trunk Tag (Cassie's Collection)", player))
    set_rule(world.get_location("Cassie's Collection: Steamer Trunk Tag", player), lambda state: state._pn2_has_levitation(player))
    set_rule(world.get_location("Cassie's Collection: Dufflebag", player), lambda state: state.has("Dufflebag Tag (Cassie's Collection)", player))
    set_rule(world.get_location("Cassie's Collection: Dufflebag Tag", player), lambda state: state._pn2_has_projection(player))
    set_rule(world.get_location("Cassie's Collection: Suitcase", player), lambda state: state._pn2_has_time_bubble(player) and state._pn2_has_levitation(player) and state.has("Suitcase Tag (Cassie's Collection)", player))
    set_rule(world.get_location("Cassie's Collection: Suitcase Tag", player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_levitation(player))
    set_rule(world.get_location("Cassie's Collection: Hatbox", player), lambda state: state.has("Hatbox Tag (Cassie's Collection)", player))
    set_rule(world.get_location("Cassie's Collection: Hatbox Tag", player), lambda state: state._pn2_has_projection(player))
    set_rule(world.get_location("Cassie's Collection: Purse", player), lambda state: state.has("Purse Tag (Cassie's Collection)", player))
    set_rule(world.get_location("Cassie's Collection: Memory Vault 2", player), lambda state: state._pn2_has_projection(player))

    # Bob's Bottles Entrances
    set_rule(world.get_entrance('Enter Bob', player), lambda state: state._pn2_can_complete_ford_tomb(player) and state._pn2_has_psi_blast(player))
    set_rule(world.get_entrance('To Bob Island', player), lambda state: state._pn2_has_psi_blast(player) and state._pn2_has_clairvoyance(player))
    set_rule(world.get_entrance('To Bob Kitchen', player), lambda state: state._pn2_has_telekinesis(player))
    set_rule(world.get_entrance('To Bob Ship In Bottle', player), lambda state: state._pn2_has_telekinesis(player))
    set_rule(world.get_entrance('To Bob Sunken Motherlobe', player), lambda state: state._pn2_has_psi_blast(player))
    set_rule(world.get_entrance('To Bob Bog', player), lambda state: state._pn2_has_telekinesis(player))
    set_rule(world.get_entrance('To Bob Reception', player), lambda state: True)
    set_rule(world.get_entrance('To Bob Cake', player), lambda state: state._pn2_has_clairvoyance(player))
    set_rule(world.get_entrance('To Bob Boss', player), lambda state: state._pn2_has_levitation(player) and state._pn2_has_telekinesis(player) and state._pn2_has_psi_blast(player) and state._pn2_has_clairvoyance(player))
    set_rule(world.get_entrance('End Bob', player), lambda state: state._pn2_has_clairvoyance(player) and (state._pn2_has_psi_blast(player) or state._pn2_has_telekinesis(player)))

    # Bob's Bottles Collectibles
    set_rule(world.get_location("Bob's Bottles: Nugget of Wisdom 1", player), lambda state: state._pn2_has_psi_blast(player))
    set_rule(world.get_location("Bob's Bottles: Nugget of Wisdom 2", player), lambda state: state._pn2_has_levitation(player))
    set_rule(world.get_location("Bob's Bottles: Half-A-Mind 2", player), lambda state: state._pn2_has_levitation(player) and state._pn2_has_mental_connection(player))
    set_rule(world.get_location("Bob's Bottles: Steamer Trunk", player), lambda state: state.has("Steamer Trunk Tag (Bob's Bottles)", player))
    set_rule(world.get_location("Bob's Bottles: Dufflebag", player), lambda state: state._pn2_has_psi_blast(player) and state.has("Dufflebag Tag (Bob's Bottles)", player))
    set_rule(world.get_location("Bob's Bottles: Dufflebag Tag", player), lambda state: state._pn2_has_psi_blast(player))
    set_rule(world.get_location("Bob's Bottles: Suitcase", player), lambda state: state.has("Suitcase Tag (Bob's Bottles)", player))
    set_rule(world.get_location("Bob's Bottles: Suitcase Tag", player), lambda state: state._pn2_has_levitation(player))
    set_rule(world.get_location("Bob's Bottles: Hatbox", player), lambda state: state.has("Hatbox Tag (Bob's Bottles)", player))
    set_rule(world.get_location("Bob's Bottles: Purse", player), lambda state: state._pn2_has_psi_blast(player) and state.has("Purse Tag (Bob's Bottles)", player))
    set_rule(world.get_location("Bob's Bottles: Purse Tag", player), lambda state: state._pn2_has_psi_blast(player))
    set_rule(world.get_location("Bob's Bottles: Memory Vault 1", player), lambda state: state._pn2_has_projection(player))

    # Lucrecia's Lament Entrances
    set_rule(world.get_entrance('Enter Lucrecia', player), lambda state: state._pn2_can_complete_cassie(player) and state._pn2_can_complete_bob(player))
    set_rule(world.get_entrance('To Lucrecia Quilts 1', player), lambda state: state._pn2_has_telekinesis(player) and state._pn2_has_time_bubble(player))
    set_rule(world.get_entrance('To Lucrecia Quilts 2', player), lambda state: True)
    set_rule(world.get_entrance('To Lucrecia Quilts 3', player), lambda state: True)
    set_rule(world.get_entrance('To Lucrecia Dam', player), lambda state: True)
    set_rule(world.get_entrance('End Lucrecia', player), lambda state: state._pn2_has_clairvoyance(player) and state._pn2_has_time_bubble(player))

    # Lucrecia's Lament Collectibles
    set_rule(world.get_location("Lucrecia's Lament: Nugget of Wisdom 3", player), lambda state: state._pn2_has_telekinesis(player))
    set_rule(world.get_location("Lucrecia's Lament: Steamer Trunk", player), lambda state: state._pn2_has_clairvoyance(player) and state._pn2_has_time_bubble(player) and state.has("Steamer Trunk Tag (Lucrecia's Lament)", player))
    set_rule(world.get_location("Lucrecia's Lament: Dufflebag", player), lambda state: state._pn2_has_clairvoyance(player) and state._pn2_has_time_bubble(player) and state.has("Dufflebag Tag (Lucrecia's Lament)", player))
    set_rule(world.get_location("Lucrecia's Lament: Dufflebag Tag", player), lambda state: state._pn2_has_telekinesis(player))
    set_rule(world.get_location("Lucrecia's Lament: Suitcase", player), lambda state: state._pn2_has_clairvoyance(player) and state._pn2_has_time_bubble(player) and state.has("Suitcase Tag (Lucrecia's Lament)", player))
    set_rule(world.get_location("Lucrecia's Lament: Suitcase Tag", player), lambda state: state._pn2_has_telekinesis(player) and state._pn2_has_time_bubble(player))
    set_rule(world.get_location("Lucrecia's Lament: Hatbox", player), lambda state: state._pn2_has_clairvoyance(player) and state._pn2_has_time_bubble(player) and state.has("Hatbox Tag (Lucrecia's Lament)", player))
    set_rule(world.get_location("Lucrecia's Lament: Purse", player), lambda state: state._pn2_has_clairvoyance(player) and state._pn2_has_time_bubble(player) and state.has("Purse Tag (Lucrecia's Lament)", player))

    # Fatherland Follies Entrances
    set_rule(world.get_entrance('Enter Gristol', player), lambda state: state._pn2_can_complete_lucrecia(player))
    set_rule(world.get_entrance('To Gristol Entrance', player), lambda state: True)
    set_rule(world.get_entrance('To Gristol Grulovia', player), lambda state: True)
    set_rule(world.get_entrance('To Gristol Exile', player), lambda state: state._pn2_has_mental_connection(player))
    set_rule(world.get_entrance('To Gristol Infiltration', player), lambda state: state._pn2_has_time_bubble(player))
    set_rule(world.get_entrance('To Gristol Gift Shop', player), lambda state: state._pn2_has_time_bubble(player) and state._pn2_has_mental_connection(player))
    set_rule(world.get_entrance('End Gristol', player), lambda state: state._pn2_has_time_bubble(player))

    # Fatherland Follies Collectibles
    set_rule(world.get_location("Fatherland Follies: Nugget of Wisdom 2", player), lambda state: state._pn2_has_pyrokinesis(player))
    set_rule(world.get_location("Fatherland Follies: Nugget of Wisdom 3", player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_time_bubble(player) and state._pn2_has_psi_blast(player))
    set_rule(world.get_location("Fatherland Follies: Steamer Trunk", player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_time_bubble(player) and state.has("Steamer Trunk Tag (Fatherland Follies)", player))
    set_rule(world.get_location("Fatherland Follies: Steamer Trunk Tag", player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_time_bubble(player))
    set_rule(world.get_location("Fatherland Follies: Dufflebag", player), lambda state: state._pn2_has_mental_connection(player) and state.has("Dufflebag Tag (Fatherland Follies)", player))
    set_rule(world.get_location("Fatherland Follies: Dufflebag Tag", player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_psi_blast(player))
    set_rule(world.get_location("Fatherland Follies: Suitcase", player), lambda state: state._pn2_can_complete_gristol(player) and state.has("Suitcase Tag (Fatherland Follies)", player))
    set_rule(world.get_location("Fatherland Follies: Hatbox", player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_time_bubble(player) and state.has("Hatbox Tag (Fatherland Follies)", player))
    set_rule(world.get_location("Fatherland Follies: Hatbox Tag", player), lambda state: state._pn2_has_mental_connection(player))
    set_rule(world.get_location("Fatherland Follies: Purse", player), lambda state: state.has("Purse Tag (Fatherland Follies)", player))
    set_rule(world.get_location("Fatherland Follies: Memory Vault 1", player), lambda state: state._pn2_has_mental_connection(player))
    set_rule(world.get_location("Fatherland Follies: Memory Vault 2", player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_time_bubble(player) and state._pn2_has_psi_blast(player))

    # Maligula Entrances
    set_rule(world.get_entrance('To Maligula Boss', player), lambda state: state._pn2_has_mental_connection(player) and state._pn2_has_pyrokinesis(player))
    set_rule(world.get_entrance('End Maligula', player), lambda state: True)