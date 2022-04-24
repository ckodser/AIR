import re

from .base import build_question, tagger

object_pattern = r'(\S+) را '

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


def is_a_person(object_part: str):
    return is_name(object_part) or is_pronoun(object_part)


def subject_object(input: str):
    match = re.search(object_pattern, input)
    if match is None:
        return None, None, False

    start, end = match.start(), match.end()
    question = build_question(
        input[:start] + 'چه ' + ('کسی' if is_a_person(match.group(1)) else 'چیزی') + ' را ' + input[end:]
    )
    answer = input[start:end]

    return question, answer, True
