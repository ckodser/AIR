from .base import tagger, lemmatizer
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
    try:
        all_sentences = []
        tagged = tagger.tag(hazm.word_tokenize(input))
        index_list = [i[0] for i in list(filter(lambda i: i[1][1] == 'V', enumerate(tagged)))][:1]
        verb_count=0
        for word, pos in tagged:
            if pos=='V':
              verb_count+=1
        if verb_count>1:
          return None, None, False
        for i in range(len(index_list)):
            res = ''
            if i != 0:
                sentences = tagged[index_list[i - 1] + 1:index_list[i] + 1]
            else:
                sentences = tagged[0:index_list[i] + 1]
            for word_index, word in enumerate(sentences):
                if word_index == len(sentences) - 1:
                    res += get_positive_verb(word[0])
                else:
                    res += word[0] + ' '
            all_sentences.append(res.strip())

        for sentence in all_sentences:
            q = create_question(sentence)
            verb = list(filter(lambda i: i[1] == 'V', tagged))[0][0]
            ans = create_answer(input, verb)
            questions.append(q)
            answers.append(ans)

        return questions, answers, True
    except Exception as e:
        print(e)
        return questions, answers, False
