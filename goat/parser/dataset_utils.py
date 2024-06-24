def remove_unnecessary_symbols(str_ans: str) -> str:
    str_ans = str_ans.replace("\xad", "")
    str_ans = str_ans.replace("\xa0", " ")
    str_ans = str_ans.replace("\u202f", " ")
    str_ans = str_ans.replace("  ", " ")
    return str_ans
