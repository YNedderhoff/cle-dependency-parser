import codecs

from graphs import SparseGraph, DepTree, highest_scoring_heads, cycle, add_sparse_arc
from copy import deepcopy
from token import sentences



def chu_liu_edmonds(graph):
    g = deepcopy(graph)
    g_a = highest_scoring_heads(deepcopy(g))
    c = cycle(g_a, [], sorted(g_a.keys())[0])
    if c is None:
        print "Auweia"
    if not c:
        return g_a
    else:
        g_c = contract(g_a, c)

def contract(g_a, c):
    g_c = deepcopy(g_a)
    for node in c:
        del g_c[node]
    # g_c = add_sparse_arc()
    return g_a