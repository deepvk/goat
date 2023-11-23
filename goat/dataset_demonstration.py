import pandas as pd

from dataset_utils import remove_unnecessary_symbols
from spider_utils import TaskType

file_path = "./goat/ege_data.jsonl"
ege_data = pd.read_json(path_or_buf=file_path, lines=True)
text_columns = ["task_text", "solution_text", "answer"]
for column in text_columns:
    ege_data[column] = ege_data[column].apply(remove_unnecessary_symbols)

ege_data["topic_id"] = ege_data["topic_id"].astype(int)
ege_data = ege_data.sort_values("topic_id")
sootv_tasks = ege_data.loc[ege_data["task_type"] == TaskType.SOOTV]

if len(sootv_tasks) > 0:
    print("Пример задания на соответствие -", sootv_tasks["url"].iloc[0])
    print(sootv_tasks["task_text"].iloc[0])
    print("----------")
    print(sootv_tasks["solution_text"].iloc[0])
    print("----------")
    print(sootv_tasks["answer"].iloc[0])
    print("------------------------------")

mult_choice_tasks = ege_data.loc[ege_data["task_type"] == TaskType.MULT_CHOICE]
if len(mult_choice_tasks) > 0:
    print("Пример задания на multiple_choice -", mult_choice_tasks["url"].iloc[0])
    print(mult_choice_tasks["task_text"].iloc[0])
    print("----------")
    print(mult_choice_tasks["solution_text"].iloc[0])
    print("----------")
    print(mult_choice_tasks["answer"].iloc[0])
    print("------------------------------")

text_answer_tasks = ege_data.loc[ege_data["task_type"] == TaskType.TEXT_ANSWER]
if len(text_answer_tasks) > 0:
    print("Пример задания на текстовый ответ -", text_answer_tasks["url"].iloc[0])
    print(text_answer_tasks["task_text"].iloc[0])
    print("----------")
    print(text_answer_tasks["solution_text"].iloc[0])
    print("----------")
    if text_answer_tasks["answer"].iloc[0] == "":
        print("No answer")
    else:
        print(text_answer_tasks["answer"].iloc[0])
    print("------------------------------")

based_on_text_tasks = ege_data.loc[ege_data["task_type"] == TaskType.QUESTION_ON_TEXT]
if len(based_on_text_tasks) > 0:
    print("Пример задания на вопрос по тексту -", based_on_text_tasks["url"].iloc[0])
    print(based_on_text_tasks["task_text"].iloc[0])
    print("----------")
    print(based_on_text_tasks["solution_text"].iloc[0])
    print("----------")
    if based_on_text_tasks["answer"].iloc[0] == "":
        print("No answer")
    else:
        print(based_on_text_tasks["answer"].iloc[0])