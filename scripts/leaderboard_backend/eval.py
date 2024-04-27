# type: ignore
import subprocess

from database_helper import DatabaseHelper


def eval_model(model_name: str, precision: str, num_fewshot: str):
    subprocess.run(["./eval_script.sh", model_name, precision, num_fewshot])


if __name__ == "__main__":
    db_helper = DatabaseHelper()
    subprocess.run(["./build_script.sh"])
    db_helper.listen_to_new_requests(eval_model)
