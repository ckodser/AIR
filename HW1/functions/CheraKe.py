import re
import hazm
from hazm import *

punc = [".", "،", ":", "!", "؟", " "]
tagger = POSTagger(model='resources/postagger.model')
stemmer = Stemmer()
third_person_verbs = ["است", "هست"]
all_colors=[]
normalizer = Normalizer()

with open("colors.txt", encoding="utf-8") as f:
    for color in f:
        color=color.rstrip().lstrip()
        if len(color)>2:
          all_colors.append(normalizer.normalize(color))

print(len(all_colors))
color_pattern="|".join(all_colors)
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
    a=re.search(color_pattern, input)
    if a is not None:
      qu=build_question(re.sub(color_pattern, "چه رنگی", input, 1))
      return qu, a.group(), True
    else:
      return None, None, False


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
    future_plo = "خواهند"
    future_single = "خواهد"
    correct_form = re.sub(future_plo, future_single, correct_form)
    return correct_form


def build_question(input: str):
    while input[-1] in punc:
        input = input[:-1]

    return input + "؟"
