# crossword-generator

## Get started

Clone the repository

```shell
git clone git@github.com:Cereal38/crossword-generator.git
cd crossword-generator
```

Create a virtual environment and activate it

```shell
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies

```shell
pip install -r requirements.txt
```

## Scripts

### main.py

This script allows to generate a crossword puzzle

```shell
python main.py [args]
```

#### Arguments

| Argument             | Description                                           | Default value |
| -------------------- | ----------------------------------------------------- | ------------- |
| `-h`, `--help`       | Show the help message                                 |               |
| `-f`, `--file`       | Path to the .txt file containing the words (1)        |               |
| `-d`, `--db`         | Number of words to get from the database              | 5             |
| `-i`, `--iterations` | Number of iterations to get the best crossword puzzle | 50            |
| `-o`, `--out`        | Path of the output file (2)                           | grid.txt      |

(1) File format for the `--file` argument:

```text
word1 : definition1
word2 : definition2
...
```

(2) File format example for the `--out` argument:

```text
3x4
   H
SAVE
 S Y
1:hey:A way to say hello:0:3:v
2:save:Keep it for later:1:0:h
3:as:Like that:1:1:v
```

Note: You can't use the `--file` and `--db` arguments at the same time.
But you have to use one of them.

### db_client.py

This script allows to interact with the database.

```shell
python db_client.py
```

A database containing about 900 words and definitions comes with the project.
