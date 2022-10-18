from . import ZillionTestBase


class TestGoalVanilla(ZillionTestBase):
    options = {
        "start_char": "JJ",
        "jump_levels": "vanilla",
        "gun_levels": "vanilla",
        "floppy_disk_count": 7,
        "floppy_req": 6,
    }

    def test_floppies(self):
        self.collect_by_name(["Apple", "Champ", "Red ID Card"])
        self.assertBeatable(False)  # 0 floppies
        floppies = self.get_items_by_name("Floppy Disk")
        win = self.get_item_by_name("Win")
        self.collect(floppies[:-2])  # 1 too few
        self.assertEqual(self.count("Floppy Disk"), 5)
        self.assertBeatable(False)
        self.collect(floppies[-2:-1])  # exact
        self.assertEqual(self.count("Floppy Disk"), 6)
        self.assertBeatable(True)
        self.remove([win])  # reset
        self.collect(floppies[-1:])  # 1 extra
        self.assertEqual(self.count("Floppy Disk"), 7)
        self.assertBeatable(True)

    def test_with_everything(self):
        self.collect_by_name(["Apple", "Champ", "Red ID Card", "Floppy Disk"])
        self.assertBeatable(True)

    def test_no_jump(self):
        self.collect_by_name(["Champ", "Red ID Card", "Floppy Disk"])
        self.assertBeatable(False)

    def test_no_gun(self):
        self.collect_by_name(["Apple", "Red ID Card", "Floppy Disk"])
        self.assertBeatable(False)

    def test_no_red(self):
        self.collect_by_name(["Apple", "Champ", "Floppy Disk"])
        self.assertBeatable(False)


class TestGoalBalanced(ZillionTestBase):
    options = {
        "start_char": "JJ",
        "jump_levels": "balanced",
        "gun_levels": "balanced",
    }

    def test_jump(self):
        self.collect_by_name(["Red ID Card", "Floppy Disk", "Zillion"])
        self.assertBeatable(False)  # not enough jump
        opas = self.get_items_by_name("Opa-Opa")
        self.collect(opas[:1])  # too few
        self.assertEqual(self.count("Opa-Opa"), 1)
        self.assertBeatable(False)
        self.collect(opas[1:])
        self.assertBeatable(True)

    def test_guns(self):
        self.collect_by_name(["Red ID Card", "Floppy Disk", "Opa-Opa"])
        self.assertBeatable(False)  # not enough gun
        guns = self.get_items_by_name("Zillion")
        self.collect(guns[:1])  # too few
        self.assertEqual(self.count("Zillion"), 1)
        self.assertBeatable(False)
        self.collect(guns[1:])
        self.assertBeatable(True)


class TestGoalRestrictive(ZillionTestBase):
    options = {
        "start_char": "JJ",
        "jump_levels": "restrictive",
        "gun_levels": "restrictive",
    }

    def test_jump(self):
        self.collect_by_name(["Champ", "Red ID Card", "Floppy Disk", "Zillion"])
        self.assertBeatable(False)  # not enough jump
        self.collect_by_name("Opa-Opa")
        self.assertBeatable(False)  # with all opas, jj champ can't jump
        self.collect_by_name("Apple")
        self.assertBeatable(True)

    def test_guns(self):
        self.collect_by_name(["Apple", "Red ID Card", "Floppy Disk", "Opa-Opa"])
        self.assertBeatable(False)  # not enough gun
        self.collect_by_name("Zillion")
        self.assertBeatable(False)  # with all guns, jj apple can't gun
        self.collect_by_name("Champ")
        self.assertBeatable(True)
