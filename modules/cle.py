from graphs import highest_scoring_heads, cycle, reverse_head_graph
from copy import deepcopy

def chu_liu_edmonds(graph):
    # print "cle call"
    g = deepcopy(graph)
    g_a = highest_scoring_heads(deepcopy(g))
    """
    print "highest incoming"
    for head in g_a:
        for arc in g_a[head]:
            print str(head) + " --> " + str(arc.dependent) + ", " + str(arc.score)
    print "--"
    """
    c = cycle(g_a, [], sorted(g_a.keys())[0])
    if c is None:
        print "The cycle function returned 'None'."
    if not c:
        #print "no cycle"
        return g_a
    else:
        # print "cycle befor contract " + str(c)
        highest_id = -1
        for head in g:
            if head > highest_id:
                highest_id = head
            for arc in g[head]:
                if arc.dependent > highest_id:
                    highest_id = arc.dependent
        """
        print "lol0g"
        for head in g:
            for arc in g[head]:
                print str(head) + " --> " + str(arc.dependent) + ", " + str(arc.score)
        print "_"
        """
        g_c, t_c = contract(g, g_a, c, highest_id+1)

        """
        print "t_c after g_c " + str(t_c)
        print "after g_c"
        for head in g_c:
            for arc in g_c[head]:
                print str(head) + " --> " + str(arc.dependent) + ", " + str(arc.score)
        print "--"
        """
        t_c_found = False
        for head in g_c:
            for arc in g_c[head]:
                if arc.dependent == t_c:
                    t_c_found = True
        """
        if not t_c_found:
            print "t_c has no head (in g_c)"
        """
        y = chu_liu_edmonds(g_c)

        # print "t_c after y " + str(t_c)

        t_c_found = False
        for head in y:
            for arc in y[head]:
                if arc.dependent == t_c:
                    t_c_found = True
        """
        if not t_c_found:
            print "t_c has no head (in y)"
        """

        # Resolve cycle
        # print "resolving"
        head_of_cycle = -1
        highest_score = float("-inf")
        for node in reverse_head_graph(y)[t_c]:
            if node.score > highest_score:
                highest_score = node.score
                head_of_cycle = node.head

        if head_of_cycle not in y:
            print "Head of cycle missing"
        """
        if head_of_cycle in to_keep_arcs:
            print "Head in to keep arcs"
        """
        """

        print "g_a, before adding arcs from inside to outside"
        for head in g_a:
            for arc in g_a[head]:
                print str(head) + " --> " + str(arc.dependent) + ", " + str(arc.score)
        print "--"

        """
        # adding arcs from inside cycle to outside cycle, then delete c
        if t_c in y:
            for arc in y[t_c]:
                if arc.dependent not in c:
                    former_head_found = False
                    for head in g_a:
                        if head == arc.former_head:
                            for arc2 in g_a[head]:
                                if arc2.dependent == arc.dependent:
                                    #print "former_head " + str(arc.former_head)
                                    #print "head " + str(arc.head)
                                    #print "dependent " + str(arc.dependent)
                                    former_head_found = True
                                    if head in y:
                                        y[head].append(arc2)
                                    else:
                                        y[head] = [arc2]
                    #if not former_head_found:
                        #print "former_head not found"
                        #print "former_head " + str(arc.former_head)
                        #print "head " + str(arc.head)
                        #print "dependent " + str(arc.dependent)
                        
            del y[t_c]
        """
        print "after cle and deleting c as a head"
        for head in y:
            for arc in y[head]:
                print str(head) + " --> " + str(arc.dependent) + ", " + str(arc.score)
        print "--"
        """
        counter = 0
        #print g.keys()
        t_c_is_dependent = False
        #print "cycle " + str(c)
        #print "head of cycle" + str(head_of_cycle)
        # adding arcs from outside cycle to inside cycle, adding the arc from outside to C
        new_dependents = []
        for arc in y[head_of_cycle]:
            if arc.dependent == t_c:
                t_c_is_dependent = True
                former_dependent_found = False
                for head in g:
                    if head == head_of_cycle:
                        for arc2 in g[head]:
                            if arc2.dependent == arc.former_dependent:
                                counter+=1
                                former_dependent_found = True
                                #print "former_dependent " + str(arc.former_dependent)
                                #print "head " + str(arc.head)
                                #print "dependent " + str(arc.dependent)
                                cycle_head = arc.former_dependent
                                new_dependents.append(arc2)

                #if not former_dependent_found:
                    #print "former dependent not found"
                    #print "former_dependent " + str(arc.former_dependent)
                    #print "head " + str(arc.head)
                    #print "dependent " + str(arc.dependent)

            else:
                new_dependents.append(arc)
        y[head_of_cycle] = new_dependents
        """
        print "after deleting heads and adding heads inside cycle"
        for head in y:
            for arc in y[head]:
                print str(head) + " --> " + str(arc.dependent) + ", " + str(arc.score)
        print "--"
        """
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
        if not t_c_is_dependent:
            print "t_c is not dependent of head_of_cycle"
        if not former_dependent_found:
            print "no former dependent"
        """
        print "after adding arc from inside cycle to inside cycle"
        for head in y:
            for arc in y[head]:
                print str(head) + " --> " + str(arc.dependent) + ", " + str(arc.score)
        print "--"
        """
        """
        print to_keep_arcs

        for node in to_keep_arcs:
            for arc in g_a[node]:
                print str(node) + " --> " + str(arc.dependent) + ", " + str(arc.score)
                if arc.dependent != to_keep_arcs[0]:
                    #if arc.dependent not in y:
                    not_in_dependents = True
                    for head in y:
                        for arc2 in y[head]:
                            if arc2.dependent == arc.dependent:
                                not_in_dependents = False
                    if not_in_dependents:

                        if node in y:
                            y[node].append(arc)
                        else:
                            y[node] = [arc]
                    else:
                        print "ahja"
                        print "Head of cycle: "+ str(head_of_cycle)
                        print "tc " + str(t_c)
                        print "former" + str(former)
                        print "to_keep_arcs[0]" + str(to_keep_arcs[0])
                        print str(node) + " --> " + str(arc.dependent)
                        for head in y:
                            for arc2 in y[head]:
                                if arc2.dependent == arc.dependent:
                                    print str(head) + " --> " + str(arc2.dependent)
                        print "Just saying"
                        arcs = {}
                        problem = False
                        for head in g_a:
                            if not problem:
                                local_dependents = []
                                for arc2 in g_a[head]:
                                    if arc2.dependent in local_dependents:
                                        print "A dependent is more than once in a head."
                                        problem = True
                                    else:
                                        local_dependents.append(arc2.dependent)
                                    if arc2.dependent in arcs:
                                        print "A dependent has more than one head."
                                        problem = True
                                    else:
                                        arcs[arc2.dependent] = arc
                        if problem:
                            print "_________________________________________________________________________________________"
                            for head in g_a:
                                for arc2 in g_a[head]:
                                    print str(head) + " --> " + str(arc2.dependent) + ", " + str(arc2.score)
        #print "Resolving done"
        """
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

    # add all dependents of g that had a head out of c
    """
    print "after cle and deleting c as a head"
    print "g:"
    for head in g:
        for arc in g[head]:
            print str(head) + " --> " + str(arc.dependent) + ", " + str(arc.score)
    print "--"
    print "head out of cycle call"
    """
    for head in c:
        for arc in g_a[head]:
            if arc.dependent not in c:
                #if head == 27 and arc.dependent == 36:
                #    print int(head)
                #    print int(arc.dependent)
                #    print "_"
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
                                    #del g_c[t_c][g_c[t_c].index(arc2)]
                                    #g_c[t_c].append(new_arc)
                            else:
                                new_dependents.append(arc2)

                        if not found_dependent:

                            new_arc = deepcopy(arc)
                            new_arc.head = t_c
                            new_arc.former_head = head
                            new_arc.feat_vec = []

                            new_dependents.append(new_arc)
                        """
                        if head == 27 and arc.dependent == 36:
                            print "dependents"
                            for arc2 in new_dependents:
                                print arc2.head
                                print arc2.former_head
                                print arc2.dependent
                            print "."
                        """
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
    """
    for head in g_c:
        for arc in g_c[head]:
            print str(head) + " --> " + str(arc.dependent) + ", " + str(arc.score)
    print "--"
    print "head out of cycle end"
    """
    # compute s(C), the score of the cycle
    s_c = 0.0

    for head in c:  #c[:-1]
        for arc in g_a[head]:
            if arc.dependent in c:
                s_c += arc.score
    """
    print "cycle " + str(c)
    print "t_c " + str(t_c)

    print "g1"
    for head in g:
        for arc in g[head]:
            print str(head) + " --> " + str(arc.dependent) + ", " + str(arc.score)
    print "--"
    print "g_c"
    for head in g_c:
        for arc in g_c[head]:
            print str(head) + " --> " + str(arc.dependent) + ", " + str(arc.score)
    print "--"
    """
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
                                # print "Is this even possible?"
                        if not arc_found:
                            if g_c[head]:
                                g_c[head].append(arc)
                            else:
                                g_c[head] = [arc]
    """
    print "g_c"
    for head in g_c:
        for arc in g_c[head]:
            print str(head) + " --> " + str(arc.dependent) + ", " + str(arc.score)
    print "--"

    to_keep_arcs = []

    to_keep_found = False
    start_found = False
    for node in c:
        if start_found:
            to_keep_arcs.append(node)
            if node == break_point[0]:
                to_keep_found = True
        elif node == break_point[1]:
            to_keep_arcs.append(node)
            start_found = True
    if not to_keep_found:
        end_found = False
        for node in c:
            if node == break_point[0]:
                to_keep_arcs.append(node)
                end_found = True
            elif not end_found:
                to_keep_arcs.append(node)
    """
    return g_c, t_c

