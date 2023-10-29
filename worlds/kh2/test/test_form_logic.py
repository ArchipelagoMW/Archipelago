from . import KH2TestBase
from ..Names import ItemName, LocationName

global_all_possible_forms = [ItemName.ValorForm, ItemName.WisdomForm, ItemName.LimitForm, ItemName.MasterForm, ItemName.FinalForm] + [ItemName.AutoValor, ItemName.AutoWisdom, ItemName.AutoLimit, ItemName.AutoMaster, ItemName.AutoFinal]


class KH2TestFormBase(KH2TestBase):
    allForms = [ItemName.ValorForm, ItemName.WisdomForm, ItemName.LimitForm, ItemName.MasterForm, ItemName.FinalForm]
    autoForms = [ItemName.AutoValor, ItemName.AutoWisdom, ItemName.AutoLimit, ItemName.AutoMaster, ItemName.AutoFinal]
    allLevel2 = [LocationName.Valorlvl2, LocationName.Wisdomlvl2, LocationName.Limitlvl2, LocationName.Masterlvl2,
                 LocationName.Finallvl2]
    allLevel3 = [LocationName.Valorlvl3, LocationName.Wisdomlvl3, LocationName.Limitlvl3, LocationName.Masterlvl3,
                 LocationName.Finallvl3]
    allLevel4 = [LocationName.Valorlvl4, LocationName.Wisdomlvl4, LocationName.Limitlvl4, LocationName.Masterlvl4,
                 LocationName.Finallvl4]
    allLevel5 = [LocationName.Valorlvl5, LocationName.Wisdomlvl5, LocationName.Limitlvl5, LocationName.Masterlvl5,
                 LocationName.Finallvl5]
    allLevel6 = [LocationName.Valorlvl6, LocationName.Wisdomlvl6, LocationName.Limitlvl6, LocationName.Masterlvl6,
                 LocationName.Finallvl6]
    allLevel7 = [LocationName.Valorlvl7, LocationName.Wisdomlvl7, LocationName.Limitlvl7, LocationName.Masterlvl7,
                 LocationName.Finallvl7]
    driveToAuto = {
        ItemName.FinalForm:  ItemName.AutoFinal,
        ItemName.MasterForm: ItemName.AutoMaster,
        ItemName.LimitForm:  ItemName.AutoLimit,
        ItemName.WisdomForm: ItemName.AutoWisdom,
        ItemName.ValorForm:  ItemName.AutoValor,
    }
    AutoToDrive = {Auto: Drive for Drive, Auto in driveToAuto.items()}
    driveFormMap = {
        ItemName.ValorForm:  [LocationName.Valorlvl2,
                              LocationName.Valorlvl3,
                              LocationName.Valorlvl4,
                              LocationName.Valorlvl5,
                              LocationName.Valorlvl6,
                              LocationName.Valorlvl7],
        ItemName.WisdomForm: [LocationName.Wisdomlvl2,
                              LocationName.Wisdomlvl3,
                              LocationName.Wisdomlvl4,
                              LocationName.Wisdomlvl5,
                              LocationName.Wisdomlvl6,
                              LocationName.Wisdomlvl7],
        ItemName.LimitForm:  [LocationName.Limitlvl2,
                              LocationName.Limitlvl3,
                              LocationName.Limitlvl4,
                              LocationName.Limitlvl5,
                              LocationName.Limitlvl6,
                              LocationName.Limitlvl7],
        ItemName.MasterForm: [LocationName.Masterlvl2,
                              LocationName.Masterlvl3,
                              LocationName.Masterlvl4,
                              LocationName.Masterlvl5,
                              LocationName.Masterlvl6,
                              LocationName.Masterlvl7],
        ItemName.FinalForm:  [LocationName.Finallvl2,
                              LocationName.Finallvl3,
                              LocationName.Finallvl4,
                              LocationName.Finallvl5,
                              LocationName.Finallvl6,
                              LocationName.Finallvl7],
    }
    # global_all_possible_forms = allForms + autoForms


class TestDefaultForms(KH2TestFormBase):
    """
    Test default form access rules.
    """
    options = {
        "AutoFormLogic":  False,
        "FinalFormLogic": "light_and_darkness"
    }

    def test_default_Auto_Form_Logic(self):
        allPossibleForms = global_all_possible_forms
        # this tests with a light and darkness in the inventory.
        self.collect_all_but(allPossibleForms)
        for form in self.allForms:
            self.assertFalse((self.can_reach_location(self.driveFormMap[form][0])), form)
            self.collect(self.get_item_by_name(self.driveToAuto[form]))
            self.assertFalse((self.can_reach_location(self.driveFormMap[form][0])), form)

    def test_default_Final_Form(self):
        allPossibleForms = global_all_possible_forms
        self.collect_all_but(allPossibleForms)
        self.collect_by_name(ItemName.FinalForm)
        self.assertTrue((self.can_reach_location(LocationName.Finallvl2)))
        self.assertTrue((self.can_reach_location(LocationName.Finallvl3)))
        self.assertFalse((self.can_reach_location(LocationName.Finallvl4)))

    def test_default_without_LnD(self):
        allPossibleForms = self.allForms
        self.collect_all_but(allPossibleForms)
        for form, levels in self.driveFormMap.items():
            # final form is unique and breaks using this test. Tested above.
            if levels[0] == LocationName.Finallvl2:
                continue
            for driveForm in self.allForms:
                if self.count(driveForm) >= 1:
                    for _ in range(self.count(driveForm)):
                        self.remove(self.get_item_by_name(driveForm))
            allFormsCopy = self.allForms.copy()
            allFormsCopy.remove(form)
            self.collect(self.get_item_by_name(form))
            for _ in range(self.count(ItemName.LightDarkness)):
                self.remove(self.get_item_by_name(ItemName.LightDarkness))
            self.assertTrue((self.can_reach_location(levels[0])), levels[0])
            self.assertTrue((self.can_reach_location(levels[1])), levels[1])
            self.assertFalse((self.can_reach_location(levels[2])), levels[2])
            for i in range(3):
                self.collect(self.get_item_by_name(allFormsCopy[i]))
                # for some reason after collecting a form it can pick up light and darkness
                for _ in range(self.count(ItemName.LightDarkness)):
                    self.remove(self.get_item_by_name(ItemName.LightDarkness))

                self.assertTrue((self.can_reach_location(levels[2 + i])))
                if i < 2:
                    self.assertFalse((self.can_reach_location(levels[3 + i])))
                else:
                    self.collect(self.get_item_by_name(allFormsCopy[i + 1]))
                    for _ in range(self.count(ItemName.LightDarkness)):
                        self.remove(self.get_item_by_name(ItemName.LightDarkness))
                    self.assertTrue((self.can_reach_location(levels[3 + i])))

    def test_default_with_lnd(self):
        allPossibleForms = self.allForms
        self.collect_all_but(allPossibleForms)
        for form, levels in self.driveFormMap.items():
            if form != ItemName.FinalForm:
                for driveForm in self.allForms:
                    for _ in range(self.count(driveForm)):
                        self.remove(self.get_item_by_name(driveForm))
                allFormsCopy = self.allForms.copy()
                allFormsCopy.remove(form)
                self.collect(self.get_item_by_name(ItemName.LightDarkness))
                self.assertFalse((self.can_reach_location(levels[0])))
                self.collect(self.get_item_by_name(form))

                self.assertTrue((self.can_reach_location(levels[0])))
                self.assertTrue((self.can_reach_location(levels[1])))
                self.assertTrue((self.can_reach_location(levels[2])))
                self.assertFalse((self.can_reach_location(levels[3])))
                for i in range(2):
                    self.collect(self.get_item_by_name(allFormsCopy[i]))
                    self.assertTrue((self.can_reach_location(levels[i + 3])))
                    if i <= 2:
                        self.assertFalse((self.can_reach_location(levels[i + 4])))


class TestJustAForm(KH2TestFormBase):
    # this test checks if you can unlock final form with just a form.
    options = {
        "AutoFormLogic":  False,
        "FinalFormLogic": "just_a_form"
    }

    def test_just_a_form_connections(self):
        allPossibleForms = self.allForms
        self.collect_all_but(allPossibleForms)
        allPossibleForms.remove(ItemName.FinalForm)
        for form, levels in self.driveFormMap.items():
            for driveForm in self.allForms:
                for _ in range(self.count(driveForm)):
                    self.remove(self.get_item_by_name(driveForm))
            if form != ItemName.FinalForm:
                # reset the forms
                allFormsCopy = self.allForms.copy()
                allFormsCopy.remove(form)
                self.assertFalse((self.can_reach_location(levels[0])))
                self.collect(self.get_item_by_name(form))
                self.assertTrue((self.can_reach_location(levels[0])))
                self.assertTrue((self.can_reach_location(levels[1])))
                self.assertTrue((self.can_reach_location(levels[2])))

                # level 4 of a form. This tests if the player can unlock final form.
                self.assertFalse((self.can_reach_location(levels[3])))
                # amount of forms left in the pool are 3. 1 already collected and one is final form.
                for i in range(3):
                    allFormsCopy.remove(allFormsCopy[0])
                    # so we don't accidentally collect another form like light and darkness in the above tests.
                    self.collect_all_but(allFormsCopy)
                    self.assertTrue((self.can_reach_location(levels[3 + i])), levels[3 + i])
                    if i < 2:
                        self.assertFalse((self.can_reach_location(levels[4 + i])), levels[4 + i])


class TestAutoForms(KH2TestFormBase):
    options = {
        "AutoFormLogic":  True,
        "FinalFormLogic": "light_and_darkness"
    }

    def test_Nothing(self):
        KH2TestBase()

    def test_auto_forms_level_progression(self):
        allPossibleForms = self.allForms + [ItemName.LightDarkness]
        # state has all auto forms
        self.collect_all_but(allPossibleForms)
        allPossibleFormsCopy = allPossibleForms.copy()
        collectedDrives = []
        i = 0
        for form in allPossibleForms:
            currentDriveForm = form
            collectedDrives += [currentDriveForm]
            allPossibleFormsCopy.remove(currentDriveForm)
            self.collect_all_but(allPossibleFormsCopy)
            for driveForm in self.allForms:
                # +1 every iteration.
                self.assertTrue((self.can_reach_location(self.driveFormMap[driveForm][i])), driveForm)
                # making sure having the form still gives an extra drive level to its own form.
                if driveForm in collectedDrives and i < 5:
                    self.assertTrue((self.can_reach_location(self.driveFormMap[driveForm][i + 1])), driveForm)
            i += 1
