# Parser for tasks from "Sdamgia"

This parser is using scrapy lib.

Currently, program parses tests from the Unified State Exam (EGE or OGE)
in Social Studies from the [soc-ege.sdamgia](https://soc-ege.sdamgia.ru/?redir=1) and [soc-oge.sdamgia](https://soc-oge.sdamgia.ru/?redir=1) websites.

## Structure

Program takes exam type, test id and the desired output file
name as command-line arguments. The parsing result is supposed to be stored in a jsonl file.

Additionally, in the *goat* folder, there is a script called **dataset_demonstration.py**.

After you run it (instructions on how to run it are provided below), it will display one task of each type
from the parsed test in the console.

## Usage

First, you need to install the necessary libraries. To do this, run the following command from the root folder:

`pip install -r requirements.txt`

To run the parser, navigate to the goat directory
and run the following command in the console:

`scrapy crawl ege -a exam_type='your exam type' -a test_id='your test id' -O <output file>`

*your exam type* indicates from what exam your test was taken. Currently acceptable exam type values are 'ege' and 'oge'.

*your test id* is the test id for the Social Studies exams from the [soc-ege.sdamgia](https://soc-ege.sdamgia.ru/?redir=1) or [soc-oge.sdamgia](https://soc-oge.sdamgia.ru/?redir=1) websites.

*output file* is file name that parser will generate or overwrite with parsing output. For example - ege_data.jsonl.

Parser was tested on the test with id - 10861731.

To run the dataset_demonstration.py script, execute the following command in the root directory:

`python .\goat\dataset_demonstration.py <parser output file name>`

where *parser output file name* is the name of the jsonl file that parser has generated.
