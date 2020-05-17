from sklearn.metrics import roc_auc_score
from collections import defaultdict


def R_precision_score(results, options, query_label, R):
    ctr = 0
    for i, res in enumerate(results):
        if i == R:
            break
        opt = res['option']
        if options[opt] == query_label:
            ctr += 1
    return ctr / R


def diff(a, b):
    if isinstance(a, tuple):
        return tuple(x - y for x, y in zip(a, b))
    else:
        return a - b


def recall_score(results, options, query_label, R, threshold=80):
    ctr = 0
    size = 0
    if isinstance(threshold, str) and threshold.startswith('cluster'):
        size_limit = len(results)
        if threshold[7:].isnumeric():
            size_limit = min(int(threshold[7:]), size_limit)
        max_dist, size = None, 0
        for i in reversed(range(1, size_limit)):
            curr_dist = diff(results[i - 1]['score'], 
                             results[i]['score'])
            if not max_dist or curr_dist > max_dist:
                max_dist = curr_dist
                size = i
    else:
        if isinstance(results[0]['score'], tuple):
            threshold = (threshold, -float('inf'))
        for i, res in enumerate(results):
            if res['score'] < threshold:
                size = i
                break

    for i in range(size):
        opt = results[i]['option']
        if options[opt] == query_label:
            ctr += 1
    
    recall = ctr / R if R else 1
    return recall, size


def roc_score(results, options, query_label):
    y_score = [res['score'] for res in results]
    if isinstance(y_score[0], tuple):
        compressor = defaultdict(list)
        for i, score in enumerate(y_score):
            compressor[score].append(i)
        for code, score in enumerate(sorted(compressor)):
            for i in compressor[score]:
                y_score[i] = code                
    y_true = [int(options[res['option']] == query_label) for res in results]    
    try:
        return roc_auc_score(y_true, y_score)
    except ValueError:
        return 0


def precision_score(results, options, query_label):
    if not results:
        return 0
    
    ctr = 0
    n = len(results)
    for res in results:
        opt = res['option']
        if options[opt] == query_label:
            ctr += 1
    return ctr / n
