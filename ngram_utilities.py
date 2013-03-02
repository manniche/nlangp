from __future__ import division
from nltk import util
import math
from collections import Counter

def unigram_counts( unigram_coll, counts={} ):
    """
    input of the form:
    
    """
    for word in unigram_coll:
        if counts.has_key( word ):
            counts[word] = counts[word]+1
        else:
            counts[word] = 1
    #print( "unigram: {0}".format( counts ) )
    return counts

def ngram_counts( ngram_coll ):

    counts = {}

    for item in ngram_coll:
        unigram_counts( item, counts )
        #print( "ngrams: {0}".format( counts ) )
    return counts

def unigram_format( test_corpus ):
    wl = []

    for sentence in test_corpus:
        for word in sentence.split():
            wl.append( ( word, ) )

    return wl

def bigram_format( test_corpus ):
    wl = [ [word for word in sentence.split()] for sentence in test_corpus] 
    return [ util.bigrams( l ) for l in wl ]

def trigram_format( test_corpus ):
    wl = [ [word for word in sentence.split()] for sentence in test_corpus] 
    return [ util.trigrams( l ) for l in wl ]

def perplexity( corpus, propdict ):
    """
    >>> corpus = ["the dog runs STOP", "the cat walks STOP", "the dog runs STOP"]
    >>> propdc = {"the": {("*","*"):1}, "dog": {("*", "the"):0.5}, "cat": {("*", "the"):0.5}, "walks":{("cat", "the"):1}, "STOP":{("cat","walks"):1}, "runs":{("the","dog"):1}, "STOP":{("dog","runs"):1}}
    """
    words = []
    [[words.append(l) for l in q.split() ] for q in corpus]
    
    logp = 0.0
    for sentence in corpus:
        logp += math.log( sentence_probability( sentence, propdict ), 2 )

    m = len( words )
    l =  (1/m)*logp
    print( "1/{0}*{1}".format( m, logp) )
    return pow( 2, -l )

def sentence_probability( sentence, propdict ):
    p = 1
    sents = list(sentence.split())
    for word in sents:
        p = p * float( propdict[ word ].values()[0] )

    return float( p )

def _get_from_propdict( propdict, key ):
    for tup in propdict:
        if tup[0][0] is key:
            return tup
        else:
            return ( key, ())

if __name__ == '__main__':
    corp = ["the green book STOP",
            "the blue book STOP",
            "his green house STOP",
            "book STOP"]

    corp2 = ["the dog runs STOP", "the cat walks STOP", "the dog runs STOP"]
    props = {"the": {("*","*"):1}, "dog": {("*", "the"):0.5}, "cat": {("*", "the"):0.5}, "walks":{("cat", "the"):1}, "STOP":{("cat","walks"):1}, "runs":{("the","dog"):1}, "STOP":{("dog","runs"):1}}

    print( "unigram counts: {0}".format( unigram_counts( unigram_format( corp2 ) ) ) )
    print( "bigram counts: {0}".format( ngram_counts( bigram_format( corp2 ) ) ) )
    print( "trigram counts: {0}".format( ngram_counts( trigram_format( corp2 ) ) ) )
    print( "perplexity: {0}".format( perplexity( corp2, props ) ) )
