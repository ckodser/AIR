import re

from hazm import POSTagger, Stemmer, Normalizer, Lemmatizer

from parsi_io.modules.number_extractor import NumberExtractor
from parsi_io.modules.time_extractions import TimeExtraction

date_extractor = TimeExtraction()
number_extractor = NumberExtractor()
punc = ''.join([".", "،", ":", "!", "؟", " "])
tagger = POSTagger(model='resources/postagger.model')
stemmer = Stemmer()
third_person_verbs = ["است", "هست"]
normalizer = Normalizer()
lemmatizer = Lemmatizer()

with open('names.txt') as f:
    persian_names = set(name.strip() for name in f.readlines())

pronouns = {
    'من',
    'تو',
    'او',
    'ما',
    'شما',
    'آنها',
    'مرا',
}


def is_name(s: str):
    return s in persian_names


def is_pronoun(s: str):
    return s in pronouns


def is_a_person(s: str):
    return is_name(s) or is_pronoun(s)


def get_in_question(s: str):
    return 'کسی' if is_a_person(s) else 'چیزی'


def build_question(input: str):
    return input.rstrip(punc) + "؟"


def third_person(verb: str):
    if verb in third_person_verbs:
        return verb
    correct_form = stemmer.stem(verb)
    lemmatized = lemmatizer.lemmatize(normalizer.normalize(verb), pos='V')
    if '#' in lemmatized:
        past, imperative = lemmatized.split('#', 1)
        imperative_pos = verb.rfind(imperative)
        past_pos = verb.rfind(past)
        if imperative_pos != -1 and 1 <= len(verb) - imperative_pos - len(imperative) <= 2:
            return verb[:imperative_pos] + imperative + 'د'
        elif past_pos != -1:
            return verb[:past_pos] + past
        else:
            return past
    else:
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


def is_third_person(verb):
    return third_person(verb) == normalizer.normalize(verb)
