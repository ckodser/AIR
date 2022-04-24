from .base import number_extractor, punc, build_question


def number(input: str):
    all_numbers = number_extractor.run(input)
    questions = []
    answers = []
    for number in all_numbers:
        r = number['span'][1]
        l = number['span'][0]
        if len(input) > r and input[r] in punc:
            qu = build_question(input[:l] + "چند" + input[r:])
            ans = input[l:r]
            questions.append(qu)
            answers.append(ans)
    return questions, answers, True
