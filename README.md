# Parser for tasks from "Sdamgia"

This parser is using scrapy lib.

Currently, program parses tests from the Unified State Exam (EGE or OGE)
from the [sdamgia](https://sdamgia.ru/?redir=1) website.

## Structure

Program takes exam subject, exam type, test id and the desired output file
name as command-line arguments. The parsing result is supposed to be stored in a jsonl file.

Additionally, in the *goat* folder, there is a script called **dataset_demonstration.py**.

After you run it (instructions on how to run it are provided below), it will display one task of each type
from the parsed test in the console.

## Usage

First, you need to install the necessary libraries. To do this, run the following command from the root folder:

`pip install -r requirements.txt`

To run the parser, navigate to the goat directory
and run the following command in the console:

`scrapy crawl sdamgia -a subject='your exam subject' -a exam_type='your exam type' -a test_id='your test id' -O <output file>`

*your exam subject* indicates which subject the exam is in. Currently acceptable subject values are 'soc' and 'lit'.

*your exam type* indicates from what exam your test was taken. Currently acceptable exam type values are 'ege' and 'oge'.

*your test id* is the test id for Unified State Exam in chosen subject from the [sdamgia](https://sdamgia.ru/?redir=1) website.

*output file* is file name that parser will generate or overwrite with parsing output. For example - ege_data.jsonl.

To run the dataset_demonstration.py script, execute the following command in the root directory:

`python .\goat\dataset_demonstration.py -f <parser output file name>`

where *parser output file name* is the name of the jsonl file that parser has generated.
