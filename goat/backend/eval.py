import json

from lm_eval import evaluator
from lm_eval.models.huggingface import HFLM

from goat.backend.add_results import add_results
from goat.utils.database_helper import DatabaseHelper


def eval(model_name: str, precision: str):
    lm = HFLM(pretrained=model_name, dtype=precision)
    taskname = "goat"
    results = evaluator.simple_evaluate(model=lm, tasks=[taskname])

    filename = model_name.replace("/", "__")
    with open(f"results/{filename}.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False)

    add_results(input_path=f"results/{filename}.json")


if __name__ == "__main__":
    db_helper = DatabaseHelper()
    db_helper.listen_to_new_requests(eval)
