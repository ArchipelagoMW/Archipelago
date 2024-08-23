"""
Unit tests for custom mission orders
"""

from .test_base import Sc2SetupTestBase
from .. import MissionFlag
from .. import item_names
from BaseClasses import ItemClassification

class TestCustomMissionOrders(Sc2SetupTestBase):
   
   def test_mini_wol_generates(self):
      world_options = {
         'mission_order': 'custom',
         'custom_mission_order': {
            'Mini Wings of Liberty': {
               'global': {
                  'type': 'column',
                  'mission_pool': [
                     'terran missions',
                     '^ wol missions'
                  ]
               },
               'Mar Sara': {
                  'size': 1
               },
               'Colonist': {
                  'size': 2,
                  'entry_rules': [{
                     'scope': '../Mar Sara'
                  }]
               },
               'Artifact': {
                  'size': 3,
                  'entry_rules': [{
                     'scope': '../Mar Sara'
                  }],
                  'missions': [
                     {
                        'index': 1,
                        'entry_rules': [{
                           'scope': 'Mini Wings of Liberty',
                           'amount': 4
                        }]
                     },
                     {
                        'index': 2,
                        'entry_rules': [{
                           'scope': 'Mini Wings of Liberty',
                           'amount': 8
                        }]
                     }
                  ]
               },
               'Prophecy': {
                  'size': 2,
                  'entry_rules': [{
                     'scope': '../Artifact/1'
                     }],
                  'mission_pool': [
                     'protoss missions',
                     '^ prophecy missions'
                  ]
               },
               'Covert': {
                  'size': 2,
                  'entry_rules': [{
                     'scope': 'Mini Wings of Liberty',
                     'amount': 2
                  }]
               },
               'Rebellion': {
                  'size': 2,
                  'entry_rules': [{
                     'scope': 'Mini Wings of Liberty',
                     'amount': 3
                  }]
               },
               'Char': {
                  'size': 3,
                  'entry_rules': [{
                     'scope': '../Artifact/2'
                  }],
                  'missions': [
                     {
                        'index': 0,
                        'next': [2]
                     },
                     {
                        'index': 1,
                        'entrance': True
                     }
                  ]
               }
            }
         }
      }

      self.generate_world(world_options)
      flags = self.world.custom_mission_order.get_used_flags()
      self.assertEqual(flags[MissionFlag.Terran], 13)
      self.assertEqual(flags[MissionFlag.Protoss], 2)
      self.assertEqual(flags.get(MissionFlag.Zerg, 0), 0)
      sc2_regions = set(self.multiworld.regions.region_cache[self.player]) - {"Menu"}
      self.assertEqual(len(self.world.custom_mission_order.get_used_missions()), len(sc2_regions))

   def test_locked_and_necessary_item_appears_once(self):
      # This is a filler upgrade with a parent
      test_item = item_names.ZERGLING_METABOLIC_BOOST
      world_options = {
         'mission_order': 'custom',
         'locked_items': { test_item: 1 },
         'custom_mission_order': {
            'test': {
               'type': 'column',
               'size': 5, # Give the generator some space to place the key
               'max_difficulty': 'easy',
               'missions': [{
                  'index': 4,
                  'entry_rules': [{
                     'items': { test_item: 1 }
                  }]
               }]
            }
         }
      }

      self.generate_world(world_options)
      test_items_in_pool = [item for item in self.multiworld.itempool if item.name == test_item]
      self.assertEqual(len(test_items_in_pool), 1)
      self.assertEqual(test_items_in_pool[0].classification, ItemClassification.progression)

   def test_start_inventory_and_necessary_item_appears_once(self):
      # This is a filler upgrade with a parent
      test_item = item_names.ZERGLING_METABOLIC_BOOST
      world_options = {
         'mission_order': 'custom',
         'start_inventory': { test_item: 1 },
         'custom_mission_order': {
            'test': {
               'type': 'column',
               'size': 5, # Give the generator some space to place the key
               'max_difficulty': 'easy',
               'missions': [{
                  'index': 4,
                  'entry_rules': [{
                     'items': { test_item: 1 }
                  }]
               }]
            }
         }
      }

      self.generate_world(world_options)
      test_items_in_pool = [item for item in self.multiworld.itempool if item.name == test_item]
      self.assertEqual(len(test_items_in_pool), 0)
      test_items_in_start_inventory = [item for item in self.multiworld.precollected_items[self.player] if item.name == test_item]
      self.assertEqual(len(test_items_in_start_inventory), 1)
      # Start inventory gets a new item so the classification is no longer progression
      self.assertEqual(test_items_in_start_inventory[0].classification, ItemClassification.filler)

   def test_start_inventory_and_locked_and_necessary_item_appears_once(self):
      # This is a filler upgrade with a parent
      test_item = item_names.ZERGLING_METABOLIC_BOOST
      world_options = {
         'mission_order': 'custom',
         'start_inventory': { test_item: 1 },
         'locked_items': { test_item: 1 },
         'custom_mission_order': {
            'test': {
               'type': 'column',
               'size': 5, # Give the generator some space to place the key
               'max_difficulty': 'easy',
               'missions': [{
                  'index': 4,
                  'entry_rules': [{
                     'items': { test_item: 1 }
                  }]
               }]
            }
         }
      }

      self.generate_world(world_options)
      test_items_in_pool = [item for item in self.multiworld.itempool if item.name == test_item]
      self.assertEqual(len(test_items_in_pool), 0)
      test_items_in_start_inventory = [item for item in self.multiworld.precollected_items[self.player] if item.name == test_item]
      self.assertEqual(len(test_items_in_start_inventory), 1)
      # Start inventory gets a new item so the classification is no longer progression
      self.assertEqual(test_items_in_start_inventory[0].classification, ItemClassification.filler)
