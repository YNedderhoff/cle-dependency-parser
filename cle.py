# !/bin/python
#  -*- coding: utf-8 -*-

import sys
import time
import numpy as np
import cPickle
import gzip
from copy import deepcopy


from modules.graph import complete_directed_graph, create_instances, graph_sanity_check
from modules.featmap import fm

# save the model (weight vectors) to a file:
def save(file_name, model):
    stream = gzip.open(file_name, "wb")
    cPickle.dump(model, stream)
    stream.close()

# load the model (weight vectors) from a file:

def load(file_name):
    stream = gzip.open(file_name, "rb")
    model = cPickle.load(stream)
    stream.close()
    return model


def expand_feature_vector(sparse_feature_vector, feature_count):
    # convert sparse representation of feature vector to full feature vector
    feat_vec = np.zeros(shape=(feature_count, 1))
    for f_index in sparse_feature_vector.keys():
        feat_vec[f_index] = [sparse_feature_vector[f_index]]
    return feat_vec


def create_weight_vector(l):
    # returns lx1 vector, filled with zeroes
    # w = np.ones(shape=(l,1))
    # w = np.zeros(shape=(l,1))
    #w = np.empty(shape=(l, 1))
    w = []
    for i in range(l):
        w.append(0.5)

    return w


def score_arcs(graph, w):  # f= feature vector, w = weight vector
    g = deepcopy(graph)
    # the score function for Arcs, the dot product of weight vector and feature vector
    score = 0
    for head in g:
        for dependent in g[head]:
            for dimension in g[head][dependent][1]:
                score = dimension * w[dimension]
            g[head][dependent][0] = score
    return g


def cycle(graph, visited=[]):
    # doesn't find cycles with more than two nodes, have to change that
    for node in graph.keys():
        for arc in graph[node].keys():
            if arc in graph.keys():
                if node in graph[arc].keys():
                    return True
                else:
                    return False
            else:
                return False


def give_cycle(graph, node, visited, cycles):
    # change format to dict where you can always see the head
    c = []
    if not cycles is None:
        c = cycles
    v = []
    if not visited is None:
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

def sum_of_arc_feature_vectors(graph, l):

    sum_of_feat_vecs = []
    for i in range(l):
        sum_of_feat_vecs.append(0)
    for head in graph:
        for dependent in graph[head]:
            for feature in graph[head][dependent][1]:
                sum_of_feat_vecs[feature] += 1
    return sum_of_feat_vecs

def structured_perceptron(ins, weight_vector, epochs):  # training
    # w[-1]=[3.57]
    # print np.vdot(v, w)
    w = deepcopy(weight_vector)
    print >> sys.stderr, "Start training ..."
    for epoch in range(1, epochs):
        print >> sys.stderr, "\tEpoch: " + str(epoch)
        print >> sys.stderr, "\t\tCurrent weight vector:"
        print >> sys.stderr, "\t\t\t"+str(w)
        total = 0
        correct = 0
        instances = 0
        for instance in ins.keys():
            instances += 1
            y_gold = ins[instance][1].graph  # the correct tree
            if not graph_sanity_check(y_gold): print "Gold"

            g = complete_directed_graph(ins[instance][1].graph)  # the complete directed graph
            if not graph_sanity_check(g): print "Complete"

            g_scored = score_arcs(g, w)
            if not graph_sanity_check(g_scored): print "Scored Complete"

            y_predicted = chu_liu_edmonds(g_scored)
            if not graph_sanity_check(y_predicted): print "Predicted"

            # print y_gold
            # print y_predicted

            if not y_gold == y_predicted:
                tmp1 = sum_of_arc_feature_vectors(y_gold, len(w))
                tmp2 = sum_of_arc_feature_vectors(y_predicted, len(w))
                tmp3 = []
                for i in range(len(w)):
                    tmp3.append(tmp1[i]-tmp2[i])
                tmp4 = []
                for i in range(len(w)):
                    tmp4.append(tmp3[i]*0.5)
                    
                w_new = []
                for i in range(len(w)):
                    w_new.append(w[i]+tmp4[i])

                w = w_new

            else: correct+=1
            total += 1
            if total % 500 == 0:
                print >> sys.stderr, "\t\tInstance Nr. " + str(total)
        print total, correct
    return w


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
                if c[n_id+1] == to_remove_dependent:
                    print "This is impossible (cle)"
                else:
                    if node in g_c:
                        if n_id == len(c)-1:
                            g_c[node][c[0]] = [0.0, {}]
                        else:
                            g_c[node][c[n_id+1]] = [0.0, {}]
                    else:
                        if n_id == len(c)-1:
                            g_c[node] = {c[n_id+1], [0.0, {}]}
                        else:
                            g_c[node] = {c[n_id+1], [0.0, {}]}

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
        if n_id == len(c)-1:
            t_c += node
        else:
            t_c += node+"-"
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
        if n_id == len(c)-1:
            score_c += g_a[node][c[0]][0]
        else:
            score_c += g_a[node][c[n_id+1]][0]
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


def run(args):
    #outstream = open(args.outputfile, 'w')

    # feat map is a dictionary with every existing feature in the training data as keys,
    # and unique indexes as values. Example: u'hpos,dform:VBD,way': 3781

    start = time.time()
    print >> sys.stderr, "Creating feature map..."

    feat_map = fm(args.inputfile)

    stop = time.time()
    print >> sys.stderr, "\tNumber of features: " + str(len(feat_map))
    print >> sys.stderr, "\tDone, " + str(stop - start) + " sec"

    # instances is a dictionary, containing a index as a key and a list,
    # containing a sentence string and a Instance object.

    start = time.time()
    print >> sys.stderr, "Creating instances..."

    instances = create_instances(args.inputfile, feat_map)

    stop = time.time()
    print >> sys.stderr, "\tDone, " + str(stop - start) + " sec"

    # print all sentences and their feature vector sparse representations:
    """
    for sentence_id in instances.keys():
        print sentence_id+1
        print instances[sentence_id][0]
        print instances[sentence_id][1].G
        #print featvec[sentence_id]
    """
    w = structured_perceptron(instances, create_weight_vector(len(feat_map)), 10)

    save("model", [feat_map, w])

    # print np.vdot(w, a)
    #outstream.close()


def write_to_file(token, file_obj):
    print >> file_obj, str(token.id) + "\t" + str(token.form) + "\t" + str(token.lemma) + "\t" + str(
        token.pos) + "\t" + "_" + "\t" + "_" + "\t" + str(token.head) + "\t" + str(token.rel) + "\t" + "_" + "\t" + "_"


def run_tests():
    # test graph beinhaltet einen cycle
    test_graph = {
        "0_Root": {
            "1_was": "x",
            "5_has": "y"
        },
        "1_was": {
            "2_is": "x",
            "6_bidde": "y"
        },
        "2_is": {
            "3_los": "x",
            "6_bidde": "y"
        },
        "3_los": {
            "3_was": "x",
            "1_is": "y",
            "4_ahja": "rofl"
        },
        "4_ahja": {
            "1_was": "x"
        }
    }


    if graph_sanity_check(test_graph):
        print "Graph passed sanity check."
    c = give_cycle(test_graph, "0_Root", [], [])
    print c
    new = remove_cycle(test_graph, c)
    print test_graph
    print new

    """
    a = complete_directed_graph(test_graph)
    c = give_cycle(a, "0_Root", [], [])
    print c
    b = highest_incoming_heads(score_arcs(a))
    c = give_cycle(b, "0_Root", [], [])
    print c
    """


if __name__ == '__main__':
    import argparse

    arg_par = argparse.ArgumentParser(description='')

    arg_par.add_argument('-i', '--input', dest='inputfile', help='input file', required=True)
    arg_par.add_argument('-o', '--output', dest='outputfile', help='output file', required=True)
    arguments = arg_par.parse_args()

    #run_tests()
    run(arguments)
