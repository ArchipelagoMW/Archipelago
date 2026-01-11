import random

from ...randomizer.data import dialogs
from . import flags


# There's a way to do perfect allocations with DYNAMIC PROGRAMMING,
# but I'm not doing that.
def allocate_string(string_length, free_list):
    for base in sorted(free_list, key=lambda x: free_list[x]):
        if free_list[base] >= string_length:
            size = free_list[base]
            del free_list[base]
            free_list[base+string_length] = size - string_length
            return base

    # If we get this far, we couldn't find space for the string.
    return None


def randomize_all(world):
    """

    Args:
        world (randomizer.logic.main.GameWorld):

    """
    # Check flag?
    if world.open_mode:
        randomize_wishes(world)
        if world.settings.is_flag_enabled(flags.QuizShuffle):
            randomize_quiz(world)


def randomize_wishes(world):
    """

    Args:
        world (randomizer.logic.main.GameWorld):

    """
    world.wishes.wishes.clear()
    available_wishes = dialogs.wish_strings.copy()

    # These are the existing wishes.
    free_list = {
        0x240958: 415,
        0x243e32: 80,
        0x24344d: 32,
        0x240e2a: 1349,  # Factory gate dialog
        # 0x22dba5: 843,  # Axem dialog (possibly problematic to use, text here gets cut weird???)
    }
    for dialog_id in dialogs.wish_dialogs:
        biggest_space = max(free_list.values())
        possible_wishes = [s for s in available_wishes if len(s) <= biggest_space]
        if not possible_wishes:
            raise ValueError("Unable to allocate space for wishes: {!r}; {!r}".format(free_list, world.wishes.wishes))

        wish = random.choice(possible_wishes)
        base = allocate_string(len(wish), free_list)
        available_wishes.remove(wish)
        # Wish strings should be short enough that this doesn't happen, but give us a traceback if it does.
        if not base:
            raise ValueError("Unable to allocate space for wish: {!r}".format(wish))

        world.wishes.wishes.append((dialog_id, base, wish))


def randomize_quiz(world):
    """

    Args:
        world (randomizer.logic.main.GameWorld):

    """
    world.quiz.questions.clear()
    questions = dialogs.get_quiz_questions()
    if len(questions) > len(dialogs.quiz_dialogs):
        random_questions = random.sample(questions, len(dialogs.quiz_dialogs))
    else:
        random_questions = questions
    random_questions += random.sample(dialogs.backfill_questions, len(dialogs.quiz_dialogs) - len(random_questions))
    random.shuffle(random_questions)

    free_list = {
        0x22e082: 3953,  # Existing Questions
    }
    for dialog_id, question in zip(dialogs.quiz_dialogs, random_questions):
        # Randomize order of incorrect answers for some extra variety.
        random.shuffle(question.wrong_answers)

        # Double check these
        if 1842 <= dialog_id < 1858:
            correct = 0
        elif 1858 <= dialog_id < 1874:
            correct = 1
        else:
            correct = 2
        string = question.get_string(correct)
        base = allocate_string(len(string), free_list)
        # Questions should be short enough that this doesn't happen, but give us a traceback if it does.
        if not base:
            raise ValueError("Unable to allocate space for question: {!r}".format(string))
        world.quiz.questions.append((dialog_id, base, string))
