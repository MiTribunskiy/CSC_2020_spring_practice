# Fuzzy string matching of companies' names

## About
This application provides help in finding legally associated companies.

Input:
- company name, whose related companies we would like to find (query)
- list of companies' names, among which the search is conducted (database)

Output:
- list of potentially associated companies

## Prerequisites:

- Unix shell
- Python, version >=3.6
- API key

API key is required to get access to [**Google Knowledge Graph Search API**](https://developers.google.com/knowledge-graph).\
To get your personal API key, visit: <https://developers.google.com/places/web-service/get-api-key>. Then save your API key in `data/.api_key` file.


## Setup:

To create virtual environment `.env_fuzzy` (with all necessary packages) and activate it, run in Unix shell:

```
source setup.sh
```

Once `.env_fuzzy` is created, the same command can be used to activate this virtual environment.


## Making queries:

To make queries, 2 files required:

- `<database>.csv` - .csv file with companies' names
- `<queries>.txt` - list of queries (separated by newlines '\n')

Query example:

```
python launcher.py -d <database>.csv -q <queries>.txt
```

### Header

By default, `<database>.csv` is considered to have no header.
Otherwise, use `--header` option:

```
python launcher.py -d <database>.csv -q <queries>.txt --header
```

### Column choice

By default, first column of `<database>.csv` is considered to be a list of companies' names.
To pick another columns, specify:

- column index (zero-based numbering), using option `-i`, `--iloc`:

```
python launcher.py -d <database>.csv -q <queries>.txt -i 2
```

- or column name, using option `-l`, `--loc`:

```
python launcher.py -d <database>.csv -q <queries>.txt -l "company name"
```

If `--loc` option is specified, `--header` option can be omitted.

### Output to file

By default, query results are written to stdout.
To write to a `.csv` file, use option `-o`, `--output`:

```
python launcher.py -d <database>.csv -q <queries>.txt -o <results>
```

One of the best ways to load a file with results `<results>.csv` is by using `pandas`:
```
import pandas as pd

df = pd.read_csv('<results>.csv', index_col=[0, 1])
```
This will create a `pandas.DataFrame` with `MultiIndex`, whose first index is a query name. Then to pick a part of the results, related to one specific query `<query>`, use:
```
query_df = df.loc[<query>]
```

### Help

Use option `-h` to access help menu:

```
$ python launcher.py -h

usage: launcher.py [-h] -d DATA -q QUERY [--header] [-i ILOC] [-l LOC]
                   [-o OUTPUT] [-t THRESHOLD]

optional arguments:
  -h, --help            show this help message and exit
  -d DATA, --data DATA  provide path to file with data
  -q QUERY, --query QUERY
                        provide path to file with queries
  --header              if specified: first line in datafile is treated as
                        header
  -i ILOC, --iloc ILOC  provide number of column with company names
  -l LOC, --loc LOC     provide name of column with company names
  -o OUTPUT, --output OUTPUT
                        provide path to output file (stdout by default)
  -t THRESHOLD, --threshold THRESHOLD
                        assign threshold value [0, 100] (80 by default)

```
