import pickle
import os

def save_data(data, filepath, check=True):
    if not filepath.endswith('.pickle'):
        filepath += '.pickle'
    
    with open(filepath, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    if check:
        with open(filepath, 'rb') as handle:
            saved_data = pickle.load(handle)
        assert data == saved_data


def load_data(filepath, folder=None):
    if not filepath.endswith('.pickle'):
        filepath += '.pickle'
    
    with open(filepath, 'rb') as handle:
        return pickle.load(handle)   
