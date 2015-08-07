from featmap import give_features, give_distance, give_direction, give_surrounding_information
import codecs


class Arc:
    def __init__(self, mode="sparse", head=None, dependent=None, head_form=None, dependent_form=None, head_lemma=None,
                 dependent_lemma=None, head_pos=None, dependent_pos=None, s=0.0):
        self.head = head
        self.dependent = dependent
        self.score = s
        self.feat_vec = []

        self.former_head = None
        self.former_dependent = None

        if mode == "full":
            self.head_form = head_form
            self.dependent_form = dependent_form

            self.head_lemma = head_lemma
            self.dependent_lemma = dependent_lemma

            self.head_pos = head_pos
            self.dependent_pos = dependent_pos


class ManualSparseGraph:  # heads has the same structure as in the other graph classes, but for addition of arcs
    def __init__(self):
        self.heads = {}

    def add_arc(self, head, arc):
        try:
            self.heads[head].append(arc)
        except KeyError:
            self.heads[head] = [arc]


class Graph:  # sparse representation of a graph (keys: heads, values: SparseArc objects)
    def __init__(self, tokens, mode="sparse", feat_map=None, weight_vector=None):

        self.heads = {0: []}

        # In every possible mode (sparse, complete-sparse, full, complete-full) at first the arcs with ROOT head are
        # added, then every other arc. Every arc, except ones in the  full graph, gets a sparse feature vector based
        # on feat_map. The completed graphs also get a score per arc (based on the features and the weight vector).

        # normal graph
        if mode == "sparse":
            for token1 in tokens:

                # add arc from root to it's dependent

                if token1.head == 0:
                    direction = "left"
                    distance = give_distance(0, token1.id, direction)
                    hrform = hrpos = hlform = hlpos = drform = drpos = dlform = dlpos = "__NULL__"
                    new_arc = Arc("sparse", 0, token1.id)
                    if feat_map is not None:
                        new_arc.feat_vec = [f for f in (feat_map[feature] for feature in
                                                        give_features("__ROOT__", "__ROOT__", "__ROOT__", token1.form,
                                                                      token1.lemma, token1.pos, hrform, hrpos, hlform,
                                                                      hlpos, drform, drpos, dlform, dlpos, direction,
                                                                      distance) if feature in feat_map)]
                    self.heads[0].append(new_arc)

                # add every other arc

                dependents = []
                for token2 in (token2 for token2 in tokens if token2.head == token1.id):
                    direction = give_direction(token1.id, token2.id)
                    distance = give_distance(token1.id, token2.id, direction)
                    hrform, hrpos, hlform, hlpos, drform, drpos, dlform, dlpos = give_surrounding_information(tokens,
                                                                                                              token1.id,
                                                                                                              token2.id)

                    new_arc = Arc("sparse", token1.id, token2.id)
                    if feat_map is not None:
                        new_arc.feat_vec = [f for f in (feat_map[feature] for feature in
                                                        give_features(token1.form, token1.lemma, token1.pos,
                                                                      token2.form, token2.lemma, token2.pos, hrform,
                                                                      hrpos, hlform, hlpos, drform, drpos, dlform,
                                                                      dlpos, direction, distance) if
                                                        feature in feat_map)]
                    dependents.append(new_arc)
                if dependents:
                    self.heads[token1.id] = dependents

        # completed graph
        elif mode in ["complete-sparse", "complete-full"]:
            for token1 in tokens:

                # add arcs from root to every node

                direction = "left"
                distance = give_distance(0, token1.id, direction)
                hrform = hrpos = hlform = hlpos = drform = drpos = dlform = dlpos = "__NULL__"

                if mode == "complete-sparse":
                    new_arc = Arc("sparse", 0, token1.id)
                else:
                    new_arc = Arc("full", 0, token1.id, "__ROOT__", token1.form, "__ROOT__", token1.lemma, "__ROOT__",
                                  token1.pos)

                new_arc.feat_vec = [f for f in (feat_map[feature] for feature in
                                                give_features("__ROOT__", "__ROOT__", "__ROOT__", token1.form,
                                                              token1.lemma, token1.pos, hrform, hrpos, hlform, hlpos,
                                                              drform, drpos, dlform, dlpos, direction, distance) if
                                                feature in feat_map)]
                for feature in new_arc.feat_vec:
                    new_arc.score += weight_vector[feature]
                self.heads[0].append(new_arc)

                # add every other arc

                dependents = []
                for token2 in (token2 for token2 in tokens if token2.id != token1.id):

                    direction = give_direction(token1.id, token2.id)
                    distance = give_distance(token1.id, token2.id, direction)
                    hrform, hrpos, hlform, hlpos, drform, drpos, dlform, dlpos = give_surrounding_information(tokens,
                                                                                                              token1.id,
                                                                                                              token2.id)

                    if mode == "complete-sparse":
                        new_arc = Arc("sparse", token1.id, token2.id)
                    else:
                        new_arc = Arc("full", token1.id, token2.id, token1.form, token2.form, token1.lemma,
                                      token2.lemma, token1.pos, token2.pos)

                    new_arc.feat_vec = [f for f in (feat_map[feature] for feature in
                                                    give_features(token1.form, token1.lemma, token1.pos, token2.form,
                                                                  token2.lemma, token2.pos, hrform, hrpos, hlform,
                                                                  hlpos, drform, drpos, dlform, dlpos, direction,
                                                                  distance) if feature in feat_map)]
                    for feature in new_arc.feat_vec:
                        new_arc.score += weight_vector[feature]
                    dependents.append(new_arc)
                if dependents:
                    self.heads[token1.id] = dependents
        else:
            print "Unknown Graph mode."


def reverse_head_graph(graph):  # reverses a normal graph to a graph where the dependents are the keys
    new_graph = {}
    for h_id in graph:
        for arc in graph[h_id]:
            try:
                new_graph[arc.dependent].append(arc)
            except KeyError:
                new_graph[arc.dependent] = [arc]
    return new_graph


def reverse_dep_graph(graph):  # opposite of reverse_head_graph
    new_graph = {}
    for d_id in graph:
        for arc in graph[d_id]:
            try:
                new_graph[arc.head].append(arc)
            except KeyError:
                new_graph[arc.head] = [arc]
    return new_graph


def highest_scoring_heads(graph):  # returns a graph where every dependent only has it's highest scoring head
    rev_graph = reverse_head_graph(graph)
    highest = {}
    for dependent in rev_graph:
        for arc in rev_graph[dependent]:
            try:
                if arc.score > highest[dependent][0].score:
                    highest[dependent] = [arc]
                if arc.score == highest[dependent][0].score:
                    if arc.dependent < highest[dependent][0].dependent:
                        highest[dependent] = [arc]
            except KeyError:
                highest[dependent] = [arc]
    return reverse_dep_graph(highest)


def cycle_per_head(graph, v, n):
    c = []
    v.append(n)
    for arc in graph[n]:
        if arc.dependent == v[0]:
            c = v
            return c
        elif arc.dependent not in v:
            if arc.dependent in graph:
                c = cycle_per_head(graph, [x for x in v], arc.dependent)
                if c:
                    return c
    return c


def cycle(graph):  # returns a cycle if found by cycle_per_head, else []

    for head in sorted(graph):
        visited = []
        cy = cycle_per_head(graph, visited, head)
        if cy:
            return cy
    return []


def make_graph_compareable(graph):  # returns a simplified graph representation {head:[node1, node2 ...]}
    graph_dict = {}
    for head in sorted(graph):
        graph_dict[head] = sorted([arc.dependent for arc in graph[head]])
    return graph_dict


def write_graph_to_file(graph, out_file, mode="normal"):  # write a graph to file in conll06 format
    if mode == "normal":

        rev = reverse_head_graph(graph)
        with codecs.open(out_file, "a", "utf-8") as out:
            for dependent in sorted(rev):
                # without rel
                print >> out, u"{0}\t{1}\t{2}\t{3}\t_\t_\t{4}\t_\t_\t_".format(
                    rev[dependent][0].dependent,
                    rev[dependent][0].dependent_form,
                    rev[dependent][0].dependent_lemma,
                    rev[dependent][0].dependent_pos,
                    rev[dependent][0].head
                )
            print >> out, ""

    elif mode == "error":
        rev = reverse_head_graph(graph)
        with codecs.open(out_file, "a", "utf-8") as out:
            for dependent in sorted(rev):
                print >> out, u"{0}\t{1}\t{2}\t{3}\t_\t_\t-1\t_\t_\t_".format(
                    rev[dependent][0].dependent,
                    rev[dependent][0].dependent_form,
                    rev[dependent][0].dependent_lemma,
                    rev[dependent][0].dependent_pos,
                )
            print >> out, ""


def check_graph_sanity(predicted_graph, compare_graph):  # sanity check on graph
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

            if not predicted_graph[head]:
                sane = False
                print "Root has no dependent"

        elif not predicted_graph[head]:
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
