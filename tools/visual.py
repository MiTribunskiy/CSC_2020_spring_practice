from tools.matching import *
import pandas as pd


def print_results(queries, options, match_func=FUZZY, query_identities={}, option_identities={}, total_limit=5, use_limit=None,
                  threshold=80, show_extra=2, path_output=None):
    
    output_df = df = pd.DataFrame()
    n = len(options)
    
    for i, q in enumerate(queries):
        q_id = query_identities.get(q, q)
        curr_limit = 1 if not use_limit else use_limit
        while True:
            ctr_found = 0
            results = []
            res = {}
            for opt in options:
                opt_id = option_identities.get(opt, opt)
                frac = len(opt_id) // total_limit * curr_limit
                opt_id = opt_id[:frac]
                score, best_opt_id = Similarity.match(q_id, opt_id, match_func=match_func)
                if score[0] >= threshold:
                    ctr_found += 1
                res['option'] = opt
                res['score'] = score
                res['identity'] = best_opt_id
                results.append(res.copy())
            if ctr_found >= 10 or use_limit or curr_limit >= total_limit:
                break
            else:
                curr_limit += 1

        results.sort(key=lambda x: x['score'], reverse=True)
        query_df = pd.DataFrame(data=[{'option': q, 'score': 'QUERY', 'identity':q_id[0]}])
        query_df = query_df.append(results[:ctr_found + show_extra], ignore_index=True)
#         prepend to index
        query_df = pd.concat([query_df], keys=[q], names=['query'])
        output_df = pd.concat([output_df, query_df])

    if path_output:
        ext = '.csv'
        if not path_output.endswith(ext):
            path_output += ext
        output_df.to_csv(path_output, index=True)
    else:
        print(output_df)
