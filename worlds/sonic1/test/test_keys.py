import random
from . import Sonic1TestBase

class TestKeys(Sonic1TestBase):
    options = {"ring_goal": 0}

    def test_key_gating(self) -> None:
        progression = [
          ("Green Hill Key", "Green Hill", "Green Hill 1"),
          ("Marble Zone Key", "Marble Zone", "Marble Zone 1"),
          ("Spring Yard Key", "Spring Yard", "Spring Yard 1"),
          ("Labyrinth Key", "Labyrinth", "Labyrinth 1"),
          ("Starlight Key", "Starlight", "Starlight 1"),
          ("Scrap Brain Key", "Scrap Brain", "Scrap Brain 1"),
          ("Final Zone Key", "Final Zone", None),
          ("Special Stage 1 Key", "Special Stage 1", None),
          ("Special Stage 2 Key", "Special Stage 2", None),
          ("Special Stage 3 Key", "Special Stage 3", None),
          ("Special Stage 4 Key", "Special Stage 4", None),
          ("Special Stage 5 Key", "Special Stage 5", None),
          ("Special Stage 6 Key", "Special Stage 6", None),
        ]

        unreach = [p[1] for p in progression]
        unreach.extend([p[2] for p in progression if p[2]])

        self.assertEqual(self.count("Special Stages Key"), 1, "Missing Special Stages Key")

        def try_and_remove(keyto = None):
            if keyto is not None:
                progression.remove(keyto)
                unreach.remove(keyto[1])
                self.assertTrue(self.can_reach_region(keyto[1]), f"{keyto[1]} should be reachable with {keyto[0]}")
                if keyto[2]:
                    unreach.remove(keyto[2])
                    self.assertTrue(self.can_reach_region(keyto[2]), f"{keyto[2]} should be reachable with {keyto[0]}")
            for L in unreach:
                self.assertFalse(self.can_reach_region(L), f"{L} shouldn't be reachable")
            
        # One key will have been assigned randomly, we need to figure out which.
        for K in progression.copy():
            if self.count(K[0]):
                try_and_remove(K)
        
        # Let's try collecting them in order
        for K in progression.copy():
            self.collect_by_name(K[0])
            try_and_remove(K)

class TestKeysWeirdly(Sonic1TestBase):
    options = {"ring_goal": 0}

    def test_key_gating(self) -> None:
        progression = [
          ("Green Hill Key", "Green Hill", "Green Hill 1"),
          ("Marble Zone Key", "Marble Zone", "Marble Zone 1"),
          ("Spring Yard Key", "Spring Yard", "Spring Yard 1"),
          ("Labyrinth Key", "Labyrinth", "Labyrinth 1"),
          ("Starlight Key", "Starlight", "Starlight 1"),
          ("Scrap Brain Key", "Scrap Brain", "Scrap Brain 1"),
          ("Final Zone Key", "Final Zone", None),
          ("Special Stage 2 Key", "Special Stage 2", None),
          ("Special Stage 3 Key", "Special Stage 3", None),
          ("Special Stage 4 Key", "Special Stage 4", None),
          ("Special Stage 5 Key", "Special Stage 5", None),
          ("Special Stage 6 Key", "Special Stage 6", None),
        ]
        random.shuffle(progression)
        progression.append(("Special Stage 1 Key", "Special Stage 1", None))

        unreach = [p[1] for p in progression]
        unreach.extend([p[2] for p in progression if p[2]])

        self.assertEqual(self.count("Special Stages Key"), 1, "Missing Special Stages Key")

        def try_and_remove(keyto = None):
            if keyto is not None:
                progression.remove(keyto)
                if ("Special Stage" in keyto[0] and keyto[0] != "Special Stage 1 Key"):
                  self.assertFalse(self.can_reach_region(keyto[1]), f"{keyto[1]} should NOT be reachable with just {keyto[0]}")
                else:
                  unreach.remove(keyto[1])
                  self.assertTrue(self.can_reach_region(keyto[1]), f"{keyto[1]} should be reachable with {keyto[0]}")
                  if keyto[2]:
                      unreach.remove(keyto[2])
                      self.assertTrue(self.can_reach_region(keyto[2]), f"{keyto[2]} should be reachable with {keyto[0]}")
                  if keyto[0] == "Special Stage 1 Key":
                      while unreach:
                          L = unreach.pop()
                          self.assertTrue(self.can_reach_region(L), f"{L} should now be reachable after {keyto[0]}")
                  
            for L in unreach:
                self.assertFalse(self.can_reach_region(L), f"{L} shouldn't be reachable")
            
        # One key will have been assigned randomly, we need to figure out which.
        for K in progression.copy():
            if self.count(K[0]):
                try_and_remove(K)
        
        # Let's try collecting them in order
        for K in progression.copy():
            self.collect_by_name(K[0])
            try_and_remove(K)
