# Topic Modeling

Topic Modeling Algorithm

## Instructions

  * `mbox-parser/parser.py`: parser mbox file to generates the txt file (topic modeling input);
  * `topic-modeling/topic-modeling.py`: Topic Modeling Algorithm.

### Running mbox-parser/parser.py

Command: `python3 mbox-parser/parser.py filename`

usage: parser.py [-h] [-o O] [-l L] filename

positional arguments:
  filename    Input file

optional arguments:
  -h, --help  show this help message and exit
  -o O        Output file (default: output.txt).
  -l L        Max number of items (default: None -- No limits).

### Running topic-modeling.py

Command: `python3 topic-modeling.py filename`

usage: topic-modeling.py [-h] [-a {lda,nmf}] [-t T] filename

positional arguments:
 filename      Input the filename

optional arguments:
 -h, --help    show this help message and exit
 -a {lda,nmf}  Choose LDA or NMF algorithm (default: nmf).
 -t T          Set the number of topics (default: 5).

## Samples

[http://puredata.info/community/lists](http://puredata.info/community/lists)
