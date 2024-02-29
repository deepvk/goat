import json
from typing import Any

import numpy as np
import pandas as pd
import torch
from arg_parser import get_parser
from scripts_utils import gen_full_prompt, get_k_shot_df
from transformers import AutoModelForCausalLM, AutoTokenizer


def get_logits(model: AutoModelForCausalLM, tokenizer: AutoTokenizer, task: str, device: str) -> np.ndarray:
    messages = [
        {"role": "user", "content": task},
    ]
    input_ids = tokenizer.apply_chat_template(messages, tokenize=True, return_tensors="pt")
    input_ids = input_ids.to(device)
    with torch.inference_mode():
        logits = model(input_ids).logits[:, -1, :]
    return logits


def get_answer(model: AutoModelForCausalLM, tokenizer: AutoTokenizer, task: str, device: str) -> int:
    logits = get_logits(model, tokenizer, task, device)
    possible_answers = ["1", "2", "3", "4"]
    tokenized_answers = [tokenizer.convert_tokens_to_ids(str_ans) for str_ans in possible_answers]
    needed_logits = [logits[0][ans] for ans in tokenized_answers]
    max_val = max(needed_logits)
    answer = -1
    for i in range(4):
        if needed_logits[i] == max_val:
            answer = i + 1
            break
    return answer


def compute_accuracy(
    model: AutoModelForCausalLM,
    tokenizer: AutoTokenizer,
    val_df: pd.DataFrame,
    device: str,
    starting_prompt: str,
    subject_dict: dict[str, str],
    max_seq_len: int,
) -> tuple[np.floating[Any], dict[int, int]]:
    scores = []
    answers_dict = {}
    for i in range(len(val_df)):
        k_shot_df = get_k_shot_df(val_df, i, args.k_shot)
        prompt = gen_full_prompt(k_shot_df, val_df, i, starting_prompt, subject_dict, max_seq_len)
        model_answer = get_answer(model, tokenizer, prompt, device)

        if model_answer not in answers_dict:
            answers_dict[model_answer] = 0
        answers_dict[model_answer] += 1

        if model_answer == val_df["answer"][i]:
            scores.append(1)
        else:
            scores.append(0)

    return np.mean(scores), answers_dict


def load_model_tokenizer(
    model_path: str, device: str, torch_dtype: torch.dtype | None
) -> tuple[AutoModelForCausalLM, AutoTokenizer]:
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    if torch_dtype is not None:
        model = AutoModelForCausalLM.from_pretrained(model_path, device_map=device, torch_dtype=torch_dtype)
    else:
        model = AutoModelForCausalLM.from_pretrained(model_path, device_map=device)

    model.eval()

    return model, tokenizer


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    dataset = pd.read_json(path_or_buf=args.dataset_path, lines=True)

    torch_dtype = None
    if args.torch_dtype is not None:
        if args.torch_dtype == "float16":
            torch_dtype = torch.float16
        elif args.torch_dtype == "float32":
            torch_dtype = torch.float32

    model, tokenizer = load_model_tokenizer(args.model_path, args.device, torch_dtype)
    max_seq_len = model.config.max_position_embeddings

    with open("./scripts/validation/prompts.json", "r") as file:
        prompts = json.load(file)
    starting_prompt = prompts[args.prompt_type]

    subject_dict = dict()
    if args.prompt_type == "mmlu":
        subject_dict = {"soc": "sociology", "lit": "literature"}
    else:
        subject_dict = {"soc": "обществознание", "lit": "литература"}

    accuracy, answers_distribution = compute_accuracy(
        model, tokenizer, dataset, args.device, starting_prompt, subject_dict, max_seq_len
    )

    output_dict = dict()
    output_dict["model_path"] = args.model_path
    output_dict["device"] = args.device
    output_dict["k_shot"] = args.k_shot
    output_dict["prompt"] = starting_prompt
    if args.torch_dtype:
        output_dict["torch_dtype"] = args.torch_dtype
    output_dict["accuracy"] = accuracy
    output_dict["answers_distribution"] = answers_distribution

    with open(args.output_path, "w", encoding="utf-8") as file:
        json.dump(output_dict, file, ensure_ascii=False)
