import json
import os

import pandas as pd

from scripts.validation.scripts_utils import gen_full_prompt, get_k_shot_df


def test_full_prompt() -> None:
    dataset = pd.read_json(path_or_buf="./tests/data/prompt_testing_dataset.jsonl", lines=True)
    k_shot_df = get_k_shot_df(dataset, 0, 3)

    with open("./scripts/validation/prompts.json", "r") as file:
        prompts = json.load(file)
    starting_prompt = prompts["mmlu"]

    subject_dict = {"soc": "sociology", "lit": "literature"}
    max_seq_len = 10000

    prompt = gen_full_prompt(k_shot_df, dataset, 0, starting_prompt, subject_dict, max_seq_len)
    with open("./tests/data/expected_prompt.txt", "r", encoding="utf8") as f:
        expected_prompt = f.read()
    assert prompt == expected_prompt
