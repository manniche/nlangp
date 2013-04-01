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
