from . import BlasphemousTestBase


class TestBrotherhoodEasy(BlasphemousTestBase):
    options = {
        "starting_location": "brotherhood",
        "difficulty": "easy"
    }


class TestBrotherhoodNormal(BlasphemousTestBase):
    options = {
        "starting_location": "brotherhood",
        "difficulty": "normal"
    }


class TestBrotherhoodHard(BlasphemousTestBase):
    options = {
        "starting_location": "brotherhood",
        "difficulty": "hard"
    }


class TestAlberoEasy(BlasphemousTestBase):
    options = {
        "starting_location": "albero",
        "difficulty": "easy"
    }


class TestAlberoNormal(BlasphemousTestBase):
    options = {
        "starting_location": "albero",
        "difficulty": "normal"
    }


class TestAlberoHard(BlasphemousTestBase):
    options = {
        "starting_location": "albero",
        "difficulty": "hard"
    }


class TestConventEasy(BlasphemousTestBase):
    options = {
        "starting_location": "convent",
        "difficulty": "easy"
    }


class TestConventNormal(BlasphemousTestBase):
    options = {
        "starting_location": "convent",
        "difficulty": "normal"
    }


class TestConventHard(BlasphemousTestBase):
    options = {
        "starting_location": "convent",
        "difficulty": "hard"
    }


class TestGrievanceEasy(BlasphemousTestBase):
    options = {
        "starting_location": "grievance",
        "difficulty": "easy"
    }


class TestGrievanceNormal(BlasphemousTestBase):
    options = {
        "starting_location": "grievance",
        "difficulty": "normal"
    }


class TestGrievanceHard(BlasphemousTestBase):
    options = {
        "starting_location": "grievance",
        "difficulty": "hard"
    }


class TestKnotOfWordsEasy(BlasphemousTestBase):
    options = {
        "starting_location": "knot_of_words",
        "difficulty": "easy"
    }


class TestKnotOfWordsNormal(BlasphemousTestBase):
    options = {
        "starting_location": "knot_of_words",
        "difficulty": "normal"
    }


class TestKnotOfWordsHard(BlasphemousTestBase):
    options = {
        "starting_location": "knot_of_words",
        "difficulty": "hard"
    }


class TestRooftopsEasy(BlasphemousTestBase):
    options = {
        "starting_location": "rooftops",
        "difficulty": "easy"
    }


class TestRooftopsNormal(BlasphemousTestBase):
    options = {
        "starting_location": "rooftops",
        "difficulty": "normal"
    }


class TestRooftopsHard(BlasphemousTestBase):
    options = {
        "starting_location": "rooftops",
        "difficulty": "hard"
    }


# mourning and havoc can't be selected on easy or normal. hard only
class TestMourningHavocHard(BlasphemousTestBase):
    options = {
        "starting_location": "mourning_havoc",
        "difficulty": "hard"
    }
