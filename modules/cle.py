from copy import deepcopy

from graph import graph_sanity_check, give_cycle, highest_incoming_heads, remove_cycle

def chu_liu_edmonds(in_g):  # incomplete

    g = deepcopy(in_g)
    if not graph_sanity_check(g): print "g"

    g_a = highest_incoming_heads(g)
    if not graph_sanity_check(g_a): print "g_a"

    if not give_cycle(g_a, "0_Root", [], []):
        return g_a
    else:
        print "Cycle found."
        c = give_cycle(g_a, "0_Root", [], [])
        g_c = contract(g_a, c)
        if not graph_sanity_check(g_c): print "Contracted (in cle)"

        y = chu_liu_edmonds(g_c)
        if not graph_sanity_check(y): print "y in cle"

        # find arc to remove
        to_remove_head = ""
        to_remove_dependent = ""
        for d in c:
            for head in g_a:
                for dependent in g_a[head]:
                    if dependent == d:
                        to_remove_head = head
                        to_remove_dependent = d
        # add all arcs of c except the to remove arc to g_c
        for n_id, node in enumerate(c):
            if not node == to_remove_head:
                if c[n_id + 1] == to_remove_dependent:
                    print "This is impossible (cle)"
                else:
                    if node in g_c:
                        if n_id == len(c) - 1:
                            g_c[node][c[0]] = [0.0, {}]
                        else:
                            g_c[node][c[n_id + 1]] = [0.0, {}]
                    else:
                        if n_id == len(c) - 1:
                            g_c[node] = {c[n_id + 1], [0.0, {}]}
                        else:
                            g_c[node] = {c[n_id + 1], [0.0, {}]}

        # return g_a
        return g_c


def contract(g_a_in, c):  # incomplete

    g_a = deepcopy(g_a_in)
    # remove Cycle
    g_c = remove_cycle(g_a, c)
    if not graph_sanity_check(g_c): print "Contracted (in contract function)"
    # check if exactly to arcs have been removed
    counter = 0
    for key in g_a:
        if len(g_c[key]) != len(g_a[key]):
            if len(g_c[key]) == len(g_a[key]) - 1:
                counter += 1
    if counter != len(c):
        print "Contract function didn't remove exactly the needed amount of arcs."

    # add tc to represent C
    t_c = ""
    for n_id, node in enumerate(c):
        if n_id == len(c) - 1:
            t_c += node
        else:
            t_c += node + "-"
    print t_c
    g_c[t_c] = {}
    # g_c[c[0] + "-" + c[1]] = {}

    # arcs leaving C
    # for every dependent d: if a node out of C is head of d: add new arc <c, d> with score !?
    new_arcs = {}

    for head in g_a:
        if head in c:
            for dependent in g_a[head]:
                if dependent not in c:
                    if dependent in new_arcs:
                        if new_arcs[dependent] < g_a[head][dependent][0]:
                            new_arcs[dependent] = g_a[head][dependent][0]
                    else:
                        new_arcs[dependent] = g_a[head][dependent][0]
    for dependent in new_arcs:
        g_c[t_c][dependent] = [new_arcs[dependent], {}]

    score_c = 0  # cycle score s(c)
    for n_id, node in enumerate(c):
        if n_id == len(c) - 1:
            score_c += g_a[node][c[0]][0]
        else:
            score_c += g_a[node][c[n_id + 1]][0]
    print "Score c:"
    print score_c

    # arcs entering C
    new_arcs = {}
    for head in g_a:
        if head not in c:
            for dependent in g_a[head]:
                if dependent in c:
                    score_h_d = g_a[head][dependent][0]  # score of the arc entering c and the dependent
                    score_hd_d = 0  # score of the head of td in c and td
                    for head_2 in g_a:
                        if head_2 in c:
                            if dependent in g_a[head_2]:
                                score_hd_d = g_a[head_2][dependent][0]
                    if head in new_arcs:
                        if new_arcs[head] < score_h_d + score_c - score_hd_d:
                            new_arcs[head] = score_h_d + score_c - score_hd_d
                    else:
                        new_arcs[head] = score_h_d + score_c - score_hd_d
    for head in new_arcs:
        g_c[head][t_c] = [new_arcs[head], {}]

    return g_c
