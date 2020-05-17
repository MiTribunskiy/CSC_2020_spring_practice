from difflib import SequenceMatcher
from fuzzywuzzy import fuzz
import re


class Similarity:
    
    @classmethod
    def match(cls, query, option, match_func):
        if isinstance(query, list):
#         matching options with 1st query identity only
#         consider improvements
            query = query[0]
        
        if isinstance(option, str):
            score = match_func(query, option)
            return score, option
        else:
            '''
            Assuming that options are sorted 
            from the most to the least relevant,
            pick first best in terms of score
            from list of options.            
            '''
            best_score = -1
            best_dropped = -1
            best_option = ''
            for n_droped, opt in enumerate(option):
                score = match_func(query, opt)
                if best_score < score:
                    best_score = score
                    best_dropped = n_droped
                    best_option = opt
            return (best_score, -best_dropped), best_option
    
    @classmethod
    def fuzzy_match(cls, str0, str1):
        '''
        Common tokens/words. Order does not matter.
        '''
        return fuzz.token_set_ratio(str0, str1)

    @classmethod
    def lcms_match(cls, str0, str1):
        '''
        Longest contiguous matching subsequence.
        '''
        return round(SequenceMatcher(None, str0, str1).ratio() * 100)

# rewrite with ENUM!
FUZZY = Similarity.fuzzy_match
LCMS = Similarity.lcms_match


class JunkProcessor:
    
    junk_list = {
        'ltd', 'limited',
        'inc', 'corp', 'corporation',
        'co', 'company'
    }
    
    @classmethod
    def _clean(cls, name):
        tokens = re.findall(r'[a-zA-Z0-9]+', name)
        clean_option = ' '.join(t for t in tokens
                               if t not in cls.junk_list)
        return clean_option        
    
    @classmethod
    def clean(cls, names):
        if isinstance(names, str):
            clean_results = {names: cls._clean(names)}
        else:
            clean_results = {n:cls._clean(n) for n in names}
        return clean_results
    
    @classmethod
    def add(cls, token):
        cls.junk_list.add(token)
    
    @classmethod
    def remove(cls, token):
        cls.junk_list.remove(token)
