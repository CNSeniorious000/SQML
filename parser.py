from contextlib import suppress
from itertools import pairwise
from core import *


class NewQuestionnaire(Questionnaire):
    @staticmethod
    def parse_decoration(text):
        lft = text.find("[")
        rht = text.find("]")
        if ~lft and ~rht:
            return lft, rht

    @staticmethod
    def parse_derivation(text):
        lft = text.find("(")
        rht = text.find(")")
        if ~lft and ~rht:
            return lft, rht

    # noinspection PyUnreachableCode
    def parse_title(self, text: str) -> Question:
        assert text.startswith("#"), "must be title"

        index, title = text.split()

        if index == "#":
            return Question(self.length + 1, title)

        with suppress(ValueError):
            return Question(int(index[1:]), title)

        with suppress(TypeError):
            lft, rht = self.parse_decoration(index)
            logic = index[lft + 1:rht]
            return Question(int(index[1:lft] or str(self.length + 1)), title, logic or True)

        with suppress(TypeError):
            lft, rht = self.parse_derivation(index)
            # TODO: parse question derivative logic
            return self.parse_title(f"{index[:lft]} {title}")

        raise NotImplementedError(index, title)

    def parse_option(self, text) -> Choice:
        try:
            lft, rht = self.parse_decoration(text)
            decoration = text[lft + 1: rht]
            if "_" in decoration:
                return ChoiceWithCompletion(text[:lft])
            else:
                return Choice(text[:lft], "*" in decoration)
        except TypeError:
            return Choice(text)

    def build_question(self, title_line, choice_lines):
        question = self.parse_title(title_line)
        choices = [self.parse_option(choice) for choice in choice_lines]
        question.choices.extend(choices)
        return question

    @classmethod
    def build_questionnaire(cls, text):
        self = cls()
        lines = list(filter(None, [i.strip() for i in text.strip().split("\n")]))
        title_indices = [i for i, line in enumerate(lines) if line.startswith("#")] + [len(lines)]
        for i, j in pairwise(title_indices):
            self.append(self.build_question(lines[i], lines[i + 1:j]))

        return self


if __name__ == '__main__':
    questionnaire = NewQuestionnaire.build_questionnaire(open("example.txt", "rb").read().decode())
    print(questionnaire)
