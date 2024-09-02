"""
Unit tests for custom mission orders
"""

from .test_base import Sc2SetupTestBase
from .. import MissionFlag

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
