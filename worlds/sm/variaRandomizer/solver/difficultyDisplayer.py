from utils.parameters import easy, medium, hard, harder, hardcore, mania, impossibru, diff2text

class DifficultyDisplayer:
    def __init__(self, difficulty):
        self.difficulty = difficulty

    def scale(self):
        if self.difficulty >= impossibru:
            return "IMPOSSIBRU!"
        else:
            previous = 0
            for d in sorted(diff2text):
                if self.difficulty >= d:
                    previous = d
                else:
                    displayString = diff2text[previous]
                    displayString += ' '
                    scale = d - previous
                    pos = int(self.difficulty - previous)
                    displayString += '-' * pos
                    displayString += '^'
                    displayString += '-' * (scale - pos)
                    displayString += ' '
                    displayString += diff2text[d]
                    break

            return displayString

    def percent(self):
        # return the difficulty as a percent
        if self.difficulty == -1:
            return -1
        elif self.difficulty in [0, easy]:
            return 0
        elif self.difficulty >= mania:
            return 100

        difficultiesPercent = {
            easy: 0,
            medium: 20,
            hard: 40,
            harder: 60,
            hardcore: 80,
            mania: 100
        }

        difficulty = self.difficulty

        lower = 0
        percent = 100
        for upper in sorted(diff2text):
            if self.difficulty >= upper:
                lower = upper
            else:
                lowerPercent = difficultiesPercent[lower]
                upperPercent = difficultiesPercent[upper]

                a = (upperPercent-lowerPercent)/float(upper-lower)
                b = lowerPercent - a * lower

                percent = int(difficulty * a + b)
                break

        return percent
