from copy import deepcopy

from token import sentences, Token

class Node:
    def __init__(self, token):
        # A node object contains a Token object (the head) and a list of other 	
        # Token objects (the dependants).
        self.nodeToken = token
        self.edges = []

    def add_edge(self, node):
        self.edges.append(node)

class DepTree:
    def __init__(self, sentence):
        # This is a dictionary of node Objects.
        self.nodes = {
            0: Node(Token("0\tRoot\t__NULL__\t__NULL__\t__NULL__\t__NULL__\t__NULL_\t__NULL__\t__NULL__\t__NULL__"))
            }
        for tid, token in enumerate(sentence):
            self.nodes[tid+1] = Node(token)
        for tid, token1 in enumerate(sentence):
            if int(token1.head) == 0:
                self.nodes[0].add_edge(token1)
            for token2 in sentence:
                if token2.head == token1.id:
                    self.nodes[tid+1].add_edge(token2)

class Instance:
    def __init__(self, sentence, feat_map):
        # An instance object is a graph, represented as a dictionary.
        # This example {node1:{node2:[s, f]}} is a graph with two nodes
        # and one arc from node1 to node 2, with the score s and the feature vector f.
        t = DepTree(sentence)
        self.graph = {}
        self.dep_tree = t

        for node_id in t.nodes.keys():
            if t.nodes[node_id].edges:
                current_token = t.nodes[node_id].nodeToken
                current_token_key = str(current_token.id)+"_"+current_token.form
                self.graph[current_token_key] = {}
                for e in t.nodes[node_id].edges:
                    f = arc_feature_vector(t.nodes[node_id].nodeToken, e, feat_map)
                    self.graph[current_token_key][str(e.id)+"_"+e.form] = [0.0, f]

def arc_feature_vector(h, d, feat_map):
    # returns a feature vector in sparse representation, given the feature map, a head and a dependant
    feat_vec = {}
    if "hform:" + h.form in feat_map: feat_vec[feat_map["hform:" + h.form]] = 1
    if "hpos:" + h.pos in feat_map: feat_vec[feat_map["hpos:" + h.pos]] = 1
    if "dform:" + d.form in feat_map: feat_vec[feat_map["dform:" + d.form]] = 1
    if "dpos:" + d.pos in feat_map: feat_vec[feat_map["dpos:" + d.pos]] = 1
    if "hform,dpos:" + h.form + "," + d.pos in feat_map: feat_vec[feat_map["hform,dpos:" + h.form + "," + d.pos]] = 1
    if "hpos,dform:" + h.pos + "," + d.form in feat_map: feat_vec[feat_map["hpos,dform:" + h.pos + "," + d.form]] = 1

    return feat_vec

def complete_directed_graph(instance, feat_map):
    # converts directed Graph into a complete directed Graph, which means every node is connected to every other node,
    # except no node is connected to itself and root.
    # The new arcs, which are not in the in-tree tree, have the score 0.0 and a feature vector consisting of zeroes.
    graph = instance.graph
    dep_tree = instance.dep_tree
    a = {}
    complete_node_list = set()
    for head in graph:
        complete_node_list.add(head)
        for dependent in graph[head]:
            complete_node_list.add(dependent)
    if len(complete_node_list) > 2:
        for node in complete_node_list:
            a[node] = {}
            for node2 in complete_node_list:
                if not (node2 == node or node2 == "0_Root"):

                    node_pos = dep_tree.nodes[int(node.split("_")[0])].nodeToken.pos
                    node_form = node.split("_")[1]
                    node2_pos = dep_tree.nodes[int(node2.split("_")[0])].nodeToken.pos
                    node2_form = node2.split("_")[1]

                    a[node][node2] = [0.0, {}]

                    features = [
                        "hform:" + node_form,
                        "hpos:" + node_pos,
                        "dform:" + node2_form,
                        "dpos:" + node2_pos,
                        "hform,dpos:" + node_form + "," + node2_pos,
                        "hpos,dform:" + node_pos + "," + node2_form

                    ]

                    for feature in features:
                        if feature in feat_map:
                            a[node][node2][1][feat_map[feature]] = 1

    elif len(complete_node_list) == 2:
        for node in complete_node_list:
            if node == "0_Root":
                a[node] = {}
                for node2 in complete_node_list:
                    if not node2 == "0_Root":

                        node_pos = dep_tree.nodes[int(node.split("_")[0])].nodeToken.pos
                        node_form = node.split("_")[1]
                        node2_pos = dep_tree.nodes[int(node2.split("_")[0])].nodeToken.pos
                        node2_form = node2.split("_")[1]

                        a[node][node2] = [0.0, {}]

                        features = [
                            "hform:" + node_form,
                            "hpos:" + node_pos,
                            "dform:" + node2_form,
                            "dpos:" + node2_pos,
                            "hform,dpos:" + node_form + "," + node2_pos,
                            "hpos,dform:" + node_pos + "," + node2_form

                        ]

                        for feature in features:
                            if feature in feat_map:
                                a[node][node2][1][feat_map[feature]] = 1
    else:
        print "Error: Not enough nodes."

    return a

def give_cycle(graph, node, visited, cycles):
    # change format to dict where you can always see the head
    c = []
    if cycles is not None:
        c = cycles
    v = []
    if visited is not None:
        v = visited
    for head in graph.keys():
        if head == node:
            v.append(head)
            for dependent in graph[head].keys():
                if dependent not in v:
                    c = deepcopy(give_cycle(graph, dependent, v, c))
                else:
                    for node in visited[visited.index(dependent):]:
                        c.append(node)
                    return c
                if c:
                    return c
            if c:
                return c
        if c:
            return c
    return c

def delete_key(in_dict, key):
    to_convert_dict = deepcopy(in_dict)
    del to_convert_dict[key]
    return to_convert_dict

def remove_cycle(graph, cycle_nodes):  # incomplete
    g = deepcopy(graph)
    for n_id, node in enumerate(cycle_nodes):
        print n_id
        if node == cycle_nodes[-1]:
            g[node] = delete_key(g[node], cycle_nodes[0])
            if not g[node].keys():
                g = delete_key(g, node)
        else:
            g[node] = delete_key(g[node], cycle_nodes[n_id+1])
            if not g[node].keys():
                g = delete_key(g, node)
    return g

def highest_incoming_heads(graph):
    # graph2 is the graph with every dependent only have their head with the highest score
    d = {}
    for head in graph:
        for arc in graph[head]:
            if arc in d:
                if graph[head][arc][0] > d[arc][1][0]:
                    d[arc] = [head, [graph[head][arc][0], graph[head][arc][1]]]
            else:
                d[arc] = [head, [graph[head][arc][0], graph[head][arc][1]]]

    graph2 = {}
    for dependent in d:
        if d[dependent][0] in graph2:
            graph2[d[dependent][0]][dependent] = d[dependent][1]
        else:
            graph2[d[dependent][0]] = {dependent: d[dependent][1]}
    return graph2

def graph_sanity_check(graph):
    sane = True
    for head in graph:
        if not graph[head].keys():
            print "Head has no dependents."
            sane = False
        else:
            for dependent in graph[head]:
                if "Root" in dependent:
                    print "Root is a dependent."
                    sane = False
    if not sane:
        print "Graph didn't pass sanity check."
        print graph
    return sane
