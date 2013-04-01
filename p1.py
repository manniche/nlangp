#!/usr/bin/env python

from collections import defaultdict

def count_wordtags( counts ):
    """
    >>> count_wordtags([[2, "WORDTAG", "O", "infection"],[ 1, "WORDTAG", "I-GENE", "UEV1A"],[ 1, "WORDTAG", "O", "Hospital"]])#doctest:+ELLIPSIS
    defaultdict(..., {'I-GENE': {'tag_count': 1, 'word_count': defaultdict(<type 'int'>, {'UEV1A': 1})}, 'O': {'tag_count': 3, 'word_count': defaultdict(<type 'int'>, {'Hospital': 1, 'infection': 2})}})
    """
    observations = __makedd()
    
    for observation in counts:
        if not observation or observation[1] != "WORDTAG":
            continue
        count = int( observation[0] )
        observations[ observation[2] ][ "tag_count" ] += count
        observations[ observation[2] ][ "word_count" ][ observation[3] ] += count

    return observations

def find_tag_for_word( observations, word ):
    """
    >>> obs = count_wordtags([[2, "WORDTAG", "O", "infection"],[ 1, "WORDTAG", "I-GENE", "UEV1A"],[ 1, "WORDTAG", "O", "Hospital"]])
    >>> word = "Hospital"
    >>> find_tag_for_word( obs, word )

    """

    maximum_probability = 0.0
    best_tag = None

    rarewords = [ word for word in not is_in_observations(observations, word) ]

    for observation in observations:
        if word in rarewords:
            word = "_RARE_"
        prob = observations[observation]["word_counts"][word] / observations[observation]["total_count"]
        if prob > maximum_probability:
            best_tag = observation
            maximum_probability = prob
    return best_tag

def is_in_observations( observations, word ):
    return False

def __makedd():
    return defaultdict(
        lambda : {
            "tag_count": 0, 
            "word_count": defaultdict(int) 
            }
        )

if __name__ == '__main__':
    import doctest
    doctest.testmod()
