# Parser for tasks from "Sdamgia"

This parser is using scrapy lib.

Currently, program parses tests from the Unified State Exam (EGE)
in Social Studies from the [sdamgia](https://soc-ege.sdamgia.ru/?redir=1) website.

## Structure

Program takes the EGE test id and the desired output file
name as command-line arguments. The parsing result is stored in a jsonl file
named **ege_data.jsonl**.

Additionally, in the *goat* folder, there is a script called **dataset_demonstration.py**.

After you run it (instructions on how to run it are provided below), it will display one task of each type
from the parsed test in the console.

## Usage

First, you need to install the necessary libraries. To do this, run the following command from the root folder:

`pip install -r requirements.txt`

To run the parser, navigate to the goat directory
and run the following command in the console:

`scrapy crawl ege -a test_id='your test id' -O ege_data.jsonl`

*your test id* is the test id for the Social Studies exam on the [sdamgia](https://soc-ege.sdamgia.ru/?redir=1) website.

Parser was tested on the test with id - 10861731.

To run the dataset_demonstration.py script, execute the following command in the root directory:

`python .\goat\dataset_demonstration.py`
