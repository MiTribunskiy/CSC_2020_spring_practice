import pandas as pd
from collections import defaultdict
from matching import *
from metrics import *


def template(*info):
    return '{:35}{:15}{:10}{:35}'.format(*map(lambda x: str(x)[:34], info))


def print_results(queries, options, match_func=FUZZY, query_identities={}, option_identities={}, total_limit=5, use_limit=None,
                  threshold=80, show_extra=2, method_name=None):
    avg_recall = 0
    avg_prec = 0
    
    avg_recall_size_weight = 0
    total_relevant = 0
    avg_prec_size_weight = 0
    total_output = 0
    
    
    # preproc
    classes = defaultdict(set)
    for k, v in options.items():
        classes[v].add(k)
    
    # for recall and R-prec
    N_true = [0] * (len(queries) + 1)
    for v in options.values():
        N_true[v] += 1
    
    key_order = ['option', 'score', 'isTrue', 'identity']
    n = len(options)
    
    print(template(*key_order))
    print('=' * 70)
    
    for i, q in enumerate(queries):
        query_label = i + 1
        required = classes[query_label].copy()
        q_id = query_identities.get(q, q)
        curr_limit = 1 if use_limit is None else use_limit
        while True:
            ctr_found = 0
            results = []
            res = {}
            for opt, label in options.items():
                opt_id = option_identities.get(opt, opt)
                frac = len(opt_id) // total_limit * curr_limit
                opt_id = opt_id[:frac]
                score, best_opt_id = Similarity.match(q_id, opt_id, match_func=match_func)
                if score[0] >= threshold:
                    ctr_found += 1
                res['option'] = opt
                res['score'] = score
                res['isTrue'] = int(label == query_label)
                res['identity'] = best_opt_id
                results.append(res.copy())
            if ctr_found >= 10 or use_limit or curr_limit >= total_limit:
                break
            else:
                curr_limit += 1

        results.sort(key=lambda x: x['score'], reverse=True)
        
        R = N_true[query_label]
        recall, output_size = recall_score(results, options, query_label, R, threshold=threshold)
        prec = precision_score(results[:output_size], options, query_label)
#         Rprec = R_precision_score(results, options, query_label, R)        
#         roc = roc_score(results, options, query_label=query_label)
        print(template(f'{q} (query)', '-', '-', q_id))
    
        print('-' * 70)
        print('   Output')
        print('-' * 70)
        for i in range(output_size + show_extra):
            res = results[i]
            if i < output_size:
                required.discard(res['option'])
            elif i == output_size:
                print('-' * 70)
            print(template(*(res[key] for key in key_order)))
            
        print('-' * 70)
        print('   Missed')
        print('-' * 70)
        for res in results:
            opt = res['option']
            if opt in required:
                print(template(*(res[key] for key in key_order)))              
        
        print('-' * 70)
        print(f'Search limit: {curr_limit}/{total_limit}')        
        print(f'Recall (t={threshold}, size={output_size}): {recall:.4f}')
        print(f'Precision: {prec:.4f}')
#         print(f'R-precision: {Rprec:.4f}')
#         print(f'ROC AUC: {roc:.4f}')
        print('=' * 70)
    
        avg_recall += recall 
        avg_prec += prec
        avg_recall_size_weight += recall * R
        total_relevant += R
        avg_prec_size_weight += prec * output_size
        total_output += output_size
        
        if method_name:
            Results.update(method_name, q, 'Recall', recall)
            Results.update(method_name, q, 'Precision', prec)
#             Results.update(method_name, q, 'Rprec', Rprec)
#             Results.update(method_name, q, 'ROC', roc)
    
    avg_recall /= len(queries)
    avg_prec /= len(queries)
    avg_recall_size_weight /= total_relevant
    avg_prec_size_weight /= total_output
    
    print(f'Recall (queries are equal): {avg_recall:.4f}')
    print(f'Precision (queries are equal): {avg_prec:.4f}')
    print(f'Recall (weight = amount of relevant): {avg_recall_size_weight:.4f}')
    print(f'Precision (weight = size of output): {avg_prec_size_weight:.4f}')
    return avg_recall, avg_prec, avg_recall_size_weight, avg_prec_size_weight
        


class Results:
    table = pd.DataFrame()
    table.index.name = 'method'

    @classmethod
    def update(cls, method, query, metric, score):
        cls.table.at[method, f'{metric}_{query}'] = score
    
    @classmethod
    def show(cls):
        display(cls.table)


def reorder_identities(option_identities, limit=5):
    '''
    identities sorted by the position in GKGS results
    case: extended=True
    '''
    option_ids_reordered = {}
    for key, identities in option_identities.items():
        reordered_identities = [None] * len(identities)
        section = len(identities) // limit
        for i, val in enumerate(identities):
            subarr_i, pos = divmod(i, limit * 2)
            new_i = subarr_i * 2 + (pos & 1) + section * (pos // 2)
            reordered_identities[new_i] = val
        option_ids_reordered[key] = reordered_identities
    return option_ids_reordered
    
    