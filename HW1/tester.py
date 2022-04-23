from __future__ import unicode_literals
import hazm
from main import run
from hazm import *

normalizer = Normalizer()
with open("tests.txt", encoding="utf-8") as f:
    total = ""
    for input in f:
        if len(input) < 3:
            continue
        input = input[:-2]
        total += input + "\n"
        print(input, " ==> ", end="")
        for qu in run(input):
            print("question:", normalizer.normalize(qu["Question"]), "ans:", normalizer.normalize(qu["Answer"]),
                  end="   **  ")
        print()


