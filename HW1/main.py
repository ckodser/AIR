import re

from functions.aya import aya
from functions.CheraKe import CheraKe, baEs
from functions.date import date
from functions.number import number
from functions.color import color
from functions.causeEffect import causeEffect
from functions.subject_object import subject_object

all_functions = [subject_object, CheraKe, baEs, color, number, date, causeEffect, aya]


def run(input: str):
    output = []
    spited = split_sentences(input)
    for function in all_functions:
        for part in spited:
            question, answer, solve = function(part)
            if solve:
                if isinstance(question, str):
                    question = [question]
                    answer = [answer]
                for i in range(len(question)):
                    output.append({"Question": question[i], "Answer": answer[i], 'fn_name': function.__name__})
    return output


def split_sentences(input: str):
    stop_markers = "?.!.!؟"
    return re.findall(fr'.+(?:[{stop_markers}]|$)', input)
