from copy import deepcopy


class SparseArc:  # sparse representation of an arc
    def __init__(self, head, dependent, s=0.0):
        self.head = int(head)
        self.dependent = int(dependent)
        self.score = s
        self.feat_vec = []

        self.former_head = None
        self.former_dependent = None


class FullArc:  # full representation of an arc
    def __init__(self, head, dependent, head_form, dependent_form, head_lemma, dependent_lemma, head_pos,
                 dependent_pos, dependent_rel, s=0.0):
        self.head = int(head)
        self.dependent = int(dependent)
        self.score = s
        self.feat_vec = []

        self.head_form = head_form
        self.dependent_form = dependent_form

        self.head_lemma = head_lemma
        self.dependent_lemma = dependent_lemma

        self.head_pos = head_pos
        self.dependent_pos = dependent_pos

        self.rel = dependent_rel

        self.former_head = None
        self.former_dependent = None


class ManualSparseGraph:  # heads has the same structure as in the other graph classes, but for addition of arcs
    def __init__(self):
        self.heads = {}

    def add_arc(self, head, arc):
        if head in self.heads:
            self.heads[head].append(arc)
        else:
            self.heads[head] = [arc]


class SparseGraph:  # sparse representation of a graph (keys: heads, values: SparseArc objects)
    def __init__(self, tokens):
        self.heads = {0: []}

        for token in tokens:
            if int(token.head) == 0:
                new_arc = SparseArc(0, token.id)
                self.heads[0].append(new_arc)
        for token1 in tokens:
            dependents = []
            for token2 in tokens:
                if token2.head == token1.id:
                    new_arc = SparseArc(token1.id, token2.id)
                    dependents.append(new_arc)
            if dependents:
                self.heads[int(token1.id)] = dependents


class FullGraph:  # full representation of a graph (keys: heads, values: FullArc objects)
    def __init__(self, tokens):
        self.heads = {0: []}

        for token in tokens:
            if int(token.head) == 0:
                new_arc = FullArc(0, token.id, "__ROOT__", token.form, "__NULL__", token.lemma, "__NULL__", \
                                  token.pos, token.rel)
                self.heads[0].append(new_arc)
        for token1 in tokens:
            dependents = []
            for token2 in tokens:
                if token2.head == token1.id:
                    new_arc = FullArc(token1.id, token2.id, token1.form, token2.form, token1.lemma, token2.lemma, \
                                      token1.pos, token2.pos, token2.rel)
                    dependents.append(new_arc)
            if dependents:
                self.heads[int(token1.id)] = dependents


class CompleteFullGraph:  # complete, full representation of a graph (keys: heads, values: FullArc objects)
    def __init__(self, tokens):
        self.heads = {0: []}

        for token in tokens:
            new_arc = FullArc(0, token.id, "__ROOT__", token.form, "__NULL__", token.lemma, "__NULL__", \
                              token.pos, token.rel)
            self.heads[0].append(new_arc)
        for token1 in tokens:
            dependents = []
            for token2 in tokens:
                new_arc = FullArc(token1.id, token2.id, token1.form, token2.form, token1.lemma, token2.lemma, \
                                  token1.pos, token2.pos, token2.rel)
                dependents.append(new_arc)
            if dependents:
                self.heads[int(token1.id)] = dependents


def reverse_head_graph(graph):  # reverses a normal graph to a graph where the dependents are the keys
    new_graph = {}
    for h_id in graph:
        for arc in graph[h_id]:
            if arc.dependent in new_graph:
                new_graph[arc.dependent].append(arc)
            else:
                new_graph[arc.dependent] = [arc]
    return new_graph


def reverse_dep_graph(graph):  # opposite of reverse_head_graph
    new_graph = {}
    for d_id in graph:
        for arc in graph[d_id]:
            if arc.head in new_graph:
                new_graph[arc.head].append(arc)
            else:
                new_graph[arc.head] = [arc]
    return new_graph


def highest_scoring_heads(graph):  # returns a graph where every dependent only has it's highest scoring head
    rev_graph = reverse_head_graph(graph)
    highest = {}

    for dependent in rev_graph:
        for arc in rev_graph[dependent]:
            if dependent in highest:
                if arc.score > highest[dependent][0].score:
                    highest[dependent] = [arc]
                if arc.score == highest[dependent][0].score:
                    if arc.dependent < highest[dependent][0].dependent:
                        highest[dependent] = [arc]
            else:
                highest[dependent] = [arc]
    return reverse_dep_graph(highest)


def cycle_per_head(graph, v, n):
    c = []
    v.append(n)
    for arc in graph[n]:
        if arc.dependent == v[0]:
            # v.append(arc.dependent)
            c = v
            return c
        elif arc.dependent not in v:
            if arc.dependent in graph:
                c = cycle_per_head(graph, deepcopy(v), arc.dependent)
                if c:
                    return c
    return c


def cycle(graph):  # returns a list containing the nodes which are in a cycle (if existing), else []

    # n is "next to visit"

    cycles = []
    for head in sorted(graph.keys()):
        visited = []
        cy = cycle_per_head(graph, visited, head)
        if cy:
            cycles.append(cy)
    if cycles:
        return cycles[0]
    else:
        return []


def write_graph_to_file(graph, out_file, mode="normal"):  # write a graph to file in conll06 format
    if mode == "normal":

        rev = reverse_head_graph(graph)
        out = open(out_file, "a")
        for dependent in sorted(rev.keys()):
            # without rel
            print >> out, str(rev[dependent][0].dependent) + "\t" + rev[dependent][0].dependent_form + "\t" \
                + rev[dependent][0].dependent_lemma + "\t" + rev[dependent][0].dependent_pos + "\t_\t_\t" \
                + str(rev[dependent][0].head) + "\t" + "_" + "\t_\t_"

            # with rel
            # print >> out, str(rev[dependent][0].dependent) + "\t" + rev[dependent][0].dependent_form + "\t" + \
            #   rev[dependent][0].].dependent_lemma + "\t" + rev[dependent][0].].dependent_pos + "\t_\t_\t" + str(rev[dependent][0].].head) + \
            #       "\t" + rev[dependent][0].].rel + "\t_\t_"

        print >> out, ""
        out.close()

    elif mode == "error":
        rev = reverse_head_graph(graph)
        out = open(out_file, "a")
        for dependent in sorted(rev.keys()):
            print >> out, str(rev[dependent][0].dependent) + "\t" + rev[dependent][0].dependent_form + "\t" \
                + rev[dependent][0].dependent_lemma + "\t" + rev[dependent][0].dependent_pos + "\t_\t_\t" \
                + "-1" + "\t" + "__ERROR__" + "\t_\t_"
        print >> out, ""
        out.close()


def check_graph_sanity(predicted_graph, compare_graph={}):  # sanity check on graph
    sane = True
    # check if root exists

    if predicted_graph == {}:
        print "Predicted Graph is empty"
        sane = False

    if cycle(predicted_graph):
        print "Predicted Graph contains cycle."
        sane = False

    root_found = False

    for head in predicted_graph:
        if head == 0:
            root_found = True

            if len(predicted_graph[head]) < 1:
                sane = False
                print "Root has no dependent"
            """
            elif len(predicted_graph[head]) > 1:
                sane = False
                print "Root has more than one dependent"
            """
        elif len(predicted_graph[head]) < 1:
            sane = False
            print "A head has no dependent"
    if not root_found:
        sane = False
        print "No Root node found"

    root_is_dependent = False
    for head in predicted_graph:
        for arc in predicted_graph[head]:
            if arc.dependent == 0:
                root_is_dependent = True
    if root_is_dependent:
        sane = False
        print "root_is_dependent"
    # check if every node is in the predicted graph
    if compare_graph:
        compare_nodes = []
        predicted_nodes = []

        for head in compare_graph:
            if head not in compare_nodes:
                compare_nodes.append(head)
            for arc in compare_graph[head]:
                if arc.dependent not in compare_nodes:
                    compare_nodes.append(arc.dependent)

        for head in predicted_graph:
            if head not in predicted_nodes:
                predicted_nodes.append(head)
            for arc in predicted_graph[head]:
                if arc.dependent not in predicted_nodes:
                    predicted_nodes.append(arc.dependent)
        if sorted(compare_nodes) != sorted(predicted_nodes):
            print sorted(compare_nodes)
            print sorted(predicted_nodes)
            print "Error: Nodes do not match."
            sane = False

            for node in predicted_nodes:
                if node not in compare_nodes:
                    print "predicted has nodes that are not in compare"

    # check if every dependent has only one head
    arcs = {}
    for head in predicted_graph:
        local_dependents = []
        if not predicted_graph[head]:
            print "head has no dependent"
            sane = False
        for arc in predicted_graph[head]:
            if arc.dependent in local_dependents:
                print "Error: A dependent is more than once in a head."
                sane = False
            else:
                local_dependents.append(arc.dependent)
            if arc.dependent in arcs:
                print "A dependent has more than one head."
                sane = False
            else:
                arcs[arc.dependent] = arc
    return sane


def add_sparse_arc(graph, head_id, dependent_id, feat_vec):  # used in complete_graph to add SparseArc objects to graph
    if head_id in graph:
        new_arc = SparseArc(head_id, dependent_id)
        if not feat_vec == []:
            new_arc.feat_vec = feat_vec
        graph[head_id].append(new_arc)
    else:
        new_arc = SparseArc(head_id, dependent_id)
        if not feat_vec == []:
            new_arc.feat_vec = feat_vec
        graph[head_id] = [new_arc]

    return graph


def complete_sparse_graph(graph, feat_map,
                          rev_feat_map):  # completes a graph (every node points to every node, except ROOT)
    complete_g = {}
    dependents = {}
    for head in graph:
        for arc in graph[head]:
            if arc.dependent in dependents:
                print "Error: One dependent has several heads."
            else:
                dependents[arc.dependent] = arc
    for head in graph:
        local_dependents = []
        for arc in graph[head]:
            local_dependents.append(arc.dependent)

            if head in complete_g:
                complete_g[head].append(arc)
            else:
                complete_g[head] = [arc]
        for dependent_id in dependents:
            if dependent_id not in local_dependents and dependent_id != head:
                new_feat_vec = []

                hform = ""
                hpos = ""
                dform = ""
                dpos = ""
                bpos = ""

                # unigram features
                for arc in graph[head]:
                    for feature in arc.feat_vec:
                        if rev_feat_map[feature].startswith("hform:"):
                            hform = rev_feat_map[feature].strip("hform:")
                            if feature not in new_feat_vec:
                                new_feat_vec.append(feature)
                        if rev_feat_map[feature].startswith("hpos:"):
                            hpos = rev_feat_map[feature].strip("hpos:")
                            if feature not in new_feat_vec:
                                new_feat_vec.append(feature)
                for feature in dependents[dependent_id].feat_vec:
                    if rev_feat_map[feature].startswith("dform:"):
                        dform = rev_feat_map[feature].strip("dform:")
                        new_feat_vec.append(feature)
                    if rev_feat_map[feature].startswith("dpos:"):
                        dpos = rev_feat_map[feature].strip("dpos:")
                        new_feat_vec.append(feature)
                    if rev_feat_map[feature].startswith("bpos:"):
                        bpos = rev_feat_map[feature].strip("dpos:")
                        new_feat_vec.append(feature)

                if "hform,dpos:" + hform + "," + dpos in feat_map:
                    new_feat_vec.append(feat_map["hform,dpos:" + hform + "," + dpos])
                if "hpos,dform:" + hpos + "," + dform in feat_map:
                    new_feat_vec.append(feat_map["hpos,dform:" + hpos + "," + dform])
                if "hform,hpos:" + hform + "," + hpos in feat_map:
                    new_feat_vec.append(feat_map["hform,hpos:" + hform + "," + hpos])
                if "dform,dpos:" + dform + "," + dpos in feat_map:
                    new_feat_vec.append(feat_map["dform,dpos:" + dform + "," + dpos])

                # bigram features
                if "hform,hpos,dform,dpos:" + hform + "," + hpos + "," + dform + "," + dpos in feat_map:
                    new_feat_vec.append(
                        feat_map["hform,hpos,dform,dpos:" + hform + "," + hpos + "," + dform + "," + dpos])
                if "hpos,dform,dpos:" + hpos + "," + dform + "," + dpos in feat_map:
                    new_feat_vec.append(feat_map["hpos,dform,dpos:" + hpos + "," + dform + "," + dpos])
                if "hform,dform,dpos:" + hform + "," + dform + "," + dpos in feat_map:
                    new_feat_vec.append(feat_map["hform,dform,dpos:" + hform + "," + dform + "," + dpos])
                if "hform,hpos,dform:" + hform + "," + hpos + "," + dform in feat_map:
                    new_feat_vec.append(feat_map["hform,hpos,dform:" + hform + "," + hpos + "," + dform])
                if "hform,hpos,dpos:" + hform + "," + hpos + "," + dpos in feat_map:
                    new_feat_vec.append(feat_map["hform,hpos,dpos:" + hform + "," + hpos + "," + dpos])
                if "hform,dform:" + hform + "," + dform in feat_map:
                    new_feat_vec.append(feat_map["hform,dform:" + hform + "," + dform])
                if "hpos,dpos:" + hpos + "," + dpos in feat_map:
                    new_feat_vec.append(feat_map["hpos,dpos:" + hpos + "," + dpos])

                # other
                if "hpos,bpos,dpos:" + hpos + "," + bpos + "," + dpos in feat_map:
                    new_feat_vec.append(feat_map["hpos,bpos,dpos:" + hpos + "," + bpos + "," + dpos])
                if "hpos,bpos,dform:" + hpos + "," + bpos + "," + dform in feat_map:
                    new_feat_vec.append(feat_map["hpos,bpos,dpos:" + hpos + "," + bpos + "," + dform])
                if "hform,bpos,dpos:" + hform + "," + bpos + "," + dpos in feat_map:
                    new_feat_vec.append(feat_map["hform,bpos,dpos:" + hform + "," + bpos + "," + dpos])
                if "hform,bpos,dform:" + hform + "," + bpos + "," + dform in feat_map:
                    new_feat_vec.append(feat_map["hform,bpos,dform:" + hform + "," + bpos + "," + dform])

                complete_g = add_sparse_arc(complete_g, head, dependent_id, new_feat_vec)
    return complete_g
