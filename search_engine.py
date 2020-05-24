from abc import ABC, abstractmethod

import json
from urllib.parse import urlencode, quote
from urllib.request import urlopen

import re
from collections import defaultdict
# from tqdm.notebook import tqdm
from tqdm import tqdm


class SearchEngine(ABC):
    
    @property
    @classmethod
    @abstractmethod
    def service_url(cls):
        pass
    
    @property
    @classmethod
    @abstractmethod
    def default_search_params(cls):
        pass
    
    @classmethod
    @abstractmethod
    def _get_identity(cls):
        pass
    
    @classmethod
    @abstractmethod
    def get_identities(cls):
        pass


class Google(SearchEngine):
    '''
    Tool for identifying queries with Google KGS
    '''
    
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    api_key = open('.api_key').read()
    default_search_params = {
        'limit': 1,
        'indent': True,
        'key': api_key,
    }
    
    # business_entity_set = set(open('business_entities.txt').read().split('\n'))
    business_entity_set = {
        'ltd', 'limited', 'ltda', 'llc',
        'inc', 'incorporated', 'corp', 'corporation',        
        'gbr', 'gmbh', 'ag',
        'a/s', 'as',
        'co', 'company'
    }
    
    # country_set = set(open('countries.txt').read().split('\n'))
    country_set = {
        'uk', 'france', 'germany', 'spain', 'italy', 'ireland', 'poland', 'switzerland',
        'us', 'latin', 'america', 'mexico', 'cuba', 'argentina',
        'korea', 'japan'
    }
    
    conjunction_set = {
        '&', '-'       
    }
    
    @classmethod
    def _get_identity(cls, search_params, extended=False):
        url = cls.service_url + '?' + urlencode(search_params)
#         print(url)
        response = json.loads(urlopen(url).read())
        
        identity_list = []
        for element in response['itemListElement']:
            qid = element['result']['name']
            # score = element['resultScore']
            identity_list.append(qid)
            if extended:
                try:
                    qid_ext = element['result']['detailedDescription']['articleBody']
                except KeyError:
                    qid_ext = ''
                identity_list.append(qid_ext)
                
        curr_len = len(identity_list)
        limit = search_params['limit']
        if extended:
            limit *= 2
        identity_list.extend([''] * (limit - curr_len))
        
        return identity_list
    
    @classmethod
    def get_identities(cls, queries, extra_params={}, extended=False):
        search_params = dict(cls.default_search_params)
        search_params.update(extra_params)
        
        identities_dict = {}
        for q in tqdm(queries, total=len(queries)):
            search_params['query'] = q.lower().strip()
            identity_list = cls._get_identity(search_params, extended=extended)
            identities_dict[q] = identity_list
        
        return identities_dict
        
    @classmethod
    def get_prefix_identities(cls, queries, extra_params={}, extended=False):
        search_params = dict(cls.default_search_params)
        search_params.update(extra_params)
        
        identities_dict = defaultdict(list)
        for q in tqdm(queries, total=len(queries)):
            # tokens = re.findall(r'[a-zA-Z0-9]+', q)
            # tokens = list(map(quote, q.split()))
            tokens = q.lower().split()
            for prefix_size in reversed(range(1, len(tokens) + 1)):
                search_params['query'] = ' '.join(tokens[:prefix_size])
                identity_list = cls._get_identity(search_params, extended=extended)
                identities_dict[q].extend(identity_list)
        
        return identities_dict
    
    @classmethod
    def get_subarray_identities(cls, queries, extra_params={}, extended=False):
        search_params = dict(cls.default_search_params)
        search_params.update(extra_params)
        
        identities_dict = defaultdict(list)
        for q in tqdm(queries, total=len(queries)):
            tokens = q.lower().split()
            prefix_imp = [0]
            for t_raw in tokens:
                t = t_raw.strip('().')
                if (t in cls.business_entity_set
                    or t in cls.country_set
                    or t in cls.conjunction_set):
                    token_imp = 0
                else:
                    token_imp = 1
                prefix_imp.append(prefix_imp[-1] + token_imp)
            
            n = len(tokens)
            for subarr_size in reversed(range(1, n + 1)):
                for L in range(n - subarr_size + 1):
                    R = L + subarr_size
                    subarr_importance = prefix_imp[R] - prefix_imp[L]
                    if subarr_importance:
                        search_params['query'] = ' '.join(tokens[L:R])
                        identity_list = cls._get_identity(search_params, extended=extended)
                        identities_dict[q].extend(identity_list)
        
        return identities_dict