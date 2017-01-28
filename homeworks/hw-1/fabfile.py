from fabric.api import *
from fabric.contrib.console import confirm
import sys
import os
import subprocess
import platform

env.user = "manniche"
env.hosts = [ "manniche.net" ] 
publish_url = " http://text.manniche.net"

def gen_counts():
    local( "python count_freqs.py gene.train > gene.counts" )

def p1():
    gen_counts()
    local( "python p1.py gene.counts gene.dev > gene.dev.p1.out" )

def p2():
    pass

def p3():
    pass

def eval_p1():
    local( "python eval_gene_tagger.py gene.key gene.dev.p1.out" )

if __name__ == '__main__':

    if len(sys.argv) > 1:
        #
        #  If we got an argument then invoke fabric with it.
        #
        subprocess.call(['fab', '-f', __file__] + sys.argv[1:])
    else:
        #
        #  Otherwise list our targets.
        #
        subprocess.call(['fab', '-f', __file__, '--list'])
