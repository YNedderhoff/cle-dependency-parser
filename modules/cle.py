from graphs import highest_scoring_heads, cycle, reverse_head_graph, Arc


def chu_liu_edmonds(graph):

    g = graph

    # for every node, take the highest incoming head
    g_a = highest_scoring_heads(g)

    # check g_a for cycles
    c = cycle(g_a)

    # if g_a has no cycles, return g_a
    if not c:
        return g_a
    # if g_a has cycles contract cycle, recursively call chu_liu_edmonds(), resolve cycle
    else:

        # find the highest node id (the new node's id is going to be highest_id + 1)
        highest_id = -1
        for head in g:
            if head > highest_id:
                highest_id = head
            for arc in g[head]:
                if arc.dependent > highest_id:
                    highest_id = arc.dependent

        # Call Contract
        g_c, t_c = contract(g, g_a, c, highest_id + 1)

        # Recursively call CLE
        y = chu_liu_edmonds(g_c)

        # Resolve cycle

        # find the highest scoring head of the cycle
        head_of_cycle = -1
        highest_score = float("-inf")
        for node in reverse_head_graph(y)[t_c]:
            if node.score > highest_score:
                highest_score = node.score
                head_of_cycle = node.head

        # add arcs from inside cycle to outside cycle, then delete t_c
        if t_c in y:
            for arc in (arc for arc in y[t_c] if arc.dependent not in c):
                # dependents of t_c which are not in c
                for head in (head for head in g if head == arc.former_head):
                    # heads in g_a which are former head of arc
                    for arc2 in (arc2 for arc2 in g[head] if arc2.dependent == arc.dependent):
                        #  dependent of head which has the same id as arc
                        try:
                            y[head].append(arc2)
                        except KeyError:
                            y[head] = [arc2]

            del y[t_c]

        # add the arc from the head of the cycle to the start node inside the cycle
        new_dependents = []
        for arc in y[head_of_cycle]:
            if arc.dependent == t_c:
                # arc is t_c in y and dependent of head_of_cycle
                for head in (head for head in g if head == head_of_cycle):
                    # head in g which is head_of_cycle
                    for arc2 in (arc2 for arc2 in g[head] if arc2.dependent == arc.former_dependent):
                        # arc in g[head] which has the same id as the former_dependent of t_c
                        cycle_start_node = arc.former_dependent
                        new_dependents.append(arc2)
            else:
                new_dependents.append(arc)
        y[head_of_cycle] = new_dependents

        # add arcs from inside cycle to inside cycle except the one pointing to cycle_start_node
        for head in (head for head in g_a if head in c):
            # every head in g_a that is in c
            for arc in (arc for arc in g_a[head] if arc.dependent in c and not arc.dependent == cycle_start_node):
                # every dependent of head in g_a if it is in c but not cycle_start_node
                try:
                    y[head].append(arc)
                except KeyError:
                    y[head] = [arc]

        return y


def contract(g, g_a, c, t_c):
    g_c = {}

    # add all arcs to g_c that have nothing to do with C
    for head in (head for head in g if head not in c):
        new_dependents = []
        for arc in (arc for arc in g[head] if arc.dependent not in c):
            new_dependents.append(arc)
        if new_dependents:
            g_c[head] = new_dependents

    # Arcs leaving C
    # (add all dependents out of g that had a head out of C)
    for head in (head for head in g if head in c):
        for arc in (arc for arc in g[head] if arc.dependent not in c):
            try:
                found_dependent = False
                new_dependents = []
                for arc2 in g_c[t_c]:
                    if arc2.dependent == arc.dependent:
                        found_dependent = True
                        if arc.score > arc2.score:
                            new_arc = Arc("sparse", t_c, arc.dependent)
                            new_arc.former_head = head
                            new_arc.score = arc.score
                            new_dependents.append(new_arc)
                        else:
                            new_dependents.append(arc2)
                    else:
                        new_dependents.append(arc2)

                if not found_dependent:
                    new_arc = Arc("sparse", t_c, arc.dependent)
                    new_arc.former_head = head
                    new_arc.score = arc.score
                    new_dependents.append(new_arc)

                g_c[t_c] = new_dependents

            except KeyError:
                new_arc = Arc("sparse", t_c, arc.dependent)
                new_arc.former_head = head
                new_arc.score = arc.score
                g_c[t_c] = [new_arc]

    # compute s(C), the score of the cycle
    s_c = 0.0
    for head in c:
        for arc in (arc for arc in g_a[head] if arc.dependent in c):
            s_c += arc.score

    # Arcs entering C
    for head in (head for head in g if head not in c):
        for arc in (arc for arc in g[head] if arc.dependent in c):
            # check all arcs the go into c, save the highest

            # compute s(th, td), the score of the arc from outside the cycle to inside the cycle
            s_th_td = arc.score

            # compute s(h(td), td), the score of the head of the arc INSIDE the cycle
            s_htd_td = 0.0

            for head2 in c:
                for arc2 in g_a[head2]:
                    if arc2.dependent == arc.dependent:
                        s_htd_td = arc2.score

            s = s_th_td + s_c - s_htd_td

            try:
                found_dependent = False
                new_dependents = []
                for arc2 in g_c[head]:
                    if arc2.dependent == t_c:
                        found_dependent = True
                        if s > arc2.score:
                            new_arc = Arc("sparse", arc.head, t_c)
                            new_arc.score = s
                            new_arc.former_dependent = arc.dependent
                            new_dependents.append(new_arc)
                        else:
                            new_dependents.append(arc2)
                    else:
                        new_dependents.append(arc2)

                if not found_dependent:
                    new_arc = Arc("sparse", arc.head, t_c)
                    new_arc.score = s
                    new_arc.former_dependent = arc.dependent
                    new_dependents.append(new_arc)

                g_c[head] = new_dependents

            except KeyError:
                new_arc = Arc("sparse", arc.head, t_c)
                new_arc.score = s
                new_arc.former_dependent = arc.dependent
                g_c[head] = [new_arc]
    return g_c, t_c
