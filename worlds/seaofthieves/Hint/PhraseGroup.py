import typing


class PhraseGroup:

    def __init__(self, phrases: typing.List[str]):
        self.phrases: typing.List[str] = phrases
        self.counter = 0

    def add(self, phrase: str):
        self.phrases.append(phrase)

    def get(self, index: int = 0):
        return self.phrases[index]

    def get_random(self):
        self.counter += 1
        return self.get(len(self.phrases) % self.counter - 1)
