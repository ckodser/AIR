from functions.CheraKe import CheraKe, baEs

all_functions = [CheraKe, baEs]


def run(input: str):
    output = []
    spited = split_sentences(input)
    for function in all_functions:
        for part in spited:
            question, answer, solve = function(part)
            if solve:
                output.append({"Question": question, "Answer": answer})
    return output


def split_sentences(input: str):
    stop_marker = ["?", ".", "!", ".", "!", "؟"]
    spited_result = []
    l = 0
    for i in range(len(input)):
        if input[i] in stop_marker:
            part = input[l:i + 1].rstrip().lstrip()
            if len(part) > 0:
                spited_result.append(part)
            l = i + 1

    part = input[l:].rstrip().lstrip()
    if len(part) > 0:
        spited_result.append(part)
    return spited_result
