import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np

def clean_string(string):
    """
    Remove special characters and convert a string to lowercase.
    
    Parameters
    ----------
    string : str
        String to clean.

    Returns
    -------
    str
        Cleaned string.
    """
    return re.sub(r'\W+', ' ', string).lower()

def get_similarity(string1, string2):
    """
    Calculate similarity between two strings.
    
    Parameters
    ----------
    string1 : str
        First string.
    string2 : str
        Second string.

    Returns
    -------
    float
        Calculated similarity between string1 and string2.
    """
    string1_cleaned, string2_cleaned = clean_string(string1), clean_string(string2)
    
    # Initialize a 2D array for character comparisons
    comparison_matrix = np.array([[int(char1 == char2) for char1 in string1_cleaned] for char2 in string2_cleaned], dtype=np.int32)
    
    # Update matrix to account for consecutive character matches
    for i in range(1, comparison_matrix.shape[0]):
        for j in range(1, comparison_matrix.shape[1]):
            if comparison_matrix[i, j] > 0:
                comparison_matrix[i, j] += comparison_matrix[i-1, j-1]

    # Normalize similarity score by total comparisons
    similarity_score = np.sum(comparison_matrix) / comparison_matrix.size

    return similarity_score

def get_nearest_string(string, string_list):
    """
    Find the most similar string in a list to the given string.

    Parameters
    ----------
    source_strings : str
        String to compare against list.
    string : list of str
        List of strings to compare.

    Returns
    -------
    str
        The most similar string from the list.
    """
    _, max_index = max((get_similarity(string, option), index) for index, option in enumerate(string_list))
    return string_list[max_index]

def match_strings(source_strings, target_strings, n_jobs=None):
    """
    Map each string in the source list to its most similar string in the target list, optionally in parallel.
    
    Parameters
    ----------
    source_strings : list of str
        Source list of strings.
    target_strings : list of str
        Target list of strings.
    n_jobs : int, optional
        Number of parallel jobs. Sequential if None or 1.
        
    Returns
    -------
    dict
        Mapping of each source string to its most similar target string.
    """
    mapping = {}
    
    def map_string_to_similar(source_string):
        return source_string, get_nearest_string(source_string, target_strings)

    if n_jobs is None or n_jobs == 1:
        for string in source_strings:
            mapping[string] = get_nearest_string(string, target_strings)
    else:
        with ThreadPoolExecutor(max_workers=n_jobs) as executor:
            futures = {executor.submit(map_string_to_similar, string): string for string in source_strings}
            for future in as_completed(futures):
                source_string, similar_string = future.result()
                mapping[source_string] = similar_string

    return mapping