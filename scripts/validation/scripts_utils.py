import pandas as pd


def gen_prompt(df: pd.DataFrame, idx: int, include_answer: bool = True) -> str:
    prompt = df["task_text"][idx]
    prompt += "\nAnswer:"
    if include_answer:
        prompt += " {}\n\n".format(df["answer"][idx])
    return prompt


def gen_k_shot_prompt(k_shot_df: pd.DataFrame, starting_prompt: str) -> str:
    k_shot_prompt = starting_prompt
    for i in range(len(k_shot_df)):
        k_shot_prompt += gen_prompt(k_shot_df, i)

    return k_shot_prompt


def gen_full_prompt(
    k_shot_df: pd.DataFrame,
    val_df: pd.DataFrame,
    i: int,
    starting_prompt: str,
    subject_dict: dict[str, str],
    max_seq_len: int,
) -> str:
    filled_starting_prompt = starting_prompt.format(subject_dict[val_df["subject"][i]])
    k_shot_prompt = gen_k_shot_prompt(k_shot_df, filled_starting_prompt)
    final_prompt = gen_prompt(val_df, i, include_answer=False)
    prompt = k_shot_prompt + final_prompt

    k = len(k_shot_df) - 1
    while k >= 0 and len(prompt) > max_seq_len:
        k_shot_prompt = gen_k_shot_prompt(k_shot_df[:k], filled_starting_prompt)
        prompt = k_shot_prompt + final_prompt
        k -= 1

    return prompt


def get_k_shot_df(val_df: pd.DataFrame, i: int, k: int) -> pd.DataFrame:
    same_tasks = val_df[(val_df["topic_id"] == val_df["topic_id"][i]) & (val_df["exam_type"] == val_df["exam_type"][i])]
    if i in same_tasks.index:
        same_tasks = same_tasks.drop(i, axis=0)
    same_tasks = same_tasks.sample(frac=1, random_state=1).reset_index(drop=True)
    if k < len(same_tasks):
        return same_tasks[:k]
    else:
        return same_tasks
