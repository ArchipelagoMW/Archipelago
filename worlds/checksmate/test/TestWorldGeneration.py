from . import CMTestBase

class TestWorldGeneration(CMTestBase):
    def test_full_generation(self):
        """Test that a complete world generates successfully"""
        # This test needs the full world context
        self.world.create_items()
        # Test generation results... 