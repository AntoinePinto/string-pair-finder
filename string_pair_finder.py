import re
from itertools import product
import pandas as pd
import numpy as np

def clean(string: str) -> str:
    """Erase special characters and lowercase a string"""
    return re.sub(r'[^a-zA-Z0-9]+', ' ', string).lower()

def pair_similarity(s1: str, s2: str) -> float:
    """Compute StringPairFinder similarity score between two strings"""
    s1, s2 = clean(s1), clean(s2)
    data = np.vstack([[int(c1 == c2) for c1 in s1] for c2 in s2])
    for i in range(1, len(s2)): 
        for j in range(1, len(s1)):
            bef = data[i-1, j-1]
            if (bef*data[i, j]) > 0:
                data[i, j] = bef * 2
    return data.sum()/(data.shape[0]*data.shape[1])

def get_pairs(list1: list, list2: list) -> pd.DataFrame:
    """Link each string in list1 with the most similar in list2 according to
    StringPairFinder similarity score"""
    combinations = list(product(list1, list2))
    data = pd.DataFrame(combinations, columns=['list1', 'list2'])
    data['score'] = [pair_similarity(i, j) for i, j in combinations]
    data = data.loc[data.groupby("list1")["score"].idxmax()].set_index('list1')
    
    return data