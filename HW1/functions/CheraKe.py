punc=[".","،",":","!","؟"," "]
def CheraKe(input: str):
    ind=input.find("چرا که")
    if ind == -1:
        return None,None, False
    return build_question("چرا "+input[:ind]), input[ind:], True

def build_question(input: str):
    while input[-1] in punc:
        input=input[:-1]

    return input+"؟"