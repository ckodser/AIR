from hazm import Normalizer

from main import run

normalizer = Normalizer()
with open("tests.txt", encoding="utf-8") as f:
    total = ""
    for input in f:
        if len(input) < 3:
            continue
        input = input[:-2]
        total += input + "\n"
        print(input, " ==> ")
        for qu in run(input):
            print('question:', normalizer.normalize(qu["Question"]))
            print('ans:', normalizer.normalize(qu["Answer"]))
            print('fn_name:', qu['fn_name'])
            print('*' * 10)
        print()

with open("bigtest.txt", encoding="utf-8") as f:
    total = ""
    for input in f:
        if len(input) < 1:
            continue
        total += input + "\n"

    input=total
    print(input, " ==> ")
    for qu in run(input):
        print('question:', normalizer.normalize(qu["Question"]))
        print('ans:', normalizer.normalize(qu["Answer"]))
        print('fn_name:', qu['fn_name'])
        print('*' * 10)
    print()


