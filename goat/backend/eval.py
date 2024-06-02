# type: ignore
import json
import os
from pathlib import Path

from fastchat.llm_judge.gen_model_answer import run_eval
from fastchat.utils import str_to_torch_dtype
from lm_eval import evaluator
from lm_eval.models.huggingface import HFLM

from goat.backend.add_results import add_results
from goat.utils.database_helper import DatabaseHelper


def eval(model_name: str, precision: str, generate_fastchat: bool):
    lm = HFLM(pretrained=model_name, dtype=precision)
    taskname = "goat"
    results = evaluator.simple_evaluate(model=lm, tasks=[taskname])

    model_id = model_name.replace("/", "__")
    Path(f"goat/backend/results/{model_id}").mkdir(exist_ok=True)
    lm_eval_output_file = f"goat/backend/results/{model_id + '_lm_eval'}.json"
    with open(lm_eval_output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False)

    if generate_fastchat:
        fastchat_filename = os.path.join("goat/backend/results", model_id + "_fastchat.jsonl")
        question_file = "goat/backend/data/question.jsonl"

        run_eval(
            model_path=model_name,
            model_id=model_id,
            answer_file=fastchat_filename,
            question_file=question_file,
            question_begin=None,
            question_end=None,
            max_new_token=1024,
            num_choices=1,
            num_gpus_per_model=1,
            num_gpus_total=1,
            max_gpu_memory=None,
            dtype=str_to_torch_dtype(precision),
            revision="main",
        )

    add_results(input_path=lm_eval_output_file)


if __name__ == "__main__":
    db_helper = DatabaseHelper()
    db_helper.listen_to_new_requests(eval)
