import argparse

import pandas as pd
from dataset_utils import remove_unnecessary_symbols
from spider_utils import TaskType

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This program prints different tasks from input file")
    parser.add_argument("-f", "--filename", required=True, type=str)
    args = parser.parse_args()
    file_path = f"./{args.filename}"
    sdamgia_data = pd.read_json(path_or_buf=file_path, lines=True)
    text_columns = ["task_text", "solution_text", "answer", "criteria_table"]
    for column in text_columns:
        sdamgia_data[column] = sdamgia_data[column].apply(remove_unnecessary_symbols)

    sdamgia_data["topic_id"] = sdamgia_data["topic_id"].astype(int)
    sdamgia_data = sdamgia_data.sort_values("topic_id")
    task_description = {
        TaskType.MULT_CHOICE: "выбор вариантов ответа",
        TaskType.SOOTV: "установление соответствия",
        TaskType.TEXT_ANSWER: "текстовый ответ",
    }

    for task_type in TaskType:
        tasks = sdamgia_data.loc[sdamgia_data["task_type"] == task_type]
        print(f"Пример задания на {task_description[task_type]} -", tasks["url"].iloc[0])
        print(tasks["task_text"].iloc[0])
        print("----------")
        print(tasks["solution_text"].iloc[0])
        print("----------")
        if tasks["answer"].iloc[0] == "":
            print("No answer")
        else:
            print(tasks["answer"].iloc[0])
        print("----------")
        print("Количество первичных баллов за правильное решение задачи -", tasks["task_points"].iloc[0])
        print("------------------------------")
