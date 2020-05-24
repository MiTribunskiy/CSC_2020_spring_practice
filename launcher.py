import argparse

import pandas as pd

from search_engine import *
from processed import *
from visual import *

parser = argparse.ArgumentParser()


# required arguments
parser.add_argument("-d", "--data",
                    required=True,
                    help="provide path to file with data")
parser.add_argument("-q", "--query",
                    required=True,
                    help="provide path to file with queries")

# optional arguments
parser.add_argument("--header",
                    action="store_const", const=0,
                    help="if specified: first line in datafile is treated as header")
parser.add_argument("-i", "--iloc",
                    type=int, default=0,
                    help="provide number of column with company names")
parser.add_argument("-l", "--loc",
                    help="provide name of column with company names")
parser.add_argument("-o", "--output",
                    help="provide path to output file (stdout by default)")
parser.add_argument("-t", "--threshold",
                    type=int, default=80,
                    help="assign threshold value [0, 100] (80 by default)")


# process command line arguments
args = parser.parse_args()
path_db = args.data
path_query = args.query
path_output = args.output
company_loc = args.loc
company_iloc = args.iloc
header = 0 if company_loc else args.header
threshold = args.threshold
if threshold < 0:
    threshold = 0
elif threshold > 100:
    threshold = 100


# load identities of companies processed earlier 
processed_companies = Processed.load_csv()


# load database and extract companies' names
df = pd.read_csv(path_db, header=header)
if company_loc:
    options = df[company_loc]
else:
    options = df.iloc[:, company_iloc]


# search identities of new companies from database
new_keys = set()
for opt in options:
    key = opt.lower()
    if key not in processed_companies:
        new_keys.add(key)

print(f'Searching identities for #{len(new_keys)} new companies from database:')
new_opt_ids_raw = Google.get_subarray_identities(new_keys,
                                                  extra_params={'limit':5, 'types': 'Organization'},
                                                  extended=True)
new_opt_ids = reorder_identities(new_opt_ids_raw,
                                 limit=5,
                                 extended=True)
Processed.update_csv(new_opt_ids)


# assign identities to all companies from database
option_ids = {}
for opt in options:
    key = opt.lower()
    if key in processed_companies:
        option_ids[opt] = processed_companies[key]
    else:
        option_ids[opt] = new_opt_ids[key]


# load queries
queries = open(path_query).read().strip().split('\n')


# search identities of the queries
print(f'Searching identities for queries:')
query_ids = Google.get_identities(queries, 
                                  extra_params={'types': 'Organization'})


# output relevant companies
print_results(queries=queries,
              options=options,
              match_func=FUZZY,
              query_identities=query_ids, 
              option_identities=option_ids,
              use_limit=5,
              total_limit=5,
              threshold=threshold, 
              show_extra=5, 
              path_output=path_output);