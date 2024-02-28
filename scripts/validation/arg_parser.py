import argparse


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="This program prints different tasks from input file")
    parser.add_argument("dataset_path", type=str, help="Relative path to validation dataset")
    parser.add_argument("model_path", type=str, help="Path to model on HuggingFace hub")
    parser.add_argument("output_path", type=str, help="Path to the file in which output will be written")
    parser.add_argument(
        "-d", "--device", required=False, type=str, help="Can be cpu, some cuda devices or auto", default="cuda"
    )
    parser.add_argument(
        "-prompt",
        "--prompt_type",
        required=False,
        type=str,
        choices=["mmlu", "mmlu_translated", "not_mmlu"],
        help="Choice of prompt to model",
        default="mmlu",
    )
    parser.add_argument(
        "-dtype",
        "--torch_dtype",
        required=False,
        type=str,
        choices=["float32", "float16"],
        help="Type of model's weights",
    )
    parser.add_argument("-k", "--k_shot", required=False, type=int, help="Number k for k-shot validation", default=0)
    return parser
