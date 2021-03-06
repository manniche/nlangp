#!/usr/bin/env python

from __future__ import division 
from collections import defaultdict
import sys

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
    >>> find_tag_for_word( obs, 'Hospital' )
    'O'
    >>> find_tag_for_word( obs, 'UEV1A' )
    'I-GENE'
    >>> find_tag_for_word( obs, 'does_not_exist')
    'O'
    """

    maximum_probability = 0.0
    best_tag = None

    for observation in observations:
        if not is_in_observations( word, observations ):
            word = "_RARE_"
        prob = observations[observation]["word_count"][word] / observations[observation]["tag_count"]
        if prob > maximum_probability:
            best_tag = observation
            maximum_probability = prob

        if best_tag is None or word is "_RARE_":
            #sys.stderr.write( word+"\n" )
            best_tag = None

    return best_tag

def is_in_observations( word, observations ):
    for observation in observations:
        if word in observations[observation]["word_count"]:
            return True
    return False


def __makedd():
    return defaultdict(
        lambda : {
            "tag_count": 0, 
            "word_count": defaultdict(int) 
            }
        )

if __name__ == '__main__':
    # import doctest
    # doctest.testmod()

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument( "gene_counts" )
    parser.add_argument( "gene_dev" )
    args = parser.parse_args()

    l = [line.strip().split( " " ) for line in open(args.gene_counts, "r")]

    observations = count_wordtags( l )

    with open( args.gene_dev, "r" ) as infile:
        for line in infile:
            word = line.strip()
            if not word:
                print
                continue
            tag = find_tag_for_word( observations, word )
            print word, tag
