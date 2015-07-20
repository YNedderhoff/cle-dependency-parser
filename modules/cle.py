import codecs

from graphs import SparseGraph, DepTree, highest_scoring_heads, cycle, add_sparse_arc, reverse_head_graph, SparseOwnGraph, SparseOwnArc
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
        print c
        g_c = contract(g, g_a, c, sorted(g, reverse=True)[0]+1)
        y = chu_liu_edmonds(g_c)

        # to_do: Resolve cycle

        return y

def contract(g, g_a, c, l):
    g_c = deepcopy(g_a)
    print g_c.keys()
    for node in c:
        del g_c[node]

    # add tc to represent C

    g_c[l] = []

    # add all dependents of g_a that had a head out of c

    for head in c:
        for arc in g[head]:
            if arc.dependent not in c:
                new_arc = deepcopy(arc)
                s = new_arc.score
                for head2 in c:
                    if head2 != head:
                        for arc2 in g[head2]:
                            if arc2.dependent == arc.dependent:
                                if arc2.score > s:
                                    s = arc2.score
                new_arc.score = s
                new_arc.head = l
                new_arc.feat_vec = []

                arc_is_there = False

                for arc2 in g_c[l]:
                    if arc2.dependent == new_arc.dependent:
                        if arc2.score == new_arc.score:
                            arc_is_there = True
                        else:
                            print "Scoring problem."

                if not arc_is_there: g_c[l].append(new_arc)

    for head in g:
        if head not in c:
            for arc in g[head]:
                if arc.dependent in c:
                    new_arc = deepcopy(arc)

                    # compute s(th, td)
                    s_th_td = 0.0

                    for arc2 in g[head]:
                        if arc2.dependent in c:
                            if arc2.score > s_th_td:
                                s_th_td = arc2.score

                    # compute s(C)

                    s_c = 0.0

                    for head2 in c:
                        for arc2 in g[head2]:
                            if arc2.dependent in c:
                                s_c += arc2.score

                    # compute s(h(td), td)

                    s_htd_td = 0.0

                    for head2 in c:
                        for arc2 in g[head2]:
                            if arc2.dependent in c:
                                if arc2.score > s_htd_td:
                                    s_htd_td = arc2.score

                    s = s_th_td + s_c - s_htd_td

                    new_arc.score = s
                    new_arc.dependent = l

                    arc_is_there = False

                    if head in g_c:
                        for arc2 in g_c[head]:
                            if arc2.dependent == new_arc.dependent:
                                if arc2.score == new_arc.score:
                                    arc_is_there = True
                                else:
                                    print head
                                    print new_arc.dependent
                                    print arc2.dependent
                                    print "Scoring problem. (Head outside of tc)"

                    if not arc_is_there:
                        print new_arc.score
                        if head in g_c:
                            g_c[head].append(new_arc)
                        else:
                            g_c[head] = [new_arc]

    for head in g_c:
        print head
        for arc in g_c[head]:
            print arc.dependent
        print "-"

    return g_c
