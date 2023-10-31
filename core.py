class Questionnaire:
    def __init__(self):
        self.questions: list[Question] = []
        self.length = 0

    def append(self, question):
        assert isinstance(question, Question)
        self.questions.append(question)
        self.length += 1

    def __str__(self):
        return "\n\n".join(map(str, self.questions))

    __repr__ = __str__


class Choice:
    symbols = {True: "√", False: " "}

    @property
    def prefix(self):
        return f"[{self.symbols[self.chosen]}]"

    def __init__(self, text: str, chosen=False):
        self.text = text
        self.chosen = chosen

    def __str__(self):
        return f"{self.prefix} {self.text}"

    __repr__ = __str__


class ChoiceWithCompletion(Choice):
    letters = '_' * 8

    def __str__(self):
        return f"{super().__str__()} {self.letters}" if self.text else self.letters

    __repr__ = __str__


class Question:
    def __init__(self, num, text, multi_choice=False):
        self.num = num
        self.text = text
        self.multi_choice = multi_choice
        self.choices = []

    def __str__(self):
        if len(self.choices) == 1 and not self.choices[0].text:
            return f"【{self.num}】{self.text}（填空题）\n\t{self.choices[0]}"

        return f"【{self.num}】{self.text}" \
               f"（{'多' if self.multi_choice else '单'}选题）\n\t" + \
               "\n\t".join(map(str, self.choices))

    __repr__ = __str__
