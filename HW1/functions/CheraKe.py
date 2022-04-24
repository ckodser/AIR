import re
import hazm

from .base import build_question, third_person_verbs, stemmer, tagger

chera_ke_pattern = 'چرا که|زیرا'


def CheraKe(input: str):
    if re.search(chera_ke_pattern, input) is None:
        return None, None, False
    else:
        x = re.split(chera_ke_pattern, input)
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
        tagged = tagger.tag(hazm.word_tokenize(x[1]))
        for i, p in enumerate(tagged):
            verb, part = p
            if part == "V":
                verb = verb.replace("_", " ")
                correct_form = third_person(verb)
                x[1] = x[1].replace(verb, correct_form)

        return build_question("چه چیزی باعث" + x[1]), input, True


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
