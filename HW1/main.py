from functions.CheraKe import CheraKe
all_functions = [CheraKe]


def run(input: str):
    output = []
    for function in all_functions:
        question, answer, solve = function(input)
        if solve:
            output.append({"Question": question, "Answer": answer})
    return output
