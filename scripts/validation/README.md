# Validation of HF models on single choice tasks

## Structure

Program takes path to validation dataset, path to model on HF and output file name
as required command-line arguments. Also you can specify model device and torch_dtype arguments and
which prompt type you want to use. For more precise input configuration from root directory run this code:

`python scripts\validation\validate.py -h`

The validation result is supposed to be stored in a json file.

Output of the script contains arguments of this current script run and resulting model accuracy with model answers distribution dict.
Output file is encoded in utf8.

## Usage

First, you need to install the necessary libraries. To do this, run the following command from the root directory:

`pip install -r requirements.txt`

To run the validation script, run this command:

`python scripts\validation\validate.py  <validation dataset path> <path to model on HF hub> <output file>`

Example of TinyLlama model validation:

`python scripts\validation\validate.py single_choice_tasks.jsonl TinyLlama/TinyLlama-1.1B-Chat-v1.0 output.json`

If you want to use k-shot validation you should specify k value. For example, command for 3-shot validation:

`python scripts\validation\validate.py single_choice_tasks.jsonl TinyLlama/TinyLlama-1.1B-Chat-v1.0 output.json -k 3`
