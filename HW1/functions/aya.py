from .base import tagger, lemmatizer, is_third_person
import hazm

n_start_verbs = [
    'نوشتن',
    'نوردیدن',
    'نغوشیدن',
    'نیوشیدن',
    'نوشیدن',
    'نگریستن',
    'نگاشتن',
    'نشستن',
]

n_start_lemmatized_verbs = list(map(lemmatizer.lemmatize, n_start_verbs))


def verb_is_positive(verb: str):
    lemmatized_verb = lemmatizer.lemmatize(verb)
    if lemmatized_verb in n_start_lemmatized_verbs:
        if verb[0] == 'ن' and verb[1] == 'ن':
            return False
    return not verb[0] == 'ن'


def get_positive_verb(verb: str):
    lemmatized_verb = lemmatizer.lemmatize(verb)
    if lemmatized_verb in n_start_lemmatized_verbs:
        if verb[0] == 'ن' and verb[1] == 'ن':
            return verb[2:]
    if verb[0] == 'ن':
        return verb[1:]
    return verb


def create_question(input: str):
    return f'آیا {input}؟'


def create_answer(input: str, verb: str):
    if verb_is_positive(verb):
        answer = f'بله، {input}'
    else:
        answer = f'خیر، {input}'
    return answer


def aya(input: str):
    questions = []
    answers = []
    tagged = tagger.tag(hazm.word_tokenize(input))
    index_list = [i[0] for i in list(filter(lambda i: i[1][1] == 'V', enumerate(tagged)))]
    if len(index_list) != 1 or not is_third_person(tagged[index_list[0]][0]):
        return None, None, False
    words = tagged[:index_list[0] + 1]
    res = ''
    for word_index, (word, pos) in enumerate(words):
        if word_index == len(words) - 1:
            res += get_positive_verb(word)
        else:
            res += word + ' '
    q = create_question(res)
    verb = list(filter(lambda i: i[1] == 'V', tagged))[0][0]
    ans = create_answer(input, verb)
    questions.append(q)
    answers.append(ans)

    return questions, answers, True
