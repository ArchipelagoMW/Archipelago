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
            'Avarice Jade': 1,
            'Bearing Jade': 1,
            'Breather Jade': 1,
            'Cultivation Jade': 1,
            'Divine Hand Jade': 3,
            'Focus Jade': 2,
            'Harness Force Jade': 3,
            'Health Thief Jade': 1,
            'Hedgehog Jade': 2,
            'Immovable Jade': 1,
            'Iron Skin Jade': 1,
            'Killing Blow Jade': 3,
            'Last Stand Jade': 1,
            'Medical Jade': 2,
            'Mob Quell Jade - Yang': 1,
            'Mob Quell Jade - Yin': 2,
            'Pauper Jade': 1,
            'Qi Blade Jade': 1,
            'Qi Swipe Jade': 2,
            'Qi Thief Jade': 1,
            'Quick Dose Jade': 1,
            'Reciprocation Jade': 2,
            'Recovery Jade': 2,
            'Revival Jade': 2,
            'Ricochet Jade': 2,
            'Soul Reaper Jade': 1,
            'Stasis Jade': 1,
            'Steely Jade': 2,
            'Swift Blade Jade': 2,
            'Swift Descent Jade': 1
        })
