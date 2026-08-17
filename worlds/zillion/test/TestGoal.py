from . import ZillionTestBase


class TestGoalVanilla(ZillionTestBase):
    options = {
        "start_char": "JJ",
        "jump_levels": "vanilla",
        "gun_levels": "vanilla",
        "floppy_disk_count": 7,
        "floppy_req": 6,
    }

    def test_floppies(self) -> None:
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

    def test_with_everything(self) -> None:
        self.collect_by_name(["Apple", "Champ", "Red ID Card", "Floppy Disk"])
        self.assertBeatable(True)

    def test_no_jump(self) -> None:
        self.collect_by_name(["Champ", "Red ID Card", "Floppy Disk"])
        self.assertBeatable(False)

    def test_no_gun(self) -> None:
        self.ensure_gun_3_requirement()
        self.collect_by_name(["Apple", "Red ID Card", "Floppy Disk"])
        self.assertBeatable(False)

    def test_no_red(self) -> None:
        self.collect_by_name(["Apple", "Champ", "Floppy Disk"])
        self.assertBeatable(False)


class TestGoalBalanced(ZillionTestBase):
    options = {
        "start_char": "JJ",
        "jump_levels": "balanced",
        "gun_levels": "balanced",
    }

    def test_jump(self) -> None:
        self.collect_by_name(["Red ID Card", "Floppy Disk", "Zillion"])
        self.assertBeatable(False)  # not enough jump
        opas = self.get_items_by_name("Opa-Opa")
        self.collect(opas[:1])  # too few
        self.assertEqual(self.count("Opa-Opa"), 1)
        self.assertBeatable(False)
        self.collect(opas[1:])
        self.assertBeatable(True)

    def test_guns(self) -> None:
        self.ensure_gun_3_requirement()
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

    def test_jump(self) -> None:
        self.collect_by_name(["Champ", "Red ID Card", "Floppy Disk", "Zillion"])
        self.assertBeatable(False)  # not enough jump
        self.collect_by_name("Opa-Opa")
        self.assertBeatable(False)  # with all opas, jj champ can't jump
        self.collect_by_name("Apple")
        self.assertBeatable(True)

    def test_guns(self) -> None:
        self.ensure_gun_3_requirement()
        self.collect_by_name(["Apple", "Red ID Card", "Floppy Disk", "Opa-Opa"])
        self.assertBeatable(False)  # not enough gun
        self.collect_by_name("Zillion")
        self.assertBeatable(False)  # with all guns, jj apple can't gun
        self.collect_by_name("Champ")
        self.assertBeatable(True)


class TestGoalAppleStart(ZillionTestBase):
    """ creation of character rescue items has some special interactions with logic """
    options = {
        "start_char": "Apple",
        "jump_levels": "balanced",
        "gun_levels": "low",
        "zillion_count": 5,
    }

    def test_guns_jj_first(self) -> None:
        """ with low gun levels, 5 Zillion is enough to get JJ to gun 3 """
        self.ensure_gun_3_requirement()
        self.collect_by_name(["JJ", "Red ID Card", "Floppy Disk", "Opa-Opa"])
        self.assertBeatable(False)  # not enough gun
        self.collect_by_name("Zillion")
        self.assertBeatable(True)

    def test_guns_zillions_first(self) -> None:
        """ with low gun levels, 5 Zillion is enough to get JJ to gun 3 """
        self.ensure_gun_3_requirement()
        self.collect_by_name(["Zillion", "Red ID Card", "Floppy Disk", "Opa-Opa"])
        self.assertBeatable(False)  # not enough gun
        self.collect_by_name("JJ")
        self.assertBeatable(True)


class TestGoalChampStart(ZillionTestBase):
    """ creation of character rescue items has some special interactions with logic """
    options = {
        "start_char": "Champ",
        "jump_levels": "low",
        "gun_levels": "balanced",
        "opa_opa_count": 5,
        "opas_per_level": 1,
    }

    def test_jump_jj_first(self) -> None:
        """ with low jump levels, 5 level-ups is enough to get JJ to jump 3 """
        self.collect_by_name(["JJ", "Red ID Card", "Floppy Disk", "Zillion"])
        self.assertBeatable(False)  # not enough jump
        self.collect_by_name("Opa-Opa")
        self.assertBeatable(True)

    def test_jump_opa_first(self) -> None:
        """ with low jump levels, 5 level-ups is enough to get JJ to jump 3 """
        self.collect_by_name(["Opa-Opa", "Red ID Card", "Floppy Disk", "Zillion"])
        self.assertBeatable(False)  # not enough jump
        self.collect_by_name("JJ")
        self.assertBeatable(True)
