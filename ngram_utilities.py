from __future__ import division
from nltk import util
import math
from collections import Counter

def unigram_counts( unigram_coll, counts={} ):
    """
    >>> unigram_counts([('first',), ('sentence',), ('second',), ('sentence',), ('third',), ('one',)])
    {('first',): 1, ('sentence',): 2, ('one',): 1, ('third',): 1, ('second',): 1}
    """
    for word in unigram_coll:
        if counts.has_key( word ):
            counts[word] = counts[word]+1
        else:
            counts[word] = 1
    return counts

def ngram_counts( ngram_coll ):
    """
    >>> ngram_counts(bigram_format( ["sentence one is this one", "and this one is the second"] )) #doctest: +NORMALIZE_WHITESPACE
    {('is', 'this'): 1, ('sentence', 'one'): 1, ('one', 'is'): 2, ('is', 'the'): 1, ('and', 'this'): 1, ('this', 'one'): 2, ('the', 'second'): 1}
    """
    counts = {}

    for item in ngram_coll:
        unigram_counts( item, counts )
    return counts

def unigram_format( test_corpus ):
    """
    This function takes a list of sentences and produces tokens
    suitable for unigram formatting

    >>> unigram_format( [ "first sentence", "second sentence", "third one" ] ) #doctest: +NORMALIZE_WHITESPACE
    [('first',), ('sentence',), ('second',), ('sentence',), ('third',), ('one',)]
    """

    wl = []

    for sentence in test_corpus:
        for word in sentence.split():
            wl.append( ( word, ) )

    return wl

def bigram_format( test_corpus ):
    """
    >>> bigram_format(["the dog runs STOP", "the cat walks STOP", "the dog runs STOP"])
    [[('the', 'dog'), ('dog', 'runs'), ('runs', 'STOP')], [('the', 'cat'), ('cat', 'walks'), ('walks', 'STOP')], [('the', 'dog'), ('dog', 'runs'), ('runs', 'STOP')]]
    """

    wl = [ [word for word in sentence.split()] for sentence in test_corpus] 
    return [ util.bigrams( l ) for l in wl ]

def trigram_format( test_corpus ):
    """
    >>> trigram_format(["the dog runs STOP", "the cat walks STOP", "the dog runs STOP"])
    [[('the', 'dog', 'runs'), ('dog', 'runs', 'STOP')], [('the', 'cat', 'walks'), ('cat', 'walks', 'STOP')], [('the', 'dog', 'runs'), ('dog', 'runs', 'STOP')]]
    """
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

def prob_mass( ngrams, word, discount ):
    """
    Given a dict of `ngrams`, a `word` and a `discount` factor, this
    function returns the remaining probability mass
    >>> ngrams = ngram_counts(bigram_format(["the dog eats the cat", "the cat walks the walk", "the cat and the dog catches the mouse"]))
    >>> prob_mass(ngrams, 'the', 0.3)
    1.234    
    """
    pm = 0.0
    word_count = 0
    for ngram_tuple in ngrams.keys():
        if ngram_tuple[0] == word:
            word_count += ngrams.get(ngram_tuple)
    print( ngrams )
    print( "occurrence of {0} in ngram basis: {1}".format( word, word_count ) )

    return pm

def sentence_probability( sentence, propdict ):
    """
    >>> sentence_probability("the dog runs STOP", {"the": {("*","*"):1}, "dog": {("*", "the"):0.5}})
    0.5
    """
    p = 1
    sents = list(sentence.split())
    for word in sents:
        if propdict.get( word ) is not None:
            p = p * float( propdict.get( word ).values()[0] )

    return float( p )

def _get_from_propdict( propdict, key ):
    for tup in propdict:
        if tup[0][0] is key:
            return tup
        else:
            return ( key, ())

if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    # corp = ["the green book STOP",
    #         "the blue book STOP",
    #         "his green house STOP",
    #         "book STOP"]

    # corp2 = ["the dog runs STOP", "the cat walks STOP", "the dog runs STOP"]
    # props = {"the": {("*","*"):1}, "dog": {("*", "the"):0.5}, "cat": {("*", "the"):0.5}, "walks":{("cat", "the"):1}, "STOP":{("cat","walks"):1}, "runs":{("the","dog"):1}, "STOP":{("dog","runs"):1}}

    # print( "unigram counts: {0}".format( unigram_counts( unigram_format( corp2 ) ) ) )
    # print( "bigram counts: {0}".format( ngram_counts( bigram_format( corp2 ) ) ) )
    # print( "trigram counts: {0}".format( ngram_counts( trigram_format( corp2 ) ) ) )

    c1 = [ "the dog STOP" ]
    p1 = { "the": {("*","*"):1}, "dog": {("the","*"):1}, "STOP":{("dog","the"):1}}
    p2 = { "the": {("*","*"):0.5}, "a": {("*","*"):0.5}, "dog": {("the","*"):1},"dog": {("a","*"):1}, "STOP":{("dog","the"):1}}
    print( "perplexity: {0}".format( perplexity( c1, p1 ) ) )
    print( "perplexity: {0}".format( perplexity( c1, p1 ) ) )
