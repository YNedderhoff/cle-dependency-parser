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

class SparseArc:
    def __init__(self, nodeToken):
        self.head = int(nodeToken.head)
        self.dependent = int(nodeToken.id)
        self.score = 0.0
        self.feat_vec = []

        self.is_cycle = False
        self.former_dependent = None

class SparseGraph:
    def __init__(self, nodes):
        self.heads = {}
        for node in nodes:
            if not nodes[node].nodeToken.head == '__NULL_':
                if int(nodes[node].nodeToken.head) in self.heads:
                    self.heads[int(nodes[node].nodeToken.head)].append(SparseArc(nodes[node].nodeToken))
                else:
                    self.heads[int(nodes[node].nodeToken.head)] = [SparseArc(nodes[node].nodeToken)]


class FullArc:
    def __init__(self, nodeToken):
        self.head = int(nodeToken.head)
        self.dependent = int(nodeToken.id)
        self.score = 0.0
        self.feat_vec = []

        self.head_form = "__NULL__"
        self.dependent_form = nodeToken.form
        self.head_pos = "__NULL__"
        self.dependent_pos = nodeToken.pos

        self.is_cycle = False
        self.former_dependent = None

class FullGraph:
    def __init__(self, nodes):
        self.heads = {}
        for node in nodes:
            if not nodes[node].nodeToken.head == '__NULL_':
                if int(nodes[node].nodeToken.head) in self.heads:
                    self.heads[int(nodes[node].nodeToken.head)].append(FullArc(nodes[node].nodeToken))
                else:
                    self.heads[int(nodes[node].nodeToken.head)] = [FullArc(nodes[node].nodeToken)]

        # filling the fields head_form and head_pos
        for head in self.heads:
            for arc in self.heads[head]:
                for head2 in self.heads:
                    for arc2 in self.heads[head2]:
                        if arc2.dependent == head:
                            arc.head_form = arc2.dependent_form
                            arc.head_pos = arc2.dependent_pos

def add_sparse_arc(graph, head_id, feat_vec, dependent_token):

    if head_id in graph:
        new_arc = SparseArc(dependent_token)
        if not feat_vec == []:
            new_arc.feat_vec = feat_vec
        graph[head_id].append(new_arc)
    else:
        new_arc = SparseArc(dependent_token)
        if not feat_vec == []:
            new_arc.feat_vec = feat_vec
        graph[head_id] = [new_arc]

    return graph

def complete_graph(graph, feat_map, rev_feat_map):
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

                for feature in arc.feat_vec:
                    if rev_feat_map[feature].startswith("hform:"):
                        hform = rev_feat_map[feature].strip("hform:")
                        new_feat_vec.append(feature)
                    if rev_feat_map[feature].startswith("hpos:"):
                        hpos = rev_feat_map[feature].strip("hpos:")
                        new_feat_vec.append(feature)
                for feature in dependents[dependent_id].feat_vec:
                    if rev_feat_map[feature].startswith("dform:"):
                        dform = rev_feat_map[feature].strip("dform:")
                        new_feat_vec.append(feature)
                    if rev_feat_map[feature].startswith("dpos:"):
                        dpos = rev_feat_map[feature].strip("dpos:")
                        new_feat_vec.append(feature)
                if "hform,dpos:"+hform+","+dpos in feat_map:
                    new_feat_vec.append(feat_map["hform,dpos:"+hform+","+dpos])
                if "hpos,dform:"+hpos+","+dform in feat_map:
                    new_feat_vec.append(feat_map["hpos,dform:"+hpos+","+dform])
                complete_g = add_sparse_arc(complete_g, head, new_feat_vec, Token(str(dependent_id) + "\t_\t_\t_\t_\t_\t" + str(head) + "\t_\t_\t_"))

    return complete_g


def reverse_head_graph(graph):
    new_graph = {}
    for h_id in graph:
        for arc in graph[h_id]:
            if arc.dependent in new_graph:
                new_graph[arc.dependent].append(arc)
            else:
                new_graph[arc.dependent] = [arc]
    return new_graph


def reverse_dep_graph(graph):
    new_graph = {}
    for d_id in graph:
        for arc in graph[d_id]:
            if arc.head in new_graph:
                new_graph[arc.head].append(arc)
            else:
                new_graph[arc.head] = [arc]
    return new_graph

def highest_scoring_heads(graph):
    rev_graph = reverse_head_graph(graph)
    highest = {}

    for dependent in rev_graph:
        for arc in rev_graph[dependent]:
            if dependent in highest:
                if arc.score > highest[dependent][0].score:
                    highest[dependent] = [arc]
            else:
                highest[dependent] = [arc]
    return reverse_dep_graph(highest)

def cycle(graph, visited, n): # n is next to visit
    c = []
    v = visited
    for h_id in graph:
        if h_id == n:
            v.append(h_id)
            for arc in graph[h_id]:
                if arc.dependent in v:
                    c = v[v.index(arc.dependent):]
                else:
                    if arc.dependent in graph:
                        c = cycle(graph, v, arc.dependent)
                if c:
                    return c
            if c:
                return c
        if c:
            return c
    return c
