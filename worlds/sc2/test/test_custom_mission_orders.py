"""
Unit tests for custom mission orders
"""

from .test_base import Sc2SetupTestBase
from .. import MissionFlag

class TestCustomMissionOrders(Sc2SetupTestBase):
    
    def test_mini_wol_generates(self):
        world_options = {
            'custom_mission_order': {
                'Mini Wings of Liberty': {
                    'global': {
                       'type': 'column',
                       'mission_pool': [
                          'terran missions',
                          'and wol missions'
                       ]
                    },
                    'Mar Sara': {
                       'order': 0,
                       'size': 1
                    },
                    'Colonist': {
                       'order': 10,
                       'size': 2
                    },
                    'Artifact': {
                       'order': 20,
                       'size': 3,
                       'unlock_count': 0,
                       'unlock_specific': ['Mar Sara'],
                       1: {
                          'unlock_count': 4
                       },
                       2: {
                          'unlock_count': 8
                       }
                    },
                    'Prophecy': {
                       'order': 30,
                       'size': 2,
                       'unlock_count': 0,
                       'unlock_specific': ['Artifact/1'],
                       'mission_pool': [
                          'protoss missions',
                          'and prophecy missions'
                       ]
                    },
                    'Covert': {
                       'order': 40,
                       'size': 2,
                       'unlock_count': 0,
                       0: {
                          'unlock_count': 2
                       }
                    },
                    'Rebellion': {
                       'order': 50,
                       'size': 2,
                       'unlock_count': 0,
                       0: {
                          'unlock_count': 3
                       }
                    },
                    'Char': {
                        'order': 60,
                        'size': 3,
                        'unlock_count': 0,
                        'unlock_specific': ['Artifact/2'],
                        0: {
                            'next': [2]
                        },
                        1: {
                            'entrance': True
                        }
                    }
                }
            }
        }

        self.generate_world(world_options)
        flags = self.world.custom_mission_order.get_used_flags()
        self.assertEqual(flags[MissionFlag.Terran], 13)
        self.assertEqual(flags[MissionFlag.Protoss], 2)
        self.assertEqual(flags[MissionFlag.Zerg], 0)
        self.assertEqual(len(self.world.custom_mission_order.get_used_missions()), len(self.multiworld.regions))
