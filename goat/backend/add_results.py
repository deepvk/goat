# type: ignore
import json

from datasets import get_dataset_config_names, load_dataset

from goat.utils.database_helper import DatabaseHelper, EvalResult


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


def get_metrics_values(tasks, evaluation, datasets_len):
    metrics = [
        "multi_choice_em_unordered,get-answer",
        "word_in_set,none",
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
                break

    single_choice_score /= datasets_len["single_choice"]
    multiple_choice_score /= datasets_len["multiple_choice"]
    word_gen_score /= datasets_len["word_gen"]

    return single_choice_score, multiple_choice_score, word_gen_score


def add_results(input_path):
    with open(input_path, "r") as j:
        contents = json.loads(j.read())
    evaluation = contents["results"]
    tasks = get_dataset_config_names("deepvk/goat")

    datasets_len = get_datasets_len(tasks)
    single_choice_score, multiple_choice_score, word_gen_score = get_metrics_values(tasks, evaluation, datasets_len)

    model_name = contents["config"]["model"]

    eval_result = EvalResult(
        model=model_name,
        single_choice=single_choice_score,
        multiple_choice=multiple_choice_score,
        word_gen=word_gen_score,
    )

    db = DatabaseHelper()
    db.add_eval_result(eval_result)
    db.end_connection()
