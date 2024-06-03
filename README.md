# GOAT

This project consists of three different subprojects:
- Parser for tasks from Russian USE;
- Script for validation of HF models on GOAT dataset;
- Web app with models' leaderboard after their validation on GOAT dataset;


## Installation
Firstly, you need to install the necessary libraries. To do this, run the following commands:

```bash
pip install -r requirements.txt
```

## Parser
This parser was used to gather tasks for GOAT dataset. It is using Scrapy lib.

Currently, program parses tests from the Unified State Exam (EGE or OGE)
from the [sdamgia](https://sdamgia.ru/?redir=1) website.

### Structure

Program takes exam subject, exam type, test id and the desired output file
name as command-line arguments. The parsing result is supposed to be stored in a jsonl file.

Additionally, in the *goat* folder, there is a script called **dataset_demonstration.py**.

After you run it (instructions on how to run it are provided below), it will display one task of each type
from the parsed test in the console.

### Usage
To run the parser, run the following command from goat/parser directory:

```bash
scrapy crawl sdamgia \
    -a subject='your exam subject' \
    -a exam_type='your exam type' \
    -a test_id='your test id' \
    -O <output file>
```

*your exam subject* indicates which subject the exam is in. Currently acceptable subject values are 'soc' and 'lit'.

*your exam type* indicates from what exam your test was taken. Currently acceptable exam type values are 'ege' and 'oge'.

*your test id* is the test id for Unified State Exam in chosen subject from the [sdamgia](https://sdamgia.ru/?redir=1) website.

*output file* is file name that parser will generate or overwrite with parsing output. For example - ege_data.jsonl.

To run the dataset_demonstration.py script, execute the following command from the root directory:

`python goat/parser/dataset_demonstration.py -f <parser output file name>`

where *parser output file name* is the name of the jsonl file that parser has generated.

## Leaderboard frontend

### Structure
My leaderboard follows similar structure that [Open LLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard) uses.
It is a gradio web app that is used in a HuggingFace space. Database info is stored in environment variables.

### Usage
In this app you can send your model validation request to
backend database and after some time validation result on your model will appear
in the leaderboard folder after reloading the app.

To run leaderboard web app execute this command from root directory
(it is supposed that you have set all needed environment variables for database connection):

`python -m goat.frontend.app`

## Leaderboard backend

### Structure
Leaderboard backend after receiving new validation request validate
the model in the request on GOAT dataset using modified
[LM Evaluation Harness benchmark](https://github.com/deepvk/lm-evaluation-harness/tree/goat) from deepvk repository.
After finishing validation it adds the resulting scores in the leaderboard.

### Usage
Firstly, you need to install one additional library to run leaderboard backend. To do this, run the following commands:

```bash
pip install -U wheel
pip install flash-attn==2.5.8
```

To run leaderboard backend execute this command from root directory
(it is supposed that you have set all needed environment variables for database connection):

`python -m goat.backend.eval`

After running the script, it will listen to new validation requests in the database.
After receiving new request it will start validating the model in the request on GOAT dataset.
After getting results of the validation it will add these results in leaderboard table in database.
