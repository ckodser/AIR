import re

import hazm

from .base import build_question, tagger, third_person, get_in_question, normalizer

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
        x[1] = normalizer.normalize(x[1])
        tagged = tagger.tag(hazm.word_tokenize(x[1]))
        words = []
        for p in tagged:
            verb, part = p
            if part == "V":
                verb = verb.replace("_", " ")
                verb = third_person(verb)
            words.append(verb)

        return build_question(f"چه {get_in_question(x[0].strip())} باعث " + ' '.join(words)), input, True
