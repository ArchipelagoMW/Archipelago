import typing

import Utils


def get_intended_text(input_text: str, possible_answers) -> typing.Tuple[str, bool, str]:
    picks = Utils.get_fuzzy_results(input_text, possible_answers, limit=2)
    if len(picks) > 1:
        dif = picks[0][1] - picks[1][1]
        if picks[0][1] == 100:
            return picks[0][0], True, "Perfect Match"
        elif picks[0][1] < 75:
            return picks[0][0], False, f"Didn't find something that closely matches '{input_text}', " \
                                       f"did you mean '{picks[0][0]}'? ({picks[0][1]}% sure)"
        elif dif > 5:
            return picks[0][0], True, "Close Match"
        else:
            return picks[0][0], False, f"Too many close matches for '{input_text}', " \
                                       f"did you mean '{picks[0][0]}'? ({picks[0][1]}% sure)"
    else:
        if picks[0][1] > 90:
            return picks[0][0], True, "Only Option Match"
        else:
            return picks[0][0], False, f"Didn't find something that closely matches '{input_text}', " \
                                       f"did you mean '{picks[0][0]}'? ({picks[0][1]}% sure)"


def get_input_text_from_response(text: str, command: str) -> typing.Optional[str]:
    if "did you mean " in text:
        for question in ("Didn't find something that closely matches",
                         "Too many close matches"):
            if text.startswith(question):
                name = Utils.get_text_between(text, "did you mean '",
                                              "'? (")
                return f"!{command} {name}"
                break
    elif text.startswith("Missing: "):
        return text.replace("Missing: ", "!hint_location ")
    return None
