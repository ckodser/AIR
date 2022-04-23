import re
import hazm
from hazm import *


punc = [".", "،", ":", "!", "؟", " "]


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
        tagger = POSTagger(model='resources/postagger.model')
        print(tagger.tag(word_tokenize('ما بسیار کتاب می‌خوانیم')))
        exit(0)
        x = re.split("باعث", input)
        if len(x) != 2:
            return None, None, False
        return build_question("چه چیزی باعث" + third_person(x[1])), input, True

def third_person(input: str):
    return input

def build_question(input: str):
    while input[-1] in punc:
        input = input[:-1]

    return input + "؟"
