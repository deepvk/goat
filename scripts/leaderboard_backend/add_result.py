# type: ignore
import argparse
import json

from database_helper import DatabaseHelper, EvalResult
from datasets import get_dataset_config_names, load_dataset


def get_datasets_len(tasks):
    datasets_len = dict()
    datasets_len["single_choice"] = 0
    datasets_len["multiple_choice"] = 0
    datasets_len["word_gen"] = 0

    for task in tasks:
        dataset = load_dataset("deepvk/goat", task, split="test")
        datasets_len[task] = len(dataset)
        if "single_choice" in task:
            datasets_len["single_choice"] += len(dataset)
        elif "multiple_choice" in task:
            datasets_len["multiple_choice"] += len(dataset)
        elif "word_gen" in task:
            datasets_len["word_gen"] += len(dataset)
    return datasets_len


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This program redacts dataset -_-")
    parser.add_argument("eval_result_path", type=str, help="Path to evaluation result")

    args = parser.parse_args()
    with open(args.eval_result_path, "r") as j:
        contents = json.loads(j.read())
    evaluation = contents["results"]
    tasks = get_dataset_config_names("deepvk/goat")

    datasets_len = get_datasets_len(tasks)
    metrics = [
        "multi_choice_em_unordered,get-answer",
        "word_in_set,none",
        "multi_choice_em_unordered,get-answer",
        "acc,none",
    ]

    single_choice_score = 0
    multiple_choice_score = 0
    word_gen_score = 0

    for task in tasks:
        for metric in metrics:
            if metric in evaluation[task].keys():
                if "single_choice" in task:
                    single_choice_score += datasets_len[task] * evaluation[task][metric]
                elif "multiple_choice" in task:
                    multiple_choice_score += datasets_len[task] * evaluation[task][metric]
                elif "word_gen" in task:
                    word_gen_score += datasets_len[task] * evaluation[task][metric]
                print(evaluation[task][metric])
                break

    single_choice_score /= datasets_len["single_choice"]
    multiple_choice_score /= datasets_len["multiple_choice"]
    word_gen_score /= datasets_len["word_gen"]

    model_params = contents["config"]["model_args"].split(",")
    model_name = None
    for param in model_params:
        if "pretrained" in param:
            model_name = param[11:]
        break

    eval_result = EvalResult(
        model=model_name,
        single_choice=single_choice_score,
        multiple_choice=multiple_choice_score,
        word_gen=word_gen_score,
    )

    db = DatabaseHelper()
    db.add_eval_result(eval_result)
