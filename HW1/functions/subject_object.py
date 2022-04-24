import re

from .base import build_question, get_in_question

object_pattern = r'(\S+) را '


def subject_object(input: str):
    match = re.search(object_pattern, input)
    if match is None:
        return None, None, False

    start, end = match.start(), match.end()
    question = build_question(
        input[:start] + f'چه {get_in_question(match.group(1))} را ' + input[end:]
    )
    answer = input[start:end]

    return question, answer, True
