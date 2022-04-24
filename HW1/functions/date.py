from .base import date_extractor, build_question


def date(input: str):
    all_dates = date_extractor.run(input)['markers']['datetime']
    questions = []
    answers = []
    for segment in all_dates:
        answers.append(all_dates[segment])
        inner_segment = segment[1:-1].split(",")
        l = int(inner_segment[0])
        r = int(inner_segment[1])
        questions.append(build_question(input[:l] + "چه زمانی" + input[r:]))
    return questions, answers, True
