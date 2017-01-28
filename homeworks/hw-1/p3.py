#! /usr/bin/python

from __future__ import division
import sys
from collections import defaultdict
import pprint

def get_mle(counts_file):
    """
    """
    obs_counts = defaultdict(
        lambda : {
            "total_count": 0, 
            "word_counts": defaultdict(int) 
        }
    )
    bi_c = {} 
    q = {}
    for line in counts_file:
        line = line.strip()
        if not line: 
            continue

        # Extract information from line.
        # Each line has the format
        # count WORDTAG tag word
        fields = line.split(" ")
        if fields[1] == "WORDTAG":
            (count, count_type, tag, word) = fields
            count = int(count)
            obs_counts[tag]["total_count"] += count
            obs_counts[tag]["word_counts"][word] += count
        elif fields[1] == "2-GRAM":
            (count, count_type, u, v) = fields
            bi_c[(u, v)] = int(count)
        elif fields[1] == "3-GRAM":
            (count, count_type, u, v, w) = fields
            q[(u, v, w)] = int(count) / bi_c[(u, v)]

    e = {}
    for tag in obs_counts:
        e[tag] = {}
        for (word, count) in obs_counts[tag]["word_counts"].iteritems():
            e[tag][word] = count / obs_counts[tag]["total_count"]

    return (q, e)

class TrigramHMM(object):
    def __init__(self, q, e):
        self.q = q
        self.e = e
        self.s = e.keys()

    def states(self, i):
        if i <= 0:
            return ("*")
        else:
            return self.s

    def is_word_in_vocab(self, word):
        for tag in self.e:
            if word in self.e[tag]:
                return True
        return False

    def get_rare_class(self, word):
        if all(c.isupper() for c in word):
            rare_class = "_RARE_ALLCAPS_"
        elif any(c.isdigit() for c in word):
            rare_class = "_RARE_NUM_"
        elif word[-1].isupper():
            rare_class = "_RARE_LASTCAP_"
        else:
            rare_class = "_RARE_"
        return rare_class

    def find_tags(self, words):
        y = [None] * len(words)
        p = {}
        bp = {}
        p[(0, "*", "*")] = 1
        n = len(words)
        for i in xrange(1, n + 1):
            for u in self.states(i - 1):
                for v in self.states(i):
                    max_p = -1
                    max_w = None
                    for w in self.states(i - 2):
                        word = words[i - 1]
                        if word not in e[v]:
                            if self.is_word_in_vocab(word):
                                e_p = 0
                            else:
                                rare_class = self.get_rare_class(word)
                                e_p = e[v][rare_class]
                        else:
                            e_p = e[v][word]
                        p_w = p[(i - 1, w, u)] * q[(w, u, v)] * e_p
                        if p_w > max_p:
                            max_p = p_w
                            max_w = w

                    p[(i, u, v)] = max_p
                    bp[(i, u, v)] = max_w

        max = -1
        for u in self.states(n - 1):
            for v in self.states(n):
                p_y = p[(n, u, v)] * q[(u, v, "STOP")]
                if p_y > max:
                    max = p_y
                    y[n - 2] = u
                    y[n - 1] = v
        
        for i in xrange(n - 3, -1, -1):
            y[i] = bp[(i + 3, y[i + 1], y[i + 2])]

        return y

def usage():
    print """
    python part2.py counts_file test_file > output_file
    """

if __name__ == "__main__":

    if len(sys.argv) != 3: 
        sys.exit(2)

    with open(sys.argv[1], "r") as counts_file:
        (q, e) = get_mle(counts_file)

    hmm = TrigramHMM(q, e)
    with open(sys.argv[2], "r") as test_file:
        words = []
        for line in test_file:
            word = line.strip()
            if word:
                words.append(word)
            else:
                tags = hmm.find_tags(words)
                for i in xrange(len(tags)):
                    print words[i], tags[i]
                print
                words = []
