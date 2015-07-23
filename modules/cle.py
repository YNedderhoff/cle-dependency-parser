from graphs import highest_scoring_heads, cycle, reverse_head_graph
from copy import deepcopy

def chu_liu_edmonds(graph):

    g = deepcopy(graph)
    g_a = highest_scoring_heads(deepcopy(g))
    c = cycle(g_a, [], sorted(g_a.keys())[0])

    if c is None:
        print "The cycle function returned 'None'."
    if not c:
        return g_a
    else:
        highest_id = -1
        for head in g:
            if head > highest_id:
                highest_id = head
            for arc in g[head]:
                if arc.dependent > highest_id:
                    highest_id = arc.dependent

        # Call Contract
        g_c, t_c = contract(g, g_a, c, highest_id+1)

        # Recursively call CLE
        y = chu_liu_edmonds(g_c)

        # Resolve cycle

        head_of_cycle = -1
        highest_score = float("-inf")
        for node in reverse_head_graph(y)[t_c]:
            if node.score > highest_score:
                highest_score = node.score
                head_of_cycle = node.head

        # adding arcs from inside cycle to outside cycle, then delete c
        if t_c in y:
            for arc in y[t_c]:
                if arc.dependent not in c:
                    for head in g_a:
                        if head == arc.former_head:
                            for arc2 in g_a[head]:
                                if arc2.dependent == arc.dependent:
                                    if head in y:
                                        y[head].append(arc2)
                                    else:
                                        y[head] = [arc2]
                        
            del y[t_c]

        # adding arcs from outside cycle to inside cycle, adding the arc from outside to C
        new_dependents = []
        for arc in y[head_of_cycle]:
            if arc.dependent == t_c:
                for head in g:
                    if head == head_of_cycle:
                        for arc2 in g[head]:
                            if arc2.dependent == arc.former_dependent:
                                cycle_head = arc.former_dependent
                                new_dependents.append(arc2)

            else:
                new_dependents.append(arc)
        y[head_of_cycle] = new_dependents

        # adding arcs from inside cycle to inside cycle except the one pointing to cycle_head
        for node in c:
            for head in g_a:
                if head == node:
                    for arc in g_a[head]:
                        if arc.dependent in c:
                            if not arc.dependent == cycle_head:
                                if head in y:
                                    y[head].append(arc)
                                else:
                                    y[head] = [arc]
        return y

def contract(g, g_a, c, t_c):

    g_c = deepcopy(g_a)

    # delete all nodes that are in c out of g_c
    for node in c:
        if node in g_c:
            del g_c[node]

    # remove all dependents out of c of every head they are in, keep dependents that are not in c
    for head in g_c:
        new_dependents = []
        for arc in g_c[head]:
            if arc.dependent not in c:
                new_dependents.append(arc)
        g_c[head] = new_dependents

    # if there are heads with no dependents, remove them completely
    tmp_g_c = deepcopy(g_c)
    for head in g_c:
        if not g_c[head]:
            del tmp_g_c[head]
    g_c = tmp_g_c

    # Arcs leaving C
    # (add all dependents out of g_a that had a head out of C)
    for head in c:
        for arc in g_a[head]:
            if arc.dependent not in c:
                if t_c in g_c:
                    if g_c[t_c]:
                        found_dependent = False
                        new_dependents = []
                        for arc2 in g_c[t_c]:
                            if arc2.dependent == arc.dependent:
                                found_dependent = True
                                if arc.score > arc2.score:
                                    new_arc = deepcopy(arc)
                                    new_arc.head = t_c
                                    new_arc.former_head = head
                                    new_arc.feat_vec = []

                                    new_dependents.append(new_arc)
                                else:
                                    new_dependents.append(arc2)
                            else:
                                new_dependents.append(arc2)

                        if not found_dependent:

                            new_arc = deepcopy(arc)
                            new_arc.head = t_c
                            new_arc.former_head = head
                            new_arc.feat_vec = []

                            new_dependents.append(new_arc)

                        g_c[t_c] = new_dependents

                    else:
                        new_arc = deepcopy(arc)
                        new_arc.head = t_c
                        new_arc.former_head = head
                        new_arc.feat_vec = []

                        g_c[t_c] = [new_arc]
                else:
                    new_arc = deepcopy(arc)
                    new_arc.head = t_c
                    new_arc.former_head = head
                    new_arc.feat_vec = []

                    g_c[t_c] = [new_arc]

    # compute s(C), the score of the cycle
    s_c = 0.0
    for head in c:
        for arc in g_a[head]:
            if arc.dependent in c:
                s_c += arc.score

    # Arcs entering C
    for head in g:
        if head not in c:
            for arc in g[head]:
                # check all arcs the go into c, save the highest
                if arc.dependent in c:

                    # compute s(th, td), the score of the arc from outside the cycle to inside the cycle
                    s_th_td = arc.score

                    # compute s(h(td), td), the score of the head of the arc INSIDE the cycle
                    s_htd_td = 0.0

                    for head2 in c:
                        for arc2 in g_a[head2]:
                            if arc2.dependent == arc.dependent:
                                s_htd_td = arc2.score

                    s = s_th_td + s_c - s_htd_td

                    if head in g_c:
                        if g_c[head]:
                            found_dependent = False
                            new_dependents = []
                            for arc2 in g_c[head]:
                                if arc2.dependent == t_c:
                                    found_dependent = True
                                    if s > arc2.score:
                                        new_arc = deepcopy(arc)
                                        new_arc.score = s
                                        new_arc.dependent = t_c
                                        new_arc.former_dependent = arc.dependent
                                        new_dependents.append(new_arc)
                                    else:
                                        new_dependents.append(arc2)
                                else:
                                    new_dependents.append(arc2)

                            if not found_dependent:
                                new_arc = deepcopy(arc)
                                new_arc.score = s
                                new_arc.dependent = t_c
                                new_arc.former_dependent = arc.dependent
                                new_dependents.append(new_arc)

                            g_c[head] = new_dependents

                        else:
                            new_arc = deepcopy(arc)
                            new_arc.score = s
                            new_arc.dependent = t_c
                            new_arc.former_dependent = arc.dependent
                            g_c[head].append(new_arc)
                    else:
                        new_arc = deepcopy(arc)
                        new_arc.score = s
                        new_arc.dependent = t_c
                        new_arc.former_dependent = arc.dependent
                        g_c[head] = [new_arc]
                else:
                    # find all arcs that are outside of c, add them if not there
                    if head in g_c:
                        arc_found = False
                        for arc2 in g_c[head]:
                            if arc2.dependent == arc.dependent:
                                arc_found = True
                        if not arc_found:
                            if g_c[head]:
                                g_c[head].append(arc)
                            else:
                                g_c[head] = [arc]

    return g_c, t_c


