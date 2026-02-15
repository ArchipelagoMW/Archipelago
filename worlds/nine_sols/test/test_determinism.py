from .bases import NineSolsTestBase


class TestJadeCostDeterminism(NineSolsTestBase):
    options = {
        "randomize_jade_costs": True,
    }
    seed = 1

    def world_setup(self, *args, **kwargs):
        super().world_setup(self.seed)

    def test_determinism(self):
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data['jade_costs'], {
            'Avarice Jade': 2,
            'Bearing Jade': 2,
            'Breather Jade': 1,
            'Cultivation Jade': 2,
            'Divine Hand Jade': 1,
            'Focus Jade': 1,
            'Harness Force Jade': 3,
            'Health Thief Jade': 2,
            'Hedgehog Jade': 2,
            'Immovable Jade': 1,
            'Iron Skin Jade': 1,
            'Last Stand Jade': 1,
            'Medical Jade': 2,
            'Mob Quell Jade - Yang': 1,
            'Mob Quell Jade - Yin': 2,
            'Pauper Jade': 3,
            'Qi Blade Jade': 1,
            'Qi Swipe Jade': 1,
            'Quick Dose Jade': 1,
            'Reciprocation Jade': 1,
            'Recovery Jade': 2,
            'Revival Jade': 2,
            'Ricochet Jade': 1,
            'Soul Reaper Jade': 2,
            'Stasis Jade': 1,
            'Steely Jade': 2,
            'Swift Blade Jade': 1,
            'Swift Descent Jade': 3
        })
