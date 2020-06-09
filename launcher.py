import argparse

import pandas as pd

from tools.search_engine import *
from tools.processed import *
from tools.visual import *


parser = argparse.ArgumentParser()

# required argument
parser.add_argument("-d", "--database",
                    required=True,
                    help="provide path to file with database")

# at least one argument is required
parser.add_argument("-q", "--query",
                    metavar="QUERY", dest="queries", action="append", default=[],
                    help="add search query")
parser.add_argument("-f", "--file",
                    metavar="QUERYFILE",
                    help="provide path to file with queries")


# optional mutually exclusive arguments
exclusive = parser.add_mutually_exclusive_group()
exclusive.add_argument("-i", "--iloc",
                       help="provide number of column with company names")
exclusive.add_argument("-l", "--loc",
                       help="provide name of column with company names")

# other optional arguments
parser.add_argument("-e", "--header",
                    action="store_const", const=0,
                    help="if specified: first line in datafile is treated as header")
parser.add_argument("-o", "--output",
                    help="provide path to output file (stdout by default)")
parser.add_argument("-t", "--threshold",
                    type=int, default=80,
                    help="assign threshold value [0, 100] (80 by default)")
parser.add_argument("-s", "--showextra",
                    type=int, default=5,
                    help="assign how many extra companies whose score is less than threshold are shown (5 by default)")

# process command line arguments
args = parser.parse_args()
path_db = args.database
queries = args.queries
path_queries = args.file
if not (queries or path_queries):
    parser.error('No query specified, add -q or -f argument')
elif path_queries:
    queries.extend(q for q in open(path_queries).readlines() if q)

path_output = args.output
company_loc = args.loc
company_iloc = args.iloc
header = 0 if company_loc else args.header
threshold = min(max(args.threshold, 0), 100)
show_extra = max(args.showextra, 0)


# load identities of companies processed earlier 
processed_companies = Processed.load_csv()


# load database and extract companies' names
df = pd.read_csv(path_db, header=header)
if company_loc:
    options = df[company_loc]
elif company_iloc:
    options = df.iloc[:, company_iloc]
else:
    options = df.iloc[:, 0]


# search identities of new companies from database
new_keys = set()
for opt in options:
    key = opt.lower()
    if key not in processed_companies:
        new_keys.add(key)
if new_keys:
    print(f'Searching identities for #{len(new_keys)} new companies from database:')
    new_opt_ids = Google.get_subarray_identities(new_keys,
                                                 extra_params={'limit':5, 'types': 'Organization'},
                                                 extended=True, reorder=True)
    Processed.update_csv(new_opt_ids)
else:
    print(f'All companies from database found in: "{Processed.filepath}"')
    new_opt_ids = {}


# assign identities to all companies from database
option_ids = {}
for opt in options:
    key = opt.lower()
    if key in processed_companies:
        option_ids[opt] = processed_companies[key]
    else:
        option_ids[opt] = new_opt_ids[key]


# search identities of the queries
print(f'Searching identities of the queries:')
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
              show_extra=show_extra, 
              path_output=path_output);