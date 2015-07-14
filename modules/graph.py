from token import sentences, Token
import codecs

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
    def __init__(self, t, feat_map):
        # An instance object is a graph, represented as a dictionary.
        # This example {node1:{node2:[s, f]}} is a graph with two nodes
        # and one arc from node1 to node 2, with the score s and the feature vector f.

        self.graph = {}

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
    feat_vec = {
        feat_map["hform:" + h.form]: 1,
        feat_map["hpos:" + h.pos]: 1,
        feat_map["dform:" + d.form]: 1,
        feat_map["dpos:" + d.pos]: 1,
        feat_map["hform,dpos:" + h.form + "," + d.pos]: 1,
        feat_map["hpos,dform:" + h.pos + "," + d.form]: 1
        }
    return feat_vec

def complete_directed_graph(ins):
    # converts directed Graph into a complete directed Graph, which means every node is connected to every other node,
    # except no node is connected to itself and root.
    # The new arcs, which are not in the in-tree tree, have the score 0.0 and a feature vector consisting of zeroes.

    a = {}
    complete_node_list = set()
    for head in ins:
        complete_node_list.add(head)
        for dependent in ins[head]:
            complete_node_list.add(dependent)
    if len(complete_node_list) > 2:
        for node in complete_node_list:
            a[node] = {}
            for node2 in complete_node_list:
                if not (node2 == node or node2 == "0_Root"):
                    if node in ins.keys():
                        if node2 in ins[node].keys():
                            a[node][node2] = ins[node][node2]
                    else:
                        a[node][node2] = [0.0, {}]
    elif len(complete_node_list) == 2:
        for node in complete_node_list:
            if node == "0_Root":
                a[node] = {}
                for node2 in complete_node_list:
                    if not node2 == "0_Root":
                        a[node][node2] = ins[node][node2]
    else:
        print "Error: Not enough nodes."

    """
    for v in ins:
        a[v] = {}
        for v2 in ins[v].keys():
            if not (v2 == v or v2 == "0_Root"):
                if v2 in ins[v].keys():
                    a[v][v2] = ins[v][v2]
                else:
                    a[v][v2] = [0.0, {}]
    """
    return a

def create_instances(infile, featmap):
    # creates a dictionary with numbers as keys and Instances in the Format (sentence, Instance object)
    # as values
    ins = {}
    s_count = 0
    for sentence in sentences(codecs.open(infile, encoding='utf-8')):
        s = ""
        for token in sentence:
            s += token.form+" "
        ins[s_count] = [s.rstrip(), Instance(DepTree(sentence), featmap)]
        s_count += 1
    return ins

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
