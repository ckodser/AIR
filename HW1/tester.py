from main import run

with open("tests.txt", encoding="utf-8") as f:
    for input in f:
        if len(input) < 3:
            continue
        input = input[:-2]
        print(input, " ==> ", run(input))
