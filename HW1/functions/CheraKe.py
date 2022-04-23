import re
import hazm
from hazm import *
from parsi_io.modules.number_extractor import NumberExtractor
from parsi_io.modules.time_extractions import TimeExtraction

date_extractor = TimeExtraction()
number_extractor = NumberExtractor()
punc = [".", "،", ":", "!", "؟", " "]
tagger = POSTagger(model='resources/postagger.model')
stemmer = Stemmer()
third_person_verbs = ["است", "هست"]
all_colors = []
normalizer = Normalizer()

with open("colors.txt", encoding="utf-8") as f:
    for color in f:
        color = color.rstrip().lstrip()
        if len(color) > 2:
            all_colors.append(" " + normalizer.normalize(color) + " ")

color_pattern = "|".join(all_colors)


def CheraKe(input: str):
    if re.search("چرا که", input) is None:
        return None, None, False
    else:
        x = re.split("چرا که", input)
        if len(x) != 2:
            return None, None, False
        return build_question("چرا " + x[0]), "چرا که" + x[1], True


def baEs(input: str):
    if re.search("باعث", input) is None:
        return None, None, False
    else:
        x = re.split("باعث", input)
        if len(x) != 2:
            return None, None, False
        tagged = tagger.tag(word_tokenize(x[1]))
        for i, p in enumerate(tagged):
            verb, part = p
            if part == "V":
                verb = verb.replace("_", " ")
                correct_form = third_person(verb)
                x[1] = x[1].replace(verb, correct_form)

        return build_question("چه چیزی باعث" + x[1]), input, True


def color(input: str):
    a = re.search(color_pattern, input)
    if a is not None:
        qu = build_question(re.sub(color_pattern, "چه رنگی", input, 1))
        return qu, a.group(), True
    else:
        return None, None, False


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


def date(input: str):
    all_dates = date_extractor.run(input)['markers']['datetime']
    questions = []
    answers = []
    for segment in all_dates:
        answers.append(all_dates[segment])
        inner_segment = segment[1:-1].split(",")
        l = int(inner_segment[0])
        r = int(inner_segment[1])
        questions.append(input[:l] + "چه زمانی" + input[r:])
    return questions, answers, True


def third_person(verb: str):
    if verb in third_person_verbs:
        return verb
    correct_form = stemmer.stem(verb)
    if correct_form[-1] != "د":
        correct_form = correct_form + "د"
    elif correct_form[-2] == 'ن':
        correct_form = correct_form[:-2] + "د"
        if correct_form[-2] == correct_form[-1]:
            correct_form = correct_form[:-1]
    future_plo = "خواهند" + "|" + "خواهیم" + "|" + "خواهید" + "|" + "خواهم" + "|" + "خواهی"
    future_single = "خواهد"
    correct_form = re.sub(future_plo, future_single, correct_form)
    return correct_form


def build_question(input: str):
    while input[-1] in punc:
        input = input[:-1]

    return input + "؟"
