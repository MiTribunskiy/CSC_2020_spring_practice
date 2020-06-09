# Fuzzy string matching of companies' names

## About
This application provides help in finding legally associated companies.

Input:
- company name, whose related companies we would like to find (query)
- list of companies' names, among which the search is conducted (database)

Output:
- list of potentially associated companies

## Prerequisites:

- Python, version >=3.6
- Unix shell (for dependency management)
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

To make queries, specify 2 parameters:

- path to a `.csv` file with companies' name, using argument `-d <database>.csv`
- list of queries, using `-q <query>` or `-f <queryfile>` arguments (or even both)

Queries in `<queryfile>` should be separated by newlines.

Query examples:

```
python launcher.py -d <database>.csv -q <some_company_1> -q <some_company_2>
```

```
python launcher.py -d <database>.csv -f <queryfile>
```

### Header

By default, `<database>.csv` is considered to have no header.
Otherwise, use `-e`, `--header` argument:

```
python launcher.py -d <database>.csv -q <company_name> -e
```

### Column choice

By default, first column of `<database>.csv` is considered to be a list of companies' names.
To pick another column, specify one of the following:

- column index (zero-based numbering), using `-i`, `--iloc` argument:

```
python launcher.py -d <database>.csv -q <company_name> -i 2
```

- or column name, using `-l`, `--loc` argument:

```
python launcher.py -d <database>.csv -q <company_name> -l "company names"
```

If `--loc` is specified, `--header` can be omitted.

### Output to file

By default, query results are written to stdout.
To write them to a `.csv` file, use `-o`, `--output` argument:

```
python launcher.py -d <database>.csv -q <company_name> -o <results>
```

One neat way to load results from `<results>.csv` is by using `pandas`:
```
import pandas as pd

df = pd.read_csv('<results>.csv', index_col=[0, 1])
```
This will create a `pandas.DataFrame` with `MultiIndex`, whose first index is a query name. Then to pick a part of the results, related to one specific query `<query>`, use:
```
query_df = df.loc[<query>]
```

### Help

Use `-h` argument to access help menu:

```
>python launcher.py -h

usage: launcher.py [-h] -d DATABASE [-q QUERY] [-f QUERYFILE]
                   [-i ILOC | -l LOC] [-e] [-o OUTPUT] [-t THRESHOLD]
                   [-s SHOWEXTRA]

optional arguments:
  -h, --help            show this help message and exit
  -d DATABASE, --database DATABASE
                        provide path to file with database
  -q QUERY, --query QUERY
                        add search query
  -f QUERYFILE, --file QUERYFILE
                        provide path to file with queries
  -i ILOC, --iloc ILOC  provide number of column with company names
  -l LOC, --loc LOC     provide name of column with company names
  -e, --header          if specified: first line in datafile is treated as
                        header
  -o OUTPUT, --output OUTPUT
                        provide path to output file (stdout by default)
  -t THRESHOLD, --threshold THRESHOLD
                        assign threshold value [0, 100] (80 by default)
  -s SHOWEXTRA, --showextra SHOWEXTRA
                        assign how many extra companies whose score is less
                        than threshold are shown (5 by default)
```