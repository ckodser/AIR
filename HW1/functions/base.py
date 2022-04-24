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


def build_question(input: str):

    return input.rstrip(punc) + "؟"
