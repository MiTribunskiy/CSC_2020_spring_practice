from matching import *


def template(*info):
    return '{:50}{:15}{:50}'.format(*map(lambda x: str(x)[:49], info))


def print_results(queries, options, match_func=FUZZY, query_identities={}, option_identities={}, total_limit=5, use_limit=None,
                  threshold=80, show_extra=2, path_output=None):
    
    key_order = ['option', 'score', 'identity']
    n = len(options)
    
    ouf = open(path_output, 'w', encoding='utf-8') if path_output else None
    print(template(*key_order), file=ouf)
    print('=' * 70, file=ouf)
    
    for i, q in enumerate(queries):
        query_label = i + 1
        q_id = query_identities.get(q, q)
        curr_limit = 1 if use_limit is None else use_limit
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
        
        print(template(f'{q} (query)', '-', q_id), file=ouf)
    
        print('-' * 70, file=ouf)
        print('   Output', file=ouf)
        print('-' * 70, file=ouf)
        for i in range(ctr_found + show_extra):
            res = results[i]
            if i == ctr_found:
                print('-' * 70, file=ouf)
            print(template(*(res[key] for key in key_order)), file=ouf)
            
        print('=' * 70, file=ouf)
    
    if ouf:
        ouf.close()
    