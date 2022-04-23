import re
from functions.CheraKe import build_question

pos_patterns_first_cause = [
    '.*(دلا?یل|عل[تل]|عامل|از دلایل|از عوامل|از علل|چرایی).*(است|هست|هستند|میباشد|می باشد|میباشند|می باشند|بود|بودند|باشد|باشند)',
    '(را نتیجه|رانتیجه).*(میدهند|میدهد|خواهند داد|خواهد داد|می دهد|می دهند|داد|داده|داده اند).*',
    '.*(منجر به|موجب|باعث|منجربه).*(است|هست|هستند|میباشد|می باشد|میباشند|می باشند|بود|بودند|باشد|باشند)',
    '.*(نتایج).*(میتوان|می توان).*(اشاره کرد|برشمرد|بر شمرد).*',
    '.*(منجر به|سبب|منجربه).*(می شوند|میشوند|میشود|می شود|شد|شوند|شود).*'
]
question_seperator = [
    '(نتیجه|از نتایج|به خاطر|دلا?یل|عل[تل]|عامل|از دلایل|از عوامل|از علل|چرایی|است|هست|هستند|میباشد|می باشد|میباشند|می باشند|بود|بودند|باشد|باشند)',
    '(را نتیجه|رانتیجه|میدهند|میدهد|خواهند داد|خواهد داد|می دهد|می دهند|داد|داده|داده اند)',
    '(منجر به|موجب|باعث|منجربه|است|هست|هستند|میباشد|می باشد|میباشند|می باشند|بود|بودند|باشد|باشند)',
    '(نتایج|میتوان|می توان|اشاره کرد|برشمرد|بر شمرد)',
    '(منجر به|سبب|منجربه|می شوند|میشوند|میشود|می شود|شد|شوند|شود)'
]

pos_patterns_second_cause = [
    '.*(نتیجه|از نتایج|به خاطر).*(است|هست|هستند|میباشد|می باشد|میباشند|می باشند|بود|بودند|باشد|باشند)',
    None,
    None,
    '.*(دلایل|علل|عوامل).*(میتوان|می توان).*(اشاره کرد|برشمرد|بر شمرد).*',
]


def causeEffect(input: str):
    questions = []
    answers = []
    for i, pattern in enumerate(pos_patterns_first_cause):
        if re.search(pattern, input) != None:
            input_pro = re.sub(question_seperator[i], '*$*', input).split('*$*')
            for i, part in enumerate(input_pro):
                if len(part) <= 1:
                    input_pro.pop(i)

            if len(input_pro) == 2:
                question_part, answer_part = input_pro[1], input_pro[0]
                questions.append(build_question("علت " + question_part + "چیست"))
                answers.append(answer_part)

    for i, pattern in enumerate(pos_patterns_second_cause):
        if pattern is not None and re.search(pattern, input) != None:
            input_pro = re.sub(question_seperator[i], '*$*', input).split('*$*')
            for i, part in enumerate(input_pro):
                if len(part) <= 1:
                    input_pro.pop(i)

            if len(input_pro) == 2:
                question_part, answer_part = input_pro[0], input_pro[1]
                questions.append(build_question("علت " + question_part + "چیست"))
                answers.append(answer_part)
    return questions, answers, True
